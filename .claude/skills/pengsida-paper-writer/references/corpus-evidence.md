# Corpus Evidence

This skill's archetype taxonomy and emphasis are not guesses — they were measured against
a random sample of 28 award/outstanding papers drawn from a 36-paper catalog spanning 8
top venues (NeurIPS, ICML, ICLR, CVPR, ICCV, ACL, SIGGRAPH, and an ICLR'25 entry). The
sample, manifest, and analysis are bundled so the numbers are reproducible.

Historical calibration from the source snapshot; these numbers were not rerun by this merge. The machine-specific download/analysis harness is retained in the [original source](https://github.com/skill-stability/possible_autoresearch/tree/97cdf786bad3141c8883c7639690da867a44ded5/.claude/skills/pengsida-paper-writer/scripts).
Catalog: `scripts/corpus.json`. Sampled manifest: `references/corpus/manifest.json`.
Full analysis: `references/corpus/analysis.md`. Six representative abstracts:
`assets/corpus-sample/`.

## What the corpus showed (seed 7, n=28)

Archetype distribution among award winners:

- Method / pipeline — 46%
- Resource / foundation-model (dataset, benchmark, or broadly transferable model) — 36%
- Analysis / position / refutation — 11%
- Theory — 4%
- Efficiency / frontier (as the primary frame) — 4%

The headline lesson: the method/pipeline archetype the original skill was built around
covers fewer than half of top-tier best papers. Resource/foundation-model papers are the
second-largest group and were entirely unrepresented in the original templates. This is
why `paper-archetypes.md` is a mandatory first step, not an appendix.

Signal prevalence (share of abstracts containing the pattern; signals overlap):

- Challenge → insight framing ("however/while … we introduce") — 71%
- Resource/foundation cues (dataset, benchmark, release, zero-shot, transfer) — 64%
- Efficiency cues (faster, real-time, lightweight, efficient, scalable) — 36%
- Analysis/refutation cues ("we show that", "in fact", "rethink", "is not") — 36%
- Scaling-study cues (scaling, power-law, compute-optimal, emergent) — 29%
- Theory cues (theorem, prove, guarantee, bound, closed-form) — 21%
- Diagnosis-first cues (we observe/identify/characterize an artifact) — 7%

## How this maps to the guides

1. Abstract default stays Version 2 (Challenge → Insight → Contribution): 71% of award
   abstracts use that spine, so it is the right default — but ~30% do not, which is why the
   archetype-specific abstract moves exist.
2. Efficiency and scaling cues appear in roughly a third of abstracts even when the paper
   is primarily a method paper. That validates treating efficiency/frontier and
   scaling-study as cross-cutting *evidence types* (`experiments.md`) rather than only as
   standalone archetypes.
3. Resource/foundation cues at 64% mean transfer/zero-shot evaluation and release/
   reproducibility are mainstream reviewer expectations, not niche ones — reflected in the
   `paper-review.md` reviewer lenses.
4. Opening move: 25/28 (89%) abstracts open with task/context rather than a limitation, so
   the skill's "introduce the task first" rule is empirically sound; limitation-first
   openings are the exception (Introduction Version 4).

## Caveat

This is a modest sample of award winners, not the full population of accepted papers, and
keyword signals are approximate. Treat the percentages as direction and emphasis, not as
precise targets. Re-run the scripts with other seeds to see stability.

