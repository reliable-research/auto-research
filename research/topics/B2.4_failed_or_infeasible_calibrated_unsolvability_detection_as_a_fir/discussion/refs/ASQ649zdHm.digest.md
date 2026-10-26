# Digest (lightweight, backfilled): Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty

- **Title**: Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty
- **OpenReview id**: ASQ649zdHm
- **URL**: https://openreview.net/forum?id=ASQ649zdHm
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `ASQ649zdHm`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
Reinforcement learning has become a central mechanism for improving reasoning capabilities in large language models. Methods based on reinforcement learning with verifiable rewards train models to generate chain-of-thought reasoning and optimize a binary correctness signal indicating whether the final answer matches ground truth. This paradigm has proven highly effective for improving reasoning accuracy, as demonstrated by systems such as DeepSeek-R1 that use RL to incentivize structured reasoning behavior @guo2025deepseekr1. However, the reward formulation underlying these approaches evaluates only answer correctness, ignoring the model’s confidence in its predictions.

This design choice introduces a critical limitation. Binary rewards treat a correct answer produced with low confidence identically to one produced with unjustified certainty, and likewise penalize cautious abstention and confident hallucination equally. Empirical analyses show that reinforcement learning objectives often amplify overconfidence in language models, leading them to produce confident but incorrect responses more frequently @leng2025rewardcalibration. Moreover, recent work on uncertainty in reasoning models demonstrates that deeper reasoning chains do not necessarily improve calibration; reasoning models frequently remain highly overconfident even when their answers are wrong @mei2025uncertaintyreasoning. As a result, RL-trained reasoning models may achieve high accuracy while simultaneously degr

## Method (from corpus proposal, truncated)
We propose Reinforcement Learning with Calibration Rewards (RLCR), a training framework that augments standard RL reasoning objectives with a calibration-aware reward component. The core idea is to train language models to generate both an answer and an explicit confidence estimate after reasoning, and to optimize a reward that combines binary correctness with a proper scoring rule measuring the accuracy of the confidence estimate. By using a bounded proper scoring rule such as the Brier score, the resulting objective preserves incentives for correct answers while encouraging confidence estimates to match the true probability of correctness.

1. **Joint Answer–Confidence Generation**: The model is prompted to produce structured outputs consisting of a reasoning chain, a final answer, and a numerical confidence estimate. This design enables the model to explicitly represent its uncertainty alongside its prediction, following evidence that training procedures can shape how models communicate confidence to downstream users @stengeleskin2024lacie. The confidence value serves as an explicit target for calibration optimization during RL training.

2. **Calibration-Aware Reward Function**: We define a reward that combines the standard binary correctness signal with a calibration term based on the Brier score. Specifically, the reward equals the correctness indicator minus the squared error between the predicted confidence and the realized correctness outcome. Proper scoring rules en

## Limitation (as used in digest.md N4, this topic)
Calibrates confidence against *answer correctness* on verifiable single-turn problems whose reward design contains no unsolvable-instance class — a perfectly calibrated model under this scheme still receives no signal distinguishing 'I cannot' from 'no one can.'

## Relevance to B2.4
Cited alongside TrustOrEscalate in digest.md N4.6 as sharing the same wrong-ground-truth gap (answer-correctness / human-agreement, never task-infeasibility) that B2.4's oracle-certified design fills.
