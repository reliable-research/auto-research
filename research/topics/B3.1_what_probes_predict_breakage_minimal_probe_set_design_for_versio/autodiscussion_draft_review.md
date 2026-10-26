# Review of AI-Generated Draft Package — B3.1 Minimal Probe-Set Design for Version-Drift Breakage Prediction

**Reviewed:** 2026-08-14. **Reviewer:** Claude (Fable 5), against `discussion.md` (2026-08-13) and 6 targeted web searches.
**Package:** `/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB3.1 Which Probes Predict Breakage Minimal Probe Sets for LLM Version Drift--0a5a141b/` (research-report.md 199KB, experiment-spec.md 53KB, paper-draft.md 82KB).
**Context:** room closed with 4 unresolved MAJOR critiques (weakest-gate cohort); portfolio says B3.1's strongest form is merged into B3.3/B3.4.

---

## 1. Architecture of the draft (~10 lines)

The draft ("Cross-Axis Probe Drift for Budgeted Prediction of LLM Contract Breakage") proposes, but does not run, a predictive framework with three modules:
1. **Category-specific cross-axis prediction** — item-level probe deltas across 5 families (capability / refusal / format / calibration / safety) are decomposed into shared drift + family-specific "innovations"; a pair-cluster-weighted hierarchical spike-and-slab logistic model with ≥2 conditional generators, conditional-randomization tests, FDR control, and ablation gates "admits" family→breakage-category blocks; the diagonal (same-axis) cells are excluded from headline claims.
2. **Out-of-sample temporal validation** — fully nested leave-one-version-pair-out (LOPO) over 18 historical pairs (admission re-run inside every fold), lineage-blocked forward chaining, and a locked prospective evaluation on 12 post-cutoff pairs.
3. **Cost-relative probe retention** — greedy conditional-gain-per-query forward selection (singleton + cross-family pair moves, screen-then-refit), a query-budget retention curve (confirmatory point at 25% budget / 80% retention), and a query-equivalent "expected validated coverage" comparison against risk-stratified direct contract testing (D = A_selected − 1.25·A_direct).
Targets are binary schema/parser/tool-call breakage on a frozen corpus of ≥200 contracts per pair; baselines are nuisance-only, change-detection-only gate, budget-matched random subsets, direct testing, all-axis model. Seven RQs mirror the three modules.

## 2. Novelty ledger

| # | Claim | Nearest prior (verified) | Delta | Stance |
|---|-------|--------------------------|-------|--------|
| 1 | Cross-axis probe drift **predicts category-specific downstream contract breakage on unseen version pairs** (not mere change detection), with diagonal/tautological cells excluded | Leshin et al., *Behavioral Fingerprints for LLM Endpoint Stability and Identity* (arXiv:2603.19022, 2026) — fingerprint-based **change detection**, no breakage target; Chishti et al., *Test Before You Deploy* (arXiv:2604.27789, 2026) — **direct** contract testing + compatibility gates, no cheap-probe prediction layer; Ma et al. (arXiv:2311.11123) — documents prompt regressions, no transfer to held-out upgrades; **PromptCanary** (2026 practitioner tool) — 19 probes across format/reasoning/safety/factual/tool-use families for canary replay, but **no predictive validation** against downstream breakage; *Skill Drift Is Contract Violation* / DriftBench (arXiv:2605.10990, 2026) — contract-violation detection for agent skills, no probe-family→breakage prediction | The probe→breakage **predictive link with held-out-pair evaluation and cross-axis (off-diagonal) attribution** is genuinely unclaimed in the 2025–26 literature; but the space is now crowded (four 2026 neighbors), so the delta is the *validated prediction matrix*, not the monitoring concept | **SUPPORT, narrowed** — must cite PromptCanary-class tooling and DriftBench as unvalidated/adjacent practice |
| 2 | **Query-budgeted minimal probe-set selection** with a budget–retention curve, vs random budget-matched subsets and change-detection gate | tinyBenchmarks (Polo et al. 2024) / EssenceBench — benchmark compression for **score fidelity at one time point**, not cross-version breakage prediction; Yoo & Harrold test-suite minimization — white-box, deterministic oracles; PredictaBoard (arXiv:2502.14445) — instance-level error prediction, not version drift; no 2026 hit performs budgeted probe selection targeting breakage prediction | Transposing minimality to black-box, non-deterministic, axis-structured drift prediction is a real delta; discussion.md's demand that benchmark-compression be an explicit **baseline arm** (A4) was dropped by the draft and must return | **SUPPORT with fix** |
| 3 | Fully nested admission-inside-LOPO + locked prospective cohort as evaluation discipline | Standard nested CV; the draft's rigor is genuine but is methodology, not a contribution per se | Discipline, not novelty | NEUTRAL |
| 4 | Query-equivalent signed "expected validated coverage" comparison vs direct testing | Casey et al. (arXiv:2604.27082) calibrate automated metrics vs human judgment for migration; no common-cost probe-vs-direct comparison exists | Minor-but-real; heavy formalism for a secondary point | WEAK SUPPORT |

## 3. Consistency vs discussion.md

**Kept (good):** five-family taxonomy; functional (not surface-diff) breakage definition; LOPO as headline; cross-axis matrix with diagonal excluded; budget–retention curve; change-detection gate (G4's A7); budget-matched random subsets (A5); frozen temporal validation; black-box constraint.

**Violations / silent scope inflation (the sibling signature, confirmed):**
1. **Scale inflated ~2×, pilot deleted.** discussion.md: pilot 4–6 open-weight pairs (~500 probes, gates G1–G4) → scale-up 15–25 pairs. Draft: 18 historical + 12 prospective = 30 pairs, **≥200 adjudicated contracts per pair, blinded human adjudicators, ≥3 lineages × ≥4 chronological pairs** — with no pilot stage and no go/no-go gates at all.
2. **SP1/G1 instrument validity dropped.** No within-version noise-floor arm, no paraphrase rank-stability (TARE-style) check anywhere in the draft. The measuring stick is never validated before prediction claims.
3. **Portfolio positioning dropped.** discussion.md: "Default = MERGED" into B3.3/B3.4, module contract, merge/standalone/kill triggers. Draft: zero mention — it silently promotes itself to a standalone Tier-1-scale paper.
4. **A4 (EssenceBench/tinyBenchmarks compression baseline) dropped** from the arms; cited only in related work.
5. **Breakage categories narrowed** to schema/parser/tool-call (drops template-break and judged answer-equivalence classes) without acknowledgment — defensible, but a silent change.
6. **B3.2-style circularity check:** the draft is *better* than B3.2 — admission is genuinely re-run inside each LOPO training fold, so probes are not selected and validated on the same *version pairs*. **But an analogous circularity survives on the contract axis:** the contract corpus 𝓒 is frozen and identical across selection, validation, and the retention curve. Nothing is evaluated on held-out **contract classes**, although discussion.md Stage 2 (refined) explicitly demands "prediction for held-out contract classes and held-out version pairs" and calls corpus-only prediction "the null hypothesis, not the goal." SP6 (real third-party pipeline spot-check) is also absent. As written, the instrument may be a compressed test suite for its own corpus.

## 4. Citation audit (10 load-bearing)

| Citation as drafted | Verdict |
|---|---|
| Chen, Zaharia, Zou — ChatGPT behavior over time (2307.09009) | REAL |
| Ma et al. — "(Why) Is My Prompt Geting Worse?" | REAL (2311.11123, CAIN 2024) — **typo "Geting"; misdated 2026** (it is 2023/24) |
| Richter et al. — Auditing test for behavioral shift | REAL (2410.19406) |
| Leshin et al. — Behavioral Fingerprints (endpoint stability) | REAL — verified arXiv:2603.19022, Mar 2026 |
| Dima et al. — "You've Changed" | REAL — verified arXiv:2504.12335 |
| Chishti et al. — Test Before You Deploy (2026) | REAL — verified arXiv:2604.27789 |
| Casey et al. — LLM End-of-Life migration | REAL — verified arXiv:2604.27082 |
| Will Cai et al. — model-substitution auditing | REAL (2504.04715; discussion.md anchor) |
| Zhou et al. IFEval / Geng et al. JSONSchemaBench / Röttger XSTest / Xiong et al. / Polo tinyBenchmarks / Pacchiardi PredictaBoard / Mazeika HarmBench | ALL REAL |
| Song et al. "Who Plays Which Role When?" + Kitouni "Factorization Curse" (research-report) | REAL papers but **topically irrelevant** — retrieval noise that must not enter the bibliography |

**Zero confabulated citations** (matches sibling signature). **Missed neighbors:** discussion.md's own anchors arXiv:2506.06975 (rank-based uniformity test) and arXiv:2512.03816 (logprob update tracking) are absent from the draft; 2026 neighbors PromptCanary, DriftBench (2605.10990), and LLM Output Drift (2511.07585) are unmentioned. Related Work ends with a leftover scaffold line "This section requires manual completion with proper citations."

## 5. Gap to implementation

**The data plan does not exist.** experiment-spec.md specifies parquet schemas only — `grep` finds **zero named models** (no Llama/Qwen/Mistral/GPT pair anywhere in the spec). The draft requires: 18 historical pairs × ≥200 contracts × 3 categories with independent blinded adjudication, a 12-pair *post-cutoff* prospective cohort (i.e., waiting for ~a year of future releases), ≥3 lineages with ≥4 chronological pairs each, plus a query-cost ledger and a null-surrogate bank. None of this is collected, costed, or scheduled; discussion.md's concrete pilot list (Llama-2→3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3, co-scheduled with B3.4's corpus, ~18k generations) was discarded rather than built upon. Eligibility floors (≥10–11 observed pairs with ≥4–6 in each event state *per family×category block*) mean that at the achievable pilot scale, essentially **every cell is inconclusive-by-design** — the paper as specified cannot produce a positive result at any budget the portfolio can fund.

## 6. Verdict and fixes

**Verdict: MAJOR REVISION — sound core, unbuildable as written.** The scientific core (cross-axis prediction matrix + nested LOPO + budget–retention curve) is novel and survives adversarial search; the draft wraps it in unimplementable statistical machinery, deletes the discussion's staging/gates/instrument-validation, ignores the merge-into-B3.3/B3.4 positioning, and rests on a nonexistent 30-pair adjudicated corpus.

**Inferred 4 unresolved MAJORs (weakest-gate cohort):**
- **M1 — Data feasibility:** the 18+12-pair adjudicated corpus and prospective cohort are not obtainable; no concrete model pairs named; prospective holdout requires future releases outside the study window.
- **M2 — Contract-corpus circularity / external validity:** probe sets are selected and validated against the same frozen author-built contract corpus; no held-out contract classes, no real third-party pipeline; "audit instrument" claim is not separated from "compressed test suite."
- **M3 — Statistical overreach at n≈18:** spike-and-slab + dual conditional generators + power-audited heterogeneity diagnostics + FDR across the matrix, with eligibility floors that its own sample size cannot meet — most categories will exit "generator-limited" or "inconclusive," i.e., a vacuous paper.
- **M4 — Instrument validity and positioning:** drift-vs-noise floor and paraphrase-stability validation (SP1/G1) deleted; merged-vs-standalone decision rule and module contract for B3.3/B3.4 deleted; scope silently inflated versus discussion.md.

**Top-3 fixes (applied in `paper-draft.revised.md`):**
1. **Restore the two-stage design with named data:** pilot on 4–6 immutable open-weight pairs (Llama-2→3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3) sharing B3.4's contract corpus, gates G1–G4 pre-registered, SP1 noise-floor + paraphrase-stability arms restored; scale-up 15–25 pairs; the prospective cohort demoted to a *growing* frozen-set temporal holdout (new snapshots evaluated as they ship), not a fixed 12-pair prerequisite.
2. **Break the contract-corpus circularity:** add leave-one-contract-class-out evaluation and an external-validity spot check on 1–2 real open-source pipelines (SP6); state the compressed-test-suite null explicitly; keep the cross-axis matrix with diagonal cells excluded.
3. **Right-size the statistics and restore positioning:** pre-registered regularized hierarchical logistic model + partial correlations + bootstrap stability selection + permutation nulls (dropping conditional generators/spike-and-slab/power-audit apparatus); restore arm A4 (tinyBenchmarks/EssenceBench compression baseline); add an explicit "instrument-design companion to B3.3/B3.4" positioning section with the merge/standalone/kill triggers; fix Ma et al. date/typo, cite 2506.06975, 2512.03816, PromptCanary, DriftBench, and remove retrieval-noise citations.

Sources checked: [arXiv:2603.19022](https://arxiv.org/abs/2603.19022), [arXiv:2604.27789](https://arxiv.org/abs/2604.27789), [arXiv:2604.27082](https://arxiv.org/abs/2604.27082), [arXiv:2504.12335](https://arxiv.org/abs/2504.12335), [arXiv:2311.11123](https://arxiv.org/html/2311.11123), [arXiv:2605.10990](https://arxiv.org/abs/2605.10990), [PromptCanary](https://pypi.org/project/promptcanary/), [arXiv:2511.07585](https://arxiv.org/abs/2511.07585).
