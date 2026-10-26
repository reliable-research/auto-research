# Pengsida Stage Review — B2.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before**
> final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion`
> → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`.
> Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was
> checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were
> applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf`
> already reflects them.

## Archetype classification

**Resource / dataset / foundation** (secondary: Analysis/Finding-flavored empirical demonstration).
Per `archetypes.md`'s tells ("we release/introduce a dataset/benchmark"): digest N12 explicitly
classifies this seed's contribution type as `benchmark`, not `empirical` or `dataset` alone,
reasoning that "the paired substitution *protocol* + labeled corpus form an evaluation harness for
scoring methods, not merely a static labeled dataset." `taste_audit.md`'s independent Method
Paradigm read agrees: primary **Artifact/System** ("the central deliverable... is a released,
reusable resource — the certified fault corpus and the substitution harness that manufactures it"),
secondary **Empirical Mapping** for the accuracy-characterization half, which the audit itself
flags as "a demonstration of the resource's value... not the headline." Stage 3 ("Method") and
Stage 4 ("Experiments") below use the **Resource** column of the archetype table — construction
methodology and design-decision justification for Stage 3; coverage, quality controls, and honest
baseline characterization (not "does it beat SOTA") for Stage 4 — while treating the attribution
battery as the resource's demonstration arm, consistent with `taste_audit.md`'s own framing.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test on stakes alone, before any method: "an operator
needs to know which stage to fix... and a growing line of work has proposed automated methods to
answer exactly that question... but what they do not report, uniformly, is how those numbers were
validated." The gap is first-principles, not a patch — it asks whether an entire evaluation
paradigm (human agreement, single-culprit heuristics) is even measuring the right thing, not
whether two existing pieces should be glued together. The problem is demonstrably still open: the
nearest precedent (a tracer that injects faults for training supervision) is conceded in the same
breath to fall short ("its injection targets one perturbed action... not a controlled,
taxonomy-spanning substitution protocol"), so this is not "patching and tweaking" an already-closed
question.

**Note for Stage 2:** Passing here means Related Work must establish precisely why the nearest
precedent (the fault-injecting tracer) does not already close this gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: PASS**

**Why:** Nearest-neighbor honesty is handled unusually well already — the second Introduction
paragraph names the closest work directly ("A tracer trained via reinforcement learning gets
closest: it already injects faults into successful traces and replays them to manufacture labels
by construction, the same trick this paper leans on — but its injection targets one perturbed
action...") rather than leaving four threads for the reader to rank, which is exactly the failure
`stage-2-related-work.md` flags as "buried twin." The Related Work section itself is genuinely
threaded (four named clusters: human/single-culprit validation, by-construction injection as
training supervision, benchmark reproducibility/coarse taxonomies, step-level credit assignment +
the classical fault-localization contrast), and every thread ends on a problem-tied limitation
rather than a generic one — e.g. "neither validates its own blame assignments against a controlled,
causally manufactured ground truth spanning a plan/tool/observation taxonomy, which is the gap this
paper's certification gate is built to close." Coverage matches what a reviewer in this subfield
would expect (WhoAndWhen, DoVer, AgenTracer-analog, SelfEvolveBench, Terminal-Bench, AutoLibra, CRM,
FAPO, Defects4J). No cited work already closes the gap.

---

## Stage 3 — "Method" (Resource variant: the construction methodology)

**STAGE 3 VERDICT: PASS**

**Why:** Every one of the five components states, in a `Challenge → Insight → Method` triple, which
difficulty it resolves — no orphan machinery. The load-bearing design decisions are justified
against the artifact's stated purpose rather than asserted: *what's included* (three fault
categories chosen because they mirror the three architecturally-entangled pipeline slots), *how
labeled* (certified only on outcome-flip against a matched no-op control, not on injection alone),
*how validated* ("Realism and label-unambiguity cannot be guaranteed analytically by careful
generator design; they can only be turned into a checkable empirical audit against independent
human judgment"). The one-breath summary holds: task = certify a causal failure locus; challenge =
architectural entanglement plus a substitution-induced confound; contribution = an
intervention-plus-matched-control harness; why-it-works = intervention breaks correlation, and the
no-op control measures the intervention's own false-positive rate rather than assuming it away.
This is first-principles, not patch architecture — the harness borrows individual mechanisms
(AgenTracer's inject-and-replay trick, DoVer's checkpoint-and-edit mechanism) but the load-bearing
labeling invariant (single fault ∧ observed flip ∧ no-op does not flip) is not assembled by gluing
two prior methods together with a connecting verb; no cited work enforces this specific gate.

**Note for Stage 4:** the discharge test here is coverage/quality-control/leakage, not ablation —
checked next, and this is where the first real gap in the draft surfaced.

---

## Stage 4 — "Experiments" (Resource variant: coverage, quality, and leakage controls)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** Most of the Resource-archetype checklist is already served: quality
control exists (RQ1's human-audit agreement, RQ3's no-op stochasticity bound), and baseline
characterization is honest rather than SOTA-chasing ("this is a benchmark-construction and
measurement study, and no research question here is framed as 'our procedure beats baseline X'").
But the one check this variant names explicitly — *"Leakage / contamination. For benchmarks, is
train/test (or pretraining/eval) contamination checked and ruled out?"* — was entirely absent from
the first assembled draft. The Datasets paragraph states plainly that "An existing GAIA-style
tool-use task suite supplies the base task pool," which is a **publicly released** benchmark; the
Baselines paragraph then applies a **post-hoc LLM-judge** to trajectories built on top of these
public tasks without ever asking whether the judge might already have memorized a task's correct
solution path from pretraining. That is a real, nameable alternative explanation distinct from the
compute-parity confound the budget-matched control already isolates (per Stage 4's universal
question: *is the claimed cause isolated from its strongest alternative?*) — a judge that recognizes
"this step deviates from the memorized correct trajectory" would look accurate for reasons that have
nothing to do with reasoning about the injected fault, and nothing in RQ1–RQ7 as drafted would catch
this.

**THE ONE FIX (applied):** Add a **Contamination control** paragraph to Experimental Setup (mirrored
in Metrics) that scores a held-out or paraphrased-surface-form subset of tasks separately, so an
attribution method whose accuracy collapses on that subset relative to the full corpus is flagged as
relying on memorized task familiarity rather than genuine causal reasoning — rather than leaving
public-benchmark contamination as an unexamined confound in the headline accuracy numbers.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The reverse-outline test breaks at the very first link. Reading only
each Introduction paragraph's first sentence in the original draft: (1) *"Tool-use LLM agents
increasingly carry out long, multi-step tasks that interleave a plan, an executor that acts on that
plan, and a stream of tool calls and observations that feed back into what happens next"* — pure
scene-setting, not a message; (2) *"The nearest existing work approaches this gap from adjacent but
distinct angles..."* — but "this gap" is never established by paragraph 1's first sentence, so a
reader doing the reverse-outline read hits a dangling reference at the second link. The paragraph's
actual message — that every current attribution method is validated against human judgment or a
single-culprit assumption, neither of which is causal ground truth — doesn't arrive until sentence
four ("A method can match what a human would have said... while still being wrong about which
component actually *caused* the failure"). This is exactly the **buried message** failure mode named
in `stage-5-writing.md`: "Paragraph's point arrives in sentence 4, not sentence 1."

**THE ONE FIX (applied):** Rewrite paragraph 1's opening so the message leads. Intended single
message: *"every current failure-attribution method validates blame against human judgment or a
single-culprit assumption, not a causal ground truth, so a plausible blame assignment may be
symptom-matching."* Topic-sentence rewrite: *"Every current method for assigning blame to a specific
component of a failing tool-use agent pipeline validates that blame against a human annotator's
judgment call or an assumption that exactly one step is decisively responsible — and neither of
those checks is a causal ground truth, so a plausible-looking blame assignment may be
symptom-matching rather than causally correct."* The original scene-setting sentence is kept, but
demoted to the second sentence as supporting context rather than the paragraph's lead. No other
paragraph in the Introduction, Abstract, or Conclusion fails the reverse-outline test: paragraphs
2–5 all declare their message in sentence 1 ("The nearest existing work approaches this gap...",
"Turning that forward-manufacturing idea into a working protocol surfaces its own difficulties.",
"Our approach turns each obstacle into a specific, checkable design choice.", "We evaluate this
design on tool-use tasks..."), the Abstract carries the same problem → gap → idea → result chain
without new claims, and the Conclusion names two real, specific forward-looking limitations
(compound/distributed faults; per-class rather than global certification) rather than only
recapping the abstract.

---

## Fixes applied

1. **Stage 4 fix** — added a **Contamination control** paragraph to the Experiments →
   Experimental Setup section (both `paper_draft.md` and `paper_draft.tex`), scoring a held-out or
   paraphrased subset of tasks to isolate memorized-solution familiarity from genuine causal
   attribution reasoning, and added the corresponding metric line.
2. **Stage 5 fix** — rewrote the Introduction's first paragraph so its topic sentence states the
   paragraph's actual message (no current attribution method is validated against causal ground
   truth) before the scene-setting sentence, closing the reverse-outline gap at paragraph 1.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the
review that produced them, not a pending to-do list. `paper_draft.tex` was recompiled twice with
`pdflatex -interaction=nonstopmode -halt-on-error` (exit code 0 both passes, zero `"! "` errors in
the log), `pdftotext -layout | grep -c "�"` returned 0, and the resulting `paper_draft.pdf` is 12
pages. Auxiliary build files (`.aux`/`.log`/`.out`) were deleted after compilation.

---

## Phase A (re-run)

> Run per `goal.md` §3's 8-item checklist (the runbook-canonical Phase A gate), independent of the
> Stage 1–5 `pengsida-stage-reviewer` pass above (which pre-dates `goal.md`/`guidance.md` and used
> the `auto-research-discussion` schema's own stage labels, not `goal.md`'s checklist). This section
> also incorporates the reference-cache upgrade performed the same run (`reference_candidates.jsonl`
> rewritten from a 150-row ad hoc harvest into `goal.md` §1's canonical schema; see counts below).
> Date: 2026-07-04.

**1. Digest self-verification — REVISE, fixed.** N0–N12 + Claims all present; cross-node ids
resolve (`C1–C4`, `M1–M5`, `CO1–CO3`, `RQ1`/`RQ_INF_1`, `t1–t5` all defined and consistently
referenced). Two gaps found and fixed:
- `digest.md` N1 (Problem Formulation) was tagged PARTIAL with `[HYPOTHESIS]` content for
  objective/inputs/outputs but carried no 3-part absence comment (`what_missing`/`why_matters`/
  `implication`) — every other non-`FOUND`-and-grounded node has one. Added.
- `digest.md` N12 (Contribution Type) stated a `[HYPOTHESIS]`-tagged `benchmark` classification
  with no `Status:`/`Absence comment:` block at all. Added, and cross-checked against `paper.md`
  Step 2's independently-derived archetype call (agrees: Resource/Benchmark primary, Empirical
  secondary) — noted as corroborating evidence in the new absence comment.
- Same pass caught a **tag-discipline defect inside N12's own rationale**: it cited "the PRISM
  dataset paper" as a second structural exemplar alongside Terminal-Bench, but no such record
  exists anywhere in the cache and no `paper_id`/URL was ever given — a citation from memory,
  exactly what guidance.md Part 5 forbids ("never cite from memory"). Removed; N12's rationale now
  cites only `[Terminal-Bench, OpenReview:a7Qa4CcHak]`, which *is* a verified, selected cache record.

**2. Reference-cache integrity — STOP-level gap found, fixed.** This is the headline finding of
the re-run. `digest.md` N3/N4 and `paper.md` (Step 0's contrast, Step 5's baselines, the Related
Work spine, all four Claims) are built entirely on eight real OpenReview papers (WhoAndWhen, DoVer,
AgenTracer, SelfEvolveBench, Terminal-Bench, AutoLibra, CRM, FAPO) plus the named canonical
Defects4J — **none of which existed anywhere in `reference_candidates.jsonl`**. The 150-row harvest
this topic shipped with was drawn from `arxiv_corpus/arxiv_miner_cache` (110 arXiv preprints, mostly
Dec-2025/2026 agentic-LLM papers on unrelated subtopics) and a generic `openview_corpus/paper_cache`
slice (40 ACL-Anthology-2023 papers on stance detection, calibration, KGC, essay scoring, etc.) —
an entirely different, largely off-target pool from the one that actually grounds this topic's own
digest. Per guidance.md Part 5 ("cache is thin ⇒ the harvest was inadequate, not the field empty"),
this harvest was inadequate for B2.1 specifically: only **7 of the 150** were legitimately
selectable (see Task 1 counts below), and every load-bearing baseline/method-twin the paper actually
argues against was missing from the cache entirely. **Fix:** added all 9 as new `selected` records
(`WhoAndWhen2025` baseline, `DoVer2025` method-twin, `AgenTracer2025` method-twin,
`SelfEvolveBench2025` method-twin, `TerminalBench2025` background, `AutoLibra2025` adjacent,
`CRM2025` baseline, `FAPO2025` baseline, `Defects4J2014` contrast), each with a `why` tying it to
the exact digest N3/N4 role it plays. None of the 8 OpenReview submissions have a locally cached PDF
(`pdf_path: null`, `verified.id_resolves: false`) — they were sourced from `topics/corpus/ideas.jsonl`
(structured proposal extracts, not a PDF cache) — flagged honestly rather than fabricating a path;
their OpenReview forum URLs are real and independently checkable. Every N3 key is now a `selected`
cache record; no `pending` entries remain anywhere in the 159-row file. **PASS after fix.**

**3. Tag discipline — PASS** (after the N12/PRISM fix in item 1). No other silent
`[HYPOTHESIS]`→`[GIVEN]` promotion found scanning N0–N12 and Claims.

**4. Claim–Evidence Map completeness — PASS.** `digest.md`'s four Claims map 1:1 onto `paper.md`'s
five-row Claim–Evidence Map (mechanical-validation claim → row 1/H1; substitution-isolates-cause
claim → row 2/H1+B0-a+A4; plan-vs-tool asymmetry claim → row 3/H4; reusable-corpus claim → row 4,
supported-by-design given E1; the fifth row, ceiling-gap, is a `paper.md`-only elaboration of
digest's implicit CO3 claim, correctly traced to H2+H3). Every H-id (H1–H4) has a verbatim
pre-committed fallback (E1–E4) plus F-G1 global-pivot coverage; no orphaned claim, no orphaned H-id.

**5. Hypothesis/assumption machinery — REVISE, fixed.** H1–H4 already filled all seven guidance.md
§3.1 slots (binary statement, `applies_if`, metric, test, alpha, effect floor, aggregation rule,
verbatim fallback) — verified by direct inspection of E1–E4. A1–A6 had detection methods and
(prose) consequences but **no named `PG-*` gate ids**, which `goal.md` §4 requires ("instrument
validation... runs inside B as PG-\* gates") and which the Walking Skeleton needs to reference
concretely. **Fix:** added explicit `PG-1`…`PG-6` labels to A1–A6 with an explicit *consequence*
clause per assumption (which H\*/stage it blocks, degrades, or restricts), and updated Step 9's
Walking Skeleton pass criterion to name exactly which PG-\* gates it exercises (PG-2/PG-3/PG-4) and
which are deferred (PG-1 to Stage-0's own yield count; PG-5/PG-6 to pre-Stage-2/pre-Stage-1, since
they need artifacts — a 200-trajectory audit, a public-weights check — the 20-task skeleton cannot
produce). B0-a/B0-b/B-alt/F-G1 all confirmed present with pre-committed wording, per-claim downgrade
language, and a stated pivoted abstract. **PASS after fix.**

**6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2's A3/A2 evidence standard) —
REVISE, fixed (3 items).**
- *Item 1 (R1 estimand)* — **missing entirely**; grepped `paper.md`/`digest.md` for "estimand",
  zero hits. Added an explicit Estimand paragraph to Step 5 (quantity: per-class flip rate +
  attribution accuracy; unit of analysis: one substitution trial; reference population: GAIA-style
  agent trajectories under a fixed scaffold; decision fed: whether an attribution method's blame is
  causally trustworthy).
- *Item 6 (R2 instrument validation)* — A5's human-audit protocol stated only a raw-agreement
  threshold ("<80%") without the 5-step sequence guidance.md §3.4 R2 requires, and used raw percent
  agreement rather than a chance-corrected statistic. Rewrote A5 to the full ground→draft-and-refine
  →**≥2 independent raters, κ≥0.7**→confusion-inspection (adjacent-class only)→freeze-before-scale
  protocol, matching the worked instance guidance.md cites (2607.01233's κ 0.84/0.81/0.93).
- *Item 9 (power / thin-cell rule)* — E1 stated power explicitly (>0.9 to detect a 0.20 gap); E2–E4
  did not restate a per-cell power figure or a thin-cell INCONCLUSIVE pre-declaration. Added a
  shared "Power statement and thin-cell rule" paragraph: ≥80 certified trajectories per class/method
  cell gives ≥0.8 power for a 0.10 accuracy gap via McNemar at α=0.05; any cell under that floor
  (after A3's yield gate and A5's certification filter) is pre-declared INCONCLUSIVE, never scored
  as null, per guidance.md situation 5.
- *Items 2, 3, 4, 5, 7, 8, 10* — verified PASS, no changes: verb check (taste_audit.md 🟢, no
  integrate/unify framing); all H\* 7-slot; B0/B-alt/F-G1 present; every design constraint names its
  confound (B-alt's compute-parity argument, A4's stochasticity bound, the pre-existing contamination
  control from the Stage 4 fix above); ≥1 mechanism analysis budgeted (E4's class-conditional
  confusion breakdown); archetype named (Resource/Benchmark primary) and Part 2 A3's evidence
  standard is met by the *plan* — construct validity by design (labels are the injected component,
  not inferred), contamination control (already fixed), headroom via E3, baseline sweep via E2/M4 —
  with R2/A5 now brought up to the same standard by this run's fix.

**7. Stage cross-check (advisory) — PASS, already discharged.** The Stage 1–5 `pengsida-stage-reviewer`
pass above (pre-dating this `goal.md` run) already checked N1↔Stage1, N3/N4↔Stage2, N6↔Stage3,
N8/E\*↔Stage4, and found + fixed two REVISE items (missing contamination control; buried
Introduction message), both still reflected in `paper_draft.md`/`.tex`. No new STOP surfaced on
re-check; this run's fixes (items 1, 5, 6 above) don't touch anything that pass covered.

**8. Taste audit currency — PASS, no re-run needed.** `taste_audit.md` (🟢) audited the confirmed
Stage 2/Stage 5 motivation + method. None of this run's fixes (absence comments, PG-\* gate ids,
the R1 estimand sentence, the R2/A5 protocol, the power/thin-cell paragraph, the PRISM-citation
removal) touch the asymmetry statement or the formal definition's substance — they add rigor
scaffolding around an unchanged mechanism — so the recorded audit remains current.

### Advisory observation (not a checklist item): phase-state mismatch

`discussion/paper_draft.md`/`.tex`/`.pdf` already exist, but no `B_pilot/`, `results/`,
`verdicts.json`, or `claim_map.md` exist anywhere in this topic folder. Per `goal.md`'s phase table,
Phase E's declared input is `claim_map.md` (Phase D's output), which does not exist here — so
despite the filenames, `paper_draft.*` cannot be genuine Phase E/F output. Inspection confirms they
are in fact honest: every Result in `paper_draft.md` is an explicit
`*[placeholder — fill in after experiments are run]*`, and the file's own header states "Status:
specification / paper draft — no experiments have been run. All numbers below are pre-registered
design targets, not results." No fabricated numbers were found. They are best understood as an
elaborately-formatted prose extension of `paper.md`'s own pre-registered Steps 6–9, produced by the
prior `auto-research-discussion` run — not verdict-backed output. **Per `goal.md`'s resumability
rule, the correct resume point for this topic remains Phase B (walking skeleton)**, regardless of
these files' presence; they should not be mistaken for a completed Phase E–I run, and no experiment
compute exists in this environment to advance past Phase A now.

### Task 1 counts (reference-cache upgrade)

150 originally-harvested candidates reviewed individually (digest skimmed for every one): **7
selected** (`TriangulationAs...` background, `AIGenerated...` adjacent, `ROADReflective...` adjacent,
`DynaFixIterative...` contrast, `WhenDoes...` adjacent, `AgenticSTSBounded...` adjacent,
`AgenticCode...` contrast), **143 rejected** with a paper-specific one-sentence reason each (no
`pending` left). Plus **9 records added** to close the item-2 cache-integrity gap (8 real
OpenReview papers + Defects4J, all `selected`). **Final cache: 159 records, 16 selected / 143
rejected.**

### Phase A gate result: **PASS** (after the fixes recorded above)

No remaining STOP. The one gate that opened as STOP-level (item 2, reference-cache integrity) is
resolved by the cache rewrite. Ready to resume at Phase B whenever real experiment compute is
available; this run stops here per its own scope (no B/C compute in this environment).
