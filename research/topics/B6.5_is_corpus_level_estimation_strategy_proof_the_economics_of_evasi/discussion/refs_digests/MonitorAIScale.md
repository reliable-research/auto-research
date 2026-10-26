# Digest: Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews

> Lightweight extraction-mode digest built from the local OpenReview idea corpus
> (`topics/corpus/ideas.jsonl`, `paper_id=bX3J7ho18S`), not from the full PDF (no PDF is
> cached locally, hence `pdf_path=null` and `verified.id_resolves=false` in
> `reference_candidates.jsonl`). Content below is grounded in the paper's own
> proposal text (motivation + method), which is itself real (the paper is real and
> resolvable at the `paper_url`), but page/section locators are unavailable.

- **paper_url**: https://openreview.net/forum?id=bX3J7ho18S
- **role in B6.5**: instantiated as the primary corpus-level estimator, M2.

## Motivation (source: paper's own proposal text)
Instance-level AI-text detection is unstable under paraphrasing/adversarial pressure and
introduces bias against non-native-English writers; several works instead suggest AI effects
manifest more reliably in aggregate than per-document. This motivates reframing AI-text
detection as a *measurement* problem: not "which documents are AI-generated" but "what fraction
of a corpus reflects substantial AI modification."

## Method (source: paper's own proposal text)
A distributional maximum-likelihood framework: (1) construct two reference corpora (human-written
and LLM-generated under matched prompts); (2) estimate token-occurrence distributions over a
restricted, empirically stable vocabulary (e.g. adjectives) from each; (3) model the target corpus
as a mixture of the two reference distributions parameterized by a single mixing coefficient
(the AI-modified proportion); (4) fit the mixing coefficient by maximizing corpus-level
log-likelihood; (5) validate via semi-synthetic mixtures with known ground-truth AI proportion.

## Limitation load-bearing for B6.5 (own scope, not author-stated)
Validated only on semi-synthetic mixtures generated under a **benign, non-adversarial** process;
never models an adversary who paraphrases specifically to shift the fitted mixing coefficient. This
is exactly the gap B6.5's cost-accuracy game tests.

## Grounding check
`paper_id` resolves in the local corpus (`topics/corpus/ideas.jsonl`); `paper_url` is a real,
independently-checkable OpenReview forum link. No PDF cached; no page-level extraction performed.
