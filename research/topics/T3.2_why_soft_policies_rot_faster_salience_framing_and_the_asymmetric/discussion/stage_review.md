# Pengsida Stage Review — T3.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how, and to what degree, a phenomenon [the soft/hard decay-rate gap] arises from candidate mechanisms," with no new pipeline proposed as a fix — the testbed (matched-pair construction, orthogonal manipulation harness, prior-proxy battery, reactivity calibration) is the *analytical apparatus* that makes the mechanism observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification, `paper.md` Step 2's own archetype call ("Primary: empirical (mechanism-attribution study)... Secondary: technical_artifact/dataset"), and Stage 1's `study_type: empirical` from `pipeline.md`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "any attempt to fix the gap is guesswork — and the guess can be wrong in an expensive direction" is a first-principles framing of concrete, decision-relevant stakes (a placement/wording fix vs. an unsolved training problem), not a generic AI-importance appeal. The specificity requirement is also met: "an agent that has drifted out of its declared role can operate undetected for many turns before anyone notices" names *where* and *why* the failure is invisible, not just that it's bad. The Einstein ratio holds in the confirmed Stage 1/2 outputs — the problem and its stakes are argued at length before any manipulation/decomposition machinery is described.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g., "TimeToInconsistency... never intervenes on wording, position, or repetition, so its hazard model cannot separate salience from framing from prior"), which clears the "citation dump" failure mode. But the first assembled draft never states, in one place, which single prior work is the *closest* competitor — a reader sees four parallel threads (soft-policy/preference measurement; multi-turn safety and degradation; mechanistic accounts of context loss; alignment-prior/wording diagnostics) and has to infer for themselves which is the nearest neighbor. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section naming PrefEval and TimeToInconsistency as the two closest prior works and stating the precise delta — PrefEval already measures soft-constraint decay under long-context distraction and TimeToInconsistency already models multi-turn behavioral drift as a survival process, but neither compares soft against hard constraint decay within one matched, causally-interventional design — rather than leaving the reader to rank the four threads unaided.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — "matched" is given an explicit two-part operational definition (covariate matching at authoring time, turn-1 adherence-parity audit at pilot time) in Problem Definition/Methodology before any claim invokes it, and the same is true of the dominance/partial-R² decomposition and the equivalence-test criterion for reactivity. The inferential chain is licensed at its one load-bearing hinge: "a benign, presentation-driven closure of the gap would show up as the boosted-soft cell reaching hard-norm-level durability; if a nonzero residual survives even maximal boosting, that residual cannot trace to anything presentation controls" — the draft states this explicitly rather than asserting the residual's prior-linkage by fiat. No orphan components — all four modules (matched-pair bank, orthogonal manipulation harness with its boosted-cell contrast, prior-proxy battery, reactivity calibration) trace to a named sub-problem, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served at the level of individual RQs: RQ6 (reactivity equivalence) is a genuine falsification design (an equivalence test that can actively fail, not a correlation), and RQ4 (boosted-cell contrast) is symmetric-falsifiable in both directions (presentation could be inert, or could fully close the gap). But the *first assembled draft's* Experimental Setup subsection listed RQ1 through RQ6 as a flat numbered list with no signal that RQ6's result gates the validity of RQ2–RQ4 — that dependency appeared only inside RQ6's own subsection, easy to miss on a first read. Per the Analysis/Finding bar and the confirmed `pipeline.md` Stage 6 critique: a reader (or a future experimenter) could run and report RQ2–RQ4 as trustworthy findings before ever checking RQ6, exactly the failure mode `paper.md`'s own Step 6 pre-empts by marking its analogous RQ "RUN FIRST — gates E1/E2."

**THE ONE FIX (applied):** Promote the execution-order dependency out of RQ6's subsection and into the Experimental Setup paragraph itself, stated before the RQ list: reactivity calibration (RQ6) must be evaluated first, on the calibration subsample, before RQ2 (factor significance), RQ3 (manipulated share), or RQ4 (boosted-cell closure) are treated as trustworthy — and restated as a one-line reminder inside RQ6's own subsection so the gating relationship is visible at both the section-level and the RQ-level.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Long-running LLM agents are governed by two qualitatively different kinds of in-context rule..." / "A recent report puts a number on the asymmetry between these two tiers..." / "The nearest existing work approaches this gap from adjacent but distinct angles..." / "Turning the core question into a measurable design surfaces its own difficulties..." / "Our approach turns each of these obstacles into a specific, checkable design choice..." / "We evaluate this design through a staged pilot-then-scale-up plan...") reconstructs the whole five-move arc (problem → the specific unexplained asymmetry → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title and abstract: "the behavioral half-life of an in-context constraint is not a function of its occupancy of the context window, but of how its persistence is loaded across three physically distinct carriers." The Conclusion names a real forward-looking limitation (the alignment-prior mechanism remains the weakest-instrumented of the three candidates, proxied rather than manipulated) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming PrefEval and TimeToInconsistency as the closest prior work and stating the delta plainly (rather than leaving four parallel threads unranked).
2. **Stage 4 fix** — promoted the RQ6-gates-RQ2/3/4 execution-order dependency from a single mention buried inside RQ6's own subsection to an explicit statement in the Experimental Setup paragraph (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's canonical 8-item checklist (distinct from the `pengsida-stage-reviewer` 5-stage pass above, which reviewed the `auto-research-discussion` stages against `pengsida-stage-reviewer`'s own archetype-adaptive bar). This pass checks `README.md`/`digest.md`/`paper.md` against `guidance.md` directly, and follows a reference-cache upgrade (`discussion/reference_candidates.jsonl` rewritten from the flat 150-item harvest schema to `goal.md` §1's canonical schema; see that file's `key`/`verdict`/`why` fields for the full record). Date: 2026-07-04.

### 1. Digest self-verification — **PASS**
Re-executed the checks `digest.md` claims: all 13 nodes (N0–N12) plus the Claims section are present; every non-`[GIVEN]` node carries a 3-part `absence_comment` (`what_missing`/`why_matters`/`implication` — 13 of each, one per node, verified by direct count). Cross-node reference resolution checked programmatically (regex scan of `digest.md`+`paper.md` for every `M1–M6`, `C1–C4`, `CO1–CO4`, `A1–A8`, `t1–t6`, `RQ1`/`RQ_INF_1`/`RQ_INF_2`, `H1–H3` id): every id used is defined somewhere in the pair, no dangling references. Minor observation (non-blocking): `t3`, `t4`, and `CO2` are defined in `digest.md` but never re-cited by literal id in `paper.md` — their content is covered there under equivalent framing (A4/A6 for t3/t4; H1's attribution result for CO2), so this is a labeling thinness, not a broken reference.

### 2. Reference-cache integrity — **REVISE, fixed**
**Finding:** `digest.md`'s N3 related-work table cites 9 OpenReview works (`SafetyFewTokensDeep`, `TimeToInconsistency`, `SinkTrack`, `PrefEval`, `OffTopicEval`, `SafeDialBench`, `ICFBench`, `TARE`, `RECAST`) plus one canonical arXiv anchor (`LLMsGetLost`, 2505.06120) — grounded via a *different* corpus (`topics/corpus/ideas.jsonl`, a proposal-mining corpus) than the 150-item `reference_candidates.jsonl` harvest (pulled from `arxiv_corpus`/`openview_corpus` PDF caches for this topic). Before this pass, **zero** of these 10 N3 keys existed in `reference_candidates.jsonl` — a direct violation of "every N3 key is a selected cache record."
**Fix applied:** added all 10 as explicit records to `reference_candidates.jsonl` (`verdict: selected`, relevance assigned per their digest.md role: `method-twin` for `PrefEval`/`TimeToInconsistency`/`ICFBench`, `adjacent` for the other six OpenReview works, `background` for `LLMsGetLost`), each `why` citing the specific concede-and-differentiate delta already reasoned in `digest.md` N3/N4. **Residual, disclosed gap:** these 10 records have `pdf_path`/`digest_path` = `null` and `verified.id_resolves = false` — no local PDF cache exists for them in this harvest pass (confirmed: neither `openview_corpus/paper_cache` nor `arxiv_corpus` contains these ids). Spot-check (3 of the 9 OpenReview ids: `6Mxhg9PtDE`, `88C7vSdn0t`, `hcJywRYc3n`) confirmed all three resolve to real papers with titles matching `digest.md`'s N3 table, cross-referenced against `topics/corpus/ideas.jsonl`'s own `paper_id`/`paper_title` fields (direct OpenReview web fetch was blocked by a bot-challenge wall in this environment — the corpus cross-reference is the available substitute verification). No `pending` verdicts remain anywhere in the cache (all 160 records are `selected` or `rejected`). **Follow-up flagged, not blocking:** a future harvest pass should fetch real PDFs for the 3 method-twins so their `digest_path` resolves locally; until then, `digest.md`'s own N3 quotations (source=`GROUNDED:corpus`) remain the load-bearing grounding text.

### 3. Tag discipline — **PASS**
No untagged assertions found in `digest.md`; every non-obvious claim carries `[GIVEN]`/`[HYPOTHESIS]`/`[PLACEHOLDER]`/`[GROUNDED:corpus]`. `paper.md` (a pre-registration spec, not a digest) does not silently promote `digest.md`'s `[HYPOTHESIS]` content to asserted fact anywhere checked: the Step 0 asymmetry sentence hedges with "reported to differ ~8x"; Abstract v0 uses unfilled `[X]%`/`[Y]%` placeholders rather than invented numbers; all H1–H3 are framed as pre-registered binary tests, not conclusions.

### 4. Claim–Evidence Map completeness — **PASS**
All 7 claims in `paper.md`'s Claim–Evidence Map trace to an H-id (H1/H2/H3) or a `supported-by-design` definition (Claims 2, 6); every H-id has a fallback (E1/E2/E3 each state pre-committed verbatim wording) or routes to the global pivot F-G1. No orphans in either direction (no claim without a traced status; no H-id without a claim it feeds).

### 5. Hypothesis/assumption machinery — **REVISE, fixed**
**Finding (assumptions):** the Assumptions table (A1–A8) had a `Detection` column that merged three distinct guidance.md §3.2 slots (detection method, gate, consequence) into unstructured prose, making "every A\* fills §3.2 incl. detection and gate" auditable only by re-parsing free text, not by inspection.
**Fix applied:** split the table into five explicit columns (`Assumption`/`Failure mode`/`Detection`/`Gate`/`Consequence`), naming a `PG-1`…`PG-8` gate id for every assumption (all currently pilot/walking-skeleton-checked, i.e. `PG-*` per §3.2's "if checked in the pilot" case) and stating each assumption's specific downstream consequence.
**Finding (hypotheses):** H1/H2/H3 in Step 6 already filled all seven §3.1 template slots in substance (binary statement, `applies_if`, metric, test, alpha, effect floor, aggregation rule, verbatim fallback) but in prose rather than the labeled template — verified slot-by-slot against §3.1 for all three; no missing slot found. No fix needed here.

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 evidence standard) — **REVISE, fixed**
- **Item 1 (R1 estimand)** — missing: no single sentence stated quantity + unit of analysis + reference population + decision fed, all four in one place. **Fixed:** added an explicit "Estimand (R1)" sentence opening Step 5.
- **Item 6 (instrument R2 plan)** — missing: A7's κ≥0.8 threshold existed, but the full 5-step R2 sequence (ground externally → draft-wide-then-refine on a held-out set with named merge/split ops → validate against ≥2 raters → inspect confusion structure → freeze before scale) was only partially present (steps ③ only). **Fixed:** added a complete 5-step R2 subsection for the M3 verifier directly under the Assumptions table, citing the newly-selected cache entry `AdversarialPragmaticsAI2607` (arXiv:2607.01153) as the external grounding for step ①.
- **Item 9 (per-cell power + thin-cell rule)** — missing: a pooled power target (≥80% at α=0.05) existed, but no pre-declared rule for what happens to an individual under-powered cell (relevant because Stage 2's fractional-factorial design will produce thinner cells than Stage 1's full factorial). **Fixed:** added an explicit pre-declared thin-cell rule (INCONCLUSIVE, never null, never silently dropped; narrow-claim/collect-more/stop ladder) at the top of Step 6, citing guidance.md Part 4 situation 5.
- **Items 2–5, 7, 8, 10** — checked, no fix needed: verb/taste check already enforced at Step 3; B0/B-alt/F-G1 all present with pre-committed wording; ≥1 mechanism-layer analysis budgeted (H1's dominance/partial-R² decomposition serves as R6); design constraints substantively name their confounds (e.g. M2's length-matched filler removing the token-budget confound, stated explicitly in the B-alt paragraph), though not every constraint uses the literal "X removes confound Y" template — a stylistic, non-blocking observation.
- **Part 2 evidence standard for the declared archetype** — met: Primary archetype `empirical` (mechanism-attribution) satisfies A2's bar (validated instrument via R2 above; controlled comparison via B0/B-alt; pre-registered effect-floor tests H1–H3; rival-explanation ablation via B-alt; mechanism layer via H1's decomposition). **Advisory, non-blocking note:** E2's boosted-soft cell is *also* a genuine A4-style counterfactual intervention (manipulate the proposed cause, observe the predicted change) — the design is unusually strong in meeting two archetypes' bars at once; `paper.md` Step 2 could optionally name this explicitly, but nothing is missing evidence-wise.

### 7. Stage cross-check (advisory) — **PASS**
Already performed and on file: the `pengsida-stage-reviewer` 5-stage pass above (this same file, Stages 1–5) covers N1↔Stage1/2, N3/N4↔Stage3(Related Work), N6/N8/E*↔Stage4(Experiments), archetype from `paper.md`↔the classification header. Two REVISE items from that pass were already fixed (nearest-neighbor sentence; RQ6-gates-RQ2-4 promotion). No new STOP or REVISE surfaced by re-checking it against this Phase A pass's fixes (none of today's edits touch Related Work ranking or RQ execution order).

### 8. Taste audit currency — **PASS**
`taste_audit.md` (dated same run as `paper_draft.*`) reviewed the Step 0 asymmetry statement and Step 3 method-verb framing that are still current — none of today's Phase A fixes (estimand sentence, assumption-table restructuring, R2 instrument-validation detail, thin-cell rule) touch the asymmetry statement or the method's load-bearing verbs. Re-audit not required.

### Phase A gate result: **PASS** (after fixes)

All three REVISE findings (items 2, 5, 6) were fixed directly in `paper.md`/`reference_candidates.jsonl` during this pass, not merely logged. No STOP condition fired. Per `goal.md` §2's table, Phase B (walking skeleton) may proceed whenever real execution compute becomes available; this environment has none, so no Phase B/C work was attempted — the run stops at the Phase A gate as instructed.
