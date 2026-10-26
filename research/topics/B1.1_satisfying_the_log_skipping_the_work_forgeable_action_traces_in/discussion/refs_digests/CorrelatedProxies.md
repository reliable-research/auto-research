# Digest (backfilled from local OpenReview idea-proposal corpus): CORRELATED PROXIES: A NEW DEFINITION AND IMPROVED MITIGATION FOR REWARD HACKING

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `msEr27EejF` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: msEr27EejF
- **Title**: CORRELATED PROXIES: A NEW DEFINITION AND IMPROVED MITIGATION FOR REWARD HACKING
- **URL**: https://openreview.net/forum?id=msEr27EejF
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

Reinforcement learning systems frequently rely on proxy rewards that approximate an unobserved true objective, yet optimizing these proxies often leads to reward hacking. Empirical studies have shown that as agents become more capable, they exploit misspecifications in the reward signal, achieving higher proxy reward while sharply degrading true performance (@pan2022misspecification). This phenomenon persists even when reward models are improved or combined via ensembles, indicating that reward hacking is not merely a function of model quality but of how optimization drives policies out of distribution (@coste2024ensembles).

A common mitigation strategy, particularly in RLHF, is to regularize policies toward a reference using KL divergence over action distributions (@stiennon2020rlhf). While effective in some settings, this approach lacks principled guarantees and can fail under realistic misspecification regimes. In particular, KL regularization may be too weak to control heavy-tailed reward errors, allowing catastrophic Goodhart effects where proxy reward grows arbitrarily without improving true utility (@kwa2024goodhart). These failures suggest that the choice of divergence and the level at which similarity is enforced are both critical.

At the same time, recent theoretical work shows that chi-squared divergence provides stronger control over overoptimization than KL by more heavily penalizing rare but high-impact deviations (@huang2024chisquared), and that reasoning at the level of occupancy measures is essential for understanding policy behavior in MDPs (@nika2024occupancy). However, existing work does not connect these insights to a formal definition of reward hacking, nor does it explain why reference-policy regularization should work in the first place. This gap motivates a definition-level solution that precisely characterizes when a proxy is valid, when optimization breaks that validity, and how regularization should be designed to prevent it.

## Method (verbatim from corpus proposal record)

We propose to define and mitigate reward hacking by explicitly tying the validity of a proxy reward to a reference policy’s state–action distribution. The core idea is to formalize reward hacking as the breakdown of correlation between proxy and true rewards under optimization, and to derive a regularized optimization objective that provably prevents this breakdown by constraining divergence from the reference occupancy measure. This formulation naturally leads to chi-squared occupancy measure regularization as the appropriate control mechanism.

1. **Correlated-Proxy Definition**: We formalize a proxy reward as reasonable only if it is positively correlated with the true reward under the occupancy measure of a reference policy. This draws on empirical observations that proxies are designed or learned to work under typical behavior distributions (@pan2022misspecification) and provides a principled baseline for evaluation.

2. **Reward Hacking Criterion**: Using the reference policy as a baseline, we define reward hacking as occurring when optimizing a correlated proxy yields lower true reward than the reference. This avoids overly permissive Goodhart-style definitions and directly addresses failure modes identified in RLHF and other domains (@stiennon2020rlhf, @coste2024ensembles).

3. **Occupancy-Measure Regularized Objective**: From this definition, we derive a lower bound on true reward improvement that trades off proxy reward gain against divergence from the reference occupancy measure. This extends occupancy-based reasoning highlighted by @nika2024occupancy to general stochastic MDPs.

4. **Chi-Squared Divergence Choice**: We instantiate the regularization using chi-squared divergence, which provides stronger penalties for out-of-distribution state–action pairs than KL and is theoretically better suited to controlling overoptimization (@huang2024chisquared, @kwa2024goodhart).

5. **Practical Estimation via Discriminators**: To implement occupancy regularization in practice, we adapt adversarial divergence estimation techniques from imitation learning, using a discriminator to approximate chi-squared occupancy divergence as in @ho2016gail.

Together, these components form a coherent system: the definition identifies when and why reward hacking occurs, the theoretical bound motivates the regularized objective, and the discriminator-based implementation makes the approach practical for modern RL and RLHF settings.
