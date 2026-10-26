# Digest: Where Thinking Starts to Hurt: Difficulty-Conditioned Boundaries of Test-Time Compute

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet. This document
> projects forward from an abstract research idea (topic **B4.3**, label `[边界]`, parent
> topic "B4. 预算分配 / 推理经济学") to what an N0–N12 digest of a future paper answering it
> *might* look like. Every field is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README (title, core question, minimal
> experiment). **[HYPOTHESIS]** = reasoned elaboration/prediction, grounded in the seed +
> standard practice for this kind of study — not a fact. **[PLACEHOLDER]** = genuinely
> unknowable until the work is done (authors, DOI, numbers, artifacts) — never invented.
> **[GROUNDED:corpus]** = a real OpenReview paper retrieved from the local corpus
> (`topics/corpus/ideas.jsonl`, 11,683 papers); its `approach_summary` is grounded in that
> paper's own motivation/method text, while the *fit* judgment to this future paper is ours.
> Locators for GIVEN content point at the seed README; locators for HYPOTHESIS/PLACEHOLDER
> content are marked `N/A — hypothesized (paper not written)`.

---

## N0 Metadata

- **title** [GIVEN]: "Where Thinking Starts to Hurt: Difficulty-Conditioned Boundaries of Test-Time Compute"
  — Locator: `{"page": null, "section_title": "seed README — title/subtitle line", "quote": "Where Thinking Starts to Hurt: Difficulty-Conditioned Boundaries of Test-Time Compute"}`
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper has been written, so no author list exists.
- **abstract** [HYPOTHESIS] (drafted, NOT a real abstract — synthesized from the core question + minimal experiment for scaffolding purposes only):
  > "Reasoning models can improve accuracy by generating longer chains of thought at test
  > time, but this benefit is not unconditional: past some point, additional 'thinking'
  > tokens stop helping and can even hurt accuracy. We study where this tipping point lies
  > as a function of task difficulty. On tasks stratified into difficulty bins by an
  > operational proxy (low-budget solve rate crossed with dataset-native difficulty tags),
  > we measure accuracy as a function of controlled reasoning length and identify, per
  > stratum, the non-monotonic region where the marginal return to more thinking turns
  > negative. We then test whether this difficulty-conditioned tipping point can be
  > predicted using cheap, pre-hoc signals — output-entropy trajectories over the first few
  > hundred thinking tokens and agreement among a handful of early truncated-answer probes —
  > without requiring the full reasoning budget or ground-truth correctness labels at
  > inference time."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` — inferred from the parent topic ("预算分配 / 推理经济学", budget allocation / reasoning economics for LLM test-time compute).

**Status:** PARTIAL (title given; authors/abstract are placeholder/hypothesis, not "found" in any real source document).
**Absence comment:**
- what_missing: "No actual authors, DOI, arXiv id, or verified abstract exist because the paper has not been written."
- why_matters: "Any downstream tooling (e.g. citation managers, reviewer assignment) that expects real bibliographic identity would be operating on fabricated data if this weren't flagged."
- implication: "Treat N0 purely as a planning placeholder; re-populate authors/abstract/doi/arxiv_id only once an actual manuscript exists."

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS], built as a full predicate directly from the core question:
  "Estimate, for LLM reasoning tasks stratified by an operational difficulty proxy, the
  difficulty-conditioned length at which additional test-time reasoning (chain-of-thought /
  'thinking' budget) yields negative marginal accuracy gain, and predict that tipping point
  at inference time using cheap signals (output-entropy trajectories, early-sample
  consistency) rather than requiring the full reasoning budget or ground-truth correctness
  labels."
  - Self-check: kind of task = *measurement + prediction* of a compute-allocation
    inflection point; domain = *LLM test-time reasoning / chain-of-thought compute*;
    outcome shape = *empirical accuracy-vs-length curves with per-stratum change points +
    a lightweight predictor function with an accuracy-cost Pareto evaluation*. All three land.
- **inputs** [HYPOTHESIS], inferred from the minimal experiment:
  1. A task suite with difficulty labels or a computable difficulty proxy (for stratification).
  2. A reasoning LLM capable of variable-length chain-of-thought generation under external
     length control (budget-forcing truncation and forced continuation).
  3. Per-item generation logs sufficient to compute output-token entropy trajectories and
     to draw a small number of early truncated-answer probes for a consistency signal.
- **outputs** [HYPOTHESIS], inferred from the minimal experiment:
  1. Accuracy-vs-thinking-length curves per difficulty stratum, with confidence intervals.
  2. The identified non-monotonic region / tipping-point location L\* per stratum (where the
     curve's local slope turns negative), with a bootstrap CI on L\*.
  3. A cheap-signal predictor mapping entropy/early-consistency features to a predicted
     tipping-point length, and its accuracy-cost tradeoff relative to fixed-budget, oracle,
     and prior early-exit baselines.
- **constraints** [GIVEN] (what the seed explicitly implies) + [HYPOTHESIS] (elaboration):
  - [GIVEN] Accuracy must be measurable as a function of thinking length, which requires
    ground-truth correctness labels per task instance ("测正确率-思考长度曲线").
  - [GIVEN] Tasks must be stratifiable by difficulty ("按难度分层的任务").
  - [HYPOTHESIS] The cheap predictive signal (entropy / early consistency) must be
    computable within a small fraction of the full budget and without access to ground
    truth, otherwise it cannot serve as a genuine pre-hoc stopping signal at deployment time.

**Status:** PARTIAL (objective/inputs/outputs are inferred, not extracted from a written method section).
**Source:** inferred, closely grounded in the seed's core question and minimal experiment.
**Locator:** `{"page": null, "section_title": "seed README — 核心问题 / 最小实验", "quote": "更多思考的边际收益转负... 按难度分层的任务上测正确率-思考长度曲线的非单调区"}`
**Absence comment** *(added at Phase A re-run, 2026-07-04, per goal.md §3 item 1 — every non-GIVEN node needs the 3-part comment)*:
- what_missing: "No written Methods section exists to extract objective/inputs/outputs from; all three are elaborated from the seed's two-sentence core question and minimal experiment."
- why_matters: "A reader could mistake this specificity (proxy definitions, arm names) for extracted fact rather than reasoned elaboration — the specificity is this document's own design choice, not the seed's."
- implication: "Re-derive N1 from `paper.md` Step 5's formal notation once experiments run; until then, treat objective/inputs/outputs as the pre-registered plan, not a report of what a written method section says."

---

## N2 Motivation

[HYPOTHESIS] — reconstructed from the parent-topic framing ("B4. 预算分配 / 推理经济学",
budget allocation / reasoning economics), and consistent with the motivation texts of the
corpus papers in N3 (which repeatedly assert overthinking wastes compute and can degrade
accuracy), not from any stated statistic:

- **motivation_text**: "Modern reasoning models (o1/R1-style systems) expose 'thinking
  budget' as a controllable resource — users or serving systems can spend more test-time
  compute to try to buy more accuracy. But compute is not free: it costs latency and
  serving cost, and if the marginal benefit of extra thinking can turn *negative* rather
  than merely flat, then naive 'always think longer' policies actively waste resources and
  can hurt correctness. A dense recent literature (see N3) builds stopping rules, difficulty
  probes, and length-shortening training objectives on the *premise* that overthinking
  exists — yet none of it publishes the underlying boundary map: *where*, as a function of
  problem difficulty, the marginal return flips sign, and whether that boundary can be
  anticipated cheaply before spending the full budget. Budget-allocation decisions are
  currently made against an unmeasured landscape." [HYPOTHESIS]
  - source: inferred
  - location: `{"page": null, "section_title": "seed README — parent_topic framing", "quote": "B4. 预算分配 / 推理经济学"}`
  - evidence: `[{type: "citation", text: "corpus papers in N3 (e.g. [WhenMoreIsLess, OpenReview:6QDFsYxtI1], [Chen et al., 2024 (Do NOT Think That Much)]) motivate their methods by asserting that excessive reasoning steps 'can also degrade accuracy'", source: "inferred", location: "N3 entries below"}]`

**Status:** PARTIAL (reconstructed from parent-topic framing and N3 corpus motivation texts, not a stated author motivation).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No author motivation paragraph exists; the stakes argument is assembled from the parent-topic label and the shared assertion (across N3 corpus papers) that overthinking exists and degrades accuracy."
- why_matters: "The 'who cares' framing (serving-policy engineers, stopping-rule researchers) is this document's own argument for relevance, not a claim any cited paper makes about B4.3 specifically."
- implication: "Re-derive N2 from the actual paper's Introduction once written; the coarse-bin-vs-continuous-predictor argument (pipeline.md Stage 2 refiner pass) should be folded in verbatim since it survived a critic round."

---

## N3 Related Works

**Grounding note.** All `[GROUNDED:corpus]` entries below are REAL OpenReview submissions
retrieved from the local corpus (`topics/corpus/ideas.jsonl`) via four keyword-angle
searches: (1) overthinking / CoT length / test-time compute, (2) difficulty-aware / adaptive
reasoning / budget allocation, (3) early stopping / entropy / self-consistency / confidence,
(4) budget forcing / thinking budget / length control. Each `approach_summary` is grounded
in the paper's own motivation+method text. Two non-corpus entries are canonical anchors of
this sub-literature (cited by name — `@muennighoff2025s1`, `@chen2024overthinking` — inside
multiple corpus papers' motivation texts) and are clearly marked **[NON-CORPUS, canonical]**.

- **citation_key**: `[WhenMoreIsLess, OpenReview:6QDFsYxtI1]` [GROUNDED:corpus]
  **approach_summary**: Models CoT as sequential sub-question decomposition with per-step
  error accumulation; derives a theoretical inverted-U relationship between reasoning
  length, task difficulty, and model capability (an optimal length exists), and validates
  the prediction on controlled synthetic arithmetic/DP-style tasks where step count is
  systematically varied, plus length-calibrated training.
  **paper_url**: https://openreview.net/forum?id=6QDFsYxtI1
  **source**: extracted (from corpus motivation/method text) | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.motivation/method", "quote": "predicts an inverted U-shaped curve relating chain length to accuracy"}`

- **citation_key**: `[DEER, OpenReview:NpU7ZXafRi]` [GROUNDED:corpus]
  **approach_summary**: Training-free dynamic early exit for reasoning models: detects
  reasoning-transition boundaries during a single CoT trace, induces a trial answer at each
  boundary, and exits when the trial answer's confidence (geometric mean of answer-token
  probabilities) exceeds a threshold.
  **paper_url**: https://openreview.net/forum?id=NpU7ZXafRi
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "probe trial answers only at reasoning transition points"}`

- **citation_key**: `[DiffAdapt, OpenReview:644FH1vVIl]` [GROUNDED:corpus]
  **approach_summary**: Trains a lightweight MLP probe on prefill-stage final-layer hidden
  states to classify query difficulty into three regimes (Easy/Normal/Hard) — supervised by
  proxy-model sampling statistics (correctness + a U-shaped token-entropy pattern) — and
  selects one of three fixed reasoning strategies/budgets before any reasoning token is
  generated, keeping the base LLM frozen.
  **paper_url**: https://openreview.net/forum?id=644FH1vVIl
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "predicts problem difficulty from ... hidden states extracted during the prefilling stage"}`

- **citation_key**: `[AdaptiveThinking, OpenReview:2i6Rp0gCq6]` [GROUNDED:corpus]
  **approach_summary**: Predicts a query's expected self-consistency from its prefill
  hidden representation using a two-layer MLP adapter (trained offline against sampled
  self-consistency labels), and uses the predicted score as a reasoning-necessity proxy to
  decide whether and how much extended CoT to allocate.
  **paper_url**: https://openreview.net/forum?id=2i6Rp0gCq6
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "predicts the expected self-consistency of a query from its hidden representation before decoding begins"}`

- **citation_key**: `[CaTS, OpenReview:jrSc4RJXy1]` [GROUNDED:corpus]
  **approach_summary**: Distills multi-sample self-consistency agreement statistics into a
  single-pass calibrated correctness-confidence predictor via fine-tuning, then uses that
  confidence for early stopping of repeated sampling and confidence-weighted aggregation —
  replacing heuristic agreement thresholds of early-stopping self-consistency variants.
  **paper_url**: https://openreview.net/forum?id=jrSc4RJXy1
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "distilling self-consistency-derived agreement statistics into the model"}`

- **citation_key**: `[JET, OpenReview:2u5ZRzDyS0]` [GROUNDED:corpus]
  **approach_summary**: RL framework ("Just-Enough Thinking") that truncates the model's own
  rollouts at multiple intermediate points, inserts stop-thinking cues, and jointly optimizes
  full and truncated trajectories with a correctness-conditioned length reward, training the
  model to terminate reasoning once sufficient information has accumulated.
  **paper_url**: https://openreview.net/forum?id=2u5ZRzDyS0
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "construct shortened reasoning trajectories directly from the model's own generated chains"}`

- **citation_key**: `[FirstImpression, OpenReview:2PP70tFY0S]` [GROUNDED:corpus]
  **approach_summary**: Mechanistic account of overthinking: operationalizes an "internal
  bias" (the model's pre-reasoning answer distribution elicited by direct-answer prompting),
  measures bias-vs-reasoned-answer deviation, and runs counterfactual interventions (question
  removal after first intermediate answer; controlled bias injection) to test whether
  bias-reasoning conflict causally triggers repeated reflection.
  **paper_url**: https://openreview.net/forum?id=2PP70tFY0S
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "whether an implicit early answer estimate—internal bias—causally triggers excessive reflection"}`

- **citation_key**: `[ThinkingSpeed, OpenReview:ESELaMThLN]` [GROUNDED:corpus]
  **approach_summary**: Inference-time control of "thinking speed" via representation
  steering: extracts a fast–slow reasoning direction with contrastive PCA, injects it with
  controllable intensity, and adapts the intensity in real time using an early-vs-late-layer
  logit-divergence difficulty signal computed per generation step.
  **paper_url**: https://openreview.net/forum?id=ESELaMThLN
  **source**: extracted | **location**: `{"page": null, "section_title": "corpus ideas.jsonl — proposal.method", "quote": "steering internal representations along a fast–slow reasoning axis"}`

- **citation_key**: `[Muennighoff et al., 2025 (s1)]` **[NON-CORPUS, canonical]**
  **approach_summary**: "s1: Simple test-time scaling" — introduces *budget forcing*:
  externally truncating the thinking segment or appending "Wait" to force continued
  thinking, yielding a controllable test-time compute knob and near-monotonic scaling curves
  on math benchmarks. Referenced as `@muennighoff2025s1` in the motivation text of at least
  four corpus papers above ([ThinkingSpeed, OpenReview:ESELaMThLN], [JET, OpenReview:2u5ZRzDyS0]'s
  lineage, e3, Elastic Reasoning), which is why we are confident it exists.
  **source**: HYPOTHESIS-GROUNDED (real paper, arXiv 2501.19393; summary from general knowledge, not corpus text)
  **location**: `{"page": null, "section_title": "N/A — canonical anchor cited inside corpus motivation texts", "quote": "simple budget forcing can sometimes recover additional accuracy"}`

- **citation_key**: `[Chen et al., 2024 (Do NOT Think That Much)]` **[NON-CORPUS, canonical]**
  **approach_summary**: The empirical overthinking study of o1-like models ("Do NOT Think
  That Much for 2+3=?"): documents that reasoning models expend redundant solution rounds on
  easy problems with negligible or negative benefit, defines outcome/process efficiency
  metrics, and proposes training strategies to streamline reasoning. Referenced as
  `@chen2024overthinking` / `@chen2025overthinking` in the motivation text of nearly every
  corpus paper above, which is why we are confident it exists.
  **source**: HYPOTHESIS-GROUNDED (real paper, arXiv 2412.21187; summary from general knowledge, not corpus text)
  **location**: `{"page": null, "section_title": "N/A — canonical anchor cited inside corpus motivation texts", "quote": "excessive reasoning steps can degrade accuracy"}`

**Status:** FOUND (8 corpus-grounded works + 2 clearly-marked canonical anchors; each with an approach summary grounded in real text).

---

## N4 Prior Limitations

**grounding_check**: `true` [every limitation below cites at least one N3 citation_key,
verbatim string form; each is defensible from the cited paper's own motivation text or from
what its described method demonstrably does not cover]

- **limitation_text** [HYPOTHESIS]: "The inverted-U theory of CoT length is validated on
  controlled *synthetic* tasks where step count and difficulty are constructed variables;
  it does not measure where the sign-flip point lies on natural benchmarks stratified by an
  operational difficulty proxy, and offers no per-instance, inference-time predictor of the
  flip location from cheap signals." (Defensible from the paper's own method: components 2–3
  derive the optimal length theoretically and validate on 'synthetic reasoning datasets in
  which task difficulty is fixed'.)
  **affects_works**: `["[WhenMoreIsLess, OpenReview:6QDFsYxtI1]"]`
  **limitation_type**: `generalizability`
  **source**: inferred

- **limitation_text** [HYPOTHESIS]: "Stopping-rule methods optimize the *decision* to stop
  and validate end-to-end accuracy-cost tradeoffs, but never publish the underlying
  difficulty-conditioned boundary map they implicitly exploit — where the marginal return
  of thinking turns negative per difficulty stratum — and their signals are available only
  *during* generation (mid-trace confidence probes) or after fine-tuning, not as a pre-hoc
  characterization." (Defensible: DEER's confidence is computed at transition points inside
  an ongoing trace; CaTS requires distillation fine-tuning; DiffAdapt's own motivation says
  early-exit methods 'rely on signals observed during generation'.)
  **affects_works**: `["[DEER, OpenReview:NpU7ZXafRi]", "[CaTS, OpenReview:jrSc4RJXy1]"]`
  **limitation_type**: `other`
  **source**: inferred

- **limitation_text** [HYPOTHESIS]: "Pre-hoc difficulty probes predict coarse regimes — a
  3-class Easy/Normal/Hard label or a scalar self-consistency proxy — rather than a
  continuous tipping-point length, and neither validates its prediction against oracle
  accuracy-vs-length curves, so it is unknown how much of the achievable oracle tradeoff
  such probes recover." (Defensible from the methods: DiffAdapt selects among 'three
  computational regimes'; AdaptiveThinking predicts 'expected self-consistency' as a
  reasoning-necessity proxy.)
  **affects_works**: `["[DiffAdapt, OpenReview:644FH1vVIl]", "[AdaptiveThinking, OpenReview:2i6Rp0gCq6]"]`
  **limitation_type**: `precision`
  **source**: inferred

- **limitation_text** [HYPOTHESIS]: "Intervention approaches — RL training to stop earlier,
  or representation-steering of thinking speed — *presuppose* that a difficulty-dependent
  point exists where thinking stops paying, and change the model or its decoding to exploit
  it; because the intervention and the phenomenon are entangled, their results cannot be
  read as a measurement of where the boundary lies in an unmodified model."
  **affects_works**: `["[JET, OpenReview:2u5ZRzDyS0]", "[ThinkingSpeed, OpenReview:ESELaMThLN]", "[FirstImpression, OpenReview:2PP70tFY0S]"]`
  **limitation_type**: `other`
  **source**: inferred

- **limitation_text** [HYPOTHESIS]: "The canonical overthinking study documents redundant
  solution rounds mainly on *easy* problems and reports aggregate efficiency metrics; it
  does not estimate a difficulty-conditioned sign-flip location on an accuracy-vs-length
  curve, nor test whether that location is predictable from cheap pre-hoc signals."
  **affects_works**: `["[Chen et al., 2024 (Do NOT Think That Much)]"]`
  **limitation_type**: `precision`
  **source**: inferred

- **limitation_text** [HYPOTHESIS]: "Budget forcing demonstrates that thinking length is an
  externally controllable scaling knob, but applies budgets uniformly across queries; it
  reports aggregate scaling curves (including their flattening) without conditioning on
  difficulty, so it cannot say for which problems the forced extra thinking is the part
  that hurts." (Consistent with corpus papers' own critiques: ThinkingSpeed calls budget
  forcing 'coarse, unstable, and insensitive to local reasoning needs'.)
  **affects_works**: `["[Muennighoff et al., 2025 (s1)]"]`
  **limitation_type**: `generalizability`
  **source**: inferred

---

## N5 Challenges

**conflation_check**: `true` [four separable problem-inherent obstacles: observability of
difficulty, statistical change-point localization, proxy-signal validity, and intervention
validity]

- **C1** [HYPOTHESIS, tightly derived from core question]: "Difficulty is not directly
  observable for a fresh task instance — any difficulty-conditioned curve requires an
  operational proxy (e.g. empirical solve rate at a small fixed budget, or dataset-native
  difficulty tags), and every candidate proxy is both noisy and model-relative: the same
  item can be 'easy' for one model and 'hard' for another, so the stratification itself is
  an estimated quantity."
  location: `{"page": null, "section_title": "N/A — derived from core question", "quote": "N/A"}`
- **C2** [HYPOTHESIS]: "Accuracy at a given (stratum, length) cell is a Bernoulli mean over
  stochastic rollouts, so locating where the curve's *slope* changes sign is a change-point
  detection problem on differences of noisy proportions — the quantity of interest is a
  second-order feature of the data, requiring far more samples per cell than estimating
  accuracy itself."
- **C3** [HYPOTHESIS]: "Cheap signals such as output entropy or early-sample consistency
  are indirect proxies for eventual correctness; their mapping to the tipping point may
  fail to transfer across difficulty strata (a confidently-wrong easy-looking trajectory vs.
  a hesitantly-right hard one), across task domains, or across model families — and entropy
  itself co-varies with position in the trace, confounding signal with length."
- **C4** [HYPOTHESIS]: "There is a confound between thinking length as an *externally
  imposed* intervention (truncation / forced continuation) and thinking length as an
  *emergent* correlate of the model's own difficulty assessment — an externally truncated
  or extended chain is not the same object as a naturally short or long one, so causal
  claims about 'more thinking hurting' depend on which manipulation produced the length."

**Status:** all four are problem-inherent obstacles (pass the N4-vs-N5 test: they are about
why the *problem itself* is hard, not about what a named prior tool fails to do).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No paper exists to have stated these as its own challenges; C1–C4 are this document's own problem-inherent-obstacle analysis, derived from the core question rather than extracted from a Challenges section."
- why_matters: "A reader should not read C1–C4 as an author's self-assessment of difficulty; they are the scaffolding's prediction of what will be hard, used to justify M1–M5's design choices in N6."
- implication: "Re-derive N5 from the actual paper's stated challenges once written, and check whether any challenge the real authors name is missing from C1–C4 (a real paper may surface a C5 this scaffolding did not anticipate)."

---

## N6 Methodology

### Overview [HYPOTHESIS]

**Staged plan.**
- **Stage 0 — pilot (= the seed's minimal experiment).** One open reasoning model
  (e.g. DeepSeek-R1-Distill-Qwen-7B). MATH-500 with its native Level 1–5 tags crossed with
  a measured low-budget solve rate. Thinking budget controlled by truncation at a fixed
  grid L ∈ {256, 512, 1k, 2k, 4k, 8k, 16k tokens}; 8 rollouts per (item, L). Output:
  per-stratum accuracy-vs-length curves, first bootstrap test for a non-monotonic region,
  and a first pass of the entropy/early-consistency features on the same logs (no new
  generation needed for the signals — they are computed from prefixes of already-collected
  traces).
- **Stage 1 — scale-up.** Three models spanning scale/family (e.g. R1-Distill-Qwen-1.5B,
  R1-Distill-Qwen-7B/32B or a Qwen3 hybrid-thinking model); add GSM8K (easy anchor),
  AIME 2024/25 (hard anchor), GPQA-Diamond (non-math), and one synthetic family with a
  tunable difficulty parameter (e.g. Countdown / multi-digit arithmetic with controlled
  operand count) for clean stratification; 16 rollouts per cell; train and evaluate the
  cheap-signal predictor with cross-stratum and cross-domain holdouts; run the
  predictive-stopping policy comparison.

Per stage: (M1) stratify items by difficulty proxy; (M2) elicit traces at controlled
lengths, with a truncation arm, a forced-continuation arm, and a natural-stopping arm;
(M3) fit per-stratum curves and localize the tipping point L\* with a bootstrap slope-sign
change-point test; (M4) compute cheap pre-hoc features and fit a lightweight predictor of
L\*; (M5) evaluate predicted-stop vs fixed-budget vs oracle-stop vs a DEER-style
confidence-exit baseline on the accuracy-cost Pareto plane.

### Key Components

- **M1** — *Difficulty-stratified task suite* [HYPOTHESIS]: "Operationalize difficulty as
  the empirical solve rate at a small fixed budget — pass rate over 8 samples truncated at
  512 thinking tokens — computed per item, cross-checked against dataset-native tags (MATH
  levels; AIME item ordering) and against a *second* model's solve rate to detect
  model-specific stratification artifacts. Bin items into difficulty quintiles; report all
  boundary results per bin."
- **M2** — *Controlled-length generation harness* [HYPOTHESIS]: "Three length-control arms:
  (a) truncation — cut the thinking segment at L tokens, close it with the model's
  end-of-thinking delimiter, and force an answer ('Final Answer:'); (b) forced continuation
  — suppress the end-of-thinking token and append 'Wait' to extend traces beyond natural
  stopping (budget forcing à la [Muennighoff et al., 2025 (s1)]); (c) natural stopping —
  unconstrained generation, logged for observational curves. Instrument: a vLLM-based
  harness logging per-token logprobs (for M4's entropy features) at every rollout."
- **M3** — *Accuracy-curve & tipping-point estimator* [HYPOTHESIS]: "Per (stratum, L) cell,
  accuracy aggregated over items × rollouts with item-level clustered bootstrap CIs. The
  tipping point L\* is the smallest grid length at which the forward difference
  acc(L_{k+1}) − acc(L_k) is significantly negative (one-sided bootstrap test on the
  paired per-item difference, 10,000 resamples), reported with a bootstrap CI over L\*
  itself; a monotone-then-decreasing (unimodal isotonic) fit provides a continuous
  interpolated estimate between grid points."
- **M4** — *Cheap-signal feature set & predictor* [HYPOTHESIS]: "Features computable from
  the first 256 thinking tokens plus k=4 cheap probes: (i) entropy trajectory statistics
  (mean, slope, max of a 32-token sliding window of token-level predictive entropy);
  (ii) early consistency — agreement rate among k=4 answers forced at the 256-token
  truncation point; (iii) a prefill hidden-state probe (final-token, last-layer → 2-layer
  MLP), included explicitly as a reimplementation-style baseline of
  [DiffAdapt, OpenReview:644FH1vVIl] / [AdaptiveThinking, OpenReview:2i6Rp0gCq6]. Predictor:
  gradient-boosted regressor from features to log(L\*) bin, trained on one split of strata,
  evaluated on held-out strata and held-out domains — never requiring ground-truth labels
  at inference time."
- **M5** — *Predictive-stopping evaluation protocol* [HYPOTHESIS]: "Fix a token-cost grid
  and compare accuracy at matched mean cost for: (a) stop at M4's predicted L\*; (b) each
  fixed budget in the grid; (c) oracle per-stratum L\* (hindsight); (d) a
  confidence-based early-exit baseline in the style of [DEER, OpenReview:NpU7ZXafRi]
  (trial-answer confidence threshold at reasoning transitions). Report the fraction of the
  oracle-minus-best-fixed-budget accuracy gap recovered by (a)."

### Challenge Arguments

- **C1 ← [M1]** [HYPOTHESIS]: "M1 substitutes an operational, computable proxy (low-budget
  solve rate) for unobservable 'true' difficulty, and de-risks the proxy's model-relativity
  by triangulating with dataset-native tags and a second model's solve rate — addressing C1
  by measurement design rather than by assuming difficulty is knowable."
- **C2 ← [M2, M3]** [HYPOTHESIS]: "M2's fixed length grid with many rollouts per cell,
  combined with M3's item-level clustered bootstrap on *paired* per-item differences, is
  argued to give the slope-sign test enough power at stratum level to localize L\* despite
  Bernoulli noise — trading per-item resolution for statistically stable stratum-level
  change points."
- **C3 ← [M4, M5]** [HYPOTHESIS, partially addressed]: "M4 confronts the proxy-validity
  risk head-on by evaluating the predictor under cross-stratum and cross-domain holdouts
  (not just in-distribution fit), and M5 quantifies the *consequence* of proxy error as
  recovered oracle-gap fraction; transfer across model families remains validated only to
  the extent of the models tested."
- **C4 ← [M2]** [HYPOTHESIS, partially addressed]: "M2's three-arm design (truncation,
  forced continuation, natural stopping) lets the study report whether the negative-slope
  region appears under *multiple distinct* length manipulations and in observational
  natural-stopping data; agreement across arms is evidence the boundary is a property of
  the reasoning process rather than an artifact of one manipulation — but it does not fully
  identify the causal effect of 'the model choosing to think longer'."

### Unaddressed Challenges

- **[C4]** [HYPOTHESIS, explicitly retained despite the partial mitigation above]: "The
  intervention-vs-emergence confound is reduced by triangulation, not eliminated: no arm
  realizes the counterfactual 'the same model, unmodified, deciding to think longer on the
  same item.' Any causal reading of the tipping point remains qualified."
- **C3 is only partially addressed** (cross-family transfer of the predictor is out of
  scope for Stage 1) — per V-08, stated explicitly rather than implied.

### Feasibility [HYPOTHESIS]

- **Order of magnitude.** Pilot: 500 items × 7 budgets × 8 rollouts ≈ 28k generations at
  ≤16k thinking tokens each — worst case ~4.5×10⁸ generated tokens, but truncation-arm
  prefix sharing (a single 16k trace yields all shorter truncation points, with only the
  forced-answer suffixes regenerated per L) cuts effective generation to roughly
  ~6×10⁷–1×10⁸ tokens ≈ 100–300 A100/H100 GPU-hours for a 7B model (or low-thousands USD
  API class). Stage 1 is ~10× the pilot (3 models × ~4 datasets × 16 rollouts), i.e.
  low-thousands of GPU-hours — a 1–2 GPU-node, 4–8 week effort. Zero annotator-hours: all
  target benchmarks are auto-gradable (exact-match / numeric answers).
- **Single biggest feasibility risk.** For hard strata the negative-slope region may lie
  *beyond* the affordable budget range (curves still rising at 16k tokens), leaving the
  headline "difficulty-conditioned flip" claim supported only on easy/medium strata.
  **Mitigation**: the synthetic tunable-difficulty family (M1) guarantees strata where the
  flip is reachable at low budget; additionally, pre-register the fallback framing that a
  *right-censored* tipping point ('no flip observed below 16k') is itself a reportable
  boundary datum, and use the forced-continuation arm (cheaply extendable past natural
  stopping) to probe the region where degradation is most likely.

**Status:** PARTIAL (a pre-registered plan, not a report of methods actually run — no `B_pilot/` or `results/` exist yet).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No experiment has been executed; M1–M5, the staged plan, and the feasibility estimates are a pre-registered design, not a Methodology section describing completed work."
- why_matters: "Token/GPU-hour estimates and the feasibility risk are planning estimates that could be wrong in either direction once real generation logs exist; treating them as measured would misrepresent a plan as a result."
- implication: "Re-derive N6 from `B_pilot/` once the walking skeleton (paper.md Step 9) actually runs; any deviation between planned and actual cost/behavior belongs in `pipeline.md`'s phase log, not a silent edit here."

---

## N7 Contributions

- **CO1** [HYPOTHESIS] "A difficulty-conditioned boundary map: per-stratum
  accuracy-vs-thinking-length curves with statistically localized tipping points (or
  explicit right-censoring), showing whether and where the marginal return of test-time
  reasoning turns negative as a function of an operational difficulty proxy — on natural
  benchmarks and a synthetic tunable-difficulty family, under three distinct length-control
  manipulations."
  contribution_type: `empirical_finding`; is_testable: `true`; has_rq: `true` (RQ1, RQ_INF_1).
- **CO2** [HYPOTHESIS] "A lightweight, pre-hoc tipping-point predictor built from
  entropy-trajectory and early-consistency features computable within ~256 thinking tokens
  plus 4 cheap probes, validated under cross-stratum and cross-domain holdouts, usable
  without ground-truth correctness labels or the full reasoning budget at inference time."
  contribution_type: `technical_artifact`; is_testable: `true`; has_rq: `true` (RQ1, RQ_INF_2).
- **CO3** [HYPOTHESIS] "A quantification (predicted, not yet measured) of how much of the
  oracle accuracy-cost tradeoff predictive stopping recovers, relative to fixed budgets and
  a confidence-based early-exit baseline, at matched token cost."
  contribution_type: `empirical_finding`; is_testable: `true`; has_rq: `true` (RQ_INF_2).

**Status:** PARTIAL (claimed contributions of a paper not yet written; each is_testable/has_rq flag is a design commitment, not a verified property).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No completed paper exists to have delivered CO1–CO3; these are the contributions the pre-registered plan (paper.md Step 6) commits to producing."
- why_matters: "CO2's `technical_artifact` type is a classification choice (digest N12 flags it could reconsider to `tool` if the predictor becomes the released centerpiece) — readers should not treat contribution_type as settled until N9/N12 are re-checked against actual results."
- implication: "Re-derive N7 from `claim_map.md` once Phase D verdicts exist; a contribution whose H\* fails outright (not just downgrades) should be removed here, not left claiming success."

---

## N8 Research Questions

- **RQ1** [GIVEN, near-verbatim restatement of the seed's core question]: "At what
  difficulty condition does the marginal benefit of additional thinking (test-time
  reasoning) turn negative, and can this tipping point be predicted using cheap signals
  such as output entropy or early-answer consistency?"
  rq_source: `explicit` (directly given in seed 核心问题)
  evaluates_mechanisms: `[M2, M3, M4]` | addresses_challenges: `[C2, C3]` | tests_contributions: `[CO1, CO2]`
  answered_by_experiment: "The pilot + Stage-1 measurement: accuracy-vs-length curves per
  difficulty stratum under three length-control arms, bootstrap localization of L\*, then
  cheap-signal prediction of L\* under held-out strata/domains."
  location: `{"page": null, "section_title": "seed README — 核心问题", "quote": "估计难度达到什么条件时，更多思考的边际收益转负？翻转点可否用便宜信号预测？"}`

- **RQ_INF_1** [HYPOTHESIS, inferred — the minimal experiment's explicit stratification by
  difficulty implies a logically prior question]: "Is the tipping point itself
  difficulty-conditioned — does its location shift systematically (monotonically) across
  difficulty strata, rather than being a single fixed reasoning-length threshold?"
  rq_source: `inferred`
  evaluates_mechanisms: `[M1, M3]` | addresses_challenges: `[C1, C2]` | tests_contributions: `[CO1]`
  answered_by_experiment: "Comparing per-stratum L\* estimates (with CIs) across the five
  difficulty quintiles and across the synthetic family's difficulty parameter; trend test
  on L\* vs stratum rank."
  location: `{"page": null, "section_title": "seed README — 最小实验 (implied by '按难度分层')", "quote": "按难度分层的任务上测正确率-思考长度曲线的非单调区"}`

- **RQ_INF_2** [HYPOTHESIS, inferred — the seed's '翻转点可否用便宜信号预测' implies a
  deployment-facing consequence question]: "Does stopping at the predicted tipping point
  recover a substantial fraction of the oracle accuracy-cost tradeoff, and does it beat
  both the best fixed budget and a mid-trace confidence-based early-exit baseline at
  matched token cost?"
  rq_source: `inferred`
  evaluates_mechanisms: `[M4, M5]` | addresses_challenges: `[C3]` | tests_contributions: `[CO2, CO3]`
  answered_by_experiment: "M5 protocol: Pareto comparison of predicted-stop vs fixed
  budgets vs per-stratum oracle vs DEER-style confidence exit, at matched mean token cost."
  location: `{"page": null, "section_title": "seed README — 核心问题 (second clause)", "quote": "翻转点可否用便宜信号预测？"}`

**datasets** [HYPOTHESIS — concrete instantiations of the seed's abstract '按难度分层的任务'; none is named in the seed itself]:
names: `["MATH-500 (native Level 1–5 difficulty tags; auto-gradable numeric answers)", "GSM8K (easy-stratum anchor)", "AIME 2024 / AIME 2025 (hard-stratum anchor, 30 items/year — used for curves, not for per-item statistics)", "GPQA-Diamond (non-math domain-transfer check)", "a synthetic tunable-difficulty family (e.g. Countdown or multi-digit arithmetic with controlled operand count) for clean stratification"]`
source: inferred; location: `N/A — hypothesized`

**baselines** [HYPOTHESIS — named, drawn from N3 where possible]:
names: `["fixed thinking budgets at each grid point L ∈ {256 … 16k} (includes the always-max-budget policy)", "uniform budget forcing without difficulty conditioning, per [Muennighoff et al., 2025 (s1)]", "confidence-based dynamic early exit, DEER-style, per [DEER, OpenReview:NpU7ZXafRi]", "prefill hidden-state difficulty probe, per [DiffAdapt, OpenReview:644FH1vVIl] / [AdaptiveThinking, OpenReview:2i6Rp0gCq6] (as the pre-hoc predictor baseline)", "per-stratum oracle stopping (hindsight upper bound)"]`
source: inferred; location: `N/A — hypothesized`

**metrics** [HYPOTHESIS — each with a definition]:
names: `["accuracy@L — mean correctness over items × rollouts at truncation length L, per stratum", "tipping point L* — smallest grid L with significantly negative forward accuracy difference (bootstrap, one-sided)", "tipping-point localization error — |log2(L̂*) − log2(L*)| between predicted and oracle tipping points", "oracle-gap recovery — (acc(predicted-stop) − acc(best fixed budget)) / (acc(oracle-stop) − acc(best fixed budget)) at matched mean token cost", "token savings at matched accuracy — % reduction in mean thinking tokens vs always-max-budget at ≤1pp accuracy drop", "signal informativeness — AUROC of each cheap feature for classifying whether the marginal gain beyond the probe point is negative"]`
source: inferred; location: `N/A — hypothesized`

**analysis plan** [HYPOTHESIS]:
- Sample size: pilot ≥100 items per difficulty quintile (500 total) × 7 lengths × 8
  rollouts; Stage 1 ≥16 rollouts per cell; power heuristic — detecting a 5pp accuracy drop
  between adjacent grid lengths at α=0.05, power 0.8, needs ≈1,200 Bernoulli observations
  per cell, met by 100 items × 16 rollouts.
- Statistical tests: non-monotonicity per stratum via one-sided paired item-level bootstrap
  (10,000 resamples) on acc(L_peak) − acc(L_max), with Holm correction across the 5 strata ×
  3 arms; difficulty-conditioning (RQ_INF_1) via Jonckheere–Terpstra trend test on L\*
  across ordered strata; predictor quality via Spearman ρ between predicted and oracle L\*
  (item-level where estimable, else stratum-level), α=0.01; policy comparison (RQ_INF_2)
  via McNemar test on paired per-item correctness of predicted-stop vs best fixed budget at
  matched cost, α=0.05.
- Significance threshold: α=0.05 (Holm-corrected) unless stated; α=0.01 for the predictor
  correlation, since it underwrites the headline CO2 claim.
- Expected effect direction: negative slope beyond L\* on easy/medium strata; L\*
  increasing (or right-censored) with difficulty; predicted-stop > best fixed budget at
  matched cost.

**Status:** PARTIAL (RQ1/RQ_INF_1 near-verbatim from the seed; RQ_INF_2 and the datasets/baselines/metrics/analysis-plan blocks are inferred elaborations, not extracted from a written Research Questions section).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No written paper exists to state RQ_INF_1/RQ_INF_2 or to name the specific datasets/baselines/metrics; these are inferred to operationalize the seed's two-sentence core question into a testable plan."
- why_matters: "The named baselines (DEER, DiffAdapt/AdaptiveThinking, per-stratum oracle) and datasets (MATH-500, GSM8K, AIME, GPQA-D, synthetic) are this scaffolding's concrete choices, not commitments any existing paper has made — a real implementation could reasonably substitute different ones without breaking RQ1's intent."
- implication: "Re-derive N8 from the actual experiments run; if a named baseline proves inapplicable (e.g. DEER's confidence threshold doesn't transfer to a tested model), the substitution and its rationale belong in `pipeline.md`'s phase log, not a silent edit here."

---

## N9 Results — PLACEHOLDER / HYPOTHESIZED DIRECTION ONLY (no experiment has been run; no numbers exist)

- **Result 1** — rq_id: `RQ1`
  result_text [PLACEHOLDER — predicted direction, not a measured number]: "Predicted
  direction: on easy and medium difficulty strata, the accuracy-vs-length curve will
  exhibit a statistically significant negative-slope region within the 256–16k token grid,
  under at least the truncation and forced-continuation arms; the entropy-trajectory and
  early-consistency features will carry significant information about whether marginal
  gain beyond the probe point is negative (AUROC meaningfully above 0.5)."
  result_type: `quantitative` (intended); evidence_strength: `missing`; rq_answered: `false`.
  **FALSIFICATION CONDITION**: "Refuted if accuracy is monotonically non-decreasing in
  thinking length across ALL strata and ALL three length-control arms within the studied
  grid (Holm-corrected bootstrap finds no significantly negative forward difference
  anywhere), or if no cheap feature achieves AUROC significantly above 0.5 for the
  marginal-gain-sign classification — in which case the 'tipping point' premise fails in
  the studied regime and only a diminishing-returns (never negative-returns) account
  survives."

- **Result 2** — rq_id: `RQ_INF_1`
  result_text [PLACEHOLDER — predicted direction, not a measured number]: "Predicted
  direction: the localized tipping point L\* shifts systematically to longer lengths as
  stratum difficulty increases, with the hardest strata plausibly right-censored (no flip
  observed below 16k tokens); the trend holds on both natural benchmarks and the synthetic
  tunable-difficulty family."
  result_type: `quantitative` (intended); evidence_strength: `missing`; rq_answered: `false`.
  **FALSIFICATION CONDITION**: "Refuted if the Jonckheere–Terpstra trend test finds no
  significant ordering of L\* across difficulty strata (i.e., the flip point is
  statistically indistinguishable from a single universal length threshold), or if the
  ordering reverses between the natural and synthetic suites — either outcome would break
  the 'difficulty-conditioned boundary' claim even if non-monotonicity (Result 1) holds."

- **Result 3** — rq_id: `RQ_INF_2`
  result_text [PLACEHOLDER — predicted direction, not a measured number]: "Predicted
  direction: stopping at the predicted tipping point recovers a substantial fraction of
  the oracle-minus-best-fixed-budget accuracy gap at matched token cost, and outperforms
  both uniform budget forcing and the prefill-probe baseline; the DEER-style mid-trace
  confidence exit is the strongest baseline and may be competitive, with the predictor's
  advantage concentrated where confidence signals emerge late."
  result_type: `quantitative` (intended); evidence_strength: `missing`; rq_answered: `false`.
  **FALSIFICATION CONDITION**: "Refuted if predicted-stop is not significantly better than
  the best single fixed budget at matched cost (McNemar, α=0.05), or if it recovers no
  larger share of the oracle gap than the coarse 3-class prefill-probe baseline — i.e., the
  cheap signals carry no usable information about the tipping point beyond
  difficulty-bin membership alone."

---

## N10 Threats / Self-Limitations

[HYPOTHESIS — anticipated limitations of this kind of study; no paper exists to have
actually acknowledged these, so all are forward-looking predictions, not author statements.
Each carries a validity category and a planned mitigation.]

- **t1** [category: `internal`]: "Externally forcing or truncating reasoning length is not
  the same intervention as the model electing to think longer; degradation observed under
  truncation+forced-answer could partly be a prompt-format artifact (an abruptly closed
  thinking segment) rather than a property of extended reasoning."
  mitigation: "Three-arm triangulation (M2): report curves separately for truncation,
  forced continuation, and natural stopping; only claim a boundary where at least two arms
  agree in sign."
- **t2** [category: `construct`]: "'Difficulty' is operationalized as the study model's own
  low-budget solve rate, which is circular in the worst case — the stratifier and the
  measured curves come from the same model, so strata may encode model idiosyncrasies
  rather than task difficulty."
  mitigation: "Cross-check strata against dataset-native tags (MATH levels) and a second
  model's solve rate (M1); report agreement (rank correlation) between the three
  stratifications, and replicate headline curves under the tag-based stratification."
- **t3** [category: `external`]: "Findings may be specific to the tested model
  scales/families and to math-heavy, auto-gradable domains; open-ended or agentic tasks —
  where correctness is not exact-match — are untested, and the predictor's cross-family
  transfer is out of scope."
  mitigation: "Stage 1 spans three model scales and at least one non-math benchmark
  (GPQA-Diamond) plus a synthetic family; cross-family transfer is explicitly declared out
  of scope rather than silently claimed."
- **t4** [category: `conclusion`]: "Tipping-point localization from noisy Bernoulli curves
  invites both false positives (multiple comparisons across strata × arms × datasets) and
  false negatives (underpowered cells, especially AIME with ~30 items/year); interpolated
  L\* between grid points inherits grid-resolution bias."
  mitigation: "Holm correction across the stratum × arm family; power-based minimum cell
  size (≈1,200 observations); AIME reported as curves only, excluded from per-item
  statistics; L\* always reported with bootstrap CIs and the grid disclosed as a
  resolution limit."
- **t5** [category: `construct`]: "Entropy-trajectory features co-vary mechanically with
  position in the trace and with tokenizer/vocabulary choices, so the predictor may learn
  a length-proxy rather than a difficulty-relevant uncertainty signal."
  mitigation: "Include position-controlled features (fixed 256-token window for all items),
  ablate each feature family (entropy-only vs consistency-only vs prefill-probe-only), and
  test whether the predictor beats a length-only null feature set."

**Status:** PARTIAL — these are anticipated, not author-acknowledged (no author exists yet).
**Absence comment:**
- what_missing: "No actual Threats-to-Validity or Limitations section exists because no paper has been written; the items above are reviewer-style anticipations with planned mitigations, not author admissions."
- why_matters: "A reader should not treat t1–t5 as evidence the (nonexistent) authors were self-aware about these issues — they are this document's own risk forecast and design commitments."
- implication: "Re-derive N10 from the actual paper's Limitations section once written; t1–t5 double as a design checklist the experiments should bake in from the start (three-arm control, dual stratification, Holm correction, length-null ablation)."

---

## N11 Artifacts

**Status:** NOT_FOUND [PLACEHOLDER — nothing has been released because the paper does not exist].
artifacts: `[]`
has_code: `false` | has_data: `false` | has_model: `false`

**Absence comment:**
- what_missing: "No code repository, dataset, model, or demo has been released or promised, because no paper or implementation exists yet."
- why_matters: "A reviewer relying on this digest should not assume reproducibility artifacts are forthcoming — there is no statement of intent to release anything, since there is no manuscript."
- implication: "If executed, the natural artifacts would be (a) the length-controlled generation logs with per-token logprobs (the expensive, reusable asset), (b) the curve/change-point analysis code, and (c) the trained cheap-signal predictor; revisit N11 once these exist."

---

## N12 Contribution Type

**value** [HYPOTHESIS]: `empirical`

**rationale** [HYPOTHESIS]: "The envisioned paper's core validation (N9) is a measurement
of an existing phenomenon — the difficulty-conditioned shape of the accuracy-vs-length
curve and the location of its sign flip — in unmodified, off-the-shelf reasoning models,
under controlled manipulations, exactly the shape of prior best-paper empirical studies
of boundary phenomena (cf. 'LLMs Get Lost in Multi-Turn Conversation', 'Are Emergent
Abilities a Mirage?'): existing models, a purpose-built measurement harness, and a
characterization finding as the headline. The tipping-point predictor (M4/CO2) is a small
analysis instrument in service of the empirical claim — analogous to the aptitude/
unreliability decomposition metrics of the Lost-in-Conversation study — not a system or
tool release with an independent evaluation story; the synthetic task family is
instrumentation, not a benchmark contribution. This matches the `empirical` disambiguation
hint: 'a measurement study with a published dataset is `empirical` if the study is the main
contribution' — here the study (where thinking starts to hurt) is unambiguously the headline.
Re-check against actual N9 once results exist: if the predictor were to become the released,
independently-evaluated centerpiece, `tool` would need reconsideration."

**source**: inferred (a prediction of how such a paper would self-classify; no actual N9
results exist to classify against).

**Status:** PARTIAL (a predicted self-classification, not a report of an actual paper's stated type).
**Absence comment** *(added at Phase A re-run, 2026-07-04)*:
- what_missing: "No actual paper exists to have classified itself; `empirical` is this scaffolding's best-guess classification, reasoned by analogy to two named exemplars that were themselves absent from the reference cache until the Phase A re-run backfilled them (`EmergentMirage2304`, `LostInMultiTurn2505` in `reference_candidates.jsonl`)."
- why_matters: "The archetype gates the entire evidence standard (guidance.md Part 2 A2 vs A1/A6); a wrong classification here would misapply the wrong reviewer-kill checklist to the whole plan."
- implication: "Re-check N12 against `paper.md` Step 2's archetype declaration whenever the method (M1–M6) or contribution list (N7) changes materially; the two exemplars now being real cache entries means their evidence *shape* (not just their name) can and should be imitated per guidance.md Part 2, not just cited by analogy."

---

## Claims

- [HYPOTHESIS] "The marginal benefit of additional test-time reasoning becomes negative
  beyond a difficulty-dependent length — overthinking-induced accuracy loss is not uniform
  across tasks but conditioned on task difficulty." — evidence: argument (N2 motivation;
  the inverted-U *theory* of `[WhenMoreIsLess, OpenReview:6QDFsYxtI1]` predicts exactly
  this, but on synthetic tasks — N4 limitation 1) + predicted result (N9 Result 1/2);
  source: inferred; location: `N/A — hypothesized`.
- [HYPOTHESIS] "No prior work publishes the difficulty-conditioned boundary map that the
  entire adaptive-reasoning literature implicitly exploits: stopping rules
  (`[DEER, OpenReview:NpU7ZXafRi]`, `[CaTS, OpenReview:jrSc4RJXy1]`), pre-hoc probes
  (`[DiffAdapt, OpenReview:644FH1vVIl]`, `[AdaptiveThinking, OpenReview:2i6Rp0gCq6]`), and
  training interventions (`[JET, OpenReview:2u5ZRzDyS0]`) all *presuppose* the boundary
  without measuring it." — evidence: argument (N4 limitations 2–4, each defensible from
  the cited papers' own method descriptions); source: inferred; location: `N/A — hypothesized`.
- [HYPOTHESIS] "Cheap, pre-hoc signals (entropy trajectories over the first ~256 thinking
  tokens, agreement among 4 truncated-answer probes) carry enough information to predict
  the difficulty-conditioned tipping point without ground-truth labels or the full budget
  — and this must be shown to beat a length-only null feature set and a coarse prefill
  probe, or the claim collapses to 'difficulty bins suffice'." — evidence: argument (N6 M4,
  N10 t5) + predicted result (N9 Result 3); source: inferred.
- [PLACEHOLDER] "Predictive early-stopping at the predicted tipping point recovers a
  substantial fraction of the oracle accuracy-cost tradeoff at meaningfully lower token
  cost than always-max-budget." — evidence: none yet (no experiment run); this is the
  quantitative claim N9 Result 3 would need to substantiate and currently carries
  `evidence_strength="missing"`.
- [HYPOTHESIS] "The tipping point is not a single universal reasoning-length threshold but
  shifts systematically with problem difficulty (possibly right-censored on the hardest
  strata), arguing against one-size-fits-all thinking-budget policies — including uniform
  budget forcing per `[Muennighoff et al., 2025 (s1)]` — in reasoning-economics systems."
  — evidence: argument (N5 C1, N8 RQ_INF_1, N4 limitation 6) + predicted result (N9
  Result 2); source: inferred; location: `N/A — hypothesized`.
