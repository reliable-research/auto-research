# Discussion — Candidate 1: "Skill-formation debt is real; the fix must live inside the assistant"

> **Full-paper framing (position = the paper's stance, not a position-track submission).**
> This document plans a FULL experimental paper: the H1.1 experiment itself — a real-time
> interaction-pattern classifier plus a three-arm RCT extension of Shen & Tamkin
> (arXiv:2601.20245) — with the "fix must live inside the assistant" argument as the
> Introduction's stance. Auto-research-discussion format: 6 stages, each with an internal
> critic → refine pass. Sources: `position_paper_pipeline_2026-08.md` (Candidate 1 + novelty
> ledger row 1), `topics/H1.1_.../README.md`, `topics/H1.1_.../digest.md` (N0–N12).

---

## Stage 1 — Problem definition

**Input (what is wrong, who holds it).** The field's dominant responses to AI-induced skill
erosion operate *outside* the learning interaction: usage bans and AI-free assessment gates
(institutionalized in ICPC/IOI-style proctoring, documented by Yao, arXiv:2606.06253) and
static, constant-on assistant design principles ("Agents That Teach", arXiv:2607.06101;
CHI'26 AlgoGPT-style friction). Both treat "AI use" as a monolithic exposure to restrict or
tax. Meanwhile the empirical literature keeps re-measuring *whether* erosion happens —
nobody has tested whether it can be *caught and corrected while it is happening*.

**Output (what the paper delivers).** A full experimental paper answering the question Shen
& Tamkin's own taxonomy makes askable: since 3 of their 6 interaction patterns erode skill
(<40% quiz) and 3 preserve it (65–86%), and the patterns are defined by query-log-level
behavior, (RQ1) can a classifier operating only on session-observable query-stream features
detect drift into an eroding pattern early in a session — measured as
precision-at-prefix-length against hindsight labels — and (RQ2) does a just-in-time
intervention triggered by that detection causally improve the post-task quiz outcome
relative to unintervened AI assistance, in a three-arm extension of the base RCT
(hand-coding / AI-assist-only / classify-and-intervene) using the same task and quiz
instrument for direct comparability with the published 50%/67% numbers? The stance the
results argue for: skill preservation as *targeted runtime behavior of the assistant*, not
access control and not blanket friction — "don't restrict access; instrument the
interaction."

**Critic:** The problem statement fuses two separable papers — a detection paper (RQ1,
implementable now, no human subjects) and an intervention RCT (RQ2, expensive, IRB-gated,
recruitment-heavy). If RQ2 is required for the headline claim, the project's critical path
runs through ~60–90 recruited participants (digest N6), which is not "implementable and
verifiable soon"; if RQ1 alone is the paper, the "fix must live inside the assistant" stance
outruns the evidence (a detector is not a fix).

**Refined:** Adopt the digest's own staged structure as the paper structure, with an honest
claim ladder. **Phase 1 (offline, no human subjects, buildable now)** is the paper's core
and hard gate: prefix-time classification of the six patterns from query streams, validated
against hindsight labels, reported as precision-at-prefix-length curves — this alone is a
publishable full-paper contribution (first operationalization of the RCT-validated taxonomy
as a real-time signal; digest CO1). **Phase 2 (three-arm RCT)** is designed, pre-registered,
and powered in the same paper, and run if/when Phase 1 clears its gate — either inside the
same submission (if timeline allows) or as the explicitly-scoped follow-on. The stance is
then calibrated per phase: Phase 1 licenses "erosion is detectable at interaction time,
therefore the assistant CAN act"; only Phase 2 licenses "and acting works." The paper never
claims the second on the first's evidence.

---

## Stage 2 — Motivation

**Why now.** (a) The causal anchor finally exists: before Shen & Tamkin (Jan 2026), the
deskilling debate ran on correlational and self-report data; now there is a clean RCT with
an effect size (d=0.738) *and* a behavioral taxonomy that decomposes it. (b) The wrong-layer
responses are hardening now — gates are institutionalizing and static design principles are
shipping — so evidence about the right layer has a closing policy window. (c) The coupling
this paper tests (RCT-validated patterns as tailoring variables in a closed detection→
intervention loop) is confirmed unoccupied (pipeline novelty sweep 2026-08-13): the
empirical deskilling papers exist, the FAccT framing paper exists, JITAI methodology exists
in mHealth/education — nobody has closed the loop inside a coding assistant.

**Binding evidence (only what the pipeline doc lists; [READ] unless noted):**
- [READ] **Shen & Tamkin, arXiv:2601.20245** — n=52 RCT, 50% vs 67% quiz (d=0.738, p=0.01);
  six-pattern taxonomy: eroding (<40%: full delegation, progressive reliance, iterative AI
  debugging) vs preserving (65–86%: generate-then-ask, hybrid code+explanation, purely
  conceptual). Carries both premises: the harm is real, and the harm is pattern-conditional.
  Also supplies the reusable instrument (task + quiz) for Phase 2's direct comparability.
- [READ] **Kosmyna et al., arXiv:2506.08872** — independent EEG corroboration, different
  task/instrument/population. Direction only; never magnitude.
- [READ] **Yao, arXiv:2606.06253** — observable "AI-prompt signature" in naturalistic
  submission logs; gates filter it but do not teach. Double duty: feasibility precedent for
  behavioral detection + evidence the restriction layer cannot fix formation.
- [READ] **Aouad, Lykouris & Zhong, arXiv:2605.11350** — formal skill-polarization
  conditions under heterogeneous AI literacy: why erosion compounds, and why early
  trajectory correction is the theoretically-indicated lever (digest N2's inference,
  flagged as ours).
- [NEEDS VERIFICATION — web-search-confirmed only] **Cao & Huang, CSCW2 2022** — real-time
  behavioral reliance proxy (gaze) precedent. Read in full before citing (ACM DL 403 noted
  in digest N3); until then, not load-bearing.

**Critic:** The motivation inherits a single-study dependency: the taxonomy that the entire
classifier is built on comes from one n=52 study, one library (Trio), one population — and
the six patterns were induced by qualitative coding, not validated as a stable behavioral
typology. If the patterns don't transfer to other tasks/populations, Phase 1's classifier is
fitting an artifact of one lab's codebook. The digest itself records that the "triple
corroboration" origin story was a miscount (two YouTube retellings of the same paper).

**Refined:** Make taxonomy-transfer an explicit measured question instead of an assumption.
Phase 1's labeling protocol replicates the base paper's codebook on *new* session data
(Stage 6), which means inter-rater reliability and pattern-frequency comparison against the
base paper come for free — if the six patterns fail to reappear in fresh data, that is
itself a reportable (and important) negative result about the taxonomy's stability, and the
paper's framing pivots to "which behavioral distinctions ARE stable enough to detect."
State the evidence base precisely everywhere: one RCT + one differently-instrumented
corroboration + one large-scale observational signature + one formal model; treat the base
paper's own caveat (real agentic products likely show larger effects) as a lower-bound
framing, not inflation.

---

## Stage 3 — Related work positioning

Named occupants from the novelty ledger (row 1), each concede-and-claim:

1. **"Agents That Teach" (arXiv:2607.06101)** — coins "Knowledge Debt," proposes SHIELD
   design principles.
   *Concede:* they own "assistants must be redesigned to preserve learning" as a design-
   principle program, and the debt framing.
   *Claim:* they explicitly do NOT propose detection — their prescriptions are constant-on
   and pattern-blind; we deliver the thing their framework lacks: a working prefix-time
   classifier over RCT-validated patterns plus an evidential template (three-arm RCT) for
   whether targeted intervention beats their static scaffolds — turning their design
   principles into a testable baseline condition rather than the end state.

2. **"Brainrot" (FAccT'26, arXiv:2605.03512)** — deskilling as an overlooked safety risk.
   *Concede:* they own problem legitimation — deskilling belongs on the safety/fairness
   agenda; our Introduction cites them as having settled "does this matter."
   *Claim:* they diagnose, we operationalize: the delta is a measurement instrument
   (precision-at-prefix-length on the erosion signal) and a causal test of the control loop
   — the step from "this is a harm" to "here is the harm's detector and its validated (or
   falsified) fix."

3. **JITAI literature (mHealth/education just-in-time adaptive interventions).**
   *Concede:* they own the loop architecture wholesale — tailoring variables, decision
   points, decision rules, proximal/distal outcomes — a decade of methodology we import
   explicitly rather than reinvent.
   *Claim:* JITAI has never been instantiated in coding assistants, and has never had
   RCT-validated tailoring variables for *skill formation*; our contribution is the coupling
   (ledger row 1's 🟢 cell): Shen & Tamkin's taxonomy as the first validated
   tailoring-variable candidate set, with Yao's signature as evidence the variables are
   observable without sensors or self-report — and Phase 1 is the first empirical test of
   whether they work as tailoring variables (i.e., are detectable at decision-point time).

(Cited but not built against, per the pipeline sweep: CHI'26 AlgoGPT — design-time friction,
which becomes a comparison condition in Phase 2's intervention design space, not just a
citation; arXiv:2602.20206 — static metacognitive scaffolds, same role.)

**Critic:** Two absence claims rot fast: "2607.06101 has no detection" and "JITAI never
imported to coding assistants" are universal negatives with a shelf life of one arXiv
listing — and for a *full* paper with a months-long build, the rot window is much longer
than for a position abstract. If a detection paper appears mid-build, the novelty argument
as written collapses.

**Refined:** (a) Schedule re-sweeps of both absence claims at each milestone (below), not
just at submission. (b) Shape the claim to survive a competitor detector: our delta is not
"first detector" but the *validated chain* — RCT-derived taxonomy → prefix-time detection
with honest precision-at-prefix curves → pre-registered causal intervention test with the
same instrument as the base RCT. A toy detector without hindsight-label validation, or
without the comparable outcome instrument, does not occupy this cell. (c) The full-paper
framing itself is the best rot insurance: an experimental contribution with artifacts
(classifier, labeled sessions, harness) survives a competing argument paper in a way a
position paper would not.

---

## Stage 4 — Sub-problems (argumentative sub-claims, each with evidence and weakest point)

**SC1. The erosion effect is real, causal, and pattern-conditional — so a detector has a
valid target.**
- *Evidence:* Shen & Tamkin's RCT split (same exposure, different patterns, 2× outcome
  difference); Kosmyna direction-corroboration; Aouad et al.'s compounding mechanism.
- *Weakest point:* pattern → outcome may be correlation within the treatment arm (patterns
  were not randomized; learners self-select into patterns, so a confounder — prior ability,
  metacognition — may drive both pattern and quiz score). Handle honestly: Phase 1 needs
  only "patterns predict outcomes" (true regardless of confounding); Phase 2's intervention
  arm is precisely the randomized test of whether *shifting* the pattern shifts the outcome.
  This is the paper's cleanest internal logic — say it in the Introduction.

**SC2. Restriction-layer responses cannot fix formation, so the interaction layer is the
one worth instrumenting.**
- *Evidence:* Yao — gates filter the signature (sort people) without changing practice, and
  within gated settings AI-style *practice* predicts higher performance for new entrants;
  Aouad et al. — uniform bans widen the gap under literacy heterogeneity.
- *Weakest point:* gates were built for assessment integrity, not pedagogy — attacking them
  as failed pedagogy is a straw man unless framed as "the field is *relying* on an
  assessment instrument to do pedagogical work." Concede gates' legitimate role explicitly.

**SC3. Eroding patterns are detectable from session-observable features at useful prefix
lengths.** (Phase 1's empirical claim — the paper's core.)
- *Evidence:* the patterns' own operationalizations are query-log-level (code-request vs
  explanation-request ratio, follow-up presence after code delivery, time-to-next-query,
  retry counts — digest M1); Yao proves usage-style signatures are machine-visible in
  naturalistic logs; definitional separability argument (a pattern defined by absence of
  follow-ups diverges from one defined by their presence at the first follow-up
  opportunity).
- *Weakest point:* prefix-time ≠ hindsight-time (digest C1): early queries are ambiguous
  across patterns, so precision may only be achievable late or only for the most distinctive
  pattern (full delegation). This is why precision-at-prefix-length is the headline metric
  and why the pre-registered gate (Stage 6) makes partial success reportable rather than
  fatal.

**SC4. A just-in-time, pattern-targeted intervention improves the skill-formation outcome
over unintervened assistance — and over blanket friction at equal productivity cost.**
(Phase 2's causal claim.)
- *Evidence template:* three-arm RCT with the base paper's instrument; JITAI methodology for
  decision rules and proximal outcomes; digest M4's intervention design space
  (comprehension-check appended to response; partial answer + guiding question) and M5's
  placebo-nudge reactivity control.
- *Weakest point:* a null here is genuinely ambiguous (bad intervention choice vs no effect
  — digest C2), and reactivity confounds (C3) mean even a positive needs the placebo
  control before a mechanism claim. Scope Phase 2's primary endpoint narrowly (quiz delta,
  intervene vs assist-only) and defer mechanism decomposition to the scale-up stage.

**Critic:** SC3 hides the project's real single point of failure: *where does Phase 1's
session data come from?* The base paper's transcripts may not be released; without them,
"implementable now without human subjects" is only true if an alternative source of
AI-assisted learning-session query streams exists that can be hindsight-labeled with the
six-pattern codebook. If Phase 1's data plan is hand-waved, the whole "buildable now" claim
is theater.

**Refined:** Make the data plan a first-class sub-problem with a source ladder, checked in
this order (Stage 6 details): (1) the base paper's own artifacts if released (check
arXiv/OSF/Anthropic repo first — one afternoon); (2) public developer–LLM conversation
corpora that contain multi-turn coding-assistance sessions (e.g., the DevGPT-style
developer–ChatGPT conversation datasets and similar public session corpora — availability
and licensing to be verified in M1, and the codebook's applicability to non-learning-task
sessions honestly assessed); (3) self-collected sessions from lab members / volunteers doing
an unfamiliar-library task under the base paper's protocol — small-n, no quiz needed for
Phase 1 since the label is the *pattern*, not the score, which keeps it outside
human-subjects outcome measurement (IRB status still to confirm; likely exempt-tier).
Rung 2/3 sessions labeled by two coders with the replicated codebook, κ reported. The rung
reached is reported in the paper; rung 3 alone (25–30 sessions, digest feasibility note)
suffices for a first precision-at-prefix curve.

---

## Stage 5 — Paper architecture (section skeleton + load-bearing figure/table per section)

Full-paper skeleton (CHI/CSCW/ICSE research-track shape); the stance lives in §1, the
evidence artifacts carry each section:

- **§1 Introduction — the stance.** Erosion is proven and pattern-conditional; restriction
  operates at the wrong layer; the open question is whether the assistant can catch and
  correct drift live. Contributions: (C1) first prefix-time operationalization of the
  RCT-validated taxonomy + honest feasibility curves; (C2) pre-registered three-arm causal
  design (+ results if Phase 2 runs in time); (C3) released classifier, labeled session
  set, and intervention harness.
  *Artifact:* evidence table — study × instrument × population × effect × what it does NOT
  show (the four [READ] anchors), establishing the honest evidence base in half a page.

- **§2 Background & related work.** The three concede-and-claim positionings (Stage 3) +
  gates-filter-don't-teach (Yao) + polarization theory (Aouad et al.).
  *Artifact:* a layer diagram — institutional gate / product design-time / interaction
  runtime — annotating which existing work lives at which layer and which layer is
  unoccupied (this figure IS the novelty claim drawn spatially).

- **§3 The detection target: patterns as tailoring variables.** — **the paper's centerpiece
  table.** **6 interaction patterns × quiz score × observable session features:** rows =
  the six patterns; columns = (a) published quiz-score band (<40% vs 65–86%, per-pattern
  values only where the base paper prints them, band labels otherwise), (b) the query-log
  features that operationally define each pattern (from the base paper's codebook;
  derivation flagged as ours), (c) which features are observable at prefix-time vs only in
  hindsight. Column (c) converts "detectable in principle" into a cell-by-cell inspection
  and pre-declares the hard cases (the two subtler eroding patterns).

- **§4 Phase 1 method: prefix-time classifier + hindsight-label validation.** Feature
  extraction from query streams; labeling protocol (replicated codebook, dual coders, κ);
  classifier (simple, interpretable first: logistic/GBM over running feature counts — the
  contribution is the validation methodology, not architecture novelty); evaluation at
  prefix lengths {1, 3, 5, 10 queries} vs trivial most-common-pattern baseline.
  *Artifact (headline figure):* precision-at-prefix-length curves, per pattern, with the
  pre-registered gate threshold drawn as a horizontal line.

- **§5 Phase 2 method: three-arm RCT extension.** Arms (hand-coding / AI-assist-only /
  classify-and-intervene); same task+quiz instrument as the base RCT; decision rule (flag →
  next response appends comprehension-check or delivers partial answer + guiding question,
  digest M4); detection-lag instrumentation (M3); power analysis anchored to d=0.738;
  pre-registration of gate threshold and primary contrast.
  *Artifact:* JITAI-mapping diagram — tailoring variable / decision point / decision rule /
  intervention option / proximal & distal outcome, each slot filled with this paper's
  concrete instantiation.

- **§6 Results.** Phase 1: curves, κ, pattern-frequency comparison vs base paper (taxonomy
  stability), detection-lag distributions. Phase 2 (if run): quiz deltas plotted directly
  against the published 50%/67% two-arm numbers.
  *Artifact:* the three-arm quiz-score plot with the base paper's published bars alongside
  (direct numeric comparability is this design's free gift — display it).

- **§7 Discussion + threats.** Digest N10's five threats verbatim as the seed (proxy
  validity, reactivity, Trio-population scope as lower bound, multiple-comparison
  discipline via pre-registration, transcript-reuse fidelity); implications for assistant
  design standards (telemetry, intervention RCTs as the evidence bar).

**Critic:** §3's centerpiece table has a provenance risk: the pipeline doc gives band-level
scores ("<40%", "65–86%"), and the feature column is our reconstruction of their
qualitative codebook. If the table silently mixes published numbers with our inference, it
commits the exact grounding sin this repo's discipline exists to prevent, and a reviewer
who opens the source paper will find the seams. Separately, §4's "simple classifier"
choice will draw a "why not an LLM-judge / sequence model" methods objection.

**Refined:** Partition the table's provenance typographically: published values with
citation anchors; bands marked as bands; the operationalization column footnoted as
"derived from [2601.20245]'s pattern descriptions"; column (c) labeled as this paper's
analysis. Extract every per-pattern statistic the base paper actually prints during M1 (one
pass feeds both §3 and the labeling codebook). On the classifier: pre-empt the objection by
running the simple interpretable model AND one stronger sequence baseline (an LLM-judge
prompt over the session prefix is cheap to add and is itself an interesting comparison —
does an LLM recognize erosion-prone use of LLMs?); frame model choice as ablation, keep the
methodological claim (prefix-time validation against hindsight labels) model-agnostic.

---

## Stage 6 — Experiment specification (implementable; Phase 1 buildable now)

### Phase 1 — offline prefix-time classification (no human-subjects outcome measurement)

**Step 0 — data source ladder (first week):**
1. Check whether Shen & Tamkin released session transcripts/artifacts (arXiv page, OSF,
   Anthropic repos). If yes: rung 1, use directly.
2. Else survey public developer–LLM session corpora (DevGPT-style datasets and successors)
   for multi-turn coding-assistance sessions; verify license + applicability of the
   codebook; if usable: rung 2.
3. Else collect 25–30 fresh sessions: volunteers with Python experience do an
   unfamiliar-library task (Trio or comparable) with an assistant, logging query streams;
   no quiz required for Phase 1 (labels are patterns, not outcomes); confirm IRB
   exempt-tier before collection.

**Step 1 — labeling harness:** replicate the base paper's six-pattern codebook from its
published descriptions; two coders label complete sessions; report Cohen's κ; adjudicate
disagreements; freeze the hindsight-label set. Also report pattern frequencies vs the base
paper (taxonomy-stability check from Stage 2's refinement).

**Step 2 — feature extraction:** per query: type (code-request / explanation-request /
hybrid), follow-up-after-code indicator, time-to-next-query, retry/error signals; running
counts and ratios over the prefix (digest M1's feature list — session-observable only, no
model internals).

**Step 3 — classifier + evaluation:** train on session prefixes truncated at {1,3,5,10}
queries; leave-one-session-out CV (small n); models: logistic/GBM + one LLM-judge baseline.
Report precision/recall per pattern per prefix length vs the trivial most-common-pattern
baseline; report detection lag (first-flag query index) per session.

**Pre-registered gate (from digest N6/N8):** proceed to Phase 2 iff eroding-pattern flag
precision ≥70% at a prefix ≤ half the median session length — with the threshold re-derived
from the actual base rates in the labeled set before being frozen (digest N8's own caveat
that 70% is a placeholder), and the full curve reported regardless of gate outcome.

### Phase 2 — three-arm RCT (pre-registered in the paper; run on gate pass)

~60–90 participants, three arms (hand-coding / AI-assist-only / classify-and-intervene);
base paper's task + quiz instrument; intervention = single fixed nudge chosen from the M4
design space by Phase-1 flag frequencies; primary endpoint: quiz score,
intervene-vs-assist-only (t-test / Cohen's d, same family as the base paper); secondary:
replicate the base 50%-vs-67% gap in our own control arms before trusting the three-arm
contrast; descriptive: detection-lag × outcome cross-tab. Scale-up (out of scope for the
first paper, stated as future work): placebo-nudge reactivity control (M5),
pattern-matched interventions (C2), second library (M6/C5).

**Falsification conditions (printed in the paper):**
1. Phase 1: precision statistically indistinguishable from the trivial baseline for ALL six
   patterns at every prefix length → the real-time premise fails as scoped; publishable as
   a negative result with the taxonomy-stability analysis, but the stance must retreat to
   post-hoc measurement.
2. Phase 1: six patterns fail to reappear in fresh data (κ low, frequencies incompatible)
   → the taxonomy is codebook-artifact; pivot the paper to "which distinctions are stable."
3. Phase 2: intervene arm ≈ assist-only arm → targeted JIT intervention doesn't help (as
   instantiated); report against gate-passing detection to show the failure is in the
   intervention, not the detector.
4. External: erosion shown to be exposure-duration-driven rather than pattern-driven →
   the tailoring-variable premise collapses.

**Anticipated reviewer attacks → responses:**
- *"Patterns are self-selected; pattern→score is confounded."* → Correct, and that is
  exactly what the randomized intervention arm tests; Phase 1 needs only predictive, not
  causal, validity (SC1's logic).
- *"n is small everywhere."* → Matched to the base paper's own scale for comparability;
  leave-one-out CV + pre-registration; effect-size anchor d=0.738 makes the power analysis
  concrete.
- *"Hindsight labels from your own coders, not the original authors."* → κ reported;
  codebook replication is itself a contribution (taxonomy stability); rung-1 data used if
  available.
- *"The intervention is one fixed nudge — a null is uninformative."* → Conceded and
  pre-scoped: primary claim is the detector; the RCT is powered for one contrast and the
  design space is explicitly staged for follow-up (digest C2's own resolution).
- *"Why should the assistant do this rather than the IDE/platform?"* → The interaction
  layer is the claim; the assistant is the canonical host because only it can change the
  pedagogy of its own next answer (partial answer + guiding question), which is the
  intervention itself.

**Critic:** The gate design creates a perverse incentive the paper must not fall into: if
Phase 1 lands just under threshold, there will be pressure to tune features/models until it
passes — turning a pre-registered gate into garden-of-forking-paths theater. And the
LLM-judge baseline creates a subtle leakage risk: an LLM judging LLM-assistance transcripts
may keyword-match rather than pattern-match, inflating apparent feasibility.

**Refined:** Freeze the gate protocol before touching data: feature list, model families,
threshold-derivation rule, and number of allowed iterations are written into the
pre-registration (OSF) generated in M1; any post-freeze exploration is reported in a clearly
marked exploratory subsection. For the LLM-judge: include a text-ablated control (features
only, no raw text) so the comparison separates behavioral-signal detection from lexical
shortcut; if the judge beats the feature model only with raw text access, say so — that is
a finding about what the signal is, not an embarrassment.

---

## Venue plan (full research track, not position track)

| Window (verify exact dates at M1) | Venue | Fit |
|---|---|---|
| ~Sep 2026 (CHI 2027 papers) | **CHI 2027** | Likely too early for Phase 1 results — skip unless rung-1 data appears immediately |
| Quarterly cycles (Jan/Apr/Jul 2027) | **CSCW 2027/2028 cycles** | Best fit for Phase-1(+pre-registered-Phase-2) paper: HCI methods, RCT extension, reliance literature home turf |
| ~Mar–Apr 2027 (ICSE 2028 research track) | **ICSE 2028** | Fit if framed as developer-tooling/SE-education instrument; SE audience values the Yao connection |
| Fallbacks | TOCHI (rolling), CSEd venues (ICER ~Mar), EMSE journal | Rolling safety nets |

Strategy: target the **first CSCW 2027 cycle reachable with Phase 1 complete** (likely the
Apr or Jul 2027 deadline); if Phase 2 completes in time, the combined paper upgrades to the
next cycle rather than delaying the Phase-1 submission. The position-track outlets from the
earlier plan are dropped per the full-paper decision; the stance survives as §1.

## Time-to-draft / time-to-build estimate

Phase 1 is the critical path: ~6–8 working weeks (data ladder 1–2 wks; labeling 2 wks;
features+models+evaluation 2 wks; writing 2 wks), consistent with the digest's 2–3
person-week classifier estimate plus labeling and writing. Three milestones (targeting a
Phase-1 paper ready for the first 2027 CSCW cycle, with slack):

- **M1 — by Sep 15, 2026: data + protocol frozen.** Artifact check for base-paper
  transcripts done; data rung selected; codebook replicated from the base paper (extracting
  every printed per-pattern statistic — feeds §3's table); OSF pre-registration drafted
  (features, models, gate rule); absence-claim re-sweep #1 (2607.06101 detection; JITAI in
  coding); Cao & Huang read in full or struck.
- **M2 — by Nov 15, 2026: Phase 1 complete.** Sessions labeled (κ reported), classifier +
  baselines run, precision-at-prefix curves and detection-lag distributions final; gate
  verdict recorded; Phase 2 power analysis + IRB submission if gate passes; absence-claim
  re-sweep #2.
- **M3 — by Jan 31, 2027: full draft submission-ready.** All sections drafted per Stage 5
  skeleton with provenance-partitioned tables; falsification/threat sections folded in;
  cold read + internal critic pass; submit to the nearest CSCW cycle (or hold 4–6 weeks for
  Phase-2 data if the gate passed and recruitment is on schedule).

---

## Hypothesis statement (falsifiable, one sentence)

A classifier using only session-observable query-stream features can flag a learner's drift
into one of Shen & Tamkin's three skill-eroding interaction patterns within the first half
of a session at ≥70% precision (Phase 1), and a just-in-time nudge triggered by that flag
raises post-task quiz scores significantly above the AI-assist-only arm in a three-arm
replication using the base paper's own instrument (Phase 2).

## Implementation checklist (build order)

1. Artifact check: base-paper transcripts / OSF / repo (one afternoon; decides data rung).
2. Codebook replication doc from arXiv:2601.20245's pattern descriptions + extraction of
   all printed per-pattern statistics.
3. Data acquisition per ladder (rung 1 reuse / rung 2 public corpus vetting / rung 3
   25–30-session collection; IRB exempt-tier confirmation for rung 3).
4. Dual-coder hindsight labeling + κ + pattern-frequency stability check.
5. Feature extractor over query streams (type, follow-up indicator, timing, retries;
   running prefix counts).
6. OSF pre-registration freeze (features, model families, gate-threshold derivation rule).
7. Classifiers: logistic/GBM + LLM-judge baseline (+ text-ablated control); prefix-length
   evaluation harness; leave-one-session-out CV.
8. Precision-at-prefix curves, detection-lag stats, gate verdict.
9. Paper build per Stage 5 skeleton (§3 table + §4 headline figure first).
10. On gate pass: Phase 2 — IRB full protocol, intervention harness (M4 nudge in the
    assistant response path), recruitment, three-arm run, primary contrast.

## Verification criteria

- **Publishes (positive):** eroding-pattern precision ≥70% at ≤ half-session prefix for at
  least the most distinctive pattern class, beating the trivial baseline with CIs clear of
  it → Phase-1 full paper (detection feasibility + methodology + artifacts); Phase-2
  positive (intervene > assist-only, p<.05, non-trivial d) upgrades to the closed-loop
  causal paper.
- **Publishes (negative but informative):** taxonomy fails stability in fresh data, or
  precision fails everywhere despite clean κ → negative-result paper on the limits of
  real-time erosion detection (the field currently assumes nothing either way; both
  directions are informative).
- **Kills it:** cannot assemble ANY labelable session corpus (all three rungs fail), or
  coder κ stays <0.4 after adjudication (patterns not reliably codeable even in hindsight)
  → the construct itself is not measurable as scoped; retire to the position-only form of
  the argument.
