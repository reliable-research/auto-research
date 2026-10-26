# Digest: When the Evidence Lies: Attribution under Corrupted Tool Observations

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet. This digest projects
> what an N0–N12 structured digest *would* look like if a paper answering topic **B2.5** (标签:
> [机制], parent: "B2. 失败归因（plan / tool / execution）") had been written. Every field below is
> tagged inline:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README (title, core question, minimal
>   experiment, gap-type label).
> - **[HYPOTHESIS]** — reasoned elaboration grounded in the seed + standard practice for this
>   kind of study. A prediction, not a fact.
> - **[GROUNDED:corpus]** — a REAL paper retrieved from the local OpenReview corpus
>   (`topics/corpus/ideas.jsonl`); its `approach_summary` is grounded in that paper's own
>   motivation/method text. The paper is real; its *relevance framing* to B2.5 is my judgment.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is done (authors, DOI, numbers,
>   artifacts). Never invented.

---

## N0 — Metadata

- `title`: "When the Evidence Lies: Attribution under Corrupted Tool Observations" **[GIVEN]** (verbatim from seed README, itself the seed's English rendering of 观测污染的归因盲区 / B2.5)
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — paper does not exist; no author list can be known.
- `abstract` **[HYPOTHESIS]** (drafted by synthesizing the core question + minimal experiment into abstract prose; explicitly a draft, not a real abstract):
  > "Automated failure attribution for LLM agents — deciding whether a failed trajectory should be
  > blamed on the plan, a tool, or the execution layer — implicitly treats the trajectory log as
  > trustworthy evidence. We ask what happens when the evidence itself lies: when the true root
  > cause is a tool that returned a semantically wrong but syntactically/schema-valid observation.
  > We build a controlled fault-injection testbed that corrupts the semantic content of tool
  > observations while preserving format validity, verifies via counterfactual replay that each
  > injected corruption is the decisive cause of failure, and runs representative attribution
  > methods (LLM-judge variants from the Who&When line of work, a trained tracer, and a runtime
  > monitor) over the corrupted trajectories. Against matched controls — overt tool errors and
  > genuine plan failures — we measure each method's misattribution rate and direction, and probe
  > the mechanism by testing whether an explicit 'tools may be unreliable' license in the judge
  > prompt reduces the bias. We hypothesize a systematic skew toward blaming the plan layer,
  > rooted in the structural assumption that well-formed tool output is ground truth."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"AI/ML"` **[HYPOTHESIS]** (LLM agents, tool use, failure diagnosis; AI/ML is the best single fit)

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No authors or verbatim abstract exist because the paper has not been written.", `why_matters`: "N0 identity fields are load-bearing for downstream tools (se-paper-reviewer, pengsida-paper-writer) that key off title/authors/abstract.", `implication`: "Treat all N0 content except `title` as a scaffold placeholder to be overwritten once a real manuscript exists."}

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]** (full predicate, built directly from the core question): "measure,
  via controlled fault injection into tool observations with counterfactual-replay-verified ground
  truth, whether existing LLM-agent failure-attribution methods (LLM-judge trajectory reviewers,
  trained tracers, runtime monitors) misattribute responsibility away from the tool layer when a
  tool call returns a semantically incorrect but syntactically/schema-valid result — and
  characterize the rate, the direction (toward plan vs. toward execution), and the mechanism of
  that misattribution across attribution approaches, corruption types, and agent frameworks."
  - Self-check: KIND = measurement/diagnostic evaluation study; DOMAIN = LLM agent tool-use
    trajectories; OUTCOME shape = a misattribution-rate/direction report over a constructed,
    ground-truth-labeled corruption suite. All three land. **[HYPOTHESIS]**

- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. Agent execution trajectories (task, plan, tool calls, tool observations, final outcome) from
     existing agent benchmarks/environments
  2. A tool-output corruption injector that perturbs semantic content while preserving
     syntax/schema validity, plus a replay harness to verify causal decisiveness
  3. Existing failure-attribution methods (LLM-judge variants, a trained attribution model, a
     runtime supervisor) run unmodified

- `outputs` **[HYPOTHESIS]**:
  1. Per-trajectory attributed failure layer (plan / tool / execution) and step index, per method
  2. Misattribution rate on tool-caused failures, contrasted against overt-error and
     genuine-plan-failure controls
  3. Misattribution direction distribution (share attributed to plan vs. execution), broken down
     by corruption type/locus/severity

- `constraints` **[GIVEN]** (what the seed explicitly states about ground truth / separability):
  "注入语义错误但语法合法的工具输出" — injected corruption must remain syntactically/schema-valid
  so the failure is distinguishable from a parse-time/format error, and the injected corruption
  must be the sole verified root cause (ground truth = tool layer), against which any attribution
  method's output is scored.

**Status:** PARTIAL (objective/inputs/outputs inferred, not extracted from a real paper).
`absence_comment`: {`what_missing`: "No paper text exists to extract an explicit formulation from.", `why_matters`: "Objective/inputs/outputs anchor every downstream node (N6 methodology, N8 RQs).", `implication`: "Treat this formulation as the working hypothesis the eventual paper would need to match or revise."}

---

## N2 — Motivation

**[HYPOTHESIS]** — reconstructed from the seed's parent-topic framing ("B2. 失败归因（plan / tool /
execution）") and from motivations stated by the real N3 corpus papers; no invented statistics:

- `motivation_text`: "Failure attribution is being industrialized: Who&When formalizes it as a
  first-class judging problem because manual log inspection is 'prohibitively expensive and
  inconsistent', and AgenTracer trains dedicated tracers so attribution can drive 'debugging, data
  curation, and iterative self-improvement'. If this attribution layer carries a systematic bias —
  chronically relabeling tool-caused failures as plan or execution failures — every downstream
  intervention it drives (planner retraining, executor retries, data curation) is aimed at the
  wrong component while the actual vulnerability (blind trust in tool output) stays unmonitored."
  **[HYPOTHESIS]**, `evidence`: [{`type`: "citation", `text`: "Who&When motivation text: manual attribution 'prohibitively expensive and inconsistent'; AgenTracer motivation text: attribution as 'the missing interface between failure observation and system improvement'", `source`: "extracted (from corpus records GazlTYxZss, l05DseqvuD)", `location`: null}]
- `motivation_text`: "The corrupted-but-well-formed tool observation is not an exotic fault mode:
  the agent-security literature (ChatInject, MCP-SafetyBench) shows the tool-return channel is an
  actively exploited attack surface, and the robustness literature (ResiliBench) shows tool
  unreliability is pervasive even without attackers — yet those lines measure attack success or
  task-completion resilience, never whether post-hoc diagnosis correctly localizes the root cause.
  A stale API result, a subtly wrong retrieval, or a poisoned tool return thus lands exactly in
  the blind spot between the attribution literature and the robustness literature." **[HYPOTHESIS]**, `evidence`: [{`type`: "citation", `text`: "ChatInject motivation: 'LLM agents are vulnerable to indirect prompt injection because they consume untrusted tool outputs as part of the reasoning context'; ResiliBench motivation: 'APIs timeout, validation fails, services become temporarily unavailable'", `source`: "extracted (from corpus records WVhgFSKniL, KTZ56LG7jZ)", `location`: null}]

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper prose exists to quote motivation verbatim from; the evidence quotes come from the corpus papers' own motivations, not from this hypothetical paper.", `why_matters`: "Motivation framing determines how a reviewer judges the stakes of the study.", `implication`: "Treat the above as a motivation sketch whose citations are real but whose synthesis is mine; revisit once real framing exists."}

---

## N3 — Related Works

Corpus grounding: seven keyword searches were run over the local OpenReview corpus
(`topics/corpus/ideas.jsonl`, 11,683 papers) from three keyword angles — (1) the mechanism
(failure attribution / blame assignment / root cause / which agent), (2) the failure mode
(corrupted / noisy / unreliable tool output; prompt injection / tool poisoning; error
propagation), and (3) the evaluation domain (LLM-judge / step-level critic; agent tool-use
benchmarks / stochastic environments). The seven entries below are real corpus papers whose full
motivation+method records were read; one additional non-corpus entry is kept because it is
canonical for this exact topic and is independently cited by three of the corpus papers.

`works`:

1. `citation_key`: "[Who&When, OpenReview:GazlTYxZss]" **[GROUNDED:corpus]** — *Which Agent Causes
   Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems*.
   `approach_summary`: "Formalizes automated failure attribution as identifying decisive errors —
   agent–step pairs whose correction flips a failed trajectory to success — releases the
   human-annotated Who&When dataset of multi-agent failure logs with responsible-agent and
   decisive-step labels, and evaluates LLM-judge attribution under three context-management
   strategies (all-at-once, step-by-step, binary search) plus a hybrid pipeline."
   `paper_url`: https://openreview.net/forum?id=GazlTYxZss
2. `citation_key`: "[AgenTracer, OpenReview:l05DseqvuD]" **[GROUNDED:corpus]** — *AgenTracer: Who
   Is Inducing Failure in the LLM Agentic Systems?* `approach_summary`: "Converts decisive-error
   localization into a trainable prediction problem: generates supervision by counterfactual
   replay (replacing one step at a time with a corrected action until the outcome flips) and by
   programmatic fault injection into agent actions of successful traces, then trains a dedicated
   tracer with RL to predict the responsible agent and earliest decisive step."
   `paper_url`: https://openreview.net/forum?id=l05DseqvuD
3. `citation_key`: "[BreakingAgentBackbones, OpenReview:kga18ld70t]" **[GROUNDED:corpus]** —
   *Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents*.
   `approach_summary`: "Argues that end-to-end agent benchmarks make it 'difficult to attribute
   failures to the backbone LLM rather than to tool wrappers, control flow, retrieval components',
   and answers with 'threat snapshots': isolating a single LLM call with its full context, attack
   insertion mechanism, and success metric to benchmark backbone security with clean attribution."
   `paper_url`: https://openreview.net/forum?id=kga18ld70t
4. `citation_key`: "[ChatInject, OpenReview:WVhgFSKniL]" **[GROUNDED:corpus]** — *ChatInject:
   Abusing Chat Templates for Prompt Injection in LLM Agents*. `approach_summary`: "Constructs
   malicious tool outputs that forge chat-template role tags (system/user delimiters) inside a
   tool response, including a simulated multi-turn dialogue variant, so that low-privilege tool
   content is interpreted as high-privilege instructions — demonstrating that the tool-return
   channel admits structurally disguised corruption beyond plain-text imperatives."
   `paper_url`: https://openreview.net/forum?id=WVhgFSKniL
5. `citation_key`: "[MCP-SafetyBench, OpenReview:7XYjeL46co]" **[GROUNDED:corpus]** —
   *MCP-SafetyBench: A Benchmark for Safety Evaluation of Large Language Models with Real-World
   MCP Servers*. `approach_summary`: "Embeds a 20-type, three-layer (server/host/user) attack
   taxonomy — including tool poisoning and intent injection — into executable multi-turn tasks
   against real MCP servers, with execution-based dual evaluation of task success and attack
   success." `paper_url`: https://openreview.net/forum?id=7XYjeL46co
6. `citation_key`: "[ResiliBench, OpenReview:KTZ56LG7jZ]" **[GROUNDED:corpus]** — *ResiliBench:
   Evaluating Agentic Workflow Adaptation in Stochastic Environments*. `approach_summary`:
   "Builds a simulated API-realistic tool registry where each tool has parameterized probabilistic
   error modes (timeout, invalid input, operational failure, calculation error, overflow) and
   degrades workflow instructions, to measure whether agents adapt multi-step workflows under
   controlled execution uncertainty, with MDP-derived reference workflows as an upper bound."
   `paper_url`: https://openreview.net/forum?id=KTZ56LG7jZ
7. `citation_key`: "[SupervisorAgent, OpenReview:pzFhtpkabh]" **[GROUNDED:corpus]** — *Stop
   Wasting Your Tokens: Towards Efficient Runtime Multi-Agent Systems*. `approach_summary`:
   "Adds a lightweight meta-agent that supervises three high-risk interaction channels
   (agent–agent, agent–tool, agent–memory) at runtime, activated by an LLM-free trigger filter
   (explicit error occurrence, repetitive behavior, excessive observation length) and equipped
   with structured global/local trace context for targeted intervention."
   `paper_url`: https://openreview.net/forum?id=pzFhtpkabh
8. `citation_key`: "[MAST, arXiv:2503.13657]" — **NON-CORPUS, canonical** (Cemri et al., *Why Do
   Multi-Agent LLM Systems Fail?*; cited as @cemri2025mast in the motivation text of corpus
   entries 2, 6-adjacent, and 7, which is the basis of my confidence it exists; not itself in
   ideas.jsonl). `approach_summary`: "Derives MAST, an empirically grounded taxonomy of recurring
   multi-agent failure modes (specification, inter-agent misalignment, verification categories),
   from human annotation of naturally occurring failure traces across mainstream multi-agent
   frameworks." **[HYPOTHESIS]** at the summary level (from memory + corpus papers' descriptions
   of it, not from its own text).

**Status:** FOUND (8 works, 7 grounded in the local corpus with full motivation/method records
read; 1 canonical non-corpus anchor clearly flagged). `absence_comment`: null

---

## N4 — Prior Limitations

**Node fields:** `limitations`, `grounding_check`.

All items **[HYPOTHESIS]** in their framing, but each is defensible from the cited paper's own
motivation/method text (quoted or closely paraphrased) or from what its described method
demonstrably does not cover. `affects_works` strings match N3 `citation_key`s exactly.

1. `limitation_text`: "Who&When's attribution setting takes the trajectory log as faithful
   evidence: its LLM judges 'analyze logs to output the responsible agent and step' over naturally
   failed runs annotated by humans, and its decisive-error definition is exercised on agent
   mistakes — it never controls the condition where the log's own tool observations are
   semantically corrupted yet well-formed, so it cannot say whether its judges (or its human
   annotators) would blame the tool layer or the consuming agent in that condition."
   `affects_works`: `["[Who&When, OpenReview:GazlTYxZss]"]`, `limitation_type`: "generalizability"
2. `limitation_text`: "AgenTracer's programmatic fault injection 'perturb[s] selected actions in
   successful trajectories' — the fault universe is agent-side actions, not environment-side tool
   returns; a tracer trained on action-perturbation labels has, by construction, never seen a
   trajectory whose decisive error is a lying observation, leaving its behavior on tool-caused
   failures unmeasured." `affects_works`: `["[AgenTracer, OpenReview:l05DseqvuD]"]`,
   `limitation_type`: "generalizability"
3. `limitation_text`: "BreakingAgentBackbones diagnoses the attribution problem (end-to-end
   benchmarks can't separate backbone faults from 'tool wrappers, control flow, retrieval
   components') but resolves it by *removing* the full trajectory — isolating single LLM calls for
   security scoring — rather than by testing whether attribution methods operating over full
   trajectories mislocalize tool-caused semantic corruption; the misattribution question is
   motivated, not answered." `affects_works`: `["[BreakingAgentBackbones, OpenReview:kga18ld70t]"]`,
   `limitation_type`: "other"
4. `limitation_text`: "The agent-security benchmarks measure whether an attack embedded in tool
   content *succeeds* (attack success rate, task success), not whether any post-hoc diagnosis
   correctly localizes the corrupted tool return as root cause; moreover their corruptions are
   instruction-bearing payloads designed to redirect behavior, leaving purely semantic data
   corruption (wrong value, right format, no embedded instruction) outside their threat models."
   `affects_works`: `["[ChatInject, OpenReview:WVhgFSKniL]", "[MCP-SafetyBench, OpenReview:7XYjeL46co]"]`,
   `limitation_type`: "other"
5. `limitation_text`: "ResiliBench's tool unreliability is overt by design — parameterized error
   modes like 'timeout, invalid input, operational failure' that surface as visible failures the
   agent must adapt to; it does not model the silent case where the tool *returns a well-formed
   but wrong value*, and it evaluates workflow adaptation/completion, not failure attribution."
   `affects_works`: `["[ResiliBench, OpenReview:KTZ56LG7jZ]"]`, `limitation_type`: "generalizability"
6. `limitation_text`: "SupervisorAgent's trigger filter is deliberately LLM-free and fires on
   'explicit error occurrence, inefficient repetitive behavior, and excessive observation length'
   — precisely the signals a semantically-wrong-but-schema-valid observation does not emit; its
   runtime oversight is therefore structurally blind to the fault mode B2.5 targets."
   `affects_works`: `["[SupervisorAgent, OpenReview:pzFhtpkabh]"]`, `limitation_type`: "recall"
7. `limitation_text`: "MAST's failure taxonomy is distilled from human annotation of naturally
   occurring traces, so the annotators themselves consume the trace as trustworthy evidence; the
   taxonomy categorizes specification/misalignment/verification failures among agents and has no
   controlled mechanism to detect — or even represent — cases where the root cause is corrupted
   observational input rather than agent behavior." `affects_works`: `["[MAST, arXiv:2503.13657]"]`,
   `limitation_type`: "generalizability"

`grounding_check`: `true` — every limitation has a non-empty `affects_works` whose entries appear
verbatim as N3 citation_keys.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "These limitations are reasoned from the cited papers' own motivation/method text as recorded in the corpus, not quoted from any paper's self-stated limitations section.", `why_matters`: "A reviewer should be able to check each limitation against the cited paper's actual scope before accepting the novelty claim built on it.", `implication`: "Treat each limitation as a checkable scope claim: if any cited paper in fact covers semantically-corrupted-but-valid observations, the corresponding N4 entry (and part of the gap) collapses."}

---

## N5 — Challenges

**[HYPOTHESIS, tightly derived from the core question]** — problem-inherent obstacles, not
prior-tool failures (N4-vs-N5 test applied: these hold regardless of which attribution method is
picked). Ids stable with the previous digest revision.

- `id`: "C1", `text`: "Form-invisibility: a semantically-wrong-but-schema-valid tool output is,
  at the level of any surface signal an attribution method can cheaply check (parse success, type
  validity, protocol conformance, exception flags), identical to a correct one — the ground-truth
  root cause emits no marker in the trace." **[HYPOTHESIS]**
- `id`: "C2", `text`: "Evidential circularity: the corrupted observation is simultaneously the
  cause of the failure and part of the evidence the attribution method reads to diagnose the
  failure. Any method (or human annotator) that treats the trace as trustworthy testimony inherits
  the corruption into its own premises — the blind spot is structural, not a rare edge case."
  **[HYPOTHESIS]**
- `id`: "C3", `text`: "Counterfactual entanglement: downstream of a bad observation, the agent's
  mis-plan or mis-execution is causally indistinguishable from a genuine plan/execution defect
  given the trace alone; separating 'reasonable plan given bad input' from 'bad plan given good
  input' requires counterfactual reasoning (what would the step have looked like under a correct
  observation?) plus world knowledge to recognize the observation as wrong — neither of which
  trace-reading pipelines are built to perform." **[HYPOTHESIS]**
- `id`: "C4", `text`: "Layer-ontology mismatch: there is no agreed boundary between 'plan,'
  'tool,' and 'execution' across agent frameworks (e.g., is a tool-selection mistake a plan fault
  or an execution fault? is a retrieval component a tool?), so defining one ground-truth label
  that every compared method's native output can be fairly mapped onto is itself hard."
  **[HYPOTHESIS]**

`conflation_check`: `true` **[HYPOTHESIS]** — C1 (no surface signal), C2 (diagnosis consumes the
corrupted evidence), C3 (counterfactual separation), C4 (label-space mismatch) are distinct.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper text exists to quote a challenges section from.", `why_matters`: "N6's methodology is only as sound as the challenges it claims to address.", `implication`: "Treat C1–C4 as the working challenge list a real paper on this topic would need to at least match."}

---

## N6 — Methodology

**[HYPOTHESIS]** — extrapolated from the seed's minimal experiment ("注入语义错误但语法合法的工具
输出，测主流归因思路的错记率与错记方向"), with injection/replay machinery adapted from
[AgenTracer, OpenReview:l05DseqvuD] (counterfactual replay, fault injection) and attribution
baselines from [Who&When, OpenReview:GazlTYxZss].

**`overview`** **[HYPOTHESIS]**: "Build a controlled fault-injection testbed over existing agent
environments: corrupt one tool observation per trajectory with a schema-preserving semantic
mutation, verify by counterfactual replay that the corruption is the decisive cause of failure
(the uncorrupted twin succeeds), then run existing attribution methods unmodified over the
corrupted trajectories plus two matched control sets (overt tool errors; genuine plan failures)
and score their layer/step outputs against the constructed ground truth. **Staged plan** —
*Pilot (= the seed's minimal experiment)*: one single-agent ReAct-style tool-calling framework,
2 task domains, ~100 verified corrupted trajectories, 3 LLM-judge attribution variants; success
criterion: injection yield >20% and a measurable misattribution rate with CIs. *Scale-up*: 3
frameworks (single-agent tool calling, a MetaGPT/AG2-style multi-agent system, a Who&When-logged
system), ≥300 verified corrupted trajectories per framework, the full corruption-type ablation
grid, the trained-tracer and runtime-monitor baselines, both control conditions, and the
trust-license prompt probe."

**`key_components`** **[HYPOTHESIS]** (ids assigned before challenge_arguments per EX rules):
- `id`: "M1", `name`: "Schema-Preserving Semantic Corruption Injector", `text`: "A library of
  typed mutation operators applied to one tool return per trajectory: numeric perturbation
  (sign/order-of-magnitude/off-by-k on a load-bearing field), same-type entity substitution,
  boolean flip, list truncation/reorder, and stale-value substitution (replay of an earlier call's
  return). Instrumented guarantees: (a) output re-validates against the tool's JSON schema /
  return type, (b) the agent framework's own parser accepts it without error, (c) an LLM
  plausibility screen confirms the corrupted value is not self-evidently absurd in context —
  the screen itself validated per a pre-registered R2 five-step plan (paper.md
  Instrument-validation section: 2 independent human raters on a held-out calibration set,
  κ ≥ 0.7 acceptance, frozen by hash before scale-up).
  Granularity: one injection per trajectory at a controlled step index (early/mid/late tercile),
  logged as (tool, field, operator, step)."
- `id`: "M2", `name`: "Counterfactual-Replay Ground-Truth Oracle", `text`: "Adopts AgenTracer's
  replay logic in reverse: each candidate corrupted trajectory is kept only if (i) the corrupted
  run fails the task's programmatic checker and (ii) the identical run with the original
  observation restored succeeds (same seed/temperature-0 where the framework allows), so the
  injected observation is the verified decisive root cause. Produces the hidden ground-truth
  label (layer=tool, step=injection index); over-generates 3–5x to absorb yield loss."
- `id`: "M3", `name`: "Attribution Method Harness", `text`: "Runs, unmodified and blinded to
  injection metadata, the attribution baselines over each trajectory: Who&When's three LLM-judge
  strategies (all-at-once, step-by-step, binary search) with a fixed judge model; an
  AgenTracer-style trained tracer (or its released checkpoint); a SupervisorAgent-style runtime
  monitor replayed post-hoc as a detector; and a human-annotator reference on a stratified 10%
  subsample. Each method's native output is mapped to (layer ∈ {plan, tool, execution}, step) by
  a pre-registered mapping rubric written per method before results are seen."
- `id`: "M4", `name`: "Misattribution Rate & Direction Analyzer", `text`: "Computes per method:
  layer-attribution accuracy on the corrupted set; misattribution rate (1 − accuracy);
  direction distribution among errors (share blamed to plan vs. execution); step-localization
  accuracy (exact and ±1); and the Δ-trust gap = misattribution rate on semantically-corrupted
  trajectories minus on matched overt-error controls — the study's headline statistic."
- `id`: "M5", `name`: "Corruption-Type Ablation Grid", `text`: "Crossed factors: operator family
  (numeric / entity / boolean / structural / stale) × injection locus (early / mid / late tercile
  of the trajectory) × subtlety (LLM-screened plausible vs. borderline) × task domain; each cell
  populated to a pre-set minimum count so direction-by-type contrasts are estimable."
- `id`: "M6", `name`: "Matched Control & Trust-Probe Conditions", `text`: "Four controls sharing
  tasks and frameworks with the treatment set: (a) overt tool errors (exceptions/timeouts/empty
  returns, ResiliBench-style) — same root-cause layer, visible signal; (b) genuine plan-failure
  trajectories (from Who&When logs or natural failures with verified clean observations) —
  false-positive control; (c) a trust-license prompt variant for each LLM-judge baseline that
  adds one sentence stating tool returns may be silently wrong and must be independently
  sanity-checked — the mechanism probe for the 'why' half of the core question; (d) a
  sham-injection placebo — plan-failure controls passed through the identical
  injection/replay/serialization machinery with an identity mutation (o′_t = o_t), a
  null-by-construction validity arm: any attribution shift on sham-processed vs. untouched twins
  means the harness itself is an artifact source and the run is invalid (paper.md B0-placebo)."

**`challenge_arguments`** **[HYPOTHESIS]**:
- `challenge_id`: "C1", `argument_text`: "M1's three-gate legality instrumentation (schema
  re-validation, native-parser acceptance, plausibility screen) guarantees the corruption emits no
  surface marker, and M2 keeps the ground-truth label hidden from the methods under test — so the
  testbed isolates exactly C1's form-invisibility: methods must diagnose blind, as in the wild.",
  `mechanism_components`: `["M1", "M2"]`
- `challenge_id`: "C2", `argument_text`: "M3 spans methods that differ in how much they trust the
  trace (judges that only read it, a tracer trained on action faults, a monitor keyed to overt
  signals), and M6's trust-license probe manipulates the trust assumption directly: if a
  one-sentence license to distrust observations significantly reduces misattribution, the bias is
  attributable to C2's evidential circularity rather than to capability limits.",
  `mechanism_components`: `["M3", "M6"]`
- `challenge_id`: "C3", `argument_text`: "M2 gives the *experimenter* the counterfactual (the
  uncorrupted twin) that the methods under test lack, making C3 measurable: M4's Δ-trust gap
  against M6's overt-error control quantifies exactly how much attribution degrades when
  counterfactual reasoning is required — but the study measures C3, it does not build a
  counterfactual attribution method that solves it.", `mechanism_components`: `["M2", "M4", "M6"]`
- `challenge_id`: "C4", `argument_text`: "M2 defines ground truth by a physical injection event
  rather than any framework's ontology, and M3's pre-registered per-method mapping rubric (fixed
  before results) plus dual-annotator mapping checks confine C4 to a measured, reported source of
  noise — mitigated, not eliminated.", `mechanism_components`: `["M2", "M3"]`

**`unaddressed_challenges`**: `["C3", "C4"]` **[HYPOTHESIS]** — both are explicitly only
measured/mitigated, not solved, per the arguments above (flagged per V-08).

**Feasibility** **[HYPOTHESIS]**:
- Order of magnitude: pilot ≈ 100 verified corrupted trajectories × 3–5x over-generation ≈ 400
  agent runs + 400 replay runs + 100×3 attribution runs ≈ ~1.5k LLM-heavy episodes. Scale-up ≈
  900 verified trajectories (+2×900 controls) with over-generation ≈ ~8–10k episodes, plus
  ~5k attribution runs (5 methods × conditions). API cost class: low thousands of USD (order
  $1k–$3k) at GPT-4o-class judge pricing, or 1–2 A100-weeks if open-weight backbones are used.
  Annotation: ~40–60 annotator-hours (10% human-reference subsample at ~5 min/trajectory, double
  annotated, plus mapping-rubric adjudication).
- Single biggest feasibility risk: **injection yield** — many semantic corruptions will not flip
  the outcome (agent recovers, field not load-bearing, task checker insensitive), so the verified
  treatment set could starve. Mitigation: target load-bearing fields identified by tracing which
  observation fields the agent's subsequent step actually references; over-generate 3–5x; and
  treat pilot yield (>20%) as an explicit go/no-go gate before scale-up.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper exists to extract a real methodology section from.", `why_matters`: "This is the load-bearing node for judging technical soundness.", `implication`: "Treat M1–M6 and the staged plan as a design proposal to be validated at the pilot gate, not as an implemented system."}

---

## N7 — Contributions

**[HYPOTHESIS]** — what such a paper would claim, framed from the method + expected findings:

- `id`: "CO1", `text`: "A counterfactual-replay-verified benchmark of schema-valid semantic
  corruptions of tool observations (with matched overt-error and genuine-plan-failure controls)
  for measuring failure-attribution reliability in LLM agents." `contribution_type`: "dataset",
  `is_testable`: true, `has_rq`: true (RQ1)
- `id`: "CO2", `text`: "An empirical measurement of the misattribution rate and direction (toward
  plan vs. execution) of representative attribution methods — Who&When-style LLM judges, a trained
  tracer, a runtime monitor — when the verified root cause is a corrupted tool observation,
  contrasted against overt-error controls (the Δ-trust gap)." `contribution_type`:
  "empirical_finding", `is_testable`: true, `has_rq`: true (RQ1, RQ_INF_1)
- `id`: "CO3", `text`: "A characterization of how misattribution direction depends on corruption
  type, locus, and subtlety, identifying which corruption characteristics most reliably evade
  which class of attribution method." `contribution_type`: "empirical_finding", `is_testable`:
  true, `has_rq`: true (RQ_INF_1)
- `id`: "CO4", `text`: "Mechanism evidence for *why* the bias arises: an intervention showing
  whether a minimal trust-license change to the judge prompt (license to treat observations as
  fallible) reduces misattribution — separating the trust-assumption explanation (C2) from a raw
  capability explanation, and yielding a concrete, tested design recommendation."
  `contribution_type`: "empirical_finding", `is_testable`: true, `has_rq`: true (RQ_INF_2)

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper text to quote contributions verbatim from.", `why_matters`: "Contributions anchor N8's `tests_contributions` cross-references.", `implication`: "Revisit once actual findings exist — CO4 in particular flips from 'mechanism evidence' to 'null result' if the trust-license probe shows no effect."}

---

## N8 — Research Questions

- `id`: "RQ1" **[GIVEN]** (near-verbatim restatement of the seed's 核心问题): "When a failure
  originates from a tool returning a semantically incorrect but syntactically/format-valid
  observation, do existing failure-attribution methods systematically misattribute responsibility
  to the plan or execution layer — at a rate exceeding their error rate on matched overt tool
  errors — and why?" `rq_source`: "explicit" (given by the seed, not extracted from a manuscript).
  `evaluates_mechanisms`: `["M1","M2","M3","M4","M6"]`, `addresses_challenges`: `["C1","C2","C3"]`,
  `tests_contributions`: `["CO1","CO2"]`, `answered_by_experiment`: "Treatment-vs-control design:
  per method, layer-attribution accuracy on ≥300 verified corrupted trajectories per framework vs.
  matched overt-error controls; the seed's minimal experiment is the pilot instantiation."

- `id`: "RQ_INF_1" **[HYPOTHESIS]** (the seed's minimal experiment asks for both a rate *and* a
  direction, implying this second question): "When misattribution occurs, is it directional —
  disproportionately toward the plan layer vs. the execution layer — and does the direction depend
  on corruption type, injection locus, and subtlety?" `rq_source`: "inferred",
  `evaluates_mechanisms`: `["M4","M5"]`, `addresses_challenges`: `["C3","C4"]`,
  `tests_contributions`: `["CO2","CO3"]`, `answered_by_experiment`: "Direction distribution among
  misattributed cases, cross-tabulated over the M5 grid."

- `id`: "RQ_INF_2" **[HYPOTHESIS]** (operationalizes the '为什么' clause of the core question):
  "Is the misattribution driven by the structural trust assumption over tool outputs — i.e., does
  a minimal trust-license prompt intervention (explicitly licensing the judge to treat
  observations as fallible) significantly reduce misattribution without harming attribution
  accuracy on genuine plan failures?" `rq_source`: "inferred", `evaluates_mechanisms`:
  `["M3","M4","M6"]`, `addresses_challenges`: `["C2"]`, `tests_contributions`: `["CO4"]`,
  `answered_by_experiment`: "Within-method paired comparison: each LLM-judge baseline run with vs.
  without the trust-license sentence on the same trajectories, scored on both the corrupted set
  (should improve) and the genuine-plan-failure control (should not degrade)."

`datasets` **[HYPOTHESIS]** — `names`: ["Who&When failure logs (human-annotated multi-agent
attribution dataset from [Who&When, OpenReview:GazlTYxZss]; source of genuine-plan-failure
controls and of one logged framework)", "AgentDojo agent environments (email/banking/travel/Slack
tool-calling tasks with programmatic checkers; tool returns are structured and injectable —
referenced as @debenedetti2024agentdojo by [ChatInject, OpenReview:WVhgFSKniL] and
[BreakingAgentBackbones, OpenReview:kga18ld70t])", "GAIA multi-step tool-use assistant tasks
(long-horizon trajectories where single observations are load-bearing — referenced as
@mialon2023gaia by [SupervisorAgent, OpenReview:pzFhtpkabh])", "Newly constructed
corrupted-observation suite (CO1) layered over the above"]

`baselines` **[HYPOTHESIS]** — `names`: ["Who&When all-at-once LLM judge", "Who&When step-by-step
LLM judge", "Who&When binary-search LLM judge", "AgenTracer-style trained tracer",
"SupervisorAgent-style runtime monitor (post-hoc replay as detector)", "Human annotator reference
(10% stratified subsample, double-annotated)"]

`metrics` **[HYPOTHESIS]** — `names`: ["Layer-attribution accuracy: fraction of tool-caused
trajectories whose attributed layer = tool", "Misattribution rate: 1 − layer-attribution accuracy
on the corrupted set", "Δ-trust gap: misattribution rate(semantic corruption) − misattribution
rate(overt-error control), per method", "Direction share: among misattributed cases, proportion
blamed to plan vs. execution", "Step-localization accuracy: attributed step = injection step
(exact and ±1)", "Control false-positive rate: fraction of genuine-plan-failure controls wrongly
blamed on the tool layer", "Inter-annotator agreement on the layer mapping (Cohen's κ)"]

**Analysis plan** **[HYPOTHESIS]**: Sample size — pilot n=100 corrupted trajectories (CIs only,
no hypothesis test); scale-up n≥300 per framework per condition (at a plausible 30% baseline
misattribution rate, n=300/arm gives ~80% power to detect a 10-percentage-point Δ-trust gap at
two-sided α=0.05). Tests — RQ1: per-method two-proportion test (McNemar where trajectories are
paired across treatment/control), Holm–Bonferroni across methods, significance threshold α=0.05;
expected direction: misattribution rate on semantic corruption significantly HIGHER than on overt
errors for every trace-reading method. RQ_INF_1: exact binomial test of plan-vs-execution share
against 0.5 among misattributed cases — scored only at ≥120 misattributed cases per method
(~0.89 power at a true plan-share of 0.65; the 50–119 band is pre-declared INCONCLUSIVE, <50
descriptive only, since n=50 gives only ~0.51 power for that effect size) — plus mixed-effects
logistic regression (fixed effects: operator family, locus tercile, subtlety; random intercepts:
task, framework) for direction-by-type dependence; expected direction: plan share > 0.5. RQ_INF_2: paired McNemar per
judge with vs. without trust license, α=0.05; expected direction: significant misattribution
reduction on the corrupted set with no significant false-positive increase on the plan-failure
control.

**Status:** PARTIAL (RQ1 given by seed; RQ_INF_1/RQ_INF_2, datasets/baselines/metrics/analysis
plan all inferred). `absence_comment`: {`what_missing`: "No explicit evaluation section exists yet.", `why_matters`: "The dataset/baseline/metric/test choices determine what would count as confirming or refuting the hypothesis.", `implication`: "Treat this as a pre-registration-style protocol draft; any substitution (e.g., a different judge model) must preserve the treatment/control pairing."}

---

## N9 — Results — PLACEHOLDER, HYPOTHESIZED DIRECTION ONLY (DO NOT TREAT AS REAL DATA)

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**. No experiment has been run. NO NUMBERS ARE
REPORTED ANYWHERE IN THIS NODE. `evidence_strength` = "missing" and `rq_answered` = false for
every item, by construction.

- `rq_id`: "RQ1", `source`: "inferred", `result_text`: "Predicted direction: every trace-reading
  attribution method shows a positive Δ-trust gap — misattributing tool-caused failures
  substantially more often when the corrupted observation is schema-valid than when the tool
  fault is overt — because well-formed observations are consumed as premises (C2), making the
  downstream step look like an unforced planning error." `result_type`: "quantitative" (once
  run), `evidence_strength`: "missing", `rq_answered`: false.
  **FALSIFICATION CONDITION**: refuted if the Δ-trust gap is statistically indistinguishable from
  zero (or negative) for the majority of methods at α=0.05 — i.e., methods identify the tool layer
  on schema-valid corruptions about as reliably as on overt errors.

- `rq_id`: "RQ_INF_1", `source`: "inferred", `result_text`: "Predicted direction: among
  misattributed cases the blame skews toward the plan layer rather than the execution layer —
  plan-level critique sits directly downstream of reading the corrupted observation, while
  execution-layer verdicts key on mechanical success/failure signals that the schema-valid
  corruption deliberately does not trip; the skew is predicted to strengthen for subtle,
  late-trajectory, numeric/stale corruptions." `result_type`: "quantitative" (once run),
  `evidence_strength`: "missing", `rq_answered`: false.
  **FALSIFICATION CONDITION**: refuted if the plan-vs-execution split among misattributed cases
  does not differ significantly from even (exact binomial, α=0.05), or skews toward execution; the
  type-dependence sub-claim is refuted if no corruption-grid factor is a significant predictor in
  the mixed-effects model.

- `rq_id`: "RQ_INF_2", `source`: "inferred", `result_text`: "Predicted direction: the one-sentence
  trust-license intervention significantly reduces misattribution on the corrupted set without a
  significant false-positive increase on genuine-plan-failure controls — supporting the
  trust-assumption mechanism (C2) over a raw-capability explanation. Secondary prediction: the
  reduction is partial, since recognizing *which* observation lies still requires the
  counterfactual/world-knowledge reasoning of C3." `result_type`: "quantitative" (once run),
  `evidence_strength`: "missing", `rq_answered`: false.
  **FALSIFICATION CONDITION**: refuted if the trust license yields no significant misattribution
  reduction (paired McNemar, α=0.05), or if any reduction is bought with a comparable
  false-positive increase on the plan-failure control (blaming tools indiscriminately).

**Status:** NOT_FOUND (by design — no experiment run). `absence_comment`: {`what_missing`: "All quantitative results.", `why_matters`: "Without them the core question (RQ1) remains open; this section exists only to state falsifiable predicted directions.", `implication`: "Only directions and their falsification conditions are asserted; every number is absent by construction and must never be quoted as a finding."}

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS]** — anticipated limitations of this study design (no real Threats section exists);
each categorized and paired with a planned mitigation:

- `threat_id`: "t1", `category`: "construct", `description`: "The three-way plan/tool/execution
  taxonomy and the per-method output-mapping rubric are constructs; cross-method comparisons risk
  conflating genuine misattribution with taxonomy-mapping noise (C4), and 'misattribution' itself
  is only as valid as the mapping.", `mitigation`: "Pre-register the mapping rubric per method
  before any results are seen; double-annotate the mapping on a subsample and report Cohen's κ;
  run a sensitivity analysis excluding trajectories whose mapping the two annotators dispute."
- `threat_id`: "t2", `category`: "internal", `description`: "The injector's notion of
  'semantically wrong but plausible' is a design choice (which fields, which operators, how
  subtle); the measured misattribution rate could be an artifact of the injection distribution
  rather than a property of the attribution methods.", `mitigation`: "Span five operator families
  crossed with locus and subtlety (M5); report per-cell results, not only aggregates; anchor the
  headline claim to the Δ-trust gap against matched overt-error controls (M6) so injector
  idiosyncrasies difference out."
- `threat_id`: "t3", `category`: "internal", `description`: "If the agent backbone and the
  attribution judge share a model family, self-preference or shared blind spots could inflate or
  deflate misattribution (the judge 'believes' the same corrupted premise the agent believed).",
  `mitigation`: "Cross the judge family against the agent family (at least two backbone families
  in the scale-up) and report misattribution separately for same-family vs. cross-family pairs."
- `threat_id`: "t4", `category`: "external", `description`: "Findings are demonstrated on specific
  frameworks (single-agent ReAct-style, one multi-agent system, Who&When-logged systems), specific
  environments (AgentDojo, GAIA), and specific judge models; the size and direction of the bias
  may not generalize to other architectures, tool ecosystems, or model generations.",
  `mitigation`: "Staged design with three heterogeneous frameworks and two backbone families;
  release the injection suite and harness (CO1) so the measurement is re-runnable on new stacks."
- `threat_id`: "t5", `category`: "conclusion", `description`: "Trajectories within a task/template
  are correlated (same tools, same checker), so treating each trajectory as independent would
  overstate significance; multiple methods × conditions inflate family-wise error.",
  `mitigation`: "Mixed-effects models with random intercepts per task and framework (or
  cluster-robust errors); Holm–Bonferroni across the per-method test family; power analysis fixed
  before scale-up."

**Status:** PARTIAL/anticipated, not extracted. `absence_comment`: {`what_missing`: "No authors' own stated limitations exist because there is no paper.", `why_matters`: "N10 is supposed to be author-acknowledged; here it is necessarily reviewer-anticipated.", `implication`: "Treat t1–t5 (and their mitigations) as design requirements the real study must implement, not limitations it has already handled."}

---

## N11 — Artifacts

**[PLACEHOLDER]** — nothing has been released; the paper does not exist.

`artifacts`: `[]`
`has_code`: `false`
`has_data`: `false`
`has_model`: `false`

**Status:** NOT_FOUND. `absence_comment`: {`what_missing`: "No code repository, dataset, model, or demo exists.", `why_matters`: "Artifact availability is reviewer-relevant reproducibility signal, and CO1 explicitly promises a released injection suite.", `implication`: "Expected and correct for a not-yet-written paper; if the work is conducted, the injection suite + harness + mapping rubrics are the artifacts to demand."}

---

## N12 — Contribution Type

`value`: **"empirical"** **[HYPOTHESIS]**

`rationale` **[HYPOTHESIS]**: "What N9's hypothesized results validate are measurement claims
about how *existing* attribution methods behave under a controlled fault mode — the Δ-trust gap
(RQ1), the direction skew (RQ_INF_1), and the mechanism probe (RQ_INF_2) — mirroring the
structure of measurement studies like 'LLMs Get Lost in Multi-Turn Conversation', where a
constructed simulation environment exists to expose a phenomenon in existing systems. The
injection suite (CO1) is instrumentation for that measurement, not the headline product: no new
attribution method is proposed (ruling out 'system'/'tool'), and the suite's purpose is this
study's treatment/control contrast rather than a general-purpose leaderboard (ruling out
'benchmark' under the disambiguation hint 'we compared N methods on X → empirical'). If a real
paper later centers the released suite and invites method submissions against it, the
classification should be revisited toward 'benchmark'."

**Status:** FOUND (as a reasoned classification of the hypothesized paper; the classification
itself is not a fact about a real paper). `source`: "inferred". `absence_comment`: {`what_missing`:
"No real paper exists to extract a self-declared contribution type from; this is a reasoned
classification from N7/N9's hypothesized content, not an author's own framing choice.",
`why_matters`: "N12 gates which archetype's evidence standard (guidance.md Part 2) the experiment
plan is held to; a wrong classification here would silently relax the wrong bar.", `implication`:
"Re-check this classification once real results exist — per the rationale's own note, a released,
leaderboard-inviting suite would push this toward 'benchmark' instead of 'empirical'."}

---

## Claims

Reviewer-relevant assertions, tagged per methodology:

1. **[GROUNDED:corpus]** "The literature has industrialized both halves of B2.5 separately but
   never crossed them: failure attribution assumes faithful logs ([Who&When,
   OpenReview:GazlTYxZss] judges logs; [AgenTracer, OpenReview:l05DseqvuD] injects faults into
   agent *actions*, not observations; [MAST, arXiv:2503.13657] annotates natural traces), while
   tool-channel corruption work measures attack success or adaptation, not root-cause diagnosis
   ([ChatInject, OpenReview:WVhgFSKniL], [MCP-SafetyBench, OpenReview:7XYjeL46co], [ResiliBench,
   OpenReview:KTZ56LG7jZ]), and runtime monitors trigger only on overt signals ([SupervisorAgent,
   OpenReview:pzFhtpkabh]). The specific condition 'semantically wrong, schema-valid observation
   scored against attribution ground truth' is unoccupied in the searched corpus." `evidence`:
   [{`type`: "observation", `text`: "7 keyword searches over ideas.jsonl (11,683 papers) from
   mechanism/failure-mode/evaluation-domain angles; full motivation+method records of the 7 kept
   corpus papers read; see N3/N4.", `source`: "extracted (true of the search process)",
   `location`: null}]
2. **[HYPOTHESIS]** "Failure-attribution methods are predicted to show a positive Δ-trust gap —
   misattributing tool-caused failures away from the tool layer specifically when the corrupted
   output is schema-valid — because the corrupted observation is consumed as a premise of the
   diagnosis itself (C1, C2)." `evidence`: [{`type`: "argument", `text`: "Derived from N5
   challenges C1/C2 and N9 Result RQ1; the treatment/control design (M6) makes it falsifiable.",
   `source`: "inferred", `location`: null}]
3. **[HYPOTHESIS]** "The misattribution direction is predicted to skew toward the plan layer, and
   the skew to strengthen for subtle, late, numeric/stale corruptions — because plan critique sits
   directly downstream of reading the observation while execution verdicts key on mechanical
   signals the corruption never trips." `evidence`: [{`type`: "argument", `text`: "Derived from N9
   Result RQ_INF_1 and the M5 grid design.", `source`: "inferred", `location`: null}]
4. **[HYPOTHESIS]** "If a one-sentence trust-license prompt change significantly reduces
   misattribution without raising false positives on genuine plan failures, the blind spot is a
   structural trust assumption (C2) rather than a capability ceiling — a cheap, testable design
   recommendation; if it does not, the C3 counterfactual-reasoning account gains support."
   `evidence`: [{`type`: "argument", `text`: "Derived from N9 Result RQ_INF_2's paired
   intervention design.", `source`: "inferred", `location`: null}]
5. **[PLACEHOLDER]** "No paper, dataset, or code currently exists for this study; every
   quantitative figure implied anywhere in this digest is a placeholder pending the actual
   experiment, not a reported result." `evidence`: [{`type`: "observation", `text`: "N9/N11 both
   explicitly NOT_FOUND by construction.", `source`: "extracted (true of this digest itself)",
   `location`: null}]

---

*End of reverse paper-digest for B2.5. Every node above is present per EX-11 even where content is
placeholder. Cross-node ids verified: N4→N3 — all `affects_works` strings ([Who&When,
OpenReview:GazlTYxZss], [AgenTracer, OpenReview:l05DseqvuD], [BreakingAgentBackbones,
OpenReview:kga18ld70t], [ChatInject, OpenReview:WVhgFSKniL], [MCP-SafetyBench,
OpenReview:7XYjeL46co], [ResiliBench, OpenReview:KTZ56LG7jZ], [SupervisorAgent,
OpenReview:pzFhtpkabh], [MAST, arXiv:2503.13657]) appear verbatim as N3 citation_keys; N6
challenge_arguments→N5 ids resolve (C1–C4); N6 mechanism_components→N6 key_components resolve
(M1–M6); N6.unaddressed_challenges ⊂ N5 ids; N8 addresses_challenges (C1–C4) /
tests_contributions (CO1–CO4) / evaluates_mechanisms (M1–M6) all resolve; N9.rq_id values (RQ1,
RQ_INF_1, RQ_INF_2) all exist in N8.*
