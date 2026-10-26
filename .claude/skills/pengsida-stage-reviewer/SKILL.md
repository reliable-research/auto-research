---
name: pengsida-stage-reviewer
description: >-
  Stage-aware research-paper reviewer distilled from Prof. Peng Sida's (彭思达)
  learning_research notes. One skill that reviews a draft at whatever stage it is
  in — Problem+Motivation, Related Work, Method, Experiments/Ablations, or the
  writing of Intro/Abstract/Conclusion — by loading the matching stage reviewer
  from its references/ folder. Use whenever the user wants feedback on a draft,
  section, outline, experiment plan, problem statement, or motivation — even if
  they don't say "skill" or "review". Trigger on "review my method section", "is
  my motivation strong enough", "check my related work", "is this experiment
  enough", "does my intro flow", "what stage is my paper at", "critique this
  section", or any draft pasted for feedback. Classifies the paper archetype
  (method, theory, analysis/finding, position/critique, or resource) so the Method
  and Experiments bars adapt, identifies the stage, then applies that stage's
  reviewer. Complements pengsida-paper-writer (which WRITES) by focusing on
  STAGE-GATED REVIEW.
---

# Pengsida Stage Reviewer

A single skill that reviews a research paper **at the stage it is currently in**.
Each stage has its own reviewer — its own bar, checklist, and PASS/REVISE/STOP
verdict — kept as a reference file under `references/`. This `SKILL.md` is the
manager: it classifies the paper, picks the stage, loads that one reference file,
and applies it. You do not review from this file directly — you route.

Attribution: the substantive methodology is Prof. Peng Sida's (彭思达)
`learning_research` notes (https://github.com/pengsida/learning_research,
https://pengsida.notion.site), organized here into stage-gated reviewers.

## The bundle

```
pengsida-stage-reviewer/
├── SKILL.md                                  ← you are here (manager / router)
└── references/
    ├── archetypes.md                         ← classify the paper FIRST; reshapes Stage 3 & 4
    ├── writing-logic.md                      ← the 写作思路 worked example (Stages 2, 3, 5)
    ├── stage-1-problem-motivation.md
    ├── stage-2-related-work.md
    ├── stage-3-method.md
    ├── stage-4-experiments.md
    └── stage-5-writing.md
```

## Stage routing table

| Stage | What's in hand | Reference file |
| --- | --- | --- |
| 1. Problem + Motivation | a problem statement, a pitch, "why this matters" | `references/stage-1-problem-motivation.md` |
| 2. Related Work | a related-work section or positioning | `references/stage-2-related-work.md` |
| 3. Method | a method section, an approach, a system design | `references/stage-3-method.md` |
| 4. Experiments / Ablations | an experiment plan, results tables, ablations | `references/stage-4-experiments.md` |
| 5. Writing (Intro / Abstract / Conclusion) | prose drafts of the framing sections | `references/stage-5-writing.md` |

## How to run a review

0. **Classify the archetype first** (read `references/archetypes.md`). Method,
   theory, analysis/finding, position/critique, or resource. This is not optional
   bookkeeping — it changes what Stage 3 and Stage 4 are *for*. A position paper
   has no ablations; a finding paper has no pipeline; a theory paper's
   contribution lives in its definitions and theorems. State the archetype in one
   line before any stage verdict, and carry it into Stage 3/4.

1. **Identify the stage.** If the user named a section, use that. Otherwise infer
   from content: a "why this matters" pitch is Stage 1; tables and numbers are
   Stage 4; topic-sentence flow is Stage 5; etc. If the draft spans stages (a full
   paper), review the **earliest weak stage first** — a cracked foundation makes
   later polish pointless. State which stage you're reviewing and why.

2. **Load that one reference file** and follow it. Don't load all five. Stages 2,
   3, and 5 also pull in `references/writing-logic.md` for prose rewrites; Stages
   3 and 4 use the archetype column from `references/archetypes.md`.

3. **Apply the bar, not your taste.** Each reviewer ends with a PASS / REVISE /
   STOP verdict and the single most important fix. Quote the draft — point at the
   exact sentence, table cell, or claim. No abstract feedback.

4. **Return the verdict** in that stage's format, then the prioritized fixes (one
   paragraph each, most important first), then — only if the stage passes — what
   the next stage requires.

## Core operating rules (all stages)

1. **Find the right problem before judging the solution.** The most expensive
   mistakes are upstream. When in doubt, review one stage earlier.
2. **First-principles over patching.** "You combined A's x with B's y and the
   system got more complex without a real improvement" is a fatal critique, not a
   nitpick.
3. **One message per paragraph, stated in its first sentence.** The fastest
   prose-flow diagnostic.
4. **Minimum-viable evidence** is the Stage-4 bar for exploratory work.
5. **Quote the draft.** No abstract feedback.
6. Do not soften a STOP into a REVISE to be kind. A wasted direction caught early
   is a success.
7. **Archetype before bar.** Stages 1, 2, 5 are archetype-stable; Stages 3 and 4
   are archetype-sensitive. Never apply the method-paper Stage-3/4 bar to a
   theory, finding, position, or resource paper — use the matching column in
   `references/archetypes.md`.
8. **Stage 4 is one question in every archetype:** is the claimed cause isolated
   from its strongest alternative? Method → ablation; theory → discharged
   hypotheses; finding → falsification; position → counterargument rebuttal;
   resource → leakage/quality controls. Name the alternative; check it's ruled out.
