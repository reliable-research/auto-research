# Pengsida Stage Review — B3.5

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs, quoting the first assembled draft where prose exists to quote; Stage 5 was checked against the first assembled draft of `paper_draft.md` directly. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon (cross-vendor drift synchrony) occurs" with no new pipeline proposed as a fix for it — the testbed (axis-partitioned battery, capability-residualization test, dual-alignment and axis-robustness checks, two-index diversity trend) is the *analytical apparatus* that makes the phenomenon observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification, `study_type: empirical` from Stage 1, and `paper.md`'s own Step 2 archetype note (primary `empirical`, secondary `technical_artifact` only as a pivot target if the central hypotheses fail). Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "raw agreement in how vendors' models change over time therefore carries no information about shared pipelines on its own, since a universal capability attractor guarantees some positive drift correlation regardless of whether anything is actually shared" is a first-principles framing of why the naive version of this question would be uninformative, not a patch bolted onto an existing pipeline. The stakes are concrete and consequential, not a generic AI-importance appeal: "if either mechanism operates across vendors over calendar time, the independence assumption behind multi-vendor redundancy breaks silently — the practice keeps looking diversified while no longer functioning as a hedge." The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes, with zero method leak (no mention of residualization, the battery, or the correlation test until paragraph 3's related-work framing and paragraph 5's method preview).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded, each ending on a problem-tied limitation rather than a generic one — e.g., "[the recursion and model-collapse works] are validated in controlled simulations on toy or single-family models, not by auditing whether the effect is visible in real, deployed multi-vendor version sequences — exactly the audit this paper runs." That clears the "citation dump" failure mode. But in the version of the section produced directly from the Stage 3 structured table (before the nearest-neighbor sentence was added), the reader was left to infer for themselves which of the four threads was the *closest* prior work — the table format (citation / I-O framing / limitation, one row per work) ranks nothing. Digest N3's own framing already names Artificial Hivemind as the paper's single nearest analog ("the canonical non-corpus paper... the direct nearest neighbor"), but that ranking had not yet been surfaced as an explicit standalone sentence in the assembled prose. Per the Stage 2 bar: "the single closest prior work [must be] named and its delta stated plainly... hiding the method-twin is the fastest way to a desk reject... confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence, before the four thematic paragraphs, naming Artificial Hivemind as the closest prior work and stating the precise delta ("a time axis, a capability-improvement control, and an explicit independence null — the three things a single snapshot cannot supply on its own"), rather than leaving the reader to rank the four threads unassisted.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the axis partition (K_cap/K_neu), the residualized drift vector d̃, the noise floor ν, and the diversity index D(τ) are all given in Problem Definition/Methodology ahead of any claim that invokes them, so nothing is "named after the fact." The inferential chain is licensed at its one load-bearing hinge: "a benign capability-only explanation predicts correlation concentrated on the capability-loaded axes and attenuated after residualization, while genuine homogenization predicts correlation that survives both cuts" is exactly the step that makes the residualization test non-circular — the draft states this explicitly (Methodology, "Capability-Residualized Correlation Test") rather than asserting the residualization procedure's validity by fiat. No orphan components — every one of the six modules (battery validation, capability-residualized correlation, dual-alignment check, axis-robustness check, diversity trend, noise-floor gate) traces to a named sub-problem in `pipeline.md`'s Stage 4, with no leftover machinery introduced only in the Methodology section.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ3 is a genuine falsification design (recomputing correlation after residualizing out the shared capability direction to see whether the verdict *changes*, not just correlates with something else), and RQ2/RQ3 together are explicitly built to rule out the single strongest alternative explanation (capability improvement) named in the Introduction. But the first assembled draft's RQ subsections stopped at an "**Expected outcome**" line — e.g., for RQ3: "if raw correlation was driven by the shared capability direction, residualized correlation is substantially attenuated relative to raw correlation; a homogenization claim requires that it is not" — without a paired statement of what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, *if the claim were false*, the result would differ... demand at least one such test," stated as an explicit check, not left implicit in the expected-outcome wording. An expected outcome alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had exactly this discipline (its F1/F2/F3 fallback wording, e.g. "we find no evidence of cross-vendor behavioral homogenization beyond shared capability improvement... which — against the prevailing monoculture concern — supports multi-vendor redundancy as a risk hedge") that had not yet been carried into the first assembled `paper_draft.md`'s RQ subsections in falsification-condition form.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all eight RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s F1/F2/F3 fallback language and the walking-skeleton "stop" condition in its Step 9).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Large language model vendors ship successive versions... a growing body of deployment practice treats this vendor plurality itself as a safeguard" / "Yet the premise has never been tested longitudinally" / "The nearest existing work to this question is the Artificial Hivemind study..." / "Turning this gap into a measurable claim surfaces its own obstacles" / "Our approach turns each obstacle into a specific, checkable design choice" / "We evaluate this design across dated version panels...") reconstructs the whole five-move arc (problem → gap → nearest prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across the title, abstract, and Contributions list: "only the capability-orthogonal component of drift is a valid signature of shared pipelines." The Conclusion names two real forward-looking limitations (the unverifiable causal mechanism behind any correlation, and low statistical power from a small accessible vendor set) rather than only recapping the abstract, and explicitly states the paper reports correlation, not verified causation — matching the honesty standard set by its own nearest neighbor (Artificial Hivemind's causality caveat).

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening ("The single closest prior work to this paper is the Artificial Hivemind study, and its own stated boundary marks the precise gap this paper is built to close..."), naming the closest prior work and stating the delta plainly, rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the eight RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — 2026-07-04

> Run against **goal.md §3's 8-item checklist**, using **guidance.md** as the construction standard, against the three static input files (`README.md`, `digest.md`, `paper.md`) and the just-upgraded `discussion/reference_candidates.jsonl` (Task 1 of this session). Per the runbook this gate blocks Phase B; **no Phase B/C was attempted** — no real experiment compute exists in this environment, and the existing `discussion/paper_draft.md/.tex/.pdf`/prior `stage_review.md` content above is a **separate, already-completed `pengsida-stage-reviewer` prose review of Phase E output** (Stages 1–5, run in an earlier session) — it is not a substitute for this goal.md §3 gate and is left untouched. This section is the first time goal.md's own 8-item Phase A checklist has been run explicitly for B3.5.

### 1. Digest self-verification — **REVISE (fired, fixed)**

All of N0–N12 + Claims + Self-verification notes are present in `digest.md`, and every node I checked carried a 3-part `absence_comment` (what_missing / why_matters / implication) **except N12** (Contribution Type), which stated `value`/`rationale`/`source` but had no `status` field and no `absence_comment` at all — a real gap against the rule "every non-GIVEN item carries its 3-part absence comment."
**Fix applied:** added `status: NOT_FOUND` + a full 3-part `absence_comment` to digest.md's N12, citing that the `empirical` classification is reasoned-by-analogy (to ArtificialHivemind) rather than extracted, and that it gates which Part-2 evidence standard applies downstream.
Cross-node references all resolve: N4's `affects_works` ⊆ N3 citation_keys (checked, all 5 strings match verbatim); N6's `challenge_id`/`mechanism_components` ⊆ {C1..C5}/{M1..M5} (checked); N8's `addresses_challenges`/`evaluates_mechanisms`/`tests_contributions` all resolve (checked). No other gaps found.

### 2. Reference-cache integrity — **REVISE (fired, fixed — was the session's biggest finding)**

Before Task 1 of this session, `discussion/reference_candidates.jsonl` held 150 records in the ad hoc harvest schema (`topic_id`/`rank`/`score`/`ref_id`/...), **none had a `verdict`** (all implicitly `pending`), and **none of digest.md N3's 8 citation keys** (`GreatModelsThinkAlike`, `CommunityAlignmentMonoculture`, `MultiEntityRecursion`, `DiversityAwarePO`, `DQO`, `MeasureDatasetDiversity`, `ModelCollapseMemorization`, `ArtificialHivemind`) resolved to a cache record by that name — N3 had in fact been grounded against a *different* local file, `topics/corpus/ideas.jsonl` (a 11,683-row OpenReview-proposal corpus), not against `reference_candidates.jsonl` at all. That is a direct violation of "every N3 key is a selected cache record."
**Fix applied (Task 1 + this check, same session):**
  (a) Rewrote all 150 harvested candidates into the goal.md §1 canonical schema, read/skimmed every `digest_path`, and set `verdict: selected|rejected` + `relevance` + a specific one-sentence `why` for each — **7 selected** (`PairedSeedVarianceReduction2512`=background, `LawMultiModelCollaboration2512`=adjacent, `BoundarySyncRepCoupling2607`=method-twin, `ProxyModelDataCuration2512`=background, `SafeFutureDangerousPast2512`=adjacent, `DeliberatingAICrowds2512`=adjacent, `ArtificialHivemind`=baseline), **143 rejected** with a paper-specific (non-generic) reason each. This harvest was poorly targeted for this topic — most of the 110 arXiv rows were an undifferentiated recent-arXiv feed (agentic systems, code generation, domain benchmarks, etc.) and the 40 "openview" rows were an unrelated generic ACL-2023 dump — so a ~5% selection rate is a harvest-quality finding, not a search failure; flagged for the next freshness sweep (goal.md §1's staleness clause) to re-harvest with topic-specific angles ("cross-vendor drift", "behavioral homogenization LLM", "model ensembling redundancy", "algorithmic monoculture alignment").
  (b) Appended the 7 corpus-sourced N3 records (`GreatModelsThinkAlike` through `ModelCollapseMemorization`) as `selected` cache records with `key` strings matching digest.md's N3 bracket names exactly, `ids.openreview` set, `pdf_path`/`digest_path` = `null` (no PDF cached for this proposal-level corpus) and `verified.id_resolves = false` accordingly, each `why` citing the specific digest.md N3/N4 role it plays.
  (c) Spot-checked 3 ids by extracting page 1 of the cached PDF with `pdftotext` and confirming title + arXiv id match the cache record: `ArtificialHivemind` → confirmed arXiv:2510.22954 (matches digest.md's canonical citation exactly); `LawMultiModelCollaboration2512` → confirmed arXiv:2512.23340; `BoundarySyncRepCoupling2607` → confirmed arXiv:2607.01600. No mismatches found.
  (d) No `pending` entries remain anywhere in the file (157 total records, all `selected` or `rejected`).
`reference_candidates.jsonl.bak_pre_upgrade_20260704` retains the pre-upgrade 150-row file for audit.

### 3. Tag discipline — **PASS**

Every digest.md assertion I sampled carries `[GIVEN]`/`[HYPOTHESIS]`/`[PLACEHOLDER]`/`[GROUNDED:corpus]`/`[CANONICAL:non-corpus]`; no silent `[HYPOTHESIS]`→`[GIVEN]` promotion found (e.g., N9's results stay `[HYPOTHESIS]`/`[PLACEHOLDER]` throughout, never asserted as findings; N2's motivation items are explicitly `[HYPOTHESIS]` except the one item that is genuinely `[GIVEN]` from the seed).

### 4. Claim–Evidence Map completeness — **PASS**

All 8 rows of `paper.md`'s Claim–Evidence Map trace to an H-id (H1/F1, H2/F2, H3/F3) or a `supported-by-design` definitional statement (the battery's existence, the causal-limit statement); every H-id (H1, H2, H3) has a pre-committed fallback; the conditional redundancy-validity claim is explicitly marked as "no new quantity" rather than an orphan. No claim lacks a trace; no H-id lacks a fallback.

### 5. Hypothesis/assumption machinery — **REVISE (fired, fixed)**

H1/H2/H3 each substantively fill guidance.md §3.1's seven slots (binary statement, `applies_if` via the listed Assumption line, metric, test, alpha/correction, effect floor, aggregation rule, verbatim fallback) — organized under prose sub-headings rather than seven literal bullet labels, which I judged sufficient (content present, not just structure).
The Assumptions table (A1–A6), however, only filled 3 of guidance.md §3.2's 5 slots explicitly (assumption, failure_mode, a merged detection+consequence cell) — **no explicit `gate: PG-j` label existed anywhere**, and "consequence: what happens to which H* if it fails" was folded informally into the detection cell rather than stated as its own slot, contrary to "every A* fills §3.2."
**Fix applied:** rebuilt the Assumptions table with explicit `PG-1`..`PG-6` gate IDs (all resolving inside the walking skeleton, per Step 9) and a separate "Consequence if it fails" column naming which H* is affected and how (drop/restrict/re-instrument/block), citing guidance.md §3.2.
B0 (`B0-NoDrift`) + B-alt (`B-alt-RisingTide`) + F-G1 were already all present with pre-committed wording — no gap there.

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2's A2 evidence standard) — **REVISE (fired, fixed)**

Checked all 10 Part 6 items against the plan; 4 gaps found and fixed, 6 items already passed:
- **Item 1 (R1 estimand)** — missing: no single labeled sentence stated quantity + unit of analysis + reference population + decision fed, the way guidance's own 2607.01233 example does. **Fixed:** added an explicit "Estimand (R1, guidance.md §3.4)" sentence to paper.md Step 5.
- **Item 4 (A* detection + gate)** — same gap as checklist item 5 above; fixed there (PG-1..PG-6).
- **Item 6 (instrument's 5-step R2 plan)** — only R2 step③ (κ≥0.7 human validation) was present for the M1 probe battery; steps ①②④⑤ (external grounding, held-out refinement with named ops, confusion-structure inspection, freeze-before-scale) were absent. **Fixed:** added a full "Instrument validation plan for M1 (R2...)" subsection walking through all 5 steps.
- **Item 8 (≥1 mechanism analysis, R6)** — Part 2's A2 evidence standard requires R6 as a component distinct from the rival-explanation ablations (R5); the existing RQ3 axis-robustness check is an R5-style falsification test, not a "why" mechanism analysis. **Fixed:** added a "Mechanism analysis (R6)" subsection specifying a pre-registered per-axis log-odds decomposition of which behavioral axis carries any detected homogenization signal.
- **Item 9 (power per cell; thin cells INCONCLUSIVE)** — the plan named low power as a threat (N10-t5) but never pre-declared a concrete INCONCLUSIVE rule, leaving open the Situation-5 risk of an underpowered cell being silently scored PASS/FAIL/null. **Fixed:** added an explicit "Power statement and INCONCLUSIVE pre-declaration" subsection with a numeric CI-half-width / minimum-pair-count rule and a renormalization-over-powered-cells clause.
- **Items 2, 3, 5, 7, 10** — already **PASS**: verb check (Step 3 self-audit: isolate/measure/test/gate/residualize/falsify, no integrate/unify/leverage); H* seven-slot content (see item 5); B0+B-alt+F-G1 present; every design constraint's confound is named in substance (residualization removes the "rising tide" capability confound; B-alt names C2 explicitly); archetype named (`empirical` primary / `technical_artifact` pivot-only secondary) and — after the four fixes above — the Part 2 A2 evidence standard (validated instrument + controlled comparison + effect-size-floored tests + rival-explanation ablations + ≥1 mechanism analysis) is now actually met by the plan, not merely intended.
Also fixed in passing: **undefined term** — "CAPA" was used three times in paper.md (Step 5 table, E2, B-alt) without ever being spelled out; added its definition ("Chance-Adjusted Probabilistic Agreement," citing `[GreatModelsThinkAlike]`) at first use.

### 7. Stage cross-check (advisory) — **PASS (already discharged)**

`pengsida-stage-reviewer`'s Stage 1–5 review (top of this file) already cross-checked N1↔Stage 1 (Problem+Motivation), N3/N4↔Stage 2 (Related Work), N6↔Stage 3 (Method), N8/E*↔Stage 4 (Experiments), and the archetype from `paper.md` against Stage 5 (Writing) — its two REVISE findings were fired and fixed (nearest-neighbor sentence; falsification-condition lines) before this session started. Advisory only; nothing here blocks Phase A independently, and no new cross-check gap was found in this pass.

### 8. Taste audit currency — **PASS, no re-run needed**

`taste_audit.md` (🟢, human-shaped, all 3 verdict conditions non-firing) was run against the Stage 2/Stage 5 motivation+method pair. This session's fixes (Estimand line, PG-gate labels, R2 5-step expansion, R6 mechanism analysis, INCONCLUSIVE rule, CAPA definition) added rigor scaffolding only — none altered the Step 0 asymmetry sentence or the Step 5 formal definitions' substance (no term's formal definition changed meaning; the two new subsections are additive). No material edit to the audited material occurred, so the recorded 🟢 remains current; no re-run triggered.

### Gate result: **REVISE → fixed in-session → now PASS**

All 4 fired REVISE findings (items 1, 2, 5, 6) were fixed directly in `digest.md` / `paper.md` / `discussion/reference_candidates.jsonl` during this pass, each citing the guidance.md section it violated. No `STOP`-level finding occurred (no unresolvable tag violation, no orphaned claim, no unfixable missing machinery). **Phase A now passes all 8 checklist items.** Per goal.md, **Phase B/C were not attempted** — they require real experiment compute this environment does not have; the gate is recorded as clear for whenever that compute becomes available.
