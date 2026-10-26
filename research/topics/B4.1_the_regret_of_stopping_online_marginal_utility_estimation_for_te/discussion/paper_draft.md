# The Regret of Stopping: Measuring Online Rules Against a Reconstructed Oracle in Test-Time Reasoning

> Assembled from the six confirmed stage outputs in `pipeline.md`, post-audit (`taste_audit.md`: 🟢), post-stage-review (`stage_review.md`: 2 REVISE findings fixed, folded in below). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets, not results.

## Abstract

Test-time reasoning lets a language model trade additional inference compute for a chance at a better answer, but every deployment of it hides an unresolved question: when should generation stop? We show that current stopping rules — confidence-based early exit, verifier-based trimming, self-consistency agreement thresholds — are validated only by end accuracy and token savings, never by how far they fall short of what the trajectory's own future would have told a rule that could see it. We turn this unobservable future into a measurable quantity: on mechanically verifiable reasoning tasks, we probe each trajectory at reasoning-transition checkpoints, verifier-label every probe, and reconstruct a per-instance oracle stopping point across a swept accuracy–compute exchange rate, certifying the reconstruction's own precision before trusting it. Every stopping rule's *regret* — the accuracy-minus-compute utility it forfeits relative to this oracle — is then measured, decomposed into stopping-too-early and stopping-too-late components, and tracked across task difficulty and exchange rate. A learned estimator that reads the running signal history is evaluated the same way, against both single-signal heuristics and a capacity-matched control that isolates genuine mid-trajectory value from pre-decoding difficulty prediction. We report how much regret today's stopping rules actually incur, where it concentrates, and whether any rule's ranking is stable enough to recommend independent of the deployer's own exchange rate.

## Introduction

Test-time reasoning lets a language model trade additional inference compute for a chance at a better answer, and that trade is now a routine deployment choice rather than a research curiosity: chain-of-thought reasoning, self-consistency sampling, and reflection-heavy decoding all let a system keep generating for as long as a budget allows. The practical question this raises is not whether more reasoning helps on average, but when, for a given instance, it stops helping — and every system that reasons at test time has to answer that question with some rule, whether that rule is a fixed token budget, a confidence threshold, or an agreement check across samples.

Yet no current stopping rule is measured against what the future of its own trajectory would have told it. The reason is a structural asymmetry that every deployment of test-time reasoning currently ignores: **the utility-optimal moment to stop is a functional of the trajectory's unobserved future, while every deployable stopping signal reads only the past.** A rule that exits on a confidence threshold, or on agreement across resampled answers, is validated today by reporting the accuracy and token cost it achieves — never by how far that outcome sits from the best a deployer could have achieved by knowing, after the fact, exactly when continuing stopped being worth its cost. This is not a cosmetic omission: a single reported operating point cannot tell a rule that is nearly optimal from one that leaves most of the achievable headroom on the table, and which rule looks better can flip entirely with the deployer's own accuracy-per-compute exchange rate — a laboratory with abundant compute and a metered API consumer can be handed the same accuracy/token-savings table and reasonably disagree about which rule to adopt, with nothing in that table telling them whether the disagreement is expected or an artifact of an unrepresentative comparison.

The nearest existing work approaches this gap from adjacent but distinct angles, and the two closest are DEER [DEER2607] and TrimR [TrimR2607]: both are training-free, checkpoint-based exit rules — DEER [DEER2607] exits on a single-trace confidence threshold at a detected reasoning-transition point, and TrimR [TrimR2607] exits when consecutive segments' answers stabilize — and both directly inspired the checkpoint architecture this paper's instrument reuses, but neither is ever scored against a reconstructed oracle, so neither can say how much of the achievable accuracy–compute frontier its rule actually recovers. CaTS [CaTS2607] comes closest to naming the underlying problem: its own motivation concedes that agreement-threshold criteria "are not direct estimates of correctness and may not transfer cleanly across tasks or models," but it responds by distilling agreement into a trained confidence head rather than quantifying the residual gap to an oracle. Best-of-Infinity [BestOfInfinity2607] characterizes a related but different quantity — the value of drawing more parallel samples for a majority vote — whose own reference point (the infinite-sample vote) can itself be wrong, rather than a per-instance, sequential-trace oracle. And Adaptive Thinking [AdaptiveThinking2607] raises a genuine rival explanation this paper has to confront directly: it predicts a query's expected self-consistency from a pre-decoding hidden state and allocates compute before generation even begins, raising the possibility that whatever a mid-trajectory rule appears to add is really just an implicit re-derivation of a difficulty estimate already available beforehand. A younger family of learned exit predictors — Thought Calibration [ThoughtCalib2505], which probes a model's hidden representations to decide when thinking can terminate, and TERMINATOR [TERMINATOR2603], which learns per-instance exit points from first-answer-arrival positions — shares the premise that the right stopping point is instance-specific and predictable, but each is validated the same way as DEER and TrimR: by the accuracy and tokens it achieves, never by its distance from the achievable frontier.

Turning this gap into a measurable quantity surfaces four distinct obstacles. The oracle stopping point is a functional of a trajectory's unobserved future, so any offline reconstruction of it — built from a finite number of probes — carries its own estimation noise that has to be measured before any rule's regret can be trusted as more than instrument noise. Every online signal available at a checkpoint is a proxy for correctness known to decouple from it in places that matter — confidence-style signals are documented to keep rising over training regardless of correctness in other model classes [Chen2023Close] — so a single aggregate regret number cannot distinguish a uniformly-a-little-off signal from one that is confidently wrong in a specific, concentrated way. The marginal utility of continuing is not fixed in sign — continuing can actively hurt, flipping a correct answer to an incorrect one through unproductive over-reasoning, a failure mode independently traced to a causal internal-bias mechanism [FirstImpression2607] and documented at the budget level as overthinking, with extended reasoning abandoning previously correct answers [MoreThinkingHurts2604] — so no single fixed threshold on any one signal can be optimal across tasks, difficulties, or positions in a trajectory. And the accuracy–compute exchange rate is a free parameter of whoever is evaluating a rule, not a property of the phenomenon itself, so a rule ranking computed at one exchange rate says nothing, on its own, about whether that ranking would survive a different, equally defensible choice.

Our approach turns each obstacle into one instrument with a specific, falsifiable role, rather than a single monolithic pipeline. A checkpoint-probing instrument reconstructs the oracle stopping point offline and certifies its own reconstruction noise by comparing oracles built from disjoint halves of the same probes, so every downstream regret number can be checked against how much of it is instrument noise before it is attributed to a rule. The same logged data is then replayed through every candidate stopping rule to decompose their regret into stopping-too-early and stopping-too-late mass, localizing exactly where each online signal loses its grip on correctness rather than reporting one number that conflates every failure mode. A learned estimator reads the running signal history — not a single checkpoint's snapshot — to track a marginal utility that can change sign within a trajectory, addressing the non-stationarity a fixed threshold cannot. The exchange rate itself is swept across a grid rather than fixed at one value, turning "is this ranking stable" from an assumption into a measured rank-agreement statistic. And because realized trajectory behavior can diverge from a pre-decoding difficulty estimate in both directions — an instance predicted hard can resolve quickly, one predicted easy can drift into unproductive continuation — a capacity-matched, pre-decoding-only control isolates whether mid-trajectory signals do any work a much cheaper static predictor could not already do.

We evaluate this design on tasks whose answers can be mechanically verified — grade-school and competition math, multiple-choice science QA, and executable code — across multiple model families, comparing stopping rules replayed on identical logged trajectories against the reconstructed oracle, a fixed-budget control, and the pre-decoding-only rival-explanation control described above.

In summary, we contribute:
- A checkpoint-probing instrument that reconstructs a per-instance oracle stopping point offline from a mechanically verifiable trajectory's own future, together with a certification procedure (split-half reconstruction) that measures the instrument's own noise floor before any regret claim is trusted.
- A regret-decomposition method that separates stopping-too-early from stopping-too-late mass and localizes exactly where each online stopping signal decouples from verifier-checked correctness, rather than reporting a single conflated regret number.
- A learned marginal-utility estimator that tracks a non-stationary, sign-changing continuation value from the running signal history, evaluated against single-signal heuristics and against a capacity-matched pre-decoding-only control that isolates genuine mid-trajectory value from pre-decoding difficulty prediction.
- An exchange-rate sweep that turns rule-ranking stability from an assumption into a measured quantity, reporting whether any recommendation about which stopping rule is best can be made independent of the deployer's own accuracy–compute trade-off.

## Problem Definition

**Formal setup.** Consider an instance x for a mechanically verifiable task, with verifier v(·) ∈ {0,1}. A reasoning trajectory for x is segmented into checkpoints k = 1, ..., K. At each checkpoint, a probe-estimated accuracy â_k ∈ [0,1] and a cumulative token cost c_k are available. Given an accuracy–compute exchange rate λ (accuracy points per unit of cost), define the utility of stopping at checkpoint k as U_λ(k) = â_k − λ·c_k. The oracle stopping checkpoint is t*(x, λ) = argmax_k U_λ(k) — the checkpoint a decision-maker who could see the whole trajectory's future would have chosen. A stopping rule r observes only signals available at or before its chosen checkpoint and stops at t_r(x); its regret is R_λ(r, x) = U_λ(t*) − U_λ(t_r) ≥ 0, reported as a mean over instances and, normalized, as a fraction of the gap between the oracle and never stopping early. The object of study is the distribution of R_λ(r, x) over instances, its dependence on task difficulty and on λ, and — critically — whether it exceeds the reconstruction's own noise floor before being attributed to the rule at all.

**Why this is hard.** The oracle t*(x, λ) is defined over a trajectory's counterfactual future, so any reconstruction of it from a finite number of probes carries estimation noise of its own; a regret value indistinguishable from that noise is not evidence a rule failed. Every signal available to a rule at checkpoint k — confidence, entropy, agreement across resampled probes — is a proxy for verifier-checked correctness known to decouple from it in specific, non-uniform ways, so reporting only mean regret conflates "uninformative everywhere" with "informative but wrong in a concentrated, identifiable way." The utility U_λ(k) is not monotone in k: because unproductive continuation can flip a correct answer to an incorrect one, the marginal utility U_λ(k+1) − U_λ(k) can be negative, so no fixed threshold on any single signal is guaranteed optimal across checkpoints, tasks, or difficulties. Finally, λ is a free parameter of the evaluator rather than of x or its trajectory, so any claim of the form "rule A has lower regret than rule B" is implicitly conditioned on the λ at which it was measured, and that conditioning has to be checked, not assumed away, before the claim can be treated as a general recommendation.

## Method Overview

At a conceptual level, the study is a single measurement pipeline with five cooperating parts, all operating on the same logged, checkpoint-segmented trajectories. A checkpoint-probing instrument turns an otherwise unobservable future into a certified, computable reference; a decomposition procedure turns the same logged data, replayed through every candidate rule, into a localized regret account rather than one aggregate number; a learned estimator turns a non-stationary, sign-changing marginal-utility signal into a trackable prediction; an exchange-rate sweep turns ranking stability from an assumption into a measured statistic; and a capacity-matched control turns "mid-trajectory signals matter" from an assertion into a test against the strongest available alternative explanation.

The **checkpoint-probing instrument** segments each trajectory at reasoning-transition markers, branches counterfactual probes at each checkpoint, verifier-labels them, and reconstructs the oracle t*(x, λ) across a λ grid — while a split-half reconstruction from disjoint probe subsets certifies how much of any downstream regret number is the instrument's own noise. The **decomposed regret attribution** replays every candidate stopping rule over the identical logged trajectories, computing each rule's regret and splitting it by the sign of (t_r − t*) into stop-too-early and stop-too-late mass, while measuring each signal's own per-checkpoint discrimination of correctness. The **learned history estimator** predicts a signed continuation gain from the running signal history — not a single checkpoint's snapshot — and stops once that predicted gain is non-positive. The **exchange-rate sweep** recomputes every rule's regret and ranking at each of several λ grid points and measures rank agreement across adjacent values, together with how the stop-too-early/stop-too-late split shifts with λ. The **pre-decoding control** trains a capacity-matched predictor restricted to features available before generation begins and compares it, at matched token expenditure, against the full history-based estimator — isolating whether mid-trajectory signals do any work a static, pre-decoding difficulty estimate could not already do.

## Methodology

### Checkpoint-Probing Instrument

**Challenge.** The oracle stopping point is a functional of a trajectory's unobserved future, so it cannot be read off directly from any online signal — and any reconstruction of it from a finite number of probes carries its own sampling noise, which has to be measured rather than assumed away before any downstream regret claim is meaningful.

**Insight.** Unobservability is a fact about decision time, not about the offline record: once a trajectory's future has been probed and verifier-labeled after the fact, the oracle becomes an ordinary, checkable statistic — and the same probing procedure that reconstructs it can also certify its own precision, by comparing oracles reconstructed from two disjoint halves of the same probes.

**Method.** Each trajectory is segmented at reasoning-transition checkpoints k = 1, ..., K. At each checkpoint, N counterfactual probes are branched to a trial answer and verifier-labeled, yielding â_k and the cumulative cost c_k. For each λ in a log-spaced grid, the oracle t*(x, λ) = argmax_k U_λ(k) is computed directly from these logged values. Independently reconstructing t* from two disjoint halves of the same N probes at each checkpoint yields a split-half noise floor: the disagreement between the two half-reconstructions bounds how much of any rule's measured regret could be attributable to the instrument itself rather than to the rule.

### Decomposed Regret Attribution

**Challenge.** A single aggregate regret number cannot distinguish an online signal that is uniformly weakly informative from one that is highly informative everywhere except a specific, concentrated failure region — and only the latter is actionable for understanding or fixing a rule.

**Insight.** Replaying every candidate rule over the identical logged trajectories holds everything except the rule itself constant, which is what makes it possible to attribute a difference in outcomes to the rule rather than to incidental variation across runs — and splitting regret by the sign of (t_r − t*) turns "when does this rule fail" into a located, quantified answer instead of an aggregate symptom.

**Method.** Each candidate rule in the bank (fixed-budget, confidence-threshold, entropy-threshold, self-consistency vote-share threshold, answer-stability) is replayed over the same logged checkpoints to determine its stopping index t_r(x) and resulting regret R_λ(r, x). Regret is partitioned into stop-too-early mass (instances with t_r < t*) and stop-too-late mass (t_r > t*). Each signal's per-checkpoint discrimination of verifier-checked correctness is separately measured via AUROC against the checkpoint's own verifier label.

### Learned History Estimator

**Challenge.** Because the marginal utility of continuing can change sign within a single trajectory — continuing sometimes helps, sometimes actively hurts — no fixed threshold applied to a single checkpoint's signal value can track it; the estimator needs to see how the signal is moving, not just where it currently sits.

**Insight.** A predictor conditioned on the trend of the signal history, rather than its instantaneous value, can represent a directional, sign-changing quantity that a single global threshold structurally cannot.

**Method.** At each checkpoint, a lightweight predictor (logistic regression or a shallow MLP) maps the running signal history — current and recent confidence, entropy, and vote-share readings, their short-window deltas, and cumulative cost — to a predicted signed continuation gain. The induced rule stops once this predicted gain is non-positive. The estimator is trained on one split of logged trajectories and evaluated under leave-one-benchmark-out and leave-one-model-out splits to test whether its learned mapping transfers rather than memorizing a specific benchmark or backbone.

### Exchange-Rate Sweep and Ranking Stability

**Challenge.** The accuracy–compute exchange rate λ is a free parameter chosen by whoever is evaluating a rule, not a property of the task or the trajectory — so a rule ranking computed at one λ value says nothing, by itself, about whether a different, equally defensible λ would produce the same ranking.

**Insight.** Ranking stability across λ is a distinct empirical question about the shape of the regret surface as a function of λ, answerable only by actually sweeping λ and measuring rank agreement — not by inspecting a single, however precisely measured, slice of it.

**Method.** Every rule's regret and resulting ranking are recomputed at each of several log-spaced λ grid points. Kendall's τ is computed between rule orderings at adjacent grid points, and the fraction of total regret attributable to stopping too late is tracked as a function of λ, testing whether the dominant failure mode shifts from premature stopping at low λ to overthinking at high λ.

### Pre-Decoding Control

**Challenge.** Task difficulty and mid-trajectory signal content are naturally correlated — harder instances also tend to produce noisier mid-trajectory readings — so a plain correlation between a rule's value and instance difficulty cannot show that the rule is doing anything beyond what a difficulty estimate computed before decoding even begins could already do.

**Insight.** Pre-decoding difficulty is a static, per-instance estimate fixed before generation starts, but realized trajectory behavior can diverge from it in both directions — a predicted-hard instance can resolve quickly, a predicted-easy one can drift into unproductive continuation — and only a signal that reads the trajectory as it actually unfolds can catch that divergence; a capacity-matched control is what turns this from an assumption into a falsifiable comparison.

**Method.** A predictor with the same capacity as the learned history estimator, but restricted to pre-decoding and first-checkpoint features only, is trained identically and evaluated at matched mean token expenditure against the full history-based estimator. The comparison isolates whether the full estimator's mid-trajectory signals contribute value beyond what the best static, pre-decoding-only predictor already captures.

## Experiments

### Experimental Setup

**Datasets.** GSM8K (test split, exact-match numeric verifier) — large, unambiguous grading, cheapest domain to pilot the instrument on. MATH-500 (expression-equivalence verifier) — harder, multi-step math; tests generalization beyond arithmetic-level difficulty. AIME 2024 + 2025 (integer-answer verifier, combined ~60 items) — competition-hard; reported descriptively only and excluded from hypothesis tests to avoid inflating false-discovery risk on a small sample, used to check the difficulty-regret relationship at the extreme tail. GPQA-Diamond (multiple-choice verifier) — tests generalization to a different verifier type and reasoning profile than math. LiveCodeBench (unit-test execution verifier; Stage-2 scale-up only) — tests generalization to a domain where reasoning-transition checkpoints look structurally different from prose-based math/QA traces.

**Corpus quality and contamination controls.** Because the released checkpoint-level trajectory corpus is itself a secondary contribution of this study, its construction is subject to explicit quality gates rather than assumed sound: a manual audit of 50 verifier decisions per benchmark checks the mechanical grader's own error rate, with any benchmark showing more than 2% grading errors requiring a fixed grader before that benchmark's pilot results are trusted. Each benchmark's known train/pretraining overlap status (where publicly documented) is reported alongside the released corpus, and any benchmark with disclosed contamination risk is flagged in the corpus metadata rather than silently pooled with uncontaminated benchmarks in aggregate statistics.

**Probe budget and instrument cost.** The instrument's pre-registered probe budget is N = 8 verifier-labeled probes per checkpoint — split 4/4 between the two half-reconstructions behind the RQ2 noise floor, with binomial noise on â_k of at most ±0.17 (one standard error) at N = 8 — plus an N = 32 re-probe on 100 instances to check that the N = 8 estimate is not itself the binding constraint. Trajectories carry roughly K ≈ 20 transition checkpoints, so probing multiplies generation cost by about K × N ≈ 160× naively; two pre-registered mitigations bound this: prefix-KV reuse across probes branched from the same checkpoint, and a pilot gate requiring that vote shares at N = 4 correlate above 0.95 with N = 8 before the scale-up commits to the larger budget. Probe tokens are instrument overhead and are excluded from the policy cost c_k. Under these mitigations the pilot (200 trajectories, ~32K short probes) is budgeted at roughly 10–25 A100-GPU-hours.

**Baselines** (sanity-check and rival-explanation comparators, not competitors to beat — this is a measurement study, and no research question here is framed as "our procedure beats baseline X"). Fixed-budget stopping (the best per-benchmark fixed checkpoint index or token budget, selected on a held-out development split) is the necessary "is adaptivity worth anything at all" control. The oracle t* is the upper bound every rule is measured against, by construction incurring zero regret. The prefix-only allocator — a capacity-matched predictor using only pre-decoding and first-checkpoint features, trained identically to the full history-based estimator and evaluated at matched mean token expenditure — rules out the specific rival explanation that any measured gain from mid-trajectory signals is really an implicit re-derivation of a difficulty estimate already available before decoding began.

**Metrics.** Mean regret R_λ(r) and normalized regret NR_λ(r) per rule per λ; per-checkpoint signal AUROC against the verifier label; stop-too-early / stop-too-late regret share; Kendall's τ of rule rankings across adjacent λ values; split-half oracle-reconstruction noise floor.

**Research questions:**
1. RQ1 — Is the reconstructed oracle non-trivial (does it actually recommend stopping before the trajectory's end)?
2. RQ2 — Is the oracle reconstruction precise enough, relative to its own noise floor, to license regret comparisons?
3. RQ3 — Do calibrated single-signal stopping rules incur regret that is both statistically real and larger than the instrument's noise floor?
4. RQ4 — Do any of the online signals discriminate verifier-checked correctness reliably above chance?
5. RQ5 — Does the self-consistency signal dominate confidence and entropy in mean regret?
6. RQ6 — Does a learned combination of the signal history reduce regret relative to the best single-signal rule, and does that gain transfer across benchmarks and models?
7. RQ7 — Does the learned estimator's residual regret gap to the oracle grow with task difficulty?
8. RQ8 — Is the ranking of stopping rules by regret stable across the accuracy–compute exchange rate?
9. RQ9 — Does the dominant regret failure mode shift from stopping too early to stopping too late as the exchange rate increases?
10. RQ10 — Does exploiting mid-trajectory signals add value beyond what a pre-decoding difficulty estimate alone already captures?
11. RQ11 — Is checkpoint discretization coarse enough to dominate the between-rule regret differences every other RQ above depends on?

**Placebo-first ordering (B0).** Per this study's own control structure, the fixed-budget sweep (B0) is evaluated *before* any of RQ3–RQ10 are scored, not merely reported alongside them: the pre-registered justification criterion requires the best adaptive heuristic to beat the best dev-selected fixed budget by at least 20% relative mean regret (Holm-corrected p < 0.05) at the median λ on at least 2 of the 3 pilot benchmarks. If B0 is not beaten by this margin, adaptivity itself has not been shown to be worth anything on these tasks, and the paper's framing reverts to the global pivot (Conclusion) rather than proceeding to score RQ3–RQ10 as if adaptivity were already established.

#### RQ1: Is the reconstructed oracle non-trivial?

**Setup.** At a moderate exchange rate (the λ grid's midpoint), compute the fraction of pilot instances (GSM8K, MATH-500, GPQA-Diamond; single backbone) for which t*(x, λ) falls strictly before the trajectory's final checkpoint K.

**Expected outcome.** The oracle recommends stopping before the trajectory's end on at least 20% of instances at the median λ.

**Falsification condition.** Refuted if the oracle recommends continuing to the final checkpoint on more than 80% of instances — the oracle would then be degenerate, and the entire regret framework would have nothing to measure on these tasks and this model.

**Hypothesis (plain language).** Stopping decisions are economically meaningful on these tasks: the achievable frontier genuinely lies before the end of the trajectory for a material share of instances, not only at its end.

**Metrics.** Fraction of instances with t* < K at the median λ.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Is the oracle reconstruction precise enough to license comparisons?

**Setup.** Independently reconstruct t*(x, λ) from two disjoint halves of the same per-checkpoint probes; compare the resulting split-half regret (the "self-regret" of the instrument) against the best heuristic rule's own measured regret at the median λ.

**Expected outcome.** The split-half noise floor is no more than one-third of the best heuristic rule's measured regret at the median λ.

**Falsification condition.** Refuted if the split-half noise floor equals or exceeds one-third of the best heuristic's measured regret — in that case, the instrument cannot reliably distinguish a rule's genuine regret from its own reconstruction noise, and either the probe count N must increase or all downstream regret claims must be qualified as inconclusive.

**Hypothesis (plain language).** The instrument is precise enough, relative to the effect sizes it is trying to measure, to license attributing regret to a rule rather than to sampling noise in the oracle's own construction.

**Metrics.** Split-half regret (noise floor); ratio to the best heuristic's measured regret.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Do calibrated single-signal rules incur real, non-noise regret?

**Setup.** Pilot stage: 2 backbones × 2 conditions (rule on vs. oracle) × the three pilot benchmarks × ~500 instances each (≥500 per benchmark where the test set allows). Scale-up: ≥3 model families × 5 benchmarks. Thresholds τ per rule calibrated on a held-out 20% development split; all tests on the disjoint 80% evaluation split. Two-sided Wilcoxon signed-rank test on per-instance regret, Holm–Bonferroni corrected across rule pairs and λ values, α = 0.05.

**Sample-size rationale.** ≥500 instances per benchmark (AIME excluded from hypothesis tests, reported descriptively) are sized to detect a standardized regret effect at conventional power against the split-half noise floor established in RQ2; an observed effect below that threshold in the pilot triggers a pre-committed sample enlargement in the scale-up rather than a null claim.

**Expected outcome.** Every calibrated single-signal rule has mean regret significantly greater than zero (normalized regret NR_λ ≥ 0.05) and exceeding *3×* the RQ2 split-half noise floor — not merely detectably above it — on at least two of the three pilot benchmarks and at least five of seven tested λ values.

**Falsification condition.** Refuted if any single-signal rule's regret fails to clear 3× the RQ2 noise floor across the majority of benchmarks and λ values — that rule would be effectively ε-certified as oracle-level once its regret cannot be cleanly distinguished from instrument noise at that margin, meaning the stopping problem is already solved for it on these tasks (feeding the F-G1 pivot wording in the Conclusion).

**Hypothesis (plain language).** Today's stopping heuristics leave real, measurable headroom on the table; none of them is already at the achievable frontier.

**Metrics.** Per-rule mean regret and 95% bootstrap CI; count of (benchmark, λ) cells clearing the noise floor.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Do online signals discriminate correctness above chance?

**Setup.** For each benchmark, compute each signal's (confidence, entropy, self-consistency vote share) per-checkpoint AUROC against the checkpoint's own verifier label, pooled across instances and checkpoints.

**Expected outcome.** At least one signal achieves AUROC ≥ 0.60 (bootstrap 95% CI lower bound > 0.55) on every benchmark.

**Falsification condition.** Refuted if every signal's AUROC is statistically indistinguishable from 0.5 on a benchmark — that would mean no logged online signal carries usable information about correctness on that benchmark, and any stopping rule built from these signals is a fixed-budget rule in disguise there.

**Hypothesis (plain language).** Online signals carry genuine, above-chance information about whether the current answer is already correct — the stopping problem is not hopeless, only imperfectly solved.

**Metrics.** Per-signal, per-benchmark AUROC with bootstrap CI.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Does self-consistency dominate confidence and entropy?

**Setup.** Pairwise comparison of mean regret between the self-consistency vote-share rule and each of the confidence-threshold and entropy-threshold rules, across all tested (backbone × benchmark × λ) cells, Holm–Bonferroni corrected.

**Expected outcome.** The self-consistency rule has significantly lower mean regret than both alternatives in at least 60% of tested cells, and is significantly worse in no more than 10%.

**Falsification condition.** Refuted if self-consistency is dominated by confidence or entropy in the majority of cells, or if no consistent ranking emerges (each signal wins in a similar share of cells) — either result would mean the folk intuition that sample agreement is the most reliable stopping signal does not hold in oracle-relative terms.

**Hypothesis (plain language).** Aggregating evidence across independent probe samples is a more reliable stopping signal than reading either single internal readout alone.

**Metrics.** Per-cell win/loss/tie counts and Holm-corrected pairwise significance.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Does a learned combination of signal history reduce regret, and does it transfer?

**Setup.** Train the learned history estimator on Stage-1 logged trajectories; evaluate mean normalized regret against the best single-signal rule under leave-one-benchmark-out (holding out each of 5 scale-up benchmarks in turn) and leave-one-model-out (holding out each of 3 model families in turn).

**Expected outcome.** The learned estimator reduces mean normalized regret relative to the best single-signal rule by at least 10% relative, with Holm-corrected significance, on at least 3 of 5 held-out benchmarks and at least 2 of 3 held-out models.

**Falsification condition.** Refuted if the learned estimator fails to significantly beat the best single-signal rule on a majority of held-out benchmarks or models — that would mean the signal history's trend information is redundant with the best single-signal threshold, and the binding constraint is the signals' shared blind spot, not how they are combined.

**Hypothesis (plain language).** Reading the trend of the signal history, not just its current value, captures real information a fixed threshold on any one signal misses — and that information generalizes across benchmarks and backbones, not just the data it was trained on.

**Metrics.** Normalized-regret reduction ratio (learned vs. best single signal) with bootstrap CI, per held-out split.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Does the learned estimator's residual gap to the oracle grow with difficulty?

**Setup.** Within each scale-up benchmark, bin instances into difficulty deciles by baseline pass rate; compute the learned estimator's normalized regret NR_λ at the median λ within each decile.

**Expected outcome.** The learned estimator's residual normalized regret at the median λ remains at least 0.10 on every benchmark (the oracle gap is not closed), and Spearman correlation between NR_λ and difficulty decile is at least 0.5 on at least 3 of 5 benchmarks.

**Falsification condition.** Refuted if the residual gap is flat or shrinking across difficulty deciles — that would mean harder instances are not, in fact, harder to estimate online, contradicting the mechanism this method is built around.

**Hypothesis (plain language).** Even the best estimator tested here does not close the gap to the oracle, and the remaining gap is concentrated exactly where it should be if it reflects genuine estimation difficulty: the hardest instances.

**Metrics.** Per-decile normalized regret; Spearman ρ(NR_λ, difficulty decile).

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ8: Is the ranking of stopping rules stable across the exchange rate?

**Setup.** Recompute every rule's ranking by mean regret at each of 7 log-spaced λ grid points spanning roughly 0.01–3 accuracy points per 1K tokens; compute Kendall's τ between rule orderings at each pair of adjacent grid points, pooled per model.

**Expected outcome.** Mean Kendall's τ between adjacent λ orderings is at least 0.6, with no adjacent pair falling below 0.3.

**Falsification condition.** Refuted if rule rankings reorder substantially across the λ grid (low or near-zero Kendall's τ between adjacent values) — in that case, no λ-independent statement of the form "rule X has lower regret" is defensible, and every reported comparison must be explicitly conditioned on the exchange rate at which it was measured.

**Hypothesis (plain language).** Although absolute regret values change with the exchange rate, which rule is best is a comparatively robust property, not an artifact of the one operating point being reported.

**Metrics.** Kendall's τ per adjacent λ pair, with bootstrap CI over instance resamples.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ9: Does the dominant failure mode shift from stopping early to stopping late as the exchange rate rises?

**Setup.** At each λ grid point, compute the fraction of total regret attributable to stopping too late (t_r > t*) for the best-performing heuristic rule and for the learned estimator.

**Expected outcome.** The stop-too-late regret share increases with λ (Spearman ρ ≥ 0.8 over the grid), shifting by at least 20 percentage points from the lowest to the highest tested λ.

**Falsification condition.** Refuted if the stop-too-early/stop-too-late mix does not shift with λ in the predicted direction — that would mean the overthinking-vs-underthinking failure mode is not governed by the exchange rate the way the utility formulation predicts.

**Hypothesis (plain language).** When compute is cheap relative to accuracy (low λ), rules tend to stop too early; when compute is expensive (high λ), the dominant failure becomes stopping too late — an economically legible pattern, not noise.

**Metrics.** Stop-too-late regret share per λ, per rule.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ10: Does exploiting mid-trajectory signals add value beyond pre-decoding difficulty prediction?

**Setup.** Train a capacity-matched predictor restricted to pre-decoding and first-checkpoint features only; compare its normalized regret against the full learned history estimator at matched mean token expenditure, across all scale-up benchmarks and models.

**Expected outcome.** The full history-based estimator beats the pre-decoding-only control by at least 10% relative normalized-regret reduction, with statistical significance, at matched token expenditure.

**Falsification condition.** Refuted if the pre-decoding-only control matches or beats the full estimator at the same token expenditure — that would mean the value of adaptive, mid-trajectory stopping is exhausted by pre-decoding difficulty prediction, and mid-trajectory signals add no measurable value beyond what is knowable before generation even starts.

**Hypothesis (plain language).** Reading a trajectory as it unfolds captures real, exploitable divergence from what could have been predicted before generation began — the online part of "online marginal-utility estimation" is doing genuine work, not just re-deriving a static estimate.

**Metrics.** Normalized-regret reduction (full estimator vs. pre-decoding-only control) at matched token expenditure, with bootstrap CI.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ11: Does checkpoint discretization dominate the measured between-rule regret differences?

**Setup.** Re-segment each pilot trajectory at 2× coarser checkpoint granularity (half as many transition markers retained) and recompute every rule's mean regret at the median λ; compare the resulting shift in mean regret per rule to the median between-rule regret gap measured at the original (finer) granularity.

**Expected outcome.** The 2×-coarser-checkpoint regret shift is less than 50% of the median between-rule regret gap at the same λ, for every rule in the bank.

**Falsification condition.** Refuted if coarsening checkpoints shifts any rule's mean regret by 50% or more of the between-rule gap — in that case, checkpoint granularity, not the rule's own signal quality, is the dominant driver of the regret differences reported in RQ3–RQ9, and every absolute regret number in this paper must be demoted from an oracle-relative claim to an instrument-relative one (comparisons only within a fixed granularity remain licensed).

**Hypothesis (plain language).** The checkpoint segmentation is fine enough that the regret differences attributed to a rule's own signal quality are not simply an artifact of how finely the trajectory happens to be sliced — this is the construct-validity precondition every other RQ in this paper depends on, not an independent finding in its own right.

**Metrics.** Per-rule regret shift under 2× coarsening; ratio to the median between-rule regret gap at the original granularity, with bootstrap CI.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, a natural extension is to test open-ended tasks with no mechanical verifier — precisely the deployment setting where stopping rules are most needed but where the oracle-reconstruction machinery this paper depends on cannot be directly applied, since there is no automatic correctness label to probe against. This is explicitly out of scope here because it would require a substitute for mechanical verifiability (e.g., a learned or human-judged reward model) with its own reliability questions, rather than a straightforward extension of the checkpoint-probing instrument above.

## Related Work

The two closest prior works are DEER [DEER2607] and TrimR [TrimR2607], and it is worth stating the delta plainly before surveying the wider landscape: both are training-free, checkpoint-based exit rules whose transition-detection architecture this paper's own checkpoint-probing instrument directly reuses — DEER [DEER2607] exits on a single-trace confidence threshold at a detected reasoning-transition point, and TrimR [TrimR2607] exits when consecutive segments' answers stabilize — but neither is ever scored against a reconstructed, per-instance oracle, so neither can report how much of the achievable accuracy–compute frontier its exit rule actually recovers. That is precisely the identifiability gap this paper is built to close.

**Training-free checkpoint-based stopping.** DEER [DEER2607] detects reasoning-transition points via discourse shifts and reflection tokens, induces a trial answer at each, and exits once confidence crosses a threshold; TrimR [TrimR2607] externally monitors an ongoing chain-of-thought with a lightweight verifier, exiting when consecutive segments converge to the same answer. Both establish that training-free, checkpoint-based intervention on an already-capable reasoning model is practical and effective by accuracy/token-savings measures, but neither reports a regret figure relative to any oracle, and neither certifies how much of its own reported gain reflects genuine adaptivity versus an artifact of the one operating point evaluated — the gap this paper's checkpoint-probing instrument and exchange-rate sweep are built to close.

**Learned exit predictors and optimal-stopping formulations.** Thought Calibration [ThoughtCalib2505] trains lightweight probes on a reasoning model's hidden representations to decide when novel reasoning has plateaued and thinking can terminate; TERMINATOR [TERMINATOR2603] learns per-instance exit points from the first arrival of the model's final answer; and concurrent work, OS-Pruner [OSPruner2607], formulates chain-of-thought pruning as an optimal-stopping problem over an explicit utility trading final-answer accuracy against generated length — the same utility object this paper's U_λ formalizes. All three share this paper's premise that the right stopping point is instance-specific, and OS-Pruner in particular shares its accuracy-per-cost utility; but each is a stopping *method*, validated by end accuracy and token savings against other methods. None reconstructs a per-instance oracle, certifies the reconstruction's own noise floor, decomposes any rule's regret by failure direction, or tests whether its advantage survives a change in the exchange rate — TERMINATOR's first-arrival label, in particular, is an accuracy-only target fixed at one implicit operating point rather than swept across exchange rates. This paper is the measurement study under which those methods could be scored, not a rival exit rule.

**Self-consistency and agreement-based adaptive sampling.** CaTS [CaTS2607] distills self-consistency agreement statistics into a trained, one-forward-pass confidence head that adaptively decides when to stop resampling, explicitly noting in its own motivation that agreement-based criteria "are not direct estimates of correctness and may not transfer cleanly across tasks or models"; Best-of-Infinity [BestOfInfinity2607] models repeated sampling as draws from an unknown categorical answer distribution and derives a Bayes-factor stopping rule for whether the current majority answer has converged to the population majority. Both quantify aspects of the *parallel* sampling dimension of test-time compute, but neither scores its criterion against a per-instance, sequential-trace oracle — CaTS [CaTS2607] names the proxy problem without measuring its size, and Best-of-Infinity [BestOfInfinity2607]'s own reference point (the infinite-sample vote) can itself be wrong, unlike this paper's mechanically-verified oracle.

**Offline budget calibration and risk control.** SAFER [SAFER2607] calibrates a single global sampling budget offline via conformal risk control, with an abstention option, over an exchangeable calibration set; Conformal Thinking [ConformalThinking2602] likewise frames budget setting as distribution-free risk control, pairing a confident-stop upper threshold with a preemptive lower threshold for instances unlikely to be solvable. These are genuinely different problems from the one studied here: both calibrate thresholds to a target risk level fixed in advance over an exchangeable calibration set — a condition per-step reasoning signals within a single trajectory do not satisfy — and neither measures any rule's regret against a reconstructed per-instance oracle or asks whether its guarantees survive a change in the accuracy–compute exchange rate. This paper's online framing is not subsumed by offline calibration; it addresses a setting offline calibration cannot reach.

**Learned and theoretical accounts of reasoning length.** JET [JET2607] trains a reasoning policy via reinforcement learning to stop once it has derived sufficient information, using a correctness-conditioned length reward; CoTLength [CoTLength2607] derives an error-accumulation model predicting an inverted-U relationship between chain length and accuracy, with an optimal length depending on task difficulty and model capability. JET [JET2607] changes what the underlying policy does rather than scoring a given policy's stopping behavior, and requires RL access unavailable for a fixed black-box model; CoTLength [CoTLength2607] explains *why* an optimal length exists at the population level but supplies no online, per-instance estimator of it and no evaluation of how far observable signals fall from realizing it — exactly the estimator and regret-decomposition machinery this paper contributes. When More Thinking Hurts [MoreThinkingHurts2604] documents the same inverted-U empirically at the budget level — marginal returns diminish and extended reasoning abandons previously correct answers — but, like CoTLength [CoTLength2607], stops at characterizing the phenomenon rather than measuring how far any deployable rule sits from the per-instance optimum.

**Pre-decoding compute allocation.** Adaptive Thinking [AdaptiveThinking2607] predicts a query's expected self-consistency from a pre-decoding hidden state and allocates reasoning compute before any token is generated; Snell et al. [Snell2024] show that compute-optimal allocation across strategies depends strongly on predicted prompt difficulty. Both establish that a substantial share of the value in adaptive test-time compute can be captured before generation even begins, which is precisely the rival explanation this paper's pre-decoding control is built to rule out or confirm: whether a mid-trajectory rule's apparent value is genuinely new information from the unfolding trajectory, or a re-derivation of what a static, pre-decoding difficulty estimate already knew.

## Conclusion

This work reframes test-time stopping from a question of accuracy and token savings into a question of *regret against an achievable frontier*, and shows that answering it requires more than a better heuristic — it requires an instrument that makes the frontier itself computable and certifies its own precision before anything is measured against it. The central methodological wager is that decay-style claims about "this rule is nearly optimal" or "this rule leaves headroom on the table" are only trustworthy once the oracle they are measured against has a stated, checked noise floor, and once the resulting regret has been decomposed by failure direction and tested for stability across the evaluator's own free parameter, the exchange rate. Whichever way the pilot and scale-up numbers land, the finding is decision-relevant: if today's heuristics cluster near the oracle, the stopping problem is closer to solved than the field assumes and further heuristic work has low expected value; if they leave substantial, non-noise regret — especially regret that reorders across exchange rates — every published "our stopping rule is better" claim in the literature is implicitly conditioned on an undisclosed operating point. Two limitations bound this claim from the outset and are natural next steps rather than afterthoughts: the study is scoped to mechanically verifiable tasks, leaving open-ended generation — where stopping rules may matter most but no automatic oracle exists — for future work that would need a substitute for mechanical verifiability with its own reliability question; and the reconstructed oracle's own precision, bounded by a finite probe count, may itself become the binding constraint at the hardest difficulty tier, where signals are noisiest and the split-half noise floor is largest, pointing toward adaptive or larger probe budgets specifically for high-difficulty instances as the next methodological target.

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → method → experiments → related work without forward references to undefined terms.
- **Terminology discipline** — "regret," "oracle stopping point," "exchange rate," "reconstruction noise floor," "regret decomposition" each defined at first use in Problem Definition, used consistently thereafter; no internal stage IDs (`sp_*`, `m_*`, `rq_*`) leaked into prose — checked directly against `pipeline.md`.
- **Notation with worked example** — the formal setup section defines (x, v, k, K, â_k, c_k, λ, U_λ, t*, R_λ) and the Problem Definition/Methodology sections consistently reuse this notation; no separate worked numeric example is included since no numbers exist yet (would require fabricating results).
- **RQ framing matches outcomes** — all 11 RQs are graded/quantitative (rates, effect sizes, agreement proportions), each answered in its own subsection with both an explicit falsifiable expected outcome and an explicit falsification condition, not a binary yes/no.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]` placeholders; only explicit `[placeholder — fill in after experiments are run]` markers in Results, per the drafting convention this is a pre-registered spec, not a report.
- **Artifact plan** — the checkpoint-probing harness and the released checkpoint-level trajectory corpus are the natural release artifacts, with a stated verifier-audit and contamination-disclosure gate (Experimental Setup); not yet built, so not claimed as available.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. Natural next steps: `research-paper-writing` for LaTeX conversion and prose polish once a target venue is chosen, or back into this pipeline if a stage needs revision (e.g., if the pilot's RQ1/RQ2 instrument-validity gates fail, that would mean revisiting Stage 5's checkpoint-probing instrument design before any of the substantive regret findings in RQ3–RQ10 can be trusted).
