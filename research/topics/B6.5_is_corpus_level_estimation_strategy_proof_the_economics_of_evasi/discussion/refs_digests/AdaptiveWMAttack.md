# Digest: Optimizing Adaptive Attacks against Watermarks for Language Models

> Lightweight extraction-mode digest built from the local OpenReview idea corpus
> (`topics/corpus/ideas.jsonl`, `paper_id=AsODat0dkE`), not from the full PDF (no PDF is
> cached locally, hence `pdf_path=null` and `verified.id_resolves=false` in
> `reference_candidates.jsonl`). Grounded in the paper's own real proposal text; page/section
> locators unavailable.

- **paper_url**: https://openreview.net/forum?id=AsODat0dkE
- **role in B6.5**: protocol adapted for the adaptive/coordinated adversary variant, M3.

## Motivation (source: paper's own proposal text)
Watermark robustness evaluations largely rely on non-adaptive or generic attacks, mismatched with
a realistic threat model in which attackers know the watermarking algorithm and adapt their
strategy. Paraphrasing alone already reduces detection accuracy; stronger adaptive attacks further
undermine watermark guarantees, so adaptive attackers should be the evaluation baseline, not an
edge case.

## Method (source: paper's own proposal text)
(1) formalize watermark robustness as an explicit optimization objective (expected verification
failure + quality-preservation term); (2) generate surrogate watermark keys from an open-weight
surrogate model to approximate the objective without provider key access; (3) use an LLM
paraphraser as the attack primitive; (4) curate preference triplets (watermarked text, an evasive
high-quality paraphrase, a failed paraphrase) via best-of-N sampling against the surrogate;
(5) fine-tune the paraphraser via Direct Preference Optimization (DPO) on this preference data,
avoiding RL instability/cost.

## Limitation load-bearing for B6.5 (own scope, not author-stated)
Defines its evasion objective and budget *per text* against a per-text watermark verifier; never
asks whether the same per-document budget still suffices to move a population-level aggregate
statistic, i.e. whether evasion cost changes when the target shifts from one verdict to a
corpus-level estimate.

## Grounding check
`paper_id` resolves in the local corpus; `paper_url` is a real, independently-checkable OpenReview
forum link. No PDF cached; no page-level extraction performed.
