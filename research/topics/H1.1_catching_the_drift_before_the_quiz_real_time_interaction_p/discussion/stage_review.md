# Pengsida Stage Review — H1.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and against
> (a) the confirmed stage outputs in `discussion_trace.md` (Stages 1+2, 3, 5, 6) and (b) the
> first assembled `paper_draft.md` (the Writing-stage bar). Two REVISE findings fired — one of
> them caught by actually recomputing a number the draft asserted — and were applied before the
> draft was finalized; the `paper_draft.md`/`.tex`/`.pdf` you now see already reflect them.
> Date: 2026-08-15.

## Archetype classification

**Analysis / Finding** (with an experimental-intervention component; secondary tell of a
*resource* archetype is absent — the classifier and gate are analytical apparatus, not a released
leaderboard product). Rationale per `archetypes.md`'s tells: the paper asks "how early is a
phenomenon visible, and does acting on it change an outcome" — there is no pipeline pitched
against baselines to win; digest N12 classifies the contribution `empirical` ("M1's classifier …
built as instruments for this measurement, not as a leaderboard-style benchmark product"), and
Stage 1 fixed `study_type: empirical` with zero outcome-tier RQs. Stages 3 and 4 below therefore
use the **Analysis/Finding** column: Stage 3 judges whether each inferential step of the
apparatus is licensed; Stage 4 judges whether the claims are falsification-tested, not merely
correlated.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why, quoting the draft:** The problem clears the "so what" test before any mechanism appears —
"every measurement of it arrives after the fact … as long as the drift is only nameable after
the quiz, assistants can do nothing about it at the moment it matters, and the people incurring
the harm cannot see it at decision time" is a first-principles framing of a measurement/timing
asymmetry, not a patch pitch, and the stakes are concrete (a causally established 17-point
comprehension loss whose lever — the interaction pattern — is visible in behavior). The Einstein
ratio holds: Introduction paragraphs 1–3 are problem, gap, and why-it's-hard, with zero method
leak. Importance is not generic-AI appeal: the motivation's four legs each carry an epistemic
tag and a source, and the fragility of the base effect (n = 52, one lab) is owned as a design
input ("$\Delta_{\mathrm{rep}}$ is carried inside the design rather than assumed from the
literature") rather than hidden. Feasibility evidence exists at the right granularity: the
minimum-viable first check is the human prefix ceiling ("if humans cannot call the pattern from
half a session, no classifier can") — binary, cheap, and scheduled first.

**Note for Stage 2:** passing here obligates Related Work to show nobody already estimates
erosion risk at prefix time — checked next.

## Stage 2 — Related Work

**STAGE 2 VERDICT: PASS**

**Why, quoting the draft:** The nearest-neighbor sentence exists, up front, and names *two*
neighbors with the delta stated plainly: "The closest prior work is Shen and Tamkin's (2026)
skill-formation RCT — whose task, quiz rubric, labels, and two arms this design reuses and
extends — and, for the detection claim specifically, Yao's (2026) 'AI-prompt signature' …
the former labels complete sessions in hindsight and never estimates anything at prefix time,
the latter detects a signature retrospectively at cohort level without an individual-session
model or any intervention." Each of the five threads ends on a problem-tied limitation, not a
generic one (e.g., JITAI: "No JITAI work senses AI-interaction patterns or targets skill
formation"; ITS: "they model mastery of curricular skills inside purpose-built tutors"), which
clears the citation-dump failure mode. The one live novelty threat (Agents-That-Teach as a
design-principles solution to the same harm) is confronted rather than buried, with the
fallback repositioning pre-committed in the text itself ("if their designs prove adaptive on
full reading … we supply the measurement layer their adaptivity would require") — the
buried-twin failure mode is affirmatively avoided. Engagement tiers are disclosed inline (Cao &
Huang "search-confirmed but not full-text-read this cycle"), which is the honest version of
coverage rather than its absence. No cited work closes the gap (no accidental self-refutation
found on re-check).

**Minor note (not blocking):** the pre-submission reading debts (Cao & Huang; Mehra full text;
JITAI/forcing-function page details) are correctly declared in the draft and trace; they must be
cleared before any venue submission, as the draft itself states.

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why, quoting the draft:** Every construct is defined before it is used — $L_i$, $r_{ik}$, the
gate $G$, the arms, and all four estimands appear in the Problem Definition ahead of any section
that leans on them (no named-after-the-fact construct). The load-bearing inferential hinges are
stated as arguments, not assertions: (i) the prognosis reframing — "Reframing the target as
*terminal-pattern risk* turns early indeterminacy into probability mass rather than label
noise" — is exactly the step that makes prefix-time estimation well-posed against hindsight
labels, and the draft says why; (ii) the placebo logic — "matching the placebo to the active
nudge in trigger policy, timing, length, and presentation leaves exactly one difference —
whether the appended content does cognitive work" — is the step that licenses attributing an
effect to content; (iii) the pre-treatment subgroup logic — "the risk value is frozen before
any message is delivered, so flagged subgroups are defined pre-treatment in every AI arm" — is
the step that keeps the subgroup analysis causal. No orphan components: all six modules trace to
a named obstacle (risk model and ceiling harness → hindsight-to-prefix transfer; trigger →
timing; gate → small-sample authorization; nudge+placebo → wrong-reason effects; four-arm
design → fragile-baseline comparability), and nothing else is introduced.

**Note for Stage 4:** the discharge test for this archetype is falsification, not ablation —
does each claim name the observation that would refute it, and is the strongest alternative
explanation isolated? Checked next.

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(two findings fired, both fixed — see "Fixes applied")*

**Why, quoting the draft:** The falsification structure itself is strong: all eight RQ
subsections carry an explicit "Falsification condition" line stating the concrete refuting
observation (e.g., RQ8: "refuted if active does not exceed placebo … or if guardrails fail …
or if the effect appears only outside the flagged subgroup"), and the strongest alternative
explanations are each isolated by a dedicated design element (reactivity → matched placebo;
degraded-assistant → additive-only + guardrails; base-rate guessing → prevalence-anchored
margins; lucky small-sample precision → sealed exact-bound gate; fragile base effect → internal
replication with a pre-registered interpretation tree). But two defects survived into the first
assembled draft:

1. **A wrong number in the one place the paper does arithmetic.** RQ5 asserted the gate is
   "passable at, e.g., 8 alerts with 7 true positives (Clopper–Pearson 90% lower bound
   ≈ 0.63 > 0.60)." Recomputing: the one-sided 90% CP lower bound for 7/8 is **0.594**, which
   *fails* the 0.60 margin at the illustrated prevalence — the draft's own example cell is a
   no-go under the draft's own rule. The correct minimal passing neighborhood at
   $\hat{p} \approx 0.5$ is 8 of 9 alerts (LB ≈ 0.632) or 9 of 10 (LB ≈ 0.663); 8 of 8 also
   passes (LB = 0.750). In a paper whose central methodological claim is that the pass table is
   exact and pre-enumerated, an incorrect illustrative cell is precisely the kind of
   "asserted number without protocol" the design exists to forbid. (`experiment_design.md`
   carried the same wrong cell.)
2. **Sealed-set discipline contradicted by a sibling RQ.** RQ5 requires the gate set to be
   "scored exactly once," but RQ6's setup said the trigger "is replayed over gate-set sessions
   with the frozen model" — a second pass over sealed data, as written. The intent is
   unproblematic (both quantities derive from the same frozen model outputs) but the protocol
   as stated licenses re-scoring, which is exactly the degree of freedom sealing exists to
   remove. The single scoring pass must be defined to log the full per-query risk trajectory,
   with RQ6 (and the gate's own precision computation) consuming those logs — one pass, two
   pre-registered read-outs.

**THE ONE FIX (applied):** correct the RQ5 pass-table illustration to a cell that actually
passes (8-of-9, LB ≈ 0.632 > 0.60; alert-count minimum satisfied), in both `paper_draft.md` and
`experiment_design.md`; and redefine the sealed-set procedure as one scoring pass that logs
per-query trajectories, with RQ6 consuming the logs rather than re-scoring.

## Stage 5 — Writing (Introduction / Abstract / Conclusion), against the first assembled draft

**STAGE 5 VERDICT: REVISE** *(one finding fired, fixed — see "Fixes applied")*

**Why, quoting the draft:** The reverse-outline test passes — first sentences alone ("AI
assistants are now a default companion … " / "Yet a central question about this harm remains
unexamined: every measurement of it arrives after the fact" / "Two obstacles make this harder
than it looks" / "Our design turns each obstacle into a specific, pre-registered mechanism" /
"The program is deliberately serialized so that either branch of the gate produces knowledge
the field lacks") reconstruct the full arc without any paragraph's second sentence. The
conclusion earns its place (it names what the ceiling and lag measurements will *bound* for
future work, rather than recapping the abstract). The defect is in the Abstract: at ~240 words
it exceeded the 150–200 target, and its contribution move opened with the generic "We propose a
gated, two-stage causal extension of that trial" — a sentence that could introduce almost any
follow-up study — while the actual identity of the contribution (prefix-only prognosis, the
sealed prevalence-anchored gate, the placebo-controlled nudge) only assembled itself two
sentences later. Per the quotable-contribution bar, the one sentence a reader should be able to
quote was present in the body ("either branch of the gate produces knowledge the field lacks:
how early erosive drift is visible at all, or whether catching it preserves learning") but the
abstract led with scaffolding instead.

**THE ONE FIX (applied):** tighten the Abstract to ≤ 200 words and make the contribution move
lead with the specific machinery ("We answer with a gated design: a prognostic risk … a sealed
prevalence-anchored gate … a four-arm trial with matched placebo") so the quotable sentence
carries the paragraph, cutting the redundant restatement of the base trial's design details.

---

## Fixes applied

1. **Stage 4 fix 1** — RQ5's pass-table illustration corrected from the failing cell
   (7/8, LB 0.594) to a passing one (8/9, LB ≈ 0.632 > 0.60; 9/10 ≈ 0.663 and 8/8 = 0.750 also
   noted), in `paper_draft.md` and `experiment_design.md`. No pre-registered criterion changed —
   the rule was always the exact bound; only the *illustration* of it was wrong.
2. **Stage 4 fix 2** — sealed-set procedure restated in both documents: one scoring pass logs
   per-query risk trajectories; the gate criterion (RQ5) and the lead-time distribution (RQ6)
   are two pre-registered read-outs of that single pass; no re-scoring of sealed data.
3. **Stage 5 fix** — Abstract tightened to ≤ 200 words with the contribution move leading on the
   specific machinery; no claim added, none strengthened.

All three fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf`; none touches a
hypothesis, a bound, a gate criterion, or any pre-committed fallback wording — so the 🟢 taste
audit and the cross-stage consistency recount in `discussion_trace.md` remain current.
