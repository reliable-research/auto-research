# Digest: Pinning at Scale: Token Overhead versus Violation Trade-offs under Hundreds of Constraints

> **REVERSE-DIGEST NOTICE.** No paper exists for this topic yet. This is speculative
> scaffolding for research planning, produced from a one-paragraph seed idea
> (`topics/T3.4_.../README.md`), as if a paper answering the idea had already been written.
> Every field below is tagged **[GIVEN]** (verbatim/near-verbatim from the seed),
> **[HYPOTHESIS]** (reasoned elaboration / prediction, not fact), **[GROUNDED:corpus]**
> (a real paper from the local OpenReview corpus `topics/corpus/ideas.jsonl`, with its
> actual motivation/method text as evidence), or **[PLACEHOLDER]** (genuinely unknowable
> until the work is done — never invented). Treat HYPOTHESIS content as falsifiable
> forecasts, not findings.

---

## N0 — Metadata

- **title** [GIVEN]: "Pinning at Scale: Token Overhead versus Violation Trade-offs under Hundreds of Constraints"
  — location: seed README, line under label `T3.4 规模化 pinning 的开销边界`.
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper exists, no author list can be known.
  - absence_comment: {what_missing: "No authors have been assigned because the paper has not been written.", why_matters: "Attribution cannot be verified or credited in any downstream indexing.", implication: "Treat authorship as entirely unresolved; do not cite a person or lab for this work."}
- **abstract** [HYPOTHESIS] (drafted, not real — synthesized from the core question + minimal experiment):
  > "LLM-based agents are increasingly deployed with hundreds of standing constraints — safety
  > rules, user preferences, business policies — that must be respected across a task. The
  > default engineering practice is *pinning*: repeating the full constraint set verbatim in
  > every context window so the model cannot 'forget' it. We ask when this practice stops
  > paying for itself. Sweeping constraint-set size from single digits to several hundred, we
  > jointly measure constraint-violation rate, token overhead, and downstream task success
  > rate under full pinning versus a family of selective-pinning policies that retrieve only a
  > bounded, task-relevant subset of constraints per step. We characterize the point at which
  > full pinning's token overhead begins to actively erode task success (rather than merely
  > being wasteful), and propose a selection criterion for which constraints to keep resident
  > in context under a fixed budget."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` — LLM agent context/memory management; the
  measurement-of-model-behavior framing fits AI/ML best (could also file under Systems).

**Status:** PARTIAL (title/core-question given; authors/abstract are placeholder/hypothesis, not FOUND in the schema sense since no source document exists).

---

## N1 — Problem Formulation

- **objective** [HYPOTHESIS] (full predicate, built directly from the seed's core question):
  > "measure, via constraint-count sweeps from single digits to hundreds, when the token
  > overhead of exhaustively pinning all constraints in an LLM agent's context begins to
  > degrade downstream task success rate — and to design/evaluate a selective-pinning
  > strategy that decides which bounded subset of constraints to keep resident in context at
  > each step."
  - Self-check: kind of task = empirical measurement + selection-policy design; domain = LLM
    agents under standing memory constraints; outcome shape = a three-axis trade-off
    characterization (violation rate × token overhead × task success) plus a selection
    policy. All three land.
- **inputs** [HYPOTHESIS], inferred from the minimal experiment:
  - a parametrized pool of standing constraints, sampled to size *n* (n swept from single digits to hundreds), each paired with a verification procedure (programmatic checker or LLM judge)
  - an agent task suite whose episodes can be checked, per turn, against the applicable constraints
  - a context/token budget per turn
  - a pinning policy (full / none / selective-k) to be evaluated
- **outputs** [HYPOTHESIS]:
  - violation rate as a function of n and pinning policy
  - token overhead (constraint tokens per turn, absolute and as fraction of prompt) as a function of n and policy
  - task success rate as a function of n and policy
  - a selective-pinning selection/scoring policy and its measured position on the trade-off surface
- **constraints** [GIVEN + HYPOTHESIS extension, marked]:
  - [GIVEN] "约束数量从个位数增长到数百条" — the constraint count scales from single digits
    up to hundreds (seed README, 核心问题).
  - [HYPOTHESIS] each task execution admits a checkable ground truth for whether a specific
    constraint was violated (violations are separable and attributable per-constraint) —
    assumed as a precondition for a "violation rate" metric to be computable at all; this is
    exactly the dual-mode verifiability design that [RECAST, OpenReview:90tCp2KszA]
    demonstrates is constructible at scale (rule-based checkers + LLM validators).

**Status:** PARTIAL — objective/inputs/outputs are HYPOTHESIS extrapolations from one sentence; only the constraint-count-scaling fact is GIVEN verbatim.

---

## N2 — Motivation

**motivations** (MotivationItem list) — reconstructed from the seed's `parent_topic` framing
("T3. Memory 约束保持（窄环，4条）") and now grounded against real corpus findings:

1. **motivation_text** [HYPOTHESIS, grounded]: "Production LLM agents are increasingly asked
   to honor large, standing constraint sets (safety rules, user preferences, org policy)
   across long-horizon tasks; the default engineering fix — pinning, i.e. repeating every
   constraint verbatim in every context window — is the obvious way to guarantee the model
   'sees' each rule, but nothing guarantees it scales gracefully as the rule count grows from
   a handful to enterprise-scale hundreds." evidence: [{type: "citation", text: "RECAST's own
   motivation: 'existing models struggle to simultaneously satisfy multiple constraints as
   instruction complexity grows … even advanced models experience substantial performance
   degradation when multiple requirements are present'", source: "GROUNDED:corpus", location:
   "[RECAST, OpenReview:90tCp2KszA] motivation"}].
2. **motivation_text** [HYPOTHESIS, grounded]: "If full pinning's token cost eventually
   competes with the tokens available for actually solving the task, the 'safe' choice (pin
   everything) can silently become the choice that most hurts task success. This is not
   hypothetical attention folklore: long-horizon agent work reports that append-only context
   'produces context saturation rather than merely long context length' where the few facts
   that matter are mixed with noise." evidence: [{type: "citation", text: "AgentFold
   motivation on context saturation in append-only agents", source: "GROUNDED:corpus",
   location: "[AgentFold, OpenReview:IuZoTgsUws] motivation"}].
3. **motivation_text** [HYPOTHESIS, grounded]: "The cost side of the trade-off has a mature
   toolbox (query-aware context compression under a fixed token budget), but that toolbox has
   been validated for *evidence* selection (QA/summarization), never for *normative rule*
   selection where dropping the wrong rule causes a violation rather than a wrong answer —
   so the trade-off for constraints must be measured, not assumed." evidence: [{type:
   "citation", text: "COMI frames compression as 'a constrained information selection problem:
   under a fixed token budget, the model must retain the evidence most useful for answering
   the current query'", source: "GROUNDED:corpus", location: "[COMI, OpenReview:OGDIXDfaN4]
   motivation"}].

---

## N3 — Related Works

**Provenance:** real papers retrieved from the local OpenReview corpus
(`topics/corpus/ideas.jsonl`, 11,683 papers) via keyword search from four angles —
(a) multi-constraint instruction following, (b) prompt/context compression under token
budget, (c) agent context management / long-horizon memory, (d) long-context degradation and
constraint retention over dialogue. Each `approach_summary` is grounded in the paper's own
motivation/method text. One non-corpus canonical entry is retained and clearly marked.

**works:**

| citation_key | approach_summary | paper_url | source |
|---|---|---|---|
| **[RECAST, OpenReview:90tCp2KszA]** | Builds a scalable pipeline that mines verifiable constraints from instruction–response corpora, splits them into rule-based (programmatically checkable: word counts, keywords, structure) and model-based (LLM-validated: tone, style) categories, recombines them into high-complexity multi-constraint instructions, and trains with constraint-level verification rewards (RLVC). Motivated by FollowBench-style findings that models degrade substantially as the number of simultaneous requirements grows. | https://openreview.net/forum?id=90tCp2KszA | GROUNDED:corpus |
| **[PrefEval, OpenReview:QWunLKbBGF]** | Benchmark testing whether LLMs infer, remember, and proactively follow user preferences across long multi-session conversations: manually curated preference–query pairs (explicit and implicit forms) are interleaved with long unrelated conversational spans sampled from LMSYS-Chat-1M, and behavioral compliance is measured via LLM judges plus a correlated classification proxy, with capability-oriented error categories (inference / retrieval / following / proactiveness). | https://openreview.net/forum?id=QWunLKbBGF | GROUNDED:corpus |
| **[ICF-Bench, OpenReview:hcJywRYc3n]** | Benchmark for *in-context forgetting*: paired NoForget/Forget dialogue instances isolate whether a model can suppress revoked, revised, or superseded context (instructional forgetting, subtask revision, dynamic preference change), measured by SFRR — the proportion of examples correct without interference that remain correct under it. Frames forgetting as an inference-time context-management problem. | https://openreview.net/forum?id=hcJywRYc3n | GROUNDED:corpus |
| **[Sculptor, OpenReview:HPeiH7da0Z]** | Equips an LLM agent with active context-management tools — fragmenting history into addressable spans, reversibly compressing/hiding/restoring fragments, and exact in-context search — so reasoning happens over a curated, low-interference workspace. Motivated by evidence that long-context failure is interference inside the working context (attention dilution by distracting tokens), not just window size. | https://openreview.net/forum?id=HPeiH7da0Z | GROUNDED:corpus |
| **[AgentFold, OpenReview:IuZoTgsUws]** | Long-horizon web-agent architecture that inserts a learned *folding* decision into the ReAct loop: the agent maintains multi-scale summaries of older sub-trajectories plus a full-fidelity latest step, and at each step jointly predicts a folding directive (granular condensation vs deep consolidation) and the next action — a selective, temporally informed compression policy replacing append-only context. | https://openreview.net/forum?id=IuZoTgsUws | GROUNDED:corpus |
| **[COMI, OpenReview:OGDIXDfaN4]** | Coarse-to-fine context compression that scores units by Marginal Information Gain — query relevance *minus* maximum similarity to already-kept units — applied hierarchically to allocate token budget across segments and fuse tokens into soft representations, explicitly correcting relevance-only selection that wastes budget on redundant evidence under aggressive compression. | https://openreview.net/forum?id=OGDIXDfaN4 | GROUNDED:corpus |
| **[CogniLoad, OpenReview:0Sex2H5Jnn]** | Synthetic reasoning benchmark whose difficulty is defined by three *independently tunable* parameters — intrinsic reasoning complexity, distractor density (needle-to-hay ratio of state-update statements), and sequence length — enabling factorial experiments that attribute degradation to a specific load dimension instead of conflating them. | https://openreview.net/forum?id=0Sex2H5Jnn | GROUNDED:corpus |
| **[LostInTheMiddle, arXiv:2307.03172]** | (Non-corpus, canonical — Liu et al., TACL 2024; cited as the standard positional-degradation result by multiple corpus papers above, e.g. Sculptor and PrefEval.) Shows LLM performance on multi-document QA and key-value retrieval degrades sharply when relevant information sits in the middle of a long context, establishing that mere presence of information in context does not guarantee its use. | https://arxiv.org/abs/2307.03172 | HYPOTHESIS (canonical, non-corpus) |

**Status:** FOUND (as reverse-digest scaffolding: 8 real papers, 7 corpus-grounded).

---

## N4 — Prior Limitations

**grounding_check:** true (every limitation cites `affects_works` keys that appear verbatim
as N3 citation_keys). Each limitation is defensible from the cited paper's own motivation
text or from what its method demonstrably does not cover; all framing-as-limitation is
[HYPOTHESIS] (these authors did not write a limitations section against *this* topic).

1. **limitation_text**: "Multi-constraint instruction-following work improves *satisfaction*
   of many constraints packed into a single instruction (via training data and verification
   rewards), but treats the constraint set as free to represent: it neither measures the token
   cost of carrying n constraints in context across a multi-turn agent trajectory, nor sweeps
   n as an in-context resource variable into the hundreds to find where representation cost
   harms the task itself." — affects_works: `["[RECAST, OpenReview:90tCp2KszA]"]`,
   limitation_type: `scalability`.
2. **limitation_text**: "Constraint-retention benchmarks measure whether a *small* number of
   standing items (one preference per query pair in PrefEval; one revoked/updated item per
   instance in ICF-Bench) survive long distractor-filled contexts; they never scale the count
   of *simultaneously active* constraints, and they report compliance only — the token
   overhead and task-success cost of any mitigation (such as re-injecting the items every
   turn) is outside their measurement design." — affects_works:
   `["[PrefEval, OpenReview:QWunLKbBGF]", "[ICF-Bench, OpenReview:hcJywRYc3n]"]`,
   limitation_type: `scalability`.
3. **limitation_text**: "Agent context-management systems curate the *task history* (folding
   sub-trajectories, hiding/restoring fragments) while treating the standing
   instruction/policy block as fixed and untouched; they optimize what enters the workspace
   from past interactions, not which of hundreds of standing rules deserve residence, and
   they do not report constraint-violation rate as an outcome at all." — affects_works:
   `["[Sculptor, OpenReview:HPeiH7da0Z]", "[AgentFold, OpenReview:IuZoTgsUws]"]`,
   limitation_type: `generalizability`.
4. **limitation_text**: "Budget-constrained context compression selects *evidence* whose value
   is informational (does it help answer the query?), validated on QA/summarization; it is
   unvalidated for *normative* content where the cost of dropping a unit is a rule violation,
   where 'relevance' means applicability of a rule to the current action rather than semantic
   similarity to a query, and where compressing a rule's wording may destroy its
   enforceability." — affects_works: `["[COMI, OpenReview:OGDIXDfaN4]"]`, limitation_type:
   `generalizability`.
5. **limitation_text**: "Controlled load-sweep benchmarks tune distractor density and length
   for *factual/reasoning* material and measure answer accuracy only; no analogous controlled
   sweep exists where the manipulated variable is the number of pinned normative constraints
   and the outcomes are the joint violation-rate/token-overhead/task-success surface." —
   affects_works: `["[CogniLoad, OpenReview:0Sex2H5Jnn]"]`, limitation_type: `other`.
6. **limitation_text**: "Positional-degradation results establish that in-context information
   can go unused, but for single retrieval targets (documents, key-value pairs) — they do not
   quantify how compliance degrades as the number of simultaneously binding items grows, nor
   the overhead side of keeping them all resident." — affects_works:
   `["[LostInTheMiddle, arXiv:2307.03172]"]`, limitation_type: `generalizability`.

---

## N5 — Challenges

**conflation_check:** true (each challenge below is problem-inherent and distinct; none is a
restatement of a prior tool's failure — N4-vs-N5 test applied). Stable ids C1–C4 retained
from the previous digest revision; C5 added (measurement is part of the problem, not of any
prior tool).

- **C1** [HYPOTHESIS, tightly derived from the core question]: "Per-turn token budget is
  finite while the standing constraint count is, in principle, unbounded; past some n,
  pinning all constraints verbatim either overflows the budget or crowds out the tokens
  needed for task content (observations, tool outputs, reasoning)."
- **C2** [HYPOTHESIS, grounded]: "Instruction-following fidelity degrades under long,
  redundant, high-distractor-load prompts — interference inside the working context dilutes
  attention over any single rule (the mechanism Sculptor's and LostInTheMiddle's evidence
  points to) — so pinning *more* constraints can itself reduce fidelity to each one. This is
  a property of how transformer context is processed, not a fixable bug of one system."
- **C3** [HYPOTHESIS]: "Which constraints are *applicable* at a given step is task- and
  state-dependent and cannot be computed once, statically: applicability is a normative
  matching problem ('does rule r bind action a in state s?'), not a semantic-similarity
  problem, and it must be re-decided as the task unfolds."
- **C4** [HYPOTHESIS]: "There is no single scalar ground truth for the 'right' point on the
  violation-rate / token-overhead / task-success surface — it is an inherently
  multi-objective Pareto frontier whose acceptable operating point shifts with constraint
  semantics (a safety rule and a formatting preference do not price violations equally)."
- **C5** [HYPOTHESIS]: "Measuring violations at scale is itself problem-inherent: with
  hundreds of constraints × multi-turn episodes, exhaustive human checking is infeasible,
  yet any automatic detector's error is confounded with the quantity being measured — a
  violation-rate curve is only as trustworthy as the detector that produced it."

---

## N6 — Methodology

**overview** [HYPOTHESIS]: Build a constraint-count sweep harness in the factorial spirit of
[CogniLoad, OpenReview:0Sex2H5Jnn] — the manipulated variable is the number *n* of standing
constraints (single digits → several hundred), with applicability density (fraction of
constraints that actually bind in a given episode) controlled as a second factor so that
"more rules" is not confounded with "more binding rules." Constraints are drawn from a
dual-mode pool in the style of [RECAST, OpenReview:90tCp2KszA]: rule-based constraints with
programmatic checkers, plus model-based constraints with validated LLM judges. Compare full
pinning (all n constraints verbatim every turn) against no-pinning and a family of
selective-pinning policies (budget k tokens; selection by violation-frequency prior,
embedding relevance, relevance-minus-redundancy à la [COMI, OpenReview:OGDIXDfaN4], or an
LLM applicability classifier). Jointly record token overhead, violation rate, and task
success as functions of (n, policy, model) and locate the knee of the full-pinning curve by
changepoint regression.

**Staged plan** [HYPOTHESIS]:
- *Stage 0 — pilot (= the seed's minimal experiment, 最小实验).* One executable-checkable
  task suite, one mid-tier model, n ∈ {5, 25, 100, 300}, policies {full pinning, no pinning},
  ~60 tasks × 2 seeds ≈ 960 episodes. Goal: confirm the three metrics are computable and
  jointly movable, and get a first estimate of where (if anywhere) full-pinning success
  bends. Go/no-go: if success at n=300 is statistically indistinguishable from n=5 under
  full pinning, redesign task suite (constraints too easy / never binding) before scaling.
- *Stage 1 — scale-up.* Full grid: 7 n-levels {4, 10, 25, 50, 100, 200, 400} × 6 policies ×
  3 models × 150 tasks × 3 seeds; add applicability-density factor at 3 levels on a subgrid;
  human-validate the LLM-judge detector on a 300-episode stratified sample before trusting
  the curves.

**key_components:**
- **M1 — Constraint-count sweep harness** [HYPOTHESIS]: name "constraint-count sweep
  harness"; text: "instantiates episodes = (task, constraint set of size n) with n and
  applicability density independently controlled (CogniLoad-style factorial design);
  constraint pool built by RECAST-style mining so every constraint carries its own
  verification procedure; per-episode manifest records which constraints are applicable at
  which turns (ground-truth applicability labels, authored at pool-construction time)."
- **M2 — Full-pinning baseline & overhead instrumentation** [HYPOTHESIS]: name "full
  pinning"; text: "verbatim repetition of all n constraints in the system block every turn;
  instrument = tokenizer count of the constraint block per turn, reported both absolute and
  as overhead ratio (constraint tokens ÷ total prompt tokens), plus per-episode cumulative
  constraint tokens."
- **M3 — Selective-pinning policy family** [HYPOTHESIS]: name "selective-pinning selector";
  text: "given budget k tokens, selects a constraint subset per turn by one of: (a) random-k
  (floor), (b) static top-k by pilot-measured per-constraint violation frequency, (c)
  embedding similarity between the current step (last action + observation) and constraint
  text, (d) COMI-style marginal-gain scoring (relevance minus max similarity to already
  selected constraints), (e) LLM applicability classifier ('does rule r bind the next
  action?'). Granularity: re-selected every turn; selection latency and selector token cost
  are themselves logged as overhead."
- **M4 — Dual-mode violation detector** [HYPOTHESIS]: name "violation detector"; text:
  "per turn and per applicable constraint, flags violations via (i) programmatic checkers
  for rule-based constraints (exact, RECAST rule-mode) and (ii) an LLM judge for semantic
  constraints, calibrated against a 300-episode human-annotated stratified sample with a
  pre-registered acceptance bar of Cohen's κ ≥ 0.8; violation rate = violated
  (constraint, episode) pairs ÷ applicable (constraint, episode) pairs."
- **M5 — Joint trade-off tracker & knee locator** [HYPOTHESIS]: name "trade-off tracker";
  text: "logs the full (n, policy, model, seed) → {violation rate, overhead ratio, task
  success} table; fits segmented (piecewise-linear) regression of success on log n per
  policy and tests for a breakpoint (Davies test), reporting the estimated knee n* with a
  bootstrap confidence interval; renders the three-axis surface as Pareto plots rather than
  collapsing to one scalar."

**challenge_arguments:**
1. challenge_id `C1`, argument_text [HYPOTHESIS]: "Selective pinning caps pinned-constraint
   tokens at k regardless of n, directly relieving the finite-budget-vs-unbounded-count
   tension; the overhead instrumentation makes the crowding-out quantitative (overhead ratio
   vs task success)." mechanism_components: `["M3", "M2"]`.
2. challenge_id `C2`, argument_text [HYPOTHESIS]: "The factorial sweep with full pinning and
   the calibrated detector empirically *locates* where interference/dilution under redundant
   pinning shows up as measurable violation-rate or success decline — the harness surfaces
   the phenomenon and separates constraint-count load from raw prompt-length load via
   padding controls; it does not cure the phenomenon." mechanism_components: `["M1", "M2", "M4"]`.
3. challenge_id `C3`, argument_text [HYPOTHESIS]: "The selector family is conditioned on the
   current step and re-decided every turn; comparing semantic-similarity selection (c/d)
   against the applicability classifier (e), with ground-truth applicability labels from M1
   as reference, tests whether normative applicability is in fact reducible to similarity."
   mechanism_components: `["M3", "M1"]`.
4. challenge_id `C4`, argument_text [HYPOTHESIS]: "The tracker reports the three axes as a
   characterized Pareto surface with per-constraint-class breakdowns (safety vs preference)
   instead of forcing one scalar objective — describing the frontier, not resolving it."
   mechanism_components: `["M5"]`.
5. challenge_id `C5`, argument_text [HYPOTHESIS]: "Dual-mode verification puts the majority
   of constraints on exact programmatic checkers, and the LLM-judge remainder is accepted
   only after human calibration at κ ≥ 0.8 on a stratified sample — bounding
   detector-induced error before any curve is interpreted." mechanism_components: `["M4"]`.

**unaddressed_challenges:** `["C4"]` [HYPOTHESIS, flagged per V-08] — this rests on an
inferred methodology (no paper exists). The C4 argument only *measures/describes* the
trade-off surface; it supplies no principled decision rule for which frontier point a
deployer should choose, so C4 is at most partially addressed.

**Feasibility** [HYPOTHESIS]:
- *Scale:* Stage 0 ≈ 960 episodes × ~6 turns × ~4k tokens ≈ 25M tokens — tens of USD on a
  mid-tier API model; a weekend of wall-clock. Stage 1 ≈ 7 × 6 × 3 × 150 × 3 ≈ 57k episodes;
  at ~30k tokens/episode (large-n cells dominate) ≈ 1.7B tokens — mid-four-figure USD API
  cost class (or 1–2 A100/H100-weeks if run on open-weight models), plus ~50 annotator-hours
  (300 episodes × ~10 min) for judge calibration. Constraint-pool authoring with
  applicability labels: ~1–2 person-weeks assisted by RECAST-style mining.
- *Single biggest feasibility risk:* the violation detector at hundreds of heterogeneous
  constraints — if the LLM judge cannot reach κ ≥ 0.8, every downstream curve is
  uninterpretable (C5). *Mitigation:* skew the pool toward rule-based programmatically
  checkable constraints (target ≥ 70% of the pool, which RECAST shows is constructible at
  scale), run the headline analysis on the rule-based subset alone as a robustness check,
  and report semantic-constraint results separately with judge-error bars.

---

## N7 — Contributions

1. **CO1** [HYPOTHESIS]: "First controlled empirical characterization of the joint
   violation-rate / token-overhead / task-success trade-off as the number of pinned
   constraints scales from single digits to hundreds in LLM agents, with constraint count
   deconfounded from prompt length and from applicability density." contribution_type:
   `empirical_finding`, is_testable: true, has_rq: true.
2. **CO2** [HYPOTHESIS]: "A selective-pinning policy (budgeted, step-conditioned constraint
   selection) that maintains substantially lower token overhead than full pinning while
   approximately matching its violation rate at large constraint counts — and evidence on
   whether normative applicability is reducible to semantic relevance." contribution_type:
   `technical_artifact`, is_testable: true, has_rq: true.
3. **CO3** [HYPOTHESIS]: "Localization (with confidence interval) of a constraint-count knee
   n* beyond which full pinning's token overhead stops being merely wasteful and begins to
   measurably reduce task success." contribution_type: `empirical_finding`, is_testable:
   true, has_rq: true.
4. **CO4** [HYPOTHESIS]: "A reusable constraint-count sweep harness — constraint pool with
   per-constraint verification procedures and ground-truth applicability labels — for
   evaluating future context-management and constraint-retention strategies."
   contribution_type: `dataset`, is_testable: true, has_rq: true.

---

## N8 — Research Questions

- **RQ1** [GIVEN, near-verbatim restatement of the seed's 核心问题]: "As the number of
  constraints grows from single digits to hundreds, when does the token overhead of full
  pinning begin to backfire on task performance — i.e., at what point do violation rate,
  token overhead, and task success rate trade off against each other unfavorably?"
  - rq_source: `explicit` (given by seed)
  - evaluates_mechanisms: `["M1", "M2", "M4", "M5"]`
  - addresses_challenges: `["C1", "C2"]`
  - tests_contributions: `["CO1", "CO3"]`
  - answered_by_experiment: "Stage-0 pilot then Stage-1 full sweep (7 n-levels × full/no
    pinning × 3 models), segmented regression of success on log n with Davies breakpoint
    test (最小实验: 约束数量扫描下测违规率-开销-任务成功率三方权衡)."

- **RQ_INF_1** [GIVEN question, operationalized — the seed's core question explicitly contains
  this second sub-question "选择性 pinning 的选择策略是什么?"; the id keeps its original
  RQ_INF numbering from a prior revision for cross-reference stability]: "Which
  selective-pinning strategy best preserves a low constraint-violation rate under a bounded
  token budget as constraint count scales into the hundreds — and does applicability-aware
  selection beat similarity-only selection?"
  - rq_source: `explicit`
  - evaluates_mechanisms: `["M3", "M5"]`
  - addresses_challenges: `["C3", "C4"]`
  - tests_contributions: `["CO2"]`
  - answered_by_experiment: "Stage-1 comparison of the five M3 selectors against full/no
    pinning at matched token budgets across the same sweep; per-budget Pareto plots."

- **RQ_INF_2** [HYPOTHESIS, inferred from the factorial design]: "Is the degradation at
  large n driven by constraint *count* per se, by raw added prompt *length*, or by the
  number of constraints that actually *bind* (applicability density)?"
  - rq_source: `inferred`
  - evaluates_mechanisms: `["M1", "M5"]`
  - addresses_challenges: `["C2"]`
  - tests_contributions: `["CO1"]`
  - answered_by_experiment: "Subgrid with (i) length-matched padding controls (replace
    constraints with inert same-length text) and (ii) applicability density varied at 3
    levels holding n fixed."

- **RQ_INF_3** [HYPOTHESIS, inferred — measurement-validity RQ, mirroring the
  simulator-validity RQ in the Lost-in-Conversation exemplar]: "Is the dual-mode violation
  detector reliable enough that the measured violation-rate curves reflect agent behavior
  rather than detector error?"
  - rq_source: `inferred`
  - evaluates_mechanisms: `["M4"]`
  - addresses_challenges: `["C5"]`
  - tests_contributions: `["CO4"]`
  - answered_by_experiment: "Human annotation of a 300-episode stratified sample (by n,
    policy, constraint class); Cohen's κ between judge and humans, acceptance bar κ ≥ 0.8;
    headline analyses replicated on the programmatically-checkable subset."

**datasets** [HYPOTHESIS]: names: `["τ-bench (airline/retail policy-following tool-use agent
tasks — real domain policies as constraint seeds and task success via database-state
checks)", "IFEval (verifiable-instruction pool — rule-based constraint source)",
"FollowBench (multi-level constraint templates — constraint source, per RECAST's own
motivation)", "PrefEval (preference-following pairs — semantic-constraint source and
long-context distractor protocol)", "LMSYS-Chat-1M (distractor conversation filler, as used
by PrefEval)"]`. — note: constraint pool = IFEval/FollowBench/τ-bench-policy-derived
constraints scaled to n=400 via RECAST-style mining; task suite = τ-bench episodes plus a
synthetic executable-tool suite for exact success checking.

**baselines** [HYPOTHESIS]: names: `["full pinning (verbatim repeat-all, the stress-tested
default)", "no pinning (constraints stated once at episode start)", "random-k selection
(floor)", "static top-k by violation-frequency prior", "COMI-style relevance-minus-redundancy
selection [COMI, OpenReview:OGDIXDfaN4]", "LLM applicability-classifier selection"]`.

**metrics** [HYPOTHESIS]: names: `["constraint violation rate (violated applicable
(constraint,episode) pairs ÷ all applicable pairs)", "token overhead ratio (constraint tokens
÷ total prompt tokens per turn; plus absolute constraint tokens per episode)", "task success
rate (fraction of episodes passing the task's programmatic end-state check)",
"cost-adjusted success (success per 1k constraint tokens, secondary)", "detector agreement
(Cohen's κ vs human annotation)"]`.

**Analysis plan** [HYPOTHESIS]: 150 tasks × 3 seeds = 450 episodes per (n, policy, model)
cell — sized so a two-proportion comparison detects a 10-percentage-point success difference
(50% vs 60%) at power 0.8, α=0.05 (~388/arm required). Primary test: mixed-effects logistic
regression of episode success on log n × policy with task as random effect (episodes within
a task are not independent); violation rate analyzed with cluster-robust SEs at the episode
level. Knee location: segmented regression + Davies test for a breakpoint in success vs
log n under full pinning. Multiple comparisons across the policy grid corrected with
Holm–Bonferroni at family level α=0.05. Expected directions: success(full pinning)
non-increasing in n with a knee in the low-to-mid hundreds; violation rate(no pinning)
increasing in n; selective-k sitting between the two on violations at a fraction of the
overhead.

---

## N9 — Results (PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY; DO NOT TREAT AS FACT)

*No experiment has been run; no numbers exist. Every entry below is a predicted direction
plus an explicit falsification condition.*

1. **rq_id** `RQ1`
   - result_text [PLACEHOLDER — HYPOTHESIZED DIRECTION]: "Task success under full pinning is
     predicted to stay flat through the tens of constraints, then decline once n reaches the
     low-to-mid hundreds, coinciding with the overhead ratio consuming a large fraction of
     the per-turn budget; violation rate under full pinning is predicted to rise with n even
     while all constraints remain in context (C2 interference), i.e. pinning guarantees
     presence, not compliance."
   - result_type: `quantitative`; evidence_strength: `missing`; rq_answered: `false`
   - **Falsification condition**: refuted if, across the tested range up to n=400,
     full-pinning task success shows no statistically significant decline (segmented
     regression finds no breakpoint; mixed-model coefficient on log n ≥ 0) AND overhead
     ratio shows no negative association with success — i.e., "pin everything is always at
     least as good" survives the sweep.

2. **rq_id** `RQ_INF_1`
   - result_text [PLACEHOLDER — HYPOTHESIZED DIRECTION]: "A step-conditioned,
     applicability-aware selector is predicted to approximately match full pinning's
     violation rate while using a small fraction of its constraint tokens, with the gap in
     cost-adjusted success widening as n grows; similarity-only selection is predicted to
     lag applicability-aware selection on constraints whose binding conditions are not
     lexically/semantically cued by the current step."
   - result_type: `quantitative`; evidence_strength: `missing`; rq_answered: `false`
   - **Falsification condition**: refuted if every selective policy's violation rate is
     significantly and consistently worse than full pinning's at every tested budget k
     (Holm-corrected), i.e. no favorable selective trade-off exists and full pinning remains
     the only reliable option; the applicability-vs-similarity sub-claim is separately
     refuted if selectors (c)/(d) match (e) within equivalence bounds.

3. **rq_id** `RQ_INF_2`
   - result_text [PLACEHOLDER — HYPOTHESIZED DIRECTION]: "Degradation is predicted to be
     driven jointly by count and by applicability density, and only partially by raw length:
     length-matched inert padding is predicted to reproduce some but not all of the success
     decline, and violation rate is predicted to rise with density at fixed n."
   - result_type: `quantitative`; evidence_strength: `missing`; rq_answered: `false`
   - **Falsification condition**: refuted if inert same-length padding reproduces the full
     decline (pure length effect — the 'constraint' framing adds nothing), or if density has
     no measurable effect at fixed n.

4. **rq_id** `RQ_INF_3`
   - result_text [PLACEHOLDER — HYPOTHESIZED DIRECTION]: "The dual-mode detector is predicted
     to reach κ ≥ 0.8 overall, with programmatic checkers near-exact and the LLM judge the
     binding component; judge agreement is predicted to degrade somewhat at the largest n
     (longer transcripts to audit)."
   - result_type: `quantitative`; evidence_strength: `missing`; rq_answered: `false`
   - **Falsification condition**: refuted if κ < 0.8 after one calibration iteration — in
     which case the semantic-constraint curves must be withdrawn and only the
     programmatically-checkable subset reported.

---

## N10 — Threats / Self-Limitations

All [HYPOTHESIS] — anticipated limitations of this study design; no paper exists, so none
are author-acknowledged yet. Categorized per the schema enum; each carries a mitigation.

- **t1** category: `construct` — description: "'Violation' is operationalized via a
  dual-mode detector (M4); LLM-judge error on semantic constraints directly confounds the
  measured violation-rate curve — a noisy judge could manufacture or mask the very trade-off
  being characterized. Likewise 'token overhead' assumes tokenizer counts price cost, which
  ignores provider-side prompt caching that can make repeated pinned blocks cheaper than
  their token count suggests." mitigation: "κ ≥ 0.8 human-calibration gate (RQ_INF_3);
  replicate headline analyses on the programmatic-checker-only subset; report overhead both
  as raw tokens and as cache-adjusted effective cost."
- **t2** category: `internal` — description: "Constraint count n is mechanically entangled
  with prompt length, position of task content, and applicability density; without controls,
  any degradation at large n could be a pure long-prompt effect rather than a
  constraint-load effect." mitigation: "length-matched inert-padding control and independent
  applicability-density factor (RQ_INF_2, M1's factorial design, in the CogniLoad spirit of
  decoupling load dimensions)."
- **t3** category: `external` — description: "Findings may be specific to the tested model
  families, context lengths, and to a semi-synthetic constraint pool scaled up by
  RECAST-style mining — real enterprise policy sets have redundancy, hierarchy, and
  conflicts the pool may not reproduce, and the knee n* may shift with model scale."
  mitigation: "3 model families including one open-weight; seed the pool from real domain
  policies (τ-bench airline/retail policy documents); report per-constraint-class results so
  readers can re-weight for their own constraint mix."
- **t4** category: `conclusion` — description: "The (n × policy × model) grid invites many
  comparisons, and episodes sharing a task or a constraint subset are not independent —
  naive per-cell tests would overstate significance." mitigation: "pre-specified primary
  hypotheses (RQ1 knee, RQ_INF_1 policy contrast); mixed-effects models with task random
  effects and cluster-robust SEs; Holm–Bonferroni across the policy family at α=0.05."
- **t5** category: `scope` — description: "The study is scoped to bounded-horizon,
  single-session agent episodes with a fixed constraint set; constraints introduced,
  revised, or revoked mid-task (the ICF-Bench setting) and multi-session persistence are out
  of scope." mitigation: "explicit scoping statement; harness manifest format (M1) designed
  so a follow-up can add mid-episode constraint churn without rebuilding the pool."

**Status:** NOT_FOUND in the strict schema sense (no author-stated Threats section exists
yet) — absence_comment: {what_missing: "No paper exists, so there is no author-acknowledged
Limitations/Threats section.", why_matters: "The threats above are reviewer-anticipated, not
author-conceded, so they carry less epistemic weight than a real Limitations section
would.", implication: "Re-derive this node from the actual paper's Limitations/Discussion
once written; do not cite these as the paper's own claims."}

---

## N11 — Artifacts

**Status: NOT_FOUND.** [PLACEHOLDER] — the paper does not exist, so nothing has been
released.

- artifacts: `[]`
- has_code: `false`
- has_data: `false`
- has_model: `false`
- absence_comment: {what_missing: "No code, data, or model artifacts exist because no paper or implementation has been produced for this idea yet.", why_matters: "A reviewer or future implementer cannot verify or reuse anything from this digest — it is planning scaffolding, not evidence.", implication: "If the study is executed, CO4 (sweep harness + labeled constraint pool) is the natural release target; plan for it at design time."}

---

## N12 — Contribution Type

- **value**: `empirical` [HYPOTHESIS]
- **rationale** [HYPOTHESIS]: "Re-checked against the strengthened chain: the paper's spine
  is a controlled measurement study — a factorial constraint-count sweep over existing LLMs
  that deconfounds count, length, and applicability density and locates a breakpoint in the
  success curve (CO1/CO3, RQ1/RQ_INF_2) — exactly the shape of the empirical exemplars this
  digest imitates (a multi-model degradation study and a formatted-vs-unformatted token-cost
  study, both classified `empirical` despite releasing artifacts). The selective-pinning
  policy (CO2) is a compared *condition* inside the measurement design rather than a
  proposed system with its own engineering evaluation, and the harness (CO4) exists to
  support the measurement — so `empirical` beats `system`, `tool`, and `benchmark`. If, in
  execution, the labeled constraint pool becomes the headline reusable deliverable and the
  sweep merely its validation, `benchmark` would become the defensible alternative; that is
  the one classification hinge to re-check post hoc. The seed's own tag `[资源]`
  ('[Resource]') is a topic-collection label, not an N12 enum value, and does not override
  this."
- **source**: HYPOTHESIS (a prediction about how such a paper would be framed, not a fact).

---

## Claims

1. **[HYPOTHESIS]** "Full pinning of all standing constraints eventually reverses its own
   benefit as constraint count grows into the hundreds: past a knee n*, token overhead stops
   being wasteful spend and begins to measurably reduce task success — and even with every
   rule in context, violation rate rises with n because presence does not guarantee
   compliance." — evidence: [{type: "argument", text: "seed's core question ('when does it
   backfire') + corpus evidence that models degrade under many simultaneous requirements
   (RECAST motivation citing FollowBench) and that in-context items go unused under
   interference (Sculptor motivation; LostInTheMiddle)", source: "HYPOTHESIS", location:
   null}].
2. **[HYPOTHESIS]** "A bounded, step-conditioned, applicability-aware selective-pinning
   policy can approximately match full pinning's violation rate at a fraction of its token
   overhead once n exceeds the knee — and normative applicability is not reducible to
   semantic similarity, so COMI-style relevance selection will underperform an applicability
   classifier on rules whose binding conditions are not lexically cued." — evidence:
   [{type: "argument", text: "budgeted-selection reasoning transplanted from evidence
   compression ([COMI, OpenReview:OGDIXDfaN4]) plus the N4 observation that no prior work
   validates such selection for normative content", source: "HYPOTHESIS", location: null}].
3. **[HYPOTHESIS]** "Constraint-count load is a distinct degradation dimension from raw
   prompt length: length-matched inert padding will not reproduce the full effect." —
   evidence: [{type: "argument", text: "the CogniLoad design premise that conflated load
   dimensions must be decoupled to attribute degradation, applied to normative load",
   source: "GROUNDED:corpus", location: "[CogniLoad, OpenReview:0Sex2H5Jnn] motivation"}].
4. **[PLACEHOLDER]** "The exact knee n*, the size of the selective-vs-full gap, and the
   best-performing selector are unknown until the sweep is actually run." — evidence:
   [{type: "observation", text: "no experiment has been executed; this is the central open
   unknown of the idea", source: "PLACEHOLDER", location: null}].
5. **[HYPOTHESIS]** "No prior work jointly measures violation rate, token overhead, and task
   success while sweeping the count of simultaneously active constraints: multi-constraint
   work scales satisfaction not representation cost ([RECAST, OpenReview:90tCp2KszA]),
   retention benchmarks track one-to-few standing items ([PrefEval, OpenReview:QWunLKbBGF],
   [ICF-Bench, OpenReview:hcJywRYc3n]), context managers curate history not standing rules
   ([Sculptor, OpenReview:HPeiH7da0Z], [AgentFold, OpenReview:IuZoTgsUws]), and compression
   selects evidence not norms ([COMI, OpenReview:OGDIXDfaN4])." — evidence: [{type:
   "citation", text: "gap assembled from the six N4 limitations, each grounded in the cited
   paper's own motivation/method scope", source: "GROUNDED:corpus", location: null}].

---

## Self-verification pass (performed before output)

- V-01 (locator integrity): only [GIVEN] items claim extracted-equivalent status, anchored
  to the seed README's 核心问题/最小实验 lines; [GROUNDED:corpus] items are anchored to the
  named paper's motivation/method text in `ideas.jsonl`; all [HYPOTHESIS]/[PLACEHOLDER]
  items are marked speculative (`location: null`).
- V-02 (absence comment shape): every non-FOUND node (N0 partial, N10, N11) carries a full
  3-part absence_comment.
- EX-09 / V-04 (ID consistency, checked string-by-string):
  - `N4.affects_works` ⊆ N3 citation_keys: all six limitations use exactly
    `[RECAST, OpenReview:90tCp2KszA]`, `[PrefEval, OpenReview:QWunLKbBGF]`,
    `[ICF-Bench, OpenReview:hcJywRYc3n]`, `[Sculptor, OpenReview:HPeiH7da0Z]`,
    `[AgentFold, OpenReview:IuZoTgsUws]`, `[COMI, OpenReview:OGDIXDfaN4]`,
    `[CogniLoad, OpenReview:0Sex2H5Jnn]`, `[LostInTheMiddle, arXiv:2307.03172]` — 8/8
    resolve verbatim to N3 rows.
  - `N6.challenge_arguments[].challenge_id` ⊆ {C1..C5}: 5/5 resolve; every challenge has an
    argument.
  - `mechanism_components` ⊆ {M1..M5}: all resolve; M-ids assigned before arguments.
  - `N6.unaddressed_challenges` = {C4} ⊆ {C1..C5}.
  - N8 cross-refs: RQ1 → M1/M2/M4/M5, C1/C2, CO1/CO3; RQ_INF_1 → M3/M5, C3/C4, CO2;
    RQ_INF_2 → M1/M5, C2, CO1; RQ_INF_3 → M4, C5, CO4 — all ids exist.
  - `N9.results[].rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2, RQ_INF_3}: 4/4; every N8 RQ has an N9
    entry.
- V-08 (confidence doesn't inflate under inference): all N9 entries are
  `evidence_strength="missing"`, `rq_answered=false`, with explicit falsification
  conditions; N6.unaddressed_challenges flagged as resting on inferred methodology.
- V-10/V-11: N10 status NOT_FOUND (reviewer-anticipated threats only, now ≥4 and
  categorized with mitigations); N11 NOT_FOUND with all flags false and empty list.
- V-12: N12 rationale cites a concrete internal distinction (measurement spine vs CO2 as
  compared condition vs CO4 as support artifact) and names its one post-hoc hinge
  (`benchmark`), not circular.
- EX-11 (empty-node check): all of N0–N12 plus Claims present.
- EX-12 (field-name spot check): `objective`, `motivations`, `citation_key`,
  `approach_summary`, `limitation_text`, `affects_works`, `text` (challenges),
  `key_components`, `challenge_arguments`, `unaddressed_challenges`, `rq_source`,
  `evaluates_mechanisms`, `addresses_challenges`, `tests_contributions`,
  `answered_by_experiment`, `result_text`, `evidence_strength`, `rq_answered` — no
  forbidden renames.
