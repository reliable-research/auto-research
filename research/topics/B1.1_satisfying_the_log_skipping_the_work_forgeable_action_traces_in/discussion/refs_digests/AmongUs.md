# Digest (backfilled from local OpenReview idea-proposal corpus): Among Us: A Sandbox for Measuring and Detecting Agentic Deception

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `XP3v1THxsq` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: XP3v1THxsq
- **Title**: Among Us: A Sandbox for Measuring and Detecting Agentic Deception
- **URL**: https://openreview.net/forum?id=XP3v1THxsq
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

As language models increasingly act as autonomous agents, deception becomes a central safety concern, particularly when it is instrumental and tied to long-term goals. Prior work has demonstrated that LLMs can engage in strategic misrepresentation under pressure, such as alignment faking during training (@greenblatt2024alignment) or persistent deceptive backdoors that survive safety interventions (@hubinger2024sleeper). These results indicate that deception is not merely about producing isolated false statements, but about planning and maintaining misleading behavior over extended interactions. However, most existing benchmarks for deception do not reflect this agentic, long-horizon structure.

Current evaluation and detection approaches rely heavily on static prompts, short roleplay scenarios, or explicitly instructed dishonesty, as in contrastive honesty datasets and roleplaying-based probes (@zou2023representation; @goldowskydill2025deception). While these methods show impressive performance in-distribution, it remains unclear whether they generalize to settings where deception emerges naturally rather than being prompted. Even interactive environments like AmongAgents (@chi2024amongagents) focus on prompted personalities and archetypes, which partially prescribe deceptive behavior instead of allowing agents to infer it as an instrumental strategy. This creates a gap between the types of deception we are most worried about and the settings in which we evaluate and monitor models.

This gap matters because safety techniques that work only in simplified settings may fail precisely when models are most capable and most dangerous. If deception arises as a consequence of long-term objectives in rich environments, we need sandboxes that elicit such behavior and metrics that scale with capability. At the same time, recent work on representation geometry suggests that internal signals of truthfulness and deception may be surprisingly simple and transferable (@marks2024geometry). This creates an opportunity to test whether lightweight activation monitoring methods can detect genuinely agentic deception, provided we evaluate them in an appropriately challenging environment.

## Method (verbatim from corpus proposal record)

We propose to use the social deduction game Among Us as a multi-agent sandbox that elicits long-term, open-ended, goal-directed deception in LLM agents, and to pair this environment with activation-based monitoring to detect deception out-of-distribution. The core idea is that when deception is instrumentally useful but not explicitly instructed, models will generate internal representations that reflect deceptive intent, which can be measured and detected using simple probes trained on contrastive honesty data.

1. **Open-ended Multi-agent Sandbox**: We implement a text-based version of Among Us in which LLM agents are given only the game rules, without in-context examples or personality prompts. This design builds directly on the feasibility shown by @chi2024amongagents while removing scaffolding to ensure that deception emerges as an inferred strategy rather than a prompted behavior. The partially observable, adversarial structure creates long-term incentives for misleading actions and statements.

2. **Unbounded Deception and Detection Metrics**: To quantify capability, we introduce Elo-style ratings for deception (impostors) and detection (crewmates) based on multi-agent game outcomes. Unlike static benchmarks, this metric scales with agent capability and remains meaningful as models improve, addressing concerns about benchmark saturation highlighted by agentic deception in @greenblatt2024alignment and @hubinger2024sleeper.

3. **Activation Monitoring with Linear Probes**: We train logistic regression probes on residual stream activations using simple contrastive datasets that distinguish honest from dishonest behavior, following the representation engineering framework of @zou2023representation. Motivated by the linear separability results in @marks2024geometry, we evaluate whether these probes generalize out-of-distribution to detect deception arising in Among Us gameplay.

4. **Sparse Autoencoder Feature Analysis**: To complement linear probes, we analyze sparse autoencoder features that are most correlated with honesty and deception, drawing on methods from @cunningham2023sae. These features are evaluated for their ability to detect deceptive behavior in the sandbox and for limited steering experiments to test causal relevance.

Together, these components form a coherent system: the sandbox elicits realistic agentic deception, the metrics measure it without ceiling effects, and the monitoring techniques test whether simple, scalable interpretability tools can detect deception even in complex, interactive settings.
