# Digest: Two Sound Checks, One Unsound Gate: Emergent Shortcuts under Verifier Composition

> **REVERSE DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet. This document
> projects an N0–N12 structured digest forward from a one-paragraph research-idea seed
> (topic code **B1.4**, label **[矛盾]**, parent topic **B1. Verifier 充分性（agent /
> 代码场景）**), for research-planning purposes only. Every field below is tagged
> **[GIVEN]** (verbatim/near-verbatim from the seed README), **[HYPOTHESIS]** (reasoned
> elaboration / prediction, not fact), or **[PLACEHOLDER]** (genuinely unknowable until
> the work is actually done — never invented). N3 entries additionally carry
> **[GROUNDED:corpus]**: real OpenReview papers retrieved from the local 11,683-paper
> ideas.jsonl corpus, with summaries grounded in each paper's own motivation/method text.
> Treat all non-GIVEN content as a forecast to be falsified, not a reported result.

---

## N0 — Metadata

- **title** [GIVEN]: "Two Sound Checks, One Unsound Gate: Emergent Shortcuts under Verifier Composition"
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper exists, no author list can be known.
- **abstract** [HYPOTHESIS] (drafted by synthesizing the seed's core question + minimal
  experiment into abstract prose; explicitly a draft, not a real abstract):
  > "Verification pipelines for LLM agents and code generation increasingly gate acceptance,
  > reward, or deployment on stacks of checks — unit tests plus a static/style gate, an
  > outcome verifier plus a flawed-reasoning detector, a safety classifier plus a task-success
  > judge — under the implicit assumption that combining individually sound checks can only
  > tighten the gate. We note that this assumption is subtler than it looks: extensionally,
  > the AND/OR of two sound acceptors on a fixed task is trivially sound; in practice, each
  > verifier is certified sound only relative to its own checked facet, its own task variant,
  > and the solution distribution over which certification was performed. In that realistic
  > regime we test whether composition preserves soundness. We construct matched task pairs
  > — a single-verifier variant on which the assigned verifier is certified shortcut-free
  > (by exhaustive search over a bounded program space and mutation-based differential
  > testing), and a composed AND/OR variant of the same task — and run a budget-matched
  > adversarial search for candidates that satisfy the composed gate while failing held-out
  > ground truth. We ask whether such emergent shortcuts exist, at what rate, and under what
  > structural conditions (operationalized as the overlap of the two verifiers' mutant-kill
  > sets). If compositional gaps exist and recur under identifiable conditions, this is a
  > counter-intuitive and general warning for every multi-check gating pipeline."
- **doi** [PLACEHOLDER]: null
- **arxiv_id** [PLACEHOLDER]: null
- **num_pages** [PLACEHOLDER]: null
- **research_area** [HYPOTHESIS]: `"AI/ML"` — inferred from the parent topic's framing
  ("agent / 代码场景", i.e. LLM-agent and code-generation verification); a strong secondary
  fit would be `SE` (test oracles, mutation analysis, gate design), and the corpus grounding
  below (RLVR reward design, guardrails, judge reliability) confirms the primary community
  is ML safety-of-verification.

---

## N1 — Problem Formulation

- **objective** [HYPOTHESIS], built as a full predicate from the seed's core question:
  "measure, via constructed matched task pairs in an LLM-agent/code-verification setting,
  whether the AND (conjunctive) or OR (disjunctive) composition of two verifiers — each
  certified sound in isolation relative to its own checked facet and certification
  distribution — remains sound, or whether composition admits an emergent shortcut (a
  candidate accepted by the combined gate that fails held-out ground truth) that neither
  verifier admits alone; and characterize the structural conditions (coverage
  complementarity between the two verifiers' failure surfaces) under which such gaps
  appear." (Kind of task: measurement + existence demonstration via constructed
  counterexamples; domain: code-generation / agent verification gates; outcome shape:
  existence certificates, gap-rate estimates, and a structural taxonomy — not a universal
  theorem.)
- **inputs** [HYPOTHESIS], inferred from the minimal experiment:
  - "A task family with a checkable ground truth (reference solution + differential-test
    input corpus), small enough that per-verifier soundness can be certified."
  - "Two candidate verifiers A and B (e.g., a unit-test suite and a static/property/judge
    check), each individually certified sound on its assigned single-verifier task variant
    at a stated certification budget (no shortcut passes A alone; none passes B alone)."
  - "A composition rule: AND (must pass both) or OR (must pass either), plus the adversarial
    search budget granted to the attacker of each gate."
- **outputs** [HYPOTHESIS]:
  - "A suite of matched task pairs with machine-checkable certificates: single-verifier
    variants certified shortcut-free, composed variants with a discovered shortcut (or a
    certified absence at budget)."
  - "Gap-rate estimates per composition rule and verifier-pair type, and a classification of
    each discovered shortcut by the structural relationship between A's and B's blind spots."
- **constraints** [GIVEN + HYPOTHESIS refinement]: the seed's minimal experiment explicitly
  requires a controlled contrast pair — each single-verifier task must have **no shortcut**
  (单检查无捷径) while the composed task is constructed so a shortcut **does** exist
  (组合后有捷径) [GIVEN]. [HYPOTHESIS] refinement to avoid vacuity: because the conjunction
  of two extensionally sound acceptors on one fixed task is trivially sound, "soundness" must
  be operationalized per-verifier — relative to the facet each verifier checks, its assigned
  task variant, and a stated finite certification procedure — and the adversarial budgets
  attacking single vs. composed gates must be matched.

**What N1 is NOT here:** not a claim that any real deployed pipeline has this flaw (that's
N2/N9 territory), not a description of the not-yet-built method (N6).

---

## N2 — Motivation

**motivations:**

1. **motivation_text** [HYPOTHESIS], reconstructed from the parent topic framing (B1:
   whether verifiers are *sufficient* guarantees in agent/code settings) and grounded in the
   corpus: "Real pipelines are already composing checks at scale: RLVR systems bolt
   flawed-reasoning detectors onto outcome verifiers ([FAPO, OpenReview:jhqqoimoWt]),
   open-ended RLVR decomposes one reward into chains of verifiable content and style checks
   ([RewardChain, OpenReview:ZumVIktGbt]), SWE pipelines combine execution-based tests with
   execution-free reward models ([SWE-RM, OpenReview:H9wMe1G76j]), and guardrails aggregate
   per-category safety scores ([R2-Guard, OpenReview:CkgKSqZbuC]) — all under the implicit
   monotonicity assumption that adding a sound check never introduces a new failure mode.
   No cited work tests that assumption for the composed gate itself." `source="hypothesis"`,
   `evidence=[]` (the pipeline descriptions are grounded; the untested-assumption claim is
   the hypothesis).
2. **motivation_text** [GIVEN]/[HYPOTHESIS] blend: the seed states the payoff condition
   explicitly — "反直觉结论若成立，对所有多重校验管线是普适警告" (if the counter-intuitive
   conclusion holds, it is a general warning for all multi-verification pipelines) [GIVEN,
   near-verbatim]. The generalization beyond constructed examples is the paper's motivating
   stake, not a demonstrated fact — flagged [HYPOTHESIS] as a claim about *why it would
   matter if true*.

---

## N3 — Related Works

**Grounding note.** All entries below are real papers retrieved from the local OpenReview
corpus (`topics/corpus/ideas.jsonl`, 11,683 papers) via keyword search from four angles
(RLVR/verifiable rewards; unit-test/oracle generation; LLM-judge reliability; guardrail /
defense composition; reward hacking / specification gaming). Each `approach_summary` is
grounded in the paper's own motivation/method text. Their fit to this not-yet-written paper
is my mapping, hence [GROUNDED:corpus] rather than any author's own related-work framing.

**works:**

1. **citation_key**: `[CorrelatedProxies, OpenReview:msEr27EejF]` [GROUNDED:corpus]
   — *Correlated Proxies: A New Definition and Improved Mitigation for Reward Hacking.*
   Formalizes a proxy reward as valid only if positively correlated with the true reward
   under a reference policy's occupancy measure, defines reward hacking as optimization
   breaking that correlation, and derives chi-squared occupancy-measure regularization as a
   provable mitigation; its motivation notes hacking "persists even when reward models are
   improved or combined via ensembles."
   `paper_url`: https://openreview.net/forum?id=msEr27EejF
2. **citation_key**: `[RewardChain, OpenReview:ZumVIktGbt]` [GROUNDED:corpus]
   — *From Verifiable Dot to Reward Chain.* Extends RLVR to open-ended generation by
   converting each reference answer into a *composition* of verifiable sub-rewards —
   hierarchical key-point/keyword content matching scored by normalized LCS, plus
   code-rule style checks — optimized jointly with GRPO, explicitly to avoid learned-reward
   hacking. `paper_url`: https://openreview.net/forum?id=ZumVIktGbt
3. **citation_key**: `[FAPO, OpenReview:jhqqoimoWt]` [GROUNDED:corpus]
   — *Flawed-Aware Policy Optimization.* Documents that outcome-only RLVR verifiers reward
   flawed-positive rollouts (correct answer via invalid reasoning, e.g. guessing) exactly
   like sound ones, and adds a second check — a generative flawed-positive detector with
   step-level error localization — whose signal reshapes the reward.
   `paper_url`: https://openreview.net/forum?id=jhqqoimoWt
4. **citation_key**: `[SWE-RM, OpenReview:H9wMe1G76j]` [GROUNDED:corpus]
   — *SWE-RM: Execution-free Feedback for Software Engineering Agents.* Motivated by
   execution-based validation being sparse, binary, and misaligned when test suites are
   incomplete or noisy, trains a trajectory-level generative reward model (YES-probability
   reward) selected for ranking, AUC, and calibration, intended to complement
   execution-based checks in SWE-agent pipelines.
   `paper_url`: https://openreview.net/forum?id=H9wMe1G76j
5. **citation_key**: `[R2-Guard, OpenReview:CkgKSqZbuC]` [GROUNDED:corpus]
   — *R2-Guard: Robust Reasoning Enabled LLM Guardrail.* Observes that guardrails composed
   of independent per-category unsafety classifiers with heuristic aggregation
   under-estimate risk "when unsafe intent is distributed across multiple weak signals,"
   and compiles explicit first-order safety rules into a Markov Logic Network for exact
   probabilistic inference over the category scores.
   `paper_url`: https://openreview.net/forum?id=CkgKSqZbuC
6. **citation_key**: `[FilterBarriers, OpenReview:CwoM9T55lG]` [GROUNDED:corpus]
   — *Computational Barriers to Filtering for AI Alignment.* Proves a cryptographic
   impossibility: harmful instructions hidden in pseudorandom time-lock puzzles embedded in
   benign-distribution prompts are computationally indistinguishable from benign text to
   any external filter sufficiently faster than the model, recasting moderation failure as
   computational asymmetry rather than classifier quality.
   `paper_url`: https://openreview.net/forum?id=CwoM9T55lG
7. **citation_key**: `[UTRL, OpenReview:VqjNYF9nbP]` [GROUNDED:corpus]
   — *Learning to Generate Unit Tests via Adversarial Reinforcement Learning.* Jointly
   trains a unit-test generator and a code generator from instruction–code pairs only,
   rewarding test suites by *discrimination* — accepting the reference implementation while
   rejecting sampled imperfect programs — so the verifier is adversarially hardened against
   the current solver's failure modes. `paper_url`: https://openreview.net/forum?id=VqjNYF9nbP
8. **citation_key**: `[JudgeLimits, OpenReview:NO6Tv6QcDs]` [GROUNDED:corpus]
   — *Limits to Scalable Evaluation at the Frontier.* Theoretical analysis of LLM-as-judge
   as a proxy label: ties achievable efficiency gains of debiased evaluation to
   proxy–truth correlation and proves that when the evaluated model outperforms the judge,
   correlation is bounded, capping what a single judge-based check can certify.
   `paper_url`: https://openreview.net/forum?id=NO6Tv6QcDs
9. **citation_key**: `[BiasScope, OpenReview:QGOw6AU8Lp]` [GROUNDED:corpus]
   — *BiasScope: Automated Detection of Bias in LLM-as-a-Judge Evaluation.* Iteratively
   discovers a judge's blind spots beyond any predefined taxonomy: a teacher model perturbs
   rejected responses, misjudgments and the judge's own explanations are mined for new
   candidate biases, and candidates are validated against objective correctness labels —
   i.e., an automated failure-surface characterization for one verifier.
   `paper_url`: https://openreview.net/forum?id=QGOw6AU8Lp

**Status: FOUND** (9 real, corpus-grounded works spanning the mechanism [composed
rewards/checks], the failure mode [reward hacking, flawed positives, filter bypass, judge
bias], and the evaluation domain [code/SWE agents, RLVR, guardrails]).
**Residual-gap note** (kept, since it defines the novelty claim): no retrieved paper
studies the AND/OR *soundness algebra* of two individually certified verifiers as its
subject — the closest works either compose checks assuming the combination is safe
([RewardChain, OpenReview:ZumVIktGbt], [FAPO, OpenReview:jhqqoimoWt], [R2-Guard,
OpenReview:CkgKSqZbuC]) or analyze a single check's limits ([JudgeLimits,
OpenReview:NO6Tv6QcDs], [FilterBarriers, OpenReview:CwoM9T55lG], [BiasScope,
OpenReview:QGOw6AU8Lp]). That absence is precisely the seed's claimed gap.

---

## N4 — Prior Limitations

**grounding_check** [HYPOTHESIS]: `true` — every limitation cites at least one
`N3.works[].citation_key`, verbatim, and is defensible from the cited paper's own
motivation text or from what its method demonstrably does not cover.

1. **limitation_text** [HYPOTHESIS]: "Reward-hacking theory formalizes the breakdown of a
   *single* proxy's correlation with the true objective and even observes that ensembling
   reward models does not stop hacking — but it models neither the Boolean AND/OR algebra
   of hard gates nor the question of whether composition itself manufactures a shortcut
   absent from each component; the mitigation (occupancy regularization) is defined for one
   proxy at a time." `affects_works`: `["[CorrelatedProxies, OpenReview:msEr27EejF]"]`.
   `limitation_type`: `generalizability`.
2. **limitation_text** [HYPOTHESIS]: "Composed-check reward designs assume decomposition is
   safety-improving: RewardChain motivates its ordered-LCS content matching as preventing
   'unordered keyword stuffing' and FAPO motivates its flawed-positive detector as tightening
   the outcome gate — but neither analyzes the soundness of the *combined* gate, i.e.,
   whether a rollout can satisfy every sub-check (content + style, or outcome + process)
   while still failing the intended task; the composition is validated only by end-task
   gains." `affects_works`: `["[RewardChain, OpenReview:ZumVIktGbt]", "[FAPO, OpenReview:jhqqoimoWt]"]`.
   `limitation_type`: `theoretical`.
3. **limitation_text** [HYPOTHESIS]: "Execution-free verifiers for SWE agents are motivated
   by the incompleteness/noise of execution-based tests and are positioned as complements
   to them, but verifier quality is measured by best-of-k ranking, AUC, and calibration of
   the *individual* model — not by the false-acceptance behavior of the execution-check +
   reward-model combination the pipeline actually gates on."
   `affects_works`: `["[SWE-RM, OpenReview:H9wMe1G76j]"]`. `limitation_type`: `precision`.
4. **limitation_text** [HYPOTHESIS]: "Guardrail work itself documents that independently
   aggregated category checks under-estimate risk when unsafe intent is spread across
   multiple weak signals — evidence that naive check-composition leaks — but the proposed
   fix (MLN inference over rule-linked categories) targets homogeneous safety categories
   inside one guardrail, not heterogeneous verifier pairs (tests × judges × analyzers) or
   AND-gates in code/agent settings, and it presupposes the inter-check rules are known."
   `affects_works`: `["[R2-Guard, OpenReview:CkgKSqZbuC]"]`. `limitation_type`: `generalizability`.
5. **limitation_text** [HYPOTHESIS]: "The impossibility result for external filtering is
   proven for a single filter under computational asymmetry; it does not address whether
   stacking several fast checks with disjoint coverage changes the barrier, and its
   adversary hides payloads cryptographically rather than exploiting the interaction of two
   legitimate checks' blind spots." `affects_works`: `["[FilterBarriers, OpenReview:CwoM9T55lG]"]`.
   `limitation_type`: `theoretical`.
6. **limitation_text** [HYPOTHESIS]: "Verifier-hardening and blind-spot-discovery methods
   operate on one verifier at a time: UTRL adversarially maximizes a single test suite's
   discrimination against the current coder, and BiasScope mines one judge's bias inventory
   from its own misjudgments; neither characterizes how two verifiers' independently mapped
   failure surfaces *interact* once their verdicts are combined into a gate."
   `affects_works`: `["[UTRL, OpenReview:VqjNYF9nbP]", "[BiasScope, OpenReview:QGOw6AU8Lp]"]`.
   `limitation_type`: `generalizability`.
7. **limitation_text** [HYPOTHESIS]: "Judge-limit theory bounds the certifiable accuracy of
   a single proxy judge via proxy–truth correlation, but offers no account of how the bound
   composes — whether two judges (or a judge plus a deterministic check) gated by AND/OR
   yield a better or *worse* effective proxy than either alone."
   `affects_works`: `["[JudgeLimits, OpenReview:NO6Tv6QcDs]"]`. `limitation_type`: `theoretical`.

---

## N5 — Challenges

**conflation_check** [HYPOTHESIS]: `true` — the four challenges target distinct obstacles
(non-vacuous formalization + certified construction; combinatorics of existence vs.
prevalence; attribution; emergence vs. shared blind spot). Ids C1–C4 are stable with the
previous digest revision; texts are sharpened.

- **C1** [HYPOTHESIS, sharpened from the seed's minimal experiment]: "Making the phenomenon
  non-vacuous is itself a construction problem: extensionally, the AND/OR of two sound
  acceptors on one fixed task is trivially sound, so the claim only has content when each
  verifier's soundness is certified *relative to its own facet, task variant, and a finite
  certification procedure* (e.g., exhaustive search over a bounded program space, or zero
  false acceptances over a mutant pool). Constructing task pairs where that per-verifier
  certificate demonstrably holds — before any composition — requires a precisely
  operationalized, checkable ground truth."
- **C2** [HYPOTHESIS]: "The space of verifier pairs × composition rules × shortcut
  strategies grows combinatorially, so any finite constructed counterexample establishes
  existence only; estimating how often composition-induced gaps arise in realistic,
  non-adversarially-constructed verifier stacks requires a separately designed sampling and
  budget-matching protocol, not more counterexamples."
- **C3** [HYPOTHESIS]: "Attribution: a shortcut found against the composed gate must be
  traced to the composition step rather than to an undetected latent bug in A or B alone —
  which demands that the single-gate certificates and the composed-gate attack be run under
  matched adversarial budgets, else the 'emergent' gap is an artifact of unequal search
  effort."
- **C4** [HYPOTHESIS]: "Emergence vs. coincidence: a candidate that both verifiers happen to
  independently miss (shared blind spot, a union-of-blind-spots event) is conceptually
  different from one that arises specifically because composition changes the solver's
  feasible/optimal region (e.g., B's constraint pushes solutions off the distribution on
  which A's soundness was certified). Telling these apart requires characterizing each
  verifier's failure surface independently before composing them."

---

## N6 — Methodology

### overview
[HYPOTHESIS]: "A two-stage measurement-plus-demonstration study.
**Stage 0 (pilot = the seed's minimal experiment):** hand-construct 3–5 matched task pairs
over small Python functions with a bounded solution DSL. For each task, verifier A is an
input–output unit-test suite and verifier B is a second-facet check (a resource/style static
check, a property-based check, or an LLM judge). Certify A and B individually sound on their
single-verifier task variants by exhaustive enumeration of the bounded program space plus
mutation-based differential testing (M2). Then build the AND- and OR-composed variants and
run a budget-matched adversarial search (M3) for a candidate that the composed gate accepts
but that fails the held-out differential ground truth — e.g., an OR-gate whose weaker branch
admits a degenerate solution the stronger branch would reject, or an AND-gate whose
resource constraint (B) forces solutions into a lookup-table region where A's finite test
suite loses discrimination. Deliverable: existence certificates for composition-induced
shortcuts, per the seed's 单检查无捷径/组合后有捷径 contrast.
**Stage 1 (scale-up):** systematize over ~200 tasks drawn from EvalPlus-style benchmarks
and a grid of verifier-pair types (unit tests × static analysis × property checks × LLM
judge × execution-free reward model), generate matched variants with M1, replace exhaustive
certification with budget-stamped certification (no shortcut found at budget B_cert), attack
every single and composed gate with identical budgets, and estimate gap rates. M4 classifies
every discovered shortcut and regresses shortcut incidence on a measured
coverage-complementarity score (overlap of the two verifiers' mutant-kill sets)."

### key_components
- **M1 — Task-pair generator** [HYPOTHESIS]: "Programmatically constructs matched tuples
  ⟨task, A-only variant, B-only variant, AND variant, OR variant⟩ over a shared task and
  fixed ground truth (reference solution + ≥10^4-input differential corpus, EvalPlus-style
  test amplification), with **per-variant certification spaces**: the composed variants'
  candidate space extends each single variant's space by exactly the constructs the added
  gate makes reachable, per an extension rule fixed in the manifest before certification
  (see paper.md Step 5 — over one shared space, emergent shortcuts are provably impossible;
  that degenerate configuration is reserved as the B0-P placebo arm). Granularity: one
  tuple per task × verifier-pair type; pilot uses a bounded program DSL (≤ fixed AST
  size/opcode budget) so each variant's candidate space is enumerable."
- **M2 — Single-verifier soundness certifier** [HYPOTHESIS]: "Certifies 'no shortcut passes
  A alone' at a stated strength: pilot — exhaustive enumeration of the bounded DSL,
  asserting every A-accepted candidate agrees with the reference on the full differential
  corpus; scale-up — a mutant pool (≥10^3 first-order/higher-order mutants per task via
  mutation tooling) plus an **independent certification searcher** (a different model,
  prompt scaffold, and seed family from M3's comparison attacker — certifying gates against
  the very attacker later used in the comparison would make FAR(single)≈0 by selection and
  bake in the headline) run against the single gate at budget B_cert, with zero unsound
  acceptances required. Output: a machine-checkable certificate with its budget stamped
  (per C1/C3)."
- **M3 — Adversarial shortcut search** [HYPOTHESIS]: "A budget-matched attacker applied
  identically to single and composed gates: (i) enumeration/CEGIS over the bounded DSL in
  the pilot; (ii) an LLM red-team agent (fixed model, fixed prompt scaffold, N=500 attempts
  per gate) that receives the gate's verdicts as feedback, in the scale-up. Success
  criterion: candidate accepted by the target gate but failing the held-out differential
  corpus. Discovery rates are reported per budget so single vs. composed gates are
  comparable."
- **M4 — Composition-gap classifier** [HYPOTHESIS]: "Labels each discovered shortcut by (a)
  an ablation triple — does it pass A's single gate? B's single gate? the composed gate? —
  with 'emergent' defined as composed-pass ∧ both-single-fail(on their own variants); and
  (b) a structural taxonomy {OR-weak-branch, AND-constraint-displacement (B pushes solutions
  off A's certified distribution), facet-split (each verifier certifies a facet, conjunction
  mistaken for full-task certification), threshold-interaction}. Coverage complementarity
  between A and B is measured as 1 − Jaccard overlap of their mutant-kill sets on the shared
  mutant pool."

### challenge_arguments
- `challenge_id="C1"`, `mechanism_components=["M1", "M2"]` [HYPOTHESIS]: "M1's bounded-DSL
  task construction plus M2's exhaustive/mutation-based certificates operationalize
  per-verifier soundness as a finite, checkable property — exactly the 单检查无捷径 control
  condition the seed requires — and make the non-vacuity explicit by stamping what each
  certificate is relative to (facet, variant, budget)."
- `challenge_id="C2"`, `mechanism_components=["M1", "M3"]` [HYPOTHESIS]: "The claim is
  staged: Stage 0 needs only one convincing counterexample family per composition rule
  (existence), while Stage 1's fixed task sample, verifier-pair grid, and budget-matched
  M3 attacks convert 'how often' into an estimable gap rate instead of an open-ended
  combinatorial search."
- `challenge_id="C3"`, `mechanism_components=["M2", "M3"]` [HYPOTHESIS]: "Because M3
  attacks single gates at the same budget M2 used to certify them, any composed-gate
  shortcut discovered within budget is attributable to the composition step, not to
  unequal search effort or a latent single-verifier bug."
- `challenge_id="C4"`, `mechanism_components=["M4"]` [HYPOTHESIS]: "M4's ablation triple
  separates shared-blind-spot passes (some single gate also fooled) from emergent gaps
  (both single gates hold), and its mutant-kill-set overlap measure turns 'complementary
  blind spots' from a metaphor into a per-pair covariate for the RQ_INF_1 regression."

### unaddressed_challenges
[HYPOTHESIS]: `["C2"]` — Stage 1 estimates gap rates only within the sampled benchmark
tasks and verifier-pair grid; prevalence in deployed, arbitrarily heterogeneous pipelines
(≥3 checks, weighted/thresholded aggregation) remains out of scope and is flagged in N10.

### feasibility [HYPOTHESIS]
- **Pilot:** 3–5 task pairs × 2 composition rules; exhaustive DSL enumeration ≤10^7
  candidates/task (CPU-only, hours); ~2 person-weeks of construction effort; no GPU.
- **Scale-up:** ~200 tasks × ~6 verifier-pair types × 5 gates (A, B, AND, OR, + one
  3-check condition) × 500 attacker attempts = **3×10^6 attacker LLM calls** (corrects an
  earlier 3×10^5 arithmetic slip: 200×6×5×500), plus the 10× single-gate re-attacks of every
  emergent-labeled shortcut and 3-of-3 verdict-stability calls on LLM-verifier pair types
  (order 10^6 judge calls) — upper-mid API cost class (~$10k–$30k at small-model prices);
  mutation certification ≈ 200 × 10^3 mutants × 10^4 differential inputs, embarrassingly
  parallel CPU work (~10^3 CPU-hours). No training runs required — the UTRL-style hardened
  arm and the execution-free-RM verifier type are instantiated training-free per paper.md
  E4 (iterative adversarial test augmentation; released RM checkpoint or prompted proxy);
  annotator effort limited to adjudicating ~100 flagged shortcuts (~20 hours).
- **Single biggest feasibility risk:** M2's soundness certificates outside the exhaustive
  pilot are only "no shortcut found at budget B_cert" — one later-found single-gate
  shortcut voids a pair's 'emergent' label. **Mitigation:** anchor all headline existence
  claims (RQ1) exclusively in the exhaustively certified pilot DSL; in the scale-up, report
  emergent-gap rates as a function of B_cert and re-verify every emergent-labeled shortcut
  by extending the single-gate attack budget 10× before counting it.

---

## N7 — Contributions

- **CO1** [HYPOTHESIS], `contribution_type="empirical_finding"`, `is_testable=true`,
  `has_rq=true`: "A constructive demonstration, with machine-checkable per-verifier
  soundness certificates, that composing two individually certified-sound verifiers via
  AND or OR does not preserve soundness in the realistic (facet-relative,
  budget-relative) regime — an emergent shortcut can pass the composed gate that neither
  component admits alone."
- **CO2** [HYPOTHESIS], `contribution_type="technical_artifact"`, `is_testable=true`,
  `has_rq=true`: "A reusable audit procedure and task-pair suite (generator M1 + certifier
  M2 + budget-matched attacker M3) that pipeline designers can run against their own
  verifier stacks to estimate the composed gate's false-acceptance behavior."
- **CO3** [HYPOTHESIS], `contribution_type="conceptual_framework"`, `is_testable=true`,
  `has_rq=true`: "A taxonomy of structural conditions under which composition-induced
  shortcuts arise (OR-weak-branch, AND-constraint-displacement, facet-split,
  threshold-interaction), with coverage complementarity — measured as mutant-kill-set
  overlap — as a quantitative warning signal."

---

## N8 — Research Questions

- **RQ1** [GIVEN, near-verbatim restatement of the seed's 核心问题], `id="RQ1"`,
  `rq_source="explicit"`: "Two individually sound verifiers — does their conjunctive (AND)
  or disjunctive (OR) composition remain sound? Does composition open a shortcut that does
  not exist for either individual check?"
  `evaluates_mechanisms`: `["M1","M2","M3"]`. `addresses_challenges`: `["C1","C3"]`.
  `tests_contributions`: `["CO1","CO2"]`.
  `answered_by_experiment`: "Pilot: exhaustively certified bounded-DSL task pairs; for each
  composition rule, search the full candidate space of the composed variant for a
  gate-accepted, ground-truth-failing candidate. Existence is decided exactly (the space is
  enumerated), so the pilot answer is binary per task pair."
- **RQ_INF_1** [HYPOTHESIS, inferred from the minimal experiment's second clause about
  出现条件 (conditions of appearance)], `id="RQ_INF_1"`, `rq_source="inferred"`: "Under what
  structural conditions do composition-induced shortcuts appear — specifically, does the
  emergent-gap rate increase with coverage complementarity (1 − Jaccard overlap of the two
  verifiers' mutant-kill sets), and which taxonomy classes dominate for AND vs. OR gates?"
  `evaluates_mechanisms`: `["M4"]`. `addresses_challenges`: `["C4"]`.
  `tests_contributions`: `["CO3"]`.
  `answered_by_experiment`: "Classify every discovered shortcut with M4's ablation triple
  and taxonomy; logistic regression of per-(task, verifier-pair) emergent-gap incidence on
  the complementarity score, controlling for task difficulty and gate type."
- **RQ_INF_2** [HYPOTHESIS, added for the scale-up stage], `id="RQ_INF_2"`,
  `rq_source="inferred"`: "How often do composition-induced gaps arise beyond hand
  construction — at what rate does a budget-matched adversary find emergent shortcuts
  across benchmark tasks and a realistic verifier-pair grid, per composition rule?"
  `evaluates_mechanisms`: `["M1","M3","M4"]`. `addresses_challenges`: `["C2","C3"]`.
  `tests_contributions`: `["CO1","CO2"]`.
  `answered_by_experiment`: "Stage-1 sweep: ~200 tasks × ~6 verifier-pair types; attack A,
  B, AND, OR gates with identical budgets (N=500 attempts); compare composed-gate vs.
  strictest-single-gate false-acceptance on the same tasks."

- **datasets** [HYPOTHESIS]: `names=["HumanEval+ (EvalPlus-amplified tests)", "MBPP+
  (EvalPlus-amplified tests)", "LiveCodeBench (post-cutoff subset, contamination control)",
  "BigCodeBench (multi-constraint tasks for the AND-gate conditions)", "Constructed
  bounded-DSL pilot suite (released as part of CO2)"]` — chosen because EvalPlus-style
  amplified test corpora provide exactly the held-out differential ground truth M2/M3
  require, and BigCodeBench tasks natively carry multiple constraints per task.
- **baselines** [HYPOTHESIS] (gate configurations under identical attack budgets, anchored
  in N3 systems): `names=["Verifier A alone (unit-test gate)", "Verifier B alone
  (static/property/judge gate)", "Naive AND gate", "Naive OR gate", "UTRL-style
  adversarially hardened single test suite [UTRL, OpenReview:VqjNYF9nbP] (tests whether
  hardening one check beats adding a second)", "SWE-RM-style execution-free RM as verifier
  B instance [SWE-RM, OpenReview:H9wMe1G76j]", "R2-Guard-style rule-linked aggregation
  instead of naive AND [R2-Guard, OpenReview:CkgKSqZbuC] (tests whether structured
  composition closes the gap)"]`.
- **metrics** [HYPOTHESIS], with definitions:
  `names=["False-acceptance rate FAR(gate) = P(candidate accepted ∧ fails differential
  ground truth) over attacker-found candidates per budget", "Emergent-gap rate = fraction
  of (task, pair) cells with ≥1 shortcut passing the composed gate while both single gates
  hold at equal budget", "Attack success@budget = P(attacker finds ≥1 accepted-but-wrong
  candidate within N attempts)", "Coverage complementarity = 1 − Jaccard(kill-set_A,
  kill-set_B) over the shared mutant pool", "Certificate strength B_cert = attack budget at
  which the single-gate certificate was established"]`.
- **analysis_plan** [HYPOTHESIS]: "Sample size: 200 tasks × 6 verifier-pair types (1,200
  cells; pilot adds 5 exhaustively decided pairs). Primary test: per verifier-pair type,
  paired comparison of unsound-acceptance indicators between the composed gate and the
  strictest single gate on the same tasks via McNemar's exact test; α=0.05 with
  Holm–Bonferroni correction across the 6 pair types × 2 composition rules (12 primary
  comparisons); report odds ratios with 95% CIs. Secondary: logistic regression of
  emergent-gap incidence on coverage complementarity (RQ_INF_1), Wald test on the
  complementarity coefficient, same α. Expected effect directions: OR gates show
  FAR(OR) ≥ max(FAR(A), FAR(B)) with strict increase on weak-branch pairs;
  AND gates show a nonzero emergent-gap rate concentrated in constraint-displacement
  pairs; complementarity coefficient positive. Power note: with 200 tasks per cell,
  McNemar detects discordant-pair asymmetries of ≥7 pp at 0.8 power."

---

## N9 — Results

**All entries [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].** No experiment has been run;
nothing here is a reported number. `evidence_strength="missing"` and `rq_answered=false`
throughout; each result carries an explicit falsification condition.

1. **rq_id**: `RQ1`. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "For at least one
   exhaustively certified pilot task family per composition rule, the composed gate accepts
   a candidate that fails the differential ground truth, while both single-verifier
   variants are certified shortcut-free over the full enumerated candidate space — i.e.,
   facet-relative soundness is not preserved by AND/OR composition."
   **result_type**: `theoretical_proof` (existence by exhaustive construction; scales to
   `quantitative` in Stage 1). **evidence_strength**: `missing`. **rq_answered**: `false`.
   **FALSIFICATION CONDITION**: "Refuted if, across all constructed pilot families and the
   fully enumerated candidate spaces, every composed-gate-accepted candidate also passes
   the differential ground truth — composition would be sound in the entire constructed
   regime, and the paper's central claim would not hold."
2. **rq_id**: `RQ_INF_1`. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "Emergent-gap
   incidence increases with coverage complementarity (positive, significant logistic
   coefficient); OR-gate shortcuts concentrate in the weak-branch class and AND-gate
   shortcuts in the constraint-displacement class (B's constraint pushes solutions off the
   distribution on which A's soundness was certified)."
   **result_type**: `quantitative`. **evidence_strength**: `missing`. **rq_answered**: `false`.
   **FALSIFICATION CONDITION**: "Refuted if the complementarity coefficient is
   indistinguishable from zero or negative at α=0.05, or if discovered shortcuts scatter
   across taxonomy classes with no dependence on gate type — the structural
   'complementary blind spot' account would then not explain composition failure."
3. **rq_id**: `RQ_INF_2`. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "Under matched
   attack budgets on benchmark tasks, composed gates show strictly higher unsound
   acceptance than the strictest single gate (McNemar significant after Holm correction)
   for OR gates on most verifier-pair types, and a small but nonzero emergent-gap rate for
   AND gates concentrated in test-suite × resource/style-constraint pairs; R2-Guard-style
   structured aggregation reduces but does not eliminate the gap."
   **result_type**: `quantitative`. **evidence_strength**: `missing`. **rq_answered**: `false`.
   **FALSIFICATION CONDITION**: "Refuted if, at equal budgets, composed-gate unsound
   acceptance is statistically indistinguishable from (or lower than) the strictest single
   gate across all verifier-pair types — composition would then behave at least as safely
   as its strictest component in realistic stacks, confining the pilot's counterexamples to
   adversarial curiosities."

---

## N10 — Threats / Self-Limitations

All [HYPOTHESIS] — anticipated threats for this constructed-measurement design, stated
pre-registration-style with planned mitigations; no authored Threats section exists, so
nothing here is `extracted`.

- **t1**, `category="construct"`: "'Soundness' is operationalized as a bounded certificate
  (exhaustive only in the pilot DSL; budget-stamped elsewhere) against a differential-test
  ground truth that may itself be incomplete — so 'emergent shortcut' partially measures
  the certification instrument, not only the phenomenon." `mitigation` [HYPOTHESIS]:
  "Anchor headline existence claims in the exhaustively enumerated pilot; amplify ground
  truth with EvalPlus-style test generation; human-adjudicate a 100-shortcut sample to
  confirm the candidates genuinely fail task intent."
- **t2**, `category="internal"`: "Asymmetric search effort could manufacture 'emergence':
  if the attacker spends more effective budget on composed gates than the certifier spent
  on single gates, composed-only shortcuts appear artifactually." `mitigation`
  [HYPOTHESIS]: "Identical attacker, prompts, and attempt budgets for every gate;
  re-verify each emergent-labeled shortcut by extending the single-gate attack budget 10×
  before counting it (per M2/M3 protocol)."
- **t3**, `category="external"`: "Two-verifier Boolean gates over Python function-synthesis
  tasks may not generalize to deployed pipelines with ≥3 heterogeneous checks, non-Boolean
  aggregation (voting, weights, thresholds), or non-code domains (safety judges over
  dialogue, human-in-the-loop review)." `mitigation` [HYPOTHESIS]: "Include one 3-check
  condition and one thresholded-aggregation condition in the Stage-1 grid; scope all claims
  to the studied gate class and flag the rest as untested."
- **t4**, `category="conclusion"`: "1,200 cells × 12 primary comparisons invite
  multiple-comparison false positives, and existence results (pilot) say nothing about
  prevalence; conflating the two overstates the warning." `mitigation` [HYPOTHESIS]:
  "Holm–Bonferroni across primary comparisons, CIs on all rates, and strict separation of
  existence claims (pilot, exhaustive) from rate claims (Stage 1, budgeted) in reporting."
- **t5**, `category="construct"`: "LLM-based verifiers (judge, execution-free RM) are
  stochastic, so a 'gate verdict' is itself a random variable; unsound acceptances could
  reflect sampling noise rather than a stable blind-spot interaction." `mitigation`
  [HYPOTHESIS]: "Fix temperature/seeds where the API allows, require k-of-n verdict
  stability (e.g., 3-of-3 accepts) before counting a pass, and report verdict-flip rates."

**Status**: `PARTIAL` (populated proactively as anticipated threats). **absence_comment**:
- `what_missing`: "No paper has been written, so there is no author-stated Threats to
  Validity / Limitations section to extract from."
- `why_matters`: "A reviewer cannot yet tell which of these anticipated threats the
  eventual authors will acknowledge, downplay, or actually mitigate."
- `implication`: "Treat t1–t5 as a pre-registration checklist binding the study design
  (budget matching, exhaustive pilot, correction procedures), not as reported limitations."

---

## N11 — Artifacts

**Status**: `NOT_FOUND`. `artifacts=[]`. `has_code=false`, `has_data=false`,
`has_model=false`. [PLACEHOLDER] throughout — nothing has been built or released.

**absence_comment**:
- `what_missing`: "No code repository, dataset, model, or demo exists for this idea — it is
  a research-planning seed; the task-pair suite, certifier, and attacker described in N6
  (CO2) are all prospective."
- `why_matters`: "Nothing can yet be reproduced, inspected, or reused; the audit procedure
  promised in CO2 is the artifact the field would actually consume."
- `implication`: "Revisit N11 once the pilot runs: the bounded-DSL suite with its
  exhaustive certificates (dataset), the M1–M4 pipeline (code_repo), and per-gate attack
  logs (supplement) are the expected entries."

---

## N12 — Contribution Type

**value** [HYPOTHESIS]: `empirical`

**rationale** [HYPOTHESIS]: "The seed frames the payoff as a counter-intuitive *finding* —
'反直觉结论若成立，对所有多重校验管线是普适警告' — and the strengthened design keeps that
shape: like the metric-choice mirage study it structurally imitates, the work measures and
demonstrates a property of *existing* verification practice (composition of checks that
corpus systems such as [RewardChain, OpenReview:ZumVIktGbt], [FAPO, OpenReview:jhqqoimoWt],
[SWE-RM, OpenReview:H9wMe1G76j], and [R2-Guard, OpenReview:CkgKSqZbuC] already deploy)
via constructed counterexamples, budget-matched attacks, and statistical rate comparisons —
rather than shipping a new system or benchmark as the primary claim. The pilot's exhaustive
constructions function as illustrative scaffolding for the empirical predictions (RQ_INF_1,
RQ_INF_2), and the task-pair suite (CO2) is a supporting artifact, not the headline —
so `empirical` fits over `benchmark`/`tool`/`theoretical`." `source`: `hypothesis`.

---

## Claims

1. **text** [HYPOTHESIS]: "In the facet-relative regime that real pipelines actually occupy
   — each verifier certified sound for its own checked property, on its own task variant, at
   a finite budget — AND/OR composition of two certified-sound verifiers does not preserve
   soundness: an emergent shortcut absent from either component can appear in the composed
   gate." **evidence**: `[{type: "argument", text: "Derived from the seed's core question
   and minimal experiment, made non-vacuous by the facet-relative soundness
   operationalization (C1/M2)", source: "hypothesis", location: null}]`.
2. **text** [HYPOTHESIS]: "Composition-induced shortcuts arise preferentially where the two
   verifiers' failure surfaces are complementary — measurable in advance as low mutant-kill-set
   overlap — with OR gates failing through their weaker branch and AND gates by displacing
   solutions off the distribution on which the other verifier was certified." **evidence**:
   `[{type: "argument", text: "Structural mechanism inferred to explain why an existence
   result would recur across task families; operationalized as the RQ_INF_1 regression",
   source: "hypothesis", location: null}]`.
3. **text** [GIVEN, near-verbatim from seed, framed as the paper's claimed stake rather
   than a demonstrated fact]: "If the counter-intuitive conclusion holds, it constitutes a
   general warning applicable to any multi-stage verification/reward pipeline (unit tests +
   linters, outcome + process verifiers, safety + task-success checks, multiple LLM-judge
   votes), not just the constructed example domain." **evidence**: `[{type: "citation",
   text: "反直觉结论若成立，对所有多重校验管线是普适警告", source: "given", location:
   "seed README, 最小实验"}]`.
4. **text** [HYPOTHESIS]: "Hardening a single check (UTRL-style adversarial test
   strengthening) and adding a second check are not interchangeable defenses: the
   comparison in RQ_INF_2's baseline grid is predicted to show cases where a hardened
   single gate is safer than a naive two-check gate — inverting the 'more checks = safer'
   heuristic." **evidence**: `[{type: "argument", text: "Follows from Claims 1–2 if
   composition itself is the gap-opening operation; directly testable via the
   [UTRL, OpenReview:VqjNYF9nbP] baseline condition", source: "hypothesis", location: null}]`.
5. **text** [PLACEHOLDER]: "Because the hypothesized shortcuts are reachable only via
   active budget-matched search (not passive inspection), pipelines audited by checklist
   review alone would systematically under-detect this risk — confirmable only once the
   attacker's discovery rate is measured against passive-inspection baselines."
   **evidence**: `[]` (no evidence possible yet — the claim flags its own unverifiable status).

---

## Self-verification pass

- **ID consistency (EX-09)**:
  - N4 `affects_works` values — `[CorrelatedProxies, OpenReview:msEr27EejF]`,
    `[RewardChain, OpenReview:ZumVIktGbt]`, `[FAPO, OpenReview:jhqqoimoWt]`,
    `[SWE-RM, OpenReview:H9wMe1G76j]`, `[R2-Guard, OpenReview:CkgKSqZbuC]`,
    `[FilterBarriers, OpenReview:CwoM9T55lG]`, `[UTRL, OpenReview:VqjNYF9nbP]`,
    `[JudgeLimits, OpenReview:NO6Tv6QcDs]`, `[BiasScope, OpenReview:QGOw6AU8Lp]` — each
    appears verbatim as an N3 `citation_key`; all 9 N3 keys are cited by ≥1 limitation.
  - N6 `challenge_arguments` reference C1–C4 (all in N5) and M1–M4 (all in
    N6.key_components); `unaddressed_challenges=["C2"]` ⊆ {C1,C2,C3,C4}.
  - N8: RQ1 → M1,M2,M3 / C1,C3 / CO1,CO2; RQ_INF_1 → M4 / C4 / CO3; RQ_INF_2 →
    M1,M3,M4 / C2,C3 / CO1,CO2 — every referenced C/M/CO id exists (C1–C4, M1–M4, CO1–CO3).
  - N9 `rq_id`s {RQ1, RQ_INF_1, RQ_INF_2} all exist in N8. **All checks pass.**
- **Trust-tag discipline**: seed-verbatim content tagged [GIVEN]; corpus-grounded related
  work tagged [GROUNDED:corpus]; all predictions [HYPOTHESIS]; all unknowables
  [PLACEHOLDER]; no fabricated numbers anywhere in N9 (directions + falsification
  conditions only, `evidence_strength="missing"`, `rq_answered=false` throughout).
- **Absence comments**: all non-FOUND nodes (N10 PARTIAL, N11 NOT_FOUND) carry full 3-part
  absence comments; N3 is FOUND with an explicit residual-gap note defining the novelty claim.
- **Section completeness (EX-11)**: N0–N12 all present, plus Claims.
- **N12 enum check (EX-10)**: `empirical` is a legal enum value; rationale is
  non-circular (argues from result shape and artifact role, citing the corpus systems whose
  practice is being measured).
