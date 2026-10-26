> **⚠️ SUPERSEDED SOURCE ARTIFACT — DO NOT CITE AS CURRENT.**
> This is the unedited AutoDiscussion research report, kept for provenance. It still contains
> the Hájek post-hoc replay-weighting experiment (superseded by separately trained natural/flattened checkpoints), all of which were corrected during review.
> **Current design: `paper-draft.revised.md` and `experiment-spec.md`.** See `../MAJORS.md`.

# ZW3 Which Prover Teaches Software? Mathematical Proof versus Program Verification as Post-Training Supervision

> transfer from formal proof training to software engineering capability

_Research report — 6 confirmed steps._

## Problem Definition

**input:** A single shared 0.6B–1.7B checkpoint; Lean mathematical-proof data; Dafny-style program-verification data representing states, transitions, contracts, invariants, frame conditions, and verification conditions; their staged math-proof-to-program-proof curriculum; a matched non-formal SFT control; and formal-math and software evaluation families.

**output:** Produce a transfer matrix estimating the relative effects of mathematical-proof and program-verification post-training on formal-math benchmarks and on code generation, execution reasoning, invariant inference, semantic equivalence, and program repair. Also determine whether a math-proof-to-program-proof curriculum outperforms either branch alone.

**summary:** It is unknown whether formal mathematical-proof supervision or program-verification supervision transfers more strongly to software capability under genuinely matched post-training budgets. Existing evidence does not establish transfer for either branch, and unmatched corpora, compute, search, or reporting normalizations can confound the comparison.

**objective:** Measure relative transfer at small scale, not absolute theorem-proving strength. A good result is a budget-matched, normalization-complete comparison with a valid mathematical-benchmark positive control.

**study type:** empirical

**constraints:** Use one shared checkpoint and match training tokens, optimizer steps, sampled trajectories, and accepted-trajectory counts, reporting all four normalizations despite corpus differences in length and acceptance rate. Predeclare that the math arm must win on mathematical benchmarks; otherwise it is undertrained, the comparison is void, and the study must report and stop. Evaluate against a matched non-formal SFT control.

**formal summary:** Given one shared small-scale checkpoint, matched mathematical-proof, program-verification, curriculum, and non-formal control training conditions, produce a two-branch transfer matrix and curriculum comparison, measuring relative gains across formal-math and software tasks, subject to four-way budget normalization and a predeclared math positive-control gate.

## Research Significance

**summary:** Formal-proof supervision is routinely discussed as though its transfer to software capability were established, yet the two most-cited code-transfer results are narrow or mixed, and the mature mathematical RL branch has no direct code-transfer evidence. A controlled comparison is timely because the two branches manipulate materially different semantic objects and may therefore provide different transferable capabilities.

**evidence:** FVEL improves SV-COMP only from 69 to 81 and 75 to 84 on a random 1,000-problem subset, remains far below UAutomizer's 374 solves, attributes effectiveness to dataset correlation, and gains nothing on Code2Inv at 46 to 46. Semantic-equivalence self-play gains 13.3 points only on OJ_V while DCE falls 3.2 and TVM falls 1.6, with an approximately 150-pair controlled ablation. AlphaProof uses about 80,000 TPU-days and roughly 80 million Lean problems but supplies no code-transfer evidence; RLTPF provides informal arithmetic mechanism evidence only. Novel intermediate lemmas have nevertheless proved usable as reward, raising AFP pass rate from 40.8% to 45.5% and OOD performance from 36.5% to 39.5%.

**who cares:** Researchers building small language models for theorem proving, program verification, code generation, execution reasoning, repair, and formal-reward post-training care about the result, as do teams deciding whether to invest in Lean-style theorem corpora, Dafny-style verification corpora, or staged curricula.

**why it matters:** If unmatched or selectively reported results are treated as evidence of code transfer, research programs may spend substantial training resources on the wrong formal language, curriculum, or mechanism. A negative result would be operationally decisive: equal code transfer rejects the state-transition alignment account, curriculum dominance favors decomposition, and failure against matched non-formal SFT shows that formal supervision buys nothing at this scale.

## Related Work

**summary:** Deeply compared the 8 most decisive PDF-grounded papers against our problem definition (0 candidate baselines, 0 high threats to our motivation). A further 14 cited work(s) are listed for coverage without a deep comparison (no fetchable full text, or less central than the top 8).

**general related works:**

-
  **summary:** Cited by the source draft. No openly fetchable full text, so this work is listed for coverage only and was not deeply compared against our problem.

  **work id:** 1aff47ef-e7ad-4322-bd5b-b53fc33e16ed

  **citation:** Hubert et al. Olympiad-level formal mathematical reasoning with reinforcement learning (AlphaProof). Nature 651(8106):607-613, 2026. DOI 10.1038/s41586-025-09833-y. No arXiv version exists.
-
  **summary:** Automated formal verification remains challenging for large language models because data for proof assistants and verification-aware languages is scarce, and correctness depends on satisfying precise machine-checkable specifications rather than producing plausible code. This thesis studies how verifier environments can improve LLM generation of verified programs and proofs through reinforcement learning from verifiable rewards (RLVR) and verifierguided inference-time search. First, we train open-source models in Dafny with RLVR using Group Relative Policy Optimization (GRPO) and related variants, assembling generated candidates into complete programs and scoring them with compiler and verifi

  **work id:** 87025c4e-01de-4a6b-bee0-bf6927c53b5b

  **citation:** Max Tan. Automating Formal Verification with Reinforcement Learning and Recursive Inference.
-
  **summary:** We address the problem of code generation from multi-turn execution feedback. Existing methods either generate code without feedback or use complex, hierarchical reinforcement learning to optimize multi-turn rewards. We propose a simple yet scalable approach, µCODE, that solves multi-turn code generation using only single-step rewards. Our key insight is that code generation is a one-step recoverable MDP, where the correct code can be recovered from any intermediate code state in a single turn. µCODE iteratively trains both a generator to provide code solutions conditioned on multi-turn execution feedback and a verifier to score the newly generated code. Experimental evaluations show that ou

  **work id:** fd71125c-0485-498f-967a-d65dee757d99

  **citation:** Arnav Kumar Jain et al.. Multi-Turn Code Generation Through Single-Step Rewards.
-
  **summary:** Existing code reasoning methods primarily supervise final code outputs, ignoring intermediate states, often leading to reward hacking where correct answers are obtained through inconsistent reasoning. We propose StepCodeReasoner, a framework that introduces explicit intermediate execution-state supervision. By automatically inserting structured print-based execution-trace anchors into code, the model is trained to predict runtime states at each step, transforming code reasoning into a verifiable, stepwise execution modeling problem. Building on this execution-aware method, we introduce Bi-Level GRPO, a reinforcement learning algorithm for structured credit assignment at two levels: intertraj

  **work id:** c6302e00-6cf4-4f73-8406-4bf208d6cf26

  **citation:** Hao Wang et al.. StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning.
-
  **summary:** Automated code generation with large language models has gained significant traction, but there remains no guarantee on the correctness of generated code. We aim to use formal verification to provide mathematical guarantees that the generated code is correct. However, generating formally verified code with LLMs is hindered by the scarcity of training data and the complexity of formal proofs. To tackle this challenge, we introduce AlphaVerus, a self-improving framework that bootstraps formally verified code generation by iteratively translating programs from a higher-resource language and leveraging feedback from a verifier. AlphaVerus operates in three phases: exploration of candidate transl

  **work id:** c9778a1d-acdc-46d3-bac3-467a6391ff64

  **citation:** Pranjal Aggarwal et al.. AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement.
-
  **summary:** The use of large language models for code generation is a rapidly growing trend in software development. However, without efective methods for ensuring the correctness of generated code, this trend could lead to undesirable outcomes. In this paper, we introduce a new approach for addressing this challenge: the Clover paradigm, short for Closed-Loop Verifiable Code Generation, which uses consistency checking to provide a strong filter for incorrect code. Clover performs consistency checks among code, docstrings, and formal annotations. The checker is implemented using a novel integration of formal verification tools and large language models. We provide a theoretical analysis to support our t

  **work id:** 002e7ae6-d336-426c-8f79-ad3969076c63

  **citation:** Chuyue Sun et al.. Clover: Closed-Loop Verifiable Code Generation.
-
  **summary:** Program synthesis or code generation aims to generate a program that satisfies a problem specification. Recent approaches using large-scale pretrained language models (LMs) have shown promising results, yet they have some critical limitations. In particular, they often follow a standard supervised fine-tuning procedure to train a code generation model only from the pairs of natural-language problem descriptions and ground-truth programs. Such paradigm largely ignores some important but potentially useful signals in the problem specification such as unit tests, which thus often results in poor performance when solving complex unseen coding tasks. To address the limitations, we propose “CodeRL

  **work id:** 835a9073-b884-49a6-8823-1f8061136a19

  **citation:** Hung Le et al.. CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning.
-
  **summary:** The demonstrated code-understanding capability of LLMs raises the question of whether they can be used for automated program verification, a task that demands high-level abstract reasoning about program properties that is challenging for verification tools. We propose a general methodology to combine the power of LLMs and automated reasoners for automated program verification. We formally describe this methodology as a set of transition rules and prove its soundness. We instantiate the calculus as a sound automated verification procedure and demonstrate practical improvements on a set of synthetic and competition benchmarks.

  **work id:** 790fbd0c-b8f8-4133-aa48-fd3b0ea07511

  **citation:** Haoze Wu et al.. LEMUR: INTEGRATING LARGE LANGUAGE MODELSIN AUTOMATED PROGRAM VERIFICATION.
-
  **summary:** Loop invariants are fundamental to reasoning about programs with loops. They establish properties about a given loop’s behavior. When they additionally are inductive, they become useful for the task of formal verification that seeks to establish strong mathematical guarantees about program’s runtime behavior. The inductiveness ensures that the invariants can be checked locally without consulting the entire program, thus are indispensable artifacts in a formal proof of correctness. Finding inductive loop invariants is an undecidable problem, and despite a long history of research towards practical solutions, it remains far from a solved problem. This paper investigates the capabilities of the

  **work id:** 618cc086-c826-40c4-94af-1777bf293a71

  **citation:** Adharsh Kamath et al.. Finding Inductive Loop Invariants using Large Language Models.
-
  **summary:** We introduce Goedel-Prover-V2, a series of open-source language models that set a new state-of-the-art in automated theorem proving. Built on the standard expert iteration and reinforcement learning pipeline, our approach incorporates three key innovations: (1) Scaffolded data synthesis: We generate synthetic tasks of increasing difficulty to train the model to master increasingly complex theorems; (2) Verifier-guided self-correction: We enable the model to iteratively revise its proofs by leveraging feedback from the Lean compiler; (3) Model averaging: We merge model checkpoints to mitigate the decrease in model output diversity in later stages of training. Our small model, Goedel-Prover-V2

  **work id:** 76f61bbd-105b-478c-a839-0431747cd188

  **citation:** Yong Lin et al.. GOEDEL-PROVER-V2: SCALING FORMAL THEOREM PROVING WITH SCAFFOLDED DATA SYNTHESIS AND SELF-CORRECTION.
-
  **summary:** We introduce DeepSeek-Prover-V2, an open-source large language model designed for formal theorem proving in Lean 4, with initialization data collected through a recursive theorem proving pipeline powered by DeepSeek-V3. The cold-start training procedure begins by prompting DeepSeek-V3 to decompose complex problems into a series of subgoals. The proofs of resolved subgoals are synthesized into a chain-of-thought process, combined with DeepSeek-V3’s stepby-step reasoning, to create an initial cold start for reinforcement learning. This process enables us to integrate both informal and formal mathematical reasoning into a unified model. The resulting model, DeepSeek-Prover-V2-671B, achieves sta

  **work id:** 9252ebc4-767b-4274-ab23-ce9cfa792fff

  **citation:** Z.Z. Ren et al.. DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition.
-
  **summary:** Mathematical theorem proving is an important testbed for large language models’ deep and abstract reasoning capability. This paper focuses on improving LLMs’ ability to write proofs in formal languages that permit automated proof verification/evaluation. Most previous results provide human-written lem mas to the theorem prover, which is an arguably oversimplified setting that does not sufficiently test the provers’ planning and decomposition capabilities. Instead, we work in a more natural setup where the lemmas that are directly relevant to the theorem are not given to the theorem prover at test time. We design an RL-based training algorithm that encourages the model to decompose a theorem

  **work id:** 6b3855c4-df4a-4d0e-bc85-35d8698c2f3e

  **citation:** Kefan Dong et al.. Formal Theorem Proving by Rewarding LLMs to Decompose Proofs Hierarchically.
-
  **summary:** Large Language Models excel at code generation yet struggle with complex programming tasks that demand sophisticated reasoning. To bridge this gap, traditional process supervision relies on learned reward models requiring costly training data and suffering from reward misalignment, while outcome supervision fails for complex tasks needing coordinated intermediate steps. We introduce Outcome Refining Process Supervision, which unifies process and outcome supervision by leveraging executable verification: a treestructured search framework generates strategic alternatives, profiles execution metrics, and scores candidates via self-critique mechanisms that integrate runtime feedback with reasoni

  **work id:** b9d89e5c-64b8-416d-8f7e-1d4c0fa2c4e8

  **citation:** Zhuohao Yu et al.. Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation.
-
  **summary:** The demand for synthetic data in mathematical reasoning has increased due to its potential to enhance the mathematical capabilities of large language models (LLMs). However, ensuring the validity of intermediate reasoning steps remains a significant challenge, affecting data quality. While formal verification via theorem provers effectively validates LLM reasoning, the autoformalisation of mathematical proofs remains error-prone. We introduce iterative autoformalisation, an approach that iteratively refines theorem prover formalisation to mitigate errors, thereby increasing the execution rate on the Lean prover from 60% to 87%. Building upon that, we introduce Theorem Prover as a Judge (TP-a

  **work id:** 56b7ded9-31aa-405c-9f3a-f4fb459021a5

  **citation:** Joshua Ong Jun Leang et al.. Theorem Prover as a Judge for Synthetic Data Generation.

**specific related works:**

-
  **input:** A set of code implementations c; Dafny function signatures and program bodies with annotations missing

  **output:** Full Dafny code implementations with corresponding formal specifications y; Preconditions, postconditions, loop invariants, assert statements, and other applicable annotations

  **summary:** Existing informal language-based (e.g., human language) Large Language Models (LLMs) trained with Reinforcement Learning (RL) face a significant challenge: their verification processes, which provide crucial training signals, are neither reliable nor scalable. In fact, the prevalent large proprietary models could hardly generate verifiable programs. A promising yet largely uncharted alternative is formal language-based reasoning. Grounding LLMs in rigorous formal systems where generative models operate in formal language spaces (e.g., Dafny) enables the automatic and mathematically provable verification of their reasoning processes and outcomes. This capability is pivotal for achieving large-scale, reliable formal software verification. It is a common practice to employ human-annotated chain-of-thought and answers to induce the reasoning and coding capabilities of LLMs. Unfortunately, it becomes unacceptably all-consuming to provide such priors for supervising complex programming tasks. In this work, we systematically explore ways to reduce human annotations with the formal language, Dafny, as the main environment for our pilot study. Our pipeline mainly relies on introducing an automatic and scalable data curation pipeline, and careful RL designs integrated with feedback from the formal language verifier. We introduce DafnyComp, a benchmark of compositional formal programs with auto-formalized specifications for specification reasoning. Our supervised fine-tuning (SFT) stage enables even small models (e.g., 0.5B) to generate syntactically valid and verifiable Dafny code, surpassing proprietary models. RL with regularization further improves performance, achieving stronger generalization to out-of-domain tasks and outperforming all strong baselines on the challenging DafnyComp benchmark. Anonymized code and models are available at https://github. com/Veri-Code/ReForm and https://huggingface.co/Veri-Code.

  **work id:** 53771d70-a113-4e78-881c-64cbf7860558

  **approach:** Re:Form combines automated data curation, a compositional benchmark, limited CoT-free supervised fine-tuning, and verifier-guided reinforcement learning with syntax, verification, and subset rewards plus policy regularization.

  **citation:** Chuanhao Yan et al.. Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the transfer question — whether Lean math-proof vs Dafny-style verification supervision differentially improves downstream software capabilities under matched tokens, steps, sampled and accepted trajectories — nor do they include a formal-math positive control or a matched non-formal SFT control, so their single-branch RL results cannot adjudicate relative transfer or curriculum ordering.

  **method addresses:** false

  **method rationale:** Their pipeline optimizes Dafny specification-generation quality via RL, but it does not construct a budget-matched comparison between mathematical-proof and program-verification supervision, nor measure transfer to a software capability suite with a math positive control.

  **problem alignment:** related

  **alignment rationale:** They generate verifiable Dafny programs from code implementations, whereas we study whether formal-proof vs program-verification supervision transfers to broad software capability under budget-matched post-training on a shared checkpoint.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] They never pose the transfer question — whether Lean math-proof vs Dafny-style verification supervision differentially improves downstream software capabilities under matched tokens, steps, sampled and accepted trajectories — nor do they include a formal-math positive control or a matched non-formal SFT control, so their single-branch RL results cannot adjudicate relative transfer or curriculum ordering.

    **limitation id:** lim-1

    **evidence for limitation:** They generate verifiable Dafny programs from code implementations, whereas we study whether formal-proof vs program-verification supervision transfers to broad software capability under budget-matched post-training on a shared checkpoint. | Their pipeline optimizes Dafny specification-generation quality via RL, but it does not construct a budget-matched comparison between mathematical-proof and program-verification supervision, nor measure transfer to a software capability suite with a math positive control.

  **is potential baseline:** false
-
  **input:** A dataset D of reference Haskell programs; A base language model used for Alice and Bob; A reference Haskell program P selected for each self-play round

  **output:** A fine-tuned generator that produces challenging semantically equivalent or inequivalent Haskell program variants; A fine-tuned evaluator that judges whether two programs are semantically equivalent

  **summary:**

  We introduce a self-play framework for semantic equivalence in Haskell, utilizing formal verification to guide adversarial training between a generator and an evaluator. The framework leverages Liquid Haskell proofs for validating equivalence and execution-based counterexamples for inequivalence, organized via a difficulty-aware curriculum. To facilitate this, we release OpInstruct-HSx, a synthetic dataset of ≈28k validated Haskell programs. Empirical experiments show that our evaluator transfers effectively to downstream tasks, achieving up to 13.3pp accuracy gain on EquiBench and consistent gains on PySecDB. Ablation studies on the SEQ-SINQ regimes indicate that while inequivalence supervision provides data volume, equivalence proofs are uniquely responsible for the model's reasoning capabilities. The entire training pipeline and dataset are publicly released on GitHub and Hugging Face respectively.

  We propose a self-play framework for semantic equivalence, in which two specialized agents interact: Alice, a generator that produces variants of reference programs; and Bob, an evaluator trained to decide whether two programs are equivalent. The self-play loop alternates between program generation, verification through proofs or counterexamples, difficulty scoring, and fine-tuning of both agents. By framing the problem as a game between generator and evaluator, the system encourages progressively harder examples and deeper reasoning about semantics.

  **work id:** 8ac1ff3e-c13f-49c8-be5a-32ca0dbc8b08

  **approach:** Alice generates equivalent or inequivalent variants of reference Haskell programs, external verification accepts valid proofs or counterexamples, Bob judges equivalence and supplies difficulty scores, and difficulty-aware supervised fine-tuning updates the agents.

  **citation:** Antonio Valerio Miceli Barone & Poon Tsz Nok. Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether mathematical-proof supervision (e.g., Lean) versus program-verification supervision transfers more strongly to software capability under matched training tokens, optimizer steps, sampled trajectories, and accepted-trajectory counts, so budget-matched relative transfer with a predeclared math positive control and a staged math-proof-to-program-proof curriculum is left entirely unmeasured. Their single verification branch (Liquid Haskell equivalence) and unmatched, acceptance-yield-uncontrolled corpus cannot isolate transfer effects across our broader evaluation families (code generation, execution reasoning, invariant inference, semantic equivalence, program repair).

  **method addresses:** false

  **method rationale:** Their self-play SFT pipeline produces a stronger equivalence generator/evaluator but does not compare formal-math-proof versus program-verification supervision under matched token/step/trajectory/acceptance budgets on a shared small checkpoint, so it cannot answer our relative-transfer question or supply the predeclared mathematical positive control.

  **problem alignment:** related

  **alignment rationale:** Both study whether formal-verification supervision improves code reasoning, but their goal is training generator/evaluator agents for Haskell semantic equivalence, whereas ours is a budget-matched comparison of transfer from mathematical-proof versus program-verification supervision across a broad software-capability matrix.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether mathematical-proof supervision (e.g., Lean) versus program-verification supervision transfers more strongly to software capability under matched training tokens, optimizer steps, sampled trajectories, and accepted-trajectory counts, so budget-matched relative transfer with a predeclared math positive control and a staged math-proof-to-program-proof curriculum is left entirely unmeasured. Their single verification branch (Liquid Haskell equivalence) and unmatched, acceptance-yield-uncontrolled corpus cannot isolate transfer effects across our broader evaluation families (code generation, execution reasoning, invariant inference, semantic equivalence, program repair).

    **limitation id:** lim-1

    **evidence for limitation:** Both study whether formal-verification supervision improves code reasoning, but their goal is training generator/evaluator agents for Haskell semantic equivalence, whereas ours is a budget-matched comparison of transfer from mathematical-proof versus program-verification supervision across a broad software-capability matrix. | Their self-play SFT pipeline produces a stronger equivalence generator/evaluator but does not compare formal-math-proof versus program-verification supervision under matched token/step/trajectory/acceptance budgets on a shared small checkpoint, so it cannot answer our relative-transfer question or supply the predeclared mathematical positive control.

  **is potential baseline:** false
-
  **input:** formal theorem statements in Lean 4; the Lean 4 proof environment and available premises and tactics

  **output:** complete Lean 4 proof code verified as correct by the Lean prover; diverse valid proof paths discovered through tree search

  **summary:** We introduce DeepSeek-Prover-V1.5, an open-source language model designed for theorem proving in Lean 4, which enhances DeepSeek-Prover-V1 by optimizing both training and inference processes. Pre-trained on DeepSeekMath-Base with specialization in formal mathematical languages, the model undergoes supervised fine-tuning using an enhanced formal theorem proving dataset derived from DeepSeek-Prover-V1. Further refinement is achieved through reinforcement learning from proof assistant feedback (RLPAF). Beyond the single-pass whole-proof generation approach of DeepSeek-Prover-V1, we propose RMaxTS, a variant of Monte-Carlo tree search that employs an intrinsic-reward-driven exploration strategy to generate diverse proof paths. DeepSeek-Prover-V1.5 demonstrates significant improvements over DeepSeek-Prover-V1, achieving new state-of-the-art results on the test set of the high school level miniF2F benchmark (63.5%) and the undergraduate level ProofNet benchmark (25.3%).

  **work id:** 41f8582d-1d09-453e-bac4-4cfc7d088ebb

  **approach:** DeepSeek-Prover-V1.5 combines formal-language pre-training, augmented supervised fine-tuning, reinforcement learning from Lean feedback, and an intrinsic-reward-driven Monte-Carlo tree search based on truncate-and-resume proof generation.

  **citation:** Huajian Xin et al.. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of comparative downstream transfer under matched post-training budgets: program-verification supervision is entirely absent, and no controls for tokens, optimizer steps, sampled/accepted trajectories, or a non-formal SFT baseline are established, so relative transfer of math-proof vs. program-proof supervision to software capability remains unmeasured.

  **method addresses:** false

  **method rationale:** Their pipeline optimizes a single Lean-proving arm with RL and tree search and neither includes a program-verification (Dafny-style) branch, a matched non-formal control, budget normalizations, nor any measurement of transfer to code/execution/invariant/repair tasks, so it cannot produce our transfer matrix.

  **problem alignment:** related

  **alignment rationale:** Both operate on Lean 4 formal-proof generation, but their objective is maximizing absolute theorem-proving accuracy on one branch, whereas ours is a budget-matched comparison of transfer from math-proof vs. program-verification supervision to software capabilities.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of comparative downstream transfer under matched post-training budgets: program-verification supervision is entirely absent, and no controls for tokens, optimizer steps, sampled/accepted trajectories, or a non-formal SFT baseline are established, so relative transfer of math-proof vs. program-proof supervision to software capability remains unmeasured.

    **limitation id:** lim-1

    **evidence for limitation:** Both operate on Lean 4 formal-proof generation, but their objective is maximizing absolute theorem-proving accuracy on one branch, whereas ours is a budget-matched comparison of transfer from math-proof vs. program-verification supervision to software capabilities. | Their pipeline optimizes a single Lean-proving arm with RL and tree search and neither includes a program-verification (Dafny-style) branch, a matched non-formal control, budget normalizations, nor any measurement of transfer to code/execution/invariant/repair tasks, so it cannot produce our transfer matrix.

  **is potential baseline:** false
-
  **input:** A C program with a single loop; The loop pre-condition; The loop condition and body; A post-loop assertion or post-condition

  **output:** A set of inductive loop invariants; A formally verified proof of the post-loop assertion

  **summary:** We propose a novel framework that provides constructive feedback to an LLM in the “guess-and-check” paradigm by formally verifying its own thinking process and detecting local reasoning errors. We apply this framework to the loop invariant synthesis problem. We prompt the model to produce a step-by-step natural language proof justifying its thinking process for the failed verification condition of its generated loop invariants. Then, we use an LLM to translate the reasoning steps into first-order logic implications, which can be checked automatically. An invalid implication pinpoints the exact logical flaw in the LLM’s thinking process, which we then use to construct targeted feedback for refinement. We have implemented our approach in a tool called LORIS and evaluated it on a main benchmark suite of 460 C programs and an additional benchmark suite of 50 C programs each of which involves non-linear properties. On the main benchmark suite, LORIS solved 445 of the programs, and achieved an overall success rate of 93.1%. LORIS also demonstrates robustness on the challenging non-linear benchmark suite.

  **work id:** fc8ff69f-67b3-4354-a676-a6135501fd36

  **approach:** LORIS iteratively generates candidate invariants, checks their verification conditions, obtains a structured proof for a failed condition, formalizes and checks local reasoning implications, and returns targeted errors to refine the invariants.

  **citation:** Tianchi Li et al.. Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether formal-verification supervision transfers to broader software capability, nor do they compare it against mathematical-proof supervision under matched training-token/step/trajectory budgets; invariant synthesis in their work is an evaluation target, not a supervision source whose transfer is measured.

  **method addresses:** false

  **method rationale:** Their Synthesizer/Formalizer/Frama-C feedback pipeline is a prompting-and-verification agent for one task and contains no post-training, budget-matching, or cross-branch transfer comparison, so it cannot produce our transfer matrix or curriculum comparison.

  **problem alignment:** different

  **alignment rationale:** Their problem is inference-time synthesis of loop invariants for single-loop C programs via an LLM guess-and-check loop, whereas ours is a post-training transfer study measuring whether math-proof vs program-verification supervision improves software capability under matched budgets.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether formal-verification supervision transfers to broader software capability, nor do they compare it against mathematical-proof supervision under matched training-token/step/trajectory budgets; invariant synthesis in their work is an evaluation target, not a supervision source whose transfer is measured.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem is inference-time synthesis of loop invariants for single-loop C programs via an LLM guess-and-check loop, whereas ours is a post-training transfer study measuring whether math-proof vs program-verification supervision improves software capability under matched budgets. | Their Synthesizer/Formalizer/Frama-C feedback pipeline is a prompting-and-verification agent for one task and contains no post-training, budget-matching, or cross-branch transfer comparison, so it cannot produce our transfer matrix or curriculum comparison.

  **is potential baseline:** false
-
  **input:** natural language specifications

  **output:** FPGA-ready RTL IP cores; timing and resource utilization reports

  **summary:** Large Language Models (LLMs) have demonstrated impressive capabilities in automated code generation but frequently produce code that fails formal verification, an essential requirement for hardware and safety-critical domains. To overcome this fundamental limitation, we previously proposed PREFACE, a model-agnostic framework based on reinforcement learning (RL) that iteratively repairs the prompts provided to frozen LLMs, systematically steering them toward generating formally verifiable Dafny code without costly fine-tuning. This work presents Proof2Silicon, a novel end-to-end synthesis framework that embeds the previously proposed PREFACE flow to enable the generation of correctness-by-construction hardware directly from natural language specifications. Proof2Silicon operates by: (1) leveraging PREFACE’s verifier-driven RL agent to optimize prompt generation iteratively, ensuring Dafny code correctness; (2) automatically translating verified Dafny programs into synthesizable high-level C using Dafny’s Python backend and PyLog; and (3) employing Vivado HLS to produce RTL implementations. Evaluated rigorously on a challenging 100- task benchmark, PREFACE’s RL-guided prompt optimization consistently improved Dafny verification success rates across diverse LLMs by up to 21%. Crucially, Proof2Silicon achieved an end-to-end hardware synthesis success rate of up to 72%, generating RTL designs through Vivado HLS synthesis flows. These results demonstrate a robust, scalable, and automated pipeline for LLM-driven, formally verified hardware synthesis, bridging natural-language specification and silicon realization.

  **work id:** bd32b1a5-8dae-4c66-9d05-0db937c8601d

  **approach:** Proof2Silicon couples PREFACE's verifier-guided RL prompt repair with Dafny verification, Python sanitization, PyLog HLS-C generation, and Vivado HLS synthesis.

  **citation:** (unknown authors). Proof2Silicon: Prompt Repair for Verified Code and Hardware Generation via Reinforcement Learning.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose the question of whether formal-proof supervision transfers to general software capability, nor do they compare proof supervision against program-verification supervision under matched post-training budgets; consequently, budget-matched, normalization-complete measurement of transfer with a valid mathematical-benchmark positive control is entirely absent from their framing.

  **method addresses:** false

  **method rationale:** An RL prompt-repair agent steering a frozen LLM plus a Dafny-to-RTL toolchain neither performs post-training of a shared checkpoint nor measures cross-domain transfer under matched token/step/trajectory normalizations, so it cannot produce our transfer matrix or positive-control comparison.

  **problem alignment:** different

  **alignment rationale:** Their goal is a verifier-guided prompt-refinement pipeline that turns NL specs into verified Dafny and synthesizable RTL hardware, whereas ours is a budget-matched measurement of how math-proof versus program-verification post-training transfers to software capability in a shared small checkpoint.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose the question of whether formal-proof supervision transfers to general software capability, nor do they compare proof supervision against program-verification supervision under matched post-training budgets; consequently, budget-matched, normalization-complete measurement of transfer with a valid mathematical-benchmark positive control is entirely absent from their framing.

    **limitation id:** lim-1

    **evidence for limitation:** Their goal is a verifier-guided prompt-refinement pipeline that turns NL specs into verified Dafny and synthesizable RTL hardware, whereas ours is a budget-matched measurement of how math-proof versus program-verification post-training transfers to software capability in a shared small checkpoint. | An RL prompt-repair agent steering a frozen LLM plus a Dafny-to-RTL toolchain neither performs post-training of a shared checkpoint nor measures cross-domain transfer under matched token/step/trajectory normalizations, so it cannot produce our transfer matrix or positive-control comparison.

  **is potential baseline:** false
-
  **input:** C code to be verified; corresponding SIMPL and/or Isabelle content supplied as optional supplements; program specifications such as assertions, safety requirements, or overflow requirements

  **output:** a code-verification result of success or failure; intermediate proof states; prover messages and error information

  **summary:** Formal verification (FV) has witnessed growing significance with current emerging program synthesis by the evolving large language models (LLMs). However, current formal verification mainly resorts to symbolic verifiers or hand-craft rules, resulting in limitations for extensive and flexible verification. On the other hand, formal languages for automated theorem proving, such as Isabelle, as another line of rigorous verification, are maintained with comprehensive rules and theorems. In this paper, we propose FVEL³, an interactive Formal Verification Environment with LLMs. Specifically, FVEL transforms a given code to be verified into Isabelle, and then conducts verification via neural automated theorem proving with an LLM. The joined paradigm leverages the rigorous yet abundant formulated and organized rules in Isabelle and is also convenient for introducing and adjusting cutting-edge LLMs. To achieve this goal, we extract a large-scale FVELER³. The FVELER dataset includes code dependencies and verification processes that are formulated in Isabelle, containing 758 theories, 29,125 lemmas, and 200,646 proof steps in total with in-depth dependencies. We benchmark FVELER in the FVEL environment by first fine-tuning LLMs with FVELER and then evaluating them on Code2Inv and SV-COMP. The results show that FVEL with FVELER fine-tuned Llama3- 8B solves 17.39% (69→81) more problems, and Mistral-7B 12% (75→84) more problems in SV-COMP. And the proportion of proof errors is reduced. Project page: https://fveler.github.io/.

  **work id:** b1e4b95f-24c5-462a-b647-6ea101315e2b

  **approach:** FVEL transforms C code into Isabelle facts, asks an LLM to formulate a lemma and generate proof steps, and uses an Isabelle prover through PISA to return feedback and validate the completed proof. FVELER supplies theory dependencies and step-wise proof data for fine-tuning and evaluation.

  **citation:** Xiaohan Lin et al.. FVEL: Interactive Formal Verification Environment with Large Language Models via Theorem Proving.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** The comparative question of whether formal-math-proof supervision versus program-verification supervision transfers more strongly to general software capability under matched token/step/trajectory/acceptance budgets is never posed; FVEL fine-tunes on a single verification corpus and reports only verification pass counts, with no matched control, no math positive-control gate, and no transfer matrix over code generation, invariant inference, equivalence, and repair.

  **method addresses:** false

  **method rationale:** Their pipeline produces a code-verification success/failure result and fine-tunes on one formal corpus; it neither controls training budgets across arms nor measures cross-domain transfer to code generation, execution reasoning, repair, or formal-math benchmarks, so it cannot answer our comparative-transfer question.

  **problem alignment:** different

  **alignment rationale:** FVEL builds a tool that verifies C programs by translating them to Isabelle and generating LLM proofs, whereas our problem is a budget-matched measurement of whether math-proof vs program-verification post-training transfers to broad software capability.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] The comparative question of whether formal-math-proof supervision versus program-verification supervision transfers more strongly to general software capability under matched token/step/trajectory/acceptance budgets is never posed; FVEL fine-tunes on a single verification corpus and reports only verification pass counts, with no matched control, no math positive-control gate, and no transfer matrix over code generation, invariant inference, equivalence, and repair.

    **limitation id:** lim-1

    **evidence for limitation:** FVEL builds a tool that verifies C programs by translating them to Isabelle and generating LLM proofs, whereas our problem is a budget-matched measurement of whether math-proof vs program-verification post-training transfers to broad software capability. | Their pipeline produces a code-verification success/failure result and fine-tunes on one formal corpus; it neither controls training budgets across arms nor measures cross-domain transfer to code generation, execution reasoning, repair, or formal-math benchmarks, so it cannot answer our comparative-transfer question.

  **is potential baseline:** false
-
  **input:** A pretrained code LLM; Executable programs paired with concrete inputs; Code-generation problems paired with unit tests

  **output:** A post-trained code LLM with improved execution reasoning; Predictions of intermediate control flow, variable values and types, and final program outputs; Generated programs that pass functional unit tests

  **summary:** Code LLMs still struggle with code execution reasoning, especially in smaller models. Existing methods rely on supervised fine-tuning (SFT) with teacher-generated explanations, pri marily in two forms: (1) input–output (I/O) prediction chains and (2) natural-language descriptions of execution traces. However, intermediate execution steps cannot be explicitly verified during SFT, so the training objective can be reduced to merely matching teacher explanations. Moreover, training data is typically collected without explicit control over task difficulty. We introduce ExecVerify, which goes beyond text imitation by incorporating verifi able white-box rewards derived from execution traces, including next-statement prediction and variable value/type prediction. Our work first builds a dataset with multiple difficulty levels via constraint-based program synthesis. Then, we apply reinforcement learning (RL) to re ward correct answers about both intermediate execution steps and final outputs, aligning the training objective with semantic correctness at each execution step. Finally, we adopt a twostage training pipeline that first enhances execution reasoning and then transfers to code generation. Experiments demonstrate that a 7B model trained with ExecVerify achieves performance comparable to 32B models on code reasoning benchmarks and improves pass@1 by up to 5.9% on code generation tasks over strong post-training baselines<sup>1</sup>.

  **work id:** 6c4633d1-0d32-4d80-866f-c0a3fa680bda

  **approach:** ExecVerify combines constraint-based curriculum data synthesis with a two-stage post-training pipeline using interpreter-derived white-box rewards for execution reasoning and unit-test rewards for code generation.

  **citation:** Lingxiao Tang et al.. ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** They never pose whether formal mathematical-proof supervision versus program-verification supervision transfers more strongly to software capability, and they impose no budget matching across tokens/steps/sampled/accepted trajectories nor a predeclared math positive control, so the confounded-comparison question central to our problem is entirely outside their framing.

  **method addresses:** false

  **method rationale:** Their two-stage white-box RL pipeline neither includes formal-proof (Lean) or program-verification (Dafny-style contracts/invariants) supervision nor imposes any matched-budget normalization or math-positive-control design, so it cannot answer which formal supervision branch transfers more under matched budgets.

  **problem alignment:** different

  **alignment rationale:** They post-train a code LLM for execution reasoning and functional code generation via RL, whereas we run a budget-matched comparison of formal mathematical-proof vs. program-verification supervision to measure relative transfer to software capability.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] They never pose whether formal mathematical-proof supervision versus program-verification supervision transfers more strongly to software capability, and they impose no budget matching across tokens/steps/sampled/accepted trajectories nor a predeclared math positive control, so the confounded-comparison question central to our problem is entirely outside their framing.

    **limitation id:** lim-1

    **evidence for limitation:** They post-train a code LLM for execution reasoning and functional code generation via RL, whereas we run a budget-matched comparison of formal mathematical-proof vs. program-verification supervision to measure relative transfer to software capability. | Their two-stage white-box RL pipeline neither includes formal-proof (Lean) or program-verification (Dafny-style contracts/invariants) supervision nor imposes any matched-budget normalization or math-positive-control design, so it cannot answer which formal supervision branch transfers more under matched budgets.

  **is potential baseline:** false
-
  **input:** A natural-language programming problem description; Public test cases; Execution feedback from previous code solutions, including passed and failed tests, syntax errors, and runtime errors

  **output:** A final Python code solution

  **summary:** Large language models (LLMs) deployed as agents solve user-specified tasks over multiple steps while keeping the required manual engagement to a minimum. Crucially, such LLMs need to ground their generations in any feedback obtained to reliably achieve the desired outcomes. We propose an end-to-end reinforcement learning method for teaching models to leverage execution feedback in the realm of code synthesis, where state-of-the-art LLMs struggle to improve code iteratively compared to independent sampling. We benchmark on competitive programming tasks, where we achieve new state-of-the-art results with both small (8B parameters) and large (70B) models while reducing the amount of samples required by an order of magnitude. Our analysis of inference-time behavior demonstrates that our method produces LLMs that effectively leverage automatic feedback over multiple steps.

  **work id:** ed042595-d330-4228-9803-b89b144fe924

  **approach:** RLEF represents iterative code synthesis as a partially observable decision process and uses PPO to train an LLM to revise code using textual execution feedback, with public tests exposed during interaction and private tests used for final correctness rewards.

  **citation:** Jonas Gehring et al.. RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** RLEF never poses the question of whether formal mathematical-proof supervision versus program-verification supervision transfers differently to software capability, and it uses natural-language-plus-execution-reward training rather than formal proof/verification signals under matched token/step/trajectory/acceptance budgets. It therefore does not address measuring relative transfer of formal supervision types with a mathematical-benchmark positive control.

  **method addresses:** false

  **method rationale:** RLEF is an RL-from-execution-feedback training procedure for producing better code solutions; it neither implements formal-proof/verification supervision nor a budget-matched transfer comparison across supervision types, which is the actual object of our study.

  **problem alignment:** different

  **alignment rationale:** Their problem optimizes a single LLM for iterative code synthesis via RL from execution feedback, whereas ours is a budget-matched scientific comparison of whether formal-math-proof vs. program-verification supervision transfers more to broad software capability.

  **threat to motivation:** none

  **limitations:**

  -
    **description:** [not_considered] RLEF never poses the question of whether formal mathematical-proof supervision versus program-verification supervision transfers differently to software capability, and it uses natural-language-plus-execution-reward training rather than formal proof/verification signals under matched token/step/trajectory/acceptance budgets. It therefore does not address measuring relative transfer of formal supervision types with a mathematical-benchmark positive control.

    **limitation id:** lim-1

    **evidence for limitation:** Their problem optimizes a single LLM for iterative code synthesis via RL from execution feedback, whereas ours is a budget-matched scientific comparison of whether formal-math-proof vs. program-verification supervision transfers more to broad software capability. | RLEF is an RL-from-execution-feedback training procedure for producing better code solutions; it neither implements formal-proof/verification supervision nor a budget-matched transfer comparison across supervision types, which is the actual object of our study.

  **is potential baseline:** false

## Sub-Problems

**summary:** Completing the problem requires a causally matched comparison of supervision arms, a validity-gated transfer matrix, and a controlled test of the staged curriculum. Prior work closes none of these components because it does not pose the matched comparative-transfer question.

**sub problems:**

-
  **description:** The unresolved problem is comparing Lean, Dafny-style, and matched non-formal SFT arms from a shared checkpoint under tokens, optimizer steps, sampled trajectories, and accepted trajectories.

  **sub problem id:** sp-1

  **technical challenge:** Different sequence lengths and acceptance rates can make the four normalizations incompatible, forcing principled choices between matching and reporting them.

  **why it is a problem:** Without this matching, corpus length and acceptance yield can masquerade as differences in software transfer and misdirect training investment.

  **source limitation ids:** - lim-1
-
  **description:** Arm effects remain unestablished across formal math, code generation, execution reasoning, invariant inference, semantic equivalence, and repair under the mathematical positive-control stopping rule.

  **sub problem id:** sp-2

  **technical challenge:** Evaluation families require comparable effect estimates despite heterogeneous metrics, and the study must stop rather than reinterpret results if the math arm fails its benchmark control.

  **why it is a problem:** This matrix is necessary to distinguish genuine cross-domain transfer from branch-specific gains, while the gate prevents an undertrained math arm from invalidating the comparison.

  **source limitation ids:** - lim-1
-
  **description:** Whether a matched math-proof-to-program-proof curriculum outperforms both single-branch arms and the non-formal control remains unknown.

  **sub problem id:** sp-3

  **technical challenge:** Stage allocation must preserve the same budget normalizations while separating an ordering effect from merely receiving a mixture of two supervision sources.

  **why it is a problem:** Prior work does not establish whether staging adds an ordering benefit beyond single-branch or mixed supervision, leaving the choice between combined investment and one formal language unresolved.

  **source limitation ids:** - lim-1

**internal reasoning:**

**required components:**

-
  **name:** Budget-matched arm comparison

  **note:** No prior study compares Lean, Dafny-style, and non-formal supervision from one checkpoint while matching and reporting all four budget normalizations.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Validity-gated transfer matrix

  **note:** Prior work does not combine the full formal-math and software evaluation matrix with the predeclared mathematical positive-control gate.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Staged curriculum comparison

  **note:** No cited study tests whether math-proof-to-program-proof staging outperforms either supervision branch alone under matched budgets.

  **status:** unsolved

  **covered by limitation ids:** - lim-1

## Method Design

**methods:**

-
  **method id:** m-1

  **hypotheses:**

  - Maximum pairwise imbalance across N, K, T, and S will be ≤1% and at least 80% lower than under equal-update-only scheduling.
  - For every arm contrast on the Paired Evaluation Panel, inverse-replay-weighted and unweighted mean effects will differ by <0.05 on the win-minus-loss scale.

  **key insight:** Capping all arms at the common feasible budget intersection makes otherwise incompatible sequence-length and acceptance-rate normalizations simultaneously enforceable without equating branch-specific verifier semantics.

  **proposed approach:** From one checkpoint, train Lean, Dafny, and matched non-formal verified-response SFT arms under the shared Budget Ledger: each samples N candidates, retains K checker-passing trajectories within base-model success-propensity and length strata, and uses deterministic packing and replay to supply exactly T loss-bearing tokens over S updates. Fix N, K, T, and S at the largest common feasible intersection estimated on a disjoint blinded pilot, define the checkers ex ante, and evaluate every arm on the shared Paired Evaluation Panel while reporting acceptance yield and replay multiplicity.

  **target sub problem id:** sp-1
-
  **method id:** m-2

  **hypotheses:**

  - The Lean arm's formal-math W relative to non-formal SFT will be ≥0.10, with its one-sided 95% lower confidence bound exceeding 0.05.
  - Conditional on passing the gate, the Dafny arm will exceed the Lean arm by ≥0.05 in equal-weight mean W across code generation, execution reasoning, invariant inference, semantic equivalence, and repair.

  **key insight:** Paired win-minus-loss effects provide a common bounded estimand without assuming commensurate metric units, while the unopened-endpoint gate prevents a failed treatment manipulation from being rescued post hoc.

  **proposed approach:** On the shared Paired Evaluation Panel and Budget Ledger arms, retain each benchmark's native metric but form matrix entries as paired win-minus-loss effects, W = P(arm score > control score) − P(arm score < control score), with equal benchmark weights within families and item-by-seed stratified bootstrap intervals. Before opening software-family results, require the Lean-versus-non-formal formal-math positive control to have a one-sided 95% lower confidence bound for W above 0.05; otherwise stop confirmatory analysis and label the unreinterpreted matrix diagnostic.

  **target sub problem id:** sp-2
-
  **method id:** m-3

  **hypotheses:**

  - Lean→Dafny will exceed the best of Lean-only, Dafny-only, and non-formal SFT by ≥0.05 in equal-weight software-family W, with a simultaneous 95% lower confidence bound above zero.
  - Lean→Dafny will exceed both Dafny→Lean and interleaved training by ≥0.03 in equal-weight software-family W.

  **key insight:** Equal source quotas remove composition as an explanation, leaving temporal presentation order as the sole systematic difference among the three mixed-supervision arms.

  **proposed approach:** Using the shared Budget Ledger and Paired Evaluation Panel, compare 50:50 Lean→Dafny, Dafny→Lean, and minibatch-interleaved Lean+Dafny curricula with segmented Lean-only, Dafny-only, and non-formal controls; every half receives T/2 tokens, S/2 updates, N/2 samples, and K/2 accepted trajectories, with the same uninterrupted optimizer-state policy. The reverse and interleaved arms hold source exposure fixed, so their contrasts with Lean→Dafny identify ordering rather than mixture effects.

  **target sub problem id:** sp-3

**summary:** Use a shared Budget Ledger that records loss-bearing tokens, optimizer updates, sampled candidates, and unique validator-accepted trajectories, plus a frozen Paired Evaluation Panel spanning all six outcome families. Hard budget quotas identify supervision effects, paired scale-free estimates handle heterogeneous metrics, and reverse-order and interleaved controls isolate curriculum ordering.

## Experiment Design

**summary:** The evaluation estimates a budget-normalized branch-by-outcome transfer matrix from a shared checkpoint using paired, externally checked outcomes across formal mathematics and five software-task families. Confirmatory tests assess normalization completeness, replay-weight robustness, mathematical positive-control sensitivity, per-family and aggregate cross-domain transfer, and curriculum-order effects; all training arms use matched sampled candidates, accepted trajectories, tokens, and optimizer updates. Cross-run inference uses few-cluster-robust procedures because training-seed variability is part of the estimand.

**datasets:**

-
  **name:** Budget and Replay Ledger

  **justification:** Exact per-arm records of sampled candidates, accepted trajectories, tokens, optimizer updates, and per-example replay counts/probabilities expose normalization failures and replay-induced effect distortion. The ledger is written once per training step from the trainer's data loader and sampler state; replay probability for a training example is defined as its empirical selection frequency across the arm's optimizer updates, and these are the sole inputs to the rq-2 stabilized weights.
-
  **name:** Formal-Math Positive-Control Panel

  **justification:** A contamination-screened, dependency-disjoint Lean panel drawn from established theorem-proving task styles provides a valid mathematical benchmark on which proof post-training should produce detectable transfer. Contamination screening removes any theorem whose statement or proof shares a normalized (whitespace- and identifier-canonicalized) n-gram fingerprint (n=13) with the training pool or the shared-checkpoint pretraining shards; dependency-disjointness is enforced by partitioning theorems on their Lean import/dependency graph so that no evaluation theorem imports or is imported by any training theorem. Source is a pinned Lean/mathlib release tag recorded in the panel manifest, with exact-hash deduplication applied before sampling.
-
  **name:** Paired Software-Family Panel

  **justification:** Balanced code-generation, execution-reasoning, invariant-inference, semantic-equivalence, and repair tasks stress whether the estimator distinguishes domain-specific transfer without allowing a large family to dominate. Each family is drawn from a pinned, versioned source snapshot recorded in a manifest (source name, commit/release hash, extraction date); prompts are exact-hash and near-duplicate (MinHash Jaccard ≥0.8) deduplicated within and across families, and every prompt carries an executable or verifiable oracle so wins are externally checked rather than model-judged.
-
  **name:** Curriculum-Order Panel

  **justification:** Frozen disjoint software-family splits with external execution or verification oracles isolate curriculum order while preventing evaluation reuse from driving the comparison. Disjointness across the rq-4, rq-5, and rq-6 panels is constructed by hashing each prompt to a stable ID and assigning IDs to at most one panel via a fixed partition function seeded once and frozen in the manifest; the frozen split file (prompt IDs, family labels, oracle references) is version-pinned so all arms and seeds see identical, non-overlapping evaluation sets.

**baselines:**

-
  **name:** Matched non-formal SFT

  **justification:** Controls for generic supervised post-training while matching the complete four-axis budget. It is the shared reference arm against which the full transfer matrix (formal math plus each of the five software families) is estimated.
-
  **name:** Equal-update-only scheduling

  **justification:** Sanity-checks whether matching optimizer updates alone leaves material token and trajectory imbalance.
-
  **name:** Shared checkpoint without post-training

  **justification:** Provides a zero-exposure anchor for detecting trivial or sign-inverted transfer estimates.
-
  **name:** Single-branch arms

  **justification:** Lean-only and Dafny-only identify whether a measured curriculum effect requires both branches.
-
  **name:** Reverse and interleaved curricula

  **justification:** Hold branch exposure fixed while testing sensitivity specifically to curriculum order.

**research questions:**

-
  **tier:** mechanism

  **rq id:** rq-1

  **setup:** Run all six arms from the shared checkpoint under normalization-complete and equal-update-only scheduling, with 8 independent scheduling/training seeds per arm and scheduler (96 runs). Using the method_design definitions, let N be sampled candidates, K be accepted trajectories, T be training tokens, and S be optimizer updates. For each seed, compute the maximum pairwise relative arm imbalance over all four quantities; compare schedulers using joint one-sided bootstrap bounds.

  **metrics:** Maximum over N (sampled candidates), K (accepted trajectories), T (tokens), and S (optimizer updates) of |arm_i-arm_j| divided by their pairwise mean, plus the ratio of this maximum between schedulers.

  **description:** Does four-axis budget matching reproducibly control cross-arm exposure imbalance better than equal-update-only scheduling?

  **expected outcome:** The normalized scheduler has maximum imbalance ≤0.01, and its imbalance is no more than 20% of the equal-update-only value.

  **statistical test:** Intersection-union variance-bound test using seed-stratified bootstrap 95% upper bounds at family-wise α=0.05 for normalized imbalance ≤0.01 and the normalized/equal-update imbalance ratio ≤0.20.

  **target hypotheses:** - Maximum pairwise imbalance across N, K, T, and S will be ≤1% and at least 80% lower than under equal-update-only scheduling.

  **sample size rationale:** N=8 seeds per arm-scheduler cell provides coverage of stochastic sampling and acceptance variation; the primary quantities are exact training-ledger counts rather than noisy benchmark estimates, so between-seed variance in the imbalance statistic (not prompt-level noise) drives precision, and 8 seeds is chosen to give a stable seed-stratified bootstrap over the imbalance ratio.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-2

  **setup:** Using the normalization-complete scheduler from rq-1, train all six arms with 8 paired seeds each and evaluate every arm-seed checkpoint on the same frozen panel of 4,200 prompts (700 each from formal math, code generation, execution reasoning, invariant inference, semantic equivalence, and repair). Replay weights are constructed entirely from the Budget and Replay Ledger and applied at the level of training exposure, not held-out prompts: for each arm, the stabilized inverse-replay weight for a training example i is w_i = p_bar / p_i, where p_i is example i's empirical replay probability and p_bar is the arm's mean replay probability, truncated to the [1st, 99th] percentile of the per-arm weight distribution to bound variance. Because evaluation prompts are held out and have no training replay count, the correction is transported to the evaluation estimand by reweighting each arm's accepted-trajectory training distribution when re-estimating that arm's expected paired outcome (a Hajek estimator normalized to sum-to-one weights); unweighted estimates use w_i≡1. Compute all 15 pairwise arm contrasts both ways and apply simultaneous equivalence tests clustered by prompt and training seed.

  **metrics:** For each contrast, the difference between stabilized inverse-replay-weighted and unweighted mean paired W, where W is +1 for a win, -1 for a loss, and 0 for a tie.

  **description:** Are estimated arm effects robust to replay-frequency correction rather than being driven by uneven replay exposure?

  **expected outcome:** Every contrast's weighted-minus-unweighted effect lies strictly between -0.05 and 0.05, with all adjusted equivalence tests passing.

  **statistical test:** Holm-adjusted two-one-sided equivalence tests with margin [-0.05,0.05] at family-wise α=0.05, using a wild cluster bootstrap over the 8 seed clusters (Rademacher weights) to remain calibrated with few seed clusters.

  **target hypotheses:** - For every arm contrast on the Paired Evaluation Panel, inverse-replay-weighted and unweighted mean effects will differ by <0.05 on the win-minus-loss scale.

  **sample size rationale:** N=4,200 prompts gives balanced coverage of six task families for the within-arm mean, but the equivalence test's precision is limited by the 8 paired training seeds per arm; 8 seeds is the minimum at which the wild cluster bootstrap is acceptably calibrated for a [-0.05,0.05] margin, and prompt count is set for a worst-case simultaneous half-width near 0.05 across 15 bounded paired contrasts conditional on the between-seed variance.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-3

  **setup:** Train Lean and matched non-formal SFT from the shared checkpoint with 12 paired seeds, then evaluate every checkpoint on 2,500 contamination-screened, dependency-disjoint Lean theorem tasks sampled across the formal-math panel. Estimate Lean-minus-control W treating the 12 seeds as the primary clustering unit; this is the stopping gate for rq-4 through rq-6.

  **metrics:** Mean paired formal-math W across prompts and seeds, using kernel-checked proof acceptance as the success criterion.

  **description:** Does the transfer estimator detect the preregistered mathematical-benchmark positive control before software-family claims are interpreted?

  **expected outcome:** Point-estimated W is at least 0.10 and its one-sided 95% lower bound is greater than 0.05.

  **statistical test:** One-sided paired test of H0: W≤0.05 at α=0.05 using a wild cluster bootstrap over the 12 seed clusters with a seed-level t-statistic, reporting a one-sided 95% lower confidence bound calibrated for few clusters rather than a prompt-count-driven bound.

  **target hypotheses:** - The Lean arm's formal-math W relative to non-formal SFT will be ≥0.10, with its one-sided 95% lower confidence bound exceeding 0.05.

  **sample size rationale:** Because training-seed variability is part of the estimand, power is driven by the number of paired seeds, not prompt count; 12 paired seeds is chosen so the seed-level effect (mean per-seed Lean-minus-control W) has ≥80% power to reject W=0.05 in favor of a per-seed mean of 0.10 given the observed between-seed standard deviation (to be estimated on a pilot of 4 seeds; the design freezes 12 as the confirmatory count). N=2,500 theorems per seed makes the within-seed W estimate precise enough that residual variance is dominated by the between-seed term.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-4

  **setup:** If rq-3 passes, compare 12 paired Lean, Dafny, and matched non-formal SFT seeds on a disjoint panel of 4,000 prompts, with 800 prompts in each software family. Hold checkpoint, four training budgets, decoding budget, and scoring oracles fixed. Estimate the full transfer matrix: for each of the five software families, report Dafny-minus-non-formal, Lean-minus-non-formal, and Dafny-minus-Lean paired W separately (family-level, not only aggregate), plus the equal-weight aggregate Dafny-minus-Lean. Obtain simultaneous seed-cluster confidence intervals across all family-level contrasts.

  **metrics:** Per-family paired W for each branch versus the non-formal control and for Dafny versus Lean, with execution, verifier, equivalence-oracle, or repair-test success defining wins, plus the equal-weight mean of the five family-specific Dafny-minus-Lean W values.

  **description:** Conditional on a valid mathematical positive control, does the full branch-by-outcome transfer matrix distinguish program-verification post-training from mathematical-proof post-training across each software capability, exposing heterogeneous or negative transfer rather than only an aggregate?

  **expected outcome:** The equal-weight Dafny-minus-Lean mean W is at least 0.05 and significantly positive; each family-level contrast is reported with its own sign and interval so that heterogeneous or negative per-family transfer is detectable even when the aggregate is positive.

  **statistical test:** One-sided paired wild cluster bootstrap over 12 seed clusters for H0: equal-weight mean W≤0 at α=0.05 (preregistered effect-size criterion W≥0.05), with Holm-adjusted simultaneous two-sided seed-cluster intervals for the fifteen family-level branch-versus-control and Dafny-versus-Lean contrasts.

  **target hypotheses:** - Conditional on passing the gate, the Dafny arm will exceed the Lean arm by ≥0.05 in equal-weight mean W across code generation, execution reasoning, invariant inference, semantic equivalence, and repair.

  **sample size rationale:** N=4,000 supplies 800 observations per family for precise within-seed family estimates, but confirmatory power for the aggregate and per-family contrasts is governed by the 12 paired seeds; 12 seeds targets ≥80% power for a per-seed aggregate effect of 0.05 under the pilot-estimated between-seed variance, and 800 prompts/family keeps within-seed noise below the between-seed term for the family-level breakdown.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-5

  **setup:** If rq-3 passes, train Lean→Dafny, Lean-only, Dafny-only, and non-formal SFT with 12 paired seeds and identical total four-axis budgets. Evaluate them on a frozen, disjoint 4,000-prompt software panel with 800 prompts per family. Estimate the three curriculum-minus-comparator contrasts jointly and define performance against the best comparator as their minimum; also report each contrast per family so a curriculum benefit concentrated in or absent from specific families is visible.

  **metrics:** Minimum of the three equal-weight software-family W contrasts, accompanied by simultaneous seed-cluster lower confidence bounds, plus the per-family decomposition of each contrast.

  **description:** Does the transfer measurement detect a curriculum benefit that is not attributable to selecting a favorable single-branch or non-formal comparator, and is that benefit consistent across families?

  **expected outcome:** All three point contrasts are at least 0.05, so their minimum is at least 0.05, and every simultaneous lower bound is above zero.

  **statistical test:** One-sided max-t wild cluster bootstrap over 12 seed clusters providing simultaneous 95% lower bounds for all three paired contrasts at family-wise α=0.05.

  **target hypotheses:** - Lean→Dafny will exceed the best of Lean-only, Dafny-only, and non-formal SFT by ≥0.05 in equal-weight software-family W, with a simultaneous 95% lower confidence bound above zero.

  **sample size rationale:** N=4,000 (800/family) makes within-seed contrast estimates precise, while the 12 paired seeds are the effective clusters for the max-t bootstrap; 12 seeds targets ≥80% simultaneous power for a 0.05 per-seed effect across three comparisons under the pilot-estimated between-seed variance, replacing the earlier prompt-count-based power argument.

  **target sub problem id:** sp-3
-
  **tier:** mechanism

  **rq id:** rq-6

  **setup:** If rq-3 passes, train Lean→Dafny, Dafny→Lean, and interleaved curricula with 12 paired seeds, identical data pools, total budgets, and optimizer settings; only ordering is varied. Evaluate on a disjoint 9,000-prompt panel with 1,800 prompts per software family and test both Lean→Dafny contrasts jointly, reporting per-family decompositions alongside the aggregate.

  **metrics:** Two equal-weight software-family W contrasts: Lean→Dafny minus Dafny→Lean and Lean→Dafny minus interleaving, plus their per-family breakdown.

  **description:** Is the measured curriculum effect sensitive to training order rather than merely to exposure to both formal domains?

  **expected outcome:** Lean→Dafny has W≥0.03 relative to each alternative curriculum, and both adjusted tests reject non-positive transfer.

  **statistical test:** Holm-adjusted one-sided paired wild cluster bootstrap over 12 seed clusters for both contrasts against zero at family-wise α=0.05, with a preregistered 0.03 point-effect criterion.

  **target hypotheses:** - Lean→Dafny will exceed both Dafny→Lean and interleaved training by ≥0.03 in equal-weight software-family W.

  **sample size rationale:** N=9,000 (1,800/family) drives within-seed precision for the small 0.03 target, but the two one-sided comparisons are powered on the 12 paired seed clusters; 12 seeds targets ≥80% power for a 0.03 per-seed order effect under the pilot-estimated between-seed variance, and the larger prompt count is needed here only to keep within-seed noise negligible relative to the between-seed term at this smaller effect size.

  **target sub problem id:** sp-3
