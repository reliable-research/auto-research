# From Execution Rewards to Proof Supervision: A Research Assessment of Prover-Guided Training for Code LLMs

## Executive assessment

Your core idea is **technically sound, timely, and still researchable**, but the novelty needs to move one level deeper than “use a formal verifier instead of tests as the RL reward.”

The literature through **August 21, 2026** already establishes that formal verifiers can be used as machine-checkable reward or feedback sources. Re:Form trains Dafny models using verifier-derived RL and was published in TMLR in 2026; Max Tan's 2026 thesis applies GRPO-style reinforcement learning from compiler and verifier outcomes; SpecRL combines verification with execution-derived negative tests for specification synthesis. citeturn10view0turn9view2turn13view0

At the same time, execution supervision has itself become much stronger than simple pass/fail unit-test RL. RLEF trains models to use multi-turn execution feedback; ExecVerify rewards intermediate execution-state predictions; StepCodeReasoner similarly supervises stepwise runtime state. Therefore, the scientifically meaningful comparison is no longer:

\[
\text{tests} \quad\text{vs.}\quad \text{proof}
\]

but rather:

\[
\boxed{
\text{execution-outcome reward}
\;\longrightarrow\;
\text{execution-process reward}
\;\longrightarrow\;
\text{proof-outcome reward}
\;\longrightarrow\;
\text{proof-process reward}
}
\]

RLEF demonstrates that execution-feedback RL can substantially improve iterative code synthesis, while ExecVerify reports that verifiable intermediate execution rewards transfer from execution reasoning to code generation, improving pass@1 by as much as 5.9 percentage points. citeturn2search2turn11view4

That makes your strongest remaining research question:

> **Under matched model, data, RL algorithm, and compute budgets, does verification-condition-level formal supervision produce better semantic credit assignment and stronger prover-free transfer than equally dense execution-state supervision?**

I found no primary work through August 21, 2026 that cleanly combines all of the following: **a matched execution-versus-proof reward comparison, verification-condition-level process rewards for program correctness, and evaluation after removing the prover at inference**. The closest pieces exist separately: Re:Form and the Tan thesis establish formal-verifier RL; LORIS establishes localized formal feedback at inference; ExecVerify establishes dense execution-process RL; Verifiable Process Rewards establishes the broader value of deterministic intermediate verification; and formal semantic-equivalence self-play provides evidence that proof-certified supervision can transfer to downstream code reasoning. citeturn10view0turn9view2turn9view4turn11view4turn12academia1turn0academia3

There is one important terminology correction:

> **Formal methods do not inherently replace reinforcement learning. They replace or augment the source of semantic supervision.**

You can still optimize that supervision with GRPO/PPO-style RL, as Re:Form and the Tan thesis do. Alternatively, you can use the prover to construct verified datasets for SFT, rejection sampling, preference learning, or feedback distillation; the 2026 semantic-equivalence work uses proof-certified examples without making RL essential, and Feedback Distillation for Lean shows that verifier-conditioned supervision can complement GRPO. citeturn8view4turn5academia13

That distinction matters for the paper. A cleaner title is therefore **“From Execution Rewards to Proof Supervision”**, rather than “Replacing RL with Formal Verification.”

Your interview material is already moving in the right conceptual direction. Page 1 separates **Understand → Track/Ground → Verify**, while page 2 explicitly combines token, trace, semantic, and proof-oriented learning signals. fileciteturn0file3 The main correction I would make is to soften the page-1 statement that proving a program means runtime verification is unnecessary. A proof can remove the need for concrete execution **for the property that is correctly formalized and faithfully modeled**, but it does not establish that the specification captures user intent, that external systems behave as modeled, or necessarily that the deployed binary preserves the proved source semantics. citeturn13view0turn6academia27

## Where the literature now stands

The research landscape is becoming unusually favorable for your proposal because the execution and formal-verification branches have both matured enough that a controlled comparison is now meaningful.

| Work | Supervision signal | What it establishes | What remains open for your project |
|---|---|---|---|
| **RLEF**, ICML 2025 | Compilation/test execution feedback across turns | Models can be trained to internalize iterative use of execution feedback and need far fewer samples | Does proof feedback teach a stronger semantic representation than execution feedback? citeturn2search2 |
| **Re:Form**, TMLR 2026 | Dafny verifier-driven RL | Small models can learn formal-software behavior from automatic verifier feedback; RL improves OOD performance | Primarily formal-language/specification generation; no matched proof-vs-execution process comparison citeturn10view0 |
| **ExecVerify**, 2026 | Next statement/value/type + final output | Dense, verifiable runtime-state RL improves code reasoning and transfers to generation | This is the critical dense execution baseline your method must beat citeturn11view4 |
| **StepCodeReasoner**, 2026 | Stepwise execution-state anchors | Runtime process supervision can address credit assignment rather than relying only on final outputs | Reinforces the need to compare proof-process against execution-process, not just unit tests citeturn1academia15 |
| **Tan thesis**, 2026 | Compiler/verifier outcomes with GRPO | Verified reward can rise dramatically, but weak formal specifications create specification hacking | Shows directly that “proof accepted” is not automatically “intended solution correct” citeturn9view2 |
| **SpecRL**, 2026 | Verification + execution-backed negative tests | Verifier-only feedback cannot distinguish complete from weak specifications; hybrid reward improves specification quality | Strong evidence that the right hybrid is proof for soundness plus behavioral evidence for adequacy citeturn13view0 |
| **LORIS**, TOPLAS 2026 | SMT checking of individual formalized reasoning implications | Formal verification can identify a precise local logical error rather than returning one terminal failure | Feedback is currently inference-time; converting this into learned process credit is a promising gap citeturn9view4 |
| **Semantic-equivalence self-play**, ACL Findings 2026 | Liquid Haskell proofs + executable counterexamples | Proof-certified equivalence data improves downstream code reasoning; proof data contributes uniquely in ablations | Uses verified-data training rather than a direct proof-process RL comparison citeturn0academia3 |
| **P³**, August 2026 | Joint program-and-proof planning | Anticipating proof obligations before implementation improves solve rate and can lower cost | Agentic inference result, not evidence that proof capability has entered model weights citeturn4academia1 |
| **Verifiable Process Rewards**, 2026 | Deterministic checks of intermediate agent decisions | Dense verifier-grounded process reward can improve credit assignment and transfer in structured reasoning | Not specifically about program verification conditions citeturn12academia1 |

The most consequential result for your novelty positioning is **SpecRL**. It explicitly states that a verifier alone establishes one direction—roughly, that implementation behavior is admitted by the specification—but cannot tell whether the specification unnecessarily permits behaviors that the implementation cannot produce. Its reward therefore gates on successful verification and then uses negative execution-derived behaviors to reward specification completeness. citeturn13view0

This means your proposed hybrid direction is not merely a defensive qualification. There is already empirical evidence that **proof and execution are asymmetric evidence sources**.

For an implementation \(P\) and specification \(S\), deductive verification targets something like

\[
[\![P]\!] \subseteq [\![S]\!],
\]

meaning every represented behavior of the implementation satisfies the specification. SpecRL emphasizes that this does not imply

\[
[\![S]\!] \subseteq [\![P]\!],
\]

so `ensures true`, overly restrictive preconditions, or otherwise weak contracts can still verify. citeturn13view0

This gives a particularly clean interpretation of the hybrid idea:

\[
\boxed{
\text{Formal proof is excellent at establishing universally quantified inclusion;}
}
\]

\[
\boxed{
\text{execution is excellent at cheaply producing witnesses that expose missing constraints.}
}
\]

The 2026 semantic-equivalence work independently adopts almost exactly this asymmetry: it uses Liquid Haskell proof to certify equivalence and executable counterexamples to establish inequivalence, with the resulting dataset improving EquiBench by up to 13.3 percentage points and transferring to PySecDB. citeturn0academia3

Mathematical theorem proving provides useful supporting evidence but should remain a separate branch. AlphaProof demonstrates that machine-checked formal environments can support powerful reinforcement learning for theorem proving; it reached silver-medal-level performance in the reported IMO 2024 system. But mathematical theorem proving does not directly demonstrate improved tracking of mutation, heaps, aliases, loops, or ordinary software behavior. citeturn5search0 Your main paper should therefore use mathematical-prover training, at most, as an optional transfer control rather than conflating it with program verification.

The novelty I would defend is consequently:

> **Verification-condition-level semantic credit assignment for code LLM post-training, evaluated causally against equally dense execution-derived supervision and tested for retained capability without verifier access.**

That is materially stronger than “use Dafny/Z3 as an RL reward.”

## What proof supervision actually buys

Your intuition that the prover “may not need to execute the program” is correct in an important technical sense.

Deductive verifiers such as Dafny/Boogie or Frama-C/WP can convert annotated programs into logical verification conditions and ask automated theorem provers or SMT solvers to establish those formulas. Boogie is explicitly designed around program semantics, verification-condition generation, and automated theorem proving; its verification conditions can be constructed using weakest-precondition-style reasoning. citeturn6search1turn6search2 Frama-C's WP component similarly generates a verification condition for each relevant annotation and uses SMT solvers or proof assistants to establish the property for all modeled executions rather than sampling concrete test runs. citeturn7search0turn7search1

So there is a real distinction between:

\[
\text{concrete execution:}\qquad
P(x_1),P(x_2),\ldots,P(x_n)
\]

and

\[
\text{deductive verification:}\qquad
\vdash \mathrm{VC}(P,S).
\]

A unit test tells you what happened at selected points. A sound proof of the corresponding formal property establishes the result over the full represented state space covered by the theorem. Dafny is explicitly designed for static verification of functional correctness using preconditions, postconditions, frame specifications, invariants, and other logical annotations. citeturn6search3turn6search16

That is your **evidence-strength argument**.

Your more interesting ML argument, however, is **credit assignment**.

Suppose the target loop is

```text
while G:
    S
```

with precondition \(P\), invariant \(I\), transition relation \(T_S\), and postcondition \(Q\). A traditional deductive decomposition gives obligations of the form

\[
P \Rightarrow I
\]

for initiation,

\[
I(s)\land G(s)\land T_S(s,s')
\Rightarrow I(s')
\]

for preservation, and

\[
I(s)\land\neg G(s)\Rightarrow Q(s)
\]

for postcondition sufficiency. Tools in the Dafny/Boogie and Frama-C/WP tradition generate logical obligations from annotations precisely so such claims can be checked statically. citeturn6search2turn7search0

Now compare the learning signals.

A test-only failure can be:

```text
reward = 0
```

A process-execution system can improve this to:

```text
iteration 7:
x expected 12, predicted 11
```

as approaches such as ExecVerify and StepCodeReasoner do with intermediate states. citeturn11view4turn1academia15

A program verifier can instead expose semantically different classes of failure:

```text
initiation: proved
preservation: failed
postcondition: proved conditional on invariant
termination: unknown
```

and, where the underlying solver can produce a countermodel for the failed logical implication, potentially expose values violating that implication. LORIS demonstrates the value of this localization: it formalizes individual reasoning steps as implications and uses an SMT solver to identify the precise invalid step, achieving 445/460 solved programs on its main benchmark and 93.1% overall success in the reported evaluation. citeturn9view4

That is very close to the mechanism you want—except LORIS uses it to guide **test-time repair**, rather than turning the localized obligations into **training-time process advantages**.

This difference is the research opportunity.

There are nevertheless four qualifications to the word **“exact.”**

First, prover success is exact **relative to a formal specification**. The Tan thesis observed specification hacking in verifier-reward RL, and SpecRL demonstrates why verification success does not guarantee a strong or complete behavioral specification. citeturn9view2turn13view0

Second, prover success is exact **relative to a formal semantics and trusted toolchain**. A 2025 project constructing a verified VCG and verified compiler for a subset of Dafny explicitly notes that soundness bugs have previously been found in Dafny's verifier and compiler; its purpose is to close that trust gap with HOL4-checked components. citeturn6academia27 Thus “machine checked” is much stronger than testing, but the trusted computing base still matters.

Third, failure to prove is not the same as proof of failure. SMT-based verification can become incomplete or operationally brittle around quantified reasoning; recent work on E-matching specifically discusses incompleteness and non-termination risks from quantifier instantiation in SMT-based verification. citeturn6academia25 Dafny itself phrases many failures as an assertion or postcondition that “might not hold,” reflecting the distinction between “disproved” and “not established.” citeturn6search12

Fourth, the formal model can omit real environmental behavior. Frama-C explicitly distinguishes the properties encoded in specifications from runtime concerns and notes that functional correctness depends on the developer's stated intention; its framework also has separate static and runtime-analysis mechanisms because different verification questions require different techniques. citeturn7search0turn7search5

A useful trust ladder for the paper would therefore be:

\[
\text{syntax/type validity}
<
\text{passes sampled executions}
<
\text{proved under source semantics}
<
\text{proved + adequate specification}
<
\text{proved end-to-end deployed behavior}.
\]

The central contribution does **not** need to claim the last level. It needs to establish that moving from sampled execution evidence toward proof obligations produces better learning signals for the formally modeled portion of program semantics.

## A stronger proof-reward design

I would modify your current reward formulation substantially.

Your initial decomposition,

\[
R_{\text{proof}}
=
w_1R_{\text{init}}
+w_2R_{\text{preserve}}
+w_3R_{\text{post}}
+w_4R_{\text{strength}}
+w_5R_{\text{progress}},
\]

has the right intuition, but `strength` and `progress` require care.

For a **fixed externally supplied specification**, there is usually no need to reward arbitrary invariant “strength.” The thing you actually need is whether the invariant is adequate to discharge the canonical obligations. A logically stronger invariant is not automatically better: strengthening \(I\) can make preservation harder, and syntactic or logical strength is not monotonically related to proof usefulness.

I would instead define a fixed canonical obligation set

\[
\mathcal O(P,S)
=
\{
O_{\text{init}},
O_{\text{pres}},
O_{\text{post}},
O_{\text{safety}},
O_{\text{term}},\ldots
\}
\]

and record a categorical verifier outcome for every obligation:

\[
z_j\in
\{
\text{proved},
\text{counterexample},
\text{unknown},
\text{timeout},
\text{invalid}
\}.
\]

This distinction is important because SMT “unknown” or timeout should not be treated as logically equivalent to a demonstrated counterexample. Quantified SMT reasoning can be incomplete and unpredictable, so a binary success/failure parser would inject label noise into exactly the supposedly “exact” reward signal. citeturn6academia25turn6search12

A simple process score is then

\[
R_{\mathrm{VC}}
=
\frac{
\sum_{j=1}^{m}
w_j\,v(z_j)
}{
\sum_{j=1}^{m}w_j
},
\]

with, for example,

\[
v(\text{proved})=1,\qquad
v(\text{unknown})=v(\text{timeout})=0,\qquad
v(\text{counterexample})<0.
\]

The exact numerical values are an experimental choice rather than something to hard-code theoretically.

Then add a substantial terminal bonus:

\[
R_{\mathrm{all}}
=
\mathbf 1
[
\forall j,\ z_j=\text{proved}
].
\]

This prevents the policy from optimizing only easy local obligations while never completing the proof.

For loop invariants specifically, an especially interpretable version is

\[
R_{\mathrm{loop}}
=
w_iV(P\Rightarrow I)
+
w_pV(I\land G\land T\Rightarrow I')
+
w_qV(I\land\neg G\Rightarrow Q)
+
w_tV(\text{termination}),
\]

where \(V(\phi)\) is determined by the prover outcome for the fixed semantic obligation.

Your `proof progress` term should be **relative progress on a fixed task**, not raw solver time or “VC difficulty”:

\[
R_{\mathrm{progress}}^{(t)}
=
R_{\mathrm{VC}}^{(t)}
-
R_{\mathrm{VC}}^{(t-1)}.
\]

That gives exactly the semantic transition you originally wanted:

```text
candidate
→ failed preservation
→ revised invariant
→ preservation proved
→ postcondition now fails
→ strengthened invariant
→ all VCs proved
```

This is much safer than rewarding reductions in SMT runtime. Solver runtime, particularly under quantifiers, can change sharply because of instantiation heuristics rather than meaningful semantic progress. citeturn6academia25

There is another subtle point: **do not simply reward the raw number of VCs discharged**. If the generated annotations affect how obligations are split, the policy could learn to manufacture easy obligations or restructure the proof to inflate the count. Canonical categories—initiation, preservation, postcondition, safety, termination—are much harder to game.

For generated specifications, however, proof alone is insufficient. Here SpecRL's analysis should directly influence your design. It shows that a candidate such as `ensures true` can verify while saying essentially nothing, and it therefore combines successful verification with negative behaviors that the specification ought to exclude. citeturn13view0

So I would separate two cases:

\[
\boxed{
\textbf{Fixed trusted specification:}
\quad
\text{VC reward is enough for the formal property.}
}
\]

\[
\boxed{
\textbf{Generated/inferred specification:}
\quad
\text{VC reward requires an adequacy signal.}
}
\]

For the latter,

\[
R_{\mathrm{hybrid}}
=
\mathbf 1_{\text{valid}}
\left(
\lambda_pR_{\mathrm{VC}}
+
\lambda_eR_{\mathrm{adequacy}}
+
\lambda_fR_{\mathrm{all}}
\right)
-\lambda_cR_{\mathrm{cost}}.
\]

The adequacy component can come from hidden tests, negative spectests, property-based testing, cross-specification equivalence, or adversarial counterexample search. SpecRL's progressive reward already demonstrates one workable form: extraction and compilation gates, then verification, then negative-test rejection for completeness. citeturn13view0

I would additionally make the following **hard constraints**, not soft rewards:

```text
No assume false / admit / sorry / untrusted axiom.
No modification of the supplied specification unless the task explicitly allows it.
No strengthening of preconditions to exclude difficult inputs.
No deletion or dead-coding of target functionality.
No change to the implementation in an invariant-only task.
```

SpecRL already sets zero reward for candidates that insert `assume`, alter the implementation, or generate obvious vacuous contracts such as `ensures true` and `requires false`. citeturn13view0 Your work should generalize this into a formal **reward-integrity layer**.

There is also a potentially powerful non-RL version of the same pipeline:

\[
\text{sample candidate}
\to
\text{generate VCs}
\to
\text{localize failure}
\to
\text{repair}
\to
\text{retain verified trajectory}
\to
\text{distill}.
\]

This matters because your original phrase “replacement or auxiliary of RL” contains two distinct research questions.

**Question A:** Can proof supervision replace **execution rewards while keeping RL**?

**Question B:** Can proof supervision replace **RL itself**, for example through rejection sampling, verified SFT, preference optimization, or feedback distillation?

The first question is experimentally much cleaner because the optimizer remains fixed. The semantic-equivalence self-play paper shows that proof-certified training can improve downstream reasoning without requiring RL as the central mechanism, while recent Lean work finds feedback distillation complementary to GRPO. citeturn0academia3turn5academia13

For the first paper, I would answer **Question A** and leave Question B as an ablation or follow-on study.

## The decisive experiment

Your proposed G0–G4 design is close, but one important baseline is missing: **dense execution-process supervision**.

Without it, a reviewer can reasonably argue:

> “You beat sparse test reward because your formal signal is dense, not because formal proof is intrinsically better than runtime grounding.”

ExecVerify and StepCodeReasoner make that objection unavoidable in 2026. citeturn11view4turn1academia15

The main experiment should therefore be:

| Arm | Training signal | Scientific question |
|---|---|---|
| **SFT** | Same code/specification data, no online semantic oracle | Base post-training capability |
| **Execution outcome** | Final public/hidden test result | Standard runtime RL |
| **Execution process** | Intermediate statements, values, types or traces | Dense runtime credit assignment |
| **Proof outcome** | Whole program verifies / fails | Does universality alone help? |
| **Proof process** | Fixed VC categories and localized verifier outcomes | Does symbolic semantic credit help? |
| **Hybrid** | Proof process + behavioral adequacy/counterexamples | Is the asymmetric combination strongest? |
| **Proof distillation** | Verified/repaired trajectories, no RL | Does the verifier replace the optimizer as well as the runtime oracle? |

Use the **same base checkpoint, prompts, data distribution, output budget, optimizer and RL hyperparameters** for the four RL arms. Re:Form demonstrates that formal-language SFT can make even a roughly 0.5B model capable of producing syntactically valid and verifiable Dafny programs, so your proposed 0.6B and 1.7B scale is experimentally plausible rather than obviously too small. citeturn8view0

The most important pairwise comparison becomes

\[
\boxed{
\text{Execution Process}
\quad\text{vs.}\quad
\text{Proof Process}
}
\]

rather than merely

\[
\text{Unit Tests}
\quad\text{vs.}\quad
\text{Verifier}.
\]

A second experimental axis should be **inference-time tool availability**:

| Training | No verifier/test tool at inference | Equal tool budget at inference |
|---|---|---|
| Execution-trained | measures internalized execution semantics | measures feedback-use capability |
| Proof-trained | measures internalized formal semantics | measures prover-use capability |
| Hybrid | measures durable combined representation | measures full agent effectiveness |

The **no-tool column is essential**.

P³ shows that proof-aware planning improves verified code generation when the proof machinery remains part of the inference system. LORIS similarly shows that solver-localized reasoning errors improve iterative invariant synthesis. Those are impressive system-level results, but they do not demonstrate that the model has internalized the resulting capability once the external verifier is removed. citeturn4academia1turn9view4

Your strongest result would look like:

\[
\text{proof-process training}
>
\text{execution-process training}
\]

on **ordinary semantic code tasks with neither verifier nor execution tool available**.

That would support a genuine representation-learning claim rather than merely a better agent scaffold.

Evaluation should be separated into four layers.

**Formal correctness** measures complete verification rate, individual VC success, invariant success, proof attempts and solver calls. This answers whether the training objective worked.

**Behavioral correctness** uses large hidden test suites independent of the training reward. This catches specification gaming and source-level formalization gaps. The 2026 AxDafny paper is particularly interesting here because its new 250-problem LCB-Pro-Dafny benchmark explicitly evaluates verified Dafny generation and reports that verification success and runtime-test performance capture different aspects of generated code. citeturn3academia1

**Prover-free semantic transfer** evaluates semantic equivalence, execution reasoning, unseen loop structures, ordinary code generation, and repair without exposing the formal environment. The semantic-equivalence self-play results provide direct precedent that formal proof-certified supervision can transfer beyond proof completion. citeturn0academia3

**Efficiency** reports not just verifier calls and executions, but total environment CPU time, model inference tokens, GPU training time, wall-clock time, and solved-problem-per-compute curves. You should not assume in advance that proof is cheaper than execution. SMT solving can become difficult around nonlinear arithmetic, quantifiers and complex memory models, while execution can be extremely cheap for small deterministic programs. citeturn6academia25turn7search0

For fairness, report at least two budget views:

\[
\text{accuracy at equal sampled trajectories}
\]

and

\[
\text{accuracy at equal end-to-end compute/wall time}.
\]

Otherwise either side can be favored artificially by how an “oracle call” is counted.

The generalization splits should be structural rather than random. Hold out complete algorithmic or semantic families: nested loops, nonlinear updates, arrays, alias-sensitive programs, branch-dependent invariants, different loop normal forms, and unseen specification templates. Also use variable renaming, statement reordering where semantics allow it, equivalent loop transformations, dead-code insertion, and syntactic reformulations. Such tests directly ask whether the model learned the semantic relation or merely Dafny surface patterns.

One particularly strong experiment is a **cross-representation test**:

\[
\text{train on Dafny proof obligations}
\rightarrow
\text{evaluate on ordinary Python/C code reasoning}.
\]

ExecVerify already demonstrates a form of execution-reasoning-to-generation transfer; the formal semantic-equivalence work demonstrates proof-certified-data-to-code-reasoning transfer. Your project can directly compare the two transfer pathways. citeturn11view4turn0academia3

Your central statistical outcome should therefore not be only “verified solve rate.” It should be a **transfer-efficiency frontier**:

\[
\frac{
\Delta\text{prover-free semantic correctness}
}{
\text{training oracle compute}
}.
\]

That quantity gets much closer to the claim that proof supervision is a better *learning signal*.

A convincing falsification criterion is equally important. The strong hypothesis should be rejected if proof-process training only improves tasks when a prover remains available, fails to beat dense execution-process training under matched compute, or produces higher verification rates without corresponding gains on independent hidden tests. Those outcomes would mean the prover is primarily a useful external scaffold rather than a superior way to teach program semantics.

## Tools and benchmarks that best fit the idea

For a first paper, I would begin with **Dafny**, then add a second-language validation rather than immediately trying to solve C/C++, Rust, and Lean together.

Dafny's main advantage is experimental cleanliness. It has native preconditions, postconditions, invariants, termination reasoning and an automated verifier backed by Boogie/Z3; importantly, substantial recent LLM-verification work already provides training pipelines and baselines. citeturn6search3turn10view0 The disadvantage is precisely that Re:Form, SpecRL, AxDafny and the Tan thesis make “Dafny + verifier reward” crowded territory. citeturn10view0turn13view0turn3academia1turn9view2 That is why your novelty must be the **reward comparison and VC-level process supervision**, not the language choice.

A useful tool roadmap is:

| Tool | Why useful for this project | Main trade-off |
|---|---|---|
| **Dafny + Boogie/Z3** | Easiest environment for canonical pre/post/invariant VCs; recent RL baselines; small-model feasibility | Formal-language setting can look artificial and prior-work density is high citeturn6search3turn10view0 |
| **Frama-C/WP + ACSL** | Works directly on C; each annotation generates formal obligations; strong connection to ordinary imperative semantics | C memory, undefined behavior, aliasing and annotation burden substantially raise difficulty citeturn7search0turn7search1 |
| **Verus/Rust** | More realistic systems programming, memory and concurrency reasoning; specifications/proofs live near Rust | Proof and ownership reasoning create a much larger learning problem citeturn7academia12 |
| **Lean** | Small trusted kernel and powerful proof ecosystem; clean mathematical control branch | Less direct fit for ordinary imperative state-transition supervision |
| **Execution sandbox** | Required for the matched runtime baseline and specification-adequacy checks | Evidence remains input-dependent, but this is exactly what makes it a useful control citeturn2search2turn11view4 |

For benchmarks, several 2025–2026 releases make the project much easier to execute rigorously.

The **Vericoding benchmark** contains 12,504 formal specifications: 3,029 Dafny, 2,334 Verus/Rust and 7,141 Lean examples, with 6,174 described as new unseen problems. That makes it useful for formal generalization and cross-system evaluation. citeturn3academia2

**LCB-Pro-Dafny**, introduced with AxDafny, contains 250 competition-style tasks and is unusually suitable for your exact question because it supports both formal verification and runtime-oriented assessment. citeturn3academia1

**LORIS's benchmark suite** has 460 main C programs and 50 nonlinear programs and targets exactly the invariant/VC reasoning mechanism you want to teach. It is an excellent second-stage evaluation even if the initial training environment is Dafny. citeturn9view4

**FVSpec** provides a bridge toward real software specifications. Its pipeline starts from 11,039 real-world Python property-based tests and translates 2,772 of them into 9,415 Lean specifications. The fact that only about a quarter of the collected tests could be translated is itself a useful reminder of the formalization-coverage bottleneck. citeturn3academia0

**CLEVER** contains 161 curated Lean verified-code-generation problems and was deliberately designed to avoid test-case supervision, implementation leakage, and vacuous specifications. It is a strong control if you want a smaller high-quality proof benchmark. citeturn3academia3

For prover-free transfer, the 2026 semantic-equivalence work's **EquiBench** and **PySecDB** evaluations are directly aligned with the idea that formal training might improve ordinary semantic discrimination. citeturn0academia3

For eventual repository-scale relevance, **SWE-EVO** is a useful stretch target rather than a first benchmark. It contains 48 long-horizon evolution tasks from seven mature Python projects, with changes spanning an average of 21 files and suites averaging 874 tests. Current agents remain weak on it, so failure of a 0.6B or 1.7B model would be difficult to interpret as evidence against proof supervision. citeturn4academia3

The most practical benchmark stack for your proposed model sizes is therefore:

\[
\boxed{
\text{Dafny VC training}
\rightarrow
\text{LCB-Pro-Dafny / Vericoding}
\rightarrow
\text{LORIS C invariants}
\rightarrow
\text{prover-free semantic equivalence/code reasoning}.
}
\]

Repository evolution should come only after this causal chain has been established.

## Failure modes that could invalidate the hypothesis

The first major threat is **specification gaming**, and it should be treated as a first-class experimental outcome rather than an implementation annoyance.

The Tan thesis reports exactly this phenomenon: verifier reward rose substantially while models learned to exploit weak formal specifications instead of solving the intended problem. citeturn9view2 SpecRL formalizes the same issue by showing that verification only establishes that program behavior satisfies the candidate specification; it cannot by itself identify an overly permissive or overly restrictive behavioral contract. citeturn13view0

You should therefore always report at least two separate correctness measures:

\[
\text{formal acceptance}
\]

and

\[
\text{independent semantic correctness}.
\]

A model that verifies 90% of programs but passes only 55% of independently constructed behavioral tests is not “90% correct.” It has learned to optimize the formal oracle.

The second threat is **proof-language specialization rather than program understanding**.

A small model might simply learn that particular Dafny invariant templates, assertions, triggers, or lemma patterns frequently make verification succeed. Re:Form's strong formal-language results establish feasibility but also make this alternative explanation plausible. citeturn10view0 This is precisely why adversarial renaming, syntactic transformations, unseen program templates, cross-language evaluation, and prover-removed inference are central rather than optional.

The third threat is **solver noise masquerading as semantic supervision**.

A failed VC can mean the property is false, the invariant is inadequate, the required lemma is absent, the encoding is difficult, or the solver ran into incompleteness/resource limitations. Quantifier instantiation is a known source of brittleness and potential non-termination in SMT-assisted verification. citeturn6academia25 Your dataset and RL environment should therefore preserve the verifier status rather than mapping every non-success into the same negative reward.

The fourth threat is **the trusted-computing-base gap**.

A proof is only as meaningful as the translation from program to logic and the correctness of the verifier/compiler chain. Work on a verified VCG and compiler for Dafny was explicitly motivated by soundness bugs in the conventional tools. citeturn6academia27 This does not make ordinary Dafny unsuitable for ML experiments, but it means the paper should say “proved with respect to the verifier's formal model,” rather than implying an unconditional mathematical guarantee about deployed machine code.

The fifth threat is **formalization coverage**.

Real programs interact with files, networks, operating systems, package ecosystems, time, nondeterminism, floating point, hardware and concurrency. Some of these can certainly be modeled formally, but doing so dramatically increases specification cost. FVSpec's conversion of only 2,772 out of 11,039 collected real-world property-based tests illustrates that even translating existing executable properties into a proof environment is currently nontrivial. citeturn3academia0

This means your strongest defensible claim is:

> **Proof supervision can replace concrete execution feedback for the subset of target semantics that is faithfully formalized and tractable for the verifier.**

Not:

> Formal proof makes runtime evidence obsolete.

The sixth threat is **cost**.

Your slide currently describes runtime verification/RL as delayed and costly and proof feedback as early and local. fileciteturn0file3 The “local” part is well supported by VC decomposition and systems such as LORIS. citeturn9view4 The “cheaper” part must remain an empirical hypothesis. A thousand integer unit tests may take milliseconds, whereas one quantified nonlinear proof can time out; conversely, running generated software inside isolated dependency-heavy environments can be much more expensive than a small SMT query. Frama-C and SMT research both emphasize that verification cost depends strongly on the property and logical fragment. citeturn7search0turn6academia25

A very good paper can actually find a **phase diagram** rather than a universal winner:

\[
\begin{array}{c|c}
\text{task regime} & \text{preferred oracle}\\
\hline
\text{simple executable function, cheap tests} & \text{execution}\\
\text{large input space, concise invariant} & \text{proof}\\
\text{weak/learned specification} & \text{proof + execution}\\
\text{environmental behavior} & \text{execution}\\
\text{safety invariant over huge state space} & \text{proof}
\end{array}
\]

That would be a more valuable result than trying to prove that one oracle dominates everywhere.

## Recommended research claim

I would revise the intellectual framing from:

> “Formal methods can replace RL because a prover does not need to execute the program.”

to:

> **“Formal verification provides an alternative semantic oracle to concrete execution. We study whether decomposed proof obligations can provide better training-time credit assignment than execution outcomes and execution traces, and when proof and execution should be combined.”**

That change does three things.

First, it avoids the category mistake between **RL as an optimizer** and **execution as a reward source**. Re:Form, SpecRL and verifier-RL work make clear that formal feedback can itself be used inside RL. citeturn10view0turn13view0

Second, it places the novelty beyond already-established binary verifier reward.

Third, it makes the comparison against ExecVerify and StepCodeReasoner unavoidable and therefore scientifically much stronger. citeturn11view4turn1academia15

The main hypothesis I would put in the paper is:

> **Under matched training data, model size, optimization algorithm, and total compute, verification-condition-level supervision will yield higher formal correctness and stronger prover-free semantic transfer than outcome-level test rewards, and will outperform equally dense execution-state supervision on properties for which symbolic proof provides input-independent correctness evidence.**

The hybrid hypothesis should be:

> **When specifications are incomplete or partially inferred, combining proof-based soundness signals with execution-based counterexamples or adequacy tests will outperform proof-only training because verification cannot by itself determine whether the formal specification captures the intended behavior.**

That hypothesis now has unusually strong prior motivation from SpecRL and formal semantic-equivalence self-play. citeturn13view0turn0academia3

Your primary contribution can be stated as:

> **We convert the internal structure of deductive program verification—initiation, inductiveness, postcondition sufficiency, safety and termination obligations—into verifiable process supervision for code-language-model post-training. Unlike verifier-in-the-loop systems that use proof only to accept, reject or repair completed outputs, our method uses individual proof obligations as semantic credit-assignment units and distills this experience into model parameters.**

And the central experiment is:

\[
\boxed{
\text{test outcome}
\;\;vs.\;\;
\text{execution state}
\;\;vs.\;\;
\text{proof outcome}
\;\;vs.\;\;
\text{proof obligation}
\;\;vs.\;\;
\text{hybrid}.
}
\]

That is considerably more defensible than comparing only G1 runtime RL against G3 formal RL.

A suitable paper title would be:

> **From Execution Rewards to Proof Rewards: Semantic Credit Assignment for Code Language Models**

or, even more precisely:

> **Execution or Proof? A Controlled Study of Verifiable Semantic Supervision for Code Language Models**

The second title may ultimately be stronger because it does not assume the result.

The most important sentence for your interview slide is also slightly different from the current one. Instead of:

> “If we can prove the program, we do not need runtime to tell us it is correct.”

I would use:

> **“For formally specified properties, proof can replace sampled execution as the correctness oracle—and can expose which semantic obligation failed. For incompletely specified behavior, proof and execution provide complementary evidence.”**

That wording preserves the ambitious idea on page 1 of your current research overview while closing its largest theoretical vulnerability. fileciteturn0file3

The field has now supplied almost every component needed to test the thesis: execution-feedback RL is mature enough to provide serious baselines; dense execution-state rewards exist; verifier-driven RL exists; specification hacking has been empirically exposed; local SMT-checked reasoning feedback works; proof-aware planning works; and proof-certified code reasoning has shown downstream transfer. citeturn2search2turn11view4turn10view0turn9view2turn9view4turn4academia1turn0academia3 What remains genuinely compelling is to put those ingredients into **one controlled causal experiment** and determine whether a model learns more from *what must always be true* than from *what happened on sampled executions*.



====source 


Activity · 5m

Citations · 27

arxiv.org
arxiv.org

1
[2507.16331] Re:Form -- Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny
https://arxiv.org/abs/2507.16331

3
Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification
https://arxiv.org/abs/2604.17010

10
Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification
https://arxiv.org/abs/2604.17010?utm_source=chatgpt.com

5
Reinforcement Learning with Negative Tests as Completeness Signal for Formal Specification Synthesis
https://arxiv.org/abs/2604.05820

6
[2603.11226] ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning
https://arxiv.org/abs/2603.11226

7
StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning
https://arxiv.org/abs/2605.11922?utm_source=chatgpt.com

8
[2605.30914] Automating Formal Verification with Reinforcement Learning and Recursive Inference
https://arxiv.org/abs/2605.30914

9
[2605.17914] Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors
https://arxiv.org/abs/2605.17914

11
P$^{3}$: Joint Program-and-Proof Planning for Verified Code Generation
https://arxiv.org/abs/2608.09277?utm_source=chatgpt.com

12
Verifiable Process Rewards for Agentic Reasoning
https://arxiv.org/abs/2605.10325?utm_source=chatgpt.com

18
Verified VCG and Verified Compiler for Dafny
https://arxiv.org/abs/2512.05262?utm_source=chatgpt.com

19
A Formal Model to Prove Instantiation Termination for E-matching-Based Axiomatisations (Extended Version)
https://arxiv.org/abs/2404.18007?utm_source=chatgpt.com

21
Re:Form -- Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny
https://arxiv.org/abs/2507.16331

22
AxDafny: Agentic Verified Code Generation in Dafny
https://arxiv.org/abs/2606.32007?utm_source=chatgpt.com

23
Verus: Verifying Rust Programs using Linear Ghost Types (extended version)
https://arxiv.org/abs/2303.05491?utm_source=chatgpt.com

24
A benchmark for vericoding: formally verified program synthesis
https://arxiv.org/abs/2509.22908?utm_source=chatgpt.com

25
FVSpec: Real-World Property-Based Tests as Lean Challenges
https://arxiv.org/abs/2606.01008?utm_source=chatgpt.com

26
CLEVER: A Curated Benchmark for Formally Verified Code Generation
https://arxiv.org/abs/2505.13938?utm_source=chatgpt.com

27
SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios
https://arxiv.org/abs/2512.18470?utm_source=chatgpt.com
proceedings.mlr.press
proceedings.mlr.press

2
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning
https://proceedings.mlr.press/v267/gehring25a.html?utm_source=chatgpt.com
•

4
Jian_Wang_Interview_30min copy.pdf

Jian_Wang_Interview_30min copy.pdf
nature.com
nature.com

13
Olympiad-level formal mathematical reasoning with reinforcement learning | Nature
https://www.nature.com/articles/s41586-025-09833-y?utm_source=chatgpt.com
microsoft.com
microsoft.com

14
Boogie: A Modular Reusable Verifier for Object-Oriented Programs - Microsoft Research
https://www.microsoft.com/en-us/research/publication/boogie-a-modular-reusable-verifier-for-object-oriented-programs/?utm_source=chatgpt.com

16
Dafny: A Language and Program Verifier for Functional Correctness - Microsoft Research
https://www.microsoft.com/en-us/research/project/dafny-a-language-and-program-verifier-for-functional-correctness/?utm_source=chatgpt.com

17
HOL-Boogie "” An Interactive Prover for the Boogie Program-Verifier - Microsoft Research
https://www.microsoft.com/en-us/research/publication/hol-boogie-interactive-prover-boogie-program-verifier/?utm_source=chatgpt.com
frama-c.com
frama-c.com

15
Frama-C - Framework for Modular Analysis of C programs
https://www.frama-c.com/index.html?utm_source=chatgpt.com
dafny.org
dafny.org

20
Dafny Documentation
https://dafny.org/v3.10.0/DafnyRef/DafnyRef?utm_source=chatgpt.com
Sources scanned · 120

arxiv.org
arxiv.org
ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning


https://arxiv.org/abs/2603.11226

ReVeal: Self-Evolving Code Agents via Iterative Generation-Verification


https://arxiv.org/abs/2506.11442

Re:Form -- Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny


https://arxiv.org/abs/2507.16331

StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning


https://arxiv.org/abs/2605.11922

RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


https://arxiv.org/abs/2410.02089

Theorem Prover as a Judge for Synthetic Data Generation


https://arxiv.org/abs/2502.13137

Distilling LLM Feedback for Lean Theorem Proving


https://arxiv.org/abs/2605.30861

Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving


https://arxiv.org/abs/2507.23726

Leanabell-Prover-V2: Verifier-integrated Reasoning for Formal Theorem Proving via Reinforcement Learning


https://arxiv.org/abs/2507.08649

The Dafny Integrated Development Environment


https://arxiv.org/abs/1404.6602

A Formal Model to Prove Instantiation Termination for E-matching-Based Axiomatisations (Extended Version)


https://arxiv.org/abs/2404.18007

Who Verifies the Verifiers? A Computer-Checked Implementation of the DPLL Algorithm in Dafny


https://arxiv.org/abs/2007.10842

Verified VCG and Verified Compiler for Dafny


https://arxiv.org/abs/2512.05262

Verus: Verifying Rust Programs using Linear Ghost Types (extended version)


https://arxiv.org/abs/2303.05491

RustHorn: CHC-based Verification for Rust Programs (full version)


https://arxiv.org/abs/2002.09002

Verification of Programs by Combining Iterated Specialization with Interpolation


https://arxiv.org/abs/1412.1151

Proving Properties of Sorting Programs: A Case Study in Horn Clause Verification


https://arxiv.org/abs/1907.03999

LogicTree: Structured Proof Exploration for Coherent and Rigorous Logical Reasoning with Large Language Models


https://arxiv.org/abs/2504.14089

The AutoLyap software suite for computer-assisted Lyapunov analyses of first-order methods


https://arxiv.org/abs/2506.24076

Chat-Based Support Alone May Not Be Enough: Comparing Conversational and Embedded LLM Feedback for Mathematical Proof Learning


https://arxiv.org/abs/2602.18807

Faithful and Robust LLM-Driven Theorem Proving for NLI Explanations


https://arxiv.org/abs/2505.24264

openreview.net
openreview.net
Submissions | OpenReview


BIBTEX RECORD Click anywhere on the box above to highlight complete record [Button: Done] ICML 2025 CONFERENCE SUBMISSIONS * * * * #### PENCIL: Long Thoughts with Short Memory Chenxiao Yang, Nat...

Submissions | OpenReview


ICLR 2025 CONFERENCE SUBMISSIONS * #### Global-to-Local Support Spectrums for Model Explainability Lucas Agussurja, Xinyang Lu, Bryan Kian Hsiang Low * 27 Sept 2024 (modified: 05 Feb 2025) * Submi...

ConvCodeWorld: Benchmarking Conversational Code Generation in Reproducible Feedback Environments | OpenReview


CONVCODEWORLD: BENCHMARKING CONVERSATIONAL CODE GENERATION IN REPRODUCIBLE FEEDBACK ENVIRONMENTS HOJAE HAN, SEUNG-WON HWANG, RAJHANS SAMDANI, YUXIONG HE Published: 22 Jan 2025, Last Modified: 16 May...

Submissions | OpenReview


NEURIPS 2023 WORKSHOP INSTRUCTION SUBMISSIONS * #### Delve into PPO: Implementation Matters for Stable RLHF Rui Zheng, Shihan Dou, Songyang Gao, Yuan Hua, Wei Shen, Binghai Wang, Yan Liu, Senjie Jin...

Coarse-Tuning Models of Code with Reinforcement Learning Feedback | OpenReview


COARSE-TUNING MODELS OF CODE WITH REINFORCEMENT LEARNING FEEDBACK ABHINAV JAIN, CHIMA ADIOLE, THOMAS REPS, SWARAT CHAUDHURI, CHRIS JERMAINE 21 Sept 2023 (modified: 11 Feb 2024)Submitted to ICLR 2024...

InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback | OpenReview


INTERCODE: STANDARDIZING AND BENCHMARKING INTERACTIVE CODING WITH EXECUTION FEEDBACK JOHN YANG, AKSHARA PRABHAKAR, KARTHIK R NARASIMHAN, SHUNYU YAO Published: 26 Sept 2023, Last Modified: 02 Nov 202...

SynReason: Enhancing Synthesis Reasoning via Reinforcement Learning Experimental Feedback | OpenReview


SYNREASON: ENHANCING SYNTHESIS REASONING VIA REINFORCEMENT LEARNING EXPERIMENTAL FEEDBACK ELTON PAN, THORBEN PREIN, JUNO NAM, XIAOCHEN DU, SOOJUNG YANG, PENGFEI CAI, JENNIFER L.M. RUPP, RAFAEL GOMEZ-...

LEVER: Learning to Verify Language-to-Code Generation with Execution | OpenReview


LEVER: LEARNING TO VERIFY LANGUAGE-TO-CODE GENERATION WITH EXECUTION ANSONG NI, SRINI IYER, DRAGOMIR RADEV, VESELIN STOYANOV, WEN-TAU YIH, SIDA WANG, XI VICTORIA LIN Published: 24 Apr 2023, Last Mod...

Grounding code understanding in step-by-step execution | OpenReview


GROUNDING CODE UNDERSTANDING IN STEP-BY-STEP EXECUTION DAVID W. ZHANG, MICHAËL DEFFERRARD, CORRADO RAINONE, ROLAND MEMISEVIC 27 Sept 2024 (modified: 05 Feb 2025)Submitted to ICLR 2025 EveryoneRevisi...

Interpreting Learned Feedback Patterns in Large Language Models | OpenReview


INTERPRETING LEARNED FEEDBACK PATTERNS IN LARGE LANGUAGE MODELS LUKE MARKS, AMIR ABDULLAH, CLEMENT NEO, RAUNO ARIKE, DAVID KRUEGER, PHILIP TORR, FAZL BAREZ Published: 25 Sept 2024, Last Modified: 06...

Chain of Code: Reasoning with a Language Model-Augmented Code Emulator | OpenReview


CHAIN OF CODE: REASONING WITH A LANGUAGE MODEL-AUGMENTED CODE EMULATOR CHENGSHU LI, JACKY LIANG, ANDY ZENG, XINYUN CHEN, KAROL HAUSMAN, DORSA SADIGH, SERGEY LEVINE, LI FEI-FEI, FEI XIA, BRIAN ICHTER...

Let’s Try Again: Eliciting Multi-Turn Reasoning in Language Models via Simplistic Feedback | OpenReview


LET’S TRY AGAIN: ELICITING MULTI-TURN REASONING IN LANGUAGE MODELS VIA SIMPLISTIC FEEDBACK LICHENG LIU, ZIHAN WANG, LINJIE LI, CHENWEI XU, YIPING LU, HAN LIU, AVIRUP SIL, MANLING LI Published: 06 Oc...

ai.updf.com
ai.updf.com
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning Jonas Gehring,Kunhao Zheng,3 Authors,Gabriele Synnaeve 2024 · DOI: 10.48550/arXiv.2410.02089 arXiv.org · 65 Citations C...

newx.sg
newx.sg
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING 📅 2024-10-02 🏛️ arXiv.org 📈 Citations: 0 ✨ Influential: 0 📄 PDF♡ Bookmark📋 Share 🤖 AI Summary Current large languag...

proceedings.mlr.press
proceedings.mlr.press
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


https://proceedings.mlr.press/v267/gehring25a.html

catalyzex.com
catalyzex.com
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


TITLE:RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING PAPER AND CODE View Code Notebook Oct 02, 2024 Authors:Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Ta...

Kunhao Zheng


WHAT MAKES LARGE LANGUAGE MODELS REASON IN (MULTI-TURN) CODE GENERATION? Request Code Image: Bookmark button Image: Alert button Oct 10, 2024 Authors:Kunhao Zheng, Juliette Decugis, Jonas Gehring...

alphaxiv.org
alphaxiv.org
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning | alphaXiv


Submitted 18 Feb 2025 en RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING Jonas Gehring KZ Kunhao ZhengJade Copet VM Vegard Mella QC Quentin CarbonneauxTC Taco Cohe...

RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning | alphaXiv


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING

RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning | alphaXiv


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING

emergentmind.com
emergentmind.com
RLEF: Grounding Code LLMs with Execution Feedback


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING Published 2 Oct 2024 in cs.CL and cs.AI | (2410.02089v2) Abstract: LLMs deployed as agents solve user-specified tasks ove...

researchgate.net
researchgate.net
(PDF) RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning


Preprint PDF Available RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING * October 2024 DOI:10.48550/arXiv.2410.02089 * License * CC BY 4.0 Authors: Jonas Gehring * Ka...

paperswithcode.com
paperswithcode.com
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning | Papers With Code


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING 2 Oct 2024  ·  Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Taco Cohen, Gabriel Synnaeve · Edit social preview L...

nature.com
nature.com
Olympiad-level formal mathematical reasoning with reinforcement learning | Nature


https://www.nature.com/articles/s41586-025-09833-y

Mathematicians put AI model AlphaProof to the test | Nature


* NEWS AND VIEWS * 12 November 2025 MATHEMATICIANS PUT AI MODEL ALPHAPROOF TO THE TEST Mathematicians use computational tools to prove theorems. An AI model that is trained to use these tools might...

LLMs augmented hierarchical reinforcement learning with action primitives for long-horizon manipulation tasks | Scientific Reports


LLMs augmented hierarchical reinforcement learning with action primitives for long-horizon manipulation tasks Download PDF Download PDF * Article * Open access * Published: 21 October 2025 LLMS A...

The analysis of deep reinforcement learning for dynamic graphical games under artificial intelligence | Scientific Reports


The analysis of deep reinforcement learning for dynamic graphical games under artificial intelligence Download PDF Download PDF * Article * Open access * Published: 02 July 2025 THE ANALYSIS OF D...

Multi-robot hierarchical safe reinforcement learning autonomous decision-making strategy based on uniformly ultimate boundedness constraints | Scientific Reports


Multi-robot hierarchical safe reinforcement learning autonomous decision-making strategy based on uniformly ultimate boundedness constraints Download PDF Download PDF * Article * Open access * Pub...

Evolution of cooperation guided by the coexistence of imitation learning and reinforcement learning | Scientific Reports


Evolution of cooperation guided by the coexistence of imitation learning and reinforcement learning Download PDF Download PDF * Article * Open access * Published: 18 July 2025 EVOLUTION OF COOPER...

Empowering artificial intelligence with homomorphic encryption for secure deep reinforcement learning | Nature Machine Intelligence


* Article * Published: 01 December 2025 EMPOWERING ARTIFICIAL INTELLIGENCE WITH HOMOMORPHIC ENCRYPTION FOR SECURE DEEP REINFORCEMENT LEARNING * Chi-Hieu Nguyen  ORCID: orcid.org/0009-0002-6903-0163...

PRefLexOR: preference-based recursive language modeling for exploratory optimization of reasoning and agentic thinking | npj Artificial Intelligence


PRefLexOR: preference-based recursive language modeling for exploratory optimization of reasoning and agentic thinking Download PDF Download PDF * Article * Open access * Published: 14 May 2025 P...

Enhanced exploration in reinforcement learning using graph neural network based intrinsic reward mechanism | Scientific Reports


Enhanced exploration in reinforcement learning using graph neural network based intrinsic reward mechanism Download PDF Download PDF * Article * Open access * Published: 14 November 2025 ENHANCED...

Experience-based integral reinforcement learning consensus for unknown multi-agent systems | Scientific Reports


Experience-based integral reinforcement learning consensus for unknown multi-agent systems Download PDF Download PDF * Article * Open access * Published: 26 September 2025 EXPERIENCE-BASED INTEGR...

Competitive swarm reinforcement learning improves stability and performance of deep reinforcement learning | Scientific Reports


Competitive swarm reinforcement learning improves stability and performance of deep reinforcement learning Download PDF Download PDF * Article * Open access * Published: 11 December 2025 COMPETIT...

DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning | Nature


DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning Download PDF Download PDF * Article * Open access * Published: 17 September 2025 DEEPSEEK-R1 INCENTIVIZES REASONING IN LL...

microsoft.com
microsoft.com
Fine-grained Caching of Verification Results - Microsoft Research


FINE-GRAINED CACHING OF VERIFICATION RESULTS * Rustan Leino , * Valentin Wüstholz Computer Aided Verification | July 2015 Published by Springer International Publishing Switzerland Publication Do...

Boogie: A Modular Reusable Verifier for Object-Oriented Programs - Microsoft Research


https://www.microsoft.com/en-us/research/publication/boogie-a-modular-reusable-verifier-for-object-oriented-programs/

HOL-Boogie "” An Interactive Prover for the Boogie Program-Verifier - Microsoft Research


https://www.microsoft.com/en-us/research/publication/hol-boogie-interactive-prover-boogie-program-verifier/

Dafny: A Language and Program Verifier for Functional Correctness - Microsoft Research


https://www.microsoft.com/en-us/research/project/dafny-a-language-and-program-verifier-for-functional-correctness/

A Polymorphic Intermediate Verification Language: Design and Logical Encoding - Microsoft Research


A POLYMORPHIC INTERMEDIATE VERIFICATION LANGUAGE: DESIGN AND LOGICAL ENCODING * Rustan Leino , * Philipp Rümmer Conference: Tools and Algorithms for the Construction and Analysis of Systems, 16th In...

Specification and Verification of Object-Oriented Software - Microsoft Research


SPECIFICATION AND VERIFICATION OF OBJECT-ORIENTED SOFTWARE * Rustan Leino Marktoberdorf International Summer School 2008 | June 2008 Download BibTex The specification of object-oriented and other...

Dafny: An Automatic Program Verifier for Functional Correctness - Microsoft Research


DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS * Rustan Leino 16th International Conference, LPAR-16, Dakar, Senegal | April 2010 Published by Springer Berlin Heidelberg Publicat...

The Boogie Verification Debugger - Microsoft Research


THE BOOGIE VERIFICATION DEBUGGER * Claire Le Goues , * Rustan Leino , * Michał Moskal SEFM 2011 | May 2011 Download BibTex The Boogie Verification Debugger (BVD) is a tool that lets users explore...

HOL-Boogie — An Interactive Prover-Backend for the Verifying C Compiler - Microsoft Research


HOL-BOOGIE — AN INTERACTIVE PROVER-BACKEND FOR THE VERIFYING C COMPILER * Sascha Bohme , * Michal Moskal , * Wolfram Schulte , * Burkhart Wolff Journal of Automated Reasoning | February 2010 Publi...

Co-Induction Simply: Automatic Co-Inductive Proofs in a Program Verifier - Microsoft Research


CO-INDUCTION SIMPLY: AUTOMATIC CO-INDUCTIVE PROOFS IN A PROGRAM VERIFIER * Rustan Leino , * Michal Moskal MSR-TR-2013-49 | July 2013 Download BibTex Program verification relies heavily on inductio...

Dafny Meets the Verification Benchmarks Challenge - Microsoft Research


DAFNY MEETS THE VERIFICATION BENCHMARKS CHALLENGE * Rustan Leino , * Rosemary Monahan VSTTE'10 Proceedings of the Third international conference on Verified software: theories, tools, experiments |...

The Dafny Program Verifier - Microsoft Research


THE DAFNY PROGRAM VERIFIER * Rustan Leino Seminar, Victoria University of Wellington, Wellington, New Zealand | April 2010 Published by Microsoft Research Download BibTex * Tools and specificatio...

dafny.org
dafny.org
Dafny Documentation


https://dafny.org/v3.10.0/DafnyRef/DafnyRef

Dafny Documentation


* 25.5.1.4. `dafny translate <language>` * 25.5.1.5. `dafny build` * 25.5.1.6. `dafny run` * 25.5.1.7. `dafny server` * 25.5.1.8. `dafny audit` * 25.5.1.9. `dafny format` * 25.5.1.10. `dafny test` * 2...

Dafny Documentation


Dafny Reference Manual The dafny-lang community v3.9.0 release snapshot Abstract: This is the Dafny reference manual; it describes the Dafny programming language and how to use the Dafny verificati...

How do labels in preconditions work? | Dafny Documentation


QUESTION How do labels in preconditions work? ANSWER `method M0(x: int) requires x == 0 { assert x < 10; // verifies } method M1(x: int) requires Zero: x == 0 { // the following assertion does not...

Dafny Documentation


Dafny Reference Manual The dafny-lang community Development version Abstract: This is the Dafny reference manual; it describes the Dafny programming language and how to use the Dafny verification s...

I can assert a condition right before a return, so why does the postcondition fail to verify? | Dafny Documentation


QUESTION I can assert a condition right before a return, so why does the postcondition fail to verify? ANSWER There can be lots of reasons why a postcondition might fail to verify, but if you can p...

Dafny Documentation


Dafny Reference Manual The dafny-lang community v4.0.0 release snapshot Abstract: This is the Dafny reference manual; it describes the Dafny programming language and how to use the Dafny verificati...

Lemmas and Induction | Dafny Documentation


```dafny lemma ClosedLemma(subgraph: set, root: Node, goal: Node, graph: set) requires closed(subgraph) && closed(graph) && subgraph <= graph requires root in subgraph && goal in graph - subgraph ensu...

Avoiding verification brittleness in Dafny | Dafny Blog


MORE GENERAL GUIDELINES The examples covered so far illustrate two key principles for maintainable verification: * Break long leaps of reasoning down into smaller steps. This limits the number of re...

Is there a way to ask Dafny to die on its first verification failure? | Dafny Documentation


QUESTION Is there a way to ask Dafny to die on its first verification failure? ANSWER No. At least as of version 3.7.3.

Dafny


DAFNY v3.9.1 documentation snapshot Image: Dafny | Dafny is a verification-aware programming language that has native support for recording specifications and is equipped with a static program veri...

Verification Optimization | Dafny Documentation


OPAQUE SPECIFICATION CLAUSES In addition to top-level definitions, assertions, preconditions, postconditions, and loop invariants can be made opaque. If you add a label to any instance of one of thes...

frama-c.com
frama-c.com
Frama-C - Framework for Modular Analysis of C programs


https://www.frama-c.com/index.html

WP


WP Included in main Frama-C distribution Deductive proofs of ACSL contracts. API Documentation | Publications OVERVIEW This plug-in allows proving that ACSL contracts are fulfilled for all possibl...

Chromium


Frama-C [Input] FRAMA-C V24 CHROMIUM FRAMA-C V24.0 CHROMIUM [CHANGELOG] Source distribution [Compilation instructions] User manual Plug-in development guide [Hello plug-in tutorial archive] API...

Message 1 from Frama-C-discuss on April 2018


FRAMA-C-DISCUSS MAILING LIST ARCHIVES This page gathers the archives of the old Frama-C-discuss archives, that was hosted by Inria's gforge before its demise at the end of 2020. To search for mails...

Chlorine


Frama-C [Input] FRAMA-C V17 CHLORINE FRAMA-C V17.1 CHLORINE [CHANGELOG] Source distribution [Compilation instructions] User manual Plugin-In development guide [Hello plug-in tutorial archive] AP...

Phosphorus


Frama-C [Input] FRAMA-C V15 PHOSPHORUS 14-Silicon Latest Version 16-Sulfur FRAMA-C V15.0 PHOSPORUS [CHANGELOG] Source distribution [Compilation instructions] User manual Plug-In development gu...

Message 22 from Frama-C-discuss on April 2011


FRAMA-C-DISCUSS MAILING LIST ARCHIVES This page gathers the archives of the old Frama-C-discuss archives, that was hosted by Inria's gforge before its demise at the end of 2020. To search for mails...

Admit and check annotations in ACSL


ADMIT AND CHECK ANNOTATIONS IN ACSL André Maroneze - 10th Jun 2021 In Frama-C 23 (Vanadium), two new kinds of ACSL annotations are available, to complement `assert`: the `admit` and `check` annotat...

Publications


Frama-C [Input] PUBLICATIONS FRAMA-C FRAMEWORK MANUALS Loïc Correnson, Pascal Cuoq, Florent Kirchner, André Maroneze, Virgile Prevosto, Armand Puccetti, Julien Signoles, Boris Yakobowski Frama-C...

ACSL - Frama-C


ANSI/ISO C SPECIFICATION LANGUAGE QUICK DESCRIPTION The ANSI/ISO C Specification Langage (ACSL) is a behavioral specification language for C programs. The design of ACSL is inspired of JML. It also...

A reference peeve


A REFERENCE PEEVE Pascal Cuoq - 20th Jan 2012 One thing has been peeving me for a while. It is small and does not impact me directly, so I didn't speak up, but perhaps I should. Many people, some...

Message 15 from Frama-C-discuss on March 2018


FRAMA-C-DISCUSS MAILING LIST ARCHIVES This page gathers the archives of the old Frama-C-discuss archives, that was hosted by Inria's gforge before its demise at the end of 2020. To search for mails...

minicod.com
minicod.com
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning — Jonas Gehring et al. — International Conference on Machine Learning | Minicod


RLEF: GROUNDING CODE LLMS IN EXECUTION FEEDBACK WITH REINFORCEMENT LEARNING Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Taco Cohen, Gabriel Synnaeve International Conference on Machine L...

Connector sources scanned

No connector sources scanned

