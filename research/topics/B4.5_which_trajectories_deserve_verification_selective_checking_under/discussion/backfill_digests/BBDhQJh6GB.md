# Lightweight digest (backfill): Test-time Verification via Optimal Transport: Coverage, ROC, & Sub-optimality

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: Test-time Verification via Optimal Transport: Coverage, ROC, & Sub-optimality
- **OpenReview id**: BBDhQJh6GB
- **URL**: https://openreview.net/forum?id=BBDhQJh6GB

## Motivation (from the paper's own OpenReview submission text)

Inference-time verification has emerged as a powerful mechanism for improving the performance of language models by leveraging additional compute through repeated sampling and selection. Empirical studies show that repeatedly sampling candidate responses and verifying them can dramatically improve task success rates, particularly on domains such as code generation and mathematical reasoning where correctness can be checked automatically. For example, @brown2024languagemonkeys demonstrates that coverage—the probability that at least one generated sample solves the task—scales predictably with the number of samples, producing strong empirical gains. However, these analyses largely treat the verifier as perfectly reliable and focus primarily on scaling laws rather than the structural properties of the resulting sampling policies.

More recent theoretical work highlights two critical limitations of this perspective. First, the effectiveness of sampling-based alignment depends heavily on the generator’s coverage and on constraints that limit how much the resulting policy may deviate from the reference model, as formalized by @huang2025bestofn. Second, verifier imperfection fundamentally alters the behavior of inference-time algorithms: @dorner2025rocnreroll shows that the performance of common strategies such as rejection sampling or Best-of-N depends directly on the geometry of the verifier’s ROC curve. Meanwhile, analyses of Best-of-N alignment such as @beirami2024bestofn and @aminian2025bestofnsmoothing characterize divergence and regret properties of specific algorithms but do not provide a unified framework capturing the joint influence of coverage, verifier accuracy, and algorithm design. As a result, existing theory cannot explain how these factors collectively determine the achievable performance of verifier-guided sampling.

This gap motivates a more general formulation of test-time verification. Specifically, we seek a framework that characterizes how probability mass must be redistributed from the generator distribution toward high-reward responses while respecting coverage constraints and operating under imperfect verifier feedback. Such a framework would allow principled reasoning about algorithm design, compute scaling, and verifier quality within a single geometric model.

## Method (from the paper's own OpenReview submission text)

We propose to model verifier-guided test-time scaling as an optimal transport problem between the generator distribution and a verifier-defined optimal policy under coverage constraints. In this formulation, the reference model defines a proposal distribution over responses, while the optimal policy corresponds to a target distribution that maximizes expected reward subject to a coverage constraint similar to that proposed in @huang2025bestofn. Sampling algorithms implement approximate transport plans that move probability mass from the generator toward this target distribution using only noisy membership feedback from the verifier. This transport perspective enables a decomposition of sub-optimality into intrinsic transport cost and policy improvement terms determined by verifier accuracy.

1. **Coverage-Constrained Optimal Policy Formulation**: We define the optimal inference-time policy as the reward-maximizing distribution within a divergence-constrained neighborhood of the generator, following the coverage framework introduced by @huang2025bestofn. This constraint ensures that the target distribution remains realizable through sampling from the generator. The resulting policy defines the target distribution toward which the sampling process attempts to transport probability mass.

2. **Optimal Transport Interpretation of Sampling**: We model the sampling process as constructing a coupling between the generator distribution and the target policy. The transport cost is defined using Hamming distance between proposed and accepted responses, capturing the expected rejection rate required to transform the generator distribution into the optimal policy. This formulation draws conceptual inspiration from divergence-based analyses of inference-time alignment such as @aminian2025bestofnsmoothing and @beirami2024bestofn, but reframes them in a geometric transport setting.

3. **Verifier-ROC-Aware Sub-Optimality Decomposition**: Because the target distribution cannot be accessed directly, the algorithm relies on an imperfect verifier whose behavior is characterized by ROC statistics, following insights from @dorner2025rocnreroll. We derive a decomposition in which sub-optimality equals the optimal transport cost multiplied by a policy-improvement factor determined by the verifier’s Youden index. This reveals how verifier accuracy mediates the ability of sampling algorithms to approximate the optimal transport plan.

4. **Transport-Based Sampling Algorithms**: We design sampling algorithms that explicitly approximate the transport plan under verifier feedback. Sequential rejection sampling constructs a coverage-aware acceptance rule that respects the admissible policy class, while sequential maximal coupling attempts to minimize transport cost through coupling-based sampling. Batched variants extend the approach to parallel generation settings, enabling comparison with Best-of-N strategies analyzed in prior work such as @beirami2024bestofn.

Together, these components produce a unified geometric framework in which generator coverage, verifier ROC, and algorithm design jointly determine performance. The transport formulation reveals a three-regime structure—transport-dominated, policy-improvement, and saturation—that explains observed inference-time scaling behaviors and guides the design of sampling algorithms tailored to different coverage regimes.
