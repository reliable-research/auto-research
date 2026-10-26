# Digest (lightweight, backfilled): Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks

- **Title**: Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks
- **OpenReview id**: 9gJBhkLRat
- **URL**: https://openreview.net/forum?id=9gJBhkLRat
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `9gJBhkLRat`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
Large language models are increasingly deployed in factual question-answering settings where incorrect answers can produce hallucinations and erode user trust. A natural mitigation strategy is to enable models to refuse questions that fall outside their knowledge boundaries. Recent studies demonstrate that prompting or training methods can improve this abstention behavior, encouraging models to respond with “I don’t know” when uncertain (@cheng2024knowwhatyoudontknow; @zhang2024rtuning; @kapoor2024teachdontknow). However, evaluating whether such refusals truly reflect knowledge awareness remains a challenge.

Existing evaluation frameworks only partially address this problem. Benchmarks such as SimpleQA treat refusal as a distinct outcome and evaluate reliability using heuristic combinations of accuracy and refusal rate (@wei2024simpleqa). While these metrics penalize both overconfidence and over-refusal, they do not directly measure whether refusals occur on questions the model would otherwise answer incorrectly. As a result, models can appear to improve simply by increasing refusal frequency without improving the alignment between refusal behavior and knowledge gaps. More general calibration approaches attempt to measure uncertainty quality using confidence scores or auxiliary predictors (@ulmer2024generationcalibration), but these methods estimate uncertainty rather than evaluating the model’s actual refusal decisions. Consequently, current metrics fail to isolate the core

## Method (from corpus proposal, truncated)
We propose the Refusal Index (RI), a metric that quantifies knowledge-aware refusal as the rank correlation between a model’s refusal probability and its error probability across questions. By framing refusal as a rank-calibration problem, RI evaluates whether models systematically assign higher refusal likelihood to harder questions rather than simply refusing more often. This formulation produces a metric that is invariant to overall refusal rate and can be computed using only observable model outputs in a black-box setting.

1. **Rank-Based Formulation of Knowledge-Aware Refusal**: Building on the rank-calibration perspective of uncertainty evaluation introduced by @huang2024rankcalibration, we formalize knowledge-aware refusal as the monotonic relationship between refusal probability and answer error probability. We define the Refusal Index as the Spearman rank correlation between these two latent probabilities across evaluation questions. This formulation directly measures the discriminative ability of refusal decisions—whether a model ranks difficult questions as more likely to be refused—rather than penalizing overall refusal frequency as in heuristic metrics derived from @wei2024simpleqa.

2. **Black-Box Refusal Signal from Generated Outputs**: Inspired by generation-based calibration approaches such as @ulmer2024generationcalibration, our metric relies solely on observable model outputs rather than internal probabilities or auxiliary predictors. Each model response i

## Limitation (as used in digest.md N4, this topic)
Calibrates refusal against the *model's own* error probability on single-turn factual questions — a knowledge-boundary notion of 'should refuse.' It never involves an externally certified ground truth that the task admits no answer for anyone, and it operates on static QA, not on multi-step agent traces.

## Relevance to B2.4
B2.4's calibration metric (the Unsolvability Refusal Index, M5) borrows this paper's Spearman-correlation *measurement construct* wholesale, substituting oracle-certified task infeasibility for model-own-error as the ground-truth column. Not a baseline (different setting/ground-truth) — a borrowed instrument.
