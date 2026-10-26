# Pengsida Stage Review — B5.4

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how much a phenomenon occurs and whether one specific intervention changes it" with no new pipeline proposed as a fix — the harness (dual-reference scorer, dual gap measure, structured-offer deletion, channel-attribution analysis) is the *analytical apparatus* that makes the phenomenon and the intervention's effect observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "the surplus a stronger negotiator extracts from a weaker one is not fixed by the capability gap alone but by how much of that gap can pass through the action-space channel the bargaining protocol leaves open" is a first-principles framing (root mechanism, not a patch), and the stakes are stated concretely: a deployer cannot currently set a safe capability-gap operating threshold, nor know whether a near-zero-cost self-restriction would help, because "a single-gap-level audit cannot answer the deployment question that actually matters." This is not a generic AI-importance appeal — it is tied specifically to Stage 1's four confirmed outputs (episode record, surplus-loss reading, scaling estimate, causal verdict), and the Einstein ratio holds: the opening paragraphs are pure problem/stakes with zero method leak (the structured-offer intervention itself is correctly withheld until the method paragraph).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "AI-control work... restricts the strong/untrusted side or the surrounding protocol, never the weak party's own channel as self-protection"), which clears the "citation dump" failure mode. But the first assembled draft's Related Work opened directly into the four threads without ever stating, in one place, which single prior work (or pair of works) is the *closest* competitor. Digest N3's own relevance notes already did part of this work independently for two different works — calling `ScalingLawsOversight` "the closest methodological template" and `AIControl` the work that "establishes that protocol-level restrictions can protect a weak party against a strong adversary" — but that dual ranking never made it into the assembled prose. A reviewer reading only the four parallel threads has to infer for themselves which one (or two) is the nearest neighbor; per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first." Here the situation is slightly sharper than a single missing citation: this paper's nearest neighbor genuinely splits across two axes (phenomenon-closest vs. method-closest), and the first draft didn't even flag that the split exists, let alone name both halves.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section naming `AIControl` (phenomenon-closest: restriction-as-protection) and `ScalingLawsOversight` (method-closest: capability-gap-as-scaling-law) as the two works jointly constituting the nearest prior work, stating precisely why neither alone closes the gap — rather than leaving the reader to rank the four threads unassisted.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the normalized surplus-loss metric, the dual capability-gap measure, and the structured-offer deletion are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: the zero-gap self-play existence check ("if mean surplus loss is already large at Δ=0, the metric is broken, not the phenomenon") is exactly the step that makes every subsequent gap-dependent claim interpretable rather than an artifact of a mechanically biased game — and the draft states this explicitly as a precondition rather than asserting the scaling claim by fiat. No orphan components — every one of the four modules (dual gap quantification, the bargaining harness, the structured-offer constraint, channel attribution) traces to a named sub-problem, with no leftover machinery; the tactic-taxonomy component inside channel attribution is explicitly scoped as exploratory rather than left dangling as an unjustified extra.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (the cross-tier substitution RQ is a genuine falsification design: it specifically tests whether restriction can substitute for capability, not merely whether restriction correlates with lower loss; and the zero-gap existence check is itself a falsification test of the metric before any causal claim is made). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ...with the reduction growing as the gap widens" without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline (its Step 6 "Fallback" clauses for H1, H2a, H2b, H3, and its B0 "pre-registered pass: |E[L|Δ=0]| ≤ 0.05" pass/fail line) that didn't survive into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all five RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in the pre-existing `paper.md`'s Step 6 Fallback clauses).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Autonomous LLM agents are increasingly delegated..." / "Yet how much surplus a weak agent loses... remains unmeasured" / "The nearest existing work approaches this gap from two different angles..." / "Turning this into a measurable question surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice" / "We evaluate this design across...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in both title and abstract: "surplus extraction is gated by the action-space channel a bargaining protocol leaves open, not fixed by the capability gap alone." The Conclusion names a real forward-looking limitation (the gap-measure disagreement / projection-dependence risk flagged by `sp_gap_construct`) rather than only recapping the abstract, and does not repeat the abstract's sentences verbatim.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming `AIControl` and `ScalingLawsOversight` as the two works jointly constituting the closest prior work and stating the delta plainly (rather than leaving four parallel threads unranked).
2. **Stage 4 fix** — added a **Falsification condition** line to each of the five RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — 2026-07-04

> Trigger: Task 1 reference-cache upgrade (rewriting `discussion/reference_candidates.jsonl`
> from the ad hoc harvest schema into goal.md §1's canonical schema, and triaging all 150
> harvested candidates to `selected`/`rejected`) surfaced findings that require re-running
> goal.md §3's Phase A checklist against `README.md` / `digest.md` / `paper.md`, applying
> guidance.md as the standard. This run does **not** touch Phase B/C (no experiment compute
> exists in this environment) and does not edit `paper_draft.md`/`.tex`/`.pdf` (those are
> Phase E/F artifacts, out of this gate's scope) — findings that bear on them are flagged
> as pre-Phase-E to-dos, not fixed here.

### Task 1 summary (reference cache)

150 harvested candidates (110 arXiv + 40 ACL-anthology "openview") triaged: **7 selected,
143 rejected** from the original harvest. The harvest itself turned out to be near-entirely
off-topic relative to this paper's actual construct (bilateral bargaining, capability-gap
scaling, action-space-constraint exploitation) — most of the 150 are generic LLM
training/security/benchmark/NLP papers with no bargaining, capability-gap, or
agent-exploitation content, confirming goal.md's own framing that harvest rank is "a weak
recall signal, not a relevance verdict." The 7 selected:

| key | relevance | one-line reason |
|---|---|---|
| `LanguageOfBargaining2023` | method-twin | Human-subjects AO-vs-NL bargaining contrast — near-identical manipulated variable to this paper's M3 |
| `PrincipalLoyalty2606` | adjacent | Same principal/agent/adversarial-counterparty framing, different outcome (loyalty, not surplus) |
| `BEDA2512` | adjacent | Formal adversarial/alignment dialogue-act vocabulary, usable for RQ_INF_3 tactic tagging |
| `Decepticon2512` | adjacent | Web-agent dark-pattern manipulation — a different exploitation channel, same "channel is exploitable" premise |
| `TRAP2512` | adjacent | Persuasion-driven task-redirection benchmark for web agents — same premise, different domain |
| `DeliberatingCrowds2512` | background | A2-archetype structural exemplar (factorial LLM behavioral-measurement design) |
| `LLMsKnowCapable2512` | background | A2-archetype structural exemplar (multi-experiment, falsification-oriented design) |

A more severe finding surfaced while checking these against `digest.md`'s own N3: **none of
digest.md's 10 pre-existing N3 related works (`ScalingLawsOversight`, `WeakToStrong`,
`AIControl`, `ControlTax`, `StrategicPersuasion`, `GreatModelsThinkAlike`, `CompeteAI`,
`ARIA`, `GLEE`, `DealOrNoDeal`) existed anywhere in `reference_candidates.jsonl`** — they
were grounded via a separate corpus (`topics/corpus/ideas.jsonl`, 11,683 OpenReview papers)
that the 150-candidate arXiv/ACL harvest never touched. This is exactly what goal.md §3
item 2 exists to catch. **Fix applied:** all 10 works were back-filled into
`reference_candidates.jsonl` as `selected` canonical-schema records (relevance tags carried
over from `digest.md`'s own characterization: `ScalingLawsOversight`=method-twin,
`AIControl`=contrast, `GLEE`/`DealOrNoDeal`=baseline, the rest=adjacent), bringing the total
cache to 160 records / 17 selected. Two spot-check fetches (arXiv:2606.30383, and a search
confirming `LanguageOfBargaining`'s real ACL Anthology page/DOI/arXiv id) resolved live;
OpenReview's own forum pages are behind a bot-check wall in this environment and could not
be independently confirmed by fetch — treated as unresolved-by-fetch but internally
consistent (real forum ids recorded in `topics/corpus/ideas.jsonl` with matching titles).

### Checklist (goal.md §3)

**1. Digest self-verification — PASS.** All N0–N12 + Claims present in `digest.md`; every
non-GIVEN item carries its 3-part `absence_comment`; digest.md's own V-01–V-12/EX-11
self-verification pass is internally consistent. Cross-node references (N4→N3,
N6.challenge_arguments→C*/M*, N8→C*/CO*/M*, N9.rq_id→N8) all resolve. Re-checked and
updated after this pass's N3/N4 edit (see below) — counts in V-04 bumped from 10→11 N3 keys
/ 7→8 limitations to stay consistent with the new entry.

**2. Reference-cache integrity — REVISE, fired and fixed.** Before this pass: **FAIL** — no
N3 key resolved to any cache record at all (see above). **Fix applied:** all 10 pre-existing
N3 works plus the newly-discovered `LanguageOfBargaining2023` method-twin are now `selected`
records in `reference_candidates.jsonl` (goal.md §1 schema). **Residual, unresolved gap
(logged, not fixed here):** the 10 back-filled corpus-grounded entries have `digest_path:
null` (`verified.id_resolves: false`) — they were grounded via `topics/corpus/ideas.jsonl`'s
short "proposal" summaries, not a full per-paper `paper-digest` extraction, and no PDF is
locally cached for any of them (they are OpenReview submissions without confirmed public
PDFs, or non-corpus canonical arXiv papers never separately fetched). Four of these
(`ScalingLawsOversight`, `AIControl`, `GLEE2410`, `DealOrNoDeal1706`) are load-bearing
(method-twin/contrast/baseline) — goal.md §3 item 2's "load-bearing entries have resolvable
`digest_path`" clause is **not yet satisfied** for them. **Action required before Phase E:**
run `paper-digest` in extraction mode on these four (fetch PDFs where public) to produce
real `digest_path` files; until then, any Phase E prose citing their specifics beyond what
`digest.md`'s N3 approach_summary already states is unverified. No `pending` verdicts remain
anywhere in the cache (all 160 records are `selected` or `rejected`).

**3. Tag discipline — PASS.** No untagged assertion found in `digest.md`; every forward
statement is `[HYPOTHESIS]`/`[GROUNDED:...]`/`[PLACEHOLDER]`; no silent
`[HYPOTHESIS]`→`[GIVEN]` promotion detected in this or the prior review.

**4. Claim–Evidence Map completeness — PASS.** Every claim in `paper.md`'s
Claim–Evidence Map traces to an H-id (H1/RQ1, H2a/RQ2a, H2b/RQ2b, H3/RQ_INF_3) or a
supported-by-design definition (B0, Step 5 defs); every H-id has a fallback; CO4
(deployment recommendation) is explicitly `fallback-covered (F-G1)`. No orphans in either
direction.

**5. Hypothesis/assumption machinery — REVISE, fired and fixed.** Checked every H* against
guidance.md §3.1's seven slots (applies_if / metric / test / alpha / effect_floor /
aggregation / verbatim fallback):
- **H1 (RQ1) was missing its effect floor** — the original wording tested sign,
  significance, and monotonicity but no minimum magnitude, so per guidance.md §3.1 ("a
  slope can be significant and practically zero") it could pass on a vanishingly small
  effect. **Fixed:** added an explicit floor — `β_Δ × range(Δ) ≥ 0.10` normalized-loss units
  under each gap measure — and updated H1's fallback wording to include "below the
  pre-registered practical-significance floor" as a failure mode.
- **H2b (RQ2b) was missing its non-inferiority margin** — "≤" with no stated δ is a
  superiority test mislabeled as non-inferiority. **Fixed:** added an explicit
  `δ = 0.05` normalized-loss-unit margin, matching H2a's own 0.05-unit floor convention.
- H2a and H3 already had explicit effect floors (≥0.05 units; >50% slope share) — no
  change needed there.
Checked every A* against guidance.md §3.2's five slots (assumption / failure_mode /
detection / gate / consequence): detection and gate were already present for A1–A6, but
**`consequence` was implicit rather than its own stated slot for A1–A4 and A6** (only A5 had
an explicit consequence). **Fixed:** added an explicit `consequence:` line to A1, A2, A3,
A4, and A6, each naming which H* is blocked/downgraded and how. B0 + B-alt + F-G1 were
already present with pre-committed wording — no change needed.

**6. Method-rigor audit — REVISE, fired and fixed.** Guidance.md Part 6 self-check,
items checked individually:
1. *Estimand in one sentence (R1)* — **missing** (no R1-shaped estimand sentence existed
   anywhere in `paper.md`, only the Step 0 asymmetry sentence and Step 5 notation table).
   **Fixed:** added an explicit R1 estimand sentence at the top of Step 5.
2. *Verb check* — PASS (already checked at Step 3 and in `taste_audit.md`; re-confirmed,
   no change touches the audited text).
3. *Every H\* has all seven slots* — **REVISE, fixed** (H1, H2b — see item 5 above).
4. *Every A\* has detection + gate* — PASS structurally; `consequence` slot completeness
   fixed under item 5.
5. *B0 + B-alt + F-G\* present* — PASS.
6. *Every instrument has the 5-step R2 plan with an acceptance threshold* — **REVISE,
   fixed.** The tactic-tagging instrument (M5, RQ_INF_3) only specified R2 step ③
   (validate against human raters, κ≥0.7). **Fixed:** added the missing steps — ①
   grounding the 4 tactic labels in external negotiation-tactics literature and this
   cache's own `BEDA2512`/`StrategicPersuasion` entries, ② a named draft-wide/refine-on-
   held-out-set step (100-transcript pilot, merge/split ops down to 4 labels), ④ a
   confusion-structure inspection requirement, ⑤ a freeze-before-scale step — plus the
   guidance.md Part 4 situation 7 remediation path (simplify to a 2-label split) if κ<0.7.
7. *Every design constraint names its confound (R3)* — **REVISE, fixed.** Added an explicit
   confound ledger (5 one-liners: system-prompt/condition-disclosure, side/first-mover
   counterbalancing, both-constrained control, pinned model versions, zero-gap self-play)
   under the Assumptions section, each stating the specific confound it removes.
8. *≥1 mechanism analysis budgeted (R6)* — PASS (RQ_INF_3/M5 channel attribution).
9. *Power stated per cell; thin cells pre-declared INCONCLUSIVE* — **REVISE, fixed.**
   Power was stated (n=50/cell, d≈0.4 at power 0.8) but there was no explicit
   thin-cell-INCONCLUSIVE pre-declaration (guidance.md Part 4 situation 5). **Fixed:** added
   a thin-cell rule at the top of Step 6 (< 30 valid episodes/cell → INCONCLUSIVE, excluded
   from primary tests but never dropped silently; >25% thin cells in a central test →
   the whole test is INCONCLUSIVE).
10. *Archetype named + Part 2 evidence standard met* — archetype (A2, empirical/measurement)
    is named at Step 2; the Part 2 A2 evidence standard (validated instrument + controlled
    comparison + effect-size floors + rival-explanation ablations + mechanism analysis) is
    now met by the plan **after** the items-3/6/9 fixes above (effect floors, R2 sequence,
    thin-cell rule) — before those fixes it was not.

**7. Stage cross-check (advisory) — REVISE noted, logged as pre-Phase-E to-do.**
`pengsida-stage-reviewer`'s Stages 1–5 (above this section) already passed/fixed on the
prior run. This Phase A re-run adds one new advisory finding within its scope: the
newly-discovered method-twin `LanguageOfBargaining2023` (Task 1) is now in `digest.md`'s N3
with a concede-and-differentiate treatment (guidance.md Part 4 situation 6), but
`paper_draft.md`/`.tex` (Phase E/F outputs, assembled before this discovery) do **not** yet
name it in their Related Work section. Per guidance.md Part 4 situation 6, this is "a
`paper.md` repositioning + Phase A re-check, never a silent related-work paragraph" — the
repositioning is done at the `digest.md`/`paper.md` level in this pass; **updating
`paper_draft.md`/`.tex`'s prose is out of this Phase A gate's scope** (editing Phase E/F
artifacts) and is logged here as a required pre-Phase-G fix: add
`LanguageOfBargaining2023` as a third named nearest-neighbor in the Related Work section's
opening (alongside the existing `AIControl`/`ScalingLawsOversight` sentence from the prior
Stage 2 fix), stating the concede-and-differentiate delta from `digest.md`'s N3/N4 verbatim.
Also logged: a 2026 follow-up paper surfaced incidentally during spot-checking
(arXiv:2601.04387, "The Language of Bargaining: Linguistic Effects in LLM Negotiations",
which runs an AO/NL-style contrast directly on LLM agents) is flagged for the pre-Phase-E
freshness sweep (goal.md §1) rather than added to the cache now — it was found by an
incidental web search, not this topic's own harvest pipeline, and adding it without running
that harvest step properly would violate the same discipline this pass is enforcing.

**8. Taste audit currency — PASS, no re-audit needed.** None of this pass's fixes touch the
audited asymmetry statement (Step 0) or the Motivation/Method summary text `taste_audit.md`
evaluated — the fixes add rigor machinery (effect floors, R2 steps, confound ledger,
thin-cell rule) and one new related-work concession, none of which changes the load-bearing
verbs or framing `taste_audit.md` checked. `taste_audit.md`'s 🟢 verdict stands.

### Phase A gate result: **PASS (after fixes applied in this pass)**

All REVISE-level findings (items 2, 5, 6) were fixed directly in `digest.md`/`paper.md` in
this same pass, per the task's instruction to fix static-document gaps now rather than defer
them. Two items remain logged as **pre-Phase-E / pre-Phase-G to-dos** (not blocking this
Phase A gate, since they require either new PDF/digest construction or Phase E/F prose
edits, both out of this gate's scope): (a) build real `digest_path` files for the four
load-bearing back-filled N3 works before Phase E; (b) add `LanguageOfBargaining2023` to
`paper_draft.md`/`.tex`'s Related Work section before Phase G, and resolve the
arXiv:2601.04387 freshness-sweep flag before Phase E. No STOP-level finding. Phase B/C are
explicitly out of scope for this environment (no experiment compute) and were not attempted.
