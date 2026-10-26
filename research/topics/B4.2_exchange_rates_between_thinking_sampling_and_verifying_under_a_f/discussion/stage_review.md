# Pengsida Stage Review — B4.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "what are the actual exchange rates and frontier shape for existing levers" with no new pipeline being pitted against baselines to win — the five components (cost meter, interaction-surface model, stratified replication, matched-cost binning, coverage/selection decomposition) are the *analytical apparatus* that makes the phenomenon measurable at all, not a method whose accuracy needs to beat a competitor's. This matches digest N12's own `empirical` classification, `paper.md` Step 2's independent "Primary: empirical (measurement study)... Secondary: technical_artifact, strictly in support," and Stage 1's `study_type: empirical` confirmed in `pipeline.md`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "no existing study prices all three levers, including the verifier's own cost, in one currency" is a first-principles framing (a genuine measurement absence, not a patch to an existing method), and the stakes are stated concretely: a deploying engineer currently cannot answer "given one more dollar, which lever buys the most accuracy right now" because every prior study either uses the wrong currency or treats the verifier as free. The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes — the asymmetry sentence ("a dollar spent on verification buys no accuracy by itself... a dollar spent on longer reasoning or on an additional sample can") appears before any mention of the meter, the grid, or any other method component.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "[the sample-then-verify theory cluster] treat[s] verifier feedback as an available resource with a formal performance bound, but none lets the verifier's own metered cost enter the budget constraint whose trade-off it is meant to characterize"), which clears the "citation dump" failure mode. But in the first assembled pass, the section never stated, in one place, which single prior work is the *closest* competitor before launching into the four thematic paragraphs. Digest N4's own limitation 5 already does this work explicitly — "the closest existing two-way allocation study splits budget between exploration and verification only in the deep web-search agent domain" (referring to the asymmetric-verification work) — but that ranking never made it into the assembled Related Work's opening. A reviewer reading only the first-pass `paper_draft.md` would see four parallel thematic paragraphs and have to infer for themselves which one is the nearest neighbor; per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence, naming the asymmetric-verification work for web-search agents as the single closest prior work and stating the precise delta (single domain, trajectory-priced not dollar-priced, no CoT-length axis), before the four thematic paragraphs — rather than leaving the reader to rank them unaided. The current `paper_draft.md` opens its Related Work section with exactly this sentence.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the matched-cost bin, the accuracy-per-dollar frontier, the interaction terms, and the allocation-mix vector are all given in Problem Definition/Method Overview ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge, stated explicitly rather than asserted by fiat: "coverage... and selection quality... are both functions of the same generated candidate pool, so an accuracy gain under a verify-heavy allocation cannot be attributed to the verifier without ruling out that the same dollars, spent on more candidates and no verifier, would have produced the same gain" — this is exactly what makes the coverage/selection decomposition non-redundant with simply reporting a verify-heavy allocation's raw accuracy. No orphan components — every one of the five modules (cost meter, interaction surface, stratified replication, matched-cost binning, coverage/selection decomposition) traces to a named sub-problem in `pipeline.md`, with no leftover machinery introduced only in the write-up.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ8 is a genuine falsification design (does verifier value survive a budget-matched coverage-only control, rather than merely reporting the verifier condition's raw accuracy), and every RQ subsection in the first assembled draft already carried both an "Expected outcome" and a "Falsification condition" line, since this run's assembly instructions required both from the start. What the first assembled draft's **Experimental Setup** subsection was missing is a specific commitment made load-bearing back in Stage 1: the refined Stage 1 `objective` states that "a (family, budget) cell in which no evaluated allocation beats the fixed floor-allocation by a pre-specified margin at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported separately as **allocation-moot**" — but the first assembled Experimental Setup listed the fixed floor allocation only as a generic baseline, without stating the exclusion rule that Stage 1 made a first-class part of the paper's evaluability condition. Per the Analysis/Finding bar's discharge test, a claim's validity boundary (here: which cells don't even license a claim) has to be stated as part of the experimental design, not left implicit in an earlier stage's fine print.

**THE ONE FIX (applied):** State the allocation-moot exclusion rule explicitly in the Experimental Setup's baselines paragraph, tied directly to the fixed floor allocation, rather than leaving it only in the Problem Definition's formal setup. The current `paper_draft.md`'s Experimental Setup does this: "a $(family, budget)$ cell in which nothing beats this floor by a pre-specified margin at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported as **allocation-moot** rather than folded silently into the frontier, per the Problem Definition's exclusion rule."

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Deploying a large language model to reason under a metered budget is no longer a theoretical exercise" / "Yet a specific asymmetry among these three levers goes unpriced by every existing analysis of the trade-off" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this asymmetry into a measurable question surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice rather than a hedge" / "We evaluate this design across task families spanning...") reconstructs the whole five-move arc (problem → unpriced asymmetry → prior work's shared limitation → why it's hard to measure → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and Introduction: "a dollar spent on verification buys no accuracy by itself... it only ever re-scores candidates that generation has already produced." The Conclusion names two real forward-looking limitations (price-sheet/model generalization; the coverage/selection decomposition bounding rather than eliminating a stronger-verifier explanation) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming the asymmetric-verification (web-search agent) work as the closest prior work and stating the delta plainly (single domain, trajectory-priced not dollar-priced, no CoT-length axis), rather than leaving four thematic paragraphs unranked.
2. **Stage 4 fix** — stated the Stage-1 `allocation-moot` exclusion rule explicitly in the Experimental Setup's baselines paragraph (both `paper_draft.md` and `paper_draft.tex`), tied to the fixed floor allocation, then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Date: 2026-07-04. Trigger: reference-cache upgrade (`reference_candidates.jsonl` rewritten from a 150-line ad hoc harvest schema into goal.md §1's canonical schema, all 150 candidates individually re-verdicted, plus 9 records added for works `digest.md` N3 already cites). Runs the goal.md §3 checklist against `README.md` + `digest.md` + `paper.md` + the rebuilt cache, applying `guidance.md` as the standard. This section supersedes nothing above (the Stage 1–5 pengsida cross-check on `paper_draft.md` stands); it is the first time the **full 8-item Phase A checklist** has been logged as such for this topic.

### 1. Digest self-verification — **PASS (one fix applied)**
Re-executed `digest.md`'s own self-verification claims: all cross-node ids resolve (`N4.affects_works` ⊂ `N3` keys verbatim; `N6.challenge_arguments` ids ⊂ `N5`; `N8` fields ⊂ {M1–M5, C1–C5, CO1–CO4}; `N9.rq_id` ⊂ `N8` ids — all confirmed by direct re-check, not just trusting the digest's own V-04 claim). All of N0–N12 + Claims present. **Gap found:** N12 (`Contribution Type`, tagged `[HYPOTHESIS]`) was the one node with no `**Status:**`/`absence_comment` line, breaking the convention every other non-`FOUND` node follows and violating goal.md §3 item 1's "every non-GIVEN item carries its 3-part absence comment." **Fixed:** added a `PARTIAL` status + 3-part absence comment to `digest.md` N12 (citing this checklist item).

### 2. Reference-cache integrity — **REVISE (fix applied; one residual item logged, not blocking)**
Before this run, **zero** of the 9 works `digest.md` N3 cites (`[SnellTTC]`, `[VerifierFreeSuboptimal]`, `[PlanAndBudget]`, `[CoTLength]`, `[AsymVerify]`, `[OTVerify]`, `[BestOfMajority]`, `[RerankingLaws]`, `[BrownMonkeys]`) existed anywhere in `reference_candidates.jsonl` — the 150-line harvest (110 arXiv-corpus + 40 ACL-anthology candidates) was built from a completely different corpus (`arxiv_miner_cache` + ACL Anthology) than the one `digest.md`'s N3 actually searched (`topics/corpus/ideas.jsonl`, the local OpenReview corpus), and the two were never reconciled. This is a direct violation of goal.md §3 item 2 ("every N3 key is a selected cache record") and would have blocked Phase A outright.
**Fixed:** added all 9 records to the cache as `selected` (8 sourced from `openview_corpus/ideas.jsonl` proposal text — the same corpus `digest.md` itself drew from — plus the canonical `BrownMonkeys` arXiv:2407.21787), with `relevance` set to `baseline` or `method-twin` matching how `paper.md`'s baseline list / Related Work already uses each one, and a `why` tracing to the specific digest/paper.md location that cites it.
**Residual (logged, not re-opened as a new gate):** none of these 9 have a locally cached PDF or a `paper-digest`-style `digest_path` in this environment (no PDF cache exists for these OpenReview ids, and no internet-fetch tool could retrieve them past OpenReview's bot-check — confirmed by two direct `WebFetch` attempts on `4FWAwZtd2n` and `hxL4Uf9tR3`, both blocked by a browser-verification page). `verified.id_resolves = false` is recorded honestly for all 9 (per the schema rule: true iff `pdf_path` non-null). A third spot-check, `arXiv:2407.21787` (BrownMonkeys), *did* resolve via `WebFetch` and its live title/abstract matched `digest.md`'s characterization exactly (coverage scaling log-linearly with N; majority-vote/reward-model selection plateauing without a verifier) — one of the 2–3 required spot-checks succeeded outright, two were environment-blocked, not data problems. This residual (fetch-and-digest the 9 records properly) is exactly what `digest.md`'s own N7 `absence_comment` already flagged ("re-verify vs. arXiv per N7 absence_comment before submission") and what goal.md §1 calls the freshness sweep — it is correctly a **pre-Phase-E** task, not a Phase A blocker, since Phase A only gates on the keys existing as `selected` records (now true), and no `pending` entries are cited anywhere in `digest.md` or `paper.md` (confirmed by grep — every citation key in both files resolves to a `selected` record).

### 3. Tag discipline — **PASS**
No untagged assertions found in `digest.md`; every claim in `paper.md` is either marked `[DRAFT — written before any experiment]` (Abstract v0), a pre-registered hypothesis (not asserted as fact), or a `supported-by-design` claim tied to a design decision rather than a result. No silent `[HYPOTHESIS]`→`[GIVEN]` promotion found anywhere.

### 4. Claim–Evidence Map completeness — **PASS**
All 8 claims in `paper.md`'s Claim–Evidence Map trace to an H-id (Claims 3–6) or a `supported-by-design` definition (Claims 1, 2, 7, 8); every H-id (H1a/H1b/H1c, H2a/H2b, H3a/H3b) has fallback coverage (F1, F2, F3) and F-G1 covers the joint-failure case; no orphans in either direction.

### 5. Hypothesis/assumption machinery — **REVISE (fixed)**
H\* content (metric, test, alpha, effect floor, aggregation rule, verbatim fallback) is present in prose for all seven hypotheses, though attributed at the experiment (E1/E2/E3) level rather than restated per-H-id — accepted as compliant in substance (guidance.md §3.1's slots are about content completeness, not literal per-line labels). **Gap found:** the A1–A7 assumption ledger had only 4 of guidance.md §3.2's 5 required slots — `assumption`, `failure_mode`, `detection`, `gate` were present, but **`consequence`** ("what happens to which H\* if it fails") was missing for all 7 assumptions, failing goal.md §3 item 5's "every A\* fills §3.2." **Fixed:** added a `consequence` column to the A1–A7 table in `paper.md`, naming which H-id(s) each assumption's failure degrades, restricts, or blocks, per guidance.md §3.2. B0 + B-alt + F-G1 were already present with pre-committed wording — no fix needed there.

### 6. Method-rigor audit — **REVISE (three fixes applied)**, evidence standard for `empirical` archetype otherwise met
Checked guidance.md Part 6 items 1–10 against `paper.md`:
- **Item 1 (estimand in one sentence, R1) — FAIL → fixed.** No explicit one-sentence estimand existed anywhere in `paper.md` (Step 5 opened directly with Notation). **Fixed:** added an explicit "Estimand" sentence (quantity + unit of analysis + reference population + decision it feeds) at the top of Step 5, citing guidance.md R1.
- **Item 2 (verb check) — PASS.** Step 3's self-audit already checks this explicitly and passes (verbs: meter, price, gate, isolate, measure, falsify).
- **Item 3 (H\* seven slots) — PASS** (see item 5 above; content complete, non-templated formatting accepted).
- **Item 4 (A\* detection + gate) — PASS** for detection/gate specifically; the broader §3.2 `consequence` gap is logged under checklist item 5 above and fixed there.
- **Item 5 (B0+B-alt+F-G\* present) — PASS.**
- **Item 6 (every instrument has the 5-step R2 plan) — PARTIAL → fixed.** The verifier (A6, AUC≥0.60 gate) and the openQA rubric judge (A3, κ≥0.7 gate) each only had an acceptance-threshold step (R2's step ③), missing the grounding/calibration/confusion-inspection/freeze steps (①②④⑤). **Fixed:** added the full 5-step R2 sequence for both instruments in `paper.md`'s Assumptions section, citing guidance.md R2.
- **Item 7 (every design constraint names its confound, R3) — PASS.** Confound-naming is present, distributed across the B-alt control (coverage confound), A2 (price-sheet-artifact confound), and the oracle arm (selection-quality confound) — not collected into one list, but each constraint's confound is named somewhere.
- **Item 8 (≥1 mechanism analysis, R6) — PASS.** E3/RQ_INF_2's interaction-coefficient + oracle-vs-realizable-gap analysis is the mechanism layer.
- **Item 9 (power per cell; thin cells pre-declared INCONCLUSIVE) — FAIL → fixed.** `paper.md` previously defined only binary PASS/FAIL criteria for every H-id, with no INCONCLUSIVE branch anywhere — a direct gap against goal.md §8's hard gate ("under-powered cells... pre-declared INCONCLUSIVE, never null") and guidance.md Part 4 situation 5. **Fixed:** added an explicit power/INCONCLUSIVE rule to Step 6's design-constants paragraph, citing guidance.md §3.4 R8 / Part 4 situation 5 / Part 6 item 9.
- **Item 10 (archetype named + Part 2 evidence standard met) — PASS**, contingent on items 1/6/9's fixes now being in place; the `empirical` (A2) archetype's mandatory experiment shape (measurement grid, placebo arm, rival-explanation arm, power statement) is present in `paper.md`.

### 7. Stage cross-check (advisory) — **PASS (already resolved)**
The `pengsida-stage-reviewer` Stage 1–5 cross-check above already ran and its two REVISE findings (Stage 2 nearest-neighbor sentence, Stage 4 allocation-moot exclusion rule) are already applied to `paper_draft.md`/`.tex`/`.pdf`. The reference-cache upgrade in this run surfaced one new method-twin (`ComputeAccuracy251224776`, arXiv:2512.24776) not seen by the original Stage 2/3 cross-check; per guidance.md Part 4 situation 6, this is logged as a **pre-Phase-E to-do** (add one concede-and-differentiate sentence to `paper_draft.md`'s Related Work) in `paper.md`'s new "Reference-cache update note" section — it does not reopen Stage 2's PASS-after-fix verdict above, since `paper_draft.md` itself is not being re-touched by this Phase A pass (out of scope per this run's instructions: fix `paper.md`/`digest.md` only, stop before Phase B/C).

### 8. Taste-audit currency — **PASS**
None of this run's four fixes (N12 status line, Estimand sentence, A\* consequence column + R2 5-step notes, INCONCLUSIVE rule) touch the asymmetry statement (Step 0) or the formal definition's substance (Step 5's notation/adjective table) — they add completeness/rigor scaffolding around unchanged content. `taste_audit.md`'s recorded 🟢 verdict (dated to the Stage 2/5 motivation+method pair, unchanged here) remains current; no re-audit triggered.

### Phase A gate result: **REVISE → all REVISE items fixed in this run → gate now PASSES.**

Five REVISE-level gaps were found and fixed directly in `paper.md`/`digest.md` in this pass (checklist items 1, 2, 5, 6×3): (i) `digest.md` N12 missing status/absence_comment; (ii) `reference_candidates.jsonl` missing all 9 of `digest.md` N3's own cited works; (iii) the A1–A7 assumption ledger missing the `consequence` slot; (iv) no explicit one-sentence Estimand (R1); (v) two LLM-judge-class instruments (verifier, openQA rubric judge) missing the full R2 5-step validation sequence; (vi) no INCONCLUSIVE branch for under-powered cells anywhere in the H\* criteria. One item (2) has a disclosed, non-blocking residual (9 cache records lack a locally resolvable PDF/digest — logged as a pre-Phase-E freshness-sweep task, consistent with `digest.md`'s own N7 absence_comment). **No STOP-level finding.** Phase B (walking skeleton) is unblocked from a document standpoint; this environment has no compute to actually execute it (per this task's scope, Phase B/C are not attempted).
