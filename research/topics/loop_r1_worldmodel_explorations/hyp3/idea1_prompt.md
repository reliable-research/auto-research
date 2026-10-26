# Deep Research Plan: Prover-Derived Supervision for Trustworthy Code LLMs

## 1. Research objective

Conduct a rigorous literature and evidence review to determine whether machine-checkable proof supervision can replace or complement execution-based reinforcement learning for code LLMs.

The central question is:

> Under matched data, model and compute budgets, can prover-derived supervision produce stronger, more robust and more transferable code-reasoning capabilities than rewards derived from executing programs on finite test cases?

Separate two prover branches:

1. **Mathematical theorem proving**

   * Lean, Isabelle, Rocq/Coq, HOL, Metamath and related systems.
   * Focuses on proof search, deduction, lemma discovery and mathematical reasoning.

2. **Formal program verification**

   * Loop invariants, Hoare logic, weakest preconditions, symbolic execution, bounded model checking, separation logic and verified code generation.
   * Uses systems such as Z3, Dafny, Verus, Boogie, CBMC, SeaHorn, Frama-C, Liquid Haskell, Lean and Rocq.
   * Focuses on program states, transition semantics and correctness properties.

Do not merge these branches merely because both use a prover. Determine what capabilities each branch teaches and how well those capabilities transfer to code generation, program repair and long-horizon software evolution.

---

## 2. Core hypotheses

### H1: Mathematical-prover transfer

Training with machine-checked mathematical proofs improves general deductive reasoning, proof decomposition, lemma selection and long-chain consistency.

### H2: Program-prover transfer

Training with formal program-verification obligations directly improves state-transition reasoning, loop-invariant generation, semantic equivalence, verified code generation and program repair.

### H3: Domain-specific advantage

Under matched training budgets, program-verification supervision transfers more strongly to software-engineering tasks than mathematical-proof supervision because it explicitly represents program states and transition relations.

### H4: Runtime-reward replacement

For formally expressible properties, program-prover rewards can replace test-execution rewards while providing stronger correctness evidence, better credit assignment and fewer program rollouts.

### H5: Hybrid supervision

When specifications are incomplete, combining formal proof signals with runtime counterexamples outperforms either prover-only or runtime-only supervision.

### H6: Learned capability versus external scaffolding

Prover-oriented training produces a capability retained in model parameters, rather than an improvement that exists only while the prover remains available during inference.

---

## 3. Required distinctions

Classify every relevant work along the following axes.

### 3.1 Source of supervision

* Human annotation
* Token-level SFT
* Final test outcome
* Execution trace or intermediate runtime state
* Self-generated tests
* Static-analysis output
* Binary formal-verification result
* Structured verification-condition result
* Proof-state transition
* Kernel-checked proof
* Counterexample or countermodel
* Hybrid runtime and formal evidence

### 3.2 Stage where the prover is used

* Dataset construction
* Supervised fine-tuning
* Rejection sampling
* Reinforcement learning
* Process-reward-model training
* Inference-time search
* Output filtering or reranking
* Final certification

### 3.3 What actually learns

* Base language-model parameters
* LoRA or adapter parameters
* Reward/process verifier
* Prompt-repair policy
* Agent controller
* Search strategy
* Nothing: prover is used only as a final checker

### 3.4 Strength of evidence

Use these labels:

* **A — Direct matched evidence:** same base model, data, compute and algorithm; only prover supervision changes.
* **B — Partial causal evidence:** meaningful ablation isolates proof supervision but some factors remain unmatched.
* **C — System evidence:** prover-guided system improves, but training and scaffolding effects are entangled.
* **D — Enabling infrastructure:** benchmark, dataset, verifier or toolchain without a causal capability comparison.
* **E — Position or survey evidence:** conceptual argument without adequate experiments.

Do not treat “the verifier accepts the output” as evidence that the model learned prover capability.

---

## 4. Literature-search scope

Search work from 2020 through August 2026, while including older foundational work when necessary.

Prioritize:

* peer-reviewed conference and journal papers;
* arXiv or OpenReview preprints with released code, data or detailed experiments;
* official project repositories;
* dissertations and technical reports with substantial empirical results;
* authoritative surveys.

Avoid relying on marketing pages or secondary summaries when the primary paper is available.

### 4.1 Mathematical-prover branch

Search for:

* LLM theorem proving
* reinforcement learning for theorem proving
* RL with Lean/Isabelle/Rocq feedback
* proof-state process rewards
* proof-search credit assignment
* formal proof self-play
* autoformalization
* proof-verifier training
* theorem-proving transfer to general reasoning
* theorem-proving transfer to code generation

Include relevant systems such as AlphaProof, Prover Agent, APOLLO, Draft-Sketch-Prove and comparable work.

### 4.2 Formal-program-verification branch

Search for:

* RL for verified code generation
* formal verifier as reward for code LLMs
* Dafny or Verus reinforcement learning
* verifier-guided code generation
* loop-invariant generation using LLMs
* invariant repair using prover feedback
* SMT-guided code generation
* proof-guided program repair
* semantic-equivalence training
* formal specification and code-agent reliability
* process rewards from verification conditions
* proof-aware program planning

Explicitly examine Re:Form, LORIS, LaM4Inv, Clause2Inv, P³, AlphaVerus, Clover, CLEVER, Proof2Silicon/PREFACE, FVSpec and related work.

### 4.3 Runtime and execution-reward branch

Search for:

* RL from execution feedback for code
* unit-test reward for code generation
* execution-trace supervision
* white-box execution rewards
* self-generated tests
* multi-turn code-agent RL
* program-repair agents and test overfitting
* semantic correctness beyond tests

Explicitly examine RLEF, ExecVerify, ReVeal, CodeRL and other representative execution-grounded systems.

### 4.4 Bridge and transfer work

Search specifically for papers that:

* train on formal proofs and evaluate ordinary code generation;
* train on verified programs and evaluate program repair;
* use semantic-equivalence proofs for downstream code reasoning;
* compare proof feedback with execution feedback;
* evaluate without prover access at inference;
* report out-of-domain or cross-language transfer;
* measure whether RL expands capability or only compresses search.

Give special attention to semantic-equivalence self-play using Liquid Haskell and execution-free or semi-formal code-reasoning systems.

---

## 5. Research questions

Answer each question with evidence rather than speculation.

### RQ1: Existing prior art

Has formal verification already been used as:

* a binary RL reward;
* a structured process reward;
* a source of SFT data;
* a rejection-sampling filter;
* an inference-time repair mechanism;
* a final certification tool?

### RQ2: Mathematical proof versus program proof

What capabilities are acquired from mathematical theorem proving, and which are acquired from program verification?

Is there evidence that either transfers to:

* code generation;
* code execution reasoning;
* fault localization;
* semantic equivalence;
* program repair;
* repository-scale evolution?

### RQ3: Proof reward versus execution reward

Under what conditions does a formal prover provide a stronger signal than test execution?

Compare:

* coverage;
* latency;
* sparsity;
* localization;
* cost;
* scalability;
* specification requirements;
* vulnerability to reward hacking.

### RQ4: Structured credit assignment

What prover outputs can be converted into dense training signals?

Investigate:

* proof-state progress;
* solved subgoals;
* failed verification conditions;
* initiation;
* loop-body preservation;
* postcondition sufficiency;
* invariant strength;
* countermodels;
* unsat cores;
* proof length;
* lemma usefulness;
* solver time and difficulty.

### RQ5: Capability acquisition

Does prover training produce new reasoning capability, or does it merely increase the probability of already-sampleable solutions?

Look for:

* pass@k curves before and after training;
* inference-budget-matched results;
* verifier-call efficiency;
* performance with the prover removed;
* novel proof strategies;
* out-of-distribution success;
* cross-domain transfer.

### RQ6: Specification risk

How often do systems exploit incomplete or weak specifications?

Study:

* specification hacking;
* vacuous proofs;
* trivial invariants;
* inconsistent preconditions;
* underspecified behavior;
* incorrect program-to-logic translations;
* solver unsoundness or modeling gaps.

Determine how runtime evidence, metamorphic testing, differential testing or human review can audit specification adequacy.

### RQ7: Real-world scalability

Can prover-based supervision extend beyond short algorithmic programs to:

* C/C++ with pointers and arrays;
* heap-manipulating programs;
* concurrency;
* external libraries;
* repository-level repair;
* dependency upgrades;
* long-horizon software evolution?

Identify the exact technical blockers.

---

## 6. Evidence-extraction schema

For every included paper, record:

| Field           | Required information                                        |
| --------------- | ----------------------------------------------------------- |
| Citation        | Title, authors, year, venue and direct link                 |
| Branch          | Mathematical proof, program verification, runtime or hybrid |
| Task            | Exact training and evaluation task                          |
| Formal system   | Lean, Dafny, Z3, Verus, etc.                                |
| Base model      | Model family and parameter size                             |
| Training method | SFT, GRPO, PPO, rejection sampling, search, etc.            |
| Reward          | Exact reward formulation                                    |
| Data            | Size, origin, synthesis and filtering                       |
| Baseline        | What control condition was used                             |
| Compute         | Training and inference budgets when reported                |
| Prover access   | Training, inference or both                                 |
| Main result     | Exact quantitative improvement                              |
| Transfer        | Cross-task, cross-language or out-of-domain result          |
| Robustness      | Perturbations, unseen templates or adversarial tests        |
| Limitations     | Key threats to validity                                     |
| Evidence class  | A, B, C, D or E                                             |
| Relevance       | How it supports or weakens the hypotheses                   |

Do not report a numerical result without checking the original source and its evaluation setting.

---

## 7. Required comparison tables

Produce at least the following tables.

### Table A: Two prover branches

Compare mathematical proving and program verification in terms of representation, reward, tools, acquired capability, transfer targets and limitations.

### Table B: Reward taxonomy

Compare:

1. unit-test outcome;
2. execution trace;
3. self-generated verification;
4. binary prover result;
5. structured proof-process reward;
6. hybrid proof and execution reward.

### Table C: Closest prior work

Rank the 15–25 closest papers by overlap with the proposed idea.

### Table D: Causal evidence

List only papers containing an ablation or matched comparison capable of isolating prover supervision.

### Table E: Available datasets and benchmarks

Include mathematical proof, verified code, loop invariant, program repair and long-horizon evolution benchmarks.

### Table F: Open-source implementation readiness

Identify available code, models, datasets, licences, supported languages and estimated reproduction difficulty.

---

## 8. Novelty audit

Evaluate the following candidate contributions independently:

1. First use of formal verification as an RL reward.
2. First structured verification-condition reward for code LLM training.
3. First matched comparison between execution and proof rewards.
4. First comparison between mathematical-proof and program-proof supervision.
5. First study of prover-trained capability with the prover removed at inference.
6. First transfer study from loop-invariant proof training to ordinary code generation and repair.
7. First hybrid reward using proof for universal certification and execution for counterexample discovery.
8. First program-verification RL study at both 0.6B and 1.7B scales.
9. First systematic audit of specification hacking in prover-trained code LLMs.

For each candidate, return:

* novelty status: likely novel, partially explored, or already established;
* closest conflicting paper;
* precise remaining gap;
* safer claim suitable for a paper;
* evidence needed to defend the claim.

Do not use “first” unless the search provides strong support.

---

## 9. Recommended experimental design

Based on the review, design a controlled experiment using the same 0.6B and 1.7B base-model families.

Minimum experimental groups:

| Group | Supervision                                  |
| ----- | -------------------------------------------- |
| G0    | Code SFT baseline                            |
| G1    | Final unit-test reward                       |
| G2    | Execution-state/trace reward                 |
| G3    | Mathematical-proof reward                    |
| G4    | Binary program-verifier reward               |
| G5    | Structured program-proof reward              |
| G6    | Mathematical proof followed by program proof |
| G7    | Structured program proof plus runtime reward |

Match as closely as possible:

* training tokens;
* number of sampled completions;
* optimizer;
* RL algorithm;
* wall-clock or FLOP budget;
* curriculum;
* base model;
* inference budget.

Evaluate in two modes:

1. prover/tool available at inference;
2. no prover/tool available at inference.

Include:

* in-domain verification;
* unseen loop families;
* semantic-preserving transformations;
* variable renaming;
* nonlinear arithmetic;
* arrays and pointers;
* semantic equivalence;
* code generation;
* Defects4C-style program repair;
* a tractable long-horizon evolution subset.

Define success and falsification criteria before running experiments.

---

## 10. Required final deliverables

Produce the following files:

### `deep_research_report.md`

A complete critical survey containing:

* executive conclusion;
* two-branch prover taxonomy;
* runtime-versus-proof comparison;
* closest prior work;
* evidence tables;
* novelty audit;
* research gaps;
* recommended research position.

### `literature_matrix.csv`

One row per paper using the complete evidence-extraction schema.

### `hypotheses.md`

For each hypothesis:

* rationale;
* supporting evidence;
* contradicting evidence;
* required experiment;
* success criterion;
* falsification criterion.

### `experiment_plan.md`

A reproducible plan for the 0.6B and 1.7B experiments, including datasets, reward definitions, baselines, metrics, ablations, compute accounting and stop conditions.

### `novelty_and_risk.md`

Include:

* defensible novelty claims;
* claims that should be avoided;
* closest competing work;
* specification-hacking risks;
* formalization bottlenecks;
* expected reviewer objections;
* evidence required to answer each objection.

### `references.bib`

Verified BibTeX entries for all cited primary sources.

---

## 11. Quality requirements

* Prefer primary sources.
* Verify every central claim against the full paper.
* Separate peer-reviewed work from preprints and theses.
* Record paper version and publication date.
* Deduplicate conference and arXiv versions.
* Do not infer model training when the paper only uses inference-time feedback.
* Do not infer universal correctness from test passing.
* Do not infer intended correctness from prover acceptance.
* Distinguish mathematical proofs from program-behavior proofs.
* Report negative results and weak evidence.
* Explicitly identify missing baselines and confounding variables.
* State uncertainty when information is unavailable.
* Make the final verdict falsifiable.

---

## 12. Final decision the research must support

End the report by answering:

1. Is the proposed direction genuinely novel?
2. Which component is novel: reward source, credit assignment, transfer study, hybrid design or evaluation?
3. Should the project focus on replacing runtime RL, augmenting it, or comparing both?
4. Should mathematical proving be used as pretraining, a control group or excluded from the first PoC?
5. What is the smallest experiment capable of validating or falsifying the central hypothesis?
6. What result would be strong enough for a credible software-engineering, programming-languages or machine-learning paper?

The final recommendation must select one concrete PoC rather than presenting an unranked list of possibilities.


