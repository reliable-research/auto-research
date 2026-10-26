# research-taste-auditor

A **single skill** that audits a paper's core idea — not its prose, not its
rigor — for "LLM research taste": the measured tendency of LLM-generated
research ideas to cluster around generic bridge-then-synthesize framings
rather than the sharper, mechanism-level moves that dominate published human
ideas.

Grounded in Chen, Zhao & Cohan, "Measuring the Gap Between Human and LLM
Research Ideas" (arXiv:2607.01233, 2026), which found that across nine
frontier LLMs, ideas framed as "connect two disconnected literatures" and
built by "integrate/unify" occur 4–8x more often than in published human
papers on the same literature-grounded ideation task — a pattern that
*worsened* with extended thinking mode and didn't improve with richer
context.

## Structure

```
research-taste-auditor/
├── SKILL.md                    ← the only skill: extract → classify → score → verdict → reframe
└── references/
    ├── taxonomy.md              ← the 7+7 Opportunity Pattern / Method Paradigm labels + calibration numbers
    ├── annotation-rubric.md     ← 0-3 diagnostic scoring (surface_stitching, bottleneck_specificity, boilerplate) + verdict table
    └── archetype-verbs.md       ← LLM-heavy vs. human-heavy verb lists + before/after reframing examples
```

## How it works

Given a motivation/method pair (or a full draft to extract one from), the
skill (1) classifies the idea on both taxonomy axes, (2) scores three local
specificity diagnostics, (3) checks the dominant verb of the method sentence
against archetype-frequency data, (4) combines these into a verdict
(🔴 classic LLM template / 🟡 specificity risk / 🟢 human-shaped), and (5) if
flagged, proposes 2–3 sharper, mechanism-level rewrites rather than just
naming the problem.

The two signals it checks are independent by design: a locally
well-written, specific-sounding idea can still land in the overrepresented
Bridge+Synthesis cell, and a Bridge/Synthesis-labeled idea isn't automatically
weak if it's mechanism-specific. The skill reports both rather than
collapsing them into one score.

## Relationship to other paper-review skills

Run this **before or alongside**, not instead of:
- `pengsida-stage-reviewer` — stage-gated bar (motivation/related
  work/method/experiments/writing quality)
- `se-paper-reviewer` — SE-venue reviewer panel (rigor, threats to validity,
  significance)

This skill answers a narrower, upstream question: is the idea itself
template-shaped before you've invested in writing it up well?

## Installation

Drop the `research-taste-auditor/` folder into your skills directory. It has
no nested skills and no scripts — everything is Markdown reference material
loaded on demand.

## Attribution

Taxonomy, calibration statistics, and archetype-verb frequency data: Chen,
Z., Zhao, Y., & Cohan, A. (2026). *Measuring the Gap Between Human and LLM
Research Ideas.* arXiv:2607.01233. All category definitions and worked
examples in this bundle are paraphrased, not quoted, from that paper.
