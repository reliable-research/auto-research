# Pengsida Stage Review — B1.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs (mapping: pipeline Stages 1+2 → pengsida Stage 1; pipeline Stage 3 → pengsida Stage 2; pipeline Stages 4+5 → pengsida Stage 3; pipeline Stage 6 → pengsida Stage 4); Stage 5 was checked against the assembled prose in `paper_draft.md`'s Introduction/Abstract/Conclusion. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs" — no new verifier design is proposed as a fix; the measurement instrument (locality-scoped verifier suite, topology-stratified bypass constructor, disjoint terminal oracle, strongest-checker control) is the *analytical apparatus* that makes the phenomenon (checkpoint bypass) observable and attributable, not a method competing against baselines to win. This matches digest N12's own explicit `empirical` classification ("a *measurement* of a failure mode of an existing verification paradigm... the defining signature of an empirical study") and `study_type: empirical` confirmed at pipeline Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any instrument appears — the motivation states plainly that "whether this local-checking paradigm is actually sufficient evidence of true task success... has not been directly measured," and the stakes are concrete and structural, not a generic AI-importance appeal: "scores, rewards, and completion judgments derived from this paradigm may systematically overstate real competence — the verifier itself becomes the attack surface, not the task." The refined objective is honest about scope from the outset (a *lower bound* over a pre-registered sampling distribution, never a worst-case or population claim), which is exactly the evaluability discipline this stage rewards rather than a hedge. The refiner pass at pipeline Stage 2 also does real motivational work beyond restating Stage 1's outputs — it ties each of the three promised breakdowns (strategy, topology, natural incidence) to an independently actionable consequence ("which strategy dominates tells a benchmark designer where to harden first... whether topology modulates the rate tells designers whether risk grows with task complexity... natural incidence... is what distinguishes a constructibility result from an active measurement") rather than leaving "why not just report one number" unanswered.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The three threaded paragraphs in `paper_draft.md`'s Related Work are genuinely argued, not a citation dump — each ends on a problem-tied limitation ("none isolates and measures the *rate* at which currently standard, milestone-scoped checkers can all pass while a separately computed terminal ground truth fails"; "neither audits the dual question this paper asks: whether an independent, milestone-scoped verifier can be satisfied while the graph's prerequisites are unmet in the first place"). But, exactly as in the B5.5 precedent, the section never states in one place which single prior work is the *closest* competitor overall. Pipeline Stage 3's own critique/refiner already did this ranking work — `is_potential_baseline: true` was assigned only to StepORLM, with the refined note clarifying its role as "the closest existing candidate for an alternative verification-design arm" — but that ranking never made it into the assembled Related Work prose. A reader sees three parallel threads (grading remedies, prerequisite planning, step-wise locality) and has to infer for themselves which is the nearest neighbor. Per the Stage 2 bar: "Hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming StepORLM (and LatentVeracity, which makes the same granularity point from the other direction) as the closest prior work, stating the precise three-part delta (DAG, adversarial construction, disjoint oracle), rather than leaving the reader to rank the three threads themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Every construct is defined precisely *before* it is used — `Σ, V, E, Φ, Ω`, the local-signal restriction `view_k(τ)`, the all-pass indicator `A(τ)`, and the bypass event `B(τ) := A(τ)=1 ∧ Ω(τ)=0` are all given in Problem Definition ahead of any claim invoking them. The one load-bearing inferential hinge — "a milestone verifier certifies a local, observable signal, but the prerequisite state that signal is supposed to imply is a property of causal history, and the map from history to signal is many-to-one" — is stated explicitly and is exactly what licenses "satisfying every checkpoint is strictly weaker than establishing what those checkpoints jointly certify," rather than asserting insufficiency by fiat. No orphan components: all five methodology modules (topology-stratified sampler, locality-scoped verifier suite, injection provenance probe, strongest-checker attribution control, disjoint oracle with audit) trace 1:1 to a named sub-problem from pipeline Stage 4, and each reappears as exactly one Stage-4-equivalent RQ — no leftover machinery, no sub-problem left unaddressed.

**Note for Stage 4:** the discharge test here isn't ablation — it's whether the finding is falsification-tested, not merely reported as a correlation. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served *structurally*: RQ5 (the strongest-checker attribution control) is a genuine falsification design, recomputing the bypass rate against the richest realistic still-milestone-scoped checker to see whether the vulnerability survives, rather than merely observing that it correlates with weak checkers. But the first assembled draft's six RQ subsections all stopped at "**Expected outcome.** ... demonstrating that independent per-milestone verification is not a sufficient proxy..." (RQ1) and its five siblings, without ever stating the converse — what specific result would *refute* each expected outcome. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what turns a pre-registered threshold into a breakable claim for all six RQs, not just the one (RQ5) whose design already happens to be adversarial in spirit.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the concrete statistical condition that would refute each expected outcome (e.g., for RQ1: "Refuted if the Wilson 95% lower bound on the observed rate does not exceed 0.05... that would mean constructed bypass trajectories cannot reliably defeat milestone verification on this suite"), not a vague restatement of the outcome's negation.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Long-horizon agent tasks are rarely graded end to end." / "Yet this reasoning quietly assumes something that has never been directly measured..." / "The closest existing work approaches this concern from adjacent angles without closing it." / "Turning this gap into something measurable surfaces its own difficulties." / "Our approach turns each of these obstacles into a specific design decision." / "We evaluate this design on multi-step tasks spanning coding and filesystem operations...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title, abstract, and the first contribution bullet: "milestone checking is a many-to-one projection of causal history onto a local signal, so satisfying every checkpoint is strictly weaker than establishing the prerequisite state those checkpoints jointly imply." The Conclusion names two real forward-looking limitations (the sampled-lower-bound scope of the bypass space; restriction to domains with a canonical, independently-computable terminal state) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence at the start of the Related Work section, naming StepORLM and LatentVeracity as the closest prior work and stating the three-part delta (explicit DAG, adversarial reorder/skip/inject construction, disjoint validated oracle) plainly, rather than leaving three parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf` (`pdflatex` twice, exit code 0, zero `! ` errors in the log, zero replacement-character mismatches in `pdftotext` output; final PDF is 12 pages). `.aux`/`.log`/`.out` were deleted afterward.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3 against `README.md` / `digest.md` / `paper.md` (the pre-registered spec), applying `guidance.md` as the evidence standard. This is a separate, later gate from the Stage 1–5 review above: that review checked the `auto-research-discussion` prose assembly (`paper_draft.*`); this one re-checks the **input bundle itself** — including the just-rebuilt `reference_candidates.jsonl` (150 candidates triaged: 11 `selected`, 139 `rejected`, none left `pending`). Date: 2026-07-04.

### 1. Digest self-verification — **REVISE (fired, fixed)**

Re-executing `digest.md`'s own V-01–V-12 self-verification pass: cross-node references (N4→N3 keys, N6→N5/M ids, N8→M/C/CO ids, N9 rq_id↔N8 ids) all resolve correctly, and N0–N12 + Claims are all present. But V-02 claims *"every node with status != FOUND carries a full 3-part `absence_comment`"* — this was **false as written**: `N2` (Motivation, status `PARTIAL`) and `N12` (Contribution Type, status implicitly non-`FOUND`, and missing its own `Status` line entirely) had no `absence_comment`. Fixed directly in `digest.md`: added a 3-part `absence_comment` to N2 (explaining the motivations are pipeline-reconstructed, not author-stated) and added both a `Status: PARTIAL` line and a 3-part `absence_comment` to N12 (explaining the `empirical` tag is this pipeline's classification, not a self-declared contribution type, and cross-referencing that it agrees with `paper.md` Step 2's independent archetype classification). V-02's claim is now accurate. **Citing:** goal.md §3 item 1's own requirement; guidance.md Part 6 is not the source here (this is digest.md's internal self-check contract).

### 2. Reference-cache integrity — **STOP (not fixable by a text edit; blocks Phase B)**

This is the headline finding. `digest.md`'s N3 (Related Works) grounds all eight related-work entries — TED (OpenReview:fHsVNklKOc), XENON (N22lDHYrXe), Gistify (nmdDgo4OXC), StepORLM (ZrgxU8WMmG), LatentVeracity (eux1cp8GqC), WebArbiter (canA6Ef0RP), GTool (bn47cqGQ7l), DiffTaskGraph (2HvgvB4aWq) — against a *different* corpus (`topics/corpus/ideas.jsonl`, per N3's own method note). `paper.md` cites two of these directly (TED in A3, and Gistify/TED implicitly via the Step 2 archetype-exemplar list), and the *(pre-existing)* `paper_draft.md` Related Work section builds its entire nearest-neighbor argument (StepORLM/LatentVeracity) around them.

None of these eight works — checked by both OpenReview ID and by title/first-author string — appear anywhere in this topic's actual `reference_candidates.jsonl` (confirmed by direct grep before Task 1 began, and reconfirmed against the final triaged file: 0 matches). **The topic's local reference cache and the digest's own N3 grounding are built from two disjoint corpora.** Per goal.md §3 item 2 ("every N3 key is a `selected` cache record") this fails outright — not one N3 key is even a cache *record*, selected or rejected. Per goal.md §2's table, this is exactly the failure the Phase A gate exists to catch, and per goal.md §3's framing ("one failure blocks Phase B"), **this alone blocks Phase B**, independent of every other checklist item.

Task 1's triage of the 150 harvested candidates against the real cache found 11 legitimate `selected` entries (5 `method-twin`, 5 `adjacent`, 1 `background`) that are topically relevant but are *not* substitutes for the eight N3 works — the harvest queries that produced these 150 evidently did not target the specific mechanisms (prerequisite-DAG planning, process-reward locality, checklist-checker gaming) that N3's method note says it searched for; the near-alphabetical clustering of the OpenReview/ACL batch (111–150) is itself evidence the harvest angles were generic, not query-targeted (`guidance.md` Part 5's "when the cache is thin... re-harvest from new angles" applies literally here — 11 selected is within the expected 5–20 range, but zero of them cover the load-bearing method-twins already committed to in prose).

**Not fixed here, by design:** this requires an actual re-harvest (new query angles: "process reward model locality," "prerequisite dependency graph planning," "benchmark checker gaming," the literal terms XENON/GTool/StepORLM/etc. use) — a Phase-①/② action, not a Phase A text patch, and out of scope for this pass per the task's own instruction to stop at the Phase A gate rather than run further pipeline phases. **Recommendation for whoever resumes this topic:** before Phase B, re-harvest specifically for the eight N3 titles/ids (or true equivalents), digest them into this cache, and re-run Phase A item 2.

### 3. Tag discipline — **PASS**

No untagged assertions found in `digest.md`; every content-bearing bullet across N0–N12 and Claims carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`. No silent HYPOTHESIS→GIVEN promotion detected (N9's results block is explicit: "Every item below is `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`"). `paper.md` is a separate genre (pre-registered spec, not a tagged digest) per goal.md's file contract and is not held to this tag scheme.

### 4. Claim–Evidence Map completeness — **REVISE (fired, fixed)**

Four of the map's seven rows already traced cleanly to H1–H4 with fallback coverage. But the row *"the measured cause is structural locality, not weak checkers"* traced only to **"B-alt control"** — no H-id, and critically, the B-alt paragraph in Step 6 stated only the "if it survives" interpretation ("if `ρ` remains ≥ half its weak-checker value... the cause is structural locality") with **no pre-committed downgrade wording for the case where it doesn't survive** — an orphan half of guidance.md §3.3's B-alt discipline ("pre-commit the downgrade wording: what the claim becomes if the effect survives the rival **vs. dies**"). Fixed directly in `paper.md`: formalized the B-alt control as **Hypothesis H5** with all seven guidance.md §3.1 slots (statement/applies_if/metric/test/alpha/effect_floor/aggregation) and added **Fallback F5**, the verbatim downgrade sentence for when H5 fails (bypass rate falls by more than half against the strongest checker → the structural-locality mechanism claim is conceded, Claim 1 survives downgraded, Claim 3 does not). Updated the Claim–Evidence Map row to `H5 (B-alt control) | needs-experiment; fallback-covered (H5 fallback F5)` and updated the Holm-correction preamble and Global fallback F-G1 paragraph to reference H5 by name. No orphans remain: every claim row now traces to an H-id-with-fallback or an explicit supported-by-design definition.

### 5. Hypothesis/assumption machinery — **REVISE (fired, fixed)**

H1–H4 already filled all seven guidance.md §3.1 slots (binary statement, applies_if, metric, test, alpha, effect_floor, fallback); H5 now does too (added under item 4). B0 and F-G1 already carried pre-committed wording; **B-alt's missing downgrade wording is the same fix as item 4.**

Separately, the A1–A6 assumption ledger (guidance.md §3.2) had detection methods for all six assumptions but **gate** and **consequence** were inconsistently labeled — A4 named an explicit pilot-gate threshold, but A1/A2/A6 only informally gestured at "pilot gate"/"walking-skeleton exit check" without a stable id, and A3/A5 had no gate concept stated at all, and none of the six had an explicit **consequence** field (guidance.md §3.2: "what happens to which H* if it fails — degrade, restrict scope, or block"). Fixed directly in `paper.md`: relabeled all six with explicit `Gate:` and `Consequence:` fields — A1→PG-0 (pre-pilot domain selection, blocks), A2→PG-2 (walking-skeleton exit criterion iii, blocks/invalidates whole run), A3→no hard gate, continuous per-checker-type reporting discipline, restricts scope, A4→PG-1 (walking-skeleton exit criterion ii, blocks), A5→design-time trace filter, degrades (thin-cell → INCONCLUSIVE), A6→PG-3 (pilot count gate, degrades to descriptive-only if unmet). Also added an explicit **power statement** to A6 (target power ≥0.9 for the H4 effect floor `ρ_nat≥0.02` at α=0.05, with the ≥200-rollout n justified against that floor) and the explicit pre-declared **INCONCLUSIVE** rule guidance.md Part 4 situation 5 requires for thin cells — previously `paper.md` never used the word "INCONCLUSIVE" anywhere despite Part 6 item 9 requiring it.

### 6. Method-rigor audit — **REVISE (fired, fixed)** + archetype evidence standard

Walking guidance.md Part 6's 10-item self-check against `paper.md`:
1. **Estimand in one sentence (R1) — was missing, fixed.** Step 5 had full notation but no single estimand sentence (quantity/unit/reference population/decision) preceding it. Added one directly above the Notation block.
2. Verb check — PASS (Step 3 self-audit + `taste_audit.md`, independently confirmed, verb family `formalize/isolate/construct/measure/bound/gate`, no integrate/unify/leverage).
3. Every H* has all seven slots incl. verbatim fallback — PASS after items 4–5's H5/F5 addition.
4. Every A* has detection + gate — PASS after item 5's fix.
5. B0+B-alt+F-G* present with pre-committed wording — PASS after item 4's F5 addition.
6. Every instrument has the 5-step R2 plan with acceptance threshold — **N/A, correctly so.** The only human-audit instrument (A4's manual stratified oracle-verdict audit) is auditing a *deterministic* function's correctness (hash-set/output equality), not an LLM-judge/taxonomy/rubric in R2's sense; R2's external-grounding+κ-validation protocol is the wrong tool here, and the pilot-gate threshold (≤5% false-inconsistency, PG-1) is the right-shaped rigor recipe for this kind of instrument instead.
7. Every design constraint names its confound (R3) — PASS (B0: "attributable to the bypass mechanism, not baseline M2/M4 disagreement"; B-alt/H5: "isolates structural locality from weak-implementation"; A2: disjointness "removes" the correlated-error confound) — present in substance, if not literally labeled "constraint X removes confound Y."
8. ≥1 mechanism analysis budgeted (R6) — PASS (RQ_INF_1 strategy-dominance and RQ_INF_2 topology-modulation are the mechanism layer; H5/B-alt is the attribution layer).
9. Power stated per cell; thin cells pre-declared INCONCLUSIVE — **was missing, fixed** (item 5's A6 power statement + INCONCLUSIVE rule; RQ1–RQ3's sample sizes (≥300 trajectories, ≥200 tasks) should also get an explicit power derivation before Phase B, not just A6 — flagged as a follow-up, not blocking, since A6/H4 was the one case with zero power language anywhere).
10. Archetype named + Part 2 evidence standard met by the plan — **PASS with a scope note.** Archetype = A2 empirical/measurement (paper.md Step 2, digest N12, `pengsida-stage-reviewer`'s Analysis/Finding classification, and `taste_audit.md`'s Empirical-Mapping tag all agree). Evidence standard met on paper: validated instrument (A4/PG-1), controlled comparison (B0), pre-registered effect-floor tests (H1–H4/H5), rival-explanation ablation (H5/B-alt), ≥1 mechanism analysis (RQ_INF_1/2). Part 5's "harvest 2–3 recent top-venue exemplars of the same archetype... digest them, relevance: background" is only **partially** met — Task 1 found exactly **1** background exemplar (`PLMCalibrationCloseLook2023`) against the recommended 2–3; noted as a follow-up for the same re-harvest pass that item 2 already requires, not a separate blocking gap.

### 7. Stage cross-check (advisory) — **PASS (already run)**

The Stage 1–5 review above (pre-existing, `pengsida-stage-reviewer`) already covers N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E*↔Stage 4 against the `auto-research-discussion` `pipeline.md` outputs, with two REVISE items found and fixed at the time. Advisory only; does not itself block, and nothing in this Phase A pass contradicts it. Note for whoever runs Phase G later: that review's Related Work nearest-neighbor sentence (StepORLM/LatentVeracity) inherits item 2's cache gap — the citation is grounded in the digest's separate corpus, not this topic's `reference_candidates.jsonl`.

### 8. Taste audit currency — **PASS, still current**

`taste_audit.md` was run against the Stage 2 (confirmed motivation) / Stage 5 (confirmed method summary) text. None of this Phase A pass's fixes touched the asymmetry statement (Step 0), the archetype classification (Step 2), or the method-summary sentence taste-audited — the Estimand addition, H5/F5 formalization, and A-ledger relabeling are all machinery *underneath* the audited sentences, not edits to them. No re-audit required.

---

## Phase A gate result: **FAIL** (blocks Phase B)

Items 1, 4, 5, 6 fired REVISE and were fixed directly in `digest.md`/`paper.md` in this pass (see each item above for the exact edit). Item 2 fired **STOP** and is **not resolved** — the reference cache and the digest's N3 related-work grounding remain built from disjoint corpora, and re-harvesting is out of scope for a Phase A text-fix pass (and no experiment compute exists in this environment to run Phase B/C regardless). Per goal.md §2/§3, **one failing item is sufficient to block Phase B**; this run stops here by design — both because item 2 is unresolved and because Phase B/C require real compute this environment doesn't have. See `pipeline.md` for the phase-log entry.
