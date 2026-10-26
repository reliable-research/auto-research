# Figures and Tables

Figures are how readers consume your results. Most reviewers look at the figures before reading any prose. This file covers both the production workflow (Python/Matlab → vector graphics → LaTeX) and the presentation principles (what to include, how to caption).

## What a figure is for

A figure exists to communicate one or two things to the reader. If you can't say in a sentence what the figure tells the reader, the figure isn't ready. Common failure modes:

- **Trying to show too much.** A scatterplot with eight overlapping series, all with similar colors, is a visualization of confusion. Better to split into multiple subplots, or to make supplemental detail subordinate to a primary message.
- **Showing too little.** Two-point bar charts ("our method vs. theirs") rarely justify the figure budget. They belong in tables.
- **Forgetting axes.** A plot without labeled axes, units, or scale tells the reader nothing. Even if "the scale doesn't matter," the lack of labels makes the reader spend mental energy figuring out what they're looking at.
- **Unreadable text.** Tick labels at 6pt, legend in a corner that's clipped — these are the ones reviewers complain about explicitly.

A good rule: take a figure, shrink it to the size it'll actually appear at on the printed page, and check whether you can still read it. If you can't, fix it.

## One script per data-driven figure

Some figures are hand-made (architecture diagrams, conceptual schematics — typically in TikZ, Inkscape, or PowerPoint). Others are data-driven (plots, charts, heatmaps).

For data-driven figures, use a script. Specifically:

- One script per figure (or one script that generates a clearly-named figure when called with arguments).
- The script should be runnable with one command and produce the final figure file with no manual post-processing — no resizing in Inkscape, no cropping, no annotation.
- If the data takes longer than seconds to compute, split into two scripts: one that computes and saves the data, another that loads and plots. This way you can iterate on the visualization quickly without recomputing.

In your `.tex` file, add a comment recording the command that generated each figure:

```latex
% python figure_example.py --save ../../examples/figure/figure.eps
\begin{figure}
    \centering
    \includegraphics{figure.eps}
    \caption{...}
\end{figure}
```

When you come back six months later for a revision, you'll thank yourself.

## Consistent style across all figures

All figures in a paper should look like they belong in the same paper. Specifically: same fonts, same font sizes for axis labels and ticks, same line widths, same color palette.

The right way to do this: define the size and style in the script, not in LaTeX. Don't generate a figure at default size and then `\includegraphics[width=\textwidth]` to scale it — the result is fonts that are sometimes huge, sometimes tiny, depending on the original figure dimensions.

Use a helper module like `plot_utils.py` (Wookai's example) that exposes:

- `figure_setup()` — sets matplotlib rcParams once: font, font sizes, axis style.
- `get_fig_size(width_cm, height_cm)` — returns the right tuple for `figsize`.
- `save_fig(fig, path)` — handles tight layout, format selection, cropping.

A typical script then looks like:

```python
import matplotlib.pyplot as plt
import numpy as np
import plot_utils as pu

pu.figure_setup()

fig_size = pu.get_fig_size(10, 5)
fig = plt.figure(figsize=fig_size)
ax = fig.add_subplot(111)

ax.plot(x, y, c='b', lw=pu.plot_lw())
ax.set_xlabel('$x$')
ax.set_ylabel('$\\sigma(x)$')

plt.grid()
plt.tight_layout()
pu.save_fig(fig, args.save)
```

## Figure formats

The default reflex of "save as PDF" is not always right. The community-tested recipe:

- **Save as EPS** (encapsulated PostScript). EPS works with both `latex` and `pdflatex`, gives clean vector graphics, and embeds fonts correctly.
- **If you need PDF**, convert from EPS using `epspdf`. Matplotlib's direct PDF output has known quality issues on some platforms (loss of quality when printed on paper, even though it looks fine on screen).
- **For very-high-fidelity output** consider Matplotlib's PGF backend, but be aware the file sizes are larger.

The PDF that LaTeX gives you can have excessive whitespace margins even with `tight_layout`. Fix this with `pdfcrop`, a command-line tool that crops a PDF to its tightest bounding box.

## Rasterizing parts of a figure

If your plot has thousands of data points (a dense scatter, a heatmap), the resulting EPS can be enormous and slow to render. The fix isn't to switch to PNG (the text becomes blurry); it's to **rasterize selectively** — keep the axes and text as vectors, rasterize the data layer.

In matplotlib:

```python
ax.scatter(x, y, rasterized=True)
```

Or with layers, set a `zorder` threshold:

```python
ax.set_rasterization_zorder(0)
ax.scatter(x, y, zorder=-1)  # rasterized
ax.plot(xline, yline, zorder=1)  # vector
```

The result: small file size, sharp text, dense data still legible.

## Captions: the most-read 200 words of your paper

Reviewers and skim readers read captions before they read body text. Make the caption do work.

A good caption has:

1. **A theme statement** — what is this figure showing? (One sentence.)
2. **A key conclusion** — what should the reader take away? (One sentence.)
3. **Definitions of any abbreviations or symbols** that appear in the figure.
4. **Just enough context** that the figure could be understood without the body text.

Example:

> *Figure 3: **Accuracy improves monotonically with model scale.** We evaluate models from 100M to 10B parameters on the GLUE benchmark; accuracy (y-axis, top-1) increases consistently as parameter count (x-axis, log scale) grows, with no sign of saturation in this range. Bands show 95% CI over 5 random seeds.*

The bold theme statement isn't always conventional, but the structure — theme, then claim, then context — works regardless of format.

## Tables: structure for the comparison you want

The reader's question for any results table is "who's winning, and by how much?" Design the table so that question is immediately answerable.

- **Put compared methods adjacent.** If you compare A, B, and C, put them in adjacent rows or adjacent columns. Don't separate A and B with three other rows.
- **Bold the best result** in each comparison axis (column or row). Use a footnote to say what bolding means.
- **Repeat baselines if necessary.** If the natural layout would have a single baseline being compared against multiple groups in different sections of the table, repeat the baseline in each section. Don't make readers cross-reference.
- **Avoid scientific notation if you don't need it.** "0.0023" reads more naturally than "2.3e-3" in a table.
- **Use `siunitx`'s S column** for decimal alignment (see `latex_typesetting.md`).

## Where to place explanations

Important explanations should be physically close to the chart they explain. In LaTeX this is sometimes hard because of float positioning, but try:

- The first prose mention of a figure should ideally be on the same page as the figure.
- For a key result you're emphasizing in Table 5, the analytical sentence ("The proposed method outperforms baseline X by 4 points...") should be on the same page as Table 5, with "Table 5" appearing both before and after the analysis. Why? Many readers use PDF search ("Table 5") to find the analysis, and proximity matters for visual scanners too.
- If LaTeX float placement keeps producing bad layouts, use `[!htbp]` or `[H]` (with `float` package) to force placement, or restructure the surrounding prose to give the float a better landing spot.

## A figure-and-table review checklist

Before submission:

- Does each figure tell one clear story?
- Is every figure mentioned in the body text?
- Does the order of mention in the body match the order figures appear?
- Is every figure understandable from the caption alone?
- Are axis labels, tick labels, legend text, and any in-figure annotations large enough to read at print size?
- Are font and color choices consistent across all figures?
- For each figure, does a script in your repo regenerate it from scratch?
- For each table, is the comparison the table is making immediately visible?
- Are bolded numbers really the best ones (no off-by-one mistakes)?
- Is every abbreviation in tables and figures defined nearby?
