# Lightweight digest (backfill): ROC-n-reroll: How verifier imperfection affects test-time scaling

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: ROC-n-reroll: How verifier imperfection affects test-time scaling
- **OpenReview id**: 3Gy5mmyuxn
- **URL**: https://openreview.net/forum?id=3Gy5mmyuxn

## Motivation (from the paper's own OpenReview submission text)

Test-time scaling methods such as repeated sampling, Best-of-N selection, and rejection filtering are increasingly used to improve language model performance at inference time. Existing theory, however, largely explains scaling through pass@N-style coverage under effectively perfect verification, as in @brown2024monkeys. That abstraction breaks down in the practical regime emphasized by @cobbe2021verifiers, where candidate answers are chosen using learned or LLM-based verifiers whose scores are correlated with correctness but are not error-free. Once verification is imperfect, both false negatives and false positives shape the output distribution, and the central quantity of interest is no longer whether a correct sample was generated, but whether the final selected sample is actually correct.

This gap matters because empirical work already shows that imperfect verification fundamentally changes inference-time scaling behavior. @stroebl2024inferencescaling demonstrates that false positives can impose hard limits on the gains achievable by resampling, even at very large sample budgets. At the same time, @gao2023overoptimization shows more generally that optimizing a proxy score can decouple from ground-truth performance, so verifier-score improvements alone are insufficient as an analysis target. Meanwhile, @schaeffer2025powerlaws argues that aggregate scaling trends can conceal very different per-instance mechanisms, which makes benchmark-level extrapolation an unreliable basis for theory. Together, these results create a concrete opportunity: instead of studying aggregate score trends or assuming perfect judges, we can seek an exact per-query characterization of how verifier quality determines the accuracy–compute tradeoff of resampling methods.

The specific problem we address is to determine what aspect of an imperfect verifier is sufficient to predict the performance of Rejection Sampling and Best-of-N at test time, and how this prediction changes across compute regimes. We aim to explain when one method is more compute-efficient than the other, what governs their asymptotic limits, and why early low-compute gains may fail to predict high-compute behavior. The goal is a theory stated directly in terms of true correctness, not proxy scores, while remaining general enough to cover realistic learned verifiers.

## Method (from the paper's own OpenReview submission text)

We propose to analyze verifier-based test-time scaling through a per-query binary decision framework in which the generator has base accuracy \(\pi\) and the verifier is represented by its ROC curve. The core idea is that, for binary correctness, the ROC curve captures exactly the achievable true-positive/false-positive tradeoffs of thresholding the verifier score, and this geometry is sufficient to derive the accuracy of both Rejection Sampling and Best-of-N under imperfect verification. This formulation addresses the main gap in prior work by replacing perfect-verifier pass@N analysis with exact ground-truth accuracy expressions for noisy verifiers.

1. **Per-query ROC formalization**: We model a fixed query with a base generator, a binary ground-truth correctness label, and a verifier score that can be thresholded into classifiers. This choice is motivated by @schaeffer2025powerlaws, which shows that per-instance behavior must be separated from aggregate scaling artifacts, and by @gao2023overoptimization, which motivates analyzing correctness rather than score alone. The ROC curve becomes the sufficient object because it summarizes all optimal threshold tradeoffs between true positives and false positives for that query.

2. **Rejection Sampling accuracy–compute derivation**: We derive the expected compute of RS from the acceptance probability of a thresholded verifier and express the resulting accuracy as the precision of accepted samples. This extends the rejection-style intuition seen empirically in @song2025mindgap into an exact analytical characterization under imperfect verification. The resulting formula shows how RS depends only on base accuracy and ROC geometry, enabling direct analysis of monotonicity, finite-compute gains, and asymptotic limits.

3. **Best-of-N characterization via ROC geometry**: We express BoN accuracy as the probability that the highest-scoring sample among \(N\) draws is correct, and reduce this probability to an integral determined by the ROC curve. This builds on the general theoretical perspective of @huang2025bestofn, but replaces score-based bounds with an exact characterization tailored to binary correctness. It also complements the verifier-guided selection setting introduced by @cobbe2021verifiers by explaining how imperfect ranking quality translates into final-answer accuracy.

4. **Comparative and asymptotic analysis**: We compare RS and BoN under matched compute and analyze how different regions of the ROC curve control low- and high-compute behavior. In particular, we study when concavity of the ROC curve implies RS dominates BoN at fixed compute, and how the slope near the origin determines the infinite-compute limit for both methods. This directly provides the theory missing behind the empirical saturation effects reported by @stroebl2024inferencescaling.

5. **Empirical validation with LLM verifiers**: We estimate per-query ROC curves for open-weight LLM verifiers on reasoning benchmarks and use the derived formulas to predict RS and BoN performance. This is needed to verify that the ROC-based theory is not only mathematically exact under the model, but also predictive for realistic verifier scores of the kind used in @cobbe2021verifiers and related verifier-based pipelines. The experiments test both per-query predictions and dataset-level qualitative implications such as RS's advantage at fixed compute and the non-extrapolatability of high-compute performance.

These components form a coherent system because they use a single representation—the ROC curve—to connect verifier quality, compute budget, and ground-truth accuracy across both resampling methods. The result is a unified theory that explains empirical limitations of imperfect-verifier scaling while yielding concrete comparative predictions for method design.
