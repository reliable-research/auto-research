> **⚠️ SUPERSEDED SOURCE ARTIFACT — DO NOT CITE AS CURRENT.**
> This is the unedited AutoDiscussion research report, kept for provenance. It still contains
> the adequacy-aware `V = A·D·(1−Q)` estimand (superseded by raw `δ = Pr(A)−Pr(B)`) and the `D_i`-gated definition of `B_i`, all of which were corrected during review.
> **Current design: `paper-draft.revised.md` and `experiment-spec.md`.** See `../MAJORS.md`.

# ZW2 Verified but Wrong: Measuring and Closing the Specification-Adequacy Gap in Proof-Rewarded Code Models

> specification gaming under verifier-driven reinforcement learning

_Research report — 6 confirmed steps._

## Problem Definition

**input:** Observed solutions from RL training on a Dafny single-function corpus, including training checkpoints, verifier outcomes, independently authored held-out behavioral tests, fixed human-authored or model-generated specifications, reward-arm assignments, and adversarial contracts labeled by specification-hacking mechanism.

**output:** An estimator and training-step trajectory for the specification-adequacy gap, delta, defined as formal verification rate minus independent behavioral correctness rate, with outcomes decomposed by hacking mechanism, reward arm, specification source, vacuity, and precondition-domain nonemptiness.

**summary:** Formal verifier acceptance does not establish that a model-generated specification and implementation capture the user's natural-language intent. Proof-rewarded training may therefore increase verification rates while behavioral correctness stagnates, especially when the model can generate or weaken the specification it is rewarded against.

**objective:** Measure delta reliably across training and determine whether it widens under generated specifications, remains controlled under trusted fixed specifications, and is reduced by a hybrid proof-plus-execution reward relative to binary verifier and structured verification-condition rewards.

**study type:** empirical

**constraints:** Behavioral correctness must be evaluated on held-out tests never exposed through the reward channel. Empty precondition domains and vacuous proofs must be distinct outcomes rather than successes; planted mechanisms must remain separately labeled. The study is limited to a Dafny single-function corpus, a 0.6B model, and existing prover infrastructure, with cited numerical precedents left unquoted until verified against primary sources.

**formal summary:** Given checkpointed Dafny RL solutions under binary verifier, structured verification-condition, and hybrid rewards with fixed or generated specifications, produce a mechanism-decomposed trajectory of delta, measuring the divergence between verification and held-out behavioral correctness subject to reward-isolated tests, explicit vacuity and domain checks, a 0.6B model, and no new prover engineering.

## Research Significance

**summary:** Proof-rewarded training has a measurement blind spot because accepted proofs can certify weak, contradictory, vacuous, or incomplete contracts rather than intended behavior. Existing defenses filter or cross-check misaligned code and specifications, but do not quantify how large this gap is, how it evolves during RL, or when execution evidence closes it.

**evidence:** Re:Form reports that optimizing verifier acceptance alone rewards weak or underspecified specifications. A cited 2026 MIT thesis reports verified reward rising from 2.2% to 58.1% and, after removing underspecified tasks, verified pass rate rising from 9.7% to 31.1%; both figures require primary-source verification before quotation. AlphaVerus, Clover, and 2026 semantic-equivalence self-play independently introduce defenses against code-specification misalignment without measuring delta or its training trajectory.

**who cares:** Researchers building RL with verifiable rewards, formal-methods and program-synthesis teams, benchmark designers, evaluators of verified code models, and users relying on generated Dafny specifications or implementations need to know when proof is a sufficient oracle and when independent execution evidence is required.

**why it matters:** If verifier acceptance is treated as correctness, training can appear to improve while models learn to shrink input domains, omit required outputs or frame conditions, use vacuous invariants, or satisfy written contracts that violate natural-language intent. This would invalidate proof-reward performance claims and could deploy behaviorally wrong code as verified.

## Related Work

**summary:** Deeply compared the 8 most decisive PDF-grounded papers against our problem definition (1 candidate baselines, 0 high threats to our motivation). A further 6 cited work(s) are listed for coverage without a deep comparison (no fetchable full text, or less central than the top 8).

**general related works:**

-
  **summary:** Formal verification provides a rigorous and systematic approach to ensure the correctness and reliability of software systems. Yet, constructing specifications for the full proof relies on domain expertise and non-trivial manpower. In view of such needs, an automated approach for specification synthesis is desired. While existing automated approaches are limited in their versatility, i.e., they either focus only on synthesizing loop invariants for numerical programs, or are tailored for specific types of programs or invariants. Programs involving multiple complicated data types (e.g., arrays, pointers) and code structures (e.g., nested loops, function calls) are often beyond their capabiliti

  **work id:** e1b354b1-a265-44ff-af9b-05c6e5f3790a

  **citation:** Cheng Wen et al.. Enchanting Program Specification Synthesis by Large Language Models using Static Analysis and Program Verification.
-
  **summary:** In reinforcement learning from human feedback, it is common to optimize against a reward model trained to predict human preferences. Because the reward model is an imperfect proxy, optimizing its value too much can hinder ground truth performance, in accordance with Goodhart’s law. This effect has been frequently observed, but not carefully measured due to the expense of collecting human preference data. In this work, we use a synthetic setup in which a fixed “goldstandard” reward model plays the role of humans, providing labels used to train a proxy reward model. We study how the gold reward model score changes as we optimize against the proxy reward model using either reinforcement learnin

  **work id:** 011e2b70-bada-4713-8f51-8b6f6078a688

  **citation:** (unknown authors). Scaling Laws for Reward Model Overoptimization.
-
  **summary:** Reinforcement Learning from Human Feedback (RLHF) has been crucial to the recent success of Large Language Models (LLMs), however, it is often a complex and brittle process. In the classical RLHF framework, a reward model is first trained to represent human preferences, which is in turn used by an online reinforcement learning (RL) algorithm to optimize the LLM. A prominent issue with such methods is reward over-optimization or reward hacking, where performance as measured by the learned proxy reward model increases, but true quality plateaus or even deteriorates. Direct Alignment Algorithms (DAAs) like Direct Preference Optimization have emerged as alternatives to the classical RLHF pipelin

  **work id:** 08f8acb4-8a2a-4274-8274-56cd0a8d2bf4

  **citation:** Rafael Rafailov et al.. Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms.
-
  **summary:** We present an extension to the <sup>Pythia</sup> Monte Carlo event generator that enables simulations of collisions between a generic hadron beam on a nuclear target with energy variation in event-by-event basis. This builds upon <sup>Pythia</sup>’s module for heavy ions, <sup>Angantyr</sup>, as well as previous work on simulating hadron-proton collisions. As such, the extensions in this work are largely technical, except for a rudimentary model for hadronic fluctuations. With hadron-ion simulations, we implement an explicit vector-meson dominance (VMD) model that can be used to simulate interactions of hadronic component of real photons in photo-nuclear collisions. Such processes can be stu

  **work id:** 33ea53e6-659f-4f2d-96b4-4c02ae6d0c57

  **citation:** Ilkka Helenius & Marius Utheim. Hadron-ion collisions in <sup>Pythia</sup> and the vector-meson dominance model for photoproduction.
-
  **summary:** We have developed a new theory relating partial molar volumes of binary mixtures to the specific (Voronoi) volumes. A simple relation gives new insight into the physical meaning of partial molar volumes in terms of the actual volumes occupied by the molecules. Partial molar quantities are defined through the use of the Euler theorem for homogeneous functions. These properties have been in use for a long time, despite the fact that they do not give an intuitive picture of the properties they are to represent. For instance, the partial molar volume of a given component in a mixture is the change in the total volume with a change in composition, hence it represents the derivative of a volume. T

  **work id:** 137c2ed1-24c7-4e61-a120-0dc65c3db9b0

  **citation:** Kristian Polanco Olsen et al.. A new thermodynamic function for binary mixtures: the co-molar volume.
-
  **summary:** Program verifiers such as Dafny automate proofs by outsourcing them to an SMT solver. This automation is not perfect, however, and the solver often requires hints in the form of assertions, creating a burden for the proof engineer. In this paper, we propose Laurel, a tool that alleviates this burden by automatically generating assertions using large language models (LLMs). To improve the success rate of LLMs in this task, we design two domain-specific prompting techniques. First, we help the LLM determine the location of the missing assertion by analyzing the verifier’s error message and inserting an assertion placeholder at that location. Second, we provide the LLM with example assertions f

  **work id:** 3709758b-d59c-43e4-9d07-3feba4cbc29f

  **citation:** Eric Mugnier et al.. Laurel: Unblocking Automated Verification with Large Language Models.

**specific related works:**

-
  **input:** Natural language problem description; Function signature; Optionally a ground truth code implementation (for SpecGen/ProofGen); Optionally a ground truth formal specification (for CodeGen/ProofGen)

  **output:** Generated Lean code implementation; Generated formal specification (pre-condition and post-condition); Generated formal proof of code-specification alignment in Lean

  **summary:** Large language models (LLMs) are increasingly integrated in software development, but ensuring correctness in LLM-generated code remains challenging and often requires costly manual review. Verifiable code generation—jointly generating code, specifications, and proofs of code-specification alignment—offers a promising path to address this limitation and further unleash LLMs' benefits in coding. Yet, there exists a significant gap in evaluation: current benchmarks often focus on only individual components rather than providing a holistic evaluation framework of all tasks. In this paper, we introduce VERINA (Verifiable Code Generation Arena), a high-quality benchmark enabling a comprehensive and modular evaluation of code, specification, and proof generation as well as their compositions. VERINA consists of 189 manually curated coding tasks in Lean, with detailed problem descriptions, reference implementations, formal specifications, and extensive test suites. Our extensive evaluation of state-of-the-art LLMs reveals significant challenges in verifiable code generation, especially in proof generation, underscoring the need for improving LLM-based theorem provers in verification domains. The best model, OpenAI o3, achieves a 72.6% code correctness rate, 52.3% for specification soundness and completeness, and a mere 4.9% proof success rate (based on one trial per task). We hope VERINA will catalyze progress in verifiable code generation by providing a rigorous and comprehensive benchmark. We release our dataset on https://huggingface.co/datasets/sunblaze-ucb/verina and our evaluation code on https://github.com/sunblaze-ucb/verina.

  **work id:** b362d89d-ca99-4a24-962c-f69bc2a355bb

  **approach:** VERINA benchmark construction and its modular evaluation framework for code, specification, and proof generation.

  **citation:** Zhe Ye et al.. VERINA: BENCHMARKING VERIFIABLE CODE GENER-ATION.

  **comparison:**

  **role:** baseline

  **gap type:** not_solved

  **effectiveness:** n/a

  **gap we address:** The training-dependent specification-adequacy gap is not measured: VERINA does not determine whether proof rewards widen verifier acceptance minus held-out behavioral correctness when models generate or weaken their own contracts. It also does not decompose that gap by reward arm, specification source, hacking mechanism, vacuity, or precondition-domain nonemptiness.

  **method addresses:** false

  **method rationale:** Its static benchmark and specification-quality pipeline cannot estimate training-step trajectories across reward arms or distinguish planted specification-hacking mechanisms, vacuous proofs, and empty precondition domains.

  **problem alignment:** related

  **alignment rationale:** VERINA evaluates whether generated specifications capture intended behavior, but it does not study how proof-based RL changes the longitudinal gap between verifier acceptance and independently tested behavioral correctness.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_solved] The training-dependent specification-adequacy gap is not measured: VERINA does not determine whether proof rewards widen verifier acceptance minus held-out behavioral correctness when models generate or weaken their own contracts. It also does not decompose that gap by reward arm, specification source, hacking mechanism, vacuity, or precondition-domain nonemptiness.

    **limitation id:** lim-1

    **evidence for limitation:** VERINA evaluates whether generated specifications capture intended behavior, but it does not study how proof-based RL changes the longitudinal gap between verifier acceptance and independently tested behavioral correctness. | Its static benchmark and specification-quality pipeline cannot estimate training-step trajectories across reward arms or distinguish planted specification-hacking mechanisms, vacuous proofs, and empty precondition domains.

  **is potential baseline:** true
-
  **input:** A set of code implementations c; Dafny function signatures and program bodies with annotations missing

  **output:** Full Dafny code implementations with corresponding formal specifications y; Preconditions, postconditions, loop invariants, assert statements, and other applicable annotations

  **summary:** Existing informal language-based (e.g., human language) Large Language Models (LLMs) trained with Reinforcement Learning (RL) face a significant challenge: their verification processes, which provide crucial training signals, are neither reliable nor scalable. In fact, the prevalent large proprietary models could hardly generate verifiable programs. A promising yet largely uncharted alternative is formal language-based reasoning. Grounding LLMs in rigorous formal systems where generative models operate in formal language spaces (e.g., Dafny) enables the automatic and mathematically provable verification of their reasoning processes and outcomes. This capability is pivotal for achieving large-scale, reliable formal software verification. It is a common practice to employ human-annotated chain-of-thought and answers to induce the reasoning and coding capabilities of LLMs. Unfortunately, it becomes unacceptably all-consuming to provide such priors for supervising complex programming tasks. In this work, we systematically explore ways to reduce human annotations with the formal language, Dafny, as the main environment for our pilot study. Our pipeline mainly relies on introducing an automatic and scalable data curation pipeline, and careful RL designs integrated with feedback from the formal language verifier. We introduce DafnyComp, a benchmark of compositional formal programs with auto-formalized specifications for specification reasoning. Our supervised fine-tuning (SFT) stage enables even small models (e.g., 0.5B) to generate syntactically valid and verifiable Dafny code, surpassing proprietary models. RL with regularization further improves performance, achieving stronger generalization to out-of-domain tasks and outperforming all strong baselines on the challenging DafnyComp benchmark. Anonymized code and models are available at https://github. com/Veri-Code/ReForm and https://huggingface.co/Veri-Code.

  **work id:** 03245e16-2e10-493f-8672-0c0e6c598746

  **approach:** Re:Form combines automated data curation, a compositional benchmark, limited CoT-free supervised fine-tuning, and verifier-guided reinforcement learning with syntax, verification, and subset rewards plus policy regularization.

  **citation:** Chuanhao Yan et al.. Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_solved

  **effectiveness:** n/a

  **gap we address:** The divergence between formal verification and independent behavioral correctness is not solved by comparing generated contracts with auto-formalized reference specifications. Re:Form does not determine whether proof-rewarded training widens this divergence when specifications are generated or weakened, nor decompose it by vacuity, precondition-domain emptiness, reward arm, and hacking mechanism.

  **method addresses:** false

  **method rationale:** Its verifier and specification-subset rewards cannot measure our adequacy gap because they provide no held-out behavioral oracle, training-step gap estimator, or separate accounting for vacuous proofs, empty precondition domains, and planted hacking mechanisms.

  **problem alignment:** related

  **alignment rationale:** Both study verifier-guided Dafny specification generation, but Re:Form optimizes verifiable specifications for given implementations whereas our problem estimates the divergence between verifier acceptance and independently tested natural-language intent across training.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_solved] The divergence between formal verification and independent behavioral correctness is not solved by comparing generated contracts with auto-formalized reference specifications. Re:Form does not determine whether proof-rewarded training widens this divergence when specifications are generated or weakened, nor decompose it by vacuity, precondition-domain emptiness, reward arm, and hacking mechanism.

    **limitation id:** lim-1

    **evidence for limitation:** Both study verifier-guided Dafny specification generation, but Re:Form optimizes verifiable specifications for given implementations whereas our problem estimates the divergence between verifier acceptance and independently tested natural-language intent across training. | Its verifier and specification-subset rewards cannot measure our adequacy gap because they provide no held-out behavioral oracle, training-step gap estimator, or separate accounting for vacuous proofs, empty precondition domains, and planted hacking mechanisms.

  **is potential baseline:** false
-
  **input:** a natural language specification; a Lean function signature for the implementation; a hidden ground-truth Lean specification used for certification

  **output:** a formal Lean specification expressed as a predicate; a proof that the generated specification is semantically equivalent to the hidden ground-truth specification; a Lean implementation matching the required function signature; a formal proof that the implementation satisfies the ground-truth specification

  **summary:** We introduce CLEVER<sup>1</sup>, a high-quality, curated benchmark of 161 problems for end-to-end verified code generation in Lean. Each problem consists of (1) the task of generating a specification that matches a held-out ground-truth specification, and (2) the task of generating a Lean implementation that provably satisfies this specification. Unlike prior benchmarks, CLEVER avoids test-case supervision, LLM-generated annotations, and specifications that leak implementation logic or allow vacuous solutions. All outputs are verified post-hoc using Lean’s type checker to ensure machine-checkable correctness. We use CLEVER to evaluate several few-shot and agentic approaches based on state-of-the-art language models. These methods all struggle to achieve full verification, establishing it as a challenging frontier benchmark for program synthesis and formal reasoning. Our benchmark can be found on GitHub as well as HuggingFace. All our evaluation code is also available online.

  **work id:** 04e65bc3-1e9b-4227-8fa0-cf72bd5d3880

  **approach:** CLEVER adapts 161 HUMANEVAL tasks into manually curated Lean problems with non-computable specifications and evaluates models through separately checked specification- and implementation-certification stages.

  **citation:** Amitayush Thakur et al.. CLEVER: A Curated Benchmark for Formally Verified Code Generation.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_solved

  **effectiveness:** n/a

  **gap we address:** CLEVER does not solve the problem of estimating whether proof-rewarded training widens the difference between verifier acceptance and independent behavioral correctness when models can generate or weaken contracts. It also does not decompose that gap by reward arm, specification source, hacking mechanism, vacuity, or empty precondition domain.

  **method addresses:** false

  **method rationale:** Its certification pipeline presupposes a hidden formal ground-truth specification and evaluates end-to-end generation, but it neither supplies independent held-out behavioral correctness measurements nor estimates training-induced gap trajectories under alternative proof rewards.

  **problem alignment:** related

  **alignment rationale:** CLEVER addresses specification adequacy by certifying generated Lean specifications against hidden human-authored formal specifications, whereas our problem measures the verifier–behavioral correctness gap across RL checkpoints, reward arms, and specification-hacking mechanisms in Dafny.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_solved] CLEVER does not solve the problem of estimating whether proof-rewarded training widens the difference between verifier acceptance and independent behavioral correctness when models can generate or weaken contracts. It also does not decompose that gap by reward arm, specification source, hacking mechanism, vacuity, or empty precondition domain.

    **limitation id:** lim-1

    **evidence for limitation:** CLEVER addresses specification adequacy by certifying generated Lean specifications against hidden human-authored formal specifications, whereas our problem measures the verifier–behavioral correctness gap across RL checkpoints, reward arms, and specification-hacking mechanisms in Dafny. | Its certification pipeline presupposes a hidden formal ground-truth specification and evaluates end-to-end generation, but it neither supplies independent held-out behavioral correctness measurements nor estimates training-induced gap trajectories under alternative proof rewards.

  **is potential baseline:** false
-
  **input:** A formal specification containing the function signature and conditions that must be satisfied; The external context containing definitions used by the specification; Optional natural-language documentation describing the intended behavior or prescribed algorithm

  **output:** A program implementation; A formal proof of the implementation's correctness with respect to the specification; Any additional imports, helper functions, helper lemmas, or other context needed by the solution

  **summary:** We present and test the largest benchmark for vericoding, LLM-generation of formally verified code from formal specifications — in contrast to vibe coding, which generates potentially buggy code from a natural language description. Our benchmark contains 12,504 formal specifications, with 3,029 in Dafny, 2,334 in Verus/Rust and 7,141 in Lean. Of these, 6,174 are new unseen problems. We find vericoding success rates of 27% in Lean, 44% in Verus/Rust and 82% in Dafny using off-the-shelf LLMs. Adding natural-language descriptions does not significantly improve performance. We also find that LLM progress has improved progress on pure Dafny verification from 68% to 96% over the past year. The benchmark and vericoding results are shared in this GitHub repo.

  **work id:** b9393ea2-dde8-4f48-9ca2-2829fdb65ed3

  **approach:** The method constructs a multilingual benchmark from curated sources and translated specifications, validates its quality, and evaluates off-the-shelf LLMs through iterative generation, cheating checks, and formal verification.

  **citation:** Sergiu Bursuc et al.. A BENCHMARK FOR VERICODING: FORMALLY VERIFIED PROGRAM SYNTHESIS.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** Verifier success is not compared with independent behavioral correctness when the model can generate or weaken the rewarded specification. Consequently, the training-step specification-adequacy gap and its decomposition by reward arm, specification source, vacuity, domain emptiness, and hacking mechanism remain unmeasured.

  **method addresses:** false

  **method rationale:** Their verifier-centered benchmark, cheating filters, and spot inspection do not provide held-out behavioral judgments, longitudinal training checkpoints, reward-arm comparisons, or explicit classification of vacuity, empty precondition domains, and specification-hacking mechanisms.

  **problem alignment:** related

  **alignment rationale:** Both concern Dafny verification by LLMs, but the paper measures synthesis success against supplied formal specifications whereas our problem measures divergence between verifier acceptance and independently tested natural-language intent during reward-based training.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] Verifier success is not compared with independent behavioral correctness when the model can generate or weaken the rewarded specification. Consequently, the training-step specification-adequacy gap and its decomposition by reward arm, specification source, vacuity, domain emptiness, and hacking mechanism remain unmeasured.

    **limitation id:** lim-1

    **evidence for limitation:** Both concern Dafny verification by LLMs, but the paper measures synthesis success against supplied formal specifications whereas our problem measures divergence between verifier acceptance and independently tested natural-language intent during reward-based training. | Their verifier-centered benchmark, cheating filters, and spot inspection do not provide held-out behavioral judgments, longitudinal training checkpoints, reward-arm comparisons, or explicit classification of vacuity, empty precondition domains, and specification-hacking mechanisms.

  **is potential baseline:** false
-
  **input:** Informal natural language description of a method (nl), e.g. a docstring or JavaDoc comment; Optionally, a reference code implementation (r) of the method; Surrounding code context (class/type information, call-graph methods) for real-world projects; A set of hidden test inputs (T) used only for offline evaluation

  **output:** A formal method postcondition expressed as an executable, side-effect-free program assertion over input and output states; Multiple sampled candidate postconditions per problem (e.g. 10 per prompt variant)

  **summary:** Informal natural language that describes code functionality, such as code comments or function documentation, may contain substantial information about a program’s intent. However, there is typically no guarantee that a program’s implementation and natural language documentation are aligned. In the case of a conflict, leveraging information in code-adjacent natural language has the potential to enhance fault localization, debugging, and code trustworthiness. In practice, however, this information is often underutilized due to the inherent ambiguity of natural language which makes natural language intent challenging to check programmatically. The “emergent abilities” of Large Language Models (LLMs) have the potential to facilitate the translation of natural language intent to programmatically checkable assertions. However, it is unclear if LLMs can correctly translate informal natural language specifications into formal specifications that match programmer intent. Additionally, it is unclear if such translation could be useful in practice. In this paper, we describe nl2postcond, the problem of leveraging LLMs for transforming informal natural language to formal method postconditions, expressed as program assertions. We introduce and validate metrics to measure and compare diferent nl2postcond approaches, using the correctness and discriminative power of generated postconditions. We then use qualitative and quantitative methods to assess the quality of nl2postcond postconditions, finding that they are generally correct and able to discriminate incorrect code. Finally, we find that nl2postcond via LLMs has the potential to be helpful in practice; nl2postcond generated postconditions were able to catch 64 real-world historical bugs from Defects4J.

  **work id:** e1d08596-270f-46da-aa4a-618da63cd1ce

  **approach:** nl2postcond prompts LLMs (GPT-3.5, GPT-4, StarChat) with natural language (and optionally reference code) to generate executable postconditions, evaluated via test-set correctness and an LLM-mutant-based bug-completeness metric.

  **citation:** Madeline Endres et al.. Can Large Language Models Transform Natural Language Intent into Formal Method Postconditions?.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_solved

  **effectiveness:** n/a

  **gap we address:** The evolution of the specification-adequacy gap under proof-rewarded training is not solved: their static postcondition evaluation does not determine whether verifier acceptance diverges from held-out behavioral correctness across checkpoints and reward arms. It also does not distinguish vacuous proofs, empty precondition domains, or planted specification-hacking mechanisms from genuine success.

  **method addresses:** false

  **method rationale:** Its postcondition correctness and mutant-killing metrics do not estimate a verification-minus-behavior trajectory across RL checkpoints, compare proof-reward schemes, or classify vacuity, empty precondition domains, and specification-hacking mechanisms.

  **problem alignment:** related

  **alignment rationale:** The paper evaluates whether generated executable postconditions capture natural-language intent, whereas our problem measures how proof-rewarded training changes the gap between verifier acceptance and independent behavioral correctness across specifications, reward arms, and hacking mechanisms.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_solved] The evolution of the specification-adequacy gap under proof-rewarded training is not solved: their static postcondition evaluation does not determine whether verifier acceptance diverges from held-out behavioral correctness across checkpoints and reward arms. It also does not distinguish vacuous proofs, empty precondition domains, or planted specification-hacking mechanisms from genuine success.

    **limitation id:** lim-1

    **evidence for limitation:** The paper evaluates whether generated executable postconditions capture natural-language intent, whereas our problem measures how proof-rewarded training changes the gap between verifier acceptance and independent behavioral correctness across specifications, reward arms, and hacking mechanisms. | Its postcondition correctness and mutant-killing metrics do not estimate a verification-minus-behavior trajectory across RL checkpoints, compare proof-reward schemes, or classify vacuity, empty precondition domains, and specification-hacking mechanisms.

  **is potential baseline:** false
-
  **input:** generated code; formal annotations; a precise natural-language description represented as a docstring

  **output:** an acceptance or rejection decision for the generated instance; accepted code that passes formal-verification and consistency checks

  **summary:** The use of large language models for code generation is a rapidly growing trend in software development. However, without efective methods for ensuring the correctness of generated code, this trend could lead to undesirable outcomes. In this paper, we introduce a new approach for addressing this challenge: the Clover paradigm, short for Closed-Loop Verifiable Code Generation, which uses consistency checking to provide a strong filter for incorrect code. Clover performs consistency checks among code, docstrings, and formal annotations. The checker is implemented using a novel integration of formal verification tools and large language models. We provide a theoretical analysis to support our thesis that Clover should be efective at consistency checking. We also empirically investigate its performance on a hand-designed dataset (CloverBench) featuring annotated Dafny programs at a textbook level of dificulty. Experimental results show that for this dataset: (i) LLMs are reasonably successful at automatically generating formal specifications; and (ii) our consistency checker achieves a promising acceptance rate (up to 87%) for correct instances while maintaining zero tolerance for adversarial incorrect ones (no false positives). Clover also discovered 6 incorrect programs in the existing human-written dataset MBPP-DFY-50.

  **work id:** 3eb4fcf7-5054-4049-b8e2-1fda988e2236

  **approach:** Clover generates or receives code, annotations, and docstrings, then accepts an instance only if six consistency checks based on deductive verification, LLM reconstruction, and equivalence testing all pass.

  **citation:** Chuyue Sun et al.. Clover: Closed-Loop Verifiable Code Generation.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** Clover does not consider whether proof-rewarded training systematically widens the gap between verifier acceptance and independent behavioral correctness when models can generate or weaken specifications. It therefore does not measure this gap across training steps or compare its evolution under fixed-specification, generated-specification, binary-verifier, structured-VC, and hybrid proof-plus-execution reward conditions.

  **method addresses:** false

  **method rationale:** Clover's reconstruction-based acceptance filter does not independently estimate held-out behavioral correctness, compute delta across checkpoints, or distinguish specification-hacking mechanisms, vacuity, and empty precondition domains.

  **problem alignment:** related

  **alignment rationale:** Both concern verifier-approved code whose specifications may fail to capture natural-language intent, but Clover produces a static consistency-filter decision whereas our problem estimates a behavioral verification gap and its trajectory under alternative training rewards.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] Clover does not consider whether proof-rewarded training systematically widens the gap between verifier acceptance and independent behavioral correctness when models can generate or weaken specifications. It therefore does not measure this gap across training steps or compare its evolution under fixed-specification, generated-specification, binary-verifier, structured-VC, and hybrid proof-plus-execution reward conditions.

    **limitation id:** lim-1

    **evidence for limitation:** Both concern verifier-approved code whose specifications may fail to capture natural-language intent, but Clover produces a static consistency-filter decision whereas our problem estimates a behavioral verification gap and its trajectory under alternative training rewards. | Clover's reconstruction-based acceptance filter does not independently estimate held-out behavioral correctness, compute delta across checkpoints, or distinguish specification-hacking mechanisms, vacuity, and empty precondition domains.

  **is potential baseline:** false
-
  **input:** DeepSeek-V3-Base; verifiable mathematics, coding, STEM, and logic questions with ground-truth answers or executable tests; general instruction, helpfulness, and safety data; reasoning trajectories generated by DeepSeek-R1 for distillation

  **output:** DeepSeek-R1-Zero with emergent long-chain reasoning behaviors; DeepSeek-R1 with reasoning and general instruction-following capabilities; distilled smaller DeepSeek-R1 models

  **summary:** General reasoning represents a long-standing and formidable challenge in artificial intelligence. Recent breakthroughs, exemplified by large language models (LLMs) (Brown et al., 2020; OpenAI, 2023) and chain-of-thought prompting (Wei et al., 2022b), have achieved considerable success on foundational reasoning tasks. However, this success is heavily contingent upon extensive human-annotated demonstrations, and models’ capabilities are still insufficient for more complex problems. Here we show that the reasoning abilities of LLMs can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories. The proposed RL framework facilitates the emergent development of advanced reasoning patterns, such as self-reflection, verification, and dynamic strategy adaptation. Consequently, the trained model achieves superior performance on verifiable tasks such as mathematics, coding competitions, and STEM fields, surpassing its counterparts trained via conventional supervised learning on human demonstrations. Moreover, the emergent reasoning patterns exhibited by these large-scale models can be systematically harnessed to guide and enhance the reasoning capabilities of smaller models.

  **work id:** 95f35867-2a84-4323-aef6-5b83986e15da

  **approach:** DeepSeek-R1-Zero applies outcome-based GRPO directly to DeepSeek-V3-Base, while DeepSeek-R1 uses cold-start data, reasoning-focused RL, rejection-sampled SFT, general-data SFT, and a second mixed-objective RL stage; the resulting reasoning patterns are also distilled into smaller models.

  **citation:** Daya Guo et al.. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** Specification adequacy is not considered when an RL system can generate or weaken the contract that determines its proof reward. The paper does not measure whether verification gains conceal stagnant behavioral correctness or decompose that divergence by specification-hacking mechanism.

  **method addresses:** false

  **method rationale:** Their GRPO pipeline neither compares formal verification with held-out behavioral correctness nor distinguishes specification weakening, vacuity, empty precondition domains, specification source, or hacking mechanism.

  **problem alignment:** related

  **alignment rationale:** Both study reinforcement learning from automatically checkable outcomes, but DeepSeek-R1 optimizes broad answer correctness whereas our problem measures divergence between verifier acceptance and independently tested intent satisfaction in Dafny.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] Specification adequacy is not considered when an RL system can generate or weaken the contract that determines its proof reward. The paper does not measure whether verification gains conceal stagnant behavioral correctness or decompose that divergence by specification-hacking mechanism.

    **limitation id:** lim-1

    **evidence for limitation:** Both study reinforcement learning from automatically checkable outcomes, but DeepSeek-R1 optimizes broad answer correctness whereas our problem measures divergence between verifier acceptance and independently tested intent satisfaction in Dafny. | Their GRPO pipeline neither compares formal verification with held-out behavioral correctness nor distinguishes specification weakening, vacuity, empty precondition domains, specification source, or hacking mechanism.

  **is potential baseline:** false
-
  **input:** a candidate postcondition or summary specification φ(x, y); a method signature m(x):y; a set of validation tests containing consistent input-output pairs

  **output:** an aggregate correctness score for each specification; an aggregate completeness score for each specification; a comparison of the automatic metrics with human-provided specification labels

  **summary:**

  Verification-aware programming languages such as Dafny and F* provide means to formally specify and prove properties of a program. Although the problem of checking an implementation against a specification can be defined mechanically, there is no algorithmic way of ensuring the correctness of the user-intent formalization for programs — that a specification adheres to the user’s intent behind the program. This is because intent or requirement is expressed informally in natural language and the specification is a formal artefact. However, the advent of large language models (LLMs) has made tremendous strides bridging the gap between informal intent and formal program implementations in the last couple of years, driven in large parts due to benchmarks and automated metrics to evaluate different techniques.

  Recent work has developed a framework for evaluating and benchmarking the user-intent formalization problem for mainstream programming languages [12]. However, as we argue in this paper, such an approach does not readily extend to verificationaware languages that support rich specifications (using quantifiers and ghost variables) that cannot be evaluated through dynamic execution. Previous work also required generating program mutants using LLMs to create the benchmark. We advocate an alternate, perhaps simpler approach of symbolically testing specifications to provide an intuitive metric for evaluating the quality of specifications that can be easily instantiated with most verification-aware languages. We demonstrate that our automated metric agrees closely on a human-labeled dataset of Dafny specifications for the popular MBPP code-generation benchmark, yet demonstrates cases where the human labeling is not perfect. We also outline formal verification challenges that need to be addressed to apply the technique more widely. We believe our work provides a stepping stone to enable the establishment of a benchmark and research agenda for the problem of user-intent formalization for programs.

  **work id:** 58cf9871-f809-479c-b1e5-79b9a1fd63ac

  **approach:** The method generates Dafny verification programs from candidate specifications and validation tests, proves consistency on valid input-output pairs, mutates outputs to measure specification strength, aggregates the resulting correctness and completeness scores, and compares them with human labels.

  **citation:** Shuvendu K. Lahiri. Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages.

  **comparison:**

  **role:** related_for_context

  **gap type:** not_considered

  **effectiveness:** n/a

  **gap we address:** The possibility that proof-rewarded training widens the verifier-acceptance versus behavioral-correctness gap is not considered. Their per-specification consistency and mutation scores cannot identify training-induced specification hacking or compare that gap across reward regimes.

  **method addresses:** false

  **method rationale:** Their method neither evaluates generated implementations nor estimates delta across checkpoints, reward arms, specification sources, vacuity, precondition-domain nonemptiness, and planted hacking mechanisms.

  **problem alignment:** related

  **alignment rationale:** Both study whether Dafny specifications capture intended behavior, but the paper scores individual specifications against tests and mutants rather than measuring the training-time gap between verifier acceptance and independent implementation correctness.

  **threat to motivation:** low

  **limitations:**

  -
    **description:** [not_considered] The possibility that proof-rewarded training widens the verifier-acceptance versus behavioral-correctness gap is not considered. Their per-specification consistency and mutation scores cannot identify training-induced specification hacking or compare that gap across reward regimes.

    **limitation id:** lim-1

    **evidence for limitation:** Both study whether Dafny specifications capture intended behavior, but the paper scores individual specifications against tests and mutants rather than measuring the training-time gap between verifier acceptance and independent implementation correctness. | Their method neither evaluates generated implementations nor estimates delta across checkpoints, reward arms, specification sources, vacuity, precondition-domain nonemptiness, and planted hacking mechanisms.

  **is potential baseline:** false

## Sub-Problems

**summary:** Completing the study requires a valid verifier-versus-behavior gap estimator, controlled longitudinal comparisons across training conditions, and mechanism-aware classification of misleading verification successes. Prior work leaves all three components unresolved.

**sub problems:**

-
  **description:** Independent estimation of the adequacy gap between verifier outcomes and never-rewarded held-out behavioral tests remains unresolved.

  **sub problem id:** sp-1

  **technical challenge:** The two outcome rates must be aligned over the same samples while preserving test independence and representing uncertainty in their difference.

  **why it is a problem:** Without a valid delta estimate, increased verification cannot be distinguished from genuine behavioral improvement.

  **source limitation ids:** - lim-1
-
  **description:** Identification of how delta evolves across training checkpoints by reward arm and specification source remains unresolved.

  **sub problem id:** sp-2

  **technical challenge:** Checkpoint, reward-arm, and specification-source effects must be separated despite correlated observations and potentially different verification baselines.

  **why it is a problem:** These controlled trajectories are necessary to determine whether generated specifications widen the gap and whether hybrid rewards reduce it.

  **source limitation ids:** - lim-1
-
  **description:** Distinguishing hacking mechanisms, including vacuity and empty precondition domains as separate failures, remains unresolved.

  **sub problem id:** sp-3

  **technical challenge:** Mechanism labels must remain identifiable when failures overlap, and domain nonemptiness and vacuity require reliable semantic checks beyond binary verifier output.

  **why it is a problem:** Aggregate delta can conceal how models obtain verifier acceptance and therefore cannot identify the risks driving apparent progress.

  **source limitation ids:** - lim-1

**internal reasoning:**

**required components:**

-
  **name:** Independent adequacy-gap estimation

  **note:** No cited work jointly measures verifier acceptance and held-out behavioral correctness to estimate delta.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Controlled training-trajectory comparison

  **note:** Prior work does not track delta across checkpoints while comparing reward arms and fixed versus generated specifications.

  **status:** unsolved

  **covered by limitation ids:** - lim-1
-
  **name:** Failure-mechanism outcome decomposition

  **note:** Existing evaluations do not separately quantify planted hacking mechanisms, vacuity, and empty precondition domains.

  **status:** unsolved

  **covered by limitation ids:** - lim-1

## Method Design

**methods:**

-
  **method id:** m-1

  **hypotheses:**

  - In calibration simulations preserving observed task sizes and V-B dependence, nominal 95% intervals will cover planted delta in 90-98% of runs and be at least 15% narrower than unpaired intervals at the same evaluation budget.
  - On blinded, human-validated intent-violating program mutations, E will detect at least 90% of violations and exceed the detection rate of reward-visible tests by at least 20 percentage points.

  **key insight:** Pairing removes between-candidate variation from the contrast, while escrowed oracle tests make B statistically and procedurally independent of the reward signal.

  **proposed approach:** Construct an escrowed paired evaluation primitive E: human-audited executable oracles and property-based test generators fixed before training and run with secret seeds, producing verifier outcome V and behavioral outcome B for every sampled candidate. Estimate delta as the task-stratified weighted mean of V-B, with nested task-and-test-seed bootstrap intervals that preserve the pairing.

  **target sub problem id:** sp-1
-
  **method id:** m-2

  **hypotheses:**

  - By the final checkpoint, delta in each generated-specification proof-only arm will increase by at least 8 percentage points from step zero and by at least 5 points more than its fixed-specification counterpart, whose change will remain within plus or minus 3 points.
  - Under generated specifications, the hybrid arm's final delta will be at least 5 percentage points lower than both proof-only arms while its verification rate remains within 3 points of the better proof-only arm.

  **key insight:** Randomized factorial contrasts identify reward and specification-source effects, while joint modeling of paired outcomes and repeated tasks retains their covariance without assuming equal verification baselines.

  **proposed approach:** Run a randomized 3-by-2 factorial experiment crossing binary-verifier, structured-VC, and hybrid proof-plus-execution rewards with fixed-trusted and generated specifications, using common initialization distributions, independent training seeds, and eleven equally spaced checkpoints evaluated through primitive E. Fit a hierarchical four-state model for (V,B) with checkpoint splines, full arm-source interactions, and task and seed random effects; report baseline-centered delta contrasts to absorb differing initial verification rates.

  **target sub problem id:** sp-2
-
  **method id:** m-3

  **hypotheses:**

  - On the crossed-mechanism calibration corpus, the audit will achieve at least 0.85 macro-F1 and 0.75 exact-label-set accuracy, exceeding a mutually exclusive syntactic classifier by at least 0.15 on both metrics.
  - Empty-domain and vacuity labels will each achieve at least 0.90 recall at 0.95 precision, with recall at least 20 percentage points above classification from rewarded-verifier output alone.

  **key insight:** Independent semantic predicates and counterfactual interventions give each mechanism a distinct observable signature, allowing empty domains, implementation-independent vacuity, and other attacks to be labeled concurrently rather than forced into one class.

  **proposed approach:** Apply E with a multi-label semantic-intervention audit: an independent solver must produce a replayable UNSAT certificate or validated witness for the generated precondition, while vacuity is tested by havocing outputs and modified state and checking the postcondition over E's hidden intended-domain predicate. Detect precondition exclusion and postcondition weakening through intended-input coverage, oracle-failing mutant acceptance, and one-clause ablations; retain every triggered label, mark solver timeouts unknown, and calibrate on blinded single and crossed planted mechanisms.

  **target sub problem id:** sp-3

**summary:** Use an escrowed, never-rewarded behavioral evaluation to obtain paired verifier and behavioral outcomes for identical candidates. Combine a longitudinal factorial training design with semantic intervention audits to estimate the adequacy-gap trajectory and attribute it to overlapping hacking mechanisms.

## Experiment Design

**summary:** The evaluation uses paired verifier and never-rewarded behavioral outcomes to estimate delta and construct cluster-aware uncertainty intervals and checkpoint trajectories. Calibration simulations, blinded mutations, crossed reward/specification experiments, and independently labeled mechanism corpora test coverage, sensitivity, trajectory discrimination, and sound decomposition of vacuity and empty-domain failures.

**datasets:**

-
  **name:** Paired Checkpoint Evaluation Panel

  **justification:** Common held-out tasks, paired V-B judgments, multiple seeds, reward arms, specification sources, and checkpoints stress dependence-aware delta estimation and trajectory reproducibility.
-
  **name:** Dependence-Preserving Delta Simulation Bank

  **justification:** Resampling observed task sizes and V-B dependence permits planted-gap coverage checks under conditions where an unpaired estimator can misstate uncertainty.
-
  **name:** Blinded Intent-Violation Mutation Suite

  **justification:** Human-validated mutations provide known behavioral violations that may still pass reward-visible tests, directly stressing evaluator independence and sensitivity.
-
  **name:** Crossed-Mechanism Calibration Corpus

  **justification:** Balanced single and co-occurring mechanisms expose failures hidden by mutually exclusive labels and support non-circular multi-label evaluation.
-
  **name:** Vacuity-Empty-Domain Challenge Set

  **justification:** The four-way crossed design separates two easily conflated failure modes and supplies controlled positives and negatives for precision-recall testing.

**baselines:**

-
  **name:** Unpaired Delta Interval

  **justification:** A same-budget uncertainty sanity check showing whether preserving V-B pairing contributes measurable precision.
-
  **name:** Reward-Visible Tests

  **justification:** A leakage-prone diagnostic comparator for testing whether the independent evaluator detects violations unavailable to the reward signal.
-
  **name:** Trusted Fixed Specifications

  **justification:** A controlled-source comparison that tests whether widening is specific to generated specifications rather than generic training drift.
-
  **name:** Binary-Verifier and Structured-VC Proof-Only Arms

  **justification:** These isolate the reward-signal contrast required to interpret the hybrid arm's delta and verification-rate trajectory.
-
  **name:** Mutually Exclusive Syntactic Classifier

  **justification:** A structural sanity check for whether multi-label semantic auditing is necessary on co-occurring mechanisms.
-
  **name:** Rewarded-Verifier-Output-Only Classifier

  **justification:** Tests whether vacuity and empty-domain labels contain information beyond the rewarded verifier's pass/fail outcome.

**research questions:**

-
  **tier:** mechanism

  **rq id:** rq-1

  **setup:** Run N=10,000 Monte Carlo replicates in each of 12 cells crossing planted delta and observed V-B dependence regimes. Each replicate preserves the observed task-size vector and marginal rates; compare task-stratified paired-bootstrap intervals for mean(V-B) with unpaired-bootstrap intervals using the same numbers of V and B judgments. This N limits Monte Carlo standard error near 95% coverage to about 0.22 percentage points. Apply coverage-equivalence and paired width-ratio tests.

  **metrics:** Empirical coverage, mean and median interval width, width ratio, Monte Carlo standard error, and failure rates by task size and V-B dependence.

  **description:** Does the paired estimator provide calibrated, more precise uncertainty intervals for delta under realistic verifier-behavioral dependence?

  **expected outcome:** Every simulation cell has coverage within 90-98%, and the paired-to-unpaired mean interval-width ratio is at most 0.85.

  **statistical test:** Exact-binomial TOST for coverage within [0.90, 0.98] and a one-sided paired-bootstrap test that mean width ratio is at most 0.85, with Holm familywise alpha=0.05.

  **target hypotheses:** - In calibration simulations preserving observed task sizes and V-B dependence, nominal 95% intervals will cover planted delta in 90-98% of runs and be at least 15% narrower than unpaired intervals at the same evaluation budget.

  **sample size rationale:** N=10,000 replicates per cell precisely resolves the 90-98% coverage region; 12 cells cover null, moderate, and large gaps under weak through strong dependence.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-2

  **setup:** Construct N=500 independently adjudicated intent-violating mutations, balanced across task families and mutation mechanisms. Freeze E before evaluation, blind adjudicators and evaluator operators to reward-visible outcomes, and run E and the visible tests on every mutation with equal budgets. N=500 provides roughly 3-percentage-point precision around 90% sensitivity and supports paired threshold testing.

  **metrics:** Mutation-level detection rate, paired detection difference, discordant-pair counts, and sensitivity by task family and mutation mechanism.

  **description:** Is the independent behavioral evaluator sensitive to intent violations that reward-visible tests systematically miss?

  **expected outcome:** E's detection-rate lower bound is at least 0.90 and the lower bound on its paired advantage is at least 0.20.

  **statistical test:** Intersection-union test using a one-sided exact-binomial lower bound for E sensitivity and a one-sided paired-score interval for the E-minus-visible-test difference, with alpha=0.05.

  **target hypotheses:** - On blinded, human-validated intent-violating program mutations, E will detect at least 90% of violations and exceed the detection rate of reward-visible tests by at least 20 percentage points.

  **sample size rationale:** N=500 gives a 95% binomial half-width below 3 percentage points near 90% detection and retains at least 100 examples in each major mutation stratum.

  **target sub problem id:** sp-1
-
  **tier:** mechanism

  **rq id:** rq-3

  **setup:** Train the binary-verifier and structured-verification-condition proof-only arms under generated and trusted fixed specifications using N=20 paired random seeds. At 11 preregistered checkpoints, evaluate each run on the same N=2,000 held-out tasks with paired V and never-rewarded B judgments; vary only reward arm and specification source. Estimate delta=mean(V-B) and fit a seed- and task-clustered checkpoint model, followed by final-minus-zero contrasts. The sample sizes target stable seed-level contrasts while limiting task-sampling error.

  **metrics:** Paired delta by checkpoint, final-minus-zero change, generated-minus-fixed difference-in-change, verification rate, behavioral correctness rate, and simultaneous confidence intervals.

  **description:** Does the estimated delta trajectory distinguish widening under generated specifications from stability under trusted fixed specifications?

  **expected outcome:** For both proof-only arms, generated-specification delta increases by at least 0.08, its difference-in-change versus fixed specifications is at least 0.05, and the fixed-specification change is equivalent within plus or minus 0.03.

  **statistical test:** Simultaneous cluster-bootstrap one-sided tests for generated-arm changes and generated-versus-fixed change contrasts, plus TOST for each fixed-arm change within [-0.03, 0.03], with Holm familywise alpha=0.05.

  **target hypotheses:** - By the final checkpoint, delta in each generated-specification proof-only arm will increase by at least 8 percentage points from step zero and by at least 5 points more than its fixed-specification counterpart, whose change will remain within plus or minus 3 points.

  **sample size rationale:** N=20 seeds captures training variability; N=2,000 tasks per checkpoint gives at most about 2.2-percentage-point standard error for a single bounded delta estimate before pooling across seeds.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-4

  **setup:** Using N=20 paired seeds and the same N=2,000 held-out tasks at each of 11 checkpoints, compare the hybrid proof-plus-execution arm with the binary-verifier and structured-verification-condition proof-only arms under generated specifications. Hold initialization schedule, task sampling, evaluation tests, and compute budget fixed. Use clustered bootstrap contrasts that repeat the data-dependent selection of the proof-only arm with the higher final verification rate.

  **metrics:** Final paired delta contrasts, checkpoint delta trajectories, final verification-rate difference, behavioral correctness, and seed-level confidence intervals.

  **description:** Under generated specifications, does the delta trajectory show the predicted hybrid-reward reduction without a material loss in verification rate?

  **expected outcome:** The hybrid arm's final delta is at least 0.05 below each proof-only arm, and its final verification-rate difference from the better proof-only arm lies within [-0.03, 0.03].

  **statistical test:** Intersection-union cluster-bootstrap tests for both delta-reduction margins and TOST for the hybrid verification rate within plus or minus 0.03 of the selected better proof-only arm, with simultaneous alpha=0.05.

  **target hypotheses:** - Under generated specifications, the hybrid arm's final delta will be at least 5 percentage points lower than both proof-only arms while its verification rate remains within 3 points of the better proof-only arm.

  **sample size rationale:** N=20 paired seeds estimates between-training variability, while N=2,000 common tasks reduces evaluation noise and enables paired comparisons of five-percentage-point delta differences.

  **target sub problem id:** sp-2
-
  **tier:** mechanism

  **rq id:** rq-5

  **setup:** Create N=2,400 independently labeled programs balanced over eight preregistered strata containing no mechanism, single mechanisms, and co-occurring mechanisms. Use 800 cases for audit calibration and lock all rules before evaluating the remaining 1,600 cases. Fit the mutually exclusive syntactic classifier on the same 800 cases and evaluate both systems on identical locked cases. Independent semantic adjudication excludes audit and reward outputs, preventing circular labels.

  **metrics:** Per-label precision, recall, and F1; macro-F1; exact-label-set accuracy; co-occurrence error rate; and paired metric differences.

  **description:** Can the multi-label audit accurately separate individual and co-occurring hacking mechanisms rather than forcing mutually exclusive explanations?

  **expected outcome:** The audit's lower confidence bounds are at least 0.85 for macro-F1 and 0.75 for exact-label-set accuracy, and both paired improvements have lower bounds of at least 0.15.

  **statistical test:** Stratified paired bootstrap with 10,000 resamples for one-sided threshold and audit-minus-classifier margin tests, using Holm familywise alpha=0.05.

  **target hypotheses:** - On the crossed-mechanism calibration corpus, the audit will achieve at least 0.85 macro-F1 and 0.75 exact-label-set accuracy, exceeding a mutually exclusive syntactic classifier by at least 0.15 on both metrics.

  **sample size rationale:** N=1,600 locked cases supplies 200 cases per label-set stratum, supporting stable macro-F1 and exact-set estimates; 800 separate cases permit calibration without test leakage.

  **target sub problem id:** sp-3
-
  **tier:** mechanism

  **rq id:** rq-6

  **setup:** Evaluate locked audit rules on N=1,500 independently adjudicated programs: 375 empty-domain only, 375 vacuity only, 375 both, and 375 neither. Apply the audit and a classifier restricted to rewarded-verifier output to every case; hold program text, verifier execution, and label prevalence fixed. N=1,500 yields 750 positives and 750 negatives per focal label. Use exact precision/recall bounds and paired recall comparisons.

  **metrics:** Label-specific precision, recall, false-positive rate, paired recall advantage, exact joint-label accuracy, and confusion among empty-only, vacuous-only, both, and neither.

  **description:** Does the audit identify empty precondition domains and vacuity separately with high precision and recall beyond what verifier output alone reveals?

  **expected outcome:** For both empty-domain and vacuity labels, lower confidence bounds are at least 0.90 for recall and 0.95 for precision, and the recall-advantage lower bound over verifier-output-only classification is at least 0.20.

  **statistical test:** One-sided Clopper-Pearson bounds for each label's precision and recall plus paired stratified-bootstrap tests for recall advantages, with Holm familywise alpha=0.05.

  **target hypotheses:** - Empty-domain and vacuity labels will each achieve at least 0.90 recall at 0.95 precision, with recall at least 20 percentage points above classification from rewarded-verifier output alone.

  **sample size rationale:** With 750 positives per label, the 95% half-width near 90% recall is about 2.2 percentage points, while the balanced negative set makes 95% precision meaningfully testable.

  **target sub problem id:** sp-3
