# Digest (backfilled from local OpenReview idea-proposal corpus): Empowering LLM Tool Invocation with Tool-call Reward Model

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `LnBEASInVr` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: LnBEASInVr
- **Title**: Empowering LLM Tool Invocation with Tool-call Reward Model
- **URL**: https://openreview.net/forum?id=LnBEASInVr
- **Domain**: ml
- **Related works cited by this paper (count)**: 6

## Motivation (verbatim from corpus proposal record)

Current RL-based LLM agents can learn to invoke search engines and code interpreters, but their reward design remains mismatched to the structure of the decision process. In systems such as @jin2025searchr1 and @li2025torl, the model makes a sequence of tool decisions across multiple turns, yet optimization is driven mainly by whether the final answer is correct. This trajectory-level supervision cannot distinguish a necessary, well-executed tool call from an unnecessary or poorly parameterized one. As a result, correct intermediate tool use may be penalized when the final answer is wrong, while ineffective tool behavior may be reinforced if the answer happens to be correct.

This gap matters because tool-use quality is itself a learnable competence. The process-supervision literature shows that intermediate feedback can substantially improve reasoning when the task unfolds over multiple steps. In particular, @lightman2024verify demonstrates the value of step-level reward modeling, and @luo2024processsupervision shows that such supervision can be collected automatically at useful scale. Meanwhile, @deng2025atomsearcher identifies gradient conflict and reward sparsity in agentic search, but its rewards are anchored at the thought level rather than at the tool interaction itself. For tool-using agents, the missing technical piece is a reward model that explicitly evaluates each completed tool invocation.

This creates a concrete opportunity: if we can learn a reward model that scores the utility of each tool call and assign that reward at the exact turn where the call concludes, then RL can optimize tool behavior with much finer credit assignment than outcome-only methods. The challenge is twofold. First, it is unclear how to construct an effective tool-call reward model, including what labels it should predict and how much distilled data is needed. Second, standard RL integration is nontrivial: naively mixing per-call rewards into PPO or GRPO can distort optimization and even incentivize avoiding tools altogether. The research problem is therefore to design a specialized reward model for tool invocations and an RL integration scheme that converts its predictions into stable learning signals.

## Method (verbatim from corpus proposal record)

We propose a Tool-call Reward Model (TRM) framework for RL-trained LLM agents. The core idea is to replace purely outcome-level supervision with per-tool-invocation utility estimates, then align RL credit assignment to the turn where each tool action finishes. This formulation directly addresses the credit granularity gap in @jin2025searchr1 and @li2025torl by preserving useful intermediate tool behavior even when the final trajectory fails.

1. **Tool-call utility labeling via distillation**: We construct TRM training data by collecting multi-turn tool-use trajectories from a strong reasoning model and re-evaluating each tool call in context. Following the scalable process-supervision logic of @luo2024processsupervision and leveraging strong rollout quality as motivated by @guo2025deepseekr1, each invocation is labeled with two criteria: necessity for task progress and execution quality. Their conjunction yields a binary utility target that is specific to tool behavior rather than generic reasoning quality.

2. **Specialized Tool-call Reward Model**: We train a transformer-based classifier that predicts a utility score for each completed tool invocation from the trajectory context and the tool output. This extends the process reward modeling idea from @lightman2024verify to agentic tool use, but changes the supervision unit from reasoning steps to environment-interacting actions. The TRM is needed because thought-level or trajectory-level reward models do not explicitly model whether a tool call was worth making and whether it was executed correctly.

3. **Turn-level credit assignment for PPO**: We integrate TRM into PPO by assigning each predicted tool reward to the token corresponding to the end of the associated tool action, while keeping the final answer correctness reward at the terminal answer token. This design is necessary to bridge turn-level utility signals and token-level policy optimization without diffusing the signal across unrelated tokens. Relative to outcome-only PPO in @jin2025searchr1 and @li2025torl, the method provides localized reinforcement for effective tool actions and reduces gradient conflict.

4. **Turn-level advantage estimation for GRPO**: For GRPO, we normalize rewards independently at each turn across grouped trajectories instead of pooling all tool-call rewards together. This extends the fine-grained optimization motivation of @deng2025atomsearcher, but uses tool-call-aligned normalization to avoid reward hacking behaviors such as preferring fewer tool calls over better ones. The component is needed because naive group-level normalization conflates different turns and tool counts, producing biased relative advantages.

5. **Joint process-and-outcome optimization**: We optimize the agent with a combined reward structure in which intermediate TRM scores are weighted and complemented by the final answer reward. This preserves the end-task objective emphasized in @jin2025searchr1 and @li2025torl while injecting the process supervision benefits established by @lightman2024verify. The balance is important: too little TRM signal leaves tool behavior under-supervised, while too much can over-prioritize tool use irrespective of final task success.

Together, these components form a coherent system in which data distillation supplies scalable supervision, TRM converts it into per-call utility estimates, and turn-aware PPO/GRPO translates those estimates into stable policy gradients. The result is an RL framework that learns not only to reach correct answers, but to use tools effectively along the way.
