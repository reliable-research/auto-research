# Digest (manual, cache-integrity fix): ResiliBench: Evaluating Agentic Workflow Adaptation in Stochastic Environments

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: KTZ56LG7jZ), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: ResiliBench: Evaluating Agentic Workflow Adaptation in Stochastic Environments
- OpenReview: https://openreview.net/forum?id=KTZ56LG7jZ
- paper_id: KTZ56LG7jZ

## N2-style Motivation (verbatim from mined proposal text)
Existing benchmarks show that LLM agents can retrieve APIs, plan multi-step tool sequences, and act in interactive environments, but they do not isolate robustness under uncertainty as a primary evaluation target. @qin2023toolllm and @li2023apibank demonstrate the value of structured tool registries, executable environments, and multi-step tasks, yet both are designed around assessing whether models can discover and use tools correctly under relatively clean conditions. @liu2023agentbench extends evaluation to interactive agent settings, and @patil2023gorilla highlights realistic API-style invocation challenges, but neither framework systematically controls tool unreliability or instruction degradation. As a result, current evaluation mixes many sources of failure without measuring whether an agent can recover when a correct plan encounters probabilistic execution errors or when the provided workflow guidance is flawed.

This gap matters because production workflows rarely operate under deterministic assumptions. APIs timeout, validation fails, services become temporarily unavailable, and user-provided instructions are often incomplete or internally inconsistent. @xu2024agentcompany reveals that realistic benchmark environments can still remain largely deterministic at the tool-execution level, while @wang2024metatool shows that even benchmarks focused on tool generalization usually presume stable tools and high-quality task descriptions. The resulting opportunity is to build a benchmark where uncertainty is not incidental noise but the central experimental variable: by controlling both tool failure processes and instruction-quality perturbations, we can measure workflow adaptation directly rather than inferring it from aggregate task completion.

The specific research problem is therefore to evaluate how well LLM agents execute and adapt multi-step workflows when two uncertainty sources are introduced in a controlled way: stochastic tool behavior and degraded workflow instructions. We seek an evaluation setup that is scalable like simulated API benchmarks, interactive like agent benchmarks, and analytically grounded enough to provide a meaningful reference policy for expected success under probabilistic execution.

## N6-style Method (verbatim from mined proposal text)
We propose ResiliBench, a benchmark for evaluating agentic workflow execution under stochastic tool failures and varying instruction quality. The central idea is to generate workflow tasks in a simulated but API-realistic environment, derive high-quality workflow prompts from an MDP that models tool reliability, and then systematically perturb those prompts to test robustness. This formulation addresses the identified gap by separating three factors that prior benchmarks conflate: task structure, execution uncertainty, and instruction quality.

1. **Structured Stochastic Tool Environment**: We build a standardized tool registry with API-style signatures, typed parameters, and return schemas, following the scalable benchmark design principles of @li2023apibank and the broad API realism emphasized by @qin2023toolllm and @patil2023gorilla. Unlike those settings, each tool is also assigned parameterized probabilistic error modes such as timeout, invalid input, operational failure, calculation error, and overflow. This component is needed to make execution uncertainty an explicit, repeatable experimental factor rather than an uncontrolled artifact of real APIs.

2. **Interactive Multi-Step Workflow Tasks**: We generate multi-turn tasks with explicit tool dependencies, operation sequences, and completion criteria, extending the interactive-agent perspective of @liu2023agentbench to workflow execution. Tasks are constructed from semantic operation chains over the tool library so that agents must search, inspect, and invoke tools across several turns. This is necessary because robustness to failures can only be observed when agents must maintain state, react to feedback, and continue execution under sequential constraints.

3. **MDP-Derived Reference Workflows**: We formulate workflow generation as an MDP whose states capture execution progress and tool usage, and whose transitions incorporate known tool success probabilities. This component operationalizes an approximate upper bound on achievable success under probabilistic tools: unlike prior benchmarks such as @qin2023toolllm or @li2023apibank, we do not only supply a valid path, but a workflow optimized for expected success. It is needed so that evaluation can compare model behavior against reliability-aware guidance rather than against arbitrary demonstrations.

4. **Controlled Instruction Perturbation Suite**: Starting from the MDP-derived workflow, we inject systematic errors including step-order mistakes, tool misuse, parameter errors, missing steps, redundancy, logical discontinuities, and semantic drift. This extends the concern with tool-use generalization in @wang2024metatool by shifting attention from learning transferable tool knowledge to measuring resilience when guidance quality degrades. The component is necessary to quantify whether a model follows flawed instructions blindly or can implicitly correct them during execution.

5. **Unified Robustness Evaluation Protocol**: We evaluate agents with baseline, Chain-of-Thought, MDP-optimal, and flawed workflow prompts using full success, partial success, tool coverage, sequence correctness, output generation, and termination criteria. This combines the executable assessment style of @li2023apibank with the agent-centric environment philosophy of @liu2023agentbench, while adding robustness-specific comparisons absent from both. The protocol is needed to reveal not just average task completion but sensitivity to uncertainty along distinct axes.

Together, these components form a coherent system: the structured environment creates controllable uncertainty, the MDP provides a reliability-aware reference plan, and the perturbation framework tests whether agents can adapt beyond instruction following. This enables direct measurement of workflow resilience rather than generic tool-use competence.

## Related works cited by this paper (as mined)
- ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs
- API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs
- AgentBench: Evaluating LLMs as Agents
- Gorilla: Large Language Model Connected with Massive APIs
- TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks
- MetaTool: Facilitating Large Language Models to Master Tools with Meta-Task Augmentation
