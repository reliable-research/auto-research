# Pengsida Stage Review — T3.4

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether, and when, a phenomenon occurs" with no new pipeline proposed as a fix to be pitted against baselines to win — the sweep harness, overhead instrumentation, selector family, and dual-mode detector are the *analytical apparatus* that makes the phenomenon (and the trade-off it produces) observable, not a method being benchmarked for SOTA. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. N12's own rationale is explicit on the one place this could tip toward a method paper — the selective-pinning policy (CO2) — and rules it out: "The selective-pinning policy (CO2) is a compared *condition* inside the measurement design rather than a proposed system with its own engineering evaluation." Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "the token cost of verbatim repetition grows linearly with rule count, while nothing guarantees the compliance benefit grows with it too" is a first-principles framing (an asymmetry internal to one mechanism, not a patch), and the stakes are concrete: practitioners "who currently pin by default" are relying on an unmeasured assumption. The Einstein ratio holds: the Introduction's opening move is pure problem/stakes, with zero method leak (the sweep harness, detector, and selector family are not named until the pivot paragraph).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "Sculptor... treats the standing instruction/policy block as fixed" and "never reports constraint-violation rate as an outcome at all"), which clears the "citation dump" failure mode. But the section never states, in one place, which single prior work (or pair of works) is the *closest* competitor. Digest N4's own limitation list already does this ranking implicitly — RECAST is closest in domain (multi-constraint LLM behavior degrading at scale) and CogniLoad is closest in method (a controlled, deconfounded load sweep) — but that ranking never made it into the first assembled Related Work prose. A reviewer reading only the first draft of `paper_draft.md` sees four parallel threads and has to infer for themselves which is the nearest neighbor; per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming RECAST (nearest in domain — multi-constraint degradation at scale) and CogniLoad (nearest in method — a controlled, deconfounded load sweep) as the closest prior work, stating the precise delta (neither measures representation cost, and CogniLoad's sweep has never been applied to normative content), rather than leaving the reader to rank the four threads themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the token-overhead ratio, the breakpoint test, applicability labels, and the dual-mode detector are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: a detected breakpoint in task success *and* a rising violation rate under full pinning together are what distinguish "presence without compliance" from ordinary noise, and the draft states this explicitly rather than asserting it by fiat. No orphan components — four of the five modules trace to a named sub-problem with a falsifiable hypothesis; the fifth (`m_tradeoff_tracker`) is disclosed as deliberately descriptive, not silently missing a hypothesis — this was checked directly against `pipeline.md`'s Stage 5 critique, which confirms the omission is intentional (digest N6's own `unaddressed_challenges: ['C4']`) rather than an unexamined gap. A hypothesis-free component that is *disclosed* as such is not an orphan component; one that is silently absent would be.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether each hypothesis-bearing claim is falsification-tested, not merely correlational, and whether the one non-hypothesis-bearing component is honestly framed as description rather than a hidden claim. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (RQ3's count-vs-length-density design is a genuine falsification test: a length-matched inert-padding arm that would have to reproduce the *same* decline if the effect were really just "more text," not "more constraints"). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... at least 10 percentage points below success at n=10..." without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline (the "Fallback" clauses in E1–E4) that didn't survive into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all four RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition already present in `paper.md`'s pre-committed Fallback text.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Production LLM agents are now asked to honor hundreds of standing rules at once" / "Yet nothing establishes whether the default fix for this — pinning — keeps working as the rule count grows" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this into a measurable question surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice" / "We evaluate this design across a constraint-count sweep") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in both title and abstract: "the token cost of guaranteeing a rule is seen scales linearly with rule count, while the attention budget that pays for compliance to each rule does not." The Conclusion names a real forward-looking limitation (the multi-objective frontier is characterized, not resolved into a single recommended operating point) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming RECAST and CogniLoad as the two closest prior works (nearest in domain and nearest in method, respectively) and stating the delta plainly, rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the four RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`).

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run against goal.md §3's 8-item checklist, applying guidance.md as the standard, over `README.md`/`digest.md`/`paper.md` (not `paper_draft.*` — those are the output of a prior `auto-research-discussion` pipeline run reviewed above under Stages 1–5; this section is the canonical goal.md Phase A gate, run here for the first time). Preceded by a reference-cache rebuild (Task 1): `discussion/reference_candidates.jsonl` was rewritten from the 150 flat-schema harvested candidates into goal.md §1's canonical schema, every candidate given a `selected`/`rejected` verdict with a specific `why`, and 8 entries added for the works `digest.md` N3/N4 already cite (see finding under item 2). Backup of the pre-canonical file kept at `discussion/reference_candidates.jsonl.pre_canonical.bak`.

### 1. Digest self-verification — **PASS**

`digest.md`'s own "Self-verification pass" section (V-01…V-12, EX-09/11/12) was re-executed by hand: N0–N12 + Claims all present; every `N4.affects_works` id resolves verbatim to an `N3` `citation_key` (8/8); every `N6.challenge_arguments[].challenge_id` ∈ {C1–C5} (5/5) and every `mechanism_components` ∈ {M1–M5}; every `N8` RQ has exactly one `N9` result entry (4/4) with `evidence_strength: missing` and an explicit falsification condition (no confidence inflation, V-08). No cross-reference breaks.

### 2. Reference-cache integrity — **REVISE (fired, fixed)**

**Finding:** Before Task 1, `digest.md` N3/N4 cited 8 works (`RECAST`, `PrefEval`, `ICF-Bench`, `Sculptor`, `AgentFold`, `COMI`, `CogniLoad`, `LostInTheMiddle`) grounded against a *different* corpus (`topics/corpus/ideas.jsonl`, the reverse-digest proposal corpus) than the one `reference_candidates.jsonl` was harvested from (`arxiv_miner_cache` + `openview_corpus/paper_cache`, the 150-candidate pool). None of the 8 were present in the cache at all — a hard fail of "every N3 key is a selected cache record." Cross-checked sibling topics `T3.1`–`T3.3`'s own `reference_candidates.jsonl`: none contain these 8 ids either, so this isn't a copy-paste omission local to T3.4.

**Fix applied:** Added all 8 works to `reference_candidates.jsonl` as `verdict: selected` records, sourced from `topics/corpus/ideas.jsonl` (title/id/url resolvable; no local PDF/digest file exists in the standard cache directories for these, so `pdf_path`/`digest_path` are `null` and `verified.id_resolves: false` — honest bookkeeping per the stated rule, not a fabricated resolution). Relevance tags follow the roles already worked out in `pipeline.md` Stage 3 (RECAST/PrefEval/ICF-Bench/Sculptor/AgentFold → `method-twin`; COMI → `baseline`, since its marginal-gain selector is literally run as the `comi` arm of M3; CogniLoad/LostInTheMiddle → `background`, since neither is ever run as a comparator). Every N3 key now resolves to a `selected` cache record; no `pending` entries exist anywhere in the file (158/158 records carry a final `selected`/`rejected` verdict).

**Spot-check (3 ids fetched):** `2512.22087.pdf` (7pp), `2512.22733.pdf` (5pp), `2601.00086.pdf` (8pp) — all resolve to real PDF files via `file(1)`, not placeholders.

**Follow-on finding (logged, not fixed here — see "Deferred" below):** Task 1's harvest surfaced 17 *new* selected candidates from the 150-pool that `digest.md`/`paper.md` don't yet discuss, several of which are genuine method-twins by the same test Stage 3 already applied to the original 8 (same estimand: LLM/agent context management under a token/turn budget) — notably `2512.22087` ("Context as a Tool," CAT paradigm — learnable context-management tool for long-horizon SWE agents), `2512.23457` ("Replay Failures as Successes" / HiR — RL for multi-constraint instruction following with an explicit hard/soft constraint set `C={c1..cn}`), and `2607.02255` ("AgenticSTS" — a bounded-memory testbed that ablates which typed experience slots enter a finite per-decision window against task win-rate). None of these were discoverable when `digest.md`/`paper.md` were originally written (they were built from the `ideas.jsonl` corpus only, which doesn't include them).

### 3. Tag discipline — **PASS**

`digest.md` carries no untagged assertion — every field-level entry checked is `[GIVEN]`, `[HYPOTHESIS]`, `[GROUNDED:corpus]`, or `[PLACEHOLDER]`; N9 results are explicitly `evidence_strength: missing` / `rq_answered: false`, i.e. no silent `[HYPOTHESIS]`→`[GIVEN]` promotion anywhere (results are stated as predicted directions with falsification conditions, never as findings). `paper.md`'s Abstract v0 is explicitly marked "(Draft; results slots empty by design.)"

### 4. Claim–Evidence Map completeness — **PASS**

All 7 rows of `paper.md`'s Claim–Evidence Map trace to an H-id (H1/H1b, H2/H2b, H3, H4) or to a `supported-by-design` definitional claim (Claim 4's "unknown until run," Claim 5's positioning claim); every H-id has either a pre-committed fallback (`needs-experiment; fallback-covered`) or is folded into the global pivot F-G1. No orphans in either direction.

### 5. Hypothesis/assumption machinery — **REVISE (fired, fixed)**

**Finding:** H1/H1b/H2/H2b/H3/H4 each fill guidance.md §3.1's seven slots, but in inline prose under each `E*` subsection rather than as literally-labeled fields — acceptable in substance (binary criteria, effect floors, named tests, alpha, aggregation votes, and verbatim fallbacks are all present and specific) so no content fix was needed there. The **assumption ledger (A1–A6)** was genuinely incomplete against §3.2's template: each had `failure_mode` and `detection`, but none had an explicit **`gate:`** (which `PG-*` walking-skeleton criterion, or which later phase, checks it) or **`consequence:`** (what happens to which H\* if it fails) slot.

**Fix applied (in `paper.md`, "## Assumptions"):** added `*Gate:*` and `*Consequence if false:*` clauses to all six assumptions, mapping each to a concrete walking-skeleton pass criterion where one exists (A3→PG-4, A5→PG-1, A6→PG-2; Step 9's pass criteria (i)/(ii)/(iv)) or to the specific later phase that checks it where the skeleton deliberately defers it (A1→E4's κ-gate; A2→a pre-Stage-0 pool-construction gate, labeled PG-0; A4→Stage-1 analysis, explicitly flagged as not skeleton-checked). Every consequence names which H\* degrade/narrow/block, rather than leaving "what happens if this is false" implicit.

### 6. Method-rigor audit — **REVISE (fired, fixed) — guidance.md Part 6 self-check + Part 2 A2 evidence standard**

Ran all 10 Part-6 items against the archetype (empirical/measurement, A2 in Part 2):

1. Estimand in one sentence (R1) — **REVISE, fixed.** No single estimand sentence existed (Step 5 had notation + core quantities but never R1's "quantity, unit of analysis, reference population, decision it feeds" in one place). **Fix:** added an explicit "Estimand (guidance.md R1)" sentence at the top of Step 5.
2. Verb check / no undefended integrate-unify (Prime directive) — **PASS** (Step 3's table already checks this; verbs are measure/sweep/deconfound/locate/isolate/gate/calibrate).
3. H\* seven slots incl. verbatim fallback — **PASS**, content present (see item 5 above; format is prose, not literal field labels — judged acceptable since every slot's content is unambiguously findable).
4. A\* detection + gate — **REVISE, fixed** (see item 5 above).
5. B0 + B-alt + F-G\* present — **PASS** (`paper.md` "Mandatory baselines" + "Global fallback F-G1", all with pre-committed wording).
6. Every instrument has the 5-step R2 plan with an acceptance threshold — **REVISE, fixed.** The M4 dual-mode detector had step ③ (validate against ≥2 human raters, κ≥0.8) and an implicit step ⑤ (freeze after one iteration), but never stated step ① (grounding categories in the constraints' own external verification specs) or step ② (draft-wide-then-refine on a *held-out* calibration set with named merge/split/remove operations), and step ④ (inspect confusion structure for adjacent-vs-systematic collapse) was implied by "per-class confusion rates" as a metric but never stated as an acceptance check. **Fix:** added an explicit 5-step "Instrument validation plan" under E4 in `paper.md`, and extended the E4 fallback to trigger per-class (not just globally) on a systematic confusion-structure failure.
7. Every design constraint names its confound (R3) — **REVISE, fixed.** "Deconfound"/"confound" appeared as a claimed property in several places but no single place named, per design constraint, which specific confound it removes. **Fix:** added a "Confound accounting (R3)" table in `paper.md` (6 rows: padding arm, density-held-fixed factorial design, random-k floor, programmatic-subset replication, cache-adjusted cost, task-random-effect clustering — each with its removed confound named).
8. ≥1 mechanism analysis budgeted (R6) — **PASS.** E3/RQ_INF_2 (count vs. length vs. density decomposition) *is* the mechanism-layer analysis for this archetype — it explains *why* degradation occurs (load vs. length vs. density) rather than only *that* it occurs, which is what R6 requires; no separate addition needed.
9. Power stated per cell; thin cells pre-declared INCONCLUSIVE — **REVISE, fixed.** Power was stated for the design as a whole (450 episodes/cell, 0.8 power at a 10pp floor) but there was no pre-declared rule for what happens to a cell or hypothesis that ends up under-powered (Part 4 situation 5 requires this pre-declared, not decided post hoc). **Fix:** added a "Power / thin-cell rule" paragraph in `paper.md` Step 6 stating the 388-episode/arm floor, that under-powered cells are reported as INCONCLUSIVE (never null, never dropped), and that a primary hypothesis whose required cells fall short is itself declared INCONCLUSIVE with the claim narrowed to the powered subset.
10. Archetype named + Part 2 evidence standard met by the plan — **PASS.** Archetype = `empirical` (A2), named consistently in `digest.md` N12 and `paper.md` Step 2/Step 3; A2's evidence standard (validated instrument R2 + controlled comparison R3 + pre-registered effect-floor tests R4 + rival-explanation ablations R5 + ≥1 mechanism analysis R6) is met by the plan as revised above (R4's "plain-language magnitude gloss per headline number" is a Phase-E/post-results requirement and cannot be evaluated before real numbers exist — not a gap at this stage).

### 7. Stage cross-check (advisory) — **REVISE items logged as pre-B fixes (see above); no STOP**

`pengsida-stage-reviewer`'s Stage 1–5 review (above, pre-existing) already checked N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E\*↔Stage 4 and fired two REVISEs, both fixed in `paper_draft.*`. This Phase A pass adds one more advisory finding not caught by that review: the freshness-sweep gap under item 2 (new method-twins from Task 1's harvest not yet reflected in `digest.md` N3/`paper.md`'s framing). Logged as a required pre-Phase-E action per guidance.md Part 4 situation 6, not fixed here — situation 6 explicitly calls for a considered `paper.md` repositioning (concede-and-differentiate treatment) rather than a quick prose patch risking a half-updated, internally-inconsistent related-work apparatus. **Deferred, tracked in `pipeline.md`.**

### 8. Taste audit currency — **PASS**

`taste_audit.md` was run against Stage 2 (Motivation) / Stage 5 (Method summary) of `pipeline.md`, both of which are unchanged by this pass's fixes (all fixes here are in the Assumptions/Experiments machinery of `paper.md`, not the asymmetry statement or the formal problem definition's substance — the Estimand sentence added under item 6.1 restates Step 5's existing notation, it doesn't change it). No re-audit required.

---

### Phase A gate result: **PASS after REVISE-fixes applied in this pass**

Items 2, 5, 6 (sub-items 1/4/6/7/9) fired REVISE and were fixed directly in `paper.md` (and the cache, for item 2) as documented above. No item fired STOP. Per goal.md §3 ("Run all; one failure blocks Phase B... REVISE items logged as pre-B fixes"), with all REVISEs now applied, **Phase A is clear for Phase B** — though per this run's explicit instructions, Phase B/C are out of scope here (no experiment compute available in this environment) and are not attempted.

### Deferred (not a Phase A blocker, but tracked for pre-Phase-E)

- **Freshness-sweep repositioning** (guidance.md Part 4 situation 6): `digest.md` N3/N4 and `paper.md`'s framing should be extended to concede-and-differentiate against the 3 strongest new method-twins Task 1 surfaced (`2512.22087` Context-as-a-Tool, `2512.23457` Replay-Failures/HiR, `2607.02255` AgenticSTS) before Phase E prose is written. Not performed in this pass — flagged explicitly rather than silently skipped, per goal.md's freshness-sweep requirement and the hard gate "new method-twin → repositioning + Phase A re-check."
