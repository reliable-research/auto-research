# Digest: How Many Prompts Break per Upgrade? Contract Breakage Rates for Structured-Output Pipelines

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet for this idea. Every
> field below is tagged **[GIVEN]** (verbatim/near-verbatim from the seed topic file), **[HYPOTHESIS]**
> (a reasoned, falsifiable prediction grounded in the seed + real adjacent literature + standard
> practice for this kind of study — NOT a fact), or **[PLACEHOLDER]** (genuinely unknowable until
> the work is actually done — never invented). Related works drawn from the local OpenReview
> corpus (`topics/corpus/ideas.jsonl`) are additionally tagged **[GROUNDED:corpus]**: the paper
> is real and its approach_summary is grounded in its actual motivation/method text, but its
> placement in this future paper's related-work section is this document's judgment call.
>
> Seed source: `topics/B3.4_how_many_prompts_break_per_upgrade_contract_breakage_rates_for_s/README.md`
> Topic code: **B3.4** · Label: **[证据] (Evidence)** · Parent topic: **B3. 跨版本行为漂移 / 纵向审计**
> (Cross-version behavioral drift / longitudinal audit) [GIVEN]

---

## N0 Metadata

- **title** [GIVEN]: "How Many Prompts Break per Upgrade? Contract Breakage Rates for
  Structured-Output Pipelines"
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper has been written; authorship is
  unknowable.
- **abstract** [HYPOTHESIS] (drafted, not real — synthesized from the seed's core question +
  minimal experiment + the upgraded N6/N8 design below; explicitly a draft of what such a
  paper's abstract *might* say):
  > "Production systems built on LLMs routinely depend on structured-output contracts —
  > JSON schemas, formatting conventions, and few-shot prompt templates — that assume the
  > underlying model's behavior is stable. Provider-side model upgrades, however, are
  > frequent and often only loosely documented, raising the question of how much of this
  > contracted behavior survives a version jump. We construct a library of production-style
  > contracts spanning JSON-schema conformance (sourced from SchemaStore and
  > JSONSchemaBench), verifiable formatting conventions (IFEval-style checkable rules), and
  > few-shot templates mined from real user–LLM conversations (WildChat), and measure the
  > fraction that newly fail ('break') across successive pinned versions of both closed
  > dated API snapshots and open-weight model families. To separate upgrade-induced
  > breakage from ordinary sampling variance, we compare every breakage rate against a
  > within-version split-half resampling noise floor. We further fit a fragility model
  > relating contract-level features — schema depth, constraint density, few-shot example
  > count, instruction length — to breakage probability, and evaluate whether
  > constrained-decoding and prompt-recompilation mitigations reduce breakage. We report
  > per-upgrade breakage rates by contract type and identify which contract characteristics
  > are most associated with fragility, offering downstream engineering teams a basis for
  > prioritizing regression testing before adopting a new model version."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"SE"` — the study's unit of analysis (production prompt
  contracts, regression testing across upgrades) and its intended audience (engineering
  teams maintaining LLM-integrated software) place it closer to empirical software
  engineering (ICSE/FSE-style measurement study) than to core NLP model-behavior research,
  though it draws heavily on NLP evaluation methodology.
- **Status**: PARTIAL. `absence_comment`: {"what_missing": "No authors or verbatim abstract
  exist because no paper has been written for this idea yet.", "why_matters": "N0 identity
  fields are referenced by every downstream tool (reviewer, writer agents) as the paper's
  canonical identity, so a reader must not mistake the drafted abstract above for a real
  quoted one.", "implication": "Treat title and area as the only load-bearing facts here;
  treat authors/abstract/doi/arxiv_id as placeholders to be filled in only once the paper
  is actually written and published."}

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS] (full predicate constructed from the seed's core question):
  "measure, across successive released versions of one or more production LLM APIs and
  open-weight model families, what fraction of a fixed library of production-style
  structured-output contracts (JSON-schema conformance targets, machine-checkable
  formatting conventions, and few-shot prompt templates) that passed under the prior
  version newly fail under the new version — after subtracting a within-version resampling
  noise floor — and identify which contract-level features (e.g., schema nesting depth,
  constraint density, few-shot example count) predict this breakage."
  - Self-check: (1) kind of task — a longitudinal measurement/audit study; (2) domain — LLM
    version upgrades affecting structured-output prompt contracts; (3) outcome shape — a
    per-upgrade, noise-adjusted breakage-rate statistic plus a validated set of fragility
    predictors. All three land.
- **inputs** [HYPOTHESIS]:
  - A constructed library of production-style contracts: JSON schemas, output-format
    conventions (delimiter/casing/length rules), and few-shot prompt templates, each paired
    with an input distribution and a machine-checkable acceptance predicate.
  - Sequences of successive, individually addressable LLM versions: dated closed-API
    snapshots and permanently archived open-weight checkpoints.
  - A deterministic pass/fail validator per contract (schema validator, rule checker,
    template-conformance checker).
- **outputs** [HYPOTHESIS]:
  - A per-version-transition breakage rate (fraction of previously-passing contracts that
    now fail), overall and per contract type, reported alongside its within-version noise
    floor.
  - A fitted fragility model (odds ratios + predictive AUC) over contract features.
  - An estimate of how much breakage two mitigations (constrained decoding; per-version
    prompt recompilation) remove.
- **constraints** [GIVEN] (from the seed's minimal experiment, near-verbatim intent): the
  study requires a constructed contract library with well-defined ground truth for
  pass/fail (JSON schema validity, format-convention adherence) so that breakage is
  objectively separable from mere output variation — i.e., "构造模拟生产契约库（JSON schema、
  格式约定、few-shot 模板），逐版本测破坏率与脆弱性预测因子" (construct a simulated production
  contract library — JSON schema, format conventions, few-shot templates — and measure
  breakage rate and fragility predictors version by version).
- **Status**: PARTIAL (objective/inputs/outputs are inferred, not stated in full formulation
  form in the one-line seed). `absence_comment`: {"what_missing": "The seed gives only a
  one-sentence core question and one-sentence minimal experiment, not a full problem
  formulation with explicit inputs/outputs/constraints.", "why_matters": "Without an
  explicit formulation, a reviewer cannot yet judge whether the contract library's
  pass/fail criterion is well-specified enough to make 'breakage' a clean, non-subjective
  measurement.", "implication": "Treat inputs/outputs above as the most conservative
  reconstruction consistent with the seed; a real paper may narrow or extend the contract
  types studied."}

---

## N2 Motivation

**motivations** (reconstructed from the parent-topic framing "B3. 跨版本行为漂移 / 纵向审计" —
cross-version behavioral drift / longitudinal audit — now partially grounded in real
adjacent papers; no invented statistics) [HYPOTHESIS]:

- "Production software increasingly embeds LLM calls behind structured-output contracts
  (JSON schemas, format conventions, few-shot templates) that downstream code parses
  programmatically; when a provider upgrades the underlying model, any silent shift in the
  model's tendency to honor those contracts can break the downstream code without any
  change on the application side." — source: HYPOTHESIS, evidence: [{type: "citation",
  text: "[DSPy, OpenReview:sY5N0zY5Od] motivates its entire programming model with the
  observation that LM pipelines 'are typically implemented with hand-written prompt
  templates, making them brittle', and that such prompts 'do not transfer cleanly across
  tasks or models'.", location: null}].
- "Model endpoints demonstrably change under users' feet: [LogProbTracking,
  OpenReview:hFxivbAgVP] frames continuous detection of endpoint response-distribution
  change as an open monitoring problem precisely because 'LLM APIs are expected to provide
  stable behavior over time, yet users typically access them only as black-box services',
  and [ChatGPTDrift, arXiv:2307.09009] documented substantial behavior shifts between
  successive GPT snapshots. What remains unmeasured is the *downstream* consequence: the
  rate at which production-style contracts break per upgrade — teams currently learn about
  breakage reactively, after their own production incidents." — source: HYPOTHESIS,
  evidence: [{type: "citation", text: "See N3 entries for both works.", location: null}].
- "This sits within a broader need (per the parent topic B3, cross-version behavioral
  drift / longitudinal audit) for systematic, repeated measurement of how LLM behavior
  drifts release over release, rather than one-off snapshot evaluations — the same
  methodological move [LAMDA, OpenReview:1FnCrZtBNQ] makes for malware concept drift."
  — source: HYPOTHESIS, grounded in parent_topic field of the seed [GIVEN pointer,
  HYPOTHESIS elaboration], evidence: [].
- **Status**: PARTIAL. `absence_comment`: {"what_missing": "No motivating statistics
  specific to contract breakage (e.g., X% of production incidents attributable to model
  upgrades) exist because the paper hasn't been written and no such measurement exists in
  the surveyed corpus.", "why_matters": "Motivation claims of this kind normally carry
  citations or data in a real paper; here only the premise (endpoints drift; templates are
  brittle) is citation-grounded, while the consequence (production breakage rate) is the
  unmeasured gap itself.", "implication": "Do not cite the consequence claims as fact in a
  literature review; they are the planning hypotheses this study would test."}

---

## N3 Related Works

Grounding procedure: seven keyword searches over the local corpus
`topics/corpus/ideas.jsonl` (11,683 OpenReview papers) from three angles — the mechanism
(structured output / constrained decoding / instruction constraints), the failure mode
(prompt brittleness / model updates / backward compatibility / drift), and the evaluation
methodology (longitudinal benchmarks / API monitoring). Full motivation+method texts of the
nine best hits were read. Entries below tagged **[GROUNDED:corpus]** are real corpus
papers; one entry is a non-corpus canonical paper, clearly marked.

- **[ChatGPTDrift, arXiv:2307.09009]** — Chen, Zaharia & Zou, "How Is ChatGPT's Behavior
  Changing over Time?". Evaluates the March-2023 and June-2023 snapshots of GPT-3.5 and
  GPT-4 on a fixed task suite and documents large, task-dependent behavior and
  format-compliance shifts between snapshots of the "same" service. **[NON-CORPUS —
  canonical; confident it exists (arXiv 2307.09009, later TMLR); the single closest real
  predecessor to this topic and cited as @chen2023chatgptbehavior by the corpus paper
  [LogProbTracking, OpenReview:hFxivbAgVP].]**
  paper_url: https://arxiv.org/abs/2307.09009
- **[LogProbTracking, OpenReview:hFxivbAgVP]** — "Log Probability Tracking of LLM APIs".
  Black-box endpoint monitoring: repeatedly queries an API with a fixed minimal prompt,
  collects top-k first-token logprobs, and applies a nonparametric two-sample test to
  detect shifts in the endpoint's response distribution under production nondeterminism —
  a cheap detector of *whether* a deployed model/serving stack changed. **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=hFxivbAgVP
- **[CoIPO, OpenReview:TUd3c7Vr1z]** — "Towards Self-Robust LLMs: Intrinsic Prompt Noise
  Resistance via CoIPO". Documents (via PromptBench and instruction-robustness studies it
  builds on) that LLMs are highly sensitive to semantics-preserving prompt perturbations,
  and trains intrinsic robustness by aligning label-token logits between paired clean and
  noisy prompts using an inverse-DPO objective. **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=TUd3c7Vr1z
- **[TARE, OpenReview:YEBDvqsniH]** — "Beyond Magic Words: Sharpness-Aware Prompt Evolving
  for Robust Large Language Models with TARE". Argues prompt optimizers converge to prompts
  "whose performance depends heavily on exact wording", and optimizes prompts for
  worst-case loss over a semantic paraphrase neighborhood (a black-box, discrete analogue
  of sharpness-aware minimization). **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=YEBDvqsniH
- **[DSPy, OpenReview:sY5N0zY5Od]** — "DSPy: Compiling Declarative Language Model Calls
  into Self-Improving Pipelines". Replaces brittle hand-written prompt templates with
  declarative signatures, parameterized modules, and metric-driven compilers
  (teleprompters) that re-derive prompts/demonstrations per task and per model — a
  mitigation strategy for the very fragility this topic wants to measure.
  **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=sY5N0zY5Od
- **[RECAST, OpenReview:90tCp2KszA]** — "RECAST: Expanding the Boundaries of LLMs' Complex
  Instruction Following with Multi-Constraint Data". Mines verifiable constraints
  (rule-based programmatic checkers + model-based validators) from instruction–response
  corpora, recombines them into high-constraint-count instructions, and uses per-constraint
  verification as RL reward — building on FollowBench's finding that performance degrades
  as the number of simultaneous constraints grows. **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=90tCp2KszA
- **[AutoIF, OpenReview:cRR0oDFEBC]** — "Self-Play with Execution Feedback: Improving
  Instruction-Following Capabilities of Large Language Models". Generates verifiable
  instructions together with executable verification functions and unit tests (leveraging
  IFEval's insight that many constraints are programmatically checkable), and uses
  execution pass/fail as training supervision — a direct precedent for building automated
  contract validators. **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=cRR0oDFEBC
- **[DiffusionCFG, OpenReview:7Sph4KyeYO]** — "Constrained Decoding of Diffusion LLMs with
  Context-Free Grammars". Guarantees outputs conform to formal structures (programming
  languages, JSON schemas) by grammar-constrained decoding, extending prefix-based
  constrained decoding to diffusion LLMs via CFG–regular-language intersection and
  emptiness checking — the decoding-time-guarantee alternative to prompt-level contracts.
  **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=7Sph4KyeYO
- **[CAR-LoRA, OpenReview:5GimteSrgW]** — "CAR-LoRA: Training Compression-Aware and Robust
  LoRA Adapters for Evolving LLMs". Shows that LoRA adapters trained against one base-model
  configuration degrade when the base model is compressed or updated ("model providers
  periodically release updated checkpoints whose parameters differ from the original
  training version"), and trains a single adapter over a distribution of base-model
  perturbations — version fragility of *weight-space* downstream artifacts.
  **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=5GimteSrgW
- **[LAMDA, OpenReview:1FnCrZtBNQ]** — "LAMDA: A Longitudinal Android Malware Benchmark for
  Concept Drift Analysis". Constructs a 2013–2025, >1M-sample temporally structured
  benchmark with a consistent feature representation and evaluation protocols that simulate
  increasing temporal distance between training and deployment — the methodological
  template for longitudinal drift measurement over software artifacts. **[GROUNDED:corpus]**
  paper_url: https://openreview.net/forum?id=1FnCrZtBNQ

**Status**: PARTIAL. `absence_comment`: {"what_missing": "No paper in the searched corpus
(and, to this document's knowledge, in the wider literature) directly measures
per-version-upgrade breakage *rates* of structured-output prompt contracts or fits
contract-level fragility predictors — the corpus contains endpoint-change detectors
([LogProbTracking, OpenReview:hFxivbAgVP]), input-side prompt-robustness work ([CoIPO,
OpenReview:TUd3c7Vr1z], [TARE, OpenReview:YEBDvqsniH]), and constraint-verification
machinery ([RECAST, OpenReview:90tCp2KszA], [AutoIF, OpenReview:cRR0oDFEBC]), but not the
longitudinal contract-breakage measurement itself.", "why_matters": "This supports the
seed's gap claim while also showing every ingredient of the proposed method (validators,
version monitoring, longitudinal protocol) has a real precedent to build on.",
"implication": "A real paper should anchor its Introduction on [ChatGPTDrift,
arXiv:2307.09009] + [LogProbTracking, OpenReview:hFxivbAgVP] for the drift premise, on
[RECAST, OpenReview:90tCp2KszA]/[AutoIF, OpenReview:cRR0oDFEBC] for validator
construction, and on [LAMDA, OpenReview:1FnCrZtBNQ] for longitudinal protocol design."}

---

## N4 Prior Limitations

**limitations** [HYPOTHESIS] (what the N3 works fail to do relative to this idea's core
question; each defensible from the cited paper's own motivation text or from what its
method demonstrably does not cover; each grounded via `affects_works`):

- "[ChatGPTDrift, arXiv:2307.09009] demonstrates that behavior shifts between two snapshots
  of two models on a general task suite, but it covers a single provider, a single snapshot
  pair, and tasks not designed as production contracts — it yields no per-upgrade breakage
  *rate* over a designed contract library, no per-contract-type decomposition, and no
  fragility predictors." — limitation_type: `generalizability`, affects_works:
  `["[ChatGPTDrift, arXiv:2307.09009]"]`.
- "[LogProbTracking, OpenReview:hFxivbAgVP] detects *that* an endpoint's response
  distribution changed (its own framing: continuous 'detection of whether an endpoint's
  response distribution has changed'), but by design it says nothing about *what breaks
  downstream* — a statistically detectable distribution shift may break 0% or 50% of
  deployed contracts, and the method does not quantify or predict which." —
  limitation_type: `other`, affects_works: `["[LogProbTracking, OpenReview:hFxivbAgVP]"]`.
- "[CoIPO, OpenReview:TUd3c7Vr1z] and [TARE, OpenReview:YEBDvqsniH] study the *input-side*
  perturbation direction — the prompt varies while the model is held fixed. The upgrade
  setting is the exact dual (prompt held fixed, model varies underneath), which neither
  work measures; their robustness scores therefore cannot be read as upgrade-survival
  predictions." — limitation_type: `generalizability`, affects_works:
  `["[CoIPO, OpenReview:TUd3c7Vr1z]", "[TARE, OpenReview:YEBDvqsniH]"]`.
- "[RECAST, OpenReview:90tCp2KszA] and [AutoIF, OpenReview:cRR0oDFEBC] build exactly the
  programmatic constraint-verification machinery a contract validator needs, but both
  deploy it as a *training-time* reward/filter signal evaluated at a single model snapshot;
  neither applies its verifiers longitudinally across successive versions of the same
  model, so constraint-satisfaction drift over upgrades remains unmeasured." —
  limitation_type: `other`, affects_works: `["[RECAST, OpenReview:90tCp2KszA]",
  "[AutoIF, OpenReview:cRR0oDFEBC]"]`.
- "[DiffusionCFG, OpenReview:7Sph4KyeYO] guarantees schema conformance only when the
  deployer controls decoding (token-mask/grammar access at inference time); the common
  production case this topic targets — contracts enforced purely through prompts against a
  black-box API — receives no guarantee from constrained decoding, and the paper does not
  measure how often unconstrained prompt-level contracts are violated, let alone across
  versions." — limitation_type: `usability`, affects_works:
  `["[DiffusionCFG, OpenReview:7Sph4KyeYO]"]`.
- "[DSPy, OpenReview:sY5N0zY5Od] asserts in its own motivation that hand-written prompt
  templates are 'brittle' and 'do not transfer cleanly across tasks or models', and offers
  re-compilation as the fix — but it never quantifies the breakage phenomenon itself (no
  rate, no predictors), so the cost/benefit of recompiling per model version is asserted
  rather than measured." — limitation_type: `other`, affects_works:
  `["[DSPy, OpenReview:sY5N0zY5Od]"]`.
- "[CAR-LoRA, OpenReview:5GimteSrgW] establishes version-fragility for *weight-space*
  downstream artifacts (adapters degrade when base checkpoints evolve) but leaves the
  prompt/contract space — where most production LLM integrations actually live —
  unmeasured." — limitation_type: `generalizability`, affects_works:
  `["[CAR-LoRA, OpenReview:5GimteSrgW]"]`.
- "[LAMDA, OpenReview:1FnCrZtBNQ] provides the longitudinal-drift-benchmark methodology
  (consistent representation, temporally structured evaluation) but for Android malware; no
  analogous temporally structured benchmark exists for LLM contract behavior across model
  versions." — limitation_type: `generalizability`, affects_works:
  `["[LAMDA, OpenReview:1FnCrZtBNQ]"]`.

**grounding_check**: `true` — every limitation above is tied to at least one
`N3.works[].citation_key`, in exactly the same string form.

**Status**: PARTIAL. `absence_comment`: {"what_missing": "These are reasoned limitations
inferred by comparing each real work's actual motivation/method scope (read from the
corpus texts) to the seed's core question, not limitations any of those authors stated
about their own work relative to this topic.", "why_matters": "Per EX-01, inferred
prior-limitations must be flagged as inference, not presented with the same certainty as an
author's own stated related-work critique.", "implication": "A real paper would re-verify
these limitation claims against each cited paper's full published text before asserting
them in an Introduction/Related-Work section."}

---

## N5 Challenges

**challenges** [HYPOTHESIS, tightly derived from the core question — problem-inherent, not
tied to any one prior tool's failure; ids stable from the previous digest revision]:

- **C1**: "Defining an objective, automatable pass/fail ground truth for 'contract
  breakage' is nontrivial: JSON-schema conformance is mechanically checkable, but
  formatting-convention adherence and few-shot template-following admit graded compliance
  (e.g., correct fields but reordered keys; correct list but different bullet glyph), so
  the acceptance predicate must be calibrated against what a real downstream *parser*
  would reject — too strict flags benign variation, too lenient misses real failures."
  source: HYPOTHESIS.
- **C2**: "Provider-side model versions are not always cleanly enumerable or independently
  re-queryable after the fact — closed endpoints can change silently within a named
  snapshot and old snapshots get deprecated — making it hard to attribute an observed
  behavior change to a specific, citable, replicable version transition."
  source: HYPOTHESIS.
- **C3**: "Breakage is confounded with ordinary within-version output variance: a contract
  sampled twice from the *same* version can flip pass/fail under nonzero temperature or
  serving nondeterminism, so any credible upgrade-breakage estimate must be reported as an
  excess over a within-version noise floor, not as a raw flip count."
  source: HYPOTHESIS.
- **C4**: "Identifying fragility *predictors* requires enough contract diversity and enough
  independent version transitions for statistical power, and contract features are mutually
  correlated (deep schemas tend to have more fields and more constraints), so naive
  per-feature correlations are confounded; a well-powered multivariate design with grouped
  cross-validation is required for any feature-level claim." source: HYPOTHESIS.

**conflation_check**: `true` — C1–C4 target genuinely distinct obstacles (ground-truth
definition, version attribution, noise confound, statistical power/collinearity).

**Status**: PARTIAL. `absence_comment`: {"what_missing": "No paper text exists to confirm
these are the challenges the eventual authors would foreground.", "why_matters":
"Challenges drive the methodology's justification (N6); if the real paper frames the
problem differently, the challenge-to-mechanism map below would need revision.",
"implication": "Treat C1–C4 as a reasonable minimum challenge set any team attempting this
study would have to address, not as a confirmed authorial framing."}

---

## N6 Methodology

**overview** [HYPOTHESIS]: A two-stage longitudinal measurement study. **Stage 1 — pilot
(= the seed's minimal experiment):** construct ~300 contracts (100 JSON-schema contracts
sampled from SchemaStore/JSONSchemaBench stratified by depth and constraint count; 100
verifiable formatting-convention contracts in the style of IFEval's checkable rules; 100
few-shot template contracts mined from WildChat production-style conversations), run each
contract against one model lineage with ≥3 individually pinned successive versions (a
dated closed-API snapshot chain, e.g. successive gpt-4o dates, plus one open-weight chain,
e.g. Qwen2 → Qwen2.5 → Qwen3, as the reproducible anchor), with n=20 samples per
(contract, version) at fixed decoding settings, score every output with an automated
validator, and compute per-transition breakage rates against a within-version split-half
noise floor. **Stage 2 — scale-up:** grow to ~3,000 contracts and ≥10 version transitions
across 3 model families, fit the fragility model with grouped cross-validation, test
cross-family generalization of predictors, and add two mitigation arms (grammar-constrained
decoding on the open-weight chain; DSPy-style per-version prompt recompilation) to bound
how much of the measured breakage is avoidable.

**key_components** [HYPOTHESIS]:
- **M1** — *Contract Library Construction*: each contract is a triple (prompt template,
  input distribution, machine-checkable acceptance predicate). Sources: real-world JSON
  schemas from SchemaStore and JSONSchemaBench (schema contracts); IFEval-style
  programmatically verifiable format rules (convention contracts); few-shot templates mined
  from WildChat conversations exhibiting production-style structured-output usage
  (template contracts). Every contract carries a pre-registered feature vector: schema max
  nesting depth, field count, required-field ratio, count of enum/regex/pattern/format
  constraints, few-shot example count, instruction token length, and count of
  delimiter/casing rules — measured mechanically from the contract artifact itself.
- **M2** — *Automated Conformance Validator*: a three-tier deterministic checker per
  output: (a) parse tier — does the output parse as the expected envelope (e.g., valid
  JSON, expected code fence)?; (b) schema tier — `jsonschema` (Draft 2020-12) validation
  against the contract's schema; (c) convention tier — regex/rule checkers in the style of
  AutoIF's executable verification functions and IFEval's rule set. A contract instance
  passes iff all applicable tiers pass. Validators are themselves unit-tested against
  hand-constructed positive/negative example outputs before any measurement run (AutoIF's
  cross-validation discipline), and the strict-vs-lenient boundary (e.g., trailing prose
  around a JSON block) is a pre-registered, sensitivity-analyzed design constant.
- **M3** — *Version-Paired Execution Harness*: executes the full library against pinned,
  individually addressable versions — dated closed-API snapshots and permanently archived
  open-weight checkpoints — at temperature 0 (primary arm) and temperature 0.7 (secondary
  arm), n=20 samples per (contract, version, arm). All raw responses plus request metadata
  are archived in a content-addressed store for later re-scoring. Alongside every
  collection batch, a [LogProbTracking, OpenReview:hFxivbAgVP]-style first-token top-k
  logprob probe runs against the same endpoint, so any mid-collection silent serving change
  is detected and the affected batch re-collected.
- **M4** — *Breakage-Rate Computation*: per (contract, version): pass probability
  p̂ = passes/20; a contract "passes at v" iff p̂ ≥ 0.9 and "fails at v" iff p̂ ≤ 0.5
  (the indeterminate band is excluded from the primary statistic and covered by
  sensitivity analysis). Breakage rate B(v→v′) = |{c : pass@v ∧ fail@v′}| / |{c : pass@v}|;
  companion statistics: fix rate F(v→v′) (previously failing, now passing) and net
  regression B−F; all reported overall and per contract type.
- **M5** — *Fragility Predictor Model*: mixed-effects logistic regression of the
  per-contract breakage event on the M1 feature vector plus contract type, with random
  intercepts for version transition and model family; reported as odds ratios with 95%
  CIs. Predictive utility assessed separately via a gradient-boosted classifier's ROC-AUC
  under 5-fold cross-validation grouped by contract family (so near-duplicate contracts
  never straddle folds).
- **M6** — *Within-Version Noise-Floor Estimator*: for each version, the 20 samples per
  contract are split into two disjoint 10-sample halves and the full M4 pipeline is run
  between the halves as if they were two "versions"; the resulting pseudo-breakage rate
  B_null is the noise floor. Upgrade-induced breakage is claimed only where B(v→v′)
  significantly exceeds B_null under a paired test (see N8 analysis plan).

**challenge_arguments** [HYPOTHESIS — anticipated design arguments, not authorial claims]:
- {challenge_id: "C1", argument_text: "The three-tier validator (M2) makes pass/fail
  mechanically checkable and mirrors what a downstream parser actually enforces
  (parse → schema → convention), while contract construction (M1) restricts the library to
  contracts whose acceptance predicate is decidable, following AutoIF/IFEval's
  verifiable-constraint discipline; the strict/lenient boundary is pre-registered and
  sensitivity-analyzed rather than judged ad hoc.", mechanism_components: ["M1", "M2"]}
- {challenge_id: "C2", argument_text: "The harness (M3) only targets individually
  addressable versions — dated API snapshots and archived open-weight checkpoints — and
  runs a logprob-probe canary beside every batch so silent within-snapshot serving changes
  are detected rather than silently absorbed into the breakage estimate; the open-weight
  chains make the central claims permanently re-runnable.", mechanism_components: ["M3"]}
- {challenge_id: "C3", argument_text: "The split-half noise-floor estimator (M6) turns
  'is this real breakage or noise?' into an explicit paired comparison: the headline
  statistic is not raw B(v→v′) but its excess over B_null computed by the identical
  pipeline (M4) within a single version.", mechanism_components: ["M4", "M6"]}
- {challenge_id: "C4", argument_text: "Stage-2 scale (≈3,000 diverse contracts × ≥10
  transitions × 3 families) plus a multivariate mixed-effects model (M5) with grouped
  cross-validation addresses power and feature collinearity; the stratified library design
  (M1) deliberately decorrelates depth from constraint count by sampling schemas across
  the joint feature grid.", mechanism_components: ["M1", "M5"]}

**unaddressed_challenges** [HYPOTHESIS, V-08 flagged]: `["C2"]` — partially addressed
only: the logprob canary (M3) can *detect* silent within-snapshot changes on closed
endpoints but cannot prevent them, recover deprecated snapshots, or attribute a detected
change to a citable version identity; full attribution is achievable only on the
open-weight chains, which is why they anchor the primary claims. This assessment rests on
inferred (not extracted) N5/N6 items.

**Feasibility** [HYPOTHESIS]:
- *Pilot*: 300 contracts × 3 versions × 20 samples × 2 temperature arms ≈ 36K requests
  (~35–70M tokens at ~1–2K tokens/request) → **low-hundreds-of-USD API cost class**;
  open-weight arm ≈ 2–4 days on a single A100/H100 node (vLLM batch inference). Zero
  annotator-hours for scoring (fully mechanical validators); ~2 person-weeks of
  engineering, of which ~20 hours is authoring/unit-testing validators.
- *Scale-up*: 3,000 contracts × ~12 version-points × 20 samples ≈ 720K requests →
  **low-thousands-of-USD API cost class** plus ~1–2 GPU-weeks for the open-weight chains;
  ~1 person-month total effort.
- *Single biggest feasibility risk*: closed-API historical snapshots being deprecated
  mid-study (or changing silently), truncating the longitudinal chain and making the
  headline numbers irreproducible. **Mitigation**: anchor all primary claims on
  open-weight version chains (permanently downloadable checkpoints, e.g. Llama 2 → 3 →
  3.1 → 3.3 and Qwen2 → 2.5 → 3), treat closed dated snapshots as a secondary
  external-validity arm, archive every raw response on first contact so all statistics are
  re-computable offline forever.

**Status**: PARTIAL. `absence_comment`: {"what_missing": "No method section exists; M1–M6
are a design sketch extrapolated from the one-sentence minimal experiment plus real
precedents (AutoIF/IFEval validators, LogProbTracking canary, LAMDA longitudinal
protocol), not a description of an implemented system.", "why_matters": "A reviewer should
not treat 'M2 addresses C1' as a demonstrated design choice — it is a plausible choice
this document proposes for the hypothetical paper to adopt.", "implication": "Anyone using
this digest to scope the study should treat N6 as a starting design to critique and
refine — in particular the p̂ thresholds in M4 and the strictness constants in M2 need
pilot-stage calibration."}

---

## N7 Contributions

**contributions** [HYPOTHESIS — what such a paper would plausibly claim, framed from the
method + expected findings]:

- **CO1** [contribution_type: `empirical_finding`, is_testable: true, has_rq: true]: "A
  quantified, noise-floor-adjusted per-upgrade breakage rate for production-style
  structured-output contracts across multiple real LLM version transitions, decomposed by
  contract type."
- **CO2** [contribution_type: `empirical_finding`, is_testable: true, has_rq: true]: "An
  identification of contract-level features (e.g., schema nesting depth, constraint
  density, few-shot example count) that predict fragility to version upgrades, validated
  by out-of-family predictive performance."
- **CO3** [contribution_type: `dataset`, is_testable: false, has_rq: false]: "A reusable,
  versioned contract library (contracts + validators + archived raw model outputs) that
  other longitudinal LLM-drift audits can re-run and extend, in the spirit of [LAMDA,
  OpenReview:1FnCrZtBNQ]'s longitudinal benchmark."
- **CO4** [contribution_type: `empirical_finding`, is_testable: true, has_rq: true]: "A
  measurement of how much per-upgrade breakage is avoidable by two existing mitigations —
  grammar-constrained decoding and DSPy-style per-version prompt recompilation — bounding
  the fraction of breakage that is a deployment choice rather than an inherent cost."

**Status**: PARTIAL. `absence_comment`: {"what_missing": "No paper text exists to confirm
these as the authors' own asserted contributions.", "why_matters": "Contribution claims
anchor what N8's RQs should test; without a real paper, these are proposed contributions a
reviewer should expect, not confirmed ones.", "implication": "Use CO1–CO4 as a checklist
for what the eventual paper should explicitly claim, and verify against the real text once
written."}

---

## N8 Research Questions

- **RQ1** [GIVEN — near-verbatim restatement of the first half of the seed's core question]:
  "一次版本跳变平均打断多少生产风格的 prompt 模板/结构化输出契约？" (On average, how many
  production-style prompt templates / structured-output contracts does a single version
  jump break?) — rq_source: explicit(seed), evaluates_mechanisms: `["M2", "M3", "M4",
  "M6"]`, addresses_challenges: `["C1", "C2", "C3"]`, tests_contributions: `["CO1"]`,
  answered_by_experiment: "Pilot then scale-up: run the contract library (M1) against each
  successive version pair via the harness (M3), score with the validator (M2), compute
  B(v→v′), F(v→v′) and net regression (M4) per contract type, and test each B(v→v′)
  against the within-version noise floor (M6)."
- **RQ2** [GIVEN — near-verbatim restatement of the second half of the seed's core question]:
  "什么特征的契约最脆弱？" (Which contract features are most fragile?) — rq_source:
  explicit(seed), evaluates_mechanisms: `["M1", "M5"]`, addresses_challenges: `["C4"]`,
  tests_contributions: `["CO2"]`, answered_by_experiment: "Fit the mixed-effects fragility
  model (M5) on the feature vectors defined at library-construction time (M1) over all
  Stage-2 breakage events; report odds ratios and grouped-CV predictive AUC, including a
  train-on-two-families / test-on-third generalization split."
- **RQ3** [HYPOTHESIS — added to test the strengthened chain's mitigation arm]: "How much
  of the measured per-upgrade breakage is removed by (a) grammar-constrained decoding and
  (b) per-version prompt recompilation?" — rq_source: inferred, evaluates_mechanisms:
  `["M2", "M3", "M4"]`, addresses_challenges: `["C1", "C3"]`, tests_contributions:
  `["CO4"]`, answered_by_experiment: "Re-run the open-weight version chains with (a) an
  xgrammar/outlines-style constrained-decoding arm (guaranteed schema tier, convention
  tier still free) and (b) a DSPy-recompiled prompt arm per version, and compare each
  arm's B(v→v′) to the unmitigated arm on identical contracts."

**datasets** [HYPOTHESIS — real, existing sources for library construction and model
chains]: {names: ["SchemaStore (schemastore.org) — real-world JSON schemas, sampled and
stratified by depth/constraint count", "JSONSchemaBench — ~10K real-world JSON schemas for
schema-constrained generation evaluation", "IFEval — programmatically verifiable
instruction constraints (format-convention contracts)", "FollowBench — multi-constraint
instructions (constraint-density stratification; the benchmark [RECAST,
OpenReview:90tCp2KszA] builds on)", "WildChat-1M — real user–ChatGPT conversations, mined
for production-style few-shot/structured-output templates", "Berkeley Function Calling
Leaderboard (BFCL) v3 — function-calling structured-action contracts", "Model version
chains: dated OpenAI gpt-4o snapshots (e.g., 2024-05-13 → 2024-08-06 → 2024-11-20);
Llama 2 → 3 → 3.1 → 3.3; Qwen2 → Qwen2.5 → Qwen3"], source: HYPOTHESIS}

**baselines** [HYPOTHESIS]: {names: ["Within-version split-half resampling noise floor
(M6) — the null model every breakage claim is tested against", "[LogProbTracking,
OpenReview:hFxivbAgVP]-style first-token logprob change detector — tests whether cheap
distribution-shift signals predict contract-level breakage", "Grammar-constrained decoding
arm (lineage of [DiffusionCFG, OpenReview:7Sph4KyeYO]; implemented with
xgrammar/outlines on open-weight chains) — conformance upper bound", "[DSPy,
OpenReview:sY5N0zY5Od]-style per-version prompt recompilation — mitigation baseline"],
source: HYPOTHESIS}

**metrics** [HYPOTHESIS — with definitions]: {names: ["Breakage rate B(v→v′) =
P(fail@v′ | pass@v), where pass/fail per version uses the p̂≥0.9 / p̂≤0.5 rule over 20
samples", "Fix rate F(v→v′) = P(pass@v′ | fail@v) and net regression B−F", "Excess
breakage ΔB = B(v→v′) − B_null, where B_null is the split-half within-version
pseudo-breakage (M6)", "Per-contract-type breakage (schema / convention / few-shot
template)", "Fragility odds ratios with 95% CIs (mixed-effects logistic model, M5)",
"Fragility predictive ROC-AUC under grouped 5-fold CV and under leave-one-family-out"],
source: HYPOTHESIS}

**analysis plan** [HYPOTHESIS]: Pilot sample size n=300 contracts (100/type; with 300
paired pass/fail observations per transition, a two-sided exact McNemar-style paired test
has >0.9 power to distinguish B=5% from B_null=1% at α=0.05). Per transition:
paired-permutation test of B(v→v′) vs B_null over contracts, two-sided, α=0.05, with
Benjamini–Hochberg correction across all (transition × contract-type) cells. Stage-2
fragility analysis: pre-registered feature list (the M1 vector, 7 features), mixed-effects
logistic regression, α=0.05 on Wald tests after BH correction; ~3,000 contracts × ≥10
transitions gives ≥0.8 power to detect a per-feature odds ratio of 1.3. Expected effect
directions: B(v→v′) > B_null for most transitions (upgrades break real contracts beyond
noise); positive coefficients for nesting depth and constraint density; negative
coefficient for few-shot example count (more demonstrations → more anchored output
format).

**Status**: PARTIAL. `absence_comment`: {"what_missing": "RQ1/RQ2 are given directly by the
seed's two-part core question; RQ3, the datasets, baselines, metrics, and the analysis
plan are this document's design proposals, not stated by any source.", "why_matters":
"Without the noise-floor baseline and the pre-registered analysis plan, RQ1's headline
number could be inflated by sampling noise and RQ2's feature claims by multiple
comparisons (challenges C3/C4).", "implication": "The actual experiment must freeze the
p̂ thresholds, feature list, and test procedure before data collection for the breakage
rate to be trustworthy as evidence of upgrade-induced change specifically."}

---

## N9 Results

**PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY. No experiment has been run; nothing below is
a real number, and no numeric value is predicted.**

- **Result for RQ1** [PLACEHOLDER]: rq_id: "RQ1". result_text: "Predicted direction: for
  most tested version transitions, the noise-adjusted excess breakage ΔB will be
  significantly positive — a real, non-zero fraction of previously-passing contracts newly
  fails per upgrade — and breakage will differ by contract type, with strict-envelope
  contracts (schema contracts with tight constraint sets, exact-format conventions)
  breaking more often than few-shot template contracts whose demonstrations redundantly
  anchor the output format. Magnitudes are unknown and deliberately not predicted."
  result_type: `quantitative` (anticipated), evidence_strength: `missing`, rq_answered:
  `false`. **Falsification condition**: refuted if, across all tested transitions and
  contract types, B(v→v′) is statistically indistinguishable from the within-version
  noise floor B_null (BH-corrected paired tests, α=0.05) — i.e., if apparent
  cross-version breakage is no larger than same-version resampling variance, the claim
  that upgrades meaningfully break contracts is false.
- **Result for RQ2** [PLACEHOLDER]: rq_id: "RQ2". result_text: "Predicted direction:
  higher schema nesting depth and higher constraint density (enum/regex/pattern/format
  constraints) will carry significantly positive breakage odds ratios, and higher few-shot
  example count a significantly negative one, in the multivariate model; the fitted
  fragility model will retain above-chance predictive AUC on a held-out model family."
  result_type: `quantitative` (anticipated), evidence_strength: `missing`, rq_answered:
  `false`. **Falsification condition**: refuted if no pre-registered feature attains a
  significant odds ratio after BH correction, or if grouped-CV/leave-one-family-out AUC is
  indistinguishable from 0.5 — i.e., fragility is unpredictable from the proposed
  structural features and contract-design guidance cannot be derived from them.
- **Result for RQ3** [PLACEHOLDER]: rq_id: "RQ3". result_text: "Predicted direction:
  grammar-constrained decoding will eliminate schema-tier breakage nearly entirely (by
  construction) but leave convention-tier and semantic-envelope breakage; per-version
  prompt recompilation will reduce, but not eliminate, breakage relative to the frozen
  prompt arm. Together the arms will show a substantial share of measured breakage is
  avoidable by deployment choices." result_type: `quantitative` (anticipated),
  evidence_strength: `missing`, rq_answered: `false`. **Falsification condition**: refuted
  if mitigation arms show no significant reduction in B(v→v′) versus the unmitigated arm
  on identical contracts (paired test, α=0.05) — which would imply breakage is dominated
  by failure modes neither decoding guarantees nor prompt re-optimization can reach.

**Status**: NOT_FOUND (by construction — no paper exists). `absence_comment`:
{"what_missing": "No experiment has been run; the entries above are directional
hypotheses, each with an explicit pre-registered falsification condition, not measured
outcomes.", "why_matters": "Presenting a hypothesized direction with confidence
indistinguishable from a measured result would be exactly the kind of unsupported claim
EX-01 forbids.", "implication": "Treat all three entries as predictions to be tested; the
falsification conditions are the criteria by which the eventual experiment should judge
whether each hypothesis held."}

---

## N10 Threats / Self-Limitations

**threats** [HYPOTHESIS — anticipated threats to validity for this study design, not
author-acknowledged, since no paper exists; each with a planned mitigation]:

- **t1** [category: `construct`]: "The contract library is a constructed proxy for real
  production usage; both the contract mix and the validator's strict/lenient boundary
  (M2) operationalize 'breakage' in ways that may not match what real downstream parsers
  reject, inflating or deflating the measured rate." mitigation: "Source contracts from
  real artifacts (SchemaStore/JSONSchemaBench schemas, WildChat-mined templates, BFCL
  function signatures) rather than inventing them; report breakage per source; unit-test
  validators against hand-built positive/negative outputs; sensitivity-analyze the
  strictness constants and the p̂ thresholds."
- **t2** [category: `internal`]: "Within-version decoding stochasticity and serving
  nondeterminism can masquerade as upgrade-induced breakage, confounding the causal
  attribution of pass→fail flips to the version change." mitigation: "Temperature-0
  primary arm; n=20 samples per (contract, version); explicit split-half noise floor
  (M6) with paired testing; logprob-probe canary (M3) to detect and re-collect batches
  affected by mid-collection silent serving changes."
- **t3** [category: `external`]: "Findings may be specific to the model families, version
  windows, and contract genres tested, and may not generalize to other providers, future
  upgrade styles, or contract types outside the three studied classes." mitigation:
  "Three model families including at least two open-weight lineages; report all
  statistics per family and per transition rather than pooled only; frame closed-API
  results as a secondary arm; publish the library so others can extend coverage."
- **t4** [category: `conclusion`]: "The fragility analysis (RQ2) tests multiple correlated
  features across many transition × type cells, risking false-positive feature claims and
  overfitted predictors." mitigation: "Pre-registered 7-feature list frozen before data
  collection; Benjamini–Hochberg correction across all tests; multivariate mixed-effects
  model rather than marginal correlations; grouped 5-fold CV plus leave-one-family-out
  evaluation for the predictive claim; a priori power analysis sizing Stage 2."
- **t5** [category: `reproducibility`]: "Closed commercial endpoints can be updated
  silently within a named snapshot and deprecated entirely, so exact replication of a
  specific 'version N → N+1' comparison may become impossible." mitigation: "Anchor
  primary claims on permanently downloadable open-weight checkpoints; archive every raw
  response in a content-addressed store on first contact so all statistics are recomputable
  offline; release contracts, validators, and raw outputs (CO3)."

**Status**: NOT_FOUND (no author-acknowledged Threats/Limitations section exists — no
paper exists). `absence_comment`: {"what_missing": "No paper exists yet to author-state
its own limitations; t1–t5 are anticipated by this document, not acknowledged by any
author.", "why_matters": "Per N10's spec, only author-acknowledged limitations belong in a
real digest's N10 — these are included only because the reverse-digest methodology calls
for anticipated limitations under HYPOTHESIS, and must not be mistaken for a real
Limitations section.", "implication": "When the real paper is written, replace t1–t5 with
whatever the actual authors state; until then they serve as a design-review checklist."}

---

## N11 Artifacts

**artifacts**: `[]` — nothing has been released; the paper does not exist. [PLACEHOLDER]

- **has_code**: `false` [PLACEHOLDER]
- **has_data**: `false` [PLACEHOLDER]
- **has_model**: `false` [PLACEHOLDER]

**Status**: NOT_FOUND. `absence_comment`: {"what_missing": "No code repository,
contract-library dataset, or archived-output corpus has been released because no paper or
implementation exists yet.", "why_matters": "This is reviewer-relevant signal for anyone
tracking this topic's maturity — B3.4 is currently pure idea-stage, not even a preprint;
the planned CO3 artifact (contracts + validators + raw outputs) is the load-bearing
reproducibility commitment of the design.", "implication": "Any future tracking of this
topic should update N11 the moment a contract library, execution harness, or raw-output
archive is actually released."}

---

## N12 Contribution Type

- **value** [HYPOTHESIS]: `empirical`
- **rationale** [HYPOTHESIS]: "Re-checked against the strengthened design: the paper's
  central claims remain CO1 (a noise-adjusted per-upgrade breakage rate), CO2 (validated
  fragility predictors), and CO4 (measured mitigation headroom) — all empirical
  measurements of an existing phenomenon, tested by RQ1–RQ3. The design does produce a
  reusable longitudinal contract library (CO3) in the spirit of [LAMDA,
  OpenReview:1FnCrZtBNQ], which raises the `benchmark`/`dataset` alternative; but unlike
  LAMDA, whose stated contribution *is* the benchmark infrastructure, here the library is
  the measurement instrument and the findings are the headline — matching the
  disambiguation hint 'measurement study with a published dataset → empirical if the study
  is the main contribution.' Not `tool` (the harness is not proposed for adoption as a
  system) and not `case_study` (systematic multi-family measurement, not a single-context
  narrative)."
- **source**: HYPOTHESIS

**Status**: PARTIAL. `absence_comment`: {"what_missing": "No published paper exists to
confirm `empirical` as the authors' own asserted contribution-type label; this
classification is this document's inference from the seed + N6/N7/N12 design, not an
extracted self-classification.", "why_matters": "Contribution-type is what downstream
tooling (Phase A's stage cross-check, `pengsida-stage-reviewer`'s archetype gate,
`research-paper-writing`'s section-template choice) reads to decide which evidence
standard and archetype template apply — treating an inferred label as settled fact would
propagate a silent [HYPOTHESIS]→[GIVEN] promotion exactly like the one this field's own
`rationale` explicitly reasons through (dataset/benchmark vs. empirical) rather than
resolves.", "implication": "Re-derive N12 from the real paper's own stated framing once
written; until then, downstream phases should treat `empirical` as the best-supported
inference, not an authorial declaration, and re-run the Part 2 archetype check (guidance.md
Part 2) if a future draft's Introduction reads more like a benchmark-contribution paper."}

---

## Claims

- "A single LLM version upgrade breaks a measurable fraction of previously-passing
  production-style structured-output contracts, in excess of within-version sampling
  noise." — evidence: [{type: "argument", text: "Derived from the seed's core question
  ('一次版本跳变平均打断多少……契约') plus two real premises: endpoints demonstrably change
  ([ChatGPTDrift, arXiv:2307.09009] documents cross-snapshot behavior shifts;
  [LogProbTracking, OpenReview:hFxivbAgVP] treats endpoint change detection as a live
  monitoring problem) and prompt templates are wording-fragile ([DSPy,
  OpenReview:sY5N0zY5Od]; [TARE, OpenReview:YEBDvqsniH]). The magnitude is unknown and is
  exactly what RQ1 measures.", source: HYPOTHESIS, location: null}] — **[HYPOTHESIS]**
- "Contract-level structural features (schema nesting depth, constraint density, few-shot
  example count) predict which contracts are most fragile to version upgrades." —
  evidence: [{type: "argument", text: "Extrapolated from the seed's second question
  ('什么特征的契约最脆弱') plus the real finding line that constraint satisfaction degrades
  with constraint count at a fixed version ([RECAST, OpenReview:90tCp2KszA], building on
  FollowBench); whether the same features govern *cross-version* fragility is untested and
  is what RQ2 measures.", source: HYPOTHESIS, location: null}] — **[HYPOTHESIS]**
- "The specific measurement gap — a noise-adjusted per-upgrade contract-breakage rate with
  validated fragility predictors — is unfilled: the corpus contains endpoint-change
  detectors, input-side prompt-robustness studies, single-snapshot constraint verifiers,
  and weight-space version-fragility work, but no longitudinal contract-breakage
  measurement." — evidence: [{type: "citation", text: "Absence established across seven
  keyword searches of topics/corpus/ideas.jsonl from mechanism / failure-mode /
  methodology angles; nearest neighbors are [LogProbTracking, OpenReview:hFxivbAgVP],
  [CoIPO, OpenReview:TUd3c7Vr1z], [RECAST, OpenReview:90tCp2KszA], [AutoIF,
  OpenReview:cRR0oDFEBC], and [CAR-LoRA, OpenReview:5GimteSrgW]; see N3/N4.", source:
  HYPOTHESIS, location: null}] — **[HYPOTHESIS]**
- "Whatever breakage rate is measured is only meaningful relative to a reported
  within-version noise floor, and part of it is avoidable: constrained decoding and
  per-version prompt recompilation bound how much breakage is a deployment choice rather
  than an inherent upgrade cost." — evidence: [{type: "argument", text: "Follows from
  challenge C3 and the M6 noise-floor design, plus the existence of the two mitigation
  families in the real literature ([DiffusionCFG, OpenReview:7Sph4KyeYO] lineage for
  decoding-time guarantees; [DSPy, OpenReview:sY5N0zY5Od] for recompilation); RQ3's
  falsification condition operationalizes this.", source: HYPOTHESIS, location: null}] —
  **[HYPOTHESIS]**

---

## Self-verification pass (per `references/self-verification.md`)

- V-01 (locator integrity): nothing is tagged `source="extracted"` from a real paper of
  this topic (none exists); all grounded statements point to the seed README, to corpus
  entries identified by OpenReview id, or are explicitly null with an absence_comment.
- V-02 (absence comment shape): every node with non-FOUND status carries a full 3-part
  `absence_comment`.
- V-04 / EX-09 (id consistency), checked item by item:
  - `N4.affects_works` ⊆ N3 citation_keys, verbatim: `[ChatGPTDrift, arXiv:2307.09009]`,
    `[LogProbTracking, OpenReview:hFxivbAgVP]`, `[CoIPO, OpenReview:TUd3c7Vr1z]`,
    `[TARE, OpenReview:YEBDvqsniH]`, `[RECAST, OpenReview:90tCp2KszA]`,
    `[AutoIF, OpenReview:cRR0oDFEBC]`, `[DiffusionCFG, OpenReview:7Sph4KyeYO]`,
    `[DSPy, OpenReview:sY5N0zY5Od]`, `[CAR-LoRA, OpenReview:5GimteSrgW]`,
    `[LAMDA, OpenReview:1FnCrZtBNQ]` — all resolve.
  - `N6.challenge_arguments`: challenge_ids ∈ {C1,C2,C3,C4} (all in N5);
    mechanism_components ∈ {M1,M2,M3,M4,M5,M6} (all in N6.key_components).
  - `N6.unaddressed_challenges` = ["C2"] ⊆ N5 ids.
  - N8: RQ1 → M2/M3/M4/M6, C1/C2/C3, CO1; RQ2 → M1/M5, C4, CO2; RQ3 → M2/M3/M4, C1/C3,
    CO4 — every referenced C/M/CO id exists in N5/N6/N7.
  - N9 rq_ids {RQ1, RQ2, RQ3} all exist in N8.
  - N7 `has_rq` flags consistent: CO1/CO2/CO4 tested by RQ1/RQ2/RQ3; CO3 has_rq=false and
    is referenced by no RQ.
- V-08 (confidence doesn't inflate under inference): N6's unaddressed_challenges note,
  the feasibility risk statement, and all three N9 falsification conditions explicitly
  flag that they rest on inferred, not extracted, upstream items; no numeric outcome is
  predicted anywhere in N9.
- V-10/V-11 (N10/N11 self-consistency): N10 status NOT_FOUND with anticipated threats
  explicitly marked as not author-acknowledged; N11 status NOT_FOUND with `artifacts=[]`
  and all three flags `false`.
- V-12 (N12 rationale quality): rationale names the competing classification
  (`benchmark`/`dataset` via CO3), cites the disambiguation hint, and distinguishes this
  design from [LAMDA, OpenReview:1FnCrZtBNQ] where the benchmark *is* the contribution.
- Field-name spot check (EX-12): `objective`, `motivations`, `citation_key`,
  `approach_summary`, `limitation_text` semantics respected; no forbidden renames.
- Empty-node check (EX-11): all of N0–N12 plus Claims appear above; none silently omitted.
