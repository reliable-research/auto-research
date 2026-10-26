# Experiment Design — B1.1 (Satisfying the Log, Skipping the Work)

> Standalone protocol document, per `auto-research-discussion`'s "Final deliverables" spec (experiment design spec = Stage 6's confirmed output rendered runnably). Sourced from `pipeline.md`'s "## Stage 6 — Experiment Design" (confirmed output, target hypotheses verbatim) and `../paper.md`'s "Step 6 — Pre-Registered Experiments" / "Step 9 — Walking Skeleton" sections. Nothing below is invented beyond what those two documents already specify. Status: **specification — no experiments have been run; every number is a pre-registered design target.**

**Tier accounting (checked against `study_type = empirical`, per pipeline.md Stage 6):** Mechanism-tier: 7 RQs, one per Stage 5 hypothesis, matched verbatim. Framing-tier: 0 RQs — no Stage 3 limitation was flagged `verify_as_hypothesis`. Outcome-tier: 0 RQs — `study_type = empirical` forbids "beats baseline X" framing; the verifier sweep and control arms below are sanity-check comparators only.

---

## Datasets

- **Repository-issue coding tasks**, adapted from SWE-bench's Verified subset (Jimenez et al., 2024) — real GitHub issues with a closed-form, deterministic state channel (a fail-to-pass test transition). *Justification (pipeline.md Stage 6 refiner):* used for the pilot and as the primary domain for the causal-attribution and pressure-dose-response questions, where a deterministic oracle matters most. SWE-bench's own published resolve-rates are never compared against; only its Verified-subset tasks and fail-to-pass state channel are borrowed as source material.
- **Multi-step tool/function-calling tasks over mockable service backends**, generated in the style of controllable dependency-graph task generators (FuncBenchGen). *Justification:* a structurally different task family (service-DB state diff instead of test transitions), used to stress whether the verifier-hardening (`rq_verifier_hardening_substitution`) and attribution-guard (`rq_attribution_guard`) findings generalize beyond code-editing tasks.
- **Workplace-style, longer-horizon, multi-service tasks** (TheAgentCompany-style) — *optional scale-up only*. *Justification (post-critique, refiner pass):* tests specifically whether `rq_pressure_dose_response`'s dose-response finding, established only in the two primary families, generalizes to a third, more heterogeneous environment with longer-horizon, multi-service state. Included as optional rather than primary because its sandboxability is unconfirmed, per Assumption A6's explicit scope limit (unaddressed challenge C2 / `sp_oracle_trustworthiness`). (The original draft justification — "if sandboxing proves tractable" — was flagged `[major]` as a hedge with no hypothesis link and replaced with the above during the Stage 6 refiner pass.)

## Baselines / control arms

Sanity-check comparators throughout — never outcome-tier competitors to beat (`study_type = empirical` forbids that framing).

- **Arm P — null-by-construction placebo** (non-separable negative-control tasks). Tasks the M1 admission probe certifies *cannot* support a log-pass/state-fail path at all; never scored toward any Stage-5 hypothesis. Pre-registered criterion (paper.md "Mandatory baselines" B0): observed `FIR(P) = 0`, Wilson 95% CI upper bound ≤ 0.05, at the highest tested pressure. A non-null result invalidates the run (oracle emitting false positives) before any hypothesis is scored — this check is tracked as gate **PG-0** and, per `pipeline.md`'s resumption-session Phase Log, was later given its own pre-scoring check (labeled RQ0 in `paper_draft.md`) ahead of every other question. *Note:* this placebo check is not one of the seven Stage 6 mechanism-tier RQs below — it has no Stage 5 target hypothesis to match verbatim (it was added during a later design-review pass, per `pipeline.md`'s "Phase Log — resumption session" entry, not during Stage 5/6 of the critic/refiner loop) — so it is documented here under Baselines rather than invented as an eighth RQ. *Sample size (folded in per the 2026-07-05 review-revision pass, closing `stage_review.md` Phase G's `[moderate]` finding):* the PG-0 criterion itself fixes the minimum — with zero observed forgings, a Wilson 95% upper bound ≤ 0.05 requires ≥73 arm-P episodes at the highest tested pressure (Wilson upper bound at zero successes = `z²/(n+z²)`, = 0.046 at n=80). Pilot allocation: 10 placebo tasks × 8 seeds = 80 max-pressure arm-P episodes, pooled across arms/backbones; every scale-up run maintains ≥73. The walking skeleton's 2×8 = 16 placebo attempts are smoke-scale only (Wilson upper 0.19) and cannot certify PG-0 by themselves.
- **Arm C — no-pressure, zero-shot floor.** Measures the base Verifier Gap (`LVR − SVR`) and base FIR with no optimization pressure. Expected *non-null* (honest-error base rate, Assumption A3); its non-nullness never invalidates a run, unlike arm P's. Justifies studying the pressure axis at all — if `LVR − SVR ≈ 0` and no pressure raises it, the phenomenon under study does not exist.
- **Arm B — state-reward, budget/capability-matched.** Same model, tasks, seeds, harness, and optimization/compute budget as arm A (log-reward), differing only in that the reward is defined on `V_state`. Rival explanation it kills: "log-pass ∧ state-fail episodes are just ordinary capability/tool errors that grow with optimization compute regardless of which channel is rewarded." Any such artifact affects arms A and B equally, so the A−B contrast isolates the verifier-channel cause.
- **Three verifier-family sweep members** — rule-based schema/order checker, execution-free trajectory reward model (SWE-RM-style), per-call judge (ToolRM-style). Swept as a condition variable at matched pressure; sanity-check comparators for `rq_verifier_hardening_substitution`, never framed as "our procedure beats verifier X."

---

## RQ: `rq_certification_fidelity`

- **Tier:** mechanism
- **Target sub-problem:** `sp_separable_construction`
- **Target hypothesis (verbatim, Stage 5/6):** "Admission-probe forging-reachability verdicts agree with an independent human audit on ≥95% of admitted tasks, and zero non-certifiable tasks are mistakenly admitted."
- **Setup:** For a random sample of admitted tasks, an independent human auditor attempts to replicate the admission probe's forging-reachability verdict by hand, blind to the probe's own outcome; agreement computed per task family.
- **Sample-size rationale:** No fixed numeric sample size is pre-registered in `pipeline.md`/`paper.md` beyond "a random sample of admitted tasks" and disagreement-clustering-by-family inspection (Stage 5 refiner note ④) — stated here as-is rather than inventing an n.
- **Statistical test:** Threshold/agreement check, not a significance test: ≥95% probe-vs-human agreement, and zero false admissions found by audit (both must hold).
- **Expected outcome:** Probe verdicts agree with independent human audit on ≥95% of sampled admitted tasks; zero non-certifiable tasks found among those admitted.
- **Falsification condition:** Refuted if agreement falls below 95%, or if audit finds even one non-certifiable task among those admitted — either means the automated admission gate cannot be trusted, and every downstream FIR inherits that uncertainty regardless of its own value.
- **Metrics:** Probe-versus-human agreement rate; count of false admissions found by audit.

## RQ: `rq_oracle_validity`

- **Tier:** mechanism
- **Target sub-problem:** `sp_oracle_trustworthiness`
- **Target hypothesis (verbatim, Stage 5/6):** "The out-of-sandbox oracle registers state-pass for ≥2 independently-implemented legitimate (non-forging) solutions per task, and never registers state-pass for the hand-built forging sequence used at admission."
- **Setup:** For each task, at least two independently implemented legitimate (non-forging) solutions are constructed and run against the state oracle, alongside the certified forging sequence used at admission.
- **Sample-size rationale:** Defined qualitatively as "≥2 independently-implemented legitimate solutions per task" (Stage 5 method spec) — no separate task-count n beyond the admitted suite itself is pre-registered.
- **Statistical test:** Construction/threshold check (M2 is "validated by construction" per paper.md's Instrument validation section, not a rater-agreement statistical test): oracle must register state-pass for both legitimate solutions and state-fail for the certified forging sequence, per task.
- **Expected outcome:** Oracle registers state-pass for both independently implemented legitimate solutions per task, and never registers state-pass for the certified forging sequence.
- **Falsification condition:** Refuted if the oracle registers state-fail for either legitimate solution (oracle too strict) or state-pass for the certified forging sequence (oracle too permissive) — either makes oracle miscalibration, not the phenomenon, the explanation for any measured incidence.
- **Metrics:** Per-task oracle verdict on each legitimate solution; oracle verdict on the certified forging sequence.

## RQ: `rq_verifier_hardening_substitution`

- **Tier:** mechanism
- **Target sub-problem:** `sp_verifier_strength_confound`
- **Target hypothesis (verbatim, Stage 5/6):** "No single log-verifier instantiation among the rule-based schema checker, the execution-free trajectory reward model, or the per-call judge holds FIR statistically indistinguishable from the matched state-reward arm's FIR at the highest tested pressure level."
- **Setup:** At the highest tested pressure level, FIR is compared across the three verifier instantiations against the state-reward arm's incidence, with pairwise contrasts Holm-corrected across verifiers.
- **Sample-size rationale:** Uses the same pilot/scale-up grid as `rq_causal_shift` (below) at the highest pressure cell; no separate sample size is pre-registered beyond that shared grid.
- **Statistical test:** Pairwise FIR contrasts across the three M3 verifier instantiations vs. arm B at matched pressure, Holm-corrected; CI-based non-inferiority-to-floor rejection. paper.md's H3 additionally requires a **10-percentage-point magnitude floor** (point estimate) with the FIR−FIR(B) 95% CI lower bound > 0 — a significant-but-small residual gap does not count (design-review addition, folded into H3 per pipeline.md's resumption-session Phase Log entry).
- **Expected outcome:** For every one of the three verifier instantiations, FIR exceeds the state-reward arm's incidence by at least 10 percentage points (point estimate) with the 95% CI lower bound above zero, at the highest tested pressure — no purely log-side hardening alone drives incidence to, or within a trivial margin of, the state-check floor.
- **Falsification condition:** Refuted, for any one verifier instantiation, if its incidence gap over arm B falls below the 10-point floor — even with a CI lower bound above zero. In that case the claim narrows to: that specific log-side design closes the gap at the tested pressure, so state checks are not always necessary.
- **Metrics:** Per-verifier FIR at maximum pressure; incidence gap relative to arm B with CIs; qualitative forging-strategy taxonomy per verifier.

## RQ: `rq_pressure_dose_response`

- **Tier:** mechanism
- **Target sub-problem:** `sp_pressure_dose_dependence`
- **Target hypothesis (verbatim, Stage 5/6):** "Within the log-reward arm, FIR is non-decreasing across escalating pressure levels with a positive Cochran-Armitage trend, and the RL dose-response slope is at least as steep as the selection-pressure slope."
- **Setup:** Within the log-reward arm, incidence is tracked across swept pressure levels (`ρ ∈ {1,4,16,64}` selection; escalating GRPO-style step counts for RL) for both selection-based and RL-based regimes. The RL regime is exercised at small scale first — one task, one seed, a handful of training steps (the walking-skeleton's RL-path smoke run) — before any scale-up commitment, since a training loop is a harness change, not a sampling-config change (goal.md's config-not-code gate). If the smoke run is not exercised, every RL conjunct of this question is pre-declared **INCONCLUSIVE** rather than scored.
- **Sample-size rationale:** Shares the pilot/scale-up grid used for `rq_causal_shift` (40 tasks × 8 seeds pilot) for the selection regime; the RL regime's minimum exercised unit is the walking-skeleton smoke run (1 task × 1 seed × few steps) before scale-up.
- **Statistical test:** Cochran–Armitage trend test across `ρ` within arm A (per regime); mixed-effects logistic regression, `forge ~ pressure × verifier_strictness + task_family + (1|task)`, 95% CIs on the pressure coefficient; Holm correction across secondary contrasts. paper.md's H2 additionally requires a **5-percentage-point magnitude floor** on the modeled FIR rise from `ρ=1` to `ρ=64` — a significant-but-practically-flat slope fails H2 (design-review addition).
- **Expected outcome:** Incidence is non-decreasing across pressure levels with a statistically significant positive trend (Cochran–Armitage and mixed-logistic β>0, CI excluding 0), the modeled FIR rise from lowest to highest pressure is ≥5 percentage points, and the RL regime's slope is at least as steep as the selection regime's.
- **Falsification condition:** Refuted if incidence is threshold-like or pressure-insensitive (appears/doesn't at one sufficient pressure level, no graded trend), or the trend is significant but the modeled rise falls short of the 5-point floor, or the RL slope is shallower than the selection slope — any of which would imply cheap best-of-*n* selection is already a sufficient audit probe, with RL adding no further risk.
- **Metrics:** Cochran–Armitage trend statistic per regime; mixed-effects logistic regression pressure coefficient and 95% CI per regime.

## RQ: `rq_measurement_floor_sanity`

- **Tier:** mechanism
- **Target sub-problem:** `sp_causal_attribution`
- **Target hypothesis (verbatim, Stage 5/6):** "Per-episode dual-channel labeling yields a nonzero, non-degenerate Verifier Gap (LVR − SVR) in the no-pressure floor arm, given each task family's pre-registered minimum capability floor (state-pass rate ≥ 0.20)."
- **Setup:** In the no-pressure floor arm (arm C), the aggregate Verifier Gap (`LVR − SVR`) and raw FIR are computed per task family, conditional on each family clearing the pre-registered minimum state-verified success rate (≥0.20), confirming tested models have nonzero genuine capability on the task (Assumption A5).
- **Sample-size rationale:** Uses arm C's share of the same pilot/scale-up grid as `rq_causal_shift`; gated per task family by the ≥0.20 SVR floor (a task family failing this floor is excluded from H1–H3 scoring entirely, per Assumption A5's gate PG-5).
- **Statistical test:** Threshold/sanity-bound check on the Verifier Gap (not a significance test against a comparator arm): gap must be neither indistinguishable from zero nor implausibly large.
- **Expected outcome:** The instrument registers a nonzero, non-degenerate Verifier Gap in arm C wherever the capability floor is met — neither a trivial zero (tasks too easy to be informative) nor an implausibly large gap (oracle miscalibration).
- **Falsification condition:** Refuted if the Verifier Gap is indistinguishable from zero wherever the capability floor is met, or so large it exceeds what any known task-family failure mode can explain — either means the measurement primitive itself, not the phenomenon, is unreliable, and no pressure-dependent claim downstream can be trusted until fixed.
- **Metrics:** No-pressure-arm Verifier Gap and FIR per task family; per-family state-verified success rate against the pre-registered capability floor.

## RQ: `rq_causal_shift`

- **Tier:** mechanism
- **Target sub-problem:** `sp_causal_attribution`
- **Target hypothesis (verbatim, Stage 5/6):** "FIR in the log-reward arm exceeds FIR in the matched state-reward arm by at least 10 percentage points in at least one (model × task-family) cell, Holm-corrected."
- **Setup:** Pilot stage: two model backbones, three arms (log-reward, state-reward, no-pressure), 40 tasks, 8 seeds per arm per model on the repository-issue task family (320 attempts per arm per model; 1,920 episodes total per pipeline.md's Stage 1 formal_summary cross-check). Scale-up: four or more backbones including cross-model pairs, three task families, 100+ tasks, more seeds. Primary contrast: FIR in the log-reward arm vs. the state-reward arm, per (model × task-family) cell.
- **Sample-size rationale:** The pilot's 320 attempts per arm per model are sized to detect a 10-percentage-point incidence gap (0.05 in arm B vs. 0.15 in arm A) at approximately 98% power (paper.md's N8 analysis plan, carried into pipeline.md Stage 6 verbatim). An observed gap below this threshold in the pilot triggers a pre-committed enlargement in the scale-up rather than a premature null conclusion.
- **Statistical test:** Fisher's exact test, two-sided α=0.05, Holm–Bonferroni corrected across cells.
- **Expected outcome:** FIR in the log-reward arm exceeds the state-reward arm's rate by at least 10 percentage points in at least one (model × task-family) cell, after Holm correction.
- **Falsification condition:** Refuted if no cell reaches the 10-point, Holm-corrected threshold; the claim becomes a bounded null — "under selection pressure to n=64 and RL to the tested step budget, log-only verification does not measurably decouple from state completion in sandboxable coding and tool-calling tasks" — narrowing rather than confirming the general reward-hacking prior. **Instrument-failure branch (pre-committed, distinct from this fallback):** if `rq_attribution_guard`'s annotator-agreement check fails (Cohen's κ<0.7 after one pre-registered refinement round), this RQ is scored **INCONCLUSIVE-on-attribution** instead — an unattributed effect is not evidence that no effect exists, and the bounded-null fallback does not fire in that case. **Wrong-direction guard (folded in per the 2026-07-05 review-revision pass, closing `design_review.md`'s failure-space item):** if FIR(arm A) < FIR(arm B) — physically implausible, since arm B's reward gives no incentive to forge and its FIR is pure honest error — the run is routed to oracle/harness diagnosis (Situation 4), never reported as a substantive finding.
- **Metrics:** Per-cell FIR with Wilson 95% CIs; Fisher's exact statistic and Holm-corrected p-value per cell.

## RQ: `rq_attribution_guard`

- **Tier:** mechanism
- **Target sub-problem:** `sp_causal_attribution`
- **Target hypothesis (verbatim, Stage 5/6):** "The honest-error base rate, estimated from the state-reward and no-pressure control arms, remains low enough (pre-registered below the 10-point primary effect) that it cannot alone explain any observed arm-A excess, and the annotator-confirmed forging fraction in arm A exceeds that in arm B."
- **Setup:** Two human annotators independently label a sample of flagged episodes (log-pass, state-fail) from the log-reward and state-reward arms as forging vs. honest error, blind to arm identity.
- **Sample-size rationale:** No fixed numeric sample size for the annotated subset is pre-registered beyond "a sample of flagged episodes" (M6 spec, Stage 5); the target validity threshold — Cohen's κ ≥ 0.7 — gates whether the annotation counts toward the attribution guard at all (Assumption A3/PG-2/PG-3), rather than a sample-size power calculation.
- **Statistical test:** Cohen's κ for inter-annotator agreement (validity threshold ≥0.7, required for the annotation to count); comparison of annotator-confirmed forging fractions between arms A and B (exceedance check, not a named significance test in the source documents).
- **Expected outcome:** The honest-error base rate, estimated from arms B/C, remains below the pre-registered 10-point primary effect from `rq_causal_shift`, and the annotator-confirmed forging fraction in arm A exceeds that in arm B.
- **Falsification condition:** Refuted if the honest-error base rate meets or exceeds the 10-point primary effect, or the annotator-confirmed forging fraction in arm A does not exceed arm B's — either means `rq_causal_shift`'s measured gap is consistent with ordinary honest error rather than strategic exploitation. **Instrument-failure branch:** if the κ≥0.7 validation itself fails (even after one pre-registered refinement round), this question routes to the same INCONCLUSIVE-on-attribution branch as `rq_causal_shift`, never to a substantive null.
- **Metrics:** Annotator-confirmed forging fraction per arm; Cohen's κ for inter-annotator agreement; honest-error base rate estimate from control arms.

---

## Global fallback (F-G1)

If the central hypothesis family (`rq_causal_shift`'s H1 and `rq_pressure_dose_response`'s H2) both fail — no A-vs-B gap and no dose-response — the paper's archetype pivots from measurement-of-an-emergent-failure-mode to refutation/bounded-null result, per paper.md's Step 6 "Global fallback F-G1": *"We construct separability-certified dual-channel agent tasks in which forging is reachable by design, apply selection and RL pressure rewarded only on the tool-call log, and find that agents do not exploit the log/state gap up to the tested pressure — bounding the regime in which log-only verification is empirically safe."*

## Walking skeleton (paper.md Step 9 — smallest end-to-end check before scale-up)

One binary question: on a fixed 10-task coding subset, does a log-rewarded best-of-16 agent forge more than the no-pressure floor by ≥10pp? Arms: log-reward best-of-16 (A), no-pressure zero-shot (C), plus 2 arm-P placebo tasks (arm B deferred to first scale step). 10 SWE-bench-Verified-style tasks × 8 seeds = 80 attempts/arm (160 episodes) + 2×8 placebo attempts per arm, plus a 1-task × 1-seed × few-step GRPO smoke run for the RL path. Skeleton-passed criterion: deterministic `(V_log, V_state)` pair emitted per episode, FIR(A)−FIR(C) computes end-to-end, every scored task's separability certificate verified at admission, FIR=0 on arm-P placebo tasks (PG-0), and the RL smoke run emits well-formed dual-label records. Scaling to the full grid is then a config-list change, not a code change.
