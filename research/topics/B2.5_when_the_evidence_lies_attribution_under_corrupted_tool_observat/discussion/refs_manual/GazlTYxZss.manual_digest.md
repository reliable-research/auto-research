# Digest (manual, cache-integrity fix): Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems

> **Source note.** This is a lightweight digest constructed from the paper's own
> motivation+method proposal text as mined in `topics/corpus/ideas.jsonl`
> (paper_id: GazlTYxZss), NOT a full N0-N12 paper-digest extraction. Constructed to
> close a Phase A reference-cache-integrity gap (goal.md Sec.3 item 2): this
> work is cited in `digest.md` N3/N4 as a method-twin/baseline/adjacent work
> for B2.5 but had no resolvable `digest_path` in `reference_candidates.jsonl`.
> Treat as PARTIAL: re-run `paper-digest` in extraction mode against the primary
> source (OpenReview forum) before this record is used for anything beyond
> related-work framing.

## Paper
- Title: Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems
- OpenReview: https://openreview.net/forum?id=GazlTYxZss
- paper_id: GazlTYxZss

## N2-style Motivation (verbatim from mined proposal text)
LLM-powered multi-agent systems increasingly rely on benchmark-based evaluation to assess task success, yet the development cycle breaks down after failure: engineers must manually inspect long interaction logs to determine which agent and which action caused the failure. Existing evaluation frameworks, such as Agent-as-a-Judge, provide richer outcome-level and intermediate feedback but still stop short of assigning responsibility within the system (@zhuge2024agentjudge). As systems grow in scale and interaction length, this manual attribution becomes prohibitively expensive and inconsistent, as illustrated by complex collaborative frameworks like MetaGPT (@hong2023metagpt).

Prior work reveals several partial ingredients but no integrated solution. ProcessBench formalizes the notion of identifying the earliest decisive error in step-by-step reasoning, but only for single-model mathematical solutions (@zheng2024processbench). Reflexion shows that LLMs can analyze past trajectories and feedback signals, implying that failure logs already contain diagnostic information (@shinn2024reflexion). Meanwhile, MT-Bench establishes practical prompting patterns for LLM-based judging and demonstrates that such judges can approximate human assessments at scale (@zheng2023mtbench). What remains missing is a formal problem definition, dataset, and methodology that connect these ideas to automated failure attribution in multi-agent systems.

This gap matters because without automated attribution, evaluation results cannot efficiently drive system improvement. Treating evaluation as an endpoint leaves a critical blind spot between detecting failure and fixing it. The opportunity is to leverage existing evaluation logs and LLM judging capabilities to partially automate attribution, reducing human effort and enabling systematic analysis of failure patterns across agents and steps.

## N6-style Method (verbatim from mined proposal text)
We propose to formulate automated failure attribution in LLM multi-agent systems as a first-class judging problem and to study it through a new benchmark and baseline methods. The core idea is that evaluation logs already encode sufficient structured information to identify failure-responsible agents and decisive error steps when paired with an explicit counterfactual definition of failure and carefully designed LLM prompts. This formulation directly addresses the gap between evaluation and debugging by making attribution measurable and automatable.

1. **Formalization of Decisive Errors**: We define failure attribution in terms of decisive errors—agent–time pairs whose correction flips a failed trajectory into success—extending the earliest-error concept from ProcessBench to turn-based multi-agent systems (@zheng2024processbench). This formalization is necessary to disambiguate multiple mistakes and to ground attribution in a counterfactual criterion rather than heuristic blame.

2. **Who&When Dataset Construction**: We introduce the Who&When dataset, consisting of failure logs from diverse multi-agent systems with human annotations identifying failure-responsible agents and decisive steps. This dataset is needed because no existing benchmark provides agent- and step-level attribution labels, and it operationalizes the diagnostic task suggested but not addressed by prior evaluation work (@zhuge2024agentjudge).

3. **LLM-Based Attribution as Judging**: Building on LLM-as-a-Judge practices from MT-Bench, we frame attribution as a judging task where an LLM analyzes logs to output the responsible agent and step (@zheng2023mtbench). Prompt designs explicitly mitigate known judging biases and enable consistent comparisons across methods.

4. **Context Management Strategies**: Inspired by findings on long-context retrieval limitations (@nelson2024needle), we evaluate multiple attribution strategies—all-at-once, step-by-step, and binary search—to balance global context for agent identification with localized context for step identification.

5. **Hybrid Attribution Pipeline**: We combine complementary strategies by first identifying the likely failure-responsible agent using a global view, then localizing the decisive step within that agent’s actions. This component directly leverages the strengths of different judging formulations revealed by prior analysis.

Together, these components form a coherent system that formalizes, benchmarks, and operationalizes automated failure attribution, transforming evaluation logs into actionable debugging signals for multi-agent systems.

## Related works cited by this paper (as mined)
- Agent-as-a-Judge: Evaluate Agents with Agents
- Reflexion: Language Agents with Verbal Reinforcement Learning
- ProcessBench: Identifying Process Errors in Mathematical Reasoning
- Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- Needle in the Haystack for Memory-Based Large Language Models
- MetaGPT: Meta Programming for Multi-Agent Collaborative Framework
