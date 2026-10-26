# Digest (manual, cache-integrity fix): ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: WVhgFSKniL), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents
- OpenReview: https://openreview.net/forum?id=WVhgFSKniL
- paper_id: WVhgFSKniL

## N2-style Motivation (verbatim from mined proposal text)
LLM agents are vulnerable to indirect prompt injection because they consume untrusted tool outputs as part of the reasoning context. Benchmarks such as @zhan2024injecagent and @debenedetti2024agentdojo make this risk concrete, showing that malicious content embedded in emails, web pages, or API responses can redirect agent behavior. However, the attack formulations studied in these settings are predominantly plain-text: the attacker inserts imperatives into tool-returned content and relies on semantic persuasion alone to override the user's task.

This leaves a specific technical gap. Modern chat-based agents do not process inputs as undifferentiated text; they are trained with chat templates that encode an instruction hierarchy across roles, as formalized by @wallace2024instructionhierarchy. At the same time, @jiang2024chatbug shows that these template tokens are themselves exploitable structural interfaces. Existing indirect injection work, including adaptive attacks in @zhan2025adaptiveinjection, has not directly targeted this structural layer. As a result, current evaluations understate an attack surface where low-privilege tool content can be rewritten to mimic high-privilege system or user messages.

A second gap concerns interaction structure. Jailbreak work shows that persuasion becomes substantially stronger when delivered through staged dialogue rather than a single command, as demonstrated by @zeng2024persuasion and @weng2025footdoor. But indirect prompt injection is usually treated as one-shot because attackers only control a passive tool response. This creates an opportunity: if chat-template role tokens can be forged inside a tool output, then a single payload may simulate an entire multi-turn conversation. That would allow indirect prompt injection to exploit both structural authority and dialogue-based persuasion, potentially bypassing defenses and significantly increasing attack success in realistic agent environments.

## N6-style Method (verbatim from mined proposal text)
We propose ChatInject, a template-level indirect prompt injection attack that abuses chat-role formatting inside tool outputs. The core idea is to wrap malicious content in forged role tags so the model interprets attacker-controlled text as higher-priority conversational structure rather than untrusted tool data. We further extend this with a simulated multi-turn variant that embeds a fabricated dialogue history inside one payload, allowing one-shot tool-output attacks to inherit the effectiveness of multi-turn persuasion shown by @zeng2024persuasion and @weng2025footdoor.

1. **Role-Template Payload Forging**: We construct malicious tool outputs using model-aligned chat-template delimiters instead of plain text. This component is needed because the role hierarchy identified by @wallace2024instructionhierarchy implies that system- and user-formatted text receives higher authority than tool content; by forging these tags inside a tool response, we exploit the same structural dependency highlighted by @jiang2024chatbug. In the simplest variant, an attention-catching prefix is wrapped in system-role tags and the attack instruction is wrapped in user-role tags.

2. **Simulated Multi-Turn Dialogue Injection**: We encode a fabricated sequence of user and assistant turns within a single tool output, with the malicious action introduced gradually and justified contextually. This is needed to transplant the effectiveness of persuasive and staged attacks from interactive jailbreak settings into the one-shot indirect injection regime, extending insights from @zeng2024persuasion and @weng2025footdoor. Concretely, the dialogue is designed so earlier turns normalize the task, decompose it into harmless-looking substeps, and culminate in a final forged request to execute the attacker objective.

3. **Model-Specific and Unknown-Model Template Strategies**: We generate payloads with native chat templates when the target backbone is known, and with a mixture-of-templates wrapper when it is not. This component is needed because template similarity affects whether a payload is accepted as authoritative, a concern already suggested by the structural sensitivity exposed in @jiang2024chatbug. Extending the benchmark-oriented threat models of @zhan2024injecagent and @debenedetti2024agentdojo, the mixed-template strategy increases the chance that at least part of the payload matches the target model's latent formatting conventions.

4. **Agentic Formatting Hooks**: We augment template-based payloads with reasoning and tool-use scaffolds that resemble agent prompts, such as explicit thought-style wrappers or tool-call patterns. This is needed because practical LLM agents process not only dialogue roles but also reasoning and action schemas; aligning the payload with these conventions can further steer execution toward attacker-selected tools. This component extends the same structural attack principle beyond chat roles to the broader agent formatting context studied in @debenedetti2024agentdojo and @zhan2024injecagent.

5. **Evaluation Against Realistic Pipelines and Defenses**: We evaluate attack success rate and utility degradation in the agent environments introduced by @zhan2024injecagent and @debenedetti2024agentdojo, comparing plain-text injections, template-only injections, and multi-turn template injections. This component is needed to isolate whether gains come from structural role forgery, persuasive dialogue simulation, or their combination. We also test against existing prompt-based and detector-based defenses to measure whether methods built for plain-text injections remain effective against template-level attacks, as motivated by the defense failures reported in @zhan2025adaptiveinjection.

Together, these components form a coherent system: role-template forgery raises the authority of attacker content, simulated dialogue increases persuasive force, and model-aware formatting makes the attack practical across known and unknown backbones. The evaluation then tests whether this structural reformulation materially changes the security profile of LLM agents beyond what plain-text indirect prompt injection can achieve.

## Related works cited by this paper (as mined)
- InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents
- AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
- The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions
- ChatBug: A Common Vulnerability of Aligned LLMs Induced by Chat Templates
- How Johnny Can Persuade LLMs to Jailbreak Them: Rethinking Persuasion to Challenge AI Safety by Humanizing LLMs
- Foot-in-the-Door: A Multi-Turn Jailbreak for LLMs
- Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents
