# The Regret of Stopping: Hindsight-Oracle Evaluation of Test-Time Stopping Rules

## Abstract

Reasoning models decide, implicitly or explicitly, when to stop thinking. A growing zoo of test-time stopping rules — confidence thresholds, entropy monitors, answer-stability checks, learned stoppers — is evaluated almost exclusively through aggregate accuracy–token trade-offs, which compare rules to *each other* but cannot answer the deployer's question: how far is any rule from the *achievable* optimum, and where is the remaining utility lost? We introduce a hindsight-oracle regret framework for test-time stopping. For each logged reasoning trajectory, forced-answer probes at reasoning-transition checkpoints reconstruct the per-checkpoint accuracy–cost utility curve; the hindsight-optimal stopping point is treated not as ground truth but as an *uncertain object*, estimated with paired block-bootstrap utility bands and split-conformal confidence sets that account for the selection bias of maximizing over noisy checkpoint estimates. Every candidate rule, with thresholds calibrated per cost weight on a development split, is replayed causally on identical logged trajectories; its regret is decomposed additively — inside each calibrated oracle draw — into stop-too-early and stop-too-late components, reported as curves over an interpretable accuracy-per-token cost grid and stratified by task difficulty. A pilot study (one open reasoning model, three mechanically verifiable benchmarks, ~1,500 trajectories, ~2.4×10⁵ probe generations) measures the oracle gap of six calibrated rule families and a small learned marginal-utility estimator, answering directly whether the marginal benefit of continued thinking is online-estimable. All checkpoint-level logs are released as a replayable, leakage-controlled corpus: any future stopping rule becomes regret-scorable offline, without model access.

## 1. Introduction

Test-time scaling lets language models convert additional inference compute into accuracy by generating extended chains of thought [Snell et al., 2024; Guo et al., 2025]. But the marginal utility of continued thinking is not uniformly positive. Preferring shorter sampled chains can outperform longer ones [Hassid et al., 2025]; overthinking measurably harms agentic-task outcomes [Cuadron et al., 2025]; correct intermediate solutions are overwritten by subsequent reasoning [Song et al., 2025; Chen et al., 2024]; and a recent systematic study finds diminishing — and at high budgets negative — marginal returns to reasoning tokens, with the optimal thinking length varying by problem difficulty [Zhou et al., 2026]. Stopping, in short, is a consequential per-instance decision, and an efficient-reasoning subfield has grown up around it [Sui et al., 2025].

The stopping rules themselves exist in abundance: confidence-triggered early exit at reasoning transitions [Yang et al., 2025], log-probability-margin braking [Song et al., 2025], answer-stabilization monitors [Fu et al., 2024], and learned stoppers compared under calibrated risk [Dong et al., 2026]. What does not exist is an account of **how far any of them is from the achievable frontier**. Published rules are evaluated by end accuracy and token savings — a comparison of rules to each other. Cost-aware evaluations [Zhou et al., 2026; Dong et al., 2026] sharpen this to matched-cost or matched-risk comparisons, but the reference remains other rules or aggregate budget sweeps. A deployer choosing among stopping rules today cannot tell whether the remaining headroom is 2% or 40% of achievable utility — whether the problem is essentially solved or barely started — nor whether a given rule's losses come from stopping before value arrives or from paying for thinking that no longer helps.

Answering those questions requires a different estimand: **per-instance regret against a hindsight oracle**. For a logged trajectory with mechanically verifiable answers, forced-answer probes at each reasoning checkpoint reconstruct, in hindsight, the accuracy the model would have achieved by stopping there; combined with cumulative token cost under an exchange rate λ, this yields the trajectory's utility curve and its hindsight-optimal stopping point t*(λ). A rule's regret is the utility gap between its stop and t*, and the gap decomposes exactly into stop-too-early and stop-too-late mass — the quantified cost of underthinking and overthinking on that instance.

Two obstacles have kept this estimand unmeasured, and they structure our contribution. First, **the oracle is a construction, not ground truth**: per-checkpoint accuracy is estimated from finitely many probes, checkpoint estimates are correlated through the shared trajectory, and t* is an argmax over noisy quantities — a maximum that is biased upward, mechanically inflating every rule's measured regret. We therefore treat the oracle as an uncertain object: paired block-bootstrap resampling preserves cross-checkpoint dependence, simultaneous (sup-t) bands control uncertainty over the whole utility curve, and split-conformal calibration against disjoint higher-budget audit probes yields a confidence *set* of plausible oracle checkpoints rather than a brittle plug-in argmax. Regret and its early/late attribution are computed inside each calibrated oracle draw, so uncertainty in the reference propagates into every reported number. Second, **comparisons must be exactly paired and leakage-free**: all rules are replayed on identical logged trajectories through a causal interface that reveals only checkpoint-prefix observables, with verifier labels and oracle state sealed; the corpus is released so that future rules can be regret-scored offline.

The framework is an instrument, and we validate it as one — probe-intervention validity, oracle-set coverage against audit probes, decomposition exhaustiveness, replay reproducibility, and leakage canaries — but the paper's headline deliverables are empirical: regret curves over λ for six calibrated rule families on three benchmarks; the decomposition of each rule's loss into early/late mass by task-difficulty decile; a direct test of whether mid-trajectory observables carry enough signal to estimate marginal utility online, via per-checkpoint signal AUROC and a deliberately small learned estimator; and the replayable corpus itself.

**Contributions.**
1. **Estimand.** Per-instance, cost-indexed hindsight-oracle regret of test-time stopping rules, with an exact early/late decomposition — a quantity no published stopping evaluation reports (we verify this against the closest cost-aware evaluations [Zhou et al., 2026; Dong et al., 2026]).
2. **Instrument.** An uncertainty-calibrated oracle construction (paired block bootstrap, sup-t bands, conformal oracle sets) that converts "distance to the oracle" from a noise artifact into a measurable quantity with instrument error bars, plus a two-pronged validity protocol for the forced-answer probe intervention.
3. **Findings (pilot).** Calibrated regret curves, headroom estimates, and early/late/difficulty decompositions for six rule families and a learned marginal-utility estimator on one open reasoning model × three verifiable benchmarks.
4. **Artifact.** A checkpoint-level, verifier-labeled, causally-sealed replay corpus: any future stopping rule becomes regret-scorable on identical trajectories without GPU access.

## 2. Related Work

**Overthinking and the value of stopping.** Chen et al. [2024] document overthinking in o1-like models and define outcome/process efficiency metrics; Wang et al. [2025] study the complementary underthinking failure; Cuadron et al. [2025] show overthinking degrades agentic outcomes; Hassid et al. [2025] find shorter sampled chains preferable; Sui et al. [2025] survey the efficient-reasoning field. These works establish that continuation can carry negative marginal utility — the premise that makes stopping regret worth measuring — but none defines a per-instance oracle-relative regret or attributes losses to early versus late stopping.

**Test-time scaling and length control.** Snell et al. [2024] allocate test-time compute across strategies as a function of difficulty; s1's budget forcing [Muennighoff et al., 2025] and L1's length-controlled RL [Aggarwal & Welleck, 2025] impose token budgets; DeepSeek-R1 [Guo et al., 2025] trains long-form reasoning. These control *how much* thinking happens but evaluate by aggregate accuracy at budget, treating within-trajectory stopping as given.

**Online stopping rules — the measured objects.** DEER exits at reasoning transitions when trial-answer confidence is high [Yang et al., 2025]; ThinkBrake monitors the log-probability margin toward `</think>` at sentence boundaries and reports that hindsight-optimal sentence-boundary stopping would gain +8% accuracy while cutting 72% of thinking tokens — an oracle headroom number, but a plug-in aggregate, without uncertainty, per-instance resolution, cost-weight indexing, or decomposition [Song et al., 2025]. Certaindex monitors answer stabilization for early exit and scheduling [Fu et al., 2024]. Dong et al. [2026] compare learned versus scalar early exits under matched lost-correct risk with serving-aware cost accounting — the closest evaluation methodology to ours; their reference, however, is the competing rule set at matched risk, not a per-instance hindsight optimum, and their protocol yields no regret magnitude or early/late attribution. All of these rules are *inputs* to our framework: each becomes an arm scored on the common logs.

**Adaptive parallel sampling (boundary).** ESC [Li et al., 2024], Adaptive-Consistency [Aggarwal et al., 2023], CGES [Aghazadeh et al., 2025], RASC [Wan et al., 2024], and DeepConf [Fu et al., 2025] stop *sampling* — the parallel axis. We scope to the sequential axis (when to stop one chain); probe samples used for measurement form a fixed overlay charged identically to all rules (§4.1), so no rule receives free parallel compute. Verifier-effort allocation and cross-axis exchange rates (thinking vs. sampling vs. verifying) are likewise distinct problems; our λ machinery is consumable by, but does not address, either.

**Cost-aware evaluation — the critical adjacents.** Zhou et al. [2026] propose a cost-aware evaluation framework showing diminishing marginal utility and difficulty-dependent optimal thinking length. Their analysis is aggregate: budget-level accuracy–cost curves over populations. Our delta, stated precisely: (i) the formal object is *per-instance* regret against an *uncertainty-calibrated* hindsight optimum, which turns "rule A beats rule B" into "rule A leaves X% of achievable utility unclaimed, mostly by stopping too late on hard instances"; (ii) we measure the *online estimability* of marginal utility from partial-trajectory signals; (iii) we release a replayable corpus on which their stopping procedure — and any future one — can be regret-scored.

**Relation to optimal stopping theory.** The word "regret" imports expectations from online learning; ours is not that quantity. R_λ is *hindsight* (prophet-style, competitive-analysis) regret with respect to a fixed logged trajectory realization, not no-regret-learning regret accumulated over rounds. Classical optimal stopping and best-arm budget allocation are formal ancestors, but their machinery does not transfer directly: the payoff process (per-checkpoint accuracy) is neither Markov nor observed — the policy sees only proxies (confidence, entropy, agreement), which is precisely why the estimability question (§5.3, RQ-M3) is empirical. Calibration research is the natural lens on the dominant failure signal we expect: confidently-wrong intermediate answers.

## 3. Problem Formulation

**Trajectories and checkpoints.** For task instance x with a mechanically verifiable answer, the model generates a reasoning trajectory segmented at reasoning-transition checkpoints k = 1,…,K (paragraph breaks; reflection tokens such as "Wait", "Alternatively"). At each checkpoint we log: cumulative token cost c_k; the online-observable signal history H_k (answer-span mean log-probability, two pre-registered entropy variants, modal-answer vote share among probes, answer-stability indicators, their deltas, and c_k — never a verifier label); and N forced-answer probes branched off the frozen prefix, each verifier-labeled, giving the probe-accuracy estimate â_k ∈ [0,1].

**Utility and the oracle.** Fix an exchange rate λ (accuracy points per 1K tokens), swept over a log-spaced 7-point grid λ ∈ [0.01, 3]. The utility of stopping at k is

U_λ(k) = â_k − λ·c_k,

and the hindsight-optimal checkpoint is t*(x,λ) = argmin of the earliest maximizer of U_λ over the logged lattice. Three degrees of freedom are made explicit rather than hidden: (i) regret is defined **relative to the logged checkpoint lattice** — a lower bound on continuous-time regret, with a 2×-coarser-lattice ablation reporting discretization sensitivity; (ii) every headline number is a **curve over λ**, never a single-λ scalar; (iii) â_k carries binomial noise (±0.17 s.e. at N=8), and because t* is a max over ~20 noisy values, the plug-in oracle utility is biased upward — §4.2 replaces the plug-in with calibrated uncertainty over t*.

**Stopping rules as calibrated policy classes.** A rule π maps H_k to {stop, continue}; its stop τ_π(x) must be a stopping time of the observable filtration (no future checkpoints, no verifier labels). Every heuristic family is calibrated per λ on a held-out development split by minimizing dev regret, so comparisons are between policy classes, not arbitrary threshold picks.

**Regret, per logged trajectory.** With stochastic decoding both τ_π and t* are random; regret is therefore defined on the logged trajectory (the replayable object), making all rule comparisons exactly paired offline replays on identical logs, with seed variance quantified separately (3 repeated collections on a 200-instance subsample):

R_λ(π; x) = U_λ(t*(x,λ)) − U_λ(τ_π(x)) ≥ 0.

**Decomposition.** Regret splits exactly by the sign of τ_π − t*: stop-too-early mass (τ_π < t*: the model was interrupted before value arrived) and stop-too-late mass (τ_π > t*: the quantified cost of overthinking), with a tie component of zero regret. Under oracle uncertainty (§4.2) the split is computed within each calibrated oracle draw, so the decomposition stays additive draw-by-draw and direction becomes a probability rather than a brittle label. Headline outputs: mean regret curves over λ, normalized headroom (regret ÷ oracle-vs-never-stop gap), and the early/late split by task-difficulty decile (per-instance baseline pass rate).

**Probe-cost accounting.** Probes are a measurement overlay shared by all rules. Rules whose signals consume probe statistics (vote share, stability) get no free parallel compute: we report both accountings — probe cost charged to c_k for all rules, and excluded for all rules — and check that conclusions are stable across the two.

## 4. Measurement Framework

![Figure 1: The regret-of-stopping measurement pipeline. Logged trajectories with forced-answer probe overlays feed an uncertainty-calibrated hindsight oracle; calibrated stopping rules are replayed causally on identical logs; regret is decomposed into early/late mass per calibrated oracle draw, reported over the λ grid and difficulty strata; the sealed corpus makes future rules scorable offline. Pilot gates guard each stage.](architecture.svg)

*Figure 1: The regret-of-stopping measurement pipeline: trajectory generation with probe overlay → uncertainty-calibrated hindsight-oracle construction → causal replay of the calibrated stopping-rule zoo → per-draw regret decomposition over the λ grid and difficulty strata → released replayable corpus, with go/no-go pilot gates guarding each stage.*

### 4.1 Trajectory logging and probe overlay

Instrumented decoding segments the chain of thought at transition markers (following DEER's transition-point insight). At each of K ≈ 10–30 checkpoints, N = 8 forced-answer probes ("…Final answer:") are branched at temperature 0.6 off the shared prefix with KV reuse, while the main trace continues unmodified. **Branch-isolation invariant:** the main trace never sees probe tokens; a unit test asserts main-trace token identity with probes on/off. Per checkpoint we record probe answers with verifier labels (→ â_k), the pre-registered signal set (one confidence: answer-span mean log-prob; two entropies: answer-span mean, last-64-token trend slope; one vote share; one stability indicator), and c_k. Signal definitions are frozen before full collection to preclude garden-of-forking-paths analysis. All online signals derive from the same 8 probe branches; no additional generation exists.

### 4.2 Uncertainty-calibrated hindsight oracle

The oracle must not be treated as ground truth. Checkpoint accuracies are estimated from N probes, are correlated across k through the shared trajectory, and enter an argmax — three reasons a plug-in t* misstates both regret magnitude and direction.

- **Joint estimation.** A paired block bootstrap resamples matched probe seed blocks — the same resampled block indices across all checkpoints — yielding joint draws of the whole utility curve U_b(·,λ) that preserve cross-checkpoint dependence without assuming monotonicity.
- **Simultaneous bands.** Sup-t (max-t) bands control familywise uncertainty over the full checkpoint set, i.e., over exactly the comparison the argmax performs.
- **Conformal oracle sets.** Split-conformal calibration against *disjoint, higher-budget audit probes* (N = 32, on a 100-instance-per-benchmark subsample) converts bands into a confidence set S(x,λ) of plausible oracle checkpoints with target 90% coverage, and yields calibrated weights over oracle draws. The N=32 re-probe additionally bounds the max-of-noisy-means inflation empirically: the induced shift in mean regret is reported as the instrument error bar, and the instrument passes only if this error is smaller than the smallest between-rule regret gap (§5.4, Gate B).

### 4.3 Probe-intervention validity

A forced answer at checkpoint k may differ systematically from what a genuinely stopped model would produce. Two-pronged check: (a) *terminal agreement* — branch-probe vs. natural final answer at the last checkpoint, cheap, on all instances; (b) *true termination* — on a 100-instance × 5-checkpoint subsample, generation is actually stopped at k with fresh answer elicitation, and the resulting accuracy is compared with branch-probe â_k; this is the only direct mid-trajectory test, budgeted at ≈500 medium generations (noise-level cost).

### 4.4 The stopping-rule zoo, calibrated

Arms replayed on identical logs (collection is one pass; arms are free): fixed-budget sweep (stop at checkpoint j); confidence threshold (DEER-style); two pre-registered entropy thresholds; vote-share threshold (the agreement family); answer-stability (two consecutive modal answers agree, TrimR-style); a learned marginal-utility estimator (§5.3) in exactly two frozen architectures (logistic; ≤2-layer MLP) predicting signed continuation gain from H_k — a measured condition, deliberately capped so the paper remains an instrument, not another stopping method; plus oracle (upper anchor) and never-stop (lower anchor). Every thresholded family is calibrated per λ on the dev split; test regret is reported on the disjoint eval split.

### 4.5 Regret scoring and decomposition

For each (rule, instance, λ): replay the rule causally to obtain τ; for each calibrated oracle draw b, compute regret U_b(t*_b,λ) − U_b(τ,λ) and assign it to early (τ < t*_b), late (τ > t*_b), or tie. Draw-level components are mutually exclusive and sum exactly to draw regret, so weighted averaging preserves additivity while oracle uncertainty appears as soft direction probabilities. Aggregation: mean regret ± bootstrap 95% CIs per (rule, λ, difficulty decile); normalized headroom; Wilcoxon signed-rank on paired per-instance differences with Holm–Bonferroni over rule pairs; Kendall's τ for rule-ranking stability across λ.

### 4.6 Replayable sealed corpus

Each trajectory is serialized as a versioned, content-addressed record with two namespaces: a **causal namespace** (prefix text per checkpoint, permitted signals, timing, costs, generation metadata, ordered so the view at k contains nothing introduced after k) and a **sealed namespace** (verifier labels, probe outcomes, oracle draws). A sandboxed sequential API reveals causal records up to the current checkpoint and accepts one irrevocable STOP; scoring joins the sealed namespace only afterward. SHA-256 manifests, schema taint checks (fields derived from sealed data are rejected from the causal view), and randomized hindsight canaries (balanced bits written only to sealed metadata; causal-feature classifiers must stay at chance while a sealed-access positive control detects them) enforce reproducibility and leakage resistance. Any future rule expressible over the causal features is regret-scorable on CPU, without model access.

## 5. Experimental Design

### 5.1 Tasks, model, scale

*Pilot (the deadline paper):* DeepSeek-R1-Distill-Qwen-7B × {GSM8K (exact-match numeric), MATH-500 (expression equivalence), GPQA-Diamond (multiple choice)} × ~500 instances each; K ≈ 20 checkpoints × N = 8 probes ≈ 2.4×10⁵ short probe generations + 1,500 full traces; with prefix-KV reuse ≈ 100–300 A100-hours (~1 node-week). Verification is mechanical; zero annotation. Difficulty labels = per-instance baseline pass rates. *Stage 2 (post-deadline or fallback venue):* +1 open 32B-class model (N=4 if vote-share correlation with N=8 exceeds 0.95), +AIME 2024/25 (descriptive) and LiveCodeBench. Analysis is CPU-only offline replay; additional rules, λ values, and decompositions are free after logging.

### 5.2 Instrument validation (I-series)

Compressed, realistically budgeted versions of the framework audits, run on pilot data plus synthetic stress cases:

- **I1 — Oracle coverage.** On the N=32 audit subsample: simultaneous-band familywise coverage in [0.85, 0.95] at nominal 90% and closer to nominal than independent per-checkpoint bands; conformal oracle-set inclusion of the audit argmax ≥ 0.85 with a ≥ 0.10 paired advantage over the singleton plug-in.
- **I2 — Decomposition exhaustiveness.** Over all empirical tuples plus 50,000 synthetic edge-case tuples (exact ties, adjacent optima, extreme probabilities, cancellation): |direct regret − (early+late+tie)| ≤ 1e−10 in float64, zero violations.
- **I3 — Replay reproducibility.** Six deterministic reference rules × 100 reruns × 2 clean environments: bit-exact stop indices and score tensors against the SHA-256 manifest.
- **I4 — Leakage canaries.** Causal-API classifiers (logistic, boosted trees, MLP; trajectory-grouped cross-fitting) at chance AUC ∈ [0.45, 0.55] on sealed canary bits; sealed-access positive control ≥ 0.95.
- **I5 — Intervention validity.** §4.3's terminal-agreement and true-termination checks; discrepancies reported as instrument error alongside the N=32 re-probe bound.

### 5.3 Main research questions (M-series)

- **RQ-M1 (Headroom).** For each calibrated rule family: mean regret and normalized headroom curves over λ, with instrument error bars. *The* deployer-facing number: what fraction of achievable utility does the best current rule leave unclaimed?
- **RQ-M2 (Where regret lives).** Early/late decomposition per (rule, λ, difficulty decile): does the dominant failure flip from stop-too-late at high λ to stop-too-early at low λ, and does the oracle gap grow with difficulty [cf. difficulty-dependence in Zhou et al., 2026; Snell et al., 2024]?
- **RQ-M3 (Online estimability).** Per-checkpoint AUROC of each frozen signal against the verifier label, as a function of checkpoint index (information decay/accretion curves); regret of the two frozen learned estimators; leave-one-benchmark-out transfer of the estimator. This answers the seed question directly: can the marginal benefit of continued thinking be estimated online, and how much of the oracle gap does the best online-information rule close?
- **RQ-M4 (Ranking stability).** Kendall's τ of rule rankings across λ and across the two probe-cost accountings; a ranking that inverts with λ is itself a deployment-relevant finding [cf. regime-dependence in Dong et al., 2026].

### 5.4 Pilot gates and fallbacks

- **Gate A (week-1 dry run, 50 instances):** probe cost within 2× of projection; branch-isolation invariant passes; checkpoint counts median K ∈ [10, 30]. Hard fail (cost > 4×) → shrink to 2 benchmarks × 300 instances. If the dry run has not passed by the pre-committed calendar trigger, retarget the fallback venue and expand to Stage-2 scope — no renegotiation under deadline pressure.
- **Gate B (week-2 slice, 300 instances):** (a) power-based signal gate — the best signal's regret separation from fixed-budget must be detectable at ≥80% power at full-pilot n, else the online-estimability claim is vacuous and the result ships as a negative note; (b) instrument-resolution gate — the N=32 instrument error must be smaller than the smallest between-rule regret gap, else redesign probes before scaling.
- **Pivot, not death:** if calibrated heuristics prove statistically indistinguishable from zero regret across λ on ≥2 benchmarks, the paper pivots to an audit-style finding ("online stopping is solved for this regime") — a different but publishable claim.

## 6. Limitations

Single-model pilot scope: findings quantify one open 7B reasoning model; the corpus-replay design is the extensibility argument — scoring new models requires only re-collection, scoring new rules requires no GPU at all — and a second model proceeds in parallel for the camera-ready or fallback venue. Regret is lattice-relative (a lower bound on continuous-time regret; sensitivity reported). Forced-answer probes are an intervention with a validity protocol, not a proof of equivalence. Mechanical verifiers bound the task domain: free-form tasks with judge-based scoring would import judge noise into â_k. The oracle set's coverage guarantee is conditional on the audit-probe protocol. Sequential-axis scope: parallel-sampling budget allocation and verifier-effort allocation are deliberately out of scope.

## 7. Conclusion

We reframe test-time stopping evaluation around the question deployers actually face: not which rule wins a pairwise accuracy–token comparison, but how much achievable utility every rule forfeits, where, and why. The framework's estimand — per-instance, cost-indexed, uncertainty-calibrated hindsight-oracle regret with an exact early/late decomposition — turns the overthinking literature's aggregate warnings into an instance-level accounting, and its pilot answers whether marginal utility is online-estimable at all. Because every scientific iteration after logging is a CPU-side replay, the released corpus converts the incoming wave of stopping-rule papers from incomparable one-off evaluations into entries on a common, leakage-controlled regret leaderboard. If the calibrated heuristics turn out to sit near the oracle, that too is a finding — the field can stop writing stopping rules; if they do not, the decomposition says where the remaining utility is, and the corpus says which ideas claim it.

## References

- Aggarwal, P., Madaan, A., Yang, Y., Mausam. *Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs.* arXiv:2305.11860, 2023.
- Aggarwal, P., Welleck, S. *L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning.* arXiv:2503.04697, 2025.
- Aghazadeh, E., et al. *CGES: Confidence-Guided Early Stopping for Efficient and Accurate Self-Consistency.* arXiv:2511.02603, 2025.
- Chen, X., et al. *Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs.* arXiv:2412.21187, 2024.
- Cuadron, A., et al. *The Danger of Overthinking: Examining the Reasoning-Action Dilemma in Agentic Tasks.* arXiv:2502.08235, 2025.
- Dong, Z., et al. *When Does Learning to Stop Help? A Cost-Aware Study of Early Exits in Reasoning Models.* arXiv:2606.30852, 2026.
- Fu, Y., et al. *Efficiently Scaling LLM Reasoning with Certaindex.* arXiv:2412.20993, 2024.
- Fu, Y., et al. *Deep Think with Confidence.* arXiv:2508.15260, 2025.
- Guo, D., et al. *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.* arXiv:2501.12948, 2025.
- Hassid, M., et al. *Don't Overthink It: Preferring Shorter Thinking Chains for Improved LLM Reasoning.* arXiv:2505.17813, 2025.
- Li, Y., et al. *Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning.* arXiv:2401.10480, 2024.
- Lightman, H., et al. *Let's Verify Step by Step.* arXiv:2305.20050, 2023.
- Muennighoff, N., et al. *s1: Simple Test-Time Scaling.* arXiv:2501.19393, 2025.
- Snell, C., Lee, J., Xu, K., Kumar, A. *Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters.* arXiv:2408.03314, 2024.
- Song, S., et al. *ThinkBrake: Efficient Reasoning via Log-Probability Margin Guided Decoding.* arXiv:2510.00546, 2025.
- Sui, Y., et al. *Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models.* arXiv:2503.16419, 2025.
- Wan, G., et al. *Reasoning Aware Self-Consistency: Leveraging Reasoning Paths for Efficient LLM Sampling.* arXiv:2408.17017, 2024.
- Wang, Y., et al. *Thoughts Are All Over the Place: On the Underthinking of o1-Like LLMs.* arXiv:2501.18585, 2025.
- Yang, C., et al. *Dynamic Early Exit in Reasoning Models.* arXiv:2504.15895, 2025.
- Zhou, S., et al. *When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling.* arXiv:2604.10739, 2026.
