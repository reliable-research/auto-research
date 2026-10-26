# Digest (manual, cache-integrity fix): Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: kga18ld70t), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents
- OpenReview: https://openreview.net/forum?id=kga18ld70t
- paper_id: kga18ld70t

## N2-style Motivation (verbatim from mined proposal text)
LLM-based agents introduce a specific evaluation problem: security failures often originate inside a single backbone model call, but existing benchmarks typically assess them only through end-to-end agent execution. This makes it difficult to attribute failures to the backbone LLM rather than to tool wrappers, control flow, retrieval components, or other conventional software layers. Both AgentDojo and ASB demonstrate the feasibility and importance of benchmark-based agent security evaluation, but they also reveal this attribution problem because they require modeling complete agents and their execution pipelines @debenedetti2024agentdojo @zhang2025asb.

A second limitation is threat coverage. InjecAgent focuses on indirect prompt injection in tool-using agents, which is important, but it leaves open whether a benchmark can systematically compare backbone LLMs across a broader range of attack vectors and attacker goals @zhan2024injecagent. At the same time, work on indirect prompt injection shows that the root vulnerability is not limited to one application pattern: LLMs often cannot reliably separate external data from operative instructions, and this weakness can manifest anywhere contextual text is consumed @greshake2023indirectprompt @yi2025indirectbenchmark. This suggests that the right unit of analysis is not the whole agent, but the individual model-call state where this confusion becomes actionable.

This gap matters because model developers and agent builders need a benchmark that isolates backbone security as a first-class property. HarmBench shows how standardization can accelerate progress by making model-level robustness measurable at scale, but its focus is broader harmfulness and refusal rather than adversarial exploitability inside agent workflows @mazeika2024harmbench. The opportunity, therefore, is to define an evaluation abstraction that preserves realistic agent context while avoiding full workflow simulation, enabling systematic coverage, cleaner attribution, and scalable comparison of backbone LLMs under agent-relevant attack scenarios.

## N6-style Method (verbatim from mined proposal text)
We propose threat snapshots, an abstraction that evaluates backbone LLM security by isolating a single LLM call together with its full execution context, attack insertion mechanism, attacker objective, and success metric. This formulation targets the specific gap in prior work: it preserves the contextual realism needed for agent-security evaluation while separating LLM-native vulnerabilities from surrounding agent implementation details, allowing broad and scalable benchmarking of backbone models.

1. **Threat Snapshot Abstraction**: We represent an agent security risk as a single execution-state snapshot containing the full model context for one LLM call, plus a formal specification of how an attack is inserted and how success is scored. This is needed to decouple backbone-model vulnerabilities from whole-agent behavior, addressing the attribution limitations that remain in full-agent benchmarks such as @debenedetti2024agentdojo and @zhang2025asb. The abstraction is grounded in the observation, emphasized by indirect prompt-injection work, that many exploits arise from how the model interprets contextual text at a particular call site @greshake2023indirectprompt @yi2025indirectbenchmark.

2. **Attack Taxonomy for Coverage**: We organize threats along complementary dimensions such as attack vector, attack objective, and affected task type, then instantiate snapshots to cover this space. This is needed because narrow benchmarks centered on indirect prompt injection do not expose the full range of agentic vulnerabilities relevant to backbone selection @zhan2024injecagent. Our taxonomy extends the structured categorization spirit of prior benchmarking work into an agent-specific, LLM-call-centric framework @yi2025indirectbenchmark @zhang2025asb.

3. **Benchmark Construction via Curated Snapshots**: We build a compact but representative set of threat snapshots spanning different agent contexts, output modes, and defense settings. This is needed to balance breadth of security coverage with the practical requirement of collecting strong attacks per scenario, similar to the benchmark-design principles highlighted by @mazeika2024harmbench. By evaluating the same snapshots across many backbone LLMs, we obtain a comparable vulnerability score that reflects backbone susceptibility rather than idiosyncrasies of a full agent stack.

4. **Crowdsourced Adaptive Attack Collection**: We use a gamified red-teaming pipeline to gather large-scale, human-generated attacks tailored to each threat snapshot, then select high-performing attacks for evaluation. This is needed because static prompt datasets lack adaptiveness and context specificity, especially in agent settings where attack efficacy depends strongly on the exact state being targeted. The design directly builds on the evidence from @pfister2025gandalf that crowdsourced challenges can efficiently surface realistic, high-quality adversarial prompts.

Together, these components form a coherent system: threat snapshots define the atomic evaluation unit, the taxonomy ensures systematic coverage, the benchmark operationalizes cross-model comparison, and adaptive crowdsourcing supplies realistic attacks strong enough to make the benchmark meaningful.

## Related works cited by this paper (as mined)
- AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents
- Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-Based Agents
- InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents
- Not What You’ve Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal
- Gandalf the Red: Adaptive Security for LLMs
- Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models
