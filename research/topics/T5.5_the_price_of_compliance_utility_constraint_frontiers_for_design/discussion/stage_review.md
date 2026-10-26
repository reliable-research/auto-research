# Pengsida Stage Review — T5.5

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. A nearest-neighbor sentence (Related Work) and per-RQ falsification conditions (Experiments) were built into the confirmed stage outputs and the first assembled draft **from the start**, not left for this review to discover — so this review was deliberately pushed to find different, genuine issues rather than re-reporting those two. Four findings fired below (three REVISE plus one writing-level fix) and were applied; the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding, with a Resource / dataset secondary.** Per `archetypes.md`'s tells: the core question is "we ask how much a phenomenon costs and what shape it takes" with no new enforcement technique or agent proposed as the fix — the sweep harness, audited rule catalog, and dual-criterion shape test are the *analytical apparatus* that makes the phenomenon measurable, not a method being pitted against baselines to win. This matches digest N12's own primary classification (`empirical`) and Stage 1's `study_type: empirical`. The secondary Resource reading follows from the seed's own `[资源]` label and from CO1 (the audited catalog + harness + constraint-annotated suites) being a genuine, separately releasable deliverable — consistent with `archetypes.md`'s guidance to "run the dominant archetype's bar and add the secondary one's Stage-4 check" for a hybrid paper. Stage 3 ("Method") and Stage 4 ("Experiments") below apply the **Analysis/Finding** column as primary, with the **Resource** column's coverage/leakage checks added at Stage 4 as the secondary check.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "a team that measures only the average cost across whatever range it happened to pilot cannot tell a frontier that degrades gracefully from one that hides a knee just past that range" is a first-principles framing (the root asymmetry from shared generation budget, not a patch), and the stakes are concrete: a team could deploy design-aware agents believing compliance is linearly affordable and be wrong the moment strength crosses an untested threshold. The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes, with zero method leak — no statistical test name (Davies, ΔAIC, mixed-effects) appears until the Methodology section, consistent with the Stage-1 auto-discussion refiner's deliberate choice to keep the objective's cross-axis-disagreement fix abstract ("a pre-specified breakpoint-existence criterion") rather than naming a specific procedure at the problem-definition level.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap for *semantically binding* design constraints specifically — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The nearest-neighbor sentence and the four threaded paragraphs (each ending on a problem-tied limitation, not a generic one — e.g., constraint-following benchmarks "measure satisfaction rates on general instruction-following tasks with no independent functional-correctness oracle... and cost never appears as an evaluation axis at all") were built into the confirmed Stage 3 output and the first assembled draft from the start, so this review looked past that pair for a different problem — and found one. Digest N3's own grounding procedure is unusually honest about a gap in its own search: `absence_comment` states plainly that "corpus SE coverage of design-constraint compliance specifically is thin (searches 5 and 8 returned no on-topic SE hits)." The rule catalog this paper builds (`import-linter-style contracts`, per digest M1) is a direct descendant of a real, decades-old software-engineering subfield — architecture-conformance checking, dependency-structure-matrix analysis, automated architectural-rule enforcement tooling — and the first assembled Related Work draft surveyed constraint-following/alignment-tax/SMC-Control/SWE-bench threads without ever naming this gap explicitly. Per the Stage 2 rubric's coverage check: "are the obvious threads a reviewer in this subfield would expect actually present? A missing thread reads as either ignorance or evasion." A reader from the software-architecture side would notice the omission immediately.

**THE ONE FIX (applied):** Rather than inventing a citation to paper over the gap (a hard rule violation), add an explicit, honestly-marked acknowledgment naming the missing thread and marking it `[citation needed]` — turning a silent omission into a disclosed, bounded limitation, and pointing at exactly what a follow-up literature pass needs to find.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** Each construct is defined precisely before it is used — the bindingness/fidelity audit, the dual-criterion shape test, and the factorial strength design are all given in Methodology ahead of any claim that invokes them, and no orphan components exist: all six modules (fidelity audit, trend model, shape test, factorial design, cost decomposition, placebo control) trace to a named sub-problem. But the Stage-3 rubric's "is each analytical step licensed" check surfaces a real gap in the cross-arm cost decomposition specifically: the first draft defined "mechanism share MS(σ) = [CCS_retry(σ) − CCS_prompt(σ)] / [CCS_retry(σ) − CCS(L0)]" and then stated "mechanism share is at least 0.30" as if this ratio is always well-behaved. It isn't — if retry-arm cost barely exceeds the unconstrained baseline at a given strength (e.g., because fewer overall attempts are needed once violations are caught early), the denominator approaches zero or even flips sign, and a ratio computed from a near-zero or negative denominator can be arbitrarily large or nonsensical. Feeding that value into a Holm-corrected hypothesis test as though it were an ordinary bounded proportion is exactly the kind of unlicensed inferential step the Analysis/Finding bar asks to be checked for — "is each inferential step licensed... does the chain have no unjustified jump?" Here the jump is treating an ill-conditioned ratio as a clean statistic without qualification.

**THE ONE FIX (applied):** Add an explicit guard to the mechanism-share construct: compute and report it only for cells where the retry arm's cost premium over the unconstrained baseline exceeds a pre-specified floor; cells below that floor are reported as **mechanism-share undefined** rather than an unstable or sign-flipped ratio — mirroring the "shape-discordant" convention already used elsewhere in this design for a criterion that can legitimately fail to produce a clean answer.

---

## Stage 4 — "Experiments" (Analysis/Finding primary + Resource secondary: falsification, and leakage/coverage controls)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The Analysis/Finding falsification bar is well served — every one of the 8 RQs already carries an explicit **Falsification condition** line stating the specific observation that would refute its expected outcome (built in from the start, not left for this review), and RQ8's falsification condition explicitly notes that failing the placebo margin would force "every claim in RQ2, RQ4, and RQ6 above" to be re-framed, which is a genuine cross-claim dependency, not a cosmetic caveat. But the Resource-secondary check — mandatory here because CO1 (the catalog + harness + task suites) is a real, separately releasable artifact — asks about coverage, leakage, and quality controls, and the first assembled draft had none of the latter. Digest N10 enumerates five threats (t1–t5: construct, internal ×2, external, conclusion) but **none addresses training-data contamination** of the benchmark tasks themselves — a real and, per `mined_review_checks.md`'s own framing, "increasingly a default reviewer question for anything LLM-based." Both BigCodeBench-Hard-style and SWE-bench Verified-style tasks are public benchmarks that may overlap with pretraining corpora; if a model has memorized a task's solution, its pass rate could sit near ceiling regardless of constraint strength, which would flatten or distort the measured frontier in a way indistinguishable, without a check, from a genuinely graceful one.

**THE ONE FIX (applied):** Add an explicit contamination check to the Experimental Setup: stratify pass rates by each task's public release date relative to each model's documented training cutoff where available, flag any near-ceiling-at-zero-strength task subset as likely-memorized, and re-run the dual-criterion shape test excluding that subset — reporting both the pooled and contamination-excluded verdicts if they differ, rather than only the pooled one.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** Running the reverse-outline test (reading only each Introduction paragraph's first sentence) on the *first* assembled draft reconstructed most of the arc correctly — mechanism/asymmetry → central question → nearest-neighbor gap → why-it's-hard → our approach → evaluation — but paragraph three's first sentence covered only the nearest-neighbor work (formatting-cost) while the same paragraph's remaining three sentences quietly introduced three *additional*, distinct related-work threads (constraint-following benchmarks, alignment-tax/Pareto framing, SMC-Control's mechanism-cost warning), each with its own citation and its own limitation. A reader doing the reverse-outline test would reconstruct the nearest-neighbor gap correctly but would have no idea, from first sentences alone, that three more lines of work and their limitations were coming — a "two-message paragraph" (in this case, four-message) violation of the Stage 5 bar: "any paragraph carrying two ideas? Split it."

**THE ONE FIX (applied):** Split the paragraph in two: one paragraph stating only the nearest-neighbor work and its specific gap (unchanged), and a second paragraph opening with an explicit topic sentence — "Several other adjacent lines of work also fall short of this specific joint measurement, each for a different reason" — that previews the multi-thread survey before it unfolds, restoring the one-message-per-paragraph property. Re-checked: the reverse-outline test now reconstructs all six moves, including the explicit signal that more than one adjacent thread follows the nearest-neighbor paragraph. The quotable contribution sentence ("design compliance and functional correctness... draw on the same bounded generation process... the price of compliance is a shape to be measured, not an average to be assumed") is used consistently across Introduction, Abstract, and Conclusion, and the Conclusion names two real forward-looking limitations (the uncited architecture-conformance literature; the possible catalog-fidelity drop rate) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an honestly-marked `[citation needed]` acknowledgment of the architecture-conformance-checking tooling/literature gap to the Related Work section's closing paragraph, rather than silently omitting the thread or inventing a citation.
2. **Stage 3 fix** — added a pre-specified floor guard to the mechanism-share construct in the Cross-Arm Cost Decomposition methodology subsection and the corresponding RQ7 setup, with a **mechanism-share undefined** reporting convention for cells below the floor.
3. **Stage 4 fix** — added a contamination/leakage check to the Experimental Setup (stratification by release date vs. training cutoff, likely-memorized task exclusion, pooled-vs-excluded shape-verdict comparison).
4. **Stage 5 fix** — split the Introduction's related-work survey paragraph in two, adding an explicit topic sentence previewing the multi-thread survey, restoring one message per paragraph.

All four fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Skill/procedure: goal.md §3's eight-item Phase A validation checklist, applied against
> `README.md` / `digest.md` / `paper.md` / `discussion/reference_candidates.jsonl`, using
> `guidance.md` as the construction standard. This is distinct from — and run after — the
> `auto-research-discussion` Stage 1–5 review above, which checked the *auto-discussion
> pipeline's own* intermediate outputs; this pass checks the actual goal.md-contract
> artifacts against goal.md's own binary gate. Date: 2026-07-04. Companion work done in
> the same pass: `reference_candidates.jsonl` was rewritten from the ad hoc 150-row
> harvest schema into goal.md §1's canonical schema (see below, item 2) — every REVISE
> found here that had a direct, cheap static-document fix was applied to `paper.md` in
> this same pass (digest.md required no fixes).

### 1. Digest self-verification — **PASS, with a minor note**

Re-ran digest.md's own self-verification claims: `N4.affects_works` ⊆ `N3.citation_key`
checked exhaustively (all 10 keys match verbatim); `N6.challenge_arguments[].challenge_id`
∈ {C1–C4} covers all four; `N8.addresses_challenges`/`evaluates_mechanisms`/
`tests_contributions` all resolve; `N9.rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2}, all three used;
all of N0–N12 + Claims present (EX-11 empty-node check holds). Every non-FOUND node
(N0–N3, N8–N11) carries a 3-part `absence_comment`. **Minor note (not blocking):** N5, N6,
N7, and N12 lack the explicit `**Status:**` line that N0–N4/N8–N11 all carry, even though
every item inside them is individually tagged `[HYPOTHESIS]` (N6 additionally closes with
an explicit "every item in this node is `source=inferred`" note) — a cosmetic
inconsistency in the digest's own formatting convention, not a tag-discipline violation
(checklist item 3 is unaffected — see below). Left as-is; flagging here so a future digest
revision can add the missing `Status:` lines for consistency.

### 2. Reference-cache integrity — **REVISE → FIXED**

**Finding:** Cross-referencing digest N3's ten `citation_key` values (`SWE-bench`,
`RECAST`, `AutoIF`, `SMC-Control`, `NSPO`, `RMOD`, `FairFront`,
`HiddenCost-Readability`, `IFEval`, `FollowBench`) against the 150-row harvested
`reference_candidates.jsonl` found **zero matches** — not even as `pending` rows. The
150-row harvest (arXiv-miner-cache + a separate OpenReview corpus, ranked by a weak
recall score, per goal.md §1's step-① harvest) drew from different query angles than
digest N3's own grounding search over `topics/corpus/ideas.jsonl`, so the two reference
sets never overlapped. This is a direct violation of goal.md §3 item 2's requirement that
"every N3 key is a `selected` cache record" — worse than a stale `pending` entry, since
the citations the paper's own Related Work depends on were entirely absent from the cache
that's supposed to be the sole source Phase E prose and `refs.bib` are generated from
(goal.md §1 step ④, hard gate in §8: "Citations only via `selected` cache keys").

**Fix applied:** Added all 10 works to `reference_candidates.jsonl` as new canonical
records, `verdict: selected`, with `relevance` tags matching their N3/N4 role (baseline:
SWE-bench, IFEval, FollowBench; method-twin: RECAST, AutoIF, HiddenCost-Readability;
adjacent: SMC-Control, NSPO, RMOD; contrast: FairFront — FairFront's exact closed-form
Pareto computation is a direct methodological foil to this paper's premise that no closed
form exists for open-ended code generation, per N4.7). Bibliographic identifiers were
pulled from real sources, not invented: the 7 OpenReview `paper_id`s and their titles/URLs
were confirmed directly against the local `corpus/ideas.jsonl` (the same corpus digest N3
itself was grounded against — `paper_id` lookups for `VTF8yNQM66`, `90tCp2KszA`,
`cRR0oDFEBC`, `xoXn62FzD0`, `GFyVxtyMvq`, `i0Nno5MgXt`, `65oFEAP42P` all resolved to real
titles/`paper_url`s); the 2 arXiv ids (`2508.13666`, `2311.07911`) were taken from digest
N3's own explicit citations. **Spot-check (goal.md §3 item 2's "fetch 2–3 ids"):** live
`WebFetch` on `arxiv.org/abs/2508.13666` confirmed the title "The Hidden Cost of
Readability..." and venue ICSE'26 exactly as digest N3 states; `WebFetch` on
`arxiv.org/abs/2512.24776` (one of the 150-harvest's selected entries) confirmed an exact
title match; the OpenReview forum URLs return a browser-verification interstitial under
`WebFetch` (expected — OpenReview blocks headless fetches), so those 7 were verified
against the local corpus record instead, which is this pipeline's own established
grounding method (digest.md's own N3 procedure uses the same corpus as ground truth). No
`pending` entries remain anywhere in the file (150 harvested rows all resolved to
`selected`/`rejected`; the 10 added rows are all `selected`).

**Resulting cache:** 160 total records (150 harvested + 10 added), 20 `selected` / 140
`rejected`. Of the 150 harvested rows: 10 `selected` (all `relevance: adjacent` except one
`background` structural exemplar — none rose to `baseline`/`method-twin`/`contrast`, which
is expected since the harvest's query angles were generic and the paper's specific-related
work already lived in N3's separate corpus), 140 `rejected` with a specific one-sentence
reason each (no generic "not relevant" rejections).

### 3. Tag discipline — **PASS**

No untagged assertion found in digest.md (every N-node item carries an inline
`[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:...]`/`[PLACEHOLDER]` tag); no silent
`[HYPOTHESIS]`→`[GIVEN]` promotion detected between digest.md and paper.md (paper.md's
Step 5 "Deleted adjectives" list — dropping "meaningful"/"realistic" as uncomputable — is
itself evidence of active tag/definition discipline rather than silent promotion).

### 4. Claim–Evidence Map completeness — **PASS**

All 5 digest Claims trace to an H-id or a `supported-by-design` definition in paper.md's
Claim–Evidence Map (Claim 3 → N3 grounding procedure; the CO1 instrument claim → A1/A2
gates + M3 audit + skeleton criterion). Every H-id (H1–H4, plus H2b/H2c added in this
pass) has a fallback: F1/F2/F2c/F3/F4, plus the global pivot F-G1. No orphans in either
direction.

### 5. Hypothesis/assumption machinery — **REVISE → FIXED**

**Finding (H\* slots, guidance.md §3.1):** H1, H3, H4 filled all seven template slots
(binary statement, `applies_if`, metric, test, alpha, effect floor, verbatim fallback).
**H2 was missing an effect floor** — its criterion (Davies p < 0.05 AND ΔAIC > 4) is
purely a statistical-significance test with no minimum-magnitude requirement on the
knee's steepness, exactly the failure guidance.md §3.1 warns against ("a slope can be
significant and practically zero"). Separately, `pipeline.md`'s Stage 1 refiner and
`taste_audit.md` (§2, Method Paradigm rationale) both already treat the **cross-axis
"shape-discordant" outcome** (pass-rate-shape vs. cost-shape disagreement) as load-bearing
— `pipeline.md`'s own final cross-stage-consistency note names this exact gap: "the
cross-axis shape-agreement check... paper.md's own A4 assumption implies but never states
as a testable claim in its own right." paper.md's Step 6 had not formalized it.

**Fix applied (paper.md, Step 5 table + Step 6 E2):** Added an explicit effect floor to
H2 (segmented fit's post-breakpoint slope ≥ 2× pre-breakpoint slope, else reported
"graceful-with-inflection" not "knee"); added **H2c** (binary) formalizing the
shape-discordant check, with its own fallback **F2c**; added a `shape-discordant` row to
the Step 5 adjective/verb definition table, closing the drift `pipeline.md` had already
flagged.

**Finding (A\* slots, guidance.md §3.2):** All seven assumptions (A1–A7) had assumption +
failure_mode + detection, but **none carried an explicit named gate (`PG-*`) or an
explicit `consequence:` clause naming which H\* it degrades/restricts/blocks** — both
required slots per guidance.md §3.2's five-slot template, and `PG-*` gate ids are
specifically what goal.md §4 says Phase B must check ("instrument validation runs inside
B as PG-\* gates"). This is precisely goal.md's example REVISE case ("missing assumption
detection/gate").

**Fix applied (paper.md, Assumptions section):** Added explicit `PG-1`…`PG-6` gate ids
(mapped onto the walking skeleton's existing pass criteria (i)/(ii)/(iii) where
applicable, plus post-pilot/continuous gates where not) and an explicit `*Consequence:*`
clause per assumption naming the affected H\*. **A6 additionally gained the missing
INCONCLUSIVE rule** (see item 9 below).

### 6. Method-rigor audit — **REVISE → FIXED** (guidance.md Part 6 items 1–10 + Part 2 A2)

- **Item 1 (R1, estimand):** Missing entirely — no one-sentence estimand existed anywhere
  in paper.md or paper_draft.md. **Fixed:** added an explicit "Estimand" paragraph at the
  top of Step 5 (quantity, unit of analysis, reference population, decision it feeds).
- **Item 6 (R2, 5-step instrument validation):** The M3 checker's κ-audit covered step ③
  (validate against ≥2 raters, κ ≥ 0.8) and, loosely, step ① (rules grounded in named
  external conventions — import-linter, radon, ruff), but was missing step ② (draft-wide,
  refine-on-held-out-calibration-set with named merge/split/remove ops), step ④ (confusion
  structure inspection), and step ⑤ (freeze/hash before scale). **Fixed:** A1's detection
  clause in paper.md now states all five R2 steps explicitly.
- **Item 9 (power / INCONCLUSIVE):** `INCONCLUSIVE` did not appear anywhere in paper.md,
  digest.md, or paper_draft.md — A6 described a one-time sample-size enlargement if
  power < 0.8 but never stated what happens if that still leaves a cell underpowered,
  contrary to goal.md's Phase D order ("`PASS | FAIL | INCONCLUSIVE`... INCONCLUSIVE only
  where pre-declared") and guidance.md Part 4 situation 5. **Fixed:** A6 now pre-declares
  such cells `INCONCLUSIVE`, excluded from PASS/FAIL aggregation, never counted as null.
- **Items 2, 3, 4, 5, 7, 8, 10:** verb check (Step 3, PASS), B0+B-alt+F-G1 (present,
  PASS), confound-per-constraint naming (R3 — determinism constraint, B-alt placebo, M2
  arm separation all name their confound, PASS), mechanism analysis (R6 — H3's
  mechanism-share decomposition, PASS), archetype evidence standard for `empirical` (A2 —
  validated instrument + controlled comparison + effect-floored trend tests +
  rival-explanation ablation (B-alt) + mechanism analysis, all present post-fix) — no
  further gaps found.

### 7. Stage cross-check (advisory) — **REVISE items already folded in**

`pengsida-stage-reviewer`'s Stage 1–5 review above (run against the `auto-research-
discussion` outputs and the first assembled `paper_draft.md`) already fired and fixed 4
REVISE items (related-work coverage gap, mechanism-share ill-conditioning guard,
contamination check, paragraph-splitting). This Phase A pass's own N1↔Stage-1 /
N3-N4↔Stage-2 / N6↔Stage-3 / N8↔Stage-4 cross-check surfaced one additional item not
caught there: the shape-discordant formalization gap (item 5 above), which `pipeline.md`'s
own final cross-stage-consistency note had already named but which had not propagated
back into paper.md's pre-registered Step 5/6 — now fixed. No STOP-level cross-check
failures.

### 8. Taste audit currency — **PASS, no re-run needed**

`taste_audit.md` (dated to the same construction session, Stage 2/5 confirmed outputs)
already independently describes the shape-discordant mechanism as part of the audited
Method summary (§1, §2 rationale) — the paper.md fix in item 5 above is a *formalization*
of a check the taste audit already treated as real, not a *change* to the core asymmetry
sentence (Step 0, untouched) or to the abstract's opening framing (Abstract v0, untouched).
Per guidance.md's re-run condition ("predates a material edit to the asymmetry statement
or formal definition"), none of this pass's fixes qualify as material edits to the
asymmetry claim itself — they complete pre-registered machinery the audit already assumed
existed. No re-run required.

---

## Phase A gate result: **PASS (post-fix)**

Three REVISE-class findings (checklist items 2, 5, 6 — reference-cache integrity, H\*/A\*
slot completeness, and method-rigor gaps in R1/R2/item-9-power-handling) were found and
fixed directly in this same pass, per the task's "no later pass" instruction. All eight
checklist items now clear.
Phase B/C are explicitly out of scope for this environment (no real experiment compute) —
this run stops at the Phase A gate as instructed; `discussion/pipeline.md` records the
phase-log entry pointing here.
