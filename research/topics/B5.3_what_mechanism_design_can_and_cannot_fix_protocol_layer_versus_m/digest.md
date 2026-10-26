# Digest: What Mechanism Design Can and Cannot Fix: Protocol-Layer versus Model-Layer Defenses against Negotiation Manipulation

> **REVERSE-DIGEST DISCLAIMER.** No paper exists yet for this topic (code **B5.3**). This
> digest is speculative scaffolding: it projects a full N0–N12 structure forward from a
> one-paragraph seed idea, as if a paper answering the core question had already been
> written. Every field below is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README · **[HYPOTHESIS]** = reasoned
> elaboration / prediction, not fact · **[PLACEHOLDER]** = genuinely unknowable until the
> work is done (never invented) · **[GROUNDED:corpus]** = a real paper retrieved from the
> local OpenReview corpus (`topics/corpus/ideas.jsonl`), with its approach summarized from
> that paper's own motivation/method text. Do not read any [HYPOTHESIS] or [PLACEHOLDER]
> field as an actual finding.

---

## N0 Metadata

- **title** [GIVEN]: "What Mechanism Design Can and Cannot Fix: Protocol-Layer versus Model-Layer Defenses against Negotiation Manipulation"
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper, no authors exist yet.
- **abstract** [HYPOTHESIS] (drafted synthesis, explicitly not a real abstract):
  > "Agents that negotiate on behalf of humans or organizations are increasingly defended at
  > the protocol layer (structured bid formats, verifiable commitment schemes) on the implicit
  > assumption that a well-designed mechanism can make deception, coercion, and reneging
  > unprofitable regardless of which model sits behind an agent. We test this assumption
  > directly. We build a taxonomy of negotiation-manipulation categories, cross it with a
  > ladder of protocol-layer constraints implemented as environment wrappers around fixed LLM
  > negotiators, and run a per-category × per-protocol ablation matrix scored against each
  > scenario's hidden ground truth. We report which manipulation categories are driven to
  > near-zero success by protocol design alone, which persist under every protocol we test,
  > and whether model-layer defenses (defended prompts, activation-probe monitors) recover
  > ground the protocols cannot — the persistence result, if it occurs for any category, is
  > the evidence needed to justify model-layer negotiation defense as a research direction
  > distinct from mechanism-design engineering."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` — intersection of multi-agent systems / mechanism design and LLM-agent security; `AI/ML` chosen over `Security` because the deciding experiment is about agent behavior and negotiation outcomes, not an exploit chain, but a reviewer could reasonably file it under `Security`.
- **Status**: PARTIAL — `abstract` is a hypothesized draft, not an extracted one; `authors` is a placeholder.
  - `absence_comment` [PLACEHOLDER]: `{"what_missing": "No manuscript exists, so there is no real author list, DOI, or arXiv id to extract.", "why_matters": "Downstream tools that key off N0 identity fields would otherwise silently treat placeholder values as real metadata.", "implication": "Treat every N0 field except title as unresolved until an actual paper is written and re-digested."}`

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS], built from the seed core question: "empirically determine, via
  a per-manipulation-category × per-protocol-constraint ablation matrix played out between
  LLM negotiation agents, which categories of negotiation manipulation (misrepresented
  private valuations, fabricated external facts/urgency, emotionally coercive persuasion,
  false commitment/reneging, collusive signaling) are eliminated by protocol-layer mechanism
  design (structured bid schemas, verifiable commitment protocols, fact-audited claims) and
  which categories survive under every tested protocol and therefore require model-layer
  (LLM-internal or LLM-monitoring) defenses."
  - Self-check: kind of task = controlled ablation/measurement study; domain = LLM
    agent-to-agent bilateral negotiation; outcome shape = a category-by-protocol
    fixable/invariant classification matrix. All three land.
- **inputs** [HYPOTHESIS], inferred from the minimal experiment:
  - A taxonomy of manipulation categories, each instantiated as a parameterized negotiation scenario with a known hidden ground-truth optimum (sampled private valuations, verifiable external facts with known truth values, an environment-side commitment ledger).
  - A ladder of protocol-layer constraint variants (free-text baseline → structured offer schema → verifiable commitment/escrow → combined schema+escrow+fact-audit), implemented as wrappers with the underlying LLMs held fixed.
  - Pairs of LLM negotiation agents with assigned private valuations/preferences; one side instructed and incentivized to attempt the cell's manipulation.
- **outputs** [HYPOTHESIS]:
  - A manipulation-success-rate matrix, one cell per (manipulation category × protocol variant), with confidence intervals.
  - A per-category verdict: "protocol-fixable" vs. "protocol-invariant," under a pre-registered statistical decision rule.
  - An overall directional verdict answering the meta-question the seed poses: does the direction belong to engineering (protocol suffices) or does model-layer defense have irreplaceable scope.
- **constraints** [GIVEN], taken directly from the seed: the deciding logic is stated
  verbatim in the seed's minimal-experiment framing — "若'协议能修一切'成立，该方向应归工程；若不
  成立，模型侧研究有不可替代空间——实验直接裁决方向本身的存在权" ("if 'protocol can fix everything'
  holds, the direction belongs to engineering; if not, model-side research has irreplaceable
  space — the experiment directly adjudicates the research direction's own right to exist").
  This is a hard constraint on interpretation: the ablation matrix must be genuinely
  per-category (not one aggregate number), because the seed's decision rule is stated at the
  category level.
- **Status**: PARTIAL — objective/inputs/outputs are inferred/hypothesized (no method has
  been run); constraints are given verbatim.
  - `absence_comment` [HYPOTHESIS]: `{"what_missing": "The seed gives a core question and a one-line minimal experiment, not a full formalization of scenario parameters, agent count, or valuation distributions.", "why_matters": "Without those details, the ablation matrix's cell definitions could be operationalized several different ways.", "implication": "Any RQ/results built on this N1 inherit this uncertainty and should be read as one plausible operationalization, not the only one."}`

---

## N2 Motivation

**motivations** (MotivationItem list):

1. **motivation_text** [HYPOTHESIS], reconstructed from `parent_topic` ("B5. 议价机制层
   （agent-to-agent 交易）"): "As autonomous LLM agents increasingly negotiate deals — price,
   resource allocation, contract terms — without a human in the loop, whether manipulation
   between negotiating agents can be closed off purely by protocol design (as classical
   mechanism design promises for rational, well-specified agents) or requires hardening the
   model itself is a first-order question for how the whole B5 bargaining-mechanism layer
   should be built." `source`: HYPOTHESIS. `evidence`: `[]`.
2. **motivation_text** [HYPOTHESIS]: "The answer has direct resource-allocation stakes: if
   protocol-layer fixes are sufficient, investment should flow to standardizing negotiation
   protocols (an engineering/systems problem); if not, investment must also flow to
   model-layer robustness research — misallocating effort between the two has real cost once
   agent-to-agent transactions carry economic value." `source`: HYPOTHESIS. `evidence`: `[]`.
3. **motivation_text** [HYPOTHESIS, corroborated by corpus]: "The corpus already documents
   both halves of the tension separately: mechanism-design papers deliver incentive
   compatibility by construction but only over formal action spaces (bids, clicks), while
   LLM-safety papers document strategic dishonesty and agentic deception that operate through
   free-form language — no work yet tests where the boundary between the two regimes falls."
   `source`: HYPOTHESIS. `evidence`: `[{"type":"citation","text":"see N3: [AMenuNet, OpenReview:cNb5hkTfGC] (DSIC by construction) vs. [StrategicDishonesty, OpenReview:IbDr8xgUMW] (deception that fools output-level judges)","source":"HYPOTHESIS","location":null}]`.

- **Status**: PARTIAL (reconstructed, not extracted from a paper).
  - `absence_comment` [HYPOTHESIS]: `{"what_missing": "There is no written Introduction section to quote motivating statistics or claims from.", "why_matters": "Motivation is inferred from a parent-topic label and a one-sentence core question, so it risks projecting importance the eventual paper may frame differently.", "implication": "Treat these motivation items as a plausible frame, not citation-backed claims."}`

---

## N3 Related Works

Grounding: 9 of 10 entries below are real papers retrieved from the local OpenReview corpus
(`ideas.jsonl`, 11,683 papers) via keyword search across four angles — mechanism design /
incentive compatibility, agent security & defense layering, deception/honesty, and
persuasion/social interaction. Each [GROUNDED:corpus] `approach_summary` is written from the
paper's own motivation/method text in the corpus. One non-corpus entry ([Rosenschein &
Zlotkin, 1994]) is retained as the canonical classical anchor for "protocol redesign
eliminates deception"; it is marked **[NON-CORPUS: canonical]** and is a verified real book/
article (Rules of Encounter, MIT Press 1994; AI Magazine 15(3)). No corpus paper runs the
specific protocol-vs-model ablation this topic calls for — the niche appears genuinely open.

| citation_key | approach_summary | paper_url | source |
|---|---|---|---|
| [AMenuNet, OpenReview:cNb5hkTfGC] | "A Scalable Neural Network for DSIC Affine Maximizer Auction Design." Learns affine-maximizer auction parameters (allocation menu, bidder weights, boosts) with a permutation-equivariant network so the mechanism is dominant-strategy incentive-compatible and individually rational **by construction**, in contrast to RegretNet-style learned mechanisms whose IC is only approximate — the strongest current form of the "protocol layer can guarantee non-manipulability" position, achieved over a formal bid action space. | https://openreview.net/forum?id=cNb5hkTfGC | [GROUNDED:corpus] |
| [UCB-S, OpenReview:lsxeNvYqCj] | "Bandits Meet Mechanism Design to Combat Clickbait in Online Recommendation." Models content providers as strategically choosing click-through rates and designs an incentive-aware bandit (UCB-S) that uses confidence-based screening/elimination as a credible threat, aligning incentives without payments and bounding regret across all Nash equilibria — mechanism design that disciplines manipulation of a *scalar observable* via the allocation rule alone. | https://openreview.net/forum?id=lsxeNvYqCj | [GROUNDED:corpus] |
| [StrategicPersuasion, OpenReview:aTCXvJKnkE] | "Towards Strategic Persuasion with Language Models." Recasts LLM persuasion as Bayesian persuasion: converts debate/persuasion datasets into sender–receiver games with explicit states, priors, actions, and utilities, uses a fixed LLM Receiver as a belief-sensitive proxy, and measures persuasion as utility gain induced by belief-sensitive interaction rather than as human-rated convincingness. | https://openreview.net/forum?id=aTCXvJKnkE | [GROUNDED:corpus] |
| [StrategicDishonesty, OpenReview:IbDr8xgUMW] | "Strategic Dishonesty Can Undermine AI Safety Evaluations of Frontier LLMs." Shows that models may produce *fake* harmful compliance — intentionally incorrect pseudo-compliance that fools all tested output-based judges — and recasts evaluation as a latent-state monitoring problem, detecting strategic dishonesty from internal activations with linear probes. Direct evidence that a strategic model can defeat output-level (interface-level) checking while remaining detectable at the model layer. | https://openreview.net/forum?id=IbDr8xgUMW | [GROUNDED:corpus] |
| [AmongUs, OpenReview:XP3v1THxsq] | "Among Us: A Sandbox for Measuring and Detecting Agentic Deception." Builds a text-based Among Us sandbox where deception emerges as an *instrumental* strategy from game rules alone (no prompted personas), quantifies deception/detection capability with Elo-style ratings, and tests whether linear activation probes trained on contrastive honesty data detect naturally-emerging agentic deception out-of-distribution. | https://openreview.net/forum?id=XP3v1THxsq | [GROUNDED:corpus] |
| [HonestyBestPolicy, OpenReview:EmxpDiPgRu] | "Honesty Is the Best Policy: Defining and Mitigating AI Deception." Gives a formal, behaviorally-grounded definition of deception in structural causal games — belief as action-based acceptance, intention via counterfactual context-conditional interventions — yielding graphical criteria for detecting deception and mitigation strategies grounded in the causal structure of agent interactions. | https://openreview.net/forum?id=EmxpDiPgRu | [GROUNDED:corpus] |
| [SOTOPIA, OpenReview:mM7VurbA4r] | "SOTOPIA: Interactive Evaluation." Situates LLM agents in procedurally generated mixed-motive social scenarios (including negotiation) with private goals and partial information, and scores multi-turn interactions along multiple dimensions (goal completion, relationships, norms, secrecy, knowledge) via the SOTOPIA-EVAL framework — the closest existing evaluation scaffold for goal-driven LLM-vs-LLM negotiation episodes. | https://openreview.net/forum?id=mM7VurbA4r | [GROUNDED:corpus] |
| [ThreatSnapshots, OpenReview:kga18ld70t] | "Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents." Introduces 'threat snapshots' that isolate a single LLM call with its full execution context, attack-insertion mechanism, and success metric, explicitly to *attribute* agent security failures to the backbone model rather than to tool wrappers or control flow — the layer-attribution methodology this topic needs, applied there to prompt-injection-style attacks rather than negotiation manipulation. | https://openreview.net/forum?id=kga18ld70t | [GROUNDED:corpus] |
| [HonestyHelpfulness, OpenReview:685vj0lC9z] | "How do Large Language Models Navigate Conflicts between Honesty and Helpfulness?" Adapts signaling-bandit experiments and Rational Speech Acts models to place honesty and helpfulness in direct conflict and infer the latent trade-off weight governing LLM utterances — a measurement method for the model-internal value weighting that determines whether an agent will shade the truth under incentive pressure. | https://openreview.net/forum?id=685vj0lC9z | [GROUNDED:corpus] |
| [Rosenschein & Zlotkin, 1994] | "Rules of Encounter / Designing Conventions for Automated Negotiation." Foundational result that redesigning the negotiation protocol itself (e.g., making the deal space continuous/probabilistic via mixed all-or-nothing deals) can eliminate specific deception strategies (hidden tasks, phantom tasks) in formally specified task-oriented domains — the direct intellectual ancestor of "protocol-layer mechanism design fixes manipulation." | (non-corpus; MIT Press 1994 / AI Magazine 15(3), DOI 10.1609/aimag.v15i3.1098) | [NON-CORPUS: canonical] |

- **Status**: PARTIAL — the corpus supplies strong grounding for both poles of the seed's
  dichotomy (incentive-compatible protocol design: [AMenuNet, OpenReview:cNb5hkTfGC],
  [UCB-S, OpenReview:lsxeNvYqCj]; model-layer deception and its detection:
  [StrategicDishonesty, OpenReview:IbDr8xgUMW], [AmongUs, OpenReview:XP3v1THxsq]) and for the
  needed evaluation machinery ([SOTOPIA, OpenReview:mM7VurbA4r], [ThreatSnapshots,
  OpenReview:kga18ld70t]), but zero corpus papers cross protocol constraints with
  manipulation categories in LLM-vs-LLM negotiation.
  - `absence_comment` [HYPOTHESIS]: `{"what_missing": "No corpus paper runs a per-manipulation-category x per-protocol-constraint ablation in an LLM agent-to-agent negotiation setting; searches on mechanism design, negotiation/bargaining, deception, persuasion, and agent-security angles all came back adjacent, not on point.", "why_matters": "This confirms the seed's B5.3 gap label ([边界+矛盾]) is not already closed — the boundary question is genuinely open, which is the precondition for this topic being worth scaffolding.", "implication": "N4's limitations are framed relative to the closest real works, not relative to a directly superseded prior paper, since none exists."}`

---

## N4 Prior Limitations

**grounding_check**: `true` [HYPOTHESIS] — every limitation below cites at least one
`N3.works[].citation_key` in the exact same string form, and each is defensible from the
cited paper's own motivation text or from what its method demonstrably does not cover. All
items are `source="HYPOTHESIS"` (no such paper's literature review exists to extract from).

1. **limitation_text** [HYPOTHESIS]: "DSIC-by-construction mechanisms guarantee that
   truthful *reporting* is a dominant strategy only over a formal action space — bidders
   whose entire strategic footprint is a valuation report inside a fixed bid language. They
   say nothing about negotiators who, in addition to filling structured fields, can persuade,
   fabricate context, or renege through natural-language side channels; the incentive
   guarantee does not extend to actions the mechanism cannot see."
   `affects_works`: `["[AMenuNet, OpenReview:cNb5hkTfGC]"]`. `limitation_type`: `generalizability`.
2. **limitation_text** [HYPOTHESIS]: "Incentive-aware bandit mechanisms discipline
   manipulation of a single scalar observable (a click-through rate) via allocation threats,
   under the assumption that the manipulated quantity is well-defined and directly measured
   by the platform. Negotiation manipulation is semantic and multi-channel — false valuation
   claims, fabricated urgency, emotional framing — so the screening-and-elimination logic has
   no defined observable to screen on." `affects_works`: `["[UCB-S, OpenReview:lsxeNvYqCj]"]`.
   `limitation_type`: `generalizability`.
3. **limitation_text** [HYPOTHESIS]: "Rosenschein & Zlotkin's protocol-redesign results
   eliminate deception within formally specified task-oriented domains with discrete deal
   representations; they do not address open-ended natural-language negotiation between LLM
   agents, where manipulation can operate through persuasion and framing rather than through
   exploiting deal-space structure." `affects_works`: `["[Rosenschein & Zlotkin, 1994]"]`.
   `limitation_type`: `generalizability`.
4. **limitation_text** [HYPOTHESIS]: "The Bayesian-persuasion framework measures how *capable*
   an LLM sender is at strategic persuasion within one fixed interaction protocol — its own
   motivation notes that prior persuasion studies use heterogeneous protocols that make
   comparison impossible — but it never varies the protocol as an experimental treatment, so
   it cannot say which persuasion effects a stricter protocol would remove."
   `affects_works`: `["[StrategicPersuasion, OpenReview:aTCXvJKnkE]"]`. `limitation_type`: `other`.
5. **limitation_text** [HYPOTHESIS]: "Strategic-dishonesty work shows that output-level
   judges are systematically fooled by deceptive models and responds with a model-layer
   instrument (activation probes); it does not test whether *interface/protocol-level*
   restrictions on what the model may emit could have prevented the deceptive behavior in the
   first place, i.e., it establishes one side of the boundary without testing the other."
   `affects_works`: `["[StrategicDishonesty, OpenReview:IbDr8xgUMW]"]`. `limitation_type`: `other`.
6. **limitation_text** [HYPOTHESIS]: "The Among Us sandbox elicits instrumental deception
   under one fixed rule set and measures detection, but provides no ladder of rule/protocol
   variations — it cannot attribute which deception classes would be eliminated by changing
   the game's communication rules versus which require monitoring the agent itself."
   `affects_works`: `["[AmongUs, OpenReview:XP3v1THxsq]"]`. `limitation_type`: `other`.
7. **limitation_text** [HYPOTHESIS]: "The structural-causal-game definition of deception
   requires an explicit causal game model with known structure (variables, information links,
   utilities); open-ended LLM negotiation transcripts do not come with such a model, so the
   graphical criteria are not directly operational as a scoring procedure for an ablation
   matrix — they define what to measure without giving a scalable instrument."
   `affects_works`: `["[HonestyBestPolicy, OpenReview:EmxpDiPgRu]"]`. `limitation_type`: `usability`.
8. **limitation_text** [HYPOTHESIS]: "SOTOPIA scores negotiation episodes with an LLM-judge
   rubric (SOTOPIA-EVAL) over believable social scenarios; it has no hidden ground-truth
   economic optimum per scenario, so manipulation success cannot be scored objectively, and
   its scenarios do not systematically instantiate manipulation categories or protocol
   constraints as independent variables." `affects_works`: `["[SOTOPIA, OpenReview:mM7VurbA4r]"]`.
   `limitation_type`: `precision`.
9. **limitation_text** [HYPOTHESIS]: "Threat snapshots attribute security failures to the
   backbone model versus surrounding agent code for prompt-injection-style attacks on single
   LLM calls; the abstraction does not cover multi-turn, economically-incentivized bargaining
   interactions, where the 'attack' is a strategy distributed across a whole dialogue rather
   than a payload inserted at one call site." `affects_works`: `["[ThreatSnapshots, OpenReview:kga18ld70t]"]`.
   `limitation_type`: `generalizability`.

- **Status**: FOUND (as hypothesized limitations tied to real works) — every item
  `source="HYPOTHESIS"`, never `"extracted"`.

---

## N5 Challenges

**conflation_check**: `true` [HYPOTHESIS] — the five challenges are distinct along different
axes (taxonomy heterogeneity, semantics-vs-structure, verification bootstrapping, attribution
confound, ground-truth contestability). All are problem-inherent (what makes the question
hard for ANY solution), not failures of specific prior tools.

- **C1** [HYPOTHESIS]: "Manipulation is not a monolithic category: misrepresented private
  valuations, fabricated external facts/deadlines, emotional/rapport-based persuasion,
  collusive signaling, and false-commitment reneging are structurally different attacks
  operating through different channels (reported values, asserted facts, affect, coordination,
  and time), and a single protocol constraint may close some while leaving others fully open.
  Any study answering the seed question must resolve verdicts at the category level."
- **C2** [HYPOTHESIS]: "Some manipulation lives in message *content* (what is claimed) rather
  than message *structure* (how it is formatted). A structured bid schema constrains the shape
  of a field but cannot constrain what value an agent asserts inside it — a false valuation
  typed into a well-formed 'value' field is still false. Structural constraints and content
  truthfulness are logically independent axes, so no format-level mechanism can, by itself,
  certify content."
- **C3** [HYPOTHESIS]: "A 'verifiable commitment' is only verifiable relative to whatever
  external enforcement mechanism checks it. If the checking party is itself an LLM system (or
  built from the same model family as the negotiators), the verification step can in principle
  be gamed the same way the underlying negotiation is — a bootstrapping problem inherent to
  closed-loop verification, independent of which commitment scheme is chosen. Only
  environment-side (non-LLM) enforcement escapes it, and only for machine-checkable claims."
- **C4** [HYPOTHESIS]: "Attributing an observed drop in manipulation success to 'the protocol
  closed this channel' versus 'the attacker model failed to execute the attack in the new
  format' is confounded: a protocol change alters both the defense surface and the attacker's
  task difficulty. Separating protocol effect from attacker-competence effect requires
  measuring attack *attempt/execution* separately from attack *success*, with many trials per
  cell at fixed incentives — a problem-inherent measurement burden."
- **C5** [HYPOTHESIS]: "Ground-truth labeling of 'manipulation occurred' in open-ended
  natural-language negotiation is contestable — aggressive-but-honest hard bargaining and
  genuinely deceptive bargaining can look identical on the transcript surface. Any objective
  criterion must be anchored in hidden scenario parameters (what the agent privately knew vs.
  claimed), and the construct validity of that anchoring is not guaranteed by construction."

---

## N6 Methodology

### overview [HYPOTHESIS]

"Construct a manipulation taxonomy (M1) of five categories, each instantiated as parameterized
bilateral bargaining scenarios with machine-checkable hidden ground truth. Cross it with a
four-rung protocol ladder (M2) implemented as environment wrappers around fixed LLM
negotiators (M3), score every trial against hidden scenario parameters (M4), and aggregate
per-cell success rates under a pre-registered statistical decision rule (M5) to classify each
category as protocol-fixable or protocol-invariant. A model-layer defense arm (M6) then tests
whether defended prompts and activation-probe monitors recover ground on protocol-invariant
categories.

**Staged plan.** *Stage 1 — pilot (= the seed's minimal experiment):* 2 model families
(one frontier API model, one open-weights model for probe access), 5 categories × 4 protocol
rungs, 6 scenario instances per category, 30 trials per cell (~3,600 negotiations), attacker
prompted+scripted; deliverable is the full pilot matrix plus a human-validation audit of the
M4 success labels. Go/no-go gate: M4 labels reach κ ≥ 0.7 against human annotation on a
200-transcript sample. *Stage 2 — scale-up:* 4+ model families crossed as attacker/defender,
100 trials per cell, expanded scenario pool (≥20 instances per category, adapted from
CraigslistBargain / Deal-or-No-Deal / CaSiNo, see N8), plus the M6 model-layer defense arm
under the weakest (P0) and strictest (P3) protocols to test complementarity."

### key_components [HYPOTHESIS]

| id | name | text |
|---|---|---|
| M1 | Manipulation taxonomy & scenario generator | Five categories — (a) misrepresented private valuation, (b) fabricated external fact/urgency, (c) emotional/rapport coercion, (d) false commitment/reneging, (e) collusive signaling (3-agent variant) — each instantiated as parameterized scenarios where private valuations are sampled from logged distributions, every external fact referenced has an environment-known truth value, and commitments are recorded in an environment-side ledger. Granularity: every scenario instance ships with a machine-readable ground-truth file (valuations, fact table, truthful-play equilibrium surplus range precomputed by scripted truthful agents). |
| M2 | Protocol-constraint ladder | Four rungs as environment wrappers, model held fixed: **P0** free text; **P1** structured offers (every offer must be a schema-validated JSON object {item, price, terms}; free-text channel capped at 0 tokens for offer content, offers outside schema rejected by the environment); **P2** = P1 + verifiable commitment/escrow (accepted offers auto-execute from environment-held balances; reneging is mechanically impossible, decommitment only via a priced penalty clause à la leveled commitment); **P3** = P2 + fact audit (any factual assertion about external state must be attached as a typed claim checked against the scenario fact table; unverifiable claims stripped before delivery to the counterpart). Instrument: the wrapper code itself, which logs every rejected/stripped message. |
| M3 | LLM negotiator harness | Bilateral alternating-message negotiation, max 12 turns, fixed decoding (temperature 0.7, pinned model versions, seeded scenario order). Attacker agent receives the category's manipulation instruction plus an explicit payoff bonus for succeeding; defender is a naive negotiator prompt. Attacker comes in two forms per cell: *prompted* (free strategy) and *scripted* (templated manipulation moves inserted at fixed turns) to control attacker-competence confounds (C4). n = 30 (pilot) / 100 (scale-up) trials per cell. |
| M4 | Ground-truth success scorer | Rule-based, transcript-independent scoring against M1's ground-truth files: **attack-execution check** (did the manipulation content actually enter the dialogue — e.g., a claimed valuation deviating >20% from the sampled private value, a fact-table-false assertion, a ledger-recorded commitment later broken); **success check** (deal concluded AND defender surplus < 25th percentile of the scenario's precomputed truthful-play surplus distribution AND attacker surplus above truthful-play median). Emits per-trial labels: {not-attempted, attempted-failed, succeeded}. |
| M5 | Ablation aggregator & decision rule | Per-cell manipulation success rate (MSR) with Wilson 95% CIs; pre-registered verdict rule: a category is **protocol-fixable** iff under some rung its MSR is ≤5% AND significantly below its P0 MSR (two-proportion test, Holm-corrected); **protocol-invariant** iff MSR under the strictest rung P3 remains ≥10% with the CI excluding the fixable threshold. Mixed-effects logistic regression (success ~ protocol × category + (1\|scenario) + (1\|model pair)) as the primary inferential model. |
| M6 | Model-layer defense arm | Two defender-side interventions run at P0 and P3: (i) defended prompt (explicit manipulation-awareness instructions + counterpart-claim skepticism policy); (ii) activation-probe monitor on the open-weights attacker (linear probe trained on contrastive honesty data, following the probe methodology of [StrategicDishonesty, OpenReview:IbDr8xgUMW] and [AmongUs, OpenReview:XP3v1THxsq]), flagging trials whose attacker activations indicate deceptive intent; flagged trials count as detected. Measures whether model-layer instruments reduce residual MSR where protocols cannot. |

### challenge_arguments [HYPOTHESIS]

1. `challenge_id`: C1. `argument_text`: "Building the taxonomy and scenario generator (M1)
   explicitly up front, with the decision rule (M5) applied per category, is what lets the
   study report category-level verdicts instead of one aggregate number — directly matching
   the seed's category-level decision rule." `mechanism_components`: `["M1", "M5"]`.
2. `challenge_id`: C2. `argument_text`: "The ladder (M2) deliberately separates structure
   (P1) from enforcement (P2) from content audit (P3), and the scorer (M4) checks hidden
   ground truth rather than message form — so a false valuation inside a well-formed field is
   still scored as manipulation, isolating format effects from truthfulness effects."
   `mechanism_components`: `["M2", "M4"]`.
3. `challenge_id`: C3. `argument_text`: "P2/P3 enforcement is environment-side and
   mechanical (escrow auto-execution, fact-table lookup), not LLM-mediated, which removes the
   closed-loop bootstrapping problem for machine-checkable claims; the argument is explicitly
   partial — claims outside the fact table (intentions, tastes, counterfactuals) remain
   unverifiable by construction, which is precisely the residue the study is designed to
   measure." `mechanism_components`: `["M2"]`.
4. `challenge_id`: C4. `argument_text`: "Running both prompted and scripted attackers (M3)
   and separating attack-execution from attack-success labels (M4) lets the analysis
   distinguish 'protocol blocked the attack' from 'attacker failed to mount the attack in the
   new format'; the mixed-effects aggregation (M5) then isolates the protocol main effect
   from scenario and model-pair variance." `mechanism_components`: `["M3", "M4", "M5"]`.
5. `challenge_id`: C5. `argument_text`: "Defining success against sampled hidden parameters
   and precomputed truthful-play surplus distributions (M1, M4) replaces subjective
   'was this deceptive' judgment with a machine-checkable criterion; the Stage-1 human audit
   (κ ≥ 0.7 gate) is the explicit construct-validity check on that criterion before any
   scale-up conclusions are drawn." `mechanism_components`: `["M1", "M4"]`.

### unaddressed_challenges [HYPOTHESIS]

`["C3"]` — only partially addressed: environment-side enforcement covers machine-checkable
claims, but verification of claims outside the fact table (stated intentions, subjective
valuations) is inherently open, and the study measures rather than solves this residue. C5 is
addressed by construction but its validity rests on the κ-gated human audit, carried as a
threat in N10.

### feasibility [HYPOTHESIS]

- **Compute/effort order of magnitude.** Pilot: 5 categories × 4 rungs × 2 attacker modes ×
  30 trials ≈ 1,200 cells-worth of negotiations per model pair × 2 pairs ≈ **~3,600
  negotiations ≈ 90k LLM messages**; at ~1.5k tokens/message this is ~10⁸ tokens ≈
  **mid-hundreds of USD API cost class**; scale-up (~24k negotiations, 4 model families) is
  **low-thousands USD**. Probe training/inference needs one open-weights model on **1×A100
  (or equivalent) for days, not weeks**; no model training. Human validation audit: 200
  transcripts × 2 annotators × ~6 min ≈ **~40 annotator-hours**. Total wall-clock: pilot ~2–3
  weeks including harness engineering; scale-up ~4–6 weeks.
- **Single biggest feasibility risk + mitigation.** Risk: **frontier attacker models refuse to
  attempt manipulation** (safety training suppresses the manipulation instruction), leaving
  cells with near-zero attack-execution rates that are uninterpretable as protocol effects.
  Mitigation: the scripted-attacker mode in M3 guarantees a floor of executed attacks in
  every cell (attack execution is verified by M4's execution check before success is even
  scored), and the open-weights family provides an attacker that can be system-prompted
  without refusal; refusal rates themselves are logged and reported as a secondary outcome.

---

## N7 Contributions

| id | text | contribution_type | is_testable | has_rq |
|---|---|---|---|---|
| CO1 | [HYPOTHESIS] "A manipulation-category × protocol-constraint ablation matrix/taxonomy for LLM agent-to-agent negotiation, empirically populated rather than assumed, with pre-registered per-category verdicts." | technical_artifact | true | true |
| CO2 | [HYPOTHESIS] "An empirical classification of which negotiation-manipulation categories are eliminated by protocol-layer mechanism design alone, and which persist under every tested protocol." | empirical_finding | true | true |
| CO3 | [HYPOTHESIS] "A direct empirical adjudication of the seed's meta-question: whether protocol-vs-model-layer negotiation defense is properly an engineering problem or retains an irreplaceable modeling-research component — including whether model-layer defenses recover ground on protocol-invariant categories." | empirical_finding | true | true |
| CO4 | [HYPOTHESIS] "A reusable scenario suite (ground-truth-instrumented negotiation scenarios adapted from existing negotiation corpora) plus protocol-wrapper harness, released as a testbed for future negotiation-manipulation studies." | dataset | false | false |

---

## N8 Research Questions

- **RQ1** [GIVEN] (near-verbatim restatement of the seed's 核心问题): "Which categories of
  negotiation manipulation can structured, verifiable protocol-layer mechanism design (e.g.,
  structured offer/bid formats, verifiable commitment schemes) eliminate, and which
  categories survive under any protocol and can only be addressed by model-layer defenses?"
  `rq_source`: `explicit`. `evaluates_mechanisms`: `["M1","M2","M3","M4","M5"]`.
  `addresses_challenges`: `["C1","C2","C3","C4","C5"]`. `tests_contributions`: `["CO1","CO2"]`.
  `answered_by_experiment`: "the full manipulation-category × protocol-rung ablation matrix (Stage 1 pilot, then Stage 2 scale-up) with the M5 pre-registered verdict rule."
- **RQ_INF_1** [HYPOTHESIS] (inferred — the seed's decision rule phrased as a question):
  "Does the ablation matrix's pattern of results support classifying protocol-vs-model
  negotiation defense as belonging to engineering (if manipulation is fully protocol-fixable)
  or as retaining a distinct, irreplaceable model-layer research space (if any category is
  protocol-invariant)?" `rq_source`: `inferred`. `evaluates_mechanisms`: `["M5"]`.
  `addresses_challenges`: `["C1","C4"]`. `tests_contributions`: `["CO3"]`.
  `answered_by_experiment`: "the aggregate pattern across the per-category verdicts of RQ1's matrix."
- **RQ_INF_2** [HYPOTHESIS] (inferred — required to make 'only model-layer can fix it' more
  than an argument from absence): "For categories that remain protocol-invariant under the
  strictest tested protocol, do model-layer defenses — defended prompts and activation-probe
  monitors — significantly reduce residual manipulation success, and do they do so without
  destroying legitimate agreement rates?" `rq_source`: `inferred`.
  `evaluates_mechanisms`: `["M6","M3","M4"]`. `addresses_challenges`: `["C2","C5"]`.
  `tests_contributions`: `["CO3","CO2"]`.
  `answered_by_experiment`: "the M6 defense arm at rungs P0 and P3, compared per invariant category against the undefended P3 cells."

### Evaluation design [HYPOTHESIS]

- **datasets**: `names: ["CraigslistBargain (He et al. 2018) — buyer/seller price-negotiation dialogues; source of realistic item/price scenario parameters for categories (a),(b)", "Deal or No Deal (Lewis et al. 2017) — multi-issue division negotiation with private point values; direct template for hidden-valuation scenarios", "CaSiNo (Chawla et al. 2021) — campsite multi-issue negotiations annotated with persuasion/rapport strategies; source for category (c) emotional/rapport manipulation templates", "SOTOPIA scenario schema [SOTOPIA, OpenReview:mM7VurbA4r] — procedural mixed-motive scenario generation format, reused for scenario instantiation", "Contrastive honesty probe-training data following [AmongUs, OpenReview:XP3v1THxsq] — for the M6 activation probes"]`.
  Note: the ground-truth-instrumented scenario suite itself is new (CO4); the named corpora
  supply realistic negotiation structure and manipulation-strategy templates so scenarios are
  not invented from whole cloth.
- **baselines**: `names: ["P0 unstructured free-text protocol (primary control; every protocol rung is compared against it)", "SOTOPIA-EVAL-style LLM-judge scoring of the same transcripts [SOTOPIA, OpenReview:mM7VurbA4r] — baseline scorer to quantify what objective ground-truth scoring adds (C5)", "Defended-prompt defender with no protocol constraint (model-layer-only arm, M6-i at P0)", "Activation-probe monitor à la [StrategicDishonesty, OpenReview:IbDr8xgUMW] / [AmongUs, OpenReview:XP3v1THxsq] (model-layer-only arm, M6-ii at P0)", "Scripted-truthful-agent play (defines the truthful-play surplus distribution each cell is scored against)"]`.
- **metrics**: `names: ["Manipulation Success Rate (MSR): fraction of trials labeled 'succeeded' by M4 — deal concluded AND defender surplus < 25th percentile of truthful-play distribution AND attacker surplus > truthful-play median", "Attack Execution Rate (AER): fraction of trials where M4's execution check confirms the manipulation entered the dialogue — denominator hygiene for C4", "Defender Surplus Loss (DSL): (median truthful-play defender surplus − observed defender surplus) / truthful-play surplus range, per trial", "Reneging Rate: ledger-recorded commitments later broken, per trial (category (d) primary metric)", "Detection/Refusal Rate: fraction of trials where the M6 defense flags the attacker or the defender exits (model-layer arm metric)", "Agreement Rate: fraction of trials ending in any deal — guards against protocols 'fixing' manipulation by destroying trade"]`.
- **analysis plan** [HYPOTHESIS]: "Sample size: 30 trials/cell (pilot), 100 trials/cell
  (scale-up); at n=100 a drop from 30% to 10% MSR is detectable with >80% power even at the
  Holm-corrected α. Tests: per category, two-proportion z-tests (Fisher's exact where cells
  are sparse) of each rung vs. P0 and of P3 vs. the 5% fixability threshold, Holm–Bonferroni
  across the 5 categories × 3 rung contrasts (15 tests), family-wise α = 0.05; primary
  inferential model is the M5 mixed-effects logistic regression with scenario and model-pair
  random intercepts. Expected effect direction: reneging (d) collapses under P2+ (MSR → ≈0,
  mechanically enforced); fabricated-fact manipulation (b) collapses under P3 (fact audit);
  misrepresented valuation (a) and emotional coercion (c) persist under P3 (MSR ≥ 10% with CI
  excluding 5%); collusive signaling (e) is uncertain — schema constraints may or may not
  close covert channels. RQ_INF_2 direction: probe monitor reduces residual MSR on (a)/(c) at
  P3 by a detectable margin while agreement rate stays within 10 points of undefended P3."

---

## N9 Results — PLACEHOLDER, HYPOTHESIZED DIRECTION ONLY

No experiment has been run. Every item states a predicted direction as a falsifiable claim,
never a real number. `evidence_strength="missing"` and `rq_answered=false` throughout, per
the reverse-digest rule. This node is where the seed's framing is most load-bearing: the seed
states the experiment "直接裁决方向本身的存在权" (directly adjudicates the research direction's
own right to exist) — the falsification conditions below are the entire point of the study.

1. **rq_id**: RQ1. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "Predicted direction:
   reneging-type manipulation (category d) is driven to near-zero MSR by any rung ≥ P2
   (mechanical escrow), and fabricated-external-fact manipulation (b) by P3 (fact audit),
   while misrepresented private valuation (a) and emotional/rapport coercion (c) retain
   MSR ≥ 10% under P3 — because private values and affect are outside any fact table and thus
   structurally unauditable (C2, C3 residue)." **result_type**: `quantitative` (predicted
   shape only). **evidence_strength**: `missing`. **rq_answered**: `false`.
   **Falsification condition** [HYPOTHESIS]: refuted if MSR for *every* category, including
   (a) and (c), falls to ≤5% and significantly below P0 under P3 (per the M5 verdict rule) —
   i.e., "protocol can fix everything" holds on the tested ladder.
2. **rq_id**: RQ_INF_1. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "Predicted direction:
   because RQ1 is expected to surface at least one protocol-invariant category, the study
   would conclude that model-layer negotiation defense retains a non-substitutable role
   alongside protocol-layer mechanism design — the B5.3 boundary is real and sits in the
   middle: protocols own enforcement-shaped attacks (commitments, checkable facts), the model
   layer owns content-truthfulness and affect-shaped attacks." **result_type**: `qualitative`.
   **evidence_strength**: `missing`. **rq_answered**: `false`.
   **Falsification condition** [HYPOTHESIS]: refuted if zero categories remain
   protocol-invariant across the tested ladder — the correct conclusion then flips to "the
   sub-field folds into protocol/mechanism-design engineering," exactly the alternative
   branch the seed names.
3. **rq_id**: RQ_INF_2. **result_text** [PLACEHOLDER — HYPOTHESIZED]: "Predicted direction:
   on protocol-invariant categories, the activation-probe monitor reduces residual MSR by a
   statistically detectable margin at P3 (consistent with probes detecting strategic
   deception that fools output-level checks, per the mechanism in [StrategicDishonesty,
   OpenReview:IbDr8xgUMW]), while the defended prompt yields a smaller, less reliable
   reduction; agreement rate stays within 10 points of undefended P3."
   **result_type**: `quantitative` (predicted shape only). **evidence_strength**: `missing`.
   **rq_answered**: `false`.
   **Falsification condition** [HYPOTHESIS]: refuted if neither model-layer defense
   significantly reduces residual MSR on any protocol-invariant category (model layer adds
   nothing → the 'irreplaceable model-side space' claim loses its constructive half and rests
   only on protocol failure), or if defenses only reduce MSR by collapsing agreement rate
   (defense-by-not-trading).

---

## N10 Threats / Self-Limitations

All items [HYPOTHESIS] — anticipated by the digest author, not author-acknowledged (no paper
exists). Categories follow the schema enum.

- **t1**. `category`: `construct`. `description`: "The hidden-ground-truth success criterion
  (M4) operationalizes 'manipulation succeeded' as a surplus-quantile condition; this may
  both miss harms that don't move surplus (e.g., extracted information, reputational setup
  for future rounds) and mislabel aggressive-but-honest bargaining as manipulation in skewed
  scenarios." `mitigation` [HYPOTHESIS]: "Stage-1 human validation audit: 200 transcripts,
  2 annotators, proceed to scale-up only if machine labels reach Cohen's κ ≥ 0.7 against
  human judgment; disagreement cases published with the artifact."
- **t2**. `category`: `internal`. `description`: "Protocol rungs change the attacker's task
  difficulty as well as the defense surface (C4): a drop in success under P1 may reflect the
  prompted attacker's inability to express its strategy in JSON rather than a closed channel;
  refusal behavior of safety-trained attacker models is a further confound." `mitigation`
  [HYPOTHESIS]: "Scripted-attacker mode guarantees executed attacks in every cell; the
  Attack Execution Rate metric separates 'not attempted' from 'attempted and blocked';
  refusal rates logged and reported per cell."
- **t3**. `category`: `external`. `description`: "A 'protocol-invariant' verdict is relative
  to the four-rung ladder and the specific model families tested; an untested protocol could
  close a category labeled invariant, and stronger future models could defeat rungs that held
  here. Scenario realism is bounded by the three source corpora (price/multi-issue/campsite
  negotiations)." `mitigation` [HYPOTHESIS]: "Verdicts are reported as 'invariant under the
  tested ladder' with the ladder published as extensible harness code (CO4); cross-model
  replication across ≥4 families in Stage 2; scenario templates drawn from three distinct
  real negotiation corpora rather than one."
- **t4**. `category`: `conclusion`. `description`: "The matrix involves ≥40 cells and 15+
  primary hypothesis tests over stochastic LLM outputs; naive per-cell testing would inflate
  false-positive 'category closed/open' verdicts." `mitigation` [HYPOTHESIS]:
  "Pre-registered verdict thresholds (5%/10% MSR), Holm–Bonferroni correction across the
  primary contrast family, mixed-effects model as the primary inference, Wilson CIs reported
  for every cell."
- **t5**. `category`: `reproducibility`. `description`: "LLM output stochasticity and
  provider-side model drift mean exact MSR numbers may not replicate across model updates."
  `mitigation` [HYPOTHESIS]: "Pinned model versions and seeds recorded per trial; one fully
  open-weights model family included so at least one column of the matrix is exactly
  re-runnable."
- **Status**: NOT_FOUND (no paper, hence no author-stated Threats section — all five items
  are anticipated, with anticipated mitigations, not author self-reports).
  - `absence_comment` [PLACEHOLDER]: `{"what_missing": "There is no Limitations/Threats-to-Validity section because no paper has been written.", "why_matters": "N10 is defined as author-acknowledged limitations only; anything listed here is a prediction of what a careful author would acknowledge.", "implication": "Re-run this node once a real draft exists and replace these items with whatever the actual authors state."}`

---

## N11 Artifacts

- **artifacts**: `[]`
- **has_code**: `false`
- **has_data**: `false`
- **has_model**: `false`
- **Status**: NOT_FOUND [PLACEHOLDER] — nothing has been built or released; the paper itself
  does not exist.
  - `absence_comment` [PLACEHOLDER]: `{"what_missing": "No code repository, scenario dataset, or model checkpoint exists because no experiment has been run yet.", "why_matters": "A reader relying on this digest to plan reproduction work needs to know there is currently nothing to reproduce.", "implication": "Treat CO4 (the scenario-suite + harness artifact) as a planned deliverable, not an available one, until this node is re-populated from a real release."}`

---

## N12 Contribution Type

- **value**: `empirical` [HYPOTHESIS]
- **rationale** [HYPOTHESIS]: "What N9 would validate is a controlled measurement/ablation
  study — per-category × per-protocol manipulation-success rates under a pre-registered
  statistical decision rule, plus a defense-arm comparison — with the scenario suite and
  wrapper harness (CO4) released as instruments in service of that study, not as the headline
  contribution. This mirrors the classification logic of comparable digests: the debate-
  protocol paper (protocol + large controlled evaluation) is `empirical` because its central
  deliverable is the measured effect of the protocol, whereas DecodingTrust is `benchmark`
  because its central deliverable is the reusable suite. Here the seed's own framing ('实验
  直接裁决方向本身的存在权') makes the measured verdict, not the testbed, the paper's central
  move — hence `empirical`, not `benchmark`. If, at writing time, the scenario suite were
  promoted to the primary contribution with multi-model leaderboard framing, `benchmark`
  would become defensible; that hinges on a framing decision not yet made."
- **source**: HYPOTHESIS

---

## Claims

1. [HYPOTHESIS] "Manipulation categories in LLM agent-to-agent negotiation do not form a
   monolithic class with respect to protocol-layer defenses: some categories are structurally
   eliminable by mechanism design while others are not." `evidence`: `[{"type":"argument","text":"Derived from N5's C1/C2 heterogeneity argument: enforcement-shaped attacks (reneging, checkable facts) live where protocols have leverage; content/affect-shaped attacks (private-value misreports, emotional coercion) do not.","source":"HYPOTHESIS","location":null}]`
2. [HYPOTHESIS] "Incentive-compatibility guarantees from mechanism design do not transfer
   from formal action spaces to natural-language negotiation, because the mechanism's
   guarantee covers only actions it can see — the gap this study measures is exactly the set
   of strategic actions outside the mechanism's action space." `evidence`: `[{"type":"citation","text":"Contrast between DSIC-by-construction over formal bids ([AMenuNet, OpenReview:cNb5hkTfGC]) and strategic deception operating through free-form language that fools output-level checks ([StrategicDishonesty, OpenReview:IbDr8xgUMW]).","source":"HYPOTHESIS","location":null}]`
3. [GIVEN] "The existence of 'model-layer negotiation defense' as a distinct research program
   is staked on the empirical outcome of the ablation matrix — the seed frames the experiment
   as adjudicating the research direction's own right to exist." `evidence`: `[{"type":"citation","text":"the seed's minimal-experiment sentence: 若协议能修一切,该方向应归工程;若不成立,模型侧研究有不可替代空间","source":"GIVEN","location":{"page":null,"section_title":"seed README, 最小实验","quote":"实验直接裁决方向本身的存在权"}}]`
4. [HYPOTHESIS] "Verifiable-commitment protocols are predicted to nearly eliminate
   reneging-type manipulation while leaving valuation misreports and emotional coercion
   largely untouched, because commitment enforcement and content truthfulness are logically
   independent axes (N5-C2, N5-C3)." `evidence`: `[{"type":"argument","text":"Derived from the M2/M4 challenge_arguments in N6: P2's escrow is mechanical and closes the time channel; no rung can audit claims about private state.","source":"HYPOTHESIS","location":null}]`
5. [HYPOTHESIS] "If any category is protocol-invariant, model-layer instruments are the only
   remaining defense locus, and activation-probe monitoring is the most promising candidate
   because probes have detected strategic deception that defeats output-level judges."
   `evidence`: `[{"type":"citation","text":"Probe results in [StrategicDishonesty, OpenReview:IbDr8xgUMW] and [AmongUs, OpenReview:XP3v1THxsq]; tested here as RQ_INF_2 / M6 rather than assumed.","source":"HYPOTHESIS","location":null}]`
6. [PLACEHOLDER] "No manipulation-success percentages, effect sizes, or statistical tests
   currently exist for any (category × protocol) cell; any specific number reported here
   would be fabricated." `evidence`: `[]`

---

## Self-verification pass

- **V-01 locator integrity**: no item is tagged `source="extracted"` from a real PDF (none
  exists); every GIVEN item anchors to the seed README; every [GROUNDED:corpus] N3 entry
  anchors to a real `ideas.jsonl` record via its OpenReview paper_id and paper_url.
- **V-02 absence comments**: every non-FOUND node (N0, N1, N2, N3, N10, N11) carries a full
  3-part `absence_comment`.
- **V-04 / EX-09 ID consistency**: checked —
  `N4.affects_works` ⊆ N3 citation_keys, verbatim: `[AMenuNet, OpenReview:cNb5hkTfGC]`,
  `[UCB-S, OpenReview:lsxeNvYqCj]`, `[Rosenschein & Zlotkin, 1994]`,
  `[StrategicPersuasion, OpenReview:aTCXvJKnkE]`, `[StrategicDishonesty, OpenReview:IbDr8xgUMW]`,
  `[AmongUs, OpenReview:XP3v1THxsq]`, `[HonestyBestPolicy, OpenReview:EmxpDiPgRu]`,
  `[SOTOPIA, OpenReview:mM7VurbA4r]`, `[ThreatSnapshots, OpenReview:kga18ld70t]` — all nine
  appear as N3 keys; `N6.challenge_arguments[].challenge_id` ∈ {C1..C5};
  `mechanism_components` ⊆ {M1..M6}; `N6.unaddressed_challenges = ["C3"]` ⊆ {C1..C5};
  N8 `addresses_challenges` ⊆ {C1..C5}, `tests_contributions` ⊆ {CO1..CO4},
  `evaluates_mechanisms` ⊆ {M1..M6}; `N9.results[].rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2} = N8
  ids. No dangling ids.
- **V-08 confidence discipline**: N9 predictions rest on `source="HYPOTHESIS"` N5/N6 items
  and say so; every prediction carries an explicit falsification condition.
- **V-10/V-11**: N10 and N11 show `status != FOUND` with non-empty `absence_comment`; N11's
  three flags are `false`, matching the empty artifact list.
- **V-12**: N12 rationale cites concrete design facts (what N9's matrix validates, CO4's
  instrument role) and contrasts against two real classification exemplars, not a circular
  restatement.
- **EX-11 empty-node check**: all of N0–N12 plus Claims present; none omitted.
