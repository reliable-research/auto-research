---
name: auto-research-discussion
description: Drive a research idea or codebase through a structured 6-stage workflow (problem→motivation→related work→sub-problems→methods→experiments→paper draft) using an internal critic↔refiner discussion loop, plus an optional brainstorming funnel for a rough direction with no specific topic yet. Use for a raw idea, partial draft, research question, rough direction, or code repo/project folder headed toward publication-ready outputs. Trigger on "help me develop my research idea", "run a critic-refiner loop", "polish my problem statement/motivation/methods/experiments end-to-end", "go from idea to paper draft", "write a paper from this repo", "extract the research framing from this codebase", "run autoclaude on /path/to/project", "help me find a research topic in X", "I don't have a specific idea yet, just an area", or requests naming multiple stages in sequence. Also use for partial outputs needing downstream stages built consistently. Prefer over single-shot writing when quality beats speed and iteration is welcome.
---

# Auto Research Discussion

A structured pipeline that takes a raw research idea and walks it through six tightly-coupled stages, running an internal critic↔refiner loop at each stage so the user gets a defensible, internally-consistent draft they can hand to a paper-writing skill.

This workflow (stage names, field schemas, checklist rubric, tier system) is modeled on a real research-mentorship platform: a student submits, an AI critic reviews, an AI refiner polishes, and a human supervisor approves each of the six stages before the next unlocks. In that system, only the **critic** and **refiner** are AI — the proposer is the student themselves, writing by hand. In this skill, **Claude plays proposer, critic, and refiner** within a single conversation (proposer as a convenience, so the user doesn't have to hand-draft every field), and the user plays student-and-supervisor combined. The win is structure: forcing the work into discrete stages with explicit field schemas catches the failure modes that plague research drafts (method leaking into problem statement, motivation that doesn't cover the eventual contribution, sub-problems that quietly assume a method, experiments that don't actually test the stated hypothesis).

## When to use this skill — and when not to

Use this skill when:
- The user has a raw idea or rough draft and wants to develop it through several stages
- The user explicitly asks for a critic/refiner loop or multi-round iteration
- The user names two or more stages from the list below in one request
- Cross-stage consistency matters (e.g., "my method should actually address the sub-problems")

Do **not** use this skill when:
- The user just wants a single section polished — that's a job for `research-paper-writing`
- The user has a fully-drafted paper and wants reviewer rebuttal help
- The request is purely about LaTeX, figures, or citations

If the user starts here but actually only needs one section, hand off to `research-paper-writing` mid-conversation. Don't force the full workflow on them.

## The six stages

The stages are ordered. Each stage's confirmed output is a structured object that feeds the next stage as context. Skipping or reordering breaks downstream consistency checks.

| # | Stage | What gets confirmed |
|---|---|---|
| 1 | **Problem Definition** | A clean statement of *what* the problem is — input, output, constraints, objective — with no methods leaked in. Also fixes `study_type` (technical / empirical / theory), which gates what stage 6 is allowed to ask for |
| 2 | **Motivation** | Why this problem matters: stakes, who's affected, why now, what evidence backs the claim — tied specifically to stage 1's outputs, not the topic in general |
| 3 | **Related Work** | A scouted-and-triaged landscape tier, plus a promoted deep tier where each paper gets a **problem-relative comparison** (alignment → method-addresses → effectiveness → derived threat/gap/hypothesis) that constructs the novelty position and yields the **specific limitations** this paper will exploit |
| 4 | **Sub-Problems** | Decomposition into sub-problems, each linked to a related-work limitation *or* flagged as a novel decisive component, still method-free |
| 5 | **Method Design** | Concrete methods that target specific sub-problems, each with falsifiable hypotheses |
| 6 | **Experiment Design** | Research questions tiered as mechanism / framing / outcome, matching hypotheses one-to-one (verbatim, not paraphrased) |

After stage 6, the skill assembles a paper draft from the confirmed outputs.

For the full field schema and stage-specific anti-patterns to watch for, read `references/stages.md` **before** starting stage 1 and again whenever the user jumps to a new stage. That file is the source of truth for what counts as a valid output — the field names below are simplified for this table; use the reference file's exact schema when actually drafting.

## The discussion loop (how each stage runs)

Read `references/discussion_loop.md` before running the loop for the first time in a conversation. The summary — note this has two distinct phases, not one repeating cycle:

1. **Propose** — produce v1 of the stage's structured output. If the user supplied a draft, treat it as v1; otherwise draft from the prior confirmed outputs and the user's seed idea.
2. **Critic phase (can repeat, bounded)** — review the draft against the stage-specific rubric in `references/stages.md`, checking for the named anti-patterns and for cross-stage consistency with prior confirmed outputs. Produce a `summary` plus a list of `comments` tagged with `[major]` or `[minor]` and the field they reference. The user (or Claude, in autoclaude mode) then decides each round whether to revise and go another round, or move on to the refiner.
3. **Refiner pass (runs once)** — after the critic phase ends, produce exactly one refined version, addressing what the critic flagged. The refiner is deliberately conservative: tighten wording and consistency, formalize where the content already supports it, but don't invent new content or redesign the argument. If a `[major]` issue needs more than that, that's a signal to re-propose, not to over-extend the refiner.

**Stop the critic phase — the prime rule is that a stage does not close over an open `[major]`:**
- Any `[major]` in the latest critique → automatically run another round (revise targeting each major, re-critique), tracking per-major resolution status, until majors are resolved or the round cap is hit
- Zero `[major]` flags (minors are fine — they go to the refiner or carry as notes) → move to the refiner
- The user may override with majors open — warn once concretely, then record them as `known_open_majors` in the confirmed output. No override exists in autoclaude mode
- Round cap hit with majors still open (default 5; user may set up to 50) → escalate: revise the seed, back up a stage, raise the cap, or accept with `known_open_majors`

Then always run the single refiner pass before presenting the confirmed output — even after a clean critique, since the refiner's formalization pass (e.g. tightening a `formal_summary`) is worth doing regardless of whether anything was flagged as wrong.

**Hard mode:** `references/mined_review_checks.md` holds a second, adversarial checklist layer mined from real reviewer comments on submitted papers, keyed by stage. Use it selectively (never on round 1) when the user asks for a reviewer-level review, when a nontrivial draft passes the base rubric suspiciously cleanly, or on stages 5-6 for competitive venues. The file itself explains how to pick which checks to fire.

## Modes

Pick the mode at the start of the conversation. If the user's request makes the choice obvious, just go; otherwise ask once.

- **Stage-by-stage (default)** — run one stage, present the confirmed output, wait for the user to say "next" or to edit. Best when the user wants to steer.
- **Autonomous** — run all stages back-to-back without checking in, then present everything plus the paper draft at the end. Use only when the user explicitly says "run the whole thing" or similar.
- **Single stage** — user dropped in mid-pipeline and only wants one stage. Ask them to paste the confirmed outputs of any prior stages they want used as context.
- **Autoclaude** — repo-driven self-play. The user points the skill at a code repository or project folder; Claude reads the project to extract a research seed, then runs the full pipeline as both student and teacher until the loop converges. The user only sees the final outputs (and per-round summaries if they want to follow along). **Read `references/autoclaude_mode.md` before running this mode** — repo scanning, anti-sycophancy, and how to keep the self-play honest are all covered there. Triggered by phrases like "run autoclaude on this folder," "write a paper from this repo," or "extract the research framing from /path/to/project."
- **Brainstorm** — the user has a direction but no specific problem yet ("I want to work on something in mobile testing," not an actual idea). Generate several candidate topics, scout each against the literature, compare, and promote one winner into stage 1 as its seed — don't run the six-stage loop on multiple competing ideas at once. **Read `references/brainstorm_mode.md` before running this mode.** Triggered by phrases like "help me find a research topic in X," "I don't have a specific idea yet, just an area," or "brainstorm some project ideas around Y."

## Defaults you should apply unless overridden

- **Max critic rounds per stage: 5.** Only the critic phase loops — the refiner runs exactly once after the critic phase concludes, and is deliberately conservative (polish and formalize, don't invent or redesign). See `references/discussion_loop.md` for why this split matters and how it differs from a naive repeated critique-refine cycle. Raise the critic-round cap on request, up to 50 — the user already opted into a longer ceiling than the reference platform's default; honor whatever they ask for in this range. Going above 10 is rarely productive for a single stage — flag this if the user asks for very high values, but do it if they insist.
- **What to show during the loop:** brief per-round summaries (≤3 lines: what changed, what the critic flagged, decision) plus the full final confirmed output. Don't dump every round's full draft unless the user asks — it's overwhelming.
- **Round numbering** is per-stage, not global. "Stage 4, round 3" not "round 18."
- **Stage independence in critique:** the critic is allowed — and expected — to flag inconsistencies with prior confirmed outputs. If a confirmed output from stage 2 doesn't actually match what stage 5 needs, raise it as a `[major]` and offer to back up and revise stage 2.

## Output shape

Every confirmed stage output is a structured object — see `references/stages.md` for the exact fields. When presenting to the user, render it as readable Markdown but keep the underlying structure intact (e.g., `related_works[].limitations[]` becomes a nested list with stable IDs). Stable IDs matter because later stages reference them — `sub_problem_3` must mean the same thing in stage 4 and stage 5.

## Final deliverables

A completed run produces **three artifacts**, not one:

1. **The paper draft** — sectioned Markdown assembled from the confirmed outputs. Read `references/paper_assembly.md` before generating it. If the user wants LaTeX or `.docx`, hand off to the appropriate skill (`research-paper-writing` for LaTeX patterns, `docx` for Word output) — don't do those formats inside this skill.
2. **The experiment design spec** — stage 6's confirmed output rendered as a *standalone* document: datasets and baselines with justifications, then one section per research question (tier, target hypothesis verbatim, setup, sample-size rationale, statistical test, expected outcome, metrics). This exists separately from the paper draft because it's the document the user actually executes from — it should be runnable as a protocol without opening the paper. Keep the two synchronized: if a late edit changes one, change the other.
3. **The discussion trace** — the complete round-by-round record across all stages: every draft version, every critique (all comments with severities and resolution status), every decision including user overrides and `known_open_majors`, every refiner pass. This is the audit trail that makes the confirmed outputs defensible — "we considered X and rejected it in stage 3 round 2 because Y" is rebuttal material.

In a file-tool environment, write all three as separate files (e.g. `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`) and present them together. In pure chat, present the draft and experiment spec in full, and offer the trace ("I've kept the full round-by-round trace — want it rendered?") rather than dumping it unprompted. Partial runs deliver what exists: a run stopped after stage 6 still delivers the experiment spec and the trace-so-far.

## How to start

If the user pointed the skill at a **repository or project folder** (a path, an uploaded zip, a `git clone` URL, etc.):
1. Read `references/autoclaude_mode.md` first — it covers repo scanning order and the self-play discipline.
2. Read `references/stages.md` so you have the rubrics ready.
3. Run autoclaude mode: scan the repo, extract a seed, then loop through all six stages with you playing both student and teacher. Default max rounds: 5 per stage. Show compact per-round summaries plus the final paper draft.

If the conversation has already given you a research idea, problem statement, or partial draft:
1. Read `references/stages.md` if you haven't yet.
2. Identify which stage the user is implicitly at (do they have a problem statement? a method already?).
3. State your read-back: "I see you have X confirmed and you want to start at stage Y" — give them one chance to correct.
4. Confirm mode and max-rounds (default to stage-by-stage with 5 rounds unless they specified otherwise).
5. Begin stage Y, propose v1, run the loop.

If they've just said "I want to run this skill" or arrived with a fresh idea:
1. Ask for the seed: a paragraph describing the research idea, even very rough.
2. Ask whether they want stage-by-stage (default) or autonomous.
3. Begin at stage 1.

If they only have a rough direction and no specific idea yet ("I want to work on something in X"):
1. Read `references/brainstorm_mode.md` first.
2. Run the brainstorm funnel: direction & context → generate and scout several candidates → compare → promote one.
3. Carry the winning candidate's seed into stage 1 as v1, rather than starting from a blank page.

## Things to refuse

- **Don't fabricate citations in stage 3.** If you don't actually know a paper that fits the description, say so and ask the user to fill it in, or mark it `[citation needed]`. This is the one rule the reference platform treats as a hard safety constraint rather than a quality one ("no fabrication" — don't invent facts, claims, evidence, citations, or outcomes not supported by the provided content) — it applies everywhere in this skill, not just stage 3.
- **Don't let the loop run silently for many rounds.** If the loop is going to exceed 10 rounds in a single stage, pause and ask the user whether to keep going. Long loops usually mean the rubric is wrong or the user's seed idea has a fundamental gap that more iteration won't fix.
- **Don't merge stages.** "Just write me the problem and method together" defeats the point. If the user asks for that, redirect to `research-paper-writing` instead.
