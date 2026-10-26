# Digest (backfilled from local OpenReview idea-proposal corpus): Inference-Time Reward Hacking in Large Language Models

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `hSX7Dd8dxy` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: hSX7Dd8dxy
- **Title**: Inference-Time Reward Hacking in Large Language Models
- **URL**: https://openreview.net/forum?id=hSX7Dd8dxy
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

Inference-time alignment methods such as Best-of-n are widely used to improve large language model outputs using reward models, yet they rely on imperfect proxy rewards. Empirical evidence from @gao2023overoptimization shows that aggressively optimizing these proxies produces a characteristic peak-and-collapse in true reward, while theoretical analysis from @huang2025bestofn proves that Best-of-n inevitably suffers from reward hacking as n grows. These results indicate that inference-time optimization strength cannot be treated as monotonically beneficial.

Existing approaches either accept this risk or attempt ad hoc mitigations. Soft Best-of-n introduces temperature as a smoother control mechanism (@verdun2025softbon), and theoretical work connects BoN to KL-regularized reinforcement learning (@beirami2025bon, @gui2024bonbon). However, these methods still assume that increasing optimization toward the proxy is desirable, and they lack a principled way to determine when optimization becomes harmful. Moreover, as argued by @laidlaw2025correlated, reward hacking arises from systematic proxy–true reward mismatch, not noise that can be averaged away, implying that stronger optimization worsens the problem.

This gap matters because inference-time alignment is increasingly used as a substitute for fine-tuning, as emphasized by @welleck2024inference. Without principled control, practitioners risk deploying systems that overoptimize proxies and degrade real performance. The opportunity is to formally characterize when reward hacking is inevitable and to design inference-time mechanisms that explicitly hedge against it while retaining near-optimal reward–KL tradeoffs.

## Method (verbatim from corpus proposal record)

We propose a framework that formalizes inference-time reward hacking as a winner’s-curse phenomenon and mitigates it via principled hedging. The core idea is to view inference-time selection methods as inducing monotone-likelihood-ratio families over proxy rewards, which guarantees unimodal true reward behavior and enables calibrated parameter tuning. We introduce Best-of-Poisson sampling to approximate the optimal KL-constrained exponential tilt and HedgeTune to identify the hacking threshold.

1. **MLR-Based Formalization of Inference-Time Alignment**: We model inference-time methods such as BoN and SBoN as parameterized distributions over proxy reward quantiles with monotone likelihood ratios. This abstraction unifies empirical findings from @gao2023overoptimization and theoretical guarantees from @huang2025bestofn, and it establishes unimodality of true reward as a function of optimization strength.

2. **Best-of-Poisson Sampling**: We replace fixed-n BoN with a Poisson-randomized sample size, yielding a single-parameter method that closely approximates the optimal exponential tilt derived in KL-regularized alignment (@beirami2025bon, @gui2024bonbon). This randomization induces an exponential structure that spans the reward–KL frontier with negligible approximation error.

3. **Hedging via Optimal Parameter Selection**: Building on the unimodality guarantee, we derive analytic score functions for BoN, SBoN, and BoP that characterize the hacking threshold. This directly addresses the collapse observed by @gao2023overoptimization by identifying where marginal proxy gains no longer improve true reward.

4. **HedgeTune Algorithm**: We introduce an efficient root-finding procedure that estimates the optimal inference-time parameter using limited true reward feedback. This operationalizes hedging in practice and complements soft control mechanisms introduced by @verdun2025softbon.

Together, these components form a coherent system: BoP provides a near-optimal inference-time distribution, while HedgeTune calibrates it to avoid overoptimization, yielding robust reward–distortion tradeoffs under proxy misspecification.
