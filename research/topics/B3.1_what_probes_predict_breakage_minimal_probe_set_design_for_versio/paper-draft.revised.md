# Which Probes Predict Breakage? Budgeted Cross-Axis Probe-Set Design for LLM Version-Drift Auditing

*Revised draft (2026-08-14), superseding the auto-generated draft "Cross-Axis Probe Drift for Budgeted Prediction of LLM Contract Breakage." Positioned as the instrument-design companion to B3.3 (silent-change rate) and B3.4 (contract breakage): B3.4 supplies the breakage ground truth; this paper supplies the model-side prediction and probe-selection layer. Standalone submission only under the pre-registered triggers in Section 7.*

## Abstract

Providers ship new LLM versions on their own schedule, and upgrades can silently invalidate the schemas, parsers, and tool-call interfaces that downstream systems depend on. Existing black-box monitors detect *that* a model changed; direct compatibility frameworks re-test application contracts at full cost; neither answers the operational question in between: **which cheap behavioral probes, and how few of them, predict what will functionally break on an unseen upgrade?** We design a five-family probe battery (capability, refusal-boundary, format, calibration, safety) and evaluate its drift signals as predictors of category-specific functional breakage — schema-validation failure, parser exception, tool-call inexecutability — measured on a shared contract corpus run across real version pairs. Three disciplines separate prediction from tautology and overfitting: (i) an *instrument gate* requiring each family's drift to exceed the within-version sampling-noise floor and remain rank-stable under paraphrase before any predictive claim; (ii) fully nested leave-one-version-pair-out evaluation with probe selection re-run inside every training fold, plus a frozen-set temporal holdout that grows as new versions ship; and (iii) a *cross-axis prediction matrix* whose near-tautological diagonal (format probes predicting format breakage) is excluded from headline claims, together with leave-one-contract-class-out evaluation so that the selected probe set is shown to generalize beyond the corpus it was selected on. Budgeted greedy selection with bootstrap stability produces a query-budget–retention curve, benchmarked against budget-matched random subsets, benchmark-compression baselines, a change-detection-only gate, and cost-equivalent direct contract testing. A pilot on 4–6 immutable open-weight version pairs, sharing the B3.4 contract corpus, gates scale-up to 15–25 pairs under pre-registered go/no-go criteria. The deliverable is an audited early-warning instrument — or an honest negative result that cheap probes cannot forecast breakage and auditors must run contract suites.

## 1. Introduction

Large language models are now externally managed dependencies. A provider upgrades the model behind an API endpoint — or a team bumps an open-weight checkpoint — and every downstream pipeline tuned against the old version inherits the change: prompt templates, output parsers, JSON-schema contracts, tool-call fillers, moderation wrappers. Longitudinal audits document that such upgrades shift behavior substantially and unevenly across tasks [Chen et al. 2023], and regression studies of evolving LLM APIs find that a majority of prompt–model combinations lose accuracy across updates [Ma et al. 2024]. The 2026 literature has responded on two fronts. Black-box *change detectors* — behavioral auditing tests [Richter et al. 2024], endpoint fingerprinting [Leshin et al. 2026], linguistic-feature tests [Dima et al. 2025], rank-based uniformity tests [arXiv:2506.06975], logprob tracking [arXiv:2512.03816], and substitution audits [Cai et al. 2025] — tell an integrator *that* the served model changed. Deployment-governance frameworks — production-contract gating [Chishti et al. 2026] and confident model migration [Casey et al. 2026] — re-run the application's own contract tests, at the application's own cost. Practitioner tooling now ships "canary prompt" replay with hand-picked probe families, but with no validation that canary drift predicts anything downstream.

Between these two fronts sits an unanswered measurement question. Detection is cheap but consequence-blind: a detector that fires on every harmless fine-tune delays adoption; one that is quiet while a parser-killing format shift ships gives false reassurance. Direct contract testing is consequence-exact but expensive and enumerable-only: an integrator's private pipeline is in nobody's test suite. If a small battery of behavioral probes — run once against each new version — *predicted* the rate and category of functional breakage, an auditor would gain a triage instrument: quiet probes, skip the full re-test; loud probes, know which re-test to run. Whether such predictive signal exists, which behavioral axes carry it, and how few queries retain it are empirical questions that no published work answers.

Answering them credibly requires guarding against three specific failure modes, and these guards are the technical substance of this paper.

**Tautology.** Format probes are miniature format contracts; that they "predict" format breakage is compression, not discovery. Our headline estimand is the *off-diagonal* of a probe-family × breakage-category prediction matrix: does refusal-boundary drift forecast tool-call breakage? does capability drift forecast parser failures? Diagonal cells are reported but excluded from claims. Symmetrically, a probe set selected against one contract corpus may merely memorize that corpus; we therefore evaluate under leave-one-contract-class-out as well as leave-one-version-pair-out, and spot-check on real third-party pipelines.

**Unvalidated instruments.** A drift score is meaningless if it does not exceed the model's own sampling noise, or if it flips sign under paraphrase of the probe items. Before any prediction claim, each family must pass a pre-registered instrument gate: cross-version drift above the within-version noise floor on most pilot pairs, and rank-stability across ≥3 paraphrase variants.

**Small-n overfitting.** Version pairs — not contract rows — are the independent unit, and there will be at most ~25 of them. We pre-register a deliberately small model class (regularized hierarchical logistic regression), re-run *all* selection inside each leave-one-pair-out training fold, quantify selection stability under bootstrap, and freeze the selected probe set for evaluation on version pairs that ship after selection — a temporal holdout that grows for free as providers release.

**Contributions.**
1. A validated five-family black-box probe battery with per-family drift instruments, a within-version noise-floor protocol, and a paraphrase-stability certificate (the instrument layer that prior canary tooling lacks).
2. The first predictive evaluation linking probe-family drift to category-specific functional breakage across real LLM version pairs, under fully nested leave-one-version-pair-out and leave-one-contract-class-out protocols, with a cross-axis prediction matrix whose diagonal is excluded from claims.
3. A query-budgeted minimality analysis: greedy conditional-gain selection with bootstrap stability, yielding a budget–retention curve and a frozen minimal set S* validated on later-shipping pairs, benchmarked against budget-matched random subsets and benchmark-compression baselines.
4. A pluggable module contract and released artifacts (probe bank, cached outputs, selection code) consumable by contract-breakage (B3.4) and silent-change (B3.3) audits, with pre-registered gates deciding merged vs standalone publication.

## 2. Related Work

**Black-box change detection.** Richter et al.'s sequential auditing test [arXiv:2410.19406], the rank-based uniformity test [arXiv:2506.06975], Dima et al.'s linguistic-feature equivalence tests [arXiv:2504.12335], Leshin et al.'s Stability Monitor endpoint fingerprints [arXiv:2603.19022], logprob-signature tracking of updates [arXiv:2512.03816], model-equality testing [Gao et al., arXiv:2410.20247], and substitution auditing [Cai et al., arXiv:2504.04715] all decide *whether* the model behind an interface changed. None ranks behavioral axes by downstream consequence or predicts which integrations break. We use this class of test as a component (the change-detection-only baseline A7) and build the prediction layer above it; our beyond-detection gate G4 requires the probe battery to beat it by a pre-registered margin.

**Drift evidence and regression testing for LLM APIs.** Chen, Zaharia & Zou [arXiv:2307.09009] document large per-task swings across hosted snapshots; Ma et al. [arXiv:2311.11123, CAIN 2024] reframe regression testing for evolving LLM APIs and quantify widespread prompt regressions; Xie et al. [2021] measure negative flips across NLP model updates; output-drift studies quantify cross-provider instability on regulated workflows [arXiv:2511.07585]. These document breakage; none tests whether cheap probes *forecast* it on unseen upgrades.

**Deployment governance and direct testing.** Chishti et al.'s supply-chain gating [arXiv:2604.27789] and Casey et al.'s end-of-life migration framework [arXiv:2604.27082] evaluate application contracts directly; DriftBench/SkillGuard treat agent-skill drift as contract violation [arXiv:2605.10990]; practitioner canary-replay tools ship fixed probe sets with no predictive validation. These are our cost comparator (direct testing) and our motivation, respectively: the probe battery must be materially cheaper than the contract suite *and* generalize beyond enumerated contracts, or it has no reason to exist — a null we state and test.

**Efficient evaluation and test minimization.** tinyBenchmarks [Polo et al. 2024] and EssenceBench-style compression select minimal item subsets preserving *scores at one time point*; PredictaBoard [Pacchiardi et al. 2025] predicts instance-level errors; classical regression-test selection and suite minimization [Yoo & Harrold 2012; Rothermel & Harrold] optimize the same minimality criterion under white-box coverage with deterministic oracles. We transpose the minimality logic to black-box, stochastic, axis-structured drift prediction — and keep benchmark compression as an explicit baseline (A4): if compressing capability items alone matches our axis-structured selection, the axis structure adds nothing.

**Single-axis instruments.** IFEval [Zhou et al. 2023], JSONSchemaBench [Geng et al. 2025], schema-RL [Cong et al. 2025], format-restriction effects [Tam et al. 2024], XSTest [Röttger et al. 2024], HarmBench [Mazeika et al. 2024], confidence elicitation [Xiong et al. 2024], and OpenReview-corpus instruments (RefusalIndex, B-Calibration, OffTopicEval, TARE paraphrase-brittleness) supply the item pools and scoring conventions for our five families. They measure behavior statically; we ask whether *changes* in these measurements carry predictive information across versions.

**Gap.** No prior work performs an axis-resolved, black-box comparison of probe-family drift against functional downstream-breakage ground truth across LLM version pairs, with budgeted minimality and held-out validation on both the version axis and the contract axis. The claim is the composite predictive protocol — not "first minimal test suite" (false vs SE literature) and not "first drift detector" (false vs the detection line).

## 3. Problem Definition

**Setting.** A version pair v = (m⁻, m⁺) is a pre/post-upgrade model pair queryable only through inputs and outputs (immutable open-weight checkpoints, or dated API snapshots while both are served). Let 𝒱 = {vᵢ}ⁿᵢ₌₁ be the observed pairs, partitioned chronologically into a development set 𝒱_dev and a growing temporal holdout 𝒱_temp of pairs shipped after selection is frozen.

**Probes.** The battery 𝒫 is partitioned into five families F = {capability, refusal-boundary, format, calibration, safety}. Family f has item set Q_f; each item is administered to both models with k ≥ 3 repeats under fixed decoding, plus a within-version repeat arm estimating the sampling-noise floor. The drift representation x_{i,f} is computed from outputs only. For any subset S ⊆ ⋃_f Q_f, the query cost is c(S) = |S| (per-item repeat counts folded in), so minimality is denominated in queries, not families.

**Breakage ground truth.** A contract corpus 𝒞 (canonically B3.4's simulated-production corpus) partitioned into classes; categories 𝒦 = {schema-validation failure, parser exception, template break, tool-call inexecutability, judged answer-equivalence break}. For contract c, category k, pair vᵢ: y_{i,c,k} = 1 iff c passes under m⁻ and fails under m⁺ in category k; the target is the per-class breakage rate b_{i,k} = mean_c y_{i,c,k}. Raw output-diff magnitude is a descriptive statistic only — breakage is functional by definition.

**Estimands.**
- *Prediction:* A_k(S) = out-of-sample performance (AUC for flagging, R² for magnitude) of predicting b_{i,k} from x_{i,S}, estimated by leave-one-version-pair-out (LOPO) with **all** selection, fitting, and tuning inside each training fold, and — separately — by leave-one-contract-class-out (LOCO) with the class's contracts removed from both selection and fitting.
- *Cross-axis matrix:* M_{f,k} = A_k(Q_f) − max{R_k(c(Q_f)), G_k}, where R_k is a budget-matched random-subset baseline and G_k a change-detection-only predictor (omnibus drift magnitude, no family identity). Cells with axis(f) = axis(k) form the near-tautological diagonal, reported but excluded from headline claims; the principal estimand is the off-diagonal set.
- *Minimality:* the budget–retention curve A(B) = max_{c(S)≤B} mean_k A_k(S) with selection nested per fold, and the minimal set S* = argmin c(S) s.t. A(S) ≥ A(full) − ε, with ε pre-registered as max(0.03 AUC, half-width of the full battery's bootstrap CI) so minimality is never claimed below the resolution the data supports.

**Constraints.** Black-box outputs only (no weights, gradients, or required logprobs); no selection or tuning may touch a held-out pair, a held-out contract class, or 𝒱_temp.

## 4. Method

![Figure 1: Overview of the budgeted cross-axis probe-selection pipeline: a five-family probe universe passes an instrument gate (noise floor, paraphrase stability), drift features and contract-corpus breakage rates meet in a nested selection/prediction layer, and claims are audited by cross-axis, held-out-pair, held-out-class, and frozen temporal validation under pre-registered pilot gates.](architecture.svg)

*Figure 1: Overview of the budgeted cross-axis probe-selection pipeline. Probe families are validated against the within-version noise floor and paraphrase instability before use; version-pair evaluation produces per-class functional breakage rates; nested greedy selection with stability bootstrap yields the budget–retention curve and minimal set S*; validation discipline (LOPO, LOCO, frozen temporal holdout, cross-axis matrix with excluded diagonal) and pilot gates G1–G4 guard every claim.*

### 4.1 Probe battery and instrument validation (SP1, gate G1)

Each family pairs an item pool with a drift instrument:
1. **Capability** — MMLU/GSM8K/BBH-style items, format-robust scoring (normalized answer extraction; code executed after fence-stripping); drift = signed aggregate of paired per-item correctness deltas.
2. **Refusal-boundary** — borderline items stratified from XSTest / OR-Bench; drift = refusal-rate delta plus a rate-invariant RefusalIndex-style rank shift.
3. **Format** — IFEval-style instructed-format items + JSON-schema tasks; drift = change in schema-validity / structural-match rates across paraphrase sets.
4. **Calibration** — labeled items; drift = change in ECE / semantic-calibration error (B-Calibration-style for free-form).
5. **Safety** — harm-adjacent + policy-conditioned out-of-scope prompts (OffTopicEval-style) + pseudo-harmful over-refusal items; drift = per-stratum accept/refuse rate changes.

*Validation before prediction.* For every family: (a) **noise floor** — within-version repeat runs (same model, fresh sampling; fixed and re-sampled decoding) give the null distribution of the drift score; a family's cross-version drift on a pair counts as signal only when it exceeds the 95th percentile of this null; (b) **paraphrase stability** — each item has ≥3 paraphrase variants; family drift must be rank-stable across variants (Kendall's τ ≥ pre-registered threshold across pairs). Families failing either check are excluded from prediction and reported as instrument negatives. This is gate **G1**.

### 4.2 Cross-axis breakage prediction (SP2, SP3)

*Unit and model.* The analysis cell is (version pair × contract class); the independent unit is the pair. We pre-register one small model class: L1/L2-regularized hierarchical logistic (flagging) and linear (magnitude) models with pair-level random effects; contract-class effects absorb baseline fragility. No model search beyond the pre-registered grid, tuned by inner-fold CV only.

*Attribution under co-movement.* Families co-move (safety with refusal; capability with format). Family-level answers to RQ1 use standardized coefficients, partial correlations (each family conditioned on the other four + omnibus drift magnitude), and bootstrap stability selection (a family "predicts" only if selected in ≥70% of bootstrap-over-pairs replicates). The honest possible outcome — "a correlated bundle predicts; no single family does" — is a reportable result, not a failure.

*Cross-axis matrix.* For each (family f, category k): nested-LOPO A_k(Q_f) vs budget-matched random subsets and the change-detection gate. Diagonal cells (format→format-schema, safety→refusal-adjacent classes, per a pre-registered axis map) are excluded from headline claims. The off-diagonal is the scientific payload: probes forecasting breakage they do not superficially resemble.

*Guarding the contract axis.* All headline numbers are also computed under LOCO (leave-one-contract-class-out): the held-out class's contracts are removed from selection and fitting, and predicted cold. A probe set that predicts held-out pairs but not held-out classes is a compressed test suite, and is reported as such. As an external-validity spot check (SP6, best-effort), 1–2 real open-source pipelines with their own test suites are run across one pilot pair as out-of-corpus breakage points.

### 4.3 Budgeted minimality (SP4) and frozen-set temporal validation

*Selection.* Items are clustered by drift-profile correlation (clusters may cross family boundaries). Greedy forward selection over clusters maximizes conditional AUC gain per query, nested inside each LOPO training fold; a cluster enters S* only if selected in ≥70% of bootstrap replicates. Sweeping the budget B yields the budget–retention curve; S* is the cheapest subset within ε of the full battery.

*Two granularities, both answered.* RQ1 (which family predicts) is answered at family level with partialling; RQ2 (which items to buy) at item-cluster level — explicitly two views of one question, so the family-level science is not silently swapped for engineering.

*Frozen-set temporal validation.* S* and its predictor are frozen at selection time and evaluated untouched on every version pair that ships afterwards (𝒱_temp grows for free). This is the deployment-credible number: the instrument as an integrator would actually use it.

*Composition sensitivity.* Because the family ranking inherits the corpus mix, rankings are re-computed under re-weighted contract-class mixes (equal-weight, JSON-heavy, tool-call-heavy). A ranking that survives re-weighting is a finding; one that does not is a property of the corpus and is reported as such.

### 4.4 Module contract (B3.3/B3.4 interface)

Input: any collection matching the declared schema (pair id, contract class, breakage rate, provenance) — canonically B3.4's corpus, alternatively B3.3's category-resolved behavior diffs. Output: (i) family-level predictive ranking with uncertainty; (ii) selected minimal probe set with query budget; (iii) a calibrated breakage-risk score for future pairs; (iv) per-family drift logged against B3.3's changelog taxonomy so silent-change categories can be severity-weighted without new runs. Released: probe bank (with paraphrase variants), all cached model outputs, selection/evaluation code, and the frozen S*.

## 5. Experimental Design

**Arms.**
- A1: each family alone (five arms) — per-family predictive baseline.
- A2: full five-family battery — upper bound.
- A3: minimal set S* (stability-selected, frozen for temporal validation).
- A4: tinyBenchmarks/EssenceBench-style compression within capability items only — does generic benchmark compression already suffice?
- A5: random subsets budget-matched to S* (10 draws) — selection-value control.
- A6: raw aggregate output-diff magnitude ignoring family structure.
- A7: change-detection-only gate (rank-based uniformity test à la arXiv:2506.06975) — how much predictive information exists beyond detection?
- A8: cost-equivalent direct contract testing at matched query budget — the "why probe at all" comparator; the probe set must be ≥10× cheaper than the full suite (headline cost ratio) and beat budget-matched partial direct testing, or the honest conclusion is "run the contract suite."

**Data.**
- *Pilot (co-scheduled with B3.4's pilot):* 4–6 open-weight pairs with immutable checkpoints — Llama-2→Llama-3, Qwen1.5→Qwen2→Qwen2.5, Mistral v0.1→v0.2→v0.3 — ~500 probe items (×3 paraphrases for the stability arm), ground truth = B3.4 pilot corpus (~10 contract classes). ≈18k generations beyond B3.4's own runs; marginal cost is small because the ground truth is shared.
- *Scale-up (gated):* 15–25 pairs adding further open-weight lineages and dated API snapshots while both endpoints are live (interleaved query windows; all raw outputs cached and released so analyses outlive endpoint deprecation). ~1,500 probe items, ~20 contract classes, ≈200–650k generations (2–4 A100-class GPUs + low-thousands-USD API budget). API pairs are bonus, never load-bearing: every gate and the temporal holdout are powered on open-weight pairs alone.

**Metrics.** LOPO and LOCO AUC / R² with bootstrap-over-pairs CIs and permutation nulls; per-family Spearman ρ, partial correlations, stability-selection frequencies; off-diagonal cross-axis AUC; ΔAUC(S* vs full); budget–retention curve; noise-floor exceedance rate and paraphrase Kendall's τ; frozen-set temporal-holdout AUC; headline cost ratio (S* vs full contract suite).

**Pre-registered gates.**
- **G1 (instrument, pilot):** ≥2 families show drift above the noise floor on ≥70% of pilot pairs, rank-stable under paraphrase. Fail → probes cannot measure drift; publish the instrument negative inside B3.4; stop.
- **G2 (signal, pilot→scale-up):** full-battery LOPO AUC point ≥ 0.70 *and* bootstrap lower bound ≥ 0.60 on pilot cells (permutation p < 0.05). Fail → negative-result framing ("cheap probes do not forecast contract breakage") merged into B3.4.
- **G3 (minimality, scale-up only):** some subset at ≤40% of full budget within ε. Fail → "no free lunch: all axes carry non-redundant signal" — an anti-compression finding, still reportable. Pilot results for G3 are directional only.
- **G4 (beyond-detection):** A2 beats A7 by ΔAUC ≥ 0.05. Fail → contribution over shift detectors is not established; standalone framing is dead regardless of other gates.
A simulation-based power check (synthetic breakage at plausible effect sizes over the pilot pair×class layout) sizes the probe bank before any model is queried.

**Research questions.** RQ1: which probe family's drift predicts functional breakage, after partialling out co-movement? RQ2: what is the cheapest probe subset within ε of the full battery, and does data-driven selection respect the hand taxonomy? RQ3: does measured drift exceed noise and survive paraphrase? RQ4: does off-diagonal (cross-axis) predictive signal exist? RQ5: does the selected set transfer — to held-out contract classes, to later-shipping pairs, to another vendor's lineage?

## 6. Limitations and Threats

*Sample size.* Even at scale-up, n ≤ 25 pairs; only the pre-registered small model class, nested selection, permutation inference, and the growing temporal holdout keep estimates honest, and pilot conclusions are explicitly directional for RQ2/RQ4. *Corpus dependence.* Ground truth is a simulated-production corpus; composition-sensitivity reweighting and the SP6 real-pipeline spot check bound, but do not eliminate, this threat. *Same-axis leakage.* The axis map defining "diagonal" cells is hand-declared and pre-registered; an adversarial reading of any off-diagonal claim against that map is invited. *API mortality.* Dated API endpoints die; all raw outputs are cached and released so every analysis is reproducible post-deprecation. *Construct narrowness.* Functional breakage ignores silent semantic degradation inside format-valid outputs; that construct belongs to B3.3's silent-change instrument, which this module feeds but does not replace.

## 7. Positioning and Publication Triggers (pre-registered)

**Default = merged.** If B3.4 proceeds on schedule with ≥10 scale-up pairs, this work ships as the model-side prediction + minimal-probe-set module of B3.4's paper (shared corpus, one paper), with a negotiated floor: the budget–retention curve and cross-axis matrix appear as main-paper figures, or the standalone track re-opens. B3.3 consumes the family ranking as severity weights for silent-change categories. **Standalone trigger (all three):** (i) G1–G2 pass and the cross-axis matrix shows non-trivial off-diagonal signal; (ii) B3.4 slips a submission cycle or descopes below ~8 pairs; (iii) the adjacency check stays clean (no published probe→breakage predictor — verified against the 2026 neighbors as of this draft). **Kill/absorb:** G1 or G4 fail → at most one section + released probe bank inside B3.4.

## 8. Conclusion

The question "which probes predict breakage, and how few suffice?" sits unclaimed between change detection and direct contract testing. This design answers it with instruments validated before use, prediction evaluated only out-of-sample on both the version axis and the contract axis, tautological cells excluded by construction, minimality denominated in queries and certified by a frozen temporal holdout, and pre-registered gates that convert every failure mode into an honest, publishable finding. Whatever the outcome — a cheap early-warning instrument, an anti-compression result, or a demonstration that only contract suites forecast contract breakage — the auditing community gains a decision it can act on, and the B3.3/B3.4 audits gain the layer that makes their measurements forward-looking.

## References

- Lingjiao Chen, Matei Zaharia, James Zou. How Is ChatGPT's Behavior Changing over Time? arXiv:2307.09009, 2023.
- Wanqin Ma, Chenyang Yang, Christian Kästner. (Why) Is My Prompt Getting Worse? Rethinking Regression Testing for Evolving LLM APIs. CAIN 2024; arXiv:2311.11123.
- Leo Richter, Xuanli He, Pasquale Minervini, Matt J. Kusner. An Auditing Test to Detect Behavioral Shift in Language Models. arXiv:2410.19406, 2024.
- Rank-based uniformity test for behavioral shift in black-box LLM APIs. arXiv:2506.06975, 2025.
- Logprob-based tracking of model updates behind LLM APIs. arXiv:2512.03816, 2025.
- Irena Gao, Percy Liang, Carlos Guestrin. Model Equality Testing: Which Model Is This API Serving? arXiv:2410.20247, 2024.
- Will Cai, Tianneng Shi, Xuandong Zhao, Dawn Song. Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs. arXiv:2504.04715, 2025.
- Alden Dima, James Foulds, Shimei Pan, Philip Feldman. You've Changed: Detecting Modification of Black-Box Large Language Models. arXiv:2504.12335, 2025.
- Jonah Leshin et al. Behavioral Fingerprints for LLM Endpoint Stability and Identity. arXiv:2603.19022, 2026.
- Mohd Sameen Chishti et al. Test Before You Deploy: Governing Updates in the LLM Supply Chain. arXiv:2604.27789, 2026.
- Emma Casey, David Roberts, David Sim, Ian Beaver. When Your LLM Reaches End-of-Life: A Framework for Confident Model Migration in Production Systems. arXiv:2604.27082, 2026.
- Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries (SkillGuard / DriftBench). arXiv:2605.10990, 2026.
- LLM Output Drift: Cross-Provider Validation & Mitigation for Financial Workflows. arXiv:2511.07585, 2025.
- Yuqing Xie et al. Regression Bugs Are In Your Model! Measuring, Reducing and Analyzing Regressions in NLP Model Updates. 2021.
- Felipe Maia Polo et al. tinyBenchmarks: Evaluating LLMs with Fewer Examples. ICML 2024.
- Lorenzo Pacchiardi et al. PredictaBoard: Benchmarking LLM Score Predictability. arXiv:2502.14445, 2025.
- Shin Yoo, Mark Harman. Regression Testing Minimization, Selection and Prioritization: A Survey. Software Testing, Verification and Reliability 22(2), 2012.
- Jeffrey Zhou et al. Instruction-Following Evaluation for Large Language Models (IFEval). arXiv:2311.07911, 2023.
- Saibo Geng et al. JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models. arXiv:2501.10868, 2025.
- Xin Cong et al. Learning to Generate Structured Output with Schema Reinforcement Learning. arXiv:2502.18878, 2025.
- Zhi Rui Tam et al. Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models. EMNLP Industry 2024.
- Paul Röttger et al. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models. NAACL 2024.
- Mantas Mazeika et al. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal. ICML 2024.
- Miao Xiong et al. Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. ICLR 2024.
- PromptCanary: canary-prompt replay tooling with format/reasoning/safety/factual/tool-use probes (practitioner software, 2026) — cited as unvalidated adjacent practice.
- OpenReview-corpus instruments: EssenceBench [lZlZjSxdio]; RefusalIndex [9gJBhkLRat]; OffTopicEval [EcIyiJrajc]; B-Calibration [0sCyk9Tr5J]; TARE [YEBDvqsniH]; ProSafePrune [QkHKaPfRAB]; BiasSimilarity-BSM [EveruzAsGI]; WeightDiff [6As4wfTB77].
