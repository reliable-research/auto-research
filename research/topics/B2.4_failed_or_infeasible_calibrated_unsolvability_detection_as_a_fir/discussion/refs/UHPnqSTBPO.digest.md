# Digest (lightweight, backfilled): TRUST OR ESCALATE: LLM JUDGES WITH PROVABLE GUARANTEES FOR HUMAN AGREEMENT

- **Title**: TRUST OR ESCALATE: LLM JUDGES WITH PROVABLE GUARANTEES FOR HUMAN AGREEMENT
- **OpenReview id**: UHPnqSTBPO
- **URL**: https://openreview.net/forum?id=UHPnqSTBPO
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `UHPnqSTBPO`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
LLM-based evaluation is increasingly used as a substitute for human judgment, yet existing practice typically relies on a single strong judge model or heuristic confidence thresholds. Empirically, even strong LLM judges can disagree systematically with humans, and without formal guarantees there is no way to bound this disagreement on new data. Selective prediction offers a way to abstain when uncertain, but applying it to LLM evaluation requires both a meaningful confidence signal and a calibration procedure that provides finite-sample guarantees.

Prior work exposes concrete limitations. Conformal and alignment-based methods show that guarantees are possible for foundation models, but they often provide marginal or expectation-based control rather than per-run guarantees relevant to evaluation pipelines (@gui2024alignment). Abstention methods for LLMs demonstrate feasibility in controlling hallucination rates, yet focus on factual correctness rather than subjective human agreement (@yadkori2024abstention). Critically, confidence elicitation from RLHF LLMs is often miscalibrated, making predictive probabilities or verbalized confidence unreliable for selective decisions (@tian2023calibration).

At the same time, work on subjective tasks shows that annotator disagreement carries essential information about reliability (@khurana2024crowd), and cascading strategies indicate that uncertainty-aware escalation can reduce cost (@ramirez2024twotier). These observations create an opp

## Method (from corpus proposal, truncated)
We propose a selective, cascaded LLM-judge framework that guarantees a user-specified level of agreement with human judgments. The core idea is to evaluate only when a judge’s confidence—defined as estimated human agreement—exceeds a calibrated threshold, and to escalate uncertain cases through a cascade of increasingly strong judges. Exact calibration on a small human-labeled set ensures that the resulting evaluations satisfy the desired risk bound with high probability.

1. **Selective Evaluation with Risk Control**: We frame LLM-based evaluation as selective prediction with abstention, where a judge outputs a decision only if its confidence exceeds a threshold. Thresholds are calibrated using a learn-then-test, fixed-sequence hypothesis testing procedure to guarantee disagreement risk below a user-specified level, following @angelopoulos2022learntest and the selective paradigm of @geifman2017selective.

2. **Agreement-Based Confidence via Simulated Annotators**: Instead of relying on model self-confidence, we estimate confidence by simulating multiple annotators through in-context prompting and measuring their agreement. This draws on the insight that annotator disagreement reflects subjectivity and reliability in human evaluation, extending ideas from @khurana2024crowd to an unsupervised LLM setting.

3. **Exact Calibration on Human Data**: Using a small calibration set with human judgments, we compute exact upper confidence bounds on selective risk and select thresholds 

## Limitation (as used in digest.md N4, this topic)
Escalates uncertain cases to a stronger judge rather than declaring the item itself infeasible — calibrates against human-judge agreement, not against an oracle-certified feasibility ground truth.

## Relevance to B2.4
B2.4's B-alt control (oracle-calibrated ceiling probe) borrows the idea of a privileged/calibrated reader from this paper's cascade-to-stronger-judge design, but redirects the calibration target from human agreement to oracle feasibility.
