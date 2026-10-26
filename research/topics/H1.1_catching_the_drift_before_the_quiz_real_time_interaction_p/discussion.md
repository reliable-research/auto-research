# Discussion: H1.1 — Catching the Drift Before the Quiz: Real-Time Interaction-Pattern Classification as a Just-in-Time Intervention Against AI-Induced Skill Erosion (技能侵蚀的实时预警与即时干预)

> Structured 6-stage research discussion (auto-research-discussion style). Each stage is
> drafted, then attacked by an internal critic, then refined. Source: `README.md` +
> `digest.md` (a full reverse N0-N12 with verified grounding, dated 2026-08-13 — this
> document does NOT redo that work; it converts it into discussion form and adds the
> operational detail the digest deliberately left as placeholders). Audit context:
> KEEP-TOP, human-axis (family H1, orthogonal to the repo's B/T system-trust axis);
> venue clock: CHI/CSCW/AIES — cannot hit Sep/Oct 2026 ML windows; FAccT 2027 (deadline
> Nov 3, 2026) is the position-form's window; the experimental form targets CHI 2028 /
> CSCW timelines. Date of this discussion: 2026-08-13.

---

## Stage 1 — Problem Definition

**Draft.** Shen & Tamkin's RCT ([SkillFormationRCT, arXiv:2601.20245], read in full)
established the causal fact: 52 developers (1+ yr Python, new to the Trio library),
AI-assisted arm scores 50% vs. 67% for hand-coders on a post-task concept/debugging quiz
(d=0.738, p=0.01), with six interaction patterns identified by post-hoc qualitative
coding — three erosive patterns (<40%: full AI delegation, progressive reliance,
iterative AI debugging) and three protective ones (65-86%: generate-then-ask,
code+explanation hybrid queries, purely conceptual questions). All measurement happens
*after* the session, in a quiz. H1.1's question, in two halves [GIVEN]:

- **RQ1 (detection):** Can a classifier trained ONLY on session-observable query-stream
  features (no model internals, no biometrics) recognize the early behavioral signature
  of an erosive pattern from a *partial session prefix* — early enough that most of the
  session is still ahead?
- **RQ2 (intervention):** Does a just-in-time nudge triggered by that detection (e.g.,
  the assistant appends a comprehension probe instead of only returning runnable code)
  causally improve the downstream quiz outcome vs. unintervened AI assistance, in a
  three-arm RCT directly comparable to the published 50%/67% baseline?

This is explicitly NOT a re-measurement of "does AI harm skill formation" (settled by
the base paper); it is "can the drift be caught in the behavior stream before the quiz,
and does catching it help." Outcome shape: a precision-at-prefix-length curve (RQ1), a
detection-lag distribution, and a three-arm quiz-score comparison plotted against the
base paper's own numbers (RQ2).

**Critic:** (a) The draft treats "pattern" as if it were a stable latent state a prefix
reveals, but the base paper's taxonomy is a *hindsight summary of a whole session* — a
learner may genuinely be pattern-indeterminate at query 3, in which case "early
detection" is not merely hard but partially ill-posed. The problem statement must define
what the classifier is estimating: not "which of six patterns is this," but "risk that
this session, if uninterrupted, terminates in an erosive pattern" — a prognostic risk
score, not a diagnostic label. (b) Two halves, one paper, is a compound bet: RQ2 is
uninterpretable if RQ1 is weak, and the digest already encodes this as a hard gate
(precision ≥70% at ≤half-session, offline, BEFORE any live arm). The problem definition
should carry the gate, not bury it in methods. (c) "Directly comparable to 50%/67%"
requires replicating the base arms too — the problem definition should own that the
three-arm study internally replicates the two-arm result as a validity precondition.

**Refined:** The problem is defined as a **gated, two-stage causal extension of a
published RCT**. Stage 1 (offline, no human subjects beyond transcript collection):
learn a *prognostic risk score* r(prefix) = P(session terminates in an erosive pattern |
first k queries), evaluated as precision/recall at prefix lengths k ∈ {1,3,5,10} against
hindsight labels produced by the base paper's own coding protocol. **Hard gate:**
precision ≥70% (placeholder pending base-rate analysis — see Stage 5 threshold
procedure) for flagging erosive-terminal sessions at a prefix no longer than half the
median session, beating the always-predict-majority baseline with statistical margin.
Stage 2 (live, only if gated through): three-arm RCT — hand-code / AI-assist /
classify+intervene — on the same task+quiz instrument, where the internal AI-vs-hand
contrast must replicate the base gap directionally before the third-arm contrast is
interpreted. Primary endpoint: quiz score, classify+intervene vs. AI-assist. Secondary:
detection lag; exploratory: lag × benefit. The compound bet is thereby serialized: a
gate failure yields a publishable negative/characterization paper (CO1 alone), not a
dead study.

---

## Stage 2 — Motivation

**Draft.** Why this, why now:

- **The causal premise is fresh, strong, and singular.** [SkillFormationRCT] (Jan 2026,
  Anthropic) is the first clean RCT showing AI assistance impairs skill formation, and
  it *names the lever*: interaction patterns, not AI use per se, predict who learns
  (<40% vs. 65-86% by pattern). A pattern that predicts the outcome and is visible in
  behavior is an invitation to detect-and-intervene. The paper itself stops at hindsight
  characterization; the real-time question is stated by its framing but not attempted.
- **Independent corroboration exists but is thin — two studies, not three.** The
  digest's freshness check caught the industry-scan miscount: two YouTube channels were
  narrating the SAME paper. The corrected base: [SkillFormationRCT] (coding, quiz) +
  [CognitiveDebt, Kosmyna et al., 2506.08872] (essay writing, EEG, preprint — weakest
  link, not peer-reviewed [VERIFY peer-review status before citing as more than
  convergent direction]). Direction converges across instrument/domain/population.
- **The behavioral-signature bet has an existence proof.** [ScaffoldStaysOn, Yao,
  2606.06253]: an "AI-prompt signature" (high first-attempt acceptance, few debug
  retries) is detectable in naturalistic platform data — but observational, cohort-level,
  retrospective, no closed loop. [RelianceGaze, Cao & Huang, CSCW2 2022]: real-time
  behavioral proxy (gaze) beats retrospective self-report for reliance — but different
  signal, different outcome, and search-confirmed only [VERIFY — full text not yet read;
  ACM DL returned 403; must obtain before submission].
- **Theory says early is when it matters.** [ProductivityParadox, Aouad et al.,
  2605.11350]: heterogeneous AI literacy → skill polarization via compounding — if the
  compounding runs through early interaction differences, early intervention is exactly
  the lever the model predicts (digest's inference, not the papers' claim — motivating
  color only).
- **Nobody owns the closed loop.** Detection exists (retrospective), harm exists
  (post-hoc), interventions exist (untargeted pedagogy). The detect→intervene→outcome
  loop on skill formation is unclaimed. The window is real: the base paper is seven
  months old; tooling vendors are shipping "learning modes" [VERIFY — product-level
  claim, confirm examples before using in a paper] without any detection component.
- **Why us / why this repo:** the repo's 40 existing topics all study whether the AI
  system is trustworthy; H1.1 opens the orthogonal human axis (what long-term reliance
  does to the human), which is where CHI/CSCW/FAccT live.

**Critic:** (a) The motivation over-relies on the base paper being replicable; n=52,
single task, single lab — if the 17-point gap is fragile, the whole edifice inherits
that fragility, and the motivation should claim the *replication itself* as a
contribution, not a cost. (b) Two [VERIFY]s (Kosmyna peer-review status; "learning
modes" products) plus one weakly-grounded anchor (Cao & Huang) sit in the motivation;
FAccT/CHI reviewers punish sloppy sourcing on exactly this kind of AI-harms claim.
(c) The "nobody owns the closed loop" priority claim has only been checked against five
papers — the JITAI literature (mobile health) has run detect→intervene loops for a
decade; the novelty is the *domain* (skill formation in AI-assisted work) and the
*sensor* (query streams), not the loop concept. Overclaiming the loop invites a
one-line rejection from anyone who knows mHealth.
(d) "Why now" for the FAccT position form is different from "why now" for the CHI
experiment — the position paper's urgency is normative (products optimize for
delegation; erosion is invisible to the user at decision time), and the draft doesn't
articulate it.

**Refined:** Motivation restructured on four legs, each with its epistemic status:
(1) *Causal premise* [GROUNDED: read]: pattern→outcome link from the base RCT; our
three-arm design internally replicates it, so the premise is re-tested, not assumed —
fragility becomes a measured result either way. (2) *Feasibility precedents*
[GROUNDED: read / search-only flagged]: Yao for signal-in-behavior; Cao & Huang for
real-time-proxy-beats-retrospection (upgrade to full read before any submission
[VERIFY]); JITAI literature for the loop template — explicitly credited so our novelty
claim is scoped: *first closed JITAI-style loop where the sensed state is an
AI-interaction pattern and the outcome is skill formation, with a published RCT as the
comparable baseline*. (3) *Normative urgency* (FAccT form): skill erosion is a harm
invisible at decision time to the person incurring it, produced by products optimized
for exactly the erosive patterns (delegation is the product's happy path); post-hoc
measurement structurally favors the vendor; real-time detection is an accountability
instrument. All product-level claims [VERIFY] before use. (4) *Timing*: base paper is
7 months old and its authors listed the open question; the offline stage needs no IRB
beyond secondary-data/transcript collection, so a first-mover result is achievable
within the FAccT clock even while the live RCT waits for CHI 2028 timelines.

---

## Stage 3 — Related Work

**Draft.** Three lanes:

**Lane 1 — the grounding five (all named, boundaries per digest N3/N4):**
- **[SkillFormationRCT, Shen & Tamkin, arXiv:2601.20245]** [read in full]: the base
  RCT, taxonomy source, quiz instrument, 50%/67% baseline. Boundary: post-hoc coding of
  complete transcripts; never real-time; own future work is longitudinal dissipation,
  not within-session detection; setup "differs from agentic coding products" (its own
  caveat — our results inherit it as a likely lower bound).
- **[CognitiveDebt, Kosmyna et al., arXiv:2506.08872]** [read]: EEG, essays, 54
  participants; weakest connectivity + lowest ownership in LLM arm. Boundary: preprint,
  one LLM, different domain — corroborates direction only, never coding-domain evidence.
- **[ScaffoldStaysOn, Yao, arXiv:2606.06253]** [read]: AI-prompt signature in
  competitive-programming submissions; AI-prohibited gates screen for durable skill.
  Boundary: aggregate, cross-cohort, observational; no individual-session classifier, no
  intervention; its "gates matter more than prohibition" conclusion is the institutional
  cousin of our individual-level nudge.
- **[ProductivityParadox, Aouad, Lykouris & Zhong, arXiv:2605.11350]** [read]: theory of
  skill polarization under heterogeneous AI literacy. Boundary: purely
  simulated; supplies the "why early matters" account, no empirical or mechanism
  content usable directly.
- **[RelianceGaze, Cao & Huang, CSCW2 2022]** [search-confirmed ONLY — [VERIFY]: full
  text must be read; ACM DL 403'd]: gaze duration as real-time reliance proxy. Boundary:
  decision-accuracy outcome, not skill formation; hardware sensor (eye tracker) vs. our
  zero-hardware query-log features — whether text-only features match gaze-grade signal
  is exactly our C4 risk, untested by them or anyone.

**Lane 2 — JITAI (just-in-time adaptive interventions), the loop template:** the mHealth
literature (Nahum-Shani et al.'s JITAI framework and successors [VERIFY exact citations —
from memory: Nahum-Shani et al., Health Psychology 2018 (framework); Klasnja et al. on
micro-randomized trials (HeartSteps) [VERIFY]]) formalized: decision points, tailoring
variables, proximal vs. distal outcomes, and micro-randomized trials for intervention
timing. Boundary: sensors are physical/context (accelerometer, GPS, self-report);
outcomes are health behaviors; no JITAI work senses AI-interaction patterns or targets
skill formation. We import the vocabulary (our tailoring variable = r(prefix); proximal
outcome = next-queries pattern shift; distal outcome = quiz score) rather than
reinventing it — and the micro-randomized-trial idea is the scale-up design for
intervention-timing questions.

**Lane 3 — the design-principles foil: [AgentsThatTeach, arXiv:2607.06101]** [VERIFY —
must be read in full before submission; used here per its role as assigned in planning]:
represents the current normative answer to AI-induced deskilling — design AI assistants
around pedagogical principles (scaffolding, productive struggle, guided questioning) so
that erosion doesn't happen by construction. Boundary, and why it is the foil rather
than a competitor: principles are prescribed *open-loop* — applied to all users all the
time, unconditioned on any measured state of the individual learner. That design stance
(a) taxes users who are in protective patterns already (the 65-86% group needs no
Socratic gate) and (b) has no answer to whether the principles are working mid-session.
H1.1 is the closed-loop complement: measure first, intervene conditionally, verify
against the same quiz that established the harm. If the foil's open-loop designs are the
thesis and laissez-faire assistants the antithesis, conditional intervention is the
synthesis — and the three-arm RCT is what none of the principles papers run.

**Critic:** (a) Lane 2 and Lane 3 both carry [VERIFY] on their core citations —
acceptable in a planning document, fatal in a submission; the related-work debt list
must be explicit and small: read Cao & Huang, read 2607.06101, pin 2-3 canonical JITAI
cites, plus one sweep of the automation-bias/appropriate-reliance literature (Lee & See;
Bucinca et al.'s cognitive forcing functions [VERIFY]) which is conspicuously missing —
cognitive forcing functions ARE lightweight anti-reliance interventions with RCT
evidence in decision-making, the nearest thing to our nudge with data behind it.
(b) The foil framing is rhetorically neat but must not strawman: if 2607.06101 already
proposes *adaptive* (state-conditioned) teaching behavior, the "open-loop" boundary
collapses — verify before building the intro around it. (c) An education-science lane is
missing entirely (intelligent tutoring systems have done real-time learner modeling +
adaptive scaffolding for 30 years — Anderson's cognitive tutors, Bayesian knowledge
tracing). The honest position: ITS does closed-loop learner modeling for *domain
knowledge acquisition inside a tutor*; nobody has ported that loop to *AI-assistant
usage patterns during authentic work*, where the "tutor" is the same tool causing the
erosion. Omitting ITS invites the deadliest CHI review: "this is knowledge tracing,
rediscovered."

**Refined:** Related work becomes five lanes with a declared debt ledger. Lanes 1-3 as
drafted, with the foil claim conditioned on reading 2607.06101 (fallback framing if it
turns out adaptive: "we supply the missing measurement layer its adaptivity would
require"). **Lane 4 — appropriate reliance & cognitive forcing** [VERIFY cites]:
Bucinca et al.-style forcing functions show interruption-based nudges can improve
decision quality at a UX cost — direct precedent for our intervention class AND for our
placebo-control worry (their effects partly run through friction, which is exactly what
M5's placebo nudge isolates). **Lane 5 — ITS/learner modeling**: knowledge tracing and
adaptive scaffolding as the closed-loop ancestor; boundary: models mastery of curricular
skills inside purpose-built tutors, not interaction-pattern risk during authentic
AI-assisted work with a general-purpose assistant; our contribution is the transplant of
that loop to the setting where the assistant itself is the erosion vector. Debt ledger
(pre-submission, ~1 week of reading): Cao & Huang full text; 2607.06101 full text; 2-3
JITAI canon; 2-3 forcing-function/appropriate-reliance canon; 1-2 knowledge-tracing
canon.

---

## Stage 4 — Sub-problems

**Draft.** Five, with the hard part named:

- **SP1 — Feature engineering from query streams without model internals.** The
  classifier sees only what a logging proxy sees: query text, timestamps, response
  text, edit/copy events if instrumented. Needed: features operationalizing the
  taxonomy's discriminators — query intent (runnable-code request vs. explanation
  request vs. hybrid vs. conceptual), follow-up-after-code presence, inter-query gaps,
  code-paste-then-error-paste cycles (the "iterative debugging" tell), and their
  running ratios/trajectories. Risk: the taxonomy was built from rich qualitative
  reading; thin features may not carry it.
- **SP2 — Label transfer from hindsight annotation to prefix classification (THE HARD
  PART).** Ground truth is a session-level label assigned in hindsight; training a
  prefix classifier against it assumes the terminal label was "already true" early —
  false for learners who drift or self-correct. This is a label-noise-by-construction
  problem, and it bounds achievable prefix precision from above.
- **SP3 — Intervention design that doesn't tank task performance.** The nudge must
  shift pattern without wrecking the session: withholding runnable code could reduce
  task completion, frustrate participants, and depress quiz scores through
  discouragement — an intervention that "works" by making AI assistance worse merely
  re-derives the hand-coding arm. Constraint: intervention must preserve task-completion
  parity with the AI-assist arm (base paper found no significant time savings from AI;
  we must not manufacture a time or completion penalty).
- **SP4 — IRB/recruitment logistics.** Human-subjects study with mild information
  asymmetry (participants know an AI assistant is involved and sessions are logged;
  they are not told which arm or that nudges are algorithmically triggered until
  debrief). Recruitment: 60-90 developers with 1+ yr Python and no Trio experience —
  a screenable but not abundant population; compensation, screening integrity (people
  misreport experience), and attrition all bite at this n.
- **SP5 — Baseline comparability.** Reusing the base paper's task+quiz requires either
  obtaining their materials/transcripts as artifacts or reconstructing them faithfully;
  every deviation erodes the "directly comparable to 50%/67%" selling point.

**Critic:** (a) SP2 is correctly the hard part but the draft gives no resolution
strategy — planning documents that name a hard problem without an attack are decoration.
At minimum: measure the *human* hindsight-vs-prefix agreement ceiling (have annotators
label prefixes blind to session ends; their agreement with terminal labels IS the
achievable ceiling and the honest denominator for classifier performance), and reframe
the target as prognosis (Stage 1 refinement) so "the learner hadn't decided yet" is
probability mass, not label noise. (b) SP3 hides a subtle confound: if the intervention
changes the session, it also changes the *features* the classifier subsequently sees —
the loop is non-stationary. One-shot interventions (at most one nudge per session,
pre-registered) cap this in the pilot. (c) SP4 misses the two slowest items: IRB
review latency (2-3 months typical for expedited [VERIFY local IRB norms]) must be
pipelined with offline work, and transcript reuse from the base paper may require its
own data-use agreement with Anthropic — start that email in week 1. (d) SP5 should be
split: materials fidelity (task/quiz) vs. data fidelity (transcripts for training);
the first is essential, the second merely accelerates.

**Refined:** Five sub-problems with attacks attached:

1. **SP1 — Features without internals.** Two-tier featurization: (i) deterministic
   log features (timing, lengths, code-block presence, paste/error cycles);
   (ii) query-intent tags from a small LLM tagger with frozen prompt + 15% human audit
   (κ ≥ 0.75 gate) — the tagger is an annotation tool, not a component requiring model
   internals. Ablation: deterministic-only vs. +intent-tags, so the "how thin can the
   signal be" question is answered, not assumed.
2. **SP2 — Hindsight→prefix transfer (hard part).** Attack in three moves:
   (a) reframe target as terminal-pattern *risk* (prognostic); (b) measure the human
   prefix-labeling ceiling on a 30-session subset (annotators see only prefixes) — the
   classifier is judged against this ceiling, and the ceiling itself is a reportable
   scientific result about how early the patterns are humanly visible; (c) prefix-time
   validity: check that flagged-at-k sessions differ in *subsequent* behavior, so the
   flag is prognostic rather than merely correlated with prefix quirks.
3. **SP3 — Non-destructive intervention.** Design rule: additive-only nudges in the
   pilot (full answer PLUS a comprehension question / "want the why?" affordance) —
   never withholding; withholding variants deferred to scale-up under placebo control.
   One nudge per session (caps non-stationarity per critic (b)). Guardrail metrics
   pre-registered: task completion rate and time-on-task must not degrade vs. AI-assist
   arm beyond a pre-set margin (e.g., 10%), else the intervention "worked" vacuously.
4. **SP4 — IRB & recruitment, pipelined.** Week-1 actions: IRB protocol drafted
   (expedited/minimal-risk, debrief-based partial disclosure); artifact/data-use
   request to base-paper authors. Recruitment: Prolific/Upwork + screening quiz with
   embedded Trio-familiarity trap questions; over-recruit 20% for attrition; budget
   ~$100-150/participant for 2-2.5h (~$9-14k for 90). IRB latency runs concurrent with
   the offline classifier stage, which needs only the (separately consented, lighter)
   transcript-collection protocol.
5. **SP5 — Comparability, split.** Essential: task+quiz fidelity (reconstruct from
   paper if artifacts unavailable; document every deviation). Accelerant: base-paper
   transcripts for classifier training (pursue, don't depend on — the fallback is our
   own 25-30-session AI-arm collection, which doubles as the internal replication's
   first data).

---

## Stage 5 — Methods

**Draft.** The digest's M1-M6, made operational:

- **M1 — Classifier.** Inputs: SP1's two-tier features over prefixes k ∈ {1,3,5,10}
  queries. Class: small-n-appropriate — L2 logistic regression and gradient-boosted
  trees (no deep models at n≈30-60 sessions); leave-one-participant-out CV; calibrated
  probabilities (Platt/isotonic on held-out folds). Output: r(prefix) = risk of erosive
  terminal label; ternary decision {no-flag, watch, flag} via thresholds.
- **M2 — Hindsight-label validation harness.** Dataset: base-paper transcripts if
  released (pursue via SP4 email) else fresh collection: 25-30 AI-assist sessions,
  coded with the published six-pattern protocol by 2 annotators (κ reported; disputes
  adjudicated). Deliverable: precision/recall-at-prefix-length curves per pattern
  cluster (erosive vs. protective as primary binary; six-way as secondary), against the
  trivial majority baseline AND the human prefix ceiling (SP2b).
- **M3 — Detection-lag instrumentation.** Query index + wall-clock of first flag;
  logged in every live session.
- **M4 — Intervention design space.** Pilot: ONE pre-registered additive nudge —
  assistant answers as normal, then appends a targeted comprehension question keyed to
  the just-delivered code ("what happens if the timeout fires inside the nursery?"),
  with a visible affordance to answer or dismiss. Scale-up space: explanation-first
  variants, partial-answer variants, pattern-matched nudges (debugging-pattern → "what
  do you think the bug is?" before the fix).
- **M5 — Reactivity control.** Placebo nudge: same visual interruption, content-free
  ("tip: you can ask follow-up questions"), same trigger policy — separates
  content-driven comprehension gains from interruption-driven effort effects.
  Scale-up arm (pilot is 3-arm; placebo makes 4 in scale-up).
- **M6 — Threshold-setting procedure** (replaces the ≥70% placeholder): (i) estimate
  the erosive-pattern base rate from M2's labeled set (base paper implies roughly half
  of AI-arm sessions land erosive [VERIFY against paper's per-pattern counts]);
  (ii) fix the operating point by decision analysis: cost(false flag) = one wasted
  nudge + mild friction (low); cost(miss) = an unprotected erosive session (high) →
  favor recall, but precision floor set so that expected nudges per protective-pattern
  session ≤ 0.3 (annoyance budget); (iii) pre-register the resulting threshold and the
  gate: classifier must beat majority-baseline precision with p<0.05 (bootstrap over
  participants) at k ≤ half the median session length, AND clear the annoyance budget.
  The "≥70%" number survives only if the base-rate math endorses it.
- **Power analysis (live pilot, ~60-90 participants).** Primary contrast
  classify+intervene vs. AI-assist, two-sample t on quiz %: at n=30/arm, 80% power at
  α=.05 detects d≈0.74 — exactly the base paper's AI-vs-hand effect size. Sobering
  implication: the pilot is powered ONLY for an intervention that recovers a large
  fraction of the lost 17 points; a half-recovery effect (d≈0.35-0.4) needs ~100+/arm.
  Therefore the pilot is framed as estimation + gate (report CI on the effect; proceed
  to scale-up if the point estimate exceeds a pre-set fraction of the base gap), not as
  a confirmatory test of small effects. Randomization stratified by screening-quiz
  score; ANCOVA with baseline covariates (experience, screening score) to claw back
  power (expect effective d gain from covariate R²≈0.2-0.3 [VERIFY on pilot data]).

**Critic:** (a) M2's fallback dataset (25-30 sessions) will yield maybe 12-18 erosive
sessions — LOPO-CV precision estimates at that n have brutal variance; the gate decision
could be noise. Either budget the offline set up (40-50 sessions if transcripts aren't
released — cost is only ~$5-7k more and it is the load-bearing dataset of the whole
topic) or make the gate a CI-based rule (lower bound of bootstrap CI must clear the
baseline), not a point estimate. (b) The six-way secondary task at this n is hopeless;
drop it to descriptive. (c) M4's single nudge keyed to "the just-delivered code"
requires generating a *good* comprehension question in real time — that generation is
itself an LLM behavior that can fail; needs a quality gate (template bank + generation
with fallback to template) and its failures logged as intervention-integrity metrics.
(d) The power sketch is honest but incomplete: it ignores the internal-replication
contrast (hand vs. AI-assist), which at 30/arm has ~80% power for d=0.74 — fine — but
if THAT fails to replicate, the pre-registered interpretation must be specified now
(interpret third-arm contrast descriptively only). (e) Quiz grading: the base paper's
instrument includes open-ended debugging items — grader blinding to arm is mandatory
and unmentioned.

**Refined:** Methods as drafted, with five amendments locked in: (1) offline labeled
set targeted at **40-50 sessions** if base transcripts are not released (pursued in
week 1; answer expected within a month), and the M6 gate stated as: *bootstrap 90% CI
lower bound of precision at k ≤ half-median-session must exceed majority-baseline
precision, subject to the annoyance budget* — no point-estimate gating. (2) Six-way
classification demoted to descriptive appendix; the scientific unit is the
erosive/protective binary (which is also what the intervention needs). (3) M4 nudge
implemented as template-bank-first with LLM instantiation and deterministic fallback;
intervention-integrity (question relevance, fired-at-right-moment) audited on 100% of
pilot firings (cheap at pilot scale). (4) Pre-registered interpretation tree: if
hand-vs-AI replication fails directionally, the three-arm comparison is reported as
estimation-only with the replication failure as a headline finding in its own right
(either outcome is informative given the base paper's prominence). (5) Blinded quiz
grading (two graders, arm-masked transcripts, κ reported), reusing the base paper's
rubric verbatim where obtainable [VERIFY artifact availability].

---

## Stage 6 — Experiment Design

**Draft.** Arms, scale, cost, gates, milestones:

- **Phase 0 (Aug-Oct 2026) — debts + offline dataset.** Read the five debt-ledger
  papers; artifact/DUA request to base authors; IRB protocols (transcript collection
  now, live RCT drafted in parallel); build logging harness + task/quiz reconstruction;
  collect 40-50 AI-assist sessions (or receive transcripts); dual-annotate labels.
  Cost: ~$6-9k participants + ~2 person-months.
- **Phase 1 (Oct-Dec 2026) — classifier + gate.** SP1 features, M1 models, human prefix
  ceiling (SP2b), M6 threshold procedure, gate decision. Deliverable regardless of
  outcome: the precision-at-prefix-length characterization (CO1).
- **Parallel fast deliverable — FAccT 2027 position paper (deadline Nov 3, 2026).**
  Position form: "Skill erosion is a measurable, intervenable harm: post-hoc quizzes
  structurally favor vendors; real-time interaction-pattern auditing should be a design
  obligation for AI assistants in learning-adjacent work." Uses: the corrected
  two-study evidence base, the JITAI/forcing-function synthesis, the closed-loop
  design + gate methodology (as proposal), and — if Phase 0/1 are on schedule — the
  first offline precision curves as preliminary evidence. Position papers do not
  require the live RCT; this is the only deliverable that can ship in 2026.
- **Phase 2 (Jan-May 2027) — live three-arm pilot.** n=90 (30/arm): hand-code /
  AI-assist / classify+intervene (single additive nudge). Primary endpoint per Stage 5.
  Cost: ~$12-15k participants + annotation + ~2 person-months.
- **Phase 3 (May-Aug 2027) — scale-up decision + placebo arm.** If pilot point estimate
  ≥ pre-set fraction (e.g., ≥40%) of the base gap: add placebo-nudge arm (M5) and, if
  budget allows, a second library task (M6/RQ_INF_1), n≈120-160 total, possibly as a
  micro-randomized design for timing questions.
- **Phase 4 (Aug-Sep 2027) — write for CHI 2028** (papers deadline ~Sep 2027 [VERIFY
  exact date]); CSCW 2027/2028 cycles as rolling fallback; AIES as secondary fallback
  for the ethics-forward framing.

Go/no-go gates: **G0** (Oct 2026): labeled set exists with annotator κ ≥ 0.7 on
erosive/protective; else re-code protocol before proceeding. **G1** (Dec 2026-Jan
2027): the M6 CI-based classifier gate — fail → publish CO1 as a negative/
characterization paper (CHI LBW / CSCW note / workshop) + narrow to
delegation-pattern-only detection and re-gate once; hard-fail twice → the real-time
premise is dead as scoped, pivot topic to retrospective session-audit tooling.
**G2** (May 2027): internal replication directional + guardrail metrics clean →
scale-up; else estimation-only reporting and no placebo expansion. **G3** (Aug 2027):
paper-ready evidence for at least CO1+CO2.

**Critic:** (a) The FAccT deadline is 12 weeks away and Phase 0 is 10 weeks of it —
promising "first offline curves as preliminary evidence" by Nov 3 is fantasy unless
transcript release happens fast; the position paper must be written to stand WITHOUT
any new data, with our empirical plan as its constructive proposal. Decide that now,
not in October. (b) IRB timing: live-RCT protocol must be submitted by ~Nov 2026 to
plausibly clear for a Jan-Feb 2027 pilot start; the draft has it merely "drafted in
parallel." (c) No attrition/screening-failure margins in the n arithmetic (SP4 said
over-recruit 20% — carry it into the budget: 90→108 recruited, ~$16-18k). (d) The
two-hard-fails pivot at G1 is good but the timeline consequence is unstated: a January
re-gate burns 6-8 weeks; acceptable only because CHI 2028 has slack — say so.
(e) Nothing schedules the *classifier-frozen* requirement: the model, threshold, and
nudge templates must be frozen and hashed before the first live participant, or the
whole pre-registration story collapses.

**Refined:** Final plan:

- **Deliverable A — FAccT 2027 position paper (Nov 3, 2026), data-free by design.**
  Thesis as drafted; empirical content = the published five-paper evidence base + the
  gated study design itself (pre-registration as an exhibit). Any Phase-0/1 preliminary
  numbers that happen to exist by late October are a bonus appendix, never load-bearing.
  Writing window reserved: Oct 6-31, 2026.
- **Deliverable B — CHI 2028 full paper (submission ~Sep 2027 [VERIFY]); CSCW/AIES
  fallbacks.** Timeline with hard dates: transcripts/DUA answer by Sep 15, 2026 (else
  fresh collection auto-starts Sep 16); offline set complete + G0 by Oct 31; classifier
  + human ceiling + G1 by Jan 15, 2027 (one re-gate allowed, absorbing to Mar 1 — CHI
  slack covers it); live-RCT IRB submitted Nov 15, 2026, approval assumed by Feb 2027
  [VERIFY local IRB latency]; **freeze-and-hash** (classifier, threshold, nudge
  templates, analysis plan, OSF pre-registration) by pilot launch; pilot Feb-May 2027
  (recruit 108 for 90, budget $16-18k); G2 May 31; Phase-3 placebo/second-task
  Jun-Aug 2027 (budget $15-20k, contingent on G2); paper complete for CHI Sep 2027.
- **Total budget envelope:** ~$35-50k participant+annotation costs, ~6-8 person-months
  research effort, negligible compute (classifiers are shallow; the assistant is a
  hosted API).
- **Failure products (pre-committed):** G1 hard-fail → "How early are erosive
  AI-interaction patterns visible? A prefix-labeling ceiling study" (CSCW note);
  G2 replication-fail → "A pre-registered replication of AI-assisted skill-formation
  effects" (valuable given the base paper's prominence); both keep the human-axis topic
  alive rather than sunk.

---

## Residual risks (carried forward, not resolved)

1. **SP2's ceiling may be low** — if humans can't call the pattern from half a session,
   no classifier can; mitigated by making the ceiling itself a headline measurement.
2. **Base-effect fragility** — n=52, one lab; mitigated by internal replication with a
   pre-registered interpretation tree.
3. **Grounding debts** — Cao & Huang and 2607.06101 unread; JITAI/forcing-function
   cites from memory [VERIFY]; one week of reading scheduled before any submission.
4. **Recruitment integrity at n≈100** — screening traps + over-recruitment budgeted,
   but a Prolific-population shift away from the base paper's population would erode
   comparability (documented as a scope limit).
5. **The nudge may work through friction, not comprehension** — unresolvable in the
   pilot by design; placebo arm is scale-up-only, and pilot claims are capped at
   "an effect exists," never "the mechanism is comprehension" (digest t2 discipline).
