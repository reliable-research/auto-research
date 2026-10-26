---
name: pengsida-paper-writer
description: >-
  A research-and-writing skill bundle distilled from Prof. Peng Sida's (彭思达)
  learning_research notes and the Research-Paper-Writing-Skills package, refined against
  28 award papers from NeurIPS/ICML/ICLR/CVPR/ICCV/ACL/SIGGRAPH. Use this whenever the
  user is doing or writing academic research — even if they don't say "skill" —
  including: finding/framing a research problem, generating or pressure-testing ideas,
  planning or debugging experiments and ablations, and drafting or revising any paper
  section (Abstract, Introduction, Related Work, Method, Experiments, Conclusion).
  Also use it for figure/table polish, claim-evidence checking, identifying the paper's
  archetype (method, efficiency, analysis/position, dataset/foundation, or theory),
  adversarial reviewer-style review, rebuttal drafting, and talk slides.
  Prefer it for prompts like "improve my introduction", "is my contribution
  clear", "help me write the method", "does this flow", "plan my ablations", "write a
  rebuttal", or "review my paper like a reviewer".
---

# Pengsida Paper Writer

A multi-file skill bundle (this SKILL.md routes into `references/` guides, `scripts/` for
reproducing the evidence corpus, and `assets/` sample abstracts) for doing and writing
strong research. It merges two sources: the research-process methodology from Prof. Peng
Sida's `learning_research` notes, and the section-by-section writing templates from the
curated `Research-Paper-Writing-Skills` package (itself adapted from Prof. Peng's writing
template), then refines them against a measured corpus of award papers
(`references/corpus-evidence.md`). Attribution: the substantive methodology is Prof. Peng
Sida's; this bundle is an organization, consolidation, and evidence-based extension.
Original notes: https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e — original
repo: https://github.com/pengsida/learning_research

## When To Use Which Part

- **Digest first when you have the paper in hand.** To reconstruct, compare, or review an
  existing paper, decompose it into the N1–N12 argument chain with `references/digest-paper.md`
  (run `scripts/digest_paper.py <paper.txt>` for a skeleton). Mapping each claim to a node
  makes the rest of the work checkable.

- **First, identify the paper archetype** (method / efficiency / analysis-position /
  resource-foundation-model / theory) with `references/paper-archetypes.md`. It changes
  what counts as the contribution and what evidence reviewers expect. The section guides
  default to the method archetype; the archetype file says what to adjust for the others.
- Doing research (problem, idea, experiments, rebuttal, slides): start with
  `references/research-process.md`.
- Writing or revising a paper section: load only the matching section guide below.
- Checking flow/clarity of any paragraph: run the Paragraph Clarity Check, source
  in `references/does-my-writing-flow-source.md`.
- Final review before submission: `references/paper-review.md`.

Do not load all references at once. Load only the file needed for the current target.

## Core Operating Rules

1. Clarify the paper story before any sentence-level edit. Know, in one breath: the
   task, the exact technical challenge you solve, your contribution, and why it works.
   Also fix the **archetype** — a finding, a released resource, or a theorem is a
   contribution even when there is no new pipeline.
2. One paragraph carries exactly one message, stated in its first sentence.
3. Rewrite paragraph-by-paragraph — one paragraph per turn — not whole sections in bulk.
4. After writing any section, run reverse outlining (thesis → topic sentences →
   evidence) and delete what cannot be mapped.
5. Every major claim in Abstract/Introduction must be technically correct AND backed
   by reported experimental evidence. If unsupported, add evidence or weaken/remove it.
6. Treat figures, tables, and layout as core content, not decoration. First impression
   (teaser, pipeline figure, clean tables) drives reviewer perception.
7. Keep terminology and notation stable across the whole paper; never swap key terms.
8. Never write the method as an incremental patch over a naive baseline, even when the
   work is incremental — that framing kills reviewer curiosity and looks low-score.
9. Iterate adversarially: read your own draft as a skeptical reviewer and resolve every
   high-risk question before finalizing.

## Research Process (idea → experiments → rebuttal)

Use `references/research-process.md`. In brief, a paper needs three capabilities, each
trainable:

1. Ideas — find an important problem (real scientific/practical value), then propose a
   solution. Set a long-horizon research goal and a roadmap; each paper advances it.
2. Writing/presentation — papers, weekly meeting PPTs, demos, slides, videos.
3. Experiments — write code, run experiments, and (critically) analyze why things do
   not work; keep a disciplined experiment log.

## Paragraph Clarity Check

Run whenever asked whether a paragraph "flows" or is clear.

1. Read as an external reader: Does it have one explicit message? Does sentence one
   state what the paragraph does? Are all nouns/terms readable without hidden context?
   Does each sentence relate to the previous one (cause, contrast, consequence,
   refinement, example)?
2. Reverse outline the section: write the thesis, each topic sentence, each evidence
   point; check topic-sentence → thesis and evidence → topic-sentence mappings; revise
   or cut anything that does not map.
3. If flow is still weak, temporarily add section headers and explicit transition words
   during revision, then remove unnecessary ones before finalizing.

Source: `references/does-my-writing-flow-source.md`.

## Section Guides (load one at a time)

- Introduction: `references/introduction.md`
- Abstract: `references/abstract.md`
- Related Work: `references/related-work.md`
- Method: `references/method.md`
- Experiments: `references/experiments.md`
- Conclusion: `../research-paper-writing/references/paper_structure.md` (Conclusion guidance)
- Paper archetypes (method / efficiency / analysis / resource / theory): `references/paper-archetypes.md`
- Corpus evidence (measured archetype/signal stats from 28 award papers): `references/corpus-evidence.md`
- Digest a paper into N1–N12 parts (then reconstruct/compare/review): `references/digest-paper.md`
- Worked digests + two-paper comparison: `references/digest-examples.md`, `references/comparison.md`
- Round-trip recovery self-evaluation (encode→decode, 0.87 on 28 AI papers): `references/roundtrip-recovery.md` (historical calibration; see the source-revision link in that reference)
- Cross-domain round-trip (AI+SE, 0.85 on 41 papers): `references/roundtrip-se.md` (historical calibration; see the source-revision link in that reference)
- Paper review (adversarial): `references/paper-review.md`
- Research process (idea/experiments/rebuttal/slides): `references/research-process.md`
- Example bank index: `references/examples/index.md`
- Worked archetype examples (real annotated award abstracts): `references/examples/archetype-examples.md`

## Pre-Submission Self-Review (five dimensions)

Append and answer near the end of the draft, then revise on unresolved items
(full checklist in `references/paper-review.md`):

1. Contribution — is the solved failure case meaningful and non-obvious; is there a
   clear novelty type (task/pipeline/module/design finding/insight)?
2. Writing clarity — can a knowledgeable reader reproduce the method; is each module's
   motivation explicit; is notation consistent?
3. Experimental strength — are gains meaningful and consistent across
   datasets/settings/metrics; is absolute performance venue-competitive?
4. Evaluation completeness — ablations for every key design choice; all strong/recent
   baselines under fair settings; standard sufficient metrics.
5. Method-design soundness — realistic setting; no hidden defects; robust without
   per-case retuning; benefits outweigh added complexity.

Treat claim-evidence alignment as a hard constraint. Mark each item `pass`,
`needs revision`, or `needs new experiment`, and iterate until no major reject risk remains.

## Output Contract

When asked to draft or rewrite sections, return:

1. A compact section outline (3–7 bullets).
2. Revised paragraphs with explicit roles
   (opening / challenge / method / advantage / evidence / limitation).
3. A short self-review checklist (clarity, flow, terminology, unsupported claims,
   missing evidence).
4. A claim-evidence map for each major claim:
   `Claim: ... | Evidence: ... | Status: supported / needs evidence`.

Reuse the sentence logic in the example bank, never the exact wording.

