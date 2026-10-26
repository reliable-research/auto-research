# Pengsida Stage Review — B8.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor`
> (🟢) and **before** the final `paper_draft.md` was locked — per the pipeline
> order: `auto-research-discussion` → `research-taste-auditor` →
> `pengsida-stage-reviewer` → assemble/finalize. Stages 1–4 below are checked
> against the confirmed stage outputs in `discussion_trace.md`; the Writing stage
> is checked against the first assembled draft of `paper_draft.md`. **Two REVISE
> findings fired and were applied** (see "Fixes applied" at the end); the draft in
> `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification (done first, per the manager rule)

**Analysis / Finding** (empirical measurement study). Per `archetypes.md`'s tells:
the core question is "we ask whether/how often a phenomenon occurs" (do deployed
servers fall into a divergence window? how often does authority degrade to
visibility?) with **no new protocol proposed as a fix** — the differential-
conformance apparatus (matched-reference probes, non-destructive authority
observation, unchanged-clause placebo, interval-censored survival estimator) is
the *analytical apparatus that makes the phenomenon observable*, not a method
pitted against baselines to win. This matches the README's `[证据]` (evidence)
label and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4
("Experiments") below therefore use the **Analysis/Finding** column: Stage 3 asks
whether each *analytical step is licensed*; Stage 4 asks whether the finding is
*falsification-tested*, not merely correlational. Secondary archetype:
empirical-mapping *instrument* (the reusable probe-synthesis + safe-probing
harness) — its Stage-4 leakage/quality analogue (probe faithfulness on references,
RQ1) is checked as an added lens.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. The
framing is first-principles, not a patch: "a reputation channel … feeds back only
whether an episode concluded in agreement" is the *root asymmetry* here restated
for protocols — "a single-version conformance check and a static framework audit
both miss it *because it exists only between versions and only on the wire*." The
stakes are concrete (a client interoperating against an unspecified behavior; an
authority constraint un-enforced for the exposure-duration of a window) with a
real, dated environmental signal (NSA/CISA MCP CSI, 2026-06), not a generic
"AI-is-important" appeal. Importance × openness both hold: the README's own
occupancy sweep confirms no one measures *longitudinal/differential* conformance,
and AgentRFC's withheld artifact means no reproducible deployed-side check exists.
The Einstein ratio holds — the Motivation is pure problem/stakes with no method
leak (probe synthesis, survival estimation, etc. appear only in Method).

**Note for Stage 2:** Passing here means Related Work must now establish that no
prior work has already closed this exact gap — and, critically for this topic,
that the two papers owning the *authority* concept (Capability-Gates, HCP) and the
one owning the *conformance* lane (AgentRFC) are each confronted, not filed
quietly. Checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic threads are genuinely argued (each
ends on a problem-tied limitation, not a generic one — e.g. AgentRFC "certifies the
spec, not the fleet, and its artifact is withheld under coordinated disclosure"),
which clears the citation-dump failure mode, and the authority-axis repositioning
sentence conceding the concept to Capability-Gates/HCP is present (carried from the
Stage-3 self-play fix). **But the section never states, in one place, which single
prior work is *the* nearest neighbor on the *conformance* axis.** AgentRFC
(2603.23801) is the closest competitor on the paper's primary lane — it is the only
cited work that does agent-protocol *conformance* checking — yet the first
assembled draft leaves it as one of four parallel threads, so a reviewer has to
infer for themselves that AgentRFC, not Capability-Gates, is the method-twin to
beat on positioning. Per the Stage 2 bar: "hiding the method-twin is the fastest
way to a desk reject … reviewers find it anyway; confront it first." The authority-
axis repositioning handles the *security* half of the twin problem; the
*conformance* half was left implicit.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming
AgentRFC as *the* closest prior work on the conformance axis and stating the
precise delta plainly — spec-side, single-version, model-checking-with-withheld-
artifact vs. deployed-side, version-differential, longitudinal, reproducible
wire measurement — rather than leaving the reader to rank the four threads.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is *defined precisely before it is used* — the divergence
window (with its version-bracket reference frame and out-of-frame category), the
enforced/advertise-only/silent enforcement-status labels, and the changed-vs-
unchanged placebo are all given in Problem Definition / Methodology ahead of any
claim that invokes them; no "named after the fact" violation. The inferential
chain is licensed at each load-bearing hinge: (i) a probe may call a live server
"neither" *only after* it provably separates two pinned reference implementations —
this is the hinge that makes a wire "neither" a conformance verdict rather than an
arbitrary failed request, and the draft states it explicitly rather than asserting
probe validity by fiat; (ii) a "neither" is counted as *drift* only when it
exceeds a matched *unchanged*-clause placebo that cannot produce a version-induced
failure by construction — this is what licenses the causal reading over generic
non-conformance; (iii) enforcement is inferred from the *accept/deny decision at
the boundary*, which is why the non-destructive probe can witness a downgrade
without performing the unauthorized effect. No orphan components — every one of the
five modules (probe synthesis, safe probing, placebo/persistence, authority
classifier, censored estimator) traces to a named sub-problem, with no leftover
machinery. The safe-probing module in particular is not decoration: it is the
component without which authority-clause measurement on live servers is impossible
*and* the longitudinal estimator is confounded — a genuinely decisive piece the
self-play Stage-4 critic surfaced.

**Note for Stage 4:** the discharge test here is not ablation (that is the
method-paper bar) — it is whether each finding is *falsification-tested*, not
merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype —
is the claimed cause isolated from its strongest alternative? — is well-served
structurally. The strongest rival ("these 'neither' verdicts just reflect servers
that are broadly non-conformant, not drift") is isolated by a genuine falsification
design: the within-server changed-minus-unchanged contrast (RQ5) and the unchanged-
clause placebo baseline (RQ2) both *would differ* if the rival were true. And the
probe-discrimination check (RQ1) is a real instrument-validity falsification (if
the probes fail to separate the two references, the instrument is declared invalid,
not patched). **But the first assembled draft's RQ subsections stopped at an
"Expected outcome" line** — e.g. "the interval-censored median window width exceeds
the resolution floor by ≥2×" — **without stating the converse: the specific
observation that would *refute* each expectation.** Per the Analysis/Finding bar:
"the strongest finding papers construct a case where, if the claim were false, the
result would differ … demand at least one such test" *stated as a check, not
implied*. An "Expected outcome" alone reads as a hope; a stated falsification
condition is what makes it a pre-registered, breakable claim — and the machinery to
state it already exists (each Stage-5 hypothesis has a pre-committed threshold whose
negation is the falsifier).

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all
seven RQ subsections, stating the concrete statistical observation that would
refute each expected outcome (not a vague restatement of its negation) — including
the two honest-null cases that are *themselves* findings: RQ2's "changed-clause
'neither' ≤ placebo baseline" (no measurable divergence window — a robustness
certification that the ecosystem tracks versions cleanly) and RQ4's "zero
enforced→advertise/silent downgrades among authority clauses" (the security half of
the claim does not reproduce).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's
first sentence ("Agent-to-agent interoperability now runs on published protocols…"
/ "Yet these protocols are revised faster than the servers deployed against them…"
/ "The nearest existing work approaches this from adjacent angles…" / "Turning this
into a measurable question surfaces its own difficulties…" / "Our approach turns
each obstacle into a specific design choice…" / "We evaluate this across…")
reconstructs the whole five-move arc (problem → gap → prior work's shared
limitation → why it is hard → the approach → the evaluation) without needing
sentence 2 of any paragraph. One quotable contribution sentence exists and is used
consistently in title and abstract: "a deployed server transitioning across a
revision can conform to *neither* the old version nor the new one, and inside that
window an authority constraint can silently degrade from enforced to visibility-
only." The Conclusion names a real forward-looking limitation (the divergence-
window width is bounded below by sweep cadence, so the true short-window tail is
censored) rather than only recapping the abstract, and the whole draft carries no
internal stage IDs (`sp_*`, `m_*`, `rq_*`) in prose — checked directly.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit single-nearest-neighbor sentence to the
   Related Work section naming **AgentRFC** as the closest prior work on the
   conformance axis and stating the delta plainly (spec-side / single-version /
   withheld-artifact vs. deployed-side / version-differential / longitudinal /
   reproducible), complementing the already-present authority-axis repositioning
   against Capability-Gates and HCP.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven
   RQ subsections in the Experiments section (both `paper_draft.md` and
   `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file
records the review that produced them, not a pending to-do list.

---

## Writing-stage re-pass on the assembled draft (per the task's Writing bar)

After the two REVISE fixes were spliced and the draft re-rendered, one final Stage-5
pass confirmed: (a) the AgentRFC nearest-neighbor sentence did not disturb the
Related Work thread flow (it opens the section, then the four threads follow); (b)
every RQ subsection now reads Setup → Expected outcome → **Falsification condition**
→ plain-language hypothesis → Metrics → Result-placeholder, so each RQ is visibly a
breakable pre-registered claim; (c) no `[CITE]`/`[TODO]` artifacts and no internal
IDs leaked; (d) the Abstract/Contributions assert only pre-registered *tests*
("We test whether…", "We measure…"), never accomplished results, consistent with
the empty Results placeholders. No further REVISE. **Writing bar: PASS.**
