# deerflow_review — ZW2 "Verified but Wrong"

- **Skills used**: `.claude/skills/academic-paper-review/SKILL.md` (review procedure + output template) and `.claude/skills/deep-research/SKILL.md` (literature-context web methodology)
- **Review date**: 2026-08-23
- **Reviewer**: deer-flow academic-paper-review skill (Claude agent)
- **Materials reviewed**: `paper-draft.revised.md` (current manuscript, read in full including revision log), `experiment-spec.md` (current spec, read in full), `seed.md` (context only)
- **Review mode**: pre-registration-style draft with no collected results. The Statistical Rigor row assesses the *planned* analysis; Reproducibility is rated on the spec's completeness.

## Search log

All queries run 2026-08-23 via WebSearch/WebFetch per the deep-research skill; every query listed with hit/empty status.

| # | Type | Query / URL | Status |
|---|------|-------------|--------|
| 1 | WebSearch | specification-mediated reward hacking formal verification RL code models 2026 | HIT (Reward Hacking in the Era of Large Models 2604.13602; SpecBench 2605.21384; LLMs Gaming Verifiers 2604.15149; Specification Gaming in Reasoning Models 2605.02269) |
| 2 | WebSearch | Dafny reinforcement learning verifier reward specification hacking weak specifications | HIT (Tan thesis 2605.30914; Re:Form 2507.16331 incl. OpenReview camera-ready) |
| 3 | WebSearch | verified but wrong code vacuous specification detection LLM generated contracts | HIT (uDebug/Dafny NL-to-verified-code 2604.22601; SpecPylot 2604.16560; intent-aligned spec synthesis 2604.10392) |
| 4 | WebSearch | paired estimator reward hacking measurement checkpoint trajectory held-out tests false positive rate RL training | HIT (When the Reward Suite Is Leaky 2607.11022; Fuzzing RLVR Verifiers 2606.01066; EvilGenie 2511.21654) |
| 5 | WebSearch | "When the Reward Suite Is Leaky" arXiv GRPO rewarded false positives MBPP | HIT (2607.11022 confirmed: preregistered GRPO MBPP vs MBPP+ contrast, July 2026) |
| 6 | WebSearch | formal verification reward RL limitations criticism verifier acceptance does not imply correctness | HIT (rubric-RL reward hacking 2605.12474; Fuzzing RLVR Verifiers 2606.01066; RLVR surveys) |
| 7 | WebSearch | Lean Dafny verified code generation benchmark specification soundness completeness VERINA CLEVER 2026 | HIT (VERINA 2505.23135, ICLR 2026; CLEVER 2505.13938; Vericoding 2509.22908, POPL/Dafny 2026 + TMLR) |
| 8 | WebSearch | vacuity detection specification quality KaPilot VeriAct precheck verify 2026 | HIT (KaPilot 2607.21957; classical model-checking vacuity literature — Kupferman & Vardi etc.) |
| 9 | WebSearch | specification hacking proof reward August 2026 new paper adequacy gap behavioral oracle | HIT (SpecBench 2605.21384; Reward Hacking as Equilibrium 2603.28063; no proof-reward δ-estimator twin surfaced) |
| 10 | WebSearch | paired difference of correlated proportions bootstrap McNemar evaluation LLM benchmark estimand | HIT (Resolution Diagnostics for Paired LLM Evaluation 2605.30315; McNemar/paired-bootstrap methodology sources) |
| 11 | WebSearch | arXiv August 2026 Dafny specification adequacy verified pass rate behavioral correctness gap RL checkpoints | HIT (Re:Form, Tan thesis, compositional Dafny benchmark 2509.23061; no August-2026 scoop found) |
| 12 | WebFetch | https://arxiv.org/abs/2607.11022 | HIT — confirmed: rewarded-FP incidence does not grow in the observation window; base models already produce the same wrong outputs (selection, not learned exploitation); execution-test rewards only, no formal verification or specifications |
| 13 | WebFetch | https://arxiv.org/abs/2605.30914 | HIT — abstract quotes confirmed verbatim: "models exploit weak formal specifications…", 2.2%→58.1% verified reward, 9.7%→31.1% post-filtering |
| 14 | WebFetch | https://arxiv.org/abs/2604.15149 | HIT — RLVR reward hacking on inductive reasoning tasks; extensional vs isomorphic verification; no formal specs/proof rewards — adjacent, not a twin |

**arXiv id verification**: all 14 ids cited in this review were verified against the live export API in two batched requests (the first request was truncated at the API's default max_results=10; the remaining 4 ids were verified in one follow-up batch — no per-id loop). Verified: 2507.16331v4, 2605.30914v1, 2505.23135v3, 2505.13938v4, 2509.22908v1, 2607.11022v1, 2607.24300v1 (title on arXiv: "Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents"), 2605.21384v1, 2604.15149v1, 2606.01066v1, 2607.21957v1, 2604.00280v1, 2604.22601v1, 2605.30315v1.

---

# Paper Review: Tracking Dafny Specification-Adequacy Gaps with Paired Behavioral Oracles and Semantic Audits

## Paper Metadata
- **Authors**: not listed (AutoDiscussion room `98e3ae6b` output, revised through nine review passes; ZW2 in the loop_r1 four-paper family)
- **Venue**: none (pre-registration-style internal draft, pre-submission)
- **Year**: 2026 (draft dated 2026-08-21, revised 2026-08-23)
- **Domain**: ML for formal software verification; RL from verifiable rewards; measurement/evaluation methodology
- **Paper Type**: Empirical (pre-registered measurement study; no results collected yet)

## Executive Summary

The paper proposes to measure, longitudinally across RL training checkpoints, the "specification-adequacy gap" δ = Pr(A) − Pr(B): raw Dafny verifier acceptance minus independent behavioral correctness on escrowed, never-rewarded tests evaluated over the trusted intended domain. A 3×2 randomized factorial (binary-verifier / structured-VC / hybrid proof-plus-execution rewards × fixed-trusted / model-generated specifications) with 20 seeds, 2,000 held-out tasks, and 11 checkpoints feeds a hierarchical four-state model; a multi-label semantic-intervention audit (UNSAT certificates, havoc-based vacuity checks, coverage, mutant acceptance, clause ablations) decomposes δ into an adequacy-aware component and a mechanism component. Six RQs carry explicit numeric success and falsification criteria. The motivation rests on two verified primary sources — Re:Form (arXiv:2507.16331) and the MIT Dafny RLVR thesis (arXiv:2605.30914, 2.2%→58.1% verified reward vs 9.7%→31.1% after task filtering) — which the paper correctly treats as suggestive but uncontrolled.

The draft's core intellectual asset is estimand discipline: it identifies (and documents reversing) the seed's self-defeating instruction to exclude vacuous acceptances from the verification rate, showing that an adequacy-aware numerator zeroes out exactly the pathology being measured, and instead retains vacuity/empty-domain flags as a decomposition of a raw-acceptance δ. The literature-context phase of this review found no method twin: the closest published cousins measure the analogous quantity under execution-test rewards (arXiv:2607.11022, whose no-growth null the draft engages head-on in RQ3) and in self-improving agents (arXiv:2607.24300), not in proof-rewarded, specification-mediated settings. The main shortfalls are (i) residual reversed-estimand notation (V−B) surviving in the Method and Experiments sections after the round-9 fix to Related Work, (ii) no power analysis behind the preregistered thresholds despite a 120-run RL factorial whose feasibility at 0.6B scale is asserted rather than budgeted, (iii) audit validity established only on planted mechanisms with no plan for the planted→emergent distribution shift, and (iv) boundary citations (SEAL, SpecBench, fuzzing-verifiers) recorded in the seed ledger but never landed in the manuscript body. As a pre-registration this is a strong, falsifiable design; the identified consistency and power gaps are fixable without new ideas.

## Claims Ledger

```
Claim 1: Specification hacking under proof rewards is documented in practice but has never been
         measured longitudinally, attributed to reward design/spec provenance, or mechanism-decomposed.
Evidence: Verbatim-verified quotes and figures from Re:Form (2507.16331) and Tan (2605.30914);
         this review's own searches found no counterexample (search log #1, #4, #9, #11).
Strength: Strong.

Claim 2: The correct primary estimand is raw-acceptance δ = Pr(A)−Pr(B); an adequacy-aware
         numerator V = A·D·(1−Q) is self-defeating.
Evidence: Analytical argument (Formal Problem Definition): for a vacuous acceptance A=1, B=0
         but V=0, so V−B contributes zero exactly where the pathology is worst.
Strength: Strong (self-contained logical argument; no data needed).

Claim 3: Pairing yields calibrated and narrower intervals for δ (RQ1).
Evidence: None yet — planned 12-cell × 10,000-replicate simulation with explicit coverage
         (0.90–0.98) and width-ratio (≤0.85) criteria.
Strength: Weak (planned; plausible given paired-estimation statistics literature).

Claim 4: The escrowed evaluator detects intent violations reward-visible tests miss (RQ2).
Evidence: None yet — planned 500-mutation blinded suite with lower-bound criteria (0.90 / 0.20).
Strength: Weak (planned; validity hinges on mutation-suite authorship independence, see W3).

Claim 5: δ widens under generated specs and stays controlled under fixed specs (RQ3).
Evidence: None yet; the strongest published contrary evidence (2607.11022's no-growth null in the
         execution-reward setting) is engaged explicitly, and the falsification plan kills the
         hypothesis if the null transfers.
Strength: Weak (planned; honestly framed as a genuine test, not a confirmation exercise).

Claim 6: Hybrid proof-plus-execution reward reduces δ without materially reducing verification (RQ4).
Evidence: None yet — planned contrasts with selection-aware clustered bootstrap.
Strength: Weak (planned; interpretation depends on the uncharacterized relationship between
         reward-visible execution tests and the escrowed suite, see W4).

Claim 7: A multi-label semantic audit separates empty domains, vacuity, exclusion, and weakening,
         including co-occurring mechanisms (RQ5/RQ6).
Evidence: None yet — planned calibration/locked-evaluation on 2,400 + 1,500 planted programs.
Strength: Weak (planned; criteria are defined only on planted corpora, see W3).

Claim 8: No prior work produces a paired, reward-isolated, checkpoint-indexed δ decomposed by
         reward construction, specification provenance, and failure mechanism.
Evidence: Related Work's family-by-family contrast against δ; the seed's 8-pass scoop sweeps;
         corroborated by this review's independent searches (nothing closer than 2607.11022
         and 2607.24300, both outside the proof-rewarded spec-mediated setting).
Strength: Moderate-to-Strong (a scoped first-measurement claim; but the scoping citations are
         not all in the manuscript body, see W5).
```

## Summary of Contributions

1. A paired estimator of the specification-adequacy gap δ = Pr(A) − Pr(B) on raw verifier acceptance, with escrowed behavioral oracles, task-stratified nested bootstrap, and the decomposition δ = [Pr(V)−Pr(B)] + [Pr(A)−Pr(V)].
2. A randomized 3×2 longitudinal factorial (reward type × specification source) with a hierarchical four-state model attributing gap trajectories to reward design and specification provenance.
3. A multi-label semantic-intervention audit distinguishing empty precondition domains, implementation-independent vacuity, precondition exclusion, and postcondition weakening under co-occurrence.
4. A preregistered evaluation plan (five purpose-built datasets, six matched baselines, explicit numeric success and falsification criteria for six RQs).

## Strengths

### S1: Estimand discipline that catches and documents a self-defeating design
The Formal Problem Definition's argument for raw acceptance A over the adequacy-aware V (paper-draft.revised.md, "The primary estimand uses raw verifier acceptance", around lines 70–89) is the sharpest piece of thinking in the package: gating the numerator on adequacy subtracts exactly the misleading acceptances the paper exists to count, so the estimator would report its smallest gap where the pathology is worst. The decomposition δ = [Pr(V)−Pr(B)] + [Pr(A)−Pr(V)] then makes the mechanism flags earn their keep as attribution rather than filtering, and the further refusal to gate B on the candidate's own precondition ("Any definition that restricted T to inputs 'applicable' under P would hand the model the same lever on the behavioral side") closes the symmetric loophole. The seed file shows this reverses the original submitted design, with the reversal reasoned and logged — exactly the audit trail a pre-registration should have.

### S2: Adversarial engagement with the strongest contrary evidence, wired into falsification
RQ3 (manuscript, "RQ3: Specification-Dependent Adequacy-Gap Trajectories") explicitly imports the no-growth null of arXiv:2607.11022 — a preregistered GRPO contrast this review independently verified (search log #12): rewarded-false-positive incidence does not grow during training under execution-test rewards, and base models already produce the same wrong outputs. The draft neither ignores nor hand-waves this; it states that if the null transfers to the proof-rewarded setting "the widening hypothesis dies as specified in the falsification plan," and identifies the spec-authorship factor as the mechanism that would make the settings differ. Every RQ carries numeric success thresholds (e.g., coverage ∈ [0.90, 0.98], width ratio ≤ 0.85, Δδ ≥ +0.08, TOST ±0.03), so the design is falsifiable in the concrete, checkable sense.

### S3: Unusually complete and implementable experiment specification
experiment-spec.md is close to directly executable: typed record schemas for all five datasets (D1–D5) with a load-time invariant assertion (`V == A and not vacuity and not empty_domain`, spec lines 104–107), a hard escrow module boundary with a runtime leakage guard and a test that the reward pipeline cannot see escrowed fields (spec item 3), a mock `TrainingRunner` so all statistical machinery runs without RL, nine ablation switches each isolating one mechanism, selection-aware bootstrap for RQ4's data-dependent arm choice, and an append-only oracle-call ledger feeding the companion cost study. Open Decisions honestly record the underspecified points (copula choice, GLMM fallback, label vocabulary). For the Reproducibility rating this is near the ceiling of what a spec-only package can provide.

### S4: Evidence hygiene and concede-and-claim positioning
Every load-bearing number is tagged with primary-source verification status; version pinning (VERINA v3 vs v1's different model and numbers), venue corrections, and author-order traps (Bursuc→Chiosa; Crossref's swapped "Zhou Yuanyuan") are documented in the provenance note. Vacuity *detection* is explicitly conceded as prior art (KaPilot arXiv:2607.21957, VeriAct arXiv:2604.00280, the model-checking vacuity literature — all confirmed by this review's searches #8), with novelty claimed only for using the flags as a δ-decomposition. This review's independent searches corroborated both incident quotes verbatim (search log #13) and found no scoop the draft has missed at the measured-contribution level.

## Weaknesses

### W1: Residual reversed-estimand notation survives in the Method and Experiments sections
The round-9 revision fixed Related Work's reversed estimand but the same V/A drift persists elsewhere in the current manuscript: (a) "Independent Adequacy-Gap Estimation" states "Each sampled candidate will receive a binary verifier outcome V… The candidate-level adequacy gap is therefore V−B" (line 152) — using V where A is meant, one paragraph before the correcting sentence; (b) "Controlled Training-Trajectory Comparison" says the four-state model "preserves the covariance between V and B" (line 164), though the spec's M2 explicitly models raw (A,B) as primary; (c) Experimental Setup describes the Simulation Bank as resampling "V-B dependence" and pairing as "preservation of V-B pairing" (lines 194, 196), and RQ1's metrics list "failure rates stratified by task size and V-B dependence" (line 219) — while spec Open Decision 1 insists the simulation must plant A–B dependence because "simulating V–B would validate the wrong estimator." The spec itself has one residual: D2's prose says replicates "preserve task sizes and the joint (V,B) distribution" (spec line 116), contradicting its own SimConfig comment. In a paper whose entire identity is this estimand choice, an implementer following the Method/Experiments text as written could rebuild the rejected estimator. Fix: a mechanical sweep replacing every estimand-bearing V with A (keeping V only where the decomposition or adequacy-aware secondary is genuinely meant), plus one sentence fixing spec D2.

### W2: No power analysis behind the preregistered thresholds, and feasibility at 0.6B scale is asserted, not budgeted
The design requires 3×2×20 = 120 independent RL training runs of a 0.6B model with a Dafny verifier in the loop, evaluated at 11 checkpoints on 2,000 tasks (≈2.64M paired evaluations per panel, before bootstrap). Yet no power or design analysis justifies that 20 seeds suffice to detect the preregistered effect sizes (Δδ ≥ +0.08, difference-in-change ≥ +0.05, TOST equivalence within ±0.03, RQ4's ±0.03 verification-rate window) given seed-level variance — which in small-model RL is notoriously large. The thresholds read as convention-picked rather than derived. Compounding this, the motivating incident began at a 2.2% verified rate: at 0.6B scale, early checkpoints may contain so few acceptances that per-stratum δ components (especially Pr(A)−Pr(V)) are estimated from a handful of events, making baseline-centered contrasts noisy exactly where the trajectory story starts. Fix: add a simulation-based power/assurance analysis (the RQ1 simulation bank is already the right instrument — extend it to the RQ3/RQ4 contrast level with realistic seed variance), and state the minimum per-checkpoint acceptance counts below which strata are reported but not tested.

### W3: Audit validity is established only on planted mechanisms; the planted→emergent shift and oracle-error rates are unaddressed
RQ5/RQ6 criteria (macro-F1 ≥ 0.85, exact-label-set accuracy ≥ 0.75, recall ≥ 0.90 at precision ≥ 0.95) are all defined on corpora of *planted* mechanisms (D4, D5) authored by the research team; nothing tests whether the locked audit rules transfer to mechanisms an RL policy actually discovers, which may be qualitatively different (e.g., partial frame-condition omission, exploiting prover timeouts). Similarly, RQ2's 500 mutations are "independently adjudicated" but the suite is constructed within the same project, so the evaluator is validated against violations of the kind its designers anticipated — a circularity the blinding protocol does not remove. Finally, B itself is treated as ground truth, yet the human-audited oracles and property-based generators have their own error rates (a flaky oracle deflates B and inflates δ), and no oracle-quality audit (e.g., cross-adjudication sample, mutation score of the escrowed suite itself) is planned. Fix: add (i) a held-out audit evaluation on mechanisms harvested from actual RL runs and adjudicated post hoc, (ii) an external or at least author-disjoint mutation source for part of D3, and (iii) a quantified oracle-error estimate propagated into δ's uncertainty.

### W4: The mechanism label m_i is typed as an observed stratum, and the hybrid arm's reward-visible tests are uncharacterized
Two soundness gaps in the formal setup. First, the record x_i = (c_i, k_i, r_i, s_i, m_i, P_i, f_i) includes a mechanism label m_i, and strata g range over M — but for real RL-generated candidates, mechanism labels are *outputs of the audit whose accuracy RQ5/RQ6 are still establishing*, not observed covariates; stratifying δ by m on live data conditions on a measured-with-error variable, and the manuscript never distinguishes planted-label strata (where m is ground truth) from audit-label strata (where it is a prediction). Second, RQ4's interpretability depends on how the hybrid arm's reward-visible execution tests relate to the escrowed suite: if visible tests are distributionally close to the escrowed oracles, hybrid "reduces δ" partly by optimizing a proxy of the measurement instrument — a benign form of teaching-to-the-test the escrow boundary does not prevent, since escrow blocks access, not distributional similarity. Neither the manuscript nor the spec says how visible execution tests are sourced or how their overlap with the escrowed suite is controlled or reported. Fix: notate audit-derived labels as m̂_i with their error model, restrict m-stratification claims to planted corpora, and preregister the construction and overlap metric of reward-visible vs escrowed tests.

### W5: Boundary citations recorded in the seed ledger never landed in the manuscript body
The 8th-pass scoop sweep (seed.md and revision-log item 7) concluded the first-measurement claim must be scoped against the execution-reward analogue (2607.11022 — landed, in RQ3), the agentic self-verification analogue (SEAL, arXiv:2607.24300 — **not in the body**), SpecBench (arXiv:2605.21384 — **not in the body**), plus boundary sentences for SpecRL (2604.05820), verifier-implementation false positives (Fuzzing RLVR Verifiers, arXiv:2606.01066), and uDebug's vacuous-spec blocking (arXiv:2604.22601) — none of which appear in the manuscript. Once working notes are stripped for submission, a reviewer running the same searches this review ran (log #1, #4, #9) will find SEAL and SpecBench in the first page of results and read their absence as either ignorance or claim inflation — the exact failure mode round 9 flagged for the vacuity-detection concession. Fix: add one boundary paragraph to Related Work's third family placing 2607.24300 and 2605.21384 as execution/agentic analogues of the measured quantity, and one sentence distinguishing verifier-implementation false positives (2606.01066) from specification inadequacy.

## Methodology Assessment

| Criterion | Rating (1-5) | Assessment |
|-----------|:---:|------------|
| Soundness | 4 | The estimand argument (raw A, decomposition, B over trusted intended domain) is rigorous and correct; docked one point for the m_i-as-observed-stratum type error and the residual V/A notation drift (W1, W4), either of which could propagate into an implementation. |
| Novelty | 4 | No method twin found in 11 independent searches: measurement templates exist for execution rewards (2607.11022) and agentic self-verification (2607.24300), and vacuity detection is conceded prior art, but the paired, reward-isolated, checkpoint-indexed δ with mechanism decomposition in the proof-rewarded, specification-mediated setting is new. Not a 5 because the template (proxy-vs-holdout gap over checkpoints) is established and the transfer, while consequential, is an instantiation. |
| Reproducibility | 4 | Rated on spec completeness: typed schemas, invariants, leakage-guard tests, mock runners, config-driven ablations, and locked-rule mechanisms are exemplary for a spec-only package. Docked for the underspecified hybrid-reward test source (W4), the unenumerated mechanism vocabulary (spec Open Decision 4), and heavy operator-supplied inputs (4,400 adjudicated programs, 120 RL runs) whose provisioning is not planned. |
| Experimental Design | 4 | Randomized factorial with matched six-baseline slate, blinded calibration/locked-evaluation splits, equivalence testing, and selection-aware resampling is strong design; docked for absent power analysis behind every preregistered threshold and the planted-only validation of the audit (W2, W3). |
| Statistical Rigor | 4 | Planned analysis is sophisticated and mostly correct: nested task/test-seed bootstrap preserving (A,V,B) pairing, four-state joint modeling preserving V–B covariance, TOST, simultaneous CIs, Clopper–Pearson bounds, MC-SE reporting, data-dependent selection repeated inside resamples. Docked for missing power justification and the ambiguity of the GLMM-vs-clustered-bootstrap fallback (which analysis is confirmatory is not fixed in advance). |
| Scalability | 3 | Compute is acknowledged only as a bullet ("GPU budget for the 3×2×20-seed factorial") with no estimate; the design is 120 RL runs plus 120k Monte-Carlo replicates plus per-candidate solver calls (UNSAT certificates, havoc checks, mutant batteries) whose solver cost at 2.64M panel evaluations is unbudgeted — partially mitigated by the oracle-call ledger and the ZW4 companion cost study, and by honest scoping to single-function Dafny at 0.6B. |

## Questions for the Authors

1. How will the error rate of the escrowed behavioral oracles themselves be estimated, and how would a nonzero oracle false-failure rate (deflating B, inflating δ) be propagated into the reported δ intervals? B is currently treated as exact ground truth.
2. In the hybrid arm, how are the reward-visible execution tests constructed, and what is their distributional relationship to the escrowed oracles? If they are near-duplicates in distribution, does RQ4's δ reduction measure alignment or proxy optimization of the measurement instrument?
3. For real RL-generated candidates, m_i can only be the audit's *predicted* label set. Is stratification of δ by mechanism restricted to planted corpora, and if not, how is label noise from an audit with (at best) 0.90 recall handled in the mechanism-stratified trajectories?
4. What power do 20 seeds provide against the ±0.03 TOST margin and the 0.05 difference-in-change threshold under realistic seed-level variance for 0.6B RL runs? Can the RQ1 simulation bank be extended to an assurance analysis for RQ3/RQ4 before the runs are launched?
5. At 0.6B scale with initial verified rates around 2% (per the motivating incident), how many acceptances per checkpoint-stratum do you expect at checkpoints 0–2, and is there a preregistered minimum-count rule below which strata are excluded from testing?
6. The GLMM with checkpoint splines and crossed random effects has a documented clustered-bootstrap fallback. Which of the two is the confirmatory analysis for RQ3/RQ4, decided in advance of seeing data?

## Minor Issues

- **Duplicate/nested headings**: "Problem Definition" immediately followed by "Formal Problem Definition" (lines 36–38); "Method Overview" and "Methodology" both at H2 with the module subsections under the latter; "Experiments" followed immediately by "Experimental Setup".
- **Citation-name inconsistency for arXiv:2509.22908**: the Introduction cites "Bursuc et al. [2025]" (line 18) while Related Work cites "Chiosa et al. [2026]" (line 295) for the same paper; the provenance note (item 3) says the draft "now cites Chiosa et al." — the Introduction was missed.
- **Year inconsistency for arXiv:2505.23135**: cited as "Ye et al. [2026]" with a v3-pinned link (line 16) and as "Ye et al. [2025]" unpinned (line 18). The provenance note mandates pinning v3; unify.
- **Dangling comma** after the displayed equation δ = Pr(A=1)−Pr(B=1) in "Controlled Training-Trajectory Comparison" (lines 169–172): "…\] Comparisons will be reported…" — the sentence break is malformed.
- The abstract's second sentence is 60+ words with three nested qualifications; splitting it would help the first-screen read.
- Spec D2 prose says "preserve … the joint (V,B) distribution" (spec line 116) contradicting Open Decision 1 and the SimConfig comment (A–B dependence) — see W1.
- Optional missing reference for the paired-estimation statistics: Resolution Diagnostics for Paired LLM Evaluation (arXiv:2605.30315) makes the same paired-vs-unpaired precision argument for LLM benchmarks and would strengthen RQ1's framing.
- "Evidence provenance" and revision-log sections are correctly marked remove-before-submission; ensure the vacuity-concession and estimand-reversal reasoning survive that stripping (they now do, per rounds 8–9, but W1's residuals show the sweep is incomplete).

## Literature Positioning

The draft's three-family organization (specification synthesis/intent alignment; verifiable-code-generation benchmarks; RL from verifiable-but-imperfect rewards), each contrasted against the δ estimand, is the right structure and unusually well verified: Re:Form (2507.16331, TMLR), Tan (2605.30914), VERINA (2505.23135, ICLR 2026), CLEVER (2505.13938, NeurIPS 2025 D&B), Vericoding (2509.22908), Clover/Sun, Endres (FSE 2024), Lahiri (FMCAD 2024), Laurel/Mugnier (OOPSLA 2025), Gao (ICML 2023), Rafailov (NeurIPS 2024), plus the round-9 additions VeriAct (2604.00280) and KaPilot (2607.21957) conceding vacuity detection. This review's independent searches confirmed all of these exist as characterized and found no closer prior work than what the seed's scoop sweeps already surfaced. The scoped first-measurement claim — proof-rewarded, specification-mediated settings — survives this review's independent sweep.

What is missing from the *body* (not the working notes): the execution-side and agentic analogues that define the claim's boundary — When the Reward Suite Is Leaky (2607.11022) appears only inside RQ3, not in Related Work's third family where a reviewer will look for it; SEAL (2607.24300) and SpecBench (2605.21384) are absent entirely; Fuzzing RLVR Verifiers (2606.01066) would cleanly separate verifier-implementation false positives (a soundness bug in the checker) from specification inadequacy (a soundness-preserving contract defect), a distinction the paper relies on when it says "the verifier is sound, so the failure is relocated… to the specification." LLMs Gaming Verifiers (2604.15149) is adjacent (RLVR gaming without formal specs) and optional. Comparisons made are fair — notably fair, given the concede-and-claim treatment of CLEVER's by-construction vacuity avoidance and Vericoding's self-reported 9% weak-spec rate.

## Recommendations

**Overall Assessment**: Weak Accept — as a pre-registration. The estimand is right and non-obviously so, the design is randomized, falsifiable, and specified to an implementable level, and the novelty claim survived an adversarial literature sweep. It is held below a clear Accept by internal estimand-notation inconsistencies that could corrupt an implementation (W1), the absence of any power justification for a 120-run factorial's preregistered thresholds (W2), and audit validity resting entirely on planted mechanisms (W3). All are fixable without new ideas or new data.

**Confidence**: Medium-High — the review covers both documents in full, verified every quoted figure against primary sources, and ran an 11-query independent literature sweep; confidence is not High because no results exist to check the statistical machinery against, the RL-at-0.6B variance regime is judged from general experience rather than reported pilots, and the classical vacuity-detection literature was checked only at survey depth.

**Contribution Level**: Moderate (as specified) — with a credible path to Significant if executed as designed: a calibrated, mechanism-decomposed δ trajectory with the RQ3 contrast resolved in either direction would be a load-bearing measurement for the verified-code-generation field, and even the null result is preregistered as informative.

### Actionable Suggestions for Improvement
1. **Run a mechanical estimand-notation sweep** (W1): replace every estimand-bearing V with A in "Independent Adequacy-Gap Estimation" (line 152), "Controlled Training-Trajectory Comparison" (line 164), Experimental Setup and RQ1 metrics (lines 194, 196, 219), and spec D2's prose (spec line 116), leaving V only where the adequacy-aware decomposition is genuinely meant; add a repo grep-based check (e.g., forbid "V-B dependence"/"V−B pairing" outside decomposition contexts) so the ninth-pass class of bug cannot recur.
2. **Add a simulation-based power/assurance analysis before launching the factorial** (W2): extend the RQ1 simulation bank to the RQ3/RQ4 contrast level with a plausible range of seed-level variances, report the detectable effect size at 20 seeds, and either justify the 0.08/0.05/±0.03 thresholds from it or revise seed counts; simultaneously preregister a minimum per-stratum acceptance count for early checkpoints at low verified rates.
3. **Close the planted→emergent gap in the audit's validation** (W3, W4): preregister a post-hoc adjudicated evaluation of the locked audit on mechanisms harvested from the actual RL runs; source part of the D3 mutation suite author-disjointly; quantify escrow-oracle error and propagate it into δ intervals; notate audit-derived mechanism labels as predictions (m̂) and restrict mechanism-stratified claims accordingly; and preregister the construction and reported overlap metric of the hybrid arm's reward-visible tests versus the escrowed suite.
4. **Land the boundary citations in the manuscript body** (W5): one Related Work paragraph positioning 2607.11022, 2607.24300, and 2605.21384 as execution/agentic analogues of the measured quantity, plus one sentence separating verifier-implementation false positives (2606.01066) from specification inadequacy; fix the Bursuc/Chiosa and Ye-year citation inconsistencies at the same time.
