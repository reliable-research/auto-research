# Experiment Design — B6.5: Is Corpus-Level Estimation Strategy-Proof?

> Standalone protocol document. Rendered from Stage 6's confirmed output in `pipeline.md` ("## Stage 6 — Experiment Design", now moved verbatim into `discussion_trace.md`) plus `../paper.md`'s Step 6 ("Pre-Registered Experiments") / Step 9 ("Walking Skeleton") and the corresponding `paper_draft.md` "Experiments" section. Nothing below is invented — every setup, sample-size, statistical-test, expected-outcome, and metric line is carried over from one of those three already-confirmed sources. Status: **specification — no experiments have been run.** All numbers are pre-registered design targets, not results.
>
> **Tier accounting (from `pipeline.md` Stage 6):** Mechanism-tier: **7 RQs**, one per Stage 5 hypothesis (verbatim). Framing-tier: **0** (no Stage 3 limitation was flagged `verify_as_hypothesis`). Outcome-tier: **0** (`study_type = empirical` forbids "beats baseline X" framing — the naive-average and debias-vs-MLE comparisons are diagnostic isolations, not competitor comparisons).

---

## Datasets

- **RAID** (Dugan et al., 2024) — a large multi-domain, multi-generator machine-generated-text benchmark including adversarial/paraphrase variants. *Justification:* supplies at least three generator families (GPT-, Llama-, Claude-class) so the scaling result is not an artifact of one generator.
- **HC3** (Human ChatGPT Comparison Corpus, Guo et al., 2023) — paired human/LLM answers to the *same prompts*. *Justification (refined in Stage 6's refiner pass):* gives the tightest available control for constructing controllable-$\alpha$ semi-synthetic corpora with minimal topical confound between the human and AI portions. This directly stresses `rq_ground_truth_recovery_validity`'s shuffled-label control: if human and AI text differed systematically in topic (as they might from unpaired sources), an estimator could recover $\alpha$ by exploiting topic rather than authorship signal, and the shuffled-label check alone might not catch a *topic-correlated* shortcut. HC3's matched-prompt pairing is what makes that specific failure mode a real risk worth ruling out, rather than one simulated away by construction.
- **Semi-synthetic mixed corpora**, built from RAID + HC3, with an experimenter-controlled ground-truth AI-generation proportion $\alpha$. *Justification:* the only way to make $e_B(N)$ computable at all (no real corpus has verifiable ground truth), mirroring `[MonitorAIScale]`'s own semi-synthetic validation protocol.

## Baselines

Both are sanity-check comparators, not outcome-tier competitors — consistent with `study_type: empirical`, which forbids "our estimator beats baseline X" framing.

- **B0 — "why do this at all" control:** population-scale single-document detection = mean of per-document detector ($g$) verdicts, no distributional estimator, no calibration. This is what a practitioner does absent this paper's framing. Expected to inherit single-document fragility ($e_B$ large, tracking AUROC collapse). If B0 is *already* strategy-proof, the whole distributional-estimator apparatus is unjustified and there is no problem to solve. (This control is promoted to a full method with its own falsifiable hypothesis as `m_naive_average_control` / `rq_naive_average_vs_dedicated` below, rather than left as an unexamined sanity check.)
- **B-alt — "strongest-alternative-explanation" control:** a budget- and capability-matched adaptive/coordinated adversary (DPO-tuned paraphraser à la `[AdaptiveWMAttack]`, optimizing a surrogate of $\hat\alpha$), run at identical budget to the non-adaptive DIPPER-style adversary. **Rival explanation it kills:** "the observed corpus-level robustness is an artifact of a weak, non-adaptive adversary; a competent budget-matched attacker evades just as cheaply, so robustness is not scale-driven." (Instantiated as `m_coordinated_adversary_arm` / `rq_coordination_budget_parity` + `rq_coordination_scaling_persists` below.)

## Shared experimental grid (`paper.md` Step 6)

- Corpus sizes: $N \in \{10^2, 10^3, 10^4, 10^5\}$.
- 5 seeds per (N, strategy, estimator) cell.
- Bias margin target: $\varepsilon = 0.10$.
- Cost models: $c \in \{\text{per-token}, \text{per-document-touched}\}$ (non-nested — see `rq_cost_model_sign_invariance` below).
- Generators: $\ge 3$ families (GPT-, Llama-, Claude-class) from RAID.
- Base corpora: RAID + HC3.

**Power statement (`paper.md` Step 6).** 5 seeds × ≥3 generators per (N, strategy, estimator) cell is the pre-registered minimum designed to detect the stated effect floors (e.g. $\hat\beta \ge 0.5$ for the scaling-exponent RQs, a $\ge 2\times$ ratio for the naive-average confound RQ) at power $\ge 0.8$ under a conservative assumed effect size; achieved power is checked post-hoc from the realized bootstrap CI width. Any cell whose post-hoc power falls below 0.8 (CI too wide to distinguish the effect floor from the null at $\alpha = 0.05$) is pre-declared **INCONCLUSIVE**, never scored as a null result and never silently dropped from the reported grid.

**Design constraints and the confound each removes (`paper.md` Step 6).**
- Matched-prompt HC3 pairing removes the *topic confound* (an estimator could otherwise recover $\alpha$ by exploiting topic rather than authorship signal) — stresses `rq_ground_truth_recovery_validity`.
- The shuffled-label negative control removes the *trivial-recoverability confound* — `rq_ground_truth_recovery_validity`.
- Reporting $\hat\beta$ under both declared cost models removes the *cost-model-artifact confound* — `rq_cost_model_sign_invariance`.
- The adaptive/coordinated adversary arm removes the *weak-attacker confound* — `rq_coordination_budget_parity` / `rq_coordination_scaling_persists`.
- The naive per-document-average estimator control removes the *generic-averaging confound* — `rq_naive_average_vs_dedicated`.

---

## Research Questions

All 7 RQs below are **mechanism-tier**, each matching a Stage 5 hypothesis verbatim (`pipeline.md` Stage 6, cross-stage consistency check item 3: "every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓").

### RQ — `rq_coordination_budget_parity`

- **Tier:** mechanism
- **Target sub-problem:** `sp_coordinated_evasion`
- **Target hypothesis (verbatim, Stage 5 `m_coordinated_adversary_arm`):** "The adaptive/coordinated adversary requires no less budget than the non-adaptive adversary to bias $\hat\alpha$ by margin $\varepsilon=0.10$ at matched corpus size — budget-matched coordination does not defeat the aggregation-based robustness advantage."
- **Setup:** At a fixed corpus size, train the coordinated adversary against a surrogate of the corpus estimator via preference optimization on best-of-N rewrite candidates (no gradient access to the true estimator assumed), then measure the minimum budget each of the coordinated and non-adaptive adversaries requires to bias the estimate by margin $\varepsilon = 0.10$, at matched corpus size and cost model.
- **Sample-size rationale:** 3–5 seeds per adversary type, repeated across the same generator families used elsewhere in the shared grid (paper_draft.md Experiments; consistent with the shared grid's 5-seeds-per-cell power target).
- **Statistical test:** Minimum budget to reach $\varepsilon = 0.10$ is compared between adversary types via the ratio of coordinated-to-non-adaptive minimum budget, with a bootstrap confidence interval.
- **Expected outcome:** The coordinated adversary requires no less budget than the non-adaptive adversary to reach the same bias margin — the aggregation-based robustness advantage does not depend on the adversary being uncoordinated.
- **Metrics:** Minimum budget to reach $\varepsilon = 0.10$ for each adversary type; ratio of coordinated-to-non-adaptive minimum budget with bootstrap confidence interval.

### RQ — `rq_coordination_scaling_persists`

- **Tier:** mechanism
- **Target sub-problem:** `sp_coordinated_evasion`
- **Target hypothesis (verbatim, Stage 5 `m_coordinated_adversary_arm`):** "If the adaptive adversary requires strictly less budget than the non-adaptive one to achieve the same bias margin, the fitted scaling exponent $\beta$ will still have a 95% CI lower bound $>0$ under the adaptive adversary — coordination narrows but does not eliminate the scale-taxed cost structure."
- **Setup:** Conditional on `rq_coordination_budget_parity` finding a budget reduction under coordination, repeat the full corpus-size sweep and log-log regression of minimum budget against $N$ using the coordinated adversary in place of the non-adaptive one, at the primary cost model.
- **Sample-size rationale:** Same shared-grid cells (5 seeds × ≥3 generators per N) as the primary (non-adaptive) scaling sweep, re-run under the coordinated adversary.
- **Statistical test:** Bootstrap 95% CI on $\hat\beta$ (OLS log-log slope of minimum budget on $N$) under the coordinated adversary, compared against the non-adaptive-adversary $\hat\beta$; criterion is CI lower bound $>0$.
- **Expected outcome:** The fitted scaling exponent $\hat\beta$'s 95% bootstrap CI lower bound remains greater than 0 under the coordinated adversary — coordination may narrow the scaling advantage but does not eliminate it.
- **Metrics:** $\hat\beta$ under the coordinated adversary, with bootstrap 95% CI, compared against the non-adaptive-adversary $\hat\beta$.

### RQ — `rq_cost_model_sign_invariance`

- **Tier:** mechanism
- **Target sub-problem:** `sp_cost_model_ambiguity`
- **Target hypothesis (verbatim, Stage 5 `m_cost_model_invariance`):** "The fitted scaling exponent $\beta$ has a 95% CI lower bound $>0$ under both the per-token and the per-document-touched cost models, not only under whichever model happens to be reported."
- **Setup:** Sweep corpus size $N \in \{10^2, 10^3, 10^4, 10^5\}$ under the non-adaptive adversary, fitting the minimum budget to bias $\varepsilon = 0.10$ separately under a per-token-rewritten cost model and a per-document-touched cost model, 3–5 seeds per (N, cost model) cell.
- **Sample-size rationale:** 3–5 seeds per (N, cost model) cell across the full N grid, matching the shared grid's per-cell seed count.
- **Statistical test:** Pre-registered one-sided test $H_0: \beta \le 0$ vs. $H_1: \beta > 0$ at $\alpha = 0.05$; bootstrap 95% CI on $\hat\beta$ over seeds; require CI lower bound $>0$ **and** point estimate $\ge 0.5$ in **both** cost models (`paper.md` Step 6 RQ_INF_1 verification).
- **Expected outcome:** The fitted scaling exponent $\hat\beta$ has a 95% bootstrap CI lower bound greater than 0, with a point estimate at or above 0.5, under both cost models.
- **Metrics:** $\hat\beta$ per cost model with bootstrap 95% CI; sign agreement across cost models.
- **Fallback (`paper.md` Step 6 RQ_INF_1):** IF $0 < \hat\beta < 0.5$ but CI excludes 0 → weaker claim "Evasion cost grows sublinearly with corpus size — cheaper than proportional but not free." IF CI includes 0 or $\hat\beta \le 0$ → "Aggregate-estimate evasion cost does not grow with scale" (refutes central claim). IF the two cost models disagree in sign → reported as cost-model-dependent, unresolved, not resolved by reporting only the favorable cost model.

### RQ — `rq_ground_truth_recovery_validity`

- **Tier:** mechanism
- **Target sub-problem:** `sp_ground_truth_construction`
- **Target hypothesis (verbatim, Stage 5 `m_semisynthetic_ground_truth_design`):** "The clean corpus-level estimator recovers the experimenter-set $\alpha$ within a pre-registered tolerance across all tested corpus sizes, while a shuffled-label control's estimate deviates from $\alpha$ by significantly more than that tolerance."
- **Setup:** On each semi-synthetic corpus (no adversary present), run the clean corpus estimator and compare its recovered $\hat\alpha$ against the experimenter-set $\alpha$; separately, permute the human/AI labels independently of document content and rerun the identical estimator on this shuffled-label corpus. This is Assumption A1's gate (PG-1), checked inside the walking skeleton (Step 9) before any scale-up.
- **Sample-size rationale:** Run across all tested corpus sizes in the shared grid, consistent with A4's requirement that $e_0(N)$ be checked to shrink or plateau (not grow) across the N sweep.
- **Statistical test:** $|\hat\alpha - \alpha|$ for the clean and shuffled-label conditions, compared against the pre-registered tolerance.
- **Expected outcome:** The clean estimator recovers $\alpha$ within a pre-registered tolerance across all tested corpus sizes, while the shuffled-label control's estimate deviates from $\alpha$ by significantly more than that tolerance.
- **Metrics:** $|\hat\alpha - \alpha|$ for the clean and shuffled-label conditions.
- **Consequence if this fails (A1):** No H\* is scorable (there is no trustworthy ground truth to measure error against) — a placebo-style invalidation that blocks `rq_base_robustness_under_attack`, `rq_cost_model_sign_invariance`, and `rq_naive_average_vs_dedicated` alike until the corpus-construction procedure is fixed and re-piloted.

### RQ — `rq_base_robustness_under_attack`

- **Tier:** mechanism
- **Target sub-problem:** `sp_ground_truth_construction`
- **Target hypothesis (verbatim, Stage 5 `m_semisynthetic_ground_truth_design`):** "Under a fixed adversary budget $B$ that drives the paired single-document detector's AUROC to $\le 0.60$, the corpus-level (mixture-MLE) estimator's error $e_B(N)$ remains $\le 0.05$ and $\le 2\,e_0(N)$ at $N=10^5$ — establishing that corpus-level estimation resists the same budget that defeats single-document detection."
- **Setup:** At $N = 10^5$, apply the non-adaptive paraphrase adversary at a budget calibrated to drive the paired single-document detector's AUROC to at most 0.60; measure the corpus estimator's error under that same budget and compare it against its clean-error baseline. Requires Assumption A2 (single-document fragility premise) to hold — checked in the walking skeleton's M1 arm before scale-up.
- **Sample-size rationale:** 3–5 seeds × at least 3 generator families, Holm-corrected across generators (`paper_draft.md` RQ5 setup; `paper.md` Step 6 aggregation rule).
- **Statistical test:** Bootstrap 95% CI on $e_B$ (5 seeds × ≥3 generators); criterion met iff the CI upper bound $\le 0.05$ and the AUROC CI upper bound $\le 0.60$, with Holm correction across generators. Aggregation: criterion must hold on $\ge 2$ of the $\ge 3$ tested generator families (Holm-corrected per-family test at per-test $\alpha = 0.05/3$) — a single-generator pass does not qualify as PASS.
- **Expected outcome:** The corpus-level estimator's attacked error $e_B(10^5)$ remains at most 0.05 and at most twice its clean error $e_0(10^5)$, while the paired single-document detector's AUROC falls to at most 0.60 under the identical budget.
- **Metrics:** $e_B(N)$, $e_0(N)$, and $\mathrm{AUROC}(g; D_N')$ at $N = 10^5$, with bootstrap 95% CIs.
- **Fallback (`paper.md` Step 6 RQ1):** IF $e_B(10^5) > 2\,e_0(10^5)$ → claim "Corpus-level estimation inherits single-document fragility; aggregation confers no strategy-proofness at the tested scales" (publishable negative; feeds global fallback F-G1).

### RQ — `rq_debias_fragility_under_shift`

- **Tier:** mechanism
- **Target sub-problem:** `sp_debiasing_under_adversarial_shift`
- **Target hypothesis (verbatim, Stage 5 `m_naive_debias_control`):** "Under the fixed-budget adversary, the debias-and-aggregate estimator's error grows relative to its no-adversary baseline by more than the mixture-MLE estimator's does, at matched budget and corpus size — indicating the stationarity assumption is the more fragile of the two estimator designs."
- **Setup:** At matched corpus size and adversary budget, run both the primary likelihood-based (mixture-MLE) estimator and a debias-and-aggregate (`[DUCI]`-style) estimator under the identical non-adaptive adversary, comparing each estimator's attacked error against its own clean-error baseline.
- **Sample-size rationale:** Matched (N, B) cells from the shared grid, same seed count as the other estimator-comparison RQs.
- **Statistical test:** Relative error growth $e_B(N)/e_0(N)$ for each estimator design, with bootstrap 95% CI on the difference.
- **Expected outcome:** The debias-and-aggregate estimator's error grows relative to its no-adversary baseline by more than the likelihood-based estimator's does, at matched budget and corpus size — the stationarity assumption behind debiasing is the more fragile of the two estimator designs under this attack.
- **Metrics:** Relative error growth $e_B(N)/e_0(N)$ for each estimator design, with bootstrap 95% CI on the difference.

### RQ — `rq_naive_average_vs_dedicated`

- **Tier:** mechanism
- **Target sub-problem:** `sp_design_vs_scale_confound`
- **Target hypothesis (verbatim, Stage 5 `m_naive_average_control`):** "At matched N and B, the naive per-document-average estimator's error exceeds each dedicated estimator's (mixture-MLE, debias-aggregate) by at least 2×, with the ratio's 95% CI lower bound $\ge 2$ — indicating the robustness benefit is attributable to estimator design, not generic averaging."
- **Setup:** At matched corpus size and adversary budget, run the naive per-document-average estimator (B0) alongside both dedicated corpus estimators (mixture-MLE, debias-aggregate) under identical attack conditions.
- **Sample-size rationale:** Matched (N, B) cells from the shared grid, same seed count as the other estimator-comparison RQs.
- **Statistical test:** Paired bootstrap on the ratio $e_B^{\text{naive}}/e_B^{\text{dedicated}}$ per seed; criterion iff 95% CI lower bound $\ge 2$ (`paper.md` Step 6 RQ_INF_2 verification).
- **Expected outcome:** The naive estimator's attacked error exceeds each dedicated estimator's by at least 2×, with the ratio's 95% bootstrap CI lower bound at or above 2 — indicating the robustness benefit is attributable to estimator design, not to generic averaging over a large population.
- **Metrics:** $e_B(N)$ for the naive, mixture-MLE, and debias-aggregate estimators at matched $(N, B)$; ratio of naive to each dedicated estimator's error, with bootstrap CI.
- **Fallback (`paper.md` Step 6 RQ_INF_2):** IF naive-average is equally robust ($e_B^{\text{naive}} \le 1.25\,e_B^{\text{dedicated}}$) → claim "Robustness is a generic consequence of averaging over a large population, not of the specific estimator design" — reframes the design contribution but still supports the scale thesis.

---

## Global fallback (`paper.md` Step 6, F-G1)

IF the central hypothesis family fails (`rq_base_robustness_under_attack`'s fallback fires AND `rq_cost_model_sign_invariance` gives $\hat\beta \le 0$): **pivot archetype from "counterintuitive positive measurement" to "boundary-characterization / cautionary map."** Pivoted abstract sentence: *"We show that corpus-level AI-prevalence estimates inherit single-document evasion fragility, and we map the budget, coordination, and estimator regimes in which population-scale auditing gives practitioners a false sense of security."*

## Walking skeleton precondition (`paper.md` Step 9)

Before any scale-up, a single binary question is checked at one corpus size ($N = 10^3$, one generator family, HC3, $\alpha = 0.5$, 3 seeds): does the distributional estimator resist a fixed-budget adversary while the single-document detector collapses under the *same* attack? **Skeleton passed iff:** clean M2 recovers $\alpha$ within 0.03; M1 AUROC drops to $\le 0.60$ under paraphrase (A2 holds); M2-under-attack error is measurable and strictly below the B0 naive-collapse level. Passing means the full grid above is reachable by changing config lists only — no new estimator/adversary code paths.
