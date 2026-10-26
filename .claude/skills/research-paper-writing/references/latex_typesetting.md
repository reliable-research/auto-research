# LaTeX Typesetting

These are the typesetting practices that distinguish a professionally-produced paper from a draft. None of them are individually heroic; together they make the difference between something that reads cleanly and something that quietly looks amateurish.

Most of these come from the Wookai/paper-tips-and-tricks guide and are well-established community practice. Apply them when generating or editing `.tex` source.

## One sentence per line in source

Put each sentence on its own line in the `.tex` source:

```latex
This is my first sentence.
This is the second one.
And here is a third.
```

Not:

```latex
This is my first sentence. This is the second one. And here is a third.
```

This is purely a source-control concern. Diffs become readable — you can see exactly which sentence changed in a commit. Your collaborators (and your future self during revisions) will be much better off. The compiled output is identical either way.

A side benefit: when LaTeX compiler errors give you a line number, you get a sentence rather than a paragraph.

## Keep references and their numbers together

Use the non-breaking space `~` between an object name and its reference number:

```latex
Figure~\ref{fig:example} shows...
Table~\ref{tab:results} reports...
Section~\ref{sec:method} describes...
```

Without the `~`, LaTeX may break the line between "Figure" and "3", which looks unprofessional.

Better still, define custom commands once and use them everywhere:

```latex
\newcommand{\refalg}[1]{Algorithm~\ref{#1}}
\newcommand{\refapp}[1]{Appendix~\ref{#1}}
\newcommand{\refchap}[1]{Chapter~\ref{#1}}
\newcommand{\refeq}[1]{Equation~\ref{#1}}
\newcommand{\reffig}[1]{Figure~\ref{#1}}
\newcommand{\refsec}[1]{Section~\ref{#1}}
\newcommand{\reftab}[1]{Table~\ref{#1}}
```

Then in the body: `\reffig{fig:example}` rather than `Figure~\ref{fig:example}`. This gives you one place to change formatting if a venue insists on, say, "Fig." instead of "Figure."

## Tables: use `booktabs`, never vertical lines

The `booktabs` package produces clean professional tables:

```latex
\usepackage{booktabs}

\begin{table}
    \centering
    \begin{tabular}{lcc}
        \toprule
        & \multicolumn{2}{c}{Data} \\ \cmidrule(lr){2-3}
        Name & Column 1 & Another column \\
        \midrule
        Some data & 10 & 95 \\
        Other data & 30 & 49 \\
        \addlinespace
        Different stuff & 99 & 12 \\
        \bottomrule
    \end{tabular}
    \caption{My caption.}
    \label{tab:label}
\end{table}
```

Rules for tables:

- **No vertical lines.** Group columns using `\cmidrule` in headers, not vertical bars.
- **Replace horizontal separators with `\addlinespace`** when you want grouping without a literal line.
- **Column heads use sentence-case capitalization**, per the Chicago Manual of Style. "Some column" not "Some Column."
- **Three horizontal rules total**: `\toprule` at the top, `\midrule` between header and body, `\bottomrule` at the bottom. Don't add more.

## Number formatting with `siunitx`

The `siunitx` package handles numbers, units, and currencies consistently:

```latex
\usepackage{siunitx}

This thing costs \SI{123456}{\$}.
There are \num{987654} people, \SI{38}{\percent} of which are male.
```

It auto-formats thousand separators, handles units cleanly, and gives you alignment in tables. To round numbers globally:

```latex
\sisetup{
    round-mode = places,
    round-precision = 3
}%
```

Then `\num{1.23456}` renders as 1.235.

For tables of numbers, declare an `S` column type, which aligns on the decimal point:

```latex
\begin{tabular}{lS}
    \toprule
    Name & {Value} \\  % S column headers must be in {}
    \midrule
    Test & 2.3456 \\
    Foo  & -6.7835 \\
    Bar  & 5642.5 \\
    \bottomrule
\end{tabular}
```

## Math notation: be consistent

Pick a notation scheme and stick to it. A common one (from Wookai's tips):

- Lowercase italic for variables: `$x$`
- Lowercase bold italic for vectors: `$\mathbold{x}$` (using the `fixmath` package)
- Uppercase bold italic for matrices: `$\mathbold{X}$`
- Uppercase italic for random variables: `$X$`

The `fixmath` package's `\mathbold` is preferable to `\boldmath` or `\bm` because it italicizes Greek letters too, giving consistent look across symbols.

**Subscripts go outside the styling.** Write `$\mathbold{x}_i$`, not `$\mathbold{x_i}$` — the `i` is an index (number), not part of the vector.

Define commands for your common types:

```latex
\renewcommand{\vec}[1]{\mathbold{#1}}
\newcommand{\mat}[1]{\mathbold{#1}}
```

If you use specific vectors and matrices a lot, define those too:

```latex
\newcommand{\vx}{\vec{x}}
\newcommand{\vX}{\mat{X}}
```

Then equations get readable: `$\vx^T \vy = \vZ$`.

**Match notation to the type, even when indexing:** the *i*th element of vector `\vx` is `x_i` (a scalar, not bold), the *i*th column of matrix `\vX` is `\vx_i` (a vector, bold), an element is `x_{ij}` (scalar). Don't write `\vX_{ij}` — that's a number, not a matrix.

## Equation environments

For inline equations, prefer `\(...\)` over `$...$`. Both work, but `\(...\)` produces clearer error messages when something goes wrong.

For displayed equations, **never use `$$...$$`**. It's a TeX construct that's been semi-deprecated for LaTeX use; it gives wrong vertical spacing and is listed in the "deadly sins of LaTeX" canon. Use `\begin{equation}...\end{equation}` (with auto-numbering) or `\begin{equation*}...\end{equation*}` (without). For multi-line aligned equations, use `align` or `align*`.

## Bibliography

Use `bibtex` or (better) `biblatex` with a `.bib` file. Pick one citation style early and stick to it; venues usually mandate a specific one (numeric for IEEE, author-year for many social science journals, etc.).

For longer documents like theses, enable back-references in `hyperref`:

```latex
\usepackage[backref=page]{hyperref}
```

This adds "Cited on page 17" annotations to each bibliography entry. Customize the wording with:

```latex
\renewcommand*{\backref}[1]{}
\renewcommand*{\backrefalt}[4]{{\footnotesize [%
    \ifcase #1 Not cited.%
    \or Cited on page~#2%
    \else Cited on pages #2%
    \fi%
]}}
```

## Capitalization

Distinguish between two cases:

- **Sentence case** — "The title of the nice book" — use for column headers, captions, sub-headings within a body section if you have them.
- **Title case** — "The Title of the Nice Book" — use for paper titles, section/subsection titles.

When in doubt, [capitalizemytitle.com](https://capitalizemytitle.com) handles title case correctly per the Chicago Manual of Style.

## A few more small rules

- Use `\dots` (or `\ldots`) instead of typing three periods.
- Use `--` for en-dashes (page ranges: `pp.~10--15`) and `---` for em-dashes.
- Quotation marks: \`\`text'' (back-tick back-tick, then apostrophe apostrophe), not "text" with straight quotes.
- Use `\@` after a period that ends an abbreviation but not a sentence, so LaTeX uses normal interword spacing. E.g., `Smith et al.\@ showed that...`
- Cite multiple references in one bracket: `\cite{ref1,ref2,ref3}`, not `\cite{ref1} \cite{ref2} \cite{ref3}`.

## Common LaTeX sins to avoid

The TUG guide *l2tabu* (linked from the Wookai tips) catalogs many anti-patterns. Highlights:

- Don't use `\bf`, `\it`, `\rm` (deprecated). Use `\textbf{}`, `\textit{}`, `\textrm{}`.
- Don't use `eqnarray`. Use `align` from `amsmath`.
- Don't load packages you don't need; each one slows compilation and can interact badly with others.
- Don't manually reformat what LaTeX is doing for you (manual line breaks, manual hyphenation, etc.) until you've exhausted the proper tools.
