# Digest (backfilled from local OpenReview idea-proposal corpus): SWE-Lancer: Can Frontier LLMs Earn $\$ 1$ Million from Real-World Freelance Software Engineering?

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `xZXhFg43EI` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: xZXhFg43EI
- **Title**: SWE-Lancer: Can Frontier LLMs Earn $\$ 1$ Million from Real-World Freelance Software Engineering?
- **URL**: https://openreview.net/forum?id=xZXhFg43EI
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

Research on evaluating AI systems for software engineering has progressed from synthetic coding problems to repository-level issue resolution, most notably in SWE-bench (@jimenez2024swebench) and SWE-bench Verified (@chowdhury2024verified). These benchmarks demonstrate that real codebases and stricter verification dramatically increase task difficulty. However, they remain limited to open-source contexts, rely primarily on unit tests, and provide success metrics that are disconnected from real economic value. As a result, they cannot answer how much commercially relevant software engineering work models can actually perform.

A second limitation is that existing benchmarks almost exclusively assess individual contributor behavior. While some work evaluates higher-level reasoning such as idea generation (@si2024ideas), there is no benchmark that measures models’ ability to make technical management decisions, such as selecting among competing implementation proposals. This omission is significant because real-world software development, particularly in freelance and contract settings, requires both implementation and evaluative judgment. Additionally, methodological work on testing (@brar2015integration) shows that unit tests are insufficient for capturing full-system behavior, yet most benchmarks continue to rely on them.

These gaps matter because freelance software engineering represents a large, economically meaningful segment of the software industry (@gupta2020freelancers). Without benchmarks grounded in real payouts, full-stack behavior, and managerial decisions, it is impossible to assess the true economic impact of frontier models or to forecast their effects on labor and productivity. This creates an opportunity to design an evaluation that directly ties model performance to market value while preserving rigor and contamination resistance as emphasized by @jain2024livecodebench.

## Method (verbatim from corpus proposal record)

We propose SWE-Lancer, a benchmark that evaluates frontier language models on real-world freelance software engineering tasks with verified end-to-end grading and market-derived rewards. The core idea is to align technical evaluation with economic value by sourcing tasks from real freelance jobs, grading them via system-level tests, and mapping success directly to actual monetary payouts. This formulation addresses the gap between benchmark success and real-world impact.

1. **Freelance Task Sourcing**: We collect software engineering tasks from real freelance job postings, grounding each task in a commercial codebase and attaching the actual payout paid to human engineers. This extends repository-level realism from @jimenez2024swebench into an economically meaningful setting, motivated by the distinct role of freelancers identified by @gupta2020freelancers.

2. **End-to-End Test Verification**: Each individual contributor task is graded using professionally written and triple-verified end-to-end tests that simulate real user workflows. This component directly addresses the limitations of unit-test-based grading highlighted by @brar2015integration and builds on the rigor emphasized in @chowdhury2024verified.

3. **SWE Management Evaluation**: In addition to coding tasks, we introduce management tasks where models select among competing implementation proposals. This extends beyond generation-focused evaluations and responds to the decision-quality gap identified by @si2024ideas, using real historical manager choices as ground truth.

4. **Contamination-Aware Benchmark Design**: We release a public evaluation split and maintain a private holdout set, with execution in a controlled, offline environment. This design follows principles from @jain2024livecodebench to minimize contamination and preserve long-term benchmark validity.

5. **Economic Performance Metrics**: Model success is measured not only by task completion rate but by total payout earned, directly mapping technical capability to economic value. This metric provides a market-calibrated difficulty gradient absent from prior SWE benchmarks.

Together, these components form a coherent system that evaluates full-stack implementation, managerial judgment, and economic impact within a single framework, enabling more realistic assessment of AI progress in software engineering.
