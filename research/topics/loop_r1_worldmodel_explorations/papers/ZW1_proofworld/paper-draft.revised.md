> **✅ CURRENT MANUSCRIPT.** Revised from `paper-draft.md`; see the revision log at the end
> and `../MAJORS.md` for every major and where it was fixed.

# Typed Verifier Verdicts for Matched Reinforcement Learning of Tool-Free Dafny Programs

## Abstract

Reinforcement learning for code generation increasingly uses formal verifiers, yet verifier acceptance does not necessarily imply behaviorally correct programs, particularly when weak specifications permit unintended solutions. This distinction matters for allocating training compute and deploying tool-free code generators in correctness-sensitive settings. Existing work reports gains from proof-completion rewards or dense execution feedback but does not isolate whether obligation roles and solver-verdict distinctions add information beyond reward density, binary acceptance, or a verified-goals ratio under matched training conditions. We propose a seed-blocked, four-arm Dafny study that forks shared checkpoints into typed-verdict, dense execution-state, binary-verifier, and verified-goals-ratio training. Synchronized reward snapshots preserve initialization, preservation, exit/postcondition, safety, and termination obligations while distinguishing proved, refuted, unknown, timeout, and invalid outcomes; deterministic coarsenings and frozen calibration keep reward timing and scale comparable. A dual-oracle panel scores every sampled candidate using the fixed verifier and execution harness, while sealed evaluation disables verifier and countermodel access. The evaluation uses the Matched tool-off hidden-test suite, Disjoint reward calibration-audit corpus, and Perturbation and weakened-specification stress suite. Comparisons against all three baselines assess hidden-test correctness, robustness, specification hacking, verifier–behavior divergence, and sensitivity to preregistered scalarizations.

## Introduction

Large language models are increasingly trained to generate programs using feedback that can be checked automatically. Unit tests expose whether a program behaves correctly on concrete inputs, while formal verifiers determine whether it satisfies logical specifications across all executions covered by those specifications. Recent systems have therefore replaced sparse final-answer rewards with denser signals derived from intermediate execution states, proof obligations, or verifier outcomes. This development is especially relevant to Dafny, where a verifier decomposes programs into obligations concerning initialization, invariant preservation, postconditions, safety, and termination. Such structured feedback may offer more precise learning signals than a single acceptance decision, but exploiting it increases training complexity and computational cost.

Yet the value of this additional formal structure remains unknown. Existing evidence does not establish whether rewards that retain obligation types and distinguish proved, refuted, unknown, timed-out, and invalid outcomes improve tool-free coding behavior beyond either an aggregate proof-completion ratio or equally dense execution-state supervision. This is a causal question: differences observed across independently developed systems may arise from checkpoints, training instances, sampling budgets, optimizers, or reward density rather than from the semantics of verifier feedback. Without a matched comparison, verifier-based gains could be incorrectly attributed to typed proof information even if they result from generic reward shaping, encourage weakened specifications, or increase verifier acceptance without improving functional correctness.

Verifier-guided approaches demonstrate that formal tools can support learning but do not isolate this effect. Max Tan, *Automating Formal Verification with Reinforcement Learning and Recursive Inference*, and Chuanhao Yan et al., *Re:Form — Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny*, optimize aggregate compilation or verification outcomes without comparing typed verdicts against matched execution supervision. Huajian Xin et al., *DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search*, and Z.Z. Ren et al., *DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition*, similarly learn from proof-assistant feedback, but their theorem-proving settings emphasize verifier-accepted proofs rather than tool-free program behavior. Yueke Zhang et al., *GraphAlignCoder: Aligning Program and Proof Graphs for Code Generation*, transfers explicit proof structure into code generation and evaluates without a prover, while Minsu Kim and Se-Young Yun, *PROCESS-VERIFIED REINFORCEMENT LEARNING FOR THEOREM PROVING VIA LEAN*, provides fine-grained tactic-level supervision. Neither determines whether obligation typing and solver-verdict distinctions add information beyond a scalar verification reward under controlled training conditions.

Execution-based methods provide the necessary competing account. Lingxiao Tang et al., *ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning*, and Hao Wang et al., *StepCodeReasoner: Aligning Code Reasoning with Stepwise Execution Traces via Reinforcement Learning*, derive dense supervision from observable runtime states, while Shuhang Wang et al., *DHRCL: Training Code LLMs with Dense Hierarchical Rewards and Curriculum Learning*, combines syntax, execution, testing, and structural signals. A rigorous comparison with these approaches must accommodate the divergence of on-policy policies after their common initialization, equalize reward timing and scale without discarding the distinctions under study, and separate behavioral correctness from formal acceptance across perturbations and previously unseen program structures. It must also preserve timeout as distinct from refutation and avoid assuming that independently sampled candidates remain identical after training begins.

We address these requirements through a randomized, seed-blocked four-arm policy-fork experiment centered on synchronized dual-oracle measurement. Every sampled candidate is evaluated by the same fixed verifier and execution harness before arm-specific rewards are computed. Typed obligation–verdict vectors form the richest signal; deterministic coarsenings of the same synchronized observations produce a binary verifier reward and an RLFR-style verified-goals ratio, while a dense execution-state arm provides the primary semantic comparator. Fixed, preregistered scalarizations and calibration on a disjoint corpus align reward opportunity and scale, whereas hierarchical estimation and clustered resampling compare diverged policies without requiring later candidate overlap. Evaluation will use the matched tool-off hidden-test suite, the disjoint reward calibration-audit corpus, and the perturbation and weakened-specification stress suite. The study will compare all three baselines and assess hidden-test correctness, robustness, specification hacking, verifier–behavior disagreement, and sensitivity to fixed scalarizations with verifier and countermodel access disabled during generation.

## Contributions

- We propose a randomized policy-fork design with dual-oracle scoring and exact budget matching to identify reward-representation effects despite on-policy divergence.
- We introduce synchronized typed obligation–verdict rewards and deterministic binary and verified-goals-ratio coarsenings that hold reward timing and scale constant.
- We develop a tool-off behavioral evaluation that combines independent hidden tests, semantics-preserving perturbations, controlled specification weakening, and post-hoc verifier diagnostics.
- We establish an empirical protocol for determining whether structured verifier feedback contributes predictive and training value beyond dense execution supervision and scalar proof completion.

## Problem Definition

## Formal Problem Definition

Let \(\mathcal{D}_{\mathrm{tr}}\) be a fixed collection of single-function Dafny training instances and \(\mathcal{D}_{\mathrm{te}}\) a fixed hidden-test evaluation set. All training arms begin from the same base policy checkpoint \(\pi_{\theta_0}\) and use the same optimizer, training instances, sampled-token budget \(B\), verifier \(V\), and execution harness \(H\). Let

\[
\mathcal{A}=\{\mathrm{TV},\mathrm{EX},\mathrm{BV},\mathrm{GR}\}
\]

denote the typed-verdict, dense execution-state, binary-verifier, and verified-goals-ratio arms, respectively. For each arm \(a\in\mathcal{A}\), training produces a policy \(\pi_{\theta_a}\). Candidate programs may be matched across arms only at initial seeding; subsequent candidates are sampled on-policy and therefore need not be identical.

For every candidate program \(p\), the harness returns an execution observation \(E(p)=H(p)\), including the execution outcomes and states required by the dense execution reward. Independently, the verifier returns a finite indexed set of obligations

\[
O(p)=\{(t_i,v_i)\}_{i=1}^{n(p)},
\]

where \(n(p)\) is the number of generated obligations,

\[
t_i\in\mathcal{T}
=\{\mathrm{init},\mathrm{pres},\mathrm{exit},\mathrm{safety},\mathrm{term}\}
\]

is the obligation type—initialization, preservation, exit/postcondition, safety, or termination—and

\[
v_i\in\mathcal{V}
=\{\mathrm{proved},\mathrm{refuted},\mathrm{unknown},
\mathrm{timeout},\mathrm{invalid}\}
\]

is its verifier verdict. Refutation must be accompanied by a countermodel. Timeout is represented as a distinct verdict and cannot be collapsed into refutation, unknown, or failure.

Define the normalized typed-verdict vector \(q(p)\in[0,1]^{|\mathcal{T}||\mathcal{V}|}\) by

\[
q_{t,v}(p)
=
\frac{1}{n(p)}
\sum_{i=1}^{n(p)}
\mathbf{1}[t_i=t\land v_i=v],
\]

with invalid programs handled explicitly by the preregistered reward definitions. The raw vector \(q(p)\), together with \(n(p)\), must be retained and reported. Let \(f_{\lambda}\) be a fixed scalarization of \(q(p)\) parameterized by preregistered weights \(\lambda\). The typed-verdict reward is

\[
R_{\mathrm{TV}}^{\lambda}(p)=f_{\lambda}(q(p)).
\]

Let \(g\) be the preregistered dense reward computed from execution observations. The execution-state reward is

\[
R_{\mathrm{EX}}(p)=g(E(p)).
\]

The binary-verifier reward is

\[
R_{\mathrm{BV}}(p)
=
\mathbf{1}\!\left[
n(p)>0
\land
\forall i,\;v_i=\mathrm{proved}
\right],
\]

and the verified-goals ratio is

\[
R_{\mathrm{GR}}(p)
=
\frac{1}{n(p)}
\sum_{i=1}^{n(p)}
\mathbf{1}[v_i=\mathrm{proved}],
\]

again subject to a preregistered treatment of cases in which no valid obligations are generated. Every sampled candidate \(p\), regardless of its training arm, must be evaluated by both \(H\) and \(V\) before the arm-specific reward is computed.

For evaluation, let \(Y(p,x)\in\{0,1\}\) indicate whether program \(p\) passes the fixed hidden tests for evaluation instance \(x\in\mathcal{D}_{\mathrm{te}}\). Programs must be generated tool-free: neither \(V\), verifier verdicts, nor countermodels may be consulted during evaluation. For seed \(s\), define the correctness of arm \(a\) as

\[
\mu_{a,s}
=
\frac{1}{|\mathcal{D}_{\mathrm{te}}|}
\sum_{x\in\mathcal{D}_{\mathrm{te}}}
Y\!\left(p_{a,s,x},x\right),
\qquad
p_{a,s,x}\sim\pi_{\theta_{a,s}}(\cdot\mid x).
\]

The primary estimand is the seed-matched effect of typed-verdict supervision relative to dense execution-state supervision,

\[
\Delta_{\mathrm{TV,EX}}
=
\mathbb{E}_{s}\!\left[\mu_{\mathrm{TV},s}-\mu_{\mathrm{EX},s}\right].
\]

The mandatory ablation estimand is

\[
\Delta_{\mathrm{TV,GR}}
=
\mathbb{E}_{s}\!\left[\mu_{\mathrm{TV},s}-\mu_{\mathrm{GR},s}\right],
\]

with \(\Delta_{\mathrm{TV,BV}}\) providing the corresponding comparison against binary verifier feedback. Matching refers to shared seeds, checkpoints, data, budgets, optimization, and evaluation instances—not to identical post-initialization candidate programs.

The study must additionally estimate arm-level differences in preregistered measures of robustness, specification hacking, and verifier-behavior divergence. Sensitivity to reward design is assessed by repeating the typed-verdict analysis over a preregistered set \(\Lambda\) of fixed scalarizations and reporting \(\Delta_{\mathrm{TV}^{\lambda},\mathrm{EX}}\) and \(\Delta_{\mathrm{TV}^{\lambda},\mathrm{GR}}\) for each \(\lambda\in\Lambda\). The empirical objective is to determine whether \(\Delta_{\mathrm{TV,EX}}>0\), while evaluating the mandatory ratio ablation and secondary outcomes without changing the shared experimental constraints.

## Challenges

The problem is difficult because the reward functions preserve substantially different information from the same candidates. \(R_{\mathrm{GR}}\) and \(R_{\mathrm{BV}}\) collapse \(O(p)\), whereas \(R_{\mathrm{TV}}^{\lambda}\) must distinguish both obligation types \(t\) and solver verdicts \(v\), including the semantically important separation between \(\mathrm{refuted}\) and \(\mathrm{timeout}\). At the same time, \(R_{\mathrm{EX}}\) must offer comparably dense supervision through \(E(p)\), making reward density an insufficient explanation for any observed \(\Delta_{\mathrm{TV,EX}}\). Causal attribution further requires all arms to share \(\pi_{\theta_0}\), \(\mathcal{D}_{\mathrm{tr}}\), \(B\), \(V\), \(H\), and the optimizer, even though their on-policy sampling distributions diverge after initialization and preclude post hoc identical-candidate matching. High verifier reward can also be decoupled from \(Y\) through specification hacking or verifier-specific behavior, so proof-oriented outcomes must be compared with tool-free hidden-test correctness and explicit divergence measures. Finally, \(f_{\lambda}\) necessarily reduces the structured vector \(q(p)\) to a scalar training signal; preregistration, reporting of the raw vectors, and analysis across \(\Lambda\) are therefore required to distinguish benefits of typed feedback from artifacts of a particular weighting scheme.

## Method Overview

The framework takes shared policy checkpoints, programming tasks, verifier signals, and execution outcomes as input and produces causal estimates of how alternative reward semantics affect functional correctness. From each checkpoint, matched policy replicas are trained under typed-verdict, dense execution-state, binary-verifier, and verified-goals-ratio rewards while holding training resources and evaluation infrastructure constant. Because these policies generate increasingly different candidates during training, comparability is established through randomized forks and common scoring rather than candidate overlap.

Reward signals are first constructed from synchronized verifier observations and then supplied to the corresponding training arms. Fixed policy snapshots are subsequently evaluated by a frozen Dual-Oracle Panel that applies both formal verification and execution-based assessment to every arm. The resulting evidence supports contrasts among reward designs, while a separate tool-off evaluation determines whether observed gains transfer to hidden-test correctness, unseen program structures, and perturbed inputs without access to verifier feedback or countermodels.

The matched causal reward comparison uses seed-blocked randomized policy forks to isolate the effect of reward semantics from checkpoint choice, task composition, compute budget, optimization, verifier configuration, and test harness. It addresses the central difficulty that on-policy arms diverge after initialization, making direct comparisons of later candidates inappropriate. Common dual-oracle scoring and checkpoint- and task-aware inference will permit arm-level estimates without assuming that the policies continue to explore identical outputs.

Typed-verdict reward construction preserves the obligation type and the distinct meanings of proved, refuted, unknown, timeout, and invalid outcomes. Binary-verifier and verified-goals-ratio rewards are derived by deterministic coarsening of the same synchronized signals, while the dense execution-state arm provides a non-verifier dense-reward control. This design addresses the confounding between semantic structure and generic properties such as reward frequency, magnitude, timing, or proof-completion density by calibrating the arms under common constraints.

Tool-off behavioral validation treats independent hidden-test correctness as the primary measure of learned coding behavior. Models will generate outputs on a blinded battery with verifier and countermodel access disabled, including unseen program structures and paired semantics-preserving perturbations; property-based and metamorphic tests will then assess clean and perturbed behavior. Post-hoc verifier and specification analyses will quantify robustness, weakened-specification behavior, verifier–behavior disagreement, and sensitivity to fixed typed-reward scalarizations, thereby distinguishing transferable functional improvements from verifier-specific optimization.

## Methodology

## Matched Causal Reward Comparison

On-policy training causes reward arms to generate increasingly different candidates after initialization, precluding comparisons that rely on candidate overlap. Comparable causal estimates therefore require shared starting conditions, exact budget matching, and evaluation by common oracles.

Randomized policy forks isolate the effect of reward semantics without requiring the resulting policies to visit identical trajectories. Applying both formal and execution-based scoring to every evaluated candidate further distinguishes genuine behavioral improvement from verifier alignment, while controlling sampled-token budgets removes compute expenditure as a competing explanation.

We will conduct a seed-blocked, four-arm randomized fork trial from shared policy checkpoints. Replicate policies will be assigned to typed-verdict, dense execution-state, binary-verifier, or verified-goals-ratio rewards. All arms will use the same task instances, sampled-token budgets, candidates per task, optimizer configuration, update schedule, verifier, and test harness. Randomization will occur within checkpoint-seed blocks so that each reward condition is represented under comparable initialization and training conditions.

At fixed code snapshots, a frozen Dual-Oracle Panel will evaluate every on-policy candidate using both the common verifier and the execution oracle. This design permits candidates to differ across arms while retaining a common measurement procedure. Verifier outcomes will characterize formal acceptance, whereas execution outcomes will measure functional behavior under the shared test harness. Their joint application will expose cases in which an arm improves one oracle without corresponding improvement on the other.

Arm contrasts will be estimated using a checkpoint-by-task hierarchical model that accounts for variation attributable to initialization and task difficulty. Uncertainty will additionally be assessed through cluster bootstrap resampling over checkpoint seeds and task instances, preserving dependence among observations produced by the same seed or instance. The resulting analysis will attribute differences to reward assignment under matched training resources rather than to later candidate overlap, oracle choice, or computational budget.

## Typed-Verdict Reward Construction

The reward representation must preserve distinctions among obligation types and solver outcomes while remaining comparable to binary and scalar alternatives in frequency and magnitude. Equalizing reward density and scale is technically difficult because naïve calibration can inadvertently remove the semantic distinctions under study.

The central design choice is to construct all verifier-derived rewards from synchronized observations and obtain simpler rewards through deterministic coarsening. This holds reward timing, source events, and calibration procedure constant, leaving the availability of obligation and verdict identities as the principal experimental difference.

**Making partial candidates verifiable.** A prefix of a Dafny program is, in general, not a Dafny program: it may close no braces, declare no postcondition, or truncate mid-expression, and the verifier will reject it on syntax before any obligation is evaluated. Snapshotting raw token prefixes would therefore yield a degenerate signal in which nearly every early snapshot reports `invalid`, and the dense proof reward would carry almost no information where it is most needed. We therefore define a deterministic **completion procedure** applied at every snapshot before the verifier is invoked, and report it as part of the method rather than as an implementation detail.

At snapshot \(k\), the prefix is closed into a syntactically well-formed compilation unit by a rule-based completer that (i) closes open delimiters in the order the parser expects, (ii) replaces any unterminated statement or expression with a typed hole, (iii) leaves declared-but-unwritten method bodies **empty**, and (iv) leaves every already-written specification clause untouched.

Crucially, the completer inserts **no assumption of any kind** into unwritten bodies. An earlier
version of this design supplied `assume false;` stubs, intending to stop unfinished code from failing
spuriously. That is exactly backwards: `assume false` renders the remaining path unreachable, so the
verifier discharges the enclosing method's *original* postconditions and assertions **vacuously**. The
contamination would land on genuine obligations the model did write, which no tagging of inserted
scaffolding can undo — and it is precisely the vacuity failure mode the companion adequacy study
exists to measure. Any stub that strengthens the path condition is disqualified for the same reason.

The reward therefore **abstains rather than assumes**. Obligations arising solely from inserted holes
are labelled `synthetic`; an obligation is labelled `indeterminate` only while **the program text its own
verification condition depends on** is incomplete — not merely because the enclosing method is
unfinished. The distinction is what makes the dense signal feasible: gating on whole-method
completeness would leave nearly every snapshot of a single-function candidate empty, since the method
closes only at the end. Obligations become determinate at different times — precondition
well-formedness and invariant initiation once the pre-loop code and invariant clause exist,
preservation once the loop body closes, postcondition sufficiency and termination only at method
close — so each obligation's determinacy is computed from its own dependency footprint. Both are **excluded from the reward**, and both are distinct from `unknown` and
`timeout`, which denote a solver that ran and did not conclude. Only obligations whose own
dependency footprint is complete contribute reward at a snapshot — determinacy is a property of the
obligation, never of the enclosing method — so the dense signal grows as the candidate does, and a
snapshot's verdict vector is never inflated by obligations the verifier could only discharge because
of an assumption we inserted. We report the per-snapshot share of `indeterminate`
obligations, since a high early share is the expected shape of the signal rather than a defect, and a
*low* one would suggest the completer is doing more than closing syntax. Completion is deterministic, seed-independent, and identical across arms; it is applied to the execution oracle's snapshots as well, so the dense proof and dense execution signals are computed at the same positions on the same completed artifacts and remain matched by construction. Snapshots at which completion fails — the prefix cannot be closed into a parseable unit — are recorded as a distinct `uncompletable` outcome and excluded from both rewards, with their frequency reported, since a high rate would indicate the snapshot schedule is too aggressive.

Where incremental verification is available, the completer reuses the previous snapshot's verification context so that per-snapshot solver cost stays sublinear in \(K\); where it is not, per-snapshot cost is charged in full and reported, because the dense arms' solver budget is otherwise silently \(K\) times the sparse arms'.

**Snapshots are placed at syntactic-completion boundaries, not at evenly spaced token offsets.** Evenly
spaced offsets would put most snapshots of a single-function candidate inside an unfinished body, where
every obligation is `indeterminate` and the packet carries no reward. The dense arms would then be
dense in name only, and the headline typed-versus-execution comparison would quietly degenerate into a
comparison of two terminal rewards. We therefore emit a snapshot at each position where the completer's
output strictly extends the previously verifiable content — each point at which a top-level declaration,
a statement, or a specification clause closes — up to a cap of \(K_{\max}=32\). The boundary set is a
function of the candidate's own text, so it varies across candidates but is **identical across arms for
a given candidate**: the proof and execution oracles are invoked at the same positions on the same
completed artifacts. Matching is therefore between arms on a candidate, not a fixed count across
candidates, and candidates yielding fewer than \(K_{\max}\) boundaries emit fewer packets rather than
padded duplicates.

**A usable-packet-rate gate decides whether the dense comparison is interpretable at all.** Call a
packet *usable* when it contains at least one obligation with a determinate verdict — `proved`,
`refuted`, `unknown`, or `timeout` — that is neither `synthetic` nor `indeterminate`. We preregister a
minimum median usable-packet rate across candidates, measured on a pilot split before the main runs. If
the dense arms fall below it, the honest report is that at this model scale and corpus the dense proof
signal is not achievable, that the arms are operating as terminal-reward arms, and that the
typed-versus-execution contrast is uninterpretable as a dense comparison — a negative result about
feasibility rather than a null result about typed verdicts. Reporting the usable-packet rate alongside
every dense-arm result is mandatory, since a reader cannot otherwise distinguish "typed verdicts do not
help" from "typed verdicts were never delivered."

For each candidate, verifier state will then be recorded at these snapshots. At every snapshot, the reward pipeline will compute changes in the count associated with each obligation-type-by-verdict channel. Verdict channels will separately represent proved, refuted, unknown, timeout, and invalid outcomes rather than treating all non-proved obligations as equivalent. Events unavailable at a snapshot will be zero-filled, ensuring that the 25 obligation-type-by-verdict channels are present in the same arrangement in every packet, and that all four arms emit the same number of packets **on any given candidate**. The count itself is a property of the candidate, not a constant: snapshots sit at that candidate's syntactic-completion boundaries, so the packet count varies across candidates under the cap \(K_{\max}=32\). Zero-filling equalizes channel arrangement across arms; it never pads a candidate up to a fixed count.

The typed representation will transform channel-wise count changes into channel-normalized, multi-head advantages. These advantages will be combined using a single preregistered fixed weight vector during the primary comparison. Alternate fixed weight vectors will be retained exclusively for sensitivity analysis, preventing adaptive weight selection from influencing the main training comparison.

Scalar and binary controls will be derived from the same snapshot records. The ratio reward will deterministically collapse the typed state to the proportion of proved obligations among all obligations, whereas the binary reward will indicate whether all obligations are proved. Because these controls use the same snapshots and underlying verifier events, they will receive reward at the same token positions as the typed representation. This construction avoids confounding semantic resolution with reward timing or event availability.

Before reinforcement learning, every arm will be calibrated on a frozen corpus. Reward values will be scaled to unit root-mean-square magnitude under a common clipping rule, with calibration parameters fixed before policy optimization. This procedure will align reward scale without merging the obligation-type and verdict channels retained by the typed arm. The complete transformation—from raw verifier records to typed, ratio, and binary rewards—will be deterministic and fixed before the randomized training trial.

## Tool-Off Behavioral Validation

Formal acceptance alone cannot determine whether training improves program behavior or merely encourages verifier-specific strategies, including weakened specifications. Evaluation must therefore separate functional correctness from verifier acceptance across unseen program structures and semantics-preserving perturbations while maintaining sufficient comparability across reward arms.

Behavioral correctness will be treated as the primary outcome by withholding verifier and countermodel feedback during generation and judging outputs with independent semantic tests. Paired perturbations will measure robustness under controlled changes, while post-hoc formal diagnostics will identify specification manipulation and verifier–behavior divergence without influencing the sampled programs.

The frozen Dual-Oracle Panel will sample pass@1 outputs from each trained policy with verifier and countermodel access disabled. Evaluation will use a blinded battery stratified by unseen program structures. Each clean task will be paired with semantics-preserving prompt and input perturbations, allowing within-task comparison of behavioral stability while controlling for the intended program semantics.

Generated programs will be judged using independent property-based and metamorphic hidden tests. These tests will be constructed separately from the training verifier so that passing them requires preservation of the intended behavior rather than exploitation of verifier-specific conditions. Clean and perturbed outputs will be evaluated under the same testing procedure, enabling matched analysis of correctness degradation under each perturbation.

After behavioral evaluation, the common verifier will be applied to every generated program. An abstract-syntax-tree comparator against the original specification will additionally identify changes consistent with weakened or altered specifications. Combining these post-hoc diagnostics with hidden-test outcomes will distinguish successful behavior, verifier rejection of correct behavior, verifier acceptance of incorrect behavior, and verifier passes associated with specification weakening.

The analysis will report clean and perturbed functional correctness, specification-hacking incidence, verifier–behavior disagreement, and paired robustness outcomes for each reward arm. The same evaluation will be repeated for every preregistered typed scalarization, using matched tasks and perturbations, to quantify whether conclusions depend materially on the fixed aggregation of typed reward channels.

## Experiments

## Experimental Setup

**Two disjoint test sets.** Each task carries a reward-visible training set, which is the only set any oracle may consult during training, and a sealed evaluation set used exclusively for tool-off measurement and never exposed to any reward channel, arm, or checkpoint-selection decision. The two are disjoint by construction and generated so that passing one does not trivially imply passing the other. This separation is what allows the execution-reward arm to be trained on execution feedback while the tool-off endpoint remains uncontaminated; without it, the execution arm would be evaluated on the signal it was trained against.

The evaluation will use matched four-arm training runs and sealed, tool-off tests to isolate the effect of reward representation while controlling initialization checkpoints, training instances, optimization, sampled-token budgets, verifier behavior, and test harnesses. The four arms will use typed-verdict reward, dense execution-state reward, binary verifier reward, and an RLFR-style verified-goals ratio. Unless an individual research question specifies otherwise, comparisons will be paired by task and checkpoint.

Three complementary datasets will be used. The matched tool-off hidden-test suite contains 6,000 sealed tasks stratified by repository or template family, obligation-type signature, solver-verdict mix, and difficulty. It is the primary behavioral benchmark because it supports paired comparisons of tool-independent correctness across reward representations. The disjoint reward calibration-audit corpus contains frozen candidates from task families excluded from training and primary evaluation, covering feasible combinations of obligation type and verdict. This separation enables detection of packetization errors, reward-scale mismatches, and circular predictive leakage. The perturbation and weakened-specification stress suite pairs clean tasks with semantics-preserving surface variants and controlled specification weakenings. It is included to assess invariance to irrelevant transformations, specification hacking, verifier–hidden-test divergence, and sensitivity to reward scalarization.

Dense execution-state reward is the primary baseline because it isolates the effect of typed verdict feedback from dense execution supervision under otherwise identical training resources. Binary verifier reward collapses the available verifier signals to pass or fail, testing whether any advantage requires typed verdict structure rather than verifier supervision alone. The RLFR-style verified-goals ratio aggregates the same obligation signals used by the typed method into a scalar coverage measure. It therefore provides a controlled ablation of the information retained by typed reward packets.

The primary behavioral metric will be tool-off hidden-test pass@1. Supporting metrics will include paired arm differences, confidence intervals, checkpoint-level heterogeneity, perturbation retention, worst-group performance, verifier-pass/hidden-failure divergence, and scalarization spread. Reward-pipeline audits will measure packet-count violations, reward root-mean-square (RMS) scale, and RMS ratios. Predictive-information analyses will use out-of-fold log loss, relative log-loss reduction, calibration error, and task-clustered confidence bounds.

Key fixed settings include eight shared initialization checkpoints, the frozen 25-channel (obligation-type \(\times\) verdict) packet schema evaluated at each candidate's own boundary snapshots under the cap \(K_{\max}=32\) — not a fixed 32 slots per candidate — and identical training instances, optimizers, sampled-token budgets, verifiers, and harnesses across matched arms. Primary paired comparisons will use 10,000 two-way cluster-bootstrap resamples over tasks and checkpoints. Reward calibration factors and packet schemas will be frozen before auditing. Predictive probes will use identical preprocessing and nested 10-fold cross-validation grouped by task. Scalarization analysis will use eight fixed scalarizations selected before hidden-test access and RMS-matched using the disjoint audit corpus.

The evaluation addresses the following research questions:

1. **RQ1:** What is the causal effect of typed-verdict reward, relative to dense execution-state reward, on tool-off hidden-test pass@1 under fully matched conditions?
2. **RQ2:** Does retaining typed solver-verdict information improve tool-off correctness relative to collapsing the same signals into a verified-goals ratio?
3. **RQ3:** Does the reward pipeline preserve matched reward-opportunity counts and reward scale across arms on data excluded from calibration?
4. **RQ4:** Do typed reward packets retain non-circular information about hidden correctness that is lost under scalar collapse?
5. **RQ5:** Is correctness learned with typed-verdict reward stable under semantics-preserving perturbations, and is this stability greater than that of dense execution-state reward?
6. **RQ6:** Does typed-verdict training reduce verifier-pass/hidden-failure divergence under weakened specifications while remaining insensitive to preregistered scalarization choices?

## RQ1: Causal Effect of Typed-Verdict Reward

RQ1 tests whether typed-verdict reward improves tool-independent correctness relative to dense execution-state supervision. The underlying challenge is to attribute any difference specifically to reward representation rather than to initialization, training data, optimization, computation, verifier behavior, or evaluation conditions.

Typed-verdict, dense execution-state, binary verifier, and verified-goals-ratio models will be trained from the same eight initialization checkpoints. Training instances, optimizer, sampled-token budget, verifier, and harness will be matched across arms. One tool-off completion from every arm–checkpoint pair will be evaluated on each of the 6,000 sealed tasks. The primary comparison will pair typed-verdict and dense-reward outcomes by task and checkpoint. The binary and verified-goals-ratio arms will serve as secondary ablations that respectively remove typed verdict structure and collapse obligation-level information into a scalar. Paired differences will be estimated using 10,000 two-way cluster-bootstrap resamples over tasks and checkpoints.

The hypothesis is that typed verdicts provide more useful training information than dense execution states for behavior that must generalize without tool access. A positive result will require a typed-minus-dense pass@1 difference of at least 0.02 and a two-sided 95% cluster-bootstrap interval excluding zero.

Evaluation metrics will comprise per-arm tool-off hidden-test pass@1, the paired typed-minus-dense difference, its confidence interval, and descriptive typed-minus-binary and typed-minus-ratio differences.

## RQ2: Information Retained Beyond Scalar Reward Collapse

RQ2 examines whether the structure of solver verdicts contributes information that is lost when the same obligation signals are reduced to a verified-goals ratio. In plain terms, it tests whether preserving what happened for each obligation is more useful than retaining only the aggregate fraction of verified goals.

The analysis will reuse the matched four-arm experiment, the 6,000 sealed tasks, and the eight shared checkpoint blocks. Typed-verdict and verified-goals-ratio outcomes will be compared task by task using 10,000 two-way cluster-bootstrap resamples. Because both rewards derive from the same underlying obligation signals, this comparison is the principal scalar-collapse ablation. The dense execution-state and binary verifier arms will remain as matched secondary checks.

The hypothesis is that obligation-level types and verdicts convey training information beyond aggregate verified-goal coverage. Validation will require a typed-minus-ratio pass@1 difference of at least 0.02, with a two-sided 95% cluster-bootstrap interval excluding zero.

Evaluation metrics will include tool-off hidden-test pass@1 for each arm, the paired typed-minus-ratio difference, its confidence interval, and checkpoint-level heterogeneity.

## RQ3: Reward Opportunity and Scale Matching

RQ3 tests whether the implemented reward pipeline gives all arms the same number of reward opportunities and comparable reward magnitudes on data not used for calibration. This audit targets implementation artifacts that could otherwise confound behavioral comparisons, including missing packets, inconsistent packetization, and reward-scale differences.

The packet schema and scalar calibration factors will be frozen before evaluation. Each arm will emit rewards through the frozen 25-channel schema at that candidate's own boundary snapshots — the audit checks per-candidate agreement across arms and must **not** assert a fixed count of 32 — for 10,000 frozen candidates drawn from 2,000 disjoint tasks and five generation seeds. Packet counts will be recorded for every candidate, and each arm’s reward RMS will be compared with that of the typed arm. The binary and verified-goals-ratio constructions will serve as fixed collapses of the same obligation signals, while the dense execution-state arm will test whether scale matching also holds for the alternative supervision representation. A task-clustered simultaneous bootstrap equivalence analysis will assess the RMS ratios.

The hypotheses are that reward opportunity counts are exactly matched and that calibration places all arms on comparable scales. A positive result will require every audited candidate to emit the **same** number of packets in every arm — the count itself varies across candidates, since snapshots sit at syntactic-completion boundaries — together with a median usable-packet rate at or above the preregistered threshold and every non-typed arm’s simultaneous confidence interval for its RMS ratio to the typed arm to lie wholly within \([0.95, 1.05]\).

Evaluation metrics will comprise packet-count violation rate, per-arm reward RMS, RMS ratio relative to the typed arm, and simultaneous confidence intervals.

## RQ4: Non-Circular Predictive Information

RQ4 investigates whether typed packets contain information about hidden correctness that is absent from the verified-goals ratio. The challenge is to test predictive content without allowing hidden-test outcomes to influence reward construction, calibration, candidate generation, or feature preprocessing.

The study will use 12,000 frozen candidates from 2,400 tasks excluded from training, reward calibration, and primary evaluation. Preregistered regularized logistic probes will predict hidden correctness from either the candidate's typed reward packets — the frozen 25-channel schema emitted at that candidate's own boundary snapshots under the cap \(K_{\max}=32\), so the packet count varies per candidate — or the verified-goals ratio alone. Both probes will use identical preprocessing and nested 10-fold cross-validation grouped by task. Hidden correctness will appear only as the prediction label. The ratio-only probe constitutes the scalar-collapse ablation, ensuring that any difference reflects information preserved by the typed representation rather than differences in the underlying candidates or labels.

The hypothesis is that typed obligation and verdict structure carries predictive information that cannot be recovered from aggregate verified-goal coverage. A positive result will require at least a 0.05 relative reduction in cross-validated log loss for the typed-packet probe, with a one-sided 95% lower confidence bound at or above 0.05.

Evaluation metrics will include out-of-fold log loss, relative log-loss reduction, calibration error, and the task-clustered confidence bound.

## RQ5: Robustness to Semantics-Preserving Perturbations

RQ5 tests whether correctness learned under typed-verdict reward remains stable when task presentation changes without altering task semantics, and whether this stability exceeds that of dense execution-state training. The targeted challenge is preventing models from relying on superficial regularities that do not survive benign changes in identifiers, formatting, specification wording, or context.

For each of 6,000 base tasks, the typed and dense models from all eight matched checkpoints will be evaluated on the clean input and six preregistered semantics-preserving variants. The variants will cover identifier changes, equivalent specification rewrites, conjunct reordering, formatting changes, and irrelevant-context insertion. All evaluations will disable verifier and countermodel access. Clean-versus-perturbed evaluation will provide the invariance ablation, while the matched typed-versus-dense comparison will identify whether reward representation affects robustness. Joint task-and-checkpoint cluster bootstrapping will be used for inference.

The hypotheses are that typed-verdict training preserves most clean-task correctness under surface perturbations and yields higher perturbed correctness than dense execution-state training. A positive result will require simultaneous lower confidence bounds of at least 0.90 for the typed arm’s perturbed-to-clean retention and at least 0.02 for its perturbed pass@1 advantage over the dense arm.

Evaluation metrics will comprise clean and perturbed pass@1, perturbed-to-clean retention, the paired typed-minus-dense difference, per-perturbation performance, and worst-group retention.

## RQ6: Weakened-Specification Divergence and Scalarization Sensitivity

RQ6 evaluates whether typed-verdict training reduces cases in which a weakened specification passes the verifier while still failing unchanged hidden tests. It also tests whether the resulting tool-off behavior depends materially on the particular scalarization used to combine typed reward information.

The experiment will evaluate 10,000 weakenable tasks under preregistered specification-removal transformations while leaving hidden tests unchanged and disabling tool access. Typed-verdict and verified-goals-ratio models from the eight matched checkpoints will be compared on verifier-pass/hidden-failure events. This comparison tests whether typed obligation-level feedback reduces specification hacking relative to scalar coverage reward. Separately, eight typed variants will be trained using scalarizations fixed before hidden-test access and RMS-matched through the reward audit. These variants constitute the scalarization-sensitivity ablation. Task-and-checkpoint cluster bootstrapping with simultaneous bounds will quantify both effects.

The hypotheses are that typed-verdict training discourages solutions that exploit weakened specifications and that its performance is stable across reasonable fixed scalarizations. A positive result will require the upper confidence bound on the typed-to-ratio divergence-rate ratio to be at most 0.80 and the upper confidence bound on the maximum pass@1 spread across scalarizations to be at most 0.02.

Evaluation metrics will include the weakened-specification verifier-pass/hidden-failure rate, the typed-to-ratio rate ratio, pass@1 for each scalarization, maximum scalarization spread, and simultaneous confidence bounds.

## Related Work

## Verifier-Guided Program Generation and Verification

Verifier-guided program generation uses machine-checkable feedback to synthesize implementations, specifications, annotations, and proofs. Tan [2026] and Yan et al. [2025] apply verifier-reward reinforcement learning to Dafny generation, while Aggarwal et al. [2024] bootstrap verified programs through translation, verifier feedback, and iterative refinement. Jha et al. [2025] repair prompts for verified code and hardware generation while leaving the target model frozen, whereas Sun et al. [2023], Wu et al. [2023], and Lin et al. [2024] integrate language models with consistency checking, automated reasoning, or interactive theorem proving. Li et al. [2026] and Kamath et al. [2023] target loop-invariant synthesis, Huang et al. [2026] augments verifier feedback with test-based completeness rewards for specification synthesis, and Zhang et al. [2026] aligns program structure with formal proof flow. Ye et al. [2026] and Xu et al. [2026] complement these systems with benchmarks for holistic verifiable-code generation and real-world verification-condition proving. However, this line of work does not isolate whether typed, verdict-specific proof-obligation feedback improves tool-free functional correctness over binary verification, scalar proof-completion signals, and comparably dense execution feedback under matched training conditions.

**The scalar proof-obligation precursor.** The reward that the verified-goals-ratio arm \(\mathrm{GR}\) collapses to is not our invention,
and the closest prior instance of it is not peer-reviewed. A non-archival industry report (The
Haladir Team, 2026) trains Qwen2.5-Coder-7B-Instruct and Qwen3-8B with offline single-turn GRPO on a
17,521-program Dafny corpus derived from Re:Form's Python2Dafny data, using a shaped
per-proof-obligation reward: \(R_k=-1\) when the skeleton or syntax fails, \(R_k =
\text{verified\_goals}_k/\text{total\_goals}_k\) when verification runs, and \(0\) when no goals are
present. The authors describe it as computing "the proportion of verified proof obligations
discharged, providing continuous gradients for partial correctness," and motivate it explicitly
against binary signals: "Unlike unit test-based verification which provides binary pass/fail signals,
this process yields fine-grained feedback through partial proof completion." They further report
prover-free transfer to Python, their HCT variant reaching 22.0 pass@1 on LiveCodeBench (2406–2409)
against an 18.3 base, and conclude that training purely on Dafny suggests "some level of
generalization past the formal verification domain."

We therefore claim novelty neither for a graded per-obligation proof reward nor for the observation
that Dafny post-training can survive removal of the verifier. We also do **not** claim a multi-turn
advantage. That report trains offline and single-turn, and so do we: our candidates are generated in
one pass, and the progress signal is the change in the obligation--verdict vector between adjacent
**syntactic-completion boundaries within a single generation**, not between repair turns. This is a
denser signal than a terminal reward but it is not interactive repair, and an earlier framing of this
work distinguished itself partly on being multi-turn where that report is single-turn. That
distinction does not survive: it was never instantiated here, and we withdraw it rather than let a
reader infer a capability the design does not have. Extending obligation-verdict rewards across repair
turns is future work, and it is the natural follow-on if the single-generation result holds. We adopt that reward as the **verified-goals-ratio arm** \(\mathrm{GR}\) (arm `A4` in the experiment specification) and
ask the narrower question this paper is built around: whether *typing* the obligations and
distinguishing *disproved* from merely *undecided* carries information beyond the proportion
discharged. Three properties of that report keep the question open. Its reward is an
**undifferentiated ratio** — obligations are untyped, so a failed loop invariant is indistinguishable
from a failed postcondition, and a weighted per-category variant is defined but, in the authors'
words, "was not implemented for this report." It has **no verdict structure**: timeout, unknown, and
refutation collapse into a single not-discharged count. And it runs **no execution-supervision
baseline at any budget** — every non-RLFR number in its tables is quoted from published technical
reports and the LiveCodeBench leaderboard — while nonetheless asserting that "this report establishes
that RLFR outperforms standard execution-based baselines on general coding benchmarks." That
comparison is the one this study runs.

Its evidential weight is limited and we report it as such: the work is unrefereed, releases no
models, code, or data, withholds its methodology pending contact with the authors, and its Table 1
compares its own models on LiveCodeBench 2406–2409 against external models quoted at 2407–2411, so
the base-versus-RLFR contrast is internally consistent while its cross-model claims are not on a
common window. The source is also no longer available at its original URL (HTTP 404 as of 21 August
2026) and survives as a single web-archive capture; we cite the archived copy as the primary locator.
Because no implementation details are published, \(\mathrm{GR}\) is a **formula-faithful ablation under our
harness** rather than a reproduction: it instantiates the published reward formula and nothing else,
and we do not claim to reproduce the reported results.

## Execution-Grounded Reinforcement Learning for Code

Execution-grounded reinforcement learning derives supervision from tests, runtime traces, or other executable properties of generated programs. Le et al. [2022] use unit-test outcomes and a learned critic to guide program synthesis and repair, while Gehring et al. [2025] and Jain et al. [2025] train models to exploit iterative execution feedback in multi-turn code generation. Tang et al. [2026] reward predictions of intermediate control flow and variable states, and Wang et al. [2026] supervise anchored execution trajectories with stepwise credit assignment. Yu et al. [2024] combine execution metrics with process-level reasoning signals, Wang et al. [2026] organize syntax, execution, correctness, and structural rewards hierarchically, and Ouyang et al. [2022] investigate static-analysis rewards when execution signals become sparse. Barone and Nok [2026] further use formal equivalence proofs and counterexamples to support semantic-equivalence self-play. However, these approaches do not determine whether obligation type and solver-verdict identity provide benefits beyond equally dense execution-state supervision for tool-free correctness.

## Prover Feedback for Formal Reasoning

Prover-guided formal reasoning trains or searches for machine-checkable mathematical proofs using proof-assistant feedback. Xin et al. [2024] combine reinforcement learning from Lean feedback with tree search, whereas Ren et al. [2025] incorporate recursive subgoal decomposition and verified subproof generation. Lin et al. [2024] use scaffolded data synthesis and verifier-guided self-correction, Dong et al. [2024] reward hierarchical proof decomposition, and Kim and Yun [2026] obtain dense tactic-level supervision from Lean’s elaboration process. Leang et al. [2025] use theorem proving to validate synthetic reasoning data, while Hubert et al. [2026] demonstrate reinforcement-learning-based formal reasoning at Olympiad level. However, this literature primarily optimizes prover acceptance and does not establish whether fine-grained solver outcomes transfer to tool-free program behavior or outperform matched scalar and execution-derived rewards.

> This section requires manual completion with proper citations.

## Conclusion

Reliable code-generation training requires evidence that formal feedback improves executable behavior rather than merely teaching models to satisfy a particular verifier. The proposed study provides a controlled account of reward semantics: shared policy origins, matched computation, synchronized feedback opportunities, and joint verifier–execution scoring make it possible to attribute downstream differences to the information retained in each reward. Its central contribution is an integrated framework connecting structured proof evidence to independent behavioral validation while preserving distinctions among obligation roles and solver outcomes and explicitly testing whether those distinctions survive scalar collapse. Evaluation on sealed tasks, disjoint reward audits, and perturbation and weakened-specification stresses will establish whether any advantage extends to tool-off hidden-test correctness, remains stable under semantically equivalent inputs, and avoids verifier acceptance achieved through underspecification. If the planned contrasts support these expectations, the findings will justify typed verification feedback as a behaviorally meaningful training signal; otherwise, they will delimit when simpler execution or scalar verifier rewards are preferable. Future work should extend the framework from single-function Dafny tasks to multi-function and repository-scale programs and examine transfer across verification ecosystems. Further research should develop scalarization strategies and specification-quality controls that remain robust without leaking verifier or countermodel feedback into tool-off evaluation.


---

## Revision log (working note — remove before submission)

Revised from the AutoDiscussion output of room `29167d1d`, the fourth and final ZW1 seed, which closed
6/6 with 5/6 clean and one unresolved major. The three earlier rooms (`687d0e9e`, `91a3c142`,
`fdb5f013`) are superseded; the first stalled 15 refiner rounds on `motivation`, the next two were
withdrawn as the novelty position was corrected against verified readings of the competing work.

### What the pipeline got right

- **RQ2 is the ablation the paper needs.** "Information Retained Beyond Scalar Reward Collapse"
  compares typed-verdict against verified-goals-ratio rewards task by task on the same underlying
  obligation signals, with dense execution-state and binary-verifier arms retained as matched
  secondary checks. That is exactly the \(\mathrm{GR}\) (seed `G3b`) contrast the seed made mandatory, and it survived intact.
- The four-arm matched design, the dual-oracle synchronized measurement (every candidate scored by
  both verifier and execution harness before arm-specific rewards), and the sealed tool-off hidden
  tests all survived.
- **No scope inflation** — unlike ZW4, which committed to roughly 600 training runs against a seed
  that specified layered instrumentation.

### The major (related_work) — fixed

> "The problem statement names the RLFR-style verified-goals ratio as a mandatory ablation arm, yet
> none of the eight deeply compared works instantiates a scalar proof-ratio or goals-verified-fraction
> reward … which weakens the legibility of the comparison for exactly the contrast the study must run."

Correct, and the cause was ours: RLFR is that anchor but was omitted from the room's `references`
payload because it has no arXiv ID, though the schema accepts `{citation, url}` without one. The arm
was named three times in the body (in the problem statement and experimental setup) while having no
citation entry anywhere. A dedicated anchor paragraph is now inserted in Related Work, immediately
before the execution-grounded family: it concedes the shaped per-obligation reward and the
prover-free transfer, then names the three properties that keep our question open (undifferentiated
ratio, no verdict structure, no execution baseline at any budget despite claiming one).

Per the strict re-review, \(\mathrm{GR}\) is described as a **formula-faithful ablation under our harness**, not
a reproduction — the source is unrefereed, deleted from the live web, and publishes no implementation
details, so an exact reproduction cannot be claimed.

### Citation repair

**All 28 citations in the generated draft rendered as `[n.d.]`** — every author, no dates. Repaired
from the verified record: Le et al. 2022, Sun et al. 2023, Wu et al. 2023, Kamath et al. 2023,
Aggarwal et al. 2024, Lin et al. 2024, Xin et al. 2024, Yu et al. 2024, Dong et al. 2024, Yan et al.
2025, Gehring et al. 2025, Jain et al. 2025, Ren et al. 2025, Leang et al. 2025, Jha et al. 2025, and
the 2026 entries (Tan, Li, Huang, Zhang, Ye, Xu, Tang, Wang, Nok, Yun). One entry rendered as "A
recent system [n.d.]" with its authors dropped entirely — that is Proof2Silicon, now Jha et al.
\[2025\], with the frozen-target-model detail restored since it is the point of citing them here.

This `[n.d.]` failure is more severe than the citation defects in the companion packages, which at
least carried years and links. A full bib pass is still required.

### Outstanding

- Venue corrections at bib time: RLEF is **ICML 2025, PMLR 267:19034–19055** (six-author camera-ready,
  not arXiv v2's seven); ORPS must appear under its ICML title *"Reasoning Through Execution"*; μCODE
  is **ICML 2025 Spotlight**; CodeRL is **NeurIPS 2022** on a CodeT5 backbone; Re:Form is **TMLR
  05/2026**; LORIS is **ACM TOPLAS 48(2) Art. 8**; GraphAlignCoder is arXiv:2608.11394.
- Keep a local copy of the recovered RLFR text; a single web-archive capture is fragile.

- **2026-08-23 round-9 strict re-review (post round-7/8 edits).** Two majors, both residue of fixes
  that were applied to one artifact and never mirrored into this one:
  1. **Fixed-`K=32` packet assertions removed from the manuscript.** Round 7 excised the fixed-`K`
     design from `experiment-spec.md` in ten places, but three survived here: *"every candidate
     produces the same number and arrangement of reward packets"* (Methodology), *"32 schema-indexed
     reward slots per candidate"* (Experimental Setup), and *"Each arm will emit rewards through 32
     schema-indexed slots"* (RQ3). The last contradicted the paragraph directly beneath it, which
     already said the count varies across candidates, and asserted exactly what the spec's RQ3(a)
     says must **not** be asserted. All three now state the rule correctly: the schema has **25**
     channels, the packet **count** is the candidate's own boundary count under the cap
     \(K_{\max}=32\), matching across arms is per-candidate, and zero-filling equalizes channel
     arrangement rather than padding to a fixed count.
  2. **The undefined arm identifier `G3b` is gone.** Related Work referred five times to "arm G3b",
     an identifier from the seed's withdrawn six-arm `G0`–`G5` table that appears nowhere else in
     this manuscript — whose own arm vocabulary is \(\mathcal{A}=\{\mathrm{TV},\mathrm{EX},
     \mathrm{BV},\mathrm{GR}\}\) — and nowhere in the spec, which names the same arm `A4`. A reader
     had no way to resolve the referent. It is now the verified-goals-ratio arm \(\mathrm{GR}\), with
     the `A4` correspondence stated once; `major_fix_rlfr_anchor.md` keeps the old names and carries
     a mapping key.

- **2026-08-23 round-10 (deer-flow academic-paper-review pass).** One residual fixed-count assertion
  the round-9 sweep missed, in RQ4: *"predict hidden correctness from either the 32 typed reward
  packets"* — the fourth survivor of the withdrawn fixed-`K=32` design, hiding in a sentence round 9
  did not touch because it names the probe input rather than the packet-emission rule. Now states the
  variable-count rule (25-channel schema, candidate's own boundary count under the cap
  \(K_{\max}=32\)). Found by `deerflow_review_2026-08-23.md` (W-level finding); no other text changed.
