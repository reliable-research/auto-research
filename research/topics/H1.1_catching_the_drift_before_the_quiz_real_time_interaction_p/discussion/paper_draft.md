# Catching the Drift Before the Quiz: Prefix-Only Detection and Placebo-Controlled Just-in-Time Intervention Against Skill-Eroding AI Interaction Patterns

> Assembled from the six confirmed stage outputs in `discussion_trace.md`, post-audit
> (`taste_audit.md`: 🟢). Status: **pre-registered specification / paper draft — no experiments
> have been run.** All numbers below are pre-registered design targets with stated rationales,
> not results. Human-subjects work is gated on the IRB/DUA milestones stated in the Experiments
> section.

## Abstract

AI coding assistance can accelerate task completion while eroding the comprehension developers
need to supervise generated code: in a randomized trial of 52 developers learning an unfamiliar
Python library (Shen & Tamkin, 2026), the AI-assisted arm scored 17 points lower on a post-task
quiz, and the loss tracked six interaction patterns coded in hindsight from complete sessions.
Every existing measurement of this harm arrives after the fact — nothing can act on it while the
session is still running. We answer with a gated design: a calibrated prognostic risk that a
session, if uninterrupted, terminates in an erosive pattern, estimated from query-stream
prefixes alone — no model internals, no biometrics — and evaluated against a measured human
prefix-labeling ceiling; a frozen model that must pass a sealed, prevalence-anchored exact-bound
authorization gate before any live intervention; and, if authorized, a preregistered four-arm
trial — hand-code, unnotified AI, placebo notification, additive comprehension nudge — that
internally replicates the published gap, isolates nudge content from notification reactivity,
and preserves the original rubric under blinded grading. Either branch of the gate produces
knowledge the field lacks: how early erosive drift is visible at all, or whether catching it
preserves learning.

## Introduction

AI assistants are now a default companion for programmers working with unfamiliar libraries,
which makes one trade newly consequential: the same delegation that speeds the task can starve
the comprehension a developer would need to evaluate, debug, and maintain the resulting code.
For at least one controlled setting this is no longer speculation. In Shen and Tamkin's (2026)
randomized trial, 52 developers with Python experience but no exposure to the Trio async library
completed tasks with or without AI assistance; the AI-assisted arm scored 17 points lower on a
subsequent concept, code-reading, and debugging quiz (50% vs. 67%, d = 0.738), without
significant time savings. The harm was not uniform: hindsight coding of the session recordings
identified six interaction patterns, and the outcome tracked the pattern, not AI use per se —
full delegation, progressive reliance, and iterative AI debugging scored below 40%, while
generate-then-ask, hybrid code-plus-explanation queries, and purely conceptual questioning
scored 65–86%.

Yet a central question about this harm remains unexamined: every measurement of it arrives after
the fact. The base trial labels complete recordings; observational work detects an "AI-prompt
signature" only retrospectively and at cohort level (Yao, 2026); EEG and recall studies measure
downstream states, not the interaction stream (Kosmyna et al., 2025). Nobody knows how early an
erosive session announces itself in behavior — to a statistical procedure or even to an expert
human reading the transcript — and as long as the drift is only nameable after the quiz,
assistants can do nothing about it at the moment it matters, and the people incurring the harm
cannot see it at decision time. The question stated by the base paper's framing but attempted by
no one is whether the early behavioral signature of an erosive session is recognizable from a
partial session prefix, and whether acting on that recognition preserves learning.

Two obstacles make this harder than it looks. First, the pattern taxonomy is a hindsight summary
of whole sessions: a learner may be genuinely pattern-indeterminate at query three, so a
prefix-time "diagnosis" of the eventual pattern is partially ill-posed by construction. The
detector must instead estimate a prognostic risk — the probability that the session, if
uninterrupted, terminates in an erosive pattern — and the honest ceiling on any such estimate is
itself unknown, so we measure it directly by asking annotators to label prefixes blind to
session endings. Second, an intervention triggered by detection can "work" for the wrong
reasons: interruption alone changes behavior, and an intervention that degrades the assistant
merely re-derives the hand-coding arm. Worse, intervening on live participants on the strength
of a noisy small-sample precision estimate is an ethical failure before it is a statistical one.

Our design turns each obstacle into a specific, pre-registered mechanism. The risk model reads
only what a logging proxy sees — query text, timestamps, responses, paste and error events — so
the instrument is deployable by any party, including auditors who do not own the model. Its
output is converted into at most one timed alert per session by a first-crossing trigger whose
risk value is frozen before any message is delivered. No live participant is intervened on
unless a frozen model and cutoff first pass a sealed authorization gate: an exact
Clopper–Pearson bound on alert precision must clear the measured erosive base rate by a
pre-registered margin, with a minimum alert count and an explicit annoyance budget — not an
arbitrary constant threshold. And the live trial that a gate pass authorizes carries its own
validity checks: hand-code and unnotified-AI arms internally replicate the published contrast
before any intervention contrast is interpreted, and a timing-, length-, and
presentation-matched placebo notification separates what the nudge says from the fact that it
interrupts.

The program is deliberately serialized so that either branch of the gate produces knowledge the
field lacks. A gate failure still delivers the first quantification of how early erosive
patterns are visible in the behavior stream — to humans and to a leakage-controlled statistical
procedure — which is a publishable characterization with direct design implications. A gate pass
additionally delivers the first closed just-in-time loop outside purpose-built tutoring
systems whose sensed state is an AI-interaction pattern and whose distal outcome is measured
skill formation, on an instrument directly comparable to the published baseline.

In summary, we contribute:

- A prognostic, prefix-only risk model for skill-eroding AI interaction, validated with
  developer-disjoint cross-fitting against prevalence baselines and a measured **human
  prefix-labeling ceiling** — itself a new scientific quantity: how early are these patterns
  visible at all?
- A **decision-analytic, sealed authorization gate** that converts small-sample alert precision
  into an auditable, prevalence-anchored go/no-go rule, pre-registered as the ethical
  precondition for any live intervention.
- A gate-conditional, **four-arm randomized evaluation** that internally replicates the
  published hand-vs-AI skill-formation gap, estimates the effect of a one-shot additive
  comprehension nudge, and isolates nudge content from notification reactivity via a matched
  placebo.
- A **scoped novelty position**: we import, and credit, the just-in-time adaptive intervention
  vocabulary, the intelligent-tutoring closed-loop tradition — including its
  gaming-the-system detect-and-intervene line — and the learning-analytics early-warning
  detector shape; the contribution is the transplant of that loop to the setting where the
  assistant itself is the erosion vector, during authentic work, sensed through zero-hardware
  query-log features.

## Problem Definition

**Formal setup.** For developer $i$, a session is an ordered query stream
$Q_i = (q_{i1}, \ldots, q_{iT_i})$ produced while working with an AI assistant on an
unfamiliar-library task, where each $q_{it}$ carries its text, timestamp, the assistant's
response, and any paste/error events. Let $L_i \in \{0,1\}$ be the hindsight label — erosive-
versus protective-terminal — assigned to the *complete* session by the published six-pattern
coding protocol, collapsed to a binary. For prefix length $k$, write
$Q_i^{(k)} = (q_{i1}, \ldots, q_{ik})$.

**Stage 1 (offline, detection).** Learn $f: Q^{(k)} \to [0,1]$ producing a calibrated
prognostic risk $r_{ik} = f(Q_i^{(k)}) \approx P(L_i = 1 \mid Q_i^{(k)})$ using only
prefix-observable features — no model internals, no future queries, no full-session statistics.
With cutoff $c$, the alert rule is $\hat{L}_{ik} = \mathbb{1}[r_{ik} \geq c]$. Evaluation
reports precision and recall at prefix lengths $k \in \{1,3,5,10\}$ and elapsed-time checkpoints
$\{10, 20, 30\}$ minutes, against (a) the prevalence baseline and (b) the human prefix ceiling:
the agreement of annotators who label the same prefixes blind to session endings.

**Authorization gate.** Let $\hat{p}$ be the erosive-label prevalence on development data. One
final $(f, c)$ is frozen and hashed, then scored exactly once, at the half-session checkpoint,
on a sealed developer-disjoint gate set. The live study is authorized iff

$$G \;=\; \mathbb{1}\left[\; \underline{\pi}_{90} \geq \hat{p} + 0.10 \;\;\wedge\;\; a \geq 5
\;\;\wedge\;\; \mathrm{FPB} \leq 0.3 \;\right] = 1,$$

where $\underline{\pi}_{90}$ is the one-sided 90% Clopper–Pearson lower bound on gate-set alert
precision, $a$ the number of alerted sessions, and $\mathrm{FPB}$ the false-positive burden —
expected alerts per protective-terminal session (the annoyance budget). A design *target*
precision of 0.70 is retained only if the measured base rate endorses it; the gate itself is
anchored to prevalence, never to a constant.

**Stage 2 (live, intervention; only if $G = 1$).** Participants are randomized to four
concurrent arms $A_i \in \{H, U, P, N\}$: hand-code ($H$), unnotified AI assistance ($U$),
placebo-trigger ($P$), and active-nudge ($N$). The frozen classifier runs silently in all AI
arms; in $P$ and $N$, the first crossing $r_{ik} \geq c$ after a floor of $k \geq 3$ triggers,
at most once per session, either a matched content-free notification ($P$) or an additive
comprehension nudge ($N$); the risk value is frozen before any message is delivered, so flagged
subgroups are defined pre-treatment in every AI arm. With $Y_i$ the blinded, original-rubric
quiz score and $\mu_a = \mathbb{E}[Y_i \mid A_i = a]$, the pre-registered estimands are

- **Replication (validity precondition):** $\Delta_{\mathrm{rep}} = \mu_U - \mu_H$, expected
  negative, directionally replicating the published 17-point gap;
- **Primary:** $\Delta_{\mathrm{content}} = \mu_N - \mu_P$ (nudge content beyond notification
  reactivity), intention-to-treat and within the pre-trigger flagged subgroup;
- **Secondary:** $\Delta_{\mathrm{react}} = \mu_P - \mu_U$ and
  $\Delta_{\mathrm{policy}} = \mu_N - \mu_U$;
- **Process endpoints:** detection lag (query index, wall-clock, and fraction of session
  remaining at first alert) and guardrails — task completion and time-on-task in $N$ within 10%
  of $U$.

**Why this is hard.** The label $L_i$ exists only at session end, so training $f$ against it
presumes the terminal label was "already true" at query $k$ — false for learners who drift or
self-correct; this is label noise by construction, and it bounds achievable prefix precision
from above by a ceiling nobody has measured. The observable stream is thin: the taxonomy that
defines $L_i$ was built from rich qualitative reading, while $f$ sees only log features, so
signal sufficiency is an open empirical question, not an assumption. Any effect of a triggered
message on $Y$ confounds content with interruption reactivity unless the trigger policy, timing,
and presentation are matched across $P$ and $N$. The authorization decision must be made from
tens of sessions, where point estimates of precision are noise — only exact small-sample bounds,
sealed data, and a pre-enumerated decision table make $G$ trustworthy. And the entire
comparison inherits a fragile base effect ($n = 52$, one lab), which is why
$\Delta_{\mathrm{rep}}$ is carried inside the design rather than assumed from the literature.

## Method Overview

The study is one measurement-then-intervention pipeline with six cooperating parts. Query
streams enter as prefixes; a **prognostic risk model** turns them into calibrated
erosive-terminal risk after every query. A dual-purpose **annotation harness** supplies both the
hindsight labels the model trains against and the human prefix ceiling that bounds what any
prefix-time estimate can achieve. A **first-crossing trigger** converts the running risk into at
most one timed, logged alert per session, freezing the risk value before any message is sent. A
**sealed authorization gate** decides, from exact small-sample bounds on sealed data, whether
the frozen detector is good enough to justify intervening on people. If it is, an **additive
comprehension nudge with a matched placebo** delivers the intervention in a way that makes its
mechanism attributable — content versus reactivity — and a **four-arm assignment scheme** keeps
the published hand-vs-AI contrast internally re-tested alongside the intervention contrasts.
The parts are serialized left to right: no trigger fires with an unfrozen model, no participant
is nudged without a gate pass, and no intervention contrast is interpreted before the
replication check.

## Methodology

### Prefix-Only Prognostic Risk Model

**Challenge.** Ground truth is a hindsight label on the complete session; a learner can be
genuinely pattern-indeterminate early, so prefix-time six-way diagnosis is partially ill-posed,
and the informative behaviors are partly semantic while a logging proxy sees only thin features.

**Insight.** Reframing the target as *terminal-pattern risk* turns early indeterminacy into
probability mass rather than label noise — a calibrated model can honestly output 0.55 — and a
landmark structure over cumulative prefix features yields a per-query estimate that cannot leak
future information by construction.

**Method.** Two feature tiers are computed cumulatively at each prefix: deterministic log
features (query count and length, inter-query gaps, elapsed time, code-block presence,
code-paste-then-error-paste cycles, follow-up-after-code presence, user-authored diagnostic
detail), and LLM-tagged query intents (complete-solution request / explanation-or-testing
request / hybrid / conceptual question) produced by a frozen prompt with a 15% human audit at
$\kappa \geq 0.75$. A session-weighted elastic-net logistic landmark model with Platt
calibration estimates $r_{ik}$ after each query; sessions contribute equal total weight
regardless of prefix count; hyperparameters and calibration are selected by nested
leave-one-developer-out cross-fitting; no deep models at this $n$. The cutoff $c$ is selected on
fold-train data only, targeting the gate's operating point subject to the annoyance budget. A
deterministic-only ablation answers how thin the signal can be rather than assuming it.

### Hindsight-Label and Human Prefix-Ceiling Harness

**Challenge.** Any classifier's prefix-time performance is bounded above by how early the
patterns are visible *at all* — a quantity nobody has measured — and the labels themselves come
from a qualitative protocol whose reliability at this site must be demonstrated, not assumed.

**Insight.** The same annotation apparatus can produce both: protocol-coded terminal labels
(the training target) and blind prefix labels (the ceiling), making the ceiling simultaneously
the honest denominator for the model, a standalone scientific result, and the cheapest possible
de-risking of the gate — if humans cannot call the pattern from half a session, no classifier
can.

**Method.** Two annotators code all complete sessions with the published six-pattern protocol;
the erosive/protective binary is primary ($\kappa \geq 0.7$ required; disputes adjudicated;
six-way classification kept descriptive). Separately, annotators label a 30-session subset of
*prefixes* at $k \in \{1,3,5,10\}$, blind to session endings; their agreement with terminal
labels, per $k$, is the human prefix ceiling. A prefix-time validity check verifies that
flagged-at-$k$ sessions differ in *subsequent* behavior (post-$k$ feature trajectories), so
flags are prognostic rather than correlates of prefix quirks.

### First-Crossing Trigger and Detection-Lag Instrumentation

**Challenge.** A single fixed checkpoint can show that signal exists by minute 30, but not how
much session remains when it appears — and "just-in-time" is a timing property: an alert with
most of the session already spent supports no intervention worth the name.

**Insight.** Making the trigger event-driven — the first crossing of a frozen cutoff — turns
detection lag into a measured distribution, and freezing the risk value before any message is
delivered is what keeps flagged-subgroup comparisons causal: the subgroup is defined by
pre-treatment information in every arm.

**Method.** $r_{ik}$ is recomputed after every query; the alert is the first crossing of the
frozen $c$ after a floor of three queries; at most one alert fires per session (bounding the
loop's non-stationarity); the risk value and feature snapshot are logged before delivery.
Detection lag is recorded as query index, wall-clock time, and the fraction of the session's
eventual query count still ahead.

### Decision-Analytic Sealed Authorization Gate

**Challenge.** The go/no-go decision to intervene on live participants must be made from tens of
sessions, where a precision point estimate is noise, a fixed-constant bar is either unpassable
by construction or vacuously easy depending on the base rate, and any post-hoc freedom in
threshold or cutoff choice invalidates the guarantee.

**Insight.** At this $n$ only exact binomial bounds are honest — a go/no-go discipline
imported from Simon-style two-stage phase II clinical-trial designs, here gating a detector's
licence to intervene rather than a treatment effect — and anchoring the bar to the
*measured* prevalence — pass only if the lower confidence bound on alert precision beats the
base rate by a margin, with enough alerts to mean something and a bounded false-positive
burden — makes the gate simultaneously passable by a genuinely enriched detector and unpassable
by a lucky one. Sealing plus a pre-enumerated pass table removes every degree of post-hoc
freedom.

**Method.** After development analyses close, one final $(f, c)$ is fitted on all development
sessions and frozen: serialized and hashed together with the feature specification, exclusion
rules, and the fully enumerated (alerts, true-positives) pass table. The sealed,
developer-disjoint gate set (at least 20 sessions, untouched during development) is scored
exactly once — a single pass that evaluates the half-session criterion and logs each session's
full per-query risk trajectory, from which all pre-registered read-outs (the gate decision and
the lead-time distribution) are computed without ever re-scoring sealed data — and the
pre-registered criterion of the Problem Definition is applied mechanically. Zero alerts is a pre-registered no-go. One re-gate is
permitted after a pre-registered narrowing to delegation-pattern-only detection; a second
failure retires the real-time premise as scoped and redirects the topic to retrospective
session-audit tooling.

### Additive Comprehension Nudge with Matched Placebo

**Challenge.** A triggered intervention can improve quiz scores for the wrong reasons:
interruption alone increases effort, and withholding answers re-derives the hand-coding arm —
either way the mechanism claim is spurious, and an intervention that tanks task completion has
"worked" vacuously.

**Insight.** Matching the placebo to the active nudge in trigger policy, timing, length, and
presentation leaves exactly one difference — whether the appended content does cognitive work —
so an effect that survives the placebo contrast and the completion guardrails is attributable to
content acting on an ongoing session.

**Method.** On trigger, the assistant answers exactly as it otherwise would, then appends one
targeted comprehension question keyed to the just-delivered code, instantiated by an LLM from a
vetted template bank with a deterministic template fallback; nothing is ever withheld. The
placebo fires under the identical policy with content-free text. One nudge per session; 100% of
pilot firings are audited for relevance and timing (intervention-integrity metrics).
Pre-registered guardrails require task-completion rate and time-on-task in the active arm to
remain within 10% of the unnotified arm.

### Internally Replicated Four-Arm Design

**Challenge.** The headline comparability claim — results directly interpretable against the
published 50%/67% baseline — rests on a base effect measured once, at $n = 52$, in one lab; a
design that assumes it invites collapse, and one that cannot re-test it forfeits the comparison.

**Insight.** Carrying the published trial's own two arms inside the new trial converts the base
effect's fragility from an inherited assumption into a measured result, and a pre-registered
interpretation tree makes a replication failure informative rather than fatal.

**Method.** Participants are randomized, stratified by screening-quiz score, to hand-code,
unnotified-AI, placebo-trigger, or active-nudge arms; the frozen classifier runs silently in all
AI arms; AI-arm allocation and the algorithmic trigger are concealed until debrief
(IRB-approved partial disclosure). Quizzes are graded by two arm-blinded graders with the
original rubric ($\kappa$ reported). Analysis is ANCOVA with baseline covariates (experience,
screening score), multiple imputation (50 datasets, Rubin's rules), and delta-adjusted MNAR
tipping-point sensitivity. The interpretation tree is pre-registered: if the replication
contrast fails directionally, all intervention contrasts are reported as estimation-only and the
replication failure is itself a headline finding.

## Experiments

### Experimental Setup

**Data.** *Source A (pursued, not depended on):* the base trial's 52 AI-arm session transcripts
under a data-use agreement with the authors; the request is sent in week 1 with a pre-registered
answer deadline of 2026-09-15. *Source B (fallback, auto-starts 2026-09-16):* fresh collection
of 40–50 AI-assisted sessions on the reconstructed task under a lightweight
transcript-collection IRB protocol, extending to ~60 sessions if the data-use agreement fails
outright — sized so that the offline split holds in every branch; these sessions double as the
internal replication's first data, and every deviation of reconstructed materials from the
original task and quiz is documented. All available sessions are pooled and split **by
developer** into a development set (≥ 40 sessions) and a sealed gate set (≥ 20 sessions) via an
outcome-blind blocked hash balancing task family, experience, and source — correcting an
earlier 20-development/32-gate allocation that starved the model and made the gate's precision
requirement statistically unreachable. Sessions collected beyond the 40-session development
minimum are pre-committed to the gate set: at the 20-session minimum the pass table demands
observed precision near 0.90 at 9–10 alerts, and a larger gate set is the only pre-registered
lever that relaxes the demanded cell without touching the bar itself. *Live trial:* four arms, $n = 120$ (30/arm), 144
recruited (20% over-recruitment), Prolific/Upwork, 1+ year Python, no Trio experience, screening
quiz with embedded familiarity traps, $100–$150 per 2–2.5 h session.

**Comparators** (controls and references — this is a measurement-and-intervention study; no
research question is framed as "our procedure beats baseline X"). The fold-train
prevalence-only predictor is the sanity reference for every probabilistic claim. The human
prefix ceiling is the upper reference for prefix-time performance. The hand-code and
unnotified-AI arms reproduce the published trial's own two arms; the placebo-trigger arm
isolates notification reactivity.

**Metrics.** Alert precision/recall and enrichment over prevalence at prefix lengths
$k \in \{1,3,5,10\}$ and elapsed-time checkpoints; session-weighted Brier score and calibration
diagnostics; human-ceiling agreement per $k$; gate quantities (alert count, true positives,
Clopper–Pearson bound, false-positive burden); detection lead time; blinded original-rubric quiz
scores by arm; task-completion and time-on-task guardrails; nudge-firing integrity.

**Ethics, IRB, and timeline.** Two IRB protocols are pipelined: transcript collection (minimal
risk, consented logging; submitted immediately) and the live RCT (mild information asymmetry —
participants know sessions are logged and an AI assistant is involved, not which arm or that
nudges are algorithmically triggered until debrief; submitted 2026-11-15 for a Feb 2027 start
under expedited review). The model, cutoff, pass table, nudge templates, and analysis plan are
frozen, hashed, and pre-registered (OSF) before the first live participant. Gate calendar: G0
(labeled offline set, annotator $\kappa$) 2026-10-31; G1 (sealed gate) 2027-01-15, one re-gate
absorbing to 2027-03-01; pilot Feb–May 2027; G2 (replication + guardrails) 2027-05-31; scale-up
Jun–Aug 2027; CHI 2028 submission ~Sep 2027 with CSCW/AIES fallbacks. A data-free FAccT 2027
position form (deadline 2026-11-03) argues the normative case using only the published evidence
base and this gated design. Budget envelope: $35–50k participants and annotation, 6–8
person-months, negligible compute.

**Research questions:**

1. RQ1 — How early are erosive patterns humanly visible from prefixes (the ceiling)?
2. RQ2 — Does prefix-time alert precision clear the prevalence-anchored margin at half-session?
3. RQ3 — Do calibrated risk scores beat prevalence-only prediction at locked checkpoints?
4. RQ4 — Do deterministic, zero-hardware features alone retain most of the signal?
5. RQ5 — Does the frozen detector pass the sealed authorization gate?
6. RQ6 — Does the first alert fire with enough session remaining to act (lead time)?
7. RQ7 — Does the published hand-vs-AI gap internally replicate?
8. RQ8 — Does nudge content improve quiz scores beyond notification reactivity, within
   guardrails?

#### RQ1: How early are erosive patterns humanly visible? (the ceiling)

**Setup.** Annotators label 30 development-session prefixes at $k \in \{1,3,5,10\}$, blind to
session endings; agreement with protocol-coded terminal labels is computed per $k$. Sample size
is a characterization target: 120 prefix judgments per annotator, sized for a ±0.15 CI
half-width (at 90% confidence) on per-$k$ precision at the implied base rate.

**Expected outcome.** The human ceiling clears prevalence + 0.10 precision at the half-median
session prefix but not at $k = 1$: the patterns become visible somewhere between the first query
and mid-session.

**Falsification condition.** Refuted if half-session human precision fails to clear prevalence
+ 0.10 — the patterns would not be humanly visible early, bounding the real-time premise away;
the ceiling then becomes the headline finding and the classifier questions are reported as
characterization only.

**Hypothesis (plain language).** Erosive-terminal sessions are recognizably different, to expert
eyes, by the middle of the session.

**Metrics.** Human precision/recall vs. terminal labels per $k$; inter-annotator $\kappa$ on
prefixes.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Does prefix-time alert precision clear the prevalence-anchored margin?

**Setup.** Development set only (≥ 40 sessions, ~16–24 erosive under the design assumption
checked at G0); nested leave-one-developer-out cross-fitting; cluster bootstrap over developers
with the full pipeline re-run per replicate (B = 2,000); precision/recall at
$k \in \{1,3,5,10\}$ and 10/20/30-minute checkpoints.

**Sample-size rationale.** At fewer than ~40 development sessions the bootstrap lower bound
cannot clear a +0.10 margin even for a genuinely enriched detector — the feasibility failure
that sank the prior parameterization — hence the dual-source data plan.

**Expected outcome.** The one-sided 90% cluster-bootstrap lower bound on alert precision exceeds
prevalence + 0.10 at some $k$ no greater than half the median session length; not at $k = 1$.

**Falsification condition.** Refuted if the lower bound fails the margin at every
$k \leq$ half-median session — the detector would add nothing over a base-rate guess, a
pre-registered no-go before any sealing.

**Hypothesis (plain language).** A leakage-controlled statistical procedure can identify
erosive-terminal sessions from the first half of the query stream more precisely than the base
rate.

**Metrics.** Precision, recall, alert count, enrichment over prevalence per $k$ and per
checkpoint; gap to the RQ1 ceiling.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Do calibrated risk scores beat prevalence-only prediction?

**Setup.** As RQ2; session-weighted Brier scores at locked 10/20/30-minute checkpoints against
the fold-train prevalence-only predictor; Holm correction across the three checkpoints.
Pre-registered ablations: regularization on/off, calibration on/off, checkpoint-by-index vs.
by-time.

**Expected outcome.** Relative Brier improvement with a cluster-bootstrap one-sided 90% lower
bound above 0.10 at the 20- and 30-minute checkpoints; the 10-minute checkpoint may be
inconclusive.

**Falsification condition.** Refuted if no checkpoint clears the Holm-adjusted bound — the risk
scores would carry no calibrated information beyond the base rate.

**Hypothesis (plain language).** The model's probabilities are better forecasts of how a session
ends than knowing only how often sessions end badly.

**Metrics.** Session-weighted Brier per checkpoint; calibration slope and intercept; reliability
diagrams.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Can the features be thin? (zero-hardware sufficiency)

**Setup.** Re-run the full RQ3 pipeline with deterministic log features only (no LLM intent
tags); compare relative Brier improvement to the full two-tier model at the half-session
checkpoint; cluster-bootstrap CI on the retained fraction.

**Expected outcome.** The deterministic-only model retains at least 50% of the full model's
relative Brier improvement — the signal does not hinge on semantic intent tagging — while the
full model remains better.

**Falsification condition.** Refuted if the retained fraction's confidence interval falls below
0.5 — the detector's signal would depend on the LLM tagger, and the "any logging proxy can
deploy this" claim narrows to proxies with tagging capability (scope note pre-committed).

**Hypothesis (plain language).** Counting and timing behaviors — not reading their meaning —
carries most of the early-warning signal.

**Metrics.** Retained-fraction ratio with CI; per-tier feature importances (descriptive).

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Does the frozen detector pass the sealed authorization gate?

**Setup.** One final model-and-cutoff pair is frozen and hashed with the feature specification,
exclusion rules, and the fully enumerated pass table; the sealed developer-disjoint gate set
(≥ 20 sessions) is scored exactly once — a single pass evaluating the half-session criterion and
logging per-query risk trajectories — and the Problem Definition's criterion is applied
mechanically. At $n = 20$ and prevalence ≈ 0.5, the criterion is passable at, e.g., 8 true
positives among 9 alerts (Clopper–Pearson 90% lower bound ≈ 0.632 > 0.60) or 9 of 10 (≈ 0.663) —
reachable by a genuinely enriched detector — whereas 7 of 8 fails (0.594), and a fixed 0.70
lower-bound rule would be cleared only by near-perfect cells such as 8 of 8 (0.750). The
minimum-set cells are demanding — 8/9 and 9/10 are observed precisions of 0.89–0.90 — which is
why surplus sessions are pre-committed to the gate set: at ~15 alerts the demanded cell
relaxes to 12 true positives among 15 (90% lower bound ≈ 0.607).

**Expected outcome.** Conditional, not confident: at the pre-registered bar, a detector whose
true precision merely clears the RQ2 margin (0.60–0.75) passes a 9–10-alert gate with low
probability, so a first-attempt pass is expected only if the detector's true precision lands
well above the margin or the surplus-to-gate-set pre-commitment enlarges the alert count; the
design's honest expectation is a pass within the two permitted attempts — lower bound above
prevalence + 0.10, at least 5 alerts, false-positive burden within the 0.3 annoyance budget —
with the characterization paper as the pre-committed product otherwise.

**Falsification condition.** The gate is the falsification instrument: failing it twice
(including the one permitted re-gate after narrowing to delegation-only detection) refutes the
deployable-detector claim at this scale and scope, and the pre-committed failure product is the
RQ1–RQ4 characterization paper.

**Hypothesis (plain language).** The detector's precision advantage survives contact with sealed
data it has never influenced.

**Metrics.** Alert count, true positives, precision, Clopper–Pearson bound, false-positive
burden.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Does the first alert fire with enough session remaining to act?

**Setup.** First-crossing times (floor $k \geq 3$) are read from the per-query risk
trajectories logged during the gate set's single scoring pass — sealed data is never re-scored;
lead time is the fraction of the session's eventual query count still ahead at the first true
alert; one-sided sign test on the median. The 40% floor is an authored design
target: an alert with most of the session spent cannot support a just-in-time intervention, and
40%-remaining leaves the nudge roughly half the working session to act on.

**Expected outcome.** Median lead time among true alerts is at least 40% of the session's
eventual query count.

**Falsification condition.** Refuted if the median true alert fires with less than 40% of the
session remaining — detection would be real but too late, and the intervention claim would be
bounded by timing rather than accuracy; the live trial's detection-lag endpoint re-checks this
in vivo.

**Hypothesis (plain language).** When the alarm rings, most of the fire is still preventable.

**Metrics.** Lead-time distribution (query-index and wall-clock forms); later, per-arm lag in
the live trial.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Does the published hand-vs-AI gap internally replicate?

**Setup.** Hand-code vs. unnotified-AI arms of the live trial; blinded original-rubric grading
by two graders ($\kappa$ reported); one-sided ANCOVA contrast at $\alpha = 0.05$ with baseline
covariates; multiple imputation with Rubin's rules; MNAR tipping-point sensitivity. At 30/arm,
power is at least ~80% for the published $d = 0.738$ (two-sample normal approximation ≈ 0.89)
— the one contrast the pilot is confirmatorily powered for, by design.

**Expected outcome.** The unnotified-AI arm scores directionally and significantly lower than
the hand-code arm.

**Falsification condition.** Refuted if the unnotified-AI arm scores at or above the hand-code
arm, or the contrast is non-significant; the pre-registered interpretation tree then reports all
intervention contrasts as estimation-only, and the replication failure is itself a headline
finding given the base trial's prominence.

**Hypothesis (plain language).** The published skill-formation gap is real enough to reappear in
an independent replication of its own two arms.

**Metrics.** Quiz score by arm; standardized gap versus the published effect size.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ8: Does nudge content help beyond reactivity, without collateral cost?

**Setup.** Primary contrast: active-nudge vs. placebo arms, intention-to-treat and within the
pre-trigger flagged subgroup (risk frozen before notification, so the subgroup is pre-treatment
in all AI arms); secondary contrasts: placebo vs. unnotified (reactivity) and active vs.
unnotified (total policy effect); guardrails (completion, time-on-task within 10%) against the
unnotified arm; 100% intervention-integrity audit of firings; detection lag logged in all AI
arms. The pilot is pre-registered as estimation-plus-gate: report the confidence interval on the
content contrast and proceed to scale-up ($n \approx 120$–$160$, micro-randomized timing) iff
the point estimate is at least 40% of the internally replicated gap with guardrails clean. The
40%-of-gap floor is an authored target: recovering less than ~7 of 17 points would not justify a
deployed interruption channel under the annoyance budget.

**Expected outcome.** Active exceeds placebo with a point estimate of at least 40% of the
replicated gap; guardrails hold; the reactivity contrast is small.

**Falsification condition.** Refuted if active does not exceed placebo (content adds nothing
beyond reactivity), or if guardrails fail (the nudge "works" by degrading the session —
vacuous), or if the effect appears only outside the flagged subgroup (misattributed to the
trigger); each branch's reporting language is pre-committed in the interpretation tree.

**Hypothesis (plain language).** What the nudge says — not the fact that it interrupts — buys
back part of the lost comprehension, without slowing the work.

**Metrics.** Quiz score by arm (ITT and flagged subgroup); completion rate; time-on-task;
integrity rate; detection lag.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more resources, natural extensions are pattern-matched nudge
variants (a different question for a debugging-loop session than for a full-delegation one), a
second task/library to test generalization beyond Trio, and micro-randomized timing designs for
the intervention-timing question — all deferred to scale-up, all inheriting the frozen
machinery.

### Threats to Validity

**Construct validity.** The erosive/protective construct is inherited from the published
protocol; its reliability at this site is gated ($\kappa \geq 0.7$ on the binary before any
model training), and the six-way taxonomy is demoted to descriptive use. The LLM intent tagger
is an instrument inside the instrument: it runs under a frozen prompt with a 15% human audit at
$\kappa \geq 0.75$, and if it fails the audit, the deterministic-only feature set is the declared
instrument (RQ4 measures the cost of that fallback). The prefix ceiling itself depends on
annotators not inferring endings from prefixes; blinding to session endings and the
prefix-time validity check (flagged sessions must differ in subsequent behavior) address this.

**Internal validity.** The intervention contrasts are protected by three mechanisms: matched
placebo (content vs. reactivity), pre-notification risk freezing (flagged subgroups defined
pre-treatment), and additive-only nudges with completion/time guardrails (no degraded-assistant
confound). The offline stage's leakage controls are structural: prefix features cannot see the
future by construction, cross-fitting is developer-disjoint, the cutoff is chosen on fold-train
data only, and the gate set is sealed and scored once by a hashed, frozen model.

**External validity.** Findings are scoped to one task family (unfamiliar-library learning, the
Trio setting or its documented reconstruction), one population (crowd-recruited developers with
1+ year Python, no Trio), and one intervention class (one-shot additive comprehension nudges).
The base paper's own caveat that its setup differs from agentic coding products is inherited:
results are a plausible lower bound for settings with richer delegation affordances, and no
claim is made beyond the tested grid. Crowd-population drift from the original trial's
population is bounded by screening traps and documented deviations, not eliminated.

**Conclusion validity.** All offline inference is cluster-bootstrap over developers with the
full pipeline re-run per replicate; the gate uses exact binomial bounds on sealed data; the
live pilot is confirmatorily powered only for the replication contrast and is pre-registered as
estimation-plus-gate for the intervention contrast, with the 40%-of-gap decision rule and the
interpretation tree fixed in advance. Attrition and missingness are handled by 20%
over-recruitment, multiple imputation, and MNAR tipping-point sensitivity rather than
complete-case optimism.

## Related Work

The closest prior work is Shen and Tamkin's (2026) skill-formation RCT — whose task, quiz
rubric, labels, and two arms this design reuses and extends — and, for the detection claim
specifically, Yao's (2026) "AI-prompt signature"; it is worth stating the delta plainly before
surveying the landscape: the former labels complete sessions in hindsight and never estimates
anything at prefix time, the latter detects a signature retrospectively at cohort level without
an individual-session model or any intervention. The closed detect→intervene→verify loop on a
learning outcome does have a precedent — purpose-built intelligent tutors have run it for two
decades, most sharply in the gaming-the-system line conceded below — but no work closes that
loop where the sensed stream is a general-purpose assistant's query log, the setting is
authentic work, and the outcome is skill formation under the assistant causing the risk.

**The causal premise and its neighbors.** Shen and Tamkin (2026) provide the base RCT: 52
developers, a 17-point quiz gap without time savings, and six hindsight-coded interaction
patterns that track the outcome. Their own future work looks at longitudinal dissipation, not
within-session detection — the timing question is stated by their framing but not attempted.
Kosmyna et al. (2025, preprint) corroborate the direction in essay writing with EEG,
recall, and ownership measures — different domain, different instrument, cited as convergent
direction only. Becker et al. (2025) found experienced open-source maintainers *slowed* by
early-2025 AI tools — a productivity result on experts that undercuts "AI assistance is an
unqualified win" but says nothing about learning or prefixes. Liu et al. (2026) add a
convergent causal datapoint from a different task family: AI assistance reduces persistence
and hurts subsequent independent performance — same direction as the base trial, again with no
session-level detection and no intervention. Aouad, Lykouris and Zhong (2026)
supply the theoretical "why early matters": heterogeneous AI literacy compounds into skill
polarization, and if the compounding runs through early interaction differences, early
intervention is the lever their model predicts — their model, our motivating inference.

**Behavioral signatures of AI reliance.** Yao (2026) detects an AI-prompt signature (high
first-attempt acceptance, few debugging retries) in competitive-programming platform data and
shows that AI-prohibited evaluation gates screen for durable skill — the strongest existence
proof that the signal lives in behavior, but observational, cohort-level, retrospective, and
open-loop. Cao and Huang (2022) find a real-time behavioral proxy (gaze duration) more
informative than retrospective self-report for reliance in AI-assisted decision-making — a
different sensor (hardware eye tracking) and a different outcome (decision accuracy); whether
zero-hardware query-log features carry comparable signal for skill-formation risk is untested by
anyone, and is exactly what the feature-thinness question measures. The detector's *shape* —
a terminal learning outcome predicted from a partial behavioral log stream with
counting-based features at early checkpoints — is itself inherited from the learning-analytics
early-warning tradition, exemplified by MOOC dropout and success prediction (Gardner and
Brooks, 2018); we concede the shape and claim what that literature does not occupy: the
estimand (an erosive AI-interaction pattern, not course attrition), the decision clock
(queries and minutes within one session, not weeks in a course), and the measured human
prefix-labeling ceiling, for which early-warning work has no analogue. (Engagement disclosure: Cao
and Huang is search-confirmed but not full-text-read this cycle — ACM DL access failed — and
carries a pre-submission reading debt.)

**Just-in-time adaptive interventions: the loop template, credited.** The mobile-health JITAI
literature formalized decision points, tailoring variables, and proximal versus distal outcomes
(Nahum-Shani et al., 2018), and micro-randomized trials for intervention timing (Klasnja et al.,
2015). No JITAI work senses AI-interaction patterns or targets skill formation; we import the
vocabulary — tailoring variable: the running risk score; proximal outcome: post-nudge pattern
shift; distal outcome: quiz score — rather than reinventing it, and the micro-randomized design
is the pre-committed scale-up vehicle for timing questions. Our novelty claim is scoped
accordingly: outside purpose-built tutoring systems — whose closed-loop precedent is conceded
in the next paragraph — the first closed JITAI-style loop whose sensed state is an
AI-interaction pattern during authentic work and whose distal outcome is measured skill
formation.

**Appropriate reliance and cognitive forcing.** Buçinca, Malaya and Gajos (2021) showed that
cognitive forcing functions — interruption-based nudges — reduce overreliance on AI in
decision-making, at a user-experience cost; this is the nearest intervention class with RCT
evidence, and their finding that effects partly run through friction is a direct design input
here: it is why the placebo arm exists and why the gate carries an explicit annoyance budget
rather than treating false positives as free. The automation-bias tradition (Lee and See, 2004)
frames why delegation is the assistant's default happy path — the background condition that
makes erosive patterns the path of least resistance.

**Learner modeling and the design-principles response.** Intelligent tutoring systems have run
closed-loop learner modeling for three decades — Bayesian knowledge tracing (Corbett and
Anderson, 1995) and its successors — and the sharpest prior twin of our loop lives here: the
gaming-the-system line (Baker and colleagues, 2004–2008), whose "Scooter the Tutor"
deployment detected a maladaptive *interaction pattern* — not curricular mastery — from log
features, intervened live on detected students while sparing the rest, and measured learning
outcomes: a closed detect→intervene→verify loop on a learning outcome, two decades before
this design. We concede that precedent by name rather than claim the loop. What it does not
occupy is this setting: its sensed state is exploitation of a purpose-built tutor's own help
channel, whereas here the "tutor" is a general-purpose assistant that is itself the erosion
vector, the work is authentic rather than curricular, and the authorization machinery — a
measured human prefix ceiling and a sealed prevalence-anchored gate — has no analogue there,
because a tutor intervening on its own students never needed a licence to interrupt. The
nearest real-time education RCT is Tutor CoPilot (Wang et al., 2024), which delivers
expert-like guidance into live tutoring sessions — but its sensed state is tutoring context,
not a learner's AI-interaction pattern, and its outcome is tutoring quality, not skill
formation under the assistant itself. Finally, Agents-That-Teach (Mehra et al., 2026)
represents the design-principles answer to the same harm: build incidental learning back into
AI-assisted development via pedagogical scaffolding, prescribed open-loop — applied to all users,
unconditioned on any measured learner state. That stance taxes users already in protective
patterns (the 65–86% group needs no Socratic gate) and cannot tell whether its principles are
working mid-session. We are the closed-loop complement: measure first, intervene conditionally,
verify on the same quiz that established the harm — and if their designs prove adaptive on full
reading, the pre-committed repositioning is that we supply the measurement layer their
adaptivity would require.

## Conclusion

Skill erosion under AI assistance is causally established, pattern-mediated, and — so far —
visible only after the quiz. This paper's wager is that the drift is catchable in the query
stream while the session is still running, and it insists that the claim is only worth making
under discipline: a prognostic target instead of an ill-posed prefix-time diagnosis, a measured
human ceiling instead of an assumed one, an exact, sealed, prevalence-anchored gate before any
human is intervened on, a matched placebo that eats the reactivity story, and an internal
replication that keeps the borrowed baseline honest. The design is serialized so that evidence,
not optimism, decides how far it goes — and either branch produces knowledge the field lacks:
how early erosive patterns are visible at all, or whether a one-shot additive nudge can buy back
part of a 17-point comprehension loss without taxing the users who never needed it. Beyond this
study, the instrument itself — prefix-only, model-internal-free risk scoring with an auditable
authorization gate — is a template for measuring, at decision time, harms that today are only
measurable after they are locked in. The measured prefix ceiling and detection-lag distribution
will also bound what any future real-time protection can promise, a constraint the
design-principles literature currently has no way to state.

## References

> Mirrors `discussion/refs.bib` (the `.tex` build cites these via `\citep`/`\citet`). arXiv
> anchors re-verified against the arXiv export API on 2026-08-15; the three entries added in
> the 2026-08-21 review pass were verified against the live arXiv API on 2026-08-21; entries
> marked [debt] carry a pre-submission verification debt as recorded in `discussion_trace.md`
> and `review_2026-08.md` (which also lists prose-named, non-arXiv citation debt: the Baker
> gaming-the-system line and Simon 1989).

- Judy Hanwen Shen and Alex Tamkin. How AI Impacts Skill Formation. arXiv:2601.20245, 2026.
  [verified]
- Nataliya Kosmyna et al. Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI
  Assistant for Essay Writing Task. arXiv:2506.08872, 2025. Preprint. [verified]
- Joel Becker et al. Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer
  Productivity. arXiv:2507.09089, 2025. [verified]
- Song Yao. When the Scaffold Stays On: AI, Practice Style, and Screening in Elite Skill
  Formation. arXiv:2606.06253, 2026. [verified]
- Ali Aouad, Thodoris Lykouris, and Jingwei Zhong. Human-AI Productivity Paradoxes: Modeling the
  Interplay of Skill, Effort, and AI Assistance. arXiv:2605.11350, 2026. [verified]
- Rohit Mehra et al. Agents That Teach: Towards Designing Incidental Learning Back into
  AI-Assisted Software Development. arXiv:2607.06101, 2026. [verified]
- Grace Liu, Brian Christian, Tsvetomira Dumbalska, Michiel A. Bakker, and Rachit Dubey. AI
  Assistance Reduces Persistence and Hurts Independent Performance. arXiv:2604.04721, 2026.
  [verified 2026-08-21]
- Josh Gardner and Christopher Brooks. Student Success Prediction in MOOCs. arXiv:1711.06349,
  2018. [verified 2026-08-21]
- Rose E. Wang, Ana T. Ribeiro, Carly D. Robinson, Susanna Loeb, and Dora Demszky. Tutor
  CoPilot: A Human-AI Approach for Scaling Real-Time Expertise. arXiv:2410.03017, 2024.
  [verified 2026-08-21]
- Shiye Cao and Chien-Ming Huang. Understanding User Reliance on AI in Assisted Decision-Making.
  PACMHCI 6(CSCW2), 2022. [debt: full text unobtained this cycle]
- Inbal Nahum-Shani, Shawna N. Smith, et al. Just-in-Time Adaptive Interventions (JITAIs) in
  Mobile Health: Key Components and Design Principles for Ongoing Health Behavior Support.
  Annals of Behavioral Medicine 52(6), 2018. [canonical; page-detail debt]
- Predrag Klasnja, Eric B. Hekler, et al. Microrandomized Trials: An Experimental Design for
  Developing Just-in-Time Adaptive Interventions. Health Psychology 34(Suppl), 2015.
  [canonical; page-detail debt]
- Zana Buçinca, Maja Barbara Malaya, and Krzysztof Z. Gajos. To Trust or to Think: Cognitive
  Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making. PACMHCI
  5(CSCW1), 2021. [canonical; page-detail debt]
- John D. Lee and Katrina A. See. Trust in Automation: Designing for Appropriate Reliance.
  Human Factors 46(1), 2004. [canonical]
- Albert T. Corbett and John R. Anderson. Knowledge Tracing: Modeling the Acquisition of
  Procedural Knowledge. User Modeling and User-Adapted Interaction 4(4), 1995. [canonical]
- Charles J. Clopper and Egon S. Pearson. The Use of Confidence or Fiducial Limits Illustrated
  in the Case of the Binomial. Biometrika 26(4), 1934. [canonical]
- Donald B. Rubin. Multiple Imputation for Nonresponse in Surveys. Wiley, 1987. [canonical]
- Sture Holm. A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of
  Statistics 6(2), 1979. [canonical]

---

## Pre-handoff checklist

- **Organization/navigation** — problem → gap → obstacles → mechanisms → gated evaluation →
  related work, with no forward references to undefined terms; the gate is defined in the
  Problem Definition before any section relies on it.
- **Terminology discipline** — "prognostic risk," "human prefix ceiling," "first-crossing
  trigger," "sealed gate," "false-positive burden," "interpretation tree" each defined at first
  use and reused consistently; no internal stage IDs (`sp_*`, `m_*`, `rq_*` slugs, `H1`-style
  hypothesis labels, `C*`/`M*` module labels) appear in prose — RQ numbering in the Experiments
  section is the paper's own, not the pipeline's.
- **Notation** — $Q_i, L_i, Q_i^{(k)}, r_{ik}, c, G, \underline{\pi}_{90}, a, \mathrm{FPB},
  \mu_a, \Delta_*$ defined in the Problem Definition and reused throughout; no worked numeric
  example is included because no numbers exist yet (fabricating one would violate the
  no-fabrication rule); the one arithmetic illustration (the pass-table example in RQ5) is a
  property of the pre-registered decision table, not a result.
- **RQ framing matches outcomes** — all eight RQs are graded/quantitative (bounds, margins,
  medians, contrasts), each answered in its own subsection with an explicit falsification
  condition.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]`; only the explicit
  `[placeholder — fill in after experiments are run]` markers in Result slots, per the
  pre-registration convention.
- **Artifact plan** — planned releases: the feature-extraction and risk-model code, the frozen
  model manifest and pass table, the nudge template bank, the annotation protocol extension
  (prefix-labeling), and the OSF pre-registration; session transcripts release only as permitted
  by the IRB protocols and any data-use agreement.

## Hand-off

This is a pre-registered specification draft: experiments have not run, and every Result slot is
a placeholder. Natural next steps: execute Phase 0/1 from `experiment_design.md` (the standalone
protocol), or return to the discussion pipeline if a stage needs revision — e.g., if the G0
labeling pass finds the erosive base rate far from the design assumption, the gate's pass-table
arithmetic and RQ2's feasibility rationale must be re-derived before sealing anything.
