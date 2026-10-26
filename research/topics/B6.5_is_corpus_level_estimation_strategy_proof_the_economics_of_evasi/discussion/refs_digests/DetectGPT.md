# Digest: DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature

> Lightweight extraction-mode digest built from the local OpenReview idea corpus
> (`topics/corpus/ideas.jsonl`, `paper_id=UiAyIILXRd`), not from the full PDF (no PDF is
> cached locally, hence `pdf_path=null` and `verified.id_resolves=false` in
> `reference_candidates.jsonl`). Grounded in the paper's own real proposal text; page/section
> locators unavailable.

- **paper_url**: https://openreview.net/forum?id=UiAyIILXRd
- **role in B6.5**: instantiated as M1, the paired single-document fragility control.

## Motivation (source: paper's own proposal text)
Prior zero-shot detectors rely on first-order properties (average log-probability, token
rank/entropy) that are strongly affected by decoding strategy, theoretically bounded by the total
variation distance between human/model text distributions, and empirically defeated by
paraphrasing. This motivates probing a deeper property: local curvature of the model's
probability landscape around a passage.

## Method (source: paper's own proposal text)
(1) generate multiple semantically-similar perturbations of a candidate passage via a mask-filling
model (T5); (2) compute the discrepancy between the passage's log-probability and the average
log-probability of its perturbations; (3) interpret this discrepancy as an approximation to the
negative trace of the Hessian (local curvature) via finite-difference/Hutchinson estimators;
(4) threshold the curvature score for a zero-shot decision, no training required.

## Limitation load-bearing for B6.5 (own scope, not author-stated)
Produces a per-document curvature verdict only; degrades under paraphrasing (the premise B6.5
presupposes as already established); offers no aggregate-estimate quantity, so it says nothing
about whether averaging over a corpus could restore the robustness that per-document detection
loses.

## Grounding check
`paper_id` resolves in the local corpus; `paper_url` is a real, independently-checkable OpenReview
forum link. No PDF cached; no page-level extraction performed.
