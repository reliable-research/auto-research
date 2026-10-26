# Pengsida Stage Review — B2.5

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often existing attribution methods misattribute responsibility under a controlled fault mode," with no new attribution method proposed as a fix — the injector, twin-replay oracle, blinded harness, and mapping rubric are the *analytical apparatus* that makes the phenomenon measurable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "if attribution methods systematically relabel these tool-caused failures as plan or execution failures, every downstream fix they drive is aimed at a component that was never broken" is a first-principles framing (the root asymmetry between what validity checks certify and what diagnosis consumes), not a "combine A's judge with B's tracer" patch. The stakes are stated concretely (misdirected planner retraining, tool patching, or retries — real interventions these methods are already meant to drive), not a generic AI-importance appeal. The Einstein ratio holds: the first two paragraphs of the Introduction are pure problem/stakes, with zero method leak — "schema-preserving injector," "twin-replay," and "trust-license" don't appear until paragraph 5.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The three thematic paragraphs are genuinely threaded, each ending on a problem-tied limitation rather than a generic one — e.g., "AgenTracer's fault universe is agent actions, not tool returns — a tracer trained to recognize a bad action has, by construction, never seen a trajectory whose decisive error is a lying observation," which clears the "citation dump" failure mode. But the section never states, in one place, which prior works are the *closest* competitors before surveying the wider landscape. Digest N3/N4 already identified Who&When and AgenTracer as the two works closest to this paper's setting (Who&When on the attribution-method side, AgenTracer on the fault-injection/replay-verification technique side), but that ranking never made it into the assembled Related Work prose — a reader sees three parallel threads and has to infer for themselves which is the nearest neighbor. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming Who&When and AgenTracer as the closest prior work and stating the precise delta, before the three thematic paragraphs, rather than leaving the reader to rank the threads themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the corruption operator, the twin-replay decisiveness condition, and the mapping rubric are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation: the Experiments section's "Δ-trust gap" and "plan-share" both resolve to quantities already defined in the Problem Definition's formal setup). The inferential chain is licensed at its one load-bearing hinge: "Independently, μ must produce an o′_t indistinguishable from a valid observation by any surface check available to A, a property orthogonal to the twin-replay condition: a corruption can satisfy one without the other" is exactly the step that makes the injector-plus-oracle design non-redundant with a single validity check, and the draft states it explicitly rather than asserting the two-property split by fiat. No orphan components — every one of the five modules (injector, twin-replay oracle, blinded harness/trust probe, matched controls, mapping rubric) traces to a named difficulty in the Problem Definition's "Why this is hard" paragraph, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ5's design (comparing the semantic-corruption arm against a matched agent-side-fault arm carrying the *identical wrong value at a different causal locus*) is a genuine falsification design, not a correlational one — if methods correctly blame the agent-side fault but exonerate the tool-side one, the rival "subtly wrong values are just hard to spot anywhere" explanation is ruled out; if the two arms are indistinguishable, the paper's central claim fails. But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... target: at least 0.65 ... with the skew toward plan strengthening for subtle, late, numeric/stale-value corruptions" without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as an explicit check, not left implicit in the "expected outcome" framing. An expected outcome alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `pipeline.md`/`paper.md` material already had exactly this discipline (`paper.md`'s Step 6 "Fallback" clauses, e.g. F1/F2/F3) that didn't survive into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s pre-committed Fallback wording F1–F3 and the global fallback F-G1).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Multi-agent and tool-using LLM systems fail often enough... that manually reading the trajectory log... has become a bottleneck" / "Yet a central assumption behind this automation has never been tested" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this gap into a measurable claim surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific design choice rather than a hedge" / "We evaluate this design over tool-calling tasks from AgentDojo and long-horizon assistant tasks from GAIA") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and the first Contributions bullet: "validity checks certify a tool observation's form, while the diagnosis itself consumes the observation's content as an unquestioned premise." The Conclusion names two real forward-looking limitations (compounding multi-observation corruption; mapping-rubric disagreement in genuinely ambiguous trajectories) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening, naming Who&When and AgenTracer as the closest prior work and stating the delta plainly (rather than leaving three parallel threads unranked). The sentence now reads: "The closest prior work is Who&When and AgenTracer: Who&When already formalizes attribution as identifying a decisive agent-step pair from an LLM judge reading the trajectory log, and AgenTracer already trains a tracer using counterfactual replay and programmatic fault injection — but neither controls for, nor represents, the case where the log's own tool observations are corrupted yet well-formed, which is precisely the gap this paper is built to measure."
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per goal.md §3's canonical Phase-A checklist (distinct from the auto-research-discussion
> Stage 1–5 review above, which validated the *idea-construction* pipeline before drafting). This
> pass re-validates the frozen bundle — `README.md`, `digest.md`, `paper.md`, and the just-upgraded
> `reference_candidates.jsonl` — against guidance.md as the authoritative standard, per today's
> (2026-07-04) reference-cache upgrade (Task 1: 150 raw harvest hits triaged to canonical schema,
> plus 8 records added to close a cache-integrity gap described below). Phase B/C are out of scope
> for this run (no execution environment); this stops at the binary Phase A gate.

### 1. Digest self-verification — **PASS (1 REVISE found and fixed)**

Re-checked digest.md's own cross-node self-verification claim: N4→N3 `affects_works` strings all
match N3 `citation_key`s verbatim (8/8); N6 `challenge_arguments`→N5 ids (C1–C4) all resolve; N6
`mechanism_components`→N6 `key_components` (M1–M6) all resolve; `N6.unaddressed_challenges` = {C3,
C4} ⊂ N5; N8's `addresses_challenges`/`tests_contributions`/`evaluates_mechanisms` all resolve into
N5/N7/N6 respectively; N9's three `rq_id`s all exist in N8. All N0–N12 nodes + Claims present.

**Gap found:** every non-GIVEN node except N12 carries a 3-part `absence_comment`
(`what_missing`/`why_matters`/`implication`); N12 (Contribution Type, tagged `[HYPOTHESIS]` /
`source: inferred`) had `absence_comment: null` by omission, breaking the pattern goal.md §3 item 1
requires ("every non-GIVEN item carries its 3-part absence comment").
**Fixed** — added N12's `absence_comment` in `digest.md` (citing goal.md §3 item 1), explaining
that the classification is reasoned from hypothesized N7/N9 content and must be re-checked once
real results (or a released, leaderboard-inviting suite) exist.

### 2. Reference-cache integrity — **PASS (1 REVISE found and fixed, 1 residual flagged)**

**Gap found (major):** `digest.md` N3/N4 and `paper.md` (assumptions A5, H1's baseline list, the
B-alt control, the walking skeleton) all depend on 8 specific works — Who&When (GazlTYxZss),
AgenTracer (l05DseqvuD), BreakingAgentBackbones (kga18ld70t), ChatInject (WVhgFSKniL),
MCP-SafetyBench (7XYjeL46co), ResiliBench (KTZ56LG7jZ), SupervisorAgent (pzFhtpkabh), and MAST
(arXiv:2503.13657) — **none of which existed as records in `reference_candidates.jsonl`** before
today. The 150-item harvest (110 arXiv + 40 ACL-anthology, both weak-recall keyword pulls) hit zero
overlap with these 8 titles/ids; the actual related-work grounding for B2.5 has been living only in
`topics/corpus/ideas.jsonl` (a separate, differently-schematized corpus), invisible to the cache
Phase A is supposed to certify. This is exactly the failure mode goal.md §3 item 2 checks for
("every N3 key is a selected cache record").
**Fixed** — added all 8 as canonical-schema records with `verdict: selected` (relevance:
`method-twin` ×2, `baseline` ×1, `adjacent` ×3, `background` ×2, `contrast` ×1 for MAST) and a
lightweight `digest_path` reconstructed from `ideas.jsonl`'s own mined motivation+method text for
the 7 that have a corpus record (`discussion/refs_manual/*.manual_digest.md`).
**Residual gap (flagged, not blocking Phase A):** none of the 8 have a cached PDF, so
`verified.id_resolves = false` for all 8 (per the task's own rule: resolves iff `pdf_path` is
non-null); MAST additionally has no `ideas.jsonl` record at all (`digest_path: null`) and was
already self-flagged in `digest.md` N3 item 8 as content asserted from memory. **Action item before
Phase E:** re-harvest these 8 with PDF caching (goal.md §1 lifecycle step ①/②), and independently
verify MAST's content against arXiv:2503.13657 primary source before citing it again — do not let
this ride into Phase E prose uncached.
Spot-checks performed (goal.md §3 item 2): `pdftotext` on `2606.30449.pdf` and `2512.22894.pdf`
(both newly `selected` from the 150-harvest) confirmed title/abstract match the recorded metadata;
`acl_yan-etal-2023-bite.pdf` (a `rejected` record) also confirmed. A live fetch of
`openreview.net/forum?id=GazlTYxZss` was attempted but blocked by OpenReview's bot-verification
gate in this sandboxed environment — inconclusive by that channel, though independently
corroborated by the `ideas.jsonl` corpus record's own read of the paper's motivation/method text.
No `pending` verdicts remain anywhere in the 158-record cache.

### 3. Tag discipline — **PASS**

No untagged assertions found in `digest.md`; no silent `[HYPOTHESIS]`→`[GIVEN]` promotions. `N9`
keeps every quantity `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]` by construction. `paper.md`'s
Abstract v0 keeps every headline number bracketed ("[pending]") and is explicitly labeled
"WRITTEN BEFORE ANY RESULTS."

### 4. Claim–Evidence Map completeness — **PASS**

All 6 claims in `paper.md`'s Claim–Evidence Map trace to either an H-id (H1, H2/H2b, H3) or a
`supported-by-design` definition (claims 1, 2, 6); every H-id has a pre-committed fallback (F1, F2,
F3) or is covered by the global pivot F-G1; no orphans in either direction.

### 5. Hypothesis/assumption machinery — **PASS (1 REVISE found and fixed)**

H1/H2/H2b/H3 each fill guidance.md §3.1's seven slots (binary statement, `applies_if`≈Assumption
line, metric, test, alpha, effect floor, aggregation rule, verbatim fallback) — content is complete
though distributed across prose bullets rather than the literal labeled-slot template; this is a
formatting style choice, not a substance gap, and was left as-is. B0, B-alt, and F-G1 are all
present with pre-committed wording per guidance.md §3.3.

**Gap found:** the Assumptions table (A1–A7) filled only 4 of guidance.md §3.2's 5 slots —
assumption, failure_mode ("How it could fail"), detection, and gate were present, but
**`consequence`** (what happens to which H\* if the assumption fails — degrade, restrict scope, or
block) was missing entirely.
**Fixed** — added an explicit "Consequence if it fails" column to all 7 rows in `paper.md`, citing
guidance.md §3.2 and goal.md §3 item 5, distinguishing block (A1, A2 — pre-scale gates), degrade
(A3, A5, A7 — per-method/per-baseline scope narrowing), and restrict-scope (A4, A6 — task/control
coverage narrowing) consequences per assumption.

### 6. Method-rigor audit — **PASS (2 REVISEs found and fixed)**

Checked guidance.md Part 6 items 1–10 against the plan:
- Item 2 (verb check) — PASS, Step 3 already runs this.
- Item 4 (A\* detection+gate) — PASS.
- Item 5 (B0+B-alt+F-G\*) — PASS.
- Item 8 (≥1 mechanism analysis) — PASS, H3/RQ_INF_2's trust-license probe.
- Item 9 (power per cell; thin cells INCONCLUSIVE) — PASS, E2's ≥50-misattributed-cases
  pre-condition and the M5 grid's ≥15-per-cell minimum.
- Item 10 (archetype-matched evidence standard, A2) — PASS: measurement grid (M5), placebo (B0),
  rival-explanation arm (B-alt), and a power statement per cell are all present.

**Gap 1 found (item 1, R1):** no one-sentence Estimand existed anywhere in `paper.md` before Step
5's notation jumped straight into symbols — guidance.md R1 requires "quantity, unit of analysis,
reference population, decision it feeds" stated first.
**Fixed** — added an explicit "Estimand (guidance.md R1)" sentence immediately before Step 5's
Notation paragraph.

**Gap 2 found (item 7, R3):** zero occurrences of confound-naming language ("constraint X removes
confound Y") anywhere in `paper.md` — every design constraint's confound-removal function was
implicit (task-matching, operator-matching, blinding, pre-registration, model-family crossing) but
never stated as such.
**Fixed** — added a "Confound-removal ledger (guidance.md R3)" subsection after "Mandatory
baselines," naming the specific confound each of 6 constraints removes (task-difficulty,
injector-difficulty, demand-characteristic, experimenter-mapping-bias, shared-blind-spot,
trivial-majority-class).

### 7. Stage cross-check (advisory) — **PASS (advisory)**

Substantively already satisfied by the pre-existing `pengsida-stage-reviewer` pass above (Stage
1–5, with its own 2 REVISE fixes already folded into `paper_draft.*`). The stage-numbering
convention in goal.md §3 item 7 ("N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E\*↔Stage 4") doesn't
literally match `pipeline.md`'s own stage list (Stage 1 Problem, Stage 2 Motivation, Stage 3
Related Work, Stage 4 Sub-Problems, Stage 5 Method) — a cosmetic numbering mismatch between two
independently-authored conventions, not a missing cross-check: N1↔Problem, N3/N4↔Related Work,
N6↔Method/Sub-Problems, and N8/experiments↔the Experiments-section review above are all in fact
present and were all reviewed. No STOP-level finding.

### 8. Taste audit currency — **PASS**

The recorded audit in `taste_audit.md` (🟢 human-shaped, all 3 verdict conditions clear) predates
today's Task 2 fixes, but none of those fixes touched the asymmetry statement (Step 0) or the
formal definition's substance (Step 5's notation/table) — they were purely additive (Estimand
sentence, assumption-consequence column, confound-removal ledger, N12 absence_comment). No re-audit
required per goal.md §3 item 8's trigger condition ("a material edit to the asymmetry statement or
formal definition").

---

## Phase A gate result: **PASS**

All 8 checklist items cleared; 5 REVISE-level gaps were found and fixed directly in this pass (1 in
`digest.md`, 4 in `paper.md`), plus one residual non-blocking action item (re-harvest 8 cache
records with cached PDFs before Phase E). No STOP condition fired. Per goal.md §2's pipeline table,
Phase B (walking skeleton) is unblocked for whenever real execution compute becomes available; this
run does not attempt Phase B/C.

**Fixes applied in this pass (2026-07-04):**
1. `digest.md` N12 — added the missing 3-part `absence_comment` (goal.md §3 item 1).
2. `reference_candidates.jsonl` — added 8 missing method-twin/baseline/adjacent/background/contrast
   records (Who&When, AgenTracer, BreakingAgentBackbones, ChatInject, MCP-SafetyBench, ResiliBench,
   SupervisorAgent, MAST) that `digest.md`/`paper.md` already depend on (goal.md §3 item 2).
3. `paper.md` Step 5 — added the one-sentence Estimand (guidance.md R1 / Part 6 item 1).
4. `paper.md` Assumptions table — added the missing "Consequence if it fails" column to A1–A7
   (guidance.md §3.2 / goal.md §3 item 5).
5. `paper.md` — added the "Confound-removal ledger" subsection naming 6 confounds removed by
   existing design constraints (guidance.md R3 / Part 6 item 7).
