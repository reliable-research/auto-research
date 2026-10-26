# Digest: Can a Frozen Probe Replace Self-Report? Cheap Controllers for Compute Allocation

> **REVERSE-DIGEST DISCLAIMER.** No paper exists for this topic yet. This is speculative
> scaffolding for research planning, built from a seed idea (title + core question + minimal
> experiment) under topic code **B4.4** ("廉价控制器蒸馏" / Cheap Controller Distillation,
> label `[资源]`, parent topic "B4. 预算分配 / 推理经济学"). Every field below is tagged:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README.
> - **[HYPOTHESIS]** — reasoned elaboration/prediction, not a fact.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is actually done.
> - **[GROUNDED:corpus]** — a real OpenReview paper retrieved from the local corpus
>   (`topics/corpus/ideas.jsonl`, 11,683 papers); the paper is real, its *fit* to this
>   future paper's lineage is this digest's judgment call.

---

## N0 — Metadata

- **title** [GIVEN]: "Can a Frozen Probe Replace Self-Report? Cheap Controllers for Compute Allocation" (from seed README line 16).
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper/authors exist yet.
- **abstract** [HYPOTHESIS] (explicitly a draft, not a real abstract — synthesized from the seed's core question + minimal experiment):
  > "Adaptive compute allocation for large language models (LLMs) often relies on the model's
  > own self-reported confidence — a verbalized certainty or an elicited probability — to
  > decide how much reasoning budget a query deserves. Self-report requires an additional
  > model call and inherits the calibration failures of the underlying LLM. This paper asks
  > whether a small probe trained on frozen-backbone hidden states from a single prefill
  > pass can serve as a compute-allocation controller at near-zero marginal cost, matching
  > or exceeding both large-model self-report and purely training-free signals (logit
  > entropy, self-consistency agreement). We compare all three controller families on
  > accuracy-per-dollar under matched total budgets across reasoning benchmarks of varying
  > difficulty. [DRAFT — synthesized, not extracted from a real abstract.]"
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` — LLM inference economics / compute allocation.
- **status**: PARTIAL — title given; authors/abstract are placeholder/draft only.
- **absence_comment**: {what_missing: "No real authors or verbatim abstract exist because the paper has not been written.", why_matters: "A reader must not mistake the drafted abstract above for a real one when using this digest for planning.", implication: "Treat N0 authorship/abstract as scaffolding only; replace wholesale once a real manuscript exists."}

---

## N1 — Problem Formulation

- **objective** [HYPOTHESIS], built as a full predicate from the seed's core question ("一个小型冻结骨干探针做分配决策，能否达到大模型自我报告式元决策的水平？training-free 信号够不够？"):
  > "evaluate, under matched inference budgets, whether a small probe trained on frozen
  > LLM hidden states extracted at prefill time can allocate per-query compute (route each
  > query to a cheap or expensive execution tier) as effectively as (a) large-model
  > self-reported confidence and (b) training-free signals (logit entropy, self-consistency
  > agreement), measured by accuracy achieved per unit dollar cost on exact-answer reasoning
  > benchmarks spanning multiple difficulty levels."
  Self-check: kind of task = comparative controller-evaluation/measurement study; domain =
  LLM inference-time compute allocation over reasoning tasks; outcome shape = matched-budget
  accuracy and cost–accuracy curves across three controller families. All three land.
- **inputs** [HYPOTHESIS], inferred from the minimal experiment ("对比 training-free 信号（logit 熵、自洽度）、小探针、大模型自报三种控制器在同预算下的 accuracy-per-dollar"):
  1. Query text from an exact-answer reasoning benchmark (programmatically scorable).
  2. Frozen-backbone hidden states / logits from a single prefill forward pass (feeds the probe and the entropy signal).
  3. k sampled generations per query from the cheap tier (feeds the self-consistency signal and probe training labels).
  4. A large-model self-report elicitation (verbalized 0–100 confidence and/or P(True)-style logprob).
  5. A fixed total dollar budget shared identically across all controllers.
- **outputs** [HYPOTHESIS]:
  1. A per-query routing decision (cheap vs. expensive compute tier).
  2. Accuracy at matched budget and accuracy-per-dollar, per controller.
  3. Signal-quality diagnostics (AUROC of each controller signal against cheap-tier correctness; calibration).
- **constraints** [GIVEN] (from the minimal experiment's explicit "同预算下"): the three controllers must be compared under an identical total budget; [HYPOTHESIS] this requires (i) automatically checkable per-query correctness so any routing decision's downstream accuracy is scorable, and (ii) a cost accounting that charges each controller its own signal-acquisition cost (extra call, extra samples), not just the routed generation cost.
- **status**: PARTIAL (objective/inputs/outputs are inferred, not stated in full formulation form in the seed).
- **absence_comment**: {what_missing: "The seed README states only a one-sentence core question and a one-sentence minimal experiment, not a full formal problem statement.", why_matters: "Without reconstruction, a reader cannot see the full input/output/constraint shape needed to plan the experiment.", implication: "Treat inputs/outputs/objective above as a conservative, closely-grounded reconstruction, not a verbatim quote."}

---

## N2 — Motivation

**motivations** (`list[MotivationItem]`):

- **motivation_text** [HYPOTHESIS], reconstructed from the seed's `parent_topic` ("B4. 预算分配 / 推理经济学" = "Budget Allocation / Inference Economics") and grounded in the corpus literature:
  > "Test-time compute scaling makes per-query budget decisions economically material:
  > uniform allocation wastes computation on easy queries while under-serving hard ones
  > (a gap documented across the adaptive-reasoning literature, e.g. [DiffAdapt,
  > OpenReview:644FH1vVIl]'s motivation that test-time scaling 'allocates large reasoning
  > budgets uniformly across queries regardless of their actual difficulty'). The two
  > dominant controller families sit at opposite cost extremes: large-model self-report
  > costs an extra generation call and inherits the base model's calibration failures,
  > while training-free signals like self-consistency require multiple sampled generations
  > before any budget is saved. If a frozen-backbone probe — one prefill pass plus a tiny
  > head — matches their decision quality, the controller itself stops being a budget item."
  - source: hypothesis
  - evidence: [{type: "citation", text: "[DiffAdapt, OpenReview:644FH1vVIl] motivation: adaptive-reasoning methods either 'require expensive retraining' or 'rely on signals observed during generation, meaning that some reasoning tokens must already be produced before inefficiencies can be detected'", source: "GROUNDED:corpus", location: "https://openreview.net/forum?id=644FH1vVIl"}]
- **status**: PARTIAL — no real motivation section exists; the reconstruction is anchored to real corpus papers rather than invented statistics.
- **absence_comment**: {what_missing: "No actual Introduction/Motivation section exists because no paper has been written.", why_matters: "A reviewer should not treat this as a claim the (nonexistent) authors have made.", implication: "Use this only to judge whether the idea is well-motivated in principle, not as evidence a real paper argues this."}

---

## N3 — Related Works

Grounding: a real corpus search was run over `topics/corpus/ideas.jsonl` (11,683 OpenReview
papers) with five query angles — (1) "linear probe; hidden states; probing; correctness
prediction; internal representations", (2) "adaptive compute allocation; test-time compute;
early exit; dynamic inference budget; routing", (3) "verbalized confidence; calibration;
uncertainty estimation; self-report; know what they know", (4) "cascade; router; cheap
model; expensive model; cost aware; budget", (5) "self-consistency; adaptive sampling;
number of samples; entropy; overthinking; reasoning length" (+ a hallucination/difficulty
follow-up). Full motivation+method text of the top hits was read before inclusion. All
`approach_summary` text below is grounded in each paper's own proposal text.

**works** (`list[RelatedWork]`):

1. **citation_key**: `[DiffAdapt, OpenReview:644FH1vVIl]` [GROUNDED:corpus]
   **approach_summary**: Trains a lightweight MLP probe on the final-layer hidden state
   produced after prefilling the question (base LLM frozen) to classify query difficulty
   into Easy/Normal/Hard, then executes the matching reasoning configuration — proactive,
   training-free-for-the-backbone compute allocation before any reasoning token is
   generated; supervision comes from proxy-model sampling (correctness + entropy statistics
   of multiple traces).
   **paper_url**: https://openreview.net/forum?id=644FH1vVIl
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

2. **citation_key**: `[AdaptiveThinking, OpenReview:2i6Rp0gCq6]` [GROUNDED:corpus]
   **approach_summary**: Trains a two-layer MLP adapter that maps the final-token,
   last-layer hidden representation extracted during prefilling to a predicted
   self-consistency score, turning an expensive sampling-based diagnostic into a fast
   latent-space prediction that decides whether extended chain-of-thought is performed and
   how much compute is allocated; labels are computed offline by repeated sampling on a
   calibration set.
   **paper_url**: https://openreview.net/forum?id=2i6Rp0gCq6
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

3. **citation_key**: `[CaTS, OpenReview:jrSc4RJXy1]` [GROUNDED:corpus]
   **approach_summary**: Distills self-consistency-derived agreement statistics into the
   model via fine-tuning so it outputs calibrated correctness confidence in one pass, then
   uses that confidence for early stopping and confidence-aware aggregation of repeated
   sampling — replacing fixed-sample self-consistency with adaptive, calibrated allocation.
   **paper_url**: https://openreview.net/forum?id=jrSc4RJXy1
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

4. **citation_key**: `[DiSRouter, OpenReview:KDcwXKr0NU]` [GROUNDED:corpus]
   **approach_summary**: Replaces a centralized external router with distributed
   self-routing: each model in a cost-ordered cascade is trained (SFT on its own empirical
   success frequency, then RL with scenario-conditioned rewards) to either answer or
   explicitly refuse and forward the query to the next stronger model — i.e., an
   operationalized, trained form of self-report as the allocation decision.
   **paper_url**: https://openreview.net/forum?id=KDcwXKr0NU
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

5. **citation_key**: `[TRIM, OpenReview:MoKrugWUfC]` [GROUNDED:corpus]
   **approach_summary**: Routes at the reasoning-step level: a weak model drafts each step,
   a process-reward-model score plus trajectory statistics estimate risk, and a
   budget-aware threshold (or learned sequential policy) decides whether the strong model
   regenerates that step — allocating expensive compute only at likely failure points under
   a constrained strong-model token budget.
   **paper_url**: https://openreview.net/forum?id=MoKrugWUfC
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

6. **citation_key**: `[LimitedMetacognition, OpenReview:gb9HR8hxtU]` [GROUNDED:corpus]
   **approach_summary**: Behaviorally tests whether LLMs can *use* internal confidence
   rather than merely report it: in an incentive-compatible Delegate Game the model chooses
   to answer or delegate to a teammate, and delegation decisions are analyzed against
   baseline correctness and answer-token entropy while controlling for surface cues —
   finding evidence that self-reports may be largely imitative rather than evidential.
   **paper_url**: https://openreview.net/forum?id=gb9HR8hxtU
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

7. **citation_key**: `[KV-Embeddings, OpenReview:GUhmiJaAzv]` [GROUNDED:corpus]
   **approach_summary**: Pools cached key/value tensors across heads, layers, and positions
   into compact "KV-Embeddings" and trains a lightweight MLP difficulty estimator on them
   for fast/slow reasoning routing, arguing hidden-state probing's utility can be preserved
   while removing most of its storage and deployment cost because the KV cache is already
   produced during decoding.
   **paper_url**: https://openreview.net/forum?id=GUhmiJaAzv
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

8. **citation_key**: `[TPC, OpenReview:AGWa8whf92]` [GROUNDED:corpus]
   **approach_summary**: Extends linear activation-space probes to Truncated Polynomial
   Classifiers whose degree-wise terms can be evaluated incrementally, giving a monitor
   whose compute cost scales dynamically at inference — motivated by the overhead of
   LLM-based monitors and the limited capacity of purely linear probes.
   **paper_url**: https://openreview.net/forum?id=AGWa8whf92
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

9. **citation_key**: `[RouterArena, OpenReview:9HsaIi4ngF]` [GROUNDED:corpus]
   **approach_summary**: An open evaluation platform for LLM routers: a domain-diverse
   dataset with empirically calibrated difficulty levels (difficulty = fraction of models
   answering correctly), plus multi-dimensional metrics covering accuracy, inference cost,
   routing optimality (cheapest correct model chosen), robustness, and routing latency,
   evaluated through live inference.
   **paper_url**: https://openreview.net/forum?id=9HsaIi4ngF
   **source**: GROUNDED:corpus; **location**: proposal.motivation/method, ideas.jsonl.

10. **citation_key**: `[Kadavath et al., 2022]` **[NON-CORPUS — canonical, clearly marked]**
    **approach_summary**: "Language Models (Mostly) Know What They Know" (arXiv:2207.05221)
    — shows LLM self-evaluation signals (P(True) on proposed answers, elicited confidence)
    correlate with correctness and are reasonably calibrated at scale; the canonical
    first-party source for self-report/verbalized confidence as a usable meta-decision
    signal. Included from general knowledge with high confidence; not retrieved from the
    local corpus (the corpus papers above cite it as @kadavath2022know).
    **paper_url**: https://arxiv.org/abs/2207.05221
    **source**: HYPOTHESIS (canonical, non-corpus); **location**: N/A.

- **status**: PARTIAL — all entries are real papers with grounded summaries, but the set is
  this digest's reconstruction of the lineage, not an actual related-work section.
- **absence_comment**: {what_missing: "No authored related-work section exists; the lineage above is assembled by corpus search rather than extracted from a manuscript.", why_matters: "A reviewer should treat the selection (not the papers) as a judgment call that the eventual paper may revise.", implication: "When the paper is written, re-derive N3 from its actual Related Work section; the corpus entries above are strong candidate citations for it."}

---

## N4 — Prior Limitations

**limitations** (`list[Limitation]`), each [HYPOTHESIS] but defensible from the cited
paper's own motivation text or from what its method demonstrably does not cover:

1. **limitation_text**: "Hidden-state probe controllers in [DiffAdapt, OpenReview:644FH1vVIl] and [AdaptiveThinking, OpenReview:2i6Rp0gCq6] are validated against fixed-budget or heuristic reasoning baselines within one backbone's own reasoning modes; neither benchmarks the probe head-to-head against large-model self-reported confidence as a controller, and neither reports results in a matched-dollar-budget, accuracy-per-dollar frame — their headline currency is token savings at preserved accuracy."
   **affects_works**: ["[DiffAdapt, OpenReview:644FH1vVIl]", "[AdaptiveThinking, OpenReview:2i6Rp0gCq6]"]
   **limitation_type**: generalizability
   **source**: hypothesis

2. **limitation_text**: "[CaTS, OpenReview:jrSc4RJXy1] obtains its one-pass confidence by fine-tuning the base model (confidence distillation with a joint language-modeling objective), so the backbone is not frozen — the approach is unavailable when weights cannot be modified (API models, shared serving stacks) and its training cost is charged to every new backbone."
   **affects_works**: ["[CaTS, OpenReview:jrSc4RJXy1]"]
   **limitation_type**: efficiency
   **source**: hypothesis

3. **limitation_text**: "[DiSRouter, OpenReview:KDcwXKr0NU] concedes in its own motivation that 'intrinsic self-awareness is present but not sufficiently calibrated in open models for routing-quality decisions', and therefore trains every model in the pool with SFT plus RL to instill answer-or-forward behavior — a per-model training investment that a frozen-probe controller would avoid entirely."
   **affects_works**: ["[DiSRouter, OpenReview:KDcwXKr0NU]"]
   **limitation_type**: efficiency
   **source**: hypothesis

4. **limitation_text**: "[TRIM, OpenReview:MoKrugWUfC]'s controller signal is a process reward model evaluated after every drafted step, so the controller itself is a separately trained model with non-trivial per-step inference cost, and the method is scoped to decomposable multi-step (mathematical) reasoning traces rather than generic per-query allocation."
   **affects_works**: ["[TRIM, OpenReview:MoKrugWUfC]"]
   **limitation_type**: efficiency
   **source**: hypothesis

5. **limitation_text**: "[Kadavath et al., 2022] establish that self-evaluation correlates with correctness, and [LimitedMetacognition, OpenReview:gb9HR8hxtU] shows models often fail to deploy that signal behaviorally when a decision depends on it ('strong self-reports may be largely imitative rather than evidential'); neither work prices the elicitation call itself or compares self-report against internal-state probes as budget-constrained compute controllers."
   **affects_works**: ["[Kadavath et al., 2022]", "[LimitedMetacognition, OpenReview:gb9HR8hxtU]"]
   **limitation_type**: other
   **source**: hypothesis

6. **limitation_text**: "[KV-Embeddings, OpenReview:GUhmiJaAzv] motivates its representation by the memory/deployment cost of full hidden-state probing and shows KV-cache features support difficulty estimation, but its comparison set is hidden-state methods and trajectory-search controllers — training-free signals and self-report are not evaluated as competing controllers under a shared budget."
   **affects_works**: ["[KV-Embeddings, OpenReview:GUhmiJaAzv]"]
   **limitation_type**: generalizability
   **source**: hypothesis

7. **limitation_text**: "[TPC, OpenReview:AGWa8whf92] targets safety monitoring, not compute allocation: its probes classify harmfulness rather than expected correctness/difficulty, and its own motivation notes that cascading cheap probes with LLM monitors 'introduces architectural complexity and requires additional models at inference time' — the very overhead a single-signal allocation study must quantify."
   **affects_works**: ["[TPC, OpenReview:AGWa8whf92]"]
   **limitation_type**: generalizability
   **source**: hypothesis

8. **limitation_text**: "[RouterArena, OpenReview:9HsaIi4ngF] evaluates routers that choose *between models*, with metrics for cost, optimality, and latency; it does not evaluate within-model compute-tier controllers (reasoning depth / sample count) nor treat entropy, self-consistency, probes, and self-report as interchangeable controller signals under one matched budget."
   **affects_works**: ["[RouterArena, OpenReview:9HsaIi4ngF]"]
   **limitation_type**: generalizability
   **source**: hypothesis

- **grounding_check**: `true` — every limitation's `affects_works` entries match N3 `citation_key` strings verbatim.
- **status**: PARTIAL (limitations are reasoned relative to this idea's core question, anchored in the cited papers' own motivation text where quoted, not extracted from a manuscript of this paper).
- **absence_comment**: {what_missing: "None of the N3 works frames itself around the three-way probe vs. self-report vs. training-free controller comparison, so no verbatim 'prior methods fail to X' statement about this exact gap exists.", why_matters: "A reader needs to know these are inferred gaps relative to this idea, not quoted admissions.", implication: "Read N4 as 'what these adjacent works demonstrably do not cover, relative to this idea's matched-budget comparison,' and re-verify each against the cited paper before citing it in a manuscript."}

---

## N5 — Challenges

**challenges** (`list[Challenge]`), all [HYPOTHESIS but tightly derived] from the core
question itself (problem-inherent, not "prior tool X fails"). Ids kept stable from the
previous digest revision:

- **C1**: "Benchmarking 'accuracy-per-dollar' requires per-query correctness that is knowable independently of which controller routed the query — i.e., a task suite with automatic, exact-match-scorable ground truth — and the probe additionally needs correctness-labeled training queries, so label acquisition is a structural cost of the comparison itself, not an implementation detail."
  source: hypothesis
- **C2**: "The three controller families have intrinsically different signal-acquisition costs (probe: one prefill pass + tiny head, amortized training; self-consistency: k extra sampled generations; self-report: one extra large-model call), so a genuinely fair 'same total budget' comparison must charge each controller its own signal cost — including amortized training — before any routing saving is counted, which no single operating point can settle."
  source: hypothesis
- **C3**: "A probe reads features at a fixed layer of one frozen backbone trained on one task distribution, so any separability it exploits may be backbone-, layer-, and distribution-specific — the transfer question is inherent to the frozen-feature design, independent of how well the probe is trained."
  source: hypothesis
- **C4**: "Compute-allocation decisions must be made before the answer is known: every controller (probe, entropy, self-consistency, self-report) estimates a latent quantity — this query's expected correctness under a given compute tier for this model — rather than observing it, an estimation-under-uncertainty obstacle no controller design can escape."
  source: hypothesis

- **conflation_check**: `true` — C1 (label economics), C2 (cost commensurability of the controllers themselves), C3 (frozen-feature specificity/transfer), C4 (pre-hoc latent-difficulty estimation) are distinct obstacles.
- **status**: PARTIAL — derived from the core question, not stated by any existing paper's "a major challenge is..." language (none exists yet).
- **absence_comment**: {what_missing: "No paper text exists to quote a challenges paragraph from.", why_matters: "A reader must know these are reasoned obstacles inherent to the problem, not verbatim author claims.", implication: "Use C1–C4 as the design constraints the method sketch (N6) must argue it addresses."}

---

## N6 — Methodology

**overview** [HYPOTHESIS]:
> "The study compares three per-query compute-allocation controller families under matched
> total dollar budgets, using a precompute-then-simulate design: for every evaluation query,
> both execution tiers (cheap: direct answer, no chain-of-thought; expensive: CoT with
> self-consistency over k samples, or a larger model) and all controller signals are
> computed **once** and cached, so any routing policy and any budget point can be evaluated
> offline, exactly, without re-running models. **Staged plan.** *Stage 1 (pilot — the
> seed's minimal experiment):* one backbone pair (e.g., Qwen2.5-7B-Instruct cheap tier vs.
> Qwen2.5-72B-Instruct or GPT-4o-class expensive tier), two benchmarks (GSM8K, MMLU-Pro),
> ~2,000 evaluation queries per benchmark, three controllers (training-free suite, frozen
> probe, self-report), reporting matched-budget accuracy and accuracy-per-dollar. *Stage 2
> (scale-up):* add MATH-500, GPQA-Diamond, and BIG-Bench-Hard; add a second backbone family
> (e.g., Llama-3.1-8B/70B); add cross-task and cross-backbone probe-transfer conditions and
> a full budget sweep tracing each controller's cost–accuracy curve."
source: hypothesis; location: N/A (no paper text exists).

**key_components** (`list[MethodKeyComponent]`), ids assigned before `challenge_arguments`:

- **M1** — name: "Training-free signal suite"; text: "Two signals with zero training cost: (a) mean token-level logit entropy over the cheap tier's answer tokens (and, for multiple-choice tasks, predictive entropy over answer options from a single pass); (b) self-consistency agreement rate = modal-answer frequency among k=8 cheap-tier samples at temperature 0.8 (following the agreement-rate usage that [AdaptiveThinking, OpenReview:2i6Rp0gCq6] treats as the supervision signal). Each signal's acquisition cost (0 extra calls vs. k−1 extra generations) is metered and charged by M5." source: hypothesis.
- **M2** — name: "Frozen-backbone probe"; text: "A logistic-regression and a 2-layer MLP (hidden width 256) head trained on the final-token hidden state of the frozen cheap-tier backbone at prefill, extracted at the last layer and at layer L/2 (layer choice ablated), predicting the probability that the cheap tier answers this query correctly. Training labels: empirical correctness of the k cached cheap-tier samples on ~5,000 held-out training queries — the same samples that feed M1's self-consistency baseline, so label generation adds no compute beyond the baseline (the label-reuse trick of [DiffAdapt, OpenReview:644FH1vVIl] / [AdaptiveThinking, OpenReview:2i6Rp0gCq6]). Probe inference cost ≈ one already-required prefill pass + <1 ms of head compute." source: hypothesis.
- **M3** — name: "Self-report elicitation module"; text: "Two operationalizations of large-model self-report, both metered as one extra generation call: (a) verbalized confidence — the expensive-tier model is shown the query (and optionally the cheap-tier draft answer) and asked for a 0–100 confidence that the cheap tier's answer is correct; (b) P(True)-style logprob readout in the format of [Kadavath et al., 2022]. Both variants reported separately to avoid construct lock-in." source: hypothesis.
- **M4** — name: "Matched-budget two-tier router"; text: "A shared thresholded routing rule: route to the expensive tier iff the controller's signal falls below threshold τ. For each controller, τ is swept over its signal range in the offline simulator; the matched-budget comparison picks, for every target budget B, the τ whose realized total cost equals B (interpolating between adjacent thresholds), so all controllers are compared at identical realized spend including their own signal-acquisition cost." source: hypothesis.
- **M5** — name: "Accuracy-per-dollar evaluation harness"; text: "Computes per-query dollar cost from measured input/output token counts under two disclosed cost models (public API list prices; measured GPU-seconds × cloud instance price), and reports: accuracy at matched budget, accuracy-per-dollar, area under the cost–accuracy curve over a budget grid, AUROC of each raw signal against cheap-tier correctness, and ECE of probe/self-report probabilities. Correctness is scored programmatically (exact match / option match), enabling controller-independent ground truth." source: hypothesis.

**challenge_arguments** (`list[ChallengeArgument]`):

- {challenge_id: "C1", argument_text: "Ground-truth economics are contained by design: evaluation uses exact-answer benchmarks scored programmatically (no annotator labels), and probe training labels are recycled from the k cheap-tier samples already required for the self-consistency baseline, so the comparison introduces no labeling cost beyond what the weakest baseline already pays.", mechanism_components: ["M2", "M5"], source: hypothesis}
- {challenge_id: "C2", argument_text: "Cost commensurability is enforced by metering every controller's own signal-acquisition cost (probe prefill+head, self-consistency's k−1 extra samples, self-report's extra call) inside the same dollar meter as the routed generations, and by comparing at equal realized spend across a swept budget grid rather than at a single hand-picked operating point; amortized probe-training cost is reported separately as a fixed cost per backbone.", mechanism_components: ["M4", "M5"], source: hypothesis}
- {challenge_id: "C3", argument_text: "Backbone/distribution specificity is not solved but is measured: Stage 2 trains the probe on one task and tests on held-out tasks, and repeats the full comparison on a second backbone family, so any probe advantage that is distribution-specific shows up as a transfer gap rather than being averaged away.", mechanism_components: ["M2", "M5"], source: hypothesis}
- {challenge_id: "C4", argument_text: "All controllers are framed as pre-hoc estimators of latent per-query difficulty and judged only by downstream matched-budget accuracy (plus AUROC against realized correctness), never by agreement with any oracle unavailable at decision time.", mechanism_components: ["M1", "M2", "M3", "M5"], source: hypothesis}

**unaddressed_challenges**: `["C3"]` — the design measures cross-task/cross-backbone
transfer but contains no mechanism that makes the probe transferable; C3 is inherent to
the frozen-feature approach and is only characterized, not overcome.

**Feasibility** [HYPOTHESIS — order-of-magnitude planning estimates, not measurements]:
- **Scale**: Stage 1 ≈ 2 benchmarks × 2,000 eval queries × (1 cheap prefill+answer + 8 cheap samples + 1 expensive-tier CoT run + 1 self-report call) ≈ ~48k generations total, of which ~4k hit the expensive tier / API. Probe training: ~5k queries × 8 samples ≈ 40k additional cheap-tier generations, fully reused by M1's baseline.
- **Compute/cost class**: cheap tier (7B, local): roughly 30–60 A100-GPU-hours for all sampling; expensive tier + self-report via API: low hundreds of dollars (≈$200–$600 at current GPT-4o-class list prices for ~8k calls with CoT); total Stage 1 well under $1k-equivalent. Stage 2 ≈ 4–6× Stage 1 (≈200–400 GPU-hours + $1–2k API class). Annotator-hours: 0 (programmatic scoring).
- **#runs**: because signals and both tiers are precomputed once, every threshold/budget point is an offline simulation — the run count is O(benchmarks × backbones), not O(thresholds).
- **Single biggest feasibility risk**: the expensive tier must be executed for *every* evaluation query (even those a controller would route cheap) to make offline routing simulation exact — this dominates the API bill. **Mitigation**: cap eval sets at 2,000 queries/benchmark, cache all expensive-tier outputs once and share them across all controllers, thresholds, and budget points; if still over budget, subsample the expensive tier with importance weighting on queries where controllers disagree.

- **status**: PARTIAL — a concrete, operational design sketch extrapolated from a one-sentence minimal experiment, not an extracted methodology.
- **absence_comment**: {what_missing: "No implementation, hyperparameters, or measured costs exist because the method has not been built.", why_matters: "A reader must not mistake M1–M5 for a validated design; they are the most standard-practice operationalization of the seed's minimal experiment, informed by the corpus antecedents.", implication: "Use N6 as the starting design for whoever runs this experiment; revise components (especially layer choice in M2 and the cost model in M5) against pilot data."}

**V-08 note**: N6's `challenge_arguments` and `unaddressed_challenges` rest entirely on
`source="hypothesis"` N5 items — flagged per self-verification V-08 so this is never read
with extracted-level confidence.

---

## N7 — Contributions

**contributions** (`list[Contribution]`), all [HYPOTHESIS] — framed from the method sketch + expected findings, not invented novelty beyond what the minimal experiment would validate:

- **CO1** — text: "The first controlled three-way comparison of training-free signals, a frozen-backbone probe, and large-model self-report as per-query compute-allocation controllers under matched realized dollar budgets, with each controller charged its own signal-acquisition cost." contribution_type: empirical_finding; is_testable: true; has_rq: true; source: hypothesis.
- **CO2** — text: "Evidence on whether a near-zero-marginal-cost frozen probe matches or exceeds the decision quality of large-model self-report — including whether any advantage survives cross-task and cross-backbone transfer." contribution_type: empirical_finding; is_testable: true; has_rq: true; source: hypothesis.
- **CO3** — text: "A reusable precompute-then-simulate accuracy-per-dollar harness (cached two-tier outputs + offline routing simulation + dual cost models) for comparing heterogeneous controllers at exactly matched budgets." contribution_type: technical_artifact; is_testable: true; has_rq: true; source: hypothesis.

- **status**: PARTIAL — these are the most likely claims such a paper would make, not extracted contributions.
- **absence_comment**: {what_missing: "No contributions section exists in a real manuscript.", why_matters: "A reviewer should treat CO1–CO3 as predicted framing, useful for judging whether the idea is contribution-shaped, not as an author's actual claim.", implication: "Revisit and rewrite this node once real results exist."}

---

## N8 — Research Questions

**research_questions** (`list[ResearchQuestion]`):

- **RQ1** [GIVEN, near-verbatim restatement of the seed's core question]:
  text: "Can a small frozen-backbone probe used as a compute-allocation controller match the decision quality of large-model self-report as a meta-decision signal, at matched realized budget?" (seed: "一个小型冻结骨干探针做分配决策，能否达到大模型自我报告式元决策的水平？")
  rq_source: explicit (given by the seed's core question)
  evaluates_mechanisms: ["M2", "M3", "M4", "M5"]
  addresses_challenges: ["C2", "C4"]
  tests_contributions: ["CO1", "CO2"]
  answered_by_experiment: "Offline-simulated routing on cached two-tier outputs: probe-routed vs. self-report-routed accuracy at each matched budget point on GSM8K and MMLU-Pro (Stage 1), analyzed per the plan below."

- **RQ_INF_1** [HYPOTHESIS, inferred — the seed's second clause asks whether training-free signals suffice]:
  text: "Are training-free signals (logit entropy, self-consistency agreement) alone sufficient as compute-allocation controllers — i.e., statistically indistinguishable from the best trained/elicited controller at matched budget — once their own sampling cost is charged?" (seed: "training-free 信号够不够？")
  rq_source: inferred
  evaluates_mechanisms: ["M1", "M4", "M5"]
  addresses_challenges: ["C2", "C4"]
  tests_contributions: ["CO1"]
  answered_by_experiment: "Same offline simulation comparing entropy-routed and self-consistency-routed accuracy against probe and self-report at identical realized spend, across the budget grid."

- **RQ_INF_2** [HYPOTHESIS, inferred — required by C3 to qualify any probe advantage]:
  text: "Does the frozen probe's controller quality transfer across task distributions and backbone families, or is it specific to the training task and backbone?"
  rq_source: inferred
  evaluates_mechanisms: ["M2", "M5"]
  addresses_challenges: ["C3"]
  tests_contributions: ["CO2", "CO3"]
  answered_by_experiment: "Stage 2: train probe on one benchmark, evaluate routing on held-out benchmarks (MATH-500, GPQA-Diamond, BBH); repeat the full comparison on a second backbone family (Llama-3.1) and report the transfer gap in matched-budget accuracy."

- **datasets** (`EvalEntityGroup`) [HYPOTHESIS]: names: ["GSM8K (grade-school math word problems, exact-match numeric answers; Stage 1)", "MMLU-Pro (10-option multiple choice across domains; Stage 1)", "MATH-500 (competition math; Stage 2)", "GPQA-Diamond (graduate-level science MCQ; Stage 2)", "BIG-Bench-Hard (multi-task reasoning; Stage 2)"]; source: hypothesis — all are real, public, exact-answer benchmarks chosen because correctness is programmatically scorable (C1).
- **baselines** (`EvalEntityGroup`) [HYPOTHESIS]: names: ["Logit/predictive entropy router (training-free; M1a)", "Self-consistency agreement router at k=8 (training-free; M1b, per the signal [AdaptiveThinking, OpenReview:2i6Rp0gCq6] predicts)", "Verbalized-confidence self-report router (M3a)", "P(True)-style self-report router (M3b, [Kadavath et al., 2022])", "Random router (matched budget)", "All-cheap and all-expensive fixed policies (budget endpoints)", "Oracle router (routes expensive iff cheap tier is wrong; upper bound)"]; source: hypothesis.
- **metrics** (`EvalEntityGroup`) [HYPOTHESIS]: names: ["Accuracy at matched budget B (fraction correct under the routing policy whose realized cost = B)", "Accuracy-per-dollar (accuracy ÷ realized total cost, reported across the budget grid)", "Area under the cost–accuracy curve (normalized, between all-cheap and oracle endpoints)", "Signal AUROC vs. cheap-tier correctness (threshold-free controller quality)", "Expected Calibration Error (15-bin, for probe and self-report probabilities)"]; source: hypothesis.

**analysis_plan** [HYPOTHESIS]: n = 2,000 evaluation queries per benchmark (paired: every
controller routes the same queries over the same cached outputs). Primary test: McNemar's
test on paired per-query correctness of probe-routed vs. self-report-routed decisions at
each of 5 pre-registered budget points, α = 0.05 with Benjamini–Hochberg correction across
benchmarks × budget points; 2,000 paired queries gives adequate power (≈0.8) for a ≈3
percentage-point accuracy difference at typical discordance rates. Secondary: 10,000-sample
paired bootstrap 95% CIs for accuracy-per-dollar and AUCC differences. Expected direction:
probe ≥ self-report at matched budget (probe's signal cost is near zero, so at equal spend
more budget reaches actual generation); training-free signals < probe once self-consistency's
sampling cost is charged. Equivalence claims for RQ_INF_1 use a TOST equivalence test with
a ±2pp margin rather than accepting a null.

- **status**: PARTIAL — RQ1 given; RQ_INF_1/RQ_INF_2 and all datasets/baselines/metrics/analysis inferred.
- **absence_comment**: {what_missing: "The seed names controller types and the comparison metric (accuracy-per-dollar) but no benchmark, backbone, sample size, or statistical procedure.", why_matters: "Without these the minimal experiment is not executable or reviewable.", implication: "The named datasets/baselines/metrics/analysis above are this digest's concrete proposal; pre-register them (especially the budget points and TOST margin) before running."}

---

## N9 — Results

**CRITICAL: no numbers are fabricated below.** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].
`evidence_strength="missing"` and `rq_answered=false` throughout, since no experiment has
been run.

**results** (`list[Result]`):

1. **rq_id**: "RQ1"
   **result_text**: "[HYPOTHESIZED DIRECTION] At matched realized budgets, the frozen probe is predicted to meet or exceed self-report-routed accuracy on Stage-1 benchmarks, because the probe's near-zero signal cost leaves more of the shared budget for actual expensive-tier generation, and corpus evidence ([DiffAdapt, OpenReview:644FH1vVIl], [AdaptiveThinking, OpenReview:2i6Rp0gCq6]) already shows prefill hidden states carry usable difficulty signal, while [LimitedMetacognition, OpenReview:gb9HR8hxtU] gives independent reason to doubt self-report's decision quality."
   **result_type**: quantitative (predicted metric type; no values exist)
   **evidence_strength**: missing
   **rq_answered**: false
   **source**: hypothesis
   **FALSIFICATION CONDITION**: "Refuted if McNemar's test shows self-report-routed accuracy significantly exceeds probe-routed accuracy (α=0.05, BH-corrected) at a majority of pre-registered budget points on Stage-1 benchmarks — i.e., 'expensive-but-informed' beats 'cheap-but-frozen' even after paying for its own elicitation call."

2. **rq_id**: "RQ_INF_1"
   **result_text**: "[HYPOTHESIZED DIRECTION] Training-free signals are predicted to be partially sufficient: logit entropy nearly free but with the lowest AUROC; self-consistency agreement with competitive AUROC but eroded accuracy-per-dollar once its k−1 extra samples are charged — so neither is expected to be equivalent (within the ±2pp TOST margin) to the probe at matched budget."
   **result_type**: quantitative (predicted metric type; no values exist)
   **evidence_strength**: missing
   **rq_answered**: false
   **source**: hypothesis
   **FALSIFICATION CONDITION**: "Refuted if either training-free signal passes the TOST equivalence test (±2pp) against the probe at matched budget across Stage-1 benchmarks — showing training-free signals already suffice and the probe adds no measurable value, answering the seed's 'training-free 信号够不够?' with 'yes'."

3. **rq_id**: "RQ_INF_2"
   **result_text**: "[HYPOTHESIZED DIRECTION] The probe's advantage is predicted to shrink but not vanish under cross-task transfer, and to shrink most under cross-backbone transfer (a probe trained on one model's features does not apply to another's), consistent with C3; the practical claim would then be that per-backbone probe retraining is cheap enough (~5k recycled samples) to be the deployment path."
   **result_type**: quantitative (predicted metric type; no values exist)
   **evidence_strength**: missing
   **rq_answered**: false
   **source**: hypothesis
   **FALSIFICATION CONDITION**: "Refuted if the probe trained on one benchmark drops below the *training-free* self-consistency router's matched-budget accuracy on held-out benchmarks — transfer so poor that the probe is dominated by a signal requiring no training at all, undermining the 'train once, allocate cheaply' premise."

- **status**: NOT_FOUND — no experiment has actually been run.
- **absence_comment**: {what_missing: "No quantitative results exist because this paper has not been written or experimented on.", why_matters: "A reader must not treat the predicted directions above as findings; each is a falsifiable prediction, not a measurement.", implication: "Run Stage 1 (the seed's minimal experiment) to populate results for RQ1/RQ_INF_1; RQ_INF_2 requires Stage 2."}

---

## N10 — Threats / Self-Limitations

[HYPOTHESIS] anticipated limitations of this study design (no real Threats/Limitations
section exists since no paper has been written — these are *predicted*, not *author-stated*):

**threats** (`list[ThreatItem]`):

- **t1** — category: construct; description: "'Accuracy-per-dollar' depends on a contestable cost operationalization: API list prices bundle provider margins, while GPU-seconds ignore utilization and batching, and self-hosted marginal cost is ambiguous — a controller ranking could flip between cost models." mitigation: "Report both cost models (M5) side by side plus raw token/latency counts, and flag any comparison whose sign differs between the two."; source: hypothesis.
- **t2** — category: construct; description: "'Self-report' has no single canonical form; a weak verbalized-confidence prompt could strawman the baseline and inflate the probe's apparent advantage." mitigation: "Evaluate two elicitation variants (verbalized 0–100 and P(True)-style logprob per [Kadavath et al., 2022]) with prompt tuning on a dev split, and report the stronger variant as the headline baseline."; source: hypothesis.
- **t3** — category: internal; description: "The probe is trained on queries from the same benchmark distributions used for evaluation, so distribution overlap (or outright near-duplicate leakage between train and eval splits) could inflate probe quality relative to training-free and self-report controllers that use no training data." mitigation: "Enforce disjoint train/eval splits with de-duplication, and make cross-task transfer (RQ_INF_2) a primary reported condition rather than an appendix ablation."; source: hypothesis.
- **t4** — category: external; description: "Findings from two backbone families, a two-tier routing scheme, and single-turn exact-answer reasoning benchmarks may not generalize to other architectures, multi-tier or model-choice routing (the [RouterArena, OpenReview:9HsaIi4ngF] setting), or agentic/tool-use workloads where per-query cost is dominated by environment interaction." mitigation: "State scope explicitly; include the second backbone family and a model-choice (cheap-model vs. large-model) tier variant in Stage 2 to test at least one axis of generalization."; source: hypothesis.
- **t5** — category: conclusion; description: "Sweeping routing thresholds over a budget grid across multiple benchmarks invites multiple-comparison and operating-point cherry-picking errors — a controller can be made to look best by choosing the budget point post hoc." mitigation: "Pre-register the 5 budget points and the TOST margin, apply Benjamini–Hochberg correction across all benchmark × budget tests, and report full cost–accuracy curves rather than isolated points."; source: hypothesis.

- **status**: PARTIAL (populated with anticipated threats per the reverse-digest convention; these are this digest's own risk register, not author-acknowledged limitations).
- **absence_comment**: {what_missing: "No actual Threats-to-Validity/Limitations section exists because no paper has been written.", why_matters: "A reader must know t1–t5 are anticipated risks with proposed mitigations, not limitations the (nonexistent) authors admitted to.", implication: "Re-derive N10 from the real paper's own Limitations section once written; until then t1–t5 double as a pre-registration checklist."}

---

## N11 — Artifacts

**artifacts**: `[]` — nothing has been released; the paper does not exist.
**has_code**: `false` [PLACEHOLDER]
**has_data**: `false` [PLACEHOLDER]
**has_model**: `false` [PLACEHOLDER]

- **status**: NOT_FOUND
- **absence_comment**: {what_missing: "No code repository, dataset, model, or demo exists because this paper has not been written or experimented on.", why_matters: "This is reviewer-relevant signal in its own right — there is nothing to reproduce yet, not a gap to paper over.", implication: "If pursued, plan to release the probe-training code, the cached two-tier generations (which make every routing policy reproducible offline), and the accuracy-per-dollar simulation harness (M2/M5) as artifacts — the cache is the scientifically valuable artifact because it lets others evaluate new controllers at zero model cost."}

---

## N12 — Contribution Type

- **value**: `empirical` [HYPOTHESIS]
- **rationale**: "What N9's predicted results would validate is a comparison claim about existing controller families — training-free signals, a frozen probe (a standard technique per [DiffAdapt, OpenReview:644FH1vVIl] / [AdaptiveThinking, OpenReview:2i6Rp0gCq6]), and self-report — measured at matched budget; the paper proposes no new controller mechanism, and the harness (CO3), like the tool in comparable best-paper digests classified `empirical` (e.g., the code-formatting cost study), is an instrument in service of the measurement, not the object of the RQs. Re-checked against the `benchmark` alternative: the difficulty-calibrated task suite is assembled from existing public benchmarks rather than contributed as a new evaluation asset, so `empirical` remains the correct CfP category; this would flip to `benchmark` only if the released two-tier cache + simulator were promoted to the paper's primary contribution."
- **source**: hypothesis

---

## Claims

Reviewer-relevant assertions this hypothetical paper would rest on, each tagged by trust level:

1. **[GROUNDED:corpus]** "Prefill-stage hidden states of a frozen backbone carry enough signal about query difficulty/expected correctness to drive compute allocation." — evidence: {type: citation, text: "[DiffAdapt, OpenReview:644FH1vVIl] trains an MLP on post-prefill final-layer hidden states to select Easy/Normal/Hard reasoning; [AdaptiveThinking, OpenReview:2i6Rp0gCq6] predicts self-consistency from the prefill final-token hidden state to decide whether to think.", source: GROUNDED:corpus, location: ideas.jsonl proposal text}.

2. **[GROUNDED:corpus]** "Self-report is a costly and behaviorally unreliable meta-decision signal: models often cannot deploy their internal confidence when a decision depends on it, and making self-report reliable has required per-model training." — evidence: {type: citation, text: "[LimitedMetacognition, OpenReview:gb9HR8hxtU] finds delegation behavior poorly exploits internal confidence; [DiSRouter, OpenReview:KDcwXKr0NU] needs SFT+RL per model because 'intrinsic self-awareness is... not sufficiently calibrated... for routing-quality decisions'.", source: GROUNDED:corpus, location: ideas.jsonl proposal text}.

3. **[HYPOTHESIS]** "No existing work compares training-free signals, frozen probes, and self-report as interchangeable controllers under a matched realized dollar budget that charges each controller its own signal cost — the specific gap this paper fills." — evidence: {type: argument, text: "N4 items 1, 5, 6, 8: the probe papers report token savings not accuracy-per-dollar vs. self-report; the self-report papers do not price elicitation; the router benchmark evaluates model-choice routers, not controller signals.", source: hypothesis, location: N4}.

4. **[HYPOTHESIS]** "The probe's near-zero marginal signal cost implies that even a modestly informative probe should win on accuracy-per-dollar at typical budgets." — evidence: {type: argument, text: "At equal realized spend, budget not consumed by the controller's own call/samples is available for expensive-tier generation (M4/M5 accounting); this is the core mechanism behind N9's RQ1 prediction and is directly falsifiable by its stated condition.", source: hypothesis, location: N6/N9}.

5. **[PLACEHOLDER]** "Whether a probe's controller quality survives cross-task and cross-backbone transfer (C3/RQ_INF_2) is the central open question determining external validity — genuinely unknown until Stage 2 is run." — evidence: {type: argument, text: "No cross-backbone controller-transfer evidence exists in the corpus antecedents; the frozen-feature design makes some transfer gap likely but its magnitude is unknowable pre-hoc.", source: placeholder, location: N/A}.
