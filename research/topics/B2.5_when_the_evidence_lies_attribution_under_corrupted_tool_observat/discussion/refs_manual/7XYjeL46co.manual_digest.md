# Digest (manual, cache-integrity fix): MCP-SafetyBench: A Benchmark for Safety Evaluation of Large Language Models with Real-World MCP Servers

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: 7XYjeL46co), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: MCP-SafetyBench: A Benchmark for Safety Evaluation of Large Language Models with Real-World MCP Servers
- OpenReview: https://openreview.net/forum?id=7XYjeL46co
- paper_id: 7XYjeL46co

## N2-style Motivation (verbatim from mined proposal text)
Large language models are increasingly deployed as autonomous agents that interact with external tools through the Model Context Protocol (MCP). This architecture enables agents to dynamically discover and invoke tools across multiple servers, allowing them to perform complex tasks such as financial analysis, browser automation, and repository management. However, the openness of MCP significantly expands the attack surface. Prior studies have identified vulnerabilities such as tool poisoning, prompt injection, and malicious server behavior that can manipulate agent decision-making or lead to unauthorized actions. Empirical evidence from MCPTox (@wang2025mcptox) shows that even advanced LLM agents are highly vulnerable when malicious instructions are embedded in tool metadata, while broader analyses such as @hou2025mcplandscape highlight that threats can emerge across the full lifecycle of MCP systems, including server, host, and user layers.

Despite growing recognition of these risks, current evaluation frameworks fail to capture the realistic conditions under which MCP agents operate. Existing benchmarks often focus on narrow attack categories, such as tool poisoning in @wang2025mcptox, or provide taxonomy-driven attack collections without embedding them into realistic task workflows, as seen in @yang2025mcpsecbench. At the same time, capability-oriented benchmarks like MCP-Universe (@luo2025mcpuniverse) demonstrate that real MCP applications involve multi-step reasoning, dynamic tool selection, and coordination across multiple servers. These characteristics create complex interaction trajectories where vulnerabilities may emerge gradually during planning and execution. As a result, evaluating MCP security through isolated prompts or simplified tool calls provides an incomplete picture of real-world risks.

This gap creates a need for a benchmark that evaluates security within realistic agent workflows. Such a benchmark must integrate real MCP servers, diverse attack types across multiple system layers, and multi-turn task execution that mirrors practical deployments. Without this capability, it remains difficult to systematically measure the robustness of LLM agents in real MCP ecosystems or understand how different attack vectors interact with long-horizon agent planning.

## N6-style Method (verbatim from mined proposal text)
We propose MCP-SafetyBench, a benchmark designed to evaluate the safety of LLM agents operating in realistic MCP environments. The central idea is to embed a diverse taxonomy of MCP attacks directly into executable multi-step tasks that interact with real MCP servers. By combining realistic task workflows with systematic attack injection and execution-based evaluation, the benchmark measures both task success and attack success, enabling a comprehensive assessment of agent robustness in real-world MCP deployments.

1. **Real-World MCP Task Infrastructure**: We construct the benchmark on top of the task framework introduced by MCP-Universe (@luo2025mcpuniverse), which provides executable tasks interacting with real MCP servers and automated evaluators. This infrastructure allows agents to perform multi-turn reasoning and tool use across domains such as browser automation and financial analysis. Leveraging this framework ensures that evaluations occur in realistic environments rather than simulated or synthetic settings.

2. **Taxonomy-Driven Attack Modeling**: To systematically represent the MCP threat landscape, we derive a unified attack taxonomy informed by prior analyses such as @yang2025mcpsecbench and the lifecycle threat categorization in @hou2025mcplandscape. The benchmark organizes twenty attack types across three system layers: MCP server, MCP host, and user input. This design ensures coverage of diverse attack vectors including tool poisoning, function overlapping, intent injection, and credential theft.

3. **Attack-Embedded Task Construction**: Each baseline task is transformed into a security evaluation instance by injecting exactly one attack derived from the taxonomy. Server-side attacks modify tool manifests or implementations, host-side attacks alter planning pipelines, and user-side attacks introduce malicious prompts. This controlled attack injection process enables systematic evaluation while preserving realistic task structures.

4. **Execution-Based Dual Evaluation**: Following the evaluation paradigm of @luo2025mcpuniverse, we implement automated evaluators that analyze execution traces to determine both task success and attack success. Task evaluators verify whether the user goal is achieved, while attack evaluators detect whether the malicious objective has been realized. This dual-metric evaluation captures both system utility and security robustness.

Together, these components form a unified benchmarking framework that embeds diverse security threats within realistic MCP agent workflows. By combining real-server execution, taxonomy-driven attacks, and automated evaluation, MCP-SafetyBench enables systematic measurement of safety risks in modern tool-augmented LLM agents.

## Related works cited by this paper (as mined)
- MCP-Universe: Benchmarking Large Language Models with Real-World Model Context Protocol Servers
- MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers
- MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols
- MCP-AttackBench
- Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions
- MCP Security Notification: Tool Poisoning Attacks
