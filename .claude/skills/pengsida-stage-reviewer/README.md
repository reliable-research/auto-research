# pengsida-stage-reviewer

A **single skill** that reviews a research paper at whatever stage it is in.
Distilled from Prof. Peng Sida's (彭思达) `learning_research` notes.

One `SKILL.md` (the manager / router) drives the whole thing. Each stage reviewer
lives as a reference file under `references/` — not as a separate skill — so the
bundle has exactly one skill entry-point.

## Structure

```
pengsida-stage-reviewer/
├── SKILL.md                                  ← the only skill: manager / router
└── references/
    ├── archetypes.md                         ← classify the paper FIRST (reshapes Stage 3 & 4)
    ├── writing-logic.md                      ← 写作思路 worked example (Stages 2, 3, 5)
    ├── stage-1-problem-motivation.md
    ├── stage-2-related-work.md
    ├── stage-3-method.md
    ├── stage-4-experiments.md
    └── stage-5-writing.md
```

## How it works

The manager (1) classifies the paper archetype, (2) identifies the stage the
draft is in (or the earliest weak stage of a full paper), (3) loads that one
stage reference file, and (4) returns its PASS / REVISE / STOP verdict plus the
single most important fix. Stages 3 and 4 adapt their bar to the archetype;
Stages 2, 3, and 5 draw on `writing-logic.md` for prose rewrites.

## The five stages and their bars

1. **Problem + Motivation** — important? still open? first-principles, not a patch? (can STOP)
2. **Related Work** — gap earned via threaded limitations; nearest competitor confronted.
3. **Method** — every component traces to a named difficulty; archetype-variant bars for theory/finding/position/resource.
4. **Experiments** — minimum-viability (exploratory) or claim→evidence + ablations (paper-stage); one unifying question across archetypes — is the claimed cause isolated from its strongest alternative?
5. **Writing** — five-move arc, one message per paragraph, one quotable contribution sentence.

## Installation

Drop the `pengsida-stage-reviewer/` folder into your skills directory. Because the
stage reviewers are reference files (not nested skills), this installs cleanly
into a flat skills loader alongside `pengsida-paper-writer`.

## Attribution

Substantive methodology: Prof. Peng Sida's `learning_research`
(https://github.com/pengsida/learning_research, https://pengsida.notion.site).
The bars were hardened against a corpus of NeurIPS / ICLR / ICML / AAAI 2024
best & outstanding papers spanning five archetypes (method, theory,
analysis/finding, position/critique, resource).
