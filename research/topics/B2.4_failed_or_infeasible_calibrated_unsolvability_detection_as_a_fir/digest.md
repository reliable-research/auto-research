# Digest: Failed or Infeasible? Calibrated Unsolvability Detection as a First-Class Attribution Outcome

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet. This document
> projects forward from a seed research idea (topic code **B2.4**, label **[边界]**, parent
> topic **B2. 失败归因（plan / tool / execution）**) to what an N0–N12 digest of a paper
> answering this idea *would plausibly look like*, for research-planning purposes only.
> Every field is tagged `[GIVEN]` (verbatim/near-verbatim from the seed README),
> `[HYPOTHESIS]` (reasoned elaboration / prediction, not fact),
> `[GROUNDED:corpus]` (a real OpenReview paper located in the local corpus
> `topics/corpus/ideas.jsonl`; its summary is grounded in that paper's own
> motivation/method text, but its *relevance mapping* to this not-yet-written paper is my
> judgment), or `[PLACEHOLDER]` (genuinely unknowable until the work is done — never
> invented). Locators that would normally point into a PDF (`page`, `section_title`,
> `quote`) are replaced with `"N/A — no paper exists yet"` throughout, tagged `[PLACEHOLDER]`.

---

## N0 — Metadata

- **title**: "Failed or Infeasible? Calibrated Unsolvability Detection as a First-Class Attribution Outcome" `[GIVEN]`
- **title_cn**: "不可解性作为归因类别" `[GIVEN]`
- **authors**: `["Anonymous"]` `[PLACEHOLDER]`
- **abstract** `[HYPOTHESIS]` (drafted by synthesizing the core question + minimal experiment into abstract prose — explicitly a draft, not a real abstract):
  > "Failure-attribution systems for LLM agents routinely assume that when a task is not
  > completed, some component of the agent — its plan, its tool use, or its execution —
  > is at fault. This assumption breaks down when the task itself has no solution. We ask
  > whether agents and the attribution systems built around them can distinguish 'the
  > agent failed' from 'the task was never solvable,' and where the calibration boundary
  > of appropriate refusal lies. We construct matched pairs of solvable and unsolvable
  > task instances across text-to-SQL, tool-calling, customer-service, and command-line
  > agent domains, in which unsolvability is injected by mechanical mutation operators
  > (removing a required schema element, tool, or environment resource; contradicting a
  > stated constraint) so that ground truth is verifiable by script rather than by
  > judgment. Running existing agents and attribution pipelines over these pairs, we
  > measure the rate at which genuinely unsolvable instances are misattributed as agent
  > failures, and characterize how this misattribution rate trades off against an
  > abstention/confidence threshold. We report this as a first step toward treating
  > unsolvability as a first-class attribution outcome rather than an unmodeled failure
  > mode."
- **doi**: `null` `[PLACEHOLDER]`
- **arxiv_id**: `null` `[PLACEHOLDER]`
- **num_pages**: `null` `[PLACEHOLDER]`
- **research_area**: `"AI/ML"` `[HYPOTHESIS]` (inferred — the problem sits squarely in LLM-agent evaluation/attribution, adjacent to selective prediction and calibration research)
- **status**: `PARTIAL` — title/core-question given, but authors/abstract/doi are all placeholder since the paper does not exist.
- **absence_comment**: `{"what_missing": "No actual authors, abstract, DOI, or page count exist because this is a pre-paper speculative digest.", "why_matters": "A reader could otherwise mistake the drafted abstract or 'Anonymous' author tag for real bibliographic fact.", "implication": "Treat every N0 field except title/title_cn as provisional scaffolding to be replaced once (if) the paper is written."}`

---

## N1 — Problem Formulation

- **objective** `[HYPOTHESIS]` (full predicate built from the core question):
  > "Measure whether LLM-agent failure-attribution systems can distinguish genuine task
  > unsolvability from agent execution failure, on a suite of mechanically constructed,
  > script-verified solvable/unsolvable task pairs spanning text-to-SQL, tool-calling,
  > and command-line agent domains, and characterize the calibration boundary of their
  > abstention/refusal behavior as a risk–coverage trade-off over a confidence threshold."
  >
  > Self-check: (1) KIND of task — a measurement/classification-evaluation study; (2)
  > DOMAIN — LLM agent failure-attribution systems over multi-step execution traces; (3)
  > OUTCOME shape — measured misattribution rates plus calibration/risk–coverage curves,
  > with a released paired benchmark as instrument. All three land.
- **inputs** `[HYPOTHESIS]` (inferred from the minimal experiment):
  1. A constructed task instance from a matched solvable/unsolvable pair (task text + environment: schema, tool list, or file system)
  2. The agent's execution trace on that instance (actions, tool calls, errors, final output or refusal)
  3. The attribution system's classification output over that trace, with a confidence score
- **outputs** `[HYPOTHESIS]`:
  1. A per-instance attribution label from {success, agent_failure, unsolvable}
  2. A confidence/abstention score attached to the "unsolvable" judgment
  3. Aggregate misattribution rates in both directions, plus calibration and risk–coverage curves across the benchmark
- **constraints** `[GIVEN]` (verbatim from seed): "不可解性由构造保证，真值机械成立" — unsolvability
  is guaranteed by construction; the ground truth (solvable vs. unsolvable) holds
  mechanically, not by human judgment or consensus.
- **source**: `inferred` (no explicit formulation exists — there is no paper — so objective/inputs/outputs are reconstructed from the core question and minimal experiment; `constraints` is extracted verbatim from the seed).
- **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

---

## N2 — Motivation

**motivations** (`list[MotivationItem]`):

1. `[HYPOTHESIS]` motivation_text: "Failure-attribution pipelines for LLM agents (plan-level,
   tool-level, execution-level) are built on the implicit assumption that every failed run
   contains a culpable agent decision. The strongest current formulations make this explicit:
   attribution is defined as *localizing the agent-step pair that first made success
   unattainable* (cf. N3 `[AgenTracer, OpenReview:l05DseqvuD]`, `[WhoWhen, arXiv:2505.00212]`) —
   a definition that presumes such a pair exists. When the task itself has no valid solution
   (missing precondition, contradictory constraint, non-existent resource), these systems must
   still nominate a culprit, systematically over-blaming the agent, distorting debugging
   effort, and miscalibrating any downstream retry/escalate/abandon policy that consumes the
   attribution label." — reconstructed from the parent-topic framing "B2. 失败归因（plan /
   tool / execution）" plus the actual problem definitions in the cited attribution papers.
   - evidence: `[]`
   - source: `inferred`
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`
2. `[HYPOTHESIS]` motivation_text: "A calibrated boundary between 'agent should keep trying'
   and 'agent should refuse because nothing would succeed' is a prerequisite for trustworthy
   autonomous operation. The refusal-calibration literature shows why naive fixes fail:
   models can appear to improve simply by refusing more often, without refusals tracking the
   actual boundary (cf. N3 `[RefusalIndex, OpenReview:9gJBhkLRat]`) — so the boundary must be
   measured against verified unsolvability, not against refusal frequency."
   - evidence: `[]`
   - source: `inferred`
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

**status**: `PARTIAL` (motivation is reconstructed, not extracted from a real motivation section).
**absence_comment**: `{"what_missing": "There is no written Introduction/Motivation section to extract from.", "why_matters": "The stated motivations are plausible but unverified extrapolations from a one-line parent-topic label plus the cited papers' own framings, not this paper's own framing.", "implication": "Treat these as hypotheses about why this problem would matter, to be checked against the eventual paper's actual introduction."}`

---

## N3 — Related Works

Grounding: a real corpus search was run over `topics/corpus/ideas.jsonl` (11,683 OpenReview
papers) with five query angles — (a) unsolvable/infeasible/abstention/refusal, (b) failure
attribution / blame assignment / multi-agent failure, (c) calibration / selective
prediction / unanswerable questions, (d) infeasible-task agent benchmarks, (e) agent +
abstain + ambiguous instruction. Each `[GROUNDED:corpus]` entry's `approach_summary` is
written from that paper's own motivation/method text. Two non-corpus entries are retained
because they are the canonical works for this exact niche (the MAST failure taxonomy and
the Who&When decisive-error-attribution formulation, both cited repeatedly inside the
corpus papers' own motivations); they are marked `[HYPOTHESIS-canonical, NOT in corpus]`.

**works** (`list[RelatedWork]`):

1. **citation_key**: `[AgenTracer, OpenReview:l05DseqvuD]` `[GROUNDED:corpus]`
   **approach_summary**: Automated failure attribution for multi-agent LLM systems: replays
   failed trajectories with one step at a time replaced by a minimally corrected action, and
   labels as the "decisive error" the earliest step whose correction flips failure to success;
   programmatic fault injection into successful traces expands supervision, and a dedicated
   tracer is trained with RL to predict the responsible agent and earliest decisive step.
   **paper_url**: https://openreview.net/forum?id=l05DseqvuD
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `l05DseqvuD`

2. **citation_key**: `[WhoWhen, arXiv:2505.00212]` `[HYPOTHESIS-canonical, NOT in corpus]`
   **approach_summary**: Formulates automated failure attribution for LLM multi-agent systems
   as identifying *which agent* caused the failure and *at which step*, releases the Who&When
   benchmark of annotated failure trajectories, and evaluates LLM-judge attribution strategies
   (all-at-once, step-by-step, binary-search) — finding even strong models weak at step-level
   localization. (Confidence: this is `zhang2025whowhen`, cited as the problem-defining prior
   work inside `[AgenTracer, OpenReview:l05DseqvuD]`'s own motivation text.)
   **paper_url**: https://arxiv.org/abs/2505.00212
   **source**: `HYPOTHESIS-canonical`
   **location**: cited within corpus entry `l05DseqvuD` motivation (`@zhang2025whowhen`)

3. **citation_key**: `[MAST, arXiv:2503.13657]` `[HYPOTHESIS-canonical, NOT in corpus]`
   **approach_summary**: "Why Do Multi-Agent LLM Systems Fail?" — builds MAST, a taxonomy of
   recurring multi-agent failure modes (specification, inter-agent misalignment, verification
   failures) from manually annotated trajectories across mainstream frameworks, documenting
   high failure rates. (Confidence: this is `cemri2025mast`, cited in the motivations of both
   `[AgenTracer, OpenReview:l05DseqvuD]` and `[StopWasting]`-class corpus papers.)
   **paper_url**: https://arxiv.org/abs/2503.13657
   **source**: `HYPOTHESIS-canonical`
   **location**: cited within corpus entry `l05DseqvuD` motivation (`@cemri2025mast`)

4. **citation_key**: `[RefusalIndex, OpenReview:9gJBhkLRat]` `[GROUNDED:corpus]`
   **approach_summary**: Proposes the Refusal Index — the Spearman rank correlation between a
   model's refusal probability and its error probability across factual questions — measured
   black-box via a two-pass protocol (first pass allows refusal; second pass forces answers on
   previously refused questions), isolating whether refusals track knowledge gaps rather than
   rewarding higher refusal frequency as in SimpleQA-style heuristic metrics.
   **paper_url**: https://openreview.net/forum?id=9gJBhkLRat
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `9gJBhkLRat`

5. **citation_key**: `[SilenceIsGolden, OpenReview:PhUCxfS0yf]` `[GROUNDED:corpus]`
   **approach_summary**: Trains LLMs to abstain in temporal QA where TimeQA supplies both
   answerable and naturally unanswerable questions: CoT-supervised cold start followed by
   GRPO policy optimization with an abstention-aware outcome reward that pays for correct
   "No Answer" on unanswerable items — moving abstention from post-hoc confidence estimation
   to direct policy optimization.
   **paper_url**: https://openreview.net/forum?id=PhUCxfS0yf
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `PhUCxfS0yf`

6. **citation_key**: `[KnowCapable, OpenReview:EO6WtJ0q6G]` `[GROUNDED:corpus]`
   **approach_summary**: "Do Large Language Models Know What They Are Capable Of?" — evaluates
   ex-ante success prediction on executable coding tasks (BigCodeBench, SWE-bench), confidence
   updating from in-context experience, and confidence-guided accept/decline decisions in a
   contract-style setting with costly failure, treating confidence as a predictive state
   variable that should guide whether an agent starts, continues, or declines a task.
   **paper_url**: https://openreview.net/forum?id=EO6WtJ0q6G
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `EO6WtJ0q6G`

7. **citation_key**: `[TrustOrEscalate, OpenReview:UHPnqSTBPO]` `[GROUNDED:corpus]`
   **approach_summary**: Selective, cascaded LLM-judge framework with provable human-agreement
   guarantees: confidence is estimated as agreement among simulated annotators, thresholds are
   exactly calibrated on a small human-labeled set via learn-then-test fixed-sequence testing,
   and uncertain cases escalate through a cascade of stronger judges.
   **paper_url**: https://openreview.net/forum?id=UHPnqSTBPO
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `UHPnqSTBPO`

8. **citation_key**: `[RLCR, OpenReview:ASQ649zdHm]` `[GROUNDED:corpus]`
   **approach_summary**: Reinforcement Learning with Calibration Rewards — trains reasoning
   LMs to emit an answer plus a numeric confidence, optimizing a reward that combines binary
   correctness with a Brier-score calibration term under GRPO, so that cautious uncertainty
   and confident hallucination are no longer rewarded identically by binary-reward RL.
   **paper_url**: https://openreview.net/forum?id=ASQ649zdHm
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `ASQ649zdHm`

9. **citation_key**: `[EHR-ChatQA, OpenReview:hLweUPBz7k]` `[GROUNDED:corpus]`
   **approach_summary**: An interactive benchmark for EHR database agents that transforms
   real clinical SQL queries into user instructions that intentionally withhold information
   or rephrase database values, then evaluates the full user–agent–tool loop (clarification
   questions, schema/value exploration tools, SQL execution) rather than one-shot semantic
   parsing — explicitly motivated by prior findings that ambiguous and unanswerable questions
   are common but had only been tested with scripted clarification templates.
   **paper_url**: https://openreview.net/forum?id=hLweUPBz7k
   **source**: `GROUNDED:corpus`
   **location**: corpus `ideas.jsonl`, paper_id `hLweUPBz7k`

**status**: `FOUND` (9 works: 7 real corpus papers + 2 clearly-marked canonical non-corpus works; within the 5–10 target range).
**absence_comment**: `null`

---

## N4 — Prior Limitations

**grounding_check**: `true` (every limitation below cites at least one `N3.works[].citation_key`,
in the exact same string form).

**limitations** (`list[Limitation]`), all `source="HYPOTHESIS"` (no paper text exists to
extract from — but each limitation is defensible from the cited paper's own motivation text
or from what its method demonstrably does not cover):

1. **limitation_text**: "The state-of-the-art attribution formulation defines the task as
   localizing 'the specific agent-step pair that first made success unattainable' and labels
   as decisive the earliest step whose counterfactual correction flips failure to success.
   Both the label space {responsible agent, decisive step} and the counterfactual procedure
   presuppose that a success-flipping correction *exists* — on a genuinely unsolvable task no
   single-step correction can flip the outcome, so the pipeline has no well-defined output
   and must still nominate a culprit. 'The task itself is infeasible' is not an admissible
   attribution outcome." `[HYPOTHESIS]`
   **affects_works**: `["[AgenTracer, OpenReview:l05DseqvuD]", "[WhoWhen, arXiv:2505.00212]"]`
   **limitation_type**: `generalizability`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

2. **limitation_text**: "The MAST failure taxonomy classifies *how agent systems fail*
   (specification, inter-agent misalignment, verification failures) from manually annotated
   trajectories; it has no category for task-level infeasibility, and its manual annotation
   is small-scale — a scale limitation that the AgenTracer motivation itself flags ('Available
   datasets are manually annotated and small'). Any trajectory over an unsolvable task would
   have to be forced into one of the agent-fault categories." `[HYPOTHESIS]`
   **affects_works**: `["[MAST, arXiv:2503.13657]"]`
   **limitation_type**: `generalizability`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

3. **limitation_text**: "The Refusal Index calibrates refusal against the *model's own* error
   probability on single-turn factual questions — a knowledge-boundary notion of 'should
   refuse.' It never involves an externally certified ground truth that the task admits no
   answer for anyone, and it operates on static QA, not on multi-step agent traces where the
   observable signal is retries, tool errors, and partial progress." `[HYPOTHESIS]`
   **affects_works**: `["[RefusalIndex, OpenReview:9gJBhkLRat]"]`
   **limitation_type**: `precision`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

4. **limitation_text**: "Abstention-training work rewards a single generator for emitting 'No
   Answer' on dataset-labeled unanswerable QA items; the unanswerable labels are inherited
   from a benchmark (TimeQA), not injected via matched-pair construction, so answerable and
   unanswerable items differ in uncontrolled surface ways, and nothing in the setup measures
   whether a *third-party attribution system* watching an execution trace can make the same
   call about someone else's failure." `[HYPOTHESIS]`
   **affects_works**: `["[SilenceIsGolden, OpenReview:PhUCxfS0yf]"]`
   **limitation_type**: `generalizability`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

5. **limitation_text**: "Capability self-assessment work elicits the probability that *this
   model* will succeed on executable tasks — but its testbeds (BigCodeBench, SWE-bench)
   consist of tasks that are all solvable in principle, so low predicted success conflates
   'solvable but beyond me' with 'unsolvable for anyone'; the two are never dissociated by
   construction, which is exactly the dissociation this topic requires." `[HYPOTHESIS]`
   **affects_works**: `["[KnowCapable, OpenReview:EO6WtJ0q6G]"]`
   **limitation_type**: `precision`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

6. **limitation_text**: "Calibrated-abstention machinery targets the wrong ground truth for
   this problem: selective LLM-judging calibrates abstention against *human agreement* on
   subjective evaluations (escalating to a stronger judge, never declaring the item itself
   infeasible), and calibration-reward RL calibrates confidence against *answer correctness*
   on verifiable single-turn problems whose reward design contains no unsolvable-instance
   class — so a perfectly calibrated model under either scheme still receives no signal
   distinguishing 'I cannot' from 'no one can.'" `[HYPOTHESIS]`
   **affects_works**: `["[TrustOrEscalate, OpenReview:UHPnqSTBPO]", "[RLCR, OpenReview:ASQ649zdHm]"]`
   **limitation_type**: `precision`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

7. **limitation_text**: "Interactive-ambiguity benchmarks treat underspecification as
   *resolvable*: the agent is scored on recovering the missing constraint via clarification
   questions or database exploration. Their own motivation notes that unanswerable questions
   are common but were previously handled only with scripted clarification templates — the
   benchmark never requires the agent to certify that a request is infeasible and stop, nor
   does it provide construction-guaranteed infeasibility labels to score such a call
   against." `[HYPOTHESIS]`
   **affects_works**: `["[EHR-ChatQA, OpenReview:hLweUPBz7k]"]`
   **limitation_type**: `generalizability`
   **location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

---

## N5 — Challenges

**conflation_check**: `true` (construction-time verifiability, trace-time discrimination,
threshold-setting, and confound control are four separate obstacles).

**challenges** (`list[Challenge]`), all `source="HYPOTHESIS, but tightly derived"` from the
core question and minimal experiment:

- **C1**: "Ground-truth unsolvability must be certified *independently of any observed agent
  behavior*, by a mechanical procedure over the task/environment specification itself (e.g.,
  the gold query references a schema element that no longer exists and no alternative
  derivation path exists; the required API/tool/record has been removed) — because the only
  alternative certification sources, human consensus or agent failure itself, are
  respectively subjective and circular." `[HYPOTHESIS]`
- **C2**: "Traces are observationally confusable: a competent agent exhausting a genuinely
  unsolvable task and an incompetent agent botching a solvable one both produce long
  trajectories with repeated tool errors, dead-end exploration, and no final answer — the
  attribution system sees only the trace, so the discrimination signal, if it exists, is
  subtle (e.g., *systematic* absence of a needed resource vs. *recoverable* mistakes that
  were never recovered)." `[HYPOTHESIS]`
- **C3**: "The calibration boundary — the confidence threshold at which a system should
  declare 'unsolvable' — is a two-sided risk trade-off with asymmetric costs: over-flagging
  lets agents 'cop out' of solvable-but-hard tasks, under-flagging blames agents for
  impossible ones; the right operating point plausibly differs by task family and by the
  downstream policy consuming the label, so a single fixed cutoff cannot be the answer."
  `[HYPOTHESIS]`
- **C4**: "Matched-pair construction must not leak: if the unsolvability-injecting mutation
  leaves surface artifacts (length differences, telltale phrasing, a conspicuously absent
  tool), an attribution system — or the agent itself — can 'detect' unsolvability from the
  task text alone without any genuine feasibility reasoning, invalidating the measured rates.
  The pair members must differ only in the solvability-determining fact." `[HYPOTHESIS]`

**status**: `FOUND` (all four challenges are tightly derivable from the core question and
minimal experiment; none are extracted since no paper exists).
**location** (all items): `"N/A — no paper exists yet"` `[PLACEHOLDER]`

---

## N6 — Methodology

### overview

`[HYPOTHESIS]` **text**: "Build a paired solvable/unsolvable benchmark by applying mechanical
mutation operators to existing, verifier-equipped agent benchmarks — dropping a required
schema column from a Spider/BIRD text-to-SQL database, removing the required function from a
BFCL v3 tool list, deleting the target record or adding a policy contradiction in a τ-bench
environment, referencing a non-existent file in a Terminal-Bench task — such that a script
(not a human, not an LLM) certifies each instance's true label. Run existing agents over both
pair members under a fixed step budget, record full traces, and pass the traces to a battery
of attribution systems that must emit {success, agent_failure, unsolvable} plus a confidence
score. Sweep the confidence threshold for the 'unsolvable' label and report both directional
misattribution rates, threshold-free discrimination metrics, and risk–coverage curves.

**Staged plan.** *Stage 1 (pilot — the seed's minimal experiment):* 2 domains (Spider
text-to-SQL + BFCL v3 tool-calling), ~50 pairs per domain (100 pairs / 200 instances), 2
agent backbones, 1 LLM-judge attribution baseline; deliverable: the baseline
unsolvable→agent_failure misattribution rate (RQ_INF_1) and a pair-validity audit. *Stage 2
(scale-up):* 4 domains × ~150 pairs (600 pairs / 1,200 instances), 3+ agent backbones from
different model families, the full attribution-baseline battery, threshold sweeps and
calibration analysis (RQ1), plus cross-domain transfer of the fitted threshold."
**location**: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

### key_components

- **M1** — *Paired task generator (mutation operators)*: For each source task with a passing
  reference solution, applies exactly one mutation from a typed operator library —
  {missing-resource: drop the schema column/table, tool, file, or DB record the reference
  solution requires; contradictory-constraint: add a policy or goal clause inconsistent with
  a stated one; stale-reference: point the goal at an entity that does not exist in the
  environment} — holding instruction wording, length, and environment size otherwise fixed.
  Emits pair metadata (operator type, mutated element, source benchmark ID) per instance.
  `[HYPOTHESIS]`
- **M2** — *Ground-truth solvability oracle (script, not LLM)*: Certifies labels mechanically:
  the solvable member's reference solution executes and passes its original verifier; the
  unsolvable member is certified by a static check that the mutated element is (a) required
  by the reference solution and (b) has no substitute (schema-graph reachability for SQL;
  tool-signature coverage for function calling; environment-state assertion for τ-bench /
  Terminal-Bench; for open-action domains, operators are restricted to a closed sub-language
  where no-substitute is decidable — instances not certifiable this way are excluded, never
  guessed). The oracle carries its own R2 validation plan (paper.md Step 5): a 10% rater
  audit (≥2 independent raters attempting substitute derivations, κ ≥ 0.70 against the
  oracle verdict) in addition to the PG-1 strongest-agent falsification search, with the
  oracle code hash frozen before scale. The oracle is used only at evaluation time and
  never exposed to agents or attribution systems. `[HYPOTHESIS]`
- **M3** — *Agent execution harness*: Runs each agent on every instance under a fixed step/
  token budget with standardized logging — every action, tool call, tool result/error,
  intermediate reasoning summary, and the terminal event (answer, explicit refusal/infeasible
  declaration, or budget exhaustion). Agents receive no hint that unsolvable instances exist
  beyond a neutral instruction that declaring a task infeasible is an allowed final action.
  `[HYPOTHESIS]`
- **M4** — *Attribution battery under test*: Consumes a trace (and the task text, but never
  the oracle) and emits a {success, agent_failure, unsolvable} label + confidence in
  [0,1]. Instantiations: (a) LLM-judge attribution in all-at-once and step-by-step modes
  (the two strategies studied by `[WhoWhen, arXiv:2505.00212]`), (b) an
  AgenTracer-style trained tracer where its label space is extended with 'unsolvable'
  (`[AgenTracer, OpenReview:l05DseqvuD]`), (c) the acting agent's own terminal
  self-report (first-party refusal, cf. `[KnowCapable, OpenReview:EO6WtJ0q6G]`'s ex-ante
  protocol adapted to post-hoc), and (d) a trivial refusal-keyword/terminal-error heuristic
  as floor. `[HYPOTHESIS]`
- **M5** — *Calibration sweep and misattribution estimator*: Sweeps the threshold τ on the
  "unsolvable" confidence; at each τ computes the false-blame rate and cop-out rate (defined
  in N8 metrics), producing risk–coverage curves, AURC, AUROC of the unsolvability score,
  10-bin ECE, and a Refusal-Index-style Spearman correlation between abstention confidence
  and true unsolvability (metric form borrowed from `[RefusalIndex, OpenReview:9gJBhkLRat]`).
  `[HYPOTHESIS]`
- **M6** — *Pair-validity and leakage audit*: (a) surface-statistics matching test — pair
  members must be indistinguishable on length, token overlap, and instruction perplexity;
  (b) text-only probe — named per paper.md's R2 plan: two readers, gate = max of the two —
  the strongest attributor-battery backbone prompted text-only (no trace, no environment),
  plus a trained discriminator fit on a disjoint 30% pair-level calibration split; before
  its near-chance verdict counts, the trained probe must reach AUROC ≥ 0.90 on a
  positive-control set of deliberately leaky pairs (probe-power validation, R2 step③), and
  probe prompt/weights/threshold are frozen before scale (R2 step⑤). Stated blindness,
  honestly: a text-only probe cannot detect memorization-based cues available only to
  backbones that memorized the original source benchmark — that channel is controlled by
  the surface-anonymization arm (paper.md B-alt2), not by M6;
  (c) human audit of a 10% random sample of pairs, by **≥2 independent raters**,
  checking that the mutation is the only semantic difference, gated at inter-rater agreement
  **κ ≥ 0.70** (guidance.md §3.4 R2 step③; disagreements inspected for adjacent-vs-systematic
  structure per R2 step④ before the gate is considered passed). Runs before any headline
  number is reported. `[HYPOTHESIS]`

### challenge_arguments

- `{challenge_id: "C1", argument_text: "Unsolvability is injected by typed mechanical mutations (M1) and certified by a static script-level oracle (M2) that checks requirement + no-substitute conditions on the environment itself — ground truth is established before any agent runs and never depends on the observed trace.", mechanism_components: ["M1", "M2"], source: "inferred"}`
- `{challenge_id: "C2", argument_text: "Running the same attribution battery (M4) over harness-standardized traces (M3) from both members of each matched pair directly tests — rather than assumes — whether trace-level evidence suffices to tell 'agent could not do it' from 'there was nothing to do', with the first-party self-report and the trivial keyword heuristic bounding the problem from both sides.", mechanism_components: ["M3", "M4"], source: "inferred"}`
- `{challenge_id: "C3", argument_text: "Sweeping the unsolvable-confidence threshold (M5) and reporting both directional error rates plus risk–coverage curves operationalizes 'where is the boundary of calibrated refusal' as a measurable, per-task-family trade-off curve rather than a single fixed cutoff.", mechanism_components: ["M5"], source: "inferred"}`
- `{challenge_id: "C4", argument_text: "The generator (M1) mutates exactly one typed element while holding wording and environment size fixed, and the leakage audit (M6) verifies this held — surface-statistics matching, a near-chance text-only probe, and a 10% human audit — so measured rates reflect feasibility reasoning, not artifact detection.", mechanism_components: ["M1", "M6"], source: "inferred"}`

### unaddressed_challenges

`["C3"]` `[HYPOTHESIS]` — partially addressed only: the threshold sweep (M5) characterizes
the trade-off *within* the constructed benchmark's four task families, but whether a
threshold fitted on some families transfers to held-out families (let alone to naturally
occurring unsolvability) is measured only as a secondary transfer analysis and is expected
to remain open. (Per V-08: this rests on an inferred mechanism, not an extracted one, so it
is stated with that caveat rather than extracted-level confidence.)

### feasibility (order-of-magnitude)

`[HYPOTHESIS]` — *Pilot:* 100 pairs × 2 agents = 400 agent runs (≈10–30 steps each) + ≈400
LLM-judge attribution calls ⇒ API cost class **$150–500**, no GPU training, ≈1
person-week including operator implementation for 2 domains. *Scale-up:* 600 pairs (1,200
instances) × 3 agents = 3,600 runs, × 4 attribution baselines ≈ 15k–20k attribution calls ⇒
API cost class **$2k–5k**; optional AgenTracer-style tracer fine-tune adds <100 GPU-hours on
one A100-class card. *Annotation:* pair-validity audit of 10% (≈120 pairs × ~10 min) plus
disagreement adjudication ⇒ **20–40 annotator-hours** total; no other human labels are
needed because ground truth is oracle-generated (the seed's core economy: 真值机械成立).
*Single biggest feasibility risk:* the mutation operators leak surface cues (C4), which
would silently invalidate every downstream rate. *Mitigation:* M6 is a hard gate — the
text-only probe must be within a pre-registered margin of chance (e.g., AUROC < 0.60) per
domain before that domain's results count; leaking operators are repaired or dropped, and
the audit is reported in the paper regardless of outcome.

---

## N7 — Contributions

1. **CO1** — "A constructed benchmark of matched solvable/unsolvable task pairs across four
   agent domains (text-to-SQL, tool-calling, customer-service environments, command-line),
   with mechanically certified ground-truth labels, typed mutation-operator metadata, and a
   passing leakage audit — usable to stress-test any agent/attribution pipeline." `[HYPOTHESIS]`
   contribution_type: `dataset` · is_testable: `true` · has_rq: `true` (RQ_INF_1, RQ_INF_2)
2. **CO2** — "An empirical measurement of the rate at which current failure-attribution
   approaches (LLM-judge, trained tracer, first-party self-report) misclassify genuinely
   unsolvable tasks as agent failures — and the reverse — establishing this misattribution
   rate as a first measured quantity rather than an assumed-away edge case." `[HYPOTHESIS]`
   contribution_type: `empirical_finding` · is_testable: `true` · has_rq: `true` (RQ1, RQ_INF_1)
3. **CO3** — "A calibration-boundary analysis showing how the two directional misattribution
   rates trade off against an abstention/confidence threshold — reported as risk–coverage
   curves and threshold-free discrimination metrics per task family — giving a first
   characterization of where 'calibrated refusal' can be set for this class of tasks."
   `[HYPOTHESIS]`
   contribution_type: `empirical_finding` · is_testable: `true` · has_rq: `true` (RQ1)

**location** (all items): `"N/A — no paper exists yet"` `[PLACEHOLDER]`

---

## N8 — Research Questions

1. **RQ1** `[GIVEN]` (near-verbatim restatement of the seed's core question):
   "Can an agent and its failure-attribution system distinguish 'agent failure' from 'the
   task itself being unsolvable'? Where is the boundary of calibrated refusal?"
   - rq_source: `explicit`
   - evaluates_mechanisms: `["M3", "M4", "M5"]`
   - addresses_challenges: `["C2", "C3"]`
   - tests_contributions: `["CO2", "CO3"]`
   - answered_by_experiment: "Stage-2 run: 600 pairs × 3 agents; every attribution baseline
     scored against the oracle; threshold sweep on the unsolvable-confidence score; report
     FBR/CoR at fixed operating points plus AUROC, ECE, AURC and risk–coverage curves per
     domain, and cross-domain threshold transfer." `[HYPOTHESIS]`
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

2. **RQ_INF_1** `[HYPOTHESIS]` (inferred from the minimal experiment's explicit measurement
   target, a narrower operationalization of RQ1 — id kept stable from the prior digest):
   "At what rate do failure-attribution systems misclassify constructed unsolvable task
   instances as agent execution failures, across matched paired task suites?"
   - rq_source: `inferred`
   - evaluates_mechanisms: `["M1", "M2", "M4"]`
   - addresses_challenges: `["C1", "C4"]`
   - tests_contributions: `["CO1", "CO2"]`
   - answered_by_experiment: "Stage-1 pilot: build 100 pairs via M1/M2 (Spider + BFCL v3),
     run 2 agents, score the LLM-judge attribution baseline at its default threshold, and
     report the raw unsolvable→agent_failure rate with a bootstrap CI, prior to any
     threshold tuning." `[HYPOTHESIS]`
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

3. **RQ_INF_2** `[HYPOTHESIS]` (benchmark-validity question, mirroring the
   instrument-validation RQs in measurement-study exemplars):
   "Is the paired benchmark itself valid — i.e., do the mutation operators leave no surface
   leakage that lets a text-only observer detect unsolvability without feasibility
   reasoning?"
   - rq_source: `inferred`
   - evaluates_mechanisms: `["M1", "M6"]`
   - addresses_challenges: `["C4"]`
   - tests_contributions: `["CO1"]`
   - answered_by_experiment: "M6 audit: per-domain text-only probe AUROC vs. the 0.60
     pre-registered gate; surface-statistics matching tests; human audit agreement on the
     10% sample." `[HYPOTHESIS]`
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

**datasets** `[HYPOTHESIS]` `{source: "inferred", location: "N/A — no paper exists yet"}` — names:
- "Spider 1.0 (text-to-SQL; solvable sources + schema-mutation unsolvable variants)"
- "BIRD (text-to-SQL scale-up source, same mutation operators)"
- "Berkeley Function Calling Leaderboard (BFCL) v3 (tool-calling; removed-tool variants — its existing irrelevance-detection split is the closest natural precedent)"
- "τ-bench retail/airline (tool-agent environments; deleted-record and policy-contradiction variants)"
- "Terminal-Bench (command-line tasks; non-existent-resource variants)"
- "This paper's own paired suite derived from the above (the released artifact of CO1)"

**baselines** `[HYPOTHESIS]` `{source: "inferred", location: "N/A — no paper exists yet"}` — names:
- "LLM-judge attribution, all-at-once strategy (per [WhoWhen, arXiv:2505.00212])"
- "LLM-judge attribution, step-by-step strategy (per [WhoWhen, arXiv:2505.00212])"
- "AgenTracer-style trained tracer with label space extended by 'unsolvable' (per [AgenTracer, OpenReview:l05DseqvuD])"
- "First-party agent self-report / in-run infeasibility declaration (protocol adapted from [KnowCapable, OpenReview:EO6WtJ0q6G])"
- "Refusal-keyword + terminal-error heuristic (floor baseline)"

**metrics** `[HYPOTHESIS]` `{source: "inferred", location: "N/A — no paper exists yet"}` — names, with definitions:
- "False-blame rate (FBR): P(label=agent_failure | oracle=unsolvable) — the seed's headline quantity (不可解误判为 agent 失败的比率)"
- "Cop-out rate (CoR): P(label=unsolvable | oracle=solvable ∧ agent did not succeed)"
- "3-way macro-F1 over {success, agent_failure, unsolvable}"
- "AUROC of the unsolvable-confidence score against the oracle label (threshold-free discrimination)"
- "Expected Calibration Error (ECE, 10 equal-mass bins) of the unsolvable confidence"
- "Risk–coverage curve and AURC under threshold sweep (selective-prediction view of the boundary)"
- "Unsolvability Refusal Index: Spearman ρ between abstention confidence and oracle unsolvability (form borrowed from [RefusalIndex, OpenReview:9gJBhkLRat])"

**analysis plan** `[HYPOTHESIS]`: Placebo first (goal.md §5 step 1): the B0-p
null-by-construction placebo (sham inert-mutation pairs + shuffled-label check, paper.md
Step 6) is scored before any hypothesis; a non-null placebo invalidates the run. Stage 2
sample size: 600 pairs (150/domain; 1,200 instances) × 3 agents ⇒ ≥1,800
unsolvable-instance attribution decisions per baseline for the FBR class. Honest
CoR-denominator arithmetic: the CoR class conditions on *failed-solvable* instances, so
its n is agent-competence-dependent — under A3's allowed t⁺ success range [0.15, 0.90],
pooled failed-solvable n per baseline ranges ≈180–1,530; under the conservative p≈0.5
variance bound, one-sided power for the 10-pp gap at α = 0.05 exceeds 0.9 only when
failed-solvable n ≳ 400 (t⁺ success ≲ 0.78), and falls to ≈0.8 uncorrected (lower under
Holm) at the A3 worst case (n ≈ 180) — realized failed-solvable n and realized power are
reported per baseline, and any baseline below 0.8 realized power after Holm correction is
pre-declared INCONCLUSIVE, never null (paper.md RQ1 Verification). Primary hypothesis
test (directional-bias claim): per attribution system, compare FBR vs.
CoR with a two-proportion test computed by cluster bootstrap over pairs (10,000 resamples,
resampling at the pair level to respect the matched design), α = 0.05, Holm–Bonferroni
corrected across the 5 baselines; expected effect direction: FBR > CoR with an absolute gap
≥ 10 percentage points. Discrimination claim (H3): because "≥1 baseline per domain" selects
the best of 5 baselines within each domain, per-baseline AUROC CIs use the
Bonferroni-corrected 99% level (per-domain α = 0.05 preserved under selection).
Secondary: logistic regression of misattribution on {domain, operator type, agent family}
fixed effects to localize where the bias concentrates; report per-domain 95% bootstrap CIs
for every headline rate. Validity gate (RQ_INF_2): text-only probe AUROC must be < 0.60 per
domain, otherwise that domain's operators are repaired before RQ1/RQ_INF_1 analysis.

---

## N9 — Results

**CRITICAL NOTE**: No experiment has been run. Every result below is a
`[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`, `evidence_strength="missing"`,
`rq_answered=false`. Each carries an explicit **falsification condition** — the observation
that would disprove the hypothesized direction once the experiment is actually run. No
numbers below are measurements; the only numerals are pre-registered analysis thresholds.

1. **result_text**: "Current failure-attribution systems will show a directional bias:
   the false-blame rate (unsolvable→agent_failure) will exceed the cop-out rate
   (solvable-failed→unsolvable) by at least the pre-registered 10-pp margin for the
   LLM-judge and trained-tracer baselines, because their label spaces and training signals
   contain no feasibility category." `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`
   - rq_id: `RQ1`
   - result_type: `quantitative`
   - evidence_strength: `missing`
   - rq_answered: `false`
   - **falsification condition**: Refuted if, after the Holm-corrected cluster-bootstrap
     test, FBR − CoR is statistically indistinguishable from zero (or negative) for the
     majority of attribution baselines.
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

2. **result_text**: "The risk–coverage curve will have a usable knee: some confidence
   threshold reduces the false-blame rate substantially while sacrificing
   less-than-proportional coverage — i.e., the unsolvable-confidence score carries real
   discrimination signal (AUROC meaningfully above 0.5) even where hard classification
   fails." `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`
   - rq_id: `RQ1`
   - result_type: `quantitative`
   - evidence_strength: `missing`
   - rq_answered: `false`
   - **falsification condition**: Refuted if the risk–coverage curve is flat or
     monotonically 1:1 (every unit of misattribution reduction costs a proportional unit of
     coverage at every operating point) and the unsolvable-score AUROC is statistically
     indistinguishable from 0.5.
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

3. **result_text**: "The pilot benchmark (M1/M2, Spider + BFCL v3) will surface a nonzero,
   materially large baseline false-blame rate for the default LLM-judge attribution system
   before any threshold tuning — establishing that unsolvability confusion is a real,
   measurable phenomenon rather than a theoretical concern." `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`
   - rq_id: `RQ_INF_1`
   - result_type: `quantitative`
   - evidence_strength: `missing`
   - rq_answered: `false`
   - **falsification condition**: Refuted if the pilot false-blame rate is at or near zero
     (bootstrap CI overlapping zero) — i.e., attribution systems already cleanly separate
     the two classes untuned, and the premise of an open problem collapses.
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

4. **result_text**: "The mutation operators will pass the leakage gate: the text-only probe
   will score near chance (per-domain AUROC below the pre-registered 0.60 gate), and pair
   members will be statistically matched on surface statistics — validating that measured
   misattribution reflects feasibility reasoning rather than artifact detection."
   `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]`
   - rq_id: `RQ_INF_2`
   - result_type: `quantitative`
   - evidence_strength: `missing`
   - rq_answered: `false`
   - **falsification condition**: Refuted if the text-only probe exceeds the 0.60 AUROC
     gate on any domain after one operator-repair iteration — in which case that domain's
     headline rates must be withheld, and the construct itself (leak-free mechanical
     unsolvability injection) is shown harder than assumed.
   - location: `"N/A — no paper exists yet"` `[PLACEHOLDER]`

---

## N10 — Threats / Self-Limitations

`[HYPOTHESIS]` anticipated limitations of this kind of study (no author-stated threats
section exists since there is no paper; these are a pre-registration-style checklist):

1. **t1** — category: `construct` — "Mechanically constructed unsolvability (deleted column,
   removed tool, contradicted policy) may not represent naturally occurring unsolvability,
   which is often ambiguous, partial, or contested — the construct-validity gap between
   'unsolvable by design' and 'unsolvable in the wild' is unresolved by any within-benchmark
   result." `[HYPOTHESIS]`
   mitigation: "Use ≥3 typed operator families per domain and report rates per operator
   type; anchor with a small naturally-unanswerable set (e.g., TimeQA-style unanswerable
   items recast as retrieval-agent tasks) as an external sanity check, clearly separated
   from the headline mechanical-ground-truth results." `[HYPOTHESIS]`
2. **t2** — category: `external` — "Findings may not generalize beyond the tested agent
   backbones, attribution systems, and four task domains; in particular a threshold
   calibrated on these families may transfer poorly." `[HYPOTHESIS]`
   mitigation: "Test ≥3 agent model families and 5 attribution baselines; report all
   results per-domain (never only pooled); include an explicit held-out-domain threshold
   transfer analysis and state its result even if negative." `[HYPOTHESIS]`
3. **t3** — category: `internal` — "Mutation-induced confounds beyond solvability (length,
   phrasing, environment-size artifacts) could let systems discriminate for the wrong
   reason, inflating or deflating measured rates." `[HYPOTHESIS]`
   mitigation: "M6 as a hard pre-registered gate: surface-statistics matching, text-only
   probe AUROC < 0.60 per domain, and a 10% human pair audit — all reported in the paper
   regardless of outcome." `[HYPOTHESIS]`
4. **t4** — category: `conclusion` — "A single headline misattribution number is
   threshold-dependent; reporting it without the full curve, uncertainty, and multiple-
   comparison control could overstate or understate calibration quality." `[HYPOTHESIS]`
   mitigation: "Always pair operating-point rates with threshold-free metrics (AUROC,
   Refusal-Index correlation, AURC) and full risk–coverage curves; cluster-bootstrap CIs at
   the pair level; Holm–Bonferroni across baselines per the pre-registered analysis plan."
   `[HYPOTHESIS]`
5. **t5** — category: `construct` — "LLM-judge attribution baselines are prompt-sensitive:
   a poorly worded 3-way prompt could understate what LLM judges can do, making the field
   look worse than it is (a strawman-baseline risk)." `[HYPOTHESIS]`
   mitigation: "Use the two prompting strategies established by prior attribution work
   (all-at-once and step-by-step, per [WhoWhen, arXiv:2505.00212]) plus ≥3 paraphrased
   prompt variants per strategy; report variance across variants and take each baseline's
   best variant for headline comparisons." `[HYPOTHESIS]`
6. **t6** — category: `construct` — "The source benchmarks (Spider/BIRD, BFCL v3, τ-bench,
   Terminal-Bench) are famous and plausibly memorized by agent and attributor backbones:
   'unsolvability detection' could partially be mutation-detection-by-diff against a
   memorized original — a channel the text-only leakage probe is structurally blind to,
   since only a backbone that memorized the source can exploit it." `[HYPOTHESIS]`
   mitigation: "Budget-matched surface-anonymization control (paper.md B-alt2): rerun the
   strongest LLM-judge on consistently renamed schema/tool/entity variants of a 20% pair
   subset per domain (oracle labels re-verified after renaming); a pre-registered
   FBR/AUROC shift floor decides whether the memorization rival wins for that domain, with
   the anonymized-variant rates replacing famous-source rates as that domain's headline if
   it does." `[HYPOTHESIS]`

**status**: `PARTIAL` (these are anticipated, not author-acknowledged, threats).
**absence_comment**: `{"what_missing": "No Limitations/Threats-to-Validity section exists because no paper has been written.", "why_matters": "A reader could mistake these anticipated threats for the authors' own acknowledged limitations, which carry more weight than a third party's guesses.", "implication": "Treat t1–t6 as a pre-registration-style checklist for what the eventual paper's real Limitations section should cover, not as confirmed self-critique."}`

---

## N11 — Artifacts

**artifacts**: `[]`
**has_code**: `false`
**has_data**: `false`
**has_model**: `false`
**status**: `NOT_FOUND` `[PLACEHOLDER]`
**absence_comment**: `{"what_missing": "No code, benchmark data, or model has been released because the paper described here does not yet exist.", "why_matters": "Reviewers and downstream users cannot verify or reuse anything until the paired-task benchmark (CO1), the mutation-operator library (M1), the solvability oracle (M2), and the attribution battery (M4) are actually built and shared.", "implication": "Any future reader should treat all three artifact flags as false until a real release accompanies a real paper; the natural release set is the paired suite + oracle scripts + harness logs."}`

---

## N12 — Contribution Type

- **value**: `empirical` `[HYPOTHESIS]`
- **rationale**: "Re-checked against the schema's disambiguation rules. The seed frames the
  deliverable as a measurement — '测归因系统把不可解误判为agent失败的比率' — and every projected N9
  result validates a measured quantity (misattribution rates, calibration curves), with the
  paired benchmark (CO1) serving as the instrument that makes the measurement possible, not
  as the headline product. This matches the schema's rule ('measurement study with a
  published dataset → empirical if the study is the main contribution, dataset if the
  dataset is') and the pattern of comparable measurement-study exemplars whose released
  datasets support the finding rather than constitute it. The plausible alternative reading
  — `benchmark`, if the community adopts the paired suite as a reusable evaluation target
  and the paper's framing shifts to 'we introduce a benchmark of N pairs' — is noted
  explicitly; under the seed's own wording, `empirical` fits better." `[HYPOTHESIS]`
- **source**: `inferred`

---

## Claims

1. `[HYPOTHESIS]` "Failure-attribution systems will show a systematic directional bias toward
   misclassifying genuinely unsolvable tasks as agent failures, rather than the reverse."
   - evidence: `[{type: "argument", text: "The strongest current attribution formulations define the output as the agent-step pair whose counterfactual correction flips failure to success ([AgenTracer, OpenReview:l05DseqvuD], [WhoWhen, arXiv:2505.00212]) — a label space with no admissible 'no one was at fault' outcome, so unsolvable instances are structurally forced into agent-fault labels.", source: "inferred", location: "N/A — no paper exists yet"}]`
2. `[HYPOTHESIS]` "A calibration boundary (an abstention/confidence threshold) exists at which
   the false-blame rate can be reduced substantially without a proportional loss of coverage."
   - evidence: `[{type: "argument", text: "Selective-prediction machinery repeatedly finds non-trivial risk–coverage operating points when a meaningful confidence signal exists — with guarantees in the LLM-judge setting ([TrustOrEscalate, OpenReview:UHPnqSTBPO]) and trainable confidence in reasoning models ([RLCR, OpenReview:ASQ649zdHm]) — motivating the same expectation here, though neither work calibrates against verified task infeasibility, which is exactly what remains untested.", source: "inferred", location: "N/A — no paper exists yet"}]`
3. `[GIVEN]` "Unsolvability of the constructed task pairs is guaranteed by construction, making
   ground truth mechanically verifiable rather than a matter of judgment."
   - evidence: `[{type: "argument", text: "Directly stated in the seed's minimal-experiment description: '不可解性由构造保证，真值机械成立'; operationalized here as typed mutation operators (M1) plus a script-level requirement/no-substitute oracle (M2).", source: "extracted", location: "seed README, minimal experiment line"}]`
4. `[HYPOTHESIS]` "Refusal calibrated to a model's own knowledge boundary is not the same
   construct as refusal calibrated to task-level unsolvability, and the two must be
   dissociated by construction to measure either cleanly."
   - evidence: `[{type: "argument", text: "Knowledge-aware refusal work calibrates refusal against the model's own error probability ([RefusalIndex, OpenReview:9gJBhkLRat]) and capability self-assessment predicts 'will I succeed' on all-solvable testbeds ([KnowCapable, OpenReview:EO6WtJ0q6G]); neither setting contains instances that are unsolvable for everyone, so the dissociation this paper's paired design provides has not been measured before.", source: "inferred", location: "N/A — no paper exists yet"}]`
5. `[PLACEHOLDER]` "The actual misattribution rates, the shape of the calibration curve, which
   attribution systems perform best, and whether the leakage gate passes are all unknown
   until the experiment described here is actually run."
   - evidence: `[{type: "observation", text: "No experiment has been conducted; this digest is speculative scaffolding with pre-registered directions and falsification conditions only.", source: "inferred", location: "N/A — no paper exists yet"}]`

---

## Self-verification pass (per `self-verification.md`)

- **V-01 (locator integrity)**: No item is tagged `source="extracted"` with `status="FOUND"`
  and a missing locator — the only extracted-verbatim items (N1.constraints, RQ1, Claim 3)
  point to the seed README; every hypothesis/placeholder item uses the explicit
  `"N/A — no paper exists yet"` locator; every `[GROUNDED:corpus]` N3 entry carries its
  corpus `paper_id` + `paper_url` as its locator.
- **V-02 (absence comment shape)**: Every non-FOUND node (N0 partial fields, N2, N10, N11)
  has a full 3-part `absence_comment`.
- **V-04 (ID consistency)**, checked string-for-string:
  - `N4.affects_works` ⊆ N3 citation_keys: `[AgenTracer, OpenReview:l05DseqvuD]`,
    `[WhoWhen, arXiv:2505.00212]`, `[MAST, arXiv:2503.13657]`,
    `[RefusalIndex, OpenReview:9gJBhkLRat]`, `[SilenceIsGolden, OpenReview:PhUCxfS0yf]`,
    `[KnowCapable, OpenReview:EO6WtJ0q6G]`, `[TrustOrEscalate, OpenReview:UHPnqSTBPO]`,
    `[RLCR, OpenReview:ASQ649zdHm]`, `[EHR-ChatQA, OpenReview:hLweUPBz7k]` — all 9 N3 keys
    used or available; every N4 string appears verbatim in N3 ✓
  - `N6.challenge_arguments[].challenge_id` ⊆ {C1–C4} ✓ (all four covered)
  - `N6.challenge_arguments[].mechanism_components` ⊆ {M1–M6} ✓
  - `N6.unaddressed_challenges` = {C3} ⊆ {C1–C4} ✓
  - `N8.addresses_challenges`: RQ1→{C2,C3}, RQ_INF_1→{C1,C4}, RQ_INF_2→{C4} ⊆ {C1–C4} ✓
  - `N8.tests_contributions`: RQ1→{CO2,CO3}, RQ_INF_1→{CO1,CO2}, RQ_INF_2→{CO1} ⊆ {CO1–CO3} ✓
    (matches N7 `has_rq` annotations: CO1←RQ_INF_1/RQ_INF_2, CO2←RQ1/RQ_INF_1, CO3←RQ1 ✓)
  - `N8.evaluates_mechanisms`: RQ1→{M3,M4,M5}, RQ_INF_1→{M1,M2,M4}, RQ_INF_2→{M1,M6} ⊆ {M1–M6} ✓
  - `N9.results[].rq_id` ⊆ {RQ1, RQ_INF_1, RQ_INF_2} — r1,r2→RQ1; r3→RQ_INF_1; r4→RQ_INF_2 ✓
  - `RQ_INF_1` id retained verbatim from the prior digest revision, per continuity rule ✓
- **V-08**: `N6.unaddressed_challenges = ["C3"]` is flagged explicitly as resting on an
  inferred mechanism (M5's threshold sweep + transfer analysis), not presented with
  extracted-level certainty.
- **V-10/V-11**: N10 status `PARTIAL` with non-empty `threats` (6 items, 4 categories:
  construct×3, external, internal, conclusion — each with a mitigation); N11 status
  `NOT_FOUND` with empty `artifacts` and all three flags `false` — consistent.
- **V-12**: N12 rationale cites the seed's own wording ("测归因系统把不可解误判为agent失败的比率") and
  the schema's empirical-vs-dataset disambiguation rule, and names the plausible alternative
  (`benchmark`) — not circular.
- **N9 fabrication check**: no invented measurements; the only numerals in N9/N8 analysis
  text are pre-registered thresholds (10-pp margin, α=0.05, 0.60 AUROC gate, 10k bootstrap
  resamples), each labeled as such; all four results carry `evidence_strength="missing"`,
  `rq_answered=false`, and an explicit falsification condition.
- **Field-name spot check**: `objective`, `motivations`, `citation_key`, `approach_summary`,
  `limitation_text`/`affects_works`, `text` (challenges), `key_components`/
  `challenge_arguments`/`unaddressed_challenges`, `rq_source`/`evaluates_mechanisms`/
  `addresses_challenges`/`tests_contributions`/`answered_by_experiment`, `rq_id`/
  `result_type`/`evidence_strength`/`rq_answered`, `category`/`mitigation`, `has_code`/
  `has_data`/`has_model`, `value`/`rationale` — all match the node schema exactly.
- **Empty-node check**: All of N0–N12 present, including the NOT_FOUND node (N11) and the
  Claims list.
