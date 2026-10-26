---
name: research-taste-auditor
description: >-
  Audits a paper's core idea (motivation + method) for "LLM research taste" —
  the measured tendency of LLM-generated ideas to cluster around generic
  bridge-then-synthesize framings instead of sharper, mechanism-level moves
  (replace, decouple, formalize) that dominate published human ideas, per
  Chen, Zhao & Cohan, arXiv:2607.01233. Classifies the idea on a two-axis
  Opportunity-Pattern / Method-Paradigm taxonomy, scores surface-stitching /
  bottleneck-specificity / boilerplate, flags the Bridge-Opportunity +
  Synthesis/Unification cell LLMs overproduce, and proposes a sharper
  reframe. Use for a "research taste audit," "idea taste check," "does this
  sound LLM-generated," pre-submission idea sanity-checks, or after heavy
  LLM-co-writing. Trigger proactively whenever a paper draft, abstract, or
  motivation+method pair is pasted for review, even without the word
  "audit" — a companion pass alongside pengsida-stage-reviewer and
  se-paper-reviewer, focused on idea-level authenticity rather than writing
  quality or rigor.
metadata:
  version: "1.0.0"
  status: active
  task_type: open-ended
  related_skills:
    - pengsida-stage-reviewer
    - se-paper-reviewer
    - paper-digest
    - pengsida-paper-writer
---

# Research Taste Auditor

A single-pass audit that checks whether a paper's *core idea* — not its
prose, not its rigor — reads as the kind of idea LLMs disproportionately
generate versus the kind that gets published by humans.

Attribution: the taxonomy, calibration numbers, and archetype-verb data are
from Chen, Zhao & Cohan, "Measuring the Gap Between Human and LLM Research
Ideas," arXiv:2607.01233 (2026). Full details, paraphrased, live in
`references/`.

## Why this exists, in one paragraph

The source paper gave humans and nine frontier LLMs the same small set of
prior-work abstracts and asked each to propose a new idea. Individually, the
LLM ideas often looked reasonable. But across many ideas, a specific pattern
dominated: LLMs framed the motivation as *"these two things haven't been
connected"* (Bridge Opportunity) 47–64% of the time versus 12.1% for
published human papers, and built the method around *"integrate/unify them"*
(Synthesis/Unification) 22.5–38.7% of the time versus 5.1% for humans. This
held across every model family tested, got *worse* with extended thinking
mode, and didn't improve when models saw full papers instead of abstracts.
Bridging domains isn't inherently wrong — plenty of real papers do it — but
it's the specific shape an LLM defaults to when left unchecked, so it's worth
checking for on purpose.

## When to use this vs. the other paper-review skills

- **This skill** — is the *idea itself* (the gap it claims and the move it
  makes) generic/template-shaped, or does it read as a specific, human-shaped
  contribution? Run it once per paper, early, on the core motivation+method.
- **pengsida-stage-reviewer** — is *this stage* of the draft (motivation,
  related work, method, experiments, writing) meeting its bar?
- **se-paper-reviewer** — will *reviewers* accept this on rigor, threats to
  validity, and significance?

They're complementary, not redundant. Run this one first if the idea itself
hasn't been sanity-checked yet — a beautifully written, methodologically
sound paper can still be built on a Bridge+Synthesis idea, and it's cheaper
to catch that before drafting than after.

## Procedure

### Step 1 — Extract the idea

If given a full draft (or a research report / abstract from the person's
synced-document set): pull the **Motivation** (why this gap is worth
pursuing) and **Method** (how the contribution closes it) from the
abstract/introduction and method section, 2–4 sentences each. Quote the
paper's own language where possible rather than paraphrasing it yourself —
paraphrasing before classifying can accidentally sharpen or blur the framing
you're trying to audit.

If given a motivation/method pair directly, or a title + one-paragraph pitch,
use it as-is. If the input is only a title, ask for at least a one-sentence
motivation and method before proceeding — the taxonomy needs both axes to be
observable, and guessing at method from a title alone produces noise.

If the paper has multiple RQs, audit the paper's overall/title-level
contribution first. Only decompose per-RQ if the person asks, or if the
overall framing passes but a specific RQ still feels generic.

### Step 2 — Classify on the two-axis taxonomy

Read `references/taxonomy.md` for the full seven-label definitions on each
axis, plus calibration numbers. Assign one primary label (and an optional
secondary, if the idea genuinely straddles two) per axis. Keep the axes
disjoint — a method-style concept never goes on the opportunity slot.

### Step 3 — Score the three diagnostics

Read `references/annotation-rubric.md`. Score `surface_stitching`,
`bottleneck_specificity`, and `boilerplate` (0–3 each), each backed by a
one-line justification that points at specific phrases in the text, not a
vibe.

### Step 4 — Check the dominant verb

Read `references/archetype-verbs.md`. Identify the verb that carries the
method sentence's main claim (what the method *does*). Flag if it's from the
LLM-heavy list (integrate, unify, merge, adapt, combine, leverage...) versus
neutral or human-heavy (replace, decouple, formalize, separate, isolate...).

### Step 5 — Verdict

Apply the verdict table in `references/annotation-rubric.md` and report
every condition that fires — flags can co-occur, and a 🟢 requires none of
them to fire, not just an absence of the worst one.

### Step 6 — If flagged, do the reframe (don't just flag and stop)

A 🔴 or multiple 🟡 means: find the one specific, nameable thing the method
actually changes — a brittle component, a confounded variable, an oracle, an
assumption, a step boundary, a cost term — and rewrite both sentences to lead
with that instead of the generic connecting move. `references/
archetype-verbs.md` has worked before/after examples, including one for
cross-domain method transfer specifically (a very common, entirely
legitimate move that nonetheless tends to get *written up* in Bridge/
Synthesis language by default).

Offer 2–3 rewritten motivation/method alternatives, not a lecture on why the
original was weak. If the underlying contribution genuinely *is* a synthesis
(sometimes it is — the source paper is explicit that this isn't
disqualifying), say so plainly and skip the forced reframe; instead push on
`bottleneck_specificity` and `boilerplate` to make sure that particular
synthesis is a specific, load-bearing one rather than a generic one.

## Output format

Report, in this order, kept tight (this is a diagnostic pass, not a rewrite
of the paper):

1. **Extracted idea** — Motivation / Method, quoted or lightly reconstructed,
   clearly separated.
2. **Taxonomy labels** — primary (+secondary) on each axis, one-sentence
   rationale each, tied to specific phrases.
3. **Diagnostics** — the three 0–3 scores with brief justification.
4. **Dominant verb(s)** and which archetype family they belong to.
5. **Verdict** — 🔴/🟡/🟢, all firing conditions named.
6. **If flagged** — 2–3 concrete reframed alternatives for the motivation
   and/or method sentence.

## What this skill is not

- **Not an AI-text detector.** It doesn't judge whether the prose "sounds
  like" an LLM wrote it (token statistics, burstiness, etc.) — it judges the
  *shape of the idea itsel*f, which survives even heavy human editing of the
  prose.
- **Not a rejection stamp.** A 🔴 means "this is the statistically
  overrepresented LLM template," not "this idea is bad." Bridge/Synthesis
  ideas are sometimes exactly right; the point is to make sure this one is
  specific rather than default.
- **Not a replacement** for `pengsida-stage-reviewer` or `se-paper-reviewer`
  — run this alongside them, not instead of them.
