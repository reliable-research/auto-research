# Pengsida Stage Review — T5.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask how well an existing kind of instrument performs, and where" with no new pipeline proposed as a fix to be adopted — the hybrid verifier is the *analytical apparatus* that makes the automatable/human-required phenomenon observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification (verifier as instrument, not headline deliverable — "tool" and "benchmark" explicitly named as runner-up classifications, not the primary one) and `study_type: empirical` confirmed at Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "if reviewers disagree with each other about whether a card was violated, an apparent verifier failure could really be unresolved disagreement about what the card means" is a first-principles framing (the root ambiguity in what "ground truth" even means here, not a patch), and the stakes are stated concretely (a team cannot tell whether it is safely offloading review effort or quietly eroding the design guarantees the cards exist to enforce), not a generic AI-importance appeal. The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes, with zero method leak — the verifier itself is introduced only as the object being measured, never as "our hybrid approach."

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "checklist-based alignment work... studies whether a *generator* satisfies constraints, not whether a *verifier* correctly detects human-labeled violations"), which clears the "citation dump" failure mode. But the first assembled version of this section opened straight into the four threads without ever stating, in one place, which single prior work is the *closest* competitor. Digest N3's own text already did this work — describing defect-focused automated code review as "the closest corpus analog to 'automated checker on agent-produced diffs, measured for precision vs coverage'" — but that ranking had not yet been surfaced as an explicit sentence in the assembled Related Work prose. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section, naming defect-focused automated code review as the closest prior work and stating the precise delta (bug-defect oracle vs. an explicit, category-scored constraint taxonomy) plainly, rather than leaving the reader to infer the ranking from four parallel threads.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the category taxonomy, the human-agreement ceiling, and the automatable/human-required/reference-unstable/inconclusive decision rule are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: "a verifier can only meaningfully be said to fall short of a ceiling that is itself known to be attainable" is exactly the step that makes measuring κ_H,t (rather than assuming a perfect reference) non-redundant with simply reporting κ_V,t alone, and the draft states this explicitly rather than asserting the ceiling comparison by fiat. No orphan components — every one of the five modules (category-stratified scorer, measured ceiling, routed verifier with abstention, operating-curve reporting, pre-screened corpus construction) traces to a named sub-problem, with no leftover machinery. The one place a method-paper reviewer might probe — the routed verifier's internal hybrid construction (rule/AST + architecture-conformance + LLM-judge) — is not asserted as a free win: the design explicitly builds a budget-matched control (the single-shot-judge comparison) whose entire purpose is to check whether that hybrid construction, rather than the constraints themselves, is producing any observed category split. This is the same soft spot `taste_audit.md` independently flagged (`surface_stitching = 1`, not 0) — here it passes because the method treats its own hybrid construction as something to be tested for confounding, not merely presented as a synthesis win.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally by RQ5 (a genuine falsification design: rerunning the verdict-generating pipeline with the routing mechanism disabled, to see whether the category-level pattern *changes*, not just correlates with a plausible story) and by RQ8 (gating every other RQ's inclusion on a pre-screen, rather than reporting whatever numbers a possibly-trivial corpus happens to produce). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... at least two categories are classified automatable... at most one category is classified inconclusive" without ever stating the converse — what specific observation would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as an explicit, checkable condition rather than implied by the expected outcome's negation. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `pipeline.md`/`paper.md` material already had this discipline (`paper.md`'s Step 6 "Fallback" clauses, with pre-committed wording for every failure direction) that hadn't yet been carried into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all eight RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical or classification condition (mirroring the rigor already present in `paper.md`'s pre-committed fallback wording).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Coding agents are now routinely trusted to produce patches against explicit design constraints..." / "Yet a basic question about this practice remains unmeasured..." / "The nearest existing work to this question studies a closely related problem from an adjacent angle..." / "Turning this into a measurable question surfaces its own difficulties." / "Our approach turns each of these difficulties into a specific, checkable design choice." / "We evaluate this design on constructed, category-labeled design cards...") reconstructs the whole five-move arc (problem → unmeasured gap → nearest prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title, abstract, and Introduction: automated verifier agreement with human review has to be judged "against the human reviewers' own agreement with each other... rather than against an assumed-infallible ground truth." The Conclusion names a real forward-looking limitation (a reference-unstable category is a card-design problem, not a verifier problem to engineer around) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming defect-focused automated code review as the closest prior work and stating the delta plainly (bug-defect oracle vs. category-scored constraint taxonomy), rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the eight RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's 8-item checklist (the bundle-validation gate, distinct from the `pengsida-stage-reviewer` Stage 1–5 review above, which reviewed the *auto-research-discussion* framing loop). Scope: `README.md`, `digest.md`, `paper.md`, `discussion/reference_candidates.jsonl` only — no Phase B/C compute exists in this environment, so this run stops at the Phase A gate and does not touch `paper_draft.md`/`.tex`/`.pdf` (those already exist from a prior pipeline pass but are out of this task's scope; see note at the end). Date: 2026-07-04.

**Preceding this checklist, `discussion/reference_candidates.jsonl` was rewritten from the flat ad-hoc harvest schema (150 rows: 110 arXiv + 40 openview/ACL) into `goal.md` §1's canonical schema** (`key/title/ids/venue/year/url/pdf_path/digest_path/relevance/verdict/why/verified`), with every one of the 150 candidates read (digest skim) and given a `selected`/`rejected` verdict + a title-specific one-sentence `why`. Result: **12 selected, 138 rejected of the original 150** (4 genuinely load-bearing among the 150 harvested — `SWE-RM` [adjacent], `PerfBenchReliab2607` "Are Performance-Optimization Benchmarks Reliably Measuring Coding Agents?" [background/A2 archetype exemplar], `Correct2Collab2512` "From Correctness to Collaboration..." [adjacent], `LocalCalibUncert2512` "Localized Calibrated Uncertainty in Code LMs" [adjacent] — plus 8 more added below), **146 rejected overall** out of 158 final rows. The harvest's weak recall net (broad arXiv/embedding search + a generic ACL-2023 sample pool) surfaced mostly off-topic candidates (LLM safety, reasoning, reward-modeling, general NLP tasks); this matches guidance.md's expectation that most harvested candidates legitimately reject.

### 1. Digest self-verification — **PASS**

Re-checked `digest.md`: all of N0–N12 + Claims present; `N4.grounding_check: true` (every `limitation_text` cites a resolvable N3 `citation_key`, verified by string match); `N6`'s `challenge_arguments`/`unaddressed_challenges` cross-reference real C\*/M\* ids; `N8`'s RQs cross-reference real M\*/C\*/CO\* ids. `N9`–`N11` carry explicit 3-part `absence_comment` (`what_missing`/`why_matters`/`implication`); `N0`–`N8` instead use the reverse-digest `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]` tag convention in place of per-item absence comments — this is the documented, accepted substitution for reverse-digest mode (`goal.md` §9 standing TODO explicitly names this as the intended replacement scheme, not a per-run defect). No cross-node reference failed to resolve.

### 2. Reference-cache integrity — **REVISE, fixed**

**Finding:** `digest.md`'s N3 table cites 9 works by bracket key (`DefectReview`, `TrustOrEscalate`, `RLCF-Checklists`, `RECAST`, `SWE-bench`, `SWE-RM`, `VerifDynamics`, `ReflexionModel`, and `Johnson et al., 2013`), sourced from a *different* corpus (`topics/corpus/ideas.jsonl`, 11,683 OpenReview papers, searched via a keyword tool) than `reference_candidates.jsonl`'s own 150-row harvest (arXiv + ACL pool). Cross-checking by title, only `SWE-RM` (arXiv:2512.21919) actually appeared in the 150-row harvest; the other 8 N3 keys had **no corresponding cache record at all** — a direct violation of `goal.md` §3 item 2 ("every N3 key is a selected cache record").

**Fix applied (citing `goal.md` §1 lifecycle step ③ Select):** appended all 8 missing N3-cited works to `reference_candidates.jsonl` as `selected` canonical-schema records, sourced from `digest.md`'s own N3/N4 text plus `corpus/ideas.jsonl`'s `paper_url` field for OpenReview forum ids (verified present in `corpus/ideas.jsonl` by direct lookup, not invented). None have a locally cached PDF, so `digest_path`/`pdf_path` are `null` and `verified.id_resolves = false` for all 8 (per this task's explicit rule: `id_resolves` iff `pdf_path` non-null) — flagged as a load-bearing-but-unverified-by-PDF gap, honestly recorded rather than hidden. Cache `key` values were normalized to match `digest.md`'s bracket citation labels exactly (e.g. `SWE-RM`, `RLCF-Checklists`, `SWE-bench`) so the integrity check is a literal string match, not a fuzzy one; `Johnson2013` is a reconciled key since `digest.md` never assigned this reference a formal bracket token (only inline "Johnson et al., 2013" prose). **Spot-check (3 ids):** `mEV0nvHcK3`, `UHPnqSTBPO`, `H9wMe1G76j` confirmed resolvable via `corpus/ideas.jsonl`'s `paper_url` field (`https://openreview.net/forum?id=...`) — real, existing OpenReview submissions, not invented. No `pending` entries remain anywhere in the cache (all 158 rows carry a final `selected`/`rejected` verdict).

### 3. Tag discipline — **PASS**

No untagged assertions found in `digest.md`; every field carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`/`[NON-CORPUS]`. No silent HYPOTHESIS→GIVEN promotion detected between `digest.md` and `paper.md` (`paper.md` consistently marks its own contents as pre-registered/未-run, e.g. Abstract v0's "written before any results" banner).

### 4. Claim–Evidence Map completeness — **PASS**

`paper.md`'s Claim–Evidence Map (5 claims + 1 explicit exclusion) — every claim traces to an H-id (H1/H2/H3), an assumption (A2), or a "supported-by-design" reporting commitment; every H-id has pre-committed fallback wording (Step 6); no orphans in either direction (every H1–H3 feeds a claim; every claim traces to something).

### 5. Hypothesis/assumption machinery — **REVISE, fixed**

- H1/H2/H3 (Step 6): all seven guidance.md §3.1 slots present in substance (quantified statement, `applies_if` assumptions, metric, test, alpha, effect floor, aggregation rule, verbatim fallback) — verified content-complete, though written in prose rather than under the literal slot labels; not blocking.
- **A1–A6 (§3.2): 4 of 6 assumptions (A1, A3, A5, A6) omitted the explicit `consequence` slot** ("what happens to which H\* if it fails — degrade, restrict scope, or block") — only A2 and A4 stated it. **Fixed:** added a `Consequence` column to the Assumptions table in `paper.md`, filled for all 6 assumptions (citing guidance.md §3.2).
- B0 + B-alt + F-G1: all present with pre-committed wording (Step 6 "Mandatory baselines" + "Global fallback F-G1") — PASS, unchanged.

### 6. Method-rigor audit — **REVISE, fixed**

Guidance.md Part 6 items 1–10 checked against `paper.md`; three misses found and fixed (all citing guidance.md §3.4):

- **Item 1 (R1 estimand):** no explicit one-sentence estimand existed anywhere in `paper.md` (`grep -i estimand` returned nothing before the fix). **Fixed:** added an explicit Estimand paragraph at the top of Step 5, naming the quantity (`Δ_t`), unit of analysis (one adjudicated card×patch pair), reference population, and the decision it feeds (per-category automation-delegation).
- **Item 6 (R2 instrument validation):** the category taxonomy `T` is itself a measurement instrument (every H\* is scored per category) but only had the κ ≥ 0.7 acceptance threshold (A1) — the other 4 of R2's 5 steps (ground in external sources, named refine-on-held-out-set operations, confusion-structure inspection, freeze-before-scale) were not stated. **Fixed:** added a 5-step R2 validation paragraph for `T` after the Assumptions table.
- **Item 8 (R6 mechanism analysis):** no mechanism-layer analysis existed — E1/E2 establish *that* and *which* categories show the gap but nothing explains *why* (`grep -i "mechanism analysis"` returned nothing before the fix). **Fixed:** added **E3 — Mechanism analysis**, a budgeted error-taxonomy coding pass (literal-vs-intent mismatch vs. structural/pattern-matching failure vs. other) with a pre-committed reading rule distinguishing "mechanistic confirmation of the Step-0 asymmetry" from "M3 engineering artifact."
- Items 2 ("Fixed at Phase A item 3, restated: PASS"), 3 (PASS), 4 (PASS, A1–A6 detection+gate present), 5 (PASS, B0/B-alt/F-G1 present), 7 (PASS — R3 confound-removal one-liners present for A6 and B-alt), 9 (PASS — power stated per cell, thin cells pre-declared inconclusive), 10 (now PASS once items 1/6/8 above are fixed — archetype `empirical`/A2 evidence standard is met: validated instrument [R2, now explicit] + controlled comparison [B0/B-alt] + pre-registered effect-floor tests [H1–H3] + rival-explanation ablation [B-alt] + ≥1 mechanism analysis [E3, now present]).

### 7. Stage cross-check (advisory) — **PASS**

Already performed and closed prior to this Phase A re-run: see the `pengsida-stage-reviewer` review above (Stages 1–5), which found and fixed 2 REVISE items (Stage 2 nearest-neighbor sentence, Stage 4 falsification conditions), both already reflected in `paper_draft.md`/`.tex`/`.pdf`. No new stage-cross-check findings from this re-run.

### 8. Taste audit currency — **PASS, no re-audit needed**

`taste_audit.md`'s audited Motivation/Method (Stage 2 / Stage 5 text) and `paper.md`'s Step-0 asymmetry sentence and Step-5 formal notation are **unchanged** by this Phase A re-run's fixes (Estimand sentence, assumption `Consequence` column, R2 instrument-validation paragraph, and E3 mechanism analysis are additive/clarifying, not edits to the asymmetry claim or the formal definitions) — no material edit triggers re-audit per `goal.md` §3 item 8.

### Gate result: **REVISE → fixed → PASS**

Two items required fixes (#2 reference-cache integrity, #5 assumption-consequence slots, #6 method-rigor R1/R2/R6 gaps — 3 distinct fixes across 2 checklist items); all three are applied directly in `paper.md` and `reference_candidates.jsonl` as described above, not merely logged as future work. With those fixes in place, **all 8 Phase A checklist items now PASS**. Phase B is unblocked *for a future run with real compute* — this session stops here per task scope (no Phase B/C execution attempted; no real experiment compute exists in this environment).

**Scope note:** `paper_draft.md`/`.tex`/`.pdf` already exist in `discussion/` from a prior pipeline pass (predating this Phase A re-run) and were not re-audited or regenerated in this session — this task's mandate was to validate/fix the three static input documents (`README.md`, `digest.md`, `paper.md`) and the reference cache, and to stop at the Phase A gate. Whether `paper_draft.*` still accurately reflects the Assumptions-table/Step-5/Step-6 edits made here (Consequence column, Estimand sentence, R2 paragraph, E3 experiment) is a re-open item for whoever next resumes Phase E onward — flagged here rather than silently left inconsistent.
