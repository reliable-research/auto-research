# Paper Structure

A paper is a nested set of expansions of the same story. Each level — abstract, introduction, main body — should be self-complete. A reader who reads only the abstract should know what you did. A reader who reads only the introduction should know why and how. A reader who reads the body should know enough to reproduce or evaluate the work.

## The three-level structure

1. **Abstract** (~150-250 words): The paper compressed. Problem → approach → key result → why it matters. Every word counts.
2. **Introduction** (1-2 pages): The paper's pitch. Contains the "page one figure" if you have one.
3. **Main body** (Methods, Experiments, Discussion, etc.): The full story with evidence.

Each level is an expansion of the previous one. They tell the same story, just at increasing detail. If your abstract claims something the body doesn't support — or vice versa — you have a structural problem.

## IMRaD: the standard scientific structure

Most empirical papers follow some version of IMRaD:

- **Introduction** — what's the problem, why does it matter, what did you do
- **Methods** — how you did it (in enough detail for reproduction)
- **Results** — what you found (without interpretation creeping in)
- **Discussion** — what it means, limitations, future work

AI/ML conference papers typically expand this slightly:

```
Abstract
1. Introduction
2. Related Work
3. Method (or Approach)
4. Experiments
5. Discussion / Analysis
6. Conclusion
References
Appendix
```

Theoretical papers may invert: theorem statement → proof sketch → details.

## Swales' three moves: how to structure an introduction

This is the canonical model from English for Academic Purposes, and it's the one cited in the WritingAIPaper handbook. An effective introduction has three moves:

### Move 1: Establish a research territory

Show that the general area is important, central, or interesting. One paragraph, sometimes two. Not a history lesson — a positioning paragraph.

> *"Image generation models have advanced rapidly since the introduction of diffusion methods, with applications ranging from creative tools to scientific visualization."*

### Move 2: Find a niche

Indicate a gap in prior work or extend prior knowledge. This is where you set up the problem your paper solves.

> *"However, existing methods produce artifacts when conditioned on out-of-distribution prompts, and the cause has not been characterized."*

### Move 3: Occupy the niche

This is the densest move and contains most of your work. It typically includes:

- a. **State the purpose** — what your paper does
- b. **List research questions or hypotheses** — what you investigated
- c. **Announce principal findings** — your main results
- d. **State the value** — why someone should care
- e. **Indicate the structure** — "The remainder of this paper is organized as follows..." (optional and increasingly out of fashion in AI venues)

### Practical introduction tips

- **Cut to the chase.** Novel parts should appear as early as possible. The first paragraph can hint at the contribution; by the end of page one, the reader should know what the paper claims.
- **Dedicate space proportional to novelty.** Spend more space on what's original; spend less on what's standard background.
- **Respect prior work.** Affirm historical contributions before identifying their limitations. "X established the foundation for Y; we extend this by..." reads better than "X is limited because..."
- **Use a "page-one figure"** if you can. A figure that captures the key insight, sitting on the first page, gives time-pressed reviewers a hook.
- **Keep the reader uppermost in mind** (Knuth). Every sentence should be earning its place against the reader's attention budget.

## Related Work: what to write and what not to

The mediocre approach is to recite a chronological history of the field. The better approach is to organize the section around how prior methods relate to *what you're doing*.

Tactics:

- **Pick 3-4 themes** most relevant to your paper. Group prior work under those themes, not by year.
- **Don't list flaws of other methods.** Explain how you build on, improve, or differ from them. "X established Y; we extend this by Z" beats "X has limitations A, B, C."
- **Be careful with priority claims.** Calling someone a "pioneer" is a factual claim; check it. When uncertain, look at how their own paper frames itself, or how the field's review papers frame it.
- **Write a venue-neutral literature review first**, then rewrite it to position your specific paper. The first pass is for understanding; the second is for argument.

## Methods: write so someone can reproduce

The methods section is not a place for prose elegance. It's a place for precision. Anyone with the same starting point should be able to follow your description and produce the same artifact.

- Provide complete hyperparameters (or relegate to an appendix and reference it).
- Specify data — sources, splits, preprocessing, sizes.
- Specify the comparison protocol — what you ran against, with what budget, on what hardware.
- Define every symbol when introduced. Don't expect readers to remember.

## Results / Experiments: structure around contribution claims

Each subsection of results should map to a specific contribution claim from the introduction. If your introduction promised three things, your results section should have three corresponding pieces of evidence.

- **Tables for primary comparisons.** Bold the best numbers per column or row.
- **Figures for trends, distributions, ablations.** Don't make a table do a figure's job.
- **Ablations are not optional.** If you propose three components, you owe an ablation that isolates each one.
- **State what each experiment shows in the prose.** Don't make the reader figure it out from the table alone.

## Discussion: be honest about limitations

A discussion section that doesn't mention any limitations triggers reviewer suspicion. Acknowledge what your method doesn't do, where it might fail, and what's left for future work. This is not a sign of weakness — reviewers respect papers that show clear thinking about boundaries. Hiding limitations is what gets papers rejected; surfacing them is what gets them accepted.

## Conclusion: brief, no new content

A conclusion is not a second abstract. It's a short reflection: here's what we did, here's why it matters, here's where it could go. A few paragraphs is plenty. Don't introduce new claims, results, or terminology in the conclusion — every claim should already have appeared in the body.

## A note on iteration

It is normal — and good — to write the introduction last. Once the body is solid, you know what you actually claim, and the introduction practically writes itself. Drafts that start by polishing the introduction often produce papers where the introduction over-promises and the body under-delivers. Write the body, then write the introduction to match it.
