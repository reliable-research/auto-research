# Pengsida Stage Review — T5.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs" with no new pipeline proposed as a fix for agents' behavior — the mining pipeline and compliance judge are the *analytical apparatus* that makes an otherwise invisible phenomenon (design-constraint violation in test-passing patches) observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1, and `paper.md` Step 2's own explicit archetype note ("the headline is not a system's performance but two measurements"). Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "the requirements a maintainer enforces on a patch also includes error-handling, architectural, and API conventions that are never written into any spec, linter rule, or test" is a first-principles framing (the root asymmetry, not a downstream patch), and the stakes are stated concretely: coding agents are being certified as mergeable by a signal (test-pass rate) that is, by construction, silent about the signal a human reviewer actually applies. This is not an abandoned question — Stage 3 confirms only one code-review paper exists in the local ML-skewed corpus at all, and the classic MSR literature (Bacchelli & Bird, Bosu et al.) stops at human-readable taxonomies rather than a machine-applicable rule set, so the gap is genuinely open, not already closed. Feasibility is not asserted on faith either: `paper.md`'s Walking Skeleton (Step 9) gives a binary, pre-stated success criterion answerable on one pilot repository in roughly a day ("mini-catalog has ≥10 supp≥3 entries AND ≥1 human-confirmed agent violation exists that the catalog-free judge missed"), which is exactly the minimum-viability discipline this stage rewards. The Einstein ratio holds: the confirmed Stage 2 motivation spends its energy on why the gap matters and only gestures at the eventual instrument in the final sentence.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap, and — separately — that the single closest prior effort is confronted directly rather than left for a reviewer to find.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic threads in the confirmed Stage 3 table are genuinely argued, not a citation dump — each ends on a problem-tied limitation ("neither produces an explicit, per-project constraint catalog that could be audited or applied to a new patch independently of the model," for DefectCR/CodeReviewer). But the section, as confirmed in `pipeline.md`, never states in one place which single prior work is the *closest* competitor — a reader sees four parallel threads (automated review, rubric-based generation quality, test-based benchmarks, foundational empirical studies) and has to infer for themselves which is the nearest neighbor. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first." DefectCR (closest on "an automated system that reads review-adjacent signal") and RLAC (closest on "checking an output against an implicit rubric rather than a formal spec") are each individually confronted in the table, but never jointly named as *the* nearest neighbors with one explicit delta statement.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section naming DefectCR and RLAC as the closest prior work and stating the precise delta, rather than leaving the reader to rank the four threads themselves. This is now the opening sentence of `paper_draft.md`'s Related Work section: *"The closest prior efforts to this paper are DefectCR and RLAC... DefectCR explicitly discards convention-style commentary rather than cataloguing it, and RLAC generates one likely-failing rubric per output rather than mining a stable, historically-supported, per-project inventory; neither produces the explicit, auditable, multi-thread-validated catalog this paper is built to extract, and neither applies it to the specific question of whether test-passing patches comply with it."*

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the catalog entry, the support threshold, the compliance judge, and the category scheme are all given formal or operational definitions in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: "test outcomes carry no signal about this by construction... therefore a validated judge should be expected to find violations on patches that already pass every test; if it consistently fails to, that would itself be informative" — this is exactly the step that makes RQ5 a real falsification test rather than an assumed conclusion, and the draft states it explicitly. No orphan components — every one of the five modules (change-inducing extractor, catalog builder, compliance judge, category annotation, stability/comparison design) traces to a named sub-problem from Stage 4, with no leftover machinery introduced for its own sake.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational, and whether the one operationalization that is narrower than its natural-language label (linter-expressibility as a proxy for "unwritten") is scoped honestly rather than oversold. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** Most of this stage is already strong: RQ5 is a genuine falsification design (does the validated judge find confirmed violations on test-passing patches, not merely correlate with something), and RQ8's fallback wording ("we report that... agents and humans are statistically indistinguishable... a direct, publishable bound on the size of the compliance gap") is exactly the kind of pre-committed, non-hidden null result the Analysis/Finding bar rewards. But the first-pass RQ3 design ("at least half of admitted catalog entries are not mappable to any existing ruff/pylint/import-linter rule... evidencing that the catalog captures genuinely unwritten content") had an unstated alternative explanation: a low linter-expressibility rate is equally consistent with "these constraints are genuinely unwritten" *and* with "the three tools checked (ruff, pylint, import-linter) are simply a narrow, incomplete formalized-rule surface" — the test as originally worded could not tell the two apart, and "unwritten" as a natural-language label oversold what a three-tool non-expressibility check actually licenses. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ" — here, the claim needed an explicit scope boundary, not just a threshold, to be falsifiable in the way it was being stated.

**THE ONE FIX (applied):** Bound the "unwritten" claim explicitly to the checked tool surface in both the Methodology (Constraint Catalog Builder) and the RQ3 Falsification condition, rather than leaving it as an unqualified absolute claim. The fix is now in `paper_draft.md`: *"This test is scoped specifically to the three named, commonly used static-analysis tools checked here; it cannot rule out that some other static-analysis surface not tested... already expresses a given entry, and the claim of 'unwritten' content is reported as bounded to this checked tool surface rather than as an absolute claim that no tool anywhere could express it."* The Conclusion's limitations paragraph states this same scope boundary as an explicit forward-looking limitation rather than an afterthought.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Autonomous pull requests are no longer a research curiosity" / "Yet a central assumption behind this narrowing remains unexamined" / "The nearest existing efforts approach this gap from adjacent but distinct angles" / "Turning this gap into something measurable surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice" / "We evaluate this design on repositories drawn from SWE-bench Verified") reconstructs the whole five-move arc (problem → unexamined assumption → nearest prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. Paragraph 2 elaborates a single message (the orthogonality of the two signals) across several sentences rather than smuggling in a second one — checked directly, since a paragraph that reads long is the first place a two-message violation hides. One quotable contribution sentence exists and is used consistently across contributions, abstract, and Conclusion: "the signal that determines real-world mergeability is, by construction, invisible to the signal every current test-based agent benchmark measures." The Conclusion names two real forward-looking limitations (test-failing patches out of scope; the "unwritten" claim bounded to the checked tool surface) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming DefectCR and RLAC as the closest prior work and stating the delta plainly (rather than leaving four parallel threads unranked).
2. **Stage 4 fix** — bounded the RQ3 "unwritten" claim explicitly to the three checked static-analysis tools, in both the Methodology (Constraint Catalog Builder) subsection and the RQ3 Falsification condition, and carried the same scope boundary into the Conclusion's limitations sentence.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — goal.md §3 checklist, 2026-07-04

> Triggered by a reference-cache upgrade pass: `discussion/reference_candidates.jsonl` (150 harvested candidates: 110 arXiv + 40 OpenReview, ad hoc flat schema — goal.md §1 step-① harvest only) was converted to goal.md §1's canonical schema and every candidate given a `selected`/`rejected` verdict with a specific `why` (no `pending` left anywhere). Running that upgrade surfaced document gaps this section fixes directly, per this task's instruction to treat any REVISE-level static-document gap as fixable now rather than deferred. This section is independent of the Stage 1–5 `pengsida-stage-reviewer` pass above (which reviewed the `auto-research-discussion` narrative against `paper_draft.*`); it runs goal.md §3's own 8-item checklist against `README.md`/`digest.md`/`paper.md` directly.

### 1. Digest self-verification — **PASS**

Re-executed `digest.md`'s own V-01…V-12 checks: all of N0–N12 + Claims present; every cross-node id (N4 `affects_works` ⊆ N3 `citation_key`; N6 `challenge_arguments`/`unaddressed_challenges` ⊆ N5; N8 `addresses_challenges`/`tests_contributions`/`evaluates_mechanisms` ⊆ N5/N7/N6; N9 `rq_id` ⊆ N8) resolves; every non-GIVEN node carries a full 3-part `absence_comment`. The self-verification block itself was updated in this pass (N3/N4 now list 10 works, not 9, after the method-twin addition below) and re-checked — consistent.

### 2. Reference-cache integrity — **REVISE → fixed (one residual, non-blocking)**

**Found:** none of `digest.md` N3's 9 cited keys (`[DefectCR, OpenReview:mEV0nvHcK3]`, `[SWE-bench, OpenReview:VTF8yNQM66]`, `[SWE-Lancer, OpenReview:xZXhFg43EI]`, `[FHE-Coder, OpenReview:4F1py5vQXm]`, `[RLAC, OpenReview:dBmjnRR1bC]`, `[Coeditor, OpenReview:ALVwQjZRS8]`, `[Bacchelli & Bird, 2013]`, `[Bosu et al., 2015]`, `[CodeReviewer, Li et al., 2022]`) existed as records in `reference_candidates.jsonl` at all — the 150-candidate harvest was a separate arXiv-keyword + OpenReview sweep, disjoint in id-namespace from the shared `topics/corpus/ideas.jsonl` (11,683-paper) corpus that actually grounded N3 at digest-writing time. Every N3 key therefore literally failed "is a `selected` cache record."

**Fixed:** imported all 9 as canonical-schema records into `reference_candidates.jsonl`, `verdict: selected`, sourced from `topics/corpus/ideas.jsonl` for the 6 OpenReview-id works (real `paper_id`/`paper_url` verified present) and flagged per digest.md's own `[GROUNDED:canonical, non-corpus]` tag for the 3 memory-cited works (Bacchelli & Bird 2013, Bosu et al. 2015, CodeReviewer 2022) — `url`/`doi` left `null` rather than fabricated. Also discovered and added a genuine 10th, previously-uncited method-twin from this topic's own arXiv harvest (`2512.23844`, "From Correctness to Collaboration") — see digest.md N3 entry 10 / N4 limitation 7 (guidance.md Part 4 situation 6 concede-and-differentiate) and the reference-cache key `FromCorrectnesst2512`.

**Residual (not blocking):** 5 of the 9 imported entries are load-bearing (`method-twin`: DefectCR, FHE-Coder, RLAC, Coeditor, CodeReviewer) but still lack a locally cached PDF + digest (`pdf_path`/`digest_path` null, `verified.id_resolves = false`) — the shared corpus record establishes the paper is real but this topic has not independently harvested/digested it. Logged as a follow-up harvest item to close before Phase E's mandatory freshness sweep (goal.md §1 hard gate), not before Phase B. Spot-checked 5 ids (pdf existence) across both the arXiv and OpenReview harvest buckets — all resolved. No `pending` verdict remains anywhere in the 159-record file.

### 3. Tag discipline — **PASS**

No untagged assertion found; the newly added N3 #10 / N4 #7 carry explicit `[GROUNDED:corpus — this topic's dedicated harvest]` / `[HYPOTHESIS, method-twin]` tags; no silent `[HYPOTHESIS]`→`[GIVEN]` promotion anywhere in `digest.md`.

### 4. Claim–Evidence Map completeness — **REVISE → fixed**

**Found:** two hypothesis sub-parts had no route to any fallback wording in `paper.md`'s Claim–Evidence Map or Step 6 (see item 5): RQ1(ii) (LLM-vs-keyword-baseline comparison) and RQ2(i) (chi-square category non-uniformity) could fail with no pre-committed sentence — an orphan on the fallback side, not the claim side.

**Fixed:** both now have verbatim fallback wording (Step 6, item 5 below); the Claim–Evidence Map's "LLM mining beats a keyword-directive baseline" and "Violations are category-non-uniform" rows were updated to name the new fallback branches explicitly.

### 5. Hypothesis/assumption machinery — **REVISE → fixed**

Five distinct gaps found and fixed directly in `paper.md`, each citing guidance.md §3.1/§3.2/§3.3:

- **Missing fallback, RQ1(ii):** no pre-committed sentence for "LLM extractor does not beat the keyword baseline." Added.
- **Missing fallback, RQ2(i):** no pre-committed sentence for "chi-square cannot reject category uniformity" (i.e., the ranking premise fails outright, not just its ordering). Added — explicitly drops CO2's ranking claim as moot rather than merely narrowing it.
- **Missing effect floors (guidance.md §3.1: "effect floor is mandatory... significance without magnitude passes nothing"):** RQ1(ii) (McNemar p<0.05 with no minimum accuracy-gap), RQ2(i) (chi-square p<0.05 with no minimum association-strength), and RQ2(iii) (McNemar p<0.05 with no minimum rate-gap) were all significance-only. Added an explicit numeric floor to each (≥8-point paired-accuracy gap; Cramér's V≥0.15; ≥8-point matched-pair rate gap respectively) and stated that significance alone does not satisfy the hypothesis.
- **Missing assumption `gate`/`consequence` slots (guidance.md §3.2 template):** A1–A7 were written as prose `fail_mode`/`detected_by` pairs without the template's explicit `gate: PG-j` and `consequence:` (degrade/restrict/block, and which H\*/CO\* it affects) slots. Reformatted all seven to name an explicit `PG-1`…`PG-6` gate and a concrete consequence.
- **Missing B-alt pre-committed downgrade wording (guidance.md §3.3):** the B-alt arm stated a survive/not-survive criterion but no verbatim downgrade sentence. Added, distinguishing what a null result would and would not refute (CO1/CO3 fall; CO2/CO4 may still stand on the catalog-free arm's own numbers) — this reasoning already existed in `pipeline.md`'s Stage 6 critic/refiner discussion but had never been carried into `paper.md` itself, the document Phase A actually gates on.

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 A2 evidence standard) — **REVISE → fixed, 1 advisory**

- Item 1 (estimand in one sentence, R1) — **missing → fixed**: added an explicit two-part estimand paragraph to Step 5 (one sentence per RQ's measured quantity, per the R1 template: quantity / unit of analysis / reference population / decision it feeds).
- Item 8 (≥1 mechanism analysis budgeted, R6) — **missing → fixed**: added an explicit "Mechanism analysis (R6)" sub-plan to RQ2 (cross-tabulate violations against agent-system identity and patch size, to distinguish a genuine compliance gap from an exposure-opportunity confound).
- Item 9 (power stated per cell; thin cells pre-declared INCONCLUSIVE) — **missing → fixed**: added an explicit per-repo×category power/thin-cell rule to RQ2 (n<20 ⇒ INCONCLUSIVE for that stratum, never pooled silently).
- Item 7 (every design constraint names its confound, R3) — judged **adequately met in substance** (e.g., the ≥3-thread support threshold's stated rationale already names the confound it removes — one-off reviewer idiosyncrasy — even though it doesn't use the rigid "constraint X removes confound Y" phrasing); not treated as blocking.
- Items 2–6, 10 — **PASS** (verb check already passed at Step 3; H\*/A\* completeness now closed by item 5's fixes; archetype named and, with the above fixes, the A2 evidence standard — validated instrument + controlled comparison + effect-floored pre-registered tests + rival-explanation ablation (B-alt) + ≥1 mechanism analysis — is now met by the plan, not merely intended).
- **Advisory, non-blocking:** guidance.md's R2 rigor recipe states "κ ≥ 0.7 required" for instrument validation, while `paper.md`'s RQ2 judge-validity gate pre-registers κ≥0.6. 0.6 still falls in Landis–Koch's "substantial agreement" band and is used consistently across `digest.md`, `paper.md`, `pipeline.md`'s Stage 6 table, and the already-produced `paper_draft.md/.tex/.pdf`. Bumping it now would either leave those Phase E/F artifacts inconsistent with a Phase-A-only edit, or require touching documents outside this task's scope (no Phase B/C or draft-revision work was authorized). Flagged for the next run's owner to decide explicitly rather than silently changed either way.

### 7. Stage cross-check (advisory) — **PASS**

Already covered by the existing `pengsida-stage-reviewer` Stage 1–5 pass above and by `pipeline.md`'s own "Cross-stage consistency check" section (reference integrity, id stability, output coverage, `study_type` consistency all checked there). The one new fact since that pass — the added method-twin `2512.23844` — was inserted at N3/N4 only and does not disturb N1/N6/N8's existing cross-references; no new REVISE items surfaced.

### 8. Taste audit currency — **PASS, no re-audit needed**

None of this pass's fixes altered the Step 0 asymmetry sentence or Step 5's formal definitions in substance (all additions are elaborations — fallback sentences, effect floors, gate/consequence labels, a power rule, a mechanism-analysis plan, an estimand paragraph, and a downgrade sentence). Per goal.md §3 item 8's trigger condition, the recorded `taste_audit.md` remains current.

### Overall Phase A (re-run) gate: **PASS**

All 8 checklist items clear after the fixes above (one advisory note on the κ=0.6 vs. κ≥0.7 threshold, one residual non-blocking cache-completeness item for 5 method-twin entries lacking a local PDF/digest — both logged, neither blocks Phase B). No Phase B/C work was performed or attempted, per this task's scope.
