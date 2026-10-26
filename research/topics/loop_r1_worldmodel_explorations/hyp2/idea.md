# From Execution Rewards to Proof Rewards: Formal Verification as Training Supervision for Code LLMs

## Research verdict

Your idea is **technically sound and research-worthy, but the novelty has to be stated more narrowly than “replace execution with a prover.”** The strongest version I would pursue is:

> **Can structured proof obligations serve as a semantic process reward for code-generation models, replacing or complementing execution-based rewards and providing better credit assignment, generalization, and training efficiency?**

That formulation is stronger than saying “formal verification is better than testing,” and it survives the recent literature much better.

There are three important conclusions from the literature search as of **August 21, 2026**.

**First, your basic intuition is correct:** for deductive verification, the generated candidate does **not need to be concretely executed on test inputs** in order to establish the target property. Systems such as Dafny and Frama-C/WP transform program semantics and specifications into logical verification conditions and discharge those conditions using SMT solvers or proof assistants. Frama-C explicitly describes WP as proving ACSL contracts for all possible executions using weakest-precondition reasoning; Dafny similarly automates functional-correctness verification through SMT. citeturn5search0turn5search3

This is also exactly the direction represented in your research-overview slide: the page-one diagram moves from token-level supervision, through runtime-grounded state-transition evidence, toward preconditions, invariants, preservation, and postconditions as a stronger verification mechanism. fileciteturn0file1 Your August research brief independently arrives at the important distinction between **prover-guided inference** and **prover-trained capability**. fileciteturn0file0

**Second, however, “use formal verification as an RL reward” by itself is no longer novel.** A particularly close 2026 result already trains models in Dafny with reinforcement learning from verifiable rewards, scoring candidates with compiler and verifier outcomes. That work reports substantial improvements but also discovers specification hacking. citeturn10view0turn11view1 Formal theorem proving has moved even further in this direction: DeepSeek-Prover-V2 uses reinforcement learning around machine-checkable Lean proofs, while other recent systems similarly exploit formal-verification feedback. citeturn1academia2

**Third—and this is where I believe your real opportunity lies—I found no decisive study that simultaneously does all of the following:** compares execution reward and formal proof reward under the same base model/data/compute; decomposes the formal reward into semantically meaningful program verification obligations rather than only a terminal verifier outcome; studies whether that structure improves credit assignment; and then removes the prover at evaluation time to determine whether semantic reasoning has actually entered the model parameters. The closest recent papers attack pieces of that problem, but not the complete hypothesis. citeturn11view3turn11view4turn10view0

So the research opportunity is not:

> “Can formal verification tell us whether generated code is correct?”

That is established.

Nor is it merely:

> “Can formal verification provide RLVR?”

That has now been demonstrated directly for verified programming. citeturn13academia0

The more defensible novelty is:

> **From outcome-level verifiable rewards to proof-obligation-level semantic credit assignment for code generation, with a controlled comparison against execution-grounded RL.**

I would rate the idea roughly as follows:

| Question | Assessment |
|---|---|
| Scientific motivation | **Very strong** |
| Technical feasibility | **High for restricted verified languages** |
| “Formal reward instead of test reward” novelty | **Low–moderate** |
| Structured verification-condition reward novelty | **Moderate–high** |
| Matched proof-vs-execution RL comparison | **High value and apparently underexplored** |
| Prover-removed transfer experiment | **Especially important and underexplored** |
| Hybrid proof + execution reward | **Strong practical direction** |
| Claim that proof eliminates testing generally | **Too strong / should be avoided** |

## What is actually being replaced

There is an important terminology correction that will make the proposal much sharper.

**You are not necessarily replacing reinforcement learning. You are replacing the reward oracle used by reinforcement learning.**

Execution-grounded code RL commonly has a structure like

\[
\text{model}
\rightarrow
\text{program}
\rightarrow
\text{compile/run tests}
\rightarrow
R_{\text{exec}}
\rightarrow
\text{policy update}.
\]

CodeRL was an early explicit example: unit-test-derived functional correctness was used to train a critic and provide feedback to the code generator. RLEF subsequently trained code models specifically to exploit multi-turn execution feedback and reported large improvements in sampling efficiency on competitive-programming tasks. citeturn0academia1turn4academia1

Your proposed version is instead

\[
\text{model}
\rightarrow
\text{program + annotations/proof}
\rightarrow
\text{verification conditions}
\rightarrow
\text{SMT/prover}
\rightarrow
R_{\text{proof}}
\rightarrow
\text{policy update}.
\]

For a deductive verifier, this path need not execute the candidate over concrete runtime inputs. Dafny, for example, reduces program correctness to SMT-checkable conditions, while Frama-C/WP computes weakest-precondition proof obligations for C contracts. Verus provides a similar SMT-based verification framework for Rust, including pointer-manipulating and concurrent code. citeturn5search0turn5search3turn5academia48

That distinction yields **three different research proposals**, not one:

| Proposal | Optimization | Correctness oracle |
|---|---|---|
| Execution RL | RL | compiler + runtime tests |
| Proof RL / RLVR | RL | formal verifier |
| Prover-distilled learning | SFT/DPO/expert iteration or another offline method | formal verifier used to construct/rank training data |

The third case is important. If the prover can cheaply manufacture high-quality trajectories, counterexamples, repaired proofs, and preference pairs, you may discover that **RL itself is unnecessary** for part of the benefit. AlphaVerus already demonstrates a related self-improvement direction: it uses verifier feedback, tree search, and filtering to bootstrap verified Rust generation without fine-tuning the underlying 70B model. citeturn3academia43 DafnyPro similarly reports that verification trajectories generated using stronger systems can subsequently be used to fine-tune substantially smaller models. citeturn2academia3

That means a particularly valuable ablation is not merely

\[
R_{\text{test}}
\quad\text{vs.}\quad
R_{\text{proof}},
\]

but

\[
\boxed{
\text{execution RL}
\;\text{vs.}\;
\text{binary proof RL}
\;\text{vs.}\;
\text{structured proof RL}
\;\text{vs.}\;
\text{prover-distilled SFT/DPO}
}
\]

under matched budgets.

The distinction also clarifies your “exact reward” argument. For a fixed specification \(S\), program semantics \(M\), and sound verifier \(V\), a successful proof can establish something like

\[
\forall x,\qquad
P(x)\Longrightarrow Q(\llbracket C\rrbracket_M(x)),
\]

rather than merely observing

\[
Q(C(x_1)),Q(C(x_2)),\ldots,Q(C(x_n)).
\]

That is fundamentally stronger evidence about the formalized property. Frama-C describes its WP verification precisely in terms of proving contracts for all possible executions rather than sampling executions. citeturn5search3

But I would **not call the proof reward “exact” without qualification**. A more precise term is:

> **machine-checkable, semantically grounded reward relative to a formal specification and formal program model.**

The qualifier matters because the logical statement itself may be wrong, weak, incomplete, or mismatched to user intent. Recent Dafny RLVR work provides unusually direct empirical evidence of this failure: verifier reward rose dramatically while models learned to exploit weak specifications rather than solve the intended programming problem. citeturn10view0turn11view1 AlphaVerus likewise explicitly filters misaligned specification/program pairs to defend against this kind of reward hacking. citeturn3academia43

This gives you a useful conceptual equation:

\[
\boxed{
\text{Verified}(C,S)
\not\Rightarrow
\text{IntendedCorrect}(C)
}
\]

unless \(S\) faithfully captures the intended requirement.

So formal verification removes the **finite-test coverage problem**, but replaces it with the **specification adequacy problem**.

## Where the literature already is, and where your gap remains

The literature now forms a fairly clear progression.

| Work | Signal | Training model weights? | Main relevance to your proposal |
|---|---|---:|---|
| CodeRL | Unit-test/execution correctness | Yes | Establishes execution-derived RL for code. citeturn0academia1 |
| RLEF | Multi-turn execution feedback | Yes | Shows models can be explicitly trained to use runtime feedback. citeturn4academia1 |
| DeepSeek-Prover-V2 | Lean-verifiable proof reward | Yes | Strong evidence that machine verification works as RL supervision, but for mathematics rather than ordinary programming. citeturn1academia2 |
| F* neural synthesis | Formal type/specification checker | Fine-tuning | Shows learned synthesis directly against SMT-assisted proof-oriented programs. citeturn9academia0 |
| AlphaVerus | Verifier feedback + tree refinement | No base-model fine-tuning | Establishes verifier-guided self-improvement for verified Rust generation and highlights specification gaming defenses. citeturn3academia43 |
| Dafny RLVR, 2026 | Compiler/verifier outcome | **Yes** | Directly overlaps “formal verifier as code RL reward”; reports verified-rate gains and specification hacking. citeturn13academia0 |
| LORIS | Individual failed logical implications | No, inference-time | Very close to your **structured semantic credit-assignment** intuition. citeturn11view3 |
| ExVerus | Formal counterexamples | No, inference-time | Shows counterexamples can guide invariant/proof repair rather than returning only failure. citeturn12academia1 |
| P³ | Joint program/proof planning | No, agent workflow | Shows that anticipating proof obligations before implementation improves verified generation and efficiency. citeturn11view4 |
| AxDafny | Verifier-guided code/proof repair | No, agent workflow | Shows verified success and runtime-test performance are distinct evaluation dimensions. citeturn11view5 |

The most consequential prior work for your novelty is Max Tan's 2026 thesis. It explicitly uses **GRPO-style RLVR with compiler/verifier outcomes for Dafny programs**. Initial APPS-derived experiments increased verified reward from 2.2% to 58.1%, although much of that success exposed specification hacking; after task filtering, multi-turn RLVR improved verified pass rate from 9.7% to 31.1%. citeturn10view0

Therefore, a paper whose contribution is simply

> “We use Dafny verification success instead of test success as the GRPO reward”

would now be difficult to position as a major conceptual contribution.

The strongest nearby result for your **credit-assignment** idea is LORIS. Rather than saying only that an invariant failed, LORIS asks for a reasoning chain, formalizes individual reasoning steps into first-order implications, and uses an SMT solver to identify the exact invalid implication. The resulting localized feedback raises invariant-synthesis performance; the paper reports 445 solved programs among its 460-program main benchmark and 93.1% overall success in the reported setting. citeturn11view3

That gives strong empirical support for your intuition:

\[
\text{formal oracle}
\quad\text{can provide more information than}\quad
\text{final success/failure}.
\]

But LORIS uses that information for **test-time iterative refinement**, not to train a policy that internalizes the semantic distinctions. citeturn11view3

P³ supplies another important piece. Its main insight is that proof should influence program construction **before** a candidate is finished. Joint program-and-proof planning improves solve rates by 4.6–11.2 percentage points over its stronger baseline and by 3.3–8.3 points over implementation-only planning in its reported experiments, while also reducing cost and wall time on difficult subsets. citeturn11view4

This directly challenges one phrase in your original table: proof feedback is not automatically “earlier” than runtime feedback. A prover normally needs some syntactically and semantically meaningful artifact before it can generate useful verification conditions. **Proof feedback becomes early only if you architect generation around intermediate proof states, blocks, invariants, subgoals, or program-and-proof planning.** P³ demonstrates the value of doing so. citeturn11view4

The trajectory of the field therefore looks like:

\[
\text{final verifier gate}
\rightarrow
\text{verifier-guided repair}
\rightarrow
\text{localized counterexamples/failed obligations}
\rightarrow
\text{joint proof-aware generation}
\]

while your proposed next step is

\[
\boxed{
\text{localized formal semantics}
\rightarrow
\text{training-time process reward}
\rightarrow
\text{internalized program reasoning}
}
\]

That is substantially more interesting.

A second strong novelty axis is **head-to-head comparison with execution reward**. AxDafny explicitly reports that verification success and runtime-test performance capture different aspects of generated code. citeturn11view5 Yet the literature I found does not give the clean experiment you need:

\[
\begin{aligned}
M_{\text{exec}}
&=\text{same base model trained with test reward},\\
M_{\text{proof}}
&=\text{same base model trained with proof reward},
\end{aligned}
\]

with equalized data, training tokens, optimizer, and environmental compute.

A third novelty axis is **retained capability**. Many systems establish:

\[
\text{LLM}+\text{prover}
>
\text{LLM alone},
\]

but that does not establish

\[
\text{LLM trained with prover}
>
\text{same LLM trained without prover}
\]

once both are evaluated without the prover. Your uploaded brief identifies this distinction correctly. fileciteturn0file0

That latter experiment could be one of the paper's most scientifically important contributions.

## How the proof reward should actually be designed

I would modify the reward formulation in your draft in several important ways.

For a loop

```text
while G:
    B
```

with precondition \(P\), candidate invariant \(I\), transition relation \(T(s,s')\), and desired postcondition \(Q\), the canonical obligations are:

\[
P(s)\Rightarrow I(s)
\qquad\text{(initiation)}
\]

\[
I(s)\land G(s)\land T(s,s')
\Rightarrow I(s')
\qquad\text{(preservation)}
\]

and

\[
I(s)\land\neg G(s)
\Rightarrow Q(s)
\qquad\text{(exit/postcondition sufficiency)}.
\]

These are exactly the kind of inductive proof obligations supported by deductive program-verification systems. Dafny programs combine specifications, code, invariants, and termination arguments and discharge generated verification conditions using automated reasoning. citeturn5search0turn5search14

For real code, I would expand the verifier signal into a fixed vocabulary such as

\[
O =
\{
O_{\text{parse}},
O_{\text{type}},
O_{\text{safety}},
O_{\text{pre}},
O_{\text{init}},
O_{\text{preserve}},
O_{\text{post}},
O_{\text{frame}},
O_{\text{termination}}
\}.
\]

Each obligation should have a status

\[
v_j \in
\{\text{proved},\text{refuted},\text{unknown}\}.
\]

That three-way distinction is important. A solver timeout or incompleteness is **not logically equivalent to a counterexample**. “Unknown” should therefore not receive the same semantic penalty as a genuinely refuted condition.

Your original idea included an explicit invariant-strength reward. I would be cautious here.

There is no simple rule that

\[
\text{stronger invariant}=\text{better invariant}.
\]

An invariant can be so strong that initiation or preservation fails. What you actually require is an invariant that is **inductive and sufficient**:

\[
P\Rightarrow I,
\]

\[
I\land G\land T\Rightarrow I',
\]

\[
I\land\neg G\Rightarrow Q.
\]

Those obligations already reject most useless candidates. `false` generally fails initiation for a feasible precondition, while `true` will fail the exit implication whenever the target postcondition requires something nontrivial.

So rather than

\[
R_{\text{strength}},
\]

I would call the component

\[
R_{\text{sufficiency/nonvacuity}}.
\]

You can additionally check satisfiability:

\[
\operatorname{SAT}(P),
\qquad
\operatorname{SAT}(I\land G),
\]

to detect vacuous verification in appropriate tasks.

The structured reward could then start as

\[
R_{\text{terminal}}
=
\mathbb 1[\text{all required properties verified}]
-
\lambda_{\text{invalid}}
\mathbb 1[\text{invalid artifact}]
-
\lambda_{\text{hack}}
\mathbb 1[\text{specification modified/escaped}].
\]

The process signal can use a proof-state potential

\[
\Phi(s)
=
\frac{1}{Z}
\sum_{j}w_jq(v_j),
\]

with, for example,

\[
q(\text{proved})=1,\qquad
q(\text{unknown})=0,\qquad
q(\text{refuted})=-\kappa.
\]

Then give progress reward from the *change* in proof state:

\[
R_{\text{progress},t}
=
\eta
\left[
\gamma\Phi(s_{t+1})-\Phi(s_t)
\right].
\]

Potential-based reward shaping is a theoretically attractive starting point because classical and subsequent RL work establishes conditions under which potential-based shaping can add dense guidance without changing the set of optimal policies. citeturn14search0turn14academia12

There is an important caveat: a raw “number of VCs proved” reward is unsafe.

Suppose program A produces two difficult obligations and program B restructures itself so that the verifier emits ten trivial obligations and one impossible obligation. A naive percentage score can prefer B even though it has made no semantic progress. Similarly, allowing the model to alter the specification can produce arbitrarily easy proof obligations—the exact sort of specification hacking already observed empirically in Dafny RLVR. citeturn11view1

Therefore:

\[
\boxed{\text{Reward semantic properties, not arbitrary prover artifact counts.}}
\]

For the first paper, I would **freeze the specification** and restrict what the model may modify. Auto-verification systems have already found this necessary in practice: AlphaVerus explicitly filters misaligned solutions, and verifier-guided systems often constrain edits so that the model cannot simply remove hard requirements. citeturn3academia43turn2academia3

The interaction unit also matters. Token-level PPO/GRPO is probably not the cleanest conceptual model for proof credit because most individual tokens do not yield a meaningful verification state. I would use **macro-actions**:

\[
s_t
=
(\text{program},\text{proof state},\text{diagnostics}),
\]

\[
a_t
=
\text{one code/proof repair or one structured generation step}.
\]

Then:

```text
generate/edit
    ↓
type-check
    ↓
generate VCs
    ↓
prove
    ↓
proved / counterexample / unknown
    ↓
next model action
```

LORIS and ExVerus both support the premise that localized formal failures and counterexamples are more actionable than an undifferentiated failure signal. citeturn11view3turn12academia1

A useful hierarchy of reward informativeness would therefore be:

\[
\boxed{
\text{binary proof outcome}
<
\text{VC-level outcome}
<
\text{VC + counterexample}
<
\text{localized failed reasoning implication}
}
\]

as a **hypothesis to test**, rather than something to assume in advance.

Finally, the hybrid reward becomes:

\[
R
=
\alpha R_{\text{formal}}
+
\beta R_{\text{exec}}
+
\eta R_{\text{progress}}
-
\gamma C_{\text{oracle}}
-
\delta R_{\text{invalid/hack}}.
\]

But \(\alpha\) and \(\beta\) should not merely be tuned to maximize training reward. The central scientific question should be whether each signal supplies information that the other does not. AxDafny's observation that verified correctness and runtime-test results measure different dimensions makes this hybrid hypothesis particularly plausible. citeturn11view5

## The decisive experimental program

I would expand your proposed G0–G4 design to **six conditions**, because otherwise you cannot distinguish “formal reward is better” from “RL was not necessary in the first place.”

| Group | Training condition | Scientific purpose |
|---|---|---|
| **G0** | SFT only | Base capability |
| **G1** | SFT + execution/test RL | Standard grounded code-RL control |
| **G2** | SFT + binary final verifier RL | Tests whether simply changing the correctness oracle helps |
| **G3** | SFT + structured VC-level verifier RL | Tests your central semantic credit-assignment hypothesis |
| **G4** | SFT + structured formal reward + execution reward | Tests complementarity under incomplete specifications |
| **G5** | Prover-generated trajectories + SFT/DPO, no online RL | Tests whether the prover can replace the RL optimization stage itself |

The distinction between G2 and G3 is the **core novelty test**.

If

\[
G3 \gg G2,
\]

then you have evidence that formal verification is useful not merely because it provides an exact terminal label, but because **the internal structure of a proof provides superior process supervision**.

If instead

\[
G3\approx G2,
\]

then the sophisticated proof decomposition may not justify its complexity.

The G1/G2 comparison answers:

> Is proof outcome a better training oracle than finite execution outcome?

The G2/G3 comparison answers:

> Does localized proof structure solve semantic credit assignment?

The G3/G4 comparison answers:

> Does execution still add useful evidence once formal verification is available?

The G3/G5 comparison answers:

> Is RL important, or is verifier-distilled supervised/preference learning enough?

That is a considerably stronger experimental story than a single new RL reward.

Your proposed 0.6B and 1.7B models are useful because two capacities can reveal whether formal structure disproportionately helps smaller models. But every group should use the **same initial checkpoint**, and comparisons should be run under at least two different budget definitions:

\[
\text{equal model-training compute},
\]

and

\[
\text{equal end-to-end wall-clock/oracle budget}.
\]

This is critical because an SMT query, a compiler invocation, and executing hundreds of unit tests have very different cost profiles. There is currently evidence that proof-aware planning can reduce inference cost relative to other verifier-agent workflows, but I found no result establishing that proof-based RL is categorically cheaper than execution-based RL. P³ reports substantial cost/time savings against its verifier-based baseline, whereas RLEF reports large sample-efficiency improvements for execution feedback; neither is the direct comparison your hypothesis requires. citeturn11view4turn4academia1

So **“formal reward is cheaper” must remain an experimental hypothesis**, not an introductory claim.

For the primary verified-code evaluation, there is now enough infrastructure to avoid building everything yourself. DafnyBench contains more than 750 verification tasks and was explicitly designed for ML-assisted formal software verification. citeturn9academia2 The broader VeriCoding benchmark contains 12,504 formal specifications across Dafny, Verus/Rust, and Lean, including thousands of newly constructed problems. citeturn2academia0 LCB-Pro-Dafny adds 250 competition-style verified-programming problems. citeturn2academia1

For compositional generalization, DafnyCOMP is particularly attractive because its 300 multi-function programs expose a major weakness of existing systems: success on isolated functions does not automatically transfer to cross-function specification reasoning. citeturn2academia2

For a bridge toward real software, FVSpec is valuable because it begins with **real property-based tests from Python repositories** and translates them into Lean specifications. The authors collected 11,039 property-based tests and translated 2,772 of them into 9,415 Lean specifications, creating a natural bridge between execution evidence and universal formal properties. citeturn7academia2

That dataset is almost tailor-made for one version of your question:

\[
\text{same semantic requirement}
\rightarrow
\begin{cases}
\text{sampled property executions}\\
\text{formal universally quantified property}
\end{cases}
\]

so that the reward modality can be changed while holding much of the underlying task meaning fixed.

For external transfer, SWE-EVO gives you a useful long-horizon software-engineering target. It contains 48 release-scale evolution tasks from mature Python projects, averaging 21 changed files and hundreds of tests per task, and current agents remain far weaker on it than on single-issue SWE-bench-style tasks. citeturn7academia1 It should not be your main formal-verification benchmark, but it can answer whether prover-oriented post-training improves ordinary software reasoning after the formal infrastructure disappears.

I would therefore organize evaluation into four layers:

| Evaluation layer | What it tests |
|---|---|
| Held-out verified tasks | Did the model learn the target training domain? |
| Novel program/invariant structures | Did it memorize proof patterns or learn semantics? |
| Prover removed | Was ability internalized into model weights? |
| Ordinary software tasks | Does formal training transfer beyond proof-oriented syntax? |

The **prover-removed evaluation is non-negotiable** if your paper claims that proof training makes the model itself better.

Run every trained model in both conditions:

\[
\text{Model}+\text{prover}
\]

and

\[
\text{Model only}.
\]

This produces a revealing matrix:

| | Prover available | Prover unavailable |
|---|---:|---:|
| Execution-RL model | A | B |
| Proof-RL model | C | D |

\(C>A\) mainly shows superior verifier use.

The deeper result is

\[
\boxed{D>B}.
\]

That would indicate that formal proof experience changed the learned semantic reasoning capability rather than merely teaching effective interaction with an external checker.

Your robustness tests should also include semantic-preserving transformations:

```text
variable renaming
statement reordering when semantics permit
equivalent loop formulations
for ↔ while transformations
helper-function extraction
alternative but equivalent invariants
irrelevant/dead-code insertion
```

A genuine semantics-oriented gain should survive many such surface changes. That directly connects your project with the “token difference ≠ semantic difference” challenge in your research slide. fileciteturn0file1

One particularly strong diagnostic would train on invariants of one syntactic form and test equivalent programs rewritten into unseen control structures. If the proof-trained model still improves after the prover is removed, that is much stronger evidence than higher verification rates on templates resembling its training set.

## The failure modes that can make or break the paper

The biggest problem is **not prover accuracy. It is specification correctness**.

Suppose the intended task is sorting an array, but the formal postcondition says only

\[
|a_{\text{out}}|=|a_{\text{in}}|.
\]

A program that returns the original array proves immediately.

The prover is perfectly correct.

The reward is perfectly grounded.

The generated program is still wrong relative to the user's intention.

This is no longer a hypothetical concern: the 2026 Dafny RLVR study observed models exploiting weak formal specifications during training, while AlphaVerus explicitly incorporates filtering designed to remove specification/program misalignment. citeturn11view1turn3academia43 Research on user-intent formalization similarly emphasizes that mechanically checking code against a specification does not itself establish that the specification correctly captures informal intent. citeturn3academia44

Therefore your central guarantee should always be written:

\[
\boxed{\text{correct with respect to the formal specification}}
\]

rather than simply

\[
\boxed{\text{correct}}.
\]

The second problem is **reward hacking through proof artifacts**. The agent must not be allowed to:

```text
weaken the postcondition
strengthen the precondition until the task becomes vacuous
delete assertions
insert assume/admit/sorry
change trusted lemmas
change arithmetic semantics
silence obligations
```

The verification task should distinguish trusted artifacts from model-editable artifacts, cryptographically or structurally if necessary.

The third problem is **`unknown` versus `false`**.

A verifier failure can mean

\[
\text{actual counterexample},
\]

but it can also mean

\[
\text{missing invariant},
\quad
\text{solver timeout},
\quad
\text{unsupported theory},
\quad
\text{quantifier-instantiation failure}.
\]

A training system that maps all of those to

\[
R=-1
\]

is reintroducing noisy supervision through the back door.

This is one reason counterexample-based approaches such as ExVerus are important: they seek concrete behavioral evidence that can distinguish and explain certain proof failures. citeturn12academia1

The fourth problem is the **semantic gap between the verifier and deployed execution environment**. Deductive verification proves properties in a specific formal semantics. It does not automatically prove that an external API behaves according to its model, that hardware has no fault, that a dependency actually implements its assumed contract, or that arbitrary environmental behavior satisfies modeled assumptions. Verus and Dafny give powerful reasoning within their supported semantics, but those semantics and trusted components define the boundary of the guarantee. citeturn5academia48turn5search0

This is why the sentence

> “If we can prove the program, we do not need runtime”

from the conceptual slide should be refined for publication to something like:

> **For a property completely represented by the formal specification and verification semantics, a successful deductive proof can replace concrete execution as the correctness oracle for that property.**

That is both stronger scientifically and harder to attack.

Runtime remains essential or useful for properties such as empirical performance, hardware interaction, network behavior, real dependency behavior, user-experience properties, and requirements not captured by the formal model. The emergence of work such as RLPF, which specifically trains models from measured runtime performance, illustrates that some useful software objectives are inherently tied to execution rather than pure functional specification. citeturn4academia3

The fifth problem is **formalization coverage**. Real software rarely arrives with complete contracts, loop invariants, dependency models, and environmental assumptions. FVSpec's pipeline could translate only a subset of the collected real-world property tests into Lean specifications, illustrating the remaining difficulty of moving from executable informal artifacts to formal specifications at scale. citeturn7academia2

This strongly supports your hybrid hypothesis:

\[
R_{\text{hybrid}}
=
R_{\text{formalized properties}}
+
R_{\text{runtime for the residual behavior}}.
\]

Rather than seeing runtime and formal verification as competing philosophies, a practical agent can treat formal verification as the **highest-assurance signal where a valid specification exists**, with execution providing evidence for the unformalized remainder.

The sixth problem is **mistaking proof progress for semantic progress**.

LeanProgress shows that estimating progress through a proof can improve theorem-proving search, which supports your general idea that process-level proof information is useful. citeturn6academia2 But program verification adds an extra difficulty: changing the implementation itself can radically change the generated verification-condition set. Thus

\[
\#\text{proved VCs at }t+1
>
\#\text{proved VCs at }t
\]

does not necessarily mean the program is closer to the intended solution.

This is why I recommend tying progress to a fixed set of semantic goals wherever possible, rather than the raw prover-internal obligation count.

Finally, there is a potential **prover overfitting** failure. A model might learn characteristic error-message patterns, preferred lemmas, or verification-language idioms without gaining broader program understanding. Cross-verifier or prover-removed evaluation is the cleanest antidote. The current vericoding benchmark's inclusion of Dafny, Verus/Rust, and Lean makes cross-formalism evaluation increasingly feasible. citeturn2academia0

## Recommended paper positioning

I would change the headline from something like

> **Replace RL with formal verification**

because that combines two different claims and will immediately invite objections.

A much better title family is:

> **From Execution Rewards to Proof Rewards: Semantic Credit Assignment for Code LLMs**

or

> **Proof as Reward: Training Code Models with Structured Verification Conditions**

or, for the strongest version,

> **Beyond Test-Case RL: Formal Proof Obligations as Semantic Process Rewards for Code Generation**

The core problem statement could read:

> Code-generation models are increasingly post-trained using execution-based verifiable rewards, but such rewards derive correctness from a finite set of observed executions and often provide coarse, delayed feedback. Deductive program verification offers a different oracle: a generated program can be translated into machine-checkable proof obligations whose discharge establishes formally specified properties across the represented program state space without concrete execution on test inputs. Recent work has demonstrated both execution-feedback RL and verifier-guided verified programming, including RL from binary verifier outcomes, but it remains unclear whether the internal structure of formal proof obligations provides a superior learning signal. We study proof-obligation-level semantic reward as a replacement for and complement to execution reward under matched training conditions. citeturn4academia1turn13academia0turn11view3

Then state the central hypothesis as:

\[
\boxed{
H_1:
\text{Structured formal supervision provides better semantic credit assignment than execution outcome reward.}
}
\]

More concretely:

> **Under matched model, data, and end-to-end compute budgets, code models trained using structured verifier-derived feedback will achieve higher semantic correctness and stronger distribution-shift robustness than models trained using finite test-outcome rewards alone.**

The second hypothesis should be about internalization:

\[
\boxed{
H_2:
\text{The advantage persists when the prover is removed at inference.}
}
\]

This is the most important difference from much of today's verifier-in-the-loop literature. P³, LORIS, AxDafny, AlphaVerus, and related systems convincingly show that external formal reasoning improves the overall system, but their primary results do not establish your stronger retained-capability claim. citeturn11view4turn11view3turn11view5turn3academia43

The practical hypothesis should be:

\[
\boxed{
H_3:
R_{\text{formal}}+R_{\text{execution}}
>
R_{\text{formal}}
\text{ when specifications are incomplete.}
}
\]

And your efficiency hypothesis should deliberately remain empirical:

\[
\boxed{
H_4:
\text{Formal supervision reaches a target correctness level with lower total oracle cost.}
}
\]

Do **not** presume \(H_4\); measure it.

The cleanest primary contribution set would therefore be:

1. **A structured semantic reward representation** derived from canonical verification conditions rather than only final verifier acceptance.
2. **The first tightly controlled proof-vs-execution reward study** using the same model family, training data, optimizer, and budget.
3. **A prover-removal experiment** measuring whether formal supervision teaches transferable semantic reasoning rather than only prover use.
4. **A specification-hacking benchmark and defenses**, because recent formal RLVR evidence shows this is a first-order issue rather than an edge case. citeturn11view1
5. **A hybrid formal/runtime study** showing where proof can truly replace concrete execution and where it cannot.

The falsification criteria should be unusually explicit. The strong thesis is weakened if structured proof reward does no better than binary verifier reward; if gains disappear completely without the prover; if gains vanish under semantic-preserving code transformations; if proof-trained models merely exploit formal-language artifacts; or if equivalent correctness costs substantially more end-to-end than execution training.

Conversely, an especially compelling result would look like

\[
\text{G3}>\text{G2}>\text{G1}>\text{G0}
\]

on unseen verified programs,

while also obtaining

\[
\text{G3}_{\text{no prover}}
>
\text{G1}_{\text{no prover}}
\]

on semantic transformations and ordinary code reasoning.

That would support a much deeper conclusion than “formal verification catches more bugs”:

> **Machine-checkable proof structure can function as a semantic teacher for code models.**

That claim is consistent with where the strongest current evidence is pointing. LORIS shows that local formal reasoning errors can be isolated rather than returning a single failed verdict; P³ shows that proof obligations are useful early enough to shape program construction; formal theorem-proving systems show that machine verification can support effective reinforcement learning; and the first Dafny RLVR experiments show both that formal rewards can train code models and that naive verifier rewards introduce serious specification-gaming problems. citeturn11view3turn11view4turn1academia2turn10view0

The resulting research story also fits your broader Pillar II architecture better than the simpler “replace runtime” claim. Your page-two architecture already places token loss, execution traces, semantic equivalence, and proof alignment as distinct learning signals rather than mutually exclusive alternatives. fileciteturn0file1 The strongest research program is therefore not to argue that testing should disappear, but to establish an **assurance hierarchy**:

\[
\text{token supervision}
<
\text{execution evidence}
<
\text{formal semantic obligations}
\]

for properties that can be formalized, while retaining execution for the residual behavior that formal specifications do not capture.

The most defensible one-sentence thesis is consequently:

> **Execution-based RL teaches from sampled behavior; formal verification can teach from symbolic semantic obligations. We propose to turn those obligations—not merely the final prover verdict—into training-time credit, and test whether doing so produces code models that are more correct, robust, and semantically capable even after the prover is removed.**




===source 
Citations · 28

microsoft.com
microsoft.com

1
Dafny: An Automatic Program Verifier for Functional Correctness - Microsoft Research
https://www.microsoft.com/en-us/research/publication/dafny-automatic-program-verifier-functional-correctness-2/?utm_source=chatgpt.com
•

2
Jian_Wang_Interview_30min copy.pdf

Jian_Wang_Interview_30min copy.pdf
•

3
Pasted markdown.md

Pasted markdown.md
arxiv.org
arxiv.org

4
Automating Formal Verification with Reinforcement Learning and Recursive Inference
https://arxiv.org/abs/2605.30914

7
Automating Formal Verification with Reinforcement Learning and Recursive Inference
https://arxiv.org/abs/2605.30914?utm_source=chatgpt.com

5
DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
https://arxiv.org/abs/2504.21801?utm_source=chatgpt.com

6
[2605.17914] Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors
https://arxiv.org/abs/2605.17914

8
CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning
https://arxiv.org/abs/2207.01780?utm_source=chatgpt.com

9
AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement
https://arxiv.org/abs/2412.06176?utm_source=chatgpt.com

10
DafnyPro: LLM-Assisted Automated Verification for Dafny Programs
https://arxiv.org/abs/2601.05385?utm_source=chatgpt.com

12
RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning
https://arxiv.org/abs/2410.02089?utm_source=chatgpt.com

13
Towards Neural Synthesis for SMT-Assisted Proof-Oriented Programming
https://arxiv.org/abs/2405.01787?utm_source=chatgpt.com

14
ExVerus: Verus Proof Repair via Counterexample Reasoning
https://arxiv.org/abs/2603.25810?utm_source=chatgpt.com

15
[2608.09277] P$^{3}$: Joint Program-and-Proof Planning for Verified Code Generation
https://arxiv.org/abs/2608.09277

16
[2606.32007] AxDafny: Agentic Verified Code Generation in Dafny
https://arxiv.org/abs/2606.32007

18
[2605.30914] Automating Formal Verification with Reinforcement Learning and Recursive Inference
https://arxiv.org/abs/2605.30914

19
DafnyBench: A Benchmark for Formal Software Verification
https://arxiv.org/abs/2406.08467?utm_source=chatgpt.com

20
A benchmark for vericoding: formally verified program synthesis
https://arxiv.org/abs/2509.22908?utm_source=chatgpt.com

21
AxDafny: Agentic Verified Code Generation in Dafny
https://arxiv.org/abs/2606.32007?utm_source=chatgpt.com

22
Local Success Does Not Compose: Benchmarking Large Language Models for Compositional Formal Verification
https://arxiv.org/abs/2509.23061?utm_source=chatgpt.com

23
FVSpec: Real-World Property-Based Tests as Lean Challenges
https://arxiv.org/abs/2606.01008?utm_source=chatgpt.com

24
SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios
https://arxiv.org/abs/2512.18470?utm_source=chatgpt.com

25
Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages
https://arxiv.org/abs/2406.09757?utm_source=chatgpt.com

26
Verus: Verifying Rust Programs using Linear Ghost Types (extended version)
https://arxiv.org/abs/2303.05491?utm_source=chatgpt.com

27
RLPF: Reinforcement Learning from Performance Feedback for Code Generation
https://arxiv.org/abs/2607.27271?utm_source=chatgpt.com

28
LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction
https://arxiv.org/abs/2502.17925?utm_source=chatgpt.com
frama-c.com
frama-c.com

11
WP
https://www.frama-c.com/wp.html?utm_source=chatgpt.com
dblp.org
dblp.org

17
dblp: Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping.
https://dblp.org/rec/conf/icml/NgHR99.html?utm_source=chatgpt.com
Sources scanned · 190

arxiv.org
arxiv.org
DafnyPro: LLM-Assisted Automated Verification for Dafny Programs


https://arxiv.org/abs/2601.05385

AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement


https://arxiv.org/abs/2412.06176

Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages


https://arxiv.org/abs/2406.09757

Dafny as Verification-Aware Intermediate Language for Code Generation


https://arxiv.org/abs/2501.06283

Verus: Verifying Rust Programs using Linear Ghost Types (extended version)


https://arxiv.org/abs/2303.05491

Automating Formal Verification with Reinforcement Learning and Recursive Inference


https://arxiv.org/abs/2605.30914

Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors


https://arxiv.org/abs/2605.17914

Proof2Silicon: Prompt Repair for Verified Code and Hardware Generation via Reinforcement Learning


https://arxiv.org/abs/2509.06239

Hilbert: Recursively Building Formal Proofs with Informal Reasoning


https://arxiv.org/abs/2509.22819

Calculus on MDPs: Potential Shaping as a Gradient


https://arxiv.org/abs/2208.09570

Potential-Based Shaping and Q-Value Initialization are Equivalent


https://arxiv.org/abs/1106.5267

Temporal-Logic-Based Reward Shaping for Continuing Reinforcement Learning Tasks


https://arxiv.org/abs/2007.01498

Policy Invariance under Reward Transformations for General-Sum Stochastic Games


https://arxiv.org/abs/1401.3907

Retrieval-Augmented TLAPS Proof Generation with Large Language Models


https://arxiv.org/abs/2501.03073

Evidence-Grounded Verified Agentic Reasoning: A Path Toward Eliminating LLM Hallucination in Empirical Inference via Tool-Attested Kernel Proofs


https://arxiv.org/abs/2607.12650

Neuro-Symbolic Reasoning for Vulnerability Detection


https://arxiv.org/abs/2607.03963

arxiv.deeppaper.ai
arxiv.deeppaper.ai
DafnyPro: LLM-Assisted Automated Verification for Dafny Programs | Arxiv - DeepPaper


DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS PDF DeepRead KEY CONTRIBUTIONS DafnyPro framework with diff-checker, pruner, and hint-augmentation system, demonstrating improved v...

alphaxiv.org
alphaxiv.org
AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement | alphaXiv


ALPHAVERUS: BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Tra...

AutoVerus: Automated Proof Generation for Rust Code | alphaXiv


AUTOVERUS: AUTOMATED PROOF GENERATION FOR RUST CODE ImageUniversity of Illinois at Urbana-ChampaignImageUniversity of California, IrvineImageColumbia University CY Chenyuan Yang XL Xuheng Li MR...

AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement | alphaXiv


Submitted 09 Dec 2024 en ALPHAVERUS: BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT ImageCarnegie Mellon University PA Pranjal AggarwalBryan Pa...

AlphaVerus: Arranque de la Generación de Código Formalmente Verificado | alphaXiv


Submitted 09 Dec 2024 es ALPHAVERUS: ARRANQUE DE LA GENERACIÓN DE CÓDIGO FORMALMENTE VERIFICADO ImageCarnegie Mellon University PA Pranjal AggarwalBryan ParnoSean Welleck ABSTRACT Aquí tienes la...

Reducing the Costs of Proof Synthesis on Rust Systems by Scaling Up a Seed Training Set | alphaXiv


REDUCING THE COSTS OF PROOF SYNTHESIS ON RUST SYSTEMS BY SCALING UP A SEED TRAINING SET Reducing the Costs of Proof Synthesis on Rust Systems by Scaling Up a Seed Training Set May 9, 2026 Image: N...

Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization | alphaXiv


VERUS-SPECGYM: AN AGENTIC ENVIRONMENT FOR EVALUATING SPECIFICATION AUTOFORMALIZATION AA Anmol Agarwal NN Natalie NeamtuPA Pranjal AggarwalSeungone Kim JL Jannis Limperg CF Cedric Flamant KS...

Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization | alphaXiv


EVALUATING FAITHFULNESS VIA EXECUTION A major technical challenge in evaluating formal specifications is that they are written in a high-level logical language that is typically used for symbolic pro...

ExVerus: Verus Proof Repair via Counterexample Reasoning | alphaXiv


EXVERUS: VERUS PROOF REPAIR VIA COUNTEREXAMPLE REASONING Jun Yang, Yuechun Sun, Yi Wu, Rodrigo Caridad, Yongwei Yuan, Jianan Yao, Shan Lu, Kexin Pei 2026-03-30 PDF Download ABSTRACT Large Langua...

Automating Potential-based Reward Shaping with Vision Language Model Guidance | alphaXiv


CONCLUSION VLM-PBRS represents a bridge between high-level AI reasoning and low-level robotic control. By using VLMs to automate the creation of potential functions, the framework removes the need fo...

Reward Design for Reinforcement Learning Agents | alphaXiv


RELEVANT CITATIONS Ng, Andrew Y., Daishi Harada, and Stuart J. Russell. Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping. In ICML, 1999. * This seminal paper...

WybeCoder: Verified Imperative Code Generation | alphaXiv


Submitted 14 Apr 2026 en WYBECODER: VERIFIED IMPERATIVE CODE GENERATION FG Fabian Gloeckle MB Mantas Baksys DF Darius Feher KZ Kunhao Zheng AH Amaury Hayat SB Sean B. HoldenGabriel Synnae...

Retrieval-Augmented TLAPS Proof Generation with Large Language Models | alphaXiv


Submitted 06 Jan 2025 en RETRIEVAL-AUGMENTED TLAPS PROOF GENERATION WITH LARGE LANGUAGE MODELS ImageNortheastern University YZ Yuhao Zhou ABSTRACT We present a novel approach to automated proof...

Loop Invariant Generation: A Hybrid Framework of Reasoning optimised LLMs and SMT Solvers | alphaXiv


LOOP INVARIANT GENERATION: A HYBRID FRAMEWORK OF REASONING OPTIMISED LLMS AND SMT SOLVERS Varun Bharti, Shashwat Jha, Dhruv Kumar, Pankaj Jalote 2025-08-01 ABSTRACT Loop invariants are essential...

Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors | alphaXiv


GUIDING LLM-BASED LOOP INVARIANT SYNTHESIS VIA FEEDBACK ON LOCAL REASONING ERRORS Tianchi Li, Zhenyu Yan, Junhao Liu, Peng Di, Xin Zhang 2026-05-18 PDF Download ABSTRACT We propose a novel frame...

Quokka: Accelerating Program Verification with LLMs via Invariant Synthesis | alphaXiv


QUOKKA: ACCELERATING PROGRAM VERIFICATION WITH LLMS VIA INVARIANT SYNTHESIS Anjiang Wei, Tianran Sun, Tarun Suresh, Haoze Wu, Ke Wang, Alex Aiken 2026-04-02 PDF Download ABSTRACT Program verific...

오토베루스: Rust 코드용 자동화된 증명 생성 | alphaXiv


오토베루스: Rust 코드용 자동화된 증명 생성 August 22, 2025 Image: University of Illinois at Urbana-Champaign logoUniversity of Illinois at Urbana-ChampaignImage: University of California, Irvine logoUniversity of...

Automatic Generation of Formal Specification and Verification Annotations Using LLMs and Test Oracles | alphaXiv


Submitted 19 Jan 2026 en AUTOMATIC GENERATION OF FORMAL SPECIFICATION AND VERIFICATION ANNOTATIONS USING LLMS AND TEST ORACLES JP João Pascoal Faria ET Emanuel Trigo VH Vinicius Honorato RA...

VeriStruct: AI-assisted Automated Verification of Data-Structure Modules in Verus | alphaXiv


VERISTRUCT: AI-ASSISTED AUTOMATED VERIFICATION OF DATA-STRUCTURE MODULES IN VERUS Chuyue Sun, Yican Sun, Daneshvar Amrollahi, Ethan Zhang, Shuvendu Lahiri, Shan Lu, David Dill, Clark Barrett 2026-0...

AlphaVerus：引导形式化验证代码生成 | alphaXiv


ALPHAVERUS: BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT AlphaVerus：引导形式化验证代码生成 December 9, 2024 Image: Carnegie Mellon University logoCarneg...

AlphaVerus: Bootstrapping Formal Verifizierte Codegenerierung | alphaXiv


Submitted 09 Dec 2024 de ALPHAVERUS: BOOTSTRAPPING FORMAL VERIFIZIERTE CODEGENERIERUNG ImageCarnegie Mellon University PA Pranjal AggarwalBryan ParnoSean Welleck ABSTRACT **Automatisierte Code-G...

Clover: Closed-Loop Verifiable Code Generation | alphaXiv


Clover: Closed-Loop Verifiable Code Generation November 16, 2024 Image: Stanford University logoStanford University VMware Research Copy Markdown Chuyue Sun, Ying Sheng, Oded Padon, Clark Barrett...

AutoVerus: Automated Proof Generation for Rust Code | alphaXiv


AutoVerus: Automated Proof Generation for Rust Code August 22, 2025 Image: University of Illinois at Urbana-Champaign logoUniversity of Illinois at Urbana-ChampaignImage: University of California,...

Evaluating LLM-driven User-Intent Formalization for Verification-Aware Languages | alphaXiv


Submitted 15 Oct 2024 en EVALUATING LLM-DRIVEN USER-INTENT FORMALIZATION FOR VERIFICATION-AWARE LANGUAGES Shuvendu K. Lahiri ABSTRACT Verification-aware programming languages such as Dafny and F*...

Clover: Closed-Loop Verifiable Code Generation | alphaXiv


CLOVER: CLOSED-LOOP VERIFIABLE CODE GENERATION Chuyue Sun, Ying Sheng, Oded Padon, Clark Barrett 2024-11-16 PDF Download ABSTRACT The use of large language models for code generation is a rapidl...

Local Success Does Not Compose: Benchmarking Large Language Models for Compositional Formal Verification | alphaXiv


LOCAL SUCCESS DOES NOT COMPOSE: BENCHMARKING LARGE LANGUAGE MODELS FOR COMPOSITIONAL FORMAL VERIFICATION Xu Xu, Xin Li, Xingwei Qu, Jie Fu, Binhang Yuan 2025-09-27 PDF Download ABSTRACT We intro...

MINIF2F-DAFNY: LLM-Guided Mathematical Theorem Proving via Auto-Active Verification | alphaXiv


Submitted 24 Jun 2026 MINIF2F-DAFNY: LLM-GUIDED MATHEMATICAL THEOREM PROVING VIA AUTO-ACTIVE VERIFICATION MB Mantas Baksys SZ Stefan Zetzsche OB Olivier Bouissou SB Sean B. Holden ABSTRACT...

A Weakest Precondition Calculus for Programs and Linear Temporal Specifications | alphaXiv


A WEAKEST PRECONDITION CALCULUS FOR PROGRAMS AND LINEAR TEMPORAL SPECIFICATIONS Gidon Ernst 2026-02-11 PDF Download ABSTRACT Auto-active program verification rests on the ability to effectively...

Retrieval-Augmented TLAPS Proof Generation with Large Language Models | alphaXiv


RETRIEVAL-AUGMENTED TLAPS PROOF GENERATION WITH LARGE LANGUAGE MODELS Retrieval-Augmented TLAPS Proof Generation with Large Language Models January 6, 2025 Yuhao Zhou SUMMARY Researchers develop...

Inductive Deductive Synthesis: Enabling AI to Generate Formally Verified Systems | alphaXiv


INDUCTIVE DEDUCTIVE SYNTHESIS: ENABLING AI TO GENERATE FORMALLY VERIFIED SYSTEMS Inductive Deductive Synthesis: Enabling AI to Generate Formally Verified Systems May 22, 2026 Copy Markdown Shubha...

Towards Language Model Guided TLA+ Proof Automation | alphaXiv


Submitted 28 Feb 2026 en TOWARDS LANGUAGE MODEL GUIDED TLA+ PROOF AUTOMATION YZ Yuhao Zhou ST Stavros Tripakis ABSTRACT Formal theorem proving with TLA+ provides rigorous guarantees for system...

Automating Unrealizability Logic: Hoare-Style Proof Synthesis for Infinite Sets of Programs | alphaXiv


loads external code, having a summary over the set of possible external functions would save the work of reverifying properties of the function for each program. Similarly, if one has a language for w...

Manipulate-Anything: Automating Real-World Robots using Vision-Language Models | alphaXiv


tasks into sub-tasks, generates code for new skills or task-specific grasp pose, and verifies the success of each sub-task (Figure 3). Note that due to the modularity aspect of our framework, MANIPULA...

ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis | alphaXiv


ATLAS: AUTOMATED TOOLKIT FOR LARGE-SCALE VERIFIED CODE SYNTHESIS Mantas Baksys, Stefan Zetzsche, Olivier Bouissou, Remi Delmas, Soonho Kong, Sean B. Holden 2026-02-02 PDF Download ABSTRACT Large...

Re:Form -- Reducing Human Priors in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny | alphaXiv


RE:FORM -- REDUCING HUMAN PRIORS IN SCALABLE FORMAL SOFTWARE VERIFICATION WITH RL IN LLMS: A PRELIMINARY STUDY ON DAFNY Re:Form -- Reducing Human Priors in Scalable Formal Software Verification with...

Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale | alphaXiv


NEURO-SYMBOLIC SOFTWARE VERIFICATION: HYPER-CHARGING LOCAL LANGUAGE MODELS WITH SYMBOLIC REASONING AT SCALE Muhammad A. A. Pirzada, Julian Parsert, Weiqi Wang, Konstantin Korovin, Lucas C. Cordeiro...

alphaverus.github.io
alphaverus.github.io
AlphaVerus: Bootstrapping Formally Verified Code Generation


ALPHAVERUS BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT Pranjal Aggarwal^{1}, Bryan Parno^{1}, Sean Welleck^{1} ^{1}Carnegie Mellon University...

papers.cool
papers.cool
DafnyPro: LLM-Assisted Automated Verification for Dafny Programs | Cool Papers - Immersive Paper Discovery


2601.05385 Total: 1 #1 DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS [PDF^{}] [COPY] [KIMI^{}] [REL] Authors: Debangshu Banerjee, Olivier Bouissou, Stefan Zetzsche We present Da...

VeriStruct: AI-assisted Automated Verification of Data-Structure Modules in Verus | Cool Papers - Immersive Paper Discovery


2510.25015 Total: 1 #1 VERISTRUCT: AI-ASSISTED AUTOMATED VERIFICATION OF DATA-STRUCTURE MODULES IN VERUS [PDF^{}] [COPY] [KIMI^{2}] [REL] Authors: Chuyue Sun, Yican Sun, Daneshvar Amrollahi, Ethan...

Specification-Guided Repair of Arithmetic Errors in Dafny Programs using LLMs | Cool Papers - Immersive Paper Discovery


2507.03659 Total: 1 #1 SPECIFICATION-GUIDED REPAIR OF ARITHMETIC ERRORS IN DAFNY PROGRAMS USING LLMS [PDF^{}] [COPY] [KIMI^{}] [REL] Authors: Valentina Wu, Alexandra Mendes, Alexandre Abreu Debugg...

KVerus: Scalable and Resilient Formal Verification Proof Generation for Rust Code | Cool Papers - Immersive Paper Discovery


2605.03822 Total: 1 #1 KVERUS: SCALABLE AND RESILIENT FORMAL VERIFICATION PROOF GENERATION FOR RUST CODE [PDF^{}] [COPY] [KIMI^{}] [REL] Authors: Yuwei Liu, Xinyi Wan, Yanhao Wang, Minghua Wang, Li...

yertongs.com
yertongs.com
Paper page - DafnyPro: LLM-Assisted Automated Verification for Dafny Programs


DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS Published on Jan 8 Upvote 4 * * * * * Authors: Image Debangshu Banerjee , [Button: Olivier Bouissou] , [Button: Stefan Z...

huggingface.co
huggingface.co
Paper page - DafnyPro: LLM-Assisted Automated Verification for Dafny Programs


Papers arxiv:2601.05385 Copy markdown DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS Published on Jan 8 Upvote 4 * * * * * Authors: Image Debangshu Banerjee , [Butto...

Paper page - Dafny as Verification-Aware Intermediate Language for Code Generation


arxiv:2501.06283 DAFNY AS VERIFICATION-AWARE INTERMEDIATE LANGUAGE FOR CODE GENERATION Published on Jan 10, 2025 Upvote - Authors: Image Yue Chen Li , [Button: Stefan Zetzsche] , [Button: Siva...

2510/2510.06296.md · nielsr/arxiv-chandra-ocr-full-markdown-20260406


VERIEQUIVBENCH: AN EQUIVALENCE SCORE FOR GROUND-TRUTH-FREE EVALUATION OF FORMALLY VERIFIABLE CODE Lingfei Zeng^{1,*}, Fengdi Che^{2,*}, Xuhan Huang^{3}, Fei Ye^{4}, Xu Xu^{5}, Binhang Yuan^{5,†}, Ji...

microsoft.com
microsoft.com
Dafny: An Automatic Program Verifier for Functional Correctness - Microsoft Research


https://www.microsoft.com/en-us/research/publication/dafny-automatic-program-verifier-functional-correctness-2/

Dafny: An Automatic Program Verifier For Functional Correctness - Microsoft Research


DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS * Rustan Leino LPAR-16, Dakar, Senegal | April 2010 Published by Microsoft Research Download BibTex * Full functional-correctness...

AutoVerus: Automated Proof Generation for Rust Code - Microsoft Research


AUTOVERUS: AUTOMATED PROOF GENERATION FOR RUST CODE * Chenyuan Yang , * Xuheng Li , * Md Rakib Hossain Misu , * Jianan Yao , * Weidong Cui , * Yeyun Gong , * Chris Hawblitzel , * Shuvendu Lahiri , *...

VS3: SMT Solvers for Program Verification - Microsoft Research


VS3: SMT SOLVERS FOR PROGRAM VERIFICATION * Saurabh Srivastava , * Sumit Gulwani , * Jeffrey S. Foster CAV '09 Proceedings of the 21st International Conference on Computer Aided Verification | June...

Weakest-Precondition of Unstructured Programs - Microsoft Research


WEAKEST-PRECONDITION OF UNSTRUCTURED PROGRAMS * Mike Barnett , * Rustan Leino PASTE '05: The 6th ACM SIGPLAN-SIGSOFT workshop on Program analysis for software tools and engineering | September 2005...

sciweavers.org
sciweavers.org
Dafny: An Automatic Program Verifier for Functional Correctness | Sciweavers


199 views Automated Reasoning» more  LPAR 2010» DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS 15 years 5 months ago Download  research.microsoft.com Traditionally, the full veri...

Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping | Sciweavers


160 click to vote ICML 1999 IEEE 97 views Machine Learning» more  ICML 1999» POLICY INVARIANCE UNDER REWARD TRANSFORMATIONS: THEORY AND APPLICATION TO REWARD SHAPING 16 years 9 months ago Downl...

frama-c.com
frama-c.com
WP


https://www.frama-c.com/wp.html

Publications


WP MANUALS Patrick Baudin, François Bobot, Loïc Correnson, Zaynah Dargaye, Allan Blanchard WP Plug-in Manual [link] [BibTeX] @manual{wp_user_manual, title = "WP Plug-in Manual", author = "Baudin,...

2023.splashcon.org
2023.splashcon.org
Verus: Verifying Rust Programs using Linear Ghost Types (SPLASH 2023 - OOPSLA) - SPLASH 2023


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES Who Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, Chris Hawblitzel Track...

cir.nii.ac.jp
cir.nii.ac.jp
Verus: Verifying Rust Programs using Linear Ghost Types | CiNii Research


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES DOI Web Site Web Site 1 Citations * Andrea Lattuada VMware Research, Switzerland * Travis Hance Carnegie Mellon University, USA * Chanhee...

Policy Invariance Under Reward Transformations : Theory and Application to Reward Shaping | CiNii Research


POLICY INVARIANCE UNDER REWARD TRANSFORMATIONS : THEORY AND APPLICATION TO REWARD SHAPING 被引用文献1件 * NG A. Y. 書誌事項 公開日 1999 収録刊行物 * Proceedings of the 17th International Conference on Machine...

Policy invariance under reward transformations : Theory and application to reward shaping | CiNii Research


POLICY INVARIANCE UNDER REWARD TRANSFORMATIONS : THEORY AND APPLICATION TO REWARD SHAPING 1 Citations * NG A. Y. BIBLIOGRAPHIC INFORMATION Published 1999 JOURNAL * Proc. of the Sixteenth Inte...

emergentmind.com
emergentmind.com
Verus: Verifying Rust Programs using Linear Ghost Types (extended version)


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES (EXTENDED VERSION) Published 9 Mar 2023 in cs.LO and cs.PL | (2303.05491v2) Abstract: The Rust programming language provides a powerful type...

AxDafny: AI-Extended Verified Programming in Dafny


AXDAFNY: AI-EXTENDED VERIFIED PROGRAMMING IN DAFNY Updated 4 July 2026 * AxDafny is an AI-extended verified programming framework that jointly synthesizes executable Dafny code and proof artifacts...

DafnyComp: Formal Verification Frameworks


DAFNYCOMP: FORMAL VERIFICATION FRAMEWORKS Updated 2 July 2026 * DafnyComp is a collective of frameworks, benchmarks, and toolchains that automate the compositional verification of multi-function Da...

Learning-Augmented Proof Synthesis


LEARNING-AUGMENTED PROOF SYNTHESIS Updated 8 November 2025 * The paper demonstrates a multi-phase architecture where neural models decompose complex proof obligations into sub-obligations that are...

Proofstep Generation in Formal Verification


PROOFSTEP GENERATION IN FORMAL VERIFICATION Updated 13 April 2026 * Proofstep generation is the process of constructing, predicting, or synthesizing the next logical step in a formal proof, integra...

DafnyPro: LLM-Assisted Automated Verification for Dafny Programs


DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS Published 8 Jan 2026 in cs.SE | (2601.05385v1) Abstract: We present DafnyPro, an inference-time framework that enhances LLMs for gen...

Rust-to-Lean: AI-Driven Verification Pipeline


A RUST-TO-LEAN VERIFICATION PIPELINE WITH AI PROVERS: AN EXPERIENCE REPORT Published 28 May 2026 in cs.LO | (2605.30106v1) Abstract: We describe a verification pipeline that takes production Rust c...

Verification-in-the-Loop (VITL)


VERIFICATION-IN-THE-LOOP (VITL) Updated 1 March 2026 * Verification-in-the-Loop (VITL) is an iterative paradigm that embeds automated verification within training and development loops to ensure co...

Evaluation Harness in Self-Evolving Verification


EVALUATION HARNESS IN SELF-EVOLVING VERIFICATION Updated 24 May 2026 * Evaluation Harness is a framework that employs iterative feedback loops combining generation and self-verification to ensure c...

Adaptive Formal Verification Strategies


ADAPTIVE FORMAL VERIFICATION STRATEGIES Updated 5 July 2026 * Adaptive formal verification is a feedback-driven process that updates verification artifacts and proof strategies based on real-time o...

core.ac.uk
core.ac.uk
Verus: Verifying Rust Programs using Linear Ghost Types (extended version) - CORE


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES (EXTENDED VERSION) Authors 1. Matthias Brun 2. Chanhee Cho 3. +7 more 4. Travis Hance 5. Chris Hawblitzel 6. Jon Howell 7. Andrea Lattuada 8...

doi.org
doi.org
Atmosphere: Practical Verified Kernels with Rust and Verus | Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles


research-article Open access ATMOSPHERE: PRACTICAL VERIFIED KERNELS WITH RUST AND VERUS Authors: Xiangdong Chen, Zhaofeng Li, Jerry Zhang, Vikram Narayanan, Anton BurtsevAuthors Info & Claims SOS...

Dafny Meets the Verification Benchmarks Challenge | Springer Nature Link


DAFNY MEETS THE VERIFICATION BENCHMARKS CHALLENGE * Conference paper * pp 112–126 Verified Software: Theories, Tools, Experiments (VSTTE 2010) * K. Rustan M. Leino^{19} & * Rosemary Monahan^{20}...

A Verifier for Functional Properties of Sequence-Manipulating Programs | Springer Nature Link


A VERIFIER FOR FUNCTIONAL PROPERTIES OF SEQUENCE-MANIPULATING PROGRAMS * Conference paper * pp 183–186 * Cite this conference paper Save conference paper View saved research Automated Technology...

Weakest-precondition of unstructured programs | ACM SIGSOFT Software Engineering Notes


article Free access WEAKEST-PRECONDITION OF UNSTRUCTURED PROGRAMS Authors: Mike Barnett, K. Rustan M. LeinoAuthors Info & Claims ACM SIGSOFT Software Engineering Notes, Volume 31, Issue 1 Pages...

zenodo.org
zenodo.org
Verus: Verifying Rust Programs using Linear Ghost Types -- Artifact | Zenodo


Published January 7, 2023 | Version a58d0f36b889bb65911f7aad1e0d72ad0e48a9e1 Software Open VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES -- ARTIFACT AUTHORS/CREATORS * Lattuada, Andrea^{...

researchgate.net
researchgate.net
Verus: Verifying Rust Programs using Linear Ghost Types


Article VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES * April 2023 * Proceedings of the ACM on Programming Languages 7(OOPSLA1):286-315 DOI:10.1145/3586037 * License * CC BY 4.0 Authors...

(PDF) Reward Shaping in Episodic Reinforcement Learning


REWARD SHAPING IN EPISODIC REINFORCEMENT LEARNING * May 2017 Authors: Marek Grzes * University of Kent Image Download file PDFRead file ABSTRACT AAMAS presentation. Image: ResearchGate Logo...

DafnyPro: LLM-Assisted Automated Verification for Dafny Programs


DAFNYPRO: LLM-ASSISTED AUTOMATED VERIFICATION FOR DAFNY PROGRAMS * January 2026 DOI:10.48550/arXiv.2601.05385 Authors: Debangshu Banerjee Debangshu Banerjee * This person is not on ResearchGate...

(PDF) Dafny Meets the Verification Benchmarks Challenge


Conference Paper PDF Available DAFNY MEETS THE VERIFICATION BENCHMARKS CHALLENGE * August 2010 * Lecture Notes in Computer Science 6217:112-126 DOI:10.1007/978-3-642-15057-9_8 * Source * Confere...

Dafny: An Automatic Program Verifier for Functional Correctness | Request PDF


Conference Paper DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS * December 2010 * Lecture Notes in Computer Science DOI:10.1007/978-3-642-17511-4_20 * Source * DBLP * Conference:...

Weakest Precondition Calculus, Revisited using Why3 | Request PDF


WEAKEST PRECONDITION CALCULUS, REVISITED USING WHY3 * February 2013 Authors: Claude Marché Claude Marché * This person is not on ResearchGate, or hasn't claimed this research yet. Asma Tafat *...

(PDF) Proof2Silicon: Prompt Repair for Verified Code and Hardware Generation via Reinforcement Learning


Preprint PDF Available PROOF2SILICON: PROMPT REPAIR FOR VERIFIED CODE AND HARDWARE GENERATION VIA REINFORCEMENT LEARNING * September 2025 DOI:10.48550/arXiv.2509.06239 * License * CC BY 4.0 Auth...

LeanProgress: Guiding Search for Neural Theorem Proving via Proof Progress Prediction | Request PDF


LEANPROGRESS: GUIDING SEARCH FOR NEURAL THEOREM PROVING VIA PROOF PROGRESS PREDICTION * February 2025 DOI:10.48550/arXiv.2502.17925 Authors: Suozhi Huang Suozhi Huang * This person is not on Re...

andrew.cmu.edu
andrew.cmu.edu
Secure Foundations Lab - Publications


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel Proceedin...

manualzilla.com
manualzilla.com
WP manual - Frama-C


DOWNLOAD WP MANUAL - FRAMA-C Transcript WP 0.8 WP Plug-in Manual Version 0.9 for Sodium-20150201 Patrick Baudin, François Bobot, Loïc Correnson, Zaynah Dargaye CEA LIST, Software Safety Laboratory...

WP 0.4 (Draft Manual) - Frama-C


Transcript WP 0.4 (Draft Manual) WP Plug-in (Draft) Manual Version 0.4 for Nitrogen-20111001 Loïc Correnson, Zaynah Dargaye, Anne Pacalet CEA LIST, Software Safety Laboratory c 2010-2011 CEA LIST Th...

plr.csail.mit.edu
plr.csail.mit.edu
MIT PL Review 2026 | This is the website for the MIT PL Review Workshop 2026. We will be hosting the PL Review on May 8th, both in-person and virtually.


VERUS: VERIFYING RUST PROGRAMS USING LINEAR GHOST TYPES AUTHORS: ANDREA LATTUADA, TRAVIS HANCE, CHANHEE CHO, MATTHIAS BRUN, ISITHA SUBASINGHE, YI ZHOU, JON HOWELL, BRYAN PARNO, CHRIS HAWBLITZEL The...

verus-lang.github.io
verus-lang.github.io
Verus — Projects


Please see below for research publications about and using Verus, as well as projects built using Verus. To add your work here, please open a pull request that adds a new file to the 'source/docs/publ...

dblp.org
dblp.org
dblp: Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping.


https://dblp.org/rec/conf/icml/NgHR99.html

dblp: Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping.


"POLICY INVARIANCE UNDER REWARD TRANSFORMATIONS: THEORY AND APPLICATION TO ..." * help us * How can I correct errors in dblp? * contact dblp Andrew Y. Ng, Daishi Harada, Stuart Russell (1999) DE...

dblp: Dafny: An Automatic Program Verifier for Functional Correctness.


"DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS." * help us * How can I correct errors in dblp? * contact dblp K. Rustan M. Leino (2010) * * Image: use mirror server Dagstuhl...

dblp: Dafny: An Automatic Program Verifier for Functional Correctness.


"DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS." * help us * How can I correct errors in dblp? * contact dblp K. Rustan M. Leino (2010) Dagstuhl * Trier * > Home DETAILS AND...

dblp: K. Rustan M. Leino


2010 – 2019 see FAQ * What is the meaning of the colors in the publication lists? * 2018 * Image: Conference and Workshop Papers [c90] * view * electronic edition via DOI * unpaywalled version *...

ai.updf.com
ai.updf.com
Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping


Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping A. Ng,Daishi Harada,Stuart J. Russell 1999 · DBLP: conf/icml/NgHR99 International Conference on Machine Lea...

Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping


Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping A. Ng,Daishi Harada,Stuart J. Russell 1999 · DBLP: conf/icml/NgHR99 International Conference on Machine Lea...

qelloman.tistory.com
qelloman.tistory.com
Policy invariance under reward transformation :: 퀠로맨 블로그


POLICY INVARIANCE UNDER REWARD TRANSFORMATION 퀠로맨 2022. 8. 18. 21:54 2022. 8. 18. 21:54 논문 정보 Ng, Andrew Y., Daishi Harada, and Stuart Russell. "Policy invariance under reward transformations: Th...

cs.utexas.edu
cs.utexas.edu
Publications policy invariance under reward transformations: theory and application to reward shaping


POLICY INVARIANCE UNDER REWARD TRANSFORMATIONS: THEORY AND APPLICATION TO REWARD SHAPING Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping Andrew Y. Ng, Daishi...

apkallulabs.dev
apkallulabs.dev
Apkallu Labs — Where AI meets mathematical certainty


WHERE AI MEETS MATHEMATICAL CERTAINTY. Generative AI guesses; safety-critical systems can't. Apkallu Labs wraps large language models in formal verification — building a full-stack verified ecosyste...

tldr.takara.ai
tldr.takara.ai
Automating Formal Verification with Reinforcement Learning and Recursive Inference | Takara TLDR


Automating Formal Verification with Reinforcement Learning and Recursive Inference 2605.30914 AUTHORS Max Tan ABSTRACT Automated formal verification remains challenging for large language models...

next.gr
next.gr
LLMs That Read Codebases and Propose Refactors | AI Tutorial | Next Electronics


where SA_{risk}(s) represents the static analyzer's estimated risk score (0-1) for suggestion s, and P_{LLM}(s) is the model's original probability for that suggestion. RUNTIME SANDBOXING For refac...

drops.dagstuhl.de
drops.dagstuhl.de
Vehicle: Bridging the Embedding Gap in the Verification of Neuro-Symbolic Programs


To address this problem we then introduce Vehicle– standing as an abbreviation for a “verification condition language” – an intermediate programming language interface between machine learning framewo...

catalyzex.com
catalyzex.com
Drop Test


ViaImage: arxiv icon Access Paper or Ask Questions EVIDENCE-GROUNDED VERIFIED AGENTIC REASONING: A PATH TOWARD ELIMINATING LLM HALLUCINATION IN EMPIRICAL INFERENCE VIA TOOL-ATTESTED KERNEL PROOFS...

Sorin Lerner


COBBLESTONE: ITERATIVE AUTOMATION FOR FORMAL VERIFICATION Request Code Image: Bookmark button Image: Alert button Oct 25, 2024 Authors:Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerne...

api.emergentmind.com
api.emergentmind.com
Formal Counterexample Generation


FORMAL COUNTEREXAMPLE GENERATION Updated 4 July 2026 * Formal counterexample generation is a technique that constructs precise, machine-checkable witnesses (e.g., traces, states, or critical subsys...

tessl.io
tessl.io
Tessl • The package manager for agent skills


PROOF-CARRYING-CODE-GENERATOR Generate executable code together with formal proofs certifying safety and correctness properties in Isabelle/HOL or Coq. Use when building verified software, safety-cr...

deeppaper.ai
deeppaper.ai
AxDafny: Agentic Verified Code Generation in Dafny | Arxiv - DeepPaper


3. AxDafny: Agentic Verified Code Generation in Dafny AXDAFNY: AGENTIC VERIFIED CODE GENERATION IN DAFNY PDF DeepRead KEY CONTRIBUTIONS Introduced AxDafny, a verifier-guided agentic framework for...

Similar Papers for Automatic Generation of Formal Specification and Verification Annotations Using LLMs and Test Oracles | Arxiv - DeepPaper


PAPERS SIMILAR TO "AUTOMATIC GENERATION OF FORMAL SPECIFICATION AND VERIFICATION ANNOTATIONS USING LLMS AND TEST ORACLES" 2601.12845v1 ORIGINAL PAPER Recent verification tools aim to make formal v...

github.com
github.com
GitHub - cmu-l3/alphaverus: AlphaVerus: Formally Verified Code Generation through Self-Improving Translation and Treefinement · GitHub


cmu-l3 / alphaverus Public * Notifications You must be signed in to change notification settings * Fork 1 * Star * Code * Issues 2 * Pull requests 2 * Actions * Projects * Security and quality 0 *...

GitHub - microsoft/verus-proof-synthesis · GitHub


microsoft / verus-proof-synthesis Public * Notifications You must be signed in to change notification settings * Fork 23 * Star * Code * Issues 2 * Pull requests 2 * Actions * Projects VERUS PROOF...

GitHub - ChuyueSun/Clover: Clover: Closed-Loop Verifiable Code Generation · GitHub


LICENSE | LICENSE |   | README.md | README.md |   | README_LLM_CACHE.md | README_LLM_CACHE.md |   | clover_env_setup.md | clover_env_setup.md |   | run_clover.sh | run_clover.sh |   | r...

GitHub - AllanBlanchard/tutoriel_wp: Frama-C and WP tutorial · GitHub


AllanBlanchard / tutoriel_wp Public * Notifications You must be signed in to change notification settings * Fork 20 * Star * Code * Issues 4 * Pull requests 1 * Actions * Projects * Security and qu...

GitHub - microsoft/interwhen: A framework for verifiable reasoning with language models. · GitHub


INTERWHEN A Generalizable Framework for Steering Reasoning Models with Test-time Verification Paper  |  Quick Start  |  Examples  |  Monitors  |  Create your own Monitors interwhen is a test-time...

pith.science
pith.science
Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors · Pith


GUIDING LLM-BASED LOOP INVARIANT SYNTHESIS VIA FEEDBACK ON LOCAL REASONING ERRORS T0 review · 2 major / 1 minor · reviewed 2026-05-20 · grok-4.3 Challenge this review Re-run · record.json Download...

AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement · Pith


ALPHAVERUS: BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT T0 review · 3 major / 3 minor · reviewed 2026-08-11 · deepseek-v4-flash Challenge thi...

microsoft.github.io
microsoft.github.io
About - Verus Proof Synthesis Leaderboard


ABOUT THE LEADERBOARD The Verus Proof Synthesis Leaderboard tracks progress in using Large Language Models (LLMs) to automatically generate formal correctness proofs for Rust programs verified with...

scispace.com
scispace.com
(PDF) Dafny: an automatic program verifier for functional correctness (2010) | K. Rustan M. Leino | 1091 Citations


Book Chapter10.1007/978-3-642-17511-4_20 DAFNY: AN AUTOMATIC PROGRAM VERIFIER FOR FUNCTIONAL CORRECTNESS K. Rustan M. Leino - 25 Apr 2010 - Vol. 6355, pp 348-370 PDF TL;DR: A tour of the langua...

maynoothuniversity.ie
maynoothuniversity.ie
Dafny meets the Verification Benchmarks Challenge - MURAL - Maynooth University Research Archive Library


DAFNY MEETS THE VERIFICATION BENCHMARKS CHALLENGE Share and Export Share and Export Share and Export [Input] [Select] [Input] Monahan, Rosemary and Leino, K. Rustan M. (2010) Dafny meets the Ver...

do-not-panic.com
do-not-panic.com
June 2026 — AI Post Transformers


Interactive Visualization: DafnyPro for LLM-Assisted Dafny Verification Sources: 1. DafnyPro: LLM-Assisted Automated Verification for Dafny Programs — Debangshu Banerjee, Olivier Bouissou, Stefan Ze...

xn--hrdin-gra.se
xn--hrdin-gra.se
leftpad() proved in Frama-C


README.MD ABOUT FRAMA-C From the Frama-C website: > Frama-C is an extensible and collaborative platform dedicated to source-code analysis of C software. In other words, Frama-C is a set of tools f...

iteh.ai
iteh.ai
ISO/IEC DTS 42119-3 - AI Testing Verification and Validation Analysis


i C allows modeling of conditions on inputs from the preceding layer. i R One can similarly encode the activation nodes. For example, the LRA encoding for a ReLU activation node v can be given as R R...

sciencedirect.com
sciencedirect.com
Instrumenting a weakest precondition calculus for counterexample generation - ScienceDirect


JOURNAL OF LOGICAL AND ALGEBRAIC METHODS IN PROGRAMMING Volume 99, October 2018, Pages 97-113 INSTRUMENTING A WEAKEST PRECONDITION CALCULUS FOR COUNTEREXAMPLE GENERATION☆ https://doi.org/10.1016/j...

A verified VCGen based on dynamic logic: An exercise in meta-verification with Why3 - ScienceDirect


JOURNAL OF LOGICAL AND ALGEBRAIC METHODS IN PROGRAMMING Volume 133, June 2023, 100871 A VERIFIED VCGEN BASED ON DYNAMIC LOGIC: AN EXERCISE IN META-VERIFICATION WITH WHY3 https://doi.org/10.1016/j....

liner.com
liner.com
Process-Verified Reinforcement Learning for Theorem Proving via Lean [Quick Review]


Quick review PROCESS-VERIFIED REINFORCEMENT LEARNING FOR THEOREM PROVING VIA LEAN Minsu Kim, Se-Young Yun ICLR Apr 23, 2026 Abstract While reinforcement learning from verifiable rewards (RLVR)...

why3.org
why3.org
8. The VC Generators — Why3 1.8.2 documentation


8. THE VC GENERATORS¶ This chapter gives information about the various processes that generate the so-called verification conditions, VC for short, from WhyML code. 8.1. PROGRAM FUNCTIONS¶ For each...

Why3


WHY3 WHERE PROGRAMS MEET PROVERS OVERVIEW Why3 is a platform for deductive program verification. It provides a rich language for specification and programming, called WhyML, and relies on externa...

zylos.ai
zylos.ai
Formal Specification and Type-Driven Safety for AI Agent Runtimes | Zylos Research


LIMITATIONS AND TRADEOFFS THE SPECIFICATION GAP Formal verification proves that the implementation matches the specification. It does not prove that the specification captures the right properties....

stelioszach.com
stelioszach.com
CEGVR · Counterexample-Grounded Verifiable Reasoning


No. 05 · Aegis Suite · Neurosymbolic Reasoning Working Paper · 2026 SOLVER-GROUNDED verifiable reasoning with a candidate-first LLM + SMT protocol. A five-method linear study asking whether solver...

jovin555.github.io
jovin555.github.io
Day 27: Frama-C WP Plugin: Deductive Verification | jovin555


* # Day 27: Frama-C WP Plugin: Deductive Verification Jul 09, 2026 5 min read * til * formal-verification * wp * deductive * coq WHAT I EXPLORED TODAY Today I dove into Frama-C’s WP (Weakest Prec...

themoonlight.io
themoonlight.io
[Literature Review] Automating Formal Verification with Reinforcement Learning and Recursive Inference


[LITERATURE REVIEW] AUTOMATING FORMAL VERIFICATION WITH REINFORCEMENT LEARNING AND RECURSIVE INFERENCE This thesis explores methods for automating formal verification using large language models (LL...

[Revisión de artículo] LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks


[REVISIÓN DE ARTÍCULO] LEAP: SUPERCHARGING LLMS FOR FORMAL MATHEMATICS WITH AGENTIC FRAMEWORKS The paper introduces LEAP (LLM-in-Lean Environment Agentic Prover), an agentic framework designed to en...

tspi.at
tspi.at
Frama-C with wp-dynamic and function pointers


FRAMA-C WITH WP-DYNAMIC AND FUNCTION POINTERS 02 Mar 2020 - tsp Last update 10 Mar 2020 Image: Reading time 9 mins INTRODUCTION Just as a reminder: What is static analysis and what does Frama-C an...

ai-math-seminar.github.io
ai-math-seminar.github.io
AI and Mathematics Seminar


Oct 29, 2025 | Tomer Galanti (Texas A&M) | LLM-ERM: Sample-Efficient Program Learning via LLM-Guided Search Abstract. We seek algorithms for program learning that are both sample-efficient and compu...

arxiv.gg
arxiv.gg
Rewarding Progress: Scaling Automated Process Verifiers for LLM Reasoning - arXiv.gg


REWARDING PROGRESS: SCALING AUTOMATED PROCESS VERIFIERS FOR LLM REASONING `2410.08146` · 2024-10-10 · Cited by 123 · 🧠 ready Amrith Setlur, Chirag Nagpal, Adam Fisch, Xinyang Geng, Jacob Eisenstein...

Code Llama: Open Foundation Models for Code - arXiv.gg


CODE LLAMA: OPEN FOUNDATION MODELS FOR CODE `2308.12950` · 2024-01-31 · Cited by 1589 · 🧠 ready Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Ad...

lri.fr
lri.fr
VALS - Deductive Program Verification


VALS VERIFIED ALGORITHMS, LANGUAGES AND SYSTEMS DEDUCTIVE PROGRAM VERIFICATION CONTEXT In the past decade, there have been significant advances made in the domain of deductive program verificatio...

fugumt.com
fugumt.com
Related papers: AlphaVerus: Bootstrapping Formally Verified Code Generation through Self-Improving Translation and Treefinement


ALPHAVERUS: BOOTSTRAPPING FORMALLY VERIFIED CODE GENERATION THROUGH SELF-IMPROVING TRANSLATION AND TREEFINEMENT * URL: http://arxiv.org/abs/2412.06176v1 * Date: Mon, 09 Dec 2024 03:22:35 GMT * Title:...

Fugu-MT 論文翻訳(概要): Agentic Program Verification


論文の概要: AGENTIC PROGRAM VERIFICATION * arxiv url: http://arxiv.org/abs/2511.17330v1 * Date: Fri, 21 Nov 2025 15:51:48 GMT * ステータス: 翻訳完了 * システム内更新日: 2025-11-24 18:08:19.085336 * Title: Agentic Program...

arxiv-troller.com
arxiv-troller.com
KVerus: Scalable and Resilient Formal Verificatio… - arXiv


KVERUS: SCALABLE AND RESILIENT FORMAL VERIFICATION PROOF GENERATION FOR RUST CODE Authors: Yuwei Liu, Xinyi Wan, Yanhao Wang, Minghua Wang, Lin Huang, Tao Wei arXiv ID 2605.03822 Submitted May 5...

stackoverflow.com
stackoverflow.com
How many temporary variables Frama-C WP plugin can handle? - Stack Overflow


HOW MANY TEMPORARY VARIABLES FRAMA-C WP PLUGIN CAN HANDLE? Asked 10 years, 1 month ago Modified 10 years, 1 month ago Viewed 36 times I was trying to generate weakest precondition of a particular...

z3 - The exact mechanism of mapping WhyML into SMT logic - Stack Overflow


THE EXACT MECHANISM OF MAPPING WHYML INTO SMT LOGIC Asked 10 years, 11 months ago Modified 10 years, 3 months ago Viewed 708 times Good day, auto deduction and verification hackers! In order to...

scribd.com
scribd.com
Code Intelligence: A Practical Guide | PDF | Computing | Software Engineering


ADVANTAGE TYPE LOSS TYPE DAPO 9-10 GEPO Clip-Cov GAE token-level SPO KL-Cov 8 GMPO Group relative sequence-level GPPO CISPO GFPO Other 4-7 FR3E GSPO LitePPO TreePO AEPO GRPO DPO 1-3 PRIME DCPO RLOO F...

scifaro.com
scifaro.com
VeruSAGE: A Study of Agent-Based Verification for Rust Systems — Scifaro


Home › Operating Systems › VeruSAGE: A Study of Agent-Based Verification for Rust Syste… VERUSAGE: A STUDY OF AGENT-BASED VERIFICATION FOR RUST SYSTEMS Operating Systems 2026-04-16 v2 Artificial In...

sambuz.com
sambuz.com
[PPT] - Frama-C WP Tutorial Virgile Prevosto , Nikolay Kosmatov and Julien PowerPoint Presentation - 1085834


FRAMA-C WP TUTORIAL VIRGILE PREVOSTO , NIKOLAY KOSMATOV AND JULIEN - - POWERPOINT PPT PRESENTATION ▶ Image: frama c wp tutorial Download Share Report Issue SMART_READER_LITE LIVE PREVIEW Frama...

paperzz.com
paperzz.com
Frama-C, a Collaborative Framework for C Code


verification consists in “proving a program”. The weakest precondition calculus proposed by Dijkstra [20] reduces any deductive verification problem to establishing the validity of first-order formula...

chapterpal.com
chapterpal.com
LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks — Read with an AI tutor


LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks LEAP: SUPERCHARGING LLMS FOR FORMAL MATHEMATICS WITH AGENTIC FRAMEWORKS Po-Nien Kung$^{1}$, Linfeng Song$^{2}$, Dawsen Hwang$...

college-de-france.fr
college-de-france.fr
Les logiques de programmes à l'épreuve du réel : tours et détours avec Frama-C/WP | Collège de France


11 Mar 2021 11:15 à 12:15 Les logiques de programmes à l'épreuve du réel : tours et détours avec Frama-C/WP Loïc Correnson 11 Mar 2021 11:15 à 12:15 Jeudi 11 mars 2021 Amphithéâtre Guillau...

utwente.nl
utwente.nl
A Deductive Verification Infrastructure for Probabilistic Programs - University of Twente Research Information


A DEDUCTIVE VERIFICATION INFRASTRUCTURE FOR PROBABILISTIC PROGRAMS * Philipp Schröer * , Kevin Batz * , Benjamin Lucien Kaminski * , Joost Pieter Katoen * , Christoph Matheja Research output: Contr...

Connector sources scanned

No connector sources scanned

