# Digest: Breaking the Pin: Adversarial Limits of Constraint Protection under Context Compaction

> **REVERSE-DIGEST NOTICE.** No paper exists yet for this topic. This is speculative
> scaffolding for research planning, constructed by working BACKWARD from an abstract
> research idea (title + core question + minimal experiment) toward the shape a completed
> paper's N0–N12 digest would take. Every field below is tagged inline with a trust level in
> place of the normal `extracted`/`inferred` source values:
>
> - **[GIVEN]** — verbatim/near-verbatim from the seed README (title, core question, minimal
>   experiment, gap-type label). Treat as fact about the *plan*, not about a real paper.
> - **[HYPOTHESIS]** — reasoned elaboration grounded in the seed + standard practice for this
>   kind of adversarial-robustness study. A prediction, not a result.
> - **[GROUNDED:corpus]** — an entry whose factual content (approach, motivation, method) is
>   taken from a REAL paper located in the local OpenReview corpus (`topics/corpus/ideas.jsonl`).
>   The *relevance judgment* is the digester's, but the paper and its summary are real.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is actually done (authors, DOI,
>   numbers, artifacts). Never invented; always left empty/null with a note.
>
> Topic code: **T3.1**. Chinese label: **[边界]** (boundary-type gap). Parent topic: **T3.
> Memory 约束保持（窄环，4 条）** [GIVEN, from README frontmatter].

---

## N0 — Metadata

- `title`: "Breaking the Pin: Adversarial Limits of Constraint Protection under Context
  Compaction" — **[GIVEN]**, verbatim from seed README.
- `authors`: `["Anonymous"]` — **[PLACEHOLDER]**, no paper/authors exist yet.
- `abstract` (drafted, not real — synthesized from the core question + minimal experiment):
  **[HYPOTHESIS]**
  > "Pinning-style defenses aim to keep LLM-agent memory constraints intact across context
  > compaction by re-inserting or otherwise protecting critical content that summarization
  > would otherwise drop. Prior work has shown that an optimization-based injection attack can
  > break through every tested model's pinning defense, but the precise boundary of that
  > failure — how attack strength trades off against defense variant, and at what cost to the
  > attacker relative to the defender — has not been mapped. We sweep an injection
  > optimization-strength parameter against a matrix of pinning defense variants, measuring
  > break-through-rate curves and the resulting attack/defense cost ratio, to characterize
  > exactly where and how cheaply constraint-protection pinning fails under adversarial context
  > compaction."
- `doi`: `null` — **[PLACEHOLDER]**.
- `arxiv_id`: `null` — **[PLACEHOLDER]**.
- `num_pages`: `null` — **[PLACEHOLDER]**.
- `research_area`: `"Security"` — **[HYPOTHESIS]**, inferred from the adversarial
  attack/defense framing (cost-ratio, break-through rate, cheap-failure boundary). A plausible
  secondary tag is `NLP`/`AI/ML` since the substrate is LLM-agent memory, but the paper's own
  framing (attacker vs. defender, failure boundary, cost) reads as a security study of an AI
  system.
- **Status:** `PARTIAL` — abstract exists only as a drafted hypothesis, authors are a
  placeholder.
  - `absence_comment`: `what_missing`: "No author list or verbatim abstract exists because no
    paper has been written for this topic yet." / `why_matters`: "Downstream tools that key off
    N0 (citation formatting, dedup, reviewer routing) cannot rely on this metadata being real."
    / `implication`: "Treat every N0 field as a planning placeholder to be overwritten the
    moment an actual manuscript is drafted."

---

## N1 — Problem Formulation

- `objective` — **[HYPOTHESIS]**, full predicate built directly from the core question:
  "empirically measure, via an adversarial optimization-strength sweep against a matrix of
  pinning-style constraint-protection defense variants, the precise break-through-rate failure
  boundary of memory-pinning defenses for LLM agents under context compaction, and quantify the
  resulting attacker-cost-to-defender-cost ratio at that boundary."
  - Self-check: (1) KIND of task = adversarial measurement / robustness-boundary
    characterization; (2) DOMAIN = LLM-agent memory / context-compaction constraint defenses;
    (3) OUTCOME shape = break-through-rate curves + a cost-ratio number. All three land.
- `inputs` — **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. A set of persistent/pinned constraints (task-critical or safety-critical) an LLM agent
     must obey across a long-horizon session.
  2. A context-compaction (summarization/compression) mechanism that periodically compresses
     conversation/tool history.
  3. A matrix of pinning-style defense variants (verbatim re-injection, redundant multi-copy
     pinning, checksum/tag-verified pinning, structurally isolated protected-memory slots, and
     a no-defense control).
  4. An adversarial injection procedure for crafting attacker-controlled content, parametrized
     by an explicit strength/budget knob.
- `outputs` — **[HYPOTHESIS]**:
  1. Break-through-rate curves as a function of injection optimization strength, one curve per
     defense variant.
  2. A boundary characterization (e.g., minimum strength at which each variant crosses a
     50%/90% break-through threshold — "BT50").
  3. An attacker-cost / defender-cost ratio at the measured boundary.
- `constraints` — **[GIVEN]**, restated from the seed: the prior/original paper's
  optimization-injection attack broke through *all* tested models' pinning defenses — the
  starting premise the new study must be consistent with, not re-derive. A valid experiment
  additionally requires a separable ground-truth oracle for "was the pinned constraint violated
  after compaction" (implicit in measuring a break-through *rate* at all) — **[HYPOTHESIS]**,
  since the seed does not spell out the verification mechanism.
- **Status:** `PARTIAL` — objective/inputs/outputs reconstructed, not stated by an actual
  method section.
  - `absence_comment`: `what_missing`: "There is no written methods section, so
    inputs/outputs/objective are inferred from a one-line core question and one-line minimal
    experiment." / `why_matters`: "The real paper could scope inputs/outputs differently (e.g.,
    output a formal bound instead of empirical curves)." / `implication`: "Use this N1 as a
    planning draft to sanity-check the eventual design, not as ground truth."

---

## N2 — Motivation

**Node field:** `motivations: list[MotivationItem]`

1. `motivation_text` — **[HYPOTHESIS]**, reconstructed from the parent-topic framing "T3. Memory
   约束保持（窄环，4 条）" (Memory constraint preservation, a narrow ring of 4 topics):
   "As LLM agents run longer horizons, context windows must be compacted/summarized, and
   memory-pinning defenses are the proposed mechanism to keep safety-critical or task-critical
   constraints alive through that compaction. If pinning defenses have a cheaply-reachable
   adversarial failure boundary, then a load-bearing safety assumption for long-running agent
   deployments — 'pinned constraints survive compaction' — needs quantitative caveats rather
   than being treated as solved." `evidence`: `[]`.
2. `motivation_text` — **[GIVEN]** premise, restated conservatively: the seed states that "the
   original paper's optimization injection broke through all tested models" — an existing prior
   result already establishes pinning is *not* unconditionally robust; this motivates asking not
   *whether* it fails but *where exactly* and *at what cost*. `evidence`: `[]`.
   - Per task instructions: specifics of "the original paper" beyond this sentence are
     **[PLACEHOLDER]** — which paper, which models, which pinning implementation are unknown and
     must not be invented. The closest public archetype of such an "optimization injection" is
     GCG-style discrete-token attack (see N3), but the identity of the seed's original paper is
     not asserted.
- **Status:** `PARTIAL`.
  - `absence_comment`: `what_missing`: "No real Introduction/Motivation section exists to quote
    incident reports or deployment statistics." / `why_matters`: "Motivation strength cannot be
    fabricated without becoming a hallucinated statistic." / `implication`: "Keep motivation
    qualitative and tied to the seed's own stated premise until real related work is surveyed
    during actual writing."

---

## N3 — Related Works

**Search method.** A keyword search was run over the local OpenReview corpus
(`topics/corpus/ideas.jsonl`, 11,683 papers) from several angles: prompt injection / indirect
prompt injection / LLM-agent security; context compression / memory agents / summarization;
optimization jailbreaks / adversarial suffixes / attack success rate; instruction hierarchy /
constraint following; prompt-injection defense benchmarks. Unlike the general-multidisciplinary
Scholar corpus, this ML-native corpus returned many genuinely on-topic hits; the nine entries
below are grounded verbatim in those papers' motivation/method text. One canonical non-corpus
entry (GCG) is included and clearly marked, as it is the public archetype of the
"optimization injection" premise the seed refers to.

> **PHASE-A FIX — cache-verification gap (goal.md §3 checklist item 2).** This N3 search used a
> *different, general* OpenReview corpus (`topics/corpus/ideas.jsonl`, 11,683 papers) than this
> topic's formal reference-cache harvest, which lives in `discussion/reference_candidates.jsonl`
> (150 candidates, upgraded to the canonical schema in this run). None of the ten citation keys
> below (`ChatInject`, `ThreatSnapshots`, `SlotGCG`, `TAO-Attack`, `GuidedBench`, `TensorTrust`,
> `COMI`, `InfoChannel`, `LightMem`, `GCG`) resolve as records in that cache — spot-checking their
> OpenReview IDs (e.g. `WVhgFSKniL`, `fsW7wJGLBd`, `dyJ0GWpjJB`) against `reference_candidates.jsonl`
> finds no match. Per goal.md's hard gate ("citations only via `selected` cache keys"), the ten
> entries below must be treated as **unverified / pending re-harvest** — real papers, plausibly,
> but not yet cache-resolvable — rather than silently promoted to citable status. This run's cache
> upgrade (Task 1) does contain twelve `selected`, cache-verified records covering overlapping or
> adjacent ground and usable today in their place or alongside a future re-harvest:
> `AgenticSTS2026` (method-twin), `ForensicTrajSig2026`, `FoldAct2025`, `TRAP2026`,
> `GoExploreRedTeam2026`, `GCGDiffusion2026`, `TrustworthyAgenticAI2025`, `RecursiveLM2026`
> (all `adjacent`/`contrast`), and `JailbreakVsFilters2025`, `PackKV2026`, `ClawAgentSecurity2026`
> (`background` structural exemplars). See `paper.md` Step 5's matching caveat and
> `discussion/stage_review.md`'s "Phase A (re-run)" section for the full finding.

**Node field:** `works: list[RelatedWork]`

1. `citation_key`: `"[ChatInject, OpenReview:WVhgFSKniL]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "A template-level indirect prompt-injection attack for LLM agents: it
   wraps malicious tool-output content in forged chat-role delimiters so the model treats
   attacker text as higher-privilege system/user structure, and adds a simulated multi-turn
   variant that embeds a fabricated dialogue history in one payload to inherit multi-turn
   persuasion. Evaluated for attack success and utility degradation in AgentDojo/InjecAgent
   environments against existing prompt- and detector-based defenses."
   `paper_url`: https://openreview.net/forum?id=WVhgFSKniL. `source`: GROUNDED:corpus.
2. `citation_key`: `"[ThreatSnapshots, OpenReview:kga18ld70t]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "'Breaking Agent Backbones' proposes *threat snapshots*, an abstraction
   that isolates a single backbone-LLM call with its full execution context, attack-insertion
   mechanism, attacker objective, and success metric, so backbone security can be scored and
   compared across models without simulating whole agents; attacks are collected via gamified
   crowdsourced red-teaming."
   `paper_url`: https://openreview.net/forum?id=kga18ld70t. `source`: GROUNDED:corpus.
3. `citation_key`: `"[SlotGCG, OpenReview:Fn2rSOnpNf]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "Makes adversarial-token *insertion position* a first-class optimization
   variable for GCG-style jailbreaks: it probes all insertion slots, estimates a Vulnerable Slot
   Score from attention statistics, allocates a token budget across high-vulnerability slots,
   then runs standard discrete token search — expanding the attack search space beyond the
   suffix while keeping GCG's optimization machinery."
   `paper_url`: https://openreview.net/forum?id=Fn2rSOnpNf. `source`: GROUNDED:corpus.
4. `citation_key`: `"[TAO-Attack, OpenReview:XfbBiBG46D]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "An optimization-based jailbreak that replaces GCG's single prefix-target
   loss with a progressive two-stage loss (suppress refusals, then penalize pseudo-harmful
   continuations) and replaces dot-product token ranking with direction-priority token
   optimization, arguing that triggering a target prefix is not equivalent to eliciting a
   genuinely successful attack."
   `paper_url`: https://openreview.net/forum?id=XfbBiBG46D. `source`: GROUNDED:corpus.
5. `citation_key`: `"[GuidedBench, OpenReview:ZVg8y3ibyM]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "Argues jailbreak evaluation lacks an operational success definition;
   couples a curated harmful-query set with GuidedEval, a guideline-based evaluator that
   decomposes each query's success into an explicit checklist of required entities and actions
   and defines a generalized ASR as the average scoring-point completion rate, reducing
   evaluator ambiguity and variance."
   `paper_url`: https://openreview.net/forum?id=ZVg8y3ibyM. `source`: GROUNDED:corpus.
6. `citation_key`: `"[TensorTrust, OpenReview:fsW7wJGLBd]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "Builds an interpretable prompt-injection robustness benchmark from a
   competitive online game where humans author paired attacks (prompt hijacking / extraction)
   and defenses under a verifiable string-comparison objective; filters attacks by
   cross-model transferability and jointly measures robustness and task validity, explicitly to
   capture the robustness-vs-usability trade-off."
   `paper_url`: https://openreview.net/forum?id=fsW7wJGLBd. `source`: GROUNDED:corpus.
7. `citation_key`: `"[COMI, OpenReview:OGDIXDfaN4]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "Frames long-context compression as constrained information selection
   under a fixed token budget, and proposes Marginal Information Gain (query relevance minus
   redundancy) to allocate compression budget across segments and merge tokens into compact soft
   representations — a benign, cooperative model of what lossy context compaction retains and
   discards."
   `paper_url`: https://openreview.net/forum?id=OGDIXDfaN4. `source`: GROUNDED:corpus.
8. `citation_key`: `"[InfoChannel, OpenReview:isFHz8qf20]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "'An Information Theoretic Perspective on Agentic System Design' models the
   compressor in a compressor-predictor agent pipeline as a noisy channel X→Z→Y and measures
   compression quality by mutual information I(X;Z) between source context and compressed
   representation (with an information-rate metric and rate-distortion analysis), giving a
   task-agnostic, predictor-independent view of what a compaction step preserves — under a benign,
   cooperative objective."
   `paper_url`: https://openreview.net/forum?id=isFHz8qf20. `source`: GROUNDED:corpus.
9. `citation_key`: `"[LightMem, OpenReview:dyJ0GWpjJB]"` — **[GROUNDED:corpus]**.
   `approach_summary`: "A lightweight memory-augmented-generation architecture that restructures
   the memory lifecycle: sensory pre-compression, hybrid topic segmentation, topic-aware
   short-term summarization, soft online long-term insertion, and offline 'sleep-time'
   consolidation (dedup/abstraction/conflict-resolution) — a concrete, realistic pipeline for
   preserving persistent constraints across many sessions and compaction events."
   `paper_url`: https://openreview.net/forum?id=dyJ0GWpjJB. `source`: GROUNDED:corpus.
10. `citation_key`: `"[GCG / Zou et al., 2023]"` — **[HYPOTHESIS-GROUNDED, non-corpus canonical]**
   (a real, widely-cited paper; included because it is the public archetype of the seed's
   "optimization injection" premise; not from the local corpus, flagged accordingly).
   `approach_summary`: "'Universal and Transferable Adversarial Attacks on Aligned Language
   Models' — gradient-guided greedy coordinate-descent (GCG) search over adversarial suffix
   tokens that maximizes the likelihood of an affirmative prefix, producing transferable
   jailbreak strings that break aligned models. This is the discrete-optimization-injection
   family the corpus attacks above (SlotGCG, TAO-Attack) extend." `paper_url`:
   `arXiv:2307.15043` (canonical, not corpus-verified). `source`: HYPOTHESIS-GROUNDED.

- **Status:** `FOUND` — nine genuinely on-topic corpus papers plus one clearly-marked canonical
  entry, covering the three legs of the topic (the attack family, the compaction/memory
  substrate, and the evaluation/oracle methodology).
  - `absence_comment`: `null`.

---

## N4 — Prior Limitations

**Node fields:** `limitations: list[Limitation]`, `grounding_check: bool`

Each limitation below is defensible from the cited paper's own motivation/method — either what
it explicitly targets, or what its scope demonstrably does not cover. Because no prior work
studies *pinning under adversarial compaction* directly, these are scope/generalizability
mismatches rather than reported failures.

1. `limitation_text` — **[HYPOTHESIS]**: "ChatInject demonstrates that template-role forgery
   breaks agent defenses in AgentDojo/InjecAgent, but it is a single strong attack evaluated at
   a fixed configuration against plain-text/detector defenses; it does not sweep a continuous
   attack-strength parameter, does not target *memory-pinning* defenses under context
   compaction, and reports no attacker-vs-defender cost ratio — so it cannot locate a failure
   *boundary* or a cost-effectiveness ranking of defense variants."
   `affects_works`: `["[ChatInject, OpenReview:WVhgFSKniL]"]`. `limitation_type`:
   `"generalizability"`. `source`: HYPOTHESIS.
2. `limitation_text` — **[HYPOTHESIS]**: "The threat-snapshot abstraction deliberately isolates a
   *single* backbone LLM call to fix attribution, but a pinned constraint's survival is a
   property of a *multi-event lifecycle* (repeated summarization/consolidation passes), which a
   one-call snapshot cannot represent; the benchmark also scores a per-model vulnerability rather
   than a strength-swept boundary or a defender-cost ratio."
   `affects_works`: `["[ThreatSnapshots, OpenReview:kga18ld70t]"]`. `limitation_type`:
   `"generalizability"`. `source`: HYPOTHESIS.
3. `limitation_text` — **[HYPOTHESIS]**: "SlotGCG and TAO-Attack optimize adversarial tokens to
   defeat single-turn *safety-refusal* on harmful queries, measured by attack success rate at a
   given budget; neither treats attack strength as a swept continuous variable against
   *structured memory-pinning* defenses, nor measures the defender-side cost the attack must
   overcome — leaving the attack/defense cost trade-off under compaction unmeasured."
   `affects_works`: `["[SlotGCG, OpenReview:Fn2rSOnpNf]", "[TAO-Attack, OpenReview:XfbBiBG46D]",
   "[GCG / Zou et al., 2023]"]`. `limitation_type`: `"other"`. `source`: HYPOTHESIS.
4. `limitation_text` — **[HYPOTHESIS]**: "GuidedBench sharpens the *oracle* for jailbreak success
   into an entity/action checklist, but its object is single-turn harmful-content elicitation;
   it provides no oracle for 'was a pinned task/safety constraint violated *after compaction*',
   which requires checking persistence of a constraint across a summarization event rather than
   harmfulness of one response."
   `affects_works`: `["[GuidedBench, OpenReview:ZVg8y3ibyM]"]`. `limitation_type`: `"other"`.
   `source`: HYPOTHESIS.
5. `limitation_text` — **[HYPOTHESIS]**: "TensorTrust measures the robustness-vs-usability
   trade-off for prompt injection, but in a single-turn string-comparison game with static
   human-authored defenses; it has no context-compaction dynamic, no swept attack-strength axis,
   and no per-variant cost-to-break — so it cannot answer where pinning fails under compaction or
   how cheaply."
   `affects_works`: `["[TensorTrust, OpenReview:fsW7wJGLBd]"]`. `limitation_type`:
   `"generalizability"`. `source`: HYPOTHESIS.
6. `limitation_text` — **[HYPOTHESIS]**: "COMI and the information-theoretic channel view model
   what compression *cooperatively* retains (query-relevant, non-redundant evidence) under a
   benign objective; neither models an *adversary* actively trying to evict a protected
   constraint from the compressed state, so their retention guarantees say nothing about
   adversarial durability of pinned content."
   `affects_works`: `["[COMI, OpenReview:OGDIXDfaN4]", "[InfoChannel, OpenReview:isFHz8qf20]"]`.
   `limitation_type`: `"other"`. `source`: HYPOTHESIS.
7. `limitation_text` — **[HYPOTHESIS]**: "LightMem builds an efficient summarization+consolidation
   memory pipeline but evaluates on *benign* long-horizon dialogue consistency (LoCoMo /
   LongMemEval); its 'sleep-time' dedup/conflict-resolution step is a plausible attack surface
   for constraint eviction that is never adversarially stress-tested, so its persistence claims
   do not transfer to an adversarial-compaction setting."
   `affects_works`: `["[LightMem, OpenReview:dyJ0GWpjJB]"]`. `limitation_type`:
   `"generalizability"`. `source`: HYPOTHESIS.
- `grounding_check`: `true` — every limitation has a non-empty `affects_works` whose strings
  match N3 `citation_key`s verbatim.
- **Status:** `FOUND` — limitations are now tied to real, on-topic prior work.
  - `absence_comment`: `null`.

---

## N5 — Challenges

**Node fields:** `challenges: list[Challenge]`, `conflation_check: bool`

Problem-inherent obstacles, derived from the core question — about the PROBLEM, not any prior
tool's weakness (passes the N4-vs-N5 test). C-ids kept stable from the prior draft; C5 added.

- `C1` — **[HYPOTHESIS, tightly derived]**: "Context compaction is lossy summarization by
  construction; any pinning mechanism competes against information loss, so a 'perfect' defense
  would require either exempting pinned content from compaction entirely (defeating compaction's
  purpose) or a verifier robust to arbitrary adversarial rewriting of the surrounding context.
  COMI's fixed-budget selection framing makes this loss concrete: under aggressive compression
  something must be dropped."
- `C2` — **[HYPOTHESIS, tightly derived]**: "Defining a 'precise failure boundary' requires a
  continuous, comparable strength metric for the injection *and* a defense-variant matrix whose
  variants are measured in commensurable units — neither is standardized, since pinning
  implementations differ structurally (token re-injection vs. structural slots vs. checksums)
  and attack families differ (gradient-optimized suffixes vs. template-role forgery)."
- `C3` — **[HYPOTHESIS, tightly derived]**: "An optimization-capable / white-box-style adversary
  can adapt specifically to whichever pinning mechanism it faces, so any fixed defense has, in
  principle, a computable breaking point — the question is not *if* but *at what cost*, which
  requires isolating a cost signal from raw break-through rate."
- `C4` — **[HYPOTHESIS, tightly derived]**: "Computing a fair attacker-cost/defender-cost ratio
  requires a common currency across heterogeneous mechanisms (attacker optimization
  compute/queries/tokens vs. defender per-turn token/latency overhead); there is no obvious
  natural unit, so any chosen currency embeds a methodological assumption that must be made
  explicit and sensitivity-tested."
- `C5` — **[HYPOTHESIS, tightly derived]**: "A 'break-through rate' is a stochastic estimand:
  LLM outputs and any LLM-judge oracle are non-deterministic, so each (variant, strength) cell's
  rate must be estimated from repeated trials with quantified sampling error, or the location of
  a boundary curve is not identifiable from noise."
- `conflation_check`: `true` — C1 (inherent lossiness), C2 (measurement/commensurability), C3
  (adaptive-adversary inevitability), C4 (cost commensurability), C5 (stochastic estimation) are
  distinct obstacles, none a restatement of another.
- **Status:** `PARTIAL` — derived by inference from a one-sentence core question, not read off an
  actual Challenges section.
  - `absence_comment`: `what_missing`: "No paper text exists to confirm the authors would frame
    these exact five obstacles." / `why_matters`: "A real paper might merge C2+C4 into one
    'measurement methodology' challenge or scope them differently." / `implication`: "Treat
    C1–C5 as a reasonable decomposition to validate against the real paper once written."

---

## N6 — Methodology

**Node fields:** `overview`, `key_components`, `challenge_arguments`, `unaddressed_challenges`

### `overview` — **[HYPOTHESIS]**
"The method runs a two-dimensional sweep. Rows are a matrix of pinning-style
constraint-protection defense variants wrapped as middleware around an LLM agent's
context-compaction function; columns are increasing levels of an adversarial injection-strength
parameter. For every (variant, strength) cell, the injection attempts to induce the agent to
violate a pinned constraint across a compaction event; repeated trials per cell yield a
break-through rate, estimated with a Wilson confidence interval and plotted as a curve per
variant. Logistic curve fitting extracts a comparable scalar boundary (strength at 50%
break-through, BT50) across heterogeneous variants. A parallel cost accounting converts attacker
optimization effort and defender pinning overhead into a common token-equivalent currency and
reports the attacker/defender cost ratio at the measured boundary. **Staged plan.** *Stage 1
(pilot = the seed's minimal experiment):* one open-weight model, two attack families
(gradient-optimized suffix à la SlotGCG/GCG; black-box template-role forgery à la ChatInject),
5 defense variants × ~6 strength levels × ~30 tasks × ~20 trials, to produce the first
break-through-rate curves and confirm the oracle and cost instrumentation work. *Stage 2
(scale-up):* add 2–3 more models (including one closed-weight, black-box-attack-only), expand to
~8 strength levels and ~100 tasks drawn from AgentDojo/InjecAgent/τ-bench/LongMemEval, and add
adaptive-attack and cost-currency sensitivity analyses."

### `key_components` — **[HYPOTHESIS]**
- `M1` / "Defense-variant matrix (middleware)": Implement 5 pinning variants as interchangeable
  wrappers around a compaction summarizer — (a) no-defense control, (b) verbatim re-injection of
  the pinned constraint after each compaction, (c) redundant k-copy pinning, (d) tag/checksum-
  verified pinning (a validator recomputes a hash of the protected span and re-inserts on
  mismatch), (e) structurally isolated protected-memory slot exempt from summarization.
  Instrument: an agent harness logging, per turn and per constraint, the constraint's presence
  and verbatim state pre- and post-compaction. Granularity: per-turn × per-constraint.
- `M2` / "Injection optimization-strength sweep": Parametrize each attack family with an explicit
  strength knob and sweep ~6–8 levels. For the gradient family (SlotGCG/GCG-style), strength =
  optimization iterations × candidate-set size × token budget; for the template family
  (ChatInject-style), strength = number of forged roles/turns × payload token budget. Fixed
  random seeds; warm-started suffixes across adjacent strength levels to save compute.
- `M3` / "Break-through measurement protocol (oracle)": Define constraint violation with a
  two-tier oracle — programmatic exact check for hard constraints (a forbidden tool call fired; a
  numeric/format rule broken) and a GuidedBench/GuidedEval-style rubric LLM-judge (entity/action
  checklist) for soft constraints — audited against ~200 human-labeled cases. Run N≈20–30 trials
  per cell; report break-through rate with a Wilson score interval.
- `M4` / "Cost accounting": Attacker cost = optimizer queries + forward/backward passes (or API
  tokens) spent to reach a target break rate; defender cost = extra tokens + added latency per
  turn each variant imposes. Convert both to a common token-equivalent (and an API-dollar class)
  and compute the attacker/defender ratio at BT50; report the ratio under ≥2 alternative
  currencies as a robustness check for C4.
- `M5` / "Boundary curve fitting": Fit a logistic break-through-vs-strength curve per variant;
  extract BT50 (and BT90) with bootstrap confidence intervals, plus area-under-the-BT-curve as a
  strength-agnostic summary, giving one comparable scalar per otherwise-heterogeneous variant.

### `challenge_arguments` — **[HYPOTHESIS]** (predicted, not authors' actual argument)
- `{challenge_id: "C1", argument_text: "M1's structurally-isolated protected-memory slot is
  predicted to partially mitigate inherent compaction lossiness by keeping pinned content outside
  the summarization pass entirely, rather than relying on the summarizer to preserve it; the
  matrix measures how much this helps versus re-injection/checksum variants.",
  mechanism_components: ["M1"]}`
- `{challenge_id: "C2", argument_text: "M2 + M5 together establish a comparable continuous
  strength axis per attack family and a common BT50/AUC boundary scalar across heterogeneous
  defense variants, addressing the lack of a standardized comparison unit.", mechanism_components:
  ["M2", "M5"]}`
- `{challenge_id: "C3", argument_text: "M2's strength sweep, run with both a white-box gradient
  attack and a black-box template attack, makes adaptive-adversary inevitability quantifiable:
  every variant is expected to show some strength at which break-through rises, confirming rather
  than resolving C3, while M4 isolates the cost dimension.", mechanism_components: ["M2", "M3",
  "M4"]}`
- `{challenge_id: "C4", argument_text: "M4 defines an explicit token-equivalent common currency
  and reports the attacker/defender ratio under multiple currencies, making the cost ratio
  computable and its currency-dependence visible.", mechanism_components: ["M4"]}`
- `{challenge_id: "C5", argument_text: "M3's fixed per-cell trial count with Wilson intervals and
  M5's bootstrap CIs on BT50 quantify the stochastic estimation error, so boundary locations are
  reported with uncertainty rather than as point estimates.", mechanism_components: ["M3",
  "M5"]}`

### `unaddressed_challenges` — **[HYPOTHESIS]**
- `["C1"]` — predicted only *partially* addressed even by the best defense variant: the underlying
  tension (compaction is lossy by design; pinning against loss is a workaround, not a resolution)
  is characterizable but not solvable by a measurement study. Flagged per V-08: this call rests
  on an inferred N5 item, so it is stated with lower confidence.

### Feasibility subsection — **[HYPOTHESIS]**
- **Order of magnitude.** Stage-1 pilot: 5 variants × 6 strengths × 30 tasks × 20 trials × 2
  attack families ≈ 36,000 agent rollouts on 1 open-weight model. Full study (Stage 2): ~4 models,
  ~8 strengths, ~100 tasks → order 10^5–10^6 agent rollouts; with ~10–20 LLM calls per rollout
  this is ~10^6–10^7 model calls. On open-weight 7–14B models this fits ~1–4 weeks on 2–8 GPUs
  plus a low-thousands-USD API budget for the closed-weight arm and the LLM-judge oracle.
  Human effort: ~20–40 annotator-hours to validate the oracle on a ~200-case audit.
- **Single biggest feasibility risk + mitigation.** The gradient (GCG/SlotGCG-style) attack is the
  compute bottleneck — each per-cell attack is hundreds of forward/backward passes and requires
  white-box access, restricting that arm to open-weight models. *Mitigation:* (1) amortize with
  transferable / warm-started suffixes (AmpleGCG-style) reused across adjacent strength levels and
  tasks; (2) carry the black-box template-forgery attack (ChatInject-style, no gradients) as the
  primary cross-model attack so the closed-weight arm and cost-ratio comparison remain feasible;
  (3) reserve full gradient optimization for a representative task subset and interpolate.

- **Status (whole node):** `PARTIAL` — every field is an extrapolation from one sentence of
  minimal-experiment description; no real method section exists, though M1–M5 are now grounded in
  concrete instruments and real attack/oracle families from N3.
  - `absence_comment`: `what_missing`: "No implementation detail (exact optimizer hyperparameters,
    exact pinning code, exact oracle prompts) exists yet." / `why_matters`: "Different real
    implementations of M1–M5 could produce qualitatively different boundary shapes." /
    `implication`: "Use N6 as a design starting point, not as a description of an existing method."

---

## N7 — Contributions

**Node field:** `contributions: list[Contribution]`

- `CO1` — **[HYPOTHESIS]**: "A systematic empirical measurement of the precise adversarial
  break-through-rate failure boundary (BT50/BT90 curves) for pinning-style
  memory-constraint-protection defenses under context compaction, across an injection-strength
  sweep, two attack families, and a defense-variant matrix." `contribution_type`:
  `empirical_finding`. `is_testable`: `true`. `has_rq`: `true` (RQ1).
- `CO2` — **[HYPOTHESIS]**: "A quantified attacker-cost-to-defender-cost ratio at the measured
  boundary (under multiple cost currencies), giving a concrete cost-effectiveness answer to
  whether pinning defenses are worth their overhead against an optimization-capable adversary."
  `contribution_type`: `empirical_finding`. `is_testable`: `true`. `has_rq`: `true` (RQ2).
- `CO3` — **[HYPOTHESIS]**: "A reusable defense-variant × attack-strength evaluation
  matrix/protocol (with a two-tier constraint-violation oracle) that future pinning-defense
  proposals can be benchmarked against." `contribution_type`: `technical_artifact`.
  `is_testable`: `false` (a protocol claim). `has_rq`: `false`.
- **Status:** `PARTIAL` — plausible claims given the method sketch, not read from an actual
  Contributions paragraph.
  - `absence_comment`: `what_missing`: "No abstract/intro 'we contribute...' list exists." /
    `why_matters`: "The real paper might frame narrower (only the boundary) or broader (add a
    proposed mitigation, which the seed does not ask for)." / `implication`: "Treat CO1–CO3 as a
    draft to prune/expand once the real experiment is run."

---

## N8 — Research Questions

**Node fields:** `research_questions`, `datasets`, `baselines`, `metrics`

- `RQ1` — **[GIVEN]**, near-verbatim restatement of the seed's core question (first half): "Where
  exactly is the precise failure boundary at which pinning-style constraint-protection defenses
  break under adversarial context compaction, given that the original paper's optimization
  injection already broke through all tested models?" `rq_source`: `explicit`.
  `evaluates_mechanisms`: `["M1", "M2", "M3", "M5"]`. `addresses_challenges`: `["C1", "C2", "C3",
  "C5"]`. `tests_contributions`: `["CO1"]`. `answered_by_experiment`: "Injection
  optimization-strength sweep × defense-variant matrix, break-through-rate curves + logistic BT50
  fit (the seed's minimal experiment)."
- `RQ2` — **[GIVEN]**, near-verbatim restatement of the second half: "What is the cost ratio
  between attacking (breaking) and defending (maintaining) pinning protection?" `rq_source`:
  `explicit`. `evaluates_mechanisms`: `["M4"]`. `addresses_challenges`: `["C4"]`.
  `tests_contributions`: `["CO2"]`. `answered_by_experiment`: "Cost accounting (token-equivalent,
  multi-currency) layered on the same strength/variant sweep, ratio evaluated at BT50."
- `RQ_INF_3` — **[HYPOTHESIS]** (inferred, strengthens external validity): "Does the *ordering* of
  defense variants by BT50 and by attacker/defender cost ratio remain stable across models and
  across the two attack families, or is it model/attack-specific?" `rq_source`: `inferred`.
  `evaluates_mechanisms`: `["M1", "M2", "M4", "M5"]`. `addresses_challenges`: `["C2", "C3"]`.
  `tests_contributions`: `["CO1"]`. `answered_by_experiment`: "Rank-correlation
  (Kendall's τ) of variant orderings across models × attack families in the Stage-2 sweep."
- `datasets` — **[HYPOTHESIS]** (real named benchmarks that genuinely fit as the constraint/
  compaction workload; the pinned-constraint suite is layered on top of them): `names`:
  `["AgentDojo (tool-using agent environment hosting task + security constraints)", "InjecAgent
  (indirect prompt-injection agent benchmark, as the injection substrate)", "τ-bench (tau-bench)
  tool-agent tasks with policy constraints", "LongMemEval and LoCoMo (long-horizon multi-session
  dialogue, as the compaction workload)", "a constructed pinned-constraint suite layered on the
  above with scripted compaction events (size/name TBD)"]`. `source`: HYPOTHESIS.
- `baselines` — **[HYPOTHESIS]**: `names`: `["no-defense (unpinned) control", "each pinning
  variant in M1 (verbatim re-injection, k-copy, checksum, structural slot)", "black-box
  template-forgery attack (ChatInject-style) as one attack family", "white-box optimization
  attack (SlotGCG/GCG-style) as the other attack family", "GuidedEval-style rubric judge vs.
  programmatic oracle as cross-checks"]`. `source`: HYPOTHESIS.
- `metrics` — **[HYPOTHESIS]**: `names`: `["break-through rate (fraction of trials in which the
  pinned constraint is violated post-compaction), with Wilson 95% CI", "BT50 / BT90 = injection
  strength at 50%/90% break-through, from logistic fit, with bootstrap CI", "area under the
  break-through curve (AUBC)", "attacker-cost / defender-cost ratio at BT50 (token-equivalent;
  reported under ≥2 currencies)", "Kendall's τ of variant orderings across models/attack
  families (for RQ_INF_3)"]`. `source`: HYPOTHESIS.
- **Analysis plan** — **[HYPOTHESIS]**: N≈20–30 trials/cell (Stage 1) → 30+ (Stage 2); logistic
  regression of break-through on strength per (variant, model, attack); compare BT50 across
  variants with bootstrap CIs and a paired test (Wilcoxon signed-rank across tasks), significance
  threshold α = 0.05 with Holm correction across variant pairs. Expected effect directions:
  break-through rises monotonically with strength (positive slope, significant); BT50 differs
  across variants (structural-slot > checksum > k-copy > re-injection > no-defense, in resistance
  order — directional, to be confirmed); cost ratio differs across variants.
- **Status:** `PARTIAL` — RQ1/RQ2 text is given; datasets/baselines/metrics/analysis are inferred
  but now named and operationalized.
  - `absence_comment`: `what_missing`: "The constructed pinned-constraint suite's exact size,
    the exact model list, and exact metric thresholds are not yet fixed." / `why_matters`:
    "Reviewers need concrete identities to judge external validity." / `implication`: "Fix real
    dataset sizes/models the moment the design is frozen."

---

## N9 — Results (PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY, NO REAL NUMBERS)

**Node field:** `results: list[Result]` — every entry is a predicted direction, not a measured
outcome. **No numbers are fabricated.**

- `{rq_id: "RQ1", source: "PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY", result_text: "PREDICTED
  DIRECTION (not measured): break-through rate rises monotonically (or near-monotonically) with
  injection strength for every tested pinning variant, and no variant reaches an asymptotic 0%
  break-through within the tested strength range — every variant has a findable, finite BT50,
  consistent with the seed's given premise that the original paper's injection broke all tested
  models. The structural protected-memory slot is predicted to have the highest BT50 (hardest to
  break) and the no-defense control the lowest.", result_type: "quantitative", evidence_strength:
  "missing", rq_answered: false}`
  - **Falsification condition:** Refuted if, for at least one variant, break-through stays flat and
    bounded well below a meaningful threshold (e.g., under a low single-digit percentage) across
    the *entire* tested strength range — i.e., a variant the attack cannot break even at maximum
    strength. That would falsify "every variant has a findable boundary within range" and be a
    stronger, more interesting finding.
- `{rq_id: "RQ2", source: "PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY", result_text: "PREDICTED
  DIRECTION (not measured): the attacker-cost/defender-cost ratio varies substantially across
  variants — at least one variant is meaningfully more expensive to break per unit of defensive
  overhead than the others, i.e., pinning robustness is not uniform across implementation choices
  even though all eventually fail; and the ranking is expected to persist qualitatively across the
  ≥2 cost currencies tested.", result_type: "quantitative", evidence_strength: "missing",
  rq_answered: false}`
  - **Falsification condition:** Refuted if the measured cost ratio is statistically
    indistinguishable across all variants (no variant cheaper/more expensive to break than any
    other within measurement noise), OR if the variant ranking reverses depending on which cost
    currency is chosen — either would mean the choice of pinning mechanism does not robustly
    change adversarial cost.
- `{rq_id: "RQ_INF_3", source: "PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY", result_text: "PREDICTED
  DIRECTION (not measured): the ordering of defense variants by BT50 and by cost ratio is
  positively rank-correlated (Kendall's τ > 0) across models and across the two attack families —
  the *relative* robustness ranking of pinning mechanisms is largely model- and attack-agnostic
  even though absolute BT50 values shift.", result_type: "quantitative", evidence_strength:
  "missing", rq_answered: false}`
  - **Falsification condition:** Refuted if variant orderings show no significant positive
    rank-correlation across models/attack families (τ ≈ 0 or negative), meaning "which pinning
    variant is best" depends entirely on the specific model/attacker and no general guidance can
    be given.
- **Status:** `NOT_FOUND` for all — no experiment has been run.
  - `absence_comment`: `what_missing`: "No actual break-through-rate numbers, curves, or cost
    ratios exist because the experiment has not been executed." / `why_matters`: "Without real
    numbers, RQ1/RQ2/RQ_INF_3 cannot be answered; only falsifiable directional predictions can be
    stated." / `implication`: "Replace this node wholesale with measured data once the sweep is
    run; no number here is real, because there are none."

---

## N10 — Threats / Self-Limitations

**Node field:** `threats: list[ThreatItem]` — anticipated (no Discussion section exists yet). All
**[HYPOTHESIS]**; `mitigation` here records the *planned* design mitigation rather than an
author-stated one.

- `{threat_id: "t1", category: "construct", description: "The constructed suite of pinning defense
  variants (M1) is a research artifact, not a survey of production systems, so the measured
  'failure boundary' may not represent how pinning is actually implemented in deployed agent
  frameworks.", mitigation: "Model each variant on a documented real mechanism (verbatim
  re-injection, redundant copies, checksum/tag verification, structural memory slots à la
  LightMem's consolidation) and report boundaries per-variant so practitioners can map to their
  own implementation.", source: HYPOTHESIS}`
- `{threat_id: "t2", category: "construct", description: "The break-through oracle (M3) may
  mis-score constraint violation — a rubric LLM-judge can over- or under-count soft-constraint
  violations, threatening the validity of the break-through rate itself.", mitigation: "Two-tier
  oracle (programmatic exact check where possible + GuidedEval-style checklist judge), audited
  against ~200 human-labeled cases; report oracle agreement rate and treat soft-constraint results
  as secondary to hard-constraint results.", source: HYPOTHESIS}`
- `{threat_id: "t3", category: "external", description: "Findings from a specific tested model set
  and two attack families may not generalize to other LLM families/scales or to stronger future
  attacks; the boundary is characterized against *these* adversaries, not a worst case.",
  mitigation: "Test ≥4 models incl. one closed-weight; use both a white-box (SlotGCG/GCG) and a
  black-box (ChatInject) attack; RQ_INF_3 explicitly measures cross-model/attack ordering
  stability; frame results as a lower bound on breakability.", source: HYPOTHESIS}`
- `{threat_id: "t4", category: "conclusion", description: "The attacker/defender cost ratio (M4)
  depends on the chosen cost currency (queries vs. wall-clock vs. tokens vs. dollars); a different
  currency could reorder variants by cost-effectiveness.", mitigation: "Report the ratio under ≥2
  currencies and treat currency-dependence of the ranking as a first-class result (a reversal
  falsifies RQ2's ranking claim).", source: HYPOTHESIS}`
- `{threat_id: "t5", category: "internal", description: "Per-cell break-through estimates depend on
  trial count, sampling temperature, and attack random seeds; underpowered cells could place a
  boundary curve in the wrong location.", mitigation: "Fix N≥20–30 trials/cell with Wilson CIs,
  fixed seeds, bootstrap CIs on BT50, and a power check that widens N until CI width is below a
  preset threshold before fitting the curve.", source: HYPOTHESIS}`
- `{threat_id: "t6", category: "external", description: "Amortizing the gradient attack with
  transferable/warm-started suffixes (a feasibility mitigation) may *understate* attack strength
  relative to a fully re-optimized per-cell attack, biasing BT50 upward (defenses look stronger
  than they are).", mitigation: "On a representative task subset, compare warm-started vs.
  fully-re-optimized attacks and report the gap as a calibration correction on BT50.", source:
  HYPOTHESIS}`
- **Status:** `PARTIAL` — anticipated, standard-practice threats for this study type, not
  author-acknowledged (no author exists yet).
  - `absence_comment`: `what_missing`: "No real Discussion/Limitations section exists to confirm
    which threats the eventual authors would acknowledge." / `why_matters`: "A real paper might
    surface additional limitations specific to the chosen models/compaction algorithm." /
    `implication`: "Use t1–t6 as a pre-registered threats checklist to address by design."

---

## N11 — Artifacts

**Node fields:** `artifacts: []`, `has_code: false`, `has_data: false`, `has_model: false`.

- **[PLACEHOLDER]** — nothing released; no paper/code/data exists yet.
- **Status:** `NOT_FOUND`.
  - `absence_comment`: `what_missing`: "No code repository, dataset, model checkpoint, or demo
    exists for this topic." / `why_matters`: "Reproducibility of the eventual break-through-rate/
    cost-ratio findings will depend entirely on whether the defense-variant matrix, the two-tier
    oracle, and the injection procedures are released." / `implication`: "Report N11 as NOT_FOUND
    honestly until an actual release happens."

---

## N12 — Contribution Type

- `value`: `"empirical"` — **[HYPOTHESIS]**.
- `rationale`: "The seed's minimal experiment — sweeping injection strength against a matrix of
  defense variants and plotting break-through-rate curves — is a measurement study of an existing
  phenomenon (pinning-defense robustness under adversarial compaction), matching the schema's
  `empirical` category and the pattern of the two closest best-paper exemplars: ICLR-2025
  'Safety Alignment ... Few Tokens Deep' and ICLR-2026 'LLMs Get Lost in Multi-Turn Conversation'
  are both filed `empirical` even though each also *builds* instruments (a per-token diagnostic /
  a sharded-simulation environment). Here likewise, the defense-variant matrix (M1), the attack
  sweep (M2), and the two-tier oracle (M3) are instrumental to the measurement, not the headline
  offering. This rules out `system`/`tool` (no new defense is proposed as the primary
  contribution — the variants are the object of study) and `benchmark`/`dataset` (the constructed
  suite serves the measurement; the core question asks *where the boundary is* and *at what cost*,
  which N9 validates as break-through curves and a cost ratio)." `source`: HYPOTHESIS.
- **Status:** `PARTIAL` — **PHASE-A FIX (goal.md §3 checklist items 1/3):** this line was
  previously missing, inconsistent with every other node (N0–N11), each of which carries an
  explicit `Status` line; added here for tag-discipline consistency. The archetype call itself is
  reasoned from the seed's minimal experiment and two named best-paper exemplars, not read off a
  real Contribution-Type statement.
  - `absence_comment`: `what_missing`: "No real paper exists to confirm the authors would file
    this as `empirical` rather than, e.g., `benchmark` (if the constructed pinned-constraint suite
    became the headline) or `system` (if a proposed mitigation became the headline)." /
    `why_matters`: "Contribution-type misclassification would cascade into the wrong Part 2
    evidence standard (guidance.md) being applied throughout Phase A–D." / `implication`: "Re-check
    this call against the real Introduction once Phase E prose exists, before it hardens into the
    abstract's contribution framing."

---

## Claims

Top reviewer-relevant assertions this future paper would plausibly make, each tagged by trust
level.

1. **[GIVEN]** "The original paper's optimization-based injection attack broke through the
   pinning defenses of all tested models." `evidence`: `[{type: "citation", text: "原论文的优化注入击穿全部受测模型", source: "GIVEN", location: "seed README, 核心问题"}]`.
2. **[HYPOTHESIS]** "Every tested pinning-style defense variant has a findable, finite adversarial
   failure boundary (BT50) within a practical injection-strength range — none achieves
   asymptotically zero break-through." `evidence`: `[{type: "argument", text: "extrapolation of the
   given premise to a continuous strength sweep, using GCG/SlotGCG-style and ChatInject-style
   attacks as the injection families", source: "HYPOTHESIS"}]`. **Falsifiable**: see N9/RQ1.
3. **[HYPOTHESIS]** "The attacker-cost-to-defender-cost ratio differs meaningfully across pinning
   defense variants and this ordering persists across ≥2 cost currencies, so some pinning
   implementations are more cost-effective than others even though none is unconditionally
   robust." `evidence`: `[{type: "argument", text: "standard adversarial-robustness expectation
   that defense variants differ in marginal cost-to-break; TensorTrust frames the analogous
   robustness-vs-usability trade-off", source: "HYPOTHESIS"}]`. **Falsifiable**: see N9/RQ2.
4. **[HYPOTHESIS]** "The relative robustness ranking of pinning variants is largely model- and
   attack-family-agnostic (positive rank-correlation), giving transferable deployment guidance."
   `evidence`: `[{type: "argument", text: "predicted from cross-model transferability of
   optimization attacks reported by GCG/SlotGCG and the cross-model filtering used by TensorTrust",
   source: "HYPOTHESIS"}]`. **Falsifiable**: see N9/RQ_INF_3.
5. **[GROUNDED:corpus]** "Existing agent-security work covers the ingredients (template-role
   injection [ChatInject, OpenReview:WVhgFSKniL]; optimization jailbreaks [SlotGCG,
   OpenReview:Fn2rSOnpNf], [TAO-Attack, OpenReview:XfbBiBG46D]; injection-robustness benchmarking
   [TensorTrust, OpenReview:fsW7wJGLBd], [ThreatSnapshots, OpenReview:kga18ld70t]; lossy
   compaction [COMI, OpenReview:OGDIXDfaN4]; memory pipelines [LightMem, OpenReview:dyJ0GWpjJB])
   but none measures a strength-swept failure boundary or attacker/defender cost ratio for
   memory-pinning under adversarial context compaction." `evidence`: `[{type: "observation", text:
   "corpus keyword search over 11,683 OpenReview papers surfaced these adjacent works but no direct
   study of pinning under adversarial compaction with a strength-sweep/cost-ratio design", source:
   "GROUNDED:corpus"}]`.
