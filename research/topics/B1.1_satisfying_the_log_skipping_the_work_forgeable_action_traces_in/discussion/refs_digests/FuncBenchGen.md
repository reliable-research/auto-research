# Digest (backfilled from local OpenReview idea-proposal corpus): Towards Reliable Benchmarking: A Contamination Free, Controllable Evaluation Framework for Multi-step LLM Function Calling

> **Provenance note.** No PDF/full-text is locally cached for this record (no
> `pdf_path` available in this environment — no network access to fetch one).
> This digest is extracted from `topics/corpus/ideas.jsonl`'s proposal record
> for OpenReview id `UKYCJixSFt` (the same corpus `digest.md`'s N3 already grounds
> its `approach_summary` in). It is offered as the best available local
> evidence for this citation's motivation/method; treat it as PARTIAL relative
> to a full paper-digest extraction until/unless a PDF becomes available.

## Metadata
- **OpenReview id**: UKYCJixSFt
- **Title**: Towards Reliable Benchmarking: A Contamination Free, Controllable Evaluation Framework for Multi-step LLM Function Calling
- **URL**: https://openreview.net/forum?id=UKYCJixSFt
- **Domain**: ml
- **Related works cited by this paper (count)**: 7

## Motivation (verbatim from corpus proposal record)

Current benchmarks show that function-calling agents fail on realistic tool-use tasks, but they do not cleanly isolate why. Curated environments such as @li2023apibank and @patil2025bfcl are valuable for measuring end-to-end tool use, yet their fixed API sets and manually assembled tasks make it difficult to disentangle whether failure comes from API familiarity, scenario wording, domain-specific knowledge, or the underlying structure of the required call sequence. At the same time, multi-step settings such as @zhong2025complexfuncbench and long-context analyses such as @kate2025longfunceval show that chaining calls, searching over large tool catalogs, and handling long interaction histories are all challenging, but these benchmarks still offer limited control over dependency depth, branching structure, and the precise role of irrelevant tools.

This lack of structural control matters because tool-use performance is shaped by several distinct difficulty factors that should be studied independently. @qin2024toolllm indicates that simply increasing the number of available APIs stresses retrieval and planning, while @shi2023distracted suggests that irrelevant but plausible context can mislead reasoning. Existing benchmarks generally vary these factors through fixed datasets rather than through an explicit generative model, so they cannot systematically answer questions such as whether deeper dependency chains are harder than broader ones, or whether type-compatible distractors are more damaging than disconnected irrelevant tools.

A second limitation is benchmark validity over time. Because curated tool benchmarks expose public API descriptions and static tasks, they remain vulnerable to pretraining overlap and test-time leakage, a concern already implicit in large collected benchmarks like @li2023apibank and addressed more broadly by contamination-limited evaluation strategies such as @white2025livebench. This creates an opportunity for a benchmark generator that produces evaluation tasks on demand, while also parameterizing the latent dependency structure of multi-step tool use. Such a framework would enable contamination-free testing and controlled stress-testing of the exact reasoning mechanisms that current tool-use benchmarks reveal but do not precisely measure.

## Method (verbatim from corpus proposal record)

We propose a synthetic evaluation framework, FuncBenchGen, that represents multi-step function calling as traversal over a hidden function-dependency DAG. Instead of evaluating models on a fixed curated API environment, we generate synthetic function schemas and tasks at evaluation time, then vary graph properties such as dependency depth, graph size, and distractor connectivity to isolate specific failure modes. This formulation directly addresses the gaps exposed by @li2023apibank, @kate2025longfunceval, and @patil2025bfcl by combining contamination resistance with explicit control over structural task difficulty.

1. **Hidden Dependency DAG Generation**: We generate a directed acyclic graph whose core nodes define the required solution path from known inputs to a target variable. This component is needed to turn multi-step tool use into a parameterized structural problem, extending the chained function-calling perspective of @zhong2025complexfuncbench into a controllable graph-generation process. By specifying the number of core functions and dependency depth, we can separate shallow-star, branched, and path-like solution structures in a way fixed benchmarks cannot.

2. **Synthetic Function Schema Instantiation**: Each graph node is converted into a synthetic function with a random identifier, typed inputs, a single typed output, and a natural-language description. This component is needed to prevent contamination and memorization effects highlighted by @li2023apibank and @white2025livebench, since the functions do not correspond to public APIs or previously released benchmark items. It also preserves the essential inference problem of tool use: the model must infer executable dependencies from signatures and descriptions rather than from memorized API knowledge.

3. **Controllable Distractor Injection**: We add irrelevant functions in two forms: connected distractors that share type-compatible variables with the solution DAG, and disconnected distractors that remain structurally isolated. This component is needed to study the interaction between tool selection and distractibility, directly operationalizing the large-tool pressure observed in @qin2024toolllm and the irrelevant-context effect shown by @shi2023distracted. By varying the number and connectivity of distractors, we can measure whether failures arise from catalog size alone or from semantically plausible but incorrect alternatives.

4. **Deterministic Execution and Trace-Based Evaluation**: Functions return correct outputs only when given the exact required inputs; otherwise they return incorrect values, enabling automatic and objective scoring of complete function-call sequences. This component is needed to support scalable evaluation without subjective judgment, in the spirit of automatic evaluators used by @li2023apibank and @zhong2025complexfuncbench, while additionally enabling failure attribution to planning, schema use, sequencing, or state-tracking errors. The resulting traces make it possible to analyze not just success rate, but also where agents deviate from the correct dependency traversal.

5. **State Reminder Mitigation Interface**: We augment tool responses with an explicit restatement of all currently known variable values. This component is needed because execution traces reveal that many failures stem from stale or incorrectly propagated arguments rather than malformed calls, a limitation not isolated in prior fixed benchmarks such as @patil2025bfcl and @kate2025longfunceval. The interface is lightweight and benchmark-agnostic, serving as a practical intervention for testing whether explicit state grounding improves multi-step tool use.

Together, these components form a coherent system: the DAG defines the latent reasoning problem, synthetic schemas make evaluation contamination-free, distractors control confusability, deterministic execution enables precise measurement, and the mitigation interface tests a concrete hypothesis about state-tracking failures. This yields a benchmark that is both analytically rigorous and directly useful for diagnosing and improving LLM tool-use agents.
