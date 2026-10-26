# Lightweight digest (backfill): CaTS: Calibrated Test-Time Scaling for Efficient LLM Reasoning

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: CaTS: Calibrated Test-Time Scaling for Efficient LLM Reasoning
- **OpenReview id**: jrSc4RJXy1
- **URL**: https://openreview.net/forum?id=jrSc4RJXy1

## Motivation (from the paper's own OpenReview submission text)

Repeated-sampling methods have emerged as a strong mechanism for improving LLM reasoning, but their efficiency is limited by how they allocate inference-time compute. Self-Consistency improves answer quality by aggregating multiple chain-of-thought samples through majority voting, yet it uses a fixed sample count for every query and assigns equal weight to all samples regardless of their likely reliability @wang2022selfconsistency. More broadly, repeated sampling is now understood as a general axis of test-time scaling, but its practical effectiveness depends on selecting or aggregating samples well rather than merely generating more of them @brown2024monkeys. This creates a concrete inefficiency: easy queries are over-sampled, while difficult queries may still be under-explored under a uniform budget.

Adaptive methods partially address this issue by stopping early when agreement becomes sufficiently strong, but they still rely on manually designed rules over partial sample statistics. Early-Stopping Self-Consistency and Adaptive-Consistency both reduce cost by using agreement thresholds or similar stopping heuristics, yet these criteria are not direct estimates of correctness and may not transfer cleanly across tasks or models @li2024earlystopping, @aggarwal2023adaptiveconsistency. At the same time, test-time scaling studies argue that compute should be allocated according to prompt difficulty, which requires a dependable uncertainty signal available during inference rather than after exhaustive sampling @snell2024testtimescaling.

The key opportunity comes from calibration work showing that self-consistency statistics themselves are strongly correlated with true correctness probabilities @wang2024sccalibration. This suggests that repeated sampling already contains the supervisory signal needed to estimate answer correctness, but current methods only use that signal implicitly at decoding time. The missing piece is to distill multi-sample agreement into a single-pass confidence predictor, so the model can approximate self-consistency-derived uncertainty without having to fully run self-consistency on every query. Solving this gap would enable a task-agnostic and model-based mechanism for controlling sample budgets and aggregating answers more effectively.

## Method (from the paper's own OpenReview submission text)

We propose to train LLMs to output calibrated correctness confidence by distilling self-consistency-derived agreement statistics into the model, and then to use this confidence to control repeated sampling at test time. This formulation directly addresses the gap between expensive but informative multi-sample uncertainty estimation and cheap but unreliable native confidence: the model learns to approximate the former in one forward pass, enabling adaptive stopping and confidence-aware aggregation.

1. **Self-consistency supervision generation**: We construct pseudo-labeled training tuples of the form (query, sampled answer, confidence) by generating multiple candidate reasoning traces per query and estimating each answer's correctness likelihood from cross-sample agreement. This extends the insight from @wang2024sccalibration that self-consistency is a strong calibration signal, but repurposes it from post hoc evaluation into training supervision for confidence prediction.

2. **Diverse candidate generation with dynamic temperature**: We use entropy-based dynamic temperature to generate a diverse set of candidate responses when building the pseudo-labeled dataset. This is needed because confidence targets derived from low-diversity samples are less informative; by extending @zhang2024edt, we obtain broader reasoning coverage while maintaining output quality, which improves the fidelity of self-consistency-based confidence estimates.

3. **Confidence distillation via joint training**: We fine-tune the model to predict whether a candidate answer is correct using a confidence-querying prompt, while jointly retaining the standard language modeling objective on high-confidence reasoning traces. This component is necessary because off-the-shelf model confidence is poorly calibrated, whereas distilled supervision from self-consistency can align predicted confidence with empirical correctness @wang2024sccalibration; the joint objective preserves reasoning ability while improving calibration.

4. **Confidence-based early stopping for repeated sampling**: At inference time, we sequentially sample candidate solutions and stop once a sampled response reaches a target calibrated confidence threshold. This replaces the heuristic stopping logic of @li2024earlystopping and @aggarwal2023adaptiveconsistency with a learned, answer-specific correctness estimate, allowing Best-of-N style inference to terminate early on easy queries while continuing to explore harder ones.

5. **Confidence-weighted self-consistency aggregation**: Instead of majority voting over samples, we weight each answer by the model's calibrated confidence and select the answer with the largest accumulated confidence mass. This extends the aggregation rule of @wang2022selfconsistency by recognizing that not all samples should contribute equally, and it operationalizes the broader test-time scaling objective of allocating compute and influence according to estimated usefulness @snell2024testtimescaling, @brown2024monkeys.

These components form a coherent system because the same distilled confidence signal is used both to decide when to stop sampling and to decide how much each sample should matter. The training pipeline converts expensive multi-sample agreement into a reusable uncertainty estimator, and the inference pipeline uses that estimator to make repeated sampling both more accurate and more compute-efficient.
