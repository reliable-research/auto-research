# Digest (lightweight, backfilled): When Silence Is Golden: Can LLMs Learn to Abstain in Temporal QA and Beyond?

- **Title**: When Silence Is Golden: Can LLMs Learn to Abstain in Temporal QA and Beyond?
- **OpenReview id**: PhUCxfS0yf
- **URL**: https://openreview.net/forum?id=PhUCxfS0yf
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `PhUCxfS0yf`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
Temporal question answering requires more than retrieving relevant facts: the model must determine which facts are valid at the queried time and whether those facts jointly support any answer at all. The TimeQA benchmark introduced by @chen2021timeqa makes this explicit by including both answerable and naturally unanswerable questions, where contradictions or temporal mismatch invalidate an answer. This creates a setting in which answer generation and answerability judgment are inseparable. Existing LLMs often fail precisely at this boundary, producing fluent answers even when the temporal evidence does not justify one.

Prior work on abstention and uncertainty exposes this gap but does not resolve it for temporally grounded reasoning. @feng2024abstain shows that abstention is an effective way to reduce hallucinations, yet its strongest methods rely on multi-LLM collaboration rather than teaching a single model to internalize refusal behavior. @kadavath2022know and @azaria2023internalstate further indicate that LLMs contain useful internal signals about correctness and truthfulness, but these signals are typically accessed through confidence estimation or auxiliary classifiers. Such mechanisms can identify uncertainty, but they do not directly train the generation policy to convert uncertainty into the correct action: either producing a grounded answer or emitting "No Answer."

This matters especially in temporal QA because uncertainty is often caused by multi-step reasoning 

## Method (from corpus proposal, truncated)
We propose a two-stage training framework that jointly learns temporal reasoning and abstention. The core idea is to first teach the model to produce explicit temporal reasoning traces through chain-of-thought supervision, then refine the policy with reinforcement learning so that correct answers and correct abstentions are both rewarded outcomes. This formulation addresses the main gap in prior work by moving abstention from post-hoc confidence estimation to direct policy optimization over reasoning behavior.

1. **CoT-Supervised Cold Start**: We initialize the model with supervised fine-tuning on step-by-step temporal reasoning traces, following the central insight of @wei2022cot that explicit reasoning improves performance on complex tasks. This stage is needed because reinforcement learning alone is unlikely to discover reliable temporal reasoning from scratch, especially in small models. By learning to generate structured reasoning before the final answer, the model acquires the basic temporal inference skills required for later abstention decisions.

2. **GRPO-Based Policy Optimization**: We optimize the CoT-initialized model with Group Relative Policy Optimization, drawing directly on the efficiency and comparative reward structure of @shao2024grpo. GRPO is needed because the task involves sequence-level decisions with sparse correctness signals, and groupwise comparison stabilizes optimization over multiple sampled outputs. This extends prior RL-for-reasoning formulat

## Limitation (as used in digest.md N4, this topic)
Trains LLMs to abstain in temporal QA where unanswerable labels are inherited from a benchmark (TimeQA), not injected via matched-pair construction; nothing measures whether a *third-party* attribution system watching an execution trace can make the same infeasibility call about someone else's failure.

## Relevance to B2.4
Closest prior abstention-training work; B2.4's matched-pair construction (M1) is precisely the missing piece this paper's benchmark-inherited labels lack, and B2.4's harness allows first-party in-run infeasibility declaration as one of its attribution instantiations (M4c), a post-hoc analogue of this paper's trained abstention policy.
