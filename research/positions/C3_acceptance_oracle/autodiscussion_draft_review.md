# Review: C3 auto-discussion draft package ("Green Tests Are Not Acceptance")

Reviewed 2026-08-13. Inputs: `research-report.md`, `experiment-spec.md`, `paper-draft.md` in
`paper_autodiscussion/completed_jobs_dirs/ZC3 ...--53db8d88/`; baseline design doc
`positions/C3_acceptance_oracle/discussion.md`. Web verification queries run against 2025–2026 literature.

---

## 1. Architecture (what the draft actually proposes)

A preregistered measurement-and-analysis pipeline over mined public-forge PRs plus a lab agent panel, organized as:
(1) **Master enrollment register** — hash-locked sampling frame, cohort nesting/disjointness, design weights, `LabelVault` refusing outcome labels until lock.
(2) **SOC** (Specification-Obligation Checker) — frozen coverage charter/manifest → constrained span-grounded parser over issues/traces/policies → executable + static evaluators → locked threshold → lab→field transport bridge → g-computation misclassification correction.
(3) **Predictor** — SOC-disjoint task/patch feature families, residualized against surface covariates; survey-weighted group-lasso (adjudicated-violation target) + discrete-time competing-risk (technical-only rejection target); 1,000-bootstrap stability selection.
(4) **BCFD** — post-merge defect label validated by evidence-quarantined dual reference arms, organizational-control frames (refactor/dep-update/ownership), 600-case blinded replay bank, partial-identification bounds.
(5) **Review layer** — dual-coded substantive-review classifier with PPV/sensitivity-locked threshold τ*; three acceptance layers: pre-review test-pass (initial head), raw merge (day 30), review-only acceptance (merge ∧ review_prob ≥ τ*).
(6) **Gating engine** — 24 RQs with pass predicates; five-clause BCFD validity rule assigns each result {confirmatory, descriptive, reference-limited, org-confounding-unverified}.
**Estimands:** green-but-unacceptable prevalence (RQ8, gate ≥0.10), extraction P/R, transported Se/Sp, rejection RRs, predictor AUROC/tdAUC, prevalence-guarded layer agreement/discordance, doubly-robust Brier fidelity of layers vs BCFD.
**Datasets:** 7 cohorts — 240 source packages, 1,200 lab patches (≥3 agent frameworks), 1,000 bridge + 1,500 all-green audit, 6,000 inception, ~4,800 BCFD reference cases, 2,400 dual-coded reviews, 12,000 + 8,000 expanded cohorts (~35k PRs total). **Baselines (7):** PatchDiff-only, transported diff+surface, repo-time-surface, raw telemetry, approval-count rules, pre-review test-pass, raw merge.
**Load-bearing choices:** register locked before any label opens; manifest-only primary scoring; SOC-disjoint predictor features; initial-head CI (anti-leakage); nested (not independent) merge/review layers; the spec instructs the coding agent to build the pipeline against fixtures/mocks — no real data is run by the agent.

## 2. Novelty ledger

| # | Claim (framing verb) | Nearest named prior | Operational delta | Stance |
|---|---|---|---|---|
| N1 | **"Establish" the cross-layer comparison**: test-pass vs raw merge vs review-adjusted acceptance, for agreement + held-out predictive fidelity against validated outcomes | Verification Horizon (arXiv 2606.26300) — argues verifiers are proxies, "users are the most faithful verifiers", **no measurement**; AIDev (Li et al.), Peralta 2605.22534, Abujadallah 2606.13468 — single-layer field description; "Let's Make Every PR Meaningful" (2601.18749) — predicts agentic merge at AUC 0.96 but never asks which layer tracks quality | Joint agreement matrix + layer-wise Brier/tdAUC against a *validated* defect label and technical-only rejection; no prior does the comparison | **Open cell — verified.** 3 searches found no cross-layer oracle-fidelity study. But the draft never cites its own foil 2606.26300; claim is undefended against the closest occupant. |
| N2 | **"Propose" SOC + charter-scoped green-but-unacceptable prevalence** | **"Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution" (arXiv 2604.05955)**: 495 issues / 1,787 validated design constraints mined from real PRs, aligned to SWE-bench-Verified/Pro; finds <50% of "resolved" issues design-satisfying and correctness ≈ independent of design satisfaction. **ReactBench + React-Doctor (public, millionco)**: hidden fail-to-pass tests + 400-rule pinned static verifier over 50+ React repos — green-but-fails-verifier at scale already shipped | SOC's surviving delta: *field* prevalence with probability sampling, human-audit validation, transport bridge, abstention/coverage machinery, executable obligation evaluation. The lab-arm finding ("tests pass, explicit constraints violated") is **taken** | **Overlapping.** Any "first measurement of green-but-unacceptable" reading is defeated; the defensible claim is field-validated design-weighted prevalence + N1. Neither prior is cited. |
| N3 | "Introduce" dual-target gap prediction (adjudicated violation + technical-only rejection), residualized | 2601.18749 (merge prediction, AUC 0.96); classic PR-acceptance prediction (Gousios et al. line); Abujadallah rejection taxonomy | Target is *technical-only* rejection under competing risks + adjudicated violations, residualized against surface confounders — sharper estimand than merge prediction | Incremental-but-real; must cite the merge-prediction line it beats. |
| N4 | "Develop" BCFD quarantined post-merge label validation | ReDef (Nam et al., FSE 2026) — revert-anchored defect labels, GPT triage; SZZ-validity literature | Validating the *label construction itself* via blinded reference arms, org-control frames, replay qualification, partial-ID bounds | Methodologically novel; also the package's largest cost center. |
| N5 | "Establish" substantive-review measurement + rubber-stamp prevalence | "These Aren't the Reviews You're Looking For" (2605.02273); zero-review-merge findings (2601.00753: 28.3% immediate merges) | Threshold-locked calibrated classifier used as an *oracle component*, plus audited rubber-stamp prevalence | Incremental; fine as a component. |
| — | AgentLTL (2607.02599) check | Trace-level *procedural* compliance of tool-using agents (temporal structure of the trace) | Draft's estimands are consistently artifact/acceptance-level; no conflation found | Distinction kept implicitly; AgentLTL should still be cited-and-distinguished in related work. |

Framing-verb audit: contributions use propose/introduce/develop/establish over concrete instruments and estimands — not bridge-and-synthesize boilerplate. The novelty failure is omission: the foil (2606.26300) and the SOC method-twin (2604.05955) are absent, which in a "crowded" cell is disqualifying as drafted.

## 3. Consistency vs discussion.md

**Agreements (faithful):** layered acceptance construct; neither test-pass nor merge as ground truth; review-adjusted oracle as the replacement candidate; explicit lab→field transport instead of assumed transfer (Stage 1 refined); competing-risk handling of non-technical rejections (2605.22534's 35.7% is the design driver, and Peralta/Abujadallah are cited); unmerged PRs never imputed defective; reward-hackability limb correctly absent from measured claims (Stage 4 refined).

**Improvements over discussion.md:** circularity defenses are materially stronger (LabelVault, evidence quarantine, replay bank, prevalence-guarded kappa, initial-head CI anti-leakage, five-clause gating); the formal estimand section is cleaner than Stage 1's; the org-confounding treatment of survival signals (discussion.md's A5 threat) is now a full module rather than a caveat.

**Contradictions / silent scope changes (all confirmed):**
1. **Silent pilot-dropping** — the same failure found in sibling packages. Discussion.md's G1 (20-patch checker bake-off), G2 (200-PR field feasibility probe, 50 hand-audited), G3 (30-patch adjudication dry-run, κ≥0.6 gate), and the Stage-0 source-verification gate are all gone. The only surviving pilot is the BCFD escalation pre-enrollment pilot.
2. **Budget inflation ~40–60×** on human labor. Discussion.md core: ≥800 lab tasks + ~300-patch adjudication panel (2 raters + tiebreak). Draft: ~1,200 dual-coded claims (D1) + 1,200 lab patch labels + 1,000 bridge + 1,500 audit adjudications + 6,000 disposition/rationale codings + ~4,800 BCFD verifications by **two independent reference arms** + 2,400 dual-coded reviews + 1,200 rubber-stamp audits ≈ 15,000–20,000 blinded adjudication items across ≥8 mutually-sequestered panels. Discussion.md's M2 "core data frozen ~Nov 2026" is impossible under this design.
3. **Instrument swap, unacknowledged.** Track L's concrete layers (CodeQL/Semgrep, UTBoost-style strengthened suites, and the repo's differentiating T5.2 design-constraint checkers) are replaced wholesale by SOC — a to-be-built obligation parser. Also dropped: SP4 dose-response (model tier × reasoning budget), agent re-ranking Kendall τ, the oracle-ladder Figure 1 framing.
4. **Motivating-source swap.** Discussion.md's verified set is only partially carried: 2605.22534 and post-merge-survival work survive (via Peralta, Rahman & Shihab); All-Smoke-No-Alarm (2606.18168), 2601.00753, UTBoost (2506.09289), and the foil 2606.26300 vanish. Note the draft's replacement citations are real (see §4), so this is repositioning, not fabrication — but it deletes the Stage-3 concede-and-claim structure.
5. **Oracle definition drift inside the package.** The formal problem defines O_review = M·R·S^(c) (merge ∧ substantive review ∧ construction-window survival); the operational definition in spec C6 and RQ20 is `raw_merge ∧ review_prob ≥ τ*` — the survival conjunct silently dropped (survival appears only as outcome Y). Either fix the formalism or restore the conjunct with a leakage-safe window.
6. **Kill criteria weakened.** Discussion.md's F1–F5 falsification set and the explicit "what kills C3" clause have no counterpart; the 24 pass predicates gate claims but nothing encodes "gap <5% everywhere ∧ κ>0.8 ⇒ stance dead."

## 4. Citation audit (sampled load-bearing citations)

| Citation in draft | Status |
|---|---|
| Wang et al., "Are 'Solved Issues' in SWE-bench Really Solved Correctly?" (PatchDiff), 2026 | **CONFIRMED** — arXiv 2503.15223 (Wang, Pradel, Liu), ICSE 2026; 7.8%/29.6% figures match |
| Jimenez et al., SWE-bench | **CONFIRMED** (arXiv 2310.06770, ICLR 2024) |
| Liu et al., "Is Your Code Generated by ChatGPT Really Correct?" (EvalPlus) | **CONFIRMED** (NeurIPS 2023) |
| Ahmed et al., "Investigating Test Overfiting [sic] on SWE-bench" | **CONFIRMED** — arXiv 2511.16858, FSE 2026 IVR; title typo in draft |
| Zhao et al., SpecBench | **CONFIRMED** — arXiv 2605.21384 |
| Li et al., AIDev / "Rise of AI Teammates in SE 3.0" | **CONFIRMED** — corroborated via dependent papers (Cynthia, Abujadallah both build on AIDev) |
| Peralta et al., "Why Are Agentic PRs Merged or Rejected?" | **CONFIRMED** — arXiv 2605.22534 |
| Abujadallah et al., "Understanding the Rejection of Fixes..." | **CONFIRMED** — arXiv 2606.13468, MSR '26 |
| Cynthia et al., "Beyond Bug Fixes" | **CONFIRMED** — arXiv 2601.20109 |
| Rahman & Shihab, "Will It Survive?" 2026 | **CONFIRMED** — arXiv 2601.16809; note their finding (agent code survives *longer*) is a motivation tension the report itself flags |
| Watanabe et al., "On the Use of Agentic Coding" | **CONFIRMED** — arXiv 2509.14745, TOSEM |
| Nam et al., ReDef | **CONFIRMED** — FSE 2026 |

No fabricated or misattributed citations found in the sample. Two defects: (a) no citation carries an arXiv ID, venue, or year — the related-work section ends with "requires manual completion"; (b) the decisive *missing* citations (2606.26300, 2604.05955, ReactBench, AgentLTL, 2606.18168, 2506.09289) matter more than any present one.

## 5. Gap to implementation

- **What is runnable soon:** the code harness itself. The experiment-spec's Phase 0–9 plan (register, estimators, gating engine, synthetic fixtures, RQ runners) is well-decomposed, mock-driven, and genuinely implementable in ~2–4 weeks of agent coding. That is scaffolding, not results.
- **Data availability, unresolved:** forge unnamed; agent-PR identification heuristics unspecified (known-lossy per AIDev-line papers — exactly what dropped gate G2 was for); "immutable earliest-head CI status" is frequently unrecoverable after force-push/rebase, threatening the pre-review test-pass layer's coverage assumption; repo-eligibility mining (required-status-check CI + ≥1 agent PR) needs archival snapshots not budgeted.
- **SOC does not exist.** It is a substantial NLP + program-analysis system (span-grounded parsing, generated tests that must "exhibit prescribed parent behavior"); no model choice, prompt/grammar design, or error analysis exists, yet RQ1 gates the chain at P≥0.85/R≥0.80 with CI floors. The discussion.md alternative (off-the-shelf CodeQL/Semgrep + T5.2 checkers, bake-off-gated) was implementable now; SOC is a paper-sized subproject by itself.
- **Human labor is the binding constraint:** 15,000–20,000 blinded adjudications across ≥8 disjoint panels plus two independent BCFD reference arms ≈ multi-team, 12–18 month effort with real budget; no rater sourcing plan anywhere in the package.
- **Compute:** agent panel for 1,200 patches and 1,000× bootstraps are fine; the BCFD differential-execution sandbox across pinned dependency versions is the only heavy piece.
- **Timeline realism:** as specified, this is an 18–36 month registered-report-scale program. It cannot hit discussion.md's M2 (Nov 2026) / FSE 2027 plan. A core-scale instantiation (audit ~300–500 PRs, single BCFD arm with sensitivity bounds, RQ8 + RQ19–22 only) could.

## 6. Verdict

**Adopt-with-fixes** — the measurement architecture (register/lock discipline, gating engine, layer definitions, anti-leakage constructions) is the strongest artifact the pipeline has produced for C3 and should be kept; but positioning and scope are both currently submission-blocking.

**Priority fixes:**
1. **Restore the staged core and the pilots.** Reinstate G1/G2/G3 and Stage-0 gates; scope v1 to discussion.md's minimum publishable unit (prevalence + cross-layer oracle comparison ≈ RQ8, RQ19–RQ24) at core sample sizes (audit 300–500, single BCFD arm + partial-ID bounds, defer RQ15–18 dual-arm validation to a follow-up); keep the full 24-RQ design as the preregistered ideal, not the build plan. Without this, the package repeats the sibling failure (silent pilot-dropping, ~40–60× labor inflation) and misses every 2027 venue.
2. **Fix the novelty positioning.** Cite and differentiate: Verification Horizon 2606.26300 (the argument this paper supplies data for), arXiv 2604.05955 (SOC's lab-arm twin — "green but design-violating" is already measured on SWE-bench-aligned issues), ReactBench/React-Doctor (public green-but-fails-verifier instrument), AgentLTL 2607.02599 (trace-level vs artifact-level estimand), All-Smoke-No-Alarm 2606.18168 and UTBoost 2506.09289. Lead the contribution ordering with the verified open cell — the cross-layer fidelity comparison — not with SOC-as-first-measurement. Complete the stubbed related-work section with full bibliographic entries.
3. **Reconcile internal estimands and restore kill criteria.** Align O_review's formal (M·R·S^(c)) and operational (M ∧ review≥τ*) definitions; encode discussion.md's F1–F5 falsification set (including the explicit "green tests effectively are acceptance" kill condition and the publishable-negative branch for F3) into the gating engine and the paper's verification criteria.
