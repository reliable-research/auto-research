# Digest: How Much of My Dataset Did You Use? Quantitative Data Usage Inference in Machine Learning

> Lightweight extraction-mode digest built from the local OpenReview idea corpus
> (`topics/corpus/ideas.jsonl`, `paper_id=EUSkm2sVJ6`), not from the full PDF (no PDF is
> cached locally, hence `pdf_path=null` and `verified.id_resolves=false` in
> `reference_candidates.jsonl`). Grounded in the paper's own real proposal text; page/section
> locators unavailable.

- **paper_url**: https://openreview.net/forum?id=EUSkm2sVJ6
- **role in B6.5**: instantiated as the alternate ("debias-and-aggregate") corpus-level estimator.

## Motivation (source: paper's own proposal text)
Existing dataset-usage-inference methods (hypothesis testing, ownership watermarking) frame usage
as binary (used / not used), which is unstable or misleading once a dataset is only *partially*
used — a realistic setting given mixtures of data sources. Per-record membership-inference signals
are noisy and biased individually; the core issue is not the lack of signals but the inability to
aggregate them reliably into a dataset-level, quantitative estimate.

## Method (source: paper's own proposal text)
Dataset Usage Cardinality Inference (DUCI): (1) apply a high-power membership-inference attack to
each record to obtain binary membership guesses; (2) estimate the true-positive/false-positive
rates of that attack from a small number of reference models; (3) analytically debias each
record's guess into an estimate of its inclusion probability using the estimated TPR/FPR;
(4) average the debiased per-record estimates into an unbiased overall usage-proportion estimate;
(5) construct confidence intervals via asymptotic normality of the aggregated estimator.

## Limitation load-bearing for B6.5 (own scope, not author-stated)
Assumes the per-record measurement error rates (TPR/FPR) are stationary and estimable from
reference models; an adversary who deliberately shifts per-record signals (e.g. via paraphrasing)
to bias the aggregate violates that stationarity assumption, which is outside the method's stated
scope.

## Grounding check
`paper_id` resolves in the local corpus; `paper_url` is a real, independently-checkable OpenReview
forum link. No PDF cached; no page-level extraction performed.
