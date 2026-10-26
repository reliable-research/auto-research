# Final Research Direction — From Execution Feedback to Proof-Derived Semantic Supervision

After combining the previous discussion, the two prover branches, the deep-research results, and the latest research memo, I would freeze the project around **one central scientific question**:

> **Can a code LLM learn more useful program semantics from what must be true than from what happened on sampled executions?**

The important correction is that this is **not primarily “formal verification replacing RL.”** RL is the optimizer. What we want to replace or augment is the **semantic oracle used to generate supervision**. This distinction is also the cleanest continuation of the interview story: token supervision → execution/state grounding → formal semantic verification. 

---

## 1. Final title

### **Execution or Proof? Learning Program Semantics from Verifiable Feedback**

A more method-oriented paper title would be:

### **From Execution Rewards to Proof Rewards: Semantic Credit Assignment for Code Language Models**

The first title is safer for a research proposal because it does not assume in advance that proof will win.

---

# 2. Final thesis

Current code post-training increasingly relies on execution:

[
\text{program}
\rightarrow
\text{compile/run}
\rightarrow
\text{tests/traces}
\rightarrow
R_{\text{exec}}.
]

This is grounded, but the evidence is fundamentally based on concrete executions. Even dense execution-process methods still observe particular trajectories.

Formal program verification offers a different supervision channel:

[
\text{program + specification}
\rightarrow
\text{verification conditions}
\rightarrow
\text{prover}
\rightarrow
R_{\text{proof}}.
]

For a property correctly captured by the formal specification and program semantics, deductive verification can reason over the represented state space without repeatedly executing the generated program.

The research question therefore becomes:

> **Under matched model, data, optimizer and compute budgets, does proof-obligation-level supervision yield better semantic credit assignment, generalization and tool-free transfer than execution-derived supervision?**

This is the strongest remaining gap identified by the literature review: verifier-driven RL itself already exists, but a carefully controlled comparison among test outcome, execution-process, proof-outcome and proof-process supervision appears absent from the surveyed literature through August 21, 2026. 

---

# 3. What is actually novel

Do **not** claim:

> We replace tests with a formal verifier for RL.

That is already too close to Re:Form and other verifier-feedback work. 

The paper's novelty should instead consist of three connected pieces.

### Contribution A — Proof obligations as semantic process supervision

Do not reduce verification to:

[
R=1[\text{verified}].
]

Expose the internal semantic decomposition:

[
\boxed{
P\Rightarrow I
}
]

[
\boxed{
I(s)\land G(s)\land T(s,s')
\Rightarrow I(s')
}
]

[
\boxed{
I(s)\land\neg G(s)
\Rightarrow Q(s)
}
]

so the learner knows whether it failed at **initiation, state-transition preservation, postcondition sufficiency, safety, or termination**.

This moves from:

[
\text{proof outcome}
\rightarrow
\boxed{\text{proof process}}.
]

LORIS shows that localized failed verification conditions are operationally useful, but mainly uses them at inference time; the open question is whether they can become effective parameter-level post-training supervision. 

### Contribution B — A causal execution-vs-proof experiment

Compare the semantic oracles while keeping everything else as equal as practical.

The key progression is:

[
\boxed{
\text{Test Outcome}
\rightarrow
\text{Execution Process}
\rightarrow
\text{Proof Outcome}
\rightarrow
\text{Proof Process}
}
]

This matters because ExecVerify already makes binary testing a weak baseline: proof-process reward must be compared with **dense execution-state supervision**, not merely `pass/fail`. 

### Contribution C — Does the capability remain when the prover disappears?

This is perhaps the most interesting part.

After training:

[
\text{remove verifier}
]

and ask whether the proof-supervised model remains better at:

[
\text{state reasoning}
,\quad
\text{semantic equivalence}
,\quad
\text{code generation}
,\quad
\text{repair}.
]

Otherwise, we have built a better **prover-using agent**, not necessarily a stronger **code model**.

---

# 4. The two prover branches stay separate

Mathematical proving and program verification should not be collapsed into one “prover capability.”

|                   | Mathematical prover       | Program verifier                          |
| ----------------- | ------------------------- | ----------------------------------------- |
| Semantic object   | propositions / lemmas     | program states / transitions              |
| Example           | (\Gamma\vdash\phi)        | (P\Rightarrow I,\ I\land T\Rightarrow I') |
| Typical tools     | Lean, Isabelle, Rocq      | Dafny, Z3, Boogie, Frama-C, Verus         |
| Likely capability | deduction / decomposition | program-semantic reasoning                |
| Role here         | scientific control        | **main treatment**                        |

The latest research review reaches the same conclusion: mathematical proving is already a mature RL domain, whereas direct transfer into ordinary software reasoning is much less established. It is therefore a valuable positive control or later curriculum, not the center of the first PoC. 

The deeper full-paper hypothesis is eventually:

[
\boxed{
\text{Math proof teaches how to prove}
}
]

whereas

[
\boxed{
\text{Program proof teaches what program behavior must preserve}.
}
]

---

# 5. Final hypotheses

**H1 — Semantic-credit hypothesis.** Structured program-proof supervision produces stronger semantic learning than binary formal acceptance because it identifies which program property failed.

**H2 — Proof-vs-execution hypothesis.** Under matched budgets, proof-process supervision outperforms execution-outcome reward on formally specified properties and competes with or surpasses dense execution-process supervision on OOD semantic generalization.

**H3 — Internalization hypothesis.** Some advantage survives when no prover is available at inference. This is the hypothesis that turns the project from “better formal tooling” into a learning result.

**H4 — Hybrid hypothesis.** When specifications are incomplete, proof and execution become complementary: proof establishes universal properties represented by the specification, while concrete execution exposes omitted or misrepresented behavior.

**H5 — Domain hypothesis.** Program-verification supervision transfers to software tasks more strongly than mathematical-proof supervision under matched post-training budgets because it explicitly represents state transitions.

The literature already provides partial transfer evidence—for example, verification-oriented fine-tuning and proof-certified semantic-equivalence training—but not the matched experiment needed for this causal claim. 

---

# 6. Final reward design

I would remove the earlier vague `strength` reward and avoid rewarding raw VC count.

Define a fixed set of semantic obligations:

[
\mathcal O =
{
O_{\text{init}},
O_{\text{preserve}},
O_{\text{post}},
O_{\text{safety}},
O_{\text{termination}}
}.
]

For every obligation (O_j), retain a categorical prover result:

[
z_j\in
{
\text{proved},
\text{refuted/counterexample},
\text{unknown},
\text{timeout},
\text{invalid}
}.
]

Then:

[
R_{\text{VC}}
=============

\frac{\sum_jw_jV(z_j)}
{\sum_jw_j}
]

plus a strong terminal completion term:

[
R_{\text{complete}}
===================

\mathbf 1[
\forall j,\ z_j=\text{proved}
].
]

For multi-turn repair:

[
R_{\text{progress}}^{(t)}
=========================

## R_{\text{VC}}^{(t)}

R_{\text{VC}}^{(t-1)}.
]

The conceptual reward becomes:

[
\boxed{
R_{\text{proof}}
================

R_{\text{semantic obligations}}
+
\lambda R_{\text{complete}}
+
\mu R_{\text{progress}}
}
]

rather than “number of prover messages that disappeared.”

This distinction also avoids treating **solver timeout** as equivalent to a logical counterexample.

For hybrid training:

[
R_{\text{hybrid}}
=================

\alpha R_{\text{proof}}
+
\beta R_{\text{exec}}
---------------------

## \gamma C_{\text{oracle}}

\delta R_{\text{invalid}}.
]

But the hybrid must distinguish specification status:

[
\boxed{
\text{trusted fixed specification}
\Rightarrow
\text{proof can be the correctness oracle}
}
]

whereas

[
\boxed{
\text{generated/partial specification}
\Rightarrow
\text{proof needs an adequacy audit}.
}
]

That qualification is crucial because a machine can perfectly prove an inadequate requirement. The research brief explicitly identifies specification gaming as one of the central threats. 

---

# 7. Final experimental design

Use one shared SFT checkpoint and, ideally, evaluate the **same sampled candidates** with both the execution and proof environments before applying different reward functions. That substantially reduces the causal confound.

| Group  | Supervision                    | Purpose                   |
| ------ | ------------------------------ | ------------------------- |
| **G0** | SFT only                       | common baseline           |
| **G1** | final test/execution reward    | conventional outcome RL   |
| **G2** | execution-state/process reward | strongest runtime control |
| **G3** | mathematical-proof supervision | general proof control     |
| **G4** | binary program-verifier reward | proof-outcome control     |
| **G5** | **structured VC reward**       | **main proposed method**  |
| **G6** | math proof → program proof     | transfer/curriculum study |
| **G7** | structured proof + execution   | practical hybrid          |

The smallest PoC should not train all eight.

Start at **0.6B** with:

[
G0,;G1,;G4,;G5.
]

If G5 shows signal, add:

[
G2,;G7
]

before making a publication claim.

Then reproduce the important contrasts at **1.7B**.

The research memo reaches essentially this same staged recommendation and emphasizes using the same underlying programming instances and matched sampled-token budgets. 

---

# 8. The decisive evaluation is not verifier success

Evaluation must have two axes.

### Tool ON

This measures whether the model can use a verifier effectively:

[
\text{trained model}+\text{prover}
\rightarrow
\text{verified solve rate}.
]

Useful, but not the strongest scientific result.

### Tool OFF — primary endpoint

[
\boxed{
\text{trained model}
--------------------

\text{prover}
}
]

Evaluate on unseen program semantics:

| Evaluation                     | What it tests                               |
| ------------------------------ | ------------------------------------------- |
| unseen loop families           | induction rather than template memorization |
| renaming / equivalent rewrites | semantic robustness                         |
| execution reasoning            | internal state-transition knowledge         |
| semantic equivalence           | behavior rather than syntax                 |
| ordinary code generation       | cross-objective transfer                    |
| C/C++ repair                   | real semantic defect transfer               |
| cross-language tasks           | Dafny-syntax dependence                     |

The uploaded review explicitly recommends separating formal in-domain, formal OOD, tool-off formal reasoning, ordinary generation, execution reasoning, repair, cross-language transfer and full hybrid-agent evaluation. 

---

# 9. Benchmark path

Do **not** start the main experiment on repository-scale software.

A clean progression is:

[
\boxed{
\text{Dafny loops/arrays}
\rightarrow
\text{formal OOD}
\rightarrow
\text{semantic reasoning}
\rightarrow
\text{C/C++ repair}
}
]

Dafny is a good causal sandbox because specifications, invariants and VCs are directly available and small-model verifier RL has already been shown feasible. Later, C/Frama-C or the existing C→SMT pipeline can test whether the effect survives a less artificial representation.

The final research review recommends the same basic strategy: begin with single-function imperative programs and only later introduce nonlinear arithmetic, aliasing, pointers, composition and repository-scale behavior. 

---

# 10. What “no execution” should finally mean

The slide's original sentence:

> If we can prove the program, we do not need runtime to tell us it is correct.

is intuitively good but academically too absolute.

Use this instead:

> **For a formally specified property, deductive proof can replace sampled execution as the correctness oracle and expose which semantic obligation failed. For behavior not fully captured by the specification, proof and execution provide complementary evidence.**

Or, shorter for the interview slide:

> **Tests tell us what happened. Proof tells us what must hold.**

Then underneath:

> **Can we train code LLMs from the latter?**

That preserves the ambition of Research Challenge 3 without claiming that runtime validation becomes globally unnecessary. Your current Pillar II already frames the progression as Understand → Track/Ground → Verify, so this wording strengthens rather than changes the narrative. 

---

# 11. Falsification is part of the contribution

The project succeeds scientifically even if proof does **not** universally win.

The strong hypothesis should be weakened or rejected if G5 improves only verifier-assisted Dafny solving; loses to G2 dense execution supervision at matched compute; shows no improvement once the verifier is removed; collapses under semantic-preserving rewrites or cross-language evaluation; or produces higher formal acceptance without higher independent behavioral correctness.

That outcome would mean:

[
\text{prover}
\approx
\text{excellent external scaffold}
]

rather than:

[
\text{proof experience}
\Rightarrow
\text{stronger internal program semantics}.
]

A particularly valuable result could therefore be a **phase diagram** showing where each oracle wins rather than a universal “proof beats execution” result.

---

# 12. Final paper claim

This is the claim I would now lock:

> **We study formal program verification as a semantic supervision source for code-language-model post-training. Rather than using a verifier only as a terminal accept/reject oracle, we decompose verification into machine-checkable program obligations—such as invariant initiation, transition preservation and postcondition sufficiency—and use them as semantic credit-assignment units. Through matched comparisons against outcome-level and process-level execution supervision, we test whether proof-derived experience produces stronger correctness, robustness and prover-free transfer, and when formal and runtime evidence should instead be combined.**

And the **one-line research vision** is:

> **Move code learning from matching outputs, to observing behavior, to learning what behavior must remain true.**

[
\boxed{
\text{Token}
\rightarrow
\text{State}
\rightarrow
\text{Proof}
}
]

That is the final version I would carry forward. It preserves the original Pillar II story, avoids the novelty conflict around generic verifier RL, makes **structured semantic credit assignment** the methodological contribution, and gives you a genuinely falsifiable question rather than presupposing that formal methods must beat runtime supervision. 


