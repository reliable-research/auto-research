# Pengsida Stage Review — B4.4

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1, 3, and 4 below were checked against the confirmed `pipeline.md` stage outputs and cross-checked against the first assembled draft's prose; Stage 2 and Stage 5 were checked directly against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding** (secondary: Resource/Instrument for the harness). Per `archetypes.md`'s tells: the core question is "we ask whether a near-zero-cost signal matches an existing one" with no new controller mechanism proposed as a fix — the probe itself is a standard technique per `[DiffAdapt]`/`[AdaptiveThinking]`, and the matched-budget simulator (recycled-label pipeline, dual-cost router, transfer design, self-report safeguard, decision-quality isolation) is the *analytical apparatus* that makes the comparison priced and fair, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification, `paper.md` Step 2's explicit "no new controller mechanism is proposed," and Stage 1's `study_type: empirical`. N12 also explicitly checked and rejected promoting the harness to a `benchmark`/Resource-primary framing, so Resource stays secondary, not dominant. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "no prior comparison charges every controller's own signal-acquisition cost against the same budget it is trying to save" is a first-principles framing (an accounting gap, not a patch), and the stakes are stated concretely: "every deployed system currently paying for self-report or self-consistency sampling is paying a real, avoidable dollar cost for a decision a probe could make for free — and if it doesn't, that is equally decision-relevant." This is a genuine two-sided stake, not a one-directional hope. The Einstein ratio holds: the first two Introduction paragraphs are pure problem/stakes, with zero method leak — "the controller stops being a budget item at all" appears before any mention of how the probe, router, or safeguards actually work.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g., "[DiffAdapt/AdaptiveThinking/KV-Embeddings]... none of them benchmarks that signal against self-report or training-free signals under one matched dollar budget... their headline currency is token savings, not accuracy-per-dollar"), which clears the "citation dump" failure mode. But the first assembled draft's Related Work section opened directly with the "Frozen-feature probing" thematic paragraph, with no single sentence stating up front which prior work is the *closest* competitor before the four threads began. Digest N4's own limitation-1 entry already does this work implicitly ("DiffAdapt and AdaptiveThinking... neither benchmarks the probe head-to-head against large-model self-reported confidence"), but that ranking never surfaced as an explicit opening sentence in the assembled prose. A reviewer reading only the four parallel threads has to infer for themselves which one is the nearest neighbor — per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming DiffAdapt and AdaptiveThinking as the closest prior work and stating the precise delta, before the four thematic paragraphs begin, rather than leaving the reader to rank the threads themselves. The current Related Work section now opens: *"The closest prior work to this paper is DiffAdapt and AdaptiveThinking, and it is worth stating the delta plainly before surveying the wider landscape: both already train a lightweight probe on a frozen backbone's post-prefill hidden state to make a compute-allocation decision, but neither puts that probe head-to-head against large-model self-report, and neither reports a matched-dollar-budget frame..."* The same nearest-neighbor sentence was also added to the Introduction's survey paragraph so the framing is consistent across sections, not confined to one.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the controller/signal/acquisition-cost notation, the matched-budget threshold rule, and the cost-free AUROC contrast are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: "a benign budget-arithmetic win moves the matched-budget ranking without necessarily moving a budget-independent signal-quality ranking; requiring the two to agree in direction is exactly the condition that separates 'the probe makes better decisions' from 'the probe is just cheaper'" — this is exactly the step that makes the cost-free decision-quality isolation module non-redundant with the matched-budget router, and the draft states it explicitly rather than asserting the isolation by fiat. No orphan components — every one of the five modules (recycled-label pipeline, dual-cost router, transfer design, self-report safeguard, decision-quality isolation) traces to a named sub-problem in `pipeline.md`, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ6 is a genuine falsification design (checking whether a matched-budget win survives a budget-independent AUROC contrast, not just correlating the two), and RQ5 is likewise a genuine load-bearing test (recomputing the RQ2 verdict with each self-report variant alone to see if the verdict *changes*, not just noting that variants differ). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... at ≥2 of the 5 points on each benchmark" without ever stating, as its own labeled line, what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `pipeline.md`/original `paper.md` material already had this discipline (the Step 6 "Fallback" clauses and N9's own `FALSIFICATION CONDITION` fields) that didn't survive into the first assembled `paper_draft.md`'s RQ subsections.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s Step 6 fallbacks and digest N9's per-RQ falsification fields). For example, RQ2 now reads: *"**Falsification condition.** Refuted toward self-report if McNemar rejects in self-report's favor, BH-corrected, at a majority of the 10 cells... If refuted, the fallback claim becomes a cost-crossover characterization..."* — distinct from, and more specific than, the "Expected outcome" line above it.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Large language models increasingly spend a variable amount of test-time compute per query..." / "Yet the controller signal is rarely free..." / "The nearest existing work already builds exactly this probe..." / "Turning 'is the probe as good as self-report' into an answerable question surfaces several difficulties of its own..." / "Our approach turns each of these obstacles into a specific design choice rather than a hedge..." / "We evaluate this design on exact-answer reasoning benchmarks...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and Introduction: "a signal itself must be paid for out of the same budget it is trying to protect" / the title's "Paid From the Same Budget It Spends." The Conclusion names two real forward-looking limitations (model-choice/agentic scope, and the transfer gap possibly forcing per-backbone retraining rather than a universal probe) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening (and echoed it in the Introduction's survey paragraph), naming DiffAdapt and AdaptiveThinking as the closest prior work and stating the delta plainly, rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), distinct from and more specific than the "Expected outcome" line, then compiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — goal.md §3 checklist, 2026-07-04

> This is the `goal.md`-defined Phase A gate (distinct from the `auto-research-discussion` /
> `pengsida-stage-reviewer` review above, which ran earlier and is preserved unedited). Run
> against `README.md`, `digest.md`, `paper.md`, and the newly upgraded
> `discussion/reference_candidates.jsonl` (canonical schema, 160 records: 150 harvested + 10
> added — see below). No Phase B/C compute exists in this environment; this run stops at the
> Phase A gate per the task's own scope.

**1. Digest self-verification — PASS.** All of N0–N12 + Claims are present in `digest.md`. Every
non-`[GIVEN]` node carries a 3-part `absence_comment` (`what_missing` / `why_matters` /
`implication`); spot-checked N1, N5, N6, N9, N10, N11. Cross-node references resolve: N4's
`affects_works` entries match N3's `citation_key` strings verbatim (digest.md's own
`grounding_check: true`, independently re-verified by diffing the two lists). No untagged
assertions found in N0–N12 or Claims.

**2. Reference-cache integrity — REVISE, fixed.** Before this run, `discussion/reference_candidates.jsonl`
held 150 harvested candidates (110 arXiv + 40 ACL-2023) in the old ad hoc schema, with **zero**
of digest.md N3's 10 citation keys present at all — a hard fail of "every N3 key is a `selected`
cache record." Root cause: N3 was built from a *separate* corpus search (`topics/corpus/ideas.jsonl`,
5 query angles) that was never folded back into the harvested cache; the 150-candidate harvest is
a broad embedding-similarity pull that happens to miss the paper's own closest prior work entirely.
**Fix applied (Task 1 of this run):** rewrote all 150 records into the canonical schema with
selected/rejected verdicts (7 of 150 selected — see below), then **added digest.md's 10 N3
citation keys as new cache records** (DiffAdapt, AdaptiveThinking, CaTS, DiSRouter, TRIM,
LimitedMetacognition, KV-Embeddings, TPC, RouterArena, Kadavath et al. 2022), each `verdict:
selected` with a `relevance` tag matching its role in N3/N4 (2 `method-twin`, 3 `contrast`, 4
`adjacent`, 1 `baseline`). Since no PDF is cached locally for these OpenReview-submission-only
papers (or for Kadavath, arXiv:2207.05221 — not in the local arXiv mirror), `pdf_path` stays
`null` and `verified.id_resolves` is honestly `false` for these 10; but each now has a
**resolvable `digest_path`** — a minimal N2/N6 stub digest built from `openview_corpus/ideas.jsonl`'s
own `proposal.motivation`/`proposal.method` text (the same source digest.md's own N3 quotes),
written under `discussion/refs_n3_digests/`. Spot-checked 3 ids by opening the cached PDFs directly
(`2512.24661`, `2512.22364`, `acl_chen-etal-2023-close`) — all resolve, titles match. **No `pending`
entries exist anywhere in the cache (0 of 160).** Cache is now 160 records: 17 `selected` (7 from
the 150-candidate harvest + 10 added), 143 `rejected`, 0 `pending`.
*Residual note (not blocking):* the 10 added N3 records have no cached PDF, only a corpus-grounded
motivation/method stub — if this topic proceeds to Phase E, a freshness/PDF-acquisition pass on
these 10 (real OpenReview submissions) should happen before `refs.bib` generation, per goal.md's
own "freshness sweep before Phase E" hard gate.

**3. Tag discipline — PASS.** No untagged assertions found; no silent `[HYPOTHESIS]→[GIVEN]`
promotion anywhere in `digest.md` (checked N2, N6, N9 in particular, where the temptation to
promote a predicted result to a stated fact is highest — `N9`'s results are correctly marked
`[HYPOTHESIZED DIRECTION]` with `evidence_strength="missing"` throughout).

**4. Claim–Evidence Map completeness — PASS.** All 8 rows in `paper.md`'s Claim–Evidence Map trace
to either an H-id (H1/H2/H3) or a `supported-by-design` Step-5/Step-0 definition; no orphans in
either direction. Every H-id has both its own individual fallback (F1/F2/F3, written inline as
"Fallback (if H\* fails)") **and** global-pivot coverage (F-G1, for the H1∧H2 central-family
collapse case).

**5. Hypothesis/assumption machinery — REVISE, fixed.** guidance.md §3.1 requires every H\* to
carry an **effect floor** ("significance without magnitude passes nothing"). H2 and H3 had one
(H2: >2pp margin with CI excluding 0; H3: ≥ the training-free baseline); **H1 did not** — its
"strictly superior" clause was pure statistical significance (McNemar rejects) with no minimum
practical-magnitude requirement, so a significant-but-clinically-negligible (e.g. 0.1pp) win would
have counted toward the ≥2-of-5 tally. **Fixed directly in `paper.md`** (Step 6, RQ1/H1): added an
explicit ≥1pp effect-floor requirement (paired-bootstrap CI excludes 0 *and* point estimate ≥1pp)
to the superiority clause, and a symmetric ±1pp practical-equivalence margin to the non-inferiority
clause, citing guidance.md §3.1. Separately, guidance.md §3.2 requires every A\* to state
`failure_mode`, `detection`, `gate`, **and `consequence`** (what happens to which H\* if the
assumption fails — degrade/restrict/block); A1–A5 had `failure_mode`/`detection`/(informal) `gate`
but **no `consequence` field at all**. **Fixed directly in `paper.md`** (Assumptions section): added
an explicit "*Consequence if it fails:*" clause to each of A1–A5, naming the specific H\* affected
and whether the assumption's failure blocks, degrades, or restricts scope (e.g. A4's failure now
explicitly blocks H1 and H3 and reframes H2; A3's failure now explicitly degrades H1/H2 to
per-cost-model reporting rather than blocking them). B0 + B-alt + F-G1 are all present with
pre-committed wording (already PASS, unchanged).

**6. Method-rigor audit — REVISE, fixed.** guidance.md Part 6 items checked against the declared
A2 (Empirical measurement / controlled comparison) archetype:
- Item 1 (R1 estimand, one sentence) — **was missing** (no line in `paper.md` was ever labeled an
  estimand); **fixed** by adding an explicit "Estimand (R1, guidance.md §3.4)" sentence at the top
  of Step 5, reusing the already-correct `pipeline.md` Stage-1 `formal_summary` framing.
- Item 2 (verb check) — PASS, already handled in `paper.md` Step 3.
- Item 3 (H\* seven slots incl. effect floor) — REVISE→fixed, see item 5 above.
- Item 4 (A\* detection + gate) — detection present for all five; gate was explicit only for A4/A5
  (and implicit for A1); **tightened** by naming `PG-1..PG-5` explicitly in the fix applied under
  item 5.
- Item 5 (B0/B-alt/F-G\*) — PASS.
- Item 6 (R2 instrument validation, 5-step + threshold) — **not applicable**, and now says so
  explicitly: this design has no subjective rubric/LLM-judge (all ground truth is programmatic
  exact/option-match); added a clarifying note to `paper.md`'s Assumptions section so this isn't
  read as a silent omission.
- Item 7 (R3, every design constraint names its confound) — **was implicit only** (the confounds
  were addressed mechanically — dual cost model, disjoint splits, B-alt — but never named as
  "constraint X removes confound Y"); **fixed** by adding a "Design constraints → confounds
  removed" list (5 entries) to `paper.md` after the Assumptions section.
- Item 8 (≥1 mechanism analysis) — PASS: the cost-free AUROC-vs-self-report contrast (B-alt) is
  the mechanism-layer analysis separating "cheaper signal" from "better decisions."
- Item 9 (power per cell; thin cells pre-declared INCONCLUSIVE) — **was missing for H2/H3** (only
  H1's primary McNemar test had a stated power; no thin-cell INCONCLUSIVE rule existed anywhere,
  despite guidance.md Part 4 situation 5 requiring one); **fixed** by adding a "Power and
  thin-cell pre-declaration" subsection to `paper.md` Step 6 covering all three H\*, with concrete
  per-hypothesis thin-cell thresholds (30 discordant pairs for H2; n=200 routed-expensive-tier
  queries for H3) and the general INCONCLUSIVE-never-null-never-silently-dropped rule.
- Item 10 (archetype named + Part 2 evidence standard met) — archetype is named (`paper.md` Step 2:
  "Empirical measurement / controlled comparison", i.e. guidance.md A2) and, after the item-9 fix,
  the plan now meets A2's full evidence standard (validated-instrument-equivalent via A1/A4 +
  controlled comparison via R3 confound list + effect-floored pre-registered tests via R4 (H1 fix)
  + rival-explanation ablations via B-alt (R5) + ≥1 mechanism analysis (R6)). **Advisory
  cross-document note:** the earlier `pengsida-stage-reviewer` pass above (this file, Stage 3/4
  section) labels the archetype **"Analysis/Finding"** using its own (`archetypes.md`) taxonomy,
  while `paper.md` Step 2 and `digest.md` N12 both say **"empirical"** in guidance.md's Part 2
  taxonomy (which has a *distinct* A2 "Empirical/measurement" category from A4
  "Analysis/understanding" — this paper is a matched-budget *comparison*, not a mechanism
  explanation for a known phenomenon, so A2 is the correct guidance.md-native label). The two
  labels come from two different reviewers' taxonomies and are not in conflict, but a future
  reader should treat `paper.md`'s own guidance.md-Part-2 self-classification (A2) as authoritative
  for any guidance.md-referencing check (including this one), not the other skill's label.

**7. Stage cross-check (advisory) — already satisfied, no action.** The
`pengsida-stage-reviewer` cross-check (N1↔Stage1, N3/N4↔Stage2, N6↔Stage3, N8/E\*↔Stage4) was
already run in full above, with its 2 REVISE findings already fixed in `paper_draft.md`/`.tex`
(nearest-neighbor sentence in Related Work; per-RQ falsification conditions in Experiments). No
new STOP or REVISE surfaced on re-inspection.

**8. Taste audit currency — PASS, no re-audit needed.** `taste_audit.md` is dated to the same run
as the current `paper.md`/`paper_draft.*`, and none of this Phase A run's fixes touch the asymmetry
statement (Step 0) or the formal definition (Step 5's notation/table) — only the Assumptions
section, Step 6 hypothesis/power text, and a new Step-5 estimand sentence that restates (does not
change) the already-audited estimand. No material edit to the audited surface; the 🟢 "reads as
human-shaped" verdict stands.

### Phase A gate result: **REVISE-then-PASS (fixes applied in this run; gate now clears)**

Items 2, 5, and 6 fired REVISE; all three were fixed directly in `paper.md` (and cache-side, in
`reference_candidates.jsonl` + new `refs_n3_digests/` stubs) during this same run, per goal.md's
instruction that Phase A REVISE findings on static documents are fixed immediately, not merely
logged. No item fired STOP. Phase B/C are out of scope for this run (no real experiment compute
exists in this environment) — the bundle is now clear to proceed to Phase B (walking skeleton)
whenever real compute is available.
