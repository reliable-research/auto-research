# Digest: Which Trajectories Deserve Verification? Selective Checking under a Verifier-Call Budget

> **REVERSE-DIGEST NOTICE.** No paper exists yet for this topic (code B4.5, label `[资源]`,
> parent topic "B4. 预算分配 / 推理经济学"). This document is speculative scaffolding for
> research planning: it projects an N0–N12 digest forward from the seed idea, as if a paper
> answering the core question had already been written. Every field carries one of these
> trust tags instead of the usual `extracted`/`inferred` source tag:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README (title, core question, minimal
>   experiment, gap-type label).
> - **[HYPOTHESIS]** — reasoned elaboration grounded in the seed + the grounded literature
>   below + standard practice for this kind of study. A prediction, not a fact.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is done (authors, DOI, actual
>   numbers, released artifacts). Never invented.
> - **[GROUNDED:corpus]** — a real paper retrieved from the local OpenReview corpus
>   (`topics/corpus/ideas.jsonl`, 11,683 papers); `approach_summary` is grounded in that
>   paper's own motivation/method text and a real `paper_url` is given.
>
> Grounding: 6 keyword searches over the corpus (selective verification / verifier budget;
> test-time scaling / PRM / compute budget; uncertainty / confidence / self-consistency /
> calibration; LLM cascades / routing / escalation; trajectory selection / reranking;
> LLM-as-judge / selective prediction). Eight directly relevant corpus papers were retained
> for N3; full motivation+method text of each was read before summarizing.

---

## N0 Metadata

- **Title** [GIVEN]: "Which Trajectories Deserve Verification? Selective Checking under a Verifier-Call Budget"
- **Authors** [PLACEHOLDER]: `["Anonymous"]` — no paper exists, no authors can be known.
- **Abstract** [HYPOTHESIS] (drafted by synthesizing the core question + minimal experiment + the staged design in N6 into abstract prose — explicitly a draft, not a real abstract):
  > "Test-time scaling pipelines that sample many candidate reasoning trajectories per query
  > (self-consistency, best-of-N, agentic rollouts) increasingly pair the sampler with a
  > verifier — a costlier check such as unit-test execution, a process reward model, or a
  > stronger judge. Prior work either verifies every candidate, treats verification cost as
  > part of a generic compute budget, or analyzes verifier *imperfection*; almost none treats
  > the number of calls to a *trustworthy* verifier as the explicitly metered resource. We ask:
  > given a fixed budget B of calls to a trusted verifier and N > B candidate trajectories,
  > which trajectories should be verified to maximize accuracy-per-verifier-call? We formalize
  > this as budget-constrained trajectory selection and study a simple policy — rank
  > trajectories by cheap, verifier-free uncertainty signals (self-consistency mode share,
  > sequence log-likelihood, verbalized confidence) and spend the budget on the least-certain
  > candidates — against uniform-random allocation and full verification, on math (GSM8K,
  > MATH-500) and code (HumanEval+, MBPP+) benchmarks, first with an oracle verifier that
  > isolates the allocation question, then with realistic verifiers (test execution, PRM). We
  > report predicted directions (selective allocation recovers most of full-verification
  > accuracy at a small fraction of calls) as falsifiable hypotheses, not findings."
- **DOI** [PLACEHOLDER]: null
- **arXiv ID** [PLACEHOLDER]: null
- **Num pages** [PLACEHOLDER]: null
- **Research area** [HYPOTHESIS]: "AI/ML" (LLM inference-time scaling / verification economics).

**Status:** PARTIAL — title/core question are GIVEN; authors/abstract/DOI are placeholders because the paper doesn't exist.
**Absence comment:** {what_missing: "No real authorship, abstract, or publication metadata exists because this is a pre-writing planning artifact, not an extracted paper.", why_matters: "Downstream tools (se-paper-reviewer, pengsida-paper-writer) consuming this digest must not treat N0 as citable bibliographic fact.", implication: "Treat N0 purely as a working title/abstract draft for the research plan, to be replaced wholesale once a real paper is written."}

---

## N1 Problem Formulation

- **Objective** [HYPOTHESIS], built as a full predicate directly from the core question: "Given a fixed budget B of calls to a trustworthy but costly verifier, and a pool of N candidate reasoning trajectories per task instance sampled by an LLM (parallel chains-of-thought, best-of-N candidates, or agent rollouts), select which ≤B trajectories across the evaluation batch to submit for verification — and how to combine verified and unverified evidence into one final answer per instance — so as to maximize task accuracy per verifier call, relative to (a) uniform-random allocation at matched budget and (b) exhaustive verification (B = N × #instances)."
  - Self-check: task kind = selection/allocation under a hard resource constraint; domain = LLM reasoning-trajectory verification at inference time; outcome shape = a verified subset + final answers, evaluated as a budget–accuracy curve. All three land.
- **Inputs** [HYPOTHESIS], inferred from the minimal experiment:
  - N candidate trajectories per task instance, produced by temperature sampling (self-consistency-style) or parallel rollouts.
  - Per-trajectory verifier-free uncertainty/confidence signals computable before spending any verifier call (self-consistency mode share, normalized sequence log-likelihood, verbalized confidence — operationalized in N6/M1).
  - A fixed global verifier-call budget B, with B < N × #instances (otherwise the problem collapses to full verification).
- **Outputs** [HYPOTHESIS]:
  - The verified subset (size ≤ B) chosen by the allocation policy.
  - A final predicted answer per task instance, combining verifier outcomes (where spent) with unverified signal (where not).
  - Budget–accuracy curves and accuracy-per-verifier-call comparisons against baselines.
- **Constraints** [GIVEN, with light extrapolation]: the seed explicitly frames the verifier as *trustworthy* — the scarce resource is the number of calls, not the verifier's reliability (the seed's stated contrast with B1.5, where trustworthiness itself is in question). Implicitly, for selective allocation to beat uniform allocation, the pre-verification uncertainty signal must carry nonzero information about verifier-determined correctness; if it carries none, no allocation policy can outperform uniform sampling of the same size.

**Status:** PARTIAL — objective/inputs/outputs are HYPOTHESIS (conservative, closely grounded in the seed); the verifier-trustworthy constraint is GIVEN.
**Absence comment:** {what_missing: "No paper exists to state these formulation details explicitly.", why_matters: "Without an explicit formulation, a reviewer can't check whether the eventual paper's setup matches what the core question demands.", implication: "Treat this formulation as the target the real paper should hit, and revisit once a draft exists."}

---

## N2 Motivation

[HYPOTHESIS] Reconstructed from the parent-topic framing ("B4. 预算分配 / 推理经济学" — budget allocation / inference economics) and the grounded corpus literature; no invented statistics:

- **Motivation 1** [HYPOTHESIS, grounded in corpus framing]: Test-time compute scaling multiplies the number of candidate trajectories a verification step must judge. The corpus literature already treats *generation* compute as an allocation problem — `[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]` argues test-time compute "is expensive and increasingly central to deployment" and should be allocated by prompt difficulty; `[CaTS, OpenReview:jrSc4RJXy1]` notes uniform sampling budgets over-sample easy queries and under-explore hard ones. But the *verifier* side of the proposer–verifier pipeline has no analogous per-trajectory allocation account: verification is applied to every candidate or bundled invisibly into "the strategy."
- **Motivation 2** [HYPOTHESIS]: In deployed pipelines verification is either exhaustive (execution sandboxes, PRM scoring of all N candidates, a strong judge over every rollout — expensive) or absent (errors escape). Cascade/escalation work shows uncertainty-aware escalation cuts evaluation cost (`[Trust-or-Escalate, OpenReview:UHPnqSTBPO]`), and step-level routing shows budgeted strong-model intervention beats uniform intervention (`[TRIM, OpenReview:MoKrugWUfC]`), but neither answers the trajectory-pool question: with B calls and N > B candidates, which trajectories deserve the calls?
- **Motivation 3 — relation to B1.5** [HYPOTHESIS, explicitly cross-referencing the seed's stated link]: This topic is the mirror image of B1.5 (untrusted verifier). B4.5 assumes the opposite: the verifier's judgment is correct when consulted, and the only scarcity is how many times it can be consulted. The corpus split mirrors this: `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]` and `[OT-Verify, OpenReview:BBDhQJh6GB]` study verifier *imperfection* with unconstrained calls; B4.5 studies verifier *scarcity* with perfect calls. "How much to verify" and "whether to trust the verifier" are two independent axes of verification-under-limits; a complete inference-economics account needs both.

**Status:** PARTIAL (no paper exists to extract real motivation prose from).
**Absence comment:** {what_missing: "No real motivating claims/statistics from an actual introduction section.", why_matters: "Motivation strength (e.g., concrete per-call verifier cost figures) is what would make or break a reviewer's sense of importance.", implication: "Validate this framing with real cost data (e.g., PRM inference cost vs. sampler cost per trajectory) during the pilot."}

---

## N3 Related Works

All entries below except the last are **[GROUNDED:corpus]** — real OpenReview papers retrieved from
`topics/corpus/ideas.jsonl`; each `approach_summary` is grounded in the paper's own
motivation/method text, which was read in full. The final entry is a clearly marked
non-corpus canonical citation.

- **[CaTS, OpenReview:jrSc4RJXy1]** [GROUNDED:corpus] — approach_summary: Distills self-consistency-derived agreement statistics into a single-pass calibrated correctness-confidence predictor (pseudo-labels from cross-sample agreement, dynamic-temperature candidate generation, joint confidence-distillation fine-tuning), then uses that confidence for early stopping of repeated sampling — allocating *generation* compute per query by calibrated confidence. paper_url: https://openreview.net/forum?id=jrSc4RJXy1
- **[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]** [GROUNDED:corpus] — approach_summary: Formalizes inference-time methods as proposer–verifier combinations under a fixed compute budget and learns a difficulty-conditioned allocation policy (difficulty estimated from base-model statistics; validation-learned mapping from difficulty bins × budgets to inference hyperparameters) that picks between PRM-guided search and sequential revisions per prompt. paper_url: https://openreview.net/forum?id=4FWAwZtd2n
- **[ROC-n-reroll, OpenReview:3Gy5mmyuxn]** [GROUNDED:corpus] — approach_summary: Gives an exact per-query theory of how verifier imperfection shapes test-time scaling: represents the verifier by its ROC curve and derives closed-form accuracy–compute expressions for Rejection Sampling and Best-of-N under noisy verification, explaining when each is more compute-efficient and what governs asymptotic limits. paper_url: https://openreview.net/forum?id=3Gy5mmyuxn
- **[OT-Verify, OpenReview:BBDhQJh6GB]** [GROUNDED:corpus] — approach_summary: Models verifier-guided test-time sampling as optimal transport from the generator distribution to a coverage-constrained reward-maximizing target policy, decomposing sub-optimality into intrinsic transport cost and verifier-ROC-determined terms — a unified theory of coverage, verifier accuracy, and algorithm design. paper_url: https://openreview.net/forum?id=BBDhQJh6GB
- **[Trust-or-Escalate, OpenReview:UHPnqSTBPO]** [GROUNDED:corpus] — approach_summary: Selective, cascaded LLM-judge evaluation with provable human-agreement guarantees: confidence is estimated via simulated-annotator agreement, thresholds are exactly calibrated on a small human-labeled set (learn-then-test), and uncertain cases escalate through a cascade from cheap to strong judges to reduce evaluation cost. paper_url: https://openreview.net/forum?id=UHPnqSTBPO
- **[TRIM, OpenReview:MoKrugWUfC]** [GROUNDED:corpus] — approach_summary: Targeted stepwise routing for multi-step reasoning under a constrained strong-model token budget: a weak model drafts each reasoning step, a PRM scores the partial trace as a risk signal, and a budget-aware threshold (or learned sequential) policy decides which individual steps to regenerate with the strong model. paper_url: https://openreview.net/forum?id=MoKrugWUfC
- **[SAFER, OpenReview:kJmLmOvwLC]** [GROUNDED:corpus] — approach_summary: Two-stage risk-controlled sample-then-filter for open-ended QA: calibrates the minimum sampling budget that statistically covers an admissible answer (Clopper–Pearson bounds, abstaining when infeasible), then calibrates an uncertainty-score filtering threshold that prunes candidates while controlling the risk of discarding all admissible answers. paper_url: https://openreview.net/forum?id=kJmLmOvwLC
- **[Self-Capability, OpenReview:EO6WtJ0q6G]** [GROUNDED:corpus] — approach_summary: Evaluation framework for whether LLMs can predict their own success *before* acting: elicits ex-ante success probabilities on executable coding tasks (BigCodeBench, SWE-bench), places models in contract-style accept/decline decisions where failure is costly, and measures whether in-context experience improves confidence calibration and decision profitability. paper_url: https://openreview.net/forum?id=EO6WtJ0q6G
- **[Wang et al., 2023]** [NON-CORPUS — canonical, confident it exists: "Self-Consistency Improves Chain of Thought Reasoning in Language Models", ICLR 2023, arXiv:2203.11171] — approach_summary: Samples multiple chain-of-thought trajectories per question and takes a majority vote over final answers, with a fixed per-query sample count and no verification step; the agreement statistic it induces is the cheapest uncertainty signal this topic builds on.

**Status:** PARTIAL (works are real and grounded; their selection as "the" related work of a future paper is a hypothesis).
**Absence comment:** {what_missing: "No actual paper exists whose Related Work section could be extracted; this list is a grounded reconstruction from a real corpus search, not the eventual authors' own positioning.", why_matters: "The eventual paper may position against additional literature (e.g., active learning / optimal experiment design, bandit budget allocation) not surfaced by these corpus queries.", implication: "Re-run the search before writing, adding query angles for active testing, label-efficient evaluation, and bandit allocation; the current 8 corpus anchors are sufficient for N4's gap analysis."}

---

## N4 Prior Limitations

[HYPOTHESIS] What the N3 works demonstrably do not cover relative to this topic's core question — each limitation is defensible from the cited papers' own motivation/method text (what they state or what their method visibly does not do), tied to N3 via `affects_works` with exact citation_key strings.

- **Limitation 1** (limitation_type: other — problem-scope) [HYPOTHESIS]: Compute-allocation work budgets *generation*, not *verification*. `affects_works: ["[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]", "[CaTS, OpenReview:jrSc4RJXy1]"]` — Compute-Optimal-TTS allocates inference hyperparameters (how much search/revision per prompt) under a FLOPs budget, and CaTS uses calibrated confidence to decide *how many samples to draw*; in both, verifier/PRM scoring is bundled into the strategy rather than metered as its own scarce resource, so neither answers which of N already-sampled trajectories to submit when only B < N verifier calls are available.
- **Limitation 2** (limitation_type: other — problem-scope) [HYPOTHESIS]: Verifier-based test-time scaling theory assumes the verifier scores *every* candidate. `affects_works: ["[ROC-n-reroll, OpenReview:3Gy5mmyuxn]", "[OT-Verify, OpenReview:BBDhQJh6GB]"]` — in both analyses (Best-of-N scores all N samples; rejection sampling queries the verifier on every draw), the number of verifier calls is an *outcome* of the sampling policy, never an explicit hard constraint B < N; and their central object is verifier *imperfection* (ROC geometry), the exact opposite corner from this topic's trusted-but-scarce verifier.
- **Limitation 3** (limitation_type: generalizability) [HYPOTHESIS]: Selective evaluation with escalation optimizes risk control per evaluation item, not accuracy-per-call over a trajectory pool. `affects_works: ["[Trust-or-Escalate, OpenReview:UHPnqSTBPO]"]` — its objective is bounding disagreement-with-humans risk while maximizing coverage, with abstention/escalation decided item-by-item; it does not consider multiple competing trajectories for the same instance nor a hard global call budget to distribute across a batch.
- **Limitation 4** (limitation_type: generalizability) [HYPOTHESIS]: Step-level routing budgets tokens *within* one trajectory, not verifier calls *across* trajectories and instances. `affects_works: ["[TRIM, OpenReview:MoKrugWUfC]"]` — TRIM's own motivation states that local, threshold-based decisions "are insufficient because PRM scores are noisy and the value of intervention depends on trajectory"-level context; its unit of allocation is the reasoning step inside a single trace, leaving the cross-trajectory, cross-instance whole-trajectory verification allocation problem open.
- **Limitation 5** (limitation_type: other — problem-scope) [HYPOTHESIS]: Risk-calibrated sample-then-filter controls error probabilities, not budgeted use of an external trusted verifier. `affects_works: ["[SAFER, OpenReview:kJmLmOvwLC]"]` — SAFER calibrates a sampling budget and an uncertainty-based filtering threshold offline against admissibility labels; at test time no trusted verifier is invoked at all, so it cannot exploit even a small number of ground-truth-quality checks, which is precisely the resource B4.5 assumes.
- **Limitation 6** (limitation_type: other — measurement-vs-mechanism) [HYPOTHESIS]: Ex-ante confidence work measures whether the signal exists, not what an allocation policy built on it buys. `affects_works: ["[Self-Capability, OpenReview:EO6WtJ0q6G]"]` — it evaluates whether pre-action confidence predicts success and supports accept/decline decisions, reporting substantial miscalibration, but does not construct or evaluate a policy that converts such signals into budgeted verification decisions over candidate trajectories.
- **Limitation 7** (limitation_type: efficiency) [HYPOTHESIS]: Majority voting uses a fixed sample count, weights all samples equally, and verifies nothing. `affects_works: ["[Wang et al., 2023]"]` — this is also stated in the corpus record of `[CaTS, OpenReview:jrSc4RJXy1]`: self-consistency "uses a fixed sample count for every query and assigns equal weight to all samples regardless of their likely reliability"; consensus-wrong answers pass unchecked, which is exactly the failure a small verifier budget could catch if aimed well.

**Grounding check:** true — every limitation cites ≥1 N3 `citation_key`, verbatim string form.

---

## N5 Challenges

[HYPOTHESIS, problem-inherent obstacles any valid solution must overcome — not weaknesses of the N3/N4 works. Ids stable from the previous digest revision.]

- **C1 — Signal-before-truth**: Any signal used to decide *which* trajectories to verify must be computed before the verifier reveals correctness, so the ranking necessarily operates on a noisy proxy for the very quantity it predicts. Worse, the proxy's errors are structured against the policy: the highest-value verification targets include *confident-but-wrong* consensus cases (all N samples agree on a wrong answer), which is precisely where agreement-based uncertainty says "don't spend here." Selective allocation only beats uniform iff the signal–correctness correlation is materially nonzero on the deployed distribution.
- **C2 — Domain transfer of signal informativeness**: The correctness-information content of a given uncertainty signal (mode share, log-likelihood, verbalized confidence) varies across task types — short-answer math with a small answer space behaves differently from open-ended code with an unbounded output space — so a policy tuned on one domain may be uninformative, or mis-ranked, on another.
- **C3 — Combinatorial/online allocation under a global budget**: With one budget B shared across many instances and N trajectories each, allocation is not a per-item threshold: the policy must trade "verify a second trajectory of this uncertain instance" against "verify the first trajectory of the next instance," and — if calls are spent sequentially — must decide with each outcome whether to keep probing the same instance or move on. This is an online resource-allocation problem; any static ranking is only an approximation to it.
- **C4 — Aggregation of mixed evidence**: Verified outcomes (ground-truth-grade, but sparse) and unverified signals (dense, but noisy) must be combined into a single answer per instance without discarding the information the budget bought — e.g., a verified-*incorrect* result eliminates a candidate but does not name the right answer, and the aggregator must exploit that elimination rather than fall back to the raw vote.

**Conflation check:** true — C1 (proxy validity), C2 (transfer), C3 (online allocation), and C4 (aggregation) are distinct obstacles: fixing any one does not fix the others.

---

## N6 Methodology

**Overview** [HYPOTHESIS]: A budget-constrained selection pipeline over sampled trajectory pools, developed in two stages. **Stage 1 — pilot (= the seed's minimal experiment, made operational)**: for each instance, sample N = 16 trajectories from one open model (Qwen2.5-7B-Instruct; second family Llama-3.1-8B-Instruct for robustness) on GSM8K and MATH-500; compute three verifier-free uncertainty signals per trajectory (M1); allocate a global verifier budget of b ∈ {5%, 10%, 25%, 50%} of all trajectories by static most-uncertain-first ranking (M2); use an *oracle verifier* (ground-truth answer check) so that the seed's "verifier 可信" assumption holds exactly and the allocation question is isolated from verifier quality (M3-a); aggregate with the elimination-aware rule (M4); compare against uniform-random allocation at matched budget, full verification, and unverified majority vote. **Stage 2 — scale-up**: replace the oracle with realistic trusted verifiers (unit-test execution on HumanEval+/MBPP+; an open PRM scorer for math) (M3-b), grow to N = 64 samples, add the sequential reallocation policy (M5), test cross-domain transfer of policies tuned on math to code (and vice versa), and run a verifier-noise sensitivity sweep that connects the trusted-verifier regime to the imperfect-verifier regime analyzed by `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]`.

**Key components** [HYPOTHESIS — each states what is measured/built, with what instrument, at what granularity]:
- **M1 — Uncertainty scorer (per-trajectory, pre-verification)**: computes, for every trajectory before any verifier call: (a) *mode share* — fraction of the instance's N sampled final answers agreeing with this trajectory's final answer (exact-match for math, test-input output equivalence for code); (b) *normalized sequence log-likelihood* — mean token log-probability of the trajectory under the sampling model; (c) *verbalized confidence* — a 0–100 self-rating elicited by one fixed follow-up prompt. Instrumented output: a per-trajectory score table plus, on held-out data, the AUROC of each signal against verifier-labeled correctness — the direct measurement of C1's proxy gap.
- **M2 — Budget-constrained selection policy (static)**: given M1 scores and global budget B, ranks all trajectories in the batch most-uncertain-first and submits the top B. Two granularities are implemented and compared: *trajectory-level* (rank all N × #instances trajectories jointly) and *instance-level* (rank instances by lowest mode share; within a selected instance, verify the most frequent distinct answers first, which maximizes information per call).
- **M3 — Trusted verifier (two instantiations)**: (a) *oracle verifier* (pilot): a ground-truth lookup that labels a submitted trajectory's final answer correct/incorrect — makes "trusted" exact by construction and isolates allocation from verifier quality; (b) *realistic verifiers* (scale-up): sandboxed execution of held-out unit tests for code; an open process-reward-model scorer thresholded to a binary judgment for math. Instrumented output: per-call binary labels plus per-call wall-clock/token cost, used to report real accuracy-per-dollar alongside accuracy-per-call.
- **M4 — Answer aggregator (elimination-aware)**: per instance: if any verified-correct trajectory exists, output its answer; else remove all verified-incorrect *answers* from the candidate set and take the confidence-weighted majority vote over the remainder; if verification eliminated every candidate answer, output the highest-confidence unverified answer and flag the instance. Compared against the naive rule ("use verified answer if any, else raw majority vote") in an ablation to quantify C4's cost.
- **M5 — Sequential reallocation policy (scale-up extension)**: spends the budget one call at a time; after each outcome, stops probing any instance that has a verified-correct trajectory and reallocates remaining calls to the next-most-uncertain unresolved instance. Evaluated as the online upgrade of M2, measuring how much of the static policy's gap to a hindsight-optimal allocation it closes.

**Challenge arguments** [HYPOTHESIS]:
- C1 ← [M1, M3]: "M1 is restricted to verifier-free signals precisely because C1 forbids peeking at correctness; its AUROC against M3's labels is the paper's central measured quantity, not an assumption — and the confident-but-wrong failure case is directly observable as verified-incorrect trajectories with high mode share."
- C2 ← [M1, M2]: "Running the identical M1/M2 pipeline on math (GSM8K, MATH-500) and code (HumanEval+, MBPP+), plus the explicit cross-domain policy-transfer test in Stage 2, is the designed probe of whether signal informativeness and the resulting allocation gains generalize."
- C3 ← [M2, M5]: "M2's two granularities (trajectory-level vs instance-level ranking) probe the cross-instance dimension of C3 within a static policy, and M5 is the direct sequential response — its measured gap-closure against hindsight-optimal allocation quantifies how much the online character of C3 actually matters."
- C4 ← [M4]: "M4's elimination-aware rule is the component responsible for not wasting verified-incorrect outcomes; the ablation against the naive rule measures C4's aggregation cost in accuracy points at matched budget."

**Unaddressed challenges** [HYPOTHESIS, V-08 flagged]: `["C3"]` — partially addressed only. The pilot is deliberately static; M5 covers sequential reallocation within one batch, but the fully online setting (streaming instances, unknown horizon, budget shared with future batches) remains out of scope. This flag rests on an inferred design (M5), so it must not be read with extracted-level confidence.

**Feasibility** [HYPOTHESIS]:
- *Pilot*: 2 datasets × ~500 instances × 16 samples × 2 models ≈ 64K generations (~40M tokens) plus 64K short confidence-elicitation calls; roughly 1–2 days on a single A100/H100 with vLLM, or low-hundreds-of-dollars API class. Oracle verification is free (label lookup). No annotators. ~10–15 experiment runs (2 models × 2 datasets × ~4 budget levels, plus 5 sampling seeds on the primary configuration).
- *Scale-up*: N = 64 on 4 datasets × 2 models ≈ 10× pilot token volume (~1–2 GPU-weeks or a ~$1–3K API-cost class), plus PRM inference (~1 GPU-day) and sandboxed test execution (CPU, negligible).
- *Single biggest feasibility risk*: the uncertainty signal may be degenerate on the chosen benchmarks — if the base model is too strong (near-unanimous agreement almost everywhere) or too weak, mode share collapses to a constant and *no* allocation policy can differ from uniform, voiding RQ1 rather than answering it. *Mitigation*: pre-screen model–dataset pairs in a 50-instance dry run and keep only pairs with base accuracy in the 30–70% band and non-trivial mode-share variance (e.g., interquartile range > 0.2); MATH-500 levels 3–5 and MBPP+ provide difficulty knobs if GSM8K saturates.

---

## N7 Contributions

[HYPOTHESIS] What such a paper would plausibly claim, framed from the method + expected findings:

- **CO1** [conceptual_framework, is_testable=true, has_rq=true]: A formalization of selective verifier-call allocation as budget-constrained trajectory selection with a *trusted* verifier — explicitly the complementary corner to verifier-imperfection analyses (`[ROC-n-reroll, OpenReview:3Gy5mmyuxn]`) and to the untrusted-verifier topic B1.5.
- **CO2** [empirical_finding, is_testable=true, has_rq=true]: A measured comparison of uncertainty-guided vs uniform-random allocation at matched budgets, including which of three verifier-free signals buys the most accuracy per call.
- **CO3** [empirical_finding, is_testable=true, has_rq=true]: A characterization of the budget–accuracy curve — what fraction of the full-verification accuracy gain is recovered at what fraction of calls — and of how that recovery rate depends on task domain, policy granularity, and verifier realism.
- **CO4** [empirical_finding, is_testable=true, has_rq=true]: An ablation-backed account of the aggregation axis (C4): how much accuracy the elimination-aware aggregator adds over the naive rule at matched budget, establishing aggregation as a design axis distinct from selection.

---

## N8 Research Questions

- **RQ1** [GIVEN, near-verbatim restatement of the seed's core question]: "When verifier calls are limited by a fixed budget, which trajectories should be verified to maximize accuracy-per-verifier-call?" — evaluates_mechanisms: [M1, M2], addresses_challenges: [C1], tests_contributions: [CO1, CO2] — answered_by_experiment: "Pilot: signal-AUROC measurement plus matched-budget comparison of the three M1 signals under M2 against uniform allocation, oracle verifier."
- **RQ_INF_1** [HYPOTHESIS, inferred from the minimal experiment's explicit comparison design]: "Does most-uncertain-first allocation outperform uniform-random allocation at matched budgets, and how much of the full-verification accuracy gain does it recover as the budget fraction varies?" — evaluates_mechanisms: [M1, M2, M4], addresses_challenges: [C1, C4], tests_contributions: [CO2, CO3, CO4] — answered_by_experiment: "Budget–accuracy curves at b ∈ {5,10,25,50,100}% with the M4-vs-naive aggregation ablation."
- **RQ_INF_2** [HYPOTHESIS, inferred from the staged plan]: "Do the allocation gains transfer across task domains and survive the move from an oracle verifier to realistic verifiers, and how much does sequential reallocation add over static ranking?" — evaluates_mechanisms: [M1, M2, M3, M5], addresses_challenges: [C2, C3], tests_contributions: [CO1, CO3] — answered_by_experiment: "Stage-2 cross-domain policy transfer (math↔code), oracle-vs-execution/PRM verifier comparison, and M5-vs-M2 gap-closure measurement."

**Datasets** [HYPOTHESIS — real benchmarks that genuinely fit]: names: ["GSM8K (test split, 1,319 grade-school math word problems; pilot uses a fixed 500-instance subsample)", "MATH-500 (500-problem competition-math subset, difficulty levels 1–5)", "HumanEval+ (164 code tasks with EvalPlus-extended test suites, enabling exact execution-based verification)", "MBPP+ (378 code tasks, EvalPlus variant, same property)"].
**Baselines** [HYPOTHESIS — named, drawn from N3 where possible]: names: ["Uniform-random verifier-call allocation at matched budget (the seed's stated control)", "Full verification, B = N × #instances (upper anchor)", "No verification: self-consistency majority vote [Wang et al., 2023] (lower anchor)", "Difficulty-conditioned instance-level allocation adapted from [Compute-Optimal-TTS, OpenReview:4FWAwZtd2n] (allocate calls by estimated instance difficulty rather than trajectory uncertainty)", "Confidence-threshold escalation adapted from [Trust-or-Escalate, OpenReview:UHPnqSTBPO] (verify iff confidence < calibrated threshold, ignoring the global budget coupling)"].
**Metrics** [HYPOTHESIS — with definitions]: names: ["accuracy@budget: fraction of instances answered correctly when the policy spends exactly B calls", "accuracy-per-verifier-call: (accuracy@B − accuracy@0) / B, marginal value of the budget", "budget-recovery fraction: (accuracy@B − accuracy@0) / (accuracy@N − accuracy@0), share of the full-verification gain recovered at budget B", "AUBC: area under the budget–accuracy curve over b ∈ [0,1], scalar policy summary", "signal AUROC: discrimination of each M1 signal against verifier-labeled trajectory correctness"].
**Analysis plan** [HYPOTHESIS]: Sample size ≥500 instances per dataset (≥164 for HumanEval+, its full size), 5 sampling seeds on the primary configuration. Primary test: per budget level, paired comparison of instance-level correctness between selective and uniform allocation on identical trajectory pools — McNemar's test plus a 10,000-resample paired bootstrap CI on the accuracy difference; significance threshold α = 0.05 with Holm–Bonferroni correction across the 4 budget levels × 4 datasets family. Expected effect direction: selective > uniform at every b < 100%, with the largest gap at small budgets (b ≤ 25%) and monotone convergence to the full-verification anchor as b → 1; secondary expectation: instance-level granularity ≥ trajectory-level granularity of M2. Signal comparison via AUROC with DeLong CIs.

**Status:** PARTIAL — RQ1 is GIVEN; RQ_INF_1/RQ_INF_2, datasets, baselines, metrics, and the analysis plan are HYPOTHESIS.
**Absence comment:** {what_missing: "No paper exists to state actual datasets/baselines/metrics; these are a concrete proposal inferred from the one-line minimal experiment plus the grounded corpus baselines.", why_matters: "Benchmark choice materially affects whether the uncertainty signal is informative (C1/C2) — the pre-screening rule in N6-Feasibility exists precisely because of this.", implication: "Treat this as a pre-registration draft: fix the instance subsets, seeds, and the Holm–Bonferroni family before running Stage 1."}

---

## N9 Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTIONS ONLY. No experiment has been run; no numbers exist; these are falsifiable predictions, not findings.]**

- **Result 1** → rq_id: RQ1. result_text [PLACEHOLDER-HYPOTHESIZED, direction only]: "Predicted: mode share is the strongest single verifier-free signal (highest AUROC against verifier labels), and spending the budget on low-mode-share trajectories yields higher accuracy-per-verifier-call than any baseline allocation at matched B." result_type: quantitative (predicted). evidence_strength: "missing". rq_answered: false.
  - **Falsification condition**: refuted if, on the pre-screened model–dataset pairs, every M1 signal's AUROC against verifier-labeled correctness is ≤ 0.55 (indistinguishable from chance within its DeLong CI), or if no signal-ranked allocation beats uniform-random allocation at any budget level after Holm–Bonferroni correction — that outcome would mean C1's proxy gap is effectively total and selective checking has no advantage over spending the budget blindly.
- **Result 2** → rq_id: RQ_INF_1. result_text [PLACEHOLDER-HYPOTHESIZED, direction only]: "Predicted: uncertainty-guided allocation recovers the majority of the full-verification accuracy gain (budget-recovery fraction > 0.5) at b = 25% of calls, exceeds uniform allocation at every b < 100%, and the elimination-aware aggregator (M4) adds accuracy over the naive rule at matched budget." result_type: quantitative (predicted). evidence_strength: "missing". rq_answered: false.
  - **Falsification condition**: refuted if the selective-vs-uniform accuracy difference is not significantly positive (McNemar + paired bootstrap, corrected α = 0.05) at any b < 100%, or if budget-recovery fraction at b = 25% is statistically indistinguishable from b itself (i.e., recovery is merely proportional to spend, the signature of an uninformative ranking); the M4 sub-claim is separately refuted if the elimination-aware rule fails to beat the naive rule in the ablation.
- **Result 3** → rq_id: RQ_INF_2. result_text [PLACEHOLDER-HYPOTHESIZED, direction only]: "Predicted: allocation gains persist but shrink when the oracle verifier is replaced by execution/PRM verifiers; policies transfer math↔code with reduced but positive advantage over uniform; sequential reallocation (M5) closes a further portion of the static policy's gap to hindsight-optimal allocation, with its benefit concentrated at small budgets." result_type: quantitative (predicted). evidence_strength: "missing". rq_answered: false.
  - **Falsification condition**: refuted (transfer sub-claim) if a policy tuned on one domain performs no better than uniform allocation on the other domain; refuted (realism sub-claim) if gains vanish entirely under execution-based verification on code — where the verifier is genuinely near-ground-truth — since that cannot be blamed on verifier noise and would instead indict the signal or the aggregation; refuted (M5 sub-claim) if sequential reallocation is statistically indistinguishable from static ranking at every budget.

---

## N10 Threats

[HYPOTHESIS] Anticipated threats to validity, categorized; no real Limitations section exists, so every item is a prediction of what such a section must address, each with a planned mitigation.

- **t1** [construct]: "Uncertainty" is operationalized by three specific signals (mode share, sequence log-likelihood, verbalized confidence); conclusions about "selective checking" could be artifacts of this choice, and mode share in particular is undefined for single-sample pipelines. — *Mitigation*: report all three signals separately plus their rank-combination; frame headline claims per-signal, never as "uncertainty" in the abstract sense; the AUROC table makes the construct's validity itself a measured result.
- **t2** [internal]: The pilot's oracle verifier conflates "trusted verification" with ground-truth lookup, and because the same ground truth defines the accuracy metric, any leakage of verifier outcomes into signal computation (rather than only into selection/aggregation) would trivialize the result. — *Mitigation*: strict pipeline separation (M1 scores are computed and frozen before any M3 call); Stage 2's execution/PRM verifiers break the oracle identity entirely, and the code domain's execution verifier is trusted *without* being the evaluation oracle (held-out tests vs. EvalPlus full suites).
- **t3** [external]: Results come from two open model families (7–8B class) on math and code benchmarks with short, checkable final answers; generalization to frontier models, long-horizon agentic trajectories, human verifiers, or domains without exact answer matching is untested — and the seed's own contrast case (untrusted verifiers, B1.5) is explicitly out of scope. — *Mitigation*: two model families × two domains bound the obvious single-setup risk; the digest and eventual paper must scope claims to "sampled-trajectory pools with checkable answers" and flag agentic rollouts as future work.
- **t4** [conclusion]: The evaluation grid (4 datasets × 4 budget levels × 3 signals × 2 policy granularities) invites multiple-comparison false positives, and instance-level correctness within a shared trajectory pool violates independence assumptions of naive tests. — *Mitigation*: pre-registered directional hypotheses (N8 analysis plan), paired tests on identical pools, Holm–Bonferroni within each declared family, and paired-bootstrap CIs reported alongside p-values.
- **t5** [reproducibility]: Trajectory sampling, verbalized-confidence elicitation, and PRM thresholds are all stochastic or configuration-sensitive; a re-run could shift budget–accuracy curves. — *Mitigation*: 5 fixed seeds on the primary configuration with seed-level dispersion reported; frozen prompts, fixed instance subsamples, and released sampling caches so allocation policies can be re-evaluated on identical pools without re-generation.

**Status:** PARTIAL (no paper exists; these are anticipated, not author-stated).
**Absence comment:** {what_missing: "No Threats-to-Validity section exists because no paper has been written.", why_matters: "A reviewer cannot yet check whether the eventual authors' stated limitations match these anticipated ones.", implication: "Use this list as a pre-registration-style checklist; replace with the authors' actual Limitations section once written."}

---

## N11 Artifacts

**Status:** NOT_FOUND [PLACEHOLDER] — nothing has been released because the paper does not exist.
- artifacts: []
- has_code: false
- has_data: false
- has_model: false

**Absence comment:** {what_missing: "No code, data, or model artifacts exist for a paper that has not been written.", why_matters: "Artifact availability is a standard reviewer signal for reproducibility; its absence here is structural (pre-writing stage), not a red flag about a real paper.", implication: "The N10-t5 mitigation (released sampling caches + policy-evaluation code) defines the artifact set the eventual paper should ship; re-check this node once a repository exists."}

---

## N12 Contribution Type

**Value** [HYPOTHESIS]: `empirical`

**Rationale** [HYPOTHESIS, re-checked against the upgraded N6–N9]: The primary deliverable remains a measurement/comparison study: the headline outputs are budget–accuracy curves, signal-AUROC tables, and matched-budget policy comparisons with statistical testing (N8 analysis plan, N9 predicted results) — evaluating how existing sampling pipelines respond to a verifier-call constraint, not shipping a new model, dataset, or system. The mechanisms built (M1 scorers, M2/M5 policies, M4 aggregator) are deliberately lightweight instruments in service of the measurement, closely analogous to how best-paper empirical studies (e.g., a formatting-cost study that builds a transformation tool, or a debate study that builds an Elo tournament harness) are still classified `empirical`: the artifact serves the RQs rather than being their object. `theoretical` is wrong (CO1's formalization carries no proved results, unlike `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]`); `benchmark`/`tool` are wrong (all datasets are existing benchmarks; no released tool is a contribution claim).

---

## Claims

- **Claim 1** [HYPOTHESIS]: "Selective, uncertainty-guided verification can recover the majority of the full-verification accuracy gain while spending a small fraction of the verifier-call budget." — evidence: [{type: "argument", text: "Predicted direction from the seed's minimal experiment plus the grounded observation that self-consistency statistics correlate with correctness (per the corpus record of [CaTS, OpenReview:jrSc4RJXy1])", source: "HYPOTHESIS", location: "N9 Result 2"}].
- **Claim 2** [GIVEN, near-verbatim from the seed]: "This topic is the mirror image of B1.5: there the verifier's trustworthiness is in question; here the verifier is trusted and the only scarce resource is the number of calls to it." — evidence: [{type: "citation", text: "与 B1.5 呼应但立场相反（这里 verifier 可信，问怎么省着用）", source: "GIVEN", location: "seed README, 最小实验"}].
- **Claim 3** [HYPOTHESIS]: "No prior work in the grounded corpus meters calls to a *trusted* verifier as the explicit scarce resource over a trajectory pool: compute-allocation work budgets generation, verifier-scaling theory assumes all candidates are scored, and escalation/routing work allocates per evaluation item or per reasoning step." — evidence: [{type: "citation", text: "N4 Limitations 1–5 with their affects_works keys, each defensible from the cited paper's own motivation/method text", source: "HYPOTHESIS", location: "N3/N4"}].
- **Claim 4** [HYPOTHESIS]: "A verifier-free uncertainty signal is a structurally imperfect proxy — its worst errors (confident-but-wrong consensus) sit exactly where verification would pay most — so no purely signal-ranked policy is optimal, and measuring this gap is a result in itself." — evidence: [{type: "argument", text: "Derived from C1 as a problem-inherent obstacle; operationalized as the signal-AUROC measurement and the verified-incorrect-with-high-mode-share count", source: "HYPOTHESIS", location: "N5 C1 / N6 M1 / N9 Result 1 falsification"}].
- **Claim 5** [PLACEHOLDER]: "The budget-recovery rate of selective allocation is domain-dependent and shrinks — but does not vanish — under realistic verifiers and cross-domain policy transfer." — evidence: [{type: "argument", text: "Predicted from C2/C3; no data collected; explicitly falsifiable per N9 Result 3", source: "PLACEHOLDER", location: "N9 Result 3"}].

---

## Self-verification pass (performed before output)

- **V-01 (locator/grounding integrity):** No item is presented with extracted-level confidence; all substantive content is GIVEN, HYPOTHESIS, PLACEHOLDER, or GROUNDED:corpus. Every GROUNDED:corpus entry carries a real OpenReview `paper_id` and `paper_url` from `topics/corpus/ideas.jsonl`, and its approach_summary was written after reading the record's full motivation+method text.
- **V-02 (absence comment shape):** Every node with non-FOUND status (N0, N1, N2, N3, N8, N10, N11) carries a full 3-part absence_comment.
- **V-04 / EX-09 (ID consistency):**
  - N3 citation_keys = {`[CaTS, OpenReview:jrSc4RJXy1]`, `[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]`, `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]`, `[OT-Verify, OpenReview:BBDhQJh6GB]`, `[Trust-or-Escalate, OpenReview:UHPnqSTBPO]`, `[TRIM, OpenReview:MoKrugWUfC]`, `[SAFER, OpenReview:kJmLmOvwLC]`, `[Self-Capability, OpenReview:EO6WtJ0q6G]`, `[Wang et al., 2023]`}. Every N4.affects_works string appears verbatim in this set ✓ (L1: CaTS + Compute-Optimal-TTS; L2: ROC-n-reroll + OT-Verify; L3: Trust-or-Escalate; L4: TRIM; L5: SAFER; L6: Self-Capability; L7: Wang et al., 2023).
  - N6.challenge_arguments.challenge_id ⊆ N5 ids {C1,C2,C3,C4} ✓; mechanism_components ⊆ {M1..M5} ✓; unaddressed_challenges = {C3} ⊆ N5 ids ✓.
  - N8: RQ1 → M1,M2 / C1 / CO1,CO2 ✓; RQ_INF_1 → M1,M2,M4 / C1,C4 / CO2,CO3,CO4 ✓; RQ_INF_2 → M1,M2,M3,M5 / C2,C3 / CO1,CO3 ✓ — all C/M/CO ids exist.
  - N9.rq_id ∈ {RQ1, RQ_INF_1, RQ_INF_2} — all three N8 ids covered, no orphans ✓.
- **V-08 (confidence doesn't inflate under inference):** N6.unaddressed_challenges flagged as resting on the inferred M5 design; N9 carries no numbers, only directions with explicit falsification conditions; N3's non-corpus entry is explicitly marked as such.
- **V-10/V-11:** N10 status PARTIAL with 5 categorized threats (construct/internal/external/conclusion/reproducibility), each with a mitigation ✓; N11 NOT_FOUND with empty artifact list and all flags false ✓.
- **V-12:** N12 rationale names the deciding evidence (budget–accuracy measurement as the deliverable; lightweight instruments in service of RQs) and rules out adjacent types (theoretical, benchmark, tool) non-circularly.
- **EX-12 field-name spot check:** `objective`, `motivations`-style prose, `citation_key`, `approach_summary`, `limitation_text`-style entries with `limitation_type`, `text` for challenges, `evidence_strength`, `rq_answered`, `threat_id`/`category`/`mitigation` — no forbidden renames.
- **EX-11 empty-node check:** all of N0–N12 plus Claims present, including the NOT_FOUND node (N11) with full absence_comment and empty lists.
- **RQ-id stability check:** RQ1 and RQ_INF_1 retain their previous ids and core intent; RQ_INF_2 is additive. C1–C4 and M1–M5 ids retained from the prior revision with sharpened text.
