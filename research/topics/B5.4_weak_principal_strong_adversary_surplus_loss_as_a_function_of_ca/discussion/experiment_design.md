# Experiment Design Spec — Weak Principal, Strong Adversary

> Standalone rendering of Stage 6's confirmed output (`pipeline.md` → "Stage 6 — Experiment Design") plus `paper.md`'s Step 6 pre-registered experiment section, which refined three of Stage 5's five hypotheses (H1 gained an effect floor, H2b gained an explicit non-inferiority margin, H2a gained a sharpened zero-gap prediction) before `paper_draft.md`'s Experiments section was written from them. This document is meant to be executed as a protocol on its own, without opening the paper. `target_hypothesis` fields below are quoted verbatim from their source (`paper.md` Step 6 where a refined, explicitly-labeled hypothesis exists; `pipeline.md` Stage 5/6 otherwise) — not paraphrased. Keep this file and `paper_draft.md`'s Experiments section synchronized: a change to one should be mirrored in the other.
>
> **Study type:** `empirical` (Stage 1). Per Stage 6's tier accounting: **5 mechanism-tier RQs, 0 framing-tier, 0 outcome-tier** — `study_type = empirical` forbids "our procedure beats baseline X" framing, so the baselines below are sanity-check comparators only, never outcome-tier competitors.

---

## Datasets

| Dataset | Justification |
|---|---|
| **GLEE bargaining game configurations** (Shapira et al., 2024 — `GLEE2410`) | Parameterized economic-game benchmark; used as the primary game family because its parameterization gives direct, controlled sweeps over surplus size and valuation asymmetry, which the pilot (Stage 1 harness build-out) needs to compute closed-form references cheaply before scaling up. |
| **Deal-or-No-Deal multi-issue division scenarios** (Lewis et al., 2017 — `DealOrNoDeal1706`) | Real multi-issue value functions with private per-item valuations; used to test whether the surplus-loss scaling relationship (RQ2) generalizes beyond GLEE's parameterized configurations to a second, independently designed game family. |
| **Synthetic 3-issue divide-the-pie suite** (generated) | Lets valuation asymmetry be swept as a controlled, continuous parameter independent of whatever asymmetry distribution GLEE's or Deal-or-No-Deal's fixed scenario pools happen to contain; specifically needed to test whether RQ2's gap-measure sign-agreement (or disagreement) concentrates at high-asymmetry instances as a designed sweep, rather than only being observed post hoc across two fixed corpora. (This justification was itself a Stage 6 refiner-pass fix — the draft version only said "generated, for controlled asymmetry," which the critic flagged as a provenance note rather than a hypothesis-linked reason.) |

## Baselines (sanity-check comparators, not outcome-tier competitors)

| Baseline | Role |
|---|---|
| **Zero-gap self-play** (weak-vs-weak, strong-vs-strong) | The existence check for the metric itself — feeds RQ1. If mean loss is not near zero when there is no capability gap to explain it, the harness (not the phenomenon) is broken. |
| **Scripted Boulware / linear-conceder opponent** | A non-adaptive, memoryless capability floor. If the gap-loss trend appears even against a scripted opponent, "the strong adversary's capability specifically" is refuted in favor of generic concession-strength differences. |
| **Both-constrained control cell** (adversary also schema-restricted) | Isolates whether any residual structured-condition gap-slope is substantive rather than rhetorical — feeds RQ5's channel attribution. |

---

## RQ1 — Does the surplus-loss metric read near zero when there is no capability gap to explain a loss?

- **Tier:** mechanism (validates `sp_reference_and_game_design` / the `m_bargaining_harness` method)
- **Target hypothesis (verbatim, `pipeline.md` Stage 5/6 — `rq_gap_validity`):** "At zero capability gap (self-play), mean normalized surplus loss is close to zero (|E[L | Δ=0]| ≤ 0.05) under the primary Nash-bargaining reference — validating that the harness measures gap-driven exploitation rather than a mechanically biased game or an arbitrary reference choice." (Restated in `paper.md`'s Step 6 as mandatory baseline **B0**'s pre-registered pass condition: "Pre-registered pass: |E[L | Δ=0]| ≤ 0.05.")
- **Setup:** Zero-capability-gap self-play episodes (weak-vs-weak and strong-vs-strong) run across all tested game families under the free-text condition, scored under the primary (Nash-bargaining) reference.
- **Sample-size rationale:** Sized to estimate the self-play mean surplus loss to within ±0.02 units at 95% confidence.
- **Statistical test:** Mean and 95% confidence interval of normalized surplus loss under self-play, checked against the pre-registered ≤0.05 threshold (no inferential test beyond the CI bound — this is an instrument-validity gate, not a hypothesis test against an alternative).
- **Expected outcome:** Mean normalized surplus loss under self-play is close to zero: |E[L | Δ = 0]| ≤ 0.05 under the primary reference.
- **Falsification condition:** Refuted if |E[L | Δ = 0]| exceeds 0.05 — this would indicate the harness itself (the game design or the reference-split computation), rather than the capability gap, is producing an apparent loss, and every downstream gap-dependent claim in RQ2–RQ5 would need to be revisited before being trusted.
- **Metrics:** Mean and 95% CI of normalized surplus loss under self-play, per game family and reference split.

---

## RQ2 — Does normalized surplus loss scale with capability gap, and do the two gap measures agree?

- **Tier:** mechanism (targets `sp_gap_construct` / method `m_gap_quantification_and_scaling`)
- **Target hypothesis (verbatim, `paper.md` Step 6, Hypothesis H1 — refined from `pipeline.md` Stage 5's `m_gap_quantification_and_scaling` hypothesis with an added effect floor):** "In the free-text condition, the mixed-effects gap slope β_Δ > 0 with two-sided Wald p < 0.05 under both Δ_a and Δ_b, AND Spearman ρ > 0 over gap levels (monotone), AND the two gap measures give same-signed slopes, AND the effect floor: the model-implied increase in L from the smallest to the largest tested gap level (β_Δ × range(Δ)) is ≥ 0.10 normalized-loss units under each gap measure — a statistically significant but sub-0.10 slope is reported as 'detected but below the pre-registered practical-significance floor,' not as H1 passing."
- **Setup:** Pilot stage — a capability ladder spanning several tiers against a fixed strong adversary, free-text condition, one game family. Scale-up — a full round-robin over the capability ladder (directed unequal pairs plus zero-gap self-play controls) across all three game families. Mixed-effects model: `L ~ Δ + (1|game instance) + (1|model pair)`, clustered by pair.
- **Sample-size rationale:** n = 50 episodes/cell; 30 directed unequal pairs + 6 zero-gap self-play controls × 3 game families (`pipeline.md` Stage 6 / `paper.md` Step 6 RQ1 Verification). Per-cell counts are sized to detect a standardized gap-slope effect of d ≈ 0.4 at ≈80% power; an observed effect below that in the pilot triggers a pre-committed enlargement of the scale-up sample, not a null claim.
- **Statistical test:** Mixed-effects linear regression with random intercepts for game instance and model pair, two-sided Wald test on the gap coefficient (α = 0.05), computed separately for Δ_a (exogenous) and Δ_b (endogenous); Spearman correlation of loss with gap level.
- **Expected outcome:** Normalized surplus loss increases with capability gap under both measures (significantly positive Wald test, p < 0.05, same sign for both), with a monotone trend across gap levels (Spearman ρ > 0), and the effect clears the 0.10-normalized-loss-unit practical-significance floor under each gap measure.
- **Falsification condition:** Refuted toward "no scaling relationship" if the gap coefficient is not significantly positive under either measure, or the trend is flat/non-monotone; refuted toward "gap is projection-dependent" (a distinct, also-reportable outcome, not a null result) if the two gap measures yield significantly opposite-signed coefficients; a slope significant but implying <0.10 units of change across the tested range is reported as "detected but below the practical-significance floor."
- **Metrics:** Per-measure mixed-effects slope and 95% CI; Spearman correlation of loss with gap level; sign-agreement between the two gap measures.

---

## RQ3 — Does restricting the weak agent to structured offers lower its surplus loss relative to free text, at matched capability gap? (same-model contrast)

- **Tier:** mechanism (targets `sp_net_effect_of_restriction` / method `m_structured_offer_constraint`)
- **Target hypothesis (verbatim, `paper.md` Step 6, Hypothesis H2a — corresponds to `pipeline.md` Stage 5/6's `rq_same_model_contrast`):** "condition main effect is negative — E[L|structured] < E[L|free] for the same (w,s) — with Holm-corrected p < 0.05, AND point-estimate reduction in normalized loss ≥ 0.05 units, AND the condition×gap interaction is positive (protection grows with Δ)."
- **Setup:** For each tested model pair and gap level, the same pair negotiates matched game instances under both the free-text and structured-offer condition for the weak side (identical adversary system prompts, condition undisclosed, side/first-mover counterbalanced — per Assumption A4's confound ledger). A 2(condition)×k(gap) mixed-effects factorial estimates the condition main effect and the condition×gap interaction.
- **Sample-size rationale:** n = 50 episodes/cell (detects d ≈ 0.4 at ≈80% power per gap level, per `paper.md`'s N8 analysis plan).
- **Statistical test:** Two primary tests (condition main effect, condition×gap interaction) with Holm correction, α = 0.05, clustered by pair.
- **Expected outcome:** The condition main effect is negative (loss lower under structured offers at matched gap, point-estimate reduction ≥0.05 normalized-loss units), and the condition×gap interaction is positive (the reduction grows as the gap widens).
- **Falsification condition:** Refuted if the condition main effect is non-significant or non-negative under Holm-corrected α = 0.05, or if the point-estimate reduction falls below 0.05 units — either would mean expressive freedom does not expose the weak agent to additional loss, and restriction is neutral-to-harmful rather than protective (the publishable-negative fallback: "expressive freedom does not expose the weak agent; action-space restriction is neutral-to-harmful, refuting constraint-as-protection").
- **Note on zero-gap cells:** A controlled human-subjects study using a near-identical structured-offer-vs-free-text manipulation between symmetric-capability dyads (`LanguageOfBargaining2023`) found the average agreed split statistically unchanged between conditions. This predicts H2a's condition main effect should be near zero specifically at Δ≈0 (the B0 self-play cells), emerging only as the significant condition×gap interaction — a near-null B0 condition contrast is therefore not evidence against H2a, it is the pattern this prior result predicts and that the interaction term is designed to detect.
- **Metrics:** Condition main-effect coefficient and 95% CI; condition×gap interaction coefficient and CI.

---

## RQ4 — Can a structured-offer restriction let a lower-capability tier match a higher one against the same adversary? (cross-tier substitution)

- **Tier:** mechanism (targets `sp_net_effect_of_restriction` / method `m_structured_offer_constraint`)
- **Target hypothesis (verbatim, `paper.md` Step 6, Hypothesis H2b — refined from `pipeline.md` Stage 5/6's `rq_cross_tier_substitution` hypothesis with an added explicit non-inferiority margin):** "a constrained weak agent of tier t undercuts an unconstrained agent of the next-stronger tier t+1 against the same adversary, within a pre-registered non-inferiority margin δ = 0.05 normalized-loss units: E[L | w=t, structured] ≤ E[L | w=t+1, free] + 0.05, one-sided non-inferiority test, α=0.05, for at least one adjacent tier pair."
- **Setup:** For each adjacent pair of capability tiers (t, t+1), a constrained weak agent at tier t is compared against an unconstrained weak agent at tier t+1, both facing the same adversary, read off the same gap×condition factorial as RQ3.
- **Sample-size rationale:** Cross-cell contrast reuses RQ3's per-cell n = 50 episodes; no separate sample beyond the RQ3 factorial is required.
- **Statistical test:** One-sided mixed-effects non-inferiority test per adjacent tier pair against the δ = 0.05 margin, Holm-corrected across the tested adjacent pairs, α = 0.05. (The explicit δ matters: "≤" alone with no stated margin would silently be a superiority test mislabeled as non-inferiority.)
- **Expected outcome:** For at least one adjacent tier pair, the constrained lower-tier agent's surplus loss is within the δ = 0.05 margin of the unconstrained higher-tier agent's — restriction substitutes for at least one tier of capability.
- **Falsification condition:** Refuted if no adjacent tier pair satisfies E[L | w=t, structured] ≤ E[L | w=t+1, free] + 0.05 at Holm-corrected α = 0.05 — this would mean restriction, even where protective in RQ3, cannot compensate for a genuine capability-tier gap even within a 0.05-unit margin, and capability remains the dominant lever (fallback: "constraint helps within a model but cannot compensate for one capability tier; capability remains the dominant lever and constraint is a second-order mitigation").
- **Metrics:** Cross-tier mean surplus-loss difference and one-sided confidence bound, per adjacent tier pair.

---

## RQ5 — How much of any restriction effect is rhetorical versus substantive? (channel attribution, exploratory)

- **Tier:** mechanism, exploratory (targets `sp_channel_attribution` / method `m_channel_attribution`)
- **Target hypothesis (verbatim, `paper.md` Step 6, Hypothesis H3 — corresponds to `pipeline.md` Stage 5/6's `rq_channel_attribution`):** "the between-condition slope difference removes >50% of the free-text gap slope, i.e. (β_free − β_structured)/β_free > 0.5, AND adversary tactic incidence correlates positively with per-episode L (p < 0.05)."
- **Setup:** The reduction in the mixed-effects gap-loss slope between the free-text and structured conditions is computed as a between-condition slope-removal ratio. Independently, an LLM judge tags each adversary free-text message against a fixed four-label tactic taxonomy (anchoring, misrepresentation of value, false deadline/commitment, flattery/pressure) — grounded in established negotiation-tactics inventories and this cache's own `BEDA2512`/`StrategicPersuasion` vocabularies, not invented ad hoc — with 10% human double-coding (target Cohen's κ ≥ 0.7, per the 5-step instrument-validation sequence: ground categories externally → draft wide and refine on a held-out calibration set → validate against ≥2 independent human raters → inspect confusion structure → freeze before scale). The both-constrained control cell provides an additional bilateral check on whether residual structured-condition loss is substantive.
- **Sample-size rationale:** Tactic tagging draws on the same episode pool as RQ3/RQ4 (n = 50/cell); the held-out calibration set for label refinement is 100 pilot transcripts from the Stage-1 skeleton run, with 10% of the scale-up set double-coded by two human raters for the κ ≥ 0.7 acceptance gate.
- **Statistical test:** Paired between-condition slope difference per gap level (bootstrap CI); logistic/Poisson regression of per-episode L on tactic counts, α = 0.05. Labeled exploratory throughout — no confirmatory claim.
- **Expected outcome:** The slope-removal ratio exceeds one-half (structured condition removes more than half of the free-text gap slope), and adversary tactic incidence correlates positively with per-episode surplus loss (p < 0.05).
- **Falsification condition:** Refuted toward "exploitation is substantive, not rhetorical" if the slope-removal ratio is near zero — i.e., the structured condition's gap slope is nearly as steep as free text's — regardless of whether tactic incidence correlates with loss in the free-text condition alone; this would mean any protective effect found in RQ3 works through decision-simplification rather than channel closure. If the κ ≥ 0.7 reliability gate fails even after one refinement pass, the taxonomy is simplified to a coarse 2-label split (rhetorical vs. non-rhetorical) and re-validated once; if that also fails, RQ5 is dropped to "not measurable at acceptable reliability" rather than reported with an uncalibrated judge.
- **Metrics:** Slope-removal ratio with bootstrap CI; tactic incidence rate per transcript; regression coefficient of loss on tactic count.

---

## Thin-cell rule (applies to all RQs above)

Any gap-level × condition × game-family cell with fewer than 30 valid episodes (below the powered n=50 target) is pre-declared **INCONCLUSIVE** for that cell — its data are reported but excluded from the primary tests, never scored as null or dropped silently. If the central test for RQ2 (pooled slope) or RQ3 (pooled condition main effect) is underpowered because more than 25% of its constituent cells are thin, the whole test is labeled INCONCLUSIVE rather than reported as a null finding.

## Global fallback (F-G1)

If the constraint-as-protection family fails outright (both H2a/RQ3 and H2b/RQ4 refuted), the archetype pivots from "actionable mitigation" to pure measurement/characterization: the headline becomes the surplus-loss-vs-gap scaling law (RQ2) plus a clean negative result on constraint-as-protection.
