# Recommended research idea

## ProofWorld: Learning Program Semantics through Verification-Condition Transitions

### One-sentence idea

> Train a code LLM to predict and improve a program’s symbolic proof state—precondition, invariant initiation, loop preservation and postcondition sufficiency—using machine-checked prover feedback, and test whether this produces stronger tool-free code reasoning than learning from concrete execution traces.

This combines your three existing directions:

1. **Execution grounding:** predict concrete program-state transitions.
2. **Formal verification:** reason over symbolic states covering many executions.
3. **Semantic credit assignment:** identify exactly which proof obligation fails instead of assigning one delayed reward.

---

# 1. Core motivation

Current code-model training has three levels:

[
\text{token prediction}
\rightarrow
\text{execution-state prediction}
\rightarrow
\text{symbolic proof-state prediction}.
]

## Token prediction

The model learns:

[
p(x_{t+1}\mid x_{\leq t})
]

but token similarity does not imply semantic correctness.

## Execution-state learning

Methods such as ExecVerify teach:

[
(s_t,\text{statement}*t)\rightarrow s*{t+1}
]

where (s_t) is one concrete runtime state.

This is semantically grounded, but each trace represents only a particular input and execution path.

## Proof-state learning

Your proposed model learns:

[
(Z_t,a_t)\rightarrow Z_{t+1}
]

where:

* (Z_t) is the symbolic proof state;
* (a_t) is a proposed invariant, lemma, annotation or code edit;
* (Z_{t+1}) contains the remaining or transformed verification obligations.

Unlike one concrete trace, a symbolic state can represent many or all executions admitted by the formal model.

---

# 2. The key research question

> Does learning symbolic proof-state transitions teach a stronger representation of program semantics than learning concrete execution-state transitions?

This is more precise and novel than:

* “use a prover as an RL reward”;
* “formal verification is better than testing”;
* “generate verified programs”;
* “use verifier feedback to repair an invariant.”

The novelty is the conversion of a verifier’s internal semantic structure into a **program world model and process-level training signal**.

---

# 3. Two world models

## Concrete execution world model

For input (x_i), execution produces:

[
s_0^{(i)}
\xrightarrow{c_1}
s_1^{(i)}
\xrightarrow{c_2}
\cdots
\xrightarrow{c_T}
s_T^{(i)}.
]

The model predicts:

* next statement;
* next variable values;
* next variable types;
* final output.

Its limitation is input dependence:

[
s_t^{(i)}\neq s_t^{(j)}
]

for different executions.

## Symbolic proof world model

A verifier constructs a symbolic state:

[
Z_t=
{
O_{\text{init}},
O_{\text{preserve}},
O_{\text{post}},
O_{\text{safety}},
O_{\text{termination}}
}.
]

After the model proposes action (a_t), such as a new invariant, the prover computes:

[
Z_{t+1}
=======

\operatorname{ProverTransition}(Z_t,a_t).
]

Each obligation receives a categorical result:

[
z_j\in
{
\text{proved},
\text{counterexample},
\text{unknown},
\text{timeout},
\text{invalid}
}.
]

The model learns which action changes which semantic obligation.

This is analogous to a world model, except that the “world” is the program’s symbolic semantics rather than one runtime trajectory.

---

# 4. Loop-invariant instantiation

For:

```c
while (G) {
    S;
}
```

with precondition (P), postcondition (Q), transition relation (T_S) and candidate invariant (I), generate the canonical obligations.

## Initiation

[
O_{\text{init}}:
P(s)\Rightarrow I(s)
]

## Preservation

[
O_{\text{preserve}}:
I(s)\land G(s)\land T_S(s,s')
\Rightarrow I(s')
]

## Postcondition sufficiency

[
O_{\text{post}}:
I(s)\land\neg G(s)\Rightarrow Q(s)
]

## Safety

[
O_{\text{safety}}:
I(s)\land G(s)\Rightarrow
\operatorname{Safe}(S,s)
]

## Termination, when required

[
O_{\text{term}}:
I(s)\land G(s)
\Rightarrow
V(s')<V(s)\land V(s)\geq 0.
]

The important point is that these are not arbitrary natural-language reasoning labels. They are machine-checkable semantic decomposition units.

---

# 5. Proposed learning task

For each training instance, the model receives:

* source program;
* precondition and postcondition;
* current invariant or annotation;
* named verification obligations;
* prover status and optional countermodel.

It performs one or more tasks.

## Task A: Proof-state prediction

Before calling the prover, predict:

* which obligations will succeed;
* which obligation will fail;
* why it will fail;
* whether failure represents a counterexample, unknown or timeout.

This teaches the model to approximate the prover’s semantic judgment.

## Task B: Proof-state transition prediction

Given a proposed edit, predict:

[
\hat Z_{t+1}
============

f_\theta(P,Z_t,a_t).
]

Then compare (\hat Z_{t+1}) with the actual prover result.

## Task C: Semantic action generation

Generate an invariant, lemma or code edit that moves the proof state toward full verification.

## Task D: Countermodel-guided repair

When preservation fails, use the countermodel to identify which relationship is missing from the invariant.

## Task E: Tool-free distillation

After prover-guided training, remove the prover and evaluate whether the model retains improved semantic capability.

---

# 6. Proposed training objective

A combined objective can be:

[
\mathcal L
==========

\lambda_{\text{gen}}\mathcal L_{\text{generation}}
+
\lambda_{\text{state}}\mathcal L_{\text{proof-state}}
+
\lambda_{\text{trans}}\mathcal L_{\text{transition}}
+
\lambda_{\text{policy}}\mathcal L_{\text{policy}}.
]

## Generation loss

Generate the invariant, proof step or repaired program:

[
\mathcal L_{\text{generation}}
==============================

-\log p_\theta(a_t\mid P,Z_t).
]

## Proof-state prediction loss

Predict each obligation’s categorical result:

[
\mathcal L_{\text{proof-state}}
===============================

-\sum_j
\log p_\theta(z_j\mid P,I).
]

## Transition loss

Predict how an edit changes the proof state:

[
\mathcal L_{\text{transition}}
==============================

d(\hat Z_{t+1},Z_{t+1}).
]

## Policy reward

Reward actions that discharge a fixed canonical obligation set:

[
R_{\text{VC}}
=============

\frac{1}{|\mathcal O|}
\sum_{O_j\in\mathcal O}
r(z_j).
]

Use different values for:

[
r(z_j)=
\begin{cases}
1 & \text{proved}\
0 & \text{counterexample}\
-\eta_u & \text{unknown}\
-\eta_t & \text{timeout}\
-\eta_i & \text{invalid}
\end{cases}
]

Do not merge counterexamples, solver unknowns and timeouts into one negative outcome.

---

# 7. Why this is more than binary prover RL

Existing verifier RL often provides:

[
R=
\mathbb{1}[\text{program verifies}].
]

That reward is rigorous but still sparse.

ProofWorld provides:

[
R=
[
R_{\text{parse}},
R_{\text{type}},
R_{\text{init}},
R_{\text{preserve}},
R_{\text{post}},
R_{\text{safety}},
R_{\text{termination}},
R_{\text{full}}
].
]

This can tell the model:

```text
Invariant is initially valid.
Invariant is not inductive.
Invariant would establish the postcondition.
The missing knowledge concerns y after one loop transition.
```

The contribution is therefore:

> Move from verification outcome reward to verification-process learning.

---

# 8. Main hypotheses

## H1 — Symbolic-state learning

> Training on verification-condition transitions improves program-state reasoning more than token-level supervision.

## H2 — Proof versus execution process

> Under matched budgets, proof-process supervision produces better distribution-shift robustness than equally dense execution-process supervision for formally expressible properties.

The decisive comparison is:

[
\text{ExecVerify-style state learning}
\quad\text{vs.}\quad
\text{ProofWorld symbolic-state learning}.
]

## H3 — Prover-free internalization

> Improvements persist when the prover is removed at inference.

This distinguishes learned capability from an effective verifier-in-the-loop agent.

## H4 — Cross-representation transfer

> Training on Dafny or SMT verification conditions improves reasoning about equivalent ordinary C/Python programs.

## H5 — Hybrid advantage

> Proof supervision plus execution counterexamples performs best when the formal specification is incomplete.

## H6 — Mathematical versus program proof

> Program-proof training transfers more strongly to code reasoning than mathematical-proof training because it represents mutation and transition semantics.

This should be a second-stage study, not the first PoC.

---

# 9. Experimental arms

Start from one shared SFT checkpoint and the same underlying programming problems.

| Arm | Training signal                     | Purpose                            |
| --- | ----------------------------------- | ---------------------------------- |
| G0  | Code SFT only                       | Base control                       |
| G1  | Final test result                   | Sparse execution reward            |
| G2  | Execution-state transitions         | Strong dense-runtime baseline      |
| G3  | Binary verifier result              | Existing proof-outcome baseline    |
| G4  | VC state and transition supervision | Main ProofWorld method             |
| G5  | VC supervision plus execution       | Hybrid method                      |
| G6  | Mathematical proof supervision      | General-proof control, later phase |
| G7  | Math proof → program proof          | Curriculum study, later phase      |

The primary causal comparison is:

[
\boxed{G2\text{ versus }G4}
]

not merely G1 versus G3.

---

# 10. Paired-oracle experimental design

For each candidate generated by the shared starting policy:

1. Run the candidate on the fixed test harness.
2. Record final outcomes and intermediate execution states.
3. Run the formal verifier on the same candidate.
4. Record all named verification-condition outcomes.
5. Place the same candidate into the experience pools for all applicable arms.
6. Train separate policy copies with matched sampled tokens and optimizer settings.

This prevents the execution and proof conditions from receiving different candidate distributions.

---

# 11. Smallest decisive PoC

## Phase 1: 0.6B feasibility

Use a single-function Dafny corpus containing:

* linear integer loops;
* polynomial loops;
* branches;
* arrays;
* explicit preconditions and postconditions;
* known valid invariants;
* executable reference implementations.

Train only four initial groups:

| Group | Signal                    |
| ----- | ------------------------- |
| G0    | SFT                       |
| G1    | Final execution reward    |
| G3    | Binary verifier reward    |
| G4    | Structured VC supervision |

This determines whether VC decomposition adds value beyond final proof acceptance.

## Phase 2: publication-grade comparison

Add:

* G2 dense execution-state supervision;
* G5 hybrid proof and execution;
* 1.7B replication.

This tests whether proof-process supervision beats the strongest execution baseline rather than a weak test-only baseline.

## Phase 3: transfer

Evaluate without tools on:

* unseen loop schemas;
* invariant selection and repair;
* execution reasoning;
* semantic equivalence;
* ordinary Python/C representations;
* selected Defects4C cases.

---

# 12. Primary evaluation

## In-domain formal correctness

* full verification rate;
* initiation success;
* preservation success;
* postcondition success;
* correct invariant rate;
* verifier calls per solution.

## Prover-free semantic capability

* select the correct invariant without verifier access;
* predict which VC will fail;
* repair an invariant without countermodel feedback;
* determine semantic equivalence;
* predict program outputs and state transitions;
* generate correct code from specifications;
* repair ordinary code.

## Robustness

Apply:

* variable renaming;
* dead-code insertion;
* equivalent loop rewrites;
* reordered independent statements;
* changed constants;
* unseen invariant templates;
* altered surface syntax;
* translation from Dafny into C or Python.

## Efficiency

Measure:

* sampled tokens;
* GPU time;
* solver CPU time;
* execution time;
* number of program executions;
* verifier calls;
* wall-clock time;
* correct solutions per total compute.

Do not assume proof is cheaper. Establish a phase diagram showing when each oracle is preferable.

---

# 13. Specification-hacking audit

Formal acceptance does not guarantee intended correctness. Construct an adversarial set containing:

* `ensures true`;
* overly strong preconditions;
* contradictory assumptions;
* missing frame conditions;
* vacuous invariants;
* contracts omitting important outputs;
* implementations satisfying the contract while violating natural-language intent.

Report separately:

[
\text{formal verification rate}
]

and:

[
\text{independent behavioral correctness}.
]

A proof-trained model succeeds only if it improves both without learning to weaken or exploit the specification.

---

# 14. Falsification criteria

The central hypothesis is weakened or rejected if:

* G4 improves only when the verifier remains available;
* G4 cannot beat G3, meaning VC decomposition adds no value;
* G4 cannot beat G2 under matched compute;
* formal acceptance rises but hidden-test correctness does not;
* gains disappear under renaming or loop transformations;
* the model learns Dafny templates rather than transferable semantics;
* solver cost makes the method consistently less efficient;
* improvements come from specification exploitation.

A negative result would still be useful if it establishes the boundary between execution and proof supervision.

---

# 15. Defensible novelty

Do not claim:

> First use of a formal verifier as an RL reward.

Instead claim:

> We model deductive program verification as a symbolic state-transition environment and use verification-condition transitions as machine-checkable process supervision for code-model post-training.

The three strongest contributions are:

1. **Proof-state world modeling**

   Represent program reasoning as transitions between symbolic verification states.

2. **VC-level semantic credit assignment**

   Train on initiation, preservation, exit, postcondition and safety obligations rather than a single verifier outcome.

3. **Matched proof-versus-execution comparison**

   Determine whether symbolic proof-state learning transfers more robustly than concrete execution-state learning when the external tools are removed.

---

# 16. Recommended title

**ProofWorld: Learning Program Semantics through Verification-Condition Transitions**

Alternatives:

* **Execution States or Proof States? Learning Semantic World Models for Code**
* **Beyond Test-Case RL: Proof Obligations as Semantic Process Supervision**
* **From Runtime Traces to Symbolic Proof States for Trustworthy Code LLMs**

---

# 17. Paper-level central claim

> Concrete execution traces teach what happened for selected inputs. Verification conditions describe what must remain true across the represented program state space. ProofWorld trains code models to predict and improve these symbolic proof states. Under matched conditions, we test whether this supervision creates more robust and transferable program-semantic capability than execution outcomes or execution-state traces.

This is the research idea I would select from the three reports. It preserves your original objective—reducing dependence on expensive execution rollouts—but moves the novelty beyond existing binary verifier RL and connects directly to your earlier world-model and state-transition research.



# ProofWorld hypothesis list and evaluation criteria

## Global experimental controls

All hypotheses require:

* same base-model family at 0.6B and 1.7B;
* same initial SFT checkpoint;
* same training instances and candidate programs;
* matched sampled-token budget;
* same optimizer/RL algorithm where applicable;
* matched inference budget;
* at least three training seeds;
* untouched validation and test sets;
* independent hidden tests not used for rewards;
* fixed, audited specifications for the primary experiment;
* separate accounting of GPU, execution and solver costs.

### Default statistical criterion

Treat a result as supported only when:

1. the improvement is practically meaningful—provisionally at least **3 percentage points absolute** or standardized effect size (d\geq0.2);
2. the 95% confidence interval excludes zero;
3. the direction is consistent across at least two seeds and the aggregate result;
4. it reproduces at 1.7B after being discovered at 0.6B;
5. it does not result from lower compute, easier candidates or specification exploitation.

The final minimum effect should be preregistered after measuring benchmark variance on a pilot split.

---

# H1 — VC decomposition improves credit assignment

## Hypothesis

> Structured verification-condition supervision produces better semantic learning than binary verifier acceptance.

Comparison:

[
G4_{\text{VC labels}}

>

G3_{\text{binary proof}}.
]

## Primary criteria

* higher full-program verification rate;
* higher invariant-generation success;
* fewer verifier calls per solved instance;
* fewer repair iterations;
* higher accuracy identifying the failed VC;
* higher successful-repair rate after a failed proof.

## Supporting result

H1 is supported if G4:

* improves verified solve rate over G3;
* reduces verifier calls or repair rounds;
* correctly distinguishes initiation, preservation and postcondition failures;
* maintains the gain under equal model and solver budgets.

## Falsification criterion

H1 is weakened if:

* G4 does not outperform G3;
* gains disappear under matched oracle cost;
* the model predicts VC labels but cannot use them to repair invariants;
* improvement comes only from longer prompts or additional tokens.

## Necessary ablation

Compare:

* binary verified/failed;
* categorical VC status;
* VC status plus countermodel;
* countermodel alone.

This determines which component creates the gain.

---

# H2 — Proof-state transition learning adds capability

## Hypothesis

> Explicitly learning how candidate edits transform the symbolic proof state provides more benefit than learning static VC labels alone.

Comparison:

[
G5_{\text{ProofWorld transition}}

>

G4_{\text{VC classification}}.
]

## Primary criteria

* proof-state transition prediction accuracy;
* next-action success rate;
* verified solutions within a fixed number of edits;
* reduction in repeated or regressive edits;
* tool-off invariant repair.

## Transition-prediction metric

For canonical obligations:

[
Z_t =
[z_{\text{init}},z_{\text{pres}},z_{\text{post}},z_{\text{safety}},z_{\text{term}}],
]

measure:

* macro-F1 over next-state categories;
* exact-vector accuracy;
* per-obligation transition accuracy;
* calibration of predicted VC outcomes.

## Supporting result

H2 is supported if G5:

* predicts (Z_{t+1}) more accurately than G4;
* selects edits that discharge more failed obligations;
* achieves higher verification and repair rates;
* retains an advantage without the prover.

## Falsification criterion

H2 is weakened if:

* G5 predicts transitions but does not improve generation or repair;
* performance matches G4 after equalizing training tokens;
* improvements exist only when actual (Z_{t+1}) is returned during inference;
* the model learns common error-message patterns rather than semantic transitions.

---

# H3 — Proof-process supervision versus execution-process supervision

## Hypothesis

> For formally specified properties, symbolic proof-state supervision produces stronger OOD semantic generalization than equally dense execution-state supervision.

Comparison:

[
G5_{\text{proof process}}
\quad\text{vs.}\quad
G2_{\text{execution process}}.
]

This is the paper’s central hypothesis.

## Primary endpoint

Tool-off performance on structurally unseen programs:

* unseen loop families;
* changed control-flow structures;
* nonlinear updates;
* arrays;
* new invariant forms;
* semantic-equivalence tasks.

## Secondary endpoints

* full verification rate with tools;
* hidden-test correctness;
* robustness to transformations;
* oracle calls and total compute;
* transfer to ordinary C/Python programs.

## Supporting result

H3 is supported if G5:

* beats G2 on tool-off OOD semantic correctness;
* retains at least comparable ordinary code-generation performance;
* is more robust to semantic-preserving transformations;
* improves independently measured behavior, not only proof acceptance.

## Falsification criterion

The strong hypothesis is rejected if G5:

* consistently loses to G2 under matched compute;
* improves only formal-language tasks;
* cannot transfer outside the verifier’s syntax;
* raises verification rate without improving independent hidden tests.

## Important interpretation

If G5 wins only on universal safety/invariant properties while G2 wins on input-specific behavior, report a phase boundary rather than declaring one oracle universally superior.

---

# H4 — Prover capability is internalized

## Hypothesis

> Some advantage from ProofWorld training remains after removing the prover at inference.

Comparison:

[
G5_{\text{tool-off}}

>

G0,G1,G3,G4_{\text{tool-off}}.
]

## Primary criteria

Without a verifier or execution tool:

* select a valid invariant from candidates;
* predict which VC fails;
* repair an incorrect invariant;
* judge semantic equivalence;
* predict program-state transitions;
* solve ordinary code-generation tasks.

## Retention ratio

Define:

[
\rho_{\text{retain}}
====================

\frac{
\Delta_{\text{tool-off}}
}{
\Delta_{\text{tool-on}}
}.
]

This estimates how much of the system-level gain survives without the tool.

## Supporting result

H4 is supported if:

* G5 remains significantly better than controls tool-off;
* the effect survives unseen syntax and program families;
* the effect reproduces at both model scales;
* retention is not limited to memorized invariant templates.

## Falsification criterion

H4 is rejected if:

* gains vanish when the prover is removed;
* the model improves only at interpreting prover messages;
* performance collapses under identifier renaming or language translation;
* tool-off accuracy is indistinguishable from the shared SFT baseline.

In that case, ProofWorld is an effective agent scaffold but not evidence of stronger internal semantic capability.

---

# H5 — Proof supervision improves semantic robustness

## Hypothesis

> ProofWorld learns program semantics rather than verifier-specific surface patterns.

## Perturbation criteria

Evaluate on:

* variable renaming;
* dead-code insertion;
* equivalent loop rewriting;
* branch restructuring;
* reordered independent statements;
* changed literal distributions;
* reformulated specifications;
* Dafny-to-C/Python translation.

## Robustness metric

For transformation (T):

[
\operatorname{Robustness}(T)
============================

\frac{
\operatorname{Score}(T(x))
}{
\operatorname{Score}(x)
}.
]

Also measure absolute degradation:

[
\Delta_T
========

## \operatorname{Score}(x)

\operatorname{Score}(T(x)).
]

## Supporting result

H5 is supported if G5:

* has smaller degradation than G1–G4;
* preserves semantic decisions across equivalent programs;
* maintains gains on unseen invariant syntax;
* transfers to at least one non-Dafny representation.

## Falsification criterion

H5 is weakened if:

* performance collapses after renaming;
* invariant success depends on familiar templates;
* cross-language transfer is no better than SFT;
* robustness gains disappear after controlling for training-data diversity.

---

# H6 — Hybrid proof and execution supervision is best under incomplete specifications

## Hypothesis

> When specifications omit part of the intended behavior, combining formal proof signals with runtime counterexamples produces better results than proof-only or execution-only supervision.

Comparison:

[
G6_{\text{proof+execution}}

>

G5_{\text{proof}}
\quad\text{and}\quad
G2_{\text{execution}}.
]

## Evaluation conditions

Create two specification regimes:

1. **Complete, audited specifications**
2. **Partial or adversarial specifications**

The second regime should contain:

* weak postconditions;
* overly strong preconditions;
* missing frame conditions;
* omitted edge cases;
* contradictory assumptions;
* vacuous domains;
* contracts that permit obviously unintended implementations.

## Primary criteria

* formal verification rate;
* independent hidden-test pass rate;
* intended-behavior satisfaction;
* specification-hacking rate;
* counterexample discovery rate;
* Pareto performance across proof correctness and behavioral adequacy.

## Supporting result

H6 is supported if G6:

* preserves formal correctness;
* improves hidden behavioral correctness;
* reduces specification exploitation;
* dominates G5 under incomplete specifications;
* does not significantly harm performance with complete specifications.

## Falsification criterion

H6 is weakened if:

* hybrid training adds cost without behavioral gain;
* runtime feedback destabilizes formal correctness;
* it performs no better than simply increasing tests;
* its apparent gain comes from receiving more total supervision.

---

# H7 — Proof supervision can reduce reliance on concrete execution

## Hypothesis

> For formally expressible properties, ProofWorld reaches a target semantic-correctness level using fewer concrete executions than execution-based training.

This is the correct version of the “no execution” hypothesis.

## Efficiency criteria

Measure:

* number of concrete executions;
* verifier calls;
* solver CPU time;
* model-generated tokens;
* GPU training time;
* end-to-end wall time;
* monetary cost;
* correct solutions per unit of compute.

## Efficiency frontier

For correctness target (\tau):

[
C_{\text{oracle}}(\tau)
=======================

\text{total oracle cost required to reach }\tau.
]

Report:

[
\frac{
\Delta\text{tool-off semantic correctness}
}{
\text{total training and oracle compute}
}.
]

## Supporting result

H7 is supported if G5:

* achieves the target with materially fewer concrete executions;
* remains competitive after counting solver cost;
* provides better correctness per total end-to-end cost in at least one important task regime.

## Falsification criterion

H7 is rejected as a general claim if:

* solver costs exceed saved execution costs;
* proof timeouts dominate training;
* test execution is consistently faster at the same correctness level;
* fewer executions do not translate into lower total cost.

A valid result may be a phase diagram:

| Task regime                              | Expected preferred oracle |
| ---------------------------------------- | ------------------------- |
| Cheap deterministic function             | Execution                 |
| Large input space with concise invariant | Proof                     |
| Incomplete specification                 | Hybrid                    |
| Environmental behavior                   | Execution                 |
| Universal safety property                | Proof                     |

---

# H8 — Program proof transfers differently from mathematical proof

## Hypothesis

> Program-verification supervision transfers more strongly to software tasks than mathematical-proof supervision, while mathematical-proof supervision transfers more strongly to theorem proving.

Comparison:

[
G5_{\text{program proof}}
\quad\text{vs.}\quad
G7_{\text{math proof}}.
]

## Matching requirements

Match:

* training tokens;
* model family;
* optimizer;
* number of proof trajectories;
* proof difficulty where possible;
* inference budget.

## Primary criteria

### Mathematical evaluation

* Lean/Isabelle theorem completion;
* lemma selection;
* proof decomposition;
* proof success under new libraries.

### Program evaluation

* loop-invariant synthesis;
* state-transition reasoning;
* semantic equivalence;
* code generation;
* program repair;
* cross-language transfer.

## Supporting result

H8 is supported if:

* G7 wins on mathematical proving;
* G5 wins on program-semantic tasks;
* G5’s program advantage survives tool removal;
* the difference cannot be explained by dataset size or language familiarity.

## Falsification criterion

H8 is weakened if:

* mathematical-proof training matches G5 on code tasks;
* program-proof training provides no domain-specific transfer advantage;
* differences disappear after matching data difficulty.

## Role in project

H8 is a full-paper extension, not part of the first ProofWorld PoC.

---

# H9 — Mathematical-to-program proof curriculum is complementary

## Hypothesis

> Mathematical proof training followed by program-proof training improves proof planning while preserving program-semantic grounding.

Comparison:

[
G8_{\text{math}\rightarrow\text{program}}

>

G5_{\text{program only}}.
]

## Primary criteria

* faster convergence during program-proof training;
* fewer verifier interactions;
* stronger long-horizon proof decomposition;
* improved tool-off program reasoning;
* no loss in ordinary code generation.

## Supporting result

H9 is supported if the curriculum:

* reaches a fixed verification target with less program-proof training;
* improves difficult multi-step or compositional verification;
* retains or improves program-semantic transfer.

## Falsification criterion

H9 is weakened if:

* mathematical pretraining creates no sample-efficiency gain;
* it causes negative transfer from theorem syntax;
* the benefit disappears after controlling for total training tokens;
* program-only training catches up under equal compute.

---

# H10 — ProofWorld does not optimize specification loopholes

## Hypothesis

> Improvements from ProofWorld reflect stronger implementation reasoning rather than exploitation of weak specifications.

This is a validity gate rather than an optional secondary hypothesis.

## Primary criteria

Measure:

* specification-hacking rate;
* vacuous-proof rate;
* hidden-test correctness;
* natural-language intent satisfaction;
* rate of weakened preconditions or postconditions;
* contradiction and unreachable-state exploitation;
* formal-versus-behavioral correctness gap.

Define:

[
G_{\text{spec-gap}}
===================

## \text{formal acceptance}

\text{independent behavioral correctness}.
]

## Supporting result

H10 is supported if G5:

* improves formal and behavioral correctness together;
* does not increase (G_{\text{spec-gap}});
* rejects or detects adversarial specifications;
* does not systematically introduce vacuous assumptions.

## Falsification criterion

The claimed semantic-learning result is invalidated if:

* formal acceptance rises while behavioral correctness remains unchanged or falls;
* the model learns to strengthen preconditions artificially;
* the model removes difficult requirements;
* verification gains are primarily explained by specification exploitation.

---

# Priority order

## PoC hypotheses

Test first:

1. **H1:** VC decomposition versus binary proof
2. **H2:** proof-state transition learning
3. **H4:** tool-off internalization
4. **H10:** specification-hacking validity gate

Initial groups:

[
G0,;G1,;G3,;G4,;G5.
]

## Publication hypotheses

Then add:

5. **H3:** proof process versus execution process
6. **H5:** robustness
7. **H6:** hybrid supervision
8. **H7:** efficiency

Add groups:

[
G2,;G6
]

and replicate at 1.7B.

## Extended research hypotheses

Finally:

9. **H8:** mathematical proof versus program proof
10. **H9:** mathematical-to-program curriculum

---

# Minimal paper success criterion

The paper has a strong positive result if:

> Under matched training and inference budgets, ProofWorld outperforms both binary verifier reward and dense execution-state supervision on tool-off semantic tasks; the gain reproduces at 0.6B and 1.7B, survives semantic-preserving transformations and cross-representation evaluation, improves independent behavioral correctness, and is not explained by specification hacking.

A useful negative result is:

> Proof supervision improves verifier-assisted generation but provides no advantage over execution-process supervision after tool removal.

That would establish that formal proof is primarily an effective external scaffold rather than a superior mechanism for teaching internal program semantics.


