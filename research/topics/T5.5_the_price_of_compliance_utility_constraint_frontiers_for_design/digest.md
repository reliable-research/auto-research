# Digest: The Price of Compliance: Utility-Constraint Frontiers for Design-Aware Coding Agents

> **REVERSE-DIGEST DISCLAIMER.** No paper exists yet for this topic. This document is
> speculative scaffolding for research planning, constructed backward from a seed idea
> (title, core question, minimal experiment) to the full N0–N12 digest shape. Every field
> below is tagged **[GIVEN]** (verbatim/near-verbatim from the seed), **[HYPOTHESIS]**
> (reasoned prediction, not a fact), **[GROUNDED:corpus]** (a real OpenReview paper from
> `topics/corpus/ideas.jsonl`, verified by reading its motivation/method text),
> **[GROUNDED:non-corpus]** (a real published paper outside the local corpus, cited only
> where the digest author is confident it exists), or **[PLACEHOLDER]** (genuinely
> unknowable until the work is done — never invented). Treat all predicted directions as
> illustrative-only until a real paper is written and re-digested with the standard
> `paper-digest` skill.

Seed source: `topics/T5.5_the_price_of_compliance_utility_constraint_frontiers_for_design/README.md`
— code T5.5, label `[资源]` ("Resource"), parent topic "T5. 设计约束合规（coding agent）"
("T5. Design-constraint compliance (coding agents)").

Style exemplars imitated for specificity level:
`samples/best_papers_recent3_digest/ICSE_2026_Hidden_Cost_Readability_LLM_Budget.md`
(constraint-cost empirical study; named benchmarks, per-component operationalization,
statistical tests named in N8) and
`samples/best_papers_recent3_digest/ICLR_2026_LLMs_Get_Lost_Multi_Turn_Conversation.md`
(large-scale degradation-measurement study; controlled simulation arms, decomposition
metrics, conservative-bias threat arguments).

---

## N0 — Metadata

- `title`: "The Price of Compliance: Utility-Constraint Frontiers for Design-Aware Coding Agents" **[GIVEN]** — verbatim from seed README line 16.
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — no paper exists; no authors can be known.
- `abstract` **[HYPOTHESIS]** (drafted synthesis, explicitly not a real abstract):
  > "Coding agents are increasingly asked to obey design constraints — architectural
  > layering rules, dependency conventions, complexity ceilings, style mandates — on top of
  > producing functionally correct code. We ask how much enforcing such constraints costs:
  > does pass rate degrade gracefully or collapse past some threshold, and how does
  > token/retry cost scale with constraint strength? We parametrically sweep a
  > design-constraint-strength knob (a graded ladder of machine-checkable design rules over
  > breadth and strictness) across executable coding benchmarks, under multiple enforcement
  > mechanisms (prompt-injection vs. checker-in-the-loop retry), measuring task pass rate,
  > residual constraint-violation rate, and generation cost at each level, and trace out
  > the resulting three-dimensional compliance-utility frontier. We characterize whether
  > this frontier degrades smoothly or exhibits a sharp knee — a distinction that
  > determines whether design-aware coding agents are engineering-feasible to deploy."
- `doi`: null **[PLACEHOLDER]**
- `arxiv_id`: null **[PLACEHOLDER]**
- `num_pages`: null **[PLACEHOLDER]**
- `research_area`: "SE" **[HYPOTHESIS]** — the parent topic ("设计约束合规（coding agent）")
  is squarely a software-engineering evaluation construct (design constraints, pass rate,
  coding agents); the measurement machinery overlaps with ML-evaluation practice but the
  object of study is an SE artifact and the natural venue class is ICSE/FSE-style empirical
  tracks (cf. the exemplar `ICSE_2026_Hidden_Cost_Readability_LLM_Budget`, an ICSE paper
  with the same "cost of a constraint on LLM coding" shape).
- **Status:** PARTIAL — title given; authors/abstract are placeholder/hypothesis, not extracted.
- `absence_comment`: {"what_missing": "There is no actual paper, so no real author list, DOI, arXiv id, or page count exist yet.", "why_matters": "Downstream consumers of this digest (e.g. paper-writer or reviewer agents) must not treat N0 identity fields as real bibliographic facts.", "implication": "Treat N0 as a planning placeholder only; re-run the standard paper-digest skill once an actual manuscript exists."}

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**, built as a full predicate directly from the core question:
  "measure, via a parametric sweep of enforced design-constraint strength under controlled
  enforcement mechanisms, how much task pass rate degrades and generation cost increases
  for LLM-based coding agents, and statistically characterize the shape (linear vs.
  knee/cliff) of the resulting pass-rate × violation-rate × cost frontier, to assess the
  engineering feasibility of design-aware coding agents."
  - Kind of task: measurement / controlled parametric sweep study. Domain: LLM coding
    agents under design-constraint enforcement. Outcome shape: a 3D empirical frontier
    plus a hypothesis-tested shape characterization (graceful vs. knee).
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. A suite of coding tasks with verifiable functional correctness (unit tests/oracles),
     e.g. BigCodeBench-style function-level tasks and a SWE-bench-style repository-level
     subset.
  2. A catalog of design/architecture constraints, each implemented as a deterministic
     machine-checkable rule (AST/static-analysis check), organized into a graded
     strength ladder over two axes: breadth (how many rules active) and strictness
     (per-rule thresholds).
  3. A constraint-strength parameter (ordinal ladder in the pilot; factorial
     breadth × strictness grid in the scale-up) controlling the active rule set.
  4. An enforcement-mechanism arm (prompt-only vs. checker-in-the-loop bounded retry).
- `outputs` **[HYPOTHESIS]**:
  1. Per-strength-level, per-arm measurements: task pass rate, residual violation rate,
     generation cost (tokens, retries, wall-clock, USD).
  2. A fitted 3D frontier (pass rate × violation rate × cost) across swept strength, with
     breakpoint/segmented-regression analysis of its shape.
- `constraints` **[GIVEN]** — from the seed: the study is explicitly a "参数化扫描约束强度"
  (parametric sweep of constraint strength) producing a three-axis frontier of "pass rate ×
  违规率 (violation rate) × 成本 (cost)"; beyond this the seed states no further formal
  constraint (e.g. no ground-truth definition of "violation" beyond the parent topic T5
  design-constraint-compliance framing).
- **Status:** PARTIAL — objective/inputs/outputs are reasoned inference (source=inferred),
  not extracted from a real methods section.
- `absence_comment`: {"what_missing": "No actual paper text exists to extract a formal problem statement from.", "why_matters": "A reviewer needs to know this formulation is a plausible reconstruction, not the authors' own wording.", "implication": "Use this objective as a planning target; expect the real paper's formulation to differ in specifics (e.g. exact constraint taxonomy)."}

---

## N2 — Motivation

**[HYPOTHESIS]**, reconstructed from the parent-topic framing "T5. 设计约束合规（coding agent）"
(design-constraint compliance for coding agents) — no statistics invented.

- `motivation_text`: "As coding agents generate production code, organizations want them to
  obey not just functional correctness but design-level constraints (architecture
  patterns, layering rules, dependency and complexity policies) — the broader concern of
  parent topic T5. But mandating compliance is not free: each enforced constraint is a
  candidate source of reduced functional pass rate and increased inference cost (longer
  prompts, more retries, more verification passes). Adjacent evidence makes the worry
  concrete: instruction-following benchmarks document substantial degradation as the
  number of simultaneous constraints grows ([RECAST, OpenReview:90tCp2KszA] motivation,
  citing FollowBench), and the safety-alignment literature has named the analogous
  phenomenon an 'alignment tax' ([NSPO, OpenReview:GFyVxtyMvq]). If the coding-agent
  version of this trade-off is severe (a cliff rather than graceful degradation),
  design-aware coding agents may be engineering-infeasible at meaningful constraint
  strength — directly decision-relevant for anyone building such agents." **[HYPOTHESIS]**,
  `source`="inferred", `evidence`=[grounded pointers to the two corpus papers above].
- **Status:** PARTIAL — grounded in the seed's parent-topic framing and real adjacent
  findings, but the specific motivating narrative is authored by this digest.
- `absence_comment`: {"what_missing": "No real Introduction section exists to extract motivating claims or citations from.", "why_matters": "A reader should not mistake this motivation paragraph for the authors' actual framing.", "implication": "Treat as a reasonable planning rationale, revise once the real paper's Introduction is written."}

---

## N3 — Related Works

**Grounding procedure.** Keyword search over the local corpus
`topics/corpus/ideas.jsonl` (11,683 OpenReview papers) with eight query angles:
(1) "code generation; constraint; instruction following", (2) "trade-off; pareto;
frontier", (3) "alignment tax; safety; helpfulness; utility", (4) "SWE-bench; coding
agent; software engineering agent; repository", (5) "code quality; readability;
maintainability; code style", (6) "inference cost; token budget; test-time compute;
accuracy cost trade-off", (7) "constrained decoding; grammar; syntactic constraint",
(8) "architecture; design pattern; software design; dependency injection". Full
motivation+method texts of every cited hit were read. **Honest coverage report:** the
corpus contains no paper that directly performs a parametrized design-constraint-strength
sweep with a joint pass-rate/violation-rate/cost frontier for coding agents — the specific
idea appears unstudied in this corpus, and the corpus's SE coverage of design-constraint
compliance specifically is thin. Entries 1–7 below are the nearest real corpus neighbors
(each **[GROUNDED:corpus]**, `[ShortName, OpenReview:paper_id]`); entries 8–10 are
canonical non-corpus citations kept because the corpus lacks direct SE matches, clearly
marked **[GROUNDED:non-corpus]** (all three are papers this digest's author is confident
exist; two are additionally cross-attested inside corpus papers' own motivation texts).

1. `citation_key`: "[SWE-bench, OpenReview:VTF8yNQM66]" — **[GROUNDED:corpus]**
   `approach_summary`: Constructs a large-scale, execution-verified benchmark pairing real
   GitHub issues with resolving pull requests; correctness is defined by fail-to-pass
   repository tests, moving evaluation from isolated functions to repository-scale edits.
   The de-facto substrate for evaluating coding agents' functional utility.
2. `citation_key`: "[RECAST, OpenReview:90tCp2KszA]" — **[GROUNDED:corpus]**
   `approach_summary`: Synthesizes large-scale multi-constraint instruction data by mining
   verifiable constraints (rule-based programmatic checks plus model-based checks) from
   seed corpora and recombining them into high-complexity instructions; trains with
   constraint-level verification rewards (RLVC) to improve simultaneous satisfaction of
   many constraints.
3. `citation_key`: "[AutoIF, OpenReview:cRR0oDFEBC]" — **[GROUNDED:corpus]**
   `approach_summary`: Self-play framework that has LLMs generate verifiable instructions
   plus executable verification functions and unit tests, then uses execution pass/fail
   feedback as scalable supervision (SFT + preference optimization) for constrained
   instruction following — establishing the "constraint checker as executable code"
   pattern.
4. `citation_key`: "[SMC-Control, OpenReview:xoXn62FzD0]" — **[GROUNDED:corpus]**
   `approach_summary`: Programmable sequential Monte Carlo framework treating controlled
   generation as posterior sampling under a product of constraint potentials: cheap
   syntactic constraints shape token-level proposals while expensive semantic constraints
   (e.g. executability) enter as incremental particle reweighting — an explicit
   compute-for-compliance enforcement mechanism.
5. `citation_key`: "[NSPO, OpenReview:GFyVxtyMvq]" — **[GROUNDED:corpus]**
   `approach_summary`: Frames safety alignment as a constrained optimization whose utility
   cost ("safety alignment tax", degrading reasoning/coding ability) is structural; projects
   safety policy-gradient updates into the null space of general-capability representations
   to improve safety while preserving utility.
6. `citation_key`: "[RMOD, OpenReview:i0Nno5MgXt]" — **[GROUNDED:corpus]**
   `approach_summary`: Casts multi-objective controlled decoding (helpfulness, safety,
   instruction-following) as a max-min game over adversarial objective weights, yielding an
   inference-time policy that optimizes worst-case trade-offs — explicitly Pareto-frontier
   framing of conflicting alignment objectives at decode time.
7. `citation_key`: "[FairFront, OpenReview:65oFEAP42P]" — **[GROUNDED:corpus]**
   `approach_summary`: Computes the optimal fairness–performance Pareto front exactly by
   reducing fair representation learning to finite-dimensional concave optimization over
   Bayes-posterior distributions — methodological precedent for characterizing an entire
   utility-constraint frontier rather than isolated operating points.
8. `citation_key`: "[HiddenCost-Readability, ICSE 2026]" — **[GROUNDED:non-corpus]**
   (Pan, Sun, Zhang, Lo, Du, "The Hidden Cost of Readability: How Code Formatting Silently
   Consumes Your LLM Budget", ICSE 2026, arXiv 2508.13666; verified via the local
   best-paper digest sample.)
   `approach_summary`: Large-scale empirical study of one code-level constraint dimension
   (human-readability formatting) on LLM cost and correctness: removing formatting cuts
   input tokens ~24.5% with negligible Pass@1 change across 10 LLMs and 4 languages, with
   McNemar/Mann-Whitney significance testing — the closest published template for
   "constraint dimension × pass rate × token cost" measurement in SE.
9. `citation_key`: "[IFEval, Zhou et al., 2023]" — **[GROUNDED:non-corpus]**
   (arXiv 2311.07911; also cross-attested as @zhou2023ifeval inside the corpus motivation
   text of [AutoIF, OpenReview:cRR0oDFEBC].)
   `approach_summary`: Defines a suite of programmatically verifiable instruction
   constraints (format, length, keyword rules) and measures LLM satisfaction rates —
   establishing objective, checker-based constraint-compliance measurement for LLM outputs.
10. `citation_key`: "[FollowBench, Jiang et al., 2024]" — **[GROUNDED:non-corpus]**
    (ACL 2024; cross-attested as @jiang2024followbench inside the corpus motivation text of
    [RECAST, OpenReview:90tCp2KszA].)
    `approach_summary`: Multi-level constraint-following benchmark that incrementally adds
    constraints to instructions (five graded levels) and measures satisfaction at each
    level — the closest existing precedent for a graded "constraint-strength ladder",
    documenting substantial model degradation as constraints accumulate.

**Status:** PARTIAL (all works real and verified; their mapping onto this unwritten paper's
related-work section is this digest's inference).
`absence_comment`: {"what_missing": "No corpus or known non-corpus work jointly sweeps design-constraint strength and measures the pass-rate × violation-rate × cost frontier for coding agents; corpus SE coverage of design-constraint compliance is thin (searches 5 and 8 returned no on-topic SE hits).", "why_matters": "Absence in this 11.7k-paper corpus is encouraging for novelty but is not proof of global absence — arXiv-first SE work and industrial reports are under-covered.", "implication": "Before final scoping, run a supplementary arXiv/DBLP search for 'architecture conformance + LLM' and 'constrained code generation cost' to confirm the gap."}

---

## N4 — Prior Limitations

`grounding_check`: true — every limitation cites at least one N3 `citation_key` verbatim,
and each is defensible from the cited paper's own motivation/method text (corpus entries)
or its digest (non-corpus entries). All **[HYPOTHESIS]** as N4 framing for an unwritten
paper, but grounded per-item as noted.

1. `limitation_text`: "Defines coding-agent utility purely as fail-to-pass test resolution;
   the task definition contains no design-constraint dimension, no violation-rate metric,
   and treats generation cost as outside the benchmark's scoring — so it cannot reveal what
   compliance costs." (Defensible: its method text defines correctness solely via
   execution-based fail-to-pass filtering.) `affects_works`: ["[SWE-bench, OpenReview:VTF8yNQM66]"]
   `limitation_type`: "generalizability".
2. `limitation_text`: "Optimizes and measures satisfaction of output-level NL constraints
   (format, lexical, semantic), not repository-level software design constraints, and
   reports satisfaction rates without jointly measuring the utility (pass-rate) and cost
   price paid for enforcement; AutoIF is additionally confined to code-verifiable
   constraint types, as RECAST's own motivation states." `affects_works`:
   ["[RECAST, OpenReview:90tCp2KszA]", "[AutoIF, OpenReview:cRR0oDFEBC]"]
   `limitation_type`: "generalizability".
3. `limitation_text`: "Measures constraint-satisfaction degradation as constraints
   accumulate, but on general instruction tasks without an independent functional
   correctness oracle — so compliance cannot be traded off against task utility, and cost
   is not an evaluation axis." `affects_works`: ["[IFEval, Zhou et al., 2023]",
   "[FollowBench, Jiang et al., 2024]"] `limitation_type`: "other".
4. `limitation_text`: "Provides an enforcement mechanism whose compute grows with
   constraint difficulty (particles, expensive semantic potentials — its own motivation
   notes such constraints are 'neither token-local nor cheap'), but evaluates constraint
   satisfaction and distributional fidelity, not a swept strength-vs-pass-rate-vs-cost
   frontier." `affects_works`: ["[SMC-Control, OpenReview:xoXn62FzD0]"]
   `limitation_type`: "efficiency".
5. `limitation_text`: "Documents and mitigates the utility tax of one constraint class
   (training-time safety alignment) but does not parametrize constraint strength, and its
   trade-off axes (harmlessness vs. reasoning ability) are not the inference-time design
   constraints of coding agents." `affects_works`: ["[NSPO, OpenReview:GFyVxtyMvq]"]
   `limitation_type`: "generalizability".
6. `limitation_text`: "Treats the multi-objective trade-off as given (reward models per
   objective already exist) and solves the decode-time weight-selection problem; it does
   not empirically map what the frontier between compliance, functional correctness, and
   cost actually looks like for agentic coding." `affects_works`:
   ["[RMOD, OpenReview:i0Nno5MgXt]"] `limitation_type`: "other".
7. `limitation_text`: "Computes exact Pareto fronts only under classification-style
   structure (Bayes-optimal label posteriors, concave utilities); open-ended code
   generation admits no such closed form, so the compliance-utility frontier must be
   measured empirically rather than derived." `affects_works`:
   ["[FairFront, OpenReview:65oFEAP42P]"] `limitation_type`: "theoretical".
8. `limitation_text`: "Measures the token-cost/pass-rate impact of a single, semantically
   neutral constraint dimension (formatting), removable without changing program behavior;
   it does not study semantically binding design constraints (layering, dependency,
   complexity rules) that can conflict with task solutions, nor any enforcement-strength
   sweep." `affects_works`: ["[HiddenCost-Readability, ICSE 2026]"]
   `limitation_type`: "generalizability".

**Status:** FOUND (as grounded limitations tied to verified citation keys; none invented
without a grounding work).

---

## N5 — Challenges

Problem-inherent obstacles, independent of any specific prior tool (N4-vs-N5 test applied:
these are about why the sweep-and-frontier problem itself is hard). Stable C-ids preserved
from the previous digest revision. **[HYPOTHESIS, derived from the core question]**

1. `id`: "C1" `text`: "Design constraints are typically stated in natural language /
   qualitative form (e.g. 'keep layers decoupled'); turning 'violation' into an objective,
   checkable, and *sweepable* quantity requires an operationalization step that is itself a
   validity risk — an over-literal rule catalog may not represent real design intent."
   **[HYPOTHESIS]**
2. `id`: "C2" `text`: "Pass rate, violation rate, and cost need not vary monotonically or
   independently as constraint strength increases — enforcement can trigger retry loops
   that simultaneously depress pass rate and inflate cost — so the frontier's shape
   (smooth vs. knee/cliff) cannot be assumed a priori and must be discovered empirically
   with enough sweep resolution to detect a breakpoint." **[HYPOTHESIS]**
3. `id`: "C3" `text`: "'Constraint strength' is inherently multi-dimensional — breadth (how
   many rules are active) and strictness (each rule's threshold) are distinct — and
   collapsing them into one ordinal knob conflates different sources of pass-rate loss and
   cost; yet a full factorial sweep multiplies experiment cost." **[HYPOTHESIS]**
4. `id`: "C4" `text`: "Measured cost is entangled with the enforcement mechanism: the same
   constraint set costs differently under prompt-only injection vs. checker-in-the-loop
   retry, so any single-mechanism frontier risks measuring the mechanism, not the
   constraints; and 'cost' itself is multi-faceted (input/output tokens, retries,
   latency, USD)." **[HYPOTHESIS]**

`conflation_check`: true (operationalization validity; shape unpredictability;
strength dimensionality vs. sweep budget; mechanism/cost entanglement — four distinct
obstacles).

**Status:** FOUND (as problem-inherent obstacles derived from the core question; every
item inline-tagged `[HYPOTHESIS]` — nothing extracted from a real paper, per this
digest's reverse-digest convention).

---

## N6 — Methodology

**[HYPOTHESIS]** — extrapolated from the one-sentence minimal experiment ("约束强度参数化扫描，
画 pass rate × 违规率 × 成本的三维前沿" **[GIVEN]**), made operational at the specificity
level of the exemplar digests.

### `overview`
**[HYPOTHESIS]** `text`: "Build a coding-agent evaluation harness with a parameterized
design-constraint-strength knob mapped to concrete, machine-checkable rule sets, run agents
on executable benchmarks at each strength level under controlled enforcement mechanisms,
and log pass rate, residual violation rate, and cost per attempt; aggregate into a 3D
frontier and statistically test its shape.

**Staged plan.**
*Stage 1 — pilot (= the seed's minimal experiment, verbatim scope):* one model
(a mid-tier API model, e.g. GPT-4o-mini-class), ~150 BigCodeBench-Hard function-level
tasks, a single ordinal strength ladder L0–L4 (L0 = no constraints; L1–L4 = cumulative
rule packs of the catalog below), prompt-only enforcement, 5 sampled generations per
(task, level). Deliverable: the first pass-rate × violation-rate × cost frontier plot and
a go/no-go signal on whether strength levels produce measurable separation.
*Stage 2 — scale-up:* 3 models (one frontier API, one mid-tier API, one open-weight),
add a repository-level suite (50-task SWE-bench Verified subset with per-repo applicable
rule mapping), replace the ordinal ladder with a factorial breadth (3 levels) × strictness
(3 levels) grid to unconfound C3, and add a second enforcement arm (checker-in-the-loop
bounded retry, k ≤ 3, violation feedback in-context) plus a binary all-or-nothing arm, to
unconfound C4. Segmented-regression shape analysis with bootstrap CIs is run on the
scale-up data."

### `key_components`
- `id`: "M1" `name`: "Machine-checkable design-constraint catalog + strength
  parameterization" `text`: "A catalog of ~20 design rules, each implemented as a
  deterministic AST/static-analysis check — import-layering / dependency-direction rules
  (import-linter-style contracts), cyclomatic-complexity and function-length ceilings
  (radon/ruff thresholds), naming and visibility conventions, forbidden-API lists,
  dependency-injection mandates (no direct instantiation of service classes). Strength is
  parameterized as (breadth b = number of active rule packs, strictness s = per-rule
  threshold tier); pilot uses the ordinal ladder L0–L4 (cumulative packs at fixed
  strictness), scale-up uses the 3×3 (b, s) grid. Instrument: rule configs versioned in
  the harness; granularity: rule × task × attempt." **[HYPOTHESIS]**
- `id`: "M2" `name`: "Controlled enforcement mechanisms (arms)" `text`: "Three arms:
  (a) prompt-only — active rules rendered as explicit numbered instructions in the system
  prompt; (b) checker-in-the-loop — after each generation, M3's violation report is fed
  back and the agent retries, bounded at k=3; (c) binary all-or-nothing — all rules on,
  single shot (baseline for graded sweeps). Instrument: harness config flag; granularity:
  arm × task × attempt." **[HYPOTHESIS]**
- `id`: "M3" `name`: "Compliance/violation checker + human validity audit" `text`:
  "Deterministic static analyzers per rule (no LLM judge in the primary metric).
  Violation rate = violated-rule count / active-rule count per task, macro-averaged.
  Checker validity audited on a 100-sample stratified subset by 2 human annotators
  labeling 'genuine design violation vs. checker artifact'; rules with Cohen's κ < 0.8
  against human judgment are dropped from the catalog. Instrument: linter suite + audit
  protocol; granularity: rule × solution." **[HYPOTHESIS]**
- `id`: "M4" `name`: "Cost instrumentation" `text`: "Per attempt: input tokens, output
  tokens, #API calls, #retries, wall-clock latency; converted to USD via published
  per-token prices; reported both disaggregated and as cost-per-solved-task. Instrument:
  API usage metadata logged by the harness; granularity: attempt-level, aggregated to
  (task, level, arm)." **[HYPOTHESIS]**
- `id`: "M5" `name`: "Frontier construction & shape analysis" `text`: "Aggregate (pass
  rate, violation rate, cost) per (level, arm, model); fit linear vs. piecewise-linear
  (segmented) regressions of pass rate and cost against strength; test breakpoint
  existence (Davies test), compare fits by AIC/BIC; bootstrap (1,000 resamples over tasks)
  for CIs on the knee location. Deliverable: the 3D frontier surface + a
  knee-exists/knee-absent verdict per model × arm." **[HYPOTHESIS]**
- `id`: "M6" `name`: "Constraint-annotated task suites" `text`: "Function-level:
  BigCodeBench-Hard (~150 tasks, executable unit tests). Repository-level: 50 tasks from
  SWE-bench Verified with a per-repository mapping of which catalog rules are applicable
  (e.g. layering contracts derived from the repo's existing package structure).
  Suite construction is an instrument, not a headline contribution; released for
  reproducibility." **[HYPOTHESIS]**

### `challenge_arguments`
- `challenge_id`: "C1" `argument_text`: "Restricting the catalog (M1) to deterministic
  machine-checkable rules and auditing checker validity against human design judgment
  (M3, κ ≥ 0.8 gate) converts fuzzy design intent into an objective, sweepable quantity
  while bounding the operationalization-validity risk." `mechanism_components`: ["M1", "M3"]
  **[HYPOTHESIS]**
- `challenge_id`: "C2" `argument_text`: "A 5-level pilot ladder refined to a 3×3 grid, with
  segmented-regression breakpoint testing and bootstrap CIs (M5), gives the sweep enough
  resolution to detect (or statistically reject) a knee rather than assuming a functional
  form." `mechanism_components`: ["M1", "M5"] **[HYPOTHESIS]**
- `challenge_id`: "C3" `argument_text`: "The scale-up's factorial breadth × strictness grid
  (M1) disentangles the two strength axes that the pilot's ordinal ladder deliberately
  conflates, at a sweep-budget cost contained by keeping the grid at 3×3."
  `mechanism_components`: ["M1"] **[HYPOTHESIS]**
- `challenge_id`: "C4" `argument_text`: "Running the identical constraint sets under
  separate enforcement arms (M2) with disaggregated cost logging (M4) lets
  mechanism-induced cost (retry blowup) be separated from constraint-induced difficulty —
  the frontier is reported per arm, never pooled." `mechanism_components`: ["M2", "M4"]
  **[HYPOTHESIS]**

### `unaddressed_challenges`
`[]` — with the staged design, each C-id has an explicit mechanism; note per V-08 that C1
and C3 are only *mitigated* (κ-gated catalog; 3×3 grid), not eliminated: the catalog still
undersamples the space of real design constraints, and 3 levels per axis bounds breakpoint
resolution on each axis. These residuals reappear as threats t1/t3 in N10.

### Feasibility (order-of-magnitude)
**[HYPOTHESIS]**
- *Pilot:* 150 tasks × 5 levels × 5 samples = 3,750 generations, ≈ 10⁷ tokens →
  **$30–150 API cost class**, ~2–3 days wall-clock with rate limits; harness + rule
  catalog ≈ 2–3 person-weeks of engineering.
- *Scale-up:* 3 models × 2 suites × (9 grid cells + arms) × 5 samples ≈ 4–6 × 10⁴
  generations (SWE-bench-style agentic runs dominate cost) → **$2k–8k API cost class**;
  checker audit ≈ 100 samples × 2 annotators × ~3 min ≈ **10 annotator-hours**; open-weight
  arm ≈ tens of GPU-hours on a single A100-class node.
- *Single biggest feasibility risk:* constructing design rules that are simultaneously
  (a) objectively machine-checkable, (b) genuinely binding on the benchmark tasks (a rule
  no solution ever approaches violating produces a degenerate sweep), and (c) faithful to
  real design intent. **Mitigation:** pilot includes a rule-bindingness screen — any rule
  violated by <5% of unconstrained (L0) generations is replaced before the scale-up — plus
  the M3 κ-audit for faithfulness; repository-level rules are derived from each repo's own
  existing structure rather than invented.

**Note (V-08 compliance):** every item in this node is `source="inferred"` — no real
methods section exists.

**Status:** FOUND (as a fully specified pre-registered methodology proposal; every item
`source="inferred"` per the V-08 note above — no real methods section exists to extract
from).

---

## N7 — Contributions

**[HYPOTHESIS]** — what such a paper would plausibly claim.

1. `id`: "CO1" `text`: "A parameterized, open experimental protocol (harness + κ-audited
   machine-checkable design-rule catalog + constraint-annotated task suites) for sweeping
   design-constraint strength in coding agents while jointly measuring pass rate,
   violation rate, and cost." `contribution_type`: "technical_artifact" `is_testable`: true
   `has_rq`: true **[HYPOTHESIS]**
2. `id`: "CO2" `text`: "The first empirical characterization of the compliance-utility
   frontier's shape for design-aware coding agents — a statistically tested verdict on
   graceful degradation vs. knee/cliff, per model and enforcement mechanism."
   `contribution_type`: "empirical_finding" `is_testable`: true `has_rq`: true
   **[HYPOTHESIS]**
3. `id`: "CO3" `text`: "A cost-accounting decomposition attributing the 'price of
   compliance' to distinct components (prompt overhead vs. retry blowup vs. output
   inflation) and to the enforcement mechanism vs. the constraints themselves."
   `contribution_type`: "conceptual_framework" `is_testable`: true `has_rq`: true
   **[HYPOTHESIS]**

**Status:** FOUND (as plausible claimed contributions for the unwritten paper; every
item inline-tagged `[HYPOTHESIS]`, `source="inferred"`).

---

## N8 — Research Questions

RQ ids RQ1 and RQ_INF_1 are stable from the previous digest revision; RQ_INF_2 is added to
cover the mechanism-attribution axis (C4).

1. `id`: "RQ1" **[GIVEN]**, near-verbatim restatement of the seed's core question:
   `text`: "How much does enforcing design constraints reduce coding-agent task pass rate
   and increase generation cost, and what does the resulting compliance-utility frontier
   (pass rate × violation rate × cost) look like across constraint-strength levels?"
   `rq_source`: "explicit" `evaluates_mechanisms`: ["M1", "M2", "M3", "M4", "M6"]
   `addresses_challenges`: ["C1", "C3"] `tests_contributions`: ["CO1", "CO2"]
   `answered_by_experiment`: "Pilot ladder sweep (150 BigCodeBench-Hard tasks × 5 levels ×
   5 samples, prompt-only arm) then scale-up 3×3 breadth × strictness grid on
   BigCodeBench-Hard + 50-task SWE-bench Verified subset, 3 models." **[GIVEN + HYPOTHESIS mapping]**
   - *Analysis plan* **[HYPOTHESIS]**: n = 150 tasks × 5 samples = 750 attempts per
     (level, model, arm) cell. Primary test: mixed-effects logistic regression of per-attempt
     pass on strength level (task as random intercept); report odds ratio per level with
     95% CI. Trend: Cochran–Armitage test across levels. α = 0.05, Holm-corrected across
     models and arms. Expected direction: pass-rate odds decrease and cost-per-solved-task
     increases monotonically with strength.
2. `id`: "RQ_INF_1" **[HYPOTHESIS]**, inferred from the seed's second sentence
   ("合规-效用前沿的形状决定该方向的工程可行性" — frontier shape determines engineering
   feasibility):
   `text`: "Does the compliance-utility frontier degrade gracefully (near-linear) or
   exhibit a statistically detectable knee/cliff beyond some strength threshold, and is
   the knee location consistent across models?" `rq_source`: "inferred"
   `evaluates_mechanisms`: ["M5"] `addresses_challenges`: ["C2"]
   `tests_contributions`: ["CO2"] `answered_by_experiment`: "Segmented vs. linear
   regression of pass rate (and cost) on strength, per model × arm, on scale-up data."
   - *Analysis plan* **[HYPOTHESIS]**: Davies test for breakpoint existence at α = 0.05;
     model selection by ΔAIC > 4 favoring the piecewise fit; knee-location CI via 1,000
     task-level bootstrap resamples; cross-model consistency = overlapping knee CIs.
     Expected direction: a knee exists (plateau then sharp drop) for the retry arm at least.
3. `id`: "RQ_INF_2" **[HYPOTHESIS]**, inferred from the C4 mechanism-entanglement problem:
   `text`: "How much of the measured compliance cost and pass-rate loss is attributable to
   the enforcement mechanism (prompt overhead, retry blowup) rather than to the constraints
   themselves, and does checker-in-the-loop retry buy lower violation rates at
   sub-proportional or super-proportional cost relative to prompt-only enforcement?"
   `rq_source`: "inferred" `evaluates_mechanisms`: ["M2", "M4"]
   `addresses_challenges`: ["C4"] `tests_contributions`: ["CO3"]
   `answered_by_experiment`: "Identical constraint grids run under arms (a)/(b)/(c) of M2
   with disaggregated M4 cost logs; arm × strength interaction analysis."
   - *Analysis plan* **[HYPOTHESIS]**: two-way (arm × strength) mixed-effects model on pass
     and on log-cost; the interaction term tests mechanism attribution, α = 0.05,
     Holm-corrected. Expected direction: retry arm reduces violation rate vs. prompt-only
     at equal strength but with super-linear cost growth at high strength (retry blowup).

`datasets` (EvalEntityGroup) **[HYPOTHESIS]**: `names`: ["BigCodeBench-Hard (~150
function-level tasks, executable unit tests; pilot + scale-up)", "SWE-bench Verified
(50-task repository-level subset with per-repo applicable-rule mapping; scale-up only)"],
`source`: "inferred". Rationale: both are real, execution-verified, and standard for
coding-agent evaluation ([SWE-bench, OpenReview:VTF8yNQM66] is itself in N3); BigCodeBench
gives cheap high-n sweeps, SWE-bench Verified gives realistic repository context where
design rules bind.

`baselines` (EvalEntityGroup) **[HYPOTHESIS]**: `names`: ["L0 / strength-0 (no active
constraints) — within-study control anchoring the utility ceiling", "Binary all-or-nothing
enforcement (M2 arm c) — the naive deployment policy the graded sweep is compared against",
"Prompt-only vs. checker-in-the-loop arms as mutual baselines (RQ_INF_2)",
"External anchor: satisfaction-only degradation curves from [FollowBench, Jiang et al., 2024]
and constraint-satisfaction training results from [RECAST, OpenReview:90tCp2KszA], compared
qualitatively (their axes lack pass-rate/cost, per N4.3/N4.2)"], `source`: "inferred".

`metrics` (EvalEntityGroup) **[HYPOTHESIS]**: `names`: ["Pass@1 (fraction of attempts
passing all unit tests; per level/arm/model)", "Residual violation rate (violated active
rules / active rules, macro-averaged over tasks; M3 checker)", "Compliant-pass rate (joint:
passes tests AND zero violations — the deployable-output rate)", "Cost per attempt (input
tokens, output tokens, #retries, wall-clock, USD at published prices)", "Cost per
compliant-solved task (primary economic metric)", "Knee location + 95% bootstrap CI
(strength units; M5)"], `source`: "inferred".

**Status:** PARTIAL. `absence_comment`: {"what_missing": "No real evaluation section exists; datasets/baselines/metrics are a concrete proposal, not extracted specifics.", "why_matters": "A reader should not assume these benchmarks have actually been run.", "implication": "Treat as the pre-registered instantiation of the minimal experiment; revise dataset sizes after the pilot's power check."}

---

## N9 — Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTIONS ONLY, NOT REAL DATA]**. No experiment has been
run; `evidence_strength="missing"` and `rq_answered=false` for every item. Each result
states a predicted direction plus an explicit falsification condition. No numbers are
fabricated.

1. `rq_id`: "RQ1" `result_text` (predicted direction): "Pass rate decreases and
   cost-per-compliant-solved-task increases as constraint strength grows, with breadth
   (more rules) costing more pass rate than strictness (tighter thresholds) at equal
   ladder position; violation rate decreases with strength under enforcement but remains
   nonzero." `result_type`: "quantitative" `evidence_strength`: "missing"
   `rq_answered`: false **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
   **Falsification condition:** refuted if the mixed-effects model finds no significant
   negative strength coefficient on pass (Holm-adjusted p ≥ 0.05) or if cost per
   compliant-solved task is flat across the swept range — i.e. compliance turns out to be
   approximately free, which would itself be a publishable negative result removing the
   premise of the 'price of compliance' framing.
2. `rq_id`: "RQ_INF_1" `result_text` (predicted direction): "The frontier exhibits a knee:
   a 'cheap compliance' region where pass rate holds and cost rises modestly, then a
   threshold beyond which pass rate drops sharply and cost inflates disproportionately;
   knee location differs across models (stronger models push the knee to higher strength)."
   `result_type`: "quantitative" `evidence_strength`: "missing" `rq_answered`: false
   **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
   **Falsification condition:** refuted if the Davies test fails to reject linearity
   (p ≥ 0.05) and ΔAIC favors the linear fit for all model × arm cells — supporting a
   proportional cost-of-compliance relationship and undermining the seed's claim that
   frontier *shape* (not just slope) determines engineering feasibility.
3. `rq_id`: "RQ_INF_2" `result_text` (predicted direction): "Checker-in-the-loop retry
   achieves lower residual violation rates than prompt-only at equal strength, but with
   super-linear cost growth at high strength driven by retry-loop blowup; a substantial
   share of total cost is attributable to the mechanism rather than the constraint set."
   `result_type`: "quantitative" `evidence_strength`: "missing" `rq_answered`: false
   **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
   **Falsification condition:** refuted if the arm × strength interaction is
   non-significant (Holm-adjusted p ≥ 0.05) — i.e. the frontier is mechanism-invariant —
   or if retry costs grow sub-linearly, implying enforcement mechanism choice is a
   second-order concern and the frontier is a property of the constraints alone.
4. `rq_id`: "RQ_INF_1" `result_text` (predicted direction): "Even at maximum swept
   strength under the retry arm, residual violation rate does not reach 0%, indicating a
   nonzero compliance floor for current coding agents." `result_type`: "quantitative"
   `evidence_strength`: "missing" `rq_answered`: false
   **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
   **Falsification condition:** refuted if violation rate reaches exactly 0% at a finite,
   affordable strength level (cost per compliant-solved task within ~2× of L0) — full
   compliance would then be achievable at tractable cost.

**Status:** NOT_FOUND (no real results exist). `absence_comment`: {"what_missing": "No experiment has been executed; all result text is predicted direction, not measured data.", "why_matters": "A reviewer must not cite these directions as findings — they are pre-registered planning hypotheses.", "implication": "Re-digest with the standard paper-digest skill once the pilot has actually run."}

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS]** — anticipated threats, categorized by validity type, each with a planned
mitigation; none are author-acknowledged yet since no paper exists.

1. `threat_id`: "t1" `category`: "construct" `description`: "The machine-checkable rule
   catalog (M1/M3) is a proxy for real design intent; checker false positives/negatives
   bias measured violation rate, and rules chosen for checkability may over-represent
   trivially mechanical constraints." `mitigation`: "M3's human audit with κ ≥ 0.8 gate per
   rule; report per-rule (not only aggregate) violation rates so readers can discount
   contested rules; derive repository-level rules from each repo's own existing structure."
   **[HYPOTHESIS]**
2. `threat_id`: "t2" `category`: "internal" `description`: "Observed cost/pass-rate effects
   may be caused by the enforcement mechanism (prompt length, retry loop) rather than the
   constraints — e.g. longer prompts alone can shift pass rate independent of constraint
   content." `mitigation`: "RQ_INF_2's multi-arm design with arm × strength interaction
   testing; a length-matched placebo-prompt control (irrelevant text of equal token count
   at each level) added in the scale-up." **[HYPOTHESIS]**
3. `threat_id`: "t3" `category`: "external" `description`: "Frontier shape and knee
   location are measured on ≤3 model families, two Python-centric benchmarks, and one rule
   catalog; results may not transfer to other languages, model scales, agent scaffolds, or
   constraint taxonomies (e.g. security or concurrency constraints)." `mitigation`:
   "Span one frontier + one mid-tier + one open-weight model; report per-model frontiers
   rather than pooled; release harness and catalog (CO1) so the sweep is rerunnable on new
   models/suites; scope claims to the studied catalog explicitly." **[HYPOTHESIS]**
4. `threat_id`: "t4" `category`: "conclusion" `description`: "Knee detection via segmented
   regression on 5 ladder points (pilot) or 3 levels per axis (scale-up grid) has limited
   resolution and multiple-comparison exposure across model × arm cells; a spurious
   breakpoint could be reported, or a real one missed." `mitigation`: "Davies test +
   ΔAIC > 4 dual criterion; Holm correction across cells; 1,000-resample task-level
   bootstrap CIs on knee location; pilot power check before committing scale-up budget;
   densify levels around any pilot-detected knee." **[HYPOTHESIS]**
5. `threat_id`: "t5" `category`: "internal" `description`: "Rule-bindingness confound: if
   some rules are never near-violated by unconstrained generations, higher 'strength'
   levels add nominal but inert constraints, flattening the frontier artificially."
   `mitigation`: "The M6/M1 bindingness screen — replace any rule violated by <5% of L0
   generations — applied between pilot and scale-up; report L0 violation prevalence per
   rule." **[HYPOTHESIS]**

**Status:** PARTIAL. `absence_comment`: {"what_missing": "These are anticipated reviewer-style threats authored by this digest, not limitations stated in a real paper's Threats section.", "why_matters": "N10 normally captures author-acknowledged limitations; presenting these as such would overstate their status.", "implication": "Use as a pre-registration checklist; re-derive from the real paper's Threats section once written."}

---

## N11 — Artifacts

**[PLACEHOLDER]** — nothing has been released; the paper does not exist.

`artifacts`: [] `has_code`: false `has_data`: false `has_model`: false

**Status:** NOT_FOUND. `absence_comment`: {"what_missing": "No code repository, dataset, model, or demo has been released because no experiment has been run.", "why_matters": "There is currently zero reproducibility surface for this idea.", "implication": "When implemented, populate with: code_repo (sweep harness + M3 checker suite), dataset (constraint-annotated BigCodeBench/SWE-bench task mappings, M6), and logged run traces for the frontier fits."}

---

## N12 — Contribution Type

`value`: "empirical" **[HYPOTHESIS]**

`rationale`: "The deliverable N9 is built to validate is a measured, swept relationship —
pass rate × violation rate × cost as a function of constraint strength — over *existing*
LLM coding agents, with the headline claim being a statistically tested shape verdict
(RQ_INF_1), exactly the profile of the measurement-study exemplars imitated here
(`ICSE_2026_Hidden_Cost_Readability_LLM_Budget`: measures formatting-constraint cost across
existing LLMs → empirical; `ICLR_2026_LLMs_Get_Lost_Multi_Turn_Conversation`: measures
multi-turn degradation of existing LLMs → empirical). The harness, rule catalog, and
constraint-annotated suites (CO1, M6) could support a `benchmark` classification if the
suite were the headline deliverable — and the seed's `[资源]` (Resource) label gestures that
way — but the core question ('how much does pass rate drop, cost rise, and what shape does
the frontier take') is answered by the sweep's findings, not by the suite's existence; the
artifacts exist to support the measurement, matching the 'measurement study with a
published dataset → empirical if the study is the main contribution' rule. Not `system`
or `tool`: no new agent or enforcement technique is proposed as the contribution."
**[HYPOTHESIS]**

`source`: "inferred" (no real paper to extract N12 from).

**Status:** FOUND (as an inferred classification with an exemplar-weighed rationale;
`source="inferred"`, inline-tagged `[HYPOTHESIS]`).

---

## Claims

1. **[HYPOTHESIS]** "Enforcing design constraints on coding agents produces a non-trivial,
   likely non-linear trade-off: pass rate degrades and cost increases with constraint
   strength, plausibly with a knee beyond which compliance costs escalate
   disproportionately." `evidence`: [{"type": "argument", "text": "Derived from core
   question + minimal experiment; adjacent evidence that multi-constraint satisfaction
   degrades with constraint count exists in [FollowBench, Jiang et al., 2024] as reported
   in [RECAST, OpenReview:90tCp2KszA]'s motivation, and constraint-utility taxes are
   documented for safety alignment in [NSPO, OpenReview:GFyVxtyMvq].", "source":
   "hypothesis", "location": null}]
2. **[GIVEN, elaborated]** "The shape of the compliance-utility frontier (graceful vs.
   cliff-like), not merely its average cost, is the key determinant of whether
   design-constraint enforcement is practically deployable in coding agents." —
   near-verbatim elaboration of the seed: "合规-效用前沿的形状决定该方向的工程可行性".
   `evidence`: [{"type": "citation", "text": "Seed README core-question sentence 2",
   "source": "given", "location": "README.md line 18"}]
3. **[GROUNDED:corpus + HYPOTHESIS]** "No paper in the 11,683-paper local OpenReview corpus
   jointly sweeps design-constraint strength and measures a pass-rate × violation-rate ×
   cost frontier for coding agents: the nearest neighbors measure constraint satisfaction
   without a utility/cost axis ([RECAST, OpenReview:90tCp2KszA], [AutoIF,
   OpenReview:cRR0oDFEBC]), utility without a compliance axis ([SWE-bench,
   OpenReview:VTF8yNQM66]), enforcement mechanisms without a swept frontier ([SMC-Control,
   OpenReview:xoXn62FzD0]), or trade-off frontiers in non-code domains ([FairFront,
   OpenReview:65oFEAP42P], [RMOD, OpenReview:i0Nno5MgXt])." `evidence`: [{"type":
   "observation", "text": "Absence confirmed across 8 keyword-angle searches of
   ideas.jsonl (see N3 grounding procedure); corpus is OpenReview-centric, so SE-venue and
   arXiv-first work may be under-indexed — treat as novelty-encouraging, not novelty-proving.",
   "source": "grounded-corpus", "location": null}]
4. **[HYPOTHESIS]** "A substantial fraction of the measured price of compliance is
   attributable to the enforcement mechanism (prompt overhead, retry blowup) rather than
   to constraint difficulty itself, so frontiers must be reported per enforcement arm."
   `evidence`: [{"type": "argument", "text": "Derived from C4 and the RQ_INF_2 multi-arm
   design; precedent that enforcement machinery carries its own compute cost is explicit
   in [SMC-Control, OpenReview:xoXn62FzD0]'s motivation ('neither token-local nor cheap').",
   "source": "hypothesis", "location": null}]
5. **[HYPOTHESIS]** "Residual violation rate likely never reaches zero at affordable
   strength, implying a practical compliance ceiling for current coding agents."
   `evidence`: [{"type": "argument", "text": "Derived from checker-imperfection and
   retry-dynamics reasoning (N5 C1/C2, N10 t1); analogous nonzero floors appear in
   constrained instruction following per [IFEval, Zhou et al., 2023]-style benchmarks.",
   "source": "hypothesis", "location": null}]

---

## Self-verification pass

- **V-01 (locator integrity):** No item is tagged `source="extracted"` from a real target
  paper (none exists); corpus grounding is anchored to `ideas.jsonl` paper_ids, non-corpus
  grounding to explicit bibliographic identifiers (arXiv 2508.13666, arXiv 2311.07911,
  ACL 2024); seed-given content is anchored to README.md.
- **V-02 (absence comments):** Every node with non-FOUND status carries a 3-part
  `absence_comment` (N0, N1, N2, N3, N8, N9, N10, N11).
- **EX-09 (cross-node id consistency), checked exhaustively:**
  - `N4.affects_works` ⊆ `N3.citation_key`, verbatim string match, all 10 keys used:
    "[SWE-bench, OpenReview:VTF8yNQM66]" (N4.1), "[RECAST, OpenReview:90tCp2KszA]" +
    "[AutoIF, OpenReview:cRR0oDFEBC]" (N4.2), "[IFEval, Zhou et al., 2023]" +
    "[FollowBench, Jiang et al., 2024]" (N4.3), "[SMC-Control, OpenReview:xoXn62FzD0]"
    (N4.4), "[NSPO, OpenReview:GFyVxtyMvq]" (N4.5), "[RMOD, OpenReview:i0Nno5MgXt]"
    (N4.6), "[FairFront, OpenReview:65oFEAP42P]" (N4.7),
    "[HiddenCost-Readability, ICSE 2026]" (N4.8). ✓
  - `N6.challenge_arguments[].challenge_id` ∈ {C1, C2, C3, C4}; all four covered. ✓
  - `N6.challenge_arguments[].mechanism_components` ⊆ {M1–M6}. ✓
  - `N6.unaddressed_challenges` = [] ⊆ N5 ids. ✓
  - `N8.addresses_challenges` ⊆ {C1–C4}; `N8.evaluates_mechanisms` ⊆ {M1–M6};
    `N8.tests_contributions` ⊆ {CO1–CO3}; every CO id is tested by ≥1 RQ (CO1←RQ1,
    CO2←RQ1/RQ_INF_1, CO3←RQ_INF_2), consistent with `has_rq=true` on all three. ✓
  - `N9.rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2} — used: RQ1 (×1), RQ_INF_1 (×2), RQ_INF_2 (×1). ✓
- **V-08 (confidence discipline):** N6/N9/N10 flagged as resting entirely on inferred or
  placeholder content; N9 uniformly `evidence_strength="missing"`, `rq_answered=false`,
  no fabricated numbers (all numerals in N6/N8 are design parameters, not results).
- **V-10/V-11:** N10 PARTIAL with 5 categorized threats, each with a mitigation
  (consistent); N11 NOT_FOUND with empty artifacts and all flags false (consistent).
- **V-12 (N12 rationale quality):** Rationale weighs `empirical` against `benchmark`
  concretely, citing the exemplar precedents and the seed's `[资源]` label.
- **Empty-node check (EX-11):** All of N0–N12 plus Claims present; none omitted.
- **RQ id stability:** RQ1 and RQ_INF_1 retain their prior ids and core meanings; RQ_INF_2
  is additive. C1–C4 ids retained with sharpened text; CO1–CO3 retained.
