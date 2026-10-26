# Experiment Design — B2.3: Cross-Backbone Stability of LLM-Agent Failure Attribution

> Standalone protocol assembled from Stage 6's confirmed output in `pipeline.md` and `paper.md`'s Step 6 ("Pre-Registered Experiments") / Claim–Evidence Map. This document is meant to be executable on its own, without opening the paper. Status: **specification — no experiments have been run; all numbers are pre-registered design targets.** `study_type = empirical`; per Stage 6's tier accounting, all research questions below are **mechanism-tier** (0 framing-tier, 0 outcome-tier — no research question is framed as "our procedure beats baseline X"). Stage 6 originally emitted 8 numbered RQs; on 2026-07-05 the former RQ6 (tie-break sensitivity) was demoted to the instrument-validation sensitivity check **SC1** per the Phase G finding logged in `stage_review.md`/`pipeline.md` (its target threshold has no H-id in `paper.md`'s pre-registered hypothesis machinery), leaving **7 numbered RQs plus SC1**; the former RQ7/RQ8 are renumbered RQ6/RQ7.
>
> Keep this file synchronized with `paper_draft.md`'s Experiments section and `paper.md`'s Step 6 if either changes.

## Datasets

| Dataset | Role | Justification |
|---|---|---|
| **GAIA (levels 1–2)** | Pilot-stage domain | Tool-use/assistant tasks with deterministic, programmatic success checkers — a checkable single-step-tool task gives the fault-injection ground truth a clean, unambiguous referent. |
| **WebArena-style tasks** | Scale-up domain | Reproducible web-agent tasks with richer multi-step tool interaction — stress-tests whether findings generalize beyond short, deterministic GAIA-style tasks to longer-horizon tool chains. |
| **Who&When (naturally-failed multi-agent logs)** | Organic-failure complement (feeds RQ1 only, non-voting) | Tests whether RQ1's stability-band finding, established on synthetic single-layer injected faults, replicates on organically-arising, human-annotated failures where the ground-truth layer comes from expert agreement rather than injection-guaranteed construction. Without it, any stability finding is scoped only to synthetic-fault artifacts rather than to failure attribution generally. Reported alongside the primary GAIA/WebArena grid as a third, non-voting data point — never pooled into the primary aggregation vote (see below). |

**Scaffold scope (added 2026-07-05 per `design_review.md` reviewer question 1; situation 14(b) narrow-envelope concession):** every trace in this design is produced under one fixed ReAct-style agent scaffold. All findings are scoped to that scaffold; whether attribution instability is itself scaffold-specific is explicitly left open, and a minimal second-scaffold arm on a task subset is named future work, not part of this pre-registration.

## Task-pool arithmetic and pre-declared shrink axis (added 2026-07-05 per `design_review.md` F6)

The Stage-2 grid needs ≈300 base tasks (≈900 (task, layer) cells; digest N6). Per-source counts, pre-registered: GAIA levels 1–2 with public, programmatically checkable answers contributes ~140 tasks, so the WebArena-style slice is sized at **≥160 tasks** (its self-hosted-environment engineering is budgeted as harness work, separate from judge-call cost). Expected analyzable pool under A6 (headline analysis restricted to tasks with clean-run success under **all** backbones): the clean-run intersection is upper-bounded by the weakest backbone's clean-run solve set, so under a pessimistic 40% weak-backbone solve rate the planning bound is ≈120 tasks (≈360 cells) *before* the failure-overlap gate Ω is applied on top; the skeleton and pilot replace this assumed 40% with measured per-backbone clean-run rates (the empirical residual `design_review.md` F6 flags). **Pre-declared shrink axis (situation 10):** if the double intersection falls below the pre-registered cell minima (e.g., RQ4's 20-task floor), the first and only pre-approved shrink is to **drop the weakest capability tier from the headline grid** (reporting it descriptively, with the resulting censoring asymmetry reported under RQ7) — never a silent reduction of per-cell n, never a post-hoc relaxation of a cell minimum.

## Baselines

All baselines are sanity-check comparators or reference labelers, not outcome-tier competitors — this is a measurement study, and no research question is framed as "our procedure beats baseline X."

- **Who&When all-at-once and step-by-step LLM-judge protocols** — the two attribution-procedure options that bracket context-granularity effects; used as the primary attribution procedure's design space, not a beat-a-number target. **Primary protocol named (added 2026-07-05 per `design_review.md` F9):** the **all-at-once** protocol is the pre-registered primary attribution procedure $A_j$ — its single trace-level pass matches the estimand's one-label-per-failing-trace unit of analysis — and the step-by-step protocol is a secondary robustness arm only, never the source of a headline number; the choice is frozen together with the codebook hash (Instrument-validation step ⑤ in `paper.md`) before any Stage-1/2 labeling, closing the analytic degree of freedom the review flagged.
- **AgenTracer-style counterfactual-replay labeling** — an independent reference labeler on a budget-permitting subset, checking the fixed judge's labels against a causal-replay definition of the decisive step.
- **Chance-level agreement** (label-marginal-preserving permutation) — the statistical floor beneath which no claim of "agreement" is meaningful.
- **Majority-vote-across-backbones pseudo-consensus** — a sanity baseline, promotable to a load-bearing contribution only if RQ4's agree-wrong mass turns out to be negligible (Fallback F-2).
- **B0 — same-backbone test–retest** ("why do this at all" control): identical backbone re-run at T=0 plus 3 seeds at T=0.7, re-judged. Pre-registered gate: cross-backbone disagreement must exceed within-backbone disagreement + 0.05 absolute, or the study's premise fails outright (pre-committed fallback wording: "attribution labels are noisy, full stop"). **Pipeline-level placebo arms (added 2026-07-05 per `design_review.md` F7):** (i) a **judge test–retest** arm — the identical trace judged twice under the frozen judge at T=0 — isolates judge sampling noise from agent re-execution nondeterminism, so a B0 gate trip can be attributed to the judge side or the agent side rather than read blindly; (ii) a **no-op injection** arm — uninjected, successful traces submitted to the judge under the same prompt — verifies the judge does not hallucinate a fault layer where none was injected. The label-marginal-preserving permutation remains the κ-code placebo only; these two arms supply the pipeline-level placebo it cannot provide.
- **B-alt — strongest-alternative-explanation control**: identical judging budget spent on (i) style-normalized/paraphrased traces and (ii) the vendor-disjoint judge swap, plus the human-codebook subset as a style-immune anchor — tests the rival explanation that labels differ because the judge reads backbone-flavored surface style differently, not because backbones fail differently.

## Cross-cutting aggregation and thin-cell discipline (applies to RQ1–RQ7 and SC1)

Cells drawn from GAIA-derived and WebArena-derived task families are pooled for every headline verdict. As a pre-registered secondary check, each hypothesis's band/threshold decision is also recomputed within each family alone; a hypothesis counts as **family-robust** only if the pooled verdict agrees with at least one of the two family-specific verdicts — disagreement on both downgrades the claim from a general statement to a family-conditional one, never reported as the pooled number alone. Any comparison cell below its pre-registered minimum count is reported as **INCONCLUSIVE** (never null, never dropped from the denominator): a (backbone-pair × layer) cell with fewer than 20 jointly-failing tasks is INCONCLUSIVE for RQ4; a (judge-backbone × agent-backbone) cell with fewer than 15 failing traces is INCONCLUSIVE for RQ3 (retained in the reported denominator); RQ6's family contrast is INCONCLUSIVE as a whole if the pooled within-family arm falls below 3 pairs or the cross-family arm falls below 6 pairs. All CIs use 10,000 task-level cluster-bootstrap resamples; multiple comparisons within each hypothesis family use Holm correction, α = 0.05.

---

## RQ1 — Does the attribution label survive a swap of the agent's executing backbone?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_censoring_confound`.
- **Target hypothesis (verbatim, paper.md Step 6, H1):** "Fleiss' κ across K ≥ 6 backbones on $\mathcal{I}$ has a 95% CI entirely below 0.8 (attribution is *not* fully stable)."
- **Setup:** Pilot stage: 60 tasks × 3 fault layers × 4 backbones (one per distinct model family) at T=0. Scale-up: ≈900 (task, layer) cells × 6–8 backbones (crossing family and capability tier) × 3 seeds, on GAIA and WebArena-style tasks.
- **Sample-size rationale:** Stage-2 grid sized for >0.9 power to detect κ differences of 0.10 between layers at α = 0.05, computed from pilot-estimated base rates (digest N8). Assumption A2 gate: pilot failure-overlap rate Ω ≥ 0.5 required before Stage 2 proceeds under Fleiss' κ as primary; if Ω falls short, Krippendorff's α over all failing (possibly partial) cells is promoted to primary by pre-commitment (Extreme-censoring fallback F-C0 applies if Ω < 0.2 and mean pairwise overlap < 0.2).
- **Statistical test:** Fleiss' κ on the failing intersection $\mathcal{I}$ (or Krippendorff's α on all failing cells if Ω < 0.5); 10,000 task-level cluster-bootstrap CIs; Holm correction across backbones and layers.
- **Expected outcome:** Cross-backbone agreement is substantially below-perfect: the primary statistic's 95% CI lies entirely below the "stable" band (κ or α ≥ 0.8), landing in "model-specific" (< 0.6) or "partially stable" (0.6–0.8).
- **Falsification condition:** Refuted toward "stable" if the CI lies entirely at or above 0.8 across layers and family pairs (Fallback F-1: diagnosis is a task property, not a backbone artifact).
- **Partial-band decision rule (added 2026-07-05 per `design_review.md` F9):** if the pooled statistic lands in the partially-stable band (0.6 ≤ κ < 0.8) or its CI straddles 0.8, the pre-registered consequence (`paper.md` Fallback F-1, straddle clause) is that the per-layer decomposition becomes the primary result and the claim becomes RQ2's layer ordering. The practitioner-facing decision (CO4) is then made **per layer, not per pipeline**: attribution labels are treated as transferable across a backbone swap only for layers whose per-layer statistic lies in the stable band (≥ 0.8); labels for layers below it are re-validated per backbone.
- **Metrics:** Primary stability statistic and its CI per layer and per backbone pair; failure-overlap rate Ω reported beside every number.

## RQ2 — Is execution-layer attribution more consistent across backbones than plan-layer attribution?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_censoring_confound`.
- **Target hypothesis (verbatim, paper.md Step 6, H1b — layer structure):** "κ_exec − κ_plan ≥ 0.10 with Holm-corrected p < 0.05."
- **Setup:** Same Stage-2 grid and fitted structure as RQ1; layer-specific κ (or α) compared pairwise (execution vs. plan, execution vs. tool, tool vs. plan).
- **Sample-size rationale:** Shares RQ1's Stage-2 grid and >0.9 power target for κ differences of 0.10 at α = 0.05 (digest N8 pilot base rates) — one fitted structure yields both RQ1's stability-band readout and RQ2's per-layer ordering readout without a second data collection pass.
- **Statistical test:** Pairwise Holm-corrected significance tests on per-layer κ (or α).
- **Expected outcome:** κ_exec exceeds κ_plan by ≥ 0.10 absolute, Holm-corrected p < 0.05 — mechanically legible (execution-layer) faults are diagnosed more consistently than interpretive (plan-layer) faults.
- **Falsification condition:** Refuted if the gap is under 0.10 absolute or non-significant, or if the ordering reverses (plan more consistent than execution) — reversal is reported at full prominence per Fallback F-1b, since it would invert which attribution claims need per-backbone re-validation.
- **Metrics:** Per-layer stability statistic and pairwise contrasts with Holm-corrected p-values.

## RQ3 — How much of any observed instability is attributable to the judge backbone rather than the agent backbone?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_agent_judge_confound`.
- **Target hypothesis (verbatim, paper.md Step 6, H3a):** "judge-backbone variance share > 0.20 of total random-effect variance, LRT p < 0.05."
- **Setup:** Three vendor-disjoint judge backbones × 6–8 agent backbones over the identical Stage-2 trace set (raw arm); cross-classified mixed-effects model: label match ~ (1|task) + (1|agent_backbone) + (1|judge_backbone) + interactions.
- **Sample-size rationale:** Model fitted on the Stage-2 factorial (~90k judge calls, raw + normalized arms). Power depends on the number of judge×agent×trace observations; any (judge_backbone × agent_backbone) cell with fewer than 15 failing traces is pre-declared INCONCLUSIVE for the variance-share point estimate (retained in the reported denominator, never silently dropped). A 200-trace human-codebook subset anchors judge validity (Cohen's κ ≥ 0.7 gate, A4). **Validation/evaluation disjointness (added 2026-07-05 per `design_review.md` reviewer question 5 / R8):** the 200-trace subset is drawn by stratified random sampling over (agent backbone × injected layer) from pilot-stage failing traces, frozen before Stage-2 judging, and excluded from every headline hypothesis estimate — it is instrument-validation data only, so the traces that validate the judge never double as the traces the judge is scored on.
- **Statistical test:** Likelihood-ratio test on variance components; bootstrap CIs on variance shares.
- **Expected outcome:** Judge-backbone variance share exceeds 0.20 of total random-effect variance — the judge is a non-trivial, independently identifiable instability source.
- **Falsification condition:** Refuted if judge-backbone variance share is statistically indistinguishable from zero (Fallback F-3, paired with RQ5's failure: instability is genuinely agent-behavioral, not judging).
- **Metrics:** Judge-backbone, agent-backbone, task, and interaction variance shares with bootstrap CIs.

## RQ4 — When backbones agree with each other, do they also agree with the injected ground truth?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_manifestation_divergence`.
- **Target hypothesis (verbatim, paper.md Step 6, H2):** "agree-wrong mass ≥ 0.05 of $\mathcal{I}$, with 95% CI lower bound > 0.02 (consistency ≠ correctness; digest N9 refutation threshold)."
- **Setup:** Over the failing intersection $\mathcal{I}$, tabulate the joint outcome {agree-correct, agree-wrong, disagree} against the injected ground-truth layer, per backbone and per layer.
- **Sample-size rationale:** Power computed from the pilot's estimated $|\mathcal{I}|$ and the pre-registered effect floor (≥0.05 mass, CI lower bound > 0.02); a (backbone-pair × layer) cell with fewer than 20 jointly-failing tasks is pre-declared INCONCLUSIVE for that cell's contribution to the mass estimate, never treated as evidence of a zero effect.
- **Statistical test:** Task-clustered bootstrap CI on the agree-wrong proportion; per-layer breakdown Holm-corrected.
- **Expected outcome:** Agree-wrong mass is ≥ 5% of $\mathcal{I}$, CI lower bound > 2% — stability and correctness are separable outcomes.
- **Falsification condition:** Refuted if the agree-wrong mass is statistically indistinguishable from zero (CI upper bound ≤ 2%) — cross-backbone consensus would then be a reliable correctness signal, upgrading majority-vote-across-backbones to a valid pseudo-oracle (Fallback F-2).
- **Metrics:** Agree-correct / agree-wrong / disagree proportions per layer; per-backbone accuracy against the injection record.

## RQ5 — How much of any observed disagreement is driven by surface style rather than substance?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_style_confound`.
- **Target hypothesis (verbatim, paper.md Step 6, H3b):** "style-share ≥ 0.10 (normalization removes ≥10% of raw cross-backbone disagreement), CI lower bound > 0."
- **Setup:** Every raw-arm trace is additionally rendered through a fixed rewriter model (distinct from all agent and judge backbones) that strips model-identifying tokens, canonicalizes tool-call formatting, and neutrally paraphrases reasoning text; the normalized arm is re-judged by the same judges.
- **Sample-size rationale:** Shares RQ3's Stage-2 judge×agent factorial (~90k judge calls including the normalized arm); no additional trace collection needed — style-share is computed from the same fitted structure's raw-vs-normalized contrast.
- **Statistical test:** Bootstrap CI on style-share = (mean pairwise disagreement, raw − mean pairwise disagreement, normalized) / mean pairwise disagreement, raw.
- **Expected outcome:** Style-share ≥ 10%, CI lower bound > 0 — surface form explains a measurable but partial fraction of disagreement.
- **Falsification condition:** Refuted if style-share's CI includes zero or is negative (Fallback F-3, paired with RQ3's failure) — style normalization would not reduce disagreement, meaning any RQ3 judge-side effect is not a simple surface-form artifact.
- **Metrics:** Style-share with bootstrap CI, raw versus normalized arm.

## RQ6 — Is cross-backbone agreement structured by model family?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_family_capability_structure`.
- **Target hypothesis (verbatim, paper.md Step 6, H4a):** "mean within-family pairwise agreement exceeds cross-family by ≥ 0.10 absolute, Holm p < 0.05."
- **Setup:** Backbone grid crosses model family with capability tier (two sizes per family where available); pairwise agreement (RQ1's primary statistic) split into within-family and cross-family pairs.
- **Sample-size rationale:** Under the 2-per-family grid, H4a's contrast operates at the **pair level, pooled across families** (restated 2026-07-04 per `design_review.md` F1, to avoid emptying H4a by construction): the within-family arm requires ≥3 within-family pairs in total (satisfied by 3–4 families × 1 within-family pair each); the cross-family arm requires ≥6 pairs. Either arm falling short pre-declares H4a as a whole INCONCLUSIVE (reported descriptively per pair, never as evidence of "unstructured"). Because every within-family pair is by construction cross-tier under the 2-sizes-per-family grid, the family contrast is restricted to cross-tier pairs on both sides — (within-family, cross-tier) vs. (cross-family, cross-tier) — removing the tier-composition confound (R3, per `design_review.md` F2); the orthogonal tier effect is estimated by (cross-family, same-tier) vs. (cross-family, cross-tier) and reported beside H4a.
- **Statistical test:** Permutation test on the family split, respecting task-level clustering, Holm-corrected across domains.
- **Expected outcome:** Mean within-family pairwise agreement exceeds cross-family by ≥ 0.10 absolute, Holm-corrected p < 0.05 — same-vendor backbones agree more than cross-vendor pairs.
- **Falsification condition:** Refuted if the gap is under 0.10 absolute or non-significant (Fallback F-4: instability is idiosyncratic, not family-structured — per-backbone re-validation cannot be amortized within a family).
- **Metrics:** Within-family versus cross-family mean pairwise agreement and permutation-test p-value; pair counts per arm reported per the INCONCLUSIVE rule.

## RQ7 — Is censoring (fault recovery) structured by backbone capability?

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_family_capability_structure`.
- **Target hypothesis (verbatim, paper.md Step 6, H4b):** "backbone fault-recovery rate correlates with clean-run capability, Spearman ρ ≥ 0.5, p < 0.05 (censoring is capability-skewed)."
- **Setup:** Each backbone's fault-recovery rate (fraction of injected cells it does not fail on) is correlated with its clean-run capability (clean-run task success rate) across the Stage-2 backbone grid.
- **Sample-size rationale:** Shares RQ6's family × capability-tier backbone grid (2 sizes per family where available) — one crossed design yields both the within/cross-family agreement contrast (RQ6) and the recovery-rate-vs-capability correlation (RQ7) as two slices of the identical grid, not two separate studies.
- **Statistical test:** Spearman's ρ between per-backbone fault-recovery rate and clean-run success rate.
- **Power note (amended 2026-08-21 per `review_2026-08.md` finding 3):** at K = 6–8 backbones the exact-permutation two-sided α = 0.05 critical value for Spearman's ρ is ≈0.89 / 0.79 / 0.74 (K = 6/7/8), so "ρ ≥ 0.5 **and** p < 0.05" was unconfirmable by construction. The confirmatory threshold is now the exact critical value at the realized K; ρ ∈ [0.5, threshold) is pre-declared suggestive-INCONCLUSIVE (descriptive, with CI); the ρ point estimate + task-level cluster-bootstrap CI is the primary reported quantity.
- **Expected outcome:** Fault-recovery rate correlates positively with clean-run capability — confirmed if ρ meets the K-adjusted exact threshold; stronger backbones recover more often, so the failing intersection $\mathcal{I}$ is systematically skewed toward weaker backbones.
- **Falsification condition:** Refuted if ρ < 0.5 (point estimate below the pre-registered effect floor) — Fallback F-4 also covers this outcome jointly with RQ6's failure (attribution instability idiosyncratic).
- **Metrics:** Spearman ρ between per-backbone fault-recovery rate and clean-run success rate.

## SC1 — Instrument-validation sensitivity check (formerly RQ6): Is the codebook's tie-break rule doing real work, or is residual disagreement concentrated in backbone effects regardless of which rule is used?

- **Tier:** Instrument-validation sensitivity check — not a headline RQ; excluded from the RQ tier accounting, feeds no aggregation vote and no fallback rule.
- **Target sub-problem:** `sp_taxonomy_ambiguity`.
- **Target hypothesis (verbatim, `pipeline.md` Stage 5, `m_codebook_tiebreak_gate`):** "Re-scoring the Stage-2 grid under the alternative tie-break rule changes the primary stability-band verdict (stable / partially stable / model-specific) in no more than one of the tested (backbone × domain) cells, showing residual disagreement concentrates in backbone effects rather than tie-break sensitivity."
- **Status note (resolved 2026-07-05):** this check's target threshold has **no corresponding H-id in `paper.md`'s Step 6 hypothesis list (H1/H1b/H2/H3a/H3b/H4a/H4b) or Claim–Evidence Map** — a pre-existing cross-artifact gap logged at Phase G (`stage_review.md`, `pipeline.md`). Per the second of the two resolutions that log pre-approved, it is now **demoted from headline RQ6 to instrument-validation sensitivity check SC1** rather than back-ported into `paper.md` as a new H5 — no pre-registration-level hypothesis construction is performed under drafting-time incentives (goal.md §6). The target hypothesis above is reproduced verbatim and unchanged; SC1's re-scoring is reported beside the headline results as a sensitivity, exactly as `paper.md`'s Codebook Tie-Break Gate already specifies.
- **Setup:** The full Stage-2 grid is re-scored under an alternative (latest-decisive-layer) tie-break rule, holding every other design choice fixed; the primary stability-band verdict is compared per (backbone × domain) cell under each rule.
- **Sample-size rationale:** Reuses the full Stage-2 grid (no separate data collection); paper.md's Instrument-validation step ⑤ requires the codebook and tie-break rule to be hashed and frozen before Stage 1/2 run, so this is a re-scoring of already-collected labels, not a new sampling exercise.
- **Statistical test:** Cell-by-cell verdict-change count under the two tie-break rules (descriptive comparison, not a significance test — no pre-registered α or effect floor is stated for this check in either source document).
- **Expected outcome:** The stability-band verdict changes in no more than one tested (backbone × domain) cell — residual disagreement is concentrated in backbone effects (RQ1–RQ3), not in codebook convention.
- **Falsification condition:** Refuted if the verdict changes in more than one cell — a meaningful share of the headline stability finding would then be an artifact of an arbitrary codebook convention, and the codebook would need to be treated as a confound in every headline RQ.
- **Metrics:** Count and identity of (backbone × domain) cells whose stability-band verdict changes across tie-break rules.

---

## Mixed-outcome and global fallback rules (pre-committed, `paper.md` Step 6)

1. **B0-fail dominates everything**: if the B0 premise gate fails (cross-backbone disagreement does not exceed within-backbone disagreement + 0.05 absolute), no other fallback is used — the only licensed claim is "attribution labels are noisy, full stop."
2. **F-C0 pre-empts RQ1–RQ5 fallbacks**: if Ω < 0.2 and mean pairwise overlap < 0.2 (extreme censoring), RQ1/RQ2/RQ4/RQ3/RQ5's hypotheses are reported INCONCLUSIVE (not failed); the censoring structure itself becomes the headline finding and RQ7 (H4b) is promoted to primary.
3. **F-G1 fires only on joint failure**: RQ1 fails toward "stable" **and** RQ3+RQ5 both fail **and** RQ6+RQ7 both fail or are INCONCLUSIVE — only then does the archetype pivot from measurement-of-instability to certification-protocol.
4. **B-alt-wins composes with RQ1's fallback, not F-G1**: if the style-normalization rival explanation wins (disagreement on human-judged normalized traces collapses to the B0 floor), the judging-artifact wording replaces RQ1's mechanism gloss, but this does not by itself trigger the certification claim (F-G1).
5. **RQ3/RQ5 mixed outcomes**: RQ3 passes + RQ5 fails → "instability is judge-driven but not a surface-form artifact." RQ3 fails + RQ5 passes → "judges are interchangeable but uniformly style-sensitive."
6. **RQ6/RQ7 mixed outcomes**: RQ6 passes + RQ7 fails → "agreement is family-structured but censoring is not capability-skewed." RQ6 fails + RQ7 passes → "agreement is family-blind but the analyzable failure set is capability-skewed."
