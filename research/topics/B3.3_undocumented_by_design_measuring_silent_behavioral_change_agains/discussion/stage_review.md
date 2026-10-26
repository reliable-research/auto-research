# Pengsida Stage Review — B3.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask what fraction of a phenomenon occurs, and where it concentrates" with no new pipeline proposed as an end in itself — the testbed (calibrated diff detector, entailment aligner, category-anchored taxonomy, boundary fingerprinting, coverage-stability check) is the *analytical apparatus* that makes the phenomenon observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification, `paper.md` Step 2's explicit "New Measurement / Instrument-and-Finding (empirical)" framing, and `study_type: empirical` confirmed at Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "the party that controls when a deployed AI system changes is also the sole author of the record of what changed" is a first-principles framing (the root structural conflict of interest, not a patch), and the stakes are concrete: an accountability process built on "the changelog is the complete record" silently inherits an unverifiable gap. The Einstein ratio holds: the first two paragraphs of the Introduction are pure problem/stakes — no mention of probes, detectors, or entailment scoring — with zero method leak. The motivation also clears `partial_output_coverage`: it explicitly argues why the *category-level taxonomy* matters beyond the headline rate ("an aggregate rate alone tells an integrator... *that* silence is common but not *where to look*"), which is the refiner-fixed version confirmed in `pipeline.md` Stage 2.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g., the rank-uniformity/logprob-tracking paragraph ends "a bare change signal is not a documented-or-silent label"), which clears the "citation dump" failure mode. But the first assembled draft of the Related Work section opened directly with the "Black-box API change and model-equality detection" thread and never stated, in one place, which single prior work is the *closest* competitor. Digest N3/N4 and `paper.md`'s own related-work framing already identify Chen, Zaharia & Zou (2023) as "the canonical direct precedent" and "the closest published analog" — but that ranking never surfaced as an explicit sentence in the assembled prose. A reader seeing only the four thematic paragraphs would have to infer for themselves which of the nine works is the nearest neighbor; per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence, before the thematic paragraphs, naming Chen, Zaharia & Zou (2023) as the closest prior work and stating the precise delta ("it never cross-references the vendor's own release notes... precisely the alignment step this paper is built to supply"), rather than leaving the reader to rank the four threads themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — $D(p)$, $\mathrm{Doc}(p)$, $\mathrm{Silent}(p)$, and $\rho_c$ are all given in Problem Definition ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its load-bearing hinges: the A/A control is what rules out "the detector manufactures its own findings" as the alternative explanation for a nonzero silent-change count, and the category-anchoring move is what rules out "the taxonomy was reverse-engineered from the observed pattern" as the alternative explanation for a concentration finding — both hinges are stated explicitly in the Methodology's Insight paragraphs, not asserted by fiat. No orphan components — every one of the five modules (calibrated diff detector, entailment aligner, category-anchored taxonomy, boundary fingerprinting, coverage-stability check) traces to a named sub-problem in `pipeline.md`, with no leftover machinery introduced in the paper draft that wasn't in the confirmed Stage 4/5 outputs.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (RQ1 is a genuine falsification design against the "the detector is trigger-happy" alternative via the A/A control; RQ3 is a genuine falsification design against the "alignment is just a lookup" alternative via the string-match floor). But the first assembled draft's RQ subsections, following `paper_assembly.md`'s base template, stopped at "**Expected outcome.** ... exceeds 0.50, with the bootstrap 95% CI lower bound also exceeding 0.50" without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as an explicit check, not left implicit in the setup description. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline (its own per-RQ "Fallback" clauses, e.g., Fallback F1/F2/F3 and the mandatory-baseline "why do this at all" control) that didn't automatically carry over into the base-template assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s Step 6 Fallback clauses and Step 9 walking-skeleton pass/fail criterion).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Large language model APIs change on a schedule the vendor alone controls..." / "Yet a basic question about that arrangement remains unanswered..." / "The nearest existing work approaches adjacent pieces of this question without closing it." / "Turning this gap into a measurable claim surfaces four distinct difficulties." / "Our approach turns each of these difficulties into a specific, checkable design choice rather than an assumption." / "We evaluate this design across real version transitions...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and Introduction: "the party that controls when a deployed AI system changes is also the sole author of the record of what changed... so the completeness of that record is unverifiable from inside it." The Conclusion names a real forward-looking limitation (the rate can never be certified as the true rate, only stability-checked as a lower bound; findings may not generalize across vendors with different documentation cultures) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the opening of the Related Work section, naming Chen, Zaharia & Zou (2023) as the closest prior work and stating the delta plainly (rather than leaving four thematic paragraphs unranked).
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's 8-item checklist, applying `guidance.md` as the standard, against `README.md` / `digest.md` / `paper.md` (not against `paper_draft.*` — that artifact is addressed separately under "Process flag" below). This re-run is independent of the Stage 1–5 pengsida review above (which used the `auto-research-discussion` 6-stage vocabulary); it is the `goal.md`-schema gate. Preceded by **Task 1** (this session): `discussion/reference_candidates.jsonl` was rewritten into the canonical `goal.md` §1 schema, all 150 harvested candidates read and given a `selected`/`rejected` verdict, and 9 records backfilled (see item 2).

### 1. Digest self-verification — **PASS**

Re-executed `digest.md`'s own self-verification pass (V-01 through V-12, Empty-node check). Confirmed independently: all of N0–N12 plus Claims are present; `affects_works` (N4) ⊆ N3 `citation_key`s; `challenge_arguments`/`unaddressed_challenges` (N6) ⊆ {C1–C4} and `mechanism_components` ⊆ {M1–M5}; N8 `addresses_challenges` ⊆ {C1–C4} and `tests_contributions` ⊆ {CO1–CO3} (RQ1→CO1, RQ2→CO3, RQ3→CO2 — all three contributions covered); N9 `rq_id`s = N8's RQ ids. Every non-GIVEN *node* that reports an absence (N0, N2, N10, N11) carries the required 3-part `absence_comment` (what_missing/why_matters/implication); nodes that instead report a hypothesis set (N1, N3–N9) use the header's own inline-tag convention ([HYPOTHESIS]/[GROUNDED:corpus]/[PLACEHOLDER]) rather than a per-item absence comment, which is the digest's declared convention for a reverse-digest, not a gap.

### 2. Reference-cache integrity — **REVISE → FIXED (this session)**

**Finding:** Before this session's Task 1, `discussion/reference_candidates.jsonl` held only the 150 harvested candidates (110 arXiv + 40 ACL-anthology, harvested by embedding-similarity search over `arxiv_corpus`/`openview_corpus`) — a *different* corpus from the one `digest.md`'s N3 actually grounds against (`topics/corpus/ideas.jsonl`). Consequence: **zero** of the 9 works cited in `digest.md` N3/N4 and used substantively in `paper.md` (M2's fingerprint borrow from LogProbTracking, M3's alternative-test borrow from FairBetting, the Related-Work nearest-neighbor Chen2023, etc.) existed in the cache at all — not `selected`, not even `rejected`. Per `goal.md` §3 item 2 ("every N3 key is a selected cache record") this is a hard fail, and per `guidance.md` Part 5 ("baseline selection is a cache query") every citation in the eventual paper would have been uncitable by the `goal.md` §8 hard gate ("citations only via selected cache keys; refs.bib... script-generated" from this file).

**Fix applied:** Backfilled all 9 N3-cited works into `reference_candidates.jsonl` as `selected` records, using the real metadata already resolvable from `topics/corpus/ideas.jsonl` (`paper_id`/`paper_title`/`paper_url`) plus arXiv for Chen et al. 2023 — `LogProbTracking` (method-twin — M2 borrows its logprob-fingerprint design), `RankUniformity` (baseline — named change-detection-only comparator), `BiasSimilarity` (adjacent), `TAIG` (background — governance-gap motivation), `SafeHarbor` (background — accountability-necessity motivation), `RobustAudit` (adjacent), `FairBetting` (method-twin — M3 borrows its sequential-test option), `LAMDA` (background — longitudinal-protocol exemplar), `Chen2023ChatGPTBehavior`/arXiv:2307.09009 (method-twin — canonical direct precedent). `reference_candidates.jsonl` now has 159 records (150 original + 9 backfilled), 12 `selected` / 147 `rejected`, zero `pending`.

**Spot-check (2 of the newly-added ids, live-fetched):** `arXiv:2307.09009` resolved via `WebFetch` — title/authors ("How is ChatGPT's behavior changing over time?", Chen/Zaharia/Zou) and abstract content match `digest.md`'s citation exactly. OpenReview forum-id fetches (`hFxivbAgVP`, `EEVpt3dJQj`) were blocked by an anti-bot verification page at the tool level (inconclusive, not a failure) for both attempts; corroborated instead via the local `topics/corpus/ideas.jsonl` record (real `paper_id`/`paper_title`/`paper_url` triple), the same grounding source `digest.md`'s own N3 methodology used.

**Residual gap (not blocking Phase A, flagged for pre-Phase-E):** the 9 backfilled records have `pdf_path`/`digest_path` = `null` (`verified.id_resolves = false`, honestly, per the task's own rule) — no local PDF cache exists for OpenReview-hosted or this specific arXiv id, so no per-paper extraction-mode digest has been run yet. Per `goal.md` §1's lifecycle step ② ("digest every potentially load-bearing candidate... with `paper-digest` in extraction mode"), `LogProbTracking`, `FairBetting`, `RankUniformity`, and `Chen2023ChatGPTBehavior` (the 4 load-bearing `baseline`/`method-twin` entries) should get a real extraction-mode digest before Phase E's Related-Work prose and `refs.bib` are script-generated from this file. This does not block Phase A/B (the entries are correctly `selected` with a specific `why` grounded in `digest.md` N3/N4 text) but must be closed before the freshness sweep gate (`goal.md` §1 "Staleness" / §8).

**Also fixed as part of Task 1:** the original 150-candidate harvest is confirmed **thin** relative to `guidance.md` Part 5's "cache thin (<~5 selected)" rule — of the 150, only 3 were genuinely selectable (`EPC2607` adjacent, `Foley2023Matching` adjacent, `RiskArchitecture2607` background); the other 147 are off-topic by domain (LLM reasoning/agents/hallucination/benchmarks with no engagement with vendor changelogs, version-transition attribution, or documented-vs-silent measurement). Per Part 5, this means **the harvest itself was inadequate, not the field empty** — recorded here rather than papered over; a fresh harvest from new angles (e.g. "model-equality testing", "API drift detection", "changelog NLP alignment", "LLM judge/evaluator staleness") is recommended before Phase E, in addition to the freshness sweep `goal.md` §1 already requires.

### 3. Tag discipline — **PASS**

No untagged assertion found in `digest.md`; every content bullet carries one of GIVEN/HYPOTHESIS/GROUNDED:corpus/PLACEHOLDER. No silent HYPOTHESIS→GIVEN promotion detected — `paper.md`'s Abstract v0 is explicitly marked "DRAFT BEFORE RESULTS" and its Step 6 RQ sections consistently use "Expected outcome" / "Hypothesis" framing, never asserting a result as achieved.

### 4. Claim–Evidence Map completeness — **REVISE → FIXED (this session)**

**Finding:** H1 and H2's Claim–Evidence Map rows were annotated `needs-experiment / fallback-covered` with an explicit `(F1 fallback)` / `(F2 fallback)` trace, but H3's row said only `needs-experiment` (no fallback annotation) even though Step 6's RQ3 subsection already had a fully-specified `Fallback F3` — an inconsistency that made H3 read as an orphan relative to `goal.md` §3 item 4 ("every H-id has a fallback... no orphans either way"), and a second row ("The instrument's own error is characterized") duplicated the same H3 trace without adding information.

**Fix applied (`paper.md`):** merged the two H3-tracing rows into one, re-annotated `needs-experiment / fallback-covered`, and explicitly cited `(F3 fallback: downgrade M4 to human-in-the-loop / recalibrate the effect-size floor, Step 6 RQ3)`, matching H1/H2's annotation style. Cites `guidance.md` §3.1 ("the fallback sentence is written now... every hypothesis fails and its fallback...") and `goal.md` §3 item 4.

### 5. Hypothesis/assumption machinery — **REVISE → FIXED (this session)**

**Finding A (H1 missing the `aggregation` slot):** `guidance.md` §3.1 requires every H\* to fill an `aggregation` slot ("pre-registered vote rule, e.g. '≥2 of 3 instruments'"). H1's Verification bullet said "Reported per-vendor, not pooled" but never stated how per-vendor results convert into one PASS/FAIL verdict for H1 once Stage 1 tests ≥3 vendors — a real binariness gap (`goal.md` §3 item 5 requires "all seven slots").

**Fix applied (`paper.md`, Step 6 RQ1):** added an explicit **Aggregation (cross-vendor vote rule)** bullet: H1 PASSes only if ≥2 of the ≥3 tested vendors individually clear $\rho>0.50$ with CI lower bound $>0.50$ (vendors below the 20-detected-diff power floor are excluded from the vote, not counted as "no"); a single-vendor pilot is explicitly flagged `INCONCLUSIVE-pending-scale-up` rather than scored. Fallback F1's trigger condition was reworded to match ("the cross-vendor vote fails").

**Finding B (Assumption `gate` slots named informally, not as explicit PG-ids):** `guidance.md` §3.2 requires each A\* to state `gate: PG-j if checked in the pilot; else the phase that checks it`. The Assumptions section referenced gates only in prose (e.g. "(RQ3 gate)") without the PG-id convention `goal.md` §4 relies on ("Instrument validation... runs inside B as PG-\* gates").

**Fix applied (`paper.md`, Assumptions section + Step 9):** added explicit `Gate: PG-1`…`PG-6` labels to A1–A6 respectively, and added an **Assumption-gate mapping (PG-\*)** bullet to Step 9's Walking Skeleton mapping each PG-id to the specific arm/check that verifies it (PG-1/PG-2/PG-4 inside the pilot; PG-3 at RQ3; PG-5 deferred to Stage-1 scale since probe-subset stability needs the full suite; PG-6 a framing check, not a pilot pass/fail).

**B0 + B-alt + F-G\*:** confirmed present and complete — B0 (Step 6 "Mandatory baselines," the assume-everything-documented/string-match arm plus the same-version-null arm) and B-alt (the A/A budget-matched rival-explanation arm with a pre-committed 3× margin) both fill `guidance.md` §3.3's slots; F-G1 (global pivot to instrument/methodology archetype) is present with a pre-written pivoted abstract sentence. **PASS** on this sub-item, no fix needed.

### 6. Method-rigor audit — **PASS**

`guidance.md` Part 6 self-check, items 1–10: (1) R1 estimand stated in Step-0/Step-5 notation; (2) verb check passed per `taste_audit.md` (no integrate/unify in claim position — verbs are run/align/attribute/isolate); (3) every H\* now has all seven slots after item-5's fix; (4) every A\* now has detection + an explicit PG-gate after item-5's fix; (5) B0+B-alt+F-G1 present (confirmed above); (6) M4's 5-step R2 instrument-validation plan is present (external category anchoring → dev-set threshold tuning → human-label F1 validation ≥0.70 → confusion/adjacent-category check implied by the human-adjudication protocol → freeze τ before scale); (7) every design constraint names its confound (A/A control → sampling-noise confound; category-anchoring → taxonomy-circularity confound; string-match B0 → "is entailment matching earning its complexity" confound); (8) ≥1 mechanism-adjacent analysis budgeted (category taxonomy via M5, split-sample stability check); (9) power stated per cell (≥20 detected diffs per category/vendor, else pooled/INCONCLUSIVE, now formalized further by item 5's vote-exclusion rule); (10) archetype named (A2, empirical/measurement per `guidance.md` Part 2) and its evidence standard (validated instrument R2 + controlled comparison + effect-size floors + rival-ablation + mechanism analysis) is met by the *plan* — confirmed, not merely asserted.

### 7. Stage cross-check (advisory) — **PASS** (already run; findings incorporated)

The existing Pengsida Stage Review (`stage_review.md` §Stages 1–5, above) already performed this exact check — Stage 1 (Problem+Motivation) ↔ N1/N2: PASS; Stage 2 (Related Work) ↔ N3/N4: REVISE→fixed (nearest-neighbor sentence added to `paper_draft.md`); Stage 3 ("Method") ↔ N6: PASS; Stage 4 ("Experiments") ↔ N8: REVISE→fixed (falsification-condition lines added to `paper_draft.md`/`.tex`); Stage 5 (Writing) PASS. No STOP fired. One terminology note, not a defect: that review's archetype label ("Analysis / Finding," the `pengsida-stage-reviewer` skill's own vocabulary) and `paper.md`/`digest.md`'s archetype label ("empirical measurement," `guidance.md` Part 2's A2) describe the *same* paper correctly from two different reference taxonomies — the evidence actually produced (validated instrument, effect-size floors, rival-explanation ablation) matches A2's standard, not A4's counterfactual-intervention standard, so no relabeling is needed.

### 8. Taste audit currency — **PASS**

`taste_audit.md`'s recorded audit (🟢, Stage 2/5-confirmed motivation+method) predates this session's fixes, but none of this session's edits touched the asymmetry statement (Step 0) or the formal problem definition (Step 5) — the fixes were confined to Step 6 (aggregation rule), the Assumptions section (PG-gate labels), and the Claim–Evidence Map (fallback annotation). No re-run required.

---

### Overall Phase A gate result: **PASS** (2 REVISE items found and fixed this session: items 2 and 4/5 combined; no STOP)

### Process flag (not a checklist item — recorded for the phase log)

`discussion/paper_draft.md`/`.tex`/`.pdf` already exist in this topic's `discussion/` folder, but **no `B_pilot/`, `results/`, `verdicts.json`, or `claim_map.md` exist** (confirmed by direct search). Inspection of `paper_draft.md` shows it consistently uses "Expected outcome" / "Falsification condition" language (e.g. "The overall silent-change rate ρ exceeds 0.50...") rather than asserting fabricated numbers as if measured — so it is **not** a fabricated-results violation of `goal.md`'s hard gates. It is, however, out of sequence: per `goal.md` §2's pipeline, Phase E prose must be spliced from `claim_map.md` (post-Phase-D verdict lookup), and Phase F/I (`.tex`/`.pdf`) must follow. Here, Phase E/F/I-shaped artifacts were produced directly from `paper.md`'s pre-registered plan, skipping Phase B (walking skeleton — no real compute run), Phase C (no `results/`), and Phase D (no verdict lookup) entirely. Per this session's explicit scope, Phase B/C require real experiment compute that does not exist in this environment, so this gap is **not fixed here** — it is recorded so `pipeline.md` does not mark B/C/D/E/F/I "passed," and so a future run with real compute knows to start at Phase B using `paper.md` as written (now with the item-5 aggregation/PG-gate fixes applied) rather than treating the existing `paper_draft.*` as licensed by any actual result.
