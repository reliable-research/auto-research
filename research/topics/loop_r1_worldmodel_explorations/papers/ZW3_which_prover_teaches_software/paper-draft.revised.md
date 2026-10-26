> **✅ CURRENT MANUSCRIPT.** Revised from `paper-draft.md`; see the revision log at the end
> and `../MAJORS.md` for every major and where it was fixed.

# Budget-Matched Formal Supervision: Comparing Lean Proofs and Dafny Verification for Software Transfer

## Abstract

Formal-proof supervision is increasingly considered a route to stronger software reasoning, yet its relative value across mathematical proofs and program verification remains unestablished, potentially misdirecting substantial data and training investments. Existing studies examine isolated formal domains, narrow software tasks, or unmatched corpora, compute, search, and acceptance yields; consequently, they cannot distinguish genuine transfer from exposure imbalance. We propose a controlled study that post-trains a shared 0.6B–1.7B checkpoint on Lean proofs, Dafny-style verification data, staged and order-controlled mixtures, and matched non-formal supervision. A common feasible budget intersection equalizes loss-bearing tokens, optimizer updates, sampled candidates, and validator-accepted trajectories while recording replay exposure. Paired win-minus-loss estimation then produces a scale-compatible transfer matrix across formal mathematics, code generation, execution reasoning, invariant inference, semantic equivalence, and program repair. Software claims are conditioned on a preregistered Lean positive-control gate, and reverse-order and interleaved curricula isolate presentation order from source composition. Evaluation uses the Budget and Replay Ledger, contamination-screened Formal-Math Positive-Control Panel, Paired Software-Family Panel, and Curriculum-Order Panel. Baselines comprise matched non-formal SFT, equal-update-only scheduling, the unmodified checkpoint, single-branch training, and reverse and interleaved curricula.

## Introduction

Formal supervision is increasingly used to post-train language models because proof assistants and program verifiers provide automatic, exact feedback without human evaluation. Mathematical-proof systems such as Lean train models to construct logically valid theorem derivations, whereas verification-aware languages such as Dafny expose program states, transitions, contracts, invariants, frame conditions, and verification conditions. These semantic objects may induce different transferable capabilities. The distinction matters particularly for small models, for which choosing a corpus or curriculum can determine whether limited training resources improve theorem proving, code generation, execution reasoning, or program repair.

Yet it remains unknown whether mathematical-proof supervision or program-verification supervision transfers more strongly to software tasks under genuinely matched post-training budgets. Current evidence is narrow or mixed. Xiaohan Lin et al., *FVEL: Interactive Formal Verification Environment with Large Language Models via Theorem Proving*, reported modest improvements on an SV-COMP subset, substantially weaker performance than a specialized verifier, and no gain on Code2Inv. Antonio Valerio Miceli Barone and Poon Tsz Nok, *Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification*, found gains concentrated in one semantic-equivalence setting alongside regressions in others. The one published formal-data fine-tuning result with a non-formal control — Lu et al., *From Informal to Formal* (FM-alpaca, ACL 2025, arXiv:2501.16207) — reports HumanEval transfer that swings from +62.5% relative over a weak SFT baseline (UltraChat) to under +1.3% over a strong one (Tulu-v3), and its 18k-pair corpus mixes five formal languages (Coq, Lean4, Dafny, ACSL, TLA+), so it cannot attribute the effect to either prover branch — precisely the baseline- and branch-confounds the present design removes. Conversely, the mature mathematical branch exemplified by Hubert et al., *Olympiad-level formal mathematical reasoning with reinforcement learning (AlphaProof)*, demonstrates large-scale theorem-proving capability but supplies no direct evidence of transfer to software tasks. Treating these unmatched results as general evidence of code transfer may therefore direct substantial training investment toward an unsuitable formal language or mechanism.

Existing approaches optimize individual branches rather than compare their transfer. Chuanhao Yan et al., *Re:Form—Reducing Human Annotations in Scalable Formal Software Verification with RL in LLMs: A Preliminary Study on Dafny*, improve verified Dafny generation through curated data and verifier-guided reinforcement learning, while Huajian Xin et al., *DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement Learning and Monte-Carlo Tree Search*, target absolute Lean theorem-proving performance. Task-specific systems—including Tianchi Li et al., *Guiding LLM-based Loop Invariant Synthesis via Feedback on Local Reasoning Errors*, and Lingxiao Tang et al., *ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning*—strengthen particular software capabilities without identifying which formal supervision source transfers most broadly. A controlled comparison is difficult because sequence lengths and verifier acceptance rates make token, update, sampled-trajectory, and accepted-trajectory budgets jointly incompatible unless training is capped at a common feasible intersection. Evaluation further requires comparable effects across heterogeneous metrics and a predeclared stopping rule when mathematical supervision fails to improve mathematical benchmarks. Curriculum analysis adds another confound: stage allocation must preserve all budget constraints while separating presentation order from mere exposure to both supervision sources.

We address these difficulties through a single normalization-complete transfer experiment starting from one shared 0.6B–1.7B checkpoint. The central insight is to identify supervision effects only within the largest budget simultaneously feasible for every arm. A shared Budget and Replay Ledger will enforce equal loss-bearing tokens, optimizer updates, sampled candidates, and validator-accepted trajectories for Lean, Dafny-style, staged-curriculum, and matched non-formal SFT conditions, while recording acceptance yield and replay multiplicity. A frozen Paired Evaluation Panel will express each arm contrast as a paired win-minus-loss effect, permitting comparison across native benchmark metrics without assuming commensurate units. Before software outcomes are opened, the Lean arm must pass a preregistered formal-mathematics positive-control gate; otherwise, confirmatory analysis will stop and the transfer matrix will remain diagnostic. Equal source quotas across Lean-to-Dafny, Dafny-to-Lean, and interleaved curricula will hold composition fixed, making temporal order the systematic difference among mixed-supervision conditions.

The evaluation will combine the Budget and Replay Ledger, a contamination-screened and dependency-disjoint Formal-Math Positive-Control Panel, a Paired Software-Family Panel spanning code generation, execution reasoning, invariant inference, semantic equivalence, and repair, and a disjoint Curriculum-Order Panel. Comparisons will include matched non-formal SFT, equal-update-only scheduling, the shared checkpoint without post-training, Lean-only and Dafny-only arms, and reverse-order and interleaved curricula. Conditional on the positive-control gate, the resulting transfer matrix will estimate relative branch effects for each outcome family and test whether mathematical-proof-to-program-proof staging improves upon both individual branches and exposure-matched curriculum alternatives.

## Contributions

- We propose a four-axis budget-matching design that caps all training arms at their common feasible intersection, jointly controlling tokens, optimizer updates, sampled candidates, and accepted trajectories.

- We introduce a validity-gated transfer matrix based on paired win-minus-loss effects, enabling normalization across heterogeneous formal-mathematics and software metrics without suppressing family-specific negative transfer.

- We isolate curriculum-order effects through equal source quotas and matched Lean-to-Dafny, Dafny-to-Lean, and interleaved conditions.

- We provide a controlled small-scale evaluation plan that distinguishes formal-supervision transfer from generic supervised post-training and from changes already present in the shared checkpoint.

## Problem Definition

## Formal Problem Definition

Let \(\theta_{0}\) denote a shared pretrained checkpoint containing between \(0.6\) and \(1.7\) billion parameters. Four post-training conditions are considered: mathematical-proof supervision (\(M\)), program-verification supervision (\(V\)), a staged mathematical-proof-to-program-verification curriculum (\(C\)), and matched non-formal supervised fine-tuning (\(N\)). The mathematical corpus \(\mathcal{D}_{M}\) contains Lean proof data. The verification corpus \(\mathcal{D}_{V}\) contains Dafny-style records encoding states, transitions, contracts, invariants, frame conditions, and verification conditions. The curriculum condition applies \(\mathcal{D}_{M}\) before \(\mathcal{D}_{V}\), whereas \(\mathcal{D}_{N}\) provides the non-formal control. For condition \(a\in\mathcal{A}=\{M,V,C,N\}\), post-training produces
\[
\theta_a=\operatorname{Train}(\theta_0,\mathcal{D}_a),
\]
where \(\mathcal{D}_C\) denotes the ordered curriculum \(\mathcal{D}_M\rightarrow\mathcal{D}_V\).

Let
\[
\mathcal{J}=\mathcal{J}_{\mathrm{math}}\cup
\{\mathrm{code},\mathrm{exec},\mathrm{inv},\mathrm{equiv},\mathrm{repair}\}
\]
index the evaluation families, where \(\mathcal{J}_{\mathrm{math}}\) contains the formal-mathematics benchmarks and the remaining elements denote code generation, execution reasoning, invariant inference, semantic equivalence, and program repair. For each \(j\in\mathcal{J}\), let \(E_j\) be its evaluation set, let \(m_j(\theta,x)\) be its predeclared performance measure oriented so that larger values are better, and define
\[
\mu_j(\theta)=\mathbb{E}_{x\sim E_j}\!\left[m_j(\theta,x)\right].
\]

Training expenditure for condition \(a\) is represented by
\[
B_a=(T_a,U_a,S_a,A_a),
\]
where \(T_a\), \(U_a\), \(S_a\), and \(A_a\) denote training tokens, optimizer steps, sampled trajectories, and accepted trajectories, respectively. Let
\[
\mathcal{R}=\{\mathrm{tok},\mathrm{step},\mathrm{sample},\mathrm{accept}\}
\]
denote the four required normalization regimes. Under regime \(r\in\mathcal{R}\), the corresponding budget component must satisfy
\[
B^{(r)}_{M,r}=B^{(r)}_{V,r}=B^{(r)}_{C,r}=B^{(r)}_{N,r},
\]
and the complete budget vector \(B^{(r)}_a\) must be reported for every condition. This yields four budget-matched comparison views despite differences in corpus length and trajectory-acceptance rate. All conditions must begin from \(\theta_0\) and use the same evaluation metrics, decoding or search procedure, and reporting conventions.

For each normalization regime \(r\), the required two-branch transfer matrix is
\[
\mathbf{T}^{(r)}
=
\left[
T^{(r)}_{a,j}
\right]_
{\substack{a\in\{M,V\}\\j\in\mathcal{J}}},
\qquad
T^{(r)}_{a,j}
=
\mu_j\!\left(\theta^{(r)}_a\right)
-
\mu_j\!\left(\theta^{(r)}_N\right).
\]
Thus, each entry measures the effect of formal post-training relative to matched non-formal fine-tuning. The relative advantage of mathematical-proof supervision over program-verification supervision on family \(j\) is
\[
D^{(r)}_j
=
T^{(r)}_{M,j}-T^{(r)}_{V,j}.
\]
Positive \(D^{(r)}_j\) favors mathematical-proof supervision, whereas negative \(D^{(r)}_j\) favors program-verification supervision.

The curriculum comparison is defined by
\[
K^{(r)}_j
=
\mu_j\!\left(\theta^{(r)}_C\right)
-
\max\!\left\{
\mu_j\!\left(\theta^{(r)}_M\right),
\mu_j\!\left(\theta^{(r)}_V\right)
\right\}.
\]
A positive \(K^{(r)}_j\) indicates that the staged curriculum outperforms both single-branch conditions on evaluation family \(j\). The empirical objective is to estimate
\[
\Phi=
\left\{
\mathbf{T}^{(r)},
\left(D^{(r)}_j\right)_{j\in\mathcal{J}},
\left(K^{(r)}_j\right)_{j\in\mathcal{J}}
\right\}_{r\in\mathcal{R}},
\]
thereby characterizing relative transfer rather than absolute theorem-proving capability.

Let \(P_{\mathrm{math}}(\theta)\) denote the predeclared aggregation of scores over \(\mathcal{J}_{\mathrm{math}}\). The mathematical positive-control gate requires
\[
P_{\mathrm{math}}\!\left(\theta^{(r)}_M\right)
>
\max\!\left\{
P_{\mathrm{math}}\!\left(\theta^{(r)}_V\right),
P_{\mathrm{math}}\!\left(\theta^{(r)}_N\right),
P_{\mathrm{math}}(\theta_0)
\right\}.
\]
If this condition fails, the mathematical arm is classified as undertrained; the transfer comparison is invalid, the failure must be reported, and the planned inferential analysis must stop.

## Challenges

Estimating \(\Phi\) is difficult because \(\mathcal{D}_M\), \(\mathcal{D}_V\), and \(\mathcal{D}_N\) can differ substantially in sequence length and trajectory-acceptance rate, so equality under one component of \(B_a\) does not imply equality under the other three; all regimes in \(\mathcal{R}\) are therefore necessary to separate supervision effects from budget artifacts. The structured verification records in \(\mathcal{D}_V\) jointly represent program states, transitions, contracts, invariants, frame conditions, and verification conditions, making their training signal qualitatively different from the proof traces in \(\mathcal{D}_M\) even when a nominal budget is matched. The entries of \(\mathbf{T}^{(r)}\) must also remain comparable across heterogeneous evaluation families without conflating task-specific metrics, decoding procedures, or reporting scales. Moreover, \(K^{(r)}_j\) must distinguish benefits of the ordered curriculum from those of either constituent branch under the same budget constraint. Finally, failure of the positive-control inequality prevents interpreting \(D^{(r)}_j\): an apparent software advantage for \(\theta^{(r)}_V\) would be uninformative if \(\theta^{(r)}_M\) had not learned the mathematical supervision strongly enough to win on \(\mathcal{J}_{\mathrm{math}}\).

## Method Overview

The framework will take a shared model checkpoint and three supervision sources—Lean proofs, Dafny-style program proofs, and matched non-formal verified responses—and produce budget-controlled estimates of supervision transfer and curriculum-ordering effects. Training arms will be constructed through a common accounting scheme, evaluated on a frozen panel spanning formal mathematics and five software-oriented outcome families, and subjected to a predeclared mathematical validity gate before confirmatory software results are examined. Mixed-supervision curricula will then reuse the same accounting and evaluation procedures to distinguish ordering effects from differences in source exposure.

The Budget Ledger will match and report loss-bearing tokens, optimizer updates, sampled candidates, and validator-accepted trajectories across all arms. It is designed to prevent sequence length, checker acceptance yield, and trajectory replay from masquerading as supervision effects when the four resource measures cannot otherwise be aligned. Common quotas determined from a disjoint blinded pilot will define the feasible comparison budget, while acceptance yield and replay multiplicity will remain explicit diagnostics.

The Paired Evaluation Panel will measure transfer across formal mathematics, code generation, execution reasoning, invariant inference, semantic equivalence, and repair. Because these families use heterogeneous native metrics, arm effects will be represented as paired win-minus-loss estimates with equal benchmark weighting within each family. A predeclared positive-control gate will require the Lean arm to improve formal-mathematics performance over non-formal supervision before software-family outcomes are opened; failure will terminate confirmatory analysis and leave the transfer matrix diagnostic.

The staged curriculum comparison will evaluate Lean-to-Dafny training against the reverse order, minibatch-interleaved supervision, both single-branch arms, and the non-formal control under the same ledger and evaluation panel. Equal source quotas and a shared optimizer-state policy will address the central challenge of separating temporal ordering from the benefit of receiving both supervision sources. Contrasts among the mixed-supervision arms will therefore estimate ordering effects, while contrasts with the single-branch and non-formal controls will assess whether staged supervision provides additional software-domain transfer.

## Methodology

## Budget-Matched Arm Comparison

Differences in sequence length and verifier acceptance rates make loss-bearing tokens, optimizer updates, sampled candidates, and accepted trajectories difficult to equalize simultaneously. If any dimension remains uncontrolled, apparent transfer effects may instead reflect unequal data volume, sampling effort, or trajectory reuse.

The comparison will therefore be restricted to the largest budget jointly feasible for every supervision arm. This common intersection permits simultaneous normalization without treating the branch-specific semantics of Lean checking, Dafny verification, and non-formal response validation as interchangeable.

Starting from a single shared checkpoint, we will train Lean, Dafny-style, and matched non-formal verified-response supervised fine-tuning arms. A shared Budget Ledger will record four quantities for each arm: the number of sampled candidates \(N\), unique checker-accepted trajectories \(K\), loss-bearing tokens \(T\), and optimizer updates \(S\). Each arm will sample exactly \(N\) candidates and retain exactly \(K\) accepted trajectories. Candidate retention will be stratified jointly by base-model success propensity and sequence length so that differences in initial task difficulty or response length do not alter the composition of the accepted training sets.

The values of \(N\), \(K\), \(T\), and \(S\) will be fixed at the largest common feasible intersection estimated using a disjoint, blinded pilot. The pilot will be used only to determine feasible quotas and packing constraints; it will not contribute training trajectories or evaluation items to the confirmatory study. Acceptance checkers and their configurations will be specified before arm construction. Lean and Dafny-style trajectories will be accepted according to their respective formal checkers, whereas non-formal responses will be subjected to a predefined task-appropriate validator. The design equalizes accepted quantity rather than assuming that acceptance has identical meaning across these validation regimes.

Deterministic packing will assign retained trajectories to update batches, and deterministic replay will fill any token shortfall caused by unequal sequence lengths. Every arm will consequently receive exactly \(T\) loss-bearing tokens over \(S\) optimizer updates. Replay decisions will be derived from the fixed packing procedure rather than model performance observed during training. Because shorter or less diverse accepted corpora may require more reuse, the Budget Ledger will additionally report acceptance yield, defined relative to the \(N\) sampled candidates, and replay multiplicity for every retained trajectory. Because shorter or less diverse accepted corpora require more reuse, replay multiplicity is a design variable rather than a nuisance to be corrected in analysis: each arm is trained under both a natural and a flattened replay regime (RQ2), and the resulting checkpoints are compared directly.

All trained arms will be evaluated on the same frozen Paired Evaluation Panel. Pairing each evaluation item and random seed across arms will ensure that contrasts reflect differences in supervision rather than differences in sampled test cases or stochastic evaluation conditions.

## Validity-Gated Transfer Matrix

The evaluation families use heterogeneous native metrics, so raw score differences cannot be compared directly across formal mathematics, code generation, execution reasoning, invariant inference, semantic equivalence, and repair. Moreover, software-transfer claims would be uninterpretable if Lean supervision failed to produce the intended formal-mathematical effect.

The evaluation will use a common ordinal effect estimand while retaining each benchmark’s native scoring procedure. A predeclared positive-control gate will be applied before software results are opened, preventing post hoc reinterpretation of software endpoints after an unsuccessful supervision manipulation.

For each benchmark, models will first be scored using its native metric. Given an arm and the matched non-formal control, every paired item-and-seed observation will then be classified as a win, tie, or loss according to the native scores. The corresponding matrix entry will be the paired win-minus-loss effect

\[
W = P(s_{\mathrm{arm}} > s_{\mathrm{control}})
    - P(s_{\mathrm{arm}} < s_{\mathrm{control}}),
\]

where \(s\) denotes the benchmark-specific score. This bounded estimand preserves the direction of paired differences without assuming that metric magnitudes are commensurate across benchmarks. Ties contribute zero, avoiding arbitrary numerical distinctions when the native metric reports equivalent performance.

Benchmark-level effects will receive equal weight within each evaluation family. Family-level estimates will therefore represent average comparative performance rather than being dominated by benchmarks with more items, seeds, or numerically larger metric ranges. Uncertainty intervals will be obtained through an item-by-seed stratified bootstrap that preserves the paired structure across arms. The resulting transfer matrix will report benchmark-level and family-level effects for formal mathematics and the five software families: code generation, execution reasoning, invariant inference, semantic equivalence, and repair.

The formal-mathematics comparison between the Lean and non-formal arms will serve as the positive control. Before any software-family result is revealed, its one-sided 95% lower confidence bound for \(W\) must exceed \(0.05\). If this criterion is not satisfied, confirmatory analysis will stop. The software portion of the matrix may subsequently be released only as diagnostic output, with its confirmatory status unchanged and without redefining endpoints, altering the gate, or using software outcomes to rationalize the failed control. If the gate is passed, the frozen analysis will proceed to the predeclared arm contrasts across all software families.

## Staged Curriculum Comparison

A mixed formal curriculum may benefit from temporal ordering, but an apparent advantage could arise merely from exposure to both supervision sources. The training design must therefore hold source composition and all budget dimensions fixed while varying only the order in which Lean and Dafny-style supervision are presented.

Equal source quotas make composition identical across mixed-supervision curricula. Reverse-order and interleaved controls then separate a genuine ordering effect from the general effect of receiving a mixture of mathematical and program-proof training.

Using the shared checkpoint and Budget Ledger, we will construct three mixed-supervision arms: Lean followed by Dafny, Dafny followed by Lean, and minibatch-interleaved Lean plus Dafny. Each source will contribute exactly half of the total training allocation: \(T/2\) loss-bearing tokens, \(S/2\) optimizer updates, \(N/2\) sampled candidates, and \(K/2\) accepted trajectories. Candidate acceptance, stratification, deterministic packing, and replay will follow the same procedures used in the budget-matched arm comparison. The interleaving schedule will be fixed before training and will preserve the same source-specific quotas as the two sequential curricula.

Optimizer state will remain uninterrupted across curriculum boundaries. In the sequential arms, parameters, optimizer moments, and the update counter will carry directly from the first stage into the second. This policy treats staging as a change in supervision order rather than as a restart or a second independent fine-tuning run. The reverse-order arm will preserve identical source exposure while exchanging temporal position, and the interleaved arm will remove a discrete stage boundary while maintaining the same total mixture.

Segmented Lean-only, Dafny-only, and non-formal controls will receive the same total budgets and optimizer-state policy. Their allocations will be divided into two consecutive halves even when both halves use the same supervision source, ensuring that comparisons with sequential curricula are not confounded by segmentation, checkpoint handling, or training duration. These controls will determine whether mixed formal supervision improves over committing the entire budget to one branch or to matched non-formal supervision.

Every curriculum will be evaluated on the frozen Paired Evaluation Panel using the same paired win-minus-loss estimand and family-level weighting. Contrasts between Lean-then-Dafny and the single-source controls will measure the value of the staged curriculum as a whole. Contrasts with Dafny-then-Lean and interleaved training will isolate temporal presentation order because source identities, source quotas, total budgets, optimizer continuity, and evaluation conditions are otherwise held fixed.

## Experiments

## Experimental Setup

The evaluation will estimate a budget-normalized branch-by-outcome transfer matrix from a shared checkpoint. The six training arms—Lean-only, Dafny-only, Lean→Dafny, Dafny→Lean, interleaved Lean/Dafny, and matched non-formal supervised fine-tuning (SFT)—will be compared using paired training seeds and frozen evaluation prompts. Under normalization-complete scheduling, arms will be matched on sampled candidates \(N\), accepted trajectories \(K\), training tokens \(T\), and optimizer updates \(S\). Decoding budgets, scoring procedures, and externally executable or verifiable oracles will be fixed within each comparison. Because variation across training seeds is part of the estimand, cross-run inference will use seed-cluster-robust procedures; simultaneous inference will be applied when multiple contrasts or families are tested.

The Budget and Replay Ledger will record \(N\), \(K\), \(T\), \(S\), and per-example replay counts and probabilities once per training step from the data-loader and sampler states. An example’s replay probability will be its empirical selection frequency across an arm’s optimizer updates. This dataset is necessary for detecting incomplete budget normalization and determining whether estimated transfer effects are distorted by uneven replay exposure.

The Formal-Math Positive-Control Panel will contain contamination-screened, dependency-disjoint Lean theorem-proving tasks from a pinned Lean/mathlib release. Before sampling, exact-hash duplicates will be removed. Contamination screening will exclude any theorem whose statement or proof shares a normalized 13-gram fingerprint with the training pool or shared-checkpoint pretraining shards, where normalization canonicalizes whitespace and identifiers. Dependency-disjointness will be enforced by partitioning the Lean import and dependency graph so that no evaluation theorem imports, or is imported by, a training theorem. This panel provides a positive control on which proof-oriented post-training should yield detectable transfer before software-domain effects are interpreted.

The Paired Software-Family Panel will balance code generation, execution reasoning, invariant inference, semantic equivalence, and repair. Each family will be extracted from a pinned source snapshot whose manifest records the source, commit or release hash, and extraction date. Exact duplicates and near-duplicates with MinHash Jaccard similarity of at least \(0.8\) will be removed within and across families. Every prompt will have an execution, verification, equivalence, or test-based oracle. The balanced design prevents larger families from dominating aggregate estimates and permits heterogeneous or negative transfer to be identified.

The Curriculum-Order Panel will provide frozen, mutually disjoint software-family splits for the curriculum experiments. Stable prompt identifiers will be assigned to at most one evaluation panel using a fixed, seeded partition function. The version-pinned manifest will record prompt identifiers, family labels, and oracle references, ensuring that all arms and seeds receive identical evaluation sets without reuse across RQ4–RQ6. This dataset isolates curriculum order from evaluation-set overlap.

Matched non-formal SFT is the principal baseline because it controls for generic supervised post-training while matching the complete four-axis budget. Equal-update-only scheduling is a normalization baseline that tests whether matching optimizer updates alone leaves consequential token or trajectory imbalances. The shared checkpoint without post-training provides a zero-exposure anchor for detecting trivial or sign-inverted effects. Lean-only and Dafny-only arms determine whether curriculum gains require exposure to both formal branches. Reverse-order and interleaved curricula hold branch exposure fixed while isolating the effect of ordering.

For paired comparisons, the outcome \(W\) will equal \(+1\) when the first arm succeeds and the second fails, \(-1\) when the reverse occurs, and \(0\) when their outcomes agree. Formal-mathematics success will require kernel-checked proof acceptance; software success will be determined by the applicable execution, verification, equivalence, or repair-test oracle.

The evaluation addresses the following research questions:

1. **RQ1:** Does four-axis budget matching control cross-arm exposure imbalance more reliably than equal-update-only scheduling?
2. **RQ2:** Are estimated arm effects robust to how replay exposure is distributed across accepted trajectories?
3. **RQ3:** Does the estimator detect the preregistered formal-mathematics positive control?
4. **RQ4:** Does program-verification post-training produce distinct family-level software transfer relative to mathematical-proof post-training?
5. **RQ5:** Does a Lean→Dafny curriculum outperform both single-branch training and matched non-formal SFT?
6. **RQ6:** Is the curriculum effect attributable to training order rather than exposure to both formal domains?

## RQ1: Four-Axis Budget Normalization

RQ1 tests whether matching sampled candidates, accepted trajectories, tokens, and optimizer updates prevents exposure differences from being mistaken for transfer. The practical challenge is that equal optimizer-update counts do not necessarily imply equal data, token, or accepted-trajectory exposure.

All six arms will be run from the shared checkpoint under both normalization-complete and equal-update-only scheduling, using eight independent scheduling and training seeds per arm and scheduler, for 96 runs. For each seed, the maximum pairwise relative imbalance will be computed across \(N\), \(K\), \(T\), and \(S\), with each pairwise difference divided by the corresponding pairwise mean. Joint one-sided bootstrap bounds will compare the two schedulers. Equal-update-only scheduling constitutes the normalization ablation: it removes explicit control of \(N\), \(K\), and \(T\) while retaining control of \(S\).

A positive result would show that normalization-complete scheduling limits the maximum imbalance to at most \(0.01\) and reduces it to no more than 20% of the equal-update-only value. This would support the hypothesis that all four exposure dimensions must be controlled and that update matching alone is insufficient.

The evaluation metrics are:

- Maximum pairwise relative imbalance over \(N\), \(K\), \(T\), and \(S\).
- Ratio of the normalization-complete maximum imbalance to the equal-update-only maximum imbalance.

## RQ2: Robustness to the Distribution of Replay Exposure

RQ2 tests whether arm effects remain stable under uneven replay exposure. The underlying challenge is that repeatedly selected training examples may disproportionately shape an arm's measured effect even when aggregate budgets are matched — because the Lean and Dafny corpora differ in verifier acceptance rate, equalizing accepted-trajectory *counts* does not equalize how often individual accepted examples are replayed.

**This must be tested by intervening on training, not by reweighting afterwards.** An earlier formulation of this question proposed stabilized inverse-replay weights \(w_i=\bar{p}/p_i\) over training examples, transported to the evaluation estimand through a Hájek estimator. That construction is invalid, and it is worth stating why, because the error is an easy one to make. The weights are indexed over *training examples*; the estimand is a mean over *held-out evaluation prompts* of an *already-frozen checkpoint*. Once training has concluded, a checkpoint's held-out behaviour is a deterministic function of the replay schedule that was actually executed. Reweighting the training distribution after the fact alters a bookkeeping quantity and cannot alter the model, so no channel exists from the weights to the estimand. The weighted and unweighted estimates would coincide identically, an equivalence test between them could not fail, and a null manufactured by the estimator's own algebra would be misread as evidence of replay robustness. **Replay-exposure robustness is a property of the training pipeline and is testable only by changing what training sees.**

The corrected design intervenes at scheduling time. Two replay regimes will be preregistered per arm and trained separately: (i) the **natural** regime, in which accepted trajectories are replayed as the sampler produces them, and (ii) a **flattened** regime, in which per-example replay multiplicity is capped at the arm's median and the freed replay slots are **deterministically redistributed** so that total exposure is unchanged. The redistribution rule is preregistered and performance-independent: freed slots are assigned by round-robin over the accepted trajectories whose multiplicity is strictly below the cap, taken in a fixed canonical order (ascending current multiplicity, ties broken by trajectory id), repeating until either all freed slots are placed or every trajectory has reached the cap; any residual slots in the latter case are placed by continuing the same round-robin with the cap lifted by one, and the residual count is reported. This keeps loss-bearing tokens, optimizer updates, sampled candidates, and accepted-trajectory totals identical to the natural regime, so the regimes differ in the *distribution* of exposure and not its total — which is what makes the flattened-minus-natural contrast attributable to replay concentration rather than to training less. Both regimes are held to the same four-axis budget intersection — loss-bearing tokens, optimizer updates, sampled candidates, and accepted trajectories — so flattening changes the *distribution* of exposure without changing its *total*. All six arms will be trained under both regimes with eight paired seeds — twelve training conditions and 96 runs, matching RQ1's budget — and evaluated on the same frozen panel of 4,200 prompts: 700 each from formal mathematics, code generation, execution reasoning, invariant inference, semantic equivalence, and repair.

The replay-robustness contrast is then a genuine difference between checkpoints, \(\mu_j(\theta_a^{\mathrm{flat}})-\mu_j(\theta_a^{\mathrm{natural}})\), estimated per arm and outcome family with clustering by prompt and training seed. The Budget and Replay Ledger records realized replay multiplicity in both regimes, so the manipulation can be verified rather than assumed.

A positive result would place every flattened-minus-natural contrast within a preregistered equivalence margin, with multiplicity-adjusted tests passing, supporting the conclusion that the transfer matrix is not materially driven by uneven replay exposure. Unlike the weighted-versus-unweighted comparison it replaces, **this test can fail** — a large flattened-minus-natural difference would show that measured transfer partly reflects which accepted examples the sampler happened to favour, and would require the transfer matrix to be reported under the flattened regime. If the doubled training cost is not affordable, the honest alternative is to drop RQ2 and state replay exposure as an unaddressed threat to validity, reporting realized multiplicity from the ledger as descriptive evidence; **it is not acceptable to retain a test that cannot fail.**

The evaluation metric is:

- For each arm \(a\) and outcome family \(j\), the flattened-minus-natural contrast
  \(\mu_j(\theta_a^{\mathrm{flat}})-\mu_j(\theta_a^{\mathrm{natural}})\), reported with a preregistered
  equivalence interval and multiplicity adjustment, clustered by prompt and training seed.
- Realized replay multiplicity per accepted trajectory under both regimes, from the Budget and Replay
  Ledger, verifying that the manipulation took effect and that accepted-trajectory totals were held equal.

## RQ3: Formal-Mathematics Positive Control

RQ3 asks whether the estimator detects an expected benefit of Lean post-training on held-out Lean theorem proving. The challenge is to establish estimator sensitivity on a domain-aligned positive control before interpreting weaker or heterogeneous software-family effects.

Lean-only and matched non-formal SFT will be trained from the shared checkpoint using 12 paired seeds and evaluated on 2,500 contamination-screened, dependency-disjoint Lean theorem tasks. The arm substitution from Lean training to budget-matched non-formal SFT isolates formal-proof post-training from generic supervised post-training. Mean Lean-minus-control \(W\) will be estimated with training seeds as the primary clustering unit. This test will serve as the stopping gate for RQ4–RQ6.

The gate will pass if the point estimate is at least \(0.10\) and its one-sided 95% lower confidence bound exceeds \(0.05\). This outcome would support the hypothesis that the estimator can identify meaningful domain-aligned transfer. If the gate does not pass, subsequent software and curriculum analyses will not be interpreted as confirmatory evidence.

The evaluation metric is:

- Mean paired formal-mathematics \(W\) across prompts and seeds, with kernel-checked proof acceptance defining success.

## RQ4: Family-Level Branch-by-Outcome Transfer

Conditional on the RQ3 gate, RQ4 tests whether Dafny post-training and Lean post-training yield distinguishable transfer across the five software capabilities. The challenge is to expose family-specific or negative transfer that an aggregate score could conceal.

Twelve paired seeds will be trained for each of the Dafny-only, Lean-only, and matched non-formal SFT arms. Evaluation will use a disjoint panel of 4,000 prompts, balanced at 800 prompts per software family. The shared checkpoint, four training budgets, decoding budget, and scoring oracles will be fixed. Replacing Dafny training with Lean training isolates branch choice, while comparison with matched non-formal SFT controls for generic post-training.

For each family, the transfer matrix will report Dafny-minus-non-formal, Lean-minus-non-formal, and Dafny-minus-Lean paired \(W\). The equal-weight mean of the five Dafny-minus-Lean family effects will provide the aggregate estimate. Simultaneous seed-cluster confidence intervals will be constructed for all family-level contrasts.

A positive aggregate result would require the equal-weight Dafny-minus-Lean effect to be at least \(0.05\) and significantly positive. This would support the hypothesis that program-verification post-training transfers more strongly to software tasks than mathematical-proof post-training. Regardless of the aggregate, every family-specific sign and interval will be reported to reveal heterogeneous or negative transfer.

The evaluation metrics are:

- Per-family paired \(W\) for Dafny versus non-formal SFT.
- Per-family paired \(W\) for Lean versus non-formal SFT.
- Per-family paired \(W\) for Dafny versus Lean.
- Equal-weight mean of the five family-specific Dafny-minus-Lean effects.

## RQ5: Curriculum Benefit over Single-Branch and Non-Formal Training

Conditional on the RQ3 gate, RQ5 tests whether Lean→Dafny training improves software performance beyond the strongest single-branch or non-formal comparator. The challenge is to distinguish a genuine cross-domain curriculum benefit from favorable selection of a weaker reference arm.

Lean→Dafny, Lean-only, Dafny-only, and matched non-formal SFT will be trained using 12 paired seeds and identical four-axis budgets. Evaluation will use a frozen, disjoint panel of 4,000 prompts, with 800 prompts from each software family. The single-branch ablations remove either the program-verification or mathematical-proof stage, while the non-formal control replaces both formal stages with matched generic supervised training.

The three curriculum-minus-comparator contrasts will be estimated jointly. Performance relative to the best comparator will be defined as the minimum of these three contrasts. Each contrast will also be decomposed by software family, and simultaneous seed-cluster lower confidence bounds will account for joint testing.

A positive result would require all three equal-weight contrasts to be at least \(0.05\), making their minimum at least \(0.05\), with every simultaneous 95% lower confidence bound above zero. This would support the hypothesis that the curriculum benefit requires the combined Lean→Dafny sequence and is not an artifact of comparator choice.

The evaluation metrics are:

- Minimum of the Lean→Dafny contrasts against Lean-only, Dafny-only, and matched non-formal SFT.
- Simultaneous seed-cluster lower confidence bounds for the three aggregate contrasts.
- Per-family decomposition of each curriculum-minus-comparator contrast.

## RQ6: Curriculum-Order Sensitivity

Conditional on the RQ3 gate, RQ6 tests whether the curriculum effect depends on presenting mathematical proofs before program proofs rather than merely exposing the model to both domains. The challenge is to separate ordering effects from total data and branch exposure.

Lean→Dafny, Dafny→Lean, and interleaved curricula will be trained with 12 paired seeds. The data pools, four-axis budgets, and optimizer settings will be identical; only presentation order will vary. Evaluation will use a disjoint panel of 9,000 prompts, balanced at 1,800 prompts per software family. Reverse-order and interleaved training are the curriculum-order ablations. The two Lean→Dafny contrasts will be tested jointly, with per-family decompositions reported alongside their equal-weight aggregates.

A positive result would require Lean→Dafny to exceed both Dafny→Lean and interleaved training by at least \(0.03\), with both multiplicity-adjusted tests rejecting non-positive transfer. This would support the hypothesis that the direction of the curriculum contributes to transfer beyond exposure to the same two formal domains.

The evaluation metrics are:

- Equal-weight software-family \(W\) for Lean→Dafny minus Dafny→Lean.
- Equal-weight software-family \(W\) for Lean→Dafny minus interleaved training.
- Per-family breakdowns of both curriculum-order contrasts.

## Related Work

**Which prior systems supply this study's training arms.** Two works are constitutive rather than
merely related: **Re:Form** is the program-verification arm's recipe, having demonstrated Dafny
verifier-guided post-training down to 0.5B, and **DeepSeek-Prover-V1.5** is the mathematical arm's.
Both are adopted as arm-supplying baselines. Each limitation below is stated as a gap that would
remain a gap if the present study did not exist, rather than as an observation that the work is not
this study.

## Formal Theorem Proving with Verifier Feedback

One line of work improves formal mathematical reasoning by coupling language models with proof-assistant feedback. Hubert et al. [2026] train AlphaProof through reinforcement learning in a formally checkable environment, while Xin et al.’s DeepSeek-Prover-V1.5 combines formal-language specialization, supervised fine-tuning, reinforcement learning from Lean feedback, and proof-path exploration through tree search. Lin et al.’s Goedel-Prover-V2 uses scaffolded data synthesis and verifier-guided self-correction, whereas Ren et al.’s DeepSeek-Prover-V2 constructs training traces through recursive subgoal decomposition. Dong et al. explicitly reward hierarchical proof decomposition, and Leang et al. use theorem provers to validate and refine synthetic mathematical reasoning data.

Their individual gaps are also specific rather than uniform. **AlphaProof** establishes that Lean proof states function as a genuine reinforcement-learning environment — states are prover states, actions are tactics — at approximately 80,000 TPU-days, but evaluates mathematics exclusively; its widely-cited 28/42 Olympiad score belongs to the **combined AlphaProof and AlphaGeometry 2 system**, with AlphaProof contributing three non-geometry solutions, and no code-transfer claim is made or tested. **DeepSeek-Prover-V1.5** never evaluates on any code task, and its 63.5% miniF2F and 25.3% ProofNet figures are search-heavy RMaxTS results at 32×6400 and 4×6400 generation budgets against a 51.6% pass@128 single-pass counterpart, so they are not directly comparable to small-model budgets. **Dong et al.** demonstrate that rewarding intermediate formal progress works — novel proved lemmas constitute 37.7% of the replay buffer, lifting AFP pass rate from 40.8% to 45.5% and an out-of-distribution set from 36.5% to 39.5% — but the out-of-distribution generalization measured is *within theorem proving*, leaving domain portability untested. **Leang et al.** provide the closest thing to cross-domain evidence, showing prover-checked intermediate reasoning improving *informal arithmetic* benchmarks by up to roughly five to six points on individual benchmarks; this establishes that formal checking can transfer outside the prover's own domain, but never to code. The mathematical branch is therefore mature in capability and entirely untested in software transfer — the complementary half of the gap described above.

## Learning to Generate and Verify Formally Specified Programs

A second line of work uses formal verifiers to train or guide models that generate verified programs and specifications. Tan studies reinforcement learning from verifiable rewards and verifier-guided recursive inference for program verification, while Aggarwal et al.’s AlphaVerus bootstraps verified code generation through iterative translation and verifier-driven refinement. Yan et al.’s Re:Form combines automated Dafny data curation, supervised fine-tuning, and verifier-guided reinforcement learning; Sun et al.’s Clover instead checks consistency among implementations, documentation, and formal annotations. Xiaohan Lin et al.’s FVEL translates C verification problems into Isabelle and fine-tunes models on proof dependencies and intermediate proof states, whereas the Proof2Silicon system applies reinforcement-learning-based prompt repair before translating verified Dafny programs into synthesizable hardware.

Each carries a distinct evidential gap that stands independently of the present study. **Re:Form** measures generalization only within Dafny and DafnyComp: its headline out-of-domain result — 14.0% pass@1 for the 14B RL model against 8.3% for SFT-only — is out-of-domain *inside formal verification*, and it reports no evaluation on ordinary software tasks. **FVEL** is the one system here that both trains on verification data and measures downstream transfer, and its own authors attribute the effect to corpus correlation rather than capability, noting that because FVELer originates from the seL4 micro-kernel, the correlation of the data makes fine-tuning on SV-COMP effective; the reported gains of 69→81 and 75→84 are drawn from a 1,000-problem random subset (6.9%→8.1% and 7.5%→8.4%) on which the symbolic solver UAutomizer solves 374, and the same fine-tuning yields 46→46 on Code2Inv. **Proof2Silicon** trains a prompt-repair policy while the target language model remains frozen, so whatever it demonstrates about verifier feedback concerns an external controller rather than retained model capability. **AlphaVerus** likewise obtains verified code without fine-tuning the underlying model. **Clover** certifies consistency at inference time and never updates parameters. Collectively these gaps mean the program-verification branch has no transfer result that survives its own authors' qualifications — which is the condition this study is designed to change. The nearest thing to a positive result, **FM-alpaca** (arXiv:2501.16207), fine-tunes on a five-language mixed formal corpus and reports code-benchmark gains that its own authors qualify ("may indicate") and that nearly vanish against a strong SFT baseline; because the corpus mixes both branches, it can neither separate mathematical-proof from program-verification supervision nor match budgets, and it is conceded here as the additive, mixed-corpus predecessor of this study's budget-matched per-branch control `N`.

## Formal Reasoning for Program Properties

A third line of work applies formal reasoning and machine-checkable feedback to specific program-analysis tasks. Wu et al.’s LEMUR integrates language-model proposals with automated reasoners through a sound verification calculus, while Kamath et al. investigate language-model generation of inductive loop invariants. Tianchi Li et al.’s LORIS localizes reasoning errors by translating natural-language proof steps into checkable logical implications and returning targeted feedback for invariant refinement. Miceli Barone and Poon train adversarial generator and evaluator agents for Haskell semantic equivalence, using Liquid Haskell proofs and execution-based counterexamples to validate self-play examples. These approaches remain specialized to particular verification or analysis tasks and therefore do not establish whether alternative forms of formal supervision yield broader, differentially transferable software capabilities.

## Reinforcement Learning from Execution Feedback

A fourth line of work improves code generation and reasoning through executable rather than deductive feedback. Le et al.’s CodeRL uses unit-test outcomes to train code generators, while Jain et al.’s µCODE learns multi-turn revision behavior from single-step rewards and a jointly trained verifier. Wang et al.’s StepCodeReasoner supervises intermediate execution states with structured trace anchors, and Yu et al. combine execution profiling, tree-structured search, and self-critique to refine process-level rewards. Tang et al.’s ExecVerify assigns interpreter-derived rewards to control-flow and variable-state predictions before transferring to code generation, whereas Gehring et al.’s RLEF trains iterative code revision from textual test feedback. The shared limitation is that execution-based rewards neither represent mathematical-proof or program-verification supervision nor support a controlled comparison of their respective transfer effects.

## Conclusion

Determining which forms of machine-checkable supervision improve software capability is essential for allocating limited post-training resources and for interpreting claims of cross-domain reasoning transfer. The proposed framework treats this question as a controlled causal comparison rather than a contest in absolute theorem-proving performance. Its central contribution is an integrated design that aligns heterogeneous formal training conditions at their common feasible exposure budget, measures outcomes through paired scale-independent effects, and prevents software conclusions when mathematical-proof training fails its preregistered validity check. By holding checkpoint, training exposure, evaluation prompts, decoding budgets, and external scoring oracles fixed, the study should reveal whether observed gains arise from mathematical reasoning, program-state semantics, generic supervised adaptation, or curriculum order. The resulting transfer matrix could provide actionable evidence for selecting Lean corpora, Dafny-style verification corpora, or staged supervision, while family-level reporting would preserve heterogeneous or negative effects hidden by aggregate scores. Future work should test whether the identified transfer patterns persist beyond small checkpoints and across additional proof assistants and verification languages. Further studies should also examine how corpus structure, verifier acceptance rates, and curriculum allocation interact while retaining normalization-complete comparisons and positive-control safeguards.


---

## Revision log (working note — remove before submission)

Revised from the AutoDiscussion output of room `9f4da36d` (twin; the original `e6e06795` stalled at
15 refiner rounds on `motivation`), which closed 6/6 with 4/6 clean and **two** unresolved majors.

### What the pipeline got right and should be preserved

- **The reframing survived intact.** The introduction reports FVEL as "modest improvements on an
  SV-COMP subset, substantially weaker performance than a specialized verifier, and no gain on
  Code2Inv," and the self-play result as "gains concentrated in one semantic-equivalence setting
  alongside regressions in others." Both are the verified readings, not the briefs' inflated ones.
- **The positive-control gate survived and was strengthened** into a blinding protocol: "Before
  software outcomes are opened, the Lean arm must pass a preregistered formal-mathematics
  positive-control gate; otherwise, confirmatory analysis will stop and the transfer matrix will
  remain diagnostic."
- **Four-axis matching became a common feasible intersection** — cap every arm at the largest budget
  simultaneously feasible for all of them across tokens, updates, sampled candidates, and accepted
  trajectories. This is a better construction than the seed's "report all four normalizations."
- **Curriculum order was separated from composition** via equal source quotas across Lean→Dafny,
  Dafny→Lean, and interleaved arms — a control the seed did not specify.
- **Paired win-minus-loss effects** avoid assuming commensurate units across heterogeneous benchmarks.
- No AlphaProof misattribution: the draft credits it with theorem-proving capability and explicitly
  says it "supplies no direct evidence of transfer to software tasks."

### Major 1 (experiment_design) — RQ2's transport step was vacuous; replaced

The generated RQ2 proposed stabilized inverse-replay weights transported to the evaluation estimand
by "reweighting each arm's accepted-trajectory training distribution," estimated with a Hájek
estimator. The weights index training examples; the estimand is a mean over held-out prompts of a
**frozen** checkpoint. No channel connects them, the weighted and unweighted estimates coincide
identically, and the stated success criterion — every contrast within (−0.05, 0.05) — **could not
fail**. A null produced by the estimator's algebra would have been reported as replay robustness.

Replaced with a training-time intervention: two preregistered replay regimes per arm — **natural**
(replay as the sampler produces it) and **flattened** (per-example multiplicity capped at the arm's
median) — both held to the same four-axis budget intersection, so exposure *distribution* changes
while exposure *total* does not. The contrast becomes a real difference between checkpoints,
μ(θ_flat) − μ(θ_nat), which **can fail**. Cost is doubled training; if unaffordable, the honest move
is to drop RQ2 and report realized replay multiplicity from the ledger as an unaddressed threat to
validity. Retaining a test that cannot fail is not an option.

### Major 2 (related_work) — circular limitations; replaced

All eight limitations restated the study's own research question. Replaced with independently
standing gaps, all primary-source verified: Re:Form measures OOD only *inside* formal verification
(14.0% vs 8.3% pass@1); FVEL's authors credit seL4 corpus correlation, and the effect is 6.9%→8.1%
on a 1,000-problem subset where UAutomizer solves 374, with Code2Inv at 46→46; Proof2Silicon trains a
prompt policy over a **frozen** model; AlphaVerus obtains verified code **without fine-tuning**;
Clover never updates parameters; AlphaProof evaluates mathematics only and its 28/42 belongs to the
**combined** system with AlphaGeometry 2; DeepSeek-Prover-V1.5 never evaluates any code task and its
headline figures are search-heavy (32×6400 and 4×6400 versus 51.6% pass@128 single-pass); Dong et
al.'s OOD generalization is *within* theorem proving; Leang et al. transfer to **informal arithmetic**,
not code. Re:Form and DeepSeek-Prover-V1.5 are now marked as arm-supplying baselines, resolving the
accompanying minor.

Together these support the framing the seed reached after verification: **neither branch has a
credible code-transfer result**, and the field cites both as though the question were settled.

### Outstanding

- Removed the "This section requires manual completion with proper citations" placeholder; the
  related-work prose still uses inline author-title references rather than linked citations with
  venues. Needs a bib pass, as with ZW2 and ZW4.
- Venue corrections for bib time: FVEL is **NeurIPS 2024 D&B**; DeepSeek-Prover-V1.5 is **ICLR 2025**;
  the semantic-equivalence self-play paper is **ACL 2026 Findings** (Poon & Miceli Barone); Leang et
  al. is **ACL 2025 Long**, 29941–29977; AlphaProof is *Nature* 651(8106):607–613 with **no arXiv
  version**; LORIS is **ACM TOPLAS 48(2), Article 8**.

- **2026-08-23 pre-push scoop re-sweep (8th pass).** Added FM-alpaca (arXiv:2501.16207) — the one
  published formal→code transfer result with a non-formal control — to the motivation and to the
  related-work concession paragraph. Its mixed five-language corpus and baseline-dependent gains
  (+62.5% rel. vs weak baseline, ~+1% vs strong) are exactly the confounds the budget-matched
  per-branch design removes; control `N` is now positioned as the budget-matched, per-branch
  successor of FM-alpaca's additive contrast rather than as unprecedented. Informal-domain
  transfer-matrix precedent (arXiv:2506.14965) recorded in the seed ledger.
