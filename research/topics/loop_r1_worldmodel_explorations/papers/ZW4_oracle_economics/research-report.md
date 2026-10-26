> **⚠️ SUPERSEDED SOURCE ARTIFACT — DO NOT CITE AS CURRENT.**
> This is the unedited AutoDiscussion research report, kept for provenance. It still contains
> the saturated 120-cell factorial, log-spaced interpolation, crossover bisection, and Re:Form as a structured-proof arm, all of which were corrected during review.
> **Current design: `paper-draft.revised.md` and `experiment-spec.md`.** See `../MAJORS.md`.

# ZW4 The Oracle Economics of Code RL: A Cost-Normalized Phase Diagram of Execution versus Proof Supervision

> compute economics of verifiable-reward oracles for code post-training

_Research report — 6 confirmed steps._

## Problem Definition

**input:** Given instrumented runs in a shared code-RL harness using test outcome, execution process, binary proof, structured proof, and hybrid oracles, observe every oracle call, per-obligation solver latency, timeout, GPU usage, CPU usage, and capability, defined as held-out test-suite pass rate under a fixed sampling protocol. Runs span straight-line code, linear loops, nonlinear arithmetic, arrays and aliasing, and recursion; human-authored fixed and model-generated specifications; and approximately 50k, 200k, and 500k candidate generations per arm.

**output:** Produce equal-model-compute and equal-end-to-end-cost phase diagrams identifying the best oracle across each program family, specification quality, and budget, plus crossover locations, disagreements between orderings, complete latency and timeout distributions, and robustness to changes in the GPU-to-CPU price ratio.

**summary:** Proof supervision is claimed to make code reinforcement learning more efficient because proofs cover many executions and may require fewer rollouts. Solver and verifier calls can have heavy-tailed latency and timeouts, so fewer oracle calls need not mean cheaper training.

**objective:** Measure and compare oracle capability efficiency under both equal model-compute budgets and equal end-to-end cost budgets, using C = H_gpu*p_gpu + H_cpu*p_cpu. A good result establishes the ordering of oracle choices, exposes disagreements between the two budget definitions, and tests whether that ordering survives a threefold shift in the GPU-to-CPU price ratio.

**study type:** empirical

**constraints:** The study may not equate fewer executions with lower cost, omit solver CPU time, summarize heavy-tailed latency only by its mean, silently raise verifier effort for a favored arm, or treat planning estimates as measurements. Every obligation must use fixed resource and time limits with complete timeout reporting. Prices remain free variables supported by a dated price sheet, and comparisons must scale across all stated program, specification, and candidate-budget axes using observed capability rather than assumed oracle correctness.

**formal summary:** Given instrumented code-RL runs across five oracle types, program families, specification qualities, and candidate-generation budgets, produce a phase diagram measuring capability per unit end-to-end cost, subject to fixed verifier limits, complete latency and timeout accounting, separate equal-compute and equal-cost comparisons, and price-robustness analysis.

## Research Significance

**summary:** The dominant efficiency argument for proof supervision rests on rollout counts rather than audited end-to-end cost. Verifier workloads can contain difficult assertions, highly variable solver costs, and timeouts. Auditing the crossover prevents the broader literature from over-claiming efficiency.

**evidence:** Primary-source checks dated 2026-08-21 show that Re:Form separates wall-clock time and GPU counts, reports no GPU-hour figure, and limits its 40-epoch detail to the 3B run, leaving end-to-end GPU cost unauditable. Dafny documentation warns that assertions may become unexpectedly hard, time out, or vary widely in solver cost. ExecVerify, RLEF, StepCodeReasoner, ORPS, and muCODE report capability without cost-normalized comparison to a proof oracle; no surveyed work charges solver CPU and GPU time under equal end-to-end cost.

**who cares:** Code-RL researchers choosing supervision signals, authors evaluating proof-based training, reviewers assessing efficiency claims, engineers budgeting GPU and solver infrastructure, and practitioners selecting test, execution-process, proof, or hybrid oracles for particular program and specification regimes are directly affected.

**why it matters:** If proof coverage and heavy-tailed solver cost respond differently to program family, specification quality, and candidate budget, a global ranking can hide regime-specific winners; the phase diagram tests that possibility. Ignoring solver CPU can reverse rankings under equal end-to-end budgets, while price-sensitive rankings make efficiency claims conditional.

## Related Work

**summary:** Deeply compared the 8 most decisive PDF-grounded papers against our problem definition (0 candidate baselines, 0 high threats to our motivation). A further 14 cited work(s) are listed for coverage without a deep comparison (no fetchable full text, or less central than the top 8).

**general related works:**

-
  **summary:** Cited by the source draft. No openly fetchable full text, so this work is listed for coverage only and was not deeply compared against our problem.

  **work id:** 0b0e1e7f-f7c5-4d88-b681-efabc4cfe196

  **citation:** Hubert et al. Olympiad-level formal mathematical reasoning with reinforcement learning (AlphaProof). Nature 651(8106):607-613, 2026. DOI 10.1038/s41586-025-09833-y. No arXiv version exists.
-
  **summary:** Automated code generation with large language models has gained significant traction, but there remains no guarantee on the correctness of generated code. We aim to use formal verification to provide mathematical guarantees that the generated code is correct. However, generating formally verified code with LLMs is hindered by the scarcity of training data and the complexity of formal proofs. To tackle this challenge, we introduce AlphaVerus, a self-improving framework that bootstraps formally verified code generation by iteratively translating programs from a higher-resource language and leveraging feedback from a verifier. AlphaVerus operates in three phases: exploration of candidate transl

  **work id:** df0eee3b-1083-4f7d-bdc5-6e550a3557cf

  **citation:** Pranjal Aggarwal et al.. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement.
-
  **summary:** Large language models (LLMs) deployed as agents solve user-specified tasks over multiple steps while keeping the required manual engagement to a minimum. Crucially, such LLMs need to ground their generations in any feedback obtained to reliably achieve the desired outcomes. We propose an end-to-end reinforcement learning method for teaching models to leverage execution feedback in the realm of code synthesis, where state-of-the-art LLMs struggle to improve code iteratively compared to independent sampling. We benchmark on competitive programming tasks, where we achieve new state-of-the-art results with both small (8B parameters) and large (70B) models while reducing the amount of samples req

  **work id:** 067e067e-5ffb-4147-a78f-7d28524e26e6

  **citation:** Jonas Gehring et al.. RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING.
-
  **summary:** We address the problem of code generation from multi-turn execution feedback. Existing methods either generate code without feedback or use complex, hierarchical reinforcement learning to optimize multi-turn rewards. We propose a simple yet scalable approach, µCODE, that solves multi-turn code generation using only single-step rewards. Our key insight is that code generation is a one-step recoverable MDP, where the correct code can be recovered from any intermediate code state in a single turn. µCODE iteratively trains both a generator to provide code solutions conditioned on multi-turn execution feedback and a verifier to score the newly generated code. Experimental evaluations show that ou

  **work id:** b4360267-0515-4902-a2de-ea25ca7a2dab

  **citation:** Arnav Kumar Jain et al.. Multi-Turn Code Generation Through Single-Step Rewards.
-
  **summary:** Existing code reasoning methods primarily supervise final code outputs, ignoring intermediate states, often leading to reward hacking where correct answers are obtained through inconsistent reasoning. We propose StepCodeReasoner, a framework that introduces explicit intermediate execution-state supervision. By automatically inserting structured print-based execution-trace anchors into code, the model is trained to predict runtime states at each step, transforming code reasoning into a verifiable, stepwise execution modeling problem. Building on this execution-aware method, we introduce Bi-Level GRPO, a reinforcement learning algorithm for structured credit assignment at two levels: intertraj

  **work id:** fa51f210-cf0d-4883-8d02-802103f2fad5

  **citation:** Hao Wang et al.. StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning.
-
  **summary:** Program synthesis or code generation aims to generate a program that satisfies a problem specification. Recent approaches using large-scale pretrained language models (LMs) have shown promising results, yet they have some critical limitations. In particular, they often follow a standard supervised fine-tuning procedure to train a code generation model only from the pairs of natural-language problem descriptions and ground-truth programs. Such paradigm largely ignores some important but potentially useful signals in the problem specification such as unit tests, which thus often results in poor performance when solving complex unseen coding tasks. To address the limitations, we propose “CodeRL

  **work id:** b91df8b4-8216-4c33-aa28-c9a26f3fb1a2

  **citation:** Hung Le et al.. CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning.
-
  **summary:** Loop invariants are fundamental to reasoning about programs with loops. They establish properties about a given loop’s behavior. When they additionally are inductive, they become useful for the task of formal verification that seeks to establish strong mathematical guarantees about program’s runtime behavior. The inductiveness ensures that the invariants can be checked locally without consulting the entire program, thus are indispensable artifacts in a formal proof of correctness. Finding inductive loop invariants is an undecidable problem, and despite a long history of research towards practical solutions, it remains far from a solved problem. This paper investigates the capabilities of the

  **work id:** 14513aa9-ebc6-4c79-9ff9-e6e24ed402e7

  **citation:** Adharsh Kamath et al.. Finding Inductive Loop Invariants using Large Language Models.
-
  **summary:** The use of large language models for code generation is a rapidly growing trend in software development. However, without efective methods for ensuring the correctness of generated code, this trend could lead to undesirable outcomes. In this paper, we introduce a new approach for addressing this challenge: the Clover paradigm, short for Closed-Loop Verifiable Code Generation, which uses consistency checking to provide a strong filter for incorrect code. Clover performs consistency checks among code, docstrings, and formal annotations. The checker is implemented using a novel integration of formal verification tools and large language models. We provide a theoretical analysis to support our t

  **work id:** 09b02673-2e1f-4d13-8dd1-cc1334b89227

  **citation:** Chuyue Sun et al.. Clover: Closed-Loop Verifiable Code Generation.
-
  **summary:** The demonstrated code-understanding capability of LLMs raises the question of whether they can be used for automated program verification, a task that demands high-level abstract reasoning about program properties that is challenging for verification tools. We propose a general methodology to combine the power of LLMs and automated reasoners for automated program verification. We formally describe this methodology as a set of transition rules and prove its soundness. We instantiate the calculus as a sound automated verification procedure and demonstrate practical improvements on a set of synthetic and competition benchmarks.

  **work id:** d61008ad-9f7c-498d-abe3-77de818af9a3

  **citation:** Haoze Wu et al.. LEMUR: INTEGRATING LARGE LANGUAGE MODELSIN AUTOMATED PROGRAM VERIFICATION.
-
  **summary:** Mathematical theorem proving is an important testbed for large language models’ deep and abstract reasoning capability. This paper focuses on improving LLMs’ ability to write proofs in formal languages that permit automated proof verification/evaluation. Most previous results provide human-written lem mas to the theorem prover, which is an arguably oversimplified setting that does not sufficiently test the provers’ planning and decomposition capabilities. Instead, we work in a more natural setup where the lemmas that are directly relevant to the theorem are not given to the theorem prover at test time. We design an RL-based training algorithm that encourages the model to decompose a theorem

  **work id:** c389f429-594c-45a9-a20f-5ceb3d3f835b

  **citation:** Kefan Dong et al.. Formal Theorem Proving by Rewarding LLMs to Decompose Proofs Hierarchically.
-
  **summary:** We introduce DeepSeek-Prover-V2, an open-source large language model designed for formal theorem proving in Lean 4, with initialization data collected through a recursive theorem proving pipeline powered by DeepSeek-V3. The cold-start training procedure begins by prompting DeepSeek-V3 to decompose complex problems into a series of subgoals. The proofs of resolved subgoals are synthesized into a chain-of-thought process, combined with DeepSeek-V3’s stepby-step reasoning, to create an initial cold start for reinforcement learning. This process enables us to integrate both informal and formal mathematical reasoning into a unified model. The resulting model, DeepSeek-Prover-V2-671B, achieves sta

  **work id:** ec98f716-d19f-4b41-b0c6-bd195610f0be

  **citation:** Z.Z. Ren et al.. DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition.
-
  **summary:** We introduce Goedel-Prover-V2, a series of open-source language models that set a new state-of-the-art in automated theorem proving. Built on the standard expert iteration and reinforcement learning pipeline, our approach incorporates three key innovations: (1) Scaffolded data synthesis: We generate synthetic tasks of increasing difficulty to train the model to master increasingly complex theorems; (2) Verifier-guided self-correction: We enable the model to iteratively revise its proofs by leveraging feedback from the Lean compiler; (3) Model averaging: We merge model checkpoints to mitigate the decrease in model output diversity in later stages of training. Our small model, Goedel-Prover-V2

  **work id:** c39c9358-f680-4fb0-9eef-42cd6d95bb23

  **citation:** Yong Lin et al.. GOEDEL-PROVER-V2: SCALING FORMAL THEOREM PROVING WITH SCAFFOLDED DATA SYNTHESIS AND SELF-CORRECTION.
-
  **summary:** We introduce DeepSeek-Prover-V1.5, an open-source language model designed for theorem proving in Lean 4, which enhances DeepSeek-Prover-V1 by optimizing both training and inference processes. Pre-trained on DeepSeekMath-Base with specialization in formal mathematical languages, the model undergoes supervised fine-tuning using an enhanced formal theorem proving dataset derived from DeepSeek-Prover-V1. Further refinement is achieved through reinforcement learning from proof assistant feedback (RLPAF). Beyond the single-pass whole-proof generation approach of DeepSeek-Prover-V1, we propose RMaxTS, a variant of Monte-Carlo tree search that employs an intrinsic-reward-driven exploration strategy

  **work id:** 062a9739-4de9-4746-9ce5-11ee6d22c9a2

  **citation:** Huajian Xin et al.. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search.
-
  **summary:** The demand for synthetic data in mathematical reasoning has increased due to its potential to enhance the mathematical capabilities of large language models (LLMs). However, ensuring the validity of intermediate reasoning steps remains a significant challenge, affecting data quality. While formal verification via theorem provers effectively validates LLM reasoning, the autoformalisation of mathematical proofs remains error-prone. We introduce iterative autoformalisation, an approach that iteratively refines theorem prover formalisation to mitigate errors, thereby increasing the execution rate on the Lean prover from 60% to 87%. Building upon that, we introduce Theorem Prover as a Judge (TP-a

  **work id:** d1d8d087-52b1-4127-9644-bab524fd863f

  **citation:** Joshua Ong Jun Leang et al.. Theorem Prover as a Judge for Synthetic Data Generation.

**specific related works:**

-
  **input:** A natural-language programming-task description; Test cases supplied by the dataset or generated by the LLM; Previous reasoning, code, and execution feedback available during iterative refinement

  **output:** A program that implements the required functionality; A functionally correct and computationally efficient code solution

  **summary:** Large Language Models excel at code generation yet struggle with complex programming tasks that demand sophisticated reasoning. To bridge this gap, traditional process supervision relies on learned reward models requiring costly training data and suffering from reward misalignment, while outcome supervision fails for complex tasks needing coordinated intermediate steps. We introduce Outcome Refining Process Supervision, which unifies process and outcome supervision by leveraging executable verification: a treestructured search framework generates strategic alternatives, profiles execution metrics, and scores candidates via self-critique mechanisms that integrate runtime feedback with reasoning. Experiments across 5 models and 3 benchmarks show consistent gains, with 26.9% higher correctness and 42.2% improved code efficiency. The results demonstrate that ORPS enables LLMs to overcome local optima in code generation, suggesting a promising direction for combining verifiable outcomes with structured reasoning to tackle complex challenges. We open-source at: https: //github.com/zhuohaoyu/ORPS

  **work id:** 7a2b8926-4ffd-4173-bc50-c1792091d6dc

  **approach:** ORPS combines reasoning, candidate-code generation, execution profiling, self-critique, and weighted process-outcome rewards in a tree-structured beam search.

  **citation:** Zhuohao Yu et al.. Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** ORPS never poses the question of whether proof or verifier supervision is cheaper than test/execution supervision under matched budgets: it omits solver/verifier CPU time, heavy-tailed latency and timeout distributions, and the GPU-to-CPU price ratio, so it cannot establish an oracle ordering under equal model-compute versus equal end-to-end cost. It also does not span proof-based oracles (binary/structured/hybrid) or the program-family, specification-quality, and candidate-budget axes needed to build our phase diagrams.

  **method addresses:** false

  **method rationale:** ORPS is an inference-only tree search that produces better programs; it does not measure oracle capability-efficiency under equal-compute/equal-cost budgets, has no proof or verifier oracles, and does not model heavy-tailed solver latency, timeouts, or GPU/CPU price tradeoffs.

  **problem alignment:** related

  **alignment rationale:** Both concern using execution/process signals as supervision for code generation, but ORPS optimizes program correctness/efficiency at inference time whereas our problem measures the compute-and-cost efficiency of different oracle types (including proofs) as RL supervision signals.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] ORPS never poses the question of whether proof or verifier supervision is cheaper than test/execution supervision under matched budgets: it omits solver/verifier CPU time, heavy-tailed latency and timeout distributions, and the GPU-to-CPU price ratio, so it cannot establish an oracle ordering under equal model-compute versus equal end-to-end cost. It also does not span proof-based oracles (binary/structured/hybrid) or the program-family, specification-quality, and candidate-budget axes needed to build our phase diagrams.

    **limitation id:** lim-1

    **evidence for limitation:** Both concern using execution/process signals as supervision for code generation, but ORPS optimizes program correctness/efficiency at inference time whereas our problem measures the compute-and-cost efficiency of different oracle types (including proofs) as RL supervision signals. | ORPS is an inference-only tree search that produces better programs; it does not measure oracle capability-efficiency under equal-compute/equal-cost budgets, has no proof or verifier oracles, and does not model heavy-tailed solver latency, timeouts, or GPU/CPU price tradeoffs.

  **is potential baseline:** false
-
  **input:** A set of code implementations c; Dafny function signatures and program bodies with annotations missing

  **output:** Full Dafny code implementations with corresponding formal specifications y; Preconditions, postconditions, loop invariants, assert statements, and other applicable annotations

  **summary:** Existing informal language-based (e.g., human language) Large Language Models (LLMs) trained with Reinforcement Learning (RL) face a significant challenge: their verification processes, which provide crucial training signals, are neither reliable nor scalable. In fact, the prevalent large proprietary models could hardly generate verifiable programs. A promising yet largely uncharted alternative is formal language-based reasoning. Grounding LLMs in rigorous formal systems where generative models operate in formal language spaces (e.g., Dafny) enables the automatic and mathematically provable verification of their reasoning processes and outcomes. This capability is pivotal for achieving large-scale, reliable formal software verification. It is a common practice to employ human-annotated chain-of-thought and answers to induce the reasoning and coding capabilities of LLMs. Unfortunately, it becomes unacceptably all-consuming to provide such priors for supervising complex programming tasks. In this work, we systematically explore ways to reduce human annotations with the formal language, Dafny, as the main environment for our pilot study. Our pipeline mainly relies on introducing an automatic and scalable data curation pipeline, and careful RL designs integrated with feedback from the formal language verifier. We introduce DafnyComp, a benchmark of compositional formal programs with auto-formalized specifications for specification reasoning. Our supervised fine-tuning (SFT) stage enables even small models (e.g., 0.5B) to generate syntactically valid and verifiable Dafny code, surpassing proprietary models. RL with regularization further improves performance, achieving stronger generalization to out-of-domain tasks and outperforming all strong baselines on the challenging DafnyComp benchmark. Anonymized code and models are available at https://github. com/Veri-Code/ReForm and https://huggingface.co/Veri-Code.

  **work id:** 7924ff84-8834-4fdd-83f7-adc717fea9e4

  **approach:** Re:Form combines automated data curation, a compositional benchmark, limited CoT-free supervised fine-tuning, and verifier-guided reinforcement learning with syntax, verification, and subset rewards plus policy regularization.

  **citation:** Chuanhao Yan et al.. Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They treat the Dafny verifier as a free, always-usable reward signal and never account for solver/verifier CPU time, heavy-tailed per-obligation latency, or timeouts, so the question of whether proof supervision is actually cheaper than test supervision under equal end-to-end cost is not posed. The cost accounting C = H_gpu*p_gpu + H_cpu*p_cpu, timeout distributions, and price-ratio robustness that define our comparison are entirely absent from their framing.

  **method addresses:** false

  **method rationale:** Their verifier-guided GRPO pipeline is a method for training a specification generator, not an instrumented measurement study of oracle latency, timeouts, and GPU/CPU cost trade-offs, so it neither measures nor compares oracle capability-efficiency as our problem requires.

  **problem alignment:** different

  **alignment rationale:** Their problem is generating verifiable Dafny specifications with RL to minimize human annotation, whereas ours is measuring and comparing the cost-efficiency of different proof/test oracles as supervision signals in code-RL under equal-compute and equal-cost budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They treat the Dafny verifier as a free, always-usable reward signal and never account for solver/verifier CPU time, heavy-tailed per-obligation latency, or timeouts, so the question of whether proof supervision is actually cheaper than test supervision under equal end-to-end cost is not posed. The cost accounting C = H_gpu*p_gpu + H_cpu*p_cpu, timeout distributions, and price-ratio robustness that define our comparison are entirely absent from their framing.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem is generating verifiable Dafny specifications with RL to minimize human annotation, whereas ours is measuring and comparing the cost-efficiency of different proof/test oracles as supervision signals in code-RL under equal-compute and equal-cost budgets. | Their verifier-guided GRPO pipeline is a method for training a specification generator, not an instrumented measurement study of oracle latency, timeouts, and GPU/CPU cost trade-offs, so it neither measures nor compares oracle capability-efficiency as our problem requires.

  **is potential baseline:** false
-
  **input:** natural language specifications

  **output:** FPGA-ready RTL IP cores; timing and resource utilization reports

  **summary:** Large Language Models (LLMs) have demonstrated impressive capabilities in automated code generation but frequently produce code that fails formal verification, an essential requirement for hardware and safety-critical domains. To overcome this fundamental limitation, we previously proposed PREFACE, a model-agnostic framework based on reinforcement learning (RL) that iteratively repairs the prompts provided to frozen LLMs, systematically steering them toward generating formally verifiable Dafny code without costly fine-tuning. This work presents Proof2Silicon, a novel end-to-end synthesis framework that embeds the previously proposed PREFACE flow to enable the generation of correctness-by-construction hardware directly from natural language specifications. Proof2Silicon operates by: (1) leveraging PREFACE’s verifier-driven RL agent to optimize prompt generation iteratively, ensuring Dafny code correctness; (2) automatically translating verified Dafny programs into synthesizable high-level C using Dafny’s Python backend and PyLog; and (3) employing Vivado HLS to produce RTL implementations. Evaluated rigorously on a challenging 100- task benchmark, PREFACE’s RL-guided prompt optimization consistently improved Dafny verification success rates across diverse LLMs by up to 21%. Crucially, Proof2Silicon achieved an end-to-end hardware synthesis success rate of up to 72%, generating RTL designs through Vivado HLS synthesis flows. These results demonstrate a robust, scalable, and automated pipeline for LLM-driven, formally verified hardware synthesis, bridging natural-language specification and silicon realization.

  **work id:** c3da246c-6232-48a9-9d05-8aeb4e4bbb3e

  **approach:** Proof2Silicon couples PREFACE's verifier-guided RL prompt repair with Dafny verification, Python sanitization, PyLog HLS-C generation, and Vivado HLS synthesis.

  **citation:** (unknown authors). Proof2Silicon: Prompt Repair for Verified Code and Hardware Generation via Reinforcement Learning.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They treat the Dafny verifier purely as a correctness feedback signal and never measure its resource cost — per-obligation solver latency, heavy-tailed timeout distributions, and CPU/GPU price under fixed limits — so the question of whether proof/verification supervision is actually cheaper than test-outcome supervision at equal end-to-end cost is never posed.

  **method addresses:** false

  **method rationale:** Their pipeline optimizes prompts to maximize verification success and produce hardware; it neither instruments oracle call latency, timeouts, CPU/GPU cost, nor compares oracle types on capability-per-cost, which is the entire measurement object of our study.

  **problem alignment:** different

  **alignment rationale:** Their problem is generating verified FPGA/RTL hardware from natural-language specs via RL prompt repair, whereas ours is measuring and comparing the cost-efficiency of different proof/test oracles in code-RL training under equal-compute and equal-cost budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They treat the Dafny verifier purely as a correctness feedback signal and never measure its resource cost — per-obligation solver latency, heavy-tailed timeout distributions, and CPU/GPU price under fixed limits — so the question of whether proof/verification supervision is actually cheaper than test-outcome supervision at equal end-to-end cost is never posed.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem is generating verified FPGA/RTL hardware from natural-language specs via RL prompt repair, whereas ours is measuring and comparing the cost-efficiency of different proof/test oracles in code-RL training under equal-compute and equal-cost budgets. | Their pipeline optimizes prompts to maximize verification success and produce hardware; it neither instruments oracle call latency, timeouts, CPU/GPU cost, nor compares oracle types on capability-per-cost, which is the entire measurement object of our study.

  **is potential baseline:** false
-
  **input:** Written or natural-language software specifications; Formal task contexts containing specifications, partial implementations, helper lemmas, or proof holes; Repository context, imported definitions, and local lemmas for repository-grounded Lean tasks

  **output:** Completed Dafny or Lean programs and proofs accepted by the target verifier; Complete verified-coding artifacts with implementations, specifications, helper lemmas, and discharged proof obligations

  **summary:** Automated formal verification remains challenging for large language models because data for proof assistants and verification-aware languages is scarce, and correctness depends on satisfying precise machine-checkable specifications rather than producing plausible code. This thesis studies how verifier environments can improve LLM generation of verified programs and proofs through reinforcement learning from verifiable rewards (RLVR) and verifierguided inference-time search. First, we train open-source models in Dafny with RLVR using Group Relative Policy Optimization (GRPO) and related variants, assembling generated candidates into complete programs and scoring them with compiler and verifier outcomes. Initial experiments on an APPS-derived Dafny dataset increased verified reward from 2.2% to 58.1%, but revealed specification hacking, where models exploit weak formal specifications instead of implementing the intended solutions. After filtering underspecified and vulnerable tasks, multi-turn RLVR on the refined benchmark improves the verified pass rate from 9.7% to 31.1%. Second, we develop a verifier-guided inference scafold in Lean that treats proof generation as structured search over decomposed subgoals, verifier feedback, diagnostics, and repair. With a fixed base model, the full scafold with proof reviser improves pass rate on an initial VeriCoding pilot set from 46.2% under direct repair to 69.2%. On the larger VERINA dataset, whole-task decomposition plus proof reviser solves 7 of 42 previously unsolved tasks. We also introduce Dalek-Bench, a repository-scale Lean benchmark derived from the Rust curve25519-dalek verification project; preliminary results remain weak, indicating that stronger progress evaluation and task-specific tool-use policies are still needed. Overall, formal verifiers become useful to LLMs when they are treated not just as checkers, but as sources of reward, feedback, and search control. However, this only succeeds when the environment supplies clean data, robust specifications, and structured ways to act on verifier feedback. Benchmarks and code are available on request from maxt114@mit.edu

  **work id:** 59557623-fcef-4353-87dc-314355bb50b4

  **approach:** The thesis combines verifier-reward post-training for Dafny with a verifier-in-the-loop Lean scafold that manages complete artifacts and performs recursive, tool-assisted, progress-controlled proof search.

  **citation:** Max Tan. Automating Formal Verification with Reinforcement Learning and Recursive Inference.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether proof supervision is more cost-efficient than test/execution oracles once heavy-tailed solver latency, timeouts, and separated GPU/CPU accounting are measured; their study reports verifier-reward and verification-success outcomes but does not measure oracle-call cost, latency distributions, or price-ratio robustness, so the equal-compute vs. equal-end-to-end-cost distinction and its crossovers remain unexamined.

  **method addresses:** false

  **method rationale:** Their RLVR/RecursiveWorker system is an artifact-generation pipeline with no instrumentation of per-obligation solver latency, timeout distributions, GPU/CPU accounting, or price-parameterized cost comparison across oracle types, so it cannot produce our capability-efficiency phase diagrams.

  **problem alignment:** different

  **alignment rationale:** Their goal is to generate and repair verified Dafny/Lean artifacts using verifier feedback, whereas ours is to measure and compare the cost-efficiency of different oracle types (test, execution, proof) as RL supervision signals under equal-compute and equal-cost budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether proof supervision is more cost-efficient than test/execution oracles once heavy-tailed solver latency, timeouts, and separated GPU/CPU accounting are measured; their study reports verifier-reward and verification-success outcomes but does not measure oracle-call cost, latency distributions, or price-ratio robustness, so the equal-compute vs. equal-end-to-end-cost distinction and its crossovers remain unexamined.

    **limitation id:** lim-1

    **evidence for limitation:** Their goal is to generate and repair verified Dafny/Lean artifacts using verifier feedback, whereas ours is to measure and compare the cost-efficiency of different oracle types (test, execution, proof) as RL supervision signals under equal-compute and equal-cost budgets. | Their RLVR/RecursiveWorker system is an artifact-generation pipeline with no instrumentation of per-obligation solver latency, timeout distributions, GPU/CPU accounting, or price-parameterized cost comparison across oracle types, so it cannot produce our capability-efficiency phase diagrams.

  **is potential baseline:** false
-
  **input:** A C program with a single loop; The loop pre-condition; The loop condition and body; A post-loop assertion or post-condition

  **output:** A set of inductive loop invariants; A formally verified proof of the post-loop assertion

  **summary:** We propose a novel framework that provides constructive feedback to an LLM in the “guess-and-check” paradigm by formally verifying its own thinking process and detecting local reasoning errors. We apply this framework to the loop invariant synthesis problem. We prompt the model to produce a step-by-step natural language proof justifying its thinking process for the failed verification condition of its generated loop invariants. Then, we use an LLM to translate the reasoning steps into first-order logic implications, which can be checked automatically. An invalid implication pinpoints the exact logical flaw in the LLM’s thinking process, which we then use to construct targeted feedback for refinement. We have implemented our approach in a tool called LORIS and evaluated it on a main benchmark suite of 460 C programs and an additional benchmark suite of 50 C programs each of which involves non-linear properties. On the main benchmark suite, LORIS solved 445 of the programs, and achieved an overall success rate of 93.1%. LORIS also demonstrates robustness on the challenging non-linear benchmark suite.

  **work id:** 35d6f322-8e60-44a3-bd3e-f69bc410bd5a

  **approach:** LORIS iteratively generates candidate invariants, checks their verification conditions, obtains a structured proof for a failed condition, formalizes and checks local reasoning implications, and returns targeted errors to refine the invariants.

  **citation:** Tianchi Li et al.. Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** LORIS never poses the question of whether proof/verifier supervision is actually cheaper than test-based supervision under heavy-tailed solver latency and timeouts; it reports only token cost on successful runs, ignoring per-obligation solver CPU time, timeout distributions, and GPU-vs-CPU price tradeoffs that determine end-to-end training cost. Its structured-proof-plus-SMT feedback is exactly one candidate oracle in our study but is never evaluated as a cost-efficiency choice against test, execution, or binary-proof oracles across program families, specification quality, and candidate budgets.

  **method addresses:** false

  **method rationale:** LORIS is an invariant-synthesis pipeline (Synthesizer/Formalizer LLMs + Frama-C/SMT feedback) and contains no mechanism to instrument oracle latency, timeouts, GPU/CPU cost, or produce cost-normalized phase diagrams comparing oracles across program families and budgets.

  **problem alignment:** different

  **alignment rationale:** Their problem is synthesizing inductive loop invariants to verify single-loop C programs, whereas ours is measuring and comparing the cost-efficiency of proof-vs-test oracles for code reinforcement learning under equal-compute and equal-cost budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] LORIS never poses the question of whether proof/verifier supervision is actually cheaper than test-based supervision under heavy-tailed solver latency and timeouts; it reports only token cost on successful runs, ignoring per-obligation solver CPU time, timeout distributions, and GPU-vs-CPU price tradeoffs that determine end-to-end training cost. Its structured-proof-plus-SMT feedback is exactly one candidate oracle in our study but is never evaluated as a cost-efficiency choice against test, execution, or binary-proof oracles across program families, specification quality, and candidate budgets.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem is synthesizing inductive loop invariants to verify single-loop C programs, whereas ours is measuring and comparing the cost-efficiency of proof-vs-test oracles for code reinforcement learning under equal-compute and equal-cost budgets. | LORIS is an invariant-synthesis pipeline (Synthesizer/Formalizer LLMs + Frama-C/SMT feedback) and contains no mechanism to instrument oracle latency, timeouts, GPU/CPU cost, or produce cost-normalized phase diagrams comparing oracles across program families and budgets.

  **is potential baseline:** false
-
  **input:** A dataset D of reference Haskell programs; A base language model used for Alice and Bob; A reference Haskell program P selected for each self-play round

  **output:** A fine-tuned generator that produces challenging semantically equivalent or inequivalent Haskell program variants; A fine-tuned evaluator that judges whether two programs are semantically equivalent

  **summary:**

  We introduce a self-play framework for semantic equivalence in Haskell, utilizing formal verification to guide adversarial training between a generator and an evaluator. The framework leverages Liquid Haskell proofs for validating equivalence and execution-based counterexamples for inequivalence, organized via a difficulty-aware curriculum. To facilitate this, we release OpInstruct-HSx, a synthetic dataset of ≈28k validated Haskell programs. Empirical experiments show that our evaluator transfers effectively to downstream tasks, achieving up to 13.3pp accuracy gain on EquiBench and consistent gains on PySecDB. Ablation studies on the SEQ-SINQ regimes indicate that while inequivalence supervision provides data volume, equivalence proofs are uniquely responsible for the model's reasoning capabilities. The entire training pipeline and dataset are publicly released on GitHub and Hugging Face respectively.

  We propose a self-play framework for semantic equivalence, in which two specialized agents interact: Alice, a generator that produces variants of reference programs; and Bob, an evaluator trained to decide whether two programs are equivalent. The self-play loop alternates between program generation, verification through proofs or counterexamples, difficulty scoring, and fine-tuning of both agents. By framing the problem as a game between generator and evaluator, the system encourages progressively harder examples and deeper reasoning about semantics.

  **work id:** 5b1a6ba4-7bab-479c-bc6a-37c516ef45ca

  **approach:** Alice generates equivalent or inequivalent variants of reference Haskell programs, external verification accepts valid proofs or counterexamples, Bob judges equivalence and supplies difficulty scores, and difficulty-aware supervised fine-tuning updates the agents.

  **citation:** Antonio Valerio Miceli Barone & Poon Tsz Nok. Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether proof/verification supervision is cheaper than test/execution supervision once heavy-tailed solver latency, timeouts, and CPU vs GPU pricing are measured — they report verification yield qualitatively but do not measure per-obligation latency/timeout distributions or compare oracles under equal end-to-end cost budgets. The cost-efficiency ordering of oracles across program families, specification quality, and candidate budgets is entirely outside their framing.

  **method addresses:** false

  **method rationale:** Their self-play SFT pipeline uses formal verification as a supervision signal to build a dataset and train models, but it neither instruments oracle latency/timeout/CPU-GPU cost nor compares oracle types under fixed cost budgets, so it cannot produce the cost-efficiency phase diagrams our problem requires.

  **problem alignment:** different

  **alignment rationale:** Our problem measures the cost-efficiency of different proof/test oracles for code-RL under equal-compute and equal-cost budgets, whereas their problem trains a generator/evaluator via formally-verified semantic-equivalence self-play to improve equivalence judgment and code reasoning.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether proof/verification supervision is cheaper than test/execution supervision once heavy-tailed solver latency, timeouts, and CPU vs GPU pricing are measured — they report verification yield qualitatively but do not measure per-obligation latency/timeout distributions or compare oracles under equal end-to-end cost budgets. The cost-efficiency ordering of oracles across program families, specification quality, and candidate budgets is entirely outside their framing.

    **limitation id:** lim-1

    **evidence for limitation:** Our problem measures the cost-efficiency of different proof/test oracles for code-RL under equal-compute and equal-cost budgets, whereas their problem trains a generator/evaluator via formally-verified semantic-equivalence self-play to improve equivalence judgment and code reasoning. | Their self-play SFT pipeline uses formal verification as a supervision signal to build a dataset and train models, but it neither instruments oracle latency/timeout/CPU-GPU cost nor compares oracle types under fixed cost budgets, so it cannot produce the cost-efficiency phase diagrams our problem requires.

  **is potential baseline:** false
-
  **input:** A pretrained code LLM; Executable programs paired with concrete inputs; Code-generation problems paired with unit tests

  **output:** A post-trained code LLM with improved execution reasoning; Predictions of intermediate control flow, variable values and types, and final program outputs; Generated programs that pass functional unit tests

  **summary:** Code LLMs still struggle with code execution reasoning, especially in smaller models. Existing methods rely on supervised fine-tuning (SFT) with teacher-generated explanations, pri marily in two forms: (1) input–output (I/O) prediction chains and (2) natural-language descriptions of execution traces. However, intermediate execution steps cannot be explicitly verified during SFT, so the training objective can be reduced to merely matching teacher explanations. Moreover, training data is typically collected without explicit control over task difficulty. We introduce ExecVerify, which goes beyond text imitation by incorporating verifi able white-box rewards derived from execution traces, including next-statement prediction and variable value/type prediction. Our work first builds a dataset with multiple difficulty levels via constraint-based program synthesis. Then, we apply reinforcement learning (RL) to re ward correct answers about both intermediate execution steps and final outputs, aligning the training objective with semantic correctness at each execution step. Finally, we adopt a twostage training pipeline that first enhances execution reasoning and then transfers to code generation. Experiments demonstrate that a 7B model trained with ExecVerify achieves performance comparable to 32B models on code reasoning benchmarks and improves pass@1 by up to 5.9% on code generation tasks over strong post-training baselines<sup>1</sup>.

  **work id:** abe98e8d-0824-44d3-8d37-5177184787a3

  **approach:** ExecVerify combines constraint-based curriculum data synthesis with a two-stage post-training pipeline using interpreter-derived white-box rewards for execution reasoning and unit-test rewards for code generation.

  **citation:** Lingxiao Tang et al.. ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether richer (proof/execution-trace) supervision is cheaper than test-outcome supervision once heavy-tailed solver/verifier latency, timeouts, and CPU time are measured; their evaluation reports only capability (pass@1) and assumes reward computation is free, so the cost-efficiency ordering of oracles under equal model-compute versus equal end-to-end cost—and its robustness to a threefold GPU-to-CPU price shift—is entirely absent.

  **method addresses:** false

  **method rationale:** ExecVerify proposes one particular white-box reward scheme to improve a model, but offers no instrumentation of oracle latency, timeouts, solver CPU time, or price-ratio-sensitive cost accounting, so it cannot produce the equal-compute/equal-cost phase diagrams or crossover analysis our problem requires.

  **problem alignment:** different

  **alignment rationale:** Their goal is to post-train a code LLM to reason about execution and generate correct code using verifiable stepwise rewards, whereas our goal is to measure and compare the cost-efficiency of different proof/test oracles used as RL supervision under equal-compute and equal-cost budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether richer (proof/execution-trace) supervision is cheaper than test-outcome supervision once heavy-tailed solver/verifier latency, timeouts, and CPU time are measured; their evaluation reports only capability (pass@1) and assumes reward computation is free, so the cost-efficiency ordering of oracles under equal model-compute versus equal end-to-end cost—and its robustness to a threefold GPU-to-CPU price shift—is entirely absent.

    **limitation id:** lim-1

    **evidence for limitation:** Their goal is to post-train a code LLM to reason about execution and generate correct code using verifiable stepwise rewards, whereas our goal is to measure and compare the cost-efficiency of different proof/test oracles used as RL supervision under equal-compute and equal-cost budgets. | ExecVerify proposes one particular white-box reward scheme to improve a model, but offers no instrumentation of oracle latency, timeouts, solver CPU time, or price-ratio-sensitive cost accounting, so it cannot produce the equal-compute/equal-cost phase diagrams or crossover analysis our problem requires.

  **is potential baseline:** false
-
  **input:** C code to be verified; corresponding SIMPL and/or Isabelle content supplied as optional supplements; program specifications such as assertions, safety requirements, or overflow requirements

  **output:** a code-verification result of success or failure; intermediate proof states; prover messages and error information

  **summary:** Formal verification (FV) has witnessed growing significance with current emerging program synthesis by the evolving large language models (LLMs). However, current formal verification mainly resorts to symbolic verifiers or hand-craft rules, resulting in limitations for extensive and flexible verification. On the other hand, formal languages for automated theorem proving, such as Isabelle, as another line of rigorous verification, are maintained with comprehensive rules and theorems. In this paper, we propose FVEL³, an interactive Formal Verification Environment with LLMs. Specifically, FVEL transforms a given code to be verified into Isabelle, and then conducts verification via neural automated theorem proving with an LLM. The joined paradigm leverages the rigorous yet abundant formulated and organized rules in Isabelle and is also convenient for introducing and adjusting cutting-edge LLMs. To achieve this goal, we extract a large-scale FVELER³. The FVELER dataset includes code dependencies and verification processes that are formulated in Isabelle, containing 758 theories, 29,125 lemmas, and 200,646 proof steps in total with in-depth dependencies. We benchmark FVELER in the FVEL environment by first fine-tuning LLMs with FVELER and then evaluating them on Code2Inv and SV-COMP. The results show that FVEL with FVELER fine-tuned Llama3- 8B solves 17.39% (69→81) more problems, and Mistral-7B 12% (75→84) more problems in SV-COMP. And the proportion of proof errors is reduced. Project page: https://fveler.github.io/.

  **work id:** f516832f-73b0-4403-8622-3aba1897b2d8

  **approach:** FVEL transforms C code into Isabelle facts, asks an LLM to formulate a lemma and generate proof steps, and uses an Isabelle prover through PISA to return feedback and validate the completed proof. FVELER supplies theory dependencies and step-wise proof data for fine-tuning and evaluation.

  **citation:** Xiaohan Lin et al.. FVEL: Interactive Formal Verification Environment with Large Language Models via Theorem Proving.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** FVEL never poses the question of whether proof-style supervision is actually cheaper to run, so it does not measure per-obligation solver latency, heavy-tailed timeout distributions, or end-to-end GPU+CPU cost under fixed resource limits — exactly the cost-vs-oracle-count tradeoff our study quantifies. It treats proving as a capability endpoint rather than as one priced oracle among test-outcome, execution, and hybrid oracles compared under equal-compute and equal-cost budgets.

  **method addresses:** false

  **method rationale:** FVEL is a verification pipeline and dataset; it provides no instrumentation of oracle latency, timeouts, GPU/CPU cost accounting, or equal-compute/equal-cost phase diagrams that our efficiency comparison requires.

  **problem alignment:** different

  **alignment rationale:** Their problem is producing a success/failure code-verification result via LLM-driven Isabelle theorem proving, whereas ours is measuring the compute- and cost-efficiency of different oracle types used to supervise code-RL training.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] FVEL never poses the question of whether proof-style supervision is actually cheaper to run, so it does not measure per-obligation solver latency, heavy-tailed timeout distributions, or end-to-end GPU+CPU cost under fixed resource limits — exactly the cost-vs-oracle-count tradeoff our study quantifies. It treats proving as a capability endpoint rather than as one priced oracle among test-outcome, execution, and hybrid oracles compared under equal-compute and equal-cost budgets.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem is producing a success/failure code-verification result via LLM-driven Isabelle theorem proving, whereas ours is measuring the compute- and cost-efficiency of different oracle types used to supervise code-RL training. | FVEL is a verification pipeline and dataset; it provides no instrumentation of oracle latency, timeouts, GPU/CPU cost accounting, or equal-compute/equal-cost phase diagrams that our efficiency comparison requires.

  **is potential baseline:** false

## Sub-Problems

**summary:** Completing the study requires a controlled multi-oracle benchmark, complete GPU/CPU and latency instrumentation, and regime-specific phase-diagram analysis under both budget definitions. All three remain unsolved because prior work treats oracle cost comparison as out of scope and provides neither the required measurements nor crossover analysis.

**sub problems:**

-
  **description:** Build a controlled multi-oracle benchmark spanning every required program family, specification source and quality, and candidate-generation budget under identical sampling and resource limits.

  **sub problem id:** sp-1

  **technical challenge:** The harness must normalize heterogeneous test, execution, proof, and hybrid calls while preventing verifier effort or sampling conditions from varying between arms.

  **why it is a problem:** Without matched coverage and observed held-out capability, oracle differences cannot be attributed to supervision choice or generalized across regimes.

  **source limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8
-
  **description:** Measure every oracle call and compute end-to-end cost from observed GPU and CPU hours while retaining complete latency and timeout distributions.

  **sub problem id:** sp-2

  **technical challenge:** Accurate attribution requires per-obligation instrumentation, censored-timeout handling, fixed limits, and price-variable accounting without collapsing tails into means.

  **why it is a problem:** This determines whether reduced rollout counts translate into real savings and whether heavy-tailed solver costs reverse oracle rankings.

  **source limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8
-
  **description:** Construct equal-model-compute and equal-end-to-end-cost phase diagrams, locating winner changes and crossovers across regimes and price ratios.

  **sub problem id:** sp-3

  **technical challenge:** Crossovers must be estimated from noisy capability and heavy-tailed cost observations across a high-dimensional grid and remain interpretable under a threefold GPU-to-CPU price shift.

  **why it is a problem:** The objective requires exposing when global rankings conceal regime-specific winners or disagree between budget definitions.

  **source limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8

**internal reasoning:**

**required components:**

-
  **name:** Controlled multi-oracle benchmark

  **note:** Prior studies do not compare all five oracles under matched protocols, fixed verifier limits, and the required program, specification, and candidate-budget axes.

  **status:** unsolved

  **covered by limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8
-
  **name:** Complete resource-cost measurement

  **note:** Every prior study omits decisive parts of call-level GPU/CPU accounting, per-obligation latency, timeout distributions, or price-parameterized end-to-end cost.

  **status:** unsolved

  **covered by limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8
-
  **name:** Budget-sensitive phase diagrams

  **note:** No prior work identifies oracle winners and crossovers under equal model compute versus equal end-to-end cost or tests their robustness to price-ratio changes.

  **status:** unsolved

  **covered by limitation ids:**

  - lim-1
  - lim-2
  - lim-3
  - lim-4
  - lim-5
  - lim-6
  - lim-7
  - lim-8

## Method Design

**methods:**

-
  **method id:** m-1

  **hypotheses:**

  - Within every equal-model-compute block, candidate count, generated tokens, and GPU hours will differ by ≤1% across oracle arms, with zero configuration or resource-cap deviations in audit logs.
  - The preregistered quality tiers will have Spearman correlation ≥0.8 with held-out specification-defect detection scores and exceed source-only quality labels by ≥0.2.

  **key insight:** Blocking all non-oracle factors and deriving heterogeneous rewards from frozen task packets makes reward information and its intrinsic evaluation cost the only systematic differences between arms.

  **proposed approach:** Construct preregistered blocks over program family, specification source, quality tier, and candidate budget; define quality before training using controlled specification defects calibrated against held-out semantic mutants and blind expert ratings. Run oracle arms from matched checkpoints with identical candidate counts, decoding limits, update schedules, and seeds under a shared Oracle Evaluation Contract whose adapters produce test, execution-trace, binary-proof, structured-proof, or hybrid rewards using frozen artifacts and fixed solver configurations and resource caps.

  **target sub problem id:** sp-1
-
  **method id:** m-2

  **hypotheses:**

  - Ledger-attributed GPU and CPU hours will each reconcile within 1% of independent device and process-tree meters, while naive job-wall-time accounting will show >5% absolute error for at least one oracle.
  - For at least one proof-based regime, completed-call p99 latency will be ≥10× its median or timeout mass will be ≥5%, and a mean-latency baseline will underpredict empirical p95 training-step stall by ≥25%.

  **key insight:** Per-obligation event sourcing separates consumed resources from wall-clock stalls and preserves the censoring information that aggregate job totals and mean latency discard.

  **proposed approach:** Route every Oracle Evaluation Contract call through an append-only ledger recording process-tree CPU time, reserved GPU time, wall latency, obligation identity, retries, caching, parallelism, termination cause, and timeout cap. Compute C directly from summed observed hours with symbolic prices, and publish stratified empirical distributions, Kaplan–Meier curves only over the identifiable pre-cap region, explicit timeout mass, and tail bounds without imputing post-timeout completion times.

  **target sub problem id:** sp-2
-
  **method id:** m-3

  **hypotheses:**

  - At least 10% of factorial cells will have different equal-GPU and equal-cost winners, with bootstrap P(best) ≥0.8 and a held-out capability advantage of ≥2 percentage points over the runner-up under each respective budget.
  - At least 75% of cells having P(best) ≥0.8 at r0 will retain the same equal-cost winner at both r0/3 and 3r0 with P(best) ≥0.8.

  **key insight:** Attainable envelopes are legitimately monotone because a larger budget can reuse any cheaper checkpoint, enabling interpretable crossover estimation without assuming monotone learning dynamics.

  **proposed approach:** Within each family-by-specification-source-by-quality-by-candidate-budget cell, use Oracle Evaluation Contract ledger records to build cross-fitted attainable-capability envelopes: select checkpoints on validation data, evaluate on held-out tasks, cluster-bootstrap tasks and training seeds, and retain the best checkpoint satisfying either H_gpu ≤ B or C(r) ≤ B. Evaluate r at r0/3, r0, and 3r0 plus a log-spaced interpolation grid, declare winners only when bootstrap P(best) ≥0.8, mark other cells ambiguous, and report crossover distributions from envelope intersections.

  **target sub problem id:** sp-3

**summary:** Use a preregistered factorial benchmark and a shared Oracle Evaluation Contract to isolate reward-oracle effects while fixing generation and verification conditions. An event-sourced resource ledger preserves per-obligation costs, latency censoring, and timeouts. Cluster-bootstrap capability envelopes then produce equal-GPU and equal-cost phase diagrams with uncertainty-aware crossovers and price-ratio sensitivity.

## Experiment Design

**summary:** The evaluation validates resource control, specification-quality measurement, cost attribution, tail-latency measurement, budget-dependent oracle ordering, and price-ratio robustness. It produces phase diagrams and crossover estimates from paired held-out trials while treating source labels, wall-time accounting, and mean latency only as measurement sanity checks.

**datasets:**

-
  **name:** Controlled Multi-Oracle Factorial Benchmark

  **justification:** Crosses every preregistered program family, specification source and quality tier, and generation budget on shared task seeds, stressing resource equivalence and budget-dependent ordering.
-
  **name:** Blinded Specification-Defect Validation Set

  **justification:** Uses held-out defect challenges unavailable during tier assignment, allowing a non-circular test of quality tiers against independently observed defect detectability.
-
  **name:** Metered Oracle Execution and Stall Traces

  **justification:** Retains per-call GPU and CPU attribution, concurrency, complete latencies, timeouts, and training-step stalls, including proof-heavy regimes where accounting and tail summaries can fail.

**baselines:**

-
  **name:** Source-Only Quality Labels

  **justification:** Checks whether quality tiers contain information beyond specification provenance rather than serving as an effectiveness baseline.
-
  **name:** Naive Job-Wall-Time Accounting

  **justification:** Exposes attribution errors caused by idle time, concurrency, and overlapping GPU and CPU work.
-
  **name:** Mean-Latency Stall Model

  **justification:** Tests whether a scalar latency summary loses operationally important tail and timeout behavior.

**research questions:**

-
  **tier:** mechanism

  **rq id:** rq-1

  **setup:** For every program-family × specification-quality × generation-budget block, run every oracle arm for N=100 independent seeds while holding models, prompts, sampling parameters, hardware, and caps fixed. Compare arm totals using simultaneous equivalence intervals and audit every launch and resource-limit event; 100 seeds provide sensitivity to persistent 1% imbalances.

  **metrics:** Relative range and pairwise differences in candidate count, generated tokens, and metered GPU hours; configuration-deviation and cap-deviation counts.

  **description:** Does the benchmark maintain equivalent candidate-generation compute across oracle arms without configuration or resource-cap violations?

  **expected outcome:** Every simultaneous arm-difference interval lies within ±1%, and all configuration- and resource-cap deviation counts equal zero.

  **statistical test:** Pairwise TOST equivalence tests with a ±1% margin and Holm familywise correction at α=0.05; exact zero-event audit check.

  **target hypotheses:** - Within every equal-model-compute block, candidate count, generated tokens, and GPU hours will differ by ≤1% across oracle arms, with zero configuration or resource-cap deviations in audit logs.

  **sample size rationale:** N=100 seeds per block and arm supports narrow equivalence intervals while covering seed-dependent scheduling and generation variation.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-2

  **setup:** Evaluate N=max(300, 60 per program family) specifications balanced across source and tier. Assign tiers before exposing a disjoint, blinded defect challenge set, then compare tier ranks and source-only labels with held-out defect-detection scores using family-stratified bootstrap inference; this sample provides coverage across source-tier combinations.

  **metrics:** Spearman correlation with held-out defect-detection score, correlation difference versus source-only labels, and bootstrap confidence intervals.

  **description:** Do preregistered specification-quality tiers measure independently observed defect detectability rather than merely encoding specification source?

  **expected outcome:** The lower 95% confidence bound for tier-score correlation is at least 0.8, and the lower bound for its improvement over source-only labels is at least 0.2.

  **statistical test:** One-sided, family-stratified bootstrap tests for Spearman ρ≥0.8 and Δρ≥0.2 at α=0.05.

  **target hypotheses:** - The preregistered quality tiers will have Spearman correlation ≥0.8 with held-out specification-defect detection scores and exceed source-only quality labels by ≥0.2.

  **sample size rationale:** At least N=300 supplies stable rank-correlation estimates and at least 60 independently scored specifications per family.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-3

  **setup:** Collect N=1000 instrumented jobs per oracle, balanced across benchmark strata and low, medium, and high concurrency. Reconcile ledger totals against independent device telemetry and OS process-tree meters, then repeat the calculation using job wall time; 1000 jobs expose short-call, idle, overlap, and concurrency attribution failures.

  **metrics:** Absolute and relative GPU-hour and CPU-hour reconciliation errors by oracle, concurrency level, and accounting method.

  **description:** Does per-call ledger accounting accurately attribute GPU and CPU consumption under heterogeneous oracle workloads?

  **expected outcome:** GPU- and CPU-hour reconciliation intervals fall wholly within ±1%, while at least one oracle has a lower 95% bound above 5% absolute error under wall-time accounting.

  **statistical test:** Clustered TOST equivalence tests with a ±1% margin for ledger errors, plus a one-sided bootstrap test for naive absolute error >5%, at α=0.05 with Holm correction.

  **target hypotheses:** - Ledger-attributed GPU and CPU hours will each reconcile within 1% of independent device and process-tree meters, while naive job-wall-time accounting will show >5% absolute error for at least one oracle.

  **sample size rationale:** N=1000 jobs per oracle provides coverage of heterogeneous runtimes and enough blocks for precise clustered error intervals.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-4

  **setup:** Record N=10000 calls and N=5000 integrated training steps per proof-based regime under fixed timeout and resource caps. Preserve completed latencies and timeout indicators, fit the mean-latency baseline on half the traces, and evaluate stall prediction on the held-out half; these sizes yield about 100 p99-tail calls and 250 p95-tail steps per regime.

  **metrics:** Full empirical latency CDF, completed-call median and p99, timeout probability, empirical p95 step stall, and relative mean-baseline underprediction.

  **description:** Do complete latency and timeout distributions reveal proof-oracle stalls that mean-latency accounting misses?

  **expected outcome:** At least one proof regime has a p99/median ratio of at least 10 or timeout mass of at least 5%, and its mean-based p95 stall prediction is at least 25% below the empirical p95.

  **statistical test:** One-sided stratified bootstrap tests for the p99-to-median ratio and stall underprediction, plus an exact binomial timeout test, at α=0.05 with multiplicity correction.

  **target hypotheses:** - For at least one proof-based regime, completed-call p99 latency will be ≥10× its median or timeout mass will be ≥5%, and a mean-latency baseline will underpredict empirical p95 training-step stall by ≥25%.

  **sample size rationale:** N=10000 calls supports p99 estimation, while N=5000 steps supports held-out p95 stall estimation without discarding timeout mass.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-5

  **setup:** Evaluate all preregistered program-family × quality × budget cells, using at least N=120 cells and 20000 paired held-out task-seed outcomes per cell and oracle. Construct equal-GPU and equal-cost frontiers using C = H_gpu*p_gpu + H_cpu*p_cpu at r0, estimate P(best) by paired bootstrap, and bisect adjacent budget intervals where winners change.

  **metrics:** Capability at matched budgets, P(best), winner-runner-up difference, disagreement fraction, and budget and cost coordinates of crossover points.

  **description:** How often do equal-model-compute and equal-end-to-end-cost constraints select different oracles, and where do winner crossovers occur?

  **expected outcome:** At least 10% of cells have different qualifying winners under the two budgets, with each winner having P(best)≥0.8 and a held-out advantage of at least two percentage points.

  **statistical test:** Paired hierarchical bootstrap for P(best), runner-up advantage, disagreement proportion, and crossover intervals at α=0.05.

  **target hypotheses:** - At least 10% of factorial cells will have different equal-GPU and equal-cost winners, with bootstrap P(best) ≥0.8 and a held-out capability advantage of ≥2 percentage points over the runner-up under each respective budget.

  **sample size rationale:** At least 120 cells resolves a 10% disagreement rate into at least 12 cells; 20000 paired outcomes per cell gives at least 80% power for a two-percentage-point Bernoulli difference under worst-case paired variance.

  **target sub problem id:** sp-3
-
  **tier:** mechanism

  **rq id:** rq-6

  **setup:** Using the same N≥120 factorial cells and 20000 paired held-out outcomes per cell, reprice every observed resource-performance point at r0/3, r0, and 3r0 and reconstruct each equal-cost frontier. Assess retention only among cells with P(best)≥0.8 at r0; require at least 80 eligible cells or report the robustness estimate as underpowered.

  **metrics:** Winner and P(best) at each price ratio, joint retention indicator, retention fraction, and price-ratio crossover locations.

  **description:** Is the equal-cost oracle ordering robust to a threefold change in the GPU-to-CPU price ratio?

  **expected outcome:** At least 75% of eligible cells retain the same winner at both altered ratios, with P(best)≥0.8 at each ratio.

  **statistical test:** Hierarchical paired bootstrap for winner probabilities and a one-sided 95% lower confidence bound on the retention fraction at α=0.05.

  **target hypotheses:** - At least 75% of cells having P(best) ≥0.8 at r0 will retain the same equal-cost winner at both r0/3 and 3r0 with P(best) ≥0.8.

  **sample size rationale:** N≥120 supplies broad factorial coverage; 80 eligible cells bound the standard error of a 75% retention proportion to approximately five percentage points before bootstrap uncertainty.

  **target sub problem id:** sp-3
