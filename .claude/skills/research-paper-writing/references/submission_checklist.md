# Submission Checklist

The hours before a deadline are when the most expensive mistakes get made. This file is two checklists: one to run a few days out, one to run in the final hours.

## A few days before submission

These items take time to fix and will torpedo the submission if missed.

### Story and contribution

- Read the abstract, introduction, and conclusion in sequence. Do they tell the same story?
- Does the introduction state the contributions in a numbered or bulleted list near the end? Are they sharp and falsifiable claims?
- Do the experiments map cleanly to the contribution claims? Each contribution should have at least one experiment supporting it; each major experiment should be in service of a contribution.
- Is there an ablation for each major component you propose? If you propose three things, you need three ablations.

### Related work

- Have you cited the obvious recent papers in the area? Look at the reference lists of three recent papers on closely-related topics; you should overlap heavily.
- Are there papers you intentionally didn't cite for tactical reasons? Reconsider — reviewers often catch these and view them harshly.
- Is the related work section organized by theme, not by chronology?

### Methods and reproducibility

- Are all hyperparameters reported? (In an appendix is fine, with a clear pointer.)
- Is data described — sources, splits, sizes, preprocessing?
- Is code being released? If yes, is the link in the paper or in supplementary? Is anonymization handled correctly for blind review?
- Compute resources: GPU types, training time, total cost. Reviewers increasingly expect this for transparency.

### Results

- Are baselines reproduced fairly? "We ran their code with default hyperparameters" is a common but legitimate criticism — give baselines the same care you give your method.
- Are confidence intervals or standard deviations reported for noisy metrics?
- Is the comparison protocol identical across methods? (Same evaluation script, same splits, same metric implementation.)

### Figures and tables

- Does each figure tell one clear story?
- Is each figure mentioned in the body text?
- Is the order of mention in the body the same as the order in which figures appear?
- Are font sizes large enough to read at print size? (Take a printed copy and look at it.)
- Are tables clear about what's being compared? Bolded numbers are actually the best?

### Writing

- Topic sentences at paragraph starts.
- No connectives that fake structure (no "First… Last but not least" if there's no real ordering).
- Every assertive claim has a citation or evidence.
- No undefined acronyms or symbols.
- Section headings use consistent capitalization (all title case, or all sentence case — pick one).

## In the last few hours

These are the items that catch desk rejections and embarrassing errors. They're tedious but they save the submission. Reproduced and slightly expanded from the WritingAIPaper checklist:

### Page limit and formatting

- **Page count is correct.** Going over the limit is the most common cause of desk rejection — venues often won't let you submit with extra pages. Do not assume the venue's LaTeX template enforces this; check manually.
- **The right LaTeX style file is in use.** Submitting with last year's style file or another venue's style file is a way to get desk-rejected.
- **Margins, font sizes, line spacing match the venue's specification.** Some venues have strict requirements and will reject for compliance.

### Anonymity (if blind review)

- **Author names removed.** Title page, headers, footers, footnote markers all checked.
- **Acknowledgments section either removed or replaced** with a placeholder ("Anonymous").
- **Self-citations are written in third person.** "[Smith et al., 2023] showed X" is acceptable; "In our previous work [Smith et al., 2023] we showed X" reveals authorship.
- **Code/data links are anonymized.** Use a service like anonymous.4open.science, or ensure the GitHub repo doesn't reveal identity. Check supplementary material too.
- **PDF metadata** doesn't reveal authorship. Some PDF tools embed author info silently; sanitize before submission.

### Numbers and consistency

- **Cross-reference all the numbers in the paper.** The number in Table 3 matches the number in the abstract matches the number in the conclusion. This kind of inconsistency is one of the most common errors and one of the worst-looking.
- **Equations are complete.** Equations are easy to break during last-minute editing — a missing closing parenthesis, a stray symbol, an unfinished derivation.
- **No `??` in the rendered PDF.** A `??` means an unresolved `\ref` or `\cite` — usually indicates a removed label or a typo in a key.

### LaTeX cleanups

- **Search for `??` in the PDF.** As above.
- **Search for "TODO," "FIXME," "XXX," "[CITATION]," and similar placeholders.** Authors often leave these in and don't catch them.
- **Search for question marks more broadly** — sometimes things like `Section ?` slip through with subtler variations.

### Captions and references

- **Captions are noticeable, grammatically correct, end in periods.** Captions are highly visible and reflect overall care.
- **All charts, tables, and figures are mentioned in the main text.**
- **The order of mention in the text matches the order they appear** in the document.

### Floats and overflow

- **No figures or tables outside the main body** (unless explicitly designed for an appendix).
- **No content overflowing the margins.** Look for long URLs, long equations, wide tables; these often overflow without warning. Use `\sloppy`, `\seqsplit`, or restructure.
- **Page breaks aren't ugly** — no orphaned section headings at page bottoms, no widows/orphans on key paragraphs.

### Final compilation

- **Vectorize all charts.** No PNG screenshots of plots that should be vector graphics.
- **Final PDF is the version you intend to submit.** Compile fresh, don't submit a stale build.
- **Open the final PDF in at least two readers** (Acrobat and a browser, say). Sometimes fonts or graphics render differently.
- **Print-preview at actual size.** Even if you don't actually print, the print-size view is closer to how reviewers will see it than your zoomed-in editor.

### Submission portal

- **All required fields completed** in the submission portal — abstract, keywords, conflict declarations, supplementary material upload.
- **Conflicts of interest declared correctly.** Most venues require listing institutional and personal conflicts; missing these can cause review-assignment problems.
- **Supplementary material uploaded** if applicable, and matches the version of the paper.
- **Test the submission well before the deadline.** Portals get slow or break in the final 30 minutes before deadline at major venues. Submit a complete-but-improvable version 6+ hours before deadline; refine and resubmit if the venue allows revisions.

## Camera-ready additional items

If the paper is accepted, the camera-ready pass adds:

- Reviewer-requested revisions incorporated (as much as feasible).
- De-anonymization: author names, affiliations, acknowledgments, self-citations restored to first person where appropriate.
- arXiv version updated (if applicable).
- Copyright forms signed.
- Final formatting per the camera-ready instructions (sometimes different from initial submission — extra page allowed, etc.).

The temptation to add a lot of new content for camera-ready is strong; resist it unless reviewers asked for it. The accepted paper is the contract; substantial additions can confuse readers comparing the published version to the openreview version.
