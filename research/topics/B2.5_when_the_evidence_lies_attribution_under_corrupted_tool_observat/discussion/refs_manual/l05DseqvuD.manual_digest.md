# Digest (manual, cache-integrity fix): AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: l05DseqvuD), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?
- OpenReview: https://openreview.net/forum?id=l05DseqvuD
- paper_id: l05DseqvuD

## N2-style Motivation (verbatim from mined proposal text)
Multi-agent LLM systems now solve tasks through role specialization, message passing, and tool use, but this same structure makes them brittle. As shown by @hong2023metagpt and @li2023camel, these systems produce long collaborative trajectories in which one agent’s early output becomes another agent’s context, so a local mistake can propagate into a global failure. @cemri2025mast makes the severity of this problem explicit by documenting high failure rates and recurring failure modes across mainstream multi-agent frameworks. This implies that improving agentic systems requires more than end-task evaluation; it requires localizing the specific agent-step pair that first made success unattainable.

The core gap is that existing failure analysis methods do not provide scalable, causally grounded attribution. @zhang2025whowhen correctly formulates the problem as identifying the earliest decisive error step, but their results show that even strong reasoning models remain ineffective, especially for step-level localization. This failure is not simply a model-capability issue; it reflects a supervision issue. Available datasets are manually annotated and small, as seen in both @cemri2025mast and @zhang2025whowhen, while judge-style inference asks a general-purpose LLM to infer latent causal responsibility from long trajectories without enough task-specific training data.

This gap matters because precise attribution is the missing interface between failure observation and system improvement. Reflection-based methods such as @madaan2023selfrefine and critique-based methods such as @gou2024critic demonstrate that structured feedback can improve outputs, but they do not solve grounded credit assignment in multi-agent traces. If decisive error labels could be generated automatically at scale, failure attribution could become a trainable prediction problem rather than a brittle prompting problem. That creates the opportunity to build a specialized tracer whose outputs are accurate enough to support debugging, data curation, and iterative self-improvement of agentic systems.

## N6-style Method (verbatim from mined proposal text)
We propose an automated failure-attribution framework that converts decisive-error localization into a scalable learning problem. The central idea is to generate high-fidelity supervision by replaying trajectories under controlled counterfactual interventions and synthetic perturbations, then train a dedicated tracer with reinforcement learning to predict the responsible agent and earliest decisive step. This formulation directly addresses the data scarcity and weak-judge limitations exposed by @zhang2025whowhen and @cemri2025mast.

1. **Counterfactual Decisive-Error Discovery**: For each failed multi-agent trajectory, we replay the execution while replacing one step at a time with a minimally corrected action proposed by an analyzer model. The earliest step whose correction flips the final outcome from failure to success is labeled as the decisive error, implementing the causal definition introduced by @zhang2025whowhen. This is needed because superficial trace inspection is insufficient; attribution must be grounded in outcome-changing interventions rather than textual plausibility.

2. **Programmatic Fault Injection from Successful Traces**: To expand coverage beyond naturally failed runs, we perturb selected actions in successful trajectories and replay the downstream execution. If the perturbed run fails, the injected step is treated as the decisive error by construction, yielding synthetic but precise labels. This complements the limited manually annotated resources in @cemri2025mast and @zhang2025whowhen by producing diverse trajectory-error pairs at scale from the same structured multi-agent settings exemplified by @hong2023metagpt and @li2023camel.

3. **TracerTraj-Style Supervision Corpus**: We unify labels from counterfactual correction of failed traces and fault injection over successful traces into a single training corpus of annotated trajectory-to-error pairs. This component is needed because the attribution model must see both organic failure modes and controlled perturbation-induced failures to generalize across heterogeneous agentic systems. Relative to prior manually curated resources such as @cemri2025mast and @zhang2025whowhen, this dataset construction strategy shifts annotation from human judgment to executable causal verification.

4. **Specialized Failure Tracer via RL**: We train a compact language model to read the full trajectory and output the responsible agent and decisive step, using reasoning-oriented reinforcement learning inspired by @guo2025deepseekr1. RL is needed because attribution over long traces requires structured latent reasoning and output discipline that are not reliably induced by generic instruction tuning. By specializing the model on causally validated labels, we replace the unreliable LLM-as-judge behavior highlighted by @zhang2025whowhen with a dedicated failure-localization policy.

5. **Multi-Granular Reward for Agent and Step Attribution**: We optimize the tracer with rewards that separately score output format, exact agent identification, and proximity to the correct step. This component is necessary because step-level attribution is harder than agent-level attribution, and a smooth reward over temporal distance provides denser learning signal than all-or-nothing supervision. It extends the task definition of @zhang2025whowhen and the RL-based reasoning insight from @guo2025deepseekr1 into a training objective tailored to multi-agent failure localization.

Together, these components form a coherent system: causal replay generates trustworthy labels, synthetic corruption broadens the supervision distribution, and RL distills both into a dedicated tracer. The resulting model is designed not only to diagnose failures accurately, but also to provide structured feedback that can support the kind of iterative self-improvement envisioned by @madaan2023selfrefine and @gou2024critic.

## Related works cited by this paper (as mined)
- Why Do Multi-Agent LLM Systems Fail?
- Who & When: Failure Attribution in Multi-Agent LLM Systems
- DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
- Self-Refine: Iterative Refinement with Self-Feedback
- CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing
- MetaGPT: Meta Programming for Multi-Agent Collaborative Framework
- CAMEL: Communicative Agents for ‘Mind’ Exploration of Large Language Model Society
