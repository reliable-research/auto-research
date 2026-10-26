# Review: B3.2 Autodiscussion Draft Package (2026-08-13)

**Package reviewed:** `/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB3.2 Capability, Policy, or Format An Identification Framework for Black-Box Drift Attribution--d7b7321a/` (research-report.md, experiment-spec.md, paper-draft.md)
**Against:** `topics/B3.2_.../discussion.md` (6-stage design doc) + README.md seed.
**Context:** room closed with 4 unresolved MAJOR critiques; known internal risk = identifiability of capability/policy/format from black-box observations.

---

## 1. Architecture of the draft (~10 lines)

The draft ("Identifiability-Gated Black-Box Decomposition of Language Model Upgrade Drift via Certified Controls") builds three coupled modules:
1. **m1 — Instrument-relative control validation:** a "causal bridge panel" of 9 intervention mechanisms (3 per source) crossed with **5 self-hosted independently-pretrained model families**; construction-certified reference classes R_s estimate *benign* cross-source effects; a purity gate licenses an anchor iff net leakage `L_s − H_s ≤ λ*` under heterogeneity ceilings `h_max / h_max^att`.
2. **m2 — Oracle-calibrated attribution licensing:** a disjunctive false-license event (wrong source / truth exclusion / licensing a nonseparable mixture) calibrated by nested-resampling grid search over an 8-parameter tolerance tuple `(κ*, λ*, s*, ε*, η*, ν*, h_max, h_max^att)`; orthogonalized "reserve moments" as overidentification; worst-case propagation of signed tolerances through the nonlinear share functional.
3. **m3 — Leakage-bounded decomposition:** drift as energy `T = ‖M‖²_W` with own-energies `Φ_s = ‖a_s‖²_W`, signed joint term `Φ_I`, nonnegative budget `T⁺`, simplex shares plus a cancellation diagnostic `ψ_I`; Tier-A "certified target" branch requiring operator-audited endpoint swaps; A0/A1/A2 scenario bands for uncertified (commercial) upgrades; nonidentification is a first-class verdict.
Evaluation: 14 RQs, 11 baselines, 5 datasets (400 calibration repeat pairs, 45 mechanism×family bridge cells, 480+480 oracle panels, 50 surrogate upgrades, 80 commercial pairs) — with the experiment-spec conceding that everything runs on a **`ResponseSimulator`** and "real model runs are student-supplied later."

## 2. Novelty ledger

Verification searches (2026-08-13): "LLM behavioral drift attribution capability policy format decomposition"; "black-box model change detection API model version drift 2026"; "capability vs alignment change decomposition ... identifiability"; "model update regression testing LLM upgrade cause attribution 2025 2026"; plus targeted checks on arXiv:2604.27789 and arXiv:2604.11581.

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|--------------|-------|--------|
| C1 | First identifiability-gated **black-box attribution** of LLM version drift into capability/policy/format, with nonidentification as a valid output | (a) **arXiv:2604.27789 "Test Before You Deploy: Governing Updates in the LLM Supply Chain" (Apr 2026)** — risk-category testing of silent updates covering *functionality / formatting / safety* regressions (the same trichotomy!), explicitly lists "how to detect and *explain* model drift" as an **open challenge**; (b) arXiv:2602.11083 "Token-Efficient Change Detection in LLM APIs" (B3IT, 2026) — black-box *detection*, no attribution; (c) arXiv:2604.27405 "Beyond the Mean: Within-Model Reliable Change Detection" (2026) — statistical change detection; (d) Chen et al. arXiv:2307.09009 — blended drift, no attribution | Prior 2026 work tests *by* category or detects change; none tests **whether** category attribution is identifiable black-box, none bounds masquerade. 2604.27789 names our problem as open, which *supports* novelty — but the draft **cites none of these 2026 neighbors** | **NOVEL, but framing must position against 2604.27789 explicitly** (a reviewer will find it in one search) |
| C2 | Construction-known control pairs with **measured purity** + oracle-calibrated licensing + quantified masquerade of naive dashboards | arXiv:2606.05396 "Willing but Unable: Separating Refusal from Capability via Abliteration" (2026) — separates policy from capability but **white-box**; OpenReview "Tracing the Drift: Attributing Alignment Failures to Training" — training-time, white-box; Schaeffer et al. 2023 (metric-induced mirage) — same *move* (attributing a claimed model property to instrument choice) on a different question; G-theory (Cronbach) — shares-are-design-relative is a solved-and-named problem | Black-box + version-pair setting is unoccupied; masquerade quantification against 2307.09009's markdown incident is concrete and new | **NOVEL** (defensible), provided classical variance-components lineage is acknowledged rather than reinvented |
| C3 | Energy decomposition `Φ_s/T⁺` with signed cancellation diagnostic `ψ_I` | Standard variance-components / ANOVA identities; Shapley-style attribution literature | Notation-level repackaging; the discussion.md already committed to G-theory vocabulary, which the draft silently dropped | **INCREMENTAL** — keep only as a diagnostic, restore G-theory framing |
| C4 | Oracle-calibrated tolerance-tuple search with three simultaneous false-license bounds | Conformal/selective-inference practice | Machinery, not a contribution; on a simulator it validates code, not the world | **OVERBUILT** — cut to pre-registered gates with CIs |

**Citation hygiene vs sibling failure signature:** zero confabulated citations (all 19 checked resolve) ✔; silent scope inflation vs discussion.md ✔ present (see §3); missed 2026 nearest neighbors ✔ present (2604.27789, 2602.11083, 2604.27405, 2606.05396 all absent). The signature reproduces exactly.

## 3. Consistency vs discussion.md

**Kept (faithful):** instrument-relativity of shares; masquerade as named phenomenon; measured (not assumed) control purity; mixed-dose recovery; nonidentification as a publishable outcome; preregistered naive-dashboard comparison.

**Silent scope changes (all unflagged):**
1. **E3 self-intervention controls on real pairs — DROPPED.** discussion.md's critic called this "the strongest idea in the document… the *only* check that runs on the real commercial pairs themselves" and promoted it to co-primary. The draft has no wrap-v_old intervention, no symmetric-wrap/placebo design. In its place, commercial pairs get only scenario bands, and real validity evidence lives exclusively in self-hosted surrogates.
2. **G-theory commitment — DROPPED.** Stage 3/5 committed the decomposition to variance-component/G-theory form (facets = axis, item, replicate) precisely to inoculate the "shares are instrument properties" critique with a 60-year literature. Replaced by an ad-hoc `‖·‖²_W` energy calculus — "reinvented variance components, badly," which the critic explicitly warned against.
3. **Assumption ledger A1–A5 — DROPPED.** Especially **A5 (calibration transfer, "the single biggest inferential leap")** with its leakage-vs-scale partial test (small→70B). The draft's Tier-A branch instead requires *operator-audited endpoint swaps* — impossible for commercial pairs by definition — so transfer is no longer even partially tested; it is bypassed.
4. **Scale inflation ~10×:** discussion budgeted ~3k probes, 6 real + ~15 control pairs, $2–5k, 250–350 GPU-h, 2–3 months. Draft requires **5 independently-pretrained self-hosted lineages with independently swappable capability/policy/format components** (a hard external requirement the spec itself flags), 45 bridge cells, 960 oracle cases, 50 surrogate upgrades, **80 commercial pairs**, 14 RQs, 11 baselines — then quietly resolves infeasibility by making the simulator the primary substrate.
5. **Sequential gates G1–G3, the G1-fail pivot to measurement critique, the merge-vs-standalone decision rule vs B3.3/B3.4, and the shared probe bank with B3.1 — all DROPPED.** The seed's second question (cross-vendor structure, 检验分解在厂商间是否有共同结构) vanishes entirely — not demoted to exploratory as the discussion prescribed, but deleted.
6. **Concrete masquerade reproductions (E4)** — the 2307.09009 markdown-fencing reproduction, refusal-as-error, knowledge-aware-refusal cases — replaced by abstract synthetic "oracle masquerade panels."

**Does it face the identifiability risk head-on?** *Formally yes, empirically no.* The licensing machinery takes nonidentification seriously — over-seriously: RQ14's own success criterion expects <20% of commercial pairs certifiable, i.e., the method's designed answer on the pairs of interest is "nonidentified." Meanwhile the one test that probes identifiability **on real pairs** (self-intervention) was dropped, and the empirical "validation" is a simulator whose generative model *is* the method's own assumed model `M = Σ_s a_s + I + r` — circular: it can only ever validate the code, not the identification claim. The risk is faced in notation and dodged in evidence.

## 4. Citation audit (load-bearing)

| Citation (as in draft) | Status |
|---|---|
| Chen, Zaharia & Zou, arXiv:2307.09009, "How Is ChatGPT's Behavior Changing over Time?" | CONFIRMED |
| Gao et al., "Model Equality Testing: Which Model Is This API Serving?" (ICLR 2025, OpenReview QCDdI7X3f9) | CONFIRMED |
| Tripathi et al., arXiv:2507.05573, "Prompt Migration…" (Tursio case study) | CONFIRMED (web-verified) |
| Lai et al., arXiv:2302.02080, Gated Fusion | CONFIRMED |
| Xie et al., ACL 2021, "Regression Bugs Are In Your Model!" | CONFIRMED |
| Cai et al., NeurIPS 2022, model-update regression in structured prediction | CONFIRMED |
| Echterhoff et al., arXiv:2407.09435, MUSCLE | CONFIRMED |
| Sclar et al., arXiv:2310.11324, FormatSpread | CONFIRMED |
| Voronov et al., Findings-ACL 2024, "Mind Your Format" | CONFIRMED |
| Mizrahi et al., TACL 2024, "State of What Art?" | CONFIRMED |
| Miller, arXiv:2411.00640, "Adding Error Bars to Evals" | CONFIRMED |
| Madaan et al., "Quantifying Variance in Evaluation Benchmarks" | CONFIRMED |
| Messing, "Hidden Measurement Error in LLM Pipelines…" | CONFIRMED (arXiv:2604.11581, 2026 — draft's catalyzex link should be replaced with arXiv) |
| Zhou et al. IFEval; Röttger et al. XSTest; Cui et al. OR-Bench; Liu et al. EvalPlus; Raji et al. 2111.15366; Biderman et al. 2405.14782 | ALL CONFIRMED |

**No NOT-FOUND, no MISATTRIBUTED.** But: the Related Work section ends with "> This section requires manual completion with proper citations." — an admission shipped inside a "final" draft — and the discussion.md sweep anchors (arXiv:2504.04715 substitution auditing, 2512.03816 logprob tracking, 2506.06975 rank-based uniformity test, RefusalIndex, ContrastiveOverRefusal, Schaeffer 2023, Cronbach G-theory) were never resolved or cited, despite Stage 3's pre-draft verification task pinned with a kill-criterion.

## 5. Gap to implementation

- The spec is a **simulator spec**: all 5 datasets come from `ResponseSimulator`; the "hard external requirement" — 5 independently-pretrained lineages with component-swappable serving stacks + custodian role + 80 commercial pairs — is unresourced and unpriced (discussion budgeted $2–5k; the draft's design is plausibly 1–2 orders beyond that, and no cost estimate appears anywhere in the package).
- ~14 free thresholds (`q, κ*, λ*, s*, ε*, η*, ν*, ν_p*, h_max, h_max^att, ψ*, τ_φ^max, τ_g^min, α_p`) with a nested-resampling grid search whose compute is never budgeted; the 81-tuple scenario grid × exemplar-triple enumeration likewise.
- No power analysis for the RQ thresholds (0.90/0.75/0.80… all round numbers — the exact flaw discussion.md's Stage 6 critic flagged for G1).
- No mapping from the draft's RQ1–RQ14 to a 2–3 month, 1–2 researcher execution plan; no pilot gate ordering (everything is "after freezing…"), no first-week deliverable.

## 6. Verdict + top-3 fixes

**Verdict: MAJOR REVISION (reject in current form).** The core direction is right and the novelty is real — verified: no published black-box capability/policy/format attribution of version drift exists as of 2026-08, and the closest 2026 work (arXiv:2604.27789) names the problem as open. But the draft replaced discussion.md's disciplined, gated, feasible design with an unfalsifiable-by-construction licensing bureaucracy validated on its own simulator, dropped the only real-pair validity check, dropped the pre-committed G-theory framing and A1–A5 ledger, and shipped an unfinished Related Work missing every 2026 nearest neighbor.

**Top-3 fixes (applied in the revision):**
1. **Re-anchor to discussion.md's design:** G-theory variance-component model, explicit A1–A5 assumption ledger (each paired with its test — A5 restored with the leakage-vs-scale ladder), E1–E5 experiment structure with sequential pre-registered gates G1–G3 and the G1-fail pivot to a measurement critique; restore **self-intervention controls (E3, symmetric wrap + placebo) as co-primary** on real pairs; restore concrete masquerade reproductions (E4) and the exploratory cross-vendor question (E5).
2. **Deflate scale to the audited budget** (~3k shared probe bank with B3.1, 9–12 control + 4–6 mixed-dose pairs on open-weight 7–8B models plus 70B transfer anchors, ≥6 real pairs / ≥2 vendors minimum viable config, ≈$2–5k + ≈300 GPU-h); keep the simulator only as a pre-registration power-analysis tool, never as evidence; keep the draft's best inventions (benign-cross-effect-aware purity grading, nonidentification verdict, signed cancellation diagnostic) in simplified, feasible form.
3. **Finish and modernize Related Work:** add arXiv:2604.27789 (Test Before You Deploy), 2602.11083 (B3IT), 2604.27405 (Beyond the Mean), 2606.05396 (Willing but Unable), fix Messing to arXiv:2604.11581, resolve the discussion's sweep anchors, and state the contribution sentence the discussion fixed: *the identification framework, not the three-axis trinity, is the claim.*

## Inferred 4 unresolved MAJOR critiques

Reconstructed from the package's internal tensions (the room log is not in the export):
- **M1 — Circular validation / simulator substitution:** every RQ that "validates identifiability" draws data from a simulator implementing the method's own generative model; no evidence path touches a real upgrade until RQ14, which is designed to return "nonidentified." (Matches: spec Open-Decision #1 admitting the simulator is primary.)
- **M2 — Feasibility of the bridge panel:** 5 independently-pretrained families with independently swappable capability/policy/format serving components + custodian + 80 commercial pairs is unobtainable at the stated tier/budget; the spec offloads it to "student supplies later."
- **M3 — Dropped real-pair validity evidence:** elimination of E3 self-intervention (and of A5's partial transfer test) leaves the commercial-pair claims resting entirely on untestable transport from synthetic controls — precisely the identifiability risk the audit flagged, now unmitigated.
- **M4 — Threshold soup without power justification:** ~14 interacting calibrated tolerances and 90/75/80-style success criteria with no power analysis, plus an unfinished Related Work — the paper cannot state what would make it fail honestly, while its complexity guarantees no one can run it.
