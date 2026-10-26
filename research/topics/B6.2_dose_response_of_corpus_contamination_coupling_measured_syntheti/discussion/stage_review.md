# Pengsida Stage Review — B6.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟡, fixed) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs, and with what shape" with no new pipeline proposed as a fix for anything — the testbed (matched-corpus harness, paired-metric battery, curve-adjudication criterion, detector-coupling module) is the *analytical apparatus* that makes the dose-response phenomenon observable and its shape adjudicable, not a method being pitted against baselines to win. This matches digest N12's own explicit `empirical` classification ("what N9 would validate is a set of measured dose-response curves and statistical verdicts... no new system, dataset, or benchmark is the headline contribution") and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. The confirmed Stage 1/2 material states the stakes concretely, not as a generic AI-importance appeal: "a curation policy calibrated on detector output could be silently miscalibrated in a specific, predictable direction — not just noisy." This is a first-principles framing (the gap is that no measured dose-response law exists at LM scale at all, not that an existing one is merely imprecise), and the Stage 2 refiner's extension closes what would otherwise be a real "so what" gap — a reader could ask "why not just check fairness once at one metric," and the confirmed motivation answers this directly: a threshold calibrated on one endpoint is only actionable if it holds for what curators actually ship, and diversity/tail behavior may erode before capability metrics move. No method leak: the Stage 1 `constraints`/`objective` fields name requirements (exogenous dose, fixed budget, distribution-matched pools) not techniques.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs in the first assembled `paper_draft.md` are genuinely threaded — each ends on a problem-tied limitation, e.g. "DoReMi... establishes that mixture proportions causally and transferably affect language-model quality, but its mixture axis is human-domain weights, with no synthetic-vs-human axis and no degradation endpoint" — which clears the "citation dump" failure mode. But the section, as first assembled, never states in one place which single prior work is the *closest* competitor before surveying the wider landscape. Digest N3 itself already did this ranking work explicitly — item 1 in N3's `works` list is annotated "the closest existing 'dose-response of mixing ratio' result, but purely theoretical and in regression, not LM training" — but that explicit ranking never made it into the assembled Related Work prose; a reader saw four parallel threads (mixing-ratio theory, extreme-dose collapse, benefit-framed synthetic data, detection) and had to infer for themselves which one is the nearest neighbor. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section, naming `[PreventCollapseMixing, OpenReview:9RdhTvYbX0]` as the closest prior work (per digest N3's own annotation) and stating the precise delta — theoretical/regression vs. empirical/LM-scale — rather than leaving the reader to rank the four threads themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used. The standardized deviation Δm(ρ), the primary-endpoint convention, the four candidate curve families, and the TOST-based "harmless" definition are all given in Problem Definition/Methodology ahead of any claim that invokes them — no "named after the fact" violation. The inferential chain is licensed at its one load-bearing hinge, stated explicitly rather than asserted by fiat: "small but non-zero effect at low dose" and "true zero effect below a threshold" are statistically adjacent but decision-theoretically opposite claims, and the equivalence-test-plus-model-comparison design is exactly what makes them distinguishable rather than eyeballed. The detector-coupling module's directional prediction is likewise derived, not asserted: Stage 5's refiner pass traced the predicted permissive bias to the shared-cause asymmetry (synthetic text's distributional proximity simultaneously depletes tail mass and raises detector recoverability, with detector sensitivity weakest exactly where the safety threshold question matters most). No orphan components — every one of the five modules (matched-corpus harness, paired-metric battery, curve adjudication, detector coupling, factorial transfer check) traces to a named sub-problem, with no leftover machinery and no sub-problem left unaddressed.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational, and whether the claimed cause (syntheticness) is isolated from its strongest alternative (generic distributional narrowing). Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: `rq_confound_control`'s human-entropy-matched (B-alt) control is a genuine falsification design, constructing a case where, if the "syntheticness specifically" claim were false, the human-low-entropy arm would reproduce the same dose-response curve as the synthetic arm; it is built to potentially refute the paper's own central attribution, not just correlate with it. But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... a soft, resolution-limited safe region rather than a genuine mechanistic threshold" without ever stating the converse — what result would *refute* that expectation and what it would mean if it did. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as an explicit check, not implied by the setup alone. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had exactly this discipline (its per-experiment "Fallback" clauses with pre-committed wording) that did not survive into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all five RQ subsections, stating the specific statistical observation that would refute each expected outcome — not a vague restatement of the outcome's negation, but the concrete condition already present in `paper.md`'s own Fallback wording (e.g., RQ3's falsification condition names the exact alternative: "refuted (order/mechanism does not matter as predicted) if the change-point family instead wins with a significant Davies test — reported as a stronger, different finding, not a failure").

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Language models are trained on web-scraped corpora that increasingly contain text those same models, or their predecessors, wrote" / "Yet no one has actually measured the shape of the relationship between how much synthetic text is present and how much a model degrades" / "The nearest existing account of a dose-response-shaped mixing law comes from a different regime entirely" / "Turning this gap into a measurable question surfaces four distinct difficulties" / "Our approach turns each of these four difficulties into a specific, checkable design choice rather than a hedge" / "We evaluate this design across a staged pilot-then-scale-up protocol") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists, placed at the head of the Conclusion and consistent with the title and abstract's framing: "contamination has a shape, not just a ceiling, and the instrument used to estimate it in practice is itself biased in a specific, predictable direction." The Conclusion names a real forward-looking limitation (the small-model, fixed-backbone proxy's scope, and the fact that the factorial transfer check cannot certify transfer beyond the tested cells) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming `[PreventCollapseMixing, OpenReview:9RdhTvYbX0]` as the closest prior work (per digest N3's own annotation) and stating the delta plainly: a theoretical, regression-scale mixing-ratio optimum vs. this paper's empirical, LM-scale dose-response measurement — rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the five RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), drawn from `paper.md`'s own pre-committed Fallback wording rather than invented fresh, then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Date: 2026-07-04. Scope: goal.md §3's 8-item Phase A checklist run against `README.md`,
> `digest.md`, and `paper.md`, applying `guidance.md` as the rigor standard, **after** the
> `discussion/reference_candidates.jsonl` cache was rebuilt into the canonical schema (goal.md
> §1). This section is a fresh, independent Phase-A pass — distinct from the Stage 1–5 review
> above, which audited the `auto-research-discussion` transcript and the assembled
> `paper_draft.*`, not the canonical Phase-A checklist. Per this run's mandate, **no Phase B/C
> work was attempted** (no real experiment compute exists in this environment); this section
> stops at the Phase A gate.

**Context — the reference cache going into this check:** the topic's harvested
`reference_candidates.jsonl` contained 150 candidates (110 arXiv + 40 ACL-Anthology-labeled
"openview") in the flat ad hoc schema, all still tagged implicitly as unreviewed. Each was
individually skimmed (digest_path, escalating to title-based judgment where the cached digest
was itself template-garbled or PDF-column-scrambled) and rewritten into the canonical schema.
**Result: 3 selected / 147 rejected** out of the 150. The harvest turned out to be near-total
noise for this topic — a broad recency-window arXiv scrape (Dec 2025–Jul 2026) plus a generic
ACL-2023-anthology sample, neither targeted at model collapse / synthetic-contamination /
mixing-ratio query angles. The 3 genuine hits: `CanSmallRunsGuideCuration` (arXiv:2512.24503,
ICLR 2026 — bears directly on threat t1's small-model-proxy risk), `CAUSALMIX1104`
(arXiv:2607.01104 — same limitation class as the already-cited DoReMi, flagged for the
pre-Phase-E freshness sweep), and `IterativeDeploymentImpro4940` (arXiv:2512.24940, co-authored
by Ilia Shumailov — a curation-contingent rival narrative to model collapse). All three are
tagged `relevance: adjacent`; none displace or duplicate an existing N3 entry.

### Checklist

**1. Digest self-verification — REVISE (fixed).** N0–N12 + Claims were all present and
cross-node ids resolved (N5 challenge ids ↔ N6 `challenge_arguments`, N3 `citation_key`s ↔ N4
`affects_works`, N8 RQ `evaluates_mechanisms`/`addresses_challenges`/`tests_contributions` ↔
M*/C*/CO* — all verified by direct grep, no dangling ids found). Gap found: per the reverse-digest
convention in digest.md's own preamble (FOUND≈GIVEN, PARTIAL≈HYPOTHESIS, NOT_FOUND≈PLACEHOLDER),
N0 (authors), N10 (threats), and N11 (artifacts) all carry the required 3-part `absence_comment`,
but **N9 (Results) did not** — it had only a section-level warning banner, not a structured
`{what_missing, why_matters, implication}` object. **Fixed:** added a section-level `status:
PLACEHOLDER` + 3-part `absence_comment` to N9 in `digest.md`, citing goal.md §3 item 1.

**2. Reference-cache integrity — REVISE (partially fixed; one residual gap).** Before this run,
**zero** of digest.md N3's 8 `[GROUNDED:corpus]` citation keys (`PreventCollapseMixing`,
`CloserLookCollapse`, `CuratedSelfConsuming`, `SyntheticCPT`, `DoReMi`, `NotAllLLMData`,
`TrainOnceAnswerAll`, `DandR`) existed anywhere in `reference_candidates.jsonl` — the N3
grounding pipeline (`topics/corpus/ideas.jsonl`, a separate 11,683-entry idea-summary corpus)
and the goal.md-§1 harvest pipeline that produced the 150 candidates were completely disjoint
sets, confirmed by exact-string grep (0 hits for all 8 OpenReview ids). This is exactly the
failure check 2 exists to catch. **Fixed (partial):** added all 8 as `verdict: selected` cache
records (relevance assigned per digest.md's own N3/N4 characterization: `method-twin` for
PreventCollapseMixing/SyntheticCPT/TrainOnceAnswerAll/DandR, `baseline` for DoReMi, `adjacent`
for CloserLookCollapse/CuratedSelfConsuming/NotAllLLMData), each with a `grounding_source`
pointing at its `topics/corpus/ideas.jsonl` record (verified present via exact `paper_id` match)
since no cached PDF exists for OpenReview-submission ids in this environment. **Residual gap
(not fixable in this pass):** all 8 have `pdf_path: null` / `digest_path: null` →
`verified.id_resolves: false` — "load-bearing entries have resolvable digest_path" still fails.
A real re-harvest (fetching these 8 papers' actual PDFs, likely via arXiv mirrors — several of
these OpenReview submissions do have arXiv preprints) is needed before Phase B; this requires
network access this pass did not exercise. Spot-check-by-fetching (the check's third clause)
was likewise not performed for the same reason. **No `pending` entries remain anywhere in the
cache** (158/158 records are `selected` or `rejected`) — that sub-clause passes clean. The two
canonical non-corpus anchors (Shumailov et al. 2024; Gerstgrasser et al. 2024) remain outside
the cache entirely — deliberately not fabricated with guessed arXiv ids in this pass; flagged
for the same future re-harvest.

**3. Tag discipline — PASS.** Every digest.md assertion carries an explicit
`[GIVEN]`/`[HYPOTHESIS]`/`[PLACEHOLDER]`/`[GROUNDED:corpus]` tag; no untagged assertion found;
no [HYPOTHESIS]→[GIVEN] promotion detected (N9's new absence_comment reinforces this rather than
changing any tag).

**4. Claim–Evidence Map completeness — PASS.** All 6 digest Claims trace to an H-id (Claims
1/3/4/6 → H1/H2/H3/composition) or a supported-by-design definition (Claim-2 → Step-5 "isolates"
definition + gates; Claim-5 → explicit non-claim). Every H1–H4 has a fallback (E1–E4) or routes
to F-G1. No orphans in either direction.

**5. Hypothesis/assumption machinery — REVISE (fixed).** H1–H4 each filled all seven
guidance.md §3.1 slots (binary criterion, `applies_if` via the stated Assumption list, metric,
test, alpha, effect floor, aggregation via explicit "succeeds iff" conjunctions, verbatim
fallback) — no gap found here. Gap found in the **A1–A6 assumption ledger** (guidance.md §3.2):
A1, A2, A4, and A5 stated `failure_mode`/`detection`/`gate` but omitted the mandatory
`consequence` slot (which H* is affected and how it degrades) — only A3 and A6 had it, via
incidental phrasing ("routes to F-G1", "making M6/RQ3 vacuous"). **Fixed:** added an explicit
`Consequence:` clause to A1, A2, A4, and A5 in `paper.md`, citing guidance.md §3.2. B0 + B-alt +
F-G1 were already present with pre-committed wording (unaffected, PASS).

**6. Method-rigor audit — REVISE (fixed).** Checked guidance.md Part 6 items 1–10 against
`paper.md`:
- Item 1 (R1 estimand) — **gap found**: no explicit one-sentence estimand (quantity / unit of
  analysis / reference population / decision fed) existed before the Step 5 component list;
  only an implicit notation paragraph. **Fixed:** added an explicit "Estimand (R1)" sentence at
  the top of Step 5.
- Item 2 (verb check) — PASS, already explicit and passing in Step 3.
- Item 3 (H* seven slots) — PASS (see check 5).
- Item 4 (A* detection+gate) — PASS (present for all 6; `consequence` gap tracked under check 5).
- Item 5 (B0/B-alt/F-G*) — PASS.
- Item 6 (instrument R2 five-step + threshold) — **gap found**: the black-box AI-text detector
  (M6/A6) is explicitly one of R2's listed instrument types ("detector"), but paper.md validated
  it only via a single AUROC≥0.8 gate (S2), not R2's full sequence (external grounding, held-out
  refinement, ≥2-rater κ validation, confusion-structure check, freeze). **Fixed:** added an
  explicit R2-mapping paragraph after A6 — grounding via reused published detector construction,
  no refinement step needed (off-the-shelf, unmodified), the provenance-known ground truth
  standing in for human raters (stronger, not weaker, than κ-agreement), a new confusion-structure
  check (previously absent), and the existing freeze-before-Stage-2 gate.
- Item 7 (R3 confound-naming) — PASS (config-hash equality / distribution-matching / B-alt each
  name their confound, even if not in the literal "constraint X removes confound Y" template).
- Item 8 (R6 mechanism analysis) — PASS: RQ2's onset-dose ordering (diversity/tail vs. capability)
  plus the reused NN-differential-entropy tail metric jointly serve as the mechanism layer,
  consistent with CloserLookCollapse's entropy-precedes-quality-loss precedent.
- Item 9 (power per cell; thin cells INCONCLUSIVE) — **gap found**: A4 stated a power analysis
  and a reallocation mitigation but never the pre-declared INCONCLUSIVE rule (guidance.md Part 4
  situation 5). **Fixed:** added a "Power addendum — thin-cell INCONCLUSIVE rule" paragraph in
  Step 6, before "Mandatory baselines".
- Item 10 (archetype named + Part 2 evidence standard met) — PASS-with-fixes: `empirical` (A2)
  is named in Step 2; the A2 evidence standard (validated instrument, controlled comparison,
  pre-registered effect-floor tests, rival-explanation ablations, ≥1 mechanism analysis) is now
  met by the plan after the item-6 and item-9 fixes above.

**7. Stage cross-check (advisory) — PASS (already performed).** `pengsida-stage-reviewer`'s
Stage 1–5 review (above, in this same file) already covers N1↔Stage1, N3/N4↔Stage2, N6↔Stage3,
N8/E*↔Stage4, and the archetype classification, with two REVISE findings already fixed in
`paper_draft.*`. No new STOP-level finding surfaced in this re-run.

**8. Taste audit currency — PASS (no re-audit needed).** `taste_audit.md`'s recorded audit
predates this run's edits, but none of the edits touch the Step 0 asymmetry statement or
redefine any Step 5 term — the estimand sentence restates existing notation, the consequence
clauses and R2/INCONCLUSIVE additions are completions of already-declared assumptions/power
rules, not new claims. Judgment: the taste audit remains current; no re-audit triggered.

### Gate result: **REVISE** (fixes applied this pass; one residual, non-blocking-for-this-run gap)

Six of eight checklist items required a fix; all six were applied directly to `digest.md` /
`paper.md` in this pass (see per-item entries above). One item (check 2) has a residual gap that
genuinely cannot be closed without a real re-harvest (network fetch of 8 specific OpenReview
papers' PDFs) — out of scope for this pass per the "no real experiment compute / no Phase B/C"
mandate, and recorded here as the pre-Phase-B action item rather than silently passed over. No
STOP-level finding was found: nothing here invalidates the study design, and every fix was a
static-document completion of content the bundle already implied, not new experimental content.
**Per this run's mandate, Phase B/C were not attempted; the run stops at this gate.**
