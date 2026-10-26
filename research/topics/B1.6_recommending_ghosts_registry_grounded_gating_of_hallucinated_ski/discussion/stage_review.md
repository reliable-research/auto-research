# Pengsida Stage Review — B1.6

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and
> **before** the final `paper_draft.md` was locked in — per the pipeline order
> `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` →
> assemble/finalize. The pengsida stages map onto the autoclaude stages as: Stage 1
> (Problem+Motivation) ← autoclaude Stage 1+2; Stage 2 (Related Work) ← autoclaude Stage
> 3; Stage 3 (Method) ← autoclaude Stage 5; Stage 4 (Experiments) ← autoclaude Stage 6;
> Stage 5 (Writing) ← the first assembled draft of `paper_draft.md`. Three REVISE findings
> fired and were applied (see "Fixes applied" at the end); the draft now in
> `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding** (empirical intervention study). Per `archetypes.md`'s tells: the
core question is "we measure whether, and under what conditions, a specific intervention
changes a specific downstream outcome" — there is no new pipeline pitted against baselines
to *win*; the trajectory harness + provenance gate + recurrence-seeded adversary are the
*analytical apparatus* that makes the intervention's effect observable, and the base
paper's four published defenses are reference markers on a shared plane, not competitors.
This matches digest N12's own `empirical` classification and `study_type: empirical` from
autoclaude Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below therefore use the
**Analysis/Finding** column of the archetype table (apparatus-is-licensed;
finding-is-falsification-tested), not the default method-paper bar (pipeline; ablations-
beat-baselines).

*Hybrid note:* there is a secondary Resource flavor (the harness + probe set + registry
snapshots are release artifacts, contribution CO1). Per `archetypes.md`, the dominant
archetype's bar is run and the secondary's Stage-4 check (leakage/quality controls for the
released instrument) is added as a lighter pass — folded into the Threats to Validity
construct/external checks below.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why (quoting the confirmed outputs):** The problem clears the "so what" test before any
mechanism appears. The root framing is a first-principles asymmetry, not a patch: "all four
[base-paper] defenses ... intervene on the recommendation distribution ... which is exactly
why they collapse recall," and the stakes are concrete and current (a confirmed squatting
attack precondition with a demonstrated end-to-end PoC, and a base paper that *explicitly
calls for* the missing intervention without building it). The Einstein ratio holds — the
motivation is spent on why the recommendation-time intervention point is the wrong one and
why existence-checking is defeated by squatting, not on the cleverness of the gate (which
is deliberately trivial: check a publisher tier). Importantly, the study_type gate was
itself *earned* in the Stage-1 critic round, not assumed: the draft objective's "beats the
four defenses" framing was caught as an outcome-tier conflict and reframed to measurement,
which is what keeps this an honest empirical study rather than a thin method paper (the
exact risk digest t1/N2 flag).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has
already closed this exact gap — and in particular must confront the nearest neighbor
(HallucSkills), which proved the phenomenon. Checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The four thematic threads are genuinely threaded
(each ends on a problem-tied limitation — e.g. the tool-grounding thread closes on "[these]
assume the tool set is fixed, known, and trustworthy by construction, the exact assumption
[the base paper] shows is false for open registries"), which clears the citation-dump
failure mode. But the nearest neighbor is the single most dangerous thing to under-play here:
HallucSkills (arXiv:2607.12340) is not just adjacent — it *proved the phenomenon, the attack,
the detection failure, and the defense collapse*, and its own closing sentence calls for the
very thing this paper builds. The Stage-2 bar is explicit: "Hiding the method-twin is the
fastest way to a desk reject ... reviewers find it anyway; confront it first." The
autoclaude Stage-3 trace *did* the concede-and-differentiate work (it set
`threat_to_motivation: high` and recorded the exact delta), but the first assembled Related
Work prose opened straight into the four threads without a single up-front sentence stating
"the closest prior work is X; here is precisely what it did and what we do that it did not."
A reader of the draft alone has to reconstruct the nearest-neighbor delta from the threads.

**THE ONE FIX (applied):** Add an explicit nearest-neighbor sentence to the Related Work
opening that names HallucSkills as the closest prior work, concedes what it established
(phenomenon + squatting attack + coin-flip detectability + recommendation-time defense
collapse + single install PoC), and states the precise delta plainly (install-time vs
recommendation-time intervention point; provenance vs existence/name signal; a
trajectory-embedded operating-point + detection-timing measurement it never ran).

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** For an Analysis/Finding paper the bar is that
*each construct is defined precisely before it is used* and *each inferential step is
licensed* — no "named after the fact," no orphan machinery. Most of the apparatus clears
this: the gate's provenance-only verdict is defined before the block-rate claim invokes it,
and the load-bearing hinge (a squatted skill satisfies "exists" but not "verified/known
publisher," so existence-gating cannot be the defense) is stated explicitly and tested by
the existence-placebo, rather than asserted. But the gate has a **third verdict —
`human-review`** — that is defined operationally (route an unknown-publisher, no-other-signal
skill to a human) yet is then *used* in the operating-point accounting (the (block-rate,
legitimate-reject-rate) plane, and RQ2's reject-rate axis) **without ever stating how a
`human-review` outcome maps onto either axis.** Is a legitimate skill routed to human-review
counted as a reject (usability cost incurred) or not (deferred, no cost)? Is a squatted skill
routed to human-review counted as blocked or not? This is an undischarged definitional step
in the very instrument whose readings the finding depends on — the Analysis/Finding analogue
of orphan machinery, and it materially changes the reject-rate number RQ2 reports and
compares to the base paper's ~84%.

**THE ONE FIX (applied):** Before the operating-point accounting uses it, pin down the
`human-review` verdict on *both* axes: a `human-review` outcome on a legitimate probe skill
counts as a **reject** for the conservative (worst-case usability) reading of the reject-rate
axis and is *also* reported separately as a deferred-not-rejected count, so the reject rate is
given as a bounded interval [block-only, block-plus-review] rather than a single number that
hides the human-review policy; a `human-review` outcome on a squatted skill counts as
**blocked** (the install did not proceed autonomously), since the security claim is about
autonomous auto-install, not about whether a human later approves. Both conventions are stated
where the gate is defined, before any RQ invokes them.

**Note for Stage 4:** the discharge test here is not ablation (that is the method-paper bar)
— it is whether the finding is falsification-tested, not merely reported. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The one question this stage asks in every
archetype — is the claimed cause isolated from its strongest alternative — is well served
structurally. The existence-placebo RQ is a genuine falsification control (it constructs the
case where, if "provenance is doing the work" were false and mere existence-checking sufficed,
the result would differ — and predicts existence-gating blocks ~0% of squatted installs); the
LLM-ablation RQ rules out the alternative that the block rate needs a model judgment; the
delayed-gate control isolates timing from task difficulty. But the first assembled draft's RQ
subsections stopped at an "Expected outcome" for several RQs without stating the converse —
the specific observation that would *refute* each expectation. Per the Analysis/Finding bar,
"the strongest finding papers construct a case where, if the claim were false, the result
would differ ... demand at least one such test" *stated as a check, not implied*. An "Expected
outcome" alone reads as a hope; a stated falsification condition is what makes each RQ a
pre-registered, breakable claim — and the underlying discussion trace (Stage 5 hypotheses,
digest N9 falsification clauses) already carries this discipline, which did not fully survive
into the first assembled prose.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ
subsections, stating the concrete statistical observation that would refute each expected
outcome (not a vague negation) — sourced from digest N9's per-RQ FALSIFICATION CONDITION
clauses and the Stage-5 hypotheses' effect floors. Also surface the **replication gate** (the
pre-run check that the harness reproduces the base paper's 36.0–43.1% hallucination rate)
explicitly in the Experimental Setup as a walking-skeleton pass criterion, since it is the
placebo-equivalent whose failure invalidates every downstream arm.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why (quoting the assembled draft, after the Stage 2–4 fixes):** Reverse-outline test passes
— reading only each Introduction paragraph's first sentence ("Autonomous LLM agents now
recommend and auto-install skills from open registries..." / "A just-published security study
settles the phenomenon but leaves one intervention point unexamined..." / "The nearest
existing work approaches this from adjacent angles..." / "Turning this into a measurable
question surfaces its own difficulties..." / "Our approach turns each obstacle into a specific
design choice..." / "We evaluate this across...") reconstructs the whole five-move arc (problem
→ gap → nearest work's shared limitation → why it is hard → the approach → the evaluation)
without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is
used consistently in title, abstract, and intro: the checkpoint is moved from *what the model
may say* (recommendation-time) to *what the agent may install* (install-time), and the signal
from *does this name exist* to *is this publisher trusted*. The Conclusion names a real
forward-looking limitation (the legitimate-first-time-publisher reject rate cannot be driven
to zero on provenance alone until trust accrues, and the single-sweep adversarial-retargeting
question is left open) rather than only recapping the abstract. The empirical study_type is
respected throughout the framing — no sentence claims the gate "beats" a defense; every claim
is about a measured operating point, its timing dependence, or a falsification control.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work opening,
   naming HallucSkills (arXiv:2607.12340) as the closest prior work, conceding what it
   established and stating the install-time/provenance/trajectory-measurement delta plainly,
   rather than leaving four parallel threads for the reader to rank.
2. **Stage 3 fix** — defined the gate's `human-review` verdict on both operating-point axes
   *before* the accounting uses it: on a legitimate probe skill it counts as a reject for the
   conservative reject-rate reading and is also reported as a separate deferred count (so the
   reject rate is a bounded interval, not a single hidden-policy number); on a squatted skill
   it counts as blocked (no autonomous auto-install). Reflected in the Methodology
   (provenance-gate subsection) and in RQ1/RQ2's metric definitions.
3. **Stage 4 fix** — added a **Falsification condition** line to all seven RQ subsections (both
   `paper_draft.md` and `paper_draft.tex`), and surfaced the replication gate explicitly in the
   Experimental Setup, then recompiled `paper_draft.pdf`.

All three fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records
the review that produced them, not a pending to-do list. No fix touched the asymmetry statement,
the formal problem definition, the archetype classification, or any pre-registered
hypothesis/falsification wording; each closes a positioning or definitional gap the stage bar
surfaced, without strengthening any claim. `taste_audit.md` (🟢) remains current — none of the
three fixes touches the audited Motivation or Method sentences.
