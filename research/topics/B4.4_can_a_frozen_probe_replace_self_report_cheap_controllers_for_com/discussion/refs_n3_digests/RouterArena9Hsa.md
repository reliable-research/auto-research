# Digest (stub, corpus-grounded): RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers

> **Source disclosure.** This is a minimal N0/N1/N2/N6-only digest built from the OpenReview submission's own reconstructed proposal text in the local corpus (`openview_corpus/ideas.jsonl`, paper_id `9HsaIi4ngF`) -- no full PDF is cached locally for this OpenReview-only submission, so N3-N12 (related work read by the authors, results, threats, artifacts) are NOT available and are intentionally omitted rather than guessed. This is the same source digest.md's own N3/N4 quote from. Tag: [GROUNDED:corpus].

- **paper_id**: 9HsaIi4ngF
- **paper_url**: https://openreview.net/forum?id=9HsaIi4ngF

## N2 Motivation (verbatim from proposal.motivation)

Large language model ecosystems now contain a wide spectrum of models that differ significantly in capability, specialization, and inference cost. As demonstrated by routing systems such as FrugalGPT, selecting different models for different queries can substantially improve the cost–accuracy trade-off compared with using a single model for all tasks (@chen2023frugalgpt). This observation has motivated the development of numerous LLM routers that dynamically assign queries to models based on predicted difficulty, domain, or expected performance. Recent work such as @ong2025routellm further shows that router architectures and training paradigms are rapidly evolving, ranging from preference-based training methods to embedding-based or graph-based routing strategies.

However, the rapid growth of router methods has not been matched by equally robust evaluation infrastructure. Existing benchmarks such as @hu2024routerbench and @huang2025routereval provide valuable datasets and large-scale performance logs, but they largely rely on offline evaluation using precomputed model outputs and fixed datasets. This design limits their ability to measure real-world routing behavior, particularly when routers interact with evolving model ecosystems or when inference cost varies with generation length and token usage. Furthermore, prior benchmarks evaluate routers primarily through a small set of metrics, often focusing on accuracy or aggregate performance, while overlooking other critical deployment dimensions such as routing optimality, robustness to input perturbations, and routing latency.

Another limitation arises from dataset design. Studies such as @feng2025fusionbench highlight that existing routing datasets often cover a limited number of domains or tasks, making it difficult to assess whether routers generalize across diverse knowledge areas. Without domain diversity and difficulty-aware queries, it is challenging to evaluate a router’s ability to recognize when inexpensive models are sufficient and when more powerful models are necessary. These gaps collectively hinder systematic comparison of routers and obscure progress in routing research, motivating the need for a comprehensive and open evaluation platform tailored specifically to LLM routing systems.

## N6 Methodology (verbatim from proposal.method)

We propose ROUTERARENA, an open evaluation platform designed to systematically benchmark LLM routers under realistic deployment conditions. The key idea is to treat router evaluation as a live, multi-dimensional systems benchmark rather than a static offline dataset comparison. ROUTERARENA integrates a principled dataset with broad domain coverage and empirically calibrated difficulty levels, a comprehensive metric framework capturing multiple aspects of routing performance, and an automated infrastructure that evaluates routers through real inference and maintains a continuously updated leaderboard.

1. **Principled Domain-Diverse Evaluation Dataset**: We construct a router evaluation dataset designed to stress-test routing behavior across diverse knowledge domains. Inspired by the domain coverage gaps observed in benchmarks such as @feng2025fusionbench, the dataset follows a Dewey Decimal Classification–inspired structure that spans multiple knowledge domains and categories. This design ensures that routers must recognize domain characteristics and assign queries to models with different specializations.

2. **Difficulty-Calibrated Query Construction**: To evaluate routers’ ability to balance cost and accuracy, we introduce empirically calibrated query difficulty levels. Instead of relying solely on manual labels, we measure difficulty based on the fraction of models that can answer each query correctly, enabling clear separation between easy, medium, and hard queries. This mechanism operationalizes the cost–accuracy trade-off emphasized by routing approaches such as @chen2023frugalgpt.

3. **Multi-Dimensional Router Evaluation Metrics**: Building on limitations identified in existing benchmarks like @huang2025routereval, ROUTERARENA evaluates routers across multiple deployment-relevant dimensions. In addition to query-answer accuracy and inference cost, we introduce routing optimality metrics that assess whether routers select the cheapest correct model, robustness metrics that measure routing stability under perturbed inputs, and latency metrics that quantify routing overhead. Together, these metrics capture the full operational behavior of routers.

4. **Automated End-to-End Evaluation Framework**: Unlike offline benchmarks such as @hu2024routerbench, which rely on static model outputs, ROUTERARENA performs evaluation through real inference calls to the models selected by routers. The framework supports both open-source and commercial routers via standardized interfaces and automatically records routing decisions, costs, and latency. Prefix caching is used to improve evaluation efficiency when routers share overlapping model pools.

5. **Live Arena-Style Leaderboard**: Inspired by the open evaluation paradigm introduced by @chiang2024chatbotarena, ROUTERARENA maintains a continuously updated public leaderboard that ranks routers across multiple metrics. This leaderboard provides transparent and standardized comparison across routing methods and encourages ongoing submission of new routers as the model ecosystem evolves.

Together, these components form a unified platform that enables realistic, comprehensive, and continuously updated evaluation of LLM routing strategies, providing the community with a standardized infrastructure for measuring progress in multi-model AI systems.

## Status

PARTIAL -- motivation+method only, grounded in the paper's own OpenReview proposal text; N0/N1/N3-N12 not reconstructed here (see digest.md N3/N4 for this paper's role in the B4.4 lineage).
