> **⚠️ SUPERSEDED SOURCE ARTIFACT — DO NOT CITE AS CURRENT.**
> This is the unedited AutoDiscussion research report, kept for provenance. It still contains
> the `assume false;` completion stub, evenly-spaced 32-token snapshots, and the multi-turn framing, all of which were corrected during review.
> **Current design: `paper-draft.revised.md` and `experiment-spec.md`.** See `../MAJORS.md`.

# ZW1 Typed Obligation Verdicts as Reward: Structured Verification-Condition versus Dense Execution-State Supervision for Code Models

> verification-condition level reward design for code language model post-training

_Research report — 6 confirmed steps._

## Problem Definition

**input:** Given a common base checkpoint, single-function Dafny training instances, candidate programs sampled by each arm, a fixed verifier, and a fixed hidden-test harness, observe for every candidate both execution outcomes and typed obligations from {initialization, preservation, exit/postcondition, safety, termination}, each labeled proved, refuted-with-countermodel, unknown, timeout, or invalid.

**output:** Produce matched estimates for typed-verdict reward versus dense execution-state reward, binary verifier reward, and the RLFR-style verified-goals ratio on the primary tool-off hidden-test correctness outcome, and report robustness, specification hacking, verifier-behavior divergence, and sensitivity to fixed scalarizations.

**summary:** It is unknown whether reinforcement learning from typed program-verification obligations and distinct solver verdicts yields better tool-free coding behavior than either an undifferentiated proof-completion ratio or equally dense execution-state supervision. The unresolved issue is causal because prior work has not compared these signals under matched checkpoints, data, sampled-token budgets, and optimization.

**objective:** Measure whether the typed-verdict arm improves tool-off hidden-test correctness over dense execution supervision as the primary contrast and over the scalar obligation ratio as the mandatory ablation; also measure robustness, specification hacking, verifier-behavior divergence, and sensitivity to fixed scalarizations.

**study type:** empirical

**constraints:** All arms must share the base checkpoint, instances, sampled-token budget, optimizer, fixed verifier, and fixed test harness; every candidate must be scored by both oracles before arm-specific rewards are computed. Tool-off evaluation may use neither verifier nor countermodel feedback. Timeout must remain distinct from refutation, weights must be preregistered, raw obligation vectors must be reported, and identical-candidate matching may be claimed only at seeding because on-policy arms subsequently diverge.

**formal summary:** Given matched Dafny training instances, checkpoints, budgets, arm-sampled candidate programs, fixed tests, and typed verifier verdicts, produce comparative effect estimates for tool-off hidden-test correctness and secondary outcomes, subject to paired-oracle scoring, preregistered rewards, and distinct timeout semantics.

## Research Significance

**summary:** Shaped per-obligation Dafny rewards and prover-off Dafny-to-Python transfer are already reported by RLFR, while GraphAlignCoder already reports named obligation roles and prover-removed evaluation. What remains unknown is whether verifier-grounded obligation typing and verdict distinctions add information beyond RLFR's scalar ratio and whether they outperform the now-established alternative of dense execution-state supervision at matched compute.

**evidence:** RLFR uses shaped per-proof-obligation GRPO and reports "some level of generalization past the formal verification domain," but runs no execution-supervision baseline, types no obligations, collapses solver verdicts, and is non-archival industry work of low evidential weight. GraphAlignCoder obtains prover-off gains from teacher-invented obligation text through cross-entropy, with consolidation alone scoring 49/175 versus 50/175 for the full method. Lean process-verified RL supplies structured tactic feedback but no code arm. ExecVerify, StepCodeReasoner, and DHRCL show dense execution supervision is a serious converged comparator.

**who cares:** Researchers building code-generation RL systems, program-verification and formal-methods researchers, benchmark designers, and teams deciding whether to invest compute in verifier-based or execution-based supervision need this evidence. Reviewers and users of tool-free coding models also need to know whether reported formal gains survive hidden tests, perturbations, translation, repair, and unseen program structures.

**why it matters:** Without the head-to-head comparison and scalar-collapse ablation, gains could be wrongly attributed to typed proof structure when they come from generic reward density, an acceptance bit, or the proportion of goals discharged. That error could direct substantial training compute toward a more complex signal that loses to execution supervision, encourages specification hacking, or improves verifier acceptance without behavioral correctness.

## Related Work

**summary:** Deeply compared the 8 most decisive PDF-grounded papers against our problem definition (8 candidate baselines, 0 high threats to our motivation). A further 21 cited work(s) are listed for coverage without a deep comparison (no fetchable full text, or less central than the top 8).

**general related works:**

-
  **summary:** Cited by the source draft. No openly fetchable full text, so this work is listed for coverage only and was not deeply compared against our problem.

  **work id:** 9fc4f2d8-d539-4100-813f-ef00c03a622d

  **citation:** Hubert et al. Olympiad-level formal mathematical reasoning with reinforcement learning (AlphaProof). Nature 651(8106):607-613, 2026. DOI 10.1038/s41586-025-09833-y. No arXiv version exists.
-
  **summary:** Large Language Models (LLMs) have demonstrated impressive capabilities in automated code generation but frequently produce code that fails formal verification, an essential requirement for hardware and safety-critical domains. To overcome this fundamental limitation, we previously proposed PREFACE, a model-agnostic framework based on reinforcement learning (RL) that iteratively repairs the prompts provided to frozen LLMs, systematically steering them toward generating formally verifiable Dafny code without costly fine-tuning. This work presents Proof2Silicon, a novel end-to-end synthesis framework that embeds the previously proposed PREFACE flow to enable the generation of correctness-by-con

  **work id:** ac55bc40-38d4-4f18-9aee-b14f5f7b5f34

  **citation:** (unknown authors). Proof2Silicon: Prompt Repair for Verified Code and Hardware Generation via Reinforcement Learning.
-
  **summary:** We propose a novel framework that provides constructive feedback to an LLM in the “guess-and-check” paradigm by formally verifying its own thinking process and detecting local reasoning errors. We apply this framework to the loop invariant synthesis problem. We prompt the model to produce a step-by-step natural language proof justifying its thinking process for the failed verification condition of its generated loop invariants. Then, we use an LLM to translate the reasoning steps into first-order logic implications, which can be checked automatically. An invalid implication pinpoints the exact logical flaw in the LLM’s thinking process, which we then use to construct targeted feedback for re

  **work id:** 6998fac4-355d-4008-8375-5e10e283a777

  **citation:** Tianchi Li et al.. Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors.
-
  **summary:** Automated code generation with large language models has gained significant traction, but there remains no guarantee on the correctness of generated code. We aim to use formal verification to provide mathematical guarantees that the generated code is correct. However, generating formally verified code with LLMs is hindered by the scarcity of training data and the complexity of formal proofs. To tackle this challenge, we introduce AlphaVerus, a self-improving framework that bootstraps formally verified code generation by iteratively translating programs from a higher-resource language and leveraging feedback from a verifier. AlphaVerus operates in three phases: exploration of candidate transl

  **work id:** b739baec-682d-4b83-8b95-c9de4c9457fb

  **citation:** Pranjal Aggarwal et al.. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement.
-
  **summary:** We introduce a self-play framework for semantic equivalence in Haskell, utilizing formal verification to guide adversarial training between a generator and an evaluator. The framework leverages Liquid Haskell proofs for validating equivalence and execution-based counterexamples for inequivalence, organized via a difficulty-aware curriculum. To facilitate this, we release OpInstruct-HSx, a synthetic dataset of ≈28k validated Haskell programs. Empirical experiments show that our evaluator transfers effectively to downstream tasks, achieving up to 13.3pp accuracy gain on EquiBench and consistent gains on PySecDB. Ablation studies on the SEQ-SINQ regimes indicate that while inequivalence supervi

  **work id:** 2f99ed7e-9e70-407c-8bba-6350149a7af1

  **citation:** Antonio Valerio Miceli Barone & Poon Tsz Nok. Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification.
-
  **summary:** Formal verification (FV) has witnessed growing significance with current emerging program synthesis by the evolving large language models (LLMs). However, current formal verification mainly resorts to symbolic verifiers or hand-craft rules, resulting in limitations for extensive and flexible verification. On the other hand, formal languages for automated theorem proving, such as Isabelle, as another line of rigorous verification, are maintained with comprehensive rules and theorems. In this paper, we propose FVEL³, an interactive Formal Verification Environment with LLMs. Specifically, FVEL transforms a given code to be verified into Isabelle, and then conducts verification via neural automa

  **work id:** bdfbc1f7-f918-40f2-ba53-14ac71ca98a6

  **citation:** Xiaohan Lin et al.. FVEL: Interactive Formal Verification Environment with Large Language Models via Theorem Proving.
-
  **summary:** Large language models (LLMs) deployed as agents solve user-specified tasks over multiple steps while keeping the required manual engagement to a minimum. Crucially, such LLMs need to ground their generations in any feedback obtained to reliably achieve the desired outcomes. We propose an end-to-end reinforcement learning method for teaching models to leverage execution feedback in the realm of code synthesis, where state-of-the-art LLMs struggle to improve code iteratively compared to independent sampling. We benchmark on competitive programming tasks, where we achieve new state-of-the-art results with both small (8B parameters) and large (70B) models while reducing the amount of samples req

  **work id:** b3f5d46b-224b-4e95-81d4-a91434188dfc

  **citation:** Jonas Gehring et al.. RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING.
-
  **summary:** We address the problem of code generation from multi-turn execution feedback. Existing methods either generate code without feedback or use complex, hierarchical reinforcement learning to optimize multi-turn rewards. We propose a simple yet scalable approach, µCODE, that solves multi-turn code generation using only single-step rewards. Our key insight is that code generation is a one-step recoverable MDP, where the correct code can be recovered from any intermediate code state in a single turn. µCODE iteratively trains both a generator to provide code solutions conditioned on multi-turn execution feedback and a verifier to score the newly generated code. Experimental evaluations show that ou

  **work id:** 6cbcb47a-e2af-4bff-a055-320a72777a2f

  **citation:** Arnav Kumar Jain et al.. Multi-Turn Code Generation Through Single-Step Rewards.
-
  **summary:** Large Language Models excel at code generation yet struggle with complex programming tasks that demand sophisticated reasoning. To bridge this gap, traditional process supervision relies on learned reward models requiring costly training data and suffering from reward misalignment, while outcome supervision fails for complex tasks needing coordinated intermediate steps. We introduce Outcome Refining Process Supervision, which unifies process and outcome supervision by leveraging executable verification: a treestructured search framework generates strategic alternatives, profiles execution metrics, and scores candidates via self-critique mechanisms that integrate runtime feedback with reasoni

  **work id:** 58377fdb-3d94-48c1-b0e5-e88bd1c9bf5b

  **citation:** Zhuohao Yu et al.. Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation.
-
  **summary:** The demonstrated code-understanding capability of LLMs raises the question of whether they can be used for automated program verification, a task that demands high-level abstract reasoning about program properties that is challenging for verification tools. We propose a general methodology to combine the power of LLMs and automated reasoners for automated program verification. We formally describe this methodology as a set of transition rules and prove its soundness. We instantiate the calculus as a sound automated verification procedure and demonstrate practical improvements on a set of synthetic and competition benchmarks.

  **work id:** fb5b1ffa-8a75-4bc6-80ee-126a0ac69c2d

  **citation:** Haoze Wu et al.. LEMUR: INTEGRATING LARGE LANGUAGE MODELSIN AUTOMATED PROGRAM VERIFICATION.
-
  **summary:** The use of large language models for code generation is a rapidly growing trend in software development. However, without efective methods for ensuring the correctness of generated code, this trend could lead to undesirable outcomes. In this paper, we introduce a new approach for addressing this challenge: the Clover paradigm, short for Closed-Loop Verifiable Code Generation, which uses consistency checking to provide a strong filter for incorrect code. Clover performs consistency checks among code, docstrings, and formal annotations. The checker is implemented using a novel integration of formal verification tools and large language models. We provide a theoretical analysis to support our t

  **work id:** 72696ae6-42c4-48cd-9c64-e90ecb9a68e9

  **citation:** Chuyue Sun et al.. Clover: Closed-Loop Verifiable Code Generation.
-
  **summary:** Loop invariants are fundamental to reasoning about programs with loops. They establish properties about a given loop’s behavior. When they additionally are inductive, they become useful for the task of formal verification that seeks to establish strong mathematical guarantees about program’s runtime behavior. The inductiveness ensures that the invariants can be checked locally without consulting the entire program, thus are indispensable artifacts in a formal proof of correctness. Finding inductive loop invariants is an undecidable problem, and despite a long history of research towards practical solutions, it remains far from a solved problem. This paper investigates the capabilities of the

  **work id:** ff9252bf-cae2-44de-861f-608f0099beae

  **citation:** Adharsh Kamath et al.. Finding Inductive Loop Invariants using Large Language Models.
-
  **summary:** We introduce Goedel-Prover-V2, a series of open-source language models that set a new state-of-the-art in automated theorem proving. Built on the standard expert iteration and reinforcement learning pipeline, our approach incorporates three key innovations: (1) Scaffolded data synthesis: We generate synthetic tasks of increasing difficulty to train the model to master increasingly complex theorems; (2) Verifier-guided self-correction: We enable the model to iteratively revise its proofs by leveraging feedback from the Lean compiler; (3) Model averaging: We merge model checkpoints to mitigate the decrease in model output diversity in later stages of training. Our small model, Goedel-Prover-V2

  **work id:** 014d75d7-1faf-459c-9c1d-60355dac4347

  **citation:** Yong Lin et al.. GOEDEL-PROVER-V2: SCALING FORMAL THEOREM PROVING WITH SCAFFOLDED DATA SYNTHESIS AND SELF-CORRECTION.
-
  **summary:** Mathematical theorem proving is an important testbed for large language models’ deep and abstract reasoning capability. This paper focuses on improving LLMs’ ability to write proofs in formal languages that permit automated proof verification/evaluation. Most previous results provide human-written lem mas to the theorem prover, which is an arguably oversimplified setting that does not sufficiently test the provers’ planning and decomposition capabilities. Instead, we work in a more natural setup where the lemmas that are directly relevant to the theorem are not given to the theorem prover at test time. We design an RL-based training algorithm that encourages the model to decompose a theorem

  **work id:** bcc6797f-f7a1-483e-b989-9e587f7470a6

  **citation:** Kefan Dong et al.. Formal Theorem Proving by Rewarding LLMs to Decompose Proofs Hierarchically.
-
  **summary:** Code large language models (LLMs) can generate syntactically plausible programs that nevertheless violate hidden semantic constraints. Existing execution-feedback training methods identify whether a completed program fails, but provide limited supervision about how a correct solution should be organized. We introduce GraphAlignCoder, a training framework that transfers explicit correctness structure into code generation. GraphAlignCoder constructs an implementation graph that captures control and dependence among program regions. In parallel, a constrained Lean pipeline produces proof traces, from which we extract a formal proof-flow graph. The model first learns executable code together wit

  **work id:** 89ee8612-5087-4f52-afe7-5c38ec4e8b2a

  **citation:** Yueke Zhang et al.. GraphAlignCoder: Aligning Program and Proof Graphs for Code Generation.
-
  **summary:** While reinforcement learning from verifiable rewards (RLVR) typically has relied on a single binary verification signal, symbolic proof assistants in formal reasoning offer rich, fine-grained structured feedback. This gap between structured processes and unstructured rewards highlights the importance of feedback that is both dense and sound. In this work, we demonstrate that the Lean proof assistant itself can serve as a symbolic process oracle, supplying both outcome-level and finegrained tactic-level verified feedback during training. Proof attempts are parsed into tactic sequences, and Lean’s elaboration marks both locally sound steps and the earliest failing step, yielding dense, verifie

  **work id:** 3ee835ff-0ef6-4deb-9524-dc9c9d854435

  **citation:** Minsu Kim & Se-Young Yun. PROCESS-VERIFIED REINFORCEMENT LEARNING FOR THEOREM PROVING VIA LEAN.
-
  **summary:** Reinforcement learning is a natural post-training paradigm for code-oriented large language models because generated programs can be evaluated through parsing, execution, unit tests, and structural analysis. However, existing methods often rely on sparse outcome rewards or statically combine heterogeneous dense signals, even though syntax validity, executability, functional correctness, and structural organization describe diferent and progressively dependent programming capabilities. We propose DHRCL, a reinforcement learning framework with Dense Hierarchical Rewards and Curriculum Learning. DHRCL decomposes feedback into syntax validation, execution success, unit-test pass rate, and AST-ba

  **work id:** cefc0910-85ca-4bc3-b4f3-7275e99c357b

  **citation:** Shuhang Wang et al.. DHRCL: Training Code LLMs with Dense Hierarchical Rewards and Curriculum Learning.
-
  **summary:** Reinforcement Learning (RL) is an important paradigm for aligning Diffusion Language Models (DLMs) toward functional correctness in code generation. However, these models often encounter a “capability cliff” on complex tasks, where execution-based semantic rewards become too low to provide a viable learning signal. In this paper, we present a systematic empirical study of RL post-training for diffusion-based code generation along three axes: reward design, hint-conditioned sampling, and task difficulty. We investigate the effectiveness of execution-free rewards as alternatives to traditional unit-test execution, the role of training-time hint-conditioned diffusion sampling in mitigating expl

  **work id:** ec111bc1-ea2a-4684-a0e8-2c4ecf28fbbc

  **citation:** Shuyin Ouyang et al.. Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation.
-
  **summary:** Specification synthesis asks a model to generate specifications and auxiliary annotations for an existing program. In modern software verification projects, specification accuracy is critical. A specification is the abstraction of a method’s behavior, and callers are verified against the callee’s specification rather than its implementation. As a result, the specification for a callee can strongly affect what properties callers can prove. However, verifier feedback alone is a poor training signal for specification synthesis: verification can prove that a specification is sound for the implementation, yet it cannot tell whether the specification is too weak. We present SpecRL, a reinforcement

  **work id:** 7dc68889-4ae4-4e2b-9adf-730c6eef74cd

  **citation:** Zhechong Huang et al.. SpecRL: Reinforcement Learning with Test-Based Completeness Rewards for Formal Specification Synthesis.
-
  **summary:** Large language models (LLMs) are increasingly integrated in software development, but ensuring correctness in LLM-generated code remains challenging and often requires costly manual review. Verifiable code generation—jointly generating code, specifications, and proofs of code-specification alignment—offers a promising path to address this limitation and further unleash LLMs' benefits in coding. Yet, there exists a significant gap in evaluation: current benchmarks often focus on only individual components rather than providing a holistic evaluation framework of all tasks. In this paper, we introduce VERINA (Verifiable Code Generation Arena), a high-quality benchmark enabling a comprehensive a

  **work id:** ec40ec37-a7f9-488e-9d36-2a4063e29f0b

  **citation:** Zhe Ye et al.. VERINA: BENCHMARKING VERIFIABLE CODE GENER-ATION.
-
  **summary:** Theorem proving is fundamental to program verification, where the automated proof of Verification Conditions (VCs) remains a primary bottleneck. Real-world program verification frequently encounters hard VCs that existing Automated Theorem Provers (ATPs) cannot prove, leading to a critical need for extensive manual proofs that burden practical application. While Neural Theorem Proving (NTP) has achieved significant success in mathematical competitions, demonstrating the potential of machine learning approaches to formal reasoning, its application to program verification—particularly VC proving—remains largely unexplored. Despite existing work on annotation synthesis and verification-related

  **work id:** 23dc03fe-4c95-4f33-bfa1-0a020ee20619

  **citation:** Qiyuan Xu et al.. NEURAL THEOREM PROVING FOR VERIFICATION CONDITIONS: A REAL-WORLD BENCHMARK.

**specific related works:**

-
  **input:** Written or natural-language software specifications; Formal task contexts containing specifications, partial implementations, helper lemmas, or proof holes; Repository context, imported definitions, and local lemmas for repository-grounded Lean tasks

  **output:** Completed Dafny or Lean programs and proofs accepted by the target verifier; Complete verified-coding artifacts with implementations, specifications, helper lemmas, and discharged proof obligations

  **summary:** Automated formal verification remains challenging for large language models because data for proof assistants and verification-aware languages is scarce, and correctness depends on satisfying precise machine-checkable specifications rather than producing plausible code. This thesis studies how verifier environments can improve LLM generation of verified programs and proofs through reinforcement learning from verifiable rewards (RLVR) and verifierguided inference-time search. First, we train open-source models in Dafny with RLVR using Group Relative Policy Optimization (GRPO) and related variants, assembling generated candidates into complete programs and scoring them with compiler and verifier outcomes. Initial experiments on an APPS-derived Dafny dataset increased verified reward from 2.2% to 58.1%, but revealed specification hacking, where models exploit weak formal specifications instead of implementing the intended solutions. After filtering underspecified and vulnerable tasks, multi-turn RLVR on the refined benchmark improves the verified pass rate from 9.7% to 31.1%. Second, we develop a verifier-guided inference scafold in Lean that treats proof generation as structured search over decomposed subgoals, verifier feedback, diagnostics, and repair. With a fixed base model, the full scafold with proof reviser improves pass rate on an initial VeriCoding pilot set from 46.2% under direct repair to 69.2%. On the larger VERINA dataset, whole-task decomposition plus proof reviser solves 7 of 42 previously unsolved tasks. We also introduce Dalek-Bench, a repository-scale Lean benchmark derived from the Rust curve25519-dalek verification project; preliminary results remain weak, indicating that stronger progress evaluation and task-specific tool-use policies are still needed. Overall, formal verifiers become useful to LLMs when they are treated not just as checkers, but as sources of reward, feedback, and search control. However, this only succeeds when the environment supplies clean data, robust specifications, and structured ways to act on verifier feedback. Benchmarks and code are available on request from maxt114@mit.edu

  **work id:** f2e06603-c7e2-4dbb-a97e-05123d0f71a3

  **approach:** The thesis combines verifier-reward post-training for Dafny with a verifier-in-the-loop Lean scafold that manages complete artifacts and performs recursive, tool-assisted, progress-controlled proof search.

  **citation:** Max Tan. Automating Formal Verification with Reinforcement Learning and Recursive Inference.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** The causal effect of typed, verdict-specific obligation rewards is not considered against equally dense execution-state supervision, binary verifier reward, and verified-goals ratio under matched checkpoints, samples, token budgets, and optimization. The paper also does not establish whether any verifier-reward gains transfer to tool-off hidden-test correctness rather than verifier-specific behavior or specification hacking.

  **method addresses:** false

  **method rationale:** Its aggregate build-and-verification rewards do not provide typed obligation vectors with distinct solver verdicts or the matched four-arm, dual-oracle experimental design required to isolate their effect.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning from Dafny verifier feedback, but the paper optimizes artifact verification success whereas our problem asks a controlled causal comparison of reward representations on tool-free hidden-test correctness.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] The causal effect of typed, verdict-specific obligation rewards is not considered against equally dense execution-state supervision, binary verifier reward, and verified-goals ratio under matched checkpoints, samples, token budgets, and optimization. The paper also does not establish whether any verifier-reward gains transfer to tool-off hidden-test correctness rather than verifier-specific behavior or specification hacking.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning from Dafny verifier feedback, but the paper optimizes artifact verification success whereas our problem asks a controlled causal comparison of reward representations on tool-free hidden-test correctness. | Its aggregate build-and-verification rewards do not provide typed obligation vectors with distinct solver verdicts or the matched four-arm, dual-oracle experimental design required to isolate their effect.

  **is potential baseline:** true
-
  **input:** A set of code implementations c; Dafny function signatures and program bodies with annotations missing

  **output:** Full Dafny code implementations with corresponding formal specifications y; Preconditions, postconditions, loop invariants, assert statements, and other applicable annotations

  **summary:** Existing informal language-based (e.g., human language) Large Language Models (LLMs) trained with Reinforcement Learning (RL) face a significant challenge: their verification processes, which provide crucial training signals, are neither reliable nor scalable. In fact, the prevalent large proprietary models could hardly generate verifiable programs. A promising yet largely uncharted alternative is formal language-based reasoning. Grounding LLMs in rigorous formal systems where generative models operate in formal language spaces (e.g., Dafny) enables the automatic and mathematically provable verification of their reasoning processes and outcomes. This capability is pivotal for achieving large-scale, reliable formal software verification. It is a common practice to employ human-annotated chain-of-thought and answers to induce the reasoning and coding capabilities of LLMs. Unfortunately, it becomes unacceptably all-consuming to provide such priors for supervising complex programming tasks. In this work, we systematically explore ways to reduce human annotations with the formal language, Dafny, as the main environment for our pilot study. Our pipeline mainly relies on introducing an automatic and scalable data curation pipeline, and careful RL designs integrated with feedback from the formal language verifier. We introduce DafnyComp, a benchmark of compositional formal programs with auto-formalized specifications for specification reasoning. Our supervised fine-tuning (SFT) stage enables even small models (e.g., 0.5B) to generate syntactically valid and verifiable Dafny code, surpassing proprietary models. RL with regularization further improves performance, achieving stronger generalization to out-of-domain tasks and outperforming all strong baselines on the challenging DafnyComp benchmark. Anonymized code and models are available at https://github. com/Veri-Code/ReForm and https://huggingface.co/Veri-Code.

  **work id:** ed715f66-e278-48af-907e-352d4d5b2a18

  **approach:** Re:Form combines automated data curation, a compositional benchmark, limited CoT-free supervised fine-tuning, and verifier-guided reinforcement learning with syntax, verification, and subset rewards plus policy regularization.

  **citation:** Chuanhao Yan et al.. Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** The causal advantage of typed obligation-verdict supervision over dense execution-state, binary verification, and scalar proof-ratio rewards is not considered. Re:Form therefore cannot determine whether its RL gains transfer to tool-free hidden-test correctness or instead reflect specification or verifier optimization.

  **method addresses:** false

  **method rationale:** Re:Form does not expose typed obligations with distinct solver verdicts, score every candidate with matched verification and execution oracles, or conduct the controlled multi-arm, tool-off evaluation required to isolate reward-signal effects.

  **problem alignment:** related

  **alignment rationale:** Both study verifier-guided reinforcement learning for Dafny generation, but Re:Form optimizes specification generation and verifier/specification quality, whereas our problem asks whether typed obligation-verdict rewards causally improve tool-free implementation correctness relative to matched reward alternatives.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] The causal advantage of typed obligation-verdict supervision over dense execution-state, binary verification, and scalar proof-ratio rewards is not considered. Re:Form therefore cannot determine whether its RL gains transfer to tool-free hidden-test correctness or instead reflect specification or verifier optimization.

    **limitation id:** lim-1

    **evidence for limitation:** Both study verifier-guided reinforcement learning for Dafny generation, but Re:Form optimizes specification generation and verifier/specification quality, whereas our problem asks whether typed obligation-verdict rewards causally improve tool-free implementation correctness relative to matched reward alternatives. | Re:Form does not expose typed obligations with distinct solver verdicts, score every candidate with matched verification and execution oracles, or conduct the controlled multi-arm, tool-off evaluation required to isolate reward-signal effects.

  **is potential baseline:** true
-
  **input:** A pretrained code LLM; Executable programs paired with concrete inputs; Code-generation problems paired with unit tests

  **output:** A post-trained code LLM with improved execution reasoning; Predictions of intermediate control flow, variable values and types, and final program outputs; Generated programs that pass functional unit tests

  **summary:** Code LLMs still struggle with code execution reasoning, especially in smaller models. Existing methods rely on supervised fine-tuning (SFT) with teacher-generated explanations, pri marily in two forms: (1) input–output (I/O) prediction chains and (2) natural-language descriptions of execution traces. However, intermediate execution steps cannot be explicitly verified during SFT, so the training objective can be reduced to merely matching teacher explanations. Moreover, training data is typically collected without explicit control over task difficulty. We introduce ExecVerify, which goes beyond text imitation by incorporating verifi able white-box rewards derived from execution traces, including next-statement prediction and variable value/type prediction. Our work first builds a dataset with multiple difficulty levels via constraint-based program synthesis. Then, we apply reinforcement learning (RL) to re ward correct answers about both intermediate execution steps and final outputs, aligning the training objective with semantic correctness at each execution step. Finally, we adopt a twostage training pipeline that first enhances execution reasoning and then transfers to code generation. Experiments demonstrate that a 7B model trained with ExecVerify achieves performance comparable to 32B models on code reasoning benchmarks and improves pass@1 by up to 5.9% on code generation tasks over strong post-training baselines<sup>1</sup>.

  **work id:** f3fd4016-a31d-4e0c-90b7-f1964696c386

  **approach:** ExecVerify combines constraint-based curriculum data synthesis with a two-stage post-training pipeline using interpreter-derived white-box rewards for execution reasoning and unit-test rewards for code generation.

  **citation:** Lingxiao Tang et al.. ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** ExecVerify does not consider whether typed obligation-and-verdict rewards outperform equally dense execution-state rewards or scalar verification rewards when checkpoints, candidates, token budgets, and optimization are matched. Consequently, the causal value of obligation type and solver-verdict distinctions for tool-off hidden-test correctness remains unresolved.

  **method addresses:** false

  **method rationale:** ExecVerify lacks typed proof obligations, distinct solver verdicts, binary and ratio ablations, dual-oracle candidate scoring, and the matched on-policy experimental design required to isolate the effect of reward semantics.

  **problem alignment:** related

  **alignment rationale:** Both study whether dense intermediate supervision improves functionally correct code generation, but ExecVerify optimizes concrete Python execution reasoning rather than causally comparing typed Dafny verifier signals under matched training conditions.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] ExecVerify does not consider whether typed obligation-and-verdict rewards outperform equally dense execution-state rewards or scalar verification rewards when checkpoints, candidates, token budgets, and optimization are matched. Consequently, the causal value of obligation type and solver-verdict distinctions for tool-off hidden-test correctness remains unresolved.

    **limitation id:** lim-1

    **evidence for limitation:** Both study whether dense intermediate supervision improves functionally correct code generation, but ExecVerify optimizes concrete Python execution reasoning rather than causally comparing typed Dafny verifier signals under matched training conditions. | ExecVerify lacks typed proof obligations, distinct solver verdicts, binary and ratio ablations, dual-oracle candidate scoring, and the matched on-policy experimental design required to isolate the effect of reward semantics.

  **is potential baseline:** true
-
  **input:** A program P and input I for output prediction; A program P and target output Y for input prediction; Execution-trace anchors inserted into the program

  **output:** The predicted program result Y for output prediction; The required input I for input prediction; A complete predicted execution trajectory of intermediate runtime states followed by the final value

  **summary:** Existing code reasoning methods primarily supervise final code outputs, ignoring intermediate states, often leading to reward hacking where correct answers are obtained through inconsistent reasoning. We propose StepCodeReasoner, a framework that introduces explicit intermediate execution-state supervision. By automatically inserting structured print-based execution-trace anchors into code, the model is trained to predict runtime states at each step, transforming code reasoning into a verifiable, stepwise execution modeling problem. Building on this execution-aware method, we introduce Bi-Level GRPO, a reinforcement learning algorithm for structured credit assignment at two levels: intertrajectory, comparing alternative execution paths, and intra-trajectory, rewarding intermediate accuracy based on its impact on downstream correctness. Extensive experiments demonstrate that StepCodeReasoner achieves SOTA performance in code reasoning. In particular, our 7B model achieves 91.1% on CRUXEval and 86.5% on Live-CodeBench, outperforming the CodeReasoner-7B baseline (86.0% and 77.7%) and GPT-4o (85.6% and 75.1%). Furthermore, on the execution-trace benchmark REval, our model scores 82.9%, outperforming baseline CodeReasoner-7B (72.3%), its 14B counterpart (81.1%), and GPT-4o (77.3%). Additionally, our approach also improves code generation performance, demonstrating that explicit execution modeling enhances both code reasoning and code generation.

  **work id:** 6158d5ab-eaf4-4421-968b-c5c42a0fba2b

  **approach:** StepCodeReasoner makes intermediate execution states observable through automatically inserted anchors, structures input and output prediction as execution-aligned traces, and applies Bi-Level GRPO for stepwise and trajectory-aware credit assignment.

  **citation:** Hao Wang et al.. StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** The causal effect of typed obligation-verdict rewards relative to equally dense execution-state rewards and scalar proof-completion rewards under matched training conditions is not considered. Their setup also does not test tool-off Dafny correctness, specification hacking, verifier-behavior divergence, or the distinct effects of refutation, unknown, and timeout verdicts.

  **method addresses:** false

  **method rationale:** Its interpreter-based step rewards provide a relevant dense-execution baseline but do not produce typed proof obligations, distinguish solver verdicts, or conduct the required matched reward-signal comparison.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning from dense execution-grounded signals, but StepCodeReasoner predicts execution traces and answers for Python reasoning tasks, whereas our problem causally compares verifier-derived and execution-derived rewards for tool-free Dafny synthesis.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] The causal effect of typed obligation-verdict rewards relative to equally dense execution-state rewards and scalar proof-completion rewards under matched training conditions is not considered. Their setup also does not test tool-off Dafny correctness, specification hacking, verifier-behavior divergence, or the distinct effects of refutation, unknown, and timeout verdicts.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning from dense execution-grounded signals, but StepCodeReasoner predicts execution traces and answers for Python reasoning tasks, whereas our problem causally compares verifier-derived and execution-derived rewards for tool-free Dafny synthesis. | Its interpreter-based step rewards provide a relevant dense-execution baseline but do not produce typed proof obligations, distinguish solver verdicts, or conduct the required matched reward-signal comparison.

  **is potential baseline:** true
-
  **input:** A natural-language problem description; Example unit tests included in the problem specification

  **output:** A complete executable program represented as a sequence of code tokens

  **summary:** Program synthesis or code generation aims to generate a program that satisfies a problem specification. Recent approaches using large-scale pretrained language models (LMs) have shown promising results, yet they have some critical limitations. In particular, they often follow a standard supervised fine-tuning procedure to train a code generation model only from the pairs of natural-language problem descriptions and ground-truth programs. Such paradigm largely ignores some important but potentially useful signals in the problem specification such as unit tests, which thus often results in poor performance when solving complex unseen coding tasks. To address the limitations, we propose “CodeRL”, a new framework for program synthesis tasks through pretrained LMs and deep reinforcement learning (RL). Specifically, during training, we treat the code-generating LM as an actor network, and introduce a critic network that is trained to predict the functional correctness of generated programs and provide dense feedback signals to the actor. During inference, we introduce a new generation procedure with a critical sampling strategy that allows a model to automatically regenerate programs based on feedback from example unit tests and critic scores. For the model backbones, we extended the encoder-decoder architecture of CodeT5 with enhanced learning objectives, larger model sizes, and better pretraining data. Our method not only achieves new SOTA results on the challenging APPS benchmark, but also shows strong zero-shot transfer capability with new SOTA results on the simpler MBPP benchmark.

  **work id:** 053e1aff-0f9a-4f40-a563-0fa5feff32dc

  **approach:** CodeRL combines an improved CodeT5 foundation model, actor-critic reinforcement learning driven by unit-test outcomes, token-level critic feedback, and critic-guided program refining and repairing.

  **citation:** Hung Le et al.. CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** CodeRL does not consider whether obligation type and solver-verdict identity provide a causal advantage over reward signals of matched density and cost. Its test-derived critic feedback also does not preserve the required distinctions among refutation, unknown, timeout, and invalid verification outcomes.

  **method addresses:** false

  **method rationale:** CodeRL cannot answer the target comparison because it neither observes typed verification obligations and distinct solver verdicts nor conducts matched reward-arm experiments against binary verification, verified-goals ratios, and equally dense execution supervision.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning for code generation from program-behavior feedback, but CodeRL generates complete Python programs from natural-language tasks to pass tests, whereas our problem isolates the causal effect of typed verifier verdicts on tool-free Dafny correctness under matched training conditions.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] CodeRL does not consider whether obligation type and solver-verdict identity provide a causal advantage over reward signals of matched density and cost. Its test-derived critic feedback also does not preserve the required distinctions among refutation, unknown, timeout, and invalid verification outcomes.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning for code generation from program-behavior feedback, but CodeRL generates complete Python programs from natural-language tasks to pass tests, whereas our problem isolates the causal effect of typed verifier verdicts on tool-free Dafny correctness under matched training conditions. | CodeRL cannot answer the target comparison because it neither observes typed verification obligations and distinct solver verdicts nor conducts matched reward-arm experiments against binary verification, verified-goals ratios, and equally dense execution supervision.

  **is potential baseline:** true
-
  **input:** formal theorem statements in Lean 4; the Lean 4 proof environment and available premises and tactics

  **output:** complete Lean 4 proof code verified as correct by the Lean prover; diverse valid proof paths discovered through tree search

  **summary:** We introduce DeepSeek-Prover-V1.5, an open-source language model designed for theorem proving in Lean 4, which enhances DeepSeek-Prover-V1 by optimizing both training and inference processes. Pre-trained on DeepSeekMath-Base with specialization in formal mathematical languages, the model undergoes supervised fine-tuning using an enhanced formal theorem proving dataset derived from DeepSeek-Prover-V1. Further refinement is achieved through reinforcement learning from proof assistant feedback (RLPAF). Beyond the single-pass whole-proof generation approach of DeepSeek-Prover-V1, we propose RMaxTS, a variant of Monte-Carlo tree search that employs an intrinsic-reward-driven exploration strategy to generate diverse proof paths. DeepSeek-Prover-V1.5 demonstrates significant improvements over DeepSeek-Prover-V1, achieving new state-of-the-art results on the test set of the high school level miniF2F benchmark (63.5%) and the undergraduate level ProofNet benchmark (25.3%).

  **work id:** 53bf4509-2815-4472-8014-2d961a724e37

  **approach:** DeepSeek-Prover-V1.5 combines formal-language pre-training, augmented supervised fine-tuning, reinforcement learning from Lean feedback, and an intrinsic-reward-driven Monte-Carlo tree search based on truncate-and-resume proof generation.

  **citation:** Huajian Xin et al.. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They do not consider whether obligation type and distinct solver verdicts improve tool-free coding over binary verification, a scalar verified-goals ratio, or equally dense execution supervision under matched training conditions. Consequently, the causal value of structured verifier feedback remains unidentified.

  **method addresses:** false

  **method rationale:** Their binary Lean-verification reward and inference-time proof search do not provide typed obligation verdicts, dense execution-state controls, matched dual-oracle scoring, or tool-off evaluation needed to answer our causal comparison.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning from formal-verifier feedback, but they optimize verifier-accepted Lean proofs whereas we causally compare alternative reward signals for tool-free Dafny program correctness.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] They do not consider whether obligation type and distinct solver verdicts improve tool-free coding over binary verification, a scalar verified-goals ratio, or equally dense execution supervision under matched training conditions. Consequently, the causal value of structured verifier feedback remains unidentified.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning from formal-verifier feedback, but they optimize verifier-accepted Lean proofs whereas we causally compare alternative reward signals for tool-free Dafny program correctness. | Their binary Lean-verification reward and inference-time proof search do not provide typed obligation verdicts, dense execution-state controls, matched dual-oracle scoring, or tool-off evaluation needed to answer our causal comparison.

  **is potential baseline:** true
-
  **input:** formal theorem statements in Lean 4; natural-language mathematical reasoning or proof sketches; formal-language training problems and verified proof demonstrations

  **output:** complete Lean 4 proofs of the input theorems; formally verified proofs whose decomposed subgoals are resolved; concise non-CoT proofs or step-by-step CoT proofs

  **summary:** We introduce DeepSeek-Prover-V2, an open-source large language model designed for formal theorem proving in Lean 4, with initialization data collected through a recursive theorem proving pipeline powered by DeepSeek-V3. The cold-start training procedure begins by prompting DeepSeek-V3 to decompose complex problems into a series of subgoals. The proofs of resolved subgoals are synthesized into a chain-of-thought process, combined with DeepSeek-V3’s stepby-step reasoning, to create an initial cold start for reinforcement learning. This process enables us to integrate both informal and formal mathematical reasoning into a unified model. The resulting model, DeepSeek-Prover-V2-671B, achieves state-of-the-art performance in neural theorem proving, reaching 88.9% pass ratio on the MiniF2F-test and solving 47 out of 658 problems from PutnamBench. In addition to standard benchmarks, we introduce ProverBench, a collection of 325 formalized problems, to enrich our evaluation, including 15 selected problems from the recent AIME competitions (years 24-25). Further evaluation on these 15 AIME problems shows that the model successfully solves 6 of them. In comparison, DeepSeek-V3 solves 8 of these problems using majority voting, highlighting that the gap between formal and informal mathematical reasoning in large language models is substantially narrowing.

  **work id:** 8789ef63-56c9-4a18-b669-530b3aec3ea2

  **approach:** DeepSeek-Prover-V2 combines recursive subgoal decomposition, lightweight subgoal proof search, curriculum-based expert iteration, synthetic cold-start reasoning data, supervised fine-tuning, reinforcement learning, and distillation.

  **citation:** Z.Z. Ren et al.. DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They do not consider whether obligation type and distinct solver verdicts causally improve tool-free coding over binary verification, a scalar verified-goals ratio, or equally dense execution supervision under matched training controls. They also do not measure timeout-versus-refutation effects, specification hacking, or verifier-behavior divergence.

  **method addresses:** false

  **method rationale:** Their binary Lean-verification GRPO does not provide typed obligation verdicts, dense execution-state rewards, dual-oracle scoring, matched-arm controls, or tool-off behavioral evaluation required to answer our comparison.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning from formal-verification feedback, but they generate Lean theorem proofs for verifier pass rates whereas we causally compare reward signals for Dafny program synthesis on tool-off hidden-test correctness.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] They do not consider whether obligation type and distinct solver verdicts causally improve tool-free coding over binary verification, a scalar verified-goals ratio, or equally dense execution supervision under matched training controls. They also do not measure timeout-versus-refutation effects, specification hacking, or verifier-behavior divergence.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning from formal-verification feedback, but they generate Lean theorem proofs for verifier pass rates whereas we causally compare reward signals for Dafny program synthesis on tool-off hidden-test correctness. | Their binary Lean-verification GRPO does not provide typed obligation verdicts, dense execution-state rewards, dual-oracle scoring, matched-arm controls, or tool-off behavioral evaluation required to answer our comparison.

  **is potential baseline:** true
-
  **input:** Few-shot mathematical solution examples sourced from GSM8K and MATH; Large language models that generate synthetic questions and candidate reasoning answers; A Lean theorem prover used to validate formalised questions and reasoning steps

  **output:** Synthetic mathematical question-answer samples with theorem-prover-verified intermediate reasoning; A verified subset for Supervised Fine-Tuning and preference pairs for Direct Preference Optimisation; Mathematical reasoning models trained sequentially with SFT and DPO

  **summary:** The demand for synthetic data in mathematical reasoning has increased due to its potential to enhance the mathematical capabilities of large language models (LLMs). However, ensuring the validity of intermediate reasoning steps remains a significant challenge, affecting data quality. While formal verification via theorem provers effectively validates LLM reasoning, the autoformalisation of mathematical proofs remains error-prone. We introduce iterative autoformalisation, an approach that iteratively refines theorem prover formalisation to mitigate errors, thereby increasing the execution rate on the Lean prover from 60% to 87%. Building upon that, we introduce Theorem Prover as a Judge (TP-as-a-Judge), a method that makes use of theorem prover formalisation to rigorously assess LLM intermediate reasoning, effectively integrating autoformalisation with synthetic data generation. Finally, we present Reinforcement Learning from Theorem Prover Feedback (RLTPF), a framework that replaces human annotation with theorem prover feedback in Reinforcement Learning from Human Feedback (RLHF). Across multiple LLMs, applying TP-as-a-Judge and RLTPF improves benchmarks with only 3,508 samples, achieving 5.56% accuracy gain on Mistral-7B for MultiArith, 6.00% on Llama-2- 7B for SVAMP, and 3.55% on Llama-3.1-8B for AQUA.<sup>1</sup>

  **work id:** b17b4be4-e8fc-4956-9f17-d691ee7e0458

  **approach:** TP-as-a-Judge generates mathematical questions and answers, formalises and verifies their questions and intermediate reasoning with Lean, iteratively repairs execution errors, and uses verification outcomes to allocate training data for SFT and DPO.

  **citation:** Joshua Ong Jun Leang et al.. Theorem Prover as a Judge for Synthetic Data Generation.

  **comparison:**

  **role:** baseline

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** RLTPF does not consider whether obligation type and distinct refuted, unknown, timeout, and invalid verdicts causally improve tool-free program correctness beyond binary or scalar prover feedback. It also does not compare prover-derived and execution-derived rewards under matched candidates, checkpoints, token budgets, and optimization.

  **method addresses:** false

  **method rationale:** RLTPF's verified-data SFT followed by binary preference DPO neither constructs typed obligation-verdict rewards nor performs matched on-policy comparisons against equally dense execution supervision and scalar verifier baselines.

  **problem alignment:** related

  **alignment rationale:** Both study learning from theorem-prover feedback, but RLTPF trains mathematical reasoning models from Lean-verified synthetic data whereas our problem causally compares typed verifier verdicts, scalar proof rewards, and execution-state rewards for tool-free Dafny coding.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] RLTPF does not consider whether obligation type and distinct refuted, unknown, timeout, and invalid verdicts causally improve tool-free program correctness beyond binary or scalar prover feedback. It also does not compare prover-derived and execution-derived rewards under matched candidates, checkpoints, token budgets, and optimization.

    **limitation id:** lim-1

    **evidence for limitation:** Both study learning from theorem-prover feedback, but RLTPF trains mathematical reasoning models from Lean-verified synthetic data whereas our problem causally compares typed verifier verdicts, scalar proof rewards, and execution-state rewards for tool-free Dafny coding. | RLTPF's verified-data SFT followed by binary preference DPO neither constructs typed obligation-verdict rewards nor performs matched on-policy comparisons against equally dense execution supervision and scalar verifier baselines.

  **is potential baseline:** true

## Sub-Problems

**summary:** Completing the problem requires a matched multi-arm causal experiment, typed-verdict reward construction with scalar ablations, and tool-off behavioral evaluation. Prior work neither isolates reward semantics under shared controls nor establishes that verifier gains reflect robust functional correctness.

**sub problems:**

-
  **description:** Matched causal reward comparison: estimate all four reward arms under shared checkpoints, instances, sampled-token budgets, optimization, verifier, and test harness.

  **sub problem id:** sp-1

  **technical challenge:** On-policy arms diverge after seeding, so comparable estimates require dual-oracle scoring, budget matching, and inference that does not assume identical later candidates.

  **why it is a problem:** This comparison is necessary to attribute gains to typed proof structure rather than generic reward density, verifier acceptance, or proof-completion ratio.

  **source limitation ids:** - lim-1
-
  **description:** Typed-verdict reward construction: encode raw obligation-type and solver-verdict vectors and derive fixed binary and scalar-collapse ablations from the same signals.

  **sub problem id:** sp-2

  **technical challenge:** Matched-density controls must equalize reward frequency and scale without erasing the verdict distinctions being tested.

  **why it is a problem:** Without isolating these distinctions, the experiment cannot determine whether typed verifier semantics provide the claimed causal advantage.

  **source limitation ids:** - lim-1
-
  **description:** Tool-off behavioral validation: evaluate hidden-test correctness without verifier or countermodel access and quantify robustness, specification hacking, verifier divergence, and scalarization sensitivity.

  **sub problem id:** sp-3

  **technical challenge:** The evaluation must separate behavioral correctness from formal acceptance across perturbations and unseen structures while retaining enough power to detect arm-level differences.

  **why it is a problem:** Verifier acceptance alone cannot show that training produced genuinely better coding behavior rather than verifier-specific optimization or weakened specifications.

  **source limitation ids:** - lim-1

**internal reasoning:**

**required components:**

-
  **name:** Matched causal reward comparison

  **note:** No prior work compares typed-verdict, dense execution-state, binary verifier, and proof-ratio rewards with matched checkpoints, budgets, optimization, and dual-oracle scoring.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Typed-verdict reward isolation

  **note:** Prior approaches do not isolate obligation type and distinct proved, refuted, unknown, timeout, and invalid verdicts from reward density or scalar proof completion.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Tool-off behavioral validation

  **note:** Prior work does not establish robust tool-off hidden-test gains while measuring specification hacking, verifier-behavior divergence, and scalarization sensitivity.

  **status:** unsolved

  **covered by limitation ids:** - lim-1

## Method Design

**methods:**

-
  **method id:** m-1

  **hypotheses:**

  - Typed-verdict training improves tool-off hidden-test pass@1 over dense execution-state training by at least 2 percentage points, with a two-sided 95% cluster-bootstrap interval excluding zero.
  - Typed-verdict training improves tool-off hidden-test pass@1 over the verified-goals-ratio arm by at least 2 percentage points, with a two-sided 95% cluster-bootstrap interval excluding zero.

  **key insight:** Randomized policy forks identify reward effects without requiring later candidate overlap, while dual scoring and exact budget matching expose oracle alignment and remove compute as a competing explanation.

  **proposed approach:** Run a seed-blocked four-arm randomized fork trial from shared checkpoints, assigning replicate policies to typed-verdict, dense execution-state, binary-verifier, or RLFR-style verified-goals-ratio reward while matching tasks, sampled tokens, candidates per task, optimizer, updates, verifier, and harness. At fixed code snapshots, a frozen Dual-Oracle Panel scores every on-policy candidate with both verifier and execution oracles; estimate arm contrasts using a checkpoint-by-task hierarchical model and cluster bootstrap over checkpoint seeds and instances.

  **target sub problem id:** sp-1
-
  **method id:** m-2

  **hypotheses:**

  - On a disjoint calibration-audit set, each arm emits exactly K reward packets per candidate and its post-calibration reward RMS remains within 5% of the typed arm's RMS.
  - A preregistered logistic probe using typed reward packets achieves at least 5% lower cross-validated hidden-correctness log loss than the same probe using the verified-goals ratio alone.

  **key insight:** Synchronized deterministic coarsenings hold reward timing and scale constant, so the experimental difference is whether obligation and verdict identities remain available to the optimizer.

  **proposed approach:** At K fixed token-indexed snapshots, encode changes in counts for every obligation-type-by-verdict channel—proved, refuted, unknown, timeout, and invalid—and compute channel-normalized multi-head advantages combined by one preregistered fixed weight vector, with alternate fixed vectors reserved for sensitivity analysis. Derive ratio and binary rewards at the same snapshots by deterministic coarsening to proved/total and all-proved, zero-fill unavailable events, and calibrate each arm on a frozen pre-RL corpus to unit reward RMS under common clipping.

  **target sub problem id:** sp-2
-
  **method id:** m-3

  **hypotheses:**

  - The typed arm retains at least 90% of its clean hidden-test pass@1 under perturbations and exceeds the dense execution-state arm's perturbed pass@1 by at least 2 percentage points.
  - Relative to the verified-goals-ratio arm, the typed arm reduces the rate of weakened-specification verifier passes with hidden-test failure by at least 20%, while its maximum pass@1 spread across fixed scalarizations is no greater than 2 percentage points.

  **key insight:** Keeping semantic tests independent and verifier feedback unavailable during generation makes behavioral correctness primary, while paired perturbations and post-hoc diagnostics localize robustness failures and verifier-specific optimization.

  **proposed approach:** Use the frozen Dual-Oracle Panel to sample pass@1 outputs with verifier and countermodel access disabled on a blinded battery stratified by unseen program structures and paired semantics-preserving prompt and input perturbations, then judge behavior using independent property-based and metamorphic hidden tests. Post hoc, apply the common verifier and an original-specification AST comparator to report clean and perturbed correctness, specification hacking, verifier–behavior disagreement, and matched outcomes for every preregistered typed scalarization.

  **target sub problem id:** sp-3

**summary:** Use randomized, seed-blocked policy forks with identical training resources and dual-oracle scoring to isolate the causal contribution of each reward signal despite on-policy divergence. Construct all verifier rewards from synchronized snapshots, then evaluate tool-off behavior with independent hidden tests, structural perturbations, and post-hoc verifier diagnostics.

## Experiment Design

**summary:** The evaluation uses matched four-arm training runs and sealed tool-off hidden tests to isolate reward-representation effects while controlling checkpoints, data, optimization, verifier, and token budgets. Separate audit and stress populations test reward calibration, predictive information, perturbation robustness, specification hacking, verifier-behavior divergence, and scalarization sensitivity.

**datasets:**

-
  **name:** Matched tool-off hidden-test suite

  **justification:** Contains 6,000 sealed tasks stratified by repository or template family, obligation-type signature, solver-verdict mix, and difficulty, creating paired cases where reward representations can produce different tool-independent behavior.
-
  **name:** Disjoint reward calibration-audit corpus

  **justification:** Contains frozen candidates from task families excluded from training and primary evaluation, with coverage of feasible obligation-type by verdict cells; it can reveal packetization errors, scale mismatch, and circular prediction leakage.
-
  **name:** Perturbation and weakened-specification stress suite

  **justification:** Pairs clean tasks with semantics-preserving surface variants and controlled specification weakenings, directly stressing robustness, specification hacking, verifier-hidden-test divergence, and scalarization sensitivity.

**baselines:**

-
  **name:** Dense execution-state reward

  **justification:** Primary matched contrast isolating typed verdict feedback from dense execution supervision under identical training resources.
-
  **name:** Binary verifier reward

  **justification:** Fixed binary collapse of the verifier signals that checks whether any observed effect requires typed verdict structure rather than verifier pass/fail alone.
-
  **name:** RLFR-style verified-goals ratio

  **justification:** Mandatory scalar-collapse ablation derived from the same obligation signals, isolating information retained by typed packets beyond aggregate verified-goal coverage.

**research questions:**

-
  **tier:** mechanism

  **rq id:** rq-1

  **setup:** Train typed-verdict, dense execution-state, binary verifier, and verified-goals-ratio arms from the same 8 initialization checkpoints, matching training instances, optimizer, sampled-token budget, verifier, and harness. Evaluate one tool-off completion from every arm-checkpoint pair on N=6,000 sealed tasks; estimate paired differences using 10,000 two-way cluster-bootstrap resamples over task and checkpoint.

  **metrics:** Per-arm tool-off hidden-test pass@1, paired typed-minus-dense difference, confidence interval, and descriptive typed-minus-binary and typed-minus-ratio estimates.

  **description:** Under fully matched training and evaluation conditions, what is the causal effect of typed-verdict reward rather than dense execution-state reward on tool-off hidden-test pass@1?

  **expected outcome:** The typed-minus-dense estimate is at least 0.02 and its two-sided 95% cluster-bootstrap interval excludes zero.

  **statistical test:** Two-sided cluster-bootstrap test of typed-minus-dense pass@1 at alpha=0.05.

  **target hypotheses:** - Typed-verdict training improves tool-off hidden-test pass@1 over dense execution-state training by at least 2 percentage points, with a two-sided 95% cluster-bootstrap interval excluding zero.

  **sample size rationale:** N=6,000 tasks and 8 checkpoint blocks target at least 80% power for a 2-point paired difference under prospective simulations allowing paired-outcome discordance up to 0.30.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-2

  **setup:** Use the same matched four-arm experiment, N=6,000 sealed tasks, and 8 shared checkpoint blocks as rq-1. Compare typed and verified-goals-ratio outcomes task by task using 10,000 two-way cluster-bootstrap resamples; keep the binary and dense arms as matched secondary checks.

  **metrics:** Tool-off hidden-test pass@1 by arm, paired typed-minus-ratio difference, confidence interval, and checkpoint-level heterogeneity.

  **description:** Does retaining typed solver-verdict information improve tool-off correctness relative to collapsing the same signals into a verified-goals ratio?

  **expected outcome:** The typed-minus-ratio estimate is at least 0.02 and its two-sided 95% cluster-bootstrap interval excludes zero.

  **statistical test:** Two-sided cluster-bootstrap test of typed-minus-ratio pass@1 at alpha=0.05.

  **target hypotheses:** - Typed-verdict training improves tool-off hidden-test pass@1 over the verified-goals-ratio arm by at least 2 percentage points, with a two-sided 95% cluster-bootstrap interval excluding zero.

  **sample size rationale:** The N=6,000 paired tasks target at least 80% power for a 2-point effect under paired-outcome discordance up to 0.30, while 8 blocks expose checkpoint sensitivity.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-3

  **setup:** Freeze K=32 schema-indexed reward slots and scalar calibration factors before auditing N=10,000 candidates from 2,000 disjoint tasks and 5 generation seeds. Record packet counts and compute each arm's RMS ratio to the typed arm; use a task-clustered simultaneous bootstrap equivalence check.

  **metrics:** Packet-count violation rate, per-arm reward RMS, RMS ratio to typed, and simultaneous confidence intervals.

  **description:** Does the implemented reward pipeline preserve matched reward opportunity counts and reward scale across arms on data excluded from calibration?

  **expected outcome:** Every audited candidate has exactly 32 packets for every arm, and every non-typed arm's simultaneous confidence interval for RMS relative to typed lies wholly within [0.95, 1.05].

  **statistical test:** Zero-tolerance packet-count audit plus simultaneous bootstrap equivalence tests for RMS ratios against [0.95, 1.05] at familywise alpha=0.05.

  **target hypotheses:** - On a disjoint calibration-audit set, each arm emits exactly K reward packets per candidate and its post-calibration reward RMS remains within 5% of the typed arm's RMS.

  **sample size rationale:** N=10,000 supports at least 100 audited candidates in every feasible obligation-type by solver-verdict cell and provides precise clustered RMS-ratio estimates.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-4

  **setup:** Construct N=12,000 frozen candidates from 2,400 tasks excluded from training, reward calibration, and primary evaluation. Fit preregistered regularized logistic probes using either the 32 typed packets or the ratio alone, with identical preprocessing and nested 10-fold cross-validation grouped by task; hidden correctness is used only as the label.

  **metrics:** Out-of-fold log loss, relative log-loss reduction, calibration error, and task-clustered confidence bound.

  **description:** Do typed reward packets contain non-circular information about hidden correctness that is lost in the verified-goals scalar collapse?

  **expected outcome:** The typed-packet probe's relative log-loss reduction is at least 0.05, with its one-sided 95% lower confidence bound at or above 0.05.

  **statistical test:** One-sided task-cluster bootstrap test of relative out-of-fold log-loss reduction at alpha=0.05.

  **target hypotheses:** - A preregistered logistic probe using typed reward packets achieves at least 5% lower cross-validated hidden-correctness log loss than the same probe using the verified-goals ratio alone.

  **sample size rationale:** N=12,000 yields 2,400 independent task clusters, broad obligation-verdict coverage, and at least 80% simulated power for a 5% relative log-loss reduction using blinded nuisance estimates.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-5

  **setup:** For N=6,000 base tasks, evaluate clean inputs and six preregistered semantics-preserving variants covering identifier changes, equivalent specification rewrites, conjunct reordering, formatting changes, and irrelevant-context insertion. Run typed and dense models from all 8 matched checkpoints without verifier or countermodel access; use joint task-and-checkpoint cluster bootstrapping.

  **metrics:** Clean and perturbed pass@1, perturbed-to-clean retention ratio, paired arm difference, per-perturbation results, and worst-group retention.

  **description:** Is tool-off correctness learned under typed-verdict reward stable under semantics-preserving perturbations, and is that stability greater than for dense execution-state reward?

  **expected outcome:** The lower simultaneous confidence bounds are at least 0.90 for typed perturbed-to-clean retention and at least 0.02 for typed-minus-dense perturbed pass@1.

  **statistical test:** Simultaneous one-sided cluster-bootstrap tests for typed retention and typed-minus-dense perturbed pass@1 at familywise alpha=0.05.

  **target hypotheses:** - The typed arm retains at least 90% of its clean hidden-test pass@1 under perturbations and exceeds the dense execution-state arm's perturbed pass@1 by at least 2 percentage points.

  **sample size rationale:** N=6,000 base-task clusters targets at least 80% power for a 2-point paired perturbed-pass difference under discordance up to 0.30 and covers all perturbation families by obligation stratum.

  **target sub problem id:** sp-3
-
  **tier:** mechanism

  **rq id:** rq-6

  **setup:** Evaluate N=10,000 weakenable tasks under preregistered specification-removal transformations, with hidden tests unchanged and tool access disabled. Compare typed and ratio arms across 8 matched checkpoints, and train typed variants under 8 fixed scalarizations chosen before hidden-test access and RMS-matched using rq-3; use task-and-checkpoint cluster bootstrapping with simultaneous bounds.

  **metrics:** Weakened-specification verifier-pass/hidden-failure rate, typed-to-ratio rate ratio, pass@1 by scalarization, maximum scalarization spread, and simultaneous confidence bounds.

  **description:** Does typed-verdict training reduce verifier-pass/hidden-failure divergence caused by weakened specifications, and is its behavior insensitive to preregistered scalarization choices?

  **expected outcome:** The upper confidence bound on the divergence rate ratio is at most 0.80, and the upper confidence bound on maximum pass@1 spread across scalarizations is at most 0.02.

  **statistical test:** Simultaneous one-sided cluster-bootstrap upper-bound tests for the typed-to-ratio divergence rate ratio and the scalarization max-minus-min spread at familywise alpha=0.05.

  **target hypotheses:** - Relative to the verified-goals-ratio arm, the typed arm reduces the rate of weakened-specification verifier passes with hidden-test failure by at least 20%, while its maximum pass@1 spread across fixed scalarizations is no greater than 2 percentage points.

  **sample size rationale:** N=10,000 targets at least 80% power for a 20% rate-ratio reduction under a conservative 10% ratio-arm divergence-rate design assumption and gives adequate precision for a 2-point scalarization-spread bound.

  **target sub problem id:** sp-3
