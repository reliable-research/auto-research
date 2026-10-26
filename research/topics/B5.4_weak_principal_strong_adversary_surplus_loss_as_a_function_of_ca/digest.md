# Digest: Weak Principal, Strong Adversary: Surplus Loss as a Function of Capability Gap

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING (v2, corpus-grounded).** No paper exists
> for this topic yet. This document projects a full N0–N12 digest *as if* a paper answering
> the seed's core question had been written, so that the eventual paper can be planned
> against it. Every field is tagged **[GIVEN]** (verbatim/near-verbatim from the seed
> README), **[HYPOTHESIS]** (reasoned elaboration / prediction, not fact),
> **[GROUNDED:corpus]** (a real paper retrieved from the local OpenReview corpus
> `topics/corpus/ideas.jsonl`, summarized from its own motivation/method text), or
> **[PLACEHOLDER]** (genuinely unknowable until the work exists — never invented). Treat
> all forward-looking numbers and results as forecasts, not findings.
>
> Seed: `topics/B5.4_weak_principal_strong_adversary_surplus_loss_as_a_function_of_ca/README.md`
> Code **B5.4**, label **[证据+矛盾]** [GIVEN], parent topic **B5. 议价机制层（agent-to-agent 交易）** [GIVEN].
> Specificity calibrated against best-paper digest exemplars
> `samples/best_papers_recent3_digest/ICML_2024_Debating_Persuasive_LLMs_Truthful_Answers.md`
> and `.../ICLR_2026_LLMs_Get_Lost_Multi_Turn_Conversation.md` (controlled behavioral /
> game-theoretic LLM experiments with capability scaling).

---

## N0 Metadata

- **title** [GIVEN]: "Weak Principal, Strong Adversary: Surplus Loss as a Function of Capability Gap" — verbatim from seed README line 16 (English gloss of 能力差距下的代理剥削).
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper exists; authors cannot be known.
- **abstract** [HYPOTHESIS] (drafted, not a real abstract — synthesized from the core question + minimal experiment for planning only):
  > "When an LLM negotiates on behalf of a human principal, it may face a stronger-model
  > adversary representing the counterparty. We measure how much bargaining surplus the
  > weak principal's agent systematically loses as the capability gap to its adversary
  > widens, and whether constraining the weak agent's action space to schema-validated
  > structured offers (no free text) protects it relative to leaving it unconstrained.
  > We run a two-factor experiment — capability gradient × action-space constraint — over
  > multi-issue alternating-offers bargaining games with closed-form Pareto frontiers and
  > a Nash-bargaining reference split, across two established negotiation game families
  > (GLEE-style bargaining configurations and Deal-or-No-Deal multi-issue division). We
  > report normalized surplus loss as a function of a dual capability-gap measure
  > (exogenous general-capability score delta; endogenous negotiation Elo estimated from
  > round-robin play), and test the counter-intuitive 'constraint-as-protection'
  > hypothesis that restricting the weak agent's expressiveness reduces its losses."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` — an empirical evaluation of LLM agents in adversarial multi-agent interaction; the game-theoretic bargaining framing is instrumental to the metric, not the paper's home field.
- **status**: PARTIAL — title/core question given; authors/abstract/doi/pages are placeholders or drafted.
- **absence_comment**: `{"what_missing": "No authors, DOI, arXiv id, or page count exist because the paper has not been written.", "why_matters": "Bibliographic identity is what lets this digest later be reconciled with the real paper.", "implication": "Treat N0 as a placeholder shell to be overwritten wholesale once a draft exists — do not carry the drafted abstract forward as if extracted."}`

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS], full predicate: "measure how normalized surplus loss for a
  weak-capability LLM agent negotiating on behalf of a human principal scales with the
  capability gap to a strong-model adversary agent in bilateral multi-issue bargaining with
  a computable reference split, and test whether constraining the weak agent's action space
  to schema-structured offers (vs. unrestricted free-form messages) reduces that surplus
  loss." Self-check: (1) kind of task = controlled factorial bargaining experiment /
  measurement study; (2) domain = LLM agents negotiating under capability asymmetry
  (agent-to-agent bargaining layer); (3) outcome shape = a surplus-loss-vs-capability-gap
  scaling curve per action-space condition, plus a constrained-vs-unconstrained deployment
  recommendation. Grounded in seed core question (README line 18).
- **inputs** [HYPOTHESIS]:
  - A capability ladder of LLMs (weak → strong tiers), each playing the "weak principal's
    agent" role against fixed strong-adversary models, with capability gap quantified both
    exogenously (general-capability score delta) and endogenously (negotiation Elo from
    round-robin play).
  - Bilateral bargaining game specifications: private valuations, reservation values, a
    closed-form Pareto frontier, and a computable reference (Nash-bargaining) split.
  - An action-space condition assigned to the weak agent: `structured-offer-only`
    (schema-validated JSON offer object, no free text) vs. `free-text` (offer + up to
    150 words of unrestricted natural-language message per turn).
- **outputs** [HYPOTHESIS]:
  - Per-episode realized surplus split, normalized surplus loss vs. the reference split,
    agreement/impasse outcomes, and full offer/message transcripts.
  - A surplus-loss-vs-capability-gap scaling estimate (regression slope + CI) per
    action-space condition.
  - A directional verdict, with statistical test, on whether the structured-offer
    constraint lowers or raises surplus loss at each capability-gap level.
- **constraints** [GIVEN]: the experiment requires a known ground-truth "fair"/efficient
  split against which realized outcomes are scored — implied by the seed's framing of
  "surplus loss" (剩余损失) as measured relative to a reference point, and by the seed's
  explicit two-factor design ("能力梯度 × 行动空间约束的双因素实验", README line 19).
- **status**: PARTIAL (objective/inputs/outputs inferred; constraints directly given).
- **absence_comment**: `{"what_missing": "The seed states only a core question and a one-sentence minimal experiment, not a full input/output/constraint formulation.", "why_matters": "Without a concretely specified game and capability metric the objective is a reasonable but unverified reconstruction.", "implication": "Treat inputs/outputs as a design proposal to be validated when the actual experiment is specified."}`

---

## N2 Motivation

**Node field:** `motivations`

- **[HYPOTHESIS]** motivation_text: "As LLM agents increasingly negotiate and transact on
  behalf of users in agent-to-agent commerce (parent topic B5, the bargaining-mechanism
  layer), a principal who deploys a weaker or cheaper model may face a counterparty running
  a stronger one. Adjacent oversight literature already shows that weak-vs-strong adversarial
  interactions have systematic, capability-dependent failure rates ([ScalingLawsOversight,
  OpenReview:u1j6RqH8nM] fits scaling laws for weak-Guard-vs-strong-Houdini games), but no
  one has measured the *economic* analogue: surplus loss in bargaining as a function of the
  gap." evidence: `[]` (no paper text exists; the corpus citation grounds the adjacent
  claim, not this paper's own motivation).
- **[HYPOTHESIS]** motivation_text: "If a deliberately constrained (structured-offer) weak
  agent protects the principal better than an unconstrained one, that is a directly
  actionable, near-zero-cost deployment mitigation — echoing the seed's own framing
  ('若成立，是可直接落地的部署建议', README line 19) — and it would parallel the AI-control
  finding that protocol-level restrictions, not capability parity, are what make weak-vs-
  strong deployments safe ([AIControl, OpenReview:KviM5k8pcP])." evidence: `[]`.
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "No motivating statistics or deployment incidents exist; motivation is reconstructed from the parent-topic label plus adjacent corpus literature.", "why_matters": "Motivation grounded in a one-line topic tag plus analogy is weaker than a paper's own cited introduction.", "implication": "Replace with the paper's own introduction once written."}`

---

## N3 Related Works

**Node field:** `works`. **Method:** local corpus retrieval over
`topics/corpus/ideas.jsonl` (11,683 OpenReview papers), 7 keyword-angle queries
(negotiation/bargaining; capability gap/weak-to-strong/scalable oversight;
persuasion/deception; game-theoretic multi-agent LLM; debate/judge; AI control/untrusted
models; economic/market agents). All `[GROUNDED:corpus]` entries are real papers whose
`approach_summary` is grounded in their own motivation/method text; their *fit* to this
future paper is my judgment. Two non-corpus entries are retained only because they are
canonical for the exact task domain and are cited by corpus papers themselves. **Update
(Phase A re-run, Task 1 reference-cache upgrade, 2026-07-04):** a 150-candidate arXiv +
ACL-anthology harvest was independently digested and triaged into
`discussion/reference_candidates.jsonl`'s canonical schema; it surfaced one additional
real method-twin the corpus-only retrieval above missed, added below as an 11th N3 entry
(`[LanguageOfBargaining, ACL:2023.acl-long.735]`), with a matching N4 limitation. All ten
of this section's original corpus/canonical works have also now been back-filled into
`reference_candidates.jsonl` as `selected` records (see that file for `key`/`relevance`),
closing the reference-cache-integrity gap flagged at this Phase A pass (goal.md §3 item 2)
— see `discussion/stage_review.md`.

- **[ScalingLawsOversight, OpenReview:u1j6RqH8nM]** [GROUNDED:corpus] —
  approach_summary: "Models scalable oversight as two-player adversarial games between
  mismatched agents (a 'Houdini' evading vs. a 'Guard' overseeing), computes pairwise
  win-rate matrices, assigns role-specific Elo scores, and fits a low-parameter (Double
  ReLU) scaling law linking general intelligence to domain Elo, then optimizes nested
  oversight schemes with it." paper_url: https://openreview.net/forum?id=u1j6RqH8nM.
  Relevance: the closest methodological template — capability-gap-vs-outcome scaling in
  weak-vs-strong adversarial games — but its outcome is oversight win probability, not
  bargaining surplus.
- **[WeakToStrong, OpenReview:ghNRg2mEgN]** [GROUNDED:corpus] — approach_summary:
  "Constructs a controlled weak-supervisor/strong-student hierarchy by finetuning large
  pretrained models on labels generated by small ones, and introduces the Performance Gap
  Recovered (PGR) metric to quantify how much of the weak-to-strong capability gap is
  recovered." paper_url: https://openreview.net/forum?id=ghNRg2mEgN. Relevance: canonical
  formalization of a manipulated capability gap as an experimental variable, in a training
  (not adversarial-bargaining) setting.
- **[AIControl, OpenReview:KviM5k8pcP]** [GROUNDED:corpus] — approach_summary: "Evaluates
  safety protocols under the assumption that the most capable model is malicious: replaces
  the untrusted strong model with an explicit adaptive attack policy and measures whether
  weak-trusted-model oversight protocols (trusted monitoring, deferral) prevent any
  catastrophic failure across long task sequences." paper_url:
  https://openreview.net/forum?id=KviM5k8pcP. Relevance: establishes that protocol-level
  restrictions can protect a weak party against a strong adversary — the safety-domain
  analogue of the seed's 'constraint-as-protection' hypothesis.
- **[ControlTax, OpenReview:BpyR6Wkl1c]** [GROUNDED:corpus] — approach_summary: "Embeds
  empirically measured ROC curves of weak monitor models into a game-theoretic
  attacker–defender model of AI control, solving for compromise probability under optimal
  strategies and converting the protective protocol's overhead into a monetary 'control
  tax'." paper_url: https://openreview.net/forum?id=BpyR6Wkl1c. Relevance: quantifies the
  *cost side* of protecting a weak principal with restrictions; this topic instead
  quantifies the *surplus side* in bargaining.
- **[StrategicPersuasion, OpenReview:aTCXvJKnkE]** [GROUNDED:corpus] — approach_summary:
  "Instantiates Bayesian persuasion in natural language: converts debate/persuasion
  datasets into sender–receiver games with explicit states, priors, actions, and utilities,
  where an LLM Sender communicates strategically and is scored by the action change induced
  in a fixed LLM Receiver." paper_url: https://openreview.net/forum?id=aTCXvJKnkE.
  Relevance: operationalizes the free-text rhetorical/persuasive channel through which a
  strong adversary could extract surplus — the channel the structured-offer constraint
  removes.
- **[GreatModelsThinkAlike, OpenReview:3Z827FtMNe]** [GROUNDED:corpus] —
  approach_summary: "Proposes CAPA, a chance-adjusted probabilistic agreement metric over
  model mistakes, and uses it to show that LLM-as-judge scores are inflated by
  judge–model functional similarity and that weak-to-strong gains vary with supervisor–
  student similarity." paper_url: https://openreview.net/forum?id=3Z827FtMNe. Relevance:
  warns that 'capability gap' is confounded by model *similarity* — directly informing this
  topic's C1 (gap is not a clean scalar) and the model-pair sampling design.
- **[CompeteAI, OpenReview:wGtzp4ZT1n]** [GROUNDED:corpus] — approach_summary: "A framework
  and persistent simulation environment for competition dynamics among LLM agents:
  resource-constrained markets with competitor/judge roles, memory-planning agent loops,
  and repeated feedback, from which strategy adaptation and winner-take-all dynamics emerge."
  paper_url: https://openreview.net/forum?id=wGtzp4ZT1n. Relevance: closest corpus precedent
  for adversarial economic interaction between LLM agents, but with emergent, uncontrolled
  capability differences and no surplus reference point.
- **[ARIA, OpenReview:eumRwpgdMU]** [GROUNDED:corpus] — approach_summary: "Trains language
  agents in open-ended strategic environments (explicitly including negotiation and
  bargaining) by projecting free-form language actions into a low-dimensional intention
  space via embedding clustering and aggregating rewards within intention clusters, to
  combat the exponential free-form action space and sparse rewards." paper_url:
  https://openreview.net/forum?id=eumRwpgdMU. Relevance: independent evidence that the
  free-form action space is the problematic object in language-based negotiation — but
  treats it as a *training* problem, not a deployment-time exploitation surface.
- **[GLEE, arXiv:2410.05254]** [HYPOTHESIS — NON-CORPUS, canonical; cited as
  @shapira2024glee by [ARIA, OpenReview:eumRwpgdMU]'s own motivation text] —
  approach_summary: "A unified framework and benchmark for language-based economic
  environments, standardizing bargaining, negotiation, and persuasion games for LLM agents
  with parameterized game configurations and payoff logging." paper_url:
  https://arxiv.org/abs/2410.05254. Relevance: the natural source of standardized
  bargaining game configurations for this topic's harness. Existence is corroborated
  inside the corpus; exact bibliographic details must be re-verified before citing.
- **[DealOrNoDeal, arXiv:1706.05125]** [HYPOTHESIS — NON-CORPUS, canonical (Lewis et al.,
  2017, "Deal or No Deal? End-to-End Learning of Negotiation Dialogues")] —
  approach_summary: "Introduces the multi-issue object-division negotiation task with
  private per-item valuations and a corpus of ~5.8k human–human negotiation dialogues,
  plus end-to-end and self-play trained negotiation models." paper_url:
  https://arxiv.org/abs/1706.05125. Relevance: canonical value-function design for
  multi-issue bargaining with computable efficient splits; its scenario generator is
  reusable as a second game family. Must be re-verified before citing.
- **[LanguageOfBargaining, ACL:2023.acl-long.735]** [GROUNDED:reference_cache — added at
  the Task-1 reference-cache upgrade pass, `discussion/reference_candidates.jsonl` key
  `LanguageOfBargaining2023`; not in the `topics/corpus/ideas.jsonl` OpenReview corpus used
  for the rest of N3, so it was missed by the original harvest angles] — approach_summary:
  "Heddaya, Dworkin, Tan, Voigt & Zentefis (ACL 2023). A controlled human-subjects bilateral
  bargaining experiment (house-price negotiation exercise) contrasting an alternating
  structured-numeric-offer condition (AO) against an unrestricted natural-language condition
  (NL), over 230 AO and 178 NL negotiations. Finds the average *agreed price* is statistically
  identical between conditions, but the NL condition reaches agreement faster, at a higher
  rate, and with substantially lower price variance; also contributes a negotiation
  speech-act taxonomy." paper_url: https://aclanthology.org/2023.acl-long.735/. **This is the
  closest real method-twin in the whole 150-candidate harvest**: its manipulated variable
  (structured offers vs. free text) is near-identical to this paper's own M3 action-space
  constraint. Relevance = method-twin, requiring concede-and-differentiate (guidance.md Part
  4 situation 6): *concede* — the core AO-vs-NL manipulation, and its empirical finding that
  the manipulation alone (absent any capability asymmetry) leaves the average agreed
  split unchanged while changing process metrics (speed, agreement rate, variance);
  *differentiate* — (i) symmetric-capability human dyads vs. this paper's capability-gap
  ladder of LLM agents; (ii) no reference-split/surplus-loss framing (raw agreed price only,
  no Pareto/Nash benchmark); (iii) no adversarial-exploitation question (both sides are
  ordinary bargainers, not a principal's weak agent vs. a strong adversary). Its finding is
  informative as a **rival prediction for B0**: if the structured/free-text manipulation
  alone does not move the split at zero capability gap (mirroring Heddaya et al.'s symmetric
  result), that sharpens H2a's own claim that any protective effect must appear as a
  condition×gap *interaction*, not a condition main effect at gap≈0.

**Status:** PARTIAL (works are real and grounded; the mapping to a not-yet-written paper's
related-work section is hypothesis). **absence_comment**: `{"what_missing": "No corpus paper studies LLM-vs-LLM bilateral bargaining with a manipulated capability gradient, and none tests action-space restriction of the weaker party as an anti-exploitation mechanism; the corpus also under-covers some negotiation-specific benchmarks (e.g., NegotiationArena-style arenas) that may exist outside it. The reference-cache upgrade pass (Task 1) also surfaced one genuine method-twin, [LanguageOfBargaining, ACL:2023.acl-long.735], that the original corpus-only harvest missed entirely.", "why_matters": "This is exactly the gap the seed targets — but the N3 list is a retrieval over one corpus, not an exhaustive prior-art search, and single-corpus retrieval systematically misses cross-community precedents (this one sat in the ACL Anthology corpus, not the OpenReview ML corpus).", "implication": "Before writing the real paper, verify the two non-corpus entries and re-run search over ACL/NeurIPS/ICLR indices for LLM negotiation benchmarks and exploitation studies."}`

**Freshness sweep (goal.md §1), resolved 2026-07-04:** a 2026 follow-up incidentally surfaced during
spot-checking, arXiv:2601.04387 ("The Language of Bargaining: Linguistic Effects in LLM
Negotiations"), was provisionally flagged above as possibly running "the same AO/NL-style
contrast on LLM agents directly" — that description was a search-summary guess, not a real
read, and turned out to be **wrong**. A full `paper-digest` extraction
(`arxiv_2601.04387.md`) confirms its manipulated variable is the **language/persona** used to
conduct free-text bargaining (English vs. Hindi/Gujarati/Punjabi/Marwadi), with protocol/format
held fixed throughout — a different independent variable from this paper's structured-offer-
vs-free-text manipulation and from `LanguageOfBargaining2023`'s AO-vs-NL contrast. Per
guidance.md Part 4 situation 6, a method-twin requires the *same* manipulated variable;
this does not qualify. **Resolution:** added to `reference_candidates.jsonl` as
`LangBargainIndic2601`, relevance `adjacent`, verdict `selected` — cited only as background
on format/language effects in LLM negotiation, no concede-and-differentiate repositioning
triggered, no `paper.md` change required.

---

## N4 Prior Limitations

**Node fields:** `limitations`, `grounding_check`

*(All items [HYPOTHESIS]: reasoned gaps defensible from each cited paper's own
motivation/method text as retrieved from the corpus — not limitations the papers state
about themselves.)*

- limitation_text: "The oversight-scaling line quantifies weak-vs-strong adversarial
  interaction only through win/loss outcomes of oversight games (Guard-vs-Houdini win-rate
  matrices) or supervision-label quality (PGR over finetuning), never through a continuous
  economic outcome such as bargaining surplus against a computable Pareto frontier — so it
  cannot say how many *units of value* a weak principal loses per unit of capability gap."
  affects_works: `["[ScalingLawsOversight, OpenReview:u1j6RqH8nM]", "[WeakToStrong, OpenReview:ghNRg2mEgN]"]`. limitation_type: `generalizability`.
- limitation_text: "Existing language-based economic environments and negotiation corpora
  evaluate whichever models are plugged in, at whatever capability they happen to have;
  neither manipulates capability gap as a controlled independent variable with a graded
  ladder, and neither implements or tests an action-space restriction on one side as a
  protective intervention." affects_works: `["[GLEE, arXiv:2410.05254]", "[DealOrNoDeal, arXiv:1706.05125]"]`. limitation_type: `generalizability`.
- limitation_text: "The AI-control line protects the weak principal by constraining the
  *strong untrusted party* or the surrounding protocol (trusted monitoring, auditing
  budgets, deferral rules) and prices that protection in safety or dollar terms; it never
  studies restricting the *weak party's own* expressive channel as self-protection, and its
  outcome variable is catastrophe probability, not surplus split." affects_works:
  `["[AIControl, OpenReview:KviM5k8pcP]", "[ControlTax, OpenReview:BpyR6Wkl1c]"]`. limitation_type: `other`.
- limitation_text: "The strategic-persuasion formalization measures the *sender's*
  persuasive gain against a fixed receiver; it does not vary the receiver's capability
  relative to the sender, and offers the receiver no structural defenses (e.g.,
  schema-restricted interaction) whose protective value could be measured." affects_works:
  `["[StrategicPersuasion, OpenReview:aTCXvJKnkE]"]`. limitation_type: `generalizability`.
- limitation_text: "ARIA treats the exponential free-form action space in negotiation as a
  *training-time* credit-assignment problem to be compressed away for sample efficiency; it
  does not ask the deployment-time question of whether exposing that action space makes an
  agent exploitable by a stronger opponent, nor compare constrained vs. free-form action
  spaces under adversarial pressure." affects_works: `["[ARIA, OpenReview:eumRwpgdMU]"]`.
  limitation_type: `other`.
- limitation_text: "CompeteAI's competition dynamics emerge among agents of roughly
  homogeneous capability in a persistent market; capability asymmetry is neither controlled
  nor measured, and without a closed-form reference split no per-interaction surplus loss
  can be attributed to exploitation." affects_works: `["[CompeteAI, OpenReview:wGtzp4ZT1n]"]`.
  limitation_type: `generalizability`.
- limitation_text: "CAPA shows that weak-to-strong outcomes are modulated by functional
  similarity between the model pair, implying that any single-axis 'capability gap' study
  that ignores pair similarity risks confounding — but CAPA itself only diagnoses this for
  judging/supervision, not for adversarial bargaining." affects_works:
  `["[GreatModelsThinkAlike, OpenReview:3Z827FtMNe]"]`. limitation_type: `theoretical`.
- limitation_text: "The closest method-twin studies bilateral bargaining under the exact
  structured-offer-vs-free-text manipulation this paper uses (M3), but only between
  symmetric-capability human dyads, scored only by raw agreed price with no computable
  reference split — so it cannot say whether the manipulation's effect (null on price,
  positive on speed/variance/agreement-rate at zero capability gap) changes sign or
  magnitude once one side is capability-disadvantaged and outcomes are scored as
  surplus loss against a Pareto/Nash reference." affects_works:
  `["[LanguageOfBargaining, ACL:2023.acl-long.735]"]`. limitation_type: `generalizability`.
- **grounding_check**: `true` — every limitation cites at least one N4-resolvable
  citation_key in exactly the N3 string form.
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "These are reasoned gaps relative to real retrieved papers, not limitations claimed by a (nonexistent) paper's own related-work section.", "why_matters": "N4 in a real digest reports the paper's own claims; here the argument chain is this digest's own.", "implication": "Re-derive N4 from the actual paper's related-work section once written; until then treat each item as a falsifiable reading of the cited paper's scope."}`

---

## N5 Challenges

**Node fields:** `challenges`, `conflation_check`

- **C1** [HYPOTHESIS]: "Model capability is multi-dimensional (reasoning, persuasion,
  theory-of-mind, instruction-following), so any scalar 'capability gap' is a projection —
  and different projections (general benchmark delta vs. task-specific rating) can order
  the same model pairs differently, threatening the meaning of a gap-vs-loss curve. Pair
  *similarity* further confounds the gap axis (two equally 'strong' adversaries of
  different families may exploit differently)." — problem-inherent: about the variable
  itself, regardless of which agents or tools are used.
- **C2** [HYPOTHESIS]: "Measuring 'surplus loss' requires a bargaining game complex enough
  to be non-trivial for LLM agents (multi-issue, private values, time pressure), yet simple
  enough to admit a closed-form Pareto frontier and a defensible reference split — and
  'fair reference' is itself contested (Nash vs. equal-split vs. Kalai–Smorodinsky), so
  the two requirements plus the reference choice pull in different directions."
- **C3** [HYPOTHESIS]: "A strong adversary can extract surplus through two confounded
  channels — better substantive bargaining (offer timing, concession strategy, value
  inference) or rhetorical/persuasive tactics in free-form language — and behavioral
  transcripts alone cannot cleanly attribute an observed loss to one channel, independent
  of instrumentation."
- **C4** [HYPOTHESIS, directly derived from the seed's framing]: "Restricting the weak
  agent's action space removes both its exposure as a *victim* of rhetorical exploitation
  and its own legitimate self-defense moves (framing, stalling, commitment language) — so
  whether restriction nets out to protection or further weakening is not decidable a
  priori; it is the crux the seed poses (README line 18: '受限行动空间的弱agent...会不会反而优于不设限的强agent')."
- **conflation_check**: `true` [HYPOTHESIS] — C1 (defining the gap), C2 (defining the
  reference), C3 (attributing the loss), C4 (net effect of restriction) are genuinely
  distinct obstacles.
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "No paper text states these challenges; they are derived from the seed plus the corpus-grounded reading in N3/N4.", "why_matters": "Without a written paper the authors' own framing of obstacles is unknowable.", "implication": "Use as a design checklist for the eventual method, not a verified account."}`

---

## N6 Methodology

**Node fields:** `overview`, `key_components`, `challenge_arguments`, `unaddressed_challenges`

- **overview** [HYPOTHESIS]: "A two-factor experiment crossing (i) a capability gradient —
  a ladder of LLM tiers playing the weak principal's agent against fixed strong-adversary
  models, with the gap quantified both exogenously and endogenously — with (ii) an
  action-space constraint applied to the weak agent only (schema-validated structured
  offers vs. free text). Each design cell runs repeated episodes of multi-issue
  alternating-offers bargaining with closed-form Pareto frontiers and a Nash-bargaining
  reference split; normalized surplus loss is regressed on capability gap per condition.
  **Staged plan** — *Stage 1 (pilot = the seed's minimal experiment, README line 19)*:
  3 weak tiers × 1 fixed strong adversary × 2 action-space conditions × 1 game family
  (GLEE-style bargaining) × 50 episodes/cell = 300 episodes; gate criterion: ≥80%
  protocol-valid episodes (parseable offers, agreement-or-impasse resolution) in the
  weakest cell, and a nonzero surplus-loss spread across tiers. *Stage 2 (scale-up)*:
  6-model round-robin (30 directed unequal pairs + 6 self-play zero-gap controls) × 2
  conditions (+1 both-constrained control cell) × 3 game families × 50 episodes/cell ≈
  22k episodes, plus a tactic-annotation subsample of ~1,500 free-text transcripts."

- **key_components** [HYPOTHESIS]:
  - **M1 — Capability ladder & dual gap quantification**: "5–6 LLMs spanning tiers (e.g.,
    ~8B open-weight → mid-tier → frontier), each playable as weak agent or adversary. Gap
    measured two ways, per model pair: (a) exogenous — delta in a public general-capability
    score (e.g., Chatbot Arena Elo or MMLU-Pro), fixed before any bargaining; (b)
    endogenous — negotiation-specific Elo fitted from round-robin free-text self-play
    win/surplus outcomes, following the role-specific Elo estimation of
    [ScalingLawsOversight, OpenReview:u1j6RqH8nM]. Granularity: one (gap_a, gap_b) pair
    per directed model pair; analyses run under both, agreement reported."
  - **M2 — Bargaining harness with computable reference split**: "A parameterized
    multi-issue alternating-offers environment (3 issues, private integer valuations,
    known reservation values, discounting or a T=10-round deadline), instantiated from two
    real game families — GLEE bargaining configurations [GLEE, arXiv:2410.05254] and
    Deal-or-No-Deal value-function scenarios [DealOrNoDeal, arXiv:1706.05125] — plus one
    synthetic divide-the-pie suite. For every instance the Pareto frontier, Nash-bargaining
    solution, equal-split, and Kalai–Smorodinsky points are computed in closed form; every
    episode logs offers, messages, and outcome. Instrument: deterministic game engine +
    per-turn JSON logs."
  - **M3 — Action-space constraint mechanism**: "Constrained condition: the weak agent's
    entire turn is one JSON object `{action: accept|reject|counteroffer, allocation:
    {issue_i: qty}}`, enforced via function-calling/constrained decoding with schema
    validation and ≤2 resamples on parse failure; no natural-language field is transmitted.
    Free-text condition: the same offer object plus ≤150 words of free-form message.
    The adversary is free-text in both primary conditions; a both-constrained control cell
    isolates adversary-side channel effects. Granularity: per turn."
  - **M4 — Surplus-loss scaling analysis**: "Per episode, normalized surplus loss =
    (u_ref − u_realized) / (u_ref − u_reservation) for the weak side, with impasse scored
    as u_reservation. Mean loss regressed on capability gap via a mixed-effects linear
    model with random intercepts for game instance and model pair; slope + 95% CI is the
    RQ1 estimand, computed separately per action-space condition and per gap measure."
  - **M5 — Constraint-contrast & channel-attribution analysis**: "Primary contrast: 2
    (condition) × k (gap level) mixed-effects factorial testing the condition main effect
    and the condition×gap interaction. Channel attribution: an LLM-judge tags each
    adversary free-text message against a closed tactic taxonomy (anchoring,
    misrepresentation of value, false deadline/commitment, flattery/pressure), with 10%
    double-coded by humans (target Cohen's κ ≥ 0.7); tactic incidence is related to
    per-episode loss to estimate how much of the gap effect flows through the rhetorical
    channel."

- **challenge_arguments** [HYPOTHESIS]:
  - `{challenge_id: "C1", argument_text: "Dual gap measurement (exogenous score delta + endogenous negotiation Elo fitted from play, per M1) plus regression under both measures (M4) operationalizes the fuzzy capability construct and makes projection-dependence itself observable: if the two gap measures disagree about the loss curve, that disagreement is reported rather than hidden.", mechanism_components: ["M1", "M4"]}`
  - `{challenge_id: "C2", argument_text: "The harness (M2) draws games from two established negotiation families with closed-form frontiers and scores every episode against three reference solutions (Nash primary; equal-split and Kalai–Smorodinsky as robustness), resolving the complexity-vs-scorability tension by construction and the contested-reference problem by sensitivity reporting.", mechanism_components: ["M2"]}`
  - `{challenge_id: "C3", argument_text: "The structured-offer condition (M3) structurally deletes the rhetorical channel, so the loss difference between conditions at matched gap bounds the rhetorical contribution; tactic tagging (M5) provides converging correlational evidence within the free-text condition.", mechanism_components: ["M3", "M5"]}`
  - `{challenge_id: "C4", argument_text: "Because the constraint contrast (M5) is run across the full capability gradient with self-play zero-gap controls and a both-constrained control cell, the design can distinguish 'constraint protects the weak' from 'constraint hurts everyone equally' — testing rather than assuming the sign of the net effect.", mechanism_components: ["M5", "M1"]}`

- **unaddressed_challenges** [HYPOTHESIS, per V-08 — inferred N5/N6, flagged explicitly]:
  `["C1", "C3"]` — C1: even dual measurement leaves capability multi-dimensional; pair
  similarity (per [GreatModelsThinkAlike, OpenReview:3Z827FtMNe]) is logged but not
  experimentally controlled. C3: only partially addressed — the between-condition bound is
  causal, but within-condition tactic attribution remains correlational.

- **Feasibility** [HYPOTHESIS]:
  - *Compute/effort order of magnitude*: Stage 1: 300 episodes × ~20 turns × ~400 tokens
    ≈ 2–3M tokens — trivial API cost (tens of dollars), ~1 person-week including harness
    debugging. Stage 2: ~22k episodes ≈ 150–250M tokens across 6 models — **$2k–$5k API
    cost class**, no GPU training anywhere; ~2,000 LLM-judge tactic calls plus ~150
    human double-coding transcripts ≈ **~30 annotator-hours**; total ~4–6 person-weeks.
  - *Single biggest feasibility risk*: weak-tier models may fail to negotiate at all —
    unparseable offers, incoherent concessions, or impasse floor effects — making surplus
    loss degenerate (all-impasse cells) and the scaling curve unidentifiable at exactly
    the gap levels of interest. *Mitigation*: schema-validated retry (≤2 resamples) with
    forced-choice fallback; impasse scored at reservation value so the metric stays
    defined; the Stage-1 gate criterion (≥80% valid episodes in the weakest cell) decides
    whether to swap in a stronger 'weak' tier before scale-up spend.

- **status**: PARTIAL. **absence_comment**: `{"what_missing": "No method has been implemented; component operationalizations are design commitments, not descriptions of built artifacts.", "why_matters": "Which challenges the real method addresses depends on implementation choices not yet fixed.", "implication": "Use as the methodology section's blueprint; revise ids only by appending, to keep cross-references stable."}`

---

## N7 Contributions

**Node field:** `contributions`

- **CO1** [HYPOTHESIS]: "An empirical scaling estimate — slope with confidence interval,
  under two capability-gap measures — of normalized surplus loss for a weak principal's
  LLM agent as a function of the capability gap to a strong adversary in multi-issue
  bargaining." contribution_type: `empirical_finding`. is_testable: `true`. has_rq: `true` (RQ1).
- **CO2** [HYPOTHESIS]: "A causal test of whether restricting the weak agent's action
  space to schema-validated structured offers changes surplus loss relative to free text,
  at matched capability gaps and with zero-gap and both-constrained controls."
  contribution_type: `empirical_finding`. is_testable: `true`. has_rq: `true` (RQ2).
- **CO3** [HYPOTHESIS]: "A reusable bargaining evaluation harness combining GLEE-style and
  Deal-or-No-Deal-style game families with closed-form Pareto frontiers, three reference
  solutions, and per-turn structured logging, for measuring LLM-agent negotiation under
  capability asymmetry." contribution_type: `technical_artifact`. is_testable: `true`.
  has_rq: `false` (instrumental infrastructure).
- **CO4** [HYPOTHESIS, conditional]: "A deployment recommendation — 'constraint as
  protection' — for practitioners fielding weaker LLM agents against unknown or stronger
  counterparties, contingent on CO1/CO2 holding in the predicted direction, plus a
  channel-attribution account of *why* (how much loss flows through the rhetorical
  channel)." contribution_type: `conceptual_framework`. is_testable: `true` (falsifiable —
  see N9). has_rq: `true` (RQ2, RQ_INF_3).
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "No paper exists to state these as its own claimed contributions.", "why_matters": "Contributions are normally the paper's asserted novelty; here they are projected from the design.", "implication": "Replace with the actual contributions section once drafted."}`

---

## N8 Research Questions

**Node fields:** `research_questions`, `datasets`, `baselines`, `metrics`

- **RQ1** [GIVEN, near-verbatim from seed core question, README line 18, first sentence]:
  "How does surplus loss for a weak-capability agent negotiating on behalf of a principal,
  against a strong-adversary agent, scale as a function of the capability gap between
  them?" rq_source: `explicit`. evaluates_mechanisms: `["M1", "M2", "M4"]`.
  addresses_challenges: `["C1", "C2"]`. tests_contributions: `["CO1"]`.
  answered_by_experiment: "capability-gradient arm: mixed-effects regression of normalized
  surplus loss on gap (both gap measures), 30 directed unequal pairs + 6 zero-gap
  self-play controls, 3 game families."
- **RQ2** [GIVEN + HYPOTHESIS — operationalized from seed core question, README line 18,
  second sentence. NOTE ON FIDELITY: the seed's literal comparison is constrained-weak vs. an
  *unconstrained strong* agent ("受限行动空间的弱 agent……会不会反而优于不设限的强 agent");
  this design decomposes that into (a) a same-model constraint contrast — the clean causal
  test of the constraint itself — plus (b) the seed's literal cross-tier contrast, read off
  the same factorial]:
  "(a) Does restricting the weak agent's action space to structured offers only (no free
  text) produce lower surplus loss than an unconstrained weak agent negotiating against the
  same strong adversary? (b) Does the constrained weak agent's surplus loss also undercut
  that of an *unconstrained agent from a stronger capability tier* facing the same adversary
  — i.e., can action-space constraint substitute for model capability, as the seed's
  '束缚反而保护' conjecture literally asks?" rq_source: `explicit`.
  evaluates_mechanisms: `["M3", "M5"]`.
  addresses_challenges: `["C4"]`. tests_contributions: `["CO2", "CO4"]`.
  answered_by_experiment: "action-space arm: 2(condition)×k(gap) mixed-effects factorial —
  condition main effect and condition×gap interaction — with both-constrained control cell;
  contrast (b) is the cross-cell comparison of constrained-weak cells against unconstrained
  cells at higher capability tiers within the same gap×condition factorial."
- **RQ_INF_3** [HYPOTHESIS, inferred extension]: "Through which channel —
  substantive bargaining skill or free-text rhetorical tactics — does the strong adversary
  extract the gap-dependent surplus?" rq_source: `inferred`. evaluates_mechanisms:
  `["M3", "M5"]`. addresses_challenges: `["C3"]`. tests_contributions: `["CO4"]`.
  answered_by_experiment: "between-condition loss difference at matched gaps (causal bound
  on the rhetorical channel) + tactic-taxonomy tagging of adversary messages related to
  per-episode loss (correlational)."
- **datasets** [HYPOTHESIS]: `{names: ["GLEE bargaining game configurations (parameterized alternating-offers economic environments) [GLEE, arXiv:2410.05254]", "Deal-or-No-Deal multi-issue object-division scenarios (value functions / scenario generator, not the human dialogues) [DealOrNoDeal, arXiv:1706.05125]", "synthetic 3-issue divide-the-pie suite with closed-form Pareto frontier (generated)"], source: "inferred"}`. Note: no natural corpus is scraped; game *specifications* are real, transcripts are generated by the experiment.
- **baselines** [HYPOTHESIS]: `{names: ["unconstrained free-text weak agent of the same underlying model (primary baseline for RQ2)", "zero-gap self-play control (weak-vs-weak and strong-vs-strong) anchoring surplus loss at gap=0", "scripted time-dependent concession agent (Boulware/linear conceder, classical automated-negotiation strategy) as a capability-floor anchor below the weakest LLM tier", "both-constrained control cell (adversary also schema-restricted)"], source: "inferred"}`.
- **metrics** [HYPOTHESIS]: `{names: ["normalized surplus loss = (u_ref − u_realized)/(u_ref − u_reservation), impasse scored at reservation (primary)", "weak agent's share of realized joint surplus", "agreement rate / impasse rate per cell", "Pareto efficiency of agreements (distance of realized split to frontier)", "gap–loss slope (mixed-effects regression coefficient, per condition and per gap measure)", "tactic incidence rate per adversary transcript (LLM-judge, human-validated κ ≥ 0.7)"], source: "inferred"}`.
- **analysis plan** [HYPOTHESIS]: sample size n=50 episodes/cell (≈22k episodes total;
  power analysis: ~50/cell detects a between-condition standardized effect d≈0.4 at
  power 0.8 within a gap level, and the pooled interaction test is substantially better
  powered). RQ1: mixed-effects linear regression, `loss ~ gap + (1|game_instance) +
  (1|model_pair)`, two-sided Wald test on the gap slope, α=0.05; expected direction:
  slope > 0 (loss increases with gap); monotonicity check via Spearman ρ over gap levels.
  RQ2: mixed-effects factorial, primary tests = condition main effect and condition×gap
  interaction, α=0.05 with Holm correction over the two primary tests; expected direction:
  constrained < unconstrained loss, gap-amplified. RQ_INF_3: paired between-condition loss
  difference per gap level + Poisson/logistic model of loss on tactic counts; α=0.05,
  labeled exploratory (no confirmatory claim). All tests cluster by model pair.
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "RQ1/RQ2 text is given by the seed; RQ_INF_3, datasets, baselines, metrics, and the analysis plan are design proposals.", "why_matters": "The RQs are the fixed anchors; the evaluation scaffolding around them is not yet locked by any experiment or pre-registration.", "implication": "Pre-register the analysis plan (tests, α, directions) before Stage 2 to make N9's falsification conditions binding."}`

---

## N9 Results — HYPOTHESIZED DIRECTION ONLY, NO REAL DATA

**Node field:** `results`. **All entries [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].
No numbers are real; each is a falsifiable directional prediction, not a finding.**

- rq_id: **RQ1** — result_text: "[PLACEHOLDER — HYPOTHESIZED DIRECTION] Normalized surplus
  loss for the weak principal's agent is predicted to increase monotonically — plausibly
  convexly — with capability gap, under both gap measures, in the free-text condition."
  result_type: `quantitative` (once measured). evidence_strength: `missing`. rq_answered:
  `false`. **Falsification condition**: refuted if the mixed-effects gap slope is not
  significantly positive (α=0.05) in the free-text condition, or if the loss curve is flat
  or non-monotonic across gap levels (Spearman ρ ≤ 0), or if the two gap measures yield
  opposite-signed slopes (which would instead confirm C1's projection-dependence worry).
- rq_id: **RQ2** — result_text: "[PLACEHOLDER — HYPOTHESIZED DIRECTION, mirroring the
  seed's explicitly counter-intuitive framing '束缚反而保护', README line 19] The
  constrained (structured-offer-only) weak agent is predicted to incur LOWER surplus loss
  than the unconstrained weak agent against the same adversary at the same gap, with the
  protective effect growing at larger gaps (positive condition×gap interaction)."
  result_type: `quantitative`. evidence_strength: `missing`. rq_answered: `false`.
  **Falsification condition**: refuted if constrained loss ≥ unconstrained loss at matched
  gaps (condition main effect non-significant or opposite-signed under Holm-corrected
  α=0.05) — i.e., if expressiveness restriction fails to protect or actively hurts the
  weak agent, supporting the default intuition that expressive freedom weakly helps the
  weaker party.
- rq_id: **RQ_INF_3** — result_text: "[PLACEHOLDER — HYPOTHESIZED DIRECTION] The majority
  of gap-dependent surplus loss is predicted to flow through the free-text rhetorical
  channel: the between-condition loss difference is predicted to account for more than
  half of the gap slope, and adversary tactic incidence is predicted to correlate
  positively with per-episode loss." result_type: `quantitative`. evidence_strength:
  `missing`. rq_answered: `false`. **Falsification condition**: refuted if surplus loss in
  the structured-only condition scales with gap nearly as steeply as in free text
  (rhetorical channel bound ≈ 0) — implying exploitation is substantive (offer strategy),
  not rhetorical, which would also undercut the mechanism story behind
  constraint-as-protection even if RQ2's contrast happens to hold.
- **status**: NOT_FOUND (no experiment has been run). **absence_comment**: `{"what_missing": "No quantitative or qualitative results exist because no experiment has been executed.", "why_matters": "N9 is the node most at risk of fabrication in a reverse digest; any number here would be invented.", "implication": "Carry forward only the directional hypotheses and falsification conditions; replace the node wholesale with measured results and check which falsification conditions triggered."}`

---

## N10 Threats / Self-Limitations

**Node field:** `threats`

*(Anticipated by this digest, not author-acknowledged — no paper exists.)*

- **t1** [HYPOTHESIS] category: `construct`. description: "The 'fair' reference split is a
  construct choice (Nash bargaining vs. equal split vs. Kalai–Smorodinsky); surplus-loss
  conclusions could flip under a different reference, and 'capability gap' is itself a
  contested scalar projection of a multi-dimensional construct." mitigation: "Score every
  episode under all three reference solutions and both gap measures (M2, M1); report
  conclusions only where the sign is invariant, and report divergences explicitly."
- **t2** [HYPOTHESIS] category: `internal`. description: "The strong adversary may behave
  differently toward constrained vs. unconstrained opponents for reasons other than the
  weak agent's expressiveness (prompt-format cues leaking the condition, order effects,
  provider-side model updates mid-experiment), confounding the condition contrast."
  mitigation: "Identical adversary system prompts across conditions with the condition not
  disclosed; role/side and first-mover counterbalancing; both-constrained control cell;
  pinned model versions and a fixed evaluation window."
- **t3** [HYPOTHESIS] category: `external`. description: "Findings from 5–6 models of a
  few families and three stylized game families may not generalize to other model
  families, richer real-world agent-commerce protocols, or repeated-relationship
  negotiations with reputation." mitigation: "Span ≥2 providers and open- plus
  closed-weight models; run all three game families and report per-family heterogeneity;
  frame the deployment recommendation (CO4) as conditional on the studied one-shot
  bilateral setting."
- **t4** [HYPOTHESIS] category: `conclusion`. description: "Episodes within a model pair
  and game instance are not independent, and the design invites many post-hoc contrasts
  (2 gap measures × 3 references × 3 game families), inflating false-positive risk."
  mitigation: "Mixed-effects models with random effects for pair and instance; two
  pre-registered primary tests with Holm correction; everything else labeled exploratory."
- **t5** [HYPOTHESIS] category: `construct`. description: "LLM-judge tactic tagging (M5)
  may itself be capability-dependent — the judge may miss exactly the subtle tactics that
  strong adversaries use — biasing channel attribution toward null." mitigation: "10%
  human double-coding with κ ≥ 0.7 acceptance gate; judge model chosen to be at least as
  strong as the strongest adversary; RQ_INF_3 kept exploratory."
- **status**: NOT_FOUND (no author-stated threats section exists). **absence_comment**: `{"what_missing": "There is no Limitations section because no paper exists; t1–t5 are this digest's anticipated threats with proposed mitigations, not author-acknowledged ones.", "why_matters": "N10 is defined as author-acknowledged limitations; third-party anticipation is weaker evidence.", "implication": "Re-derive strictly from the paper's own Limitations section once written; the mitigations above are design requirements, not accomplished facts."}`

---

## N11 Artifacts

**Node fields:** `artifacts`, `has_code`, `has_data`, `has_model`

- **artifacts**: `[]` [PLACEHOLDER]
- **has_code**: `false` [PLACEHOLDER]
- **has_data**: `false` [PLACEHOLDER]
- **has_model**: `false` [PLACEHOLDER]
- **status**: NOT_FOUND. **absence_comment**: `{"what_missing": "No code, data, or model has been released because no experiment has been run.", "why_matters": "The harness (CO3) and episode transcripts are the natural artifacts and their release will be reviewer-relevant.", "implication": "Plan to release the harness, game-instance generators, transcripts, and analysis code; revisit this node at that point."}`

---

## N12 Contribution Type

- **value** [HYPOTHESIS]: `empirical`
- **rationale** [HYPOTHESIS]: "Re-checked against the strengthened N6/N8/N9: the paper's
  headline deliverables are a measured scaling relationship (CO1, RQ1) and a
  pre-registered factorial causal contrast (CO2, RQ2) over existing, already-trained LLMs
  — a controlled behavioral measurement study in the mold of the debate-persuasiveness and
  oversight-scaling exemplars, not a new system or theory. The strongest competing label is
  `benchmark`, since M2 packages two real game families into a reusable harness (CO3); it
  is rejected because the harness is instrumental — no leaderboard, coverage claim, or
  community-evaluation framing is proposed, and every RQ tests a phenomenon (surplus-loss
  scaling, constraint protection), not the harness's own quality. `tool` fails for the same
  reason; `theoretical` fails because no formal result is derived (the Nash/KS references
  are imported, not proven)."
- **source**: `hypothesis`
- **status**: PARTIAL. **absence_comment**: `{"what_missing": "No paper exists to classify directly; this is inferred from the projected design.", "why_matters": "If the eventual paper leads with releasing the harness + game suite as a community benchmark, the correct value shifts to `benchmark`.", "implication": "Re-classify from the real abstract and results framing — check whether the measurement or the artifact is the headline."}`

---

## Claims

- **[HYPOTHESIS]** "Normalized surplus loss scales positively — plausibly convexly — with
  the capability gap between a weak principal-representative agent and a strong adversary
  in multi-issue bargaining." evidence: `[{type: "argument", text: "adjacent weak-vs-strong adversarial games show systematic capability-dependent outcomes with fittable scaling structure ([ScalingLawsOversight, OpenReview:u1j6RqH8nM] Elo scaling laws); bargaining-power intuition extrapolated from the seed's core question", source: "hypothesis", location: null}]`. Falsifiable per N9/RQ1.
- **[HYPOTHESIS]** "Restricting the weak agent to schema-validated structured offers
  reduces its surplus loss relative to free-form negotiation against the same strong
  adversary — 'constraint-as-protection' — and the protection grows with the gap."
  evidence: `[{type: "argument", text: "seed's own counter-intuitive framing '束缚反而保护' (README line 19); protocol-level restriction demonstrably protects weak principals in the AI-control setting ([AIControl, OpenReview:KviM5k8pcP], [ControlTax, OpenReview:BpyR6Wkl1c]); the free-form channel is exactly where strategic persuasion operates ([StrategicPersuasion, OpenReview:aTCXvJKnkE])", source: "hypothesis-grounded", location: null}]`. The paper's headline, most contestable claim — falsifiable per N9/RQ2.
- **[HYPOTHESIS]** "Most gap-dependent surplus loss flows through the free-text rhetorical
  channel rather than substantive offer strategy." evidence: `[{type: "argument", text: "the free-form action space is independently identified as the pathological object in language-based negotiation ([ARIA, OpenReview:eumRwpgdMU]); mechanism claim behind constraint-as-protection", source: "hypothesis-grounded", location: null}]`. Falsifiable per N9/RQ_INF_3.
- **[GIVEN]** "If 'constraint-as-protection' holds, it constitutes a directly deployable
  practitioner recommendation for agent-to-agent commerce systems." — near-verbatim from
  seed README line 19 ("是可直接落地的部署建议").
- **[PLACEHOLDER]** "No numeric results exist yet — every directional claim above is a
  pre-registration-style prediction pending an experiment that has not been run, each with
  an explicit falsification condition in N9."

---

## Self-verification pass

- **V-01 locator integrity**: nothing is tagged `source="extracted"` in the schema sense
  (no paper exists); GIVEN items anchor to the seed README lines 16/18/19 as cited inline;
  GROUNDED:corpus items anchor to `topics/corpus/ideas.jsonl` records via
  `OpenReview:paper_id` and paper_url; HYPOTHESIS/PLACEHOLDER items carry `location: null`.
- **V-02 absence comments**: every node with status != FOUND (all nodes) carries a 3-part
  `absence_comment`.
- **V-04 / EX-09 ID consistency** (checked mechanically before writing; re-checked at the
  2026-07-04 Phase A re-run after the N3/N4 method-twin addition below):
  - `N4.limitations[].affects_works` ⊆ N3 citation_keys — all 8 limitations cite keys
    verbatim from N3: {ScalingLawsOversight, WeakToStrong, GLEE, DealOrNoDeal, AIControl,
    ControlTax, StrategicPersuasion, ARIA, CompeteAI, GreatModelsThinkAlike,
    LanguageOfBargaining} — all 11 N3 keys exist; `grounding_check=true` is consistent (no
    empty affects_works). All ten pre-existing keys plus `LanguageOfBargaining` now also
    resolve to `selected` records in `discussion/reference_candidates.jsonl` (Phase A item 2
    fix, 2026-07-04).
  - `N6.challenge_arguments[].challenge_id` ⊆ {C1,C2,C3,C4}; `mechanism_components` ⊆
    {M1..M5}; `unaddressed_challenges` = ["C1","C3"] ⊆ {C1..C4}.
  - `N8.research_questions[].addresses_challenges` ⊆ {C1..C4}; `tests_contributions` ⊆
    {CO1..CO4}; `evaluates_mechanisms` ⊆ {M1..M5}.
  - `N9.results[].rq_id` ∈ {RQ1, RQ2, RQ_INF_3} — all three defined in N8.
  - All resolve; RQ1/RQ2 ids unchanged from the previous digest version (stable), C1–C4
    and M1–M5 ids stable with sharpened text.
- **V-08**: `unaddressed_challenges` rests on an inferred N5/N6 pair and is flagged as such.
- **V-10/V-11**: N10 and N11 carry `status="NOT_FOUND"` with full absence_comments;
  N10 threats now include explicit mitigations as *design requirements*, not author claims.
- **V-12**: N12 rationale names and rejects the concrete competing labels (`benchmark`,
  `tool`, `theoretical`) against projected N6/N8/N9 content.
- **EX-11 empty-node check**: all of N0–N12 plus Claims present, none omitted.
