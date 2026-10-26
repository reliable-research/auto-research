# Digest: Exchange Rates between Thinking, Sampling, and Verifying under a Fixed Dollar Budget

> **REVERSE-DIGEST NOTICE.** This is speculative scaffolding for research planning. No paper
> with this title exists yet. Every field below is tagged **[GIVEN]** (verbatim/near-verbatim
> from the seed README), **[HYPOTHESIS]** (reasoned elaboration / prediction, not a fact),
> **[GROUNDED:corpus]** (a real OpenReview paper retrieved from the local corpus
> `topics/corpus/ideas.jsonl`, summarized from its own motivation/method text), or
> **[PLACEHOLDER]** (genuinely unknowable until the work is done — never invented). Treat
> anything not tagged [GIVEN] or [GROUNDED:corpus] as a forecast, not a finding.

**Seed source:** `topics/B4.2_exchange_rates_between_thinking_sampling_and_verifying_under_a_f/README.md`
**Topic code:** B4.2 · **Label:** [证据] (Evidence-type gap) [GIVEN] · **Parent topic:** B4. 预算分配 / 推理经济学 (Budget Allocation / Inference Economics) [GIVEN]

---

## N0 — Metadata

- `title`: "Exchange Rates between Thinking, Sampling, and Verifying under a Fixed Dollar Budget" **[GIVEN]** — verbatim from seed README.
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — paper does not exist; no authors to report.
- `abstract` **[HYPOTHESIS]** (drafted by synthesizing the core question + minimal experiment; explicitly a draft, not a real abstract):
  > "Deploying LLM reasoning systems under a fixed dollar budget requires choosing among three largely orthogonal levers: lengthening chain-of-thought (CoT) reasoning, drawing more independent samples, and spending part of the budget on a verifier that selects among samples. Prior work studies each lever's scaling behavior, and compute-optimal analyses compare strategies under FLOPs- or token-matched budgets, but no study meters all three levers in a single dollar-denominated budget in which the verifier's own cost competes with generation. We treat the three levers as tradeable currencies and measure their empirical exchange rates: we grid-scan the (CoT-length L, sample-count N, verifier-calls V) allocation at matched total dollar cost across task families spanning cheaply-verifiable (math, code) and hard-to-verify (open QA) domains, extract the accuracy-per-dollar Pareto frontier per family, and test whether the frontier's shape — dominant lever, elbow location, marginal rates of substitution — is stable across families. We report the shape of the efficient frontier and the conditions under which each lever dominates."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"AI/ML"` **[HYPOTHESIS]** — LLM test-time compute / inference economics; NLP is a plausible alternate tag but AI/ML better captures the systems/economics framing of the parent topic.
- **Status:** `PARTIAL` — title given, everything else inferred or placeholder. `absence_comment`: `{"what_missing": "No real author list, abstract, or bibliographic identifiers exist because no paper has been written.", "why_matters": "Downstream tools (se-paper-reviewer, pengsida-paper-writer) that key off N0 need to know these are planning placeholders, not extracted facts.", "implication": "Treat N0 purely as a planning scaffold; regenerate this node from the real paper once it exists."}`

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**, built as a full predicate directly from the core question: "measure, via a controlled grid scan under a fixed per-query dollar budget, the empirical substitution (exchange) rates among three test-time compute levers for LLM reasoning — extended chain-of-thought length, repeated sampling, and verifier invocation (where the verifier's own token cost is charged against the same budget) — and characterize the resulting accuracy-per-dollar Pareto frontier per task family, including a statistical test of whether frontier shape is stable across task families."
  - Self-check: kind of task = *measurement / benchmarking study*; domain = *LLM test-time reasoning / inference-cost economics*; outcome shape = *an empirical Pareto frontier per task family + a quantified cross-family stability verdict*. All three dimensions land.
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  - A fixed total dollar budget per query (a small ladder of budget levels).
  - A base LLM with a controllable thinking-token budget (CoT length L).
  - A sampling mechanism producing N independent generations at fixed temperature.
  - A verifier (LLM judge / reward model) callable per candidate, with its own metered per-call token cost.
  - A suite of task families with checkable or rubric-gradable ground-truth answers.
- `outputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  - Accuracy and realized dollar cost at each point of the 3D (L, N, V) budget grid, per task family.
  - The empirical accuracy-per-dollar Pareto frontier (non-dominated allocations) per family, with bootstrap confidence bands.
  - Estimated marginal rates of substitution between lever pairs along the frontier.
  - A cross-task-family stability verdict on frontier shape, with a statistical test.
- `constraints` **[GIVEN]**+**[HYPOTHESIS]**: (a) tasks must have checkable/gradable outcomes so accuracy-per-dollar is computable **[GIVEN, implied by "accuracy-per-dollar"]**; (b) the three levers' costs must be reducible to one common dollar unit (token price × tokens for generation AND for the verifier's own tokens) **[HYPOTHESIS]**; (c) realized cost is stochastic (output lengths vary), so "matched budget" must be operationalized as matched-cost bins, not exact equality **[HYPOTHESIS]**.
- **Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "No paper exists to state inputs/outputs/constraints explicitly; they are reconstructed from a two-sentence core question and minimal experiment.", "why_matters": "A reviewer needs to know the task formulation is a forecast so they don't hold the (non-existent) authors to inferred inputs they never committed to.", "implication": "Use this as a first-draft experimental design, not a settled protocol — revisit once the pilot task suite is locked."}`

---

## N2 — Motivation

**`motivations`** (each `{motivation_text, source, location, evidence}`), reconstructed from the parent-topic framing plus the grounded corpus's own motivation texts **[HYPOTHESIS, with corpus-grounded evidence]**:

1. `motivation_text`: "Practitioners deploying LLM reasoning systems pay a real, meterable dollar cost per query and must split that budget among thinking longer, sampling more, or paying a verifier to select among samples — but there is no empirically-measured guide to the relative dollar value of each lever." **[HYPOTHESIS]** `source: HYPOTHESIS`, `location: null`, `evidence: [{type: "citation", text: "'inference-time compute is expensive and increasingly central to deployment. If compute can be allocated adaptively, smaller models with well-chosen inference strategies could outperform much larger models under matched FLOPs' — motivation text of [SnellTTC, OpenReview:4FWAwZtd2n]", source: GROUNDED:corpus, location: {corpus: "ideas.jsonl", paper_id: "4FWAwZtd2n"}}]`.
2. `motivation_text`: "The field has established that allocation matters as much as quantity for test-time compute, but existing allocation studies denominate budgets in FLOPs, tokens, or sample counts — never in dollars with the verifier's own cost inside the constraint — so the practitioner-facing question (what does a marginal dollar buy on each lever?) remains unanswered." **[HYPOTHESIS]** `evidence: [{type: "citation", text: "'additional inference compute can be highly effective but exhibits diminishing returns, implying that compute allocation matters as much as compute quantity' — motivation text of [PlanAndBudget, OpenReview:ctspw4CqbS]", source: GROUNDED:corpus, location: {corpus: "ideas.jsonl", paper_id: "ctspw4CqbS"}}]`.
3. `motivation_text`: "Verification is increasingly treated as a scalable inference-time component in its own right — sometimes cheaper than discovery — which makes the three-way trade (think vs. sample vs. verify) a live economic decision rather than a fixed pipeline choice." **[HYPOTHESIS]** `evidence: [{type: "citation", text: "'If a verifier can actively use web tools to test candidate answers, then part of the test-time budget can be shifted from expensive answer discovery to cheaper answer checking, potentially yielding a much better accuracy-cost trade-off' — motivation text of [AsymVerify, OpenReview:hxL4Uf9tR3]", source: GROUNDED:corpus, location: {corpus: "ideas.jsonl", paper_id: "hxL4Uf9tR3"}}]`.

Do NOT place prior-work failures here (they belong in N4).

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "No paper text exists to quote motivating statements verbatim; motivations are synthesized, though each is now anchored to a real corpus paper's own motivation text.", "why_matters": "Motivation strength is normally judged from the authors' own framing, which cannot exist yet.", "implication": "Replace with the actual introduction once written; the corpus anchors above are the citations that introduction should open with."}`

---

## N3 — Related Works

**Methodology note [GROUNDED:corpus search process]:** Five keyword queries were run against the local 11,683-paper OpenReview corpus (`topics/corpus/ideas.jsonl`) on 2026-07-04, covering: (1) test-time compute scaling / compute-optimal inference, (2) best-of-N sampling / verifier / reward model / self-consistency, (3) chain-of-thought length / overthinking / reasoning token budget, (4) inference cost / Pareto frontier / budget allocation, (5) repeated sampling / coverage / parallel vs. sequential scaling. Full motivation+method texts of the top hits were read; the 8 best-fitting works are below, plus 1 canonical non-corpus work. Every `approach_summary` is grounded in the paper's own proposal text.

`works`:

1. `citation_key`: `"[SnellTTC, OpenReview:4FWAwZtd2n]"` **[GROUNDED:corpus]**
   `approach_summary`: "Formalizes inference-time methods as proposer–verifier combinations under a fixed compute budget and learns a compute-optimal, difficulty-conditioned allocation policy: prompt difficulty is estimated from base-model statistics, and a mapping from difficulty bins and budgets to inference hyperparameters (best-of-N vs. PRM-guided search vs. learned sequential revisions) is fit on validation data, showing adaptive allocation can beat much larger models at matched FLOPs."
   `paper_url`: https://openreview.net/forum?id=4FWAwZtd2n
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "4FWAwZtd2n", query: "test-time compute scaling; compute-optimal"}`

2. `citation_key`: `"[VerifierFreeSuboptimal, OpenReview:beeNgQEfe2]"` **[GROUNDED:corpus]**
   `approach_summary`: "Models LLM generation as a horizon-H token-level MDP and proves that verifier-free trace distillation incurs Ω(H/√n) suboptimality under base-policy heterogeneity while a simple verifier-based algorithm achieves O(H/n) — i.e., verification enables strictly better asymptotic test-time-compute scaling, formalizing when the verifier lever is worth having at all."
   `paper_url`: https://openreview.net/forum?id=beeNgQEfe2
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "beeNgQEfe2", query: "test-time compute scaling; verifier"}`

3. `citation_key`: `"[PlanAndBudget, OpenReview:ctspw4CqbS]"` **[GROUNDED:corpus]**
   `approach_summary`: "PLAN-AND-BUDGET decomposes a query into sub-questions with a lightweight planner, estimates per-sub-question complexity weights, and allocates a fixed token budget across sub-questions via a Budget Allocation Model in which epistemic uncertainty decreases with tokens under a diminishing-return law — moving compute control from whole-response scaling to step-level budgeting to fix overthinking/underthinking miscalibration."
   `paper_url`: https://openreview.net/forum?id=ctspw4CqbS
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "ctspw4CqbS", query: "test-time scaling; budget"}`

4. `citation_key`: `"[CoTLength, OpenReview:6QDFsYxtI1]"` **[GROUNDED:corpus]**
   `approach_summary`: "Models CoT as sequential sub-question decomposition where each extra step both reduces per-step difficulty and adds error-accumulation risk, derives an inverted-U (non-monotonic) relationship between chain length and accuracy as a function of task difficulty and model capability, and validates it with controlled synthetic-length experiments plus length-aware inference strategies."
   `paper_url`: https://openreview.net/forum?id=6QDFsYxtI1
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "6QDFsYxtI1", query: "chain-of-thought length; overthinking"}`

5. `citation_key`: `"[AsymVerify, OpenReview:hxL4Uf9tR3]"` **[GROUNDED:corpus]**
   `approach_summary`: "For deep web-search agents, splits the test-time budget between exploration and verification: a ReAct-style search agent generates parallel candidate answers (with budget forcing), and an agentic verifier — the same scaffold re-prompted to check a given candidate with targeted web searches — scores candidates; because checking is cheaper than discovery (asymmetric verification), shifting budget to the verifier improves the accuracy-cost trade-off over search-only scaling."
   `paper_url`: https://openreview.net/forum?id=hxL4Uf9tR3
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "hxL4Uf9tR3", query: "test-time scaling; verification; allocation"}`

6. `citation_key`: `"[OTVerify, OpenReview:BBDhQJh6GB]"` **[GROUNDED:corpus]**
   `approach_summary`: "Casts verifier-guided test-time scaling as optimal transport from the generator distribution to a coverage-constrained reward-maximizing target policy under noisy verifier feedback, and decomposes achievable sub-optimality into an intrinsic transport cost plus terms determined by the verifier's ROC geometry — a unified account of how coverage, verifier accuracy, and algorithm design jointly bound sample-then-verify performance."
   `paper_url`: https://openreview.net/forum?id=BBDhQJh6GB
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "BBDhQJh6GB", query: "repeated sampling; coverage; verification"}`

7. `citation_key`: `"[BestOfMajority, OpenReview:a6CVQpjbXq]"` **[GROUNDED:corpus]**
   `approach_summary`: "Best-of-Majority: for the Pass@k objective, first filters N sampled responses by empirical frequency (restricting reward optimization to policy-supported regions where reward estimates are reliable), then returns the top-k survivors by reward score; proves minimax-optimal regret in coverage, reward-model error, and k, and scaling-monotonicity in N — fixing the non-monotonic failure of pure best-of-N under reward overoptimization."
   `paper_url`: https://openreview.net/forum?id=a6CVQpjbXq
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "a6CVQpjbXq", query: "best-of-n sampling; pass@k"}`

8. `citation_key`: `"[RerankingLaws, OpenReview:rhCgizNupi]"` **[GROUNDED:corpus]**
   `approach_summary`: "Models generator–reranker systems as parallel noisy channels with a decoder: LLM hypotheses are redundant transmissions, the imperfect reranker is a probabilistic decoder (Mallows / Zipf–Mandelbrot noise), and communication-theoretic analysis yields asymptotic 'reranking laws' — conditions for asymptotically error-free selection and error decay rates in the number of hypotheses, including under correlated (exchangeable) samples."
   `paper_url`: https://openreview.net/forum?id=rhCgizNupi
   `source`: `GROUNDED:corpus` · `location`: `{corpus: "ideas.jsonl", paper_id: "rhCgizNupi", query: "reranking; sampling; verifier"}`

9. `citation_key`: `"[BrownMonkeys, arXiv:2407.21787]"` **[NON-CORPUS — canonical; confident it exists (Brown et al., 2024, "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling"); cited pervasively as @brown2024monkeys / @brown2024languagemonkeys in the corpus papers above]**
   `approach_summary`: "Shows that coverage — the fraction of problems solved by at least one of N independent samples — scales predictably (approximately log-linearly) with N across tasks and models, establishing repeated sampling as a first-class inference-time scaling axis, while noting that in domains without automatic verifiers, common selection strategies (majority vote, reward ranking) plateau well below coverage."
   `paper_url`: https://arxiv.org/abs/2407.21787
   `source`: `HYPOTHESIS (non-corpus canonical)` · `location`: `null`

**Status:** `FOUND` (9 works, 8 grounded in the local corpus with full motivation/method text read; 1 canonical non-corpus anchor clearly marked). No absence_comment needed.

---

## N4 — Prior Limitations

`grounding_check`: `true` (every limitation cites at least one `N3.works[].citation_key`, exact string form; each limitation is defensible from the cited paper's own motivation text or from what its described method demonstrably does not cover).

`limitations` **[HYPOTHESIS — gap analysis by this digest's author against the grounded texts; no paper exists to assert these]**:

1. `limitation_text`: "Compute-optimal allocation work denominates the budget in FLOPs or generation counts within a single proposer–verifier abstraction and evaluates on a single task family (MATH-style reasoning); it optimizes which strategy to use per prompt, but never prices the verifier's own invocation cost in the same currency as generation, and never measures whether the resulting efficient frontier transfers across task families." `affects_works`: `["[SnellTTC, OpenReview:4FWAwZtd2n]"]` — defensible from its own motivation ("compare strategies but do not adapt them per prompt... reasoning datasets like MATH") and its method (allocation policy learned over MATH difficulty bins; no dollar/cost-meter component). `limitation_type`: `"generalizability"` `source`: `HYPOTHESIS` `location`: `{corpus: "ideas.jsonl", paper_id: "4FWAwZtd2n"}`
2. `limitation_text`: "Theoretical treatments of sampling-plus-verification treat verifier feedback as an available oracle-like resource and sample count N as abstract compute: suboptimality is bounded in horizon and sample count, transport cost in rejection rates, regret in coverage and reward-model error, and error decay in hypothesis count — but in none of these frameworks does the verifier's own metered cost enter the budget constraint, so they cannot answer what a marginal dollar buys when verification competes with generation for the same budget." `affects_works`: `["[VerifierFreeSuboptimal, OpenReview:beeNgQEfe2]", "[OTVerify, OpenReview:BBDhQJh6GB]", "[BestOfMajority, OpenReview:a6CVQpjbXq]", "[RerankingLaws, OpenReview:rhCgizNupi]"]` — defensible from what the four methods demonstrably cover (bounds in H, n, N, ROC, k; no cost model for the verifier itself). `limitation_type`: `"other"` (cost-model absence) `source`: `HYPOTHESIS` `location`: `{corpus: "ideas.jsonl", paper_ids: ["beeNgQEfe2","BBDhQJh6GB","a6CVQpjbXq","rhCgizNupi"]}`
3. `limitation_text`: "Step-level budget allocation distributes a fixed token budget across sub-questions within a single reasoning episode; it never trades tokens against additional independent samples or verifier calls, and its budget is denominated in tokens rather than dollars, so the inter-lever exchange rate is outside its scope." `affects_works`: `["[PlanAndBudget, OpenReview:ctspw4CqbS]"]` — defensible from its own method (planner + per-sub-question token allocation; no sampling or verification axis). `limitation_type`: `"generalizability"` `source`: `HYPOTHESIS` `location`: `{corpus: "ideas.jsonl", paper_id: "ctspw4CqbS"}`
4. `limitation_text`: "CoT-length analysis characterizes the inverted-U accuracy-vs-length curve for a single chain in isolation, holding the sampling and verification axes fixed; it establishes that the thinking lever has an interior optimum but provides no cost normalization against the other two levers, so it cannot say when a marginal thinking token is worth less than a marginal sample or verifier call." `affects_works`: `["[CoTLength, OpenReview:6QDFsYxtI1]"]` — defensible from its method (error-accumulation model and controlled length-only experiments). `limitation_type`: `"other"` (single-axis scope) `source`: `HYPOTHESIS` `location`: `{corpus: "ideas.jsonl", paper_id: "6QDFsYxtI1"}`
5. `limitation_text`: "The closest existing two-way allocation study splits budget between exploration and verification only in the deep web-search agent domain, with cost measured in trajectories/tool calls rather than a unified dollar unit, and with no CoT-length axis — a two-lever, single-family measurement that leaves the three-lever, cross-family exchange-rate question open." `affects_works`: `["[AsymVerify, OpenReview:hxL4Uf9tR3]"]` — defensible from its method (search-agent + agentic verifier on BrowseComp-style tasks; no thinking-length lever, no dollar meter). `limitation_type`: `"generalizability"` `source`: `HYPOTHESIS` `location`: `{corpus: "ideas.jsonl", paper_id: "hxL4Uf9tR3"}`
6. `limitation_text`: "Repeated-sampling scaling laws report coverage as a function of sample count, but coverage is not deliverable accuracy without a selector, and the selector's cost is unpriced; the coverage curve alone therefore overstates what the sampling lever buys at a fixed dollar budget." `affects_works`: `["[BrownMonkeys, arXiv:2407.21787]"]` — defensible from the finding (its own framing, echoed in corpus papers: selection strategies plateau in verifier-free domains) that coverage–accuracy gaps persist. `limitation_type`: `"other"` (metric–deployment mismatch) `source`: `HYPOTHESIS` `location`: `null`

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "These limitations are this digest author's gap analysis against real papers' texts, not limitations asserted by any paper's own authors — the hypothetical B4.2 paper does not exist to claim them.", "why_matters": "N4 normally carries only extracted author-claimed limitations; here every entry is inference-grade even though each is anchored to a real cited work.", "implication": "When the paper is written, verify each limitation against the cited work's full text (not just its corpus proposal summary) before asserting it in a real related-work section."}`

---

## N5 — Challenges

`conflation_check`: `true` (each challenge is a distinct, problem-inherent obstacle; none restates another and none is a prior-work failure — those live in N4).

`challenges` **[HYPOTHESIS, derived from the core question; N4-vs-N5 test applied: these hold for ANY attempt at the measurement, regardless of prior tools]**:

- `id: "C1"`, `text`: "Cost commensuration: the three levers are priced at different granularities and asymmetries — thinking tokens are output tokens (typically priced several times input tokens), extra samples multiply both prompt-input and output cost, and an LLM-based verifier consumes its own input tokens (the candidate) plus output tokens (the judgment) — so mapping (L, N, V) settings onto one fair dollar unit is itself a design problem any solution must solve before any comparison is meaningful."
- `id: "C2"`, `text`: "Lever interactions: the marginal value of each lever depends on the others' settings — a verifier is worthless at N=1 and increasingly valuable as candidate pools grow (but with diminishing returns as candidate correlation rises), and longer CoT changes both the per-sample accuracy and the length (hence cost) of what the verifier must read — so the 'exchange rate' between any two levers is inherently a function of the third, not a constant."
- `id: "C3"`, `text`: "Task-family heterogeneity in verifiability: domains differ in how cheaply and reliably candidate answers can be checked (executable tests for code, exact answers for math, rubric judgments for open QA), so lever values plausibly differ by family for problem-inherent reasons, and no single measured exchange rate can be assumed to transfer."
- `id: "C4"`, `text`: "Stochastic realized cost under a combinatorial grid: models cannot be forced to emit exactly L tokens, and per-query realized cost varies with output length, so grid points can only target — not fix — a total budget; matched-budget comparison therefore requires post-hoc cost binning or regression adjustment, on top of the combinatorial size of the (L, N, V) × budget-level × task-family grid."
- `id: "C5"`, `text`: "Cross-model and cross-pricing generalization: absolute exchange rates depend on a specific model's capability profile and a specific provider's price sheet (which changes over time), so any single-model, single-price measurement faces an inherent obstacle to generalizing beyond its pricing regime."

**Status:** `FOUND` (challenges are directly derivable from the seed's core question + minimal experiment). `source`: `HYPOTHESIS` throughout — flagged per V-08 as inference-level confidence, not extracted-level.

---

## N6 — Methodology

**`overview`** **[HYPOTHESIS]**: "Grid-scan a three-dimensional test-time budget allocation — thinking-token cap L, sample count N, verifier calls V — at matched total dollar cost per query, across task families spanning cheaply-verifiable (math, code) and hard-to-verify (open QA) domains, metering every generation and verifier token through a unified dollar cost meter. **Staged plan:** *Stage 1 (pilot = the seed's minimal experiment):* one open-weight reasoning model with controllable thinking budget, two task families (math + code), a coarse (4 L-levels × 5 N-levels × 3 V-modes) grid pruned to matched-cost bins at 3 budget levels, ~300 questions per family; deliverable = two per-family Pareto frontiers and a first exchange-rate estimate. *Stage 2 (scale-up):* four task families, a denser grid, 3 models spanning distinct price/capability points (small open-weight, large open-weight, one commercial API model), two verifiers of different strength, plus named allocation baselines run at the same budgets; deliverable = the cross-family stability test with confidence bands and a cross-model robustness check. At each grid point, measure accuracy and realized dollar cost; extract the non-dominated accuracy-per-dollar frontier per family; characterize frontier shape (dominant lever share along the frontier, elbow location, marginal rates of substitution); statistically compare shapes across families." `location: null` **[PLACEHOLDER — no paper exists]**.

**`key_components`** **[HYPOTHESIS — each operationalized: what is measured/built, with what instrument, at what granularity]**:

- `id: "M1"`, `name`: "Unified dollar cost meter", `text`: "A per-call accounting layer that logs input/output token counts from the inference engine's usage fields (vLLM logprobs/usage or API usage objects) and converts them to dollars via a price sheet frozen at experiment start (a single provider's published per-1M-token input/output rates; open-weight models priced at a stated GPU-hour-amortized equivalent). Verifier calls are metered identically: candidate tokens as input, judgment tokens as output. Granularity: one cost record per model call; per-query cost = sum over all generation and verifier calls. All results are additionally reported in provider-neutral normalized token units (output-token equivalents) for price-sheet robustness."
- `id: "M2"`, `name`: "Matched-cost 3D grid sampler", `text`: "Enumerates configurations L ∈ {512, 1024, 2048, 4096} thinking-token caps (enforced by budget forcing: truncating the thinking segment and forcing answer emission), N ∈ {1, 2, 4, 8, 16} samples at temperature 0.8, V ∈ {0 (majority vote), score-all-N with a cheap verifier, score-all-N with a strong verifier}; computes each configuration's expected dollar cost from pilot token statistics, and retains configurations falling in matched-cost bins (target budget ±10%) at each of 3–4 total budget levels. Realized (not nominal) cost is recorded per query for regression adjustment."
- `id: "M3"`, `name`: "Multi-family task suite", `text`: "Four families with per-family graders: math (MATH-500; AIME 2024+2025 for the hard tail) graded by exact-answer match; code (HumanEval+ and a LiveCodeBench slice) graded by test execution; graduate-level science MCQ (GPQA-Diamond) graded by option match; hard-to-verify open QA (FRAMES or SimpleQA subset) graded by an LLM rubric judge with a 200-item human audit. Pilot uses math + code (~300 questions each); Stage 2 uses all four (≥500 questions each where the benchmark allows)."
- `id: "M4"`, `name`: "Priced verifier/aggregator module", `text`: "Selection operator over the N candidates with three modes matching M2's V axis: (i) V=0: self-consistency majority vote (zero verifier dollars); (ii) cheap verifier: a small LLM judge prompted to score each candidate 0–100, best-of-N by score; (iii) strong verifier: a larger judge or process-reward-style scorer. Every verifier token is charged to the query's budget via M1. An oracle-verifier condition (ground-truth selection, cost counted as zero) is run once per grid point as a non-deployable upper bound to separate coverage from selection quality."
- `id: "M5"`, `name`: "Pareto frontier extraction & cross-family stability test", `text`: "Per family and budget level: compute the non-dominated set over (realized cost, accuracy); summarize frontier shape as (a) the allocation-mix vector (share of budget on thinking / sampling / verifying) at each frontier point, (b) elbow location via maximum-curvature estimate on a monotone spline fit, (c) pairwise marginal rates of substitution from local finite differences on the fitted surface. Stability across families is tested by permutation test on the distance between allocation-mix compositions at matched budget levels, with bootstrap (10,000 resamples over questions) confidence bands on each frontier."

**`challenge_arguments`** **[HYPOTHESIS — predicted arguments for how the design addresses the challenges, not reported author claims]**:

- `{challenge_id: "C1", argument_text: "The unified dollar cost meter (M1) prices all three levers in one currency at per-call granularity — including the verifier's own input and output tokens — and the dual reporting in normalized token units bounds sensitivity to any one price sheet, which is what makes a fair dollar-denominated grid possible at all.", mechanism_components: ["M1"]}`
- `{challenge_id: "C2", argument_text: "Scanning the full 3D grid (M2) rather than one lever at a time, with the verifier axis explicitly instantiated at multiple strengths and an oracle upper bound (M4), surfaces interaction structure — e.g., whether the verifier's marginal value grows with N and shrinks with L — instead of assuming additive effects.", mechanism_components: ["M2", "M4"]}`
- `{challenge_id: "C3", argument_text: "Running the identical grid over families spanning executable, exact-match, and rubric-graded verifiability (M3), and testing frontier-shape stability with an explicit permutation test (M5), is the mechanism that turns 'lever value differs by domain' from a plausibility claim into a measured verdict.", mechanism_components: ["M3", "M5"]}`
- `{challenge_id: "C4", argument_text: "The matched-cost-bin design with recorded realized cost (M2) plus regression adjustment on realized cost within bins (M5's fitting step) addresses the stochastic-cost problem: comparisons are cost-normalized by measurement, not by nominal settings, and bin pruning keeps the grid tractable.", mechanism_components: ["M2", "M1", "M5"]}`

**`unaddressed_challenges`**: `["C5"]` **[HYPOTHESIS]** — Stage 2's three-model sweep probes cross-model robustness, but generalization across pricing regimes and future price changes is inherently outside what any fixed-price-sheet measurement can establish; C5 is at best partially mitigated, so it is honestly listed as unaddressed.

**Feasibility [HYPOTHESIS]:**
- *Order of magnitude:* Pilot: ~2 families × 300 questions × ~35 matched-cost configurations, average ~8K generated tokens per (question, config) including verifier tokens ≈ 1.7×10⁸ tokens ≈ low hundreds of A100-hours on an open-weight 7–14B model with vLLM batching, or ≈ $300–800 if API-priced — "single-node, few-days" compute class. Stage 2: ~4 families × 500 questions × ~60 configs × 3 models ≈ 2×10⁹ tokens ≈ 1–2K GPU-hours plus an estimated $2–5K API spend for the commercial model — "small-cluster / modest-grant" class. Annotator effort: ~10–15 hours (200-item audit of the open-QA rubric judge, double-annotated).
- *Single biggest feasibility risk:* the thinking-length lever L cannot be precisely controlled on commercial API models (thinking budgets are coarse or hidden), which would break the grid's L axis exactly where pricing is most realistic. *Mitigation:* make open-weight reasoning models with s1-style budget forcing the primary instrument (full control of L, exact token accounting), and use the API model only for a coarse-grid robustness check on the (N, V) plane plus whatever discrete thinking levels its API exposes; report the API results as a partial replication, not a full grid.

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "No actual method exists; M1–M5, the staged plan, and the feasibility estimates are a forward design extrapolated from a one-sentence minimal experiment plus the grounded prior art.", "why_matters": "A reader should not mistake the named datasets, grid values, or cost estimates for committed choices — they are defaults chosen for defensibility, and the real implementation may substitute equivalents.", "implication": "Treat N6 as the pilot protocol to be finalized (and preregistered) before running Stage 1."}`

---

## N7 — Contributions

`contributions` **[HYPOTHESIS]**, framed from the method + expected findings — what such a paper would plausibly claim (novelty framing calibrated against the grounded N3/N4 landscape, which contains FLOPs-matched and two-lever precedents but no dollar-denominated three-lever measurement):

- `id: "CO1"`, `text`: "A cost-normalized measurement of accuracy-per-dollar exchange rates among CoT length, sample count, and verifier calls under matched total dollar budgets — extending FLOPs/token-matched allocation analyses to a setting where the verifier's own metered cost competes with generation inside the same budget constraint.", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id: "CO2"`, `text`: "An empirical accuracy-per-dollar Pareto frontier over the three-lever allocation space at multiple budget levels, with bootstrap confidence bands, characterizing which allocations are efficient at each budget.", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id: "CO3"`, `text`: "A quantified cross-task-family stability analysis showing whether the efficient frontier's shape is a universal property of test-time compute or is task-family-specific, tied to the family's verifiability class.", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id: "CO4"`, `text`: "A reusable, dollar-metered benchmarking harness (cost meter + matched-cost grid sampler + priced verifier module) for comparing test-time compute levers under a common budget.", `contribution_type`: `technical_artifact`, `is_testable`: `false`, `has_rq`: `false`.

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "These are forecasted contribution claims, not any author's own words.", "why_matters": "The 'no prior dollar-denominated three-lever measurement' framing rests on the corpus search in N3; a fuller literature search could still surface closer prior art (e.g., inference-economics measurements outside OpenReview).", "implication": "Re-verify the novelty framing against arXiv before submission; the grounded N4 limitations are the checklist for that comparison."}`

---

## N8 — Research Questions

`research_questions`:

- `id: "RQ1"` **[GIVEN — near-verbatim restatement of the seed's 核心问题]**: "Under a fixed dollar budget, what are the substitution (exchange) rates among lengthening chain-of-thought, multi-sampling, and invoking a verifier across different task families, and what does the resulting efficient (Pareto) frontier look like?" `rq_source`: `"explicit"`, `evaluates_mechanisms`: `["M1", "M2", "M3", "M4", "M5"]`, `addresses_challenges`: `["C1", "C2", "C4"]`, `tests_contributions`: `["CO1", "CO2"]`, `answered_by_experiment`: "Matched-cost 3D grid scan (M2) over (L, N, V) with the dollar meter (M1) on the pilot families, accuracy and realized cost per grid point, frontier extraction and MRS estimation (M5); baselines run at identical budgets for context." `location: null` **[PLACEHOLDER]**.
- `id: "RQ_INF_1"` **[HYPOTHESIS — inferred from the minimal experiment's explicit second clause "检验前沿形状跨任务族的稳定性"]**: "Is the shape of the accuracy-per-dollar Pareto frontier (dominant lever share, elbow location, marginal substitution rates) stable across task families, or does it vary systematically with the family's verifiability class?" `rq_source`: `"inferred"`, `evaluates_mechanisms`: `["M3", "M5"]`, `addresses_challenges`: `["C3"]`, `tests_contributions`: `["CO3"]`, `answered_by_experiment`: "Stage-2 run of the identical grid over all four families; permutation test on allocation-mix composition distance at matched budget levels, bootstrap frontier bands." `location: null` **[PLACEHOLDER]**.
- `id: "RQ_INF_2"` **[HYPOTHESIS — inferred from C2, which the grid design must confirm or refute]**: "Is the marginal value of a verifier dollar an increasing function of sample count N and a decreasing function of candidate length L — i.e., are the levers' exchange rates non-constant interaction terms rather than fixed coefficients?" `rq_source`: `"inferred"`, `evaluates_mechanisms`: `["M2", "M4"]`, `addresses_challenges`: `["C2"]`, `tests_contributions`: `["CO1"]`, `answered_by_experiment`: "Within-grid interaction analysis: fit accuracy ~ f(L, N, V-mode, realized cost) with explicit N×V and L×V interaction terms; compare cheap-verifier, strong-verifier, majority-vote, and oracle-verifier conditions at fixed (L, N)." `location: null` **[PLACEHOLDER]**.

`datasets` **[HYPOTHESIS — real, named benchmarks chosen to span verifiability classes; final slice sizes to be fixed at preregistration]**: `{names: ["MATH-500 (math, exact-match)", "AIME 2024 + AIME 2025 (math, hard tail)", "HumanEval+ (code, test execution)", "LiveCodeBench (code, contamination-controlled slice)", "GPQA-Diamond (graduate science MCQ)", "FRAMES (hard-to-verify open QA; SimpleQA subset as alternate)"], source: HYPOTHESIS, location: null}`.

`baselines` **[HYPOTHESIS — named allocation policies, drawn from N3, all run at the same matched budgets]**: `{names: ["Single-sample short-CoT floor (L=512, N=1, V=0)", "Long-CoT-only budget forcing (all budget into L; per [CoTLength, OpenReview:6QDFsYxtI1] and s1-style forcing as used in [AsymVerify, OpenReview:hxL4Uf9tR3])", "Self-consistency majority vote (all budget into N, V=0)", "Best-of-N with verifier (fixed L, budget split N vs. verifier per [BrownMonkeys, arXiv:2407.21787] + [OTVerify, OpenReview:BBDhQJh6GB] framing)", "Best-of-Majority selector at matched cost (frequency-filter then rank, per [BestOfMajority, OpenReview:a6CVQpjbXq])", "Difficulty-conditioned compute-optimal allocation (per-prompt strategy choice, per [SnellTTC, OpenReview:4FWAwZtd2n], re-priced in dollars)"], source: HYPOTHESIS, location: null}`.

`metrics` **[HYPOTHESIS — each with definition]**: `{names: ["Accuracy: per-family success rate (exact match for math/MCQ, pass@1-after-selection for code, audited rubric score ≥ threshold for open QA)", "Realized dollar cost per query: M1-metered sum over all generation + verifier calls", "Accuracy-per-dollar: accuracy divided by mean realized cost within a matched-cost bin", "Pareto frontier hypervolume: dominated-area above the cost-accuracy floor, per family and budget", "Marginal rate of substitution (MRS): ratio of partial accuracy gains per marginal dollar on lever i vs. lever j, from local finite differences on the fitted surface", "Frontier-shape stability statistic: permutation-test distance between allocation-mix compositions across families at matched budgets"], source: HYPOTHESIS, location: null}`.

`analysis_plan` **[HYPOTHESIS]**: Sample size: ≥300 questions/family (pilot), ≥500 (Stage 2), chosen so a 5-percentage-point accuracy difference between two frontier candidates is detectable at power 0.8 given binomial variance at accuracy ≈ 0.6. Statistical tests: paired bootstrap (10,000 resamples over questions) for frontier confidence bands and per-pair accuracy contrasts; permutation test (10,000 permutations of family labels) for RQ_INF_1's frontier-shape comparison; likelihood-ratio test on the N×V and L×V interaction terms for RQ_INF_2. Significance threshold: α = 0.05 with Holm–Bonferroni correction across family pairs and across budget levels. Expected effect directions: verify-heavy allocations dominate the frontier on math/code, think-heavy allocations on open QA, and the N×V interaction coefficient is positive (see N9).

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "RQ1 is given by the seed; RQ_INF_1/RQ_INF_2, all dataset/baseline/metric choices, and the analysis plan are inferred design commitments, not confirmed by any paper text.", "why_matters": "The task suite and baseline set materially determine the exchange-rate numbers; a different verifier or price sheet changes the frontier.", "implication": "Freeze this node as a preregistration before Stage 1; deviations in the real experiment must be logged as protocol amendments."}`

---

## N9 — Results

**CRITICAL — no paper exists, so no numbers are reported.** Each item is a **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**: a falsifiable predicted direction with `evidence_strength: "missing"`, `rq_answered: false`, and an explicit falsification condition. Nothing here may be cited as a finding.

- `rq_id: "RQ1"`, `result_text`: "PREDICTED DIRECTION (not observed): exchange rates among the three levers are budget-dependent — at low budgets the efficient frontier is dominated by thinking-only or small-N allocations (verifier overhead unaffordable), while at moderate-to-high budgets sample-then-verify allocations dominate on verifiable families; the thinking lever shows an interior optimum (inverted-U) along the frontier rather than monotone gains.", `result_type`: `quantitative` (hypothesized), `evidence_strength`: `"missing"`, `rq_answered`: `false`.
  **Falsification condition:** "Refuted if the measured MRS between every lever pair is constant within bootstrap confidence bands across budget levels — i.e., if a single fixed exchange rate prices all three levers everywhere — or if thinking-lever gains are monotone with no interior optimum at any tested budget."

- `rq_id: "RQ_INF_1"`, `result_text`: "PREDICTED DIRECTION (not observed): frontier shape is task-family-specific and ordered by verifiability — code (executable checks) shows the most verify-heavy efficient mix, math intermediate, rubric-graded open QA the most think-heavy — so the permutation test rejects cross-family shape equality.", `result_type`: `quantitative` (hypothesized), `evidence_strength`: `"missing"`, `rq_answered`: `false`.
  **Falsification condition:** "Refuted if allocation-mix compositions at matched budgets are statistically indistinguishable across families (permutation test fails to reject at α=0.05 with Holm correction), or if the observed family ordering contradicts the verifiability ordering (e.g., open QA is the most verify-heavy)."

- `rq_id: "RQ_INF_2"`, `result_text`: "PREDICTED DIRECTION (not observed): the levers interact — the marginal accuracy per verifier dollar increases with N (more candidates to discriminate) with diminishing returns as candidate correlation grows, and decreases with L (longer candidates cost more to read per unit of selection benefit); the N×V interaction term is positive and significant, the L×V term negative.", `result_type`: `quantitative` (hypothesized), `evidence_strength`: `"missing"`, `rq_answered`: `false`.
  **Falsification condition:** "Refuted if the likelihood-ratio test finds no significant N×V or L×V interaction (additive model suffices), or if the signs are opposite to prediction (e.g., verifier value flat or decreasing in N)."

**Status:** `NOT_FOUND` (by design — no experiment has been run). `absence_comment`: `{"what_missing": "No accuracy, cost, frontier, or interaction data exists because the experiment has not been run.", "why_matters": "RQ1, RQ_INF_1, and RQ_INF_2 remain open predictions; citing any of the above directions as evidence would be fabrication.", "implication": "Run Stage 1 to populate RQ1's pilot cells first; the falsification conditions above are the pass/fail gates for continuing to Stage 2."}`

---

## N10 — Threats / Self-Limitations

`threats` **[HYPOTHESIS — anticipated threats a reviewer would raise; no real authors exist to have acknowledged these]**:

- `threat_id: "t1"`, `category`: `construct`, `description`: "The dollar meter operationalizes 'cost' as list-price tokens, but production cost includes batching, caching, latency SLAs, and amortized fixed costs; a list-price frontier may not be the frontier a deployer actually faces, and open-weight 'GPU-hour-equivalent' pricing is itself a modeling choice.", `mitigation`: "Report all results in provider-neutral normalized token units alongside dollars (M1's dual reporting) and run a sensitivity analysis re-computing frontiers under ±3× perturbations of the input/output and verifier/generator price ratios; conclusions that survive the perturbation band are flagged as price-robust."
- `threat_id: "t2"`, `category`: `internal`, `description`: "Verifier quality confounds the verifying axis: a weak verifier makes verify-heavy allocations look bad (and vice versa), so a single verifier's ROC could masquerade as a property of the lever itself; likewise sample diversity confounds the sampling axis.", `mitigation`: "Instantiate the V axis at two verifier strengths plus a zero-cost majority-vote floor and a ground-truth oracle upper bound (M4), so each frontier is reported as a band between realizable and oracle selection rather than a single verifier's curve."
- `threat_id: "t3"`, `category`: `conclusion`, `description`: "Stochastic realized cost forces binning and surface-fitting choices (bin width, spline smoothing, interaction terms), and the large grid invites multiple-comparison false positives when hunting for frontier differences.", `mitigation`: "Preregister the analysis plan (bin width ±10%, test statistics, α=0.05 with Holm–Bonferroni across family pairs and budget levels), use paired bootstrap confidence bands, and regression-adjust on realized cost within bins."
- `threat_id: "t4"`, `category`: `external`, `description`: "Findings from a small set of models and one frozen price sheet may not generalize to other model families, capability tiers, or future pricing regimes; absolute exchange-rate numbers are pricing-regime artifacts even if the qualitative frontier shape transfers (this is challenge C5).", `mitigation`: "Stage 2 replicates across three models spanning distinct price/capability points and reports frontier *shape* (dominant-lever ordering, elbow, MRS signs) as the primary claim, with absolute dollar rates explicitly demoted to a dated, price-sheet-specific appendix."
- `threat_id: "t5"`, `category`: `construct`, `description`: "The open-QA family's accuracy is graded by an LLM rubric judge, so the 'accuracy' construct on the hardest-to-verify family is itself produced by a verifier-like instrument — risking circularity with the verifying lever under study.", `mitigation`: "Use a grading judge that is a different model from the in-budget verifier, audit 200 judged items with two human annotators (target agreement κ ≥ 0.7), and exclude the open-QA family from any claim that does not survive the audit."

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "These are reviewer-anticipated threats with planned mitigations, not limitations any real author has acknowledged, since no paper exists.", "why_matters": "N10 is supposed to capture only author-acknowledged limitations; here it necessarily forecasts them.", "implication": "Replace with the actual Limitations/Threats section once written; the mitigations above should be built into the protocol rather than promised post hoc."}`

---

## N11 — Artifacts

`artifacts`: `[]`. `has_code`: `false`, `has_data`: `false`, `has_model`: `false`. **[PLACEHOLDER]** — nothing has been released because the paper does not exist yet.

**Status:** `NOT_FOUND`. `absence_comment`: `{"what_missing": "No code, data, or model artifacts exist because no experiment has been run and no paper has been written.", "why_matters": "This is itself reviewer-relevant signal (there is nothing to inspect or reproduce yet), not a gap to paper over.", "implication": "Populate this node once the dollar-metered harness (M1–M5), the matched-cost grid logs, and the per-query cost records are implemented and released — the cost logs are the artifact reviewers will most need to audit CO1."}`

---

## N12 — Contribution Type

`value`: `"empirical"` **[HYPOTHESIS]**

`rationale`: "What N9's (hypothesized) results are designed to validate is a measured phenomenon — the shape and cross-family stability of the accuracy-per-dollar frontier over three existing test-time levers — obtained by running existing models, existing benchmarks (MATH-500, HumanEval+, GPQA-Diamond, FRAMES), and existing selection methods ([SnellTTC], [BestOfMajority]-style baselines) under a new cost-normalized protocol. The harness (CO4) exists to support the measurement, matching the 'measurement study with a released artifact → empirical if the study is the main contribution' rule; no new dataset, benchmark-as-product, system, or theorem is the primary claim, so `empirical` fits over `benchmark`, `tool`, `system`, or `theoretical`." `source`: `HYPOTHESIS`.

**Status:** `PARTIAL`. `absence_comment`: `{"what_missing": "No real paper exists to assert its own contribution-type classification; N12 is this digest's inference from N6/N7/N9, not an author's stated self-classification.", "why_matters": "Phase A's digest self-verification checklist (goal.md §3 item 1) requires every non-GIVEN node to carry a 3-part absence comment; N12 previously omitted this line even though its value is tagged [HYPOTHESIS], breaking the convention every other node (N0–N11) follows.", "implication": "Treat `empirical` as this digest's best-supported classification, re-derive it from the real paper's actual contribution once written rather than assuming it carries forward unchanged."}` — added on Phase A re-run (2026-07-04); see `discussion/stage_review.md`.

---

## Claims

The most reviewer-relevant assertions, each tagged by trust level:

1. **[GROUNDED:corpus]** "The grounded prior-art landscape contains FLOPs/token-matched allocation studies ([SnellTTC, OpenReview:4FWAwZtd2n], [PlanAndBudget, OpenReview:ctspw4CqbS]), single-axis analyses ([CoTLength, OpenReview:6QDFsYxtI1], [BrownMonkeys, arXiv:2407.21787]), cost-free theory of sample-then-verify ([VerifierFreeSuboptimal], [OTVerify], [BestOfMajority], [RerankingLaws]), and one two-lever domain-specific allocation study ([AsymVerify, OpenReview:hxL4Uf9tR3]) — but no dollar-denominated three-lever exchange-rate measurement in which the verifier's own cost sits inside the budget constraint. That specific gap is what B4.2 targets." — `evidence: [{type: "citation", text: "N3 corpus search (5 queries, 2026-07-04) + N4 limitation analysis", source: GROUNDED:corpus, location: {corpus: "ideas.jsonl"}}]`.
2. **[HYPOTHESIS]** "Exchange rates among CoT-length, sampling, and verifying are not constants: they vary with the budget level, with each other (N×V and L×V interactions), and with task-family verifiability." — `evidence: [{type: "argument", text: "derived from C2/C3 and the interaction structure that motivates RQ_INF_2; consistent with (but not established by) the asymmetric-verification observation in [AsymVerify]", source: HYPOTHESIS, location: null}]`.
3. **[HYPOTHESIS]** "Frontier shape is expected to be task-family-specific and ordered by verifiability (code most verify-heavy, open QA most think-heavy); a universal frontier would falsify this and would itself be a publishable negative result under the same protocol." — `evidence: [{type: "argument", text: "derived from C3/RQ_INF_1 and the falsification conditions in N9", source: HYPOTHESIS, location: null}]`.
4. **[PLACEHOLDER]** "No quantitative exchange-rate or frontier numbers exist yet — any specific figure (e.g., '1 verifier call buys as much accuracy as 2,000 thinking tokens') would be fabricated if reported now." — `evidence: [{type: "observation", text: "N9 is deliberately NOT_FOUND; no experiment has run", source: PLACEHOLDER, location: null}]`.
5. **[GIVEN]** "The intended minimal experiment is a grid scan of the 3D budget allocation, plotting an accuracy-per-dollar Pareto frontier, and checking the frontier shape's stability across task families." — `evidence: [{type: "citation", text: "verbatim from seed README 最小实验 field", source: GIVEN, location: {file: "topics/B4.2_exchange_rates_between_thinking_sampling_and_verifying_under_a_f/README.md", section: "最小实验"}}]`.

---

## Self-verification pass (per self-verification.md)

- **V-01 (locators):** All `GROUNDED:corpus` items carry a corpus locator (`paper_id` + query); all HYPOTHESIS/PLACEHOLDER content carries `location: null` honestly. The one non-corpus N3 entry ([BrownMonkeys, arXiv:2407.21787]) is explicitly flagged as canonical-but-unverified-in-corpus.
- **V-02 (absence comments):** Every node with `status != FOUND` (N0, N1, N2, N4, N6, N7, N8, N9, N10, N11) has a full 3-part `absence_comment`. N3 and N5 are FOUND with `absence_comment=null` implied.
- **V-04 / EX-09 (ID consistency):**
  - `N4.limitations[].affects_works` ⊂ N3 citation_keys, verbatim: `[SnellTTC, OpenReview:4FWAwZtd2n]`, `[VerifierFreeSuboptimal, OpenReview:beeNgQEfe2]`, `[OTVerify, OpenReview:BBDhQJh6GB]`, `[BestOfMajority, OpenReview:a6CVQpjbXq]`, `[RerankingLaws, OpenReview:rhCgizNupi]`, `[PlanAndBudget, OpenReview:ctspw4CqbS]`, `[CoTLength, OpenReview:6QDFsYxtI1]`, `[AsymVerify, OpenReview:hxL4Uf9tR3]`, `[BrownMonkeys, arXiv:2407.21787]` — all nine appear verbatim in N3. ✓
  - `N6.challenge_arguments[].challenge_id` ∈ {C1, C2, C3, C4} ⊂ N5 {C1..C5}. ✓
  - `N6.challenge_arguments[].mechanism_components` ⊂ {M1..M5} = N6 key_component ids. ✓
  - `N6.unaddressed_challenges = ["C5"]` ⊂ N5 ids. ✓
  - N8 RQs: `addresses_challenges` ∈ {C1,C2,C3,C4}; `tests_contributions` ∈ {CO1,CO2,CO3}; `evaluates_mechanisms` ∈ {M1..M5} — all resolve. ✓
  - `N9.results[].rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2} = N8 ids exactly. ✓
- **V-08 (confidence under inference):** N6/N8/N9 are explicitly flagged as resting on HYPOTHESIS-level design commitments; predicted directions are never presented as findings.
- **V-10/V-11:** N10 threats are categorized (construct×2, internal, conclusion, external) each with a mitigation; N11 flags all false, consistent with an empty artifacts list.
- **V-12:** N12 rationale cites concrete content (named datasets, named baselines, what N9 validates) rather than circular phrasing.
- **Empty-node check (EX-11):** All of N0–N12 plus Claims appear above, none omitted.
