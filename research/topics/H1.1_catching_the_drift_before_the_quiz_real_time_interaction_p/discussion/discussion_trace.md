# Auto-Research-Discussion Trace — H1.1 (autoclaude self-play, 2026-08-15)

> Mode: **autoclaude** (Claude plays proposer, critic, and refiner; no user in the loop; no
> `ignore_and_submit` override exists). Seed: the topic bundle itself — `README.md` (topic card),
> `digest.md` (reverse N0–N12, grounded 2026-08-13), `discussion.md` (a prior 6-stage
> critic-refined design, 2026-08-13), `paper-draft.revised.md` (v2 draft, 2026-08-14), and
> `autodiscussion_draft_review.md` (a MAJOR-REVISION audit of the autodiscussion package,
> 2026-08-14). Per `autoclaude_mode.md` Rule 1, every student position below cites its evidence in
> these files; every critic flag points at contradicting evidence, not vibes. The prior
> `discussion.md` is treated as a strong v1 source, **not** as pre-confirmed output — each stage
> re-proposes, takes one genuine critic round, and closes only with zero open `[major]`s.
> Round cap 5/stage (never hit). Citation freshness: all six arXiv anchors re-verified against the
> arXiv export API on 2026-08-15 (titles match; IDs 2601.20245, 2506.08872, 2507.09089,
> 2606.06253, 2605.11350, 2607.06101).

## Seed brief

- **One-sentence description:** extend Shen & Tamkin's skill-formation RCT (arXiv:2601.20245;
  52 developers, AI arm −17 quiz points, six hindsight-coded interaction patterns) with (a) a
  prefix-only, prognostic detector of erosive-pattern risk and (b) a gated, placebo-controlled
  just-in-time nudge trial on the same task/quiz instrument.
- **Inputs:** session query streams (query text, timestamps, response text, paste/error events);
  the published task, quiz rubric, and six-pattern coding protocol.
- **Outputs:** precision-at-prefix curves + human prefix-labeling ceiling; a sealed go/no-go gate
  decision; causal effect estimates from a four-arm live trial; detection-lag distribution.
- **Closest research vocabulary:** skill formation / deskilling under AI assistance (HCI, SE-ed),
  JITAI (mHealth), cognitive forcing functions, ITS/knowledge tracing.
- **In scope:** the Shen & Tamkin setting (unfamiliar-library coding, 1+yr Python devs);
  query-log-only sensing; one additive nudge. **Out of scope:** agentic coding products,
  longitudinal dissipation, multi-nudge policies (scale-up only).
- **Confidence: high** — the bundle is unusually mature; the main risk is *regressing* to the
  pre-review draft rather than misreading the seed. The review's two inferred unresolved MAJORs
  (offline-stage statistical infeasibility; loss of the concurrent hand-code arm) and its top-3
  fixes are treated as standing constraints on every stage below.

---

## Stage 1 — Problem Definition

**ROUND 1 [critic phase].**

*draft_v1* (proposer; adapted from `README.md`'s 核心问题 and `discussion.md` Stage 1 draft):

- `summary`: "Given the published causal fact that AI-assisted learners of an unfamiliar library
  score 17 points lower on a post-task quiz and that six hindsight-coded interaction patterns
  predict who learns, determine whether a classifier over query-stream features can recognize
  *which low-scoring pattern* a learner is entering within the first N queries, and whether a
  triggered nudge improves the quiz outcome in a three-arm RCT directly comparable to the
  published 50%/67% baseline."
- `input`: session-observable query streams (query text, timestamps, response text, paste/error
  events); the base paper's task, quiz rubric, and six-pattern coding protocol; hindsight labels.
- `output`: (1) real-time pattern classifications with precision/recall vs. hindsight labels;
  (2) quiz-score comparison across three arms plotted against the published numbers;
  (3) detection-lag statistics.
- `constraints`: no model internals, no biometrics; three arms (hand-code / AI-assist /
  classify+intervene); population = 1+yr Python, no Trio experience.
- `objective`: classifier beats the trivial majority baseline early enough to act; intervention
  arm significantly exceeds the AI-assist arm.
- `study_type`: technical ("a classifier that…" per the stages.md inference rule).

*critique v1:*
- summary: "The draft imports the README's diagnostic framing and a leaderboard-ish study_type;
  both are contradicted by the bundle's own later evidence."
- comments:
  1. `[major]` field `summary`/`formal_summary` (anti-pattern: `formal_summary_drift` /
     `fields_misaligned`) — "Recognize which pattern a learner is entering" treats the six-way
     label as a latent state observable at query 3. The evidence says otherwise: digest.md N4
     limitation 1 (the taxonomy is "*post-hoc qualitative coding of complete session
     transcripts*") and discussion.md Stage 1 critic (a) ("a learner may genuinely be
     pattern-indeterminate at query 3 … a prognostic risk score, not a diagnostic label").
     Prefix-time six-way diagnosis is partially ill-posed by construction; the estimand must be
     the risk that the session, if uninterrupted, *terminates* erosive. Also, the two halves are
     a compound bet — digest.md N6 makes offline validation "a hard gate … before any live
     intervention" — so the gate belongs in the problem definition's output/objective, not buried
     in methods.
  2. `[major]` field `study_type` — v1 says `technical` by pattern-matching "classifier." But the
     declared outputs are measurements (precision-at-prefix curves, a ceiling, a lag
     distribution) and a randomized treatment-effect estimate; nothing is a beats-baseline
     comparison on a shared task, and digest.md N12 already classifies the contribution type as
     `empirical` ("M1's classifier … built as instruments for this measurement, not as a
     leaderboard-style benchmark product"). Declaring `technical` would *force* an outcome-tier
     beats-baseline RQ at Stage 6 that misrepresents the paper. Per stages.md, the inference must
     be said out loud: `empirical`.
  3. `[minor]` field `constraints` — "three arms" is a design choice leaking into the problem
     statement (the placebo question is a Stage-5 matter); the constraint that belongs here is
     *comparability to the published instrument*, not an arm count.
- decision: revise_and_recritique.

**ROUND 2 [critic phase].**

*draft_v2* (majors 1–2 and minor 3 addressed): summary re-framed as a **gated, two-stage causal
extension**: Stage-1 (offline) estimand = prognostic risk r(prefix) = P(session terminates in an
erosive pattern | first k queries); Stage-2 (live) estimand = causal effect of a
detection-triggered intervention on the quiz outcome, authorized only if a pre-registered
precision criterion holds; arm-count language removed from constraints; `study_type: empirical`
with the inference stated.

*critique v2:* summary: "Both majors resolved — the estimand is now prognostic and the gate is
part of the problem's output structure; study_type is argued, not guessed." Major 1: **resolved**.
Major 2: **resolved**. Minor 3: resolved. No new flags. decision: move_to_refiner.

**REFINER PASS** (once, conservative): tightened the `formal_summary` notation (no new
assumptions): session Q_i = (q_i1,…,q_iT_i); hindsight label L_i ∈ {0,1} by the published coding
protocol; prefix Q_i^(k); learn f: Q^(k) → [0,1] with r_ik = f(Q_i^(k)) ≈ P(L_i=1 | Q_i^(k));
alert 1[r_ik ≥ c]; gate G ∈ {0,1} = a pre-registered function of sealed-set alert precision; if
G=1, estimate treatment effects on blinded quiz score Y under randomization. changes_made:
formalization + consistency; declined_to_fix: none.

**CONFIRMED STAGE 1 OUTPUT**

- **summary**: A gated, two-stage causal extension of a published skill-formation RCT.
  Offline: determine whether the risk that an AI-assisted learning session, if uninterrupted,
  terminates in a skill-eroding interaction pattern is estimable from a session *prefix* using
  only query-stream observables — and how early such risk is visible at all, to humans or to any
  statistical procedure. Live (authorized only if a pre-registered precision criterion holds on
  sealed data): determine whether a one-shot intervention triggered by that risk estimate
  causally improves the downstream quiz outcome, under controls that internally re-test the
  published hand-vs-AI gap.
- **formal_summary**: For developer i, session Q_i = (q_i1,…,q_iT_i) with hindsight label
  L_i ∈ {0,1} (erosive- vs. protective-terminal, by the published six-pattern coding protocol
  collapsed to a binary). For prefix length k, Q_i^(k) = (q_i1,…,q_ik). Offline: learn
  f: Q^(k) → [0,1], r_ik = f(Q_i^(k)) ≈ P(L_i = 1 | Q_i^(k)), alert rule 1[r_ik ≥ c]; report
  precision/recall over k, against the prevalence baseline and the human prefix ceiling. Gate:
  G = 1 iff a pre-registered function of sealed-set alert precision (with minimum alert count and
  false-positive-burden bounds) passes. Live (iff G = 1): with blinded quiz score Y and
  randomized arm assignment A, estimate pre-registered contrasts E[Y|A=a] − E[Y|A=a′], including
  an internal replication contrast anchored to the published gap.
- **input**: query text, timestamps, assistant responses, paste/error events (a logging proxy's
  view — no model internals, no biometrics, no future-of-session features at prediction time);
  the published task design, quiz rubric, and six-pattern coding protocol; hindsight labels from
  that protocol.
- **output**: (1) calibrated prognostic risk scores with precision/recall-at-prefix-length and
  at-elapsed-time curves vs. the prevalence baseline; (2) the human prefix-labeling ceiling —
  how early the patterns are visible to expert annotators blind to session endings; (3) a sealed,
  pre-registered go/no-go gate decision; (4) causal effect estimates of the triggered
  intervention on the quiz outcome, with an internal replication of the published hand-vs-AI
  contrast; (5) the detection-lag distribution (when the first alert fires, and how much session
  remains).
- **constraints**: prefix-only observability (features at k use nothing after query k); ground
  truth exists only as hindsight session-level labels; small samples (tens of offline sessions;
  ~30/arm live); human subjects with mild information asymmetry (logged sessions, arm and trigger
  concealed until debrief, IRB-approved); results must remain directly comparable to the
  published instrument (same task family, same rubric, deviations documented); the intervention
  may add content but never withhold it.
- **objective**: every stage evaluable by a pre-registered binary criterion: detection = a
  conservative lower confidence bound on alert precision exceeding a prevalence-anchored bar at a
  prefix no longer than half the median session; authorization = the sealed gate's exact
  criterion; intervention = pre-registered arm contrasts on the original-rubric quiz score with
  task-completion guardrails.
- **study_type**: **empirical** (stated inference: outputs are measurements and randomized
  treatment-effect estimates; the classifier is an instrument, not a competitor — digest N12
  concurs). Stage 6 therefore must contain **zero** outcome-tier beats-baseline RQs.

---

## Stage 2 — Motivation

**ROUND 1 [critic phase].**

*draft_v1* (proposer; adapted from `discussion.md` Stage 2 refined — four legs): (1) causal
premise from the base RCT, re-tested by internal replication; (2) feasibility precedents (Yao's
behavioral signature; Cao & Huang's real-time proxy; JITAI credited as the loop template);
(3) normative urgency for the FAccT form (erosion invisible at decision time; post-hoc
measurement structurally favors the vendor; "tooling vendors are shipping learning modes without
any detection component"); (4) timing (base paper 7 months old; offline stage needs no live-RCT
IRB).

*critique v1:*
- summary: "The four legs are well-sourced but do not cover everything Stage 1 now promises."
- comments:
  1. `[major]` field `why_it_matters` (anti-pattern: `partial_output_coverage`) — Stage 1's
     confirmed outputs include, as first-class deliverables, "(2) the human prefix-labeling
     ceiling" and "(5) the detection-lag distribution." No leg motivates either. The bundle
     itself supplies the missing argument: discussion.md SP2 makes the ceiling "the achievable
     ceiling and the honest denominator for classifier performance … itself a reportable
     scientific result," and the README's title bet ("catching the drift *before the quiz*") is
     only checkable as a *timing* property — a detector that fires at session end supports no
     just-in-time anything. The motivation must argue why these two measured quantities matter,
     or Stage 1 promised outputs the paper never justifies.
  2. `[minor]` field `evidence` (anti-pattern: `unsourced_pain`) — the "vendors are shipping
     learning modes" product claim carries discussion.md's own [VERIFY] flag and remains
     unverified; drop it or demote it to explicitly-unverified color. The verified urgency
     argument (delegation is the product's default happy path; the harmed party cannot see the
     harm at decision time) stands without it.
- decision: revise_and_recritique.

**ROUND 2 [critic phase].** *draft_v2*: leg 2 expanded to motivate the ceiling (bounds any
detector; first quantification of how early the patterns are visible at all; de-risks the gate)
and the lag distribution (the deliverable that makes "just-in-time" falsifiable); product claim
dropped. *critique v2:* major 1 **resolved**; minor 2 resolved; no new flags.
decision: move_to_refiner.

**REFINER PASS**: tightened phrasing; kept claim strength constant (no invented support).
changes_made: wording + epistemic-status tags carried from digest. declined_to_fix: none.

**CONFIRMED STAGE 2 OUTPUT**

- **summary**: Skill erosion under AI assistance is causally established and pattern-mediated,
  but every existing measurement arrives after the fact; if the drift toward an erosive pattern
  is catchable in the behavior stream — a timing question nobody has quantified, for humans or
  machines — then detection can trigger intervention before the outcome is locked in, and the
  same instrument that established the harm can verify the fix.
- **why_it_matters** (four legs, each with epistemic status):
  1. *Causal premise, re-tested rather than assumed* [GROUNDED: read]. The base RCT names the
     lever: outcome tracks the interaction pattern (<40% vs. 65–86% by pattern), not AI use per
     se. A pattern that predicts the outcome and is visible in behavior is an invitation to
     detect and intervene. The premise rests on n=52 in one lab, so the design internally
     replicates the hand-vs-AI gap — its fragility becomes a measured result either way.
  2. *The measurement gap is a timing gap, and the ceiling and lag are its first-class
     quantities* [GROUNDED: read / search-only flagged]. The base RCT codes complete recordings;
     Yao's "AI-prompt signature" is retrospective and cohort-level; Kosmyna et al. measure
     downstream neural/recall states. Nobody knows how early erosive patterns are visible *at
     all* — so the human prefix-labeling ceiling is both the honest denominator for any detector
     and a new scientific quantity, and the detection-lag distribution is what turns
     "just-in-time" from a slogan into a falsifiable timing property. Cao & Huang show a
     real-time behavioral proxy can beat retrospective measures for reliance (gaze, hardware,
     decision outcome) — whether zero-hardware query-log features match that grade of signal is
     exactly the open question this study measures.
  3. *Normative urgency (the FAccT form)* [argued from verified premises]. Erosion is invisible
     at decision time to the person incurring it; delegation is the assistant's default happy
     path; measurement that happens only after the quiz structurally favors the vendor.
     Prefix-only detection using nothing but the query log is an accountability instrument
     deployable by parties who do not own the model.
  4. *Timing/window* [GROUNDED]. The base paper is seven months old and its framing states the
     open question; the JITAI and cognitive-forcing literatures supply a credited loop template
     and intervention class with RCT evidence; the offline stage needs only a lightweight
     transcript-collection protocol, so first results can exist while the live-RCT IRB pipeline
     (submission 2026-11-15) is pending.
- **who_cares**: developers and employers making AI-assistance policy; AI-assistant vendors
  (a deployable protective-mode trigger); educators and platforms that must certify durable
  skill; auditors/regulators needing vendor-independent measurement; the HCI/CSCW research
  community (a reusable gated-intervention methodology).
- **evidence**: Shen & Tamkin RCT (50% vs. 67%, d=0.738, p=.01, six patterns; arXiv:2601.20245,
  read); Kosmyna et al. EEG essay-writing convergence (arXiv:2506.08872, preprint, direction
  only); Yao's platform-scale behavioral signature and AI-prohibited-gate screening
  (arXiv:2606.06253); Aouad, Lykouris & Zhong's polarization model as the "why early matters"
  account (arXiv:2605.11350, motivating color); Becker et al./METR (arXiv:2507.09089) as context
  that AI assistance is not an unqualified productivity win even for experts.

---

## Stage 3 — Related Work

**ROUND 1 [critic phase].**

*draft_v1* (proposer; the five-lane prose structure of `paper-draft.revised.md` §7, carried
over): Lane 1 causal premise + neighbors; Lane 2 behavioral signatures; Lane 3 JITAI; Lane 4
appropriate reliance / cognitive forcing; Lane 5 ITS lineage + the Agents-That-Teach foil.

*critique v1:*
- summary: "Lane coverage is right (it restores everything autodiscussion_draft_review.md §3.1
  says the failed package silently dropped), but v1 is positioning prose, not a Stage-3 object —
  no promoted paper carries the four-question comparison, so the foil claim and the novelty
  position are assertions."
- comments:
  1. `[major]` (anti-pattern: `missing_comparison`) — none of the specific-tier papers has a
     `comparison` (alignment → method_addresses → effectiveness → derived threat/gap). The cost
     is concrete on the foil: v1 asserts Agents-That-Teach is "open-loop," but discussion.md's
     own Stage-3 critic (b) warned "if 2607.06101 already proposes *adaptive* (state-conditioned)
     teaching behavior, the 'open-loop' boundary collapses — verify before building the intro
     around it," and mandated a fallback framing. Without a recorded threat level and
     pre-committed repositioning, this is an `unhandled_threat` waiting to fire at review time.
     Run the protocol for every promoted paper; record the Mehra fallback verbatim.
  2. `[minor]` — engagement tiers must be explicit per paper (full-read / abstract-read /
     search-confirmed-only): Cao & Huang is search-confirmed only (ACM DL 403,
     autodiscussion_draft_review.md §4 could not re-verify); the JITAI/forcing-function/ITS canon
     is well-known but carries page-detail verification debt. State this in the output, not just
     in a side note.
- decision: revise_and_recritique.

**ROUND 2 [critic phase].** *draft_v2*: full two-tier structure with comparisons (below);
engagement tier recorded per entry; Mehra threat + fallback recorded. *critique v2:* major 1
**resolved** (all five promoted papers carry complete, rule-consistent comparisons; the one
`verify_as_hypothesis` flag is deliberate); minor resolved. No new flags.
decision: move_to_refiner.

**REFINER PASS**: normalized `work_id`/`limitation_id` slugs (stable, referenced by Stage 4);
checked derivation consistency (no `proven_better`+`same` anywhere, so no high-threat entry;
Mehra = medium threat with recorded repositioning). declined_to_fix: none.

**CONFIRMED STAGE 3 OUTPUT**

- **summary**: Five lanes surround the gap without closing it: the causal premise (post-hoc
  measurement only), behavioral-signature detection (retrospective, cohort-level, or
  hardware-bound), JITAI (the closed-loop template, different sensors and outcomes), appropriate
  reliance/cognitive forcing (the intervention class, untargeted, decision-accuracy outcomes),
  and ITS/learner modeling plus design-principles responses (closed-loop, but inside purpose-built
  tutors; or open-loop by design). No prior work estimates erosive-pattern risk from a session
  prefix, and none closes the detect→intervene→verify loop on a skill-formation outcome.

- **general_related_works** (landscape tier):
  - `rw_cognitive_debt` — Kosmyna et al., "Your Brain on ChatGPT…", arXiv:2506.08872 (2025,
    preprint) [read]. EEG essay-writing study; LLM arm shows weakest connectivity, lowest
    ownership, reduced recall. Convergent direction in a different domain/instrument.
  - `rw_metr_productivity` — Becker et al., "Measuring the Impact of Early-2025 AI on Experienced
    Open-Source Developer Productivity", arXiv:2507.09089 (2025) [read]. Experienced maintainers
    *slowed* by AI tools; contextual counterweight to "AI is an unqualified win"; says nothing
    about learning or prefixes.
  - `rw_productivity_paradox` — Aouad, Lykouris & Zhong, "Human-AI Productivity Paradoxes…",
    arXiv:2605.11350 (2026) [read]. Theory: heterogeneous AI literacy compounds into skill
    polarization; supplies "why early matters"; purely simulated.
  - `rw_jitai_framework` — Nahum-Shani et al., "Just-in-Time Adaptive Interventions (JITAIs) in
    Mobile Health…", Annals of Behavioral Medicine 52(6), 2018 [canonical; page-detail debt].
    Decision points, tailoring variables, proximal/distal outcomes.
  - `rw_mrt` — Klasnja et al., "Microrandomized Trials: An Experimental Design for Developing
    Just-in-Time Adaptive Interventions", Health Psychology 34(S), 2015 [canonical; page-detail
    debt]. The timing-randomization design our scale-up inherits.
  - `rw_trust_automation` — Lee & See, "Trust in Automation: Designing for Appropriate
    Reliance", Human Factors 46(1), 2004 [canonical]. Why delegation is the default happy path.
  - `rw_knowledge_tracing` — Corbett & Anderson, "Knowledge Tracing: Modeling the Acquisition of
    Procedural Knowledge", UMUAI 4(4), 1995 [canonical]. The closed-loop learner-modeling
    ancestor; names the lineage to preempt "knowledge tracing, rediscovered."

- **specific_related_works** (promoted; four-question comparison each):

  1. `rw_skill_formation_rct` — Shen & Tamkin, "How AI Impacts Skill Formation",
     arXiv:2601.20245 (2026) [read in full]. I/O: complete session recordings + post-task quiz →
     causal effect of AI assistance on quiz score + six hindsight-coded patterns.
     *Comparison:* problem_alignment=**related** (theirs: does AI assistance impair skill
     formation; ours: is the drift detectable and intervenable before the quiz);
     method_addresses=**false** (post-hoc coding of complete transcripts cannot produce a
     prefix-time estimate — their pipeline needs the whole session); effectiveness=n/a;
     gap_type=**not_considered** (their framing never poses the within-session timing question;
     their stated future work is longitudinal dissipation); threat_to_motivation=**none** (they
     are the foundation we extend); role=**baseline** (arms, task, rubric are our comparability
     anchor). *Limitations:* `lim_hindsight_only` — patterns exist only as hindsight summaries of
     complete sessions; nothing is estimated at prefix time (evidence: their own method section;
     digest N4.1). `lim_fragile_base` — n=52, one lab, setup "differs from agentic coding
     products" by their own admission (evidence: their limitations; digest N4.1).
  2. `rw_scaffold_stays_on` — Yao, "When the Scaffold Stays On…", arXiv:2606.06253 (2026)
     [read]. I/O: platform submission histories across cohorts → cohort-level "AI-prompt
     signature" + screening value of AI-prohibited gates.
     *Comparison:* alignment=**related**; method_addresses=**false** (cross-cohort aggregate
     signature; no individual-session model, no prefix, no intervention; observational);
     effectiveness=n/a; gap_type=**not_solved** (shows the signal exists in behavior at scale but
     does not build the individual, prospective detector); threat=**low**;
     role=**related_for_context** — *the nearest neighbor for the detection half of our claim*.
     *Limitations:* `lim_cohort_retrospective` — signature is retrospective and cohort-level;
     never evaluated as an individual-session, prefix-time classifier, and no closed loop
     (evidence: abstract + design, digest N4.3).
  3. `rw_reliance_gaze` — Cao & Huang, PACMHCI 6(CSCW2), 2022 [search-confirmed ONLY; ACM DL
     403; full-text debt declared]. I/O: gaze telemetry during AI-assisted decisions → real-time
     reliance proxy.
     *Comparison:* alignment=**related** (real-time behavioral proxy, but decision-accuracy
     outcome, not skill formation); method_addresses=**false as-is** (requires eye-tracking
     hardware; different outcome); effectiveness=**untested** for our setting →
     `hypothesis_to_verify` (flagged, becomes the framing-tier RQ): **"Deterministic,
     zero-hardware query-log features alone retain at least 50% of the full two-tier feature
     set's relative Brier improvement over the prevalence-only predictor at the half-session
     checkpoint."** threat=**low**; role=**related_for_context**.
     *Limitations:* `lim_hardware_proxy` (verify_as_hypothesis: **true**) — the validated
     real-time proxy is hardware-grade gaze on a decision task; whether text-only features carry
     comparable signal for skill-formation risk is untested by anyone.
  4. `rw_agents_that_teach` — Mehra et al., "Agents That Teach: Towards Designing Incidental
     Learning Back into AI-Assisted Software Development", arXiv:2607.06101 (2026)
     [verified via arXiv API; abstract-read; full-text debt before submission]. I/O: design
     principles → assistants that scaffold incidental learning.
     *Comparison:* alignment=**related** (same harm, design-stance response);
     method_addresses=**false** (principles are prescribed open-loop — applied to all users,
     unconditioned on any measured state of the individual learner; the verified subtitle
     "Designing … Back into" confirms the design-stance reading); effectiveness=n/a;
     gap_type=**not_considered** (no measurement layer; cannot tell whether principles work
     mid-session); threat_to_motivation=**medium** — if erosion could be designed away open-loop,
     a detection loop would be unnecessary. *Repositioning (recorded):* open-loop scaffolding
     taxes users already in protective patterns (the 65–86% group needs no Socratic gate) and has
     no answer to whether it is working mid-session; **pre-committed fallback framing** if
     full-text reading shows their designs are adaptive: "we supply the measurement layer their
     adaptivity would require." role=**motivation_threat**.
     *Limitations:* `lim_open_loop` — intervention unconditioned on measured learner state; no
     mid-session verification.
  5. `rw_cognitive_forcing` — Buçinca, Malaya & Gajos, "To Trust or to Think: Cognitive Forcing
     Functions Can Reduce Overreliance on AI…", PACMHCI 5(CSCW1), 2021 [canonical, well-known;
     page-detail debt]. I/O: untargeted interruption/forcing interventions → decision accuracy
     under AI advice.
     *Comparison:* alignment=**related** (nearest intervention class with RCT evidence; different
     outcome — decision accuracy, not skill formation; untargeted); method_addresses=**partially**
     (a forcing function could be applied to our setting, but unconditionally, and nothing links
     it to skill formation); effectiveness=**untested** in our setting — but rather than a second
     framing RQ, their documented finding that effects come at a UX cost and partly through
     friction is taken as *design input*: it grounds the annoyance budget and the matched
     placebo. threat=**low**; role=**related_for_context**.
     *Limitations:* `lim_friction_untargeted` — effects partly run through interruption friction
     and apply to all users regardless of state; a triggered intervention must separate content
     from reactivity and budget its false-positive burden.

- **Nearest-neighbor honesty (one sentence, carried into the draft):** the closest prior work is
  Shen & Tamkin (we reuse their task, rubric, labels, and arms) and, for the detection claim
  specifically, Yao — neither estimates anything at prefix time, and no work in any lane closes
  the detect→intervene→verify loop on a skill-formation outcome.

---

## Stage 4 — Sub-Problems

**ROUND 1 [critic phase].**

*draft_v1* (proposer; `discussion.md` Stage 4 refined, five SPs): SP1 features without internals;
SP2 hindsight→prefix label transfer (hard part); SP3 non-destructive intervention; SP4
IRB/recruitment pipelined; SP5 baseline comparability.

*critique v1:*
- summary: "Four of five are real, distinct, method-free gaps; one is logistics, and the
  decomposition is missing the sub-problem that actually killed the previous package."
- comments:
  1. `[major]` field `sub_problems` (SP4) — "IRB & recruitment, pipelined" is an execution
     constraint, not a research sub-problem: it has no `technical_challenge` distinct from
     project management, and no method could "solve" it. It belongs in Stage 6's protocol
     (milestones, budget, over-recruitment arithmetic), where discussion.md's own Stage-6 critic
     (b, c) already placed its content. Meanwhile the decomposition *omits* the gap
     autodiscussion_draft_review.md §5 identified as fatal in the prior package: "the offline
     stage is statistically infeasible as split … the gate is near-unpassable **by
     construction**" — i.e., *making a small-n go/no-go authorization decision trustworthy* is a
     genuine, hard, distinct sub-problem (exact bounds, sealing, prevalence-anchoring, alert-count
     minimums), and no stage-3 lane provides it. Swap SP4 for it.
  2. `[minor]` — SP5's `why_it_is_a_problem` conflates materials fidelity with data fidelity;
     keep discussion.md's split (essential vs. accelerant) explicit.
- decision: revise_and_recritique.

**ROUND 2 [critic phase].** *draft_v2*: SP4 replaced by the small-n authorization sub-problem
(marked `["__novel__"]` with justification); IRB content moved to Stage 6; SP5 split clarified.
*critique v2:* major 1 **resolved** (the new SP is defensibly `__novel__`: none of the five lanes
supplies an ethically-motivated statistical authorization procedure at this n; the JITAI lane has
trial designs but no sealed small-sample gate); minor resolved. decision: move_to_refiner.

**REFINER PASS**: field-role check (description / why-a-gap / why-hard distinct per SP);
limitation links verified against Stage 3 ids. declined_to_fix: none.

**CONFIRMED STAGE 4 OUTPUT**

- **summary**: Five obstacles stand between the published hindsight fact and a verified closed
  loop: labels live at session end but decisions must be made at prefix time; the only
  deployable sensors are thin text-log features; a triggered intervention can "work" for the
  wrong reasons; the go/no-go decision must be trustworthy at tens of sessions; and every claim
  must remain comparable to a fragile published baseline.

1. `sp_prefix_transfer` — **Hindsight-to-prefix label transfer (the hard part).**
   description: ground truth is a session-level label assigned in hindsight; the study must
   estimate, at query k, the risk that the session *terminates* erosive — and establish how early
   that is knowable at all, and with how much of the session still ahead.
   why_it_is_a_problem: every existing label in every lane is terminal (`lim_hindsight_only`,
   `lim_cohort_retrospective`); no prior work defines or bounds a prefix-time target.
   technical_challenge: label-noise-by-construction — a learner can drift or self-correct, so the
   terminal label was not "already true" early; this bounds achievable prefix precision from
   above by an unknown ceiling, entangles detection quality with detection *timing*, and makes
   naive prefix training against terminal labels systematically optimistic.
   source_limitation_ids: [lim_hindsight_only, lim_cohort_retrospective]
2. `sp_thin_signal` — **Signal sufficiency of zero-hardware features.**
   description: determine whether features a logging proxy can compute (no model internals, no
   biometrics) carry enough signal for prefix-time risk estimation.
   why_it_is_a_problem: the validated real-time proxy is hardware gaze on a decision task
   (`lim_hardware_proxy`); the taxonomy being predicted was built from rich qualitative reading
   of full transcripts — nobody has shown text-log features suffice.
   technical_challenge: the informative behaviors (comprehension-seeking vs. delegation) are
   partly semantic; deterministic log features may miss them, while LLM-tagged intent features
   reintroduce an unvalidated instrument that must itself be audited — the sufficiency question
   has to be answered by ablation, not assumption.
   source_limitation_ids: [lim_hardware_proxy, lim_cohort_retrospective]
3. `sp_wrong_reason` — **Interventions that work for the wrong reason.**
   description: ensure an observed intervention benefit is attributable to nudge *content* acting
   on an ongoing session, not to interruption reactivity or to degrading the assistant.
   why_it_is_a_problem: the nearest intervention class's effects partly run through friction and
   are untargeted (`lim_friction_untargeted`); an intervention that suppresses AI use merely
   re-derives the hand-coding arm and answers nothing new.
   technical_challenge: reactivity and content are confounded in any single treated arm; a fired
   nudge also changes the subsequent feature stream (the loop is non-stationary), and withholding
   designs destroy the task-completion parity the comparison needs.
   source_limitation_ids: [lim_friction_untargeted]
4. `sp_small_n_gate` — **Trustworthy small-sample authorization.**
   description: construct a go/no-go rule that decides, from tens of sessions, whether the
   detector is good enough to justify intervening on live participants — and that cannot be
   gamed by post-hoc threshold or cutoff choice.
   why_it_is_a_problem: intervening on humans on the strength of a noisy point estimate is an
   ethical and scientific failure; the prior package's fixed-constant gate was "near-unpassable
   by construction" while its development split starved the model — both directions of
   miscalibration are fatal.
   technical_challenge: at n ≈ 20–30 gate sessions, only exact small-sample bounds are honest;
   the criterion must be anchored to measured prevalence (not an arbitrary constant), balance
   miss cost against an explicit false-positive annoyance budget, and be frozen — model, cutoff,
   pass table — before the sealed data is touched exactly once.
   source_limitation_ids: ["__novel__"] (justification: no lane supplies a sealed, exact,
   prevalence-anchored authorization procedure at this n; nearest analogue — JITAI/MRT — designs
   the trial, not the evidence bar for opening it.)
5. `sp_comparability` — **Comparability to a fragile published baseline.**
   description: keep the study directly comparable to the published 50%/67% instrument
   (materials fidelity: task + rubric — essential) while re-testing the base effect itself
   (internal replication), with base transcripts as an accelerant only, never a dependency.
   why_it_is_a_problem: the headline selling point is direct numeric comparability; the base
   effect rests on n=52 in one lab (`lim_fragile_base`), so a design that *assumes* it invites
   collapse, and one that cannot re-test it forfeits the comparison.
   technical_challenge: replication and extension compete for the same budget; a replication
   failure must be pre-registered as interpretable (what happens to the intervention contrasts)
   rather than fatal; every materials deviation must be documented because each one erodes
   comparability by an unknown amount.
   source_limitation_ids: [lim_fragile_base]

- Coverage check: solving 1–5 jointly delivers Stage 1's five outputs (risk curves + ceiling ←
  1,2; gate ← 4; causal estimates + replication ← 3,5; lag ← 1). No orphan outputs, no orphan
  sub-problems.

---

## Stage 5 — Method Design

**ROUND 1 [critic phase].**

*draft_v1* (proposer; `discussion.md` Stage 5 M1–M6 with its locked amendments): M1 classifier
(elastic-net/GBT, LOPO-CV, calibrated, prefix k ∈ {1,3,5,10}); M2 validation harness + human
ceiling; M3 detection-lag instrumentation at the half-session landmark; M4 additive nudge
(template-bank); M5 placebo (scale-up arm); M6 threshold procedure with "precision ≥ 70%
(placeholder pending base-rate analysis)" and CI-based gating; power sketch (~30/arm pilot,
three-arm).

*critique v1:*
- summary: "The module set is right but three design decisions repeat exactly the failures the
  package review documented; and the hypotheses are not yet stated with the seven-slot
  discipline Stage 6 needs."
- comments:
  1. `[major]` (M6) — v1 still carries τ=0.70 as the operative number with the base-rate analysis
     deferred. autodiscussion_draft_review.md §3.4 flagged precisely this ("τ=0.70 hard-coded …
     with no base-rate derivation") and §5 showed a fixed-constant CP bound at gate-set n is
     "near-unpassable by construction." discussion.md's own M6 rule — "the ≥70% number survives
     only if the base-rate math endorses it" — must be promoted into the criterion itself: gate
     on a **prevalence-anchored** margin (LB ≥ prevalence + 0.10) with a minimum alert count and
     the annoyance budget, τ=0.70 demoted to a design target.
  2. `[major]` (M3/M5, two halves of one propagation failure) — (a) v1 evaluates and triggers at
     a single half-session landmark; the review (§3.5) calls this "'catching the drift' degraded
     to one checkpoint" and the seed's title bet requires a *per-query* first-crossing trigger
     (floor k ≥ 3, at most one nudge/session) plus a detection-lag endpoint. (b) v1 keeps the
     placebo as a scale-up-only arm, but the review's MAJOR #2 fix and paper-draft.revised.md
     both restore a **concurrent** placebo arm — without it, the pilot cannot separate content
     from reactivity at all (digest t2: pilot claims capped at "an effect exists"), yet the
     pilot's primary contrast is exactly the one the placebo defines. Restore the four-arm
     structure as the method's own control logic (arm arithmetic is Stage 6's).
  3. `[minor]` — hypotheses in v1 are directional prose ("classifier beats majority baseline");
     restate each with metric, bound, and test population so Stage 6 can copy them verbatim.
- decision: revise_and_recritique.

**ROUND 2 [critic phase].** *draft_v2*: M6 rebuilt decision-analytic and prevalence-anchored;
M3 rebuilt as per-query first-crossing trigger with pre-notification risk freezing; M5 promoted
to a concurrent matched placebo; four-arm internal-replication logic made explicit (m_arms);
hypotheses H1–H7 stated with bounds. *critique v2:* majors 1–2 **resolved**; minor resolved. One
residual note (not a flag): H4's 40%-remaining floor and H6's 40%-of-gap floor are authored
design targets — rationales must appear in Stage 6, per the "author design parameters, don't
fabricate facts" rule. decision: move_to_refiner.

**REFINER PASS**: unified notation with Stage 1's formal summary (r_ik, c, G, arms H/U/P/N);
verified every module targets a Stage-4 sp id; hypothesis wording frozen (Stage 6 must copy
verbatim). declined_to_fix: none.

**CONFIRMED STAGE 5 OUTPUT**

- **summary**: One measurement-then-intervention pipeline with six cooperating parts: a
  prefix-only prognostic risk model turns query streams into calibrated erosive-terminal risk; a
  dual-purpose annotation harness supplies hindsight labels and the human prefix ceiling; a
  per-query first-crossing trigger converts risk into at most one timed, logged alert per
  session; a sealed decision-analytic gate converts small-sample alert precision into an
  auditable authorization decision; an additive comprehension nudge with a matched placebo makes
  the intervention's mechanism attributable; and a four-arm assignment scheme keeps the published
  baseline internally re-tested.

1. `m_risk` — **Prefix-only prognostic risk model** (targets sp_prefix_transfer, sp_thin_signal).
   proposed_approach: cumulative two-tier features at each prefix — tier 1 deterministic (query
   count/length, inter-query gaps, elapsed time, code-block presence, code-paste→error-paste
   cycles, follow-up-after-code presence, user-authored diagnostic detail), tier 2 LLM-tagged
   query intents (complete-solution / explanation-or-testing / hybrid / conceptual; frozen
   prompt, 15% human audit, κ ≥ 0.75 acceptance) — feeding a session-weighted elastic-net
   logistic landmark model with Platt calibration producing r_ik after every query; sessions
   contribute equal total weight across prefixes; hyperparameters and calibration by nested
   leave-one-developer-out cross-fitting; no deep models at this n; cutoff c selected on
   fold-train data only.
   key_insight: reframing the target as *terminal-pattern risk* makes early indeterminacy
   probability mass rather than label noise — a calibrated small model can honestly say 0.55 —
   and the landmark structure yields a per-query estimate with no future leakage by construction.
   hypotheses:
   - **H1**: "At a prefix length no greater than half the median session length, the
     cluster-bootstrap one-sided 90% lower confidence bound on the risk model's alert precision
     for erosive-terminal sessions, under nested leave-one-developer-out cross-fitting, exceeds
     the development-set erosive-label prevalence by at least 0.10."
   - **H2**: "At each locked elapsed-time checkpoint (10, 20, and 30 minutes), the risk model's
     session-weighted Brier score improves on the fold-train prevalence-only predictor by a
     relative margin whose cluster-bootstrap one-sided 90% lower bound exceeds 0.10,
     Holm-adjusted across the three checkpoints."
2. `m_ceiling` — **Hindsight-label and human prefix-ceiling harness** (targets
   sp_prefix_transfer).
   proposed_approach: two annotators code all complete sessions with the published six-pattern
   protocol (erosive/protective binary primary; κ ≥ 0.7 required; disputes adjudicated; six-way
   kept descriptive); separately, the same protocol's annotators label a 30-session subset of
   *prefixes* at k ∈ {1,3,5,10}, blind to session endings; agreement of blind prefix labels with
   terminal labels is the human prefix ceiling, reported per k. A prefix-time validity check
   verifies flagged-at-k sessions differ in *subsequent* behavior (post-k feature trajectories),
   so flags are prognostic rather than prefix-quirk correlates.
   key_insight: the ceiling is simultaneously the honest denominator for any classifier, a
   standalone scientific quantity (how early are these patterns visible at all?), and the
   cheapest possible de-risking of the gate — if humans cannot call the pattern from half a
   session, no classifier can.
   hypotheses:
   - **H3**: "At a prefix length no greater than half the median session length, human
     annotators labeling prefixes blind to session endings identify erosive-terminal sessions
     with precision exceeding the erosive-label prevalence by at least 0.10."
3. `m_trigger` — **Per-query first-crossing trigger and detection-lag instrumentation** (targets
   sp_prefix_transfer).
   proposed_approach: r_ik is recomputed after every query; the alert is the *first crossing* of
   the frozen cutoff c after a floor of 3 queries; at most one alert per session; the risk value
   and feature snapshot are frozen and logged *before* any message is delivered (so flagged
   subgroups are defined pre-treatment in every arm); detection lag is recorded as query index,
   wall-clock, and fraction of the session's eventual query count remaining.
   key_insight: a single fixed checkpoint answers "is the signal there by minute 30" but not
   "how much session is left when it appears" — the lag distribution is the quantity that makes
   just-in-time intervention possible or impossible, so the trigger must be event-driven, and
   pre-notification freezing is what keeps the flagged-subgroup analysis causal.
   hypotheses:
   - **H4**: "Among gate-set sessions correctly alerted under the frozen cutoff, the median
     first alert fires with at least 40% of the session's eventual query count still ahead."
4. `m_gate` — **Decision-analytic sealed authorization gate** (targets sp_small_n_gate).
   proposed_approach: after development analyses close, one final model-and-cutoff pair is fitted
   on all development sessions and frozen — serialized and hashed with the feature specification,
   exclusion rules, and a fully enumerated (alerts, true-positives) pass table; a
   developer-disjoint sealed gate set (≥ 20 sessions, untouched during development) is scored
   exactly once at the half-session checkpoint; authorization requires (i) one-sided 90%
   Clopper–Pearson lower bound on alert precision ≥ development prevalence + 0.10, (ii) ≥ 5
   alerted sessions, (iii) false-positive burden ≤ 0.3 alerts per protective-terminal session
   (the annoyance budget); zero alerts is a pre-registered no-go; τ = 0.70 is retained only as a
   design *target*, kept iff the observed base rate endorses it; one re-gate is permitted after
   a pre-registered narrowing (delegation-pattern-only detection); a second failure retires the
   real-time premise as scoped.
   key_insight: at this n only exact binomial bounds are honest, and anchoring the bar to
   measured prevalence rather than a fixed constant is what makes the gate simultaneously
   passable by a genuinely useful detector and unpassable by a lucky one; sealing plus the
   enumerated pass table removes every degree of post-hoc freedom.
   hypotheses:
   - **H5**: "The frozen model–cutoff pair passes the sealed gate: on a developer-disjoint gate
     set of at least 20 sessions scored exactly once at the half-session checkpoint, the
     one-sided 90% Clopper–Pearson lower bound on alert precision exceeds the development-set
     erosive-label prevalence by at least 0.10, with at least 5 alerted sessions and a
     false-positive burden of at most 0.3 alerts per protective-terminal session."
5. `m_nudge` — **Additive comprehension nudge with matched placebo** (targets sp_wrong_reason).
   proposed_approach: on trigger, the assistant answers exactly as it otherwise would, then
   appends one targeted comprehension question keyed to the just-delivered code, instantiated by
   an LLM from a vetted template bank with a deterministic template fallback; nothing is ever
   withheld; one nudge per session (caps loop non-stationarity); 100% of pilot firings audited
   for relevance and timing (intervention-integrity metrics). The placebo arm fires under the
   identical trigger policy with matched timing, length, and presentation but content-free text.
   Pre-registered guardrails: task-completion rate and time-on-task in the active arm within 10%
   of the unnotified arm.
   key_insight: with trigger policy, timing, and presentation matched, the placebo contrast
   isolates exactly one difference — whether the appended content does cognitive work — so a
   surviving effect is attributable to content acting on an ongoing session, not to interruption
   reactivity, and the additive-only rule ensures the intervention cannot "work" by re-deriving
   the hand-coding arm.
   hypotheses:
   - **H6**: "In the live trial, the active-nudge arm's mean quiz score exceeds the placebo
     arm's, with a point estimate of at least 40% of the internally replicated hand-vs-AI gap,
     while task-completion rate and median time-on-task in the active arm remain within 10% of
     the unnotified-AI arm."
6. `m_arms` — **Internally replicated four-arm assignment** (targets sp_comparability).
   proposed_approach: participants are randomized, stratified by screening-quiz score, to
   hand-code (H), unnotified AI (U), placebo-trigger (P), or active-nudge (N); the frozen
   classifier runs silently in all three AI arms; quiz grading uses the original rubric with two
   arm-blinded graders (κ reported); analysis is ANCOVA with baseline covariates (experience,
   screening score), multiple imputation (50 datasets, Rubin's rules) and delta-adjusted MNAR
   tipping-point sensitivity; the interpretation tree is pre-registered — if the U-vs-H contrast
   fails to replicate directionally, all intervention contrasts are reported as estimation-only
   and the replication failure is itself a headline finding.
   key_insight: carrying the published RCT's own two arms inside the trial converts the base
   effect's fragility from an inherited assumption into a measured result, and the pre-registered
   tree makes a replication failure informative rather than fatal.
   hypotheses:
   - **H7**: "In the live trial, the unnotified-AI arm's mean quiz score is lower than the
     hand-code arm's — directionally replicating the published 17-point gap — with a one-sided
     test significant at α = 0.05."

---

## Stage 6 — Experiment Design

**ROUND 1 [critic phase].**

*draft_v1* (proposer; `discussion.md` Stage 6 refined phases + the prior package's offline
parameters): offline split 20 development / 32 gate sessions; three-arm live pilot n=90 (placebo
deferred to scale-up); RQ list including "RQ-D: does the classifier beat the majority baseline"
framed as a beats-baseline comparison; milestones as in discussion.md.

*critique v1:*
- summary: "The phase/gate calendar is sound, but the draft re-imports the exact parameterization
  the package review proved infeasible, drops an arm the method design now requires, and carries
  a tier violation."
- comments:
  1. `[major]` field `datasets`/`sample_size_rationale` — the 20/32 split is the review's
     inferred unresolved MAJOR #1 verbatim: "20 development sessions (~10 erosive) must support
     nested LODO cross-fitting, cutoff selection, and 9,999 pipeline-rerunning bootstrap
     replicates … unreachable at this n except by luck," while the fixed gate bound needs
     "~90–100% observed precision on 32 sessions." Rebalance to development ≥ 40 / gate ≥ 20
     (developer-disjoint), which requires the dual-source plan with the fresh-collection
     fallback *sized to make the split feasible even if the DUA fails* (extend fresh collection
     to ~60 sessions in that branch; budget the difference), with the DUA answer deadline
     (2026-09-15) and auto-start pre-registered.
  2. `[major]` field `baselines`/`research_questions` — (a) three-arm pilot contradicts
     confirmed m_nudge/m_arms (H6 is defined *against the placebo arm*; a three-arm pilot cannot
     test it) — the live design is four concurrent arms, n=120 (30/arm), 144 recruited (20%
     over-recruitment), exactly the review's fix #2; (b) `tier_violation`: "does the classifier
     beat the majority baseline" is outcome-tier framing, forbidden under `study_type:
     empirical` — the same content belongs inside the mechanism-tier detection RQ as an
     *enrichment-over-prevalence attribute* of the instrument, with the prevalence predictor as
     a sanity reference, not a competitor.
  3. `[minor]` — IRB/DUA milestones, budget arithmetic, and failure products exist in
     discussion.md but v1 scatters them; consolidate into the protocol section so the spec is
     runnable stand-alone (the review's §3.6 "IRB/timeline realism: absent" must not recur).
- decision: revise_and_recritique.

**ROUND 2 [critic phase].** *draft_v2*: dual-source data plan with rebalanced ≥40/≥20 split and
sized fallback; four-arm live design restored with recruitment arithmetic; RQ set rebuilt — 8
RQs, 7 mechanism + 1 framing, 0 outcome; every `target_hypotheses` a verbatim copy of H1–H7 or
the flagged `rw_reliance_gaze` hypothesis; ethics/timeline consolidated. *critique v2:* majors
1–2 **resolved**; minor resolved; tier audit clean (zero outcome-tier RQs; prevalence predictor
and arms described as controls/sanity references throughout). decision: move_to_refiner.

**REFINER PASS**: traceability table RQ ↔ hypothesis ↔ method ↔ sub-problem completed (below);
no new datasets/baselines/RQs added. declined_to_fix: none.

**CONFIRMED STAGE 6 OUTPUT** — rendered in full as the standalone spec
`discussion/experiment_design.md` (datasets, baselines-as-controls, 8 RQ sections with setup /
sample-size rationale / statistical test / expected outcome / falsification condition / metrics,
the ethics-IRB-timeline protocol, and failure products). Summary here:

- datasets: Source A (base RCT's 52 transcripts under DUA; pursued, never depended on; answer
  deadline 2026-09-15); Source B (fresh 40–50-session transcript collection, auto-starts
  2026-09-16, extends to ~60 sessions if the DUA fails outright, sized so development ≥ 40 and
  sealed gate ≥ 20 developer-disjoint sessions hold in every branch); live four-arm pilot
  dataset (n = 120, 30/arm; 144 recruited; Prolific/Upwork with screening traps).
- baselines (controls and references, not competitors): fold-train prevalence-only predictor;
  human prefix ceiling; hand-code arm; unnotified-AI arm; placebo-trigger arm.
- research_questions: RQ1 ceiling (mechanism, H3); RQ2 detection precision (mechanism, H1);
  RQ3 probabilistic prognosis (mechanism, H2); RQ4 feature-thinness (framing, the flagged
  rw_reliance_gaze hypothesis); RQ5 sealed gate (mechanism, H5); RQ6 detection lead time
  (mechanism, H4); RQ7 internal replication (mechanism, H7); RQ8 placebo-controlled intervention
  effect (mechanism, H6). Zero outcome-tier RQs (`study_type: empirical`).
- protocol anchors: transcript-collection IRB submitted immediately; live-RCT IRB submitted
  2026-11-15 (expedited review assumed 2–3 months; pilot start Feb 2027); freeze-and-hash + OSF
  pre-registration before the first live participant; G0 (labels, κ) 2026-10-31; G1 (gate)
  2027-01-15 with one re-gate absorbing to 2027-03-01; pilot Feb–May 2027; G2 (replication +
  guardrails) 2027-05-31; scale-up Jun–Aug 2027; CHI 2028 submission Sep 2027 (CSCW/AIES
  fallbacks); FAccT 2027 position form (2026-11-03) data-free by design. Budget $35–50k + 6–8
  person-months. Failure products pre-committed (ceiling study; replication report).

---

## Cross-stage consistency check (final, literal recount)

- **Hypothesis count:** Stage 5 declares exactly **7** hypotheses (H1, H2 on m_risk; H3 on
  m_ceiling; H4 on m_trigger; H5 on m_gate; H6 on m_nudge; H7 on m_arms). Stage 3 flags exactly
  **1** limitation `verify_as_hypothesis: true` (`lim_hardware_proxy`, with a written
  `hypothesis_to_verify`). Total testable claims: **8**.
- **RQ count:** Stage 6 declares exactly **8** RQs — 7 mechanism-tier + 1 framing-tier.
  Mapping (verbatim-match verified by string comparison, not paraphrase):
  RQ1→H3, RQ2→H1, RQ3→H2, RQ4→rw_reliance_gaze.hypothesis_to_verify, RQ5→H5, RQ6→H4, RQ7→H7,
  RQ8→H6. **No uncovered hypothesis; no RQ without a source; no paraphrased target.**
- **Tier gating:** `study_type: empirical` (Stage 1) → outcome-tier RQs required to be zero;
  actual outcome-tier count: **0**. Prevalence predictor, ceiling, and arms are framed as
  controls/references throughout. PASS.
- **ID integrity:** every `source_limitation_ids` in Stage 4 resolves to a Stage-3
  `limitation_id` or the `__novel__` sentinel (sp_small_n_gate only, justified); every
  `target_sub_problem_id` in Stage 5 resolves to a Stage-4 sp id; sub-problem coverage: each of
  the 5 sps is targeted by ≥1 method (sp_prefix_transfer ← m_risk, m_ceiling, m_trigger;
  sp_thin_signal ← m_risk; sp_wrong_reason ← m_nudge; sp_small_n_gate ← m_gate;
  sp_comparability ← m_arms). No orphan methods, no uncovered sub-problems.
- **Output-chain check:** Stage 1's five outputs each reach Stage 6: risk curves → RQ2/RQ3;
  ceiling → RQ1; gate decision → RQ5; causal estimates + replication → RQ7/RQ8; lag → RQ6.
  Nothing lost along the chain.
- **Known open majors:** none (no stage closed over an open `[major]`; the cap was never hit).
- **Carried [VERIFY] debts (explicit, non-blocking for a pre-registration draft, blocking for
  submission):** Cao & Huang full text (ACM DL 403); Mehra et al. full text (abstract-read;
  fallback framing pre-committed); page-detail verification for the JITAI/MRT/forcing-function/
  knowledge-tracing canon.

## Post-review revision round (2026-08-15)

After assembly, `pengsida-stage-reviewer` fired REVISE findings against the first assembled
`paper_draft.md` (see `stage_review.md`); the fixes were applied to `paper_draft.md`/`.tex` and
recompiled. No hypothesis wording, no gate criterion, and no pre-registered bound was touched in
that pass — the fixes are positioning/writing-layer only, as recorded there.
