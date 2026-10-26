# Pengsida Stage Review — B3.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask which of several existing behavioral axes actually governs a phenomenon (downstream breakage)" with no new detector or system being pitted against baselines to win — the five-module apparatus (joint regression, functional ground truth, attrition gate, partial attribution, noise/paraphrase gate) is the *analytical instrument* that makes the phenomenon measurable, not a method competing to beat a number. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "a probe is only useful if the axis it measures is the axis that actually governs whether a downstream integration breaks, and that is not something teams currently have any evidence for" is a first-principles framing (the root asymmetry paper.md calls axis-selective, not magnitude-selective breakage), not a generic "AI moves fast" appeal. The stakes are concrete and practitioner-facing (a team re-testing the wrong axis gets a false sense of having audited the update), and the motivation's refiner pass explicitly closes the "why does *minimal* matter, not just the ranking" gap with a cadence/scale argument rather than leaving output (3) unmotivated. The Einstein ratio holds: Introduction paragraphs 1-2 are pure problem/stakes, with zero method leak (no mention of regression, partial correlation, or gating until paragraph 5).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The three thematic paragraphs (benchmark compression, single-axis instruments, instrument brittleness/training-side view) were genuinely threaded — each ends on a problem-tied limitation, not a generic one (e.g., the single-axis-instruments paragraph originally closed with "...none is compared against another axis... across a version pair," which clears the "citation dump" failure mode). But the section, as first assembled, opened straight into the "Benchmark compression" paragraph without ever stating, in one place, which single prior work is the *closest* competitor. Digest N4's own absence_comment already names the gap precisely — "no single corpus paper administers a multi-family probe battery compared retrospectively against real downstream-task breakage" — and `BiasSimilarity-BSM` is the one cited work that gets closest (a cross-*release* black-box behavioral audit), but that ranking never made it into the assembled prose. A reviewer reading only the three thematic paragraphs would have to infer for themselves which of the eight works is the nearest neighbor; per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming the cross-release behavioral-similarity audit (`BiasSimilarity-BSM`) as the closest prior work and stating the precise delta (audits one construct at a time, never connects departure to downstream breakage, never compares across axes), rather than leaving the reader to rank three parallel threads themselves. This is now the opening paragraph of the Related Work section in `paper_draft.md`/`.tex`, ahead of the three thematic paragraphs.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — drift magnitude D_f(p), downstream breakage B(p,t), predictive power π_f, and the minimal-sufficient subset criterion are all given in Problem Definition ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: the Collinearity-Aware Partial Attribution module's own stated insight — "a family's own marginal contribution is only visible once the variance it shares with the other four is accounted for; a raw pairwise correlation... cannot distinguish a family's independent signal from a collinear echo" — is exactly the step that makes RQ5 (partial vs. raw rank disagreement) non-redundant with RQ1's joint-regression coefficients, and the draft states this explicitly rather than asserting the disentanglement by fiat. No orphan components — every one of the five modules (joint regression, functional ground truth, attrition gate, partial attribution, noise/paraphrase gate) traces to a named sub-problem in `pipeline.md` Stage 4, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ4 is a genuine falsification design (directly testing whether attrited pairs differ from retained ones, rather than assuming the retrospective corpus is unbiased), and RQ5's raw-vs-partial rank comparison is exactly the test that would fail to fire if collinearity were negligible. But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... the 95% confidence interval on the top-family-minus-capability coefficient difference lies strictly above zero" without ever stating, as its own labeled line, what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as an explicit, quotable check — not left for the reader to derive by negating the expected outcome themselves. The underlying `pipeline.md`/`paper.md` material already had this discipline (`paper.md`'s own Step 6 "Fallback" clauses for RQ1/RQ_INF_1/RQ_INF_2) that did not survive into the first assembled `paper_draft.md`'s RQ subsections.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — not a bare negation of the outcome, but the concrete statistical condition and, where relevant, what that refutation would imply for the paper's premise (mirroring the rigor already present in the pre-existing `paper.md`'s Step 6 Fallback clauses, e.g. RQ2's falsification line explicitly connects a null result back to the B0 baseline check in the Experimental Setup).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Large language model providers ship new versions routinely..." / "Yet a central question about this practice remains unexamined..." / "The nearest existing work to this gap is a black-box audit..." / "Turning this gap into a measurable question surfaces genuine difficulties." / "This paper turns each of those obstacles into a specific design decision." / "We evaluate this design on retrospective version pairs...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and the first contribution bullet: breakage is governed by which axis drifted, not by how much the model changed overall — "axis-selective, not magnitude-selective." The Conclusion names a real forward-looking limitation (RQ5 may reveal an inseparably collinear bundle rather than a single governing axis) rather than only recapping the abstract, and explicitly frames that outcome as "a real possible outcome this design is built to detect and report, not to explain away" — satisfying the archetype's honest-null-result standard for an empirical/finding paper.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor paragraph at the top of the Related Work section, naming the cross-release behavioral-similarity audit (`BiasSimilarity-BSM`) as the closest prior work and stating the delta plainly (single-construct, single-time-point, never connected to downstream breakage), ahead of the three thematic paragraphs.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per goal.md §3's checklist (items 1–8), against `README.md`/`digest.md`/`paper.md` as they stand after the reference-cache upgrade (Task 1, below) and the `paper.md` fixes made in this pass. Standard = guidance.md, cited by section per item. No Phase B/C compute exists in this environment — this run stops at the Phase A gate as instructed; nothing past bundle validation was touched.

**Reference-cache upgrade context (prerequisite for items 2 and 6):** `discussion/reference_candidates.jsonl` was rewritten from the flat harvest schema (150 candidates: 110 arXiv + 40 OpenReview/ACL-Anthology) into goal.md §1's canonical schema. Every candidate's `digest_path` was read and classified per guidance.md Part 5; **9 of 150** selected (`ElicitBehaviorsMultiTurn3701`, `AdversarialPragmatics1153`, `EvaluatorPrefDynamics0297` — adjacent; `CapableOf4661`, `PrincipalLoyalty0383`, `CondGenBench0511`, `PLMCalib9999` — background structural exemplars; `CausalRobust6745`, `CompressFair0878` — adjacent), **141 rejected** with a specific one-sentence `why` each (no generic "not relevant"). Additionally, **8 records were backfilled** for the works `digest.md`'s N3 already cites (`EssenceBench2607`, `BiasSimBSM2607`, `RefusalIndex2607`, `OffTopicEval2607`, `BCalibration2607`, `TARE2607`, `WeightDiff2607`, `ProSafePrune2607`) — these were grounded via a separate corpus (`topics/corpus/ideas.jsonl`, confirmed present and title-matching by direct lookup) rather than via this topic's own 150-candidate harvest, so they were never in the cache at all before this pass. All 8 are marked `verified.id_resolves: false` (no local `pdf_path`; honestly reported, not treated as "pending" — a resolvable OpenReview id + url is on record and was locally spot-checked against `topics/corpus/ideas.jsonl`). Final cache: **158 records, 17 selected, 141 rejected, 0 pending.**

### Item 1 — Digest self-verification (goal.md §3.1)
**PASS.** Independently re-checked (not just trusting `digest.md`'s own self-verification pass): N0–N12 + Claims all present; `N4.affects_works` strings all resolve into `N3`'s 8 citation keys; `N6.challenge_arguments[].challenge_id ∈ {C1..C5}` and `mechanism_components ⊆ {M1..M7}` all valid; `N8` RQs' `addresses_challenges/tests_contributions/evaluates_mechanisms` all resolve into `{C1..C5}/{CO1..CO3}/{M1..M7}`; `N9.results[].rq_id ∈ {RQ1, RQ_INF_1, RQ_INF_2}` matches `N8` exactly. **Note on absence-comment coverage:** goal.md §3.1 says "every non-GIVEN item carries its 3-part absence comment"; `digest.md` instead applies its own documented, internally-consistent convention (stated in its header and its own V-02 self-check) of attaching `absence_comment` to non-**FOUND**-status *nodes* only (N0 partial, N9/N10/N11 not-found) rather than to every `[HYPOTHESIS]`-tagged field — reasonable for reverse-digest mode (goal.md §9's standing TODO already flags that this tag scheme isn't yet formally documented in `paper-digest`) and applied consistently throughout, so not treated as a defect.

### Item 2 — Reference-cache integrity (goal.md §3.2)
**REVISE — fired and fixed.** Before this pass, **zero** of `N3`'s 8 cited keys existed in `reference_candidates.jsonl` (the file only held the 150-candidate generic harvest, wholly disjoint from the corpus `digest.md` N3 actually used). This is a genuine goal.md §1-lifecycle violation: N3 must cite only `selected` cache records, and there were none to cite. **Fix:** backfilled all 8 as `selected` records (see above); spot-checked 3 of the 8 ids (`lZlZjSxdio`, `9gJBhkLRat`, `EcIyiJrajc`) directly against `topics/corpus/ideas.jsonl` and confirmed matching `paper_id`/`paper_title`/`paper_url`. No `pending` entries anywhere in the final 158-record cache.

### Item 3 — Tag discipline (goal.md §3.3)
**PASS.** Every assertion in `digest.md` carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`; no silent HYPOTHESIS→GIVEN promotion found. `paper.md`'s Step 0 Invariant and Abstract v0 are stated in confident pre-registration voice, but both are explicitly labeled as pre-results drafts ("no numbers are observed") — this is the correct voice for a pre-registered spec, not a promotion.

### Item 4 — Claim–Evidence Map completeness (goal.md §3.4)
**REVISE — fired and fixed.** Cross-referencing `pipeline.md`'s Stage 4–6 auto-research-discussion output against `paper.md`'s Step 6 surfaced an orphan-claim risk: `pipeline.md` Stage 6 formalized **6** mechanism-tier hypotheses (`rq_axis_top_family`, `rq_any_family_signal`, `rq_downstream_heterogeneity`, `rq_corpus_attrition_bias`, `rq_family_collinearity_partial`, `rq_noise_paraphrase_gate`), and `stage_review.md`'s own Stage 4 review above already refers to "six RQ subsections" in `paper_draft.tex` — but `paper.md`'s own pre-registered Step 6 formalized only **3** (`RQ1`/H1, `RQ_INF_1`/H2, `RQ_INF_2`/H3). `pipeline.md` line 231 itself flags this: "corpus-attrition bias and family-collinearity rank-disagreement are exactly this: claims `paper.md`'s own Assumptions section (A4, A6) gestures at but never states as its own falsifiable hypotheses." That means `paper_draft.tex` was already asserting claims not licensed by `paper.md`'s Claim–Evidence Map — precisely the "stale/unlicensed claim" risk goal.md's hard gates warn about. **Fix:** added **H4** (task-heterogeneity, RQ4), **H5** (corpus-attrition non-bias, RQ5), and **H6** (raw-vs-partial-correlation rank disagreement — also the R6 mechanism analysis, RQ6) to `paper.md` Step 6, each with the full guidance.md §3.1 template, and added Claim–Evidence Map rows 7–9. `rq_any_family_signal` was left unformalized-as-a-separate-H-id since it is already exactly what the **B0** control tests (no new gap). Every claim now traces to an H-id or a Step-5 definition; no orphans.

### Item 5 — Hypothesis/assumption machinery (guidance.md §3.1/§3.2, goal.md §3.5)
**REVISE — fired and fixed.** (a) H1 and H2 were missing an explicit `aggregation` slot (guidance.md §3.1's 7th slot) — content existed in prose but wasn't distinguishable from a "vote rule" concept; added explicit **Aggregation:** lines to H1, H2, and (labeling what was already implicit) H3. (b) None of A1–A7 had the guidance.md §3.2 `gate: PG-j` / `consequence:` labels — only `Fail:`/`Detect:` were present. Added explicit `Gate:` (mapping each to PG-1/PG-2/PG-3 walking-skeleton checks or the specific later phase that checks it) and `Consequence:` (which H* degrades/narrows) to every A1–A7. (c) B0 + B-alt + F-G1 were already present with pre-committed verbatim wording — no fix needed there.

### Item 6 — Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 A2 evidence standard)
**REVISE — fired and fixed.** Checked against guidance.md's rigor recipes (§3.4 R1–R8) and Part 6's 10-item self-check:
- **R1 (estimand)** — missing a one-sentence estimand statement; added to the top of Step 5.
- **R2 (instrument validation)** — `A3`'s construct-validity check named a validation activity ("human adjudication on a labeled subset") but not the full 5-step sequence or an acceptance threshold; added the complete R2 sequence (ground → draft-wide-refine → validate against ≥2 raters at **κ ≥ 0.7** → confusion-structure check → freeze) to `A3`, with the guidance.md Part 4 situation-7 fallback if κ < 0.7.
- **R3 (confound-removal one-liners)** — no explicit "constraint X removes confound Y" ledger existed; added one, covering all 6 major design constraints (A1's open-weight anchor, A2's fixed-decoding null, B-alt, B0, per-task `B(p,t)` scoring, M7's joint regression).
- **R6 (mechanism analysis)** — no analysis explicitly labeled as the required ≥1 mechanism-layer analysis for the A2 archetype; added an explicit paragraph identifying the raw-π-vs-partial-β comparison (now formalized as H6/RQ6) as this study's R6 mechanism analysis.
- **R8 (honest scale) / Part 4 situation 5 (under-powered cells)** — no per-cell power floor or INCONCLUSIVE pre-declaration existed anywhere; added a concrete rule to `A6` (≥50 valid downstream inputs per cell, else INCONCLUSIVE, excluded from headline `n`, reported in a supplementary thin-cell table; same INCONCLUSIVE-not-FAIL treatment at the family level).
- Items 2 (verb check), 5 (B0/B-alt/F-G*), 9 (now fixed, see R8 above), 10 (archetype+evidence-standard match) were already PASS or are PASS after the above fixes; the Part 2 A2 evidence standard (validated instrument + controlled comparison + pre-registered floors + rival-explanation ablations + ≥1 mechanism analysis) is now met by the plan, not just intended.

### Item 7 — Stage cross-check (advisory; goal.md §3.7)
**PASS, with an advisory note logged.** The `pengsida-stage-reviewer` cross-check (N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E*↔Stage 4) holds under the corrected reference cache and expanded H-set. Advisory: this Phase A pass is running *after* Phases B–H's artifacts already exist on disk (`paper_draft.md/.tex/.pdf`), which is out of the normal phase order — goal.md's resumability rule (read `pipeline.md`, resume at the first non-`passed` gate) was not followed by whatever produced those artifacts. This Phase A re-run only validates/fixes `README.md`/`digest.md`/`paper.md` (Phase A's actual read scope) and does not edit `paper_draft.*`; the H4–H6 formalization brings `paper.md` into agreement with what `paper_draft.tex` already assumed, but no attempt was made to re-verify `paper_draft.tex` prose against the now-updated `paper.md` (that is Phase E/G territory, outside this run's mandate, which stops at the Phase A gate per instruction).

### Item 8 — Taste-audit currency (goal.md §3.8)
**PASS — no re-audit needed.** `taste_audit.md`'s own Method summary (§1) already describes VIF-checked partial-correlation disentanglement and the corpus-attrition reachability test as part of the method, so the H4–H6 formalization in `paper.md` is a **pre-registration catch-up to already-audited content**, not a new framing. The asymmetry statement (Step 0) and the Step 5 term→definition→measurement table were not altered (only prefaced with an Estimand line) — no material edit to the audited framing occurred, so `taste_audit.md` remains current.

### Phase A gate result: **PASS** (after the REVISE fixes above were applied in this same pass — items 2, 4, 5, 6 fired REVISE and were fixed directly in `paper.md`/the reference cache; items 1, 3, 7, 8 were clean). Bundle is ready for Phase B under the usual proviso that no real compute exists in this environment to execute it.
