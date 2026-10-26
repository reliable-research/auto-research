# Review: B4.5 Autodiscussion Draft Package (2026-08-14)

**Package under review:** `/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB4.5 Which Trajectories Deserve Verification Allocating a Scarce Trusted Verifier--26859bdf/` (research-report.md, experiment-spec.md, paper-draft.md)
**Reference design:** `topics/B4.5_.../discussion.md` (6-stage critic→refine design doc, 2026-08-13)
**Reviewer note:** session WebSearch quota was exhausted after the first novelty query (200/200); remaining verification was done via WebFetch against arXiv API / GitHub for the specific closest neighbors surfaced by that query. Findings below are correspondingly conservative where marked.

---

## 1. Architecture of the draft (~10 lines)

1. Frozen pool: ~4,000 instances × 16 samples across four dataset–generator–verifier triples; samples grouped into answer-equivalence classes; one verifier call resolves a whole class (PASS/ELIMINATE).
2. Cheap signals: mode share, sequence log-likelihood percentile, verbalized confidence — rank-normalized, then clustered into **dependency families** (Spearman ≥ 0.8, complete linkage) so correlated signals get one vote.
3. **Actionability**: counterfactual pass/elim ledger simulation across full-family and leave-one-family-out views → decision-flip fraction + gap shift → magnitude score S(a).
4. **Value estimation**: cross-fitted state-value model q(s) and elimination-probability model p(s,a), trained purely on verifier-derived labels charged to the same budget (B = B_sweep + B_fit + B_eval, dev cap 0.4B), with path-covering label schedules, IPW truncation correction, calibration bins, and support-shift interval widening.
5. **Allocation**: receding-horizon width-32 beam search to depth 3 over a shortlist (top-2/instance, global top-128), a **shadow price λ** on first calls to unserved instances (marginal affordable instance), a priority guard on repeat calls, explicit STOP.
6. **Consensus-probe reserve** (ε=0.10 of B_eval): probes low-actionability all-family-consensus classes ranked by runner-up disagreement × shrunk calibration-gap prior — targets confidently wrong consensus invisible to value ranking.
7. **Aggregation**: total minimax-support-regret rule over family-capped votes; passed classes lexically first, eliminated classes removed with their support, forced decision even under all-eliminations.
8. Evaluation: R(B) = A_selective/A_full at per-triple budget fractions 0.05/0.10 (grid 0.05–1.00 as diagnostic), 12 RQs, triple-stratified paired bootstrap/McNemar with Holm correction; 13 comparators.
9. A value-free fallback (actionability ranking, depth-1, reserve intact) deploys when preregistered sizing floors (≥80 labeled states, ≥30 instances) are unmet.
10. Estimand check: the draft **stays at the trajectory/answer-class selection estimand** — no stopping-rule drift, no B4.6 serving-economics drift ($/resolved-task, batching, serving infra are absent). Boundary discipline is intact.

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|--------------|-------|--------|
| 1 | Cross-instance, globally coupled allocation of a scarce **trusted** verifier over a frozen candidate pool, with forced per-instance decisions | **Heteroskedastic Signals in Budgeted LLM Verification** (arXiv:2606.15841, 2026): budgeted instance-level verification allocated by confidence signals; a *limits* result (signal heteroskedasticity caps gains over simple baselines). **AVA — Anytime Verified Agents** (TMLR 2026; GitHub llmsresearch/AVA): selective verification cascades + VOI search under token/tool/verification budgets, but **per-task** budgets, no global coupling. **ADAP / Adaptive Generate-Rank-Verify** (arXiv:2605.17609, verified real): per-prompt first-positive search with costly verification, monotonicity assumption. **Best-of-Evidence** (arXiv:2607.20950, verified real, VL domain): partial-evidence allocation **within** one candidate pool. | Answer-class granularity + cross-instance budget coupling + elimination-aware forced aggregation is a genuinely unoccupied cell; but the "no direct account" absence claim is now false at instance granularity — 2606.15841 does uncertainty-signal budgeted verification and is **not cited** | **Novel but crowded; absence claim must be weakened and 2606.15841 + AVA cited with explicit deltas.** This is exactly the "missed 2026 neighbors" failure signature. |
| 2 | Label-free dependency-aware actionability + wrongness-oriented consensus-probe reserve as the allocation signal | Active testing (Kossen et al. 2021) allocates scarce labels by informativeness; 2606.15841 uses confidence signals and shows their heterogeneity **structurally limits** allocation gains; verification cascades (AVA) use calibrated uncertainty. Family-capping resembles evidence-deduplication ideas in ensemble literature. | Counterfactual decision-sensitivity at answer-class level, family-capped so correlated corroboration ≠ independent evidence, plus a reserve that ranks by disagreement-among-agreeing-sources rather than confidence | **Moderate.** Defensible delta, but 2606.15841's negative result raises the prior that cheap signals cannot aim the budget — the draft must engage it head-on; conveniently, discussion.md's pre-registered negative-result branch already covers this. |
| 3 | Total minimax-regret aggregation from partial class-level feedback (eliminations count) | Self-consistency (majority, no verification); Best-of-Evidence factor-graph aggregation (within-instance) | Totality (decision after any history incl. all-eliminated), elimination of class + its cheap support, robustness to dropping any one family | Moderate; supporting, not headline. |

Verification trail: one WebSearch (2026 selective-verification/verifier-budget query) surfaced 2606.15841, AVA/JMDCMf7mlF, LLM-as-a-Verifier (2607.05391), PPT pivot-tournament, TRACE; WebFetch confirmed 2606.15841 content, AVA scope (per-task budgets, TMLR 2026), and the existence/content of 2605.17609 and 2607.20950 via arXiv API.

## 3. Consistency vs discussion.md — silent scope drift found

The sibling failure signature ("zero confabulated citations BUT silent scope inflation; pilots/gates dropped") **partially reproduces here** — not budget inflation (budgets match: 5–10% headline of ~16K slots/triple), but **method-complexity inflation with pilot-spine deletion**:

- **Datasets/models de-named.** discussion.md pins GSM8K-500 / MATH-500 × Qwen2.5-7B-Instruct / Llama-3.1-8B-Instruct, a difficulty ladder, and a weaker-tier fallback. The draft says only "two datasets and two models" — unfalsifiable and unimplementable as written.
- **Go/no-go gates dropped.** Week-1 pre-screen (base accuracy ∈ [30,70]%, mode-share IQR > 0.2), the AUROC gate (best signal lower CI > 0.55 else negative-result pivot), the elicitation gate on verbalized confidence, and the pre-registered negative-result branch are all absent.
- **SP1 demoted.** discussion.md: per-signal AUROC + consensus-wrong-mass table is "THE HARD PART... everything else is conditional on this number." The draft buries this under RQ7/RQ8 actionability audits; no raw-signal AUROC deliverable, no consensus-wrong mass table.
- **Hindsight ceilings dropped.** OPT-static and OPT-adaptive (and their gap as the value-of-adaptivity measurement) are gone; only the full-verification ceiling remains.
- **Simple policy arms dropped.** Most-uncertain-first at two granularities, difficulty-conditioned instance ranking, per-item threshold escalation, and the ε-insurance sweep (ε∈{0,0.1,0.25}) are replaced by a single monolithic value-based policy + its own ablations. The "cheap re-ranking study" identity — the stated reason B4.5 survived the audit — is gone.
- **Artifact plan and scope contract dropped.** The [资源] identity (frozen pools + replay harness released) and the "math core frozen / code slice droppable" contract are absent.
- **Circularity containment kept, breaking dropped.** Signals frozen pre-call (kept) but the held-out-test execution verifier that breaks verifier==oracle is not in the plan.
- **No drift into B4.1/B4.6 territory** (good): no stopping rules, no serving economics.

## 4. Citation audit (~10 load-bearing)

| Citation in draft | Status |
|---|---|
| Wang et al., Self-Consistency (ICLR 2023) | Real, correctly used |
| Brown et al., Large Language Monkeys | Real (arXiv:2407.21787), correctly used |
| Zhao et al., Sample, Scrutinize and Scale | Real (arXiv:2502.01839), correctly used |
| Aggarwal et al., Adaptive-Consistency | Real (arXiv:2305.11860), correctly used |
| Damani et al., Learning How Hard to Think | Real (arXiv:2410.04707), correctly used |
| Lightman et al., Let's Verify Step by Step | Real, correctly used |
| "Training Verifiers..." (no authors) | Real (Cobbe et al. 2021) but **author attribution missing** in draft |
| Chen et al., CodeT | Real (arXiv:2207.10397) |
| Chen et al., FrugalGPT "[2026]" | Real but **misdated** — 2023, arXiv:2305.05176 |
| Dughmi et al., Adaptive Generate-Rank-Verify | **Verified real**: arXiv:2605.17609 (2026-05), matches draft's description incl. monotonicity assumption |
| Zhang et al., Best-of-Evidence | **Verified real**: arXiv:2607.20950 (2026-07); note it is vision-language — draft should say so |
| Kossen et al., active testing | Real (arXiv:2103.05331) |
| Montgomery et al.; Dip et al. | **Unverified** (search budget exhausted); flag [VERIFY] before submission |

Verdict: **zero confabulations detected among the 11 verified**, matching the sibling signature. But: every citation is rendered "[n.d.]" with no years/venues/IDs; Related Work carries a literal "This section requires manual completion" note; and the three closest **2026 neighbors are missing entirely** (2606.15841, AVA/TMLR-2026, LLM-as-a-Verifier 2607.05391).

## 5. Gap to implementation

- The frozen pool does not exist; with datasets/models unnamed, the generation pass cannot even be launched. experiment-spec.md presupposes an on-disk schema nobody has produced.
- **Dev-budget arithmetic has zero slack**: at B=800 the plan's own planning calculation yields ~102 labeled states / ~34 instances vs floors 80/30. One bad path-coverage yield and the headline policy collapses to the fallback at exactly the headline budget.
- experiment-spec records two known open flaws: the **RQ2 hypothesis-text mismatch** and the **possibly-empty PRIMARY stratum** for the consensus-targeting claims — shipped unresolved.
- Verbalized-confidence elicitation (~64K extra short calls) is uncosted; discussion.md's elicitation gate is dropped.
- Code-domain answer-equivalence (probe-input suites) is unspecified because the code slice silently vanished; yet "two datasets" is ambiguous about whether code is in.
- The machinery (beam search, IPW strata, isotonic shrunk priors, support-widening tolerances) is ~10× the engineering of discussion.md's replay grid, on the same 6-week clock that discussion.md judged feasible only for the *cheap* version.

## 6. Verdict and top-3 fixes

**Verdict: MAJOR REVISION.** The formal problem statement, dependency-family idea, elimination-aware total aggregation, and consensus-probe reserve are worth keeping. But the draft inverted the design doc's feasibility logic (complex machinery first, diagnostics demoted), de-named the experiments, dropped every gate, missed the 2026 neighbors, and ships two self-acknowledged unresolved flaws.

**Inferred 2 unresolved MAJOR critiques** (consistent with experiment-spec.md's own recorded flags and the discussion.md critic line):

- **MAJOR-1 — Value-model supportability at the motivating budget.** The label-free training pipeline is sized at ~102 states/34 instances against floors of 80/30 at B=800 — no slack — so the cross-fitted/shadow-priced headline machinery is likely *unfittable in exactly the scarce regime the paper is about*, silently demoting RQ1 to the fallback; and the RQ2 fallback hypothesis text mismatches its stated thresholds. Complexity is unvalidatable at the budget that motivates it.
- **MAJOR-2 — Confirmatory claims conditioned on a possibly-empty stratum, atop an unbroken oracle circularity.** RQ6/RQ9 (the paper's most distinctive "confidently wrong consensus" claims) are confirmatory only within a PRIMARY stratum (reliable multi-family disagreement AND transferable calibration prior) that may be empty over 4 triples; and the trusted verifier remains the evaluation oracle throughout (the execution-verifier slice that breaks the circularity was dropped), so even positive results are ambiguous between "allocation works" and "oracle self-scoring."

**Top-3 fixes (applied in the revision):**
1. **Restore the discussion.md spine as the primary surface**: named datasets/models + difficulty ladder + pilot gates; per-signal AUROC + consensus-wrong-mass diagnosis as Experiment 1; simple policy family (uniform / most-uncertain-first ×2 granularities / difficulty-conditioned / threshold-escalation / ε-insurance / sequential-greedy) + OPT-static & OPT-adaptive ceilings; the value-based shadow-priced policy becomes the *top tier* of this family with a preregistered sizing-floor fallback ladder (resolves MAJOR-1 by making the fallback the declared headline policy whenever floors are unmet, and fixing RQ2's hypothesis text).
2. **Repair the related-work perimeter**: add 2606.15841 (instance-level budgeted verification, limits result), AVA (per-task budgets, cascades), LLM-as-a-Verifier; weaken the absence claim to the answer-class + coupled-budget + elimination cell; fix FrugalGPT's date, Cobbe attribution, "[n.d.]" formatting; keep the pre-committed hidden-twin repositioning.
3. **Make every distinctive claim evaluable and de-circularized** (resolves MAJOR-2): RQ6/RQ9 restructured as premise (exact-binomial ELIMINATE floor, always evaluable) + conditional targeting margin with a guaranteed descriptive fallback; restore the held-out-test execution verifier slice (droppable per scope contract, but planned) and the artifact release.
