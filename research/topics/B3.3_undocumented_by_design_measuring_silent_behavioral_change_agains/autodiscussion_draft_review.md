# B3.3 — Review of Autodiscussion Draft Package (ZB3.3--f5267180)

Reviewed: 2026-08-15. Inputs: `research-report.md` (782 ln), `experiment-spec.md`, `paper-draft.md` vs `discussion.md` (design doc of record) and `README.md` seed.
Verification channel: WebSearch quota not attempted; citations verified via arXiv API (`export.arxiv.org/api/query`) — **narrower sweep than a full web search**, noted where it matters.

---

## 1. Architecture of the draft (~10 lines)

1. **Behavioral Change Ledger** — frozen paraphrase-grouped probe panel, repeated outputs under locked decoding; sample-only two-sample tests (blocked permutation + Benjamini–Yekutieli q=0.05 for retrospective/snapshot pairs; anytime-valid e-process change-points + e-BH for aliases); held-out confirmation; deterministic complete-link clustering (hard-compatibility keys + cosine ≥ 0.80 on effect vectors) → countable change units = the ρ denominator.
2. **Changelog Claim Registry + frozen scope lattice** — 6 axes (vendor/model, interval, behavior, direction, domain, population); **two blinded human encoders** map every claim AND every ledger record into the lattice; coverage = deterministic set-containment; specificity ∈ {absent, blanket, specific}; strict = one specific claim matching all primary axes; lenient = descendant containment incl. explicitly-scoped blanket claims.
3. **Regime-specific gap inference** — ρ(r,q) per regime × rule, never pooled; crossed-block bootstrap that resamples raw acquisition blocks and **re-runs the whole pipeline in every replicate**, nested (outer×inner) percentile-t intervals; `non-estimable` / `cluster-dominated` fallback labels.
4. Evaluation is entirely on constructed data: seeded replay benchmark (RQ1–2), 720-pair expert corpus (RQ3), 6-encoder crossover on 300 pairs (RQ4), 2,000-sims/cell dependence grid (RQ5), and a claimed 180-real-cluster cohort (RQ6); five paired baselines (aggregate-shift+LOPFO, one-pass testing, unconstrained NLI, free-form judgment, item-level bootstrap).

The three-stage decomposition (detect → align → infer) matches discussion.md's two-arm design; the lattice formalism and the ledger's confirm-then-cluster individuation are genuine improvements over the seed's looser "diff card + NLI" sketch.

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|---------------|-------|--------|
| N1 | ρ estimand: fraction of detected cross-version changes with no scope-entailed changelog claim, per-regime, strict/lenient | Chen et al. 2307.09009 (drift only); FMTI 2023/24/25 (documentation practice scores, no behavioral arm); **Chauvin 2512.03816 (logprob tracking) & 2602.11083 (token-efficient change detection)** — detect THAT APIs change, verified titles indicate no disclosure alignment | The accountability layer: aligning detected change to vendor disclosure text and estimating the uncovered fraction. Prior work stops at detection. | **KEEP — this is the paper.** But the draft never cites the Chauvin line, so the delta is undefended exactly where it's contested. Discussion.md's blocking action item (full-text check of 2512.03816 for any informal changelog comparison) is **still unresolved**. |
| N2 | Confirm-then-cluster ledger → enumerable change units (denominator) | Richter (sequential shift test), Dima (feature K-S), Zhu 2506.06975 (RUT), **Cacioli 2604.27405 "Beyond the Mean"** (within-model reliable change detection — uncited), Ma (regression testing) | Individuation into countable, auditable units rather than binary/aggregate decisions | KEEP; must position against 2604.27405 and 2602.11083. |
| N3 | Frozen scope-lattice containment matching (replaces NLI) | No direct twin; SE release-note mining (Moreno et al. ARENA) and NLI/claim-verification lit both unrepresented in draft | Deterministic, auditable coverage decisions; separates specificity from coverage | KEEP the formalism, but it is a **silent scope change** vs discussion.md (which promised calibrated NLI and explicitly disclaimed a new matching method) and as specified it is **manual-labor-bound** (see §3). |
| N4 | Crossed-block full-pipeline nested bootstrap | Blockwise bootstrap, Liu 2209.05281 (cited as "(unknown authors)") | Pipeline reconstruction inside each replicate propagates detection/clustering uncertainty | Sound idea; **computationally implausible as specified** (outer 1000 × inner 200 = 200k full pipeline re-runs each containing permutation tests). Simplify for the real cohort; keep nesting in simulation only. |

## 3. Consistency vs discussion.md

**Kept faithfully:** three regimes estimated separately and never pooled (hard constraint, restated in problem def, methods, and report spec) ✓; strict/lenient semantics identical to discussion (ρ_strict = not-specifically-covered = π_absent+π_blanket; ρ_lenient = π_absent) ✓; S0/S1/S2 → absent/blanket/specific ✓; black-box, no vendor-internal records ✓; estimand explicitly conditional on the detection procedure Δ ✓.

**Silent scope changes (the sibling signature, confirmed):**
1. **The NLI alignment arm was replaced, not calibrated.** Discussion M4: NLI/LLM-judge entailment scorer, τ_strict/τ_lenient calibrated on a 250-pair human dev set (κ ≥ 0.6 gate, matcher F1 ≥ 0.7), novelty explicitly *not* a new matcher. Draft: two blinded humans hand-encode **every** claim and **every** ledger record into the lattice; NLI survives only as baseline B3. So yes, the alignment arm is human-calibrated — it is human-*executed* — which converts a scalable instrument into an annotation protocol and silently abandons the "estimand + calibration protocol, not a new matcher" positioning.
2. **~10× scale inflation.** D3 "Clustered Three-Regime Rho Cohort" asserts **60 retrospective version-pair clusters + 60 dated API provider-date clusters + 60 prospective alias-monitoring clusters**. Discussion.md's audited reality: **6–8** open-weight transitions with disclosure texts exist, **4–6** dated snapshot pairs, and the prospective arm "cannot be scheduled" (case-study bonus only). Sixty prospective alias clusters before late Sep is impossible; ~60 dated-snapshot pairs likely don't exist across all vendors combined. RQ6's ≥54/60 criterion inherits the fantasy. Annotation similarly inflated: 720 expert-consensus pairs + 6 trained encoders × 300 pairs vs the budgeted 60–80 annotator-hours.
3. **Dropped operational safeguards:** pilot go/no-go gates (Aug 25) and NO-GO fallback; A0 same-version null-calibration arm + detector-FPR-next-to-every-headline rule; effect-size floor |Cliff's δ|≥0.33 in θ; budget caps ($4K API, 600–900 A100-h); concrete ~1,400-probe battery with named sources (MMLU/GSM8K/TruthfulQA/XSTest/HarmBench/IFEval/BFCL + changelog-mined probes); the changelog corpus as a released artifact contribution; σ companion metric and the Σ D<10 descriptive-only rule; suite-direction conservativeness statement; ToS/legal handling; fallback venues.
4. **Motivation swapped:** EU AI Act post-market monitoring, incident record, and user stories replaced by two marginal load-bearing anchors (Arif "patching" + Shu & Wei "military decision sovereignty") — real papers, but a distracting frame for an accountability-measurement paper.

## 4. Citation audit (load-bearing, ~10)

Verified via arXiv API today (IDs) or high-confidence known works (†). **Zero confabulated citations found** in the spot-checked set.

| Citation in draft | Status |
|---|---|
| Chen et al., How Is ChatGPT's Behavior Changing over Time? | Real † (2307.09009) |
| Ma et al., (Why) Is My Prompt Ge**t**ing Worse? (typo in draft) | Real † (2311.11123) |
| Dima et al., You've Changed | Real † |
| Richter et al., An Auditing Test to Detect Behavioral Shift | Real † (2406.28749/OpenReview line) |
| Zhu et al., Rank-Based Uniformity Test | **Verified** 2506.06975 |
| Cai et al., Are You Getting What You Pay For? | **Verified** 2504.04715 |
| Chishti et al., Test Before You Deploy (2026) | **Verified** 2604.27789 |
| Arif et al., Patching LLM Like Software | **Verified** 2511.08484 |
| "(unknown authors)", Modeling Dependent Structure for Utterances in ASR Evaluation | **Verified** 2209.05281 — Zhe Liu et al.; draft must name authors |
| Bommasani et al. "Rishi Bommasani¹ Kevin Klyman…" | Real work (Foundation Model Transparency Reports) but **title field is mangled author text** — must repair |
| "Sujian Li & Bill Yuchen Lin", The Good, The Bad, and The Greedy | Real paper but **misattributed** — Yifan Song is first author (2407.10457) |
| FMTI 2023 / 2024 / 2025; Mitchell model cards | Real † |

**Missing 2026 neighbors (must-cite):** 2512.03816 (Log Probability Tracking of LLM APIs), 2602.11083 (Token-Efficient Change Detection in LLM APIs), 2604.27405 (Beyond the Mean), 2606.16100 (fingerprint spoofing — needed for the adversarial-vendor scoping), 2606.05396 (Willing but Unable — refusal-vs-capability separation for category attribution). Also absent: SE release-note literature (Moreno et al.), safe-harbor/ToS context (2403.04893). The paper-draft related-work section literally ends with "> This section requires manual completion with proper citations."

## 5. Gap to implementation (ICLR late-Sep clock)

- **Feasible by Sep 25:** RQ1/RQ2 (synthetic seeded replay), RQ5 (simulation grid), the pipeline codebase (experiment-spec is well-decomposed and buildable), the changelog corpus (scrape + Wayback + claim segmentation — buildable in days, and it's a publishable artifact).
- **Not feasible as drafted:** D3's 180 real clusters (§3.2); full dual-human encoding of all claims × records; 720-pair + 1,800-rating annotation program; 200k full-pipeline bootstrap re-runs against real acquisition data; no concrete model-pair list, no acquisition budget, no pilot gate — i.e., **the headline measurement itself has no executable path in the draft**, only its validation harness does.
- Discussion.md's schedule (pilot by Aug 25, A1+A2 runs Aug 26–Sep 8) remains the only credible path; the revision must restore it.

## 6. Verdict + top-3 fixes

**Verdict: Major revision, salvageable core.** The estimand (N1), non-pooling discipline, strict/lenient formalism, and confirm-then-cluster ledger are sharp and correctly positioned as the delta over the change-detection line. But the draft silently inflated the real-data cohort ~10×, replaced the calibrated-automated alignment arm with an unscalable manual protocol, deleted every operational safeguard that made the Sep deadline plausible, and failed to cite the very 2026 drift-detection papers against which its novelty must be defended.

**Fix 1 (scale + gates):** Right-size the measurement cohort to discussion.md — 6–8 open-weight transitions (headline), 4–6 dated API snapshot pairs, prospective alias arm pre-declared as case study; restore the ~1,400-probe battery with named sources, A0 null-calibration arm with FPR reporting, |δ| floor, pilot go/no-go gates, and budget caps. Rewrite RQ6 as leave-one-transition-out over the real cohort (report max deviation; drop the 54/60 fiction).

**Fix 2 (alignment arm):** Keep the scope lattice as the representation, but make encoding automation-first: a calibrated LLM/NLI encoder maps claims and diff cards into the lattice; blinded dual-human encoding on a stratified ~250–300-pair calibration/audit subsample gates the instrument (κ ≥ 0.6 pilot gate, ≥ 0.75 target, encoder-vs-human agreement reported); deterministic containment rules unchanged. RQ3/RQ4 shrink to feasible N and become the calibration experiments. This restores discussion.md's "estimand + calibration protocol, not a new matcher" stance while retaining the lattice's auditability.

**Fix 3 (positioning + citations):** Add and position 2512.03816, 2602.11083, 2604.27405, 2606.16100 (adversarial scoping sentence), 2606.05396; repair the mangled Bommasani-reports and Song et al. entries; name Liu et al. for the blockwise bootstrap; complete the related-work section; restore the EU-AI-Act/incident motivation with the honest "reactive, externally-forced disclosure" framing.

**Unresolved majors (inferred, carried into revision):** (a) the full-text novelty check of 2512.03816/2602.11083 for any informal changelog comparison is still open — flagged in the revised draft as a pre-submission blocking item; (b) nested percentile-t bootstrap is retained only in simulation; real-cohort intervals use single-level crossed-block percentile bootstrap with pipeline reconstruction (B=1000) and this weakening is disclosed; (c) snapshot availability and disclosure-text existence per open-weight pair remain [VERIFY] items that gate the cohort freeze; (d) annotator sourcing (3 experts) unbudgeted — assigned to the authors + one external in the revision.
