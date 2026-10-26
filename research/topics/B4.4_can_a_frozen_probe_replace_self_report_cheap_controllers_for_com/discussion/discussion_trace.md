# Discussion Trace — B4.4 (auto-research-discussion, 6-stage critic/refiner loop)

> Extracted verbatim from `pipeline.md` (the "## Seed brief" through "## Cross-stage consistency check" sections), per the `auto-research-discussion` skill's updated "Final deliverables" spec, which now requires the discussion trace as its own standalone file. No content below was regenerated or altered from the original run — this is a straight move, not a re-run of the critic/refiner loop.

# Auto-Research-Discussion Run — B4.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B4.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already runs its own asymmetry/taste self-check and a full pre-registered experiment plan), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure, under a shared total dollar budget that charges every controller its own signal-acquisition cost, whether a near-zero-cost probe trained on a frozen backbone's prefill hidden state can match large-model self-report — and whether training-free signals (logit entropy, self-consistency) are alone sufficient — as per-query compute-allocation controllers.
- **Apparent inputs:** an exact-answer reasoning query set; a frozen backbone's prefill hidden states/logits; k cached cheap-tier samples; a large-model self-report elicitation; a shared total dollar budget.
- **Apparent outputs:** a per-query routing decision per controller; matched-budget accuracy / accuracy-per-dollar per controller; budget-independent signal-quality diagnostics (AUROC, calibration) per controller.
- **Closest research areas:** hidden-state probing for compute allocation ([DiffAdapt, OpenReview:644FH1vVIl]; [AdaptiveThinking, OpenReview:2i6Rp0gCq6]); self-report/verbalized confidence ([Kadavath et al., 2022]); trained routing/cascades ([DiSRouter, OpenReview:KDcwXKr0NU]; [TRIM, OpenReview:MoKrugWUfC]; [RouterArena, OpenReview:9HsaIi4ngF]); behavioral limits of self-report ([LimitedMetacognition, OpenReview:gb9HR8hxtU]).
- **In scope:** measuring existing controller families (probe, self-report, training-free signals) at matched realized dollar budget, each charged its own signal-acquisition cost. **Out of scope:** proposing a new controller mechanism; multi-model/model-choice routing (the RouterArena setting); non-sandboxable live deployment; step-level or agentic-workload routing.
- **Confidence: high.** As with a prior reverse-digested seed in this batch, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ id) and already carrying its own asymmetry/taste check (`paper.md` Step 0/3) and a formal problem definition with a full symbol-by-symbol measurement table (Step 5). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 6, which is why stages 5/6 below are framed around instrument-validity claims (label-cost gate, self-report construct-validity safeguard, decision-quality-vs-cost isolation) that `paper.md`'s Assumptions/threats (A4, t2, the B-alt baseline) gesture at but never state as their own standalone falsifiable hypotheses with dedicated research questions.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed set of exact-answer reasoning queries, a frozen LLM backbone that has already produced a prefill hidden state for each query, cached samples from a cheap execution tier, and an available (but costly) large-model self-report elicitation, determine — under a shared total dollar budget that charges every controller its own signal-acquisition cost — whether a probe trained on the frozen prefill hidden state can allocate per-query compute (cheap vs. expensive tier) at least as well as large-model self-report, and whether training-free signals (logit entropy, self-consistency agreement) are alone sufficient to do the same.
- `input`: (1) a query set from an exact-answer reasoning benchmark, each item programmatically scorable under both execution tiers; (2) frozen-backbone hidden states and logits from one prefill pass per query; (3) k sampled cheap-tier generations per query; (4) a large-model self-report elicitation (verbalized confidence and/or P(True)-style logprob) available for every query; (5) a shared total dollar budget B.
- `output`: (1) a per-query routing decision (cheap vs. expensive tier) issued by each controller; (2) each controller's accuracy and accuracy-per-dollar at every matched realized-budget point; (3) each controller's raw signal quality (AUROC against cheap-tier correctness) and calibration, independent of any budget point.
- `constraints`: controllers must be compared at identical realized total spend, where each controller's own signal-acquisition cost (probe: amortized training + one prefill/head pass; self-consistency: k−1 extra samples; self-report: one extra generation call) is charged against the same budget it is trying to allocate; correctness must be programmatically scorable and controller-independent.
- `objective`: a controller-ranking claim is accepted only relative to a pre-specified set of budget points and a pre-specified statistical test at each point.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12's own `value: empirical` and `paper.md` Step 2's "Empirical measurement / controlled comparison... No new controller mechanism is proposed" both settle this as a measurement/characterization study.

**critique:**
- summary: Strong draft, evidence-traceable to the seed, but the objective has a real evaluability gap and the summary is asymmetric where the study itself is not.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says a ranking claim needs 'a pre-specified set of budget points and test,' but doesn't say what happens when different budget points disagree (e.g., probe wins at 3 of 5 points, self-report at 2). paper.md's own Step 6 already resolves this with an explicit majority-of-points-plus-multiple-testing-correction rule (H1: 'non-inferior... AND strictly superior... at ≥2 of the 5 points', BH-corrected) — but that resolution rule is not yet part of the stage-1 objective, so as written the objective is not fully evaluable on its own."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'at least as well as' is directionally loaded toward the probe as the object of interest, folding the training-free question in as an afterthought clause. Since this is a three-way comparison (per N1's objective and CO1), the summary should treat all three controller families symmetrically before any directional hypothesis is introduced."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A controller-ranking claim at a given budget is accepted only if it holds under a pre-specified statistical decision rule applied per budget point across both Stage-1 benchmarks, with correction for the resulting multiple comparisons; a controller is judged to dominate only if that decision rule resolves in its favor at a pre-registered minimum fraction of the tested (budget × benchmark) cells, not at any single hand-picked point, and disagreement across cells is reported as a bounded regime (e.g., a cost-crossover budget) rather than resolved by an arbitrary tie-break."
- `summary` (refined): "Given a fixed set of exact-answer reasoning queries, a frozen LLM backbone whose prefill hidden state has already been computed, cached cheap-tier samples, and an available large-model self-report elicitation, determine — under a shared total dollar budget that charges every controller its own signal-acquisition cost — which of three controller families (training-free signals, a frozen-backbone probe, large-model self-report) achieves the highest accuracy at matched realized spend, and specifically whether the near-zero-cost probe's decision quality is non-inferior to self-report's."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Query set $Q$; execution tiers $t\in\{\text{cheap},\text{exp}\}$ with programmatic correctness $y_t(q)\in\{0,1\}$ and dollar cost $c_t(q)$. A controller $\pi$ emits signal $s_\pi(q)$ at acquisition cost $a_\pi(q)$; a threshold policy routes to exp iff $s_\pi(q)<\tau$. At a target total budget $B$, $\tau_\pi(B)$ solves $\text{Cost}_\pi(\tau)=\sum_q[a_\pi(q)+c_{\text{cheap}}(q)+\mathbb{1}[s_\pi(q)<\tau]c_{\text{exp}}(q)]=B$. Determine, across $\pi\in\{$training-free, probe, self-report$\}$ and a pre-registered grid of $B$, which $\pi$ maximizes $\text{Acc}_\pi(\tau_\pi(B))$."
- `changes_made`: tightened the objective's multi-point evaluability rule; rebalanced the summary to a symmetric three-way framing; added `formal_summary` reusing `paper.md` Step 5's own notation rather than inventing new symbols.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Compute-allocation controllers are usually built from whichever signal is easiest to obtain — an extra self-report call, a handful of self-consistency samples — without asking whether a signal that costs almost nothing (a probe on a hidden state the model has already computed) could do the same job, because no prior comparison charges every controller's own signal-acquisition cost against the same budget it is trying to save.
- `why_it_matters`: As test-time compute scaling makes per-query budget decisions economically material, the field has converged on two controller families that both charge extra generation to obtain their signal: self-report costs one more large-model call and inherits that model's calibration failures, while self-consistency-style training-free signals cost k−1 more samples before any budget is even saved. A probe reading a frozen backbone's prefill hidden state is the one candidate signal whose acquisition is (almost) free, because the forward pass it reads from has already happened for an unrelated reason (producing the cheap-tier answer). If that near-free signal turns out to make routing decisions of comparable quality, every deployed system currently paying for self-report or self-consistency sampling is paying a real, avoidable dollar cost for a decision a probe could make for free — and if it doesn't, that is equally decision-relevant, because it tells practitioners the extra spend on self-report or sampling is buying something the probe genuinely cannot replicate.
- `who_cares`: Teams deploying test-time compute scaling in production, where every self-report call or self-consistency sample is a real, metered API cost; designers of adaptive-reasoning systems ([DiffAdapt], [AdaptiveThinking]) deciding whether their probe's value proposition is token savings alone or also a decision-quality edge over self-report; researchers relying on [Kadavath et al., 2022]-style self-report as a default meta-decision signal without having priced its acquisition cost against an alternative.
- `evidence`: `[DiffAdapt, OpenReview:644FH1vVIl]`'s own motivation argues test-time scaling "allocates large reasoning budgets uniformly across queries regardless of their actual difficulty"; `[LimitedMetacognition, OpenReview:gb9HR8hxtU]` finds that models' delegation behavior poorly exploits their own internal confidence, giving independent reason to doubt self-report's decision quality even before its cost is counted; and N4's own audit of the ten closest works finds that none reports a matched-dollar-budget, accuracy-per-dollar comparison across all three controller families — the probe papers report token savings at preserved accuracy (not accuracy-per-dollar vs. self-report), the self-report literature does not price the elicitation call, and the router-benchmark literature (`[RouterArena, OpenReview:9HsaIi4ngF]`) evaluates model-choice, not within-model tier-choice, controllers.

**critique:**
- summary: Genuinely stake-specific motivation with real corpus citations, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is signal-quality diagnostics (AUROC, calibration) *independent of any budget point* — a claim about the controller's raw decision quality, decoupled from cost. why_it_matters as drafted only argues why the cost-adjusted comparison (accuracy-per-dollar) matters; it never explains why the budget-independent signal-quality diagnostic is worth reporting at all, as opposed to just reporting the cost-adjusted numbers. Without that, a reader could ask 'why report AUROC separately if accuracy-per-dollar already settles the ranking' — which paper.md's own B-alt baseline design (the 'rival explanation' check) answers, but the answer isn't yet in the motivation."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...Critically, a matched-budget accuracy-per-dollar ranking alone cannot tell a reader *why* a controller won — a near-zero-cost signal could win purely because it is cheap, even if its actual decisions are no better than a costlier signal's, in which case the finding would be an artifact of the budget-accounting mechanic rather than evidence about decision quality. Reporting each controller's raw, budget-independent signal quality (AUROC against realized correctness) alongside the cost-adjusted ranking is what lets a reader distinguish 'the probe makes better decisions' from 'the probe is just cheaper' — a distinction practitioners need before they trust a probe's routing decisions in a setting where budget constraints eventually loosen."
- `changes_made`: added the decision-quality-vs-cost-mechanics coverage argument for stage 1's third output.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — N3's own header states "full motivation+method text of the top hits was read before inclusion" (no title-only landscape mentions in the source material), so per the no-fabrication/no-padding rule, no additional landscape papers are invented here to build a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / `is_potential_baseline` / limitation → sub-problem it will motivate):

| work_id | citation | `is_potential_baseline` | limitation |
|---|---|---|---|
| `rw_diffadapt` | DiffAdapt (OpenReview:644FH1vVIl) | true | Validated against fixed-budget/heuristic reasoning baselines within one backbone's own reasoning modes; no head-to-head vs. self-report, and no matched-dollar-budget frame — headline currency is token savings at preserved accuracy, not accuracy-per-dollar. |
| `rw_adaptivethinking` | AdaptiveThinking (OpenReview:2i6Rp0gCq6) | true | Shares `rw_diffadapt`'s limitation above — same missing matched-budget frame, same single-backbone scope. |
| `rw_cats` | CaTS (OpenReview:jrSc4RJXy1) | false (fine-tunes the backbone — I/O mismatch: unavailable for API models/shared serving stacks) | Its one-pass confidence requires modifying the base model; training cost is charged to every new backbone, which a frozen-probe study is specifically trying to avoid. |
| `rw_disrouter` | DiSRouter (OpenReview:KDcwXKr0NU) | false (cross-model cascade routing, not within-model tier choice — I/O mismatch) | Concedes in its own motivation that "intrinsic self-awareness is present but not sufficiently calibrated... for routing-quality decisions," and so trains every pool model with SFT+RL — a per-model investment a frozen-probe controller avoids entirely. |
| `rw_trim` | TRIM (OpenReview:MoKrugWUfC) | false (step-level granularity, decomposable math-reasoning scope — I/O mismatch) | Controller itself is a separately trained process-reward model with nontrivial per-step inference cost; scoped to multi-step math traces, not generic per-query allocation. |
| `rw_limitedmetacog` | LimitedMetacognition (OpenReview:gb9HR8hxtU) | false (behavioral delegate-game study, not a controller construction — method-side reference only) | Shows self-reports may be imitative rather than evidential, but neither prices the elicitation call nor compares self-report against internal-state probes as budget-constrained controllers. |
| `rw_kvembeddings` | KV-Embeddings (OpenReview:GUhmiJaAzv) | true | Its comparison set is hidden-state methods and trajectory-search controllers; training-free signals and self-report are not evaluated as competing controllers under one shared budget. |
| `rw_tpc` | TPC (OpenReview:AGWa8whf92) | false (harmfulness classification, not correctness/difficulty estimation — I/O mismatch) | Targets safety monitoring; its own motivation flags cascading cheap probes with LLM monitors as introducing "architectural complexity" — the overhead this study's harness is built to quantify, not the object it studies. |
| `rw_routerarena` | RouterArena (OpenReview:9HsaIi4ngF) | false (model-choice routing platform, not within-model tier controller — I/O mismatch) | Evaluates routers that choose *between models*; does not evaluate within-model compute-tier controllers, nor treat entropy/self-consistency/probe/self-report as interchangeable signals under one matched budget. |
| `rw_kadavath2022` | Kadavath et al., 2022 | true | Establishes self-report correlates with correctness and is reasonably calibrated at scale, but does not price the elicitation call or compare self-report against internal-state probes as budget-constrained controllers. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but one baseline label needs scrutiny.
- comments:
  - `{severity: major, field: "specific_related_works[rw_kadavath2022].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Kadavath et al. 2022 is not an external comparator whose own reported numbers get beaten — it IS the source of one of this paper's own self-report operationalizations (M3b, P(True)-style logprob). Marking it a straightforward 'potential baseline' risks implying its published calibration numbers are being compared against directly, when in fact its elicitation *method* is being adopted wholesale as part of this paper's own instrument. Per the stage-3 rubric, a work whose I/O framing is 'defines a technique this paper directly implements' is a method-side source, not a baseline in the beat-a-number sense."}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the elicitation protocol is still legitimately reused as an experimental arm).

### Refiner pass

- `rw_kadavath2022.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — no published Kadavath et al. number is compared against. Its P(True) elicitation protocol is adopted directly as one of this paper's own two self-report operationalizations (M3b); its 'baseline' role is limited to anchoring that operationalization's canonical form, independent of any of its own reported results."
- `changes_made`: clarified Kadavath et al. 2022's role to avoid implying a reported-number comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_diffadapt`/`rw_adaptivethinking`'s shared "no matched-dollar-budget frame" limitation) is not a distinct framing check but restates this paper's own RQ1/RQ_INF_1 core question, already covered end-to-end as mechanism-tier RQs in Stage 6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus decisive components paper.md's own design surfaces):

- **`sp_label_free_ground_truth`** — *description:* Obtain per-query correctness labels usable both for scoring routing decisions and for training the probe, without introducing an annotation cost the other two controller families don't pay. *why_it_is_a_problem:* If probe training required fresh human labels while training-free and self-report controllers required none, the comparison would be measuring labeling budget, not controller quality. *technical_challenge:* The only labels available at zero marginal annotation cost are the cached cheap-tier samples' own programmatic correctness — reusing them for both the self-consistency signal and probe supervision requires that reuse not introduce train/eval leakage. *source_limitation_ids:* `["__novel__"]` — none of N3's works needed to justify this reuse against a self-report/training-free comparison's fairness; DiffAdapt/AdaptiveThinking recycle labels internally but never had to defend that recycling as fair to a symmetric three-way comparison.
- **`sp_cost_commensurability`** — *description:* Score every controller's decision quality at identical realized total spend, where each controller's own signal-acquisition cost is charged against the same budget it allocates. *why_it_is_a_problem:* The three controller families have structurally different signal costs (near-zero, k−1 samples, one extra call); comparing them at a shared nominal "budget" without charging each its own signal cost would systematically favor the cheaper-signal controller regardless of decision quality. *technical_challenge:* Signal costs are denominated in different units natively and must be converted into one dollar meter before any threshold sweep can compare them, and the two natural cost models (API list price vs. GPU-seconds) can disagree in ways that flip a ranking. *source_limitation_ids:* `["rw_diffadapt", "rw_adaptivethinking"]` — their shared limitation names exactly this missing frame.
- **`sp_transfer_specificity`** — *description:* Determine whether a probe's routing quality, trained on features from one task and one frozen backbone, degrades when applied to a different task distribution or backbone family. *why_it_is_a_problem:* A probe advantage that only holds in-distribution is a much weaker practical claim than one that transfers — deployability depends on not needing to retrain the probe for every new task/backbone. *technical_challenge:* The probe reads features at a fixed layer of one frozen backbone trained on one task's distribution, so any separability it exploits may be an artifact of that specific backbone/layer/distribution rather than a generalizable difficulty signal — inherent to the frozen-feature design, not a training deficiency more data fixes. *source_limitation_ids:* `["__novel__"]` — N6's own `unaddressed_challenges: ["C3"]` marks this as measured, not solved, by any cited work; it is a decisive component this paper's own decomposition surfaces, not a gap any prior paper names.
- **`sp_selfreport_construct_validity`** — *description:* Ensure the self-report baseline used for comparison is not an artificially weak elicitation that would inflate the probe's apparent advantage by construction. *why_it_is_a_problem:* Self-report has no single canonical form (verbalized confidence vs. P(True)-style logprob); if the comparison quietly uses whichever variant is weaker, any probe-favoring finding could be an artifact of baseline design, not of the probe's actual signal quality. *technical_challenge:* The two self-report variants can diverge in prompt sensitivity and elicitation format, so establishing which is "the" self-report baseline requires a principled, pre-registered selection procedure rather than an arbitrary choice made after results are known. *source_limitation_ids:* `["__novel__"]` — this is threat t2 in N10, not a stage-3 related-work limitation; it is surfaced by this paper's own scrutiny of its own baseline design, since none of the cited works run self-report as a competing baseline at all.
- **`sp_decision_quality_vs_cost_mechanics`** — *description:* Separate a controller's decision quality (does its signal actually rank queries by difficulty better) from the budget-accounting mechanic (does it merely spend less on its own signal, leaving more budget for generation). *why_it_is_a_problem:* A cheaper-signal controller could win the matched-budget comparison purely by arithmetic — more of the shared budget reaches expensive-tier generation — even if its signal is no better, or worse, at identifying which queries need the expensive tier; reporting only the matched-budget ranking would then misattribute a cost artifact to a decision-quality finding. *technical_challenge:* Matched-budget accuracy alone cannot distinguish these two explanations because cost and decision quality both act through the same threshold-and-route mechanism; disentangling them requires a second, budget-independent measure of signal quality computed identically for every controller. *source_limitation_ids:* `["__novel__"]` — this is the "B-alt" rival-explanation design in `paper.md`, a decisive component this paper's own scrutiny surfaces; no cited work runs this cost-free/cost-adjusted contrast because none treats probe/self-report/training-free as competing controllers under one shared meter in the first place.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's objective); one pair of sub-problems risks reading as the same concern stated twice.
- comments:
  - `{severity: minor, field: "sp_label_free_ground_truth / sp_cost_commensurability", anti_pattern: "overlap", comment: "Both invoke 'accounting fairly for cost' language — one's 'zero marginal annotation cost' and the other's 'signal-acquisition cost' can read as the same underlying concern stated twice. They are genuinely distinct — one is train-time labeling economics (paid once, before any controller runs), the other is per-query signal-acquisition cost at evaluation/routing time (paid by every controller on every query) — but the descriptions don't make that distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_label_free_ground_truth.technical_challenge` sharpened to end with: "...this is a **train-time labeling-economics** problem, distinct from the per-query signal-acquisition cost charged at evaluation time — it is about how the probe gets its supervision at all, not about what any controller costs to run at inference."
- `sp_cost_commensurability.technical_challenge` sharpened to end with: "...this is an **inference-time cost-accounting** problem: every controller, once trained (if it needs training at all), pays a different marginal cost on every future query, and it is this per-query cost that must be metered identically, regardless of how any controller's supervision was originally obtained."
- `changes_made`: made the train-time-labeling vs. inference-time-cost distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 1 sourced from a shared Stage-3 limitation, 4 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_recycled_label_pipeline`** → targets `sp_label_free_ground_truth`. *proposed_approach:* Train the probe's logistic-regression and 2-layer-MLP heads using empirical correctness computed from the k cached cheap-tier samples already generated for the self-consistency baseline (on a held-out training query pool, disjoint and de-duplicated from the evaluation set), so probe supervision is a byproduct of a computation the weakest baseline already performs. *key_insight:* The only correctness signal available at zero incremental annotation cost is exactly the signal the self-consistency baseline already needs for its own agreement-rate statistic — reusing it means the probe's added cost is training compute alone, not label acquisition, which is what keeps the eventual cost comparison fair rather than stacked in the probe's favor. *hypotheses:* ["A probe trained solely on labels recycled from cached self-consistency samples reaches AUROC > 0.60 against cheap-tier correctness on held-out GSM8K queries — the minimum separability needed for the probe to be a non-trivial routing signal at all."]
- **`m_dual_cost_metered_router`** → targets `sp_cost_commensurability`. *proposed_approach:* A shared thresholded router sweeps each controller's signal over its own range in an offline simulator; for every target total budget $B$, the threshold is chosen so that controller's realized cost (its own signal-acquisition cost plus routed generation cost, under two disclosed cost models — API list price and measured GPU-seconds) equals $B$, and all controllers are compared at that identical realized spend. *key_insight:* Because every controller's signal cost is charged before any routing benefit is counted, a controller can only win by making the shared remaining budget go further — either through cheaper signal acquisition or better-targeted routing decisions — and the two disclosed cost models let a reader check whether the ranking depends on which cost model is used. *hypotheses:* ["On both Stage-1 benchmarks (GSM8K, MMLU-Pro), at all 5 pre-registered budget points, the probe is non-inferior to the strongest self-report variant (McNemar does not reject in self-report's favor, BH-corrected α=0.05) and strictly superior at ≥2 of the 5 points on each benchmark.", "Neither training-free controller (logit/predictive entropy; self-consistency agreement, k=8) is equivalent to the best controller: TOST equivalence within ±2pp fails for each at ≥3 of 5 budget points on both benchmarks, and the probe's matched-budget accuracy exceeds each training-free controller by >2pp (paired-bootstrap 95% CI excluding 0) at ≥3 of 5 points once self-consistency's k−1 extra samples are charged."]
- **`m_cross_distribution_probe_transfer`** → targets `sp_transfer_specificity`. *proposed_approach:* Train the probe once on one Stage-1 benchmark's recycled labels, then evaluate its routing quality unchanged (no retraining) on ≥2 of 3 held-out benchmarks (MATH-500, GPQA-Diamond, BBH) and on a second backbone family (Llama-3.1), reporting the resulting transfer gap in matched-budget accuracy against the training-free self-consistency router. *key_insight:* A no-retraining floor (the training-free router) is the right comparator for a transfer test, because it isolates whether the probe's frozen-feature advantage survives distribution shift specifically, rather than comparing two numbers that could both move for unrelated reasons. *hypotheses:* ["A probe trained on one Stage-1 benchmark, evaluated on ≥2 of 3 held-out benchmarks, retains matched-budget accuracy ≥ the training-free self-consistency router at ≥3 of 5 budget points, with the cross-backbone (Llama-3.1) transfer gap larger than the cross-task transfer gap."]
- **`m_dual_selfreport_operationalization`** → targets `sp_selfreport_construct_validity`. *proposed_approach:* Implement two self-report elicitation variants — verbalized 0–100 confidence and P(True)-style logprob (Kadavath et al., 2022) — both prompt-tuned on a held-out dev split before any evaluation-set result is computed, and report the stronger of the two as the headline self-report baseline in every comparison. *key_insight:* Fixing the choice of which self-report variant is "the" baseline before seeing evaluation results, and doing so by picking the empirically stronger variant, is what prevents the comparison's headline finding from being an artifact of an unlucky (or convenient) baseline choice. *hypotheses:* ["Reporting only the weaker of the two self-report variants as the baseline would change the H1 non-inferiority/superiority verdict at ≥1 of the 5 pre-registered budget points relative to using the stronger variant — demonstrating that the dual-variant safeguard is load-bearing, not a redundant precaution."]
- **`m_costfree_decision_quality_isolation`** → targets `sp_decision_quality_vs_cost_mechanics`. *proposed_approach:* Alongside the matched-budget comparison, compute each controller's AUROC against cheap-tier correctness with no cost accounting at all — a threshold-free measure of raw decision quality — and check whether it agrees in direction with the matched-budget ranking. *key_insight:* A benign budget-arithmetic win moves the matched-budget ranking without necessarily moving the cost-free AUROC ranking; requiring the two to agree in direction is exactly the condition that separates "the probe makes better decisions" from "the probe is just cheaper." *hypotheses:* ["The probe's AUROC against cheap-tier correctness is not lower than the strongest self-report variant's AUROC; if the probe wins the matched-budget comparison (H1) while its AUROC is lower than self-report's, the win is attributable to signal cost alone, not decision quality, and is reported as such rather than as a decision-quality finding."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but one method carries two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_dual_cost_metered_router.hypotheses", anti_pattern: null, comment: "This method carries the paper's two most central claims (H1 and H2) in one method. Worth stating explicitly why one router mechanism produces both, so this doesn't read as two unrelated findings bundled under one method for convenience."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_dual_cost_metered_router.key_insight` extended: "...a single offline threshold-sweep simulator yields two distinct, separately falsifiable readouts from one instrument: the probe-vs-self-report contrast at each budget point (H1) and the training-free-vs-best-controller contrast at each budget point (H2) are both just different pairwise slices of the same matched-budget accuracy table the simulator produces — one instrument, two slices, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (1 + 2 + 1 + 1 + 1 across the five methods respectively — `m_dual_cost_metered_router` carries two, per the refiner's one-instrument-two-slices justification above).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The probe is a standard technique per `[DiffAdapt]`/`[AdaptiveThinking]`, not a new method this paper proposes to win with; Random/all-cheap/all-expensive/Oracle below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GSM8K — pilot stage; exact-match numeric answers give programmatic scoring for free (targets `sp_label_free_ground_truth`/`RQ_labelcost` and the H1/H2 budget grid).
- MMLU-Pro — pilot stage; 10-option multiple choice, stresses the predictive-entropy variant and gives a second Stage-1 domain for the BH-corrected H1/H2 tests.
- MATH-500, GPQA-Diamond — Stage 2 held-out benchmarks, used specifically to test whether the probe's transfer gap (H3) is bounded, rather than only being observed post hoc on the two fixed Stage-1 corpora.
- (draft initially listed BIG-Bench-Hard with justification only "a generic multi-task reasoning benchmark" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Random router at matched budget (B0) — the necessary "why do this at all" control: if no real controller beats Random on AUCC, per-query signal is worthless and the comparison is void.
- All-cheap / all-expensive fixed policies (budget endpoints) and the Oracle router (routes exp iff cheap tier is wrong; upper bound).
- Logit/predictive-entropy router and self-consistency router (M1, training-free family).
- Verbalized-confidence and P(True) self-report routers (M3; headline = the stronger variant, per `m_dual_selfreport_operationalization`).

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_labelcost` | `sp_label_free_ground_truth` | "A probe trained solely on labels recycled from cached self-consistency samples reaches AUROC > 0.60 against cheap-tier correctness on held-out GSM8K queries — the minimum separability needed for the probe to be a non-trivial routing signal at all." |
| `rq_probe_vs_selfreport` | `sp_cost_commensurability` | "On both Stage-1 benchmarks (GSM8K, MMLU-Pro), at all 5 pre-registered budget points, the probe is non-inferior to the strongest self-report variant (McNemar does not reject in self-report's favor, BH-corrected α=0.05) and strictly superior at ≥2 of the 5 points on each benchmark." |
| `rq_trainingfree_sufficiency` | `sp_cost_commensurability` | "Neither training-free controller (logit/predictive entropy; self-consistency agreement, k=8) is equivalent to the best controller: TOST equivalence within ±2pp fails for each at ≥3 of 5 budget points on both benchmarks, and the probe's matched-budget accuracy exceeds each training-free controller by >2pp (paired-bootstrap 95% CI excluding 0) at ≥3 of 5 points once self-consistency's k−1 extra samples are charged." |
| `rq_transfer` | `sp_transfer_specificity` | "A probe trained on one Stage-1 benchmark, evaluated on ≥2 of 3 held-out benchmarks, retains matched-budget accuracy ≥ the training-free self-consistency router at ≥3 of 5 budget points, with the cross-backbone (Llama-3.1) transfer gap larger than the cross-task transfer gap." |
| `rq_selfreport_variant_loadbearing` | `sp_selfreport_construct_validity` | "Reporting only the weaker of the two self-report variants as the baseline would change the H1 non-inferiority/superiority verdict at ≥1 of the 5 pre-registered budget points relative to using the stronger variant — demonstrating that the dual-variant safeguard is load-bearing, not a redundant precaution." |
| `rq_decisionquality_isolation` | `sp_decision_quality_vs_cost_mechanics` | "The probe's AUROC against cheap-tier correctness is not lower than the strongest self-report variant's AUROC; if the probe wins the matched-budget comparison (H1) while its AUROC is lower than self-report's, the win is attributable to signal cost alone, not decision quality, and is reported as such rather than as a decision-quality finding." |

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a generic label instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[BIG-Bench-Hard]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'a generic multi-task reasoning benchmark' is not a justification — it says nothing about which RQ needs it or why, unlike MATH-500/GPQA-Diamond which are named as held-out domains for exactly the transfer test."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "BIG-Bench-Hard (Stage 2) — *justification:* a multi-task suite whose component tasks differ from GSM8K/MMLU-Pro in *task format*, not just topic, letting `rq_transfer` (H3) test whether the probe's transfer gap is driven by topic shift alone or by format shift as well, rather than treating 'held-out benchmark' as a single undifferentiated condition."
- `changes_made`: gave BIG-Bench-Hard's inclusion a hypothesis-linked reason instead of a generic-label note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*`/`m_*`/`rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_cost_commensurability.source_limitation_ids = ["rw_diffadapt", "rw_adaptivethinking"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs are each reachable: (1) per-query routing decision and (2) matched-budget accuracy/accuracy-per-dollar via `sp_cost_commensurability` (+ `sp_transfer_specificity` for generalization), (3) budget-independent signal-quality diagnostics via `sp_decision_quality_vs_cost_mechanics` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** as with a prior reverse-digested seed in this batch, the recurring tension was **not disagreement about facts** (the seed material is unusually well-specified — `paper.md` already runs its own asymmetry check, taste self-audit, and a full formal problem definition) but **scope discipline** — repeatedly checking whether a Stage-5/6 hypothesis was quietly restating `paper.md`'s own already-finished Step 6 rather than adding something this schema's structure specifically demands. Two of the five sub-problems (`sp_selfreport_construct_validity`, `sp_decision_quality_vs_cost_mechanics`) exist precisely because `paper.md`'s own threats (t2) and rival-explanation baseline (B-alt) gesture at these concerns without ever stating them as standalone falsifiable hypotheses with their own dedicated research questions — that gap is what stages 4–6 here fill in.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`, `pipeline.md`; no `design_review.md` exists for this topic). Every finding enumerated and dispositioned below; historical rounds above are untouched.

1. **stage_review.md, Stage 2 REVISE (nearest-neighbor sentence in Related Work + Introduction)** — already applied in the original run (`stage_review.md` "Fixes applied" item 1; verified present in `paper_draft.md` Introduction ¶3 and Related Work opening). No action.
2. **stage_review.md, Stage 4 REVISE (per-RQ Falsification condition lines)** — already applied ("Fixes applied" item 2; verified in all six RQ subsections of `paper_draft.md`/`.tex` and mirrored in `experiment_design.md`). No action.
3. **stage_review.md, Phase A item 2 REVISE (reference-cache integrity: N3 keys absent)** — already applied (cache rewritten to canonical schema, 10 N3 keys added; logged in `pipeline.md` Phase Log). No action.
4. **stage_review.md, Phase A item 5 REVISE (H1 effect floor; A1–A5 Consequence clauses)** — already applied directly in `paper.md` and spliced into `paper_draft.md`/`.tex` RQ2 during Phase F. Verified: ≥1pp effect floor and −1pp non-inferiority margin present and identical in `paper.md` Step 6, `paper_draft.md` RQ2, and `experiment_design.md` RQ2. No action.
5. **stage_review.md, Phase A item 6 REVISE (R1 estimand sentence; R3 confound list; power/thin-cell INCONCLUSIVE rules)** — already applied in `paper.md` and spliced into the draft (Estimand paragraph in Problem Definition; thin-cell rules of 30 discordant pairs / n=200 in RQ2–RQ4 of both `paper_draft.md` and `experiment_design.md`). No action.
6. **stage_review.md, Phase A residual note (3 N3 records with stub-only digests)** — already resolved in the "Reference-cache follow-up — 2026-07-04" pass (DiffAdapt644F and Kadavath2207 upgraded to real-PDF digests; AdaptiveThink2i6 an honestly-logged gap after exhausted search). No action.
7. **stage_review.md / pipeline.md, Phase F [major] (zero \cite commands, no refs.bib)** — already fixed in the same pass (refs.bib script-generated from 17 selected cache records, 19 \citep instances, recompile clean). No action.
8. **stage_review.md, Phase G [minor] (Introduction's fourth contribution bullet "An empirical account of which controller family a fixed dollar actually buys the most accuracy from..." reads marginally more assertive than surrounding hedged prose)** — was the only OPEN finding; **applied in this round**. Change: bullet reworded to "An empirical account, in whichever direction the evidence falls, of which controller family a fixed dollar buys the most accuracy from at matched realized spend, ..." — dropping the assertive "actually" and adding an explicit direction-neutral hedge, matching the Abstract's deliverable-format framing that Phase G judged acceptable. Files: `paper_draft.md` (contribution bullet 4), `paper_draft.tex` (same bullet), recompiled `paper_draft.pdf` (latexmk exit 0, zero undefined citations, wording verified in PDF text).
9. **stage_review.md, Phase A item 6 advisory note (archetype-label discrepancy: pengsida "Analysis/Finding" vs guidance.md "A2 Empirical")** — rejected as moot: the note itself resolves the discrepancy (two reviewers' taxonomies, not a conflict; `paper.md`'s A2 self-classification is authoritative) and asks for no document change.
10. **stage_review.md, reference-cache follow-up note (DiffAdapt's own C3 — cross-model-only threshold transfer — "available as extra motivating material for RQ4... if a future revision wants it")** — rejected as not-requested: the review explicitly marks it optional ("not spliced into the draft in this pass — out of scope, no claim currently depends on it"); folding it in would add new motivating content no review asks for.
11. **taste_audit.md (both audits)** — verdict 🟢 both times, no conditions fired, no action items. No action.

**Cross-deliverable consistency check (this round):** 6 RQs in both `paper_draft.md` and `experiment_design.md`; RQ2 effect floor (≥1pp) and non-inferiority margin (−1pp), RQ3 TOST ±2pp and >2pp probe margin, thin-cell floors (30 discordant pairs RQ2/RQ3; n=200 routed-expensive-tier RQ4), n=2,000/benchmark, ≈80% power at ≈3pp — all identical across `paper.md` Step 6, `paper_draft.md` Experiments, and `experiment_design.md`. Target hypotheses in `experiment_design.md` remain verbatim quotes; none paraphrased. No mismatch found; no fix needed.

### Deletion-audit addendum (2026-07-05)

`stage_review.md` and `taste_audit.md` were deleted from the working tree; their git-HEAD contents were recovered (read-only, via `git show`) and every actionable finding re-verified against the current deliverables and the ledger above. Result: all findings from both files were already applied or dispositioned, with **one exception** found and fixed in this pass:

- **stage_review.md Phase A item 6 sub-item 4 (A\* gate naming)** claimed the fix "named `PG-1..PG-5` explicitly," but only PG-1 (A1), PG-2 (A2), PG-4 (A4), and PG-5 (A5) were present in `paper.md`; A3's detection clause carried no gate label, and no ledger entry dispositioned the gate-naming sub-item. **Applied now:** A3's *Detected by* clause in `paper.md` now reads "dual-cost-model gate (PG-3) — dual cost model (API list price vs GPU-seconds)...", completing the PG-1..PG-5 set. PG labels appear only in `paper.md` (never in `paper_draft.md`/`.tex`), so no draft edit or recompile was needed.

All other recovered findings verified present: Stage 2 nearest-neighbor sentence (draft Intro ¶3 + Related Work opening, `.md`/`.tex`); Stage 4 falsification conditions (6 in `paper_draft.md`, 6 in `.tex`, 6 in `experiment_design.md`); Phase A item 2 cache state (160 records, 17 selected, 0 pending, all 10 N3 keys present, `refs_n3_digests/` resolvable); Phase A item 5 (H1 ≥1pp effect floor + −1pp margin; A1–A5 consequence clauses); Phase A item 6 (estimand sentence, R2 not-applicable note, 5-entry confound list, power/thin-cell INCONCLUSIVE subsection); taste audit 🟢 with no action items. Target hypotheses in `experiment_design.md` untouched.
