# Review: T5.4 Autodiscussion Draft Package (ZT5.4, job 8e82e5bf)

Reviewed 2026-08-13. Inputs: `research-report.md`, `experiment-spec.md`, `paper-draft.md` in
`/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZT5.4 Architectural Erosion Under Sequential Agent Edits--8e82e5bf/`,
vs. this topic's `discussion.md` / `README.md`. All web checks against 2025–2026 literature.

---

## 1. Architecture

- **Design**: pre-registered three-arm matched-trajectory panel on real repos. Arms: **human-gold** (historical patch), **agent-serial** (agent edits its own last accepted state), **single-shot** (agent edits the human-gold parent, state not propagated). Identical chronological task sequences, architecture-blind frozen test gate, first-passing-patch within `N_attempts`, deterministic rebase, carry-forward on failure, joint-only censoring (experiment-spec.md L49–61; paper-draft.md L118–128).
- **Scale**: 50 repos × 60 chronological SWE-bench-style opportunities = 3,000; 50-step analysis horizon; plus 400 dual-adjudicated structural mutations and 600 clean-rerun checkpoints (experiment-spec.md L86–127).
- **Estimands**: step-by-arm interaction on the primary endpoint; restricted mean time to first new violation; decomposition θ^{A:H} = θ^{S:H} (per-patch) + θ^{A:S} (accumulation) (paper-draft.md L87–99).
- **Primary endpoint**: newly introduced forbidden layering-dependency edges per production KLOC, against a baseline-fixed executable layer manifest authored once by arm-blinded adjudicators; secondaries: complexity, coupling, token-clone coverage (experiment-spec.md L63–72).
- **Analysis**: inverse-censoring-weighted hierarchical negative-binomial (KLOC offset, repo random intercept+slope, AR(1)) + discrete-time survival with shared repo frailty + TOST equivalence; pre-registered margins δ_L = 0.20 gold-baseline SD/10 tasks, δ_T = 10% of horizon; adjudicate erosion/parity/conservatism/failed (experiment-spec.md L36–45, L73–78).
- **Baselines**: independent arm-wise complete-case replay (RQ1 comparator), human-gold reference, single-shot control (experiment-spec.md L80–84).
- **Validation RQs 1–4**: panel completeness ≥95%, blinded replay audit ≥99%, measurement reproducibility ≥99%/ICC≥0.99, mutation sensitivity ≥95% / FPR ≤5% (experiment-spec.md L27–34).
- **Load-bearing choices**: (a) existence of 50 repos × 60 verified chronological tasks; (b) manifest quality per repo; (c) agent acceptance rate high enough that the serial arm actually evolves (carry-forward makes states "measurable" but frozen); (d) the single-shot arm as counterfactual anchor. (a) and (c) are the fragile ones — see §5.

## 2. Novelty ledger

**C1 — "It is unknown whether repeated agent edits erode structure; we measure longitudinal erosion vs human-gold" (research-report.md L13, L25; paper-draft.md L11).**
- Nearest prior (NOT cited in any of the three artifacts):
  - **SlopCodeBench** (arXiv:2603.24755, Mar 2026): benchmarks coding-agent degradation over long-horizon iterative tasks; explicitly tracks a "structural erosion" metric plus verbosity; erosion rises in 80% of trajectories; agent code erosion 0.68 vs 0.31 for human-maintained repos, gap widening over time.
  - **SWE-Milestone / EvoClaw** (arXiv:2603.13428, ICML 2026): agents on continuous software evolution over milestone DAGs from real commit logs; error accumulation and technical-debt framing; >80%→≤38% score drop from isolated to continuous settings.
  - **AI-Generated Smells** (arXiv:2605.02741, Zhu/Tsantalis/Rigby): architectural decay of LLM/agent code; correctness decoupled from structural quality.
  - **Regression Accumulation** (arXiv:2607.01855) — discussion.md's own named method twin, dropped by the pipeline.
- Operational delta that survives: real repositories with a **matched human-gold arm on the identical task sequence**, a **pre-registered layering-violation endpoint against a frozen manifest** (SlopCodeBench's "erosion" is complexity-mass concentration on synthetic self-extended code; SWE-Milestone measures functional integrity), and causal arm structure. The delta is real but the "unknown / never posed" framing (repeated verbatim in every related-work row, e.g. research-report.md L87, L176) is now false: the phenomenon has been measured, just not identified against a matched counterfactual.
- **Stance: somewhat-novel** (design/identification delta, not phenomenon-first delta). Draft framing as-is would be caught by any informed reviewer.

**C2 — Three-arm single-shot decomposition of per-patch vs accumulation effects (paper-draft.md L87–99, L233–241).**
- Nearest prior: internal — discussion.md SP3 already states the identity. External searches (serial-vs-single-shot structural decomposition, accumulation-effect isolation for coding agents) found no published equivalent; SlopCodeBench's closest gesture is the observation that drift reappears "once agents extend their own prior code," with no formal decomposition and no human arm.
- Operational delta: a clean telescoping estimand (Q̂ = θ^{S:H}, Ĉ = θ^{A:S}, θ^{A:H} = Q̂+Ĉ) with TOST-based equivalence adjudication. This is the package's strongest card.
- **Stance: novel** (as estimand + design; unverifiable as result until run).

**C3 — Artifact-level design conformance vs trace-level procedural compliance (T5-family positioning).**
- Verified: **AgentLTL** (arXiv:2607.02599) and **MANTRA** (arXiv:2605.06334) verify trace-level procedural compliance (tool-call ordering, presence, grounding) — a different object than the code artifact's dependency structure. The draft's endpoint (forbidden dependency edges in the artifact) keeps the artifact-level distinction **de facto**, but the draft never cites or discusses the procedural-compliance cluster, so the distinction is implicit and undefended. **Stance: distinction preserved but unargued** — add one related-work paragraph to lock it in.

**C4 — "We introduce a baseline-fixed structural measurement pipeline" (paper-draft.md L22).**
- Nearest prior: architecture-conformance checking lineage — reflexion models, import-linter/ArchUnit dependency rules, Arcan smells (all flagged by discussion.md Stage 3 critic L46–48, absent from the draft). The instrument is standard conformance tooling plus pre-registration/mutation-validation hygiene. **Stance: not-novel as mechanism**; acceptable as instrument, must not be sold as a contribution bullet at current strength.

## 3. Consistency vs discussion.md

**Agrees / improves:**
- Two-sided erosion/parity/conservatism adjudication with outcome-neutrality — kept exactly (discussion.md L32 ↔ paper-draft.md L82–85).
- SP3 single-shot decomposition promoted to the central identity — kept and formalized (discussion.md L62 ↔ paper-draft.md L87–99). Improvement.
- Arm-symmetric attrition, carry-forward, intersection/joint-censoring rules; gold-arm conflict policy stays experimenter-free — kept and hardened with a no-selection invariant (discussion.md L62, L82 ↔ experiment-spec.md L58–61).
- Layering-violation count as pre-registered primary, rest demoted — kept (discussion.md L82 ↔ experiment-spec.md L19).
- Statistics upgraded: NB+AR(1)+frailty survival+RMTTFV+TOST margins are a genuine elaboration of discussion.md's mixed-effects/Mann-Kendall/survival sketch (discussion.md L78 ↔ experiment-spec.md L73–78).

**Contradicts / silent scope changes:**
1. **Scale silently ballooned ~17×**: discussion.md plans 3 repos × ~20 steps, 54 agent trajectories, pilot-first, $2k–8k, 2–3 person-months (L88–90). Draft asserts 50 repos × 60 opportunities = 3,000, plus 400 mutations and 600 reruns, with no feasibility argument. No current dataset supports this (see §5).
2. **All go/no-go gates dropped** (G1 rebase-survival ≥60%, G2 power check, G3 acceptance ≥40%, synthetic-sequence fallback; discussion.md L92–96). The draft replaces risk gates with an optimistic RQ1 hypothesis (≥95% three-arm measurability) and never discusses agent acceptance-rate risk — critical given SWE-bench+ reports resolution rates under 5% after filtering.
3. **T5.2 composition abandoned**: discussion.md's core efficiency argument is verbatim reuse of T5.2's validated violation detectors (L5, L19, L48). The draft silently re-derives its own instrument + mutation validation, duplicating T5.2 and severing the designed paper pair.
4. **Attribution/mechanism half of the research question dropped**: README asks "侵蚀速率与什么有关?" — discussion.md answers via mechanism profiling, retry covariate, patch-feature regressions, ordering/random-order controls, multiple agent configs × seeds (L76–82, L88). The draft has one unnamed agent, no seeds, no orderings, no mechanism profiling. Half the topic is gone without acknowledgment.
5. **Related work regressed**: discussion.md's curated neighbors (Lehman, Li et al. 2022 erosion mapping, Sas et al. 2021, Regression Accumulation, LLM-code-quality snapshot studies, conformance tooling) all vanished; replaced by a corpus-limited SWE-bench-validity cluster where every row is "different problem / not a baseline / no threat" (research-report.md L35) — a self-serving scan that misses every actual nearest neighbor in §2-C1.

## 4. Citation audit (11 sampled; all load-bearing rows checked)

| # | Citation | Verdict | Notes |
|---|----------|---------|-------|
| 1 | Cotroneo et al., *Human-Written vs. AI-Generated Code* | **CONFIRMED** | arXiv:2508.21634, ISSRE 2025; attributed claims match abstract |
| 2 | Schreiber & Tippe, *Security Vulnerabilities in AI-Generated Code* (2026) | **CONFIRMED** | arXiv:2510.26103, ICICS/Springer LNCS 16219; all figures (7,703 files, 4,241 CWE, 77 types) match |
| 3 | Mujahid & Imran, *"TODO: Fix the Mess Gemini Created"* | **CONFIRMED** | arXiv:2601.07786, TechDebt 2026; 6,540→81 SATD comments matches |
| 4 | Aleithan et al., *SWE-Bench+* | **CONFIRMED** | arXiv:2410.06992; 32.67% leakage / 31.08% weak tests / 12.47%→3.97% match |
| 5 | Yu et al., *UTBoost* | **CONFIRMED** | arXiv:2506.09289, ACL 2025; 36 instances / 345 patches / 40.9%/24.4% match |
| 6 | Zhang et al., *SWE-bench Goes Live!* | **CONFIRMED** | arXiv:2505.23419, NeurIPS 2025 D&B; draft's "1,319 tasks, 93 repos" is the v1 figure (now 1,890/223) — stale, not misattributed |
| 7 | Garg et al., *Saving SWE-Bench* (2026) | **CONFIRMED** | arXiv:2510.08996, CAIN 2026, Microsoft; repo link matches |
| 8 | Liang et al., *The SWE-Bench Illusion* | **CONFIRMED** | arXiv:2506.12286, ICSE-SEIP 2026; 76%/53%, 35%/18% figures match |
| 9 | Biazotto et al., *Automating Technical Debt Management* | **CONFIRMED** | arXiv:2502.03153, TechDebt 2025 |
| 10 | "Jacinto Ramirez et al.", *Experiences on Managing Technical Debt…* | **CONFIRMED** (minor) | arXiv:2103.11486, TechDebt 2021; author is Jacinto Ramirez **Lahti** (surname split error) |
| 11 | *Architecture Without Architects* (research-report.md L27) | **CONFIRMED** | arXiv:2604.04990; five-mechanisms + prompt-wording claims match |

**No confabulated citations** — a clean run for this pipeline's #1 failure mode. The citation problem is **coverage, not fabrication**: every cited work is honestly labeled "different problem"; every genuinely close work (SlopCodeBench, SWE-Milestone, AI-Generated Smells, Regression Accumulation, erosion literature, conformance tooling) is absent. Also: two of four "general related works" have "(unknown authors)" placeholders (research-report.md L50, L252), and paper-draft.md L257 still carries "> This section requires manual completion with proper citations."

## 5. Gap to implementation

- **Data does not exist at the specified scale.** 50 repos × ≥60 chronological, test-verified, environment-buildable task instances each. SWE-bench Verified: 500 instances over 12 repos; SWE-bench-Live: 1,890 tasks over 223 repos (~8.5/repo mean). Realistically ≤5–10 repos (django, sympy, astropy…) clear 60. The spec's D1 loader (experiment-spec.md L90–107) assumes the dataset is handed over; building it is itself a SWE-bench-Live-scale curation project. This is the single largest unstated dependency.
- **Human-labor budget unbudgeted**: 50 arm-blinded layer manifests, 400 dual-adjudicated mutation labels, 300-opportunity blinded reconstruction audit. discussion.md budgeted 20–40 expert-hours for a far smaller design (L90); this design plausibly needs person-months of adjudication.
- **Compute/API cost unestimated**: spec says "estimate accordingly" (L243). At discussion.md's $1–5/agent-run, 2 agent arms × 3,000 opportunities × N_attempts≈3 ⇒ roughly $18k–90k API, an order of magnitude above discussion.md's $2k–8k envelope, before 600 container reruns and per-checkpoint static analysis.
- **Acceptance-rate power hole**: no gate replaces discussion.md G3. If agent pass rates are 5–40%, the serial arm's state rarely changes; carry-forward preserves "measurability" while destroying erosion signal. RQ5/RQ6 power simulations assume evolution occurs.
- **Statistical stack risk**: IC-weighted NB GLMM with random slopes + AR(1) + discrete-time frailty survival essentially forces a Bayesian backend (Stan/brms); spec leaves this open (L251). RQ4 FPR ≤5% on "dependency-preserving refactorings" is fragile — import-graph extractors routinely flag moved modules; no pilot evidence offered.
- **Artifact hygiene**: experiment-spec.md L1–3 is leaked LLM preamble ("I'll analyze this research plan…"); no concrete tools, repos, agents, or models named anywhere; paper-draft related work carries a manual-completion placeholder.
- **Timeline (FSE/ICSE)**: at discussion.md scale, pilot by late 2026 → FSE 2027 cycle-2 / ASE 2027 is credible (discussion.md L98). At the draft's 50×60 scale, dataset construction alone consumes the window; not submittable in one cycle.

## 6. Verdict

**Adopt-with-fixes.** The core is sound and worth keeping: the three-arm matched-trajectory design with the single-shot decomposition (C2) is the genuinely novel estimand, the statistical machinery is a real upgrade over discussion.md, and — unusually for this pipeline — all 11 audited citations are real and accurately attributed. But the package is currently indefensible on positioning and infeasible on scale. Priority fixes: **(1) Reposition novelty** — cite and differentiate SlopCodeBench (2603.24755), SWE-Milestone/EvoClaw (2603.13428), AI-Generated Smells (2605.02741), and Regression Accumulation (2607.01855); replace every "it is unknown / never posed" with "measured but never identified against a matched human counterfactual on real repositories with an artifact-level layering endpoint," and add one paragraph fencing off the trace-level procedural-compliance cluster (AgentLTL 2607.02599, MANTRA 2605.06334). **(2) Restore feasibility** — revert to discussion.md's scale (≈3 repos × ~20 steps, pilot + G1–G3 gates + fallback) or explicitly plan the dataset-construction subproject; reinstate the acceptance-rate gate and add a compute/adjudication budget. **(3) Restore the dropped design content** — T5.2 detector reuse (the designed paper pairing), mechanism profiling / erosion-rate correlates (half the topic's core question), and either the ordering/random-order controls or an explicit de-scoping statement; clean the spec preamble and complete related work.

---

*Sources checked (verification):*
[SlopCodeBench](https://arxiv.org/abs/2603.24755) · [SWE-Milestone/EvoClaw](https://arxiv.org/abs/2603.13428) · [AI-Generated Smells](https://arxiv.org/abs/2605.02741) · [Regression Accumulation](https://arxiv.org/abs/2607.01855) · [Architecture Without Architects](https://arxiv.org/abs/2604.04990) · [AgentLTL](https://arxiv.org/pdf/2607.02599) · [MANTRA](https://arxiv.org/abs/2605.06334) · [Cotroneo et al.](https://arxiv.org/abs/2508.21634) · [Schreiber & Tippe](https://arxiv.org/abs/2510.26103) · [Mujahid & Imran](https://arxiv.org/abs/2601.07786) · [SWE-Bench+](https://arxiv.org/abs/2410.06992) · [UTBoost](https://arxiv.org/abs/2506.09289) · [SWE-bench Goes Live!](https://arxiv.org/abs/2505.23419) · [Saving SWE-Bench](https://arxiv.org/abs/2510.08996) · [SWE-Bench Illusion](https://arxiv.org/abs/2506.12286) · [Biazotto et al.](https://arxiv.org/abs/2502.03153) · [Ramirez Lahti et al.](https://arxiv.org/abs/2103.11486)
