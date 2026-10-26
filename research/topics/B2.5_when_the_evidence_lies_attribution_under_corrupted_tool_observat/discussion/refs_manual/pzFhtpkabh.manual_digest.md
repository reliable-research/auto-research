# Digest (manual, cache-integrity fix): Stop Wasting Your Tokens: Towards Efficient Runtime Multi-Agent Systems

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: pzFhtpkabh), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: Stop Wasting Your Tokens: Towards Efficient Runtime Multi-Agent Systems
- OpenReview: https://openreview.net/forum?id=pzFhtpkabh
- paper_id: pzFhtpkabh

## N2-style Motivation (verbatim from mined proposal text)
Multi-agent LLM systems are increasingly used for long-horizon tasks, but their practical bottleneck is not only raw capability; it is unstable execution. Existing evidence shows that failures often arise from repeated reasoning loops, inter-agent misalignment, and weak verification pathways rather than from an inability to solve the task in principle. In particular, @cemri2025masfailures makes clear that these systems exhibit recurring operational failure modes, while @shen2025propagation shows that erroneous intermediate outputs can spread through communication chains and amplify downstream damage. The core problem is therefore process-level: once execution enters a faulty or inefficient trajectory, current systems have little mechanism to detect and correct it in real time.

A second gap is that efficiency failures and robustness failures are entangled. @qian2025smart demonstrates that agent behavior can be monitored to reduce unnecessary external actions, suggesting that wasteful trajectories are behaviorally identifiable rather than random. At the same time, @chen2024agentpoison reveals that memory and retrieved knowledge can inject corrupted evidence into later reasoning, so token-heavy execution is not merely expensive; it also creates more opportunities for bad information to persist and compound. Existing interventions do not address this combination well. Post-hoc analyses such as those motivated by @cemri2025masfailures explain why a system failed after the fact, while topology-level approaches such as @shen2025propagation improve aggregate communication structure without controlling specific runtime incidents.

This gap matters most on realistic assistant workloads. @mialon2023gaia emphasizes that challenging benchmark tasks require multi-step reasoning, tool use, and long interaction traces, which are exactly the conditions under which loops, noisy observations, and propagated misinformation become costly. Although @xie2025aworld shows that adding a dedicated guard-like role can improve reliability, its focus is primarily verification at selected steps rather than general runtime supervision. This creates a clear opportunity: introduce a lightweight supervisory layer that monitors high-risk interactions during execution and intervenes only when necessary, so the system gains both robustness and token efficiency without requiring a redesign of the base agent architecture.

## N6-style Method (verbatim from mined proposal text)
We propose a supervised multi-agent framework centered on a lightweight meta-agent, SUPERVISORAGENT, that performs selective runtime oversight. The key idea is to monitor only the interaction events where failures and token waste concentrate, then apply targeted interventions matched to the detected risk. This formulation addresses the identified gap by turning failure analysis into proactive process control while keeping the overhead low enough to preserve overall efficiency.

1. **High-Risk Interaction Monitoring**: We supervise three interaction channels: agent-agent communication, agent-tool execution, and agent-memory retrieval. This choice is motivated by the propagation and contamination risks identified in @shen2025propagation and @chen2024agentpoison, which show that these channels are where local mistakes become system-level failures. By attaching supervision to interfaces rather than to a specific agent architecture, the framework remains modular and MAS-agnostic.

2. **Adaptive Trigger Filter**: We introduce an LLM-free filter that activates the supervisor only under three conditions: explicit error occurrence, inefficient repetitive behavior, and excessive observation length. This component is needed because always-on supervision would erase efficiency gains; instead, we leverage the observation from @cemri2025masfailures that problematic events are recurrent and concentrated, and the behavioral monitoring intuition from @qian2025smart that inefficient trajectories can be recognized from simple runtime signals. The filter makes supervision sparse, cheap, and high-leverage.

3. **Memory-Augmented Supervisor Context**: Once triggered, SUPERVISORAGENT receives a structured context consisting of the global task, local task, current interaction summary, recent local trace, and when needed a global trace across agents. This broader state view is necessary because many inefficiencies and coordination errors are only visible across multiple steps or multiple agents, consistent with the system-level failures characterized in @cemri2025masfailures. It extends the specialized oversight idea in @xie2025aworld from narrow verification to holistic runtime diagnosis.

4. **Multi-Level Intervention Policy**: The supervisor selects among approve, provide_guidance, correct_observation, and run_verification depending on issue type and severity. This action space is needed to avoid a one-size-fits-all response: some repetitive behavior should continue, some trajectories need only a hint, and others require direct correction or external verification. The design broadens the guard-agent concept in @xie2025aworld and operationalizes the efficiency and robustness concerns surfaced by @qian2025smart, @shen2025propagation, and @chen2024agentpoison.

5. **Observation Purification for Long-Horizon Tasks**: For excessively long or noisy tool outputs, the supervisor replaces raw observations with purified versions that preserve task-relevant signal while reducing token load. This is especially important on realistic assistant workloads like those emphasized by @mialon2023gaia, where long web pages and verbose tool responses can dominate cost and distract subsequent reasoning. The component complements behavioral guidance by directly reducing context noise at the moment it enters the system.

These components form a coherent system because they separate detection from intervention and make both interaction-aware. The adaptive filter keeps overhead small, while the supervisor’s richer context and graded action space ensure that interventions are targeted enough to improve robustness and efficiency simultaneously.

## Related works cited by this paper (as mined)
- Why Do Multi-Agent LLM Systems Fail?
- SMART: Self-Aware Agent for Tool Overuse Mitigation
- Understanding the Information Propagation Effects of Communication Topologies in LLM-Based Multi-Agent Systems
- AWorld: Multi-Agent Framework for Real-World Task Automation
- AgentPoison: Red-Teaming LLM Agents via Poisoning Memory or Knowledge Bases
- GAIA: A Benchmark for General AI Assistants
