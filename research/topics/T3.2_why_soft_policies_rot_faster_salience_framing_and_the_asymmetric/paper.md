# Why Soft Policies Rot Faster: Salience, Framing, and the Asymmetric Decay of In-Context Constraints — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1–C4, M1–M6, CO1–CO4, RQ1, RQ_INF_1/2, t1–t6) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** The behavioral half-life of an in-context constraint is not a function of its occupancy of the context window — token-matched soft-policy and hard-safety-norm statements decay at rates reported to differ ~8x — but of how the constraint's persistence is loaded across three physically distinct carriers: attentional salience of its placement, framing strength of its wording, and weight-level redundancy from alignment training.

**判据 (deletion test).** Delete the domain nouns:

> "The half-life of a ___ is not a function of its occupancy of the ___ but of how its persistence is loaded across ___ carriers: ___, ___, and ___."

With the nouns gone there is no proposition left to evaluate — the sentence asserts nothing checkable and cannot even be false. The claim's entire content lives in the specific carriers (context-window salience vs. wording strength vs. alignment-prior redundancy) and in the specific dissociation (occupancy ≠ persistence). It is therefore an asymmetry claim, not a bridge: no two fields are being "connected"; one confounded quantity (constraint durability) is being split into separable causes.

## Step 2 — Archetype

**Primary: `empirical` (mechanism-attribution study)** — consistent with digest N12: the headline is a measurement finding (variance shares of the decay gap; half-life contrasts), with the apparatus (M1–M3 suite) instrumental, exactly as N12's exemplars ([LLMsGetLost], [SafetyFewTokensDeep]).
**Secondary: `technical_artifact` / `dataset`** — CO1/CO3, the matched constraint-pair bank + reactivity-controlled probe environment, released as the reusable instrument.

Downstream consequences:
- **(a) Abstract contribution slot:** a quantified attribution — "salience+framing absorb X% of the soft/hard decay-rate gap; the prior-linked residual is Y%" — not a system, not a benchmark score, not a SOTA delta.
- **(b) Intro logic:** "what becomes possible": once the gap is decomposed, mitigation stops being guesswork — if salience/framing dominate, placement/wording fixes are sufficient; if the prior dominates, durable soft policies provably require training-time reinforcement (digest MotivationItem 3, CO4). The intro argues for *decidability of the mitigation route*, not for beating a number.
- **(c) Evidence standard for Results:** pre-registered factorial intervention with hard-coded pass criteria, effect directions with CIs, dominance/partial-R² decomposition, all cells reported (digest t5). A significant p-value alone does not meet the standard; the standard is the binary criteria in Step 6.

## Step 3 — Taste self-audit

| Check | Verdict | Note |
|---|---|---|
| Is the opportunity a Bridge? | **PASS** | The opportunity is an unexplained asymmetry within one phenomenon (constraint decay), not "field A meets field B". Step 0's deletion test confirms. |
| Is the method mere Synthesis? | **RISK, fixed** | Naive framing — "we combine PrefEval's padding, TimeToInconsistency's survival modeling, and RECAST's verifiers" — is synthesis. Corrected skeleton: the load-bearing move is **orthogonalization of a naturally confounded triple** (C1: in the wild, hard norms are simultaneously imperative, prominent, and RLHF-backed) via intervention on content-matched pairs. The borrowed components are commodity instrumentation; the contribution is the causal isolation design + the attribution result. All framing below uses this skeleton. |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS after fix** | Load-bearing verbs pre-committed: *isolate, decompose, attribute, intervene, measure, gate, falsify*. "Combine/leverage/unify" banned from abstract and intro claims. |
| Abstract-opening rule | **ENFORCED** | Abstract v0 (below) opens with the confound/asymmetry mechanism; the "X is increasingly used… however… we introduce" template is not used. |

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4).** The quantity of interest is the soft/hard `type×turn` hazard-gap coefficient `β_{τ×turn}` and its dominance/partial-R² decomposition across three factor blocks (wording, position×repetition, prior-proxy); the unit of analysis is one content-matched soft/hard constraint pair evaluated within one long-horizon conversation cell; the reference population is LLM agents governed by system-prompt-injected soft organizational policies and hard safety norms, sampled across ≥3 model families (Stage 2) including one open-weights base/instruct pair; the decision it feeds is binary and stated in the abstract: whether durable soft-policy compliance is achievable via a placement/wording change available to any policy author today, or requires training-time reinforcement (digest MotivationItem 3, CO4).

**Notation.** A constraint `c` has type `τ(c) ∈ {soft, hard}`, wording variant `w(c) ∈ {advisory, standard, imperative}`, position `p ∈ {sys-head, sys-tail, mid-turn-10}`, repetition `r ∈ {1, 3, 5}`. A conversation runs turns `t = 1…T` (pilot `T=30`) with probes at scheduled turns. Probe outcome `A_c(t) ∈ {0,1}` (verifier pass). Event = first *sustained* violation (2 consecutive failed probes); violation-free conversations right-censored. Discrete-time hazard `h(t | τ, w, p, r)` fitted by the M4 mixed-effects cloglog model: `hazard ~ turn × τ × w × p × r + (1|pair) + (1|model)`.

**Every load-bearing adjective/verb → computable quantity** (from digest Claims + N8 metrics):

| Term | Formal definition | Measured by |
|---|---|---|
| "decays" / "rots" | fitted hazard `h(t) > 0` with survival `S(t)` strictly decreasing | M4 fit on probe outcomes |
| "faster" (8x premise) | soft/hard hazard ratio `G = exp(β_{τ×turn}) > 1`; half-life `t½ = min{t : Ŝ(t) ≤ 0.5·Ŝ(t₁)}` | `G` with 95% CI; `t½(hard)/t½(soft)` |
| "asymmetric" | `G ≠ 1` after content matching (see "matched") | CI of `G` excludes 1 |
| "salient" | manipulated cell value of `(p, r)`; salience effect = `β_{p×τ×turn}`, `β_{r×τ×turn}` | M2 controller, M4 coefficients |
| "framing / strongly-worded" | variant class `w`, valid iff embedding-sim(variants) ≥ 0.90 AND human semantic-equivalence audit pass | M1 manipulation check (t2) |
| "prior-backed" | proxy vector `π(c) = (π₁: no-injection compliance rate; π₂: instruct−base compliance delta; π₃: per-token KL on violating continuation, open weights)` | M5 battery, entered as covariates |
| "drives / dominates" (mechanism attribution) | mechanism share = dominance weight / partial-R² of the factor block in `β_{τ×turn}` | M4 dominance analysis |
| "matched" (pair) | decision procedure: same topic domain ∧ token-length diff ≤ 10% ∧ same verifier class ∧ turn-1 adherence diff ≤ 5 pts (pilot-checked) | M1 bank audit |
| "reactive" (probing) | `Δ_react` = log hazard-ratio, within- vs between-conversation probing at matched turns | M6 calibration arm |
| "valid" (verifier) | Cohen's κ (judge vs human) ≥ 0.8 on 10% audit sample; rule-based verifiers exact by construction | M3/RECAST-style dual-mode check |
| "closes the gap" | fraction of log-half-life gap recovered: `κ_close = [log t½(boosted-soft) − log t½(std-soft)] / [log t½(std-hard) − log t½(std-soft)]` | RQ_INF_1 contrast |

Deleted adjectives (no computable referent → banned from claims): "silently", "invisible", "realistic" (distractors are *sourced from LMSYS-Chat-1M*, stated as provenance, not as an adjective claim).

## Assumptions (A1–A8)

Each assumption fills all five guidance.md §3.2 slots; "Gate" names the concrete pre-scale checkpoint (PG-\* where it runs inside the walking skeleton/pilot) and "Consequence" states what happens to which claim/hypothesis if the assumption fails, kept separate from "Detection" so the checkpoint and its downstream effect are independently auditable (Phase A checklist item 5).

| id | Assumption | Failure mode | Detection | Gate | Consequence |
|---|---|---|---|---|---|
| A1 | The soft/hard decay gap replicates directionally (`G > 1`) in content-matched pairs. | The reported ~8x gap is an artifact of unmatched banks in the source report. | Walking-skeleton criterion S-b (KM curves ordered soft < hard, turn-30 gap ≥10pts). | **PG-1** (walking skeleton, Step 9). | Fails → global pivot F-G1 fires; no H\* is scored from an invalid premise. |
| A2 | Content-matched pairs are constructible: soft and hard constraints matched on topic, length, verifier class, and turn-1 adherence. | Soft constraints are intrinsically harder → type contrast becomes difficulty contrast (C3, t1/t2). | Matched-pair audit (Step 5 "matched" procedure): pairs failing turn-1-adherence match ≤5 pts. | **PG-2** (Stage-1 pilot bank audit, pre-scale). | >50% of pairs dropped → redesign bank before Stage 1; scale-up blocked until re-audited. |
| A3 | Wording variants are semantically equivalent (framing manipulation is pure). | Imperative rewrites change specificity/content (t2). | M1 check: embedding-sim ≥ 0.90 + human equivalence audit. | **PG-3** (M1 construction, pre-scale). | Failing pairs dropped, counts reported; H1's framing-factor estimate is restricted to the surviving pairs, scope noted in Limitations. |
| A4 | Probe reactivity is measurable and type-uniform (C2). | Probes refresh salience differentially by type → all within-conversation curves biased. | M6 within- vs. between-conversation calibration contrast (H3/E3). | **PG-4**, run FIRST — gates E1/E2 (digest N9 Result-3). | Type-dependent reactivity → H3 fails; E1/E2 rerun on the between-conversation subsample only, claim scope narrowed (E3 fallback). |
| A5 | Prior-strength proxies carry signal: `π₁, π₂` vary across constraints and correlate positively. | Proxies are flat or mutually contradictory → third mechanism uninstrumented (C4). | Pilot check: sd(π₁) > 0.1 and Spearman ρ(π₁,π₂) > 0.3. | **PG-5** (Stage-1 pilot, pre-scale). | Check fails → prior share reported as "unidentified"; CO4's training-route clause withdrawn, not asserted by elimination. |
| A6 | Decay is observable within horizon: distractor padding produces nonzero event rates by turn 30. | All conversations right-censored → no hazard identifiable. | Walking-skeleton criterion S-a (≥20% sustained-violation rate by turn 30). | **PG-6** (walking skeleton, Step 9). | Fails → extend horizon / harden distractors; skeleton re-run before any grid (situation 8). |
| A7 | Verifiers are valid: κ ≥ 0.8 on the human-audit sample. | LLM judge does not track soft-policy intent (t1). | Audit gate in M3 (R2 instrument-validation plan below). | **PG-7** (M3 construction, pre-scale, before Stage 1). | Low-κ pairs excluded; rule-verified vs. judge-verified subsets reported separately; if the whole judge class fails, situation 7 applies (simplify or redirect). |
| A8 | Model behavior is pinned: dated snapshots + ≥1 open-weights anchor reproduce. | Hosted API silently updates (t6). | Version pinning + transcript logging. | **PG-8** (continuous, checked at paper time). | Open-weights re-run must reproduce `G` within its CI, or the affected hosted-model results are reported as non-reproducible and excluded from the pooled estimate. |

**Instrument validation (R2, guidance.md §3.4) for the M3 compliance verifier (A7's gate PG-7), the one instrument in this design requiring the full five-step sequence:**
① *Ground categories externally*: the rule-checkable/judge-checkable split follows IFEval's verifiable-instruction taxonomy and RECAST's dual-mode (rule vs. LLM-judge) verifier taxonomy; the finer within-judge label family (task success / policy compliance / safety risk / refusal outcome / evaluator confidence) mirrors the linguistically-controlled taxonomy validated in [AdversarialPragmaticsAI2607, arXiv:2607.01153] (cache `relevance: adjacent`), which independently documents that collapsing these into one pass/fail label obscures whether failures are capability limits, policy ambiguity, or evaluator instability — the exact failure mode A7 guards against.
② *Draft wide, refine on a held-out set*: draft the label set on a 10% held-out calibration sample of scripted probe–response pairs (drawn before Stage-1 seeds are frozen); named merge/split operations (e.g., merge "partial compliance" sub-variants that never separate two human raters; split "refusal" into "explicit" vs. "soft-deflection" if they show different verifier behavior) are logged in `B_pilot/` before the label set is frozen.
③ *Validate against ≥2 independent human raters*: κ ≥ 0.8 acceptance on the held-out set (A7's threshold); below-threshold pairs are excluded, not averaged in.
④ *Inspect the confusion structure*: judge–human disagreements must cluster on adjacent categories (e.g., "full" vs. "partial" compliance), never a systematic rule-vs-judge split; a systematic split routes to situation 7 (simplify the construct) rather than being averaged away.
⑤ *Freeze before scale*: the label rubric and κ threshold are hashed into `B_pilot/` alongside the Step 9 walking-skeleton thresholds before Stage-1 scale-up; no post hoc rubric edits after freezing.

## Step 6 — Pre-Registered Experiments

Design constants (Stage-1 pilot, digest N6/N8): 2 models, 20 matched pairs, 2×2×2×2 factorial (τ × w × p × r), 30 turns, probes every 5 turns, 3 seeds/cell → 1,920 conversations, per-cell n=60; power target ≥80% for interaction HR 1.5 at α=0.05, **confirmed by simulation before launch** (simulation script is part of the pre-registration artifact).

**Per-cell power and thin-cell rule (Part 6 self-check item 9; guidance.md Part 4 situation 5).** The ≥80% power target is computed and reported per cell, not only for the pooled design: Stage-1's 2×2×2×2 grid at n=60/cell is the reference power computation; Stage-2's fractional-factorial subsample (3-level wording/position, repetition {1,3,5}) is expected to leave some cells below n=60 by construction. **Pre-declared rule:** any cell whose simulated power for the interaction it is meant to test falls below 80% is marked `INCONCLUSIVE` for that cell specifically before any data are collected — never reported as a null effect, and never silently dropped from the table (it is reported with its n and its INCONCLUSIVE tag). If a *central* test (H1's manipulated-factor interactions, H3's equivalence test) lands in an under-powered cell, the honest options are, in order: collect more within the same config (config-only, no code change), narrow H1/H3's claim to the powered cells with the narrowing stated in the abstract, or — if the central test itself cannot be powered — stop and report the power shortfall as the finding (situation 5). Thin cells are counted and reported alongside the headline n (R8 honest-scale discipline), matching the same disclosure standard already applied to dropped matched-pairs (A2) and low-κ verifier pairs (A7).

### E1 (RQ1) — What drives the gap?
- **Assumption:** A1, A2, A3, A4, A5, A7.
- **Hypothesis H1 (binary):** In the M4 dominance analysis of `β_{τ×turn}`: (i) at least one manipulated factor block (wording; position; repetition) has a significant factor×τ×turn interaction at Holm–Bonferroni-corrected α=0.05 across the three tests, **and** (ii) the manipulated blocks (salience+framing) jointly absorb **> 50%** of the gap coefficient's partial-R². PASS requires both.
- **Metric:** mechanism share (dominance weight / partial-R² of each block in `β_{τ×turn}`); soft/hard hazard ratio `G` with 95% CI.
- **Verification:** likelihood-ratio tests on the mixed-effects cloglog model, Holm–Bonferroni over the 3 mechanism factors; conversation-level random effects against pseudo-replication; robustness: Weibull refit, leave-one-pair-out, per-model subgroup fits (digest N8 analysis plan). n as above.
- **Fallback (pre-committed wording):** *"Presentation is not the story: matching a soft policy's salience and framing to a hard norm's leaves the majority of the decay gap standing (manipulated share = X% < 50%); the residual tracks the alignment-prior proxies, implicating training-time reinforcement — not prompt engineering — as the route to durable soft policies."* (This is digest N9 Result-1's falsification branch, promoted to headline; CO4's negative clause becomes the main guidance.)

### E2 (RQ_INF_1) — Can boosting close the gap?
- **Assumption:** A1, A2, A3, A6.
- **Hypothesis H2 (binary):** the fully-boosted soft cell (imperative + sys-head + r=5) achieves gap closure **κ_close ≥ 0.5** (bootstrap 95% CI lower bound > 0.25), **and** does not fully close it: `t½(boosted-soft) < t½(std-hard)` with the half-life-ratio CI excluding 1. PASS requires both.
- **Metric:** `κ_close` (Step 5); half-life ratios with 10,000-resample bootstrap CIs (resampling at conversation level).
- **Verification:** planned contrast of boosted-soft vs std-soft vs std-hard within the fitted M4 model; bootstrap CIs; α=0.05 (single pre-registered contrast, no correction needed).
- **Fallback (two symmetric branches, digest N9 Result-2):**
  - If κ_close CI includes 0: *"Salience and framing are causally inert for constraint durability: a soft policy stated imperatively, prominently, and five times decays no slower than one stated once in passing — the asymmetry is prior-driven."*
  - If boosted-soft ≥ std-hard (gap fully closes): *"Soft-policy fragility is a presentation artifact: imperative, head-positioned, repeated statement restores hard-norm-level durability, and no training-time intervention is required."* (Falsifies CO4's negative clause; still a complete, actionable result.)

### E3 (RQ_INF_2) — Is the measurement itself clean? **[RUN FIRST — gates E1/E2]**
- **Assumption:** A6, A7 (and it *tests* A4).
- **Hypothesis H3 (binary):** probe reactivity is type-uniform: the 95% CI of the probing-regime × τ interaction hazard ratio lies entirely within **[0.80, 1.25]** (equivalence test), regardless of the size of the main reactivity effect.
- **Metric:** `Δ_react` (within- vs between-conversation log hazard ratio at matched turns); regime×τ interaction HR.
- **Verification:** M6 calibration cells: 4 pilot cells × 2 pairs × 6 probe turns × 10 seeds ≈ 480 between-conversation runs (digest N6 feasibility); TOST-style equivalence on the interaction; α=0.05.
- **Fallback (pre-committed):** *"Behavioral probing differentially refreshes constraint salience by constraint type — a measurement artifact that biases naive within-conversation decay estimates; we quantify the bias and re-estimate the soft/hard gap on the reactivity-free between-conversation design."* Main analyses (E1/E2) then rerun on a between-conversation fractional subsample only, with claim scope narrowed accordingly (digest N9 Result-3 falsification branch). This methodological finding is itself publishable under the empirical archetype.

### Mandatory baselines

- **B0 — "why do this at all" control:** the **no-injection floor arm** plus the **no-manipulation replication arm** (std wording, sys-head, r=1; digest N8 baselines). The floor arm establishes that turn-1 adherence is caused by injection and that "decay" means regression toward a measured no-constraint baseline, not toward zero — without it, the 8x gap could be a floor/ceiling artifact and there is no phenomenon to decompose. The replication arm must show `G > 1` (A1); if the trivial, unmanipulated design shows no gap, the problem does not exist in matched pairs (→ F-G1).
- **B-alt — strongest-alternative-explanation control:** **rival explanation: the gap is a difficulty/verifiability artifact** — soft constraints are intrinsically harder to satisfy and are scored by graded (judge-based) verifiers, so "soft rots faster" reduces to "harder, fuzzier tasks fail sooner" (digest C3, t1, Claim 3). Matched arm: analysis restricted to pairs with (i) rule-based binary verifiers on **both** sides, (ii) turn-1 adherence ≥ 0.95 for both types, (iii) no-injection floors within 10 pts of each other; token budget already equalized across cells by M2's length-matched filler. **Pre-registered check:** the subset gap `log G_subset` must lie within ±50% of the full-bank `log G`; if the gap vanishes in this subset, the difficulty artifact wins and the mechanism claims are withdrawn in favor of the artifact finding.

### Global fallback F-G1

If the central family fails — the gap does not replicate directionally in matched pairs (A1/B0), or no factor and no proxy moves it (H1 fail + A5 fail) — the archetype pivots from `empirical` (mechanism attribution) to `benchmark/measurement` (digest N12's own re-classification clause). Pivoted abstract sentence, pre-committed: *"The widely cited ~8x soft/hard constraint decay asymmetry does not survive content-matched, reactivity-controlled measurement: we show the reported gap is manufactured by unmatched constraint banks, verifier-class asymmetry, and probe reactivity, and we release the matched-pair decay suite that makes constraint-durability claims testable."*

## Step 9 — Walking Skeleton

**One binary question:** *In content-matched, rule-verified pairs, does soft adherence decay measurably faster than hard adherence at all?*

- **Arms (3):** (1) std-soft (natural wording, sys-head, r=1), (2) std-hard (same), (3) no-injection floor.
- **Smallest task set:** 5 matched pairs (rule-verifiable constraints only — no LLM judge in the skeleton), 1 open-weights instruct model, 30-turn conversations with LMSYS-Chat-1M distractor padding, probes every 5 turns, 5 seeds → 3 × 5 × 5 = **75 conversations, ~2,250 assistant calls**.
- **Deterministic metrics only:** per-turn adherence rate (rule verifier pass fraction), sustained-violation event rate, Kaplan–Meier curves. No mixed models, no judges, no bootstrap.
- **Expected cost:** < 1 day wall-clock on 1×A100-80GB (or < $50 hosted); harness ≈ 3 engineer-days (subset of the ~2 person-week Stage-1 estimate, digest N6 feasibility).
- **Pass criteria (all four):**
  - **S-a (A6):** ≥ 20% of std-soft conversations reach a sustained violation by turn 30 (hazard identifiable).
  - **S-b (A1):** KM curves ordered soft < hard from turn 10 onward, with turn-30 adherence gap ≥ 10 pts.
  - **S-c (B0):** no-injection soft compliance ≤ 50% at probe turns (injection is causal).
  - **S-d:** verifiers deterministic and stable across seeds (zero verifier crashes/ambiguous labels).
- **"Passed → scaling is a config change":** after the skeleton, Stage 1 differs only in enumerated config values (pairs 5→20, cells 1→16, models 1→2, seeds 5→3, + M5 proxy runs, + M6 calibration arm). No new code paths except the LLM-judge verifier class, which is developed against A7's κ gate independently of the loop.

## Claim–Evidence Map

| # | Claim (final abstract will assert) | Traces to | Status |
|---|---|---|---|
| 1 | A soft/hard decay-rate asymmetry exists in content-matched pairs (premise replication; digest Claim 1). | A1, B0, skeleton S-b, Step-5 "faster" | needs-experiment; fallback-covered (F-G1) |
| 2 | Salience, framing, and prior are separable by intervention on matched pairs (digest Claim 2, C1). | Step-5 definitions; M1/M2/M5 design; E1 | supported-by-design (separability); residual-mechanism caveat pre-stated (digest N6 unaddressed C4) |
| 3 | Matched pairs isolate type from difficulty/verifiability (digest Claim 3). | A2, A3, A7, B-alt | needs-experiment (B-alt check); fallback-covered (artifact finding) |
| 4 | Attribution result: manipulated factors absorb >50% of the gap / or prior dominates (digest Claim 4, N9 R1–R2). | H1, H2 | needs-experiment; fallback-covered (E1/E2 pre-committed wordings) |
| 5 | Decay is measured without type-differential probe reactivity (digest Claim 5, C2). | H3, A4, M6 | needs-experiment (run first); fallback-covered (E3 methodological pivot) |
| 6 | Released suite enables mitigation testing (CO3). | Skeleton + M1–M3 artifacts | supported-by-design (artifact ships regardless of H outcomes) |
| 7 | Conditional guidance for policy authors (CO4). | H1×H2 outcome matrix (all four branches worded above) | fallback-covered by construction |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; all effect statements pending E1–E3)

> In deployed LLM agents, hard safety norms and soft organizational policies are naturally confounded: the hard ones are simultaneously stated more imperatively, placed more prominently, and reinforced in the weights by alignment training — so the reported ~8x faster decay of soft policies over long conversations cannot, from observation alone, be attributed to any one cause. We isolate the three candidate mechanisms by intervention: a bank of content-matched soft/hard constraint pairs is injected into distractor-padded long-horizon conversations while wording strength, context position, and repetition are crossed orthogonally, with alignment-prior strength measured by a proxy battery and probe reactivity gated by a within- vs between-conversation calibration arm. Fitting discrete-time survival models and decomposing the soft/hard hazard gap, we attribute [X]% to salience and framing and [Y]% to the prior-linked residual, deciding whether durable soft policies are a prompt-placement problem or a training problem.

(148 words; verbs: isolate, gate, measure, attribute, decompose, decide; opens on the confound/asymmetry, no "increasingly used… however… we introduce".)
