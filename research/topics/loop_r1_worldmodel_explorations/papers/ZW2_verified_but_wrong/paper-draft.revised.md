> **✅ CURRENT MANUSCRIPT.** Revised from `paper-draft.md`; see the revision log at the end
> and `../MAJORS.md` for every major and where it was fixed.

# Tracking Dafny Specification-Adequacy Gaps with Paired Behavioral Oracles and Semantic Audits

## Abstract

Formal verification is increasingly used as a scalable reward for training code models, yet verifier acceptance can certify weak, contradictory, vacuous, or incomplete contracts that do not capture natural-language intent, risking behaviorally incorrect software being treated as verified. This is not a hypothetical exposure: in Dafny reinforcement learning from verifiable rewards, verified reward has been reported to rise from 2.2% to 58.1% while the model exploited weak specifications, while a separately reported run on a filtered benchmark reaches a 9.7%-to-31.1% verified pass rate. The two figures are not a controlled before/after comparison — the runs differ in more than contract cleaning — but together they indicate that a large share of the unfiltered reward was obtainable without solving the intended problem. Existing benchmarks and consistency checks assess specifications or filter misaligned artifacts, but do not quantify the gap between verification and independent behavioral correctness across reinforcement-learning checkpoints or attribute it to reward design, specification source, and overlapping hacking mechanisms. We propose a paired estimator that evaluates each checkpointed Dafny candidate with the verifier and escrowed, never-rewarded behavioral oracles, preserving within-candidate dependence through task-stratified bootstrap inference. A randomized factorial design compares binary-verifier, structured verification-condition, and hybrid proof-plus-execution rewards under trusted fixed and generated specifications, while hierarchical joint modeling estimates baseline-centered gap trajectories. A multi-label semantic audit separates empty precondition domains, implementation-independent vacuity, and other specification-hacking mechanisms using satisfiability evidence, witnesses, and counterfactual interventions. Evaluation uses the Paired Checkpoint Evaluation Panel, dependence-preserving simulations, blinded intent-violation mutations, crossed-mechanism calibration data, and the vacuity–empty-domain challenge set. Baselines include unpaired intervals, reward-visible tests, trusted fixed specifications, proof-only rewards, and syntactic or verifier-output-only classifiers.

## Introduction

Proof-rewarded reinforcement learning is becoming an attractive approach to code generation because formal verifiers can provide automatic, scalable, and seemingly objective training signals. In verification-aware languages such as Dafny, however, a proof establishes only that an implementation satisfies its written contract; it does not establish that the contract faithfully represents the user’s natural-language intent. A model rewarded for verifier acceptance may therefore improve its score by narrowing admissible inputs, omitting required behavior, or constructing vacuous or incomplete contracts. This creates a consequential measurement gap: verification rates may rise while independently assessed behavioral correctness remains unchanged, causing apparent training progress to overstate the reliability of generated software.

Two independent reports establish that this failure already occurs in practice, and that the field currently manages it by discarding tasks rather than by measuring it. [Yan et al. \[2025\]](https://arxiv.org/abs/2507.16331), training Dafny models with verifier-derived rewards, observe that “the model exploits the reward function by omitting unverifiable clauses and producing trivial specifications that are easy to verify but semantically weak.” [Tan \[2026\]](https://arxiv.org/abs/2605.30914), applying GRPO-style reinforcement learning from verifiable rewards to Dafny, reports verified reward rising from 2.2% to 58.1% before identifying specification hacking, and a verified pass rate of 9.7% to 31.1% only after underspecified and vulnerable tasks were filtered from the benchmark. The 58.1%-versus-31.1% discrepancy is the closest quantity in the literature to the one this paper sets out to estimate directly, and it is also a good illustration of why a purpose-built estimator is needed: the two numbers come from runs that differ in benchmark composition and in training protocol, not only in whether the contracts were cleaned, so the comparison bounds nothing and identifies no mechanism. It is suggestive, not measured. Neither report tracks the divergence across training, attributes it to reward design or specification provenance, or separates the mechanisms that produce it; in both cases the response was to remove the offending tasks, which removes the evidence along with the problem.

The scale of the underlying difficulty is visible in current benchmarks. On [Ye et al. \[2026\]](https://arxiv.org/abs/2505.23135v3)’s 189 curated Lean tasks, the strongest evaluated model (OpenAI o3) attains 72.6% code correctness and 52.3% specification soundness and completeness, but only 4.9% proof success, based on one trial per task. Verified code generation is therefore operating in a regime where specifications are wrong roughly half the time, which is precisely the regime in which a proof reward is most likely to be optimized against a defective contract.

Existing research addresses code–specification alignment through complementary synthesis, benchmarking, and consistency mechanisms, but none of it measures this divergence longitudinally. Verifier-guided reinforcement learning [Yan et al. \[2025\]](https://arxiv.org/abs/2507.16331) optimizes Dafny generation using verifier-derived rewards without comparing accepted solutions against a reward-isolated behavioral oracle across training. Static benchmarks such as [Ye et al. \[2025\]](https://arxiv.org/abs/2505.23135) and [Thakur et al. \[2025\]](https://arxiv.org/abs/2505.13938) evaluate specification quality or certify specifications against curated formal references, while [Bursuc et al. \[2025\]](https://arxiv.org/abs/2509.22908) measures synthesis success against supplied contracts. These approaches reveal important failures in verifiable code generation, yet they do not determine whether proof-based optimization progressively separates verifier acceptance from intended behavior when the model can generate or weaken the rewarded specification.

Consistency and test-based methods provide further defenses without resolving this longitudinal measurement problem. [Sun et al. \[2023\]](https://arxiv.org/abs/2310.17807) cross-checks code, annotations, and natural-language descriptions, whereas [Endres et al. \[2023\]](https://arxiv.org/abs/2310.01831) evaluates executable postconditions using hidden tests and mutation-based criteria. [Lahiri \[2024\]](https://arxiv.org/abs/2406.09757) similarly assesses specification correctness and completeness through symbolic testing. None jointly estimates the difference between verification and independent behavioral correctness across checkpoints, reward regimes, and specification sources. Doing so requires paired outcomes for identical candidates while preserving the independence of held-out tests; separation of checkpoint, reward, and specification-source effects despite repeated and correlated observations; and mechanism-aware analysis in which overlapping attacks remain identifiable. In particular, empty precondition domains and implementation-independent vacuity require semantic checks beyond the verifier’s binary decision and must not be counted as successful proofs.

The central insight is to treat specification adequacy as a paired, reward-isolated longitudinal quantity rather than as an attribute inferred from verifier acceptance alone. An escrowed evaluation will apply human-audited executable oracles and property-based tests, fixed before training and run with secret seeds, to every candidate for which verifier acceptance is recorded. The resulting paired contrast between verification and behavioral correctness will estimate the specification-adequacy gap with task-stratified, dependence-preserving uncertainty intervals. A randomized factorial design crossing reward type with fixed or generated specifications will trace this gap across checkpoints using a joint hierarchical model of verifier and behavioral outcomes. The same evaluation will support a multi-label semantic-intervention audit that checks precondition satisfiability, tests postconditions under counterfactual outputs and modified state, and detects input exclusion or contract weakening without forcing co-occurring mechanisms into a single category.

The evaluation will use the Paired Checkpoint Evaluation Panel, Dependence-Preserving Delta Simulation Bank, Blinded Intent-Violation Mutation Suite, Crossed-Mechanism Calibration Corpus, and Vacuity-Empty-Domain Challenge Set. Comparisons will include an unpaired gap interval, reward-visible tests, trusted fixed specifications, binary-verifier and structured-verification-condition proof-only rewards, a mutually exclusive syntactic classifier, and a verifier-output-only classifier. Experiments on the specified Dafny single-function corpus and model will assess estimator calibration, evaluator sensitivity, training-trajectory differences, the effect of hybrid proof-plus-execution rewards, and the accuracy of mechanism decomposition.

## Contributions

- We propose a paired estimator of the specification-adequacy gap that preserves candidate-level dependence and isolates behavioral evaluation from the training reward.

- We introduce a randomized longitudinal design that identifies how reward type and specification source affect the gap while accounting for repeated tasks, training seeds, and unequal initial verification rates.

- We develop a multi-label semantic-intervention audit that distinguishes empty input domains, implementation-independent vacuity, and other overlapping specification-hacking mechanisms.

- We establish an evaluation plan that tests uncertainty calibration, hidden behavioral sensitivity, trajectory discrimination, and mechanism-label accuracy against matched statistical and diagnostic baselines.

## Problem Definition

## Formal Problem Definition

Let \(\mathcal{C}\) be a corpus of Dafny single-function tasks, where each task \(c\in\mathcal{C}\) specifies a natural-language intent and an independently authored held-out behavioral test suite \(T_c\). The tests in \(T_c\) are never exposed to the reinforcement-learning reward channel. Training uses a \(0.6\)B-parameter model and existing prover infrastructure.

Let \(\mathcal{K}\) denote the ordered set of training checkpoints, \(\mathcal{R}=\{\text{binary},\text{structured},\text{hybrid}\}\) the reward arms, and \(\mathcal{S}=\{\text{fixed},\text{generated}\}\) the specification sources. Fixed specifications are trusted and remain unchanged during training; generated specifications may be produced or modified by the model. Let \(\mathcal{M}\) be the set of separately labeled specification-hacking mechanisms represented by the adversarial contracts.

Each observed solution is a record
\[
x_i=(c_i,k_i,r_i,s_i,m_i,P_i,f_i),
\]
where \(c_i\in\mathcal{C}\) is the task, \(k_i\in\mathcal{K}\) is the checkpoint, \(r_i\in\mathcal{R}\) is the reward arm, \(s_i\in\mathcal{S}\) is the specification source, \(m_i\in\mathcal{M}\) is the mechanism label, \(P_i\) is the effective Dafny contract, and \(f_i\) is the generated implementation. For each \(x_i\), define:

\[
A_i=\mathbf{1}\{\text{the existing Dafny verifier accepts }(P_i,f_i)\},
\]

\[
D_i=\mathbf{1}\{\operatorname{Dom}(P_i)\neq\varnothing\},
\]

\[
Q_i=\mathbf{1}\{\text{the proof is classified as vacuous}\},
\]

and

\[
B_i=\mathbf{1}\{f_i\text{ satisfies every test in }T_{c_i}\},\qquad T_{c_i}\text{ drawn over the trusted intended domain of }c_i.
\]

Here, \(\operatorname{Dom}(P_i)\) is the set of inputs satisfying the preconditions of \(P_i\), and \(B_i\) is evaluated over the **trusted intended domain** supplied with the task, not over \(\operatorname{Dom}(P_i)\) — otherwise a model could raise \(B_i\) by shrinking its own precondition.

**The primary estimand uses raw verifier acceptance.** It is tempting to define an adequacy-aware indicator \(V_i=A_iD_i(1-Q_i)\), which zeroes out acceptances obtained over an empty domain or through a vacuous proof, and to estimate \(\delta\) from that. **This would be self-defeating, and we do not do it.** Consider precisely the case the paper exists to measure: a program the verifier accepts through a vacuous contract. There \(A_i=1\) and \(B_i=0\), but \(V_i=0\), so the contribution to \(V_i-B_i\) is **zero**. An adequacy-aware numerator subtracts exactly the misleading verification successes we are trying to count, and the estimator would report the smallest gap precisely where the pathology is worst. We therefore define the primary specification-adequacy gap as

\[
\delta = \Pr(A_i = 1) - \Pr(B_i = 1),
\]

raw verifier acceptance minus independent behavioral correctness over the trusted intended domain.

The vacuity and domain-nonemptiness flags are retained, but as a **secondary decomposition of \(\delta\) rather than a filter applied before it**. Because \(A_i \ge V_i\) pointwise, the raw gap decomposes as

\[
\delta = \underbrace{\Pr(V_i=1)-\Pr(B_i=1)}_{\text{gap among adequately-specified acceptances}} \; + \; \underbrace{\Pr(A_i=1)-\Pr(V_i=1)}_{\text{acceptances explained by empty domain or vacuity}},
\]

so the adequacy-aware quantity survives as one component and the mechanism flags earn their place by attributing the second. Reporting the decomposition is the point: a \(\delta\) driven mostly by the second term is a specification-hacking story, while one driven by the first is a genuine implementation-correctness story, and the two call for different responses. Note that \(B_i\) is deliberately **not** conditioned on \(D_i\) and does not consult the candidate's own
contract. \(T_{c_i}\) is fixed with the task and drawn over the trusted intended domain, so an empty or
narrowed candidate precondition cannot make \(B_i\) vacuously true, and a candidate that fails intended
behaviour scores \(B_i=0\) whether or not its own contract admits the failing inputs. Any definition that
restricted \(T_{c_i}\) to inputs "applicable" under \(P_i\) would hand the model the same lever on the
behavioral side that it already has on the verification side.

Let a stratum be any tuple
\[
g=(r,s,m,q,d)\in
\mathcal{R}\times\mathcal{S}\times\mathcal{M}\times\{0,1\}\times\{0,1\}.
\]
For checkpoint \(k\), let
\[
I_{k,g}=\{i:k_i=k,\ r_i=r,\ s_i=s,\ m_i=m,\ Q_i=q,\ D_i=d\}
\]
and \(n_{k,g}=|I_{k,g}|\). For every nonempty stratum, estimate the formal verification rate and independent behavioral correctness rate as
\[
\widehat{p}^{\,A}_{k,g}
=\frac{1}{n_{k,g}}\sum_{i\in I_{k,g}}A_i,
\qquad
\widehat{p}^{\,V}_{k,g}
=\frac{1}{n_{k,g}}\sum_{i\in I_{k,g}}V_i,
\qquad
\widehat{p}^{\,B}_{k,g}
=\frac{1}{n_{k,g}}\sum_{i\in I_{k,g}}B_i,
\]
where \(\widehat{p}^{\,A}\) is raw acceptance and \(\widehat{p}^{\,V}\) the adequacy-aware rate. The primary
specification-adequacy-gap estimator is
\[
\widehat{\delta}_{k,g}
=\widehat{p}^{\,A}_{k,g}-\widehat{p}^{\,B}_{k,g},
\]
reported together with its two components \(\widehat{p}^{\,V}_{k,g}-\widehat{p}^{\,B}_{k,g}\) and
\(\widehat{p}^{\,A}_{k,g}-\widehat{p}^{\,V}_{k,g}\).
The required output is the checkpoint-ordered trajectory
\[
\widehat{\Delta}_g
=\bigl(\widehat{\delta}_{k,g}\bigr)_{k\in\mathcal{K}:n_{k,g}>0},
\]
together with the corresponding component rates and sample counts. Marginal trajectories may be obtained by aggregating records over selected coordinates of \(g\), while retaining mechanism-specific, reward-specific, specification-source, vacuity, and domain-nonemptiness decompositions.

The empirical objective is to characterize changes in \(\widehat{\delta}_{k,g}\) over training and compare these trajectories across reward arms and specification sources. The planned comparisons will assess whether the gap widens under generated specifications, remains controlled under trusted fixed specifications, and is smaller under the hybrid proof-plus-execution reward than under binary-verifier or structured verification-condition rewards. All comparisons are constrained to the observed Dafny corpus, the specified model scale, reward-isolated held-out tests, and existing prover infrastructure.

## Challenges

Reliable estimation is difficult because \(A_i\) and \(B_i\) measure different properties: \(A_i\) establishes consistency between \(P_i\) and \(f_i\), whereas \(B_i\) evaluates behavior against independently encoded intent. When \(s_i=\text{generated}\), the model can alter \(P_i\), changing \(\operatorname{Dom}(P_i)\) or making verification vacuous without improving \(f_i\); consequently, \(D_i\) and \(Q_i\) must be detected separately before computing \(V_i\). Reward isolation is also essential because exposure of \(T_{c_i}\) would couple \(B_i\) to the optimization signal and invalidate \(\widehat{\delta}_{k,g}\) as an independent adequacy estimate. Finally, decomposition over \((r,s,m,q,d)\) creates heterogeneous strata whose trajectories may reflect different planted mechanisms rather than a common effect, so labels cannot be pooled indiscriminately. These difficulties must be addressed without changing the prover, model scale, or corpus, limiting the available evidence to checkpointed outcomes and requiring comparisons to distinguish genuine behavioral improvement from reward-specific increases in verifier acceptance.

## Method Overview

The framework accepts candidate programs and their specifications from multiple training checkpoints and produces three linked outputs: an independently estimated gap between verifier acceptance and behavioral correctness, a longitudinal account of how this gap changes across training conditions, and a multi-label decomposition of the mechanisms underlying misleading verification successes. Each candidate is evaluated by both the rewarded verifier and an escrowed behavioral evaluation that remains inaccessible during training, enabling direct comparison of verification and behavior on the same samples.

These paired outcomes feed a randomized longitudinal analysis spanning reward designs and specification sources. The resulting gap trajectories are subsequently connected to semantic audits, which determine whether verifier–behavior disagreements arise from empty precondition domains, vacuous postconditions, input exclusion, postcondition weakening, or overlapping mechanisms. This data flow preserves behavioral-test independence while supporting both aggregate comparisons and mechanism-level attribution.

The independent adequacy-gap estimation module uses human-audited executable oracles and property-based tests fixed before training and executed with secret seeds. It estimates the difference between verifier and behavioral outcomes for identical candidates, addressing the difficulty of separating genuine behavioral improvement from increased verifier acceptance while preserving pairing, task structure, and uncertainty.

The controlled training-trajectory comparison module evaluates checkpoints from a factorial experiment crossing binary-verifier, structured verification-condition, and hybrid proof-plus-execution rewards with fixed trusted and generated specifications. A joint hierarchical model of paired outcomes will separate checkpoint, reward, and specification-source effects while accounting for repeated observations, task and seed variation, and unequal initial verification rates; this analysis will test whether generated specifications widen the adequacy gap and whether hybrid rewards constrain that growth without substantially reducing verification success.

The failure-mechanism outcome decomposition module applies a multi-label semantic-intervention audit to every evaluated candidate. Independent checks of precondition satisfiability, postcondition vacuity, intended-input coverage, mutant acceptance, and clause-level influence are designed to distinguish empty domains from implementation-independent vacuity and other forms of specification manipulation, even when several failures coexist. Calibration on blinded examples containing isolated and crossed mechanisms will assess whether these labels remain identifiable beyond what binary verifier outcomes or mutually exclusive syntactic classifications can reveal.

## Methodology

## Independent Adequacy-Gap Estimation

Verifier acceptance and behavioral correctness must be measured on the same candidate programs without allowing the behavioral tests to influence training. Their difference must also be estimated in a manner that preserves sample pairing, task heterogeneity, and uncertainty arising from hidden test generation.

The central design choice is to pair verifier and behavioral outcomes for every candidate. This pairing removes between-candidate variation from the contrast, while escrowed, never-rewarded behavioral tests remain independent of the optimization signal and therefore provide an external measure of intended behavior.

Before training, we will construct an escrowed evaluation primitive comprising human-audited executable oracles and property-based test generators. The oracles and generators will be fixed prior to optimization, excluded from all reward computation, and executed with secret random seeds. Each sampled candidate will receive a raw verifier acceptance \(A\), the derived adequacy-aware indicator \(V\), and a binary behavioral outcome \(B\) from the same evaluation instance. The candidate-level adequacy gap is therefore \(A-B\) — raw acceptance, per the problem definition — with verifier-only success contributing \(1\), behavioral-only success contributing \(-1\), and agreement contributing \(0\); \(V-B\) and \(A-V\) are recorded on the same pairs as its decomposition, never as the primary gap.

The aggregate gap, \(\delta\), will be estimated as a task-stratified weighted mean of the paired differences \(A_i-B_i\) — raw acceptance, not the adequacy-aware \(V_i\), for the reason given in the problem definition — with \(V_i-B_i\) and \(A_i-V_i\) computed on the same pairs to furnish the decomposition. Stratification prevents tasks with different sample counts from contributing implicitly in proportion to their evaluation frequency, while weighting follows the task composition of the evaluation design. Uncertainty intervals will be computed using a nested bootstrap over tasks and hidden test seeds. Resampling the paired \((A,B)\) observations jointly will retain their within-candidate dependence; nesting test-seed resampling within task resampling will additionally represent variability from both task selection and property-based test generation.

## Controlled Training-Trajectory Comparison

Changes in the adequacy gap must be attributed separately to training progress, reward construction, and specification source despite repeated evaluation of related tasks and potentially unequal initial verification rates. Direct comparison of raw verifier acceptance across conditions would confound these effects.

A randomized factorial design isolates reward and specification-source effects, while joint longitudinal modeling retains the dependence between verifier and behavioral outcomes. Baseline-centered contrasts further separate changes induced by training from differences already present at initialization.

We will conduct a randomized \(3\times2\) factorial experiment. The reward factor will comprise binary-verifier, structured verification-condition, and hybrid proof-plus-execution rewards. The specification factor will distinguish fixed, trusted specifications from generated specifications. Conditions will use common initialization distributions and independent training seeds, limiting systematic variation to the assigned reward and specification factors.

Each run will be evaluated at eleven equally spaced checkpoints using the escrowed paired evaluation primitive. Evaluation will produce one of four joint states for every candidate: verifier and behavioral failure, behavioral success without verifier acceptance, verifier acceptance without behavioral success, or joint success. Modeling these states directly preserves the covariance between \(A\) and \(B\), including the acceptance-only outcome that contributes most directly to a positive adequacy gap.

The longitudinal analysis will use a hierarchical four-state model with checkpoint splines, full interactions between reward arm and specification source, and random effects for tasks and training seeds. Checkpoint splines will permit nonlinear trajectories without imposing a constant rate of change. Full factorial interactions will allow the effect of each reward construction to vary with specification source rather than assuming that generated and trusted specifications respond identically. Task effects will account for repeated observations and heterogeneous difficulty, while seed effects will represent variation among independently trained runs.

Adequacy-gap trajectories will be derived from the fitted joint-state probabilities as
\[
\delta = \Pr(A=1)-\Pr(B=1),
\]
Comparisons will be reported as baseline-centered changes from the initial checkpoint. This centering absorbs condition-specific initial verification rates and makes the primary contrasts reflect divergence during training rather than pre-existing differences among arms.

## Multi-Label Semantic-Intervention Audit

Binary verifier output cannot distinguish empty precondition domains, vacuous postconditions, precondition exclusion, and postcondition weakening, particularly when several mechanisms occur simultaneously. Reliable attribution therefore requires semantic checks that remain identifiable under overlapping failures.

The audit assigns each mechanism an independent observable signature through semantic predicates and counterfactual interventions. Retaining all triggered labels avoids forcing compound failures into a mutually exclusive taxonomy and separates implementation-independent acceptance from genuine behavioral correctness.

For each evaluated candidate, an independent solver will analyze the generated precondition. An empty domain will require a replayable unsatisfiability certificate; a nonempty domain will require a witness whose satisfaction of the precondition can be independently validated. Solver timeouts or inconclusive outputs will be recorded as unknown rather than treated as evidence for either emptiness or nonemptiness.

Vacuity will be assessed through a counterfactual state intervention. Candidate outputs and all modified state will be replaced with unconstrained values, after which the postcondition will be checked over the hidden intended-domain predicate supplied by the escrowed evaluation. If acceptance persists after implementation-dependent state has been removed, the audit can identify that the specification does not meaningfully constrain the produced behavior. This check is distinct from domain nonemptiness: a precondition may admit valid inputs while the postcondition remains independent of the implementation.

Precondition exclusion will be assessed by measuring whether intended inputs satisfy the candidate precondition. Coverage over the hidden intended-input set will expose specifications that obtain verifier acceptance by excluding behaviorally relevant inputs. Postcondition weakening will be examined through acceptance of oracle-failing program mutations and one-clause ablations of the specification. Mutant acceptance tests whether incorrect implementations remain admissible, while clause ablations identify whether particular constraints materially affect verification.

All applicable mechanism labels will be retained for each candidate, including concurrent empty-domain, vacuity, exclusion, or weakening signals when supported by their respective checks. The audit will be calibrated on blinded examples containing both isolated and crossed planted mechanisms, enabling evaluation of whether individual labels and complete label sets remain recoverable when failures overlap.

## Experiments

## Experimental Setup

The evaluation will pair raw verifier acceptance \(A\) with never-rewarded behavioral judgments \(B\) on the same held-out tasks. The primary adequacy gap will be estimated as \(\delta=\operatorname{mean}(A-B)\), with the adequacy-aware component \(\operatorname{mean}(V-B)\) and the mechanism term \(\operatorname{mean}(A-V)\) reported alongside it as the decomposition. Pairing will be preserved throughout resampling and checkpoint analysis, with clustering by task and seed where applicable. The independent behavioral evaluator \(E\) will be frozen before evaluation and isolated from reward-visible outcomes.

Five complementary datasets will support the evaluation. The Paired Checkpoint Evaluation Panel will contain common held-out tasks evaluated across seeds, reward arms, specification sources, and checkpoints. It is selected to test dependence-aware estimation of \(\delta\) and the reproducibility of checkpoint trajectories. The Dependence-Preserving Delta Simulation Bank will resample observed task sizes and \(A\)-\(B\) dependence while introducing known adequacy gaps; it enables controlled coverage analysis under conditions in which unpaired estimation may mischaracterize uncertainty. The Blinded Intent-Violation Mutation Suite will comprise human-validated program mutations that violate intended behavior but may pass reward-visible tests, directly testing evaluator independence and sensitivity. The Crossed-Mechanism Calibration Corpus will balance programs with no mechanism, individual mechanisms, and co-occurring mechanisms, thereby supporting non-circular evaluation of multi-label auditing. Finally, the Vacuity-Empty-Domain Challenge Set will use a four-way design—empty-domain only, vacuity only, both, and neither—to distinguish two potentially conflated failure modes under controlled label prevalence.

Six baselines will be considered. Unpaired delta intervals provide a same-budget comparison for determining whether preservation of \(A\)-\(B\) pairing improves precision. Reward-visible tests serve as a leakage-prone comparator for the independent behavioral evaluator. Trusted fixed specifications provide a controlled specification-source baseline against which widening under generated specifications can be distinguished from general training drift. Binary-verifier and structured-verification-condition proof-only arms isolate the reward-signal contrasts needed to interpret the hybrid proof-plus-execution arm. A mutually exclusive syntactic classifier tests whether semantic multi-label auditing is necessary when mechanisms co-occur. A classifier restricted to rewarded-verifier output tests whether vacuity and empty-domain labels contain information beyond verifier pass/fail outcomes.

The principal metrics will include empirical interval coverage and width; paired adequacy gaps and checkpoint contrasts; verification and behavioral-correctness rates; mutation-detection sensitivity; and label-specific precision, recall, and F1. Mechanism-level evaluation will additionally report macro-F1, exact-label-set accuracy, co-occurrence errors, false-positive rates, and four-way confusion patterns. Uncertainty will be quantified using paired or clustered resampling, simultaneous confidence intervals for checkpoint analyses, and exact precision and recall bounds where specified.

The key experimental settings are preregistered by research question. Calibration will use 10,000 Monte Carlo replicates in each of 12 planted-gap and dependence cells. Mutation evaluation will use 500 independently adjudicated violations. Checkpoint experiments will use 20 paired seeds, 2,000 common held-out tasks, and 11 checkpoints. Multi-label calibration will use 2,400 programs, split into 800 calibration cases and 1,600 locked evaluation cases. The vacuity and empty-domain analysis will use 1,500 programs divided equally among the four crossed conditions. No additional model or decision-rule tuning will be performed after the corresponding evaluation rules are locked.

The evaluation addresses the following research questions:

1. **RQ1:** Does pairing yield calibrated and more precise uncertainty intervals for the adequacy gap under realistic verifier–behavior dependence?
2. **RQ2:** Does the independent behavioral evaluator detect intent violations that reward-visible tests systematically miss?
3. **RQ3:** Does the adequacy-gap trajectory distinguish widening under generated specifications from stability under trusted fixed specifications?
4. **RQ4:** Under generated specifications, does hybrid proof-plus-execution reward reduce the adequacy gap without materially reducing verification rate?
5. **RQ5:** Can multi-label auditing accurately distinguish individual and co-occurring hacking mechanisms?
6. **RQ6:** Can the audit separately identify empty precondition domains and vacuity beyond what verifier output alone reveals?

## RQ1: Calibration and Precision of Paired Adequacy-Gap Estimation

RQ1 tests whether preserving task-level pairing between verifier and behavioral judgments yields reliable and narrower uncertainty intervals for \(\delta\). The underlying challenge is to estimate disagreement between verification and intended behavior without treating dependent observations as independent.

For each of 12 cells crossing planted values of \(\delta\) with observed \(A\)-\(B\) dependence regimes, 10,000 Monte Carlo replicates will preserve the observed task-size vector, marginal rates, and dependence structure. Task-stratified paired-bootstrap intervals for \(\operatorname{mean}(A-B)\) will be compared with unpaired-bootstrap intervals using identical numbers of verifier and behavioral judgments. Removing the pairing constitutes the principal ablation. Coverage-equivalence tests and paired comparisons of interval-width ratios will assess calibration and precision.

A positive result would require every cell to attain empirical coverage between 90% and 98% for nominal 95% intervals, while the mean paired-to-unpaired width ratio does not exceed 0.85. Such an outcome would support the hypothesis that dependence-aware estimation preserves calibration while reducing uncertainty at a fixed evaluation budget.

The evaluation metrics are empirical coverage, mean and median interval width, paired-to-unpaired width ratio, Monte Carlo standard error, and failure rates stratified by task size and \(A\)-\(B\) dependence.

## RQ2: Sensitivity of the Independent Behavioral Evaluator

RQ2 examines whether the frozen behavioral evaluator detects intended-behavior violations that remain invisible to the tests used for reward. The plain-language challenge is to determine whether evaluation adds genuinely independent evidence rather than reproducing the training signal.

The Blinded Intent-Violation Mutation Suite will contain 500 independently adjudicated mutations balanced across task families and mutation mechanisms. Evaluator operators and adjudicators will be blinded to reward-visible outcomes, and \(E\) and the visible tests will receive equal evaluation budgets on every mutation. The primary baseline and ablation is replacement of the independent evaluator with reward-visible tests. Paired mutation outcomes will permit direct analysis of disagreements between the two detection procedures.

The expected outcome is a lower confidence bound of at least 0.90 for the evaluator’s detection rate and at least 0.20 for its paired detection advantage over reward-visible tests. This would support the hypothesis that a frozen, never-rewarded evaluator identifies substantial classes of intent violations omitted by the reward signal.

The evaluation metrics are mutation-level detection rate, paired detection difference, discordant-pair counts, and sensitivity stratified by task family and mutation mechanism.

## RQ3: Specification-Dependent Adequacy-Gap Trajectories

RQ3 tests whether adequacy gaps widen during proof-only training with generated specifications while remaining stable with trusted fixed specifications. The challenge is to separate specification-induced divergence from generic changes over training. The strongest published evidence against widening comes from the execution-reward setting: a preregistered GRPO contrast on MBPP (arXiv:2607.11022) found that rewarded-false-positive incidence does not grow during training — selection, not learned exploitation. RQ3 is therefore a genuine test, not a confirmation exercise: if that null transfers to the proof-rewarded setting, the widening hypothesis dies as specified in the falsification plan; if it does not transfer, the spec-authorship factor identifies the lever — a model-authored specification is an optimizable reward surface in a way a fixed execution suite is not.

Binary-verifier and structured-verification-condition proof-only arms will each be trained under generated and trusted fixed specifications using 20 paired seeds. At 11 preregistered checkpoints, every run will be evaluated on the same 2,000 held-out tasks with paired \(V\) and never-rewarded \(B\) judgments. Reward arm and specification source will be the only varied factors. A checkpoint model clustered by seed and task will estimate trajectories, followed by final-minus-initial contrasts. The specification-source comparison is the central ablation, while the two proof-only reward arms test whether the pattern generalizes across verifier representations.

The expected outcome is that, for both proof-only arms, generated-specification \(\delta\) increases by at least 0.08, exceeds the corresponding fixed-specification change by at least 0.05, and is accompanied by a fixed-specification change equivalent within \(\pm 0.03\). This pattern would support the hypothesis that widening is specifically associated with generated specifications rather than general training drift.

The evaluation metrics are paired \(\delta\) at each checkpoint, final-minus-initial change, generated-minus-fixed difference-in-change, verification rate, behavioral-correctness rate, and simultaneous confidence intervals.

## RQ4: Effect of Hybrid Reward on the Adequacy Gap

RQ4 evaluates whether adding execution-based feedback to proof reward reduces the adequacy gap under generated specifications without sacrificing verification performance. The practical challenge is to improve behavioral alignment while retaining the verifier success achieved by proof-only training.

Using 20 paired seeds, the hybrid proof-plus-execution arm will be compared with the binary-verifier and structured-verification-condition proof-only arms on the same 2,000 held-out tasks at each of 11 checkpoints. Initialization schedules, task sampling, evaluation tests, and compute budgets will be held fixed. Removing execution feedback to recover each proof-only arm provides the reward-signal ablations. Clustered bootstrap contrasts will repeat the data-dependent selection of the proof-only arm with the higher final verification rate, ensuring that uncertainty reflects this selection step.

A positive result would place the hybrid arm’s final \(\delta\) at least 0.05 below each proof-only arm while keeping its final verification-rate difference from the better proof-only arm within \([-0.03,0.03]\). This would support the hypothesis that execution feedback reduces verifier–behavior disagreement without a material loss in verification success.

The evaluation metrics are final paired-\(\delta\) contrasts, checkpoint-level \(\delta\) trajectories, final verification-rate difference, behavioral correctness, and seed-level confidence intervals.

## RQ5: Multi-Label Identification of Hacking Mechanisms

RQ5 investigates whether semantic multi-label auditing can identify individual and co-occurring hacking mechanisms without forcing each program into a single explanation. The challenge is that mutually exclusive labeling may conceal programs exhibiting several mechanisms simultaneously.

The Crossed-Mechanism Calibration Corpus will include 2,400 independently labeled programs balanced across eight preregistered strata spanning no mechanism, single mechanisms, and co-occurring mechanisms. Audit rules will be calibrated on 800 cases and locked before evaluation on the remaining 1,600. A mutually exclusive syntactic classifier will be trained on the same calibration cases and evaluated on the identical locked set. Independent semantic adjudication will exclude audit and reward outputs. The principal ablations are the restriction to mutually exclusive predictions and the substitution of syntactic features for the full semantic audit.

The expected outcome is a lower confidence bound of at least 0.85 for macro-F1 and 0.75 for exact-label-set accuracy, with paired improvements of at least 0.15 over the mutually exclusive syntactic classifier on both metrics. This would support the hypothesis that multi-label semantic analysis is necessary for faithfully representing co-occurring mechanisms.

The evaluation metrics are per-label precision, recall, and F1; macro-F1; exact-label-set accuracy; co-occurrence error rate; and paired differences between auditing methods.

## RQ6: Separation of Vacuity and Empty Precondition Domains

RQ6 tests whether the audit can separately recognize vacuity and empty precondition domains with high precision and recall. The challenge is to distinguish two failure modes that can produce similar verifier outcomes despite differing semantically.

Locked audit rules will be evaluated on 1,500 independently adjudicated programs, comprising 375 empty-domain-only cases, 375 vacuity-only cases, 375 cases exhibiting both mechanisms, and 375 cases exhibiting neither. The full audit and a classifier restricted to rewarded-verifier output will be applied to every case while program text, verifier execution, and label prevalence remain fixed. Restricting the classifier to verifier pass/fail output provides the principal information ablation. Exact precision and recall bounds and paired recall comparisons will be computed separately for both labels.

The expected outcome is that each label attains lower confidence bounds of at least 0.90 for recall and 0.95 for precision, while its recall advantage over verifier-output-only classification has a lower bound of at least 0.20. This would support the hypothesis that empty-domain and vacuity failures are independently detectable semantic phenomena whose distinction cannot be recovered reliably from rewarded-verifier output alone.

The evaluation metrics are label-specific precision, recall, and false-positive rate; paired recall advantage; exact joint-label accuracy; and confusion among empty-domain only, vacuity only, both, and neither.

## Related Work

Three families of prior work touch specification adequacy, and they differ in a way that is best
stated against the estimand δ = Pr(A=1) − Pr(B=1) — defined on **raw** verifier acceptance A, not
on the adequacy-aware V, for the reason given in the Formal Problem Definition — rather than by
enumeration. *Specification synthesis and intent alignment* work improves or cross-checks a
specification at a single point in time: it acts on the quality of P, one input to δ, but produces
no paired behavioral measurement, so δ is never formed. *Benchmarks for verifiable code generation* supply ingredients that approximate
both of δ's components, but they evaluate a fixed model against a fixed curated specification set and
typically without candidate-level pairing, so what they yield is a cross-sectional approximation for
a system that was never trained against the verifier; the training dependence that makes δ dangerous
is definitionally absent. *Reinforcement learning from verifiable
but imperfect rewards* creates the training dependence and reports the resulting pathology, but
measures only the verification side, so the divergence is observed indirectly — through the drop in
verified pass rate after task filtering — rather than estimated. No family produces a paired,
reward-isolated, checkpoint-indexed δ decomposed by reward construction, specification provenance,
and failure mechanism.

## Specification Synthesis and Intent Alignment

One line of work uses large language models to synthesize formal specifications and reconcile them with informal program intent. [Wen et al. \[2024\]](https://arxiv.org/abs/2404.00762) combine language-model generation with program decomposition, static analysis, and iterative verification, while [Mugnier et al. \[2025\]](https://doi.org/10.1145/3720499) generate assertions that unblock Dafny proofs using verifier diagnostics and structurally similar examples. [Endres et al. \[2023\]](https://arxiv.org/abs/2310.01831) evaluate executable postconditions derived from natural-language descriptions through correctness and discriminative-power metrics, whereas [Lahiri \[2024\]](https://arxiv.org/abs/2406.09757) uses symbolic tests and output mutations to assess specifications in verification-aware languages. [Sun et al. \[2023\]](https://arxiv.org/abs/2310.17807) instead check consistency among code, documentation, and formal annotations through a closed-loop combination of deductive verification and language-model reconstruction. Closest to our mechanism labels, [Misu et al. \[2026\]](https://arxiv.org/abs/2604.00280) (VeriAct) synthesize specifications judged on completeness as well as verifiability, and [Wang et al. \[2026\]](https://arxiv.org/abs/2607.21957) (KaPilot) screen candidate specifications through an explicit precheck-and-verify quality loop; together with the long-standing model-checking vacuity literature they establish that detecting vacuous or under-constrained specifications is prior art, and we claim no novelty for detection itself — only for using empty-domain and vacuity flags as an attributing decomposition of a longitudinally estimated δ. The shared limitation is that these static synthesis and consistency procedures do not characterize how proof-rewarded training may increase verifier acceptance while independently assessed behavioral correctness remains unchanged or deteriorates.

## Benchmarks for Verifiable Code Generation

A second line of work develops benchmarks for jointly generating implementations, specifications, and machine-checkable proofs. [Ye et al. \[2026\]](https://arxiv.org/abs/2505.23135v3) provide a modular Lean benchmark covering code, specification, and proof generation, and their reported 52.3% specification soundness-and-completeness rate for the strongest evaluated model quantifies how routinely a generated contract is itself defective. [Thakur et al. \[2025\]](https://arxiv.org/abs/2505.13938) evaluate generated specifications against hidden human-authored specifications before certifying corresponding implementations; their benchmark, in their own words, *avoids* “specifications that leak implementation logic or allow vacuous solutions,” achieving this by hand-writing all 161 specifications as non-computable Lean propositions rather than by screening a generated pool. That is the appropriate design choice for a static benchmark, and it is exactly why such a benchmark cannot answer the present question: vacuity is precluded by construction rather than measured under optimization pressure, so its prevalence in a reward-driven training run remains unobserved. [Chiosa et al. \[2026\]](https://arxiv.org/abs/2509.22908) broaden the evaluation setting across Dafny, Verus/Rust, and Lean using supplied formal specifications, formal verification, and checks intended to exclude trivial or nonconforming solutions — and their own audit finds those checks incomplete, reporting that “conditioned on vericoding success, roughly 9% of the specs were too weak.” The shared limitation is that benchmark-level verification success does not measure the training-dependent divergence between verifier acceptance and behavioral correctness when the rewarded specification can itself be generated or weakened.

## Reinforcement Learning from Verifiable but Imperfect Rewards

A third line of work studies reinforcement learning from automatically checkable outcomes and the risks of optimizing imperfect reward proxies. [Gao et al. \[2022\]](https://arxiv.org/abs/2210.10760) analyze how optimization against a learned reward model can degrade performance under a separate gold-standard model, and [Rafailov et al. \[2024\]](https://arxiv.org/abs/2406.02900) identify analogous overoptimization in direct alignment algorithms. Both study *learned* reward models, where the proxy is known to be approximate; the formal-verification setting is distinct precisely because the verifier is sound, so the failure is relocated from the reward model to the specification it is asked to check.

Within formal software verification, two studies document that relocation empirically. [Yan et al. \[2025\]](https://arxiv.org/abs/2507.16331) combine automated data curation, supervised fine-tuning, verifier-guided reinforcement learning, and policy regularization to generate annotated Dafny programs, and report that reward optimization produces trivially verifiable but semantically weak specifications. [Tan \[2026\]](https://arxiv.org/abs/2605.30914) reproduces the phenomenon under GRPO-style training, names it specification hacking, and quantifies its consequence through the discrepancy between the unfiltered verified reward and the post-filtering verified pass rate. Both treat the phenomenon as an obstacle to be removed by curating the task set. Neither estimates its magnitude as a function of training progress, reward construction, or specification provenance, and neither separates empty admissible input domains from implementation-independent vacuity — the two mechanisms most likely to be conflated, since both yield verifier acceptance without behavioral content. That measurement is the contribution of this work.

Outcome-based reinforcement learning over automatically checkable tasks more broadly, as in [Guo et al. \[2025\]](https://arxiv.org/abs/2501.12948), supplies the training paradigm this work analyzes but does not involve formal specifications, proof rewards, or intent-adequacy evaluation, and is cited here as background rather than as a problem-specific comparator.

## Conclusion

Reliable use of formal verification as a learning signal requires evidence that accepted programs satisfy intended behavior, because otherwise apparent training progress may reflect contract manipulation rather than software correctness. The proposed study treats specification adequacy as a longitudinal, paired measurement problem: verifier judgments and reward-isolated behavioral evidence are analyzed jointly across controlled reward and specification conditions, while semantic interventions expose the distinct and potentially co-occurring ways in which a proof can become uninformative. This integrated design should establish when verification rates are trustworthy indicators of progress, when their divergence from behavioral correctness widens during training, and whether incorporating execution evidence can control that divergence without materially weakening verification performance. Across the paired panel, simulation bank, blinded mutation suite, and mechanism-focused challenge sets, the planned comparisons are expected to yield calibrated uncertainty, reproducible trajectory contrasts, and interpretable failure attribution. Such evidence could guide benchmark design, reward selection, and claims about verified code generation. Future work should test whether the conclusions transfer beyond single-function Dafny programs and the studied model scale, and should develop scalable adequacy checks for multi-function programs and rich specifications that are not amenable to direct execution.

---

## Evidence provenance (working note — remove before submission)

Every figure quoted in this draft is tagged by verification status, because the surrounding research
program was assembled from deep-research briefs whose citation markers were not resolvable and whose
statistics turned out to contain at least four errors.

**Primary-source verified 2026-08-21** (checked against the paper text, not a summary):

- Yan et al., *Re:Form — Reducing Human **Annotations** in Scalable Formal Software Verification with
  RL in LLMs: A Preliminary Study on Dafny*, arXiv:2507.16331, **TMLR 05/2026**. The §3.3 sentence
  quoted in the introduction is verbatim. Caution: the paper never uses the phrase "specification
  hacking" or "reward hacking" — that term is attributable to Tan and to this paper, not to Re:Form,
  and the draft is worded accordingly.
- Tan, *Automating Formal Verification with Reinforcement Learning and Recursive Inference*, M.Eng.
  thesis, MIT EECS, arXiv:2605.30914. Both figures (2.2% → 58.1%; 9.7% → 31.1% post-filtering) are
  from the abstract and the thesis does use the term "specification hacking" explicitly.

**Also primary-source verified 2026-08-21 — with six corrections applied to this draft:**

1. **VERINA is not a preprint.** Ye, Yan, He, Kasriel, Yang, Song — **ICLR 2026 (Poster)**,
   arXiv:2505.23135. ⚠️ **Pin v3.** The **v1 abstract carries different numbers and a different
   model**: "OpenAI **o4-mini** … **61.4%** correct code, **51.0%** sound and complete
   specifications, and **3.6%** successful proofs." Anyone checking an unpinned link against v1 finds
   a mismatch. The v3 figures (o3; 72.6 / 52.3 / 4.9) and the "based on one trial per task" qualifier
   are confirmed verbatim, and the qualifier is now retained in our prose.
2. **CLEVER is NeurIPS 2025 Datasets & Benchmarks Track**, not a preprint. (OpenReview's
   auto-generated BibTeX says `year={2026}` — that is an OpenReview artifact; the year is 2025.)
   The word "vacuous" appears exactly **once** in the paper, in the abstract. Our earlier wording
   "*excludes* specifications that would permit vacuous solutions" implied a filtering step over a
   candidate pool; **there is none**. All 161 specifications are hand-written as non-computable Lean
   propositions, so vacuity is precluded by construction. Reworded to the authors' own "avoids."
3. **VeriCoding → Vericoding**, and **the first author changes with the venue.** arXiv v1 lists
   Bursuc first; the **TMLR 2026** camera-ready (published 2026-08-17) reorders to **Chiosa et al.**
   Do not mix the two. This draft now cites Chiosa et al. \[2026\]. Their self-reported 9% weak-spec
   rate has been added — it strengthens our motivation and it is their own number.
4. **Lahiri is FMCAD 2024**, not a preprint (DOI 10.34727/2024/isbn.978-3-85448-065-5_19). Note his
   mutations are **output-value mutations of tests**, not LLM-generated program mutants — the paper
   explicitly positions itself against the latter, so our wording "output mutations" is correct and
   must not drift.
5. **Endres et al. is FSE 2024** — *Proc. ACM Softw. Eng.* 1(FSE), 1889–1912, DOI 10.1145/3660791.
6. **Gao et al. is ICML 2023**, PMLR 202:10835–10866. **Rafailov et al. is NeurIPS 2024.**
   **Laurel is OOPSLA 2025** — *Proc. ACM Program. Lang.* 9(OOPSLA1), Article 134 — and note two
   metadata traps: arXiv and ACM disagree on author order (use ACM's: Mugnier, Anaya Gonzalez,
   Polikarpova, Jhala, Zhou), and Crossref renders the last author with given/family swapped as
   "Zhou Yuanyuan" — the correct name is **Yuanyuan Zhou**. Do not copy Crossref into the .bib.

**Corpus defect found in the source run.** The room's retrieval pulled two papers from unrelated
fields into its reference corpus — a particle-physics paper on hadron-ion collisions in Pythia and a
physical-chemistry paper on partial molar volumes. Neither reached the draft, but both must stay out
of the bibliography, and the entry credited to "(unknown authors)" is Gao, Schulman & Hilton.

## Revision log

Revised from the AutoDiscussion output of room `98e3ae6b`, which closed 6/6 with 5/6 clean and one
unresolved major. Changes:

1. **Added the missing problem-side evidence.** The generated draft argued the motivation entirely
   from benchmarks and never cited the two documented incidents, because the room was submitted
   without a `references` payload and so never saw the Tan thesis. Abstract, introduction and Related
   Work now carry it.
2. **Resolved the outstanding related_work major** — the critic objected that the section "reports
   paper and baseline counts without comparing how verifier-guided training, specification-quality
   evaluation, and static certification differ relative to the delta objective." Related Work now
   opens by contrasting the three families against δ directly.
3. **Fixed the CLEVER inconsistency** flagged as a minor: the benchmark *excludes* vacuity-permitting
   specifications, so the honest limitation is that vacuity is prevented by curation rather than
   measured under optimization pressure — not that vacuity is "not distinguished."
4. **Demoted DeepSeek-R1** from a problem-specific comparator to background, per the second minor;
   it involves no formal specifications or proof rewards.
5. **Repaired the introduction's citation formatting** — the generated text rendered citations as
   `Author et al.. Title.` with doubled periods and no identifiers, while Related Work used correct
   linked form. Unified on the linked form.
6. **Removed the placeholder** line "This section requires manual completion with proper citations."
7. **2026-08-23 pre-push scoop re-sweep addition (8th pass).** A fresh web audit found the closest
   measured cousin absent from the room's context: arXiv:2607.11022 ("When the Reward Suite Is
   Leaky", 2026-07-13), a preregistered GRPO contrast measuring rewarded-false-positive mass per
   checkpoint under execution-test rewards, whose headline null (no growth during training) is the
   strongest published evidence against RQ3's widening hypothesis. RQ3's setup now engages it
   explicitly rather than leaving it for a reviewer. Positioning consequence recorded in the seed
   ledger: the first-measurement claim is scoped to proof-rewarded, specification-mediated settings;
   vacuity *detection* is conceded as prior art (KaPilot, VeriAct, model-checking vacuity
   literature), with only its use as a δ-decomposition label claimed.

8. **2026-08-23 round-9 strict re-review (post round-7/8 edits).** One major, one moderate:
   - **Related Work stated the reversed estimand.** Its opening framed all three prior-work families
     "against the estimand δ = Pr(V=1) − Pr(B=1)" — the adequacy-aware form that round 2 reversed
     and that the Formal Problem Definition explicitly rejects, since gating on adequacy subtracts
     exactly the acceptances the paper exists to measure. The body defines δ = Pr(A=1) − Pr(B=1) in
     two places; Related Work was written before the reversal and never re-read. Now stated on raw
     acceptance A, with the reason cross-referenced.
   - **Vacuity-detection prior art was conceded only in working notes.** The round-8 audit conceded
     detection as prior art in the seed ledger and in this log, but the manuscript body — which is
     what survives once the working notes are stripped — cited none of it, while RQ6 claims
     precision/recall for separating vacuity from empty precondition domains. The concession now sits
     in Related Work, citing VeriAct (Misu et al., arXiv:2604.00280) and KaPilot (Wang et al.,
     arXiv:2607.21957), both verified against the arXiv API this pass, plus the model-checking
     vacuity literature. Novelty is claimed only for using the flags as an attributing decomposition
     of a longitudinally estimated δ.

9. **2026-08-23 round-10 (deer-flow academic-paper-review pass).** The round-9 estimand fix reached
   Related Work but not Method/Experiments: five passages still carried the reversed adequacy-aware
   form — the Methodology defined the *candidate-level* gap as \(V-B\) (§Independent Adequacy-Gap
   Estimation) one sentence before the aggregate correctly used \(A_i-B_i\); the four-state model
   motivated its states via "covariance between V and B"; and the Experimental Setup's simulation
   bank, unpaired-baseline, and RQ1-metrics sentences all said "\(V\)-\(B\) dependence/pairing"
   while RQ1's own procedure used \(A\)-\(B\). An implementer following the Methodology sentence
   could have rebuilt the rejected estimator. All five now state raw acceptance \(A\) as primary
   with \(V-B\)/\(A-V\) as decomposition only; the spec's D2 prose ("joint (V,B) distribution")
   was mirrored to (A,B) in the same pass. Found by `deerflow_review_2026-08-23.md` (W1).
