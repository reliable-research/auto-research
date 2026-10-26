# Lightweight digest (backfill): TRUST OR ESCALATE: LLM JUDGES WITH PROVABLE GUARANTEES FOR HUMAN AGREEMENT

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: TRUST OR ESCALATE: LLM JUDGES WITH PROVABLE GUARANTEES FOR HUMAN AGREEMENT
- **OpenReview id**: UHPnqSTBPO
- **URL**: https://openreview.net/forum?id=UHPnqSTBPO

## Motivation (from the paper's own OpenReview submission text)

LLM-based evaluation is increasingly used as a substitute for human judgment, yet existing practice typically relies on a single strong judge model or heuristic confidence thresholds. Empirically, even strong LLM judges can disagree systematically with humans, and without formal guarantees there is no way to bound this disagreement on new data. Selective prediction offers a way to abstain when uncertain, but applying it to LLM evaluation requires both a meaningful confidence signal and a calibration procedure that provides finite-sample guarantees.

Prior work exposes concrete limitations. Conformal and alignment-based methods show that guarantees are possible for foundation models, but they often provide marginal or expectation-based control rather than per-run guarantees relevant to evaluation pipelines (@gui2024alignment). Abstention methods for LLMs demonstrate feasibility in controlling hallucination rates, yet focus on factual correctness rather than subjective human agreement (@yadkori2024abstention). Critically, confidence elicitation from RLHF LLMs is often miscalibrated, making predictive probabilities or verbalized confidence unreliable for selective decisions (@tian2023calibration).

At the same time, work on subjective tasks shows that annotator disagreement carries essential information about reliability (@khurana2024crowd), and cascading strategies indicate that uncertainty-aware escalation can reduce cost (@ramirez2024twotier). These observations create an opportunity: by combining selective evaluation, agreement-aware confidence, and exact calibration, it should be possible to guarantee human agreement while maximizing coverage and minimizing reliance on expensive judges. The problem is to formalize this combination with provable guarantees.


## Method (from the paper's own OpenReview submission text)

We propose a selective, cascaded LLM-judge framework that guarantees a user-specified level of agreement with human judgments. The core idea is to evaluate only when a judge’s confidence—defined as estimated human agreement—exceeds a calibrated threshold, and to escalate uncertain cases through a cascade of increasingly strong judges. Exact calibration on a small human-labeled set ensures that the resulting evaluations satisfy the desired risk bound with high probability.

1. **Selective Evaluation with Risk Control**: We frame LLM-based evaluation as selective prediction with abstention, where a judge outputs a decision only if its confidence exceeds a threshold. Thresholds are calibrated using a learn-then-test, fixed-sequence hypothesis testing procedure to guarantee disagreement risk below a user-specified level, following @angelopoulos2022learntest and the selective paradigm of @geifman2017selective.

2. **Agreement-Based Confidence via Simulated Annotators**: Instead of relying on model self-confidence, we estimate confidence by simulating multiple annotators through in-context prompting and measuring their agreement. This draws on the insight that annotator disagreement reflects subjectivity and reliability in human evaluation, extending ideas from @khurana2024crowd to an unsupervised LLM setting.

3. **Exact Calibration on Human Data**: Using a small calibration set with human judgments, we compute exact upper confidence bounds on selective risk and select thresholds that satisfy the target agreement with high probability. This differs from marginal conformal approaches by providing per-run guarantees, addressing limitations observed in @gui2024alignment.

4. **Cascaded Judge Models**: We organize multiple judge models in a cascade, starting from cheap models and escalating to stronger ones only when confidence is insufficient. This leverages uncertainty-aware cost reduction ideas from @ramirez2024twotier while preserving formal guarantees through separate calibration for each stage.

Together, these components form a coherent system: agreement-based confidence enables meaningful abstention, exact calibration translates abstention into guarantees, and cascading minimizes cost while maintaining the specified level of human agreement.
