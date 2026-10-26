---
name: research-paper-writing
description: Use whenever the user is drafting, structuring, refining, or reviewing an academic research paper — including AI/ML conference submissions (NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP), journal manuscripts, theses, or technical reports. Trigger on requests to write or improve any section (abstract, introduction, related work, methods, experiments, results, discussion, conclusion), to frame a contribution, to write reviewer rebuttals, to format LaTeX tables/figures/math/citations, to apply IMRaD or Swales' three-move introduction, to run a pre-submission checklist, or to improve readability through topic sentences, logical connectives, and information density. Also trigger on phrases like "polish this section," "is my contribution clear," "help me write the related work," "improve my paper," "is this rigorous enough," or mentions of paper deadline, camera-ready, desk reject, rebuttal, or area chair. Use even when the user does not say "skill" — paper writing is where this discipline makes real quality difference.
---

# Research Paper Writing

A consolidated skill for writing scientific and AI/ML conference papers well. It distills practices from three widely-used community resources: hzwer's *Writing AI Conference Papers: A Handbook for Beginners*, Wookai's *paper-tips-and-tricks* (LaTeX/figures), and the K-Dense-AI Scientific Writer skill catalog (IMRaD, citations, reporting standards). The aim is to help the user produce papers that are clear, rigorous, defensible, and submission-ready.

## How to use this skill

This skill covers two complementary tracks:

1. **Strategic writing** — finding the core idea, framing the contribution, structuring the narrative, anticipating reviewers. This is what separates a paper that gets read from one that gets desk-rejected.
2. **Tactical craft** — typesetting, figures, tables, math notation, references, and the dozens of small decisions that make a paper feel professional.

Most user requests touch one or the other; high-stakes requests touch both. Read the relevant reference file before responding rather than trying to recall everything from this top-level document. The references are organized so each one stands alone for the task it covers.

## Reference files — when to read each

| File | Read when the user is… |
|---|---|
| `references/core_idea_and_framing.md` | Trying to articulate their contribution, deciding what the paper is "about," worried about novelty, or stuck at a blank page |
| `references/paper_structure.md` | Drafting the abstract, introduction, related work, methods, results, discussion, or conclusion; asking about IMRaD or section ordering |
| `references/readability.md` | Polishing prose, asking why their writing feels muddled, dealing with "logical flow," topic sentences, or connective overuse |
| `references/latex_typesetting.md` | Working in LaTeX — tables, math notation, references, bibliography, custom commands, `siunitx`, `booktabs` |
| `references/figures_and_tables.md` | Creating, scripting, captioning, or critiquing figures and tables; asking about EPS/PDF, rasterization, or `matplotlib` workflow |
| `references/reviewer_response.md` | Reading review comments, drafting a rebuttal, deciding whether to resubmit, or processing a rejection |
| `references/submission_checklist.md` | In the final hours before a deadline, or doing a camera-ready pass |
| `references/venue_guide.md` | Choosing a venue, understanding AI conference timelines, or formatting for a specific journal/conference |
| `references/corpus_patterns.md` | Writing or revising an abstract or introduction. Empirically-grounded patterns extracted from a corpus of 10 award-winning papers from NeurIPS/ICML/ICLR/CVPR/ACL 2023–2025 — opening templates, named-artifact rule, two-sided structure, scoped "first" claims, anti-patterns. Read this whenever the request is "is my abstract good," "how should the intro start," "what's the novelty here," or anything else where the framing of the contribution is at stake. |

For a request that spans multiple files (e.g., "write the introduction and make the figures match"), read all relevant ones before responding rather than answering, then realizing you need more context.

## Default behaviors

When helping the user write or revise paper content, apply these defaults unless they say otherwise:

- **Lead with the contribution.** The novel and interesting parts of a paper should appear as early as possible — in the abstract, in the first paragraph of the introduction, and in the topic sentence of each section. Bury nothing important.
- **Cut the meandering history lessons.** Sections should not begin with "Since the dawn of computing…" or paragraph-long surveys before getting to the point. Get to what's new in this paper.
- **Stay defensible.** Every assertive claim ("X is critical," "Y is unsolved") needs either a citation or evidence. If the user writes an unsupported claim, flag it and ask what backs it — don't rubber-stamp.
- **One sentence per line in LaTeX source.** This is for diff-friendly version control. Apply it whenever editing or producing `.tex`.
- **Use `\reffig{...}`, `\reftab{...}` style refs**, and use `~` (non-breaking space) in raw `\ref` calls so reference numbers don't get orphaned across line breaks.
- **Topic sentences at paragraph starts.** Readers skim. Make the first sentence of each paragraph carry the main claim of that paragraph.
- **Don't use connectives to fake logical structure.** "First… Second… Last but not least" only works if there's actually an ordering. Otherwise just describe the items separately.
- **Captions are read more than the body.** Caption every figure and table with both a theme and a key conclusion. Aim for figures and tables to be understandable on their own.

## Things to refuse to do

- **Don't fabricate citations.** If the user wants a reference for a claim and you don't know one that genuinely supports it, say so. Made-up citations are a serious academic integrity problem and will get caught.
- **Don't help overclaim results.** If the user's draft says "our method substantially outperforms all prior work" but the experiments show a 0.3% improvement on one benchmark, push back. Reviewers will notice; better the user does first.
- **Don't auto-anonymize without asking.** Anonymization rules vary by venue (double-blind vs. single-blind, arXiv-allowed vs. not, code-release allowed vs. not). Check what the user is targeting before stripping author info.
- **Don't write papers from nothing.** If the user has results, you can help structure and write. If they don't, the answer is to do the research, not to fabricate it.

## A note on AI-assisted writing in academic contexts

Most major AI/ML venues now allow AI assistance for language polish but require disclosure and prohibit having an LLM "write the paper." The author retains full responsibility for the content. When helping with a draft, prefer to suggest revisions on what the user has written rather than generating large stretches of new prose, and remind the user to check their target venue's policy if they ask about disclosure.

## Sources this skill is built from

- hzwer & DingXiaoH, *Writing AI Conference Papers: A Handbook for Beginners* — github.com/hzwer/WritingAIPaper
- Wookai, *Tips and Tricks for Writing Scientific Papers* — github.com/Wookai/paper-tips-and-tricks
- K-Dense-AI, *claude-scientific-writer* — github.com/K-Dense-AI/claude-scientific-writer
- Swales' three-move introduction model (Establish territory → Find niche → Occupy niche), as referenced in the WritingAIPaper handbook and standard EAP texts.
- An empirical regression-test corpus of 10 award-winning papers from NeurIPS, ICML, ICLR, CVPR, and ACL 2023–2025 (see `references/corpus_patterns.md`). The corpus was assembled to test pattern claims against real papers rather than rely on textbook intuitions; the patterns in `corpus_patterns.md` are derived directly from this corpus.
