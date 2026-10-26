# Experiment Design Spec — B7.1 (standalone protocol, Stage 6 confirmed output)

> Rendered from the confirmed Stage 6 output in `discussion_trace.md`, including the two stage-review fixes (`stage_review.md`: RQ7 operating-point pre-registration; additivity probe in the assumption ledger). This document is the one to execute from; `paper_draft.md`'s Experiments section is its synchronized mirror. **Target hypotheses are verbatim from Stage 5 / Stage 3 — do not edit their wording here without editing the trace.** Every number is an authored design target with a stated rationale; nothing below is a result.

## Global parameters

- **Streams:** MBPP+ (EvalPlus verifiers; pilot substrate), SWE-bench Lite-style subset, ALFWorld. Justifications in §Datasets.
- **Backbones:** ≥2 vendor families × 2 consecutive public generations, plus ≥1 two-generation pair within one family (≥3 upgrade pairs total; concrete generations pinned at run time and recorded with API version strings).
- **Library acquisition:** one frozen library per (stream, M_0) via a fixed Voyager/AWM-style loop; target 40–80 skills; per-skill acquisition ledger = {provenance backbone, acquisition tokens, validation record, retrieval key}. Acquisition config hashed before any evaluation.
- **Arms:** bare | full-library | placebo-library | leave-one-out masked | (policy arms for RQ7: estimate-thresholded, oracle-thresholded, never-retire, full-relearn, no-library). Invocation regimes: free-use and forced-use.
- **Library-level replay budget:** 300 tasks × 5 seeds = 1,500 paired episodes per (stream × upgrade-pair × arm). Power rationale: detects a 3pp paired success contrast at ≈0.8 power under 12–15% assumed discordance; **enlargement rule:** if pilot discordance implies <0.8 power at the 2pp floor, enlarge to 8 seeds before claiming any null; cells underpowered after enlargement → **INCONCLUSIVE** (pre-declared; excluded from majority votes; reported separately — never null, never dropped).
- **Per-skill ledger budget:** activation floor ≥20 retrievals; 30 sampled activation tasks × 3 seeds per eligible skill; below-floor skills reported as unmeasured at skill granularity.
- **Tests:** paired McNemar-style for success at α=0.05, Holm-corrected across upgrade pairs (and across the two fairness-of-comparison regimes where both are read); paired bootstrap CIs for cost outcomes; Wilcoxon for RQ2; Spearman for RQ5.
- **Ground truth:** mechanical only — verifier outcomes + token billing. No judge models, no human labels anywhere in the measurement path.

## Assumption ledger (gates checked in the pilot before scale-up)

- **A1 — additivity license (leave-one-out identification).** *Proposition:* cross-skill interactions are second-order. *Detection:* pairwise-interaction probe — pair-masking over top-frequency skill pairs; interaction share of total attributed value ≤ 15%. *Gate:* pilot (PG-1). *Consequence if failed:* per-skill claims (RQ4/RQ5/RQ7, RQ8's tabulation) downgrade to retrieval-cluster granularity; library-level claims (RQ1/RQ2/RQ3/RQ6) unaffected.
- **A2 — harness equality across arms.** *Proposition:* arms differ only in library content. *Detection:* byte-identical templates + automated per-episode token-accounting assertion (placebo matched on count, token-length distribution, retrieval-key statistics). *Gate:* every episode (PG-2). *Consequence:* violation downgrades the causal reading of the affected cell (RQ1/RQ3) rather than the run.
- **A3 — acquisition-time asset precondition.** *Proposition:* the library helped its own backbone (library-vs-bare under M_0 positive at ≥1pp success or ≥5% cost improvement). *Detection:* the M_0 paired contrast, computed first. *Gate:* pilot (PG-3). *Consequence:* streams failing it are excluded from the flip test (a library that never helped cannot depreciate) and reported; if all streams fail, the acquisition loop is re-tuned and the skeleton re-run — the study does not proceed on valueless libraries.
- **A4 — power adequacy.** *Proposition:* budgets above give ≥0.8 power at the pre-registered floors. *Detection:* pilot discordance/variance estimates. *Gate:* pilot (PG-4). *Consequence:* enlargement rule, then INCONCLUSIVE labeling as defined in Global parameters.
- **Placebo-null discipline (B0-style):** the placebo arm doubles as the run-validity check — under M_0 (no upgrade), placebo-vs-bare must show |Δ success| within noise; a non-null placebo at acquisition time means the pipeline measures a context artifact, invalidating the run (fix and re-run the skeleton; no hypothesis scored).

## Datasets

| Stream | Justification (hypothesis-linked) |
|---|---|
| MBPP+ | Execution-verified, cheap per episode, densest activations → pilot substrate; closed-form mechanical verification for the paired tests. |
| SWE-bench subset | Heavyweight workflow-like skills with the largest acquisition costs → stresses whether depreciation and amortization behave differently at high capital intensity. |
| ALFWorld | Non-code generality; short repetitive episodes give the highest per-skill activation counts → best-powered regime for the per-skill estimator (RQ4/RQ5). |

## Reference arms (not competitors)

Bare backbone (paired control for every verdict); never-retire; full-relearn (fresh library under M_1, acquisition charged); token-matched placebo; oracle per-skill selection (upper reference, ground truth from a held-out task split disjoint from the estimation split).

## Research questions

All tiers per `study_type: empirical` — 7 mechanism, 1 framing, 0 outcome.

### RQ1 — Asset-to-liability flip (mechanism)
- **Target hypothesis (verbatim H1):** "In at least one tested (stream × upgrade-pair) cell, the frozen old library reduces the upgraded backbone's paired task-success rate by ≥2 percentage points, or raises its token cost per solved task by ≥10%, relative to the same backbone running bare (Holm-corrected p<0.05 across cells) — the asset-to-liability flip exists."
- **Setup:** full-library vs bare under M_1, free-use regime; A3 precondition checked per stream first.
- **Test:** paired McNemar per cell; Holm across cells; bootstrap CI on cost ratio.
- **Expected outcome / falsification:** as `paper_draft.md` RQ1; the no-flip null routes to the pre-committed global pivot: robustness certification of library porting within the envelope (report at full prominence).

### RQ2 — Generation-distance dose response (mechanism)
- **Target hypothesis (verbatim H2):** "Median per-skill value retention declines with generation distance: for the same library, the two-generation upgrade shows lower median retention than the one-generation upgrade, in the majority of tested streams."
- **Setup:** same library, (M_0→M_1) vs (M_0→M_2) within one family; floor-eligible skills present in both.
- **Test:** paired Wilcoxon over skills, per stream; majority vote over streams.

### RQ3 — Content vs context load (mechanism)
- **Target hypothesis (verbatim H3):** "The placebo library reproduces less than 50% of the real library's measured harm (success and cost deltas vs bare) in every cell where H1's flip is observed — the harm is content-driven, not context-load-driven."
- **Setup:** placebo arm in flip cells; harm ratio with bootstrap CI.
- **Downgrade wording (pre-committed):** placebo ≥50% in a cell → that cell's phenomenon is reattributed to context mechanics; content-specific claims withdrawn there; porting warning stands.

### RQ4 — Heterogeneity (mechanism)
- **Target hypothesis (verbatim H4):** "Per-skill value change under upgrade is heterogeneous: in the majority of (stream × upgrade-pair) cells, at least 20% of floor-eligible skills retain ≥50% of their acquisition-time marginal utility while at least another 20% fall to zero or negative retained utility."
- **Setup:** ledger retention distribution per cell; granularity per A1's verdict.
- **Fallback (pre-committed):** near-homogeneity is reported at full prominence as "per-skill accounting unnecessary; the library-level verdict suffices."

### RQ5 — Estimate reliability (mechanism)
- **Target hypothesis (verbatim H5):** "Per-skill retention estimates computed on disjoint halves of each skill's activation set agree at Spearman ρ ≥ 0.6 (rank agreement over floor-eligible skills), in the majority of cells."
- **Gate role:** RQ7 is licensed only if RQ5 passes; on failure, raise per-skill budget or coarsen granularity before any decision claim.

### RQ6 — Interference share (mechanism)
- **Target hypothesis (verbatim H6):** "Interference accounts for at least 25% of the library-level net harm in at least one cell where H1's flip is observed — depreciation is not pure cost accounting; actively misleading content exists."
- **Setup:** trace-signature classification (obsolescence: bare ≥ with-skill on activation set and |u_k(M_1)| ≤ 0.02; interference: with-skill failure on bare-solved task with skill invoked in trace; cost drag: |Δ success| ≤ 0.02 with positive token delta); additive share decomposition of net harm.

### RQ7 — Decision adequacy (mechanism)
- **Target hypothesis (verbatim H7, incl. the stage-review operating-point fix):** "Thresholding on the estimated per-skill retained value recovers at least 80% of the oracle frontier's cost reduction relative to the never-retire corner, at the pre-registered matched-success operating point — the cost comparison taken where each policy's success rate is within ±1pp of the never-retire corner's success rate — in the majority of (stream × upgrade-pair) cells."
- **Setup:** estimate-ranked vs oracle-ranked threshold sweeps; oracle ground truth from the held-out split; refresh charged at full re-acquisition cost; all measurement cost metered; Holm across upgrade pairs; frontier curves descriptive only.
- **Fallback (pre-committed):** recovery <80% in most cells → "reliable but decision-insufficient at this budget," naming the gap source (boundary noise vs below-floor harm).

### RQ8 — Portability vs value (framing; from the AFTER limitation flagged `verify_as_hypothesis: true`)
- **Target hypothesis (verbatim, Stage 3 `hypothesis_to_verify`):** "Functional portability does not imply value retention: among skills that port to the upgraded backbone with preserved functional correctness (AFTER's transfer-accuracy sense — the skill still executes and returns contract-conformant output on its own validation inputs), a substantial fraction (design floor: ≥30%) nonetheless fall to zero or negative marginal utility under the upgraded backbone, because the utility of a skill depends on what the backbone *cannot do without it*, which is exactly what the upgrade changes."
- **Setup:** portability from standalone contract validation on ≥5 held-out validation inputs per skill (disjoint from the task stream); retention from the ledger; contingency tabulation; binomial test on the ≥30% floor within the ports-cleanly cell.
- **Fallback (pre-committed):** <30% → snapshot transfer accuracy is vindicated as a cheap retention proxy; the economic apparatus's decision claim narrows accordingly (reported at full prominence).

## Execution order

1. Walking skeleton on MBPP+ × one upgrade pair: acquisition loop → A3/PG gates → placebo-null check → 20-task dry run of every arm; scale-up must be config-only.
2. Pilot: full MBPP+ grid; A1/A4 verdicts; freeze thresholds (hashed) before evaluation.
3. Full grid: 3 streams × ≥3 upgrade pairs; one results JSON per RQ per cell {point_estimates, intervals, test_statistics, p_values, n_per_cell, seed/config hash}.
4. Verdict lookup is mechanical: score each hypothesis against its verbatim criterion; INCONCLUSIVE only where pre-declared; fallback/pivot sentences applied verbatim on failure.
