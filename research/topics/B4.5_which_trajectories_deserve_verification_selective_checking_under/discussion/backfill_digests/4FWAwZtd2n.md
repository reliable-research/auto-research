# Lightweight digest (backfill): SCALING LLM TEST-TIME COMPUTE OPTIMALLY CAN BE MORE EFFECTIVE THAN SCALING PARAMETERS FOR REASONING

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: SCALING LLM TEST-TIME COMPUTE OPTIMALLY CAN BE MORE EFFECTIVE THAN SCALING PARAMETERS FOR REASONING
- **OpenReview id**: 4FWAwZtd2n
- **URL**: https://openreview.net/forum?id=4FWAwZtd2n

## Motivation (from the paper's own OpenReview submission text)

Scaling model parameters has been the dominant paradigm for improving reasoning in large language models, yet recent work suggests that inference-time compute can also yield substantial gains. Methods such as best-of-N sampling with verifiers (@cobbe2021verifier) and PRM-guided search (@lightman2023verify) show that additional inference compute improves accuracy, but their benefits are inconsistent across tasks and budgets. Similarly, revision-based approaches (@qu2024recursive) demonstrate that sequential inference can refine answers, while other analyses show that naive self-correction fails (@huang2023selfcorrect). These mixed findings indicate that the effectiveness of test-time compute is not uniform, raising the question of how it should be allocated.

Existing approaches typically fix an inference strategy globally, for example using a single best-of-N value or a fixed search procedure. This assumption is implicit even in compute-optimal analyses such as @wu2024computeoptimal, which compare strategies but do not adapt them per prompt. Empirically, however, reasoning datasets like MATH contain questions spanning a wide difficulty range relative to a given base model. Averaging performance across such heterogeneous prompts obscures the fact that different inference mechanisms exploit different regimes: search excels when exploration over strategies is needed, while revisions excel when an initial solution is close to correct.

This gap matters because inference-time compute is expensive and increasingly central to deployment. If compute can be allocated adaptively, smaller models with well-chosen inference strategies could outperform much larger models under matched FLOPs. This creates an opportunity to rethink the trade-off between pretraining and inference, and to design inference systems that are efficient, modular, and responsive to prompt difficulty rather than statically configured.

## Method (from the paper's own OpenReview submission text)

We propose a compute-optimal, difficulty-conditioned framework for scaling test-time compute in reasoning tasks. The core idea is to view inference as selecting hyperparameters of a proposer–verifier system under a fixed budget, and to approximate the optimal choice by conditioning on prompt difficulty estimated from the base model. This formulation directly addresses the inefficiency of static inference strategies by matching compute allocation to the regime in which each inference mechanism is most effective.

1. **Unified Proposer–Verifier Abstraction**: We formalize inference-time methods as combinations of a proposal distribution and a verifier, extending the best-of-N framework from @cobbe2021verifier. This abstraction allows revisions, parallel sampling, and PRM-guided search to be compared and combined within a single compute budget.

2. **Process-Based Verifier and Search**: We train a dense process reward model following @lightman2023verify and use it to guide search procedures inspired by @yao2023tree. This component enables structured exploration over reasoning steps, which is particularly important for prompts where the base model’s initial solutions are poor.

3. **Learned Revision Models**: Building on @qu2024recursive, we fine-tune models to iteratively revise their own answers, overcoming the limitations of naive self-correction identified by @huang2023selfcorrect. Sequential revisions refine locally correct reasoning and provide an efficient use of compute on easier prompts.

4. **Difficulty Estimation**: We estimate prompt difficulty from the base model’s behavior, using statistics such as verifier scores to approximate pass@1 rates. This step provides a practical, model-relative notion of difficulty without requiring ground-truth labels.

5. **Compute-Optimal Allocation Policy**: Using validation data, we learn a mapping from difficulty bins and compute budgets to inference hyperparameters, extending compute-optimal ideas from @wu2024computeoptimal to the question-dependent setting.

Together, these components form a coherent system in which difficulty estimation selects among complementary inference mechanisms, allowing test-time compute to be used far more efficiently than any single static strategy.
