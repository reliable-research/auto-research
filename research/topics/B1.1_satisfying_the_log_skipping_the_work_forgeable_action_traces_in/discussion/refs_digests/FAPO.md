# Digest (backfilled from local OpenReview idea-proposal corpus): FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `jhqqoimoWt` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: jhqqoimoWt
- **Title**: FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning
- **URL**: https://openreview.net/forum?id=jhqqoimoWt
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

Reinforcement learning with verifiable rewards has become an effective way to improve reasoning models because it can optimize directly on tasks with rule-checkable answers. The practical success of GRPO-style training in @shao2024deepseekmath and the large-scale RL pipeline in @yu2025dapo show that outcome-only rewards can drive substantial capability gains. However, this supervision is fundamentally coarse: any rollout with the correct final answer receives the same positive signal, regardless of whether the intermediate reasoning is valid. For reasoning tasks, that creates an optimization mismatch between the objective being optimized and the behavior we actually want.

This mismatch is not hypothetical. @zheng2024processbench shows that models frequently make process-level reasoning errors that require step-wise critique to identify, and @wang2025falsepositives shows that mathematically correct outputs often arise from shortcut behaviors such as answer guessing or jump-in reasoning. These flawed-positive trajectories are especially problematic under RLVR because they are rewarded exactly like fully correct derivations. As a result, policy optimization can reinforce unreliable reasoning patterns rather than genuine problem-solving competence.

The opportunity is to augment RLVR with process-aware supervision without giving up the efficiency and scalability of rule-based training. Prior work on process reward models, especially @zhang2025processrm, indicates that intermediate-step evaluation can separate valid reasoning from merely successful outcomes, while @mahan2024genrm suggests that reward modeling as generation can provide interpretable, reasoning-aware judgments. At the same time, @liu2025r1zero implies that RL dynamics are stage-dependent and can amplify shortcuts if the reward signal is misaligned. This suggests a more precise problem definition: we need an online-capable mechanism to detect flawed-positive rollouts and a training objective that uses this signal adaptively, preserving the early learning utility of shortcut-derived correct answers while preventing them from dominating later optimization.

## Method (verbatim from corpus proposal record)

We propose Flawed-Aware Policy Optimization, a process-sensitive extension of GRPO-based RLVR. The core idea is to detect correct-answer rollouts that contain invalid intermediate reasoning, then modify their training contribution so they can act as useful stepping stones early in learning but are progressively penalized once the policy can produce fully correct trajectories. This directly addresses the reward-alignment gap in outcome-only RLVR by distinguishing answer correctness from reasoning validity while remaining compatible with scalable training pipelines from @shao2024deepseekmath and @yu2025dapo.

1. **Generative flawed-positive detector**: We train a compact generative reward model to judge whether a rollout is fully correct or flawed positive, and to predict the earliest erroneous reasoning step. This draws on the generative reward modeling formulation in @mahan2024genrm and the process-assessment motivation in @zheng2024processbench. A generative judge is needed because scalar outcome rewards cannot expose where a correct-answer trajectory became invalid.

2. **Step-wise reward for error localization**: The reward model is optimized with a combined objective consisting of an outcome-level correctness reward and a process-level penalty proportional to the distance between the predicted and gold error step. This extends the process supervision lessons of @zhang2025processrm by encouraging true error localization rather than coarse yes/no classification or label guessing. It is necessary because flawed-positive detection is only useful for RL if the judge reliably separates genuinely valid reasoning from shortcut-derived success.

3. **Flawed-aware reward shaping in RLVR**: We replace the standard outcome-only positive reward for detected flawed-positive rollouts with a penalized reward inside the GRPO training loop. Building on @shao2024deepseekmath, this keeps the efficient group-relative optimization structure intact while correcting its main blind spot: under vanilla RLVR, fully correct and flawed-positive rollouts receive identical policy advantages. By changing only the reward assignment, the method remains a drop-in modification for existing RLVR systems such as @yu2025dapo.

4. **Dynamic advantage shift via group-relative statistics**: The reward adjustment is designed so that the effective optimization pressure changes with the composition of the sampled rollout group. Inspired by the stage-dependent shortcut dynamics highlighted in @liu2025r1zero and the prevalence of false positives documented by @wang2025falsepositives, this mechanism allows flawed positives to contribute during warm-up when valid positives are scarce, but automatically downweights them once fully correct rollouts become the majority. This is needed to avoid the failure mode of uniformly suppressing trajectories that are helpful early but harmful later.

5. **Asynchronous integration for practical online use**: The generative reward model is deployed as an external asynchronous service during RL training so rollout generation, reward judging, and actor updates can proceed without tightly coupled latency. This extends the scalable system perspective of @yu2025dapo by making process-aware judging feasible in large-scale RLVR. It is necessary because flawed-positive detection is only valuable if it can be inserted into training without negating the efficiency benefits of rule-based RL.

These components form a coherent system: the generative judge supplies process-validity information that outcome rewards lack, and the flawed-aware GRPO objective converts that signal into a stage-appropriate optimization bias. Together they preserve early exploration benefits while steering the policy toward shorter, more reliable, and more stable reasoning trajectories.
