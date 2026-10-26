# Pengsida Stage Review — B3.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding** (primary), with a secondary **Resource** flavor. Per `archetypes.md`'s tells: the core question is "how much of an observed change comes from each of three causes, and does the answer generalize across vendors" — no new pipeline is proposed as a fix to drift itself, and the probe batteries + decomposition model are the *analytical apparatus* that makes the phenomenon measurable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. The secondary Resource flavor comes from the released battery + cached-output corpus (`paper.md` CO4) being a genuine secondary deliverable — but it is not the headline claim, so the dominant bar below is Analysis/Finding throughout, with resource-style checks (coverage, leakage-of-a-different-kind, i.e. data contamination) folded into Stage 4 rather than run as a separate archetype pass. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "a single blended before/after score cannot tell these apart" is a first-principles framing (the gap is inherent to what a blended delta *can* represent, not a patch on top of an existing instrument), and the stakes are concrete and stated with a real documented incident, not a generic AI-importance appeal: "the canonical longitudinal audit of ChatGPT's behavior over time found that part of an apparent capability regression in code generation was in fact caused by newly added markdown fencing breaking an executability check." The Einstein ratio holds — the motivation is entirely about why the conflation matters practically (mis-triaged re-benchmarking vs. re-auditing vs. parser-patching), with zero method leak.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, e.g. "WildBench... treats surface length/style as a nuisance bias to penalize away... rather than a first-class, separately reported axis"), which clears the citation-dump failure mode. But the section never states, in one place, which single prior work is the *closest* competitor. The confirmed Stage 3 output marks `rw_chatgptbehavior` as the only work with `is_potential_baseline: true` in the direct comparison sense — it is, by construction, the nearest neighbor (same exact problem: a longitudinal audit of the same phenomenon) — but that ranking is buried inside a table field, not surfaced as a sentence a reader encounters before the thematic survey. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming `[ChatGPTBehavior, arXiv:2307.09009]` as the closest prior work and stating the precise delta (blended single-axis delta vs. this paper's calibrated three-way decomposition with an explicit leakage/noise accounting), rather than leaving the reader to infer it from a baseline-flag table.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the axis share, leakage share, and noise floor are all given operational definitions in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: output text is simultaneously the only measurement channel available and itself a target of vendor change, but *content* changes (a wrong answer, a different refusal) do not alter *surface-feature* scores the way format changes do — this one-directional confounding is exactly what licenses freezing the channel (format-robust scoring) to recover content change, and the draft states it explicitly rather than asserting orthogonality by fiat. No orphan components — every one of the four modules (battery design + calibration, leakage regression, noise-floor model, cross-vendor agreement test) traces to a named sub-problem, with no leftover machinery. The excluded challenge (black-box opacity for commercial pairs) is explicitly *not* claimed to be solved by any module — it is stated as a bounded, not eliminated, limitation, which is the honest move rather than quietly implying the calibration protocol makes vendor opacity irrelevant.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: the null-pair placebo (same snapshot queried twice) is a genuine falsification design, because if the noise-floor/leakage machinery were unreliable, a null pair (which by construction contains no true drift) would still show a false-positive axis detection; and the calibration-recovery RQ is falsification-tested against control pairs with an independently known cause, not merely correlated with an assumption of orthogonality. But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... in a majority of tested cells" without stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline (its per-experiment "Fallback" clauses) that didn't survive into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in the pre-existing `paper.md`'s Step 6 fallback wording).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Large language model providers now ship new model versions... often within weeks of one another" / "Yet a central question about every such update goes unanswered by the number itself" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this gap into a measurable question surfaces four separate obstacles" / "Our approach turns each of these obstacles into a specific, checkable design choice" / "We evaluate this design against version pairs from multiple vendors") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in both title and abstract: "a blended before/after score cannot distinguish capability, policy, and format change, and standard practice has already been caught mistaking one for another." The Conclusion names a real forward-looking limitation (black-box opacity for commercial pairs remains a calibrated behavioral inference, never internally verified) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming `[ChatGPTBehavior, arXiv:2307.09009]` as the closest prior work and stating the delta plainly (a blended, single-axis, single-vendor delta vs. a calibrated three-way decomposition with explicit leakage/noise accounting and a cross-vendor test), rather than leaving the ranking implicit in a baseline-flag table.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's canonical Phase A checklist (8 items), applying `guidance.md` as the standard,
> against `README.md`/`digest.md`/`paper.md` plus the upgraded `reference_candidates.jsonl`. This is
> distinct from the Stage 1-5 pengsida cross-check above (that review's inputs — the six
> `auto-research-discussion` stage outputs — were advisory input into §3 item 7, not a substitute for it).
> Date: 2026-07-04. No Phase B/C compute was attempted; this run stops at the Phase A gate as instructed.

**Precondition — Task 1 (reference-cache upgrade) completed first.** `reference_candidates.jsonl` was
rewritten from the flat 150-row ad hoc harvest schema into goal.md §1's canonical schema. Every one of
the 150 candidates was individually read (digest skimmed; `2607.01153`'s raw digest also cross-checked
against its arXiv abstract via live fetch) and given a `selected`/`rejected` verdict with a
paper-specific `why` — **no `pending` verdicts remain**. Result: **6 of 150 selected** (method-twin ×2,
adjacent ×4), **144 rejected**. A material finding surfaced during this pass and is reported under item 2
below: **none of `digest.md` N3's 8 cited works existed in the harvested cache at all** — they were
backfilled as 8 additional canonical-schema records (total cache: 158 rows, 14 selected / 144 rejected).

1. **Digest self-verification** — **REVISE, fixed.** Cross-node references all resolve correctly
   (C1-C5 ↔ N5, M1-M6 ↔ N6, CO1-CO4 ↔ N7, RQ1/RQ_INF_1/RQ_INF_2 ↔ N8, all pointing to real ids; N6's
   `unaddressed_challenges:["C2"]` is consistent with N6 `challenge_arguments` never invoking C2). All
   N0-N12 nodes + Claims section present. **Gap found:** N4 (`grounding_check` only), N5
   (`conflation_check` only), N6, N7, N8, and N12 lacked the `Status:`/`**absence_comment:**` 3-part
   trailer that N0-N3 and N9-N11 carry, in violation of goal.md §3 item 1's "every non-GIVEN item carries
   its 3-part absence comment." **Fix applied:** added a `Status: PARTIAL/HYPOTHESIS` +
   `absence_comment:{what_missing, why_matters, implication}` trailer to each of N4, N5, N6, N7, N8, N12
   in `digest.md` (guidance.md is silent on this specific mechanic; the fix follows goal.md §0's own
   digest.md file-contract description of the reverse-digest tag scheme).

2. **Reference-cache integrity** — **REVISE, fixed with one residual noted.** Before Task 1, digest.md
   N3/N4 and paper.md cite 8 works by key (`[ChatGPTBehavior, arXiv:2307.09009]`,
   `[MoreRLHFMoreTrust, OpenReview:FpiCLJrSW8]`, `[FewTokensDeep, OpenReview:6Mxhg9PtDE]`,
   `[RefusalIndex, OpenReview:9gJBhkLRat]`, `[ContrastiveOverRefusal, OpenReview:GXcN0MuN1q]`,
   `[WildBench, OpenReview:MKEHCx25xp]`, `[DiffInterpretation, OpenReview:6As4wfTB77]`,
   `[CARLoRA, OpenReview:5GimteSrgW]`) — **none of which appeared anywhere in the 150-row harvested
   `reference_candidates.jsonl`**, a direct violation of "every N3 key is a selected cache record" and of
   goal.md §8's hard gate ("citations only via `selected` cache keys"). Root cause: these 8 works were
   sourced during digest.md's construction from a separate auxiliary corpus
   (`topics/corpus/ideas.jsonl`, 11,683 entries, confirmed present locally and containing all 8
   `paper_id`s with correct titles), never from the reference-cache harvest that produced
   `reference_candidates.jsonl`. **Fix applied:** all 8 backfilled into `reference_candidates.jsonl` as
   canonical-schema `selected` records (relevance: `baseline` for ChatGPTBehavior, `method-twin` for
   RefusalIndex per this file's own Stage 3 refinement, `adjacent` for the remaining 6), each `why`
   stating the backfill provenance explicitly. **Spot-check by live fetch (3 ids, per goal.md §3 item 2):**
   `arXiv:2307.09009` resolved and verified (title/authors/abstract match; used to build a real
   abstract-level extraction digest, now at `discussion/backfilled_digests/2307.09009.md`, so this
   baseline's `digest_path` is resolvable); `arXiv:2607.01153` (one of the 6 newly-selected 150-harvest
   candidates) resolved and verified; `OpenReview:5GimteSrgW` (CAR-LoRA) hit an anti-bot verification wall
   on both `/forum?id=` and `/pdf?id=` — existence was independently confirmed via `topics/corpus/ideas.jsonl`
   but full-text is not fetchable in this environment. **Residual gap (not closed by this pass):** the
   other 6 backfilled OpenReview entries (including the `method-twin`-tagged RefusalIndex) still carry
   `digest_path: null`, `pdf_path: null`, `verified.id_resolves: false` — real extraction-mode digests for
   these could not be produced without OpenReview access. **Action item, deferred to the pre-Phase-E
   freshness sweep (goal.md §8):** re-attempt live retrieval for these 6 (a different fetch path,
   Semantic Scholar/Scholar Gateway mirror, or manual PDF upload) before Phase E cites them, since Phase E's
   `refs.bib` must be script-generated from resolvable cache records. No `pending` verdicts remain anywhere
   in the 158-row cache.

3. **Tag discipline** — **PASS.** `digest.md` consistently tags every item
   `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`/`[NON-CORPUS]`; no silent
   HYPOTHESIS→GIVEN promotion found. `paper.md` and `paper_draft.md` both state plainly throughout
   ("specification, no experiments run"; N9 explicitly `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]") that
   nothing below is a result.

4. **Claim-Evidence Map completeness** — **PASS.** All 5 claims in `paper.md`'s Claim-Evidence Map trace
   to H1/H2/H3 or are marked `supported-by-design`; H1/H2/H3 each carry a pre-committed verbatim fallback
   (E1/E2/E3 fallback text) plus the global pivot F-G1; no orphaned claims or hypotheses in either
   direction.

5. **Hypothesis/assumption machinery** — **REVISE, fixed.** H1/H2/H3 already carried binary statements,
   metrics, tests+alpha+correction, effect floors, and verbatim fallbacks (guidance.md §3.1 slots 1-5,
   7). **Gap found:** no assumption in the A1-A7 ledger addressed statistical power or a thin-cell
   INCONCLUSIVE rule (guidance.md §3.2's worked A6 instance, and Part 6 item 9), and gates were described
   in prose without the `PG-*` numbering goal.md §4 uses to wire them into the walking skeleton. **Fix
   applied:** added `A8` (power/INCONCLUSIVE assumption, modeled on guidance.md's B6.3 A6 worked instance)
   and explicit `PG-1`..`PG-7` labels to every A1-A7 gate; wired `A8`/`PG-7` into H1's and H3's scoring
   rules in Step 6 with an explicit "excluded from numerator and denominator, reported as INCONCLUSIVE,
   never dropped silently" clause. B0 + B-alt + F-G1 were already complete (guidance.md §3.3) — no change
   needed there.

6. **Method-rigor audit** (guidance.md Part 6 items 1-10 + Part 2 A2 evidence standard) — **REVISE,
   fixed.** Item-by-item: (1) **R1 estimand one-sentence** — missing; **fixed** by adding an explicit
   "Estimand (guidance.md R1)" line to paper.md Step 5 naming the quantity, unit of analysis, reference
   population, and the decision it feeds. (2) verb check — already PASS (Step 3's own audit).
   (3)/(4)/(5) H*/A*/B0-B-alt-F-G* slots — PASS after item 5's fix above. (6) **R2 five-step instrument
   validation** — the M2 judge classifier's A4 row stated only step③ (κ≥0.70 threshold); steps
   ①②④⑤ (external-source grounding, held-out-set refinement with named merge/split ops, confusion-structure
   inspection, freeze-before-scale) were missing; **fixed** by writing out the full 5-step R2 sequence
   inline in A4. (7) R3 confound-naming — PASS (each control already states the confound it removes in
   prose, e.g. A1's interleaved-window design vs. time-of-query confound). (8) **R6 ≥1 mechanism
   analysis** — the plan had headline tests (E1/E2/E3) but no analysis explaining *why* leakage/format
   shares take the values they do; **fixed** by adding a new "M7 — Feature-level leakage attribution"
   mechanism-analysis sub-experiment to Step 6, ranking M3 surface features by regression-coefficient
   magnitude per leaky pair. (9) **power per cell / thin-cell INCONCLUSIVE** — missing; **fixed** via the
   same A8/PG-7 addition as item 5. (10) archetype named (`empirical`, secondary `technical
   artifact`/resource) and the Part 2 A2 evidence standard — now fully met post-fixes (validated
   instrument R2 + controlled comparison + effect-size floors R4 + rival-explanation ablation R5
   (B-alt) + mechanism analysis R6, all present).

7. **Stage cross-check (advisory)** — **PASS, already satisfied.** The Stage 1-5 `pengsida-stage-reviewer`
   review earlier in this file already covers N1↔Stage 1 (PASS), N3/N4↔Stage 2 (REVISE→fixed), N6↔Stage 3
   (PASS), N8/E*↔Stage 4 (REVISE→fixed), archetype from paper.md (used throughout). No new STOP surfaced;
   today's fixes (digest.md absence-comments, paper.md A8/PG-*/R2/R6 additions) are additive rigor
   scaffolding and do not touch N1/N3/N4/N6/N8/archetype substantively, so the existing cross-check
   remains valid and was not re-run from scratch.

8. **Taste audit currency** — **PASS.** `taste_audit.md` (🟢, no condition fired) predates today's fixes,
   but none of today's edits touch the Step 0 asymmetry statement or the Step 3 framing self-audit — the
   estimand sentence, `PG-*` labels, `A8` power gate, and `M7` mechanism sub-experiment add rigor
   scaffolding without changing verbs, the bridge/synthesis reading, or the core claims. Re-audit not
   required.

### Phase A gate result: **REVISE items found and fixed; one residual action item logged (item 2), not
blocking.**

Four of eight checklist items (1, 2, 5, 6) fired REVISE on the first pass; all four were fixed directly in
`digest.md`/`paper.md` during this run, per guidance.md sections cited above. Item 2 carries one residual,
explicitly-flagged gap (6 of 8 backfilled N3 citations lack a resolvable `digest_path`/`pdf_path` because
OpenReview fetch is blocked by an anti-bot wall in this environment) that does not block Phase B — Phase B's
walking skeleton does not consume these citation records — but must be closed before Phase E's citation
gate (goal.md §8) and is logged as a pre-Phase-E action item. Per this environment's scope, Phase B/C
(real experiment compute) is explicitly not attempted; this run stops at the Phase A gate as instructed.
