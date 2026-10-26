# Digest: Does the Diagnosis Survive a Model Swap? Cross-Backbone Stability of Failure Attribution

> **REVERSE-DIGEST NOTICE**: This document is speculative scaffolding for research planning. No paper exists yet — the seed is an abstract research idea (topic code B2.3, label "[矛盾]", from `topics/B2.3_.../README.md`). Every field below is tagged `[GIVEN]` (verbatim/near-verbatim from the seed), `[HYPOTHESIS]` (reasoned elaboration / prediction, not fact), `[GROUNDED:corpus]` (a real paper retrieved from the local OpenReview corpus `topics/corpus/ideas.jsonl`, with its approach summarized from that paper's own motivation/method text), or `[PLACEHOLDER]` (genuinely unknowable until the work is done — never invented). Treat all `[HYPOTHESIS]` and `[PLACEHOLDER]` content as unconfirmed.

---

## N0 Metadata

- **title** [GIVEN]: "Does the Diagnosis Survive a Model Swap? Cross-Backbone Stability of Failure Attribution"
- **title_cn** [GIVEN]: 归因的跨模型稳定性
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper written, no authors exist yet.
- **abstract** [HYPOTHESIS] (drafted as a plausible abstract synthesizing the core question + minimal experiment — explicitly a draft, not a real abstract):
  > "Failure-attribution frameworks for LLM-agent pipelines label a failed task trace as a planning failure, a tool-use failure, or an execution failure. These labels are typically produced and validated with a single underlying LLM backbone — for the agent, the judge, or both. We ask whether such diagnoses are properties of the task and the injected fault, or artifacts of the particular backbone. We run an identical fault-injection task suite (built over GAIA and WebArena tasks, with programmatic plan-, tool-, and execution-layer injectors) through multiple LLM model families as the agent's executing backbone, apply a fixed, pre-registered attribution procedure to every resulting failure trace, and measure the cross-backbone agreement of the resulting plan/tool/execution labels with chance-corrected statistics. A judge-by-agent factorial ablation decomposes label variance into agent-backbone, judge-backbone, task, and interaction components. We report agreement overall and per layer; the result is informative whether attribution turns out to be stable (supporting diagnosis as a task property) or model-specific (implying that diagnosis partly reflects backbone idiosyncrasy)."
- **doi** [PLACEHOLDER]: null
- **arxiv_id** [PLACEHOLDER]: null
- **num_pages** [PLACEHOLDER]: null
- **research_area** [HYPOTHESIS]: "AI/ML" (secondary overlap with "SE": the object of study is agent-pipeline failure diagnosis, but the central phenomenon — backbone-dependent behavior — is an ML property).

**Status**: PARTIAL — title/core-question given; authors/abstract/doi are placeholders because the paper does not exist.
**absence_comment**: {"what_missing": "No real authors, abstract, or bibliographic identifiers exist because this is a pre-writing scaffold, not an extracted paper.", "why_matters": "Downstream tools (se-paper-reviewer, pengsida-paper-writer) that consume N0 fields must not treat this metadata as citable.", "implication": "Treat N0 purely as a planning placeholder; re-run a real digest once a manuscript exists."}

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS] (full predicate, extrapolated from the core question): "measure whether the plan/tool/execution failure-attribution label assigned to a fault-injected LLM-agent task failure remains the same when the agent's underlying LLM backbone is swapped across multiple model families, and decompose any instability into agent-backbone-driven vs judge-backbone-driven components, in order to determine whether 'diagnosis' is a property of the task/fault or a property of the specific model."
  - Self-check: (1) kind of task = measurement/consistency study; (2) domain = LLM-agent failure diagnosis (plan/tool/execution attribution); (3) outcome shape = chance-corrected cross-backbone agreement + per-layer breakdown + variance decomposition. All three land.
- **inputs** [HYPOTHESIS], inferred from the minimal experiment:
  - a fixed suite of agent tasks with controlled faults injected at a known layer (plan/tool/execution), each with a machine-readable injection record
  - several LLM backbones / model families serving as the agent's executing model under an identical scaffold
  - a fixed, pre-registered attribution procedure (LLM-judge with frozen prompt + human codebook on a subset) that assigns an observed failure-layer label to each resulting trace
- **outputs** [HYPOTHESIS], inferred from the minimal experiment:
  - per-(task, fault, backbone, seed) attribution label + normalized trace
  - cross-backbone agreement/consistency statistics (pairwise agreement, Fleiss' κ, Krippendorff's α), overall and per-layer
  - agreement of labels against the injected ground-truth fault layer; failure-overlap (censoring) rate across backbones
  - a variance decomposition of label disagreement over agent backbone / judge backbone / task / interactions
- **constraints** [GIVEN, minimally elaborated]: the seed specifies the task set is built via **fault injection** ("故障注入任务集"), which by construction means each task's true failure layer is known/controlled — the closest thing to an explicit ground-truth/separability constraint the seed states.
- **status**: PARTIAL (no explicit formulation exists in a real paper; this is a reconstructed formulation).
- **source**: inferred
- **location**: N/A — reverse digest; grounded directly in seed README's 核心问题 and 最小实验 lines.
- **absence_comment**: {"what_missing": "There is no written Methods/Problem-Formulation section to extract from.", "why_matters": "A reviewer cannot verify inputs/outputs/constraints against paper text because none exists.", "implication": "Use this reconstruction only as a drafting aid; revise once real experiments are designed."}

---

## N2 Motivation

**motivations** (each `[HYPOTHESIS]` unless noted, reconstructed from the seed's `parent_topic` field — "B2. 失败归因（plan / tool / execution）" — and from what the grounded N3 corpus papers actually establish):

1. [HYPOTHESIS, grounded] motivation_text: "Automated failure attribution for LLM-agent systems is now a formalized, benchmarked task — [Who&When, OpenReview:GazlTYxZss] defines it (which agent, which decisive step) and [AgenTracer, OpenReview:l05DseqvuD] scales its supervision via counterfactual replay and programmatic fault injection. Yet both lines validate attribution within fixed execution stacks; neither measures whether the attribution label for the same injected fault survives a swap of the agent's backbone. If it does not, attribution results are (task, backbone)-pair properties being reported as task properties." evidence=[{type: "citation", text: "N3 entries [Who&When, OpenReview:GazlTYxZss], [AgenTracer, OpenReview:l05DseqvuD]", source: extracted-from-corpus, location: "corpus proposal texts"}] source=inferred location=N/A
2. [HYPOTHESIS] motivation_text: "Practitioners routinely swap the underlying LLM (for cost, latency, or capability) while keeping the agent scaffold fixed. If failure attribution does not survive this swap, diagnostic tooling built on it must be re-validated per backbone — a materially different and more expensive claim than 'this tool diagnoses the task.'" evidence=[] source=inferred location=N/A
3. [HYPOTHESIS, grounded] motivation_text: "The judge side is independently suspect: [PreferenceLeakage, OpenReview:grIvSXVJ65] shows LLM judges systematically favor outputs from related generators, and [BiasScope, OpenReview:QGOw6AU8Lp] shows judges are flipped by structured surface perturbations. Attribution labels produced by an LLM judge over backbone-flavored traces therefore inherit two unvalidated dependencies at once — the agent backbone and the judge backbone — and the seed's `[矛盾]` label is exactly this tension: diagnosis as an objective property of the failure vs a byproduct of whichever models produced and judged it." evidence=[{type: "citation", text: "N3 entries [PreferenceLeakage, OpenReview:grIvSXVJ65], [BiasScope, OpenReview:QGOw6AU8Lp]", source: extracted-from-corpus, location: "corpus proposal texts"}] source=inferred location=N/A

**status**: PARTIAL (reconstructed, not extracted).
**absence_comment**: {"what_missing": "No real Introduction/Motivation section exists to quote author-stated importance claims from.", "why_matters": "Motivation is inferred from the parent-topic label plus real corpus papers' own motivations, not from this paper's authors.", "implication": "Treat as a plausible framing to validate once the pilot is run."}

---

## N3 Related Works

**Search performed**: Yes — corpus retrieval over `topics/corpus/ideas.jsonl` (11,683 OpenReview papers) with six keyword-angle queries: (1) failure attribution / root cause / which agent causes failure; (2) LLM-as-judge consistency / evaluator bias / rater agreement; (3) agent failure taxonomy / tool-use and planning errors; (4) fault injection / counterfactual perturbation of trajectories; (5) cross-model consistency / backbone; (6) agent benchmarks (GAIA/WebArena) for the task substrate. Full motivation+method texts of the top hits were read before inclusion.

**status**: FOUND — the corpus contains directly on-target prior work for both halves of the question (attribution methods; backbone/judge sensitivity). No entry below is invented.

| citation_key | approach_summary | tag | paper_url |
|---|---|---|---|
| [Who&When, OpenReview:GazlTYxZss] | Formalizes automated failure attribution in LLM multi-agent systems as a first-class judging problem: defines *decisive errors* as agent–step pairs whose correction flips a failed trajectory to success (extending ProcessBench's earliest-error notion), releases the Who&When dataset of failure logs with human agent- and step-level annotations, and evaluates LLM-judge attribution strategies (all-at-once, step-by-step, binary search) plus a hybrid agent-then-step pipeline. | [GROUNDED:corpus] | https://openreview.net/forum?id=GazlTYxZss |
| [AgenTracer, OpenReview:l05DseqvuD] | Converts decisive-error localization into a scalable learning problem: replays failed trajectories with one step at a time minimally corrected to find the outcome-flipping step (counterfactual discovery), programmatically injects faults into *successful* trajectories so the injected step is the decisive error by construction, unifies both into a supervision corpus, and trains a compact RL tracer to predict responsible agent and earliest decisive step. | [GROUNDED:corpus] | https://openreview.net/forum?id=l05DseqvuD |
| [BreakingBackbones, OpenReview:kga18ld70t] | Argues the right unit of analysis for agent security is the single backbone LLM call, not the whole agent: proposes *threat snapshots* (one call's full context + attack insertion + success metric) to decouple backbone-native vulnerabilities from tool wrappers and control flow, builds a snapshot benchmark spanning attack vectors/objectives, and compares many backbone LLMs on identical snapshots via crowdsourced adaptive attacks. | [GROUNDED:corpus] | https://openreview.net/forum?id=kga18ld70t |
| [PreferenceLeakage, OpenReview:grIvSXVJ65] | Defines *preference leakage*: an LLM judge systematically inflates scores of student models trained on synthetic data from a related generator (same model / inheritance / same family). Trains matched students on data from different generators, evaluates under multiple judges on AlpacaEval 2.0 and Arena-Hard, and quantifies excess win rate with a Preference Leakage Score. | [GROUNDED:corpus] | https://openreview.net/forum?id=grIvSXVJ65 |
| [BiasScope, OpenReview:QGOw6AU8Lp] | Automated discovery of LLM-judge biases beyond hand-designed taxonomies: a teacher model perturbs rejected responses with candidate bias patterns over pairwise data with objective correctness labels, mines the target judge's misjudgments and self-explanations for new candidate biases, and iteratively grows a validated bias library — demonstrating that structured surface perturbations systematically alter judge decisions. | [GROUNDED:corpus] | https://openreview.net/forum?id=QGOw6AU8Lp |
| [MENLO, OpenReview:QOWYX3Q2XS] | Documents that evaluator models are not condition-invariant along the language axis: reward models and LLM judges exhibit substantial cross-language inconsistency and fairness issues, motivating a 47-language evaluation of native-like quality with human-grounded preference/proficiency annotations. | [GROUNDED:corpus] | https://openreview.net/forum?id=QOWYX3Q2XS |
| [MAST, arXiv:2503.13657] | ("Why Do Multi-Agent LLM Systems Fail?", Cemri et al. 2025) Builds the Multi-Agent System Failure Taxonomy from expert annotation of traces across mainstream multi-agent frameworks, documenting high failure rates and recurring failure-mode categories, with an LLM-annotator pipeline validated against human experts. | [NON-CORPUS — canonical; cited as @cemri2025mast inside the corpus texts of both [AgenTracer, OpenReview:l05DseqvuD] and its motivation; included with confidence but flagged as outside ideas.jsonl] | https://arxiv.org/abs/2503.13657 |

**absence_comment**: null (node populated; status FOUND).

**Harvest-adequacy caveat (added 2026-07-04, from design_review.md F4/novelty audit)**: the entries above are genuinely corpus-grounded (all six OpenReview ids resolve in `ideas.jsonl` with matching titles), but the *breadth* of the non-pre-emption check is weak: the separate 150-candidate arXiv harvest feeding `reference_candidates.jsonl` yielded 147 off-topic hits (generic keyword overlap only), meaning no targeted search for this topic's specific claim has yet been run outside the 2025 OpenReview snapshot. The "no one has measured cross-backbone attribution stability" gap statement is therefore provisional. Residual (blocking before Phase E, alongside the pdf/digest backfill): re-harvest on the named angles — "cross-backbone failure attribution stability", "LLM judge agreement on agent trajectories/traces", "fault injection agent evaluation across models", "plan tool execution error taxonomy cross-model", "backbone swap agent diagnosis reproducibility" — and route any discovered method-twin through guidance.md Part 4 situation 6 (repositioning + Phase A re-check).

---

## N4 Prior Limitations

**grounding_check**: true (every limitation cites at least one N3 `citation_key`, verbatim string form).

| limitation_text | affects_works | source | limitation_type |
|---|---|---|---|
| [HYPOTHESIS, defensible from the cited paper's own scope] "Who&When formalizes attribution and shows even strong reasoning judges attribute poorly — but every failure log is attributed as produced by one fixed system configuration; the framework never runs the *same* task/fault under multiple agent backbones, so it cannot say whether its labels are properties of the failure or of the backbone that generated the trace. Its own motivation concedes manual attribution is 'prohibitively expensive and inconsistent' without quantifying inconsistency across model choices." | [Who&When, OpenReview:GazlTYxZss] | inferred | generalizability |
| [HYPOTHESIS, defensible from method text] "AgenTracer's fault-injection labels are correct *by construction only within the execution stack that was replayed*: the counterfactual definition ('earliest step whose correction flips the outcome') is evaluated under one backbone's downstream behavior, so the same injected fault could yield a different decisive step — or no failure at all — under a different backbone. Cross-backbone label stability is neither measured nor claimed." | [AgenTracer, OpenReview:l05DseqvuD] | inferred | generalizability |
| [HYPOTHESIS, defensible from stated scope] "Breaking Agent Backbones establishes backbone-level comparison as a first-class evaluation axis, but only for *attack susceptibility scores*; it does not test whether qualitative failure *diagnoses* (which layer failed) transfer across backbones, and its snapshot abstraction deliberately removes the multi-step downstream propagation that makes layer attribution ambiguous." | [BreakingBackbones, OpenReview:kga18ld70t] | inferred | other |
| [HYPOTHESIS, defensible from stated scope] "The judge-reliability line quantifies judge-side distortions — relatedness-driven score inflation and perturbation-induced misjudgment — but only on pairwise preference tasks with short responses; neither work measures judge disagreement on long agent traces, nor separates judge-side from agent-side variance in a trace-attribution setting." | [PreferenceLeakage, OpenReview:grIvSXVJ65], [BiasScope, OpenReview:QGOw6AU8Lp] | inferred | generalizability |
| [HYPOTHESIS, defensible from stated scope] "MENLO documents evaluator non-invariance along the *language* axis; the backbone axis for trace-level failure attribution is untouched, and its evaluators score response quality, not failure-layer labels." | [MENLO, OpenReview:QOWYX3Q2XS] | inferred | other |
| [HYPOTHESIS, defensible from what the method covers] "MAST's taxonomy is induced from traces of specific framework+backbone configurations and validated by inter-annotator agreement among *human/LLM annotators on the same traces* — it never checks whether the same task re-run under a different backbone would be assigned the same failure category, i.e., taxonomy reliability is established across annotators, not across backbones." | [MAST, arXiv:2503.13657] | inferred | generalizability |

**status**: PARTIAL — limitations are reviewer-plausible extrapolations tied to real papers' own stated scopes and method texts, not author self-admissions.
**absence_comment**: {"what_missing": "None of the cited works explicitly states 'our attribution has not been tested across backbones'.", "why_matters": "These are gap statements defensible from what each method demonstrably does not cover, carrying lower evidentiary weight than extracted author admissions.", "implication": "Confirm against the actual papers (not just corpus proposal texts) during the real related-work pass."}

---

## N5 Challenges

**conflation_check**: true (five challenges, distinct axes: measurement confound, behavioral non-invariance, censoring/selection, taxonomy ambiguity, surface-style confound).

| id | text | source |
|---|---|---|
| C1 | [HYPOTHESIS, tightly derived] "Attribution is usually itself performed by an LLM judge, so comparing 'the same failure, different agent backbone' conflates two variance sources: the backbone that *produced* the failure and the backbone that *diagnosed* it. Instability could come from either, and disentangling them requires a factorial design, not a single fixed judge — this is inherent to the setup, not a flaw of any one prior tool." | inferred |
| C2 | [HYPOTHESIS, tightly derived] "Identically injected faults do not manifest identically downstream across model families — a tool-layer fault can cascade into plan-layer symptoms in one model and stay execution-local in another — so the observable failure signature is not backbone-invariant even before any attribution method is applied. 'Same fault' guarantees same *cause*, not same *evidence*." | inferred |
| C3 | [HYPOTHESIS, tightly derived] "Failure-set censoring: a stronger backbone may absorb or recover from an injected fault and simply succeed, leaving no failure to attribute in that (task, fault, backbone) cell. Cross-backbone agreement is only computable over the intersection of failing cells, and that intersection is itself backbone-dependent — so the agreement statistic is defined over a selected, non-random subsample unless overlap is measured and reported as a first-class quantity." | inferred |
| C4 | [HYPOTHESIS, tightly derived] "The plan/tool/execution boundary is not a natural kind: a single failure can genuinely span layers (a bad plan causes a malformed tool call), so any consistency metric is sensitive to codebook granularity and tie-breaking rules, independent of which backbone is used." | inferred |
| C5 | [HYPOTHESIS, tightly derived] "Model families differ systematically in verbosity, trace formatting, and self-reporting style; any text-based attribution procedure can latch onto these surface regularities (a known failure mode of LLM judges) rather than onto where the failure actually occurred, biasing cross-backbone comparisons even when the underlying failures are identical." | inferred |

**N4-vs-N5 self-check applied**: none of these describe what a prior tool cannot do (that's N4); all five describe why the underlying measurement problem is hard regardless of which tool is used.
**Note on id stability**: C1, C2 unchanged from the previous digest revision; former C3 (taxonomy ambiguity) is now C4 and former C4 (surface style) is now C5 to make room for the censoring challenge C3, which the previous revision had folded implicitly into C2. All cross-references in N6/N8 below use the *current* ids.

**status**: FOUND (as a reasoned, problem-inherent list; not extracted from a paper since none exists).
**absence_comment**: null (populated).

---

## N6 Methodology

**overview** [HYPOTHESIS]: "A two-stage measurement study.
**Stage 1 — Pilot (= the seed's 最小实验, verbatim in spirit):** build a small fault-injection suite (≈60 tasks drawn from GAIA level-1/2 and WebArena-style tool tasks, each with 3 injector types → ≈180 (task, fault) cells), run it under 4 backbones from distinct families (e.g., one GPT-family, one Claude-family, one Llama-family, one Qwen-family model) with an identical ReAct-style scaffold at temperature 0, attribute every failure with one fixed LLM judge under a frozen prompt, and compute the cross-backbone agreement rate of plan/tool/execution labels plus the failure-overlap rate. The pilot's job is to (a) produce the seed's headline number and (b) calibrate fault 'lethality' so Stage 2 cells rarely censor.
**Stage 2 — Scale-up:** ≈300 tasks × 3 fault layers, 6–8 backbones chosen to cross *family* with *capability tier* (two sizes per family where available), 3 sampling seeds per cell, and a full judge×agent factorial (3 judge backbones from different vendors, plus a human-codebook subset), enabling chance-corrected agreement, per-layer breakdowns, and a variance decomposition of label instability into agent-backbone, judge-backbone, task, and interaction components. Traces are style-normalized before judging; all injection records, traces, labels, and analysis code are released." — source: inferred, location: N/A (no paper text).

**key_components**:

| id | name | text (what is measured/built, instrument, granularity) | source |
|---|---|---|---|
| M1 | Fault-injection task suite | Instrument one fixed agent scaffold with three programmatic injectors, following the injection-into-successful-traces logic of [AgenTracer, OpenReview:l05DseqvuD]: **plan-layer** (corrupt the planner's decomposition/goal constraint before execution), **tool-layer** (swap a tool-call argument or return a corrupted tool observation), **execution-layer** (corrupt the final action/answer synthesis step). Each injection emits a machine-readable record `{task_id, layer, step_idx, payload}` — the ground-truth label. Granularity: per (task, fault) cell; pilot ≈180 cells, scale-up ≈900 cells. | inferred |
| M2 | Multi-backbone execution harness | Run every cell under K backbones (pilot K=4, scale-up K=6–8 crossing family × capability tier) with byte-identical scaffold, prompts, tool set, temperature 0 (plus 3 seeds in Stage 2 at T=0.7 for a stochasticity check). Instrument: normalized JSON trace schema (steps, tool calls, observations, final answer) + the task's programmatic success checker. Output per cell: success/failure flag + full trace. | inferred |
| M3 | Fixed attribution procedure | Two instantiations of one pre-registered codebook defining plan/tool/execution with decision rules and a forced tie-break (earliest causally decisive layer wins, per the decisive-error definition of [Who&When, OpenReview:GazlTYxZss]): (a) an LLM judge with a frozen prompt at temperature 0, using Who&When's all-at-once and step-by-step strategies as the two judging protocols; (b) two human annotators applying the same codebook to a 200-trace subset (κ target ≥0.7 before adjudication) to validate the judge. Granularity: one label per failing (task, fault, backbone, seed) trace. | inferred |
| M4 | Trace style-normalization layer | Before any judging, canonicalize traces: strip model-identifying tokens and boilerplate, normalize tool-call JSON formatting, truncate chain-of-thought to a fixed token budget, and (ablation arm) paraphrase reasoning text with a neutral rewriter. Instrument: deterministic normalizer + a paraphrase model distinct from all agent and judge backbones. Purpose: measure how much apparent cross-backbone disagreement is surface-style-driven (judge labels on raw vs normalized traces). | inferred |
| M5 | Consistency + censoring metrics | Compute, over the intersection of failing cells: pairwise percent agreement, Fleiss' κ across backbones, Krippendorff's α (handles missing cells natively, mitigating censoring), and per-layer attribution accuracy vs the M1 injection record. Compute the **failure-overlap rate** (fraction of cells failing under all K backbones) as a first-class reported quantity, with per-backbone recovery rates. Granularity: overall, per layer, per backbone pair, per family-vs-cross-family pair. | inferred |
| M6 | Judge×agent factorial variance decomposition | Stage 2 crosses J=3 judge backbones (distinct vendors, none identical to an agent backbone in the same cell where avoidable — the relatedness precaution motivated by [PreferenceLeakage, OpenReview:grIvSXVJ65]) with K agent backbones over the same traces. Fit a cross-classified mixed-effects model (label match ~ (1|task) + (1|agent_backbone) + (1|judge_backbone) + interactions) and report the share of label variance attributable to each factor. | inferred |

**challenge_arguments** (all [HYPOTHESIS]; reasoned mechanism links, not author-demonstrated):

| challenge_id | argument_text | mechanism_components | source |
|---|---|---|---|
| C1 | "Crossing judge backbones with agent backbones over the same traces (M6), with judge–agent relatedness controlled, decomposes 'which model is being diagnosed' from 'which model is doing the diagnosing' — turning the conflation into an estimated variance share instead of an assumption." | [M6] | inferred |
| C2 | "Holding the task, scaffold, and injected fault fixed while swapping only the executing backbone (M1+M2) measures behavioral divergence in fault manifestation directly; per-layer accuracy against the injection record (M5) then shows whether divergent manifestations still map back to the injected layer." | [M1, M2, M5] | inferred |
| C3 | "Reporting the failure-overlap rate as a first-class result, using Krippendorff's α for missing cells, and calibrating fault lethality in the pilot (M5 with M1) makes the censoring structure visible and keeps the agreement statistic defined over an explicitly characterized subsample rather than a silent one." | [M1, M5] | inferred |
| C4 | "A single pre-registered codebook with explicit decision rules and an earliest-decisive-layer tie-break (M3), validated by human–human κ before use, pins the label definition so residual disagreement is more attributable to backbone effects than to shifting category boundaries." | [M3] | inferred |
| C5 | "Judging raw vs style-normalized/paraphrased traces (M4) directly quantifies the surface-style share of disagreement instead of leaving it as a confound." | [M4] | inferred |

**unaddressed_challenges**: [C4] — [HYPOTHESIS] partially addressed only: a codebook reduces but cannot eliminate the fact that some failures genuinely span layers; the design measures sensitivity to the tie-break rule (re-scoring under an alternative rule) but does not resolve the ontological ambiguity itself.

**Staged plan + feasibility** [HYPOTHESIS]:
- **Pilot compute**: 180 cells × 4 backbones × 1 seed = 720 agent runs (~10–40 tool-calling steps each) + ~600 failing-trace judge calls ≈ low-$10^2 USD API class; 1–2 person-weeks of engineering (injectors + harness).
- **Scale-up compute**: 900 cells × 7 backbones × 3 seeds ≈ 18,900 agent runs; × 3 judges × 2 (raw/normalized) ≈ ~90k judge calls ≈ $10^3–low-$10^4 USD API class; open-weight backbones served on 1–2 H100 nodes for ~1–2 GPU-weeks. Human annotation: 200 traces × 2 annotators × ~8 min ≈ 55 annotator-hours.
- **Single biggest feasibility risk**: censoring (C3) — strong backbones recover from injected faults, leaving too few all-backbone-failing cells to power the agreement analysis. **Mitigation**: pilot explicitly measures per-fault lethality and iterates injector payloads toward "irrecoverable-by-design" faults (e.g., tool returns self-consistent but wrong data); Stage 2 target is ≥60% failure-overlap, and Krippendorff's α plus per-pair agreement on partial overlaps are pre-specified fallbacks.

**V-08 note**: every node from N5 through N6 is `source=inferred`; all challenge-argument confidence is capped at "reasoned prediction," not "author-demonstrated mechanism."

**status**: PARTIAL (reasoned methodology design for a study not yet run; no author-reported methodology exists).
**absence_comment**: {"what_missing": "No real Methods section exists because no experiment has been executed; every component (M1–M6), the staged plan, and the feasibility budget are reconstructed design choices, not extracted text.", "why_matters": "A reviewer cannot check M1–M6 against an actual implementation yet — compute budgets and censoring-risk numbers are estimates, not measurements.", "implication": "Replace with the real Methods section once the pilot/skeleton is run; the R2 instrument-validation plan added to paper.md (Phase A re-run) must be checked against what the skeleton actually produces."}

*(absence_comment added at Phase A re-run — guidance.md Part 6 self-check / goal.md §3 item 1: N6 previously had no status/absence_comment block even though every field is non-GIVEN.)*

---

## N7 Contributions

| id | text | source | contribution_type | is_testable | has_rq |
|---|---|---|---|---|---|
| CO1 | [HYPOTHESIS] "A measurement protocol for cross-backbone stability of LLM-agent failure attribution: fixed fault-injection suite + multi-backbone execution + fixed pre-registered labeling + chance-corrected agreement and censoring metrics." | inferred | conceptual_framework | true | true |
| CO2 | [HYPOTHESIS] "An empirical measurement of the cross-backbone agreement of plan/tool/execution attribution labels on a controlled fault-injection suite, reported overall, per layer, and per family pair — informative regardless of whether agreement is high or low." | inferred | empirical_finding | true | true |
| CO3 | [HYPOTHESIS] "A judge×agent factorial decomposition separating agent-backbone-driven from judge-backbone-driven attribution instability, with a quantified surface-style share via trace normalization." | inferred | empirical_finding | true | true |
| CO4 | [HYPOTHESIS] "Actionable scoping guidance: if attribution is model-specific, single-backbone failure-attribution claims (e.g., those built on Who&When-style benchmarks or MAST-style taxonomies) should be reported as (task, backbone)-pair properties, with the released suite enabling per-backbone re-validation." | inferred | conceptual_framework | false | false |

**status**: PARTIAL (contributions are pre-registered targets, not yet demonstrated).
**absence_comment**: {"what_missing": "No paper exists yet, so none of CO1–CO4 has been demonstrated; each is a planned deliverable contingent on the pilot/Stage-2 runs described in N6.", "why_matters": "A reader must not treat CO1–CO4 as accomplished contributions; CO2/CO3 are conditional on which κ band and variance shares are actually measured.", "implication": "Re-verify each CO against `verdicts.json`/`claim_map.md` once Phase D runs; CO4 in particular only survives if H1's band is 'model-specific' or 'partially stable'."}

*(absence_comment added at Phase A re-run — guidance.md Part 6 / goal.md §3 item 1.)*

---

## N8 Research Questions

- **RQ1** [GIVEN, near-verbatim restatement of the seed's 核心问题]: id="RQ1", text="For the same task failure, does the failure attribution (plan / tool / execution) land on the same layer after the underlying LLM backbone is swapped? If attribution is highly model-specific, then 'diagnosis' reflects a property of the model rather than a property of the task." source=extracted (verbatim from seed), rq_source="explicit", evaluates_mechanisms=[M1, M2, M3, M5], addresses_challenges=[C2, C3], tests_contributions=[CO1, CO2], answered_by_experiment="[GIVEN] 同一故障注入任务集跑多个模型家族，测归因标签的跨模型一致率 — operationalized as the pilot + Stage 2 design: identical fault-injection suite across 4–8 model families, fixed judge, pairwise agreement + Fleiss' κ + Krippendorff's α on the failing-cell intersection."

- **RQ_INF_1** [HYPOTHESIS, inferred — fault injection implies ground truth, suggesting a stability-vs-correctness question]: id="RQ_INF_1", text="Does cross-backbone attribution consistency track accuracy against the injected ground-truth fault layer, or can labels be consistently wrong across all backbones (stable but inaccurate)?" source=inferred, rq_source="inferred", evaluates_mechanisms=[M1, M5], addresses_challenges=[C4], tests_contributions=[CO2], answered_by_experiment="[HYPOTHESIS] per-backbone label accuracy vs the M1 injection record, cross-tabulated against pairwise agreement; report the joint distribution (agree-correct / agree-wrong / disagree) per layer."

- **RQ_INF_2** [HYPOTHESIS, inferred from the C1 confound]: id="RQ_INF_2", text="How much of the observed attribution instability is attributable to the agent backbone vs the judge backbone vs task vs surface style?" source=inferred, rq_source="inferred", evaluates_mechanisms=[M3, M4, M6], addresses_challenges=[C1, C5], tests_contributions=[CO3], answered_by_experiment="[HYPOTHESIS] 3-judge × K-agent factorial over the same traces, raw vs style-normalized, fit with a cross-classified mixed-effects model; variance shares with bootstrap CIs; human-codebook subset anchors judge validity."

- **RQ_INF_3** [HYPOTHESIS, inferred from the family-vs-capability design choice]: id="RQ_INF_3", text="Is cross-backbone agreement structured by model *family* (same-vendor pairs agree more) or by *capability tier* (similarly strong models agree more), and is the failure-overlap (censoring) pattern itself backbone-capability-dependent?" source=inferred, rq_source="inferred", evaluates_mechanisms=[M2, M5], addresses_challenges=[C3], tests_contributions=[CO2, CO4], answered_by_experiment="[HYPOTHESIS] Stage-2 backbone grid crossing family with size; compare within-family vs cross-family pairwise agreement and per-backbone fault-recovery rates."

**datasets** [HYPOTHESIS — real, named, fitting benchmarks; the suite is built *over* them]: names=["GAIA (level 1–2 tool-use/assistant tasks; base tasks for injection)", "WebArena (reproducible web-agent tasks; base tasks for tool/execution injection)", "Who&When (naturally-failed multi-agent logs from [Who&When, OpenReview:GazlTYxZss]; used as an organic-failure complement to check synthetic-fault findings)", "the released B2.3 fault-injection suite itself (new artifact: injection records + traces + labels)"], source=inferred, location=N/A.

**baselines** [HYPOTHESIS — named, drawn from N3]: names=["Who&When all-at-once LLM-judge attribution (from [Who&When, OpenReview:GazlTYxZss])", "Who&When step-by-step LLM-judge attribution (same source; the two protocols bracket context-granularity effects)", "AgenTracer-style counterfactual-replay labeling (from [AgenTracer, OpenReview:l05DseqvuD]; causal reference labeler on a subset, replay budget permitting)", "chance-level agreement (label-marginal-preserving permutation)", "majority-vote-across-backbones pseudo-consensus"], source=inferred, location=N/A.

**metrics** [HYPOTHESIS — with definitions]: names=["pairwise cross-backbone agreement = fraction of jointly-failing (task,fault) cells where two backbones' traces receive the same layer label", "Fleiss' κ = chance-corrected agreement across all K backbones on all-failing cells", "Krippendorff's α = chance-corrected agreement tolerating missing (recovered) cells", "attribution accuracy = fraction of labels matching the M1 injected layer", "failure-overlap rate = fraction of cells failing under all K backbones (censoring indicator)", "variance shares = proportion of label-match variance from agent/judge/task/interaction random effects", "style-share = drop in cross-backbone disagreement after M4 normalization"], source=inferred, location=N/A.

**analysis plan** [HYPOTHESIS]: sample size: pilot 180 cells (~600 failing traces), Stage 2 900 cells × ≥6 backbones × 3 seeds (~10–14k failing traces; >0.9 power to detect κ differences of 0.1 between layers at α=0.05 under pilot-estimated base rates). Statistical tests: bootstrap CIs (10,000 task-level cluster resamples) on κ/α; pre-registered decision threshold κ<0.6 = "model-specific", κ≥0.8 = "stable", between = "partially stable"; per-layer differences via mixed-effects logistic regression (match ~ layer + pair_type + (1|task)), Holm-corrected, significance p<0.05; variance decomposition via cross-classified random effects with likelihood-ratio tests. Expected effect direction: overall κ in 0.3–0.6; execution > tool > plan consistency; judge-backbone variance share >20%; within-family agreement > cross-family.

**status**: PARTIAL (pre-registered RQ/dataset/baseline/metric/analysis plan; no data collected).
**absence_comment**: {"what_missing": "RQ1/RQ_INF_1-3 and their datasets/baselines/metrics/analysis plan are pre-registered design choices, not extracted from a real Research-Questions section, because no paper exists.", "why_matters": "The per-cell power/INCONCLUSIVE pre-declaration and the cross-family aggregation rule added to paper.md's Step 6 at the Phase A re-run must be read together with this node's analysis plan — they refine it, they do not replace it.", "implication": "Once Phase B/C run, re-derive this node's numbers from `results/*.json` rather than the pre-registered estimates here."}

*(absence_comment added at Phase A re-run — guidance.md Part 6 / goal.md §3 item 1.)*

---

## N9 Results — PLACEHOLDER, HYPOTHESIZED DIRECTION ONLY (no real numbers exist)

**CRITICAL**: No experiment has been run. Each row states a predicted *direction*, never a measured value. `evidence_strength="missing"` and `rq_answered=false` for all rows — the honest state of a not-yet-conducted study.

| rq_id | result_text | result_type | evidence_strength | rq_answered | source |
|---|---|---|---|---|---|
| RQ1 | [PLACEHOLDER — HYPOTHESIZED DIRECTION] "Cross-backbone agreement is predicted to be substantially below-perfect (κ in the 0.3–0.6 band) and layer-dependent: execution-layer faults attributed most consistently (mechanically legible traces, e.g., a tool call literally erroring), plan-layer faults least (model-dependent interpretive judgment). **Refuted if** measured Fleiss' κ ≥ 0.8 (and pairwise agreement >90%) uniformly across layers and family pairs — which would itself be the informative 'diagnosis is a task property' outcome the seed anticipates." | quantitative | missing | false | inferred |
| RQ_INF_1 | [PLACEHOLDER — HYPOTHESIZED DIRECTION] "Consistency and ground-truth accuracy are predicted to move together but imperfectly: a non-trivial agree-but-wrong mass (backbones jointly mislabeling cascaded tool faults as plan faults) is expected, showing stable ≠ correct. **Refuted if** the agree-wrong cell is negligible (<5% of jointly-failing cells) across all layers, i.e., agreement and accuracy track each other near-perfectly." | quantitative | missing | false | inferred |
| RQ_INF_2 | [PLACEHOLDER — HYPOTHESIZED DIRECTION] "The judge backbone is predicted to contribute a non-trivial variance share (>20%) of label instability, and style normalization (M4) is predicted to remove a measurable part of apparent agent-backbone disagreement. **Refuted if** judge-backbone variance share is ≈0 (judges interchangeable) and normalization leaves disagreement unchanged — implying instability is genuinely agent-behavioral." | quantitative | missing | false | inferred |
| RQ_INF_3 | [PLACEHOLDER — HYPOTHESIZED DIRECTION] "Within-family backbone pairs are predicted to agree more than cross-family pairs, and stronger backbones are predicted to recover from more injected faults (higher censoring), making the analyzable failure set capability-skewed. **Refuted if** agreement is unstructured by family/tier and fault-recovery rates are uniform across backbones." | quantitative | missing | false | inferred |

**status**: NOT_FOUND (no data collected yet).
**absence_comment**: {"what_missing": "No experiment has been executed, so there are no real agreement rates, κ/α values, variance shares, or per-layer breakdowns.", "why_matters": "The hypothesized directions above must not be mistaken for findings; each carries an explicit falsification condition instead of evidence.", "implication": "Re-run this node once the pilot (Stage 1) is executed; the pre-registered thresholds in N8's analysis plan are the decision rules."}

---

## N10 Threats / Self-Limitations

(All [HYPOTHESIS] — anticipated threats for this design, categorized per validity type; no author-stated limitations exist yet.)

| threat_id | category | description | mitigation | source |
|---|---|---|---|---|
| t1 | construct | "The plan/tool/execution taxonomy is a simplification — some failures genuinely span layers — so 'attribution consistency' partly measures codebook tie-break behavior rather than a natural property (echoes C4)." | "Pre-registered codebook with explicit earliest-decisive-layer tie-break; human–human κ ≥0.7 gate before use; sensitivity re-scoring under an alternative tie-break rule reported alongside the main numbers." | inferred |
| t2 | internal | "If the attribution procedure is LLM-based, judge noise and judge–agent relatedness (a Preference-Leakage-style confound) can masquerade as cross-backbone instability; conversely, a judge trained on traces resembling one family's style may systematically favor it." | "M6 judge×agent factorial with vendor-disjoint judges; M4 style normalization ablation; 200-trace human-codebook anchor to bound judge validity." | inferred |
| t3 | external | "Findings from a handful of backbones, one scaffold, and synthetic injected faults may not generalize to other model generations, agent architectures, or organically arising failures." | "Backbone grid crosses family × capability tier; Who&When organic failure logs analyzed as a complement to synthetic faults; scaffold and injectors released so others can re-run under new configurations." | inferred |
| t4 | conclusion | "Clustered, censored data threatens inferential validity: agreement statistics computed on the all-failing intersection are a selected subsample (C3), repeated cells share tasks, and many per-layer/per-pair comparisons invite false positives." | "Failure-overlap rate reported as a first-class quantity; Krippendorff's α for partial cells; task-level cluster bootstrap; Holm correction across the pre-registered comparison family; power analysis from pilot base rates." | inferred |
| t5 | reproducibility | "Closed-weight backbones drift across provider versions, so the exact agreement numbers may be irreproducible months later." | "Pin model version identifiers and dates; include ≥3 open-weight backbones with frozen checkpoints so the core comparison is re-runnable; release all traces so re-judging never requires re-execution." | inferred |
| t6 | internal | "Prompt-fit confound: one fixed scaffold/prompt may simply suit some backbones better, so 'fault manifestation divergence' partly reflects prompt–model mismatch rather than intrinsic backbone behavior." | "Report per-backbone clean-run (no-injection) success rates as a fit covariate; restrict headline analysis to tasks all backbones solve fault-free." | inferred |

**status**: PARTIAL — forecasted threats for this study design, not author-stated limitations (no paper exists).
**absence_comment**: {"what_missing": "No Threats-to-Validity/Limitations section exists in an actual paper.", "why_matters": "These are anticipated categories with planned mitigations, not confirmed self-critique.", "implication": "Replace with the real Limitations section once written; check for threats not anticipated here (e.g., API cost forcing a smaller backbone grid)."}

---

## N11 Artifacts

**status**: NOT_FOUND — nothing has been released because the paper does not exist yet. [PLACEHOLDER]

- **artifacts**: []
- **has_code**: false [PLACEHOLDER]
- **has_data**: false [PLACEHOLDER]
- **has_model**: false [PLACEHOLDER]

**absence_comment**: {"what_missing": "No code, data, or model artifacts exist because this is a pre-writing scaffold for a study that has not been conducted.", "why_matters": "Readers should not expect the fault-injection suite, traces, or analysis code to be discoverable anywhere yet.", "implication": "Once implemented, release the injection records, normalized traces, labels, and analysis code as artifacts — this directly services threats t4/t5 in N10 and contribution CO4."}

---

## N12 Contribution Type

- **value**: `empirical` [HYPOTHESIS]
- **rationale** [HYPOTHESIS]: "Re-checked against the enum and the disambiguation rules. The core deliverable N9 would validate is a *measurement finding* about an existing phenomenon — whether automated failure attribution generalizes across backbones — obtained by running existing model families through a controlled suite and computing agreement statistics; this matches the 'we compared N models on suite X → empirical (it's a study)' pattern, and matches the classification of the closest exemplar digests (Emergent-Abilities-Mirage: metric-artifact measurement → empirical; LLMs-Get-Lost: multi-model degradation measurement → empirical). The fault-injection suite is a candidate `benchmark`/`dataset` classification, but — exactly as in LLMs-Get-Lost, where the released sharded datasets support the measurement rather than being the primary claim — the suite here exists to support the stability measurement (CO2/CO3 are the headline contributions, both empirical_finding), so the whole-paper value stays `empirical`, not `benchmark`."
- **source**: inferred

**status**: PARTIAL (classification reasoned by analogy to exemplar digests; no author self-classification exists).
**absence_comment**: {"what_missing": "No paper exists to state its own contribution type; the `empirical` value is inferred from the pre-registered design, not extracted from a real N12 statement.", "why_matters": "The archetype gate in paper.md Step 2 and stage_review.md's Analysis/Finding evidence bar both depend on this classification holding through Phase D; a global pivot (F-G1) would flip it toward conceptual_framework/benchmark.", "implication": "Re-confirm N12 after Phase D — if F-G1 fires, update this node's value alongside the pivoted abstract."}

*(absence_comment added at Phase A re-run — guidance.md Part 6 / goal.md §3 item 1.)*

---

## Claims

1. [HYPOTHESIS, grounded] "Automated failure attribution for LLM-agent systems is an established, benchmarked task — but its cross-backbone generalizability is an open, untested assumption: the attribution line ([Who&When, OpenReview:GazlTYxZss], [AgenTracer, OpenReview:l05DseqvuD], [MAST, arXiv:2503.13657]) validates labels within fixed execution stacks, and the judge-reliability line ([PreferenceLeakage, OpenReview:grIvSXVJ65], [BiasScope, OpenReview:QGOw6AU8Lp], [MENLO, OpenReview:QOWYX3Q2XS]) documents evaluator non-invariance on other axes without touching the backbone axis for trace attribution." — evidence: [{type: "argument", text: "N4's limitation table, each row tied to the cited paper's own stated scope/method text from the corpus", source: inferred, location: "N3/N4"}]

2. [HYPOTHESIS] "Cross-backbone attribution instability, if observed, has two separable sources — the backbone that produced the failure and the backbone that judged it — and only a judge×agent factorial with style normalization (M4+M6) can apportion them; single-judge designs cannot distinguish 'diagnosis is model-specific' from 'the judge is noisy'." — evidence: [{type: "argument", text: "N5 C1/C5 + N6 M4/M6 mechanism reasoning", source: inferred, location: "N5/N6"}]

3. [HYPOTHESIS] "Failure-set censoring is a first-order methodological obstacle, not a nuisance: stronger backbones recover from injected faults, so the very set of failures available for agreement computation is backbone-dependent, and any headline consistency number is uninterpretable without the failure-overlap rate reported beside it." — evidence: [{type: "argument", text: "N5 C3 + N6 M5 + feasibility-risk analysis", source: inferred, location: "N5/N6"}]

4. [PLACEHOLDER] "The measured cross-backbone agreement — whatever it turns out to be — is informative either way: κ≥0.8 validates diagnosis as a task property; κ<0.6 shows diagnosis is partly a model property, per the seed's own explicit framing ('结论无论正反都有信息量')." — evidence: [{type: "citation", text: "结论无论正反都有信息量 (seed README, 最小实验 line); thresholds from N8's pre-registered analysis plan", source: extracted, location: "seed README / N8"}]

5. [HYPOTHESIS] "If attribution proves model-specific, single-backbone failure-diagnosis claims in the B2 line (and benchmarks/taxonomies such as Who&When and MAST) should be re-scoped as properties of (task, backbone) pairs, reporting which backbone(s) the diagnosis was validated against — and the released suite makes that re-validation cheap." — evidence: [{type: "argument", text: "derived from N7 CO4 and N2 motivation reasoning", source: inferred, location: "N7/N2"}]
