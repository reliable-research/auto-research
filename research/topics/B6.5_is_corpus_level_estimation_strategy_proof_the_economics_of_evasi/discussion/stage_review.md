# Pengsida Stage Review — B6.5

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs" — is corpus-level estimation strategy-proof, or does evasion cost scale uneconomically — with no new detection *method* proposed as a fix. The estimator-vs-adversary pairing (mixture-MLE / debias-aggregate estimator vs. non-adaptive/coordinated paraphraser) is the *analytical apparatus* that makes the phenomenon observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1 of `pipeline.md`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — the confirmed Stage-2 motivation states plainly that "an operator who assumes a pooled estimate is safe 'because any one verdict can be gamed but the average can't' is trusting exactly the averaging intuition this paper sets out to test, not an established result" — a first-principles framing of a root, unverified assumption, not a patch on an existing method. The stakes are stated concretely (treating an unverified safeguard as safe is "actively misleading," while a confirmed safeguard is "a genuinely different, and better, instrument"), not a generic AI-importance appeal. The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes, with zero method leak — "coordinated adversary," "cost model," and "shuffled-label control" only appear starting in paragraph three onward.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs in Related Work are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. the debiased-proportion-estimation paragraph ends on "neither models an adversary who paraphrases, or otherwise manipulates per-record signals, specifically to bias the aggregate"), which clears the "citation dump" failure mode. But on the first assembled pass, the section never stated, in one place, which single prior work is the *closest* competitor — Stage 3 of `pipeline.md` already did this work explicitly (marking the corpus-level mixture-MLE estimator as directly instantiated as this paper's own M2, with the note "not a baseline in the beat-a-number sense... its protocol is directly run inside this paper's own pipeline"), but that ranking had not yet been surfaced as an up-front sentence in the assembled prose. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming the corpus-level mixture-model reframing (this paper's own estimator precedent) and the bandit strategy-proofness literature (the source of the paper's own title vocabulary) as the closest prior work, stating the precise delta for each, rather than leaving the reader to rank the four thematic clusters themselves. This is now the opening sentence of the Related Work section ("The closest prior work to this paper is the corpus-level measurement reframing that first estimated AI-text prevalence by fitting a mixture model over aggregate token statistics, and it is worth stating the delta plainly before surveying the wider landscape...").

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the Problem Definition section defines $D_N$, $\alpha$, $E$, $\hat\alpha$, $g$, $B(\mathcal{A})$, $e_0(N)$, $e_B(N)$, $\varepsilon$, and $\beta$ before any Methodology subsection invokes them, so no construct is "named after the fact." The inferential chain is licensed at its one load-bearing hinge: the Coordinated Adversary Arm's Insight states explicitly that "independent per-document noise cancels under aggregation by construction, but a directionally coordinated adversary specifically breaks that cancellation" — this is exactly the step that makes the coordination test non-redundant with the base (non-adaptive) measurement, and the draft states it as an argument rather than asserting the isolation by fiat. No orphan components — every one of the five modules (coordinated adversary arm, cost-model invariance check, semi-synthetic ground-truth design, debiasing-under-shift diagnostic, naive-average confound control) traces to a named sub-problem in `pipeline.md` Stage 4 (`sp_coordinated_evasion`, `sp_cost_model_ambiguity`, `sp_ground_truth_construction`, `sp_debiasing_under_adversarial_shift`, `sp_design_vs_scale_confound` respectively), with no leftover machinery and no sub-problem left unaddressed.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ7 (naive-average confound control) is a genuine falsification design, recomputing the robustness comparison against a null model that would produce the *same* result if the true cause were generic averaging rather than estimator design; RQ1/RQ2 similarly test whether the base measurement's conclusion survives dropping the independent-perturbation assumption. But on the first assembled draft, several RQ subsections stopped at an "**Expected outcome**" line without a separately stated **Falsification condition** — e.g. an early draft of RQ5 read only "the corpus-level estimator's attacked error remains at most 0.05 and at most twice its clean error... while the paired detector's AUROC falls to at most 0.60," with no adjacent line stating what result would refute that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as an explicit, checkable condition, not implied by the reader inverting the expected outcome themselves — and the underlying `paper.md` material already had this discipline (its Step 6 "Fallback" clauses for RQ1, RQ_INF_1, and RQ_INF_2) that had not yet been carried into every one of the seven RQ subsections in the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ subsections, stating the specific, concrete observation that would refute each expected outcome — not a vague restatement of the outcome's negation, but the exact statistical or comparative condition (mirroring the rigor already present in `paper.md`'s own Step 6 fallback clauses and Step 9 walking-skeleton pass/fail criteria). All seven subsections in the current `paper_draft.md` now carry this line (e.g. RQ3's: "Refuted (no scaling advantage) if either cost model's confidence interval on $\hat\beta$ includes or falls below 0; refuted as cost-model-dependent... if the two cost models disagree in sign even when each individually excludes 0").

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Synthetic, LLM-generated text is no longer a curiosity in web-scale corpora" / "Yet whether routing around single-document fragility actually buys anything has not been directly measured" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this gap into a measurable claim surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice rather than a hedge" / "We evaluate this design on semi-synthetic corpora...") reconstructs the whole six-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence two of any paragraph. One quotable contribution sentence exists and is used consistently across title and abstract: evasion is "scale-invariant against a per-document label and scale-taxed against a population proportion" — echoed directly in the title ("Scale-Taxed, Not Scale-Invariant") and unpacked in the abstract's opening two sentences. The Conclusion names two real forward-looking limitations (the budget-bounded, non-omniscient threat model, and the semi-synthetic-corpus scope) rather than only recapping the abstract at the same altitude, and states what each limitation would mean for the paper's central claim rather than gesturing at "future work" abstractly.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming the corpus-level mixture-model reframing and the bandit strategy-proofness literature as the two closest prior works and stating each delta plainly (rather than leaving the four thematic clusters unranked).
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per goal.md §3's checklist, against the current `README.md`/`digest.md`/`paper.md` and the
> just-rewritten `discussion/reference_candidates.jsonl` (canonical schema; 150 harvested
> candidates re-triaged to 3 selected + 147 rejected, plus 7 backfilled N3-grounded records — see
> "Reference-cache upgrade" note below). This is the goal.md-defined Phase A gate, distinct from
> the auto-research-discussion Stage 1-5 review above (which validated the discussion-loop
> artifacts that fed `paper_draft.md`). Date: 2026-07-04.

**0. Reference-cache upgrade (context for items 1-2 below).** `reference_candidates.jsonl` was a
flat, ad hoc harvest (topic_id/rank/score/ref_id/title/source/pdf_path/digest_path only) with
every record implicitly `pending`. Rewritten to goal.md §1's canonical schema
(key/title/ids/venue/year/url/pdf_path/digest_path/relevance/verdict/why/verified). Every one of
the 150 harvested candidates was read (digest skim) and given a specific verdict — 3 selected
(`MultiAgentMechDesign2025` adjacent, `GumbelWatermarkSampleComplexity2026` method-twin,
`ATINTER2023` adjacent), 147 rejected with a paper-specific one-sentence reason (no generic
"off-topic" filler). The harvest turned out to be generically-queried and largely missed the
paper's own real reference set: none of digest.md's N3 table's 7 works (`MonitorAIScale`,
`DetectGPT`, `AdaptiveWMAttack`, `MarkovCalib`, `DUCI`, `AnchorPeerReview`, `UCB-S`) were present in
the 150-item harvest at all — they were grounded via a separate corpus (`topics/corpus/ideas.jsonl`)
during digest construction and never re-harvested into the cache file. Backfilled all 7 as
`selected` records (relevance tags matching how `paper.md`/`pipeline.md` already use them:
`MonitorAIScale`/`AdaptiveWMAttack`/`DUCI` = method-twin, `DetectGPT` = baseline,
`MarkovCalib`/`AnchorPeerReview` = adjacent, `UCB-S` = background) so the cache actually reflects
what N3 cites. For the 4 `baseline`/`method-twin` (load-bearing) backfills lacking any local
digest, wrote lightweight extraction-mode digests under `discussion/refs_digests/` from each
paper's own real proposal text in `topics/corpus/ideas.jsonl` (motivation + method + the specific
limitation N4 already attributes to it) so `digest_path` resolves; `pdf_path` stays `null` and
`verified.id_resolves=false` for all 7 since no PDF is cached locally — reported honestly rather
than fabricated. Net: 10 selected / 147 rejected in the final 157-record cache.

**1. Digest self-verification — REVISE (fired, fixed).** Re-ran the checks `digest.md`'s own
self-verification pass claims. N0-N11 and Claims each carry a 3-part `absence_comment` for every
non-`GIVEN`/non-`GROUNDED` item; N3's `grounding_check=true` holds (all 7 `citation_key`s now also
resolve as `selected` cache records, see item 2). **Gap found:** N12 (Contribution Type) is tagged
`[HYPOTHESIS]` but carried no `absence_comment`, breaking the digest's own claimed invariant ("every
non-GIVEN item carries its 3-part absence comment"). **Fixed:** added the missing 3-part
`absence_comment` to N12 in `digest.md` (what_missing/why_matters/implication), citing goal.md §3
item 1. Cross-node ID checks (V-04: `N4.affects_works ⊆ N3.citation_key`; `N6` challenge/mechanism
ids ⊆ {C1-C4}/{M1-M5}; `N8.rq_id` = `N9.rq_id`) re-verified by hand and all resolve. **PASS after
fix.**

**2. Reference-cache integrity — REVISE (fired, fixed).** Before this run, **none** of digest.md's
N3 keys existed in `reference_candidates.jsonl` at all (see item 0) — a hard fail of "every N3 key
is a `selected` cache record." **Fixed:** backfilled all 7 as `selected` (item 0), with resolvable
`digest_path` for the 4 load-bearing (`baseline`/`method-twin`) ones. Spot-checked 3 of the 7 ids
by resolving them against the local `topics/corpus/ideas.jsonl` (the same corpus digest.md itself
cites as the grounding source) rather than a live web fetch: `bX3J7ho18S` → "Monitoring AI-Modified
Content at Scale..." (matches N3's `MonitorAIScale` summary verbatim), `UiAyIILXRd` → "DetectGPT:
Zero-Shot Machine-Generated Text Detection..." (matches), `EUSkm2sVJ6` → "How Much of My Dataset
Did You Use?..." (matches `DUCI`'s summary). No `pending` entries remain anywhere in the cache (all
157 records carry a final `selected`/`rejected` verdict). **PASS after fix.**

**3. Tag discipline — PASS.** Scanned all of `digest.md`: every assertion carries one of
`[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`; no silent `[HYPOTHESIS]→[GIVEN]`
promotion found (N9's results stay `[HYPOTHESIS]`-flagged directional predictions throughout, never
asserted as findings; N11 stays `[PLACEHOLDER]`/`NOT_FOUND`).

**4. Claim-Evidence Map completeness — PASS.** Every row in `paper.md`'s Claim-Evidence Map traces
to an H-id (RQ1 / RQ_INF_1 / RQ_INF_2) or an explicit "supported-by-design" scope declaration
(A5/B-alt/C4 scope; A3/threat t2 cost-model invariance) — no orphans in either direction. Every
H-id has a pre-committed verbatim `Fallback` in Step 6, and the fallback-combination rule into the
global pivot F-G1 is explicit ("IF the central hypothesis family fails (RQ1 fallback fires AND
RQ_INF_1 gives β≤0)"). No claim rests on an unmeasured adjective (Step 5's adjective table covers
every term used in the Claim-Evidence Map and Abstract v0).

**5. Hypothesis/assumption machinery — REVISE (fired, fixed).** RQ1/RQ_INF_1/RQ_INF_2 each already
had `applies_if` (Assumption), binary `Hypothesis`, `Metric`, `Verification` (test + alpha, Holm
correction), and a verbatim `Fallback` — 5 of guidance.md §3.1's 7 slots present; **missing:** an
explicit `effect_floor` label (present in substance as inline thresholds, e.g. $\hat\beta\ge0.5$,
but not named) and an explicit `aggregation` (pre-registered vote rule) slot. **Fixed:** added an
explicit **Aggregation** line to RQ1 ("vote across generator families — criterion must hold on
$\ge2$ of the $\ge3$ tested families, Holm-corrected"); RQ_INF_1/RQ_INF_2 already state their
aggregation rule inline ("under *both* cost models" / "CI lower bound $\ge2$") so were left as-is.
**Assumption ledger (A1-A6):** each already had the assumption statement, `Fail` (=failure_mode),
and `Detect` (=detection) — **missing** the two remaining guidance.md §3.2 slots, `gate` and
`consequence`, for all six. **Fixed:** added explicit `Gate:` (PG-1/PG-2/PG-4 for the
walking-skeleton-checked ones; Phase C for the ones only checkable at scale; "by declaration" for
the out-of-scope A5) and `Consequence:` (which H\* blocks/degrades/restricts if the assumption
fails) clauses to all of A1-A6. B0 + B-alt + F-G1 confirmed present with pre-committed wording
(unchanged). **PASS after fix.**

**6. Method-rigor audit — REVISE (fired, fixed), evidence standard for A2 met.** Ran guidance.md
Part 6 items 1-10:
- Item 1 (estimand in one sentence, R1) — **missing**; Step 5 had notation but no single R1-shaped
  sentence (quantity/unit/population/decision). **Fixed:** added an explicit **Estimand** line to
  Step 5.
- Item 2 (verb check) — PASS (Step 3 self-audit already runs this; verbs are
  formalize/isolate/measure/gate, no integrate/unify/leverage).
- Item 3 (H\* seven slots) — REVISE→fixed, see item 5.
- Item 4 (A\* detection + gate) — REVISE→fixed, see item 5.
- Item 5 (B0+B-alt+F-G\*) — PASS, already present.
- Item 6 (instrument R2 5-step validation) — **N/A, judgment call recorded here rather than a
  fabricated pass:** guidance.md's R2 protocol (ground in external sources → refine on held-out set
  → validate against ≥2 human raters, κ≥0.7 → inspect confusion structure → freeze) targets
  taxonomies/rubrics/LLM-judges. This topic's "instrument" is the M2 statistical estimator, whose
  analogous rigor is the ground-truth-recovery-within-tolerance + shuffled-label negative control
  (A1, PG-1) — no human-rater κ applies because there is no qualitative labeling step. Recorded
  explicitly rather than silently marked PASS or REVISE.
- Item 7 (every design constraint names its confound, R3) — **missing** as an explicit paper.md
  statement (the confound-removal reasoning existed only in `pipeline.md`'s Stage 6 refiner pass,
  not in `paper.md` itself). **Fixed:** added a **"Design constraints and the confound each
  removes"** list to Step 6 naming the topic-confound (HC3 pairing), trivial-recoverability-confound
  (shuffled-label control), cost-model-artifact-confound (≥2 cost models), weak-attacker-confound
  (B-alt), and generic-averaging-confound (RQ_INF_2's naive control).
- Item 8 (≥1 mechanism analysis, R6) — PASS; RQ_INF_2 (naive-average vs. dedicated estimators)
  functions as the mechanism-decomposition layer (is the effect estimator-design or generic
  averaging?).
- Item 9 (power per cell; thin cells pre-declared INCONCLUSIVE, R8) — **missing**. **Fixed:** added
  an explicit **Power statement** to Step 6 (power $\ge0.8$ target for the pre-registered effect
  floors; any cell falling below is pre-declared INCONCLUSIVE per guidance.md Part 4 situation 5,
  never scored null, never dropped).
- Item 10 (archetype named + Part 2 evidence standard met by the plan) — PASS; archetype = A2
  empirical/measurement (Step 2); the plan now has a validated-instrument analogue (A1/PG-1),
  controlled comparison (B0 vs. M2 vs. naive-average), pre-registered trend test with effect floor
  (RQ_INF_1), rival-explanation ablation (B-alt, cost-model invariance), and mechanism analysis
  (RQ_INF_2) — all five A2 evidence-standard components map to a concrete, already-specified
  experiment, not merely stated intentions.

**7. Stage cross-check (advisory) — already run.** The `pengsida-stage-reviewer` pass earlier in
this file (Stages 1-5, against `pipeline.md`'s N1↔Stage1/N3-N4↔Stage2/N6↔Stage3/N8↔Stage4
correspondences) already covers this item; its two REVISE findings were fixed in `paper_draft.md`
before this Phase A re-run. No new STOP or REVISE surfaced against the current `paper.md`/`digest.md`
that Stage cross-check didn't already anticipate.

**8. Taste audit currency — PASS, no re-run needed.** `taste_audit.md`'s recorded audit (🟢, no
condition fired) predates this run, but none of today's fixes touched the asymmetry statement (Step
0) or the formal definition (Step 5's adjective table, aside from adding the non-substantive
Estimand sentence above it) — the audit remains current per goal.md §3 item 8's own trigger
condition ("if the recorded audit predates a material edit to the asymmetry statement or formal
definition, re-run it"). No material edit occurred; re-run not required.

### Gate result: **PASS** (after fixes)

All eight checklist items now clear. Five items required a REVISE-level fix (items 1, 2, 5, 6, and
the reference-cache upgrade in item 0); all five were fixed directly in `digest.md`/`paper.md`/
`discussion/reference_candidates.jsonl` in this pass, each citing the specific guidance.md section
that required it. No STOP condition fired at any point (no orphaned claim, no un-gated assumption
that couldn't be fixed by adding the missing label, no cache integrity failure that couldn't be
backfilled from material already grounded in `digest.md`). Phase B (walking skeleton) is unblocked
by this gate, but **out of scope for this run** — no real experiment compute exists in this
environment; execution stops here per this task's instructions.
