# Discussion: T3.2 — Why Soft Policies Rot Faster: Salience, Framing, and the Asymmetric Decay of In-Context Constraints (软政策-硬规范衰减不对称的机制)

> Structured 6-stage research discussion (auto-research-discussion style). Each stage is
> drafted, then attacked by an internal critic, then refined. Built from
> `README.md` + `digest.md` (reverse digest, tags [GIVEN]/[HYPOTHESIS]/[PLACEHOLDER]
> preserved by reference). Audit context: KEEP-TOP; window-flexible (FSE Oct 2 or
> ICLR Sep 25); label [机制] (mechanism study). Date of this discussion: 2026-08-13.

---

## Stage 1 — Problem Definition

**Draft.** Deployed LLM agents carry two tiers of in-context constraints: *soft
organizational policies* (软政策 — style, scope, business-preference rules injected via
system prompt only) and *hard safety norms* (硬规范 — refusal behaviors reinforced in
weights during alignment training). The seed premise [GIVEN]: adherence to soft policies
decays roughly **8x faster** than adherence to hard norms over long-horizon interaction
("原论文报告约 8 倍差异"). The question is *why*. Three candidate mechanisms:

1. **Salience** — the constraint's contextual prominence (position in context, repetition
   count) erodes as the conversation grows and as context-management operators rewrite the
   window.
2. **Framing** — the wording strength used to state the constraint (advisory "we prefer
   that you…" vs. imperative "you must never…").
3. **Pretraining/alignment prior** — hard norms are backed by weight-level reinforcement;
   soft policies exist *only* in context, so the decayable surface is the entire
   constraint, not just its contextual restatement.

The study is a controlled ablation that orthogonalizes these three factors on
content-matched soft/hard constraint pairs and attributes the decay-rate gap to them via
variance decomposition over fitted survival curves. Crucially — per the audit's KEEP-TOP
framing — the decay is studied not only under *natural context growth* (turns accumulate)
but under *context compaction* (the window is actively rewritten by a compaction operator:
truncation, keep-top pinning, LLM summarization), because compaction is the regime in
which production agents actually live and the regime in which soft-policy rot is reported
anecdotally to be worst [VERIFY — anecdotal/relayed, no citable measurement yet].

**Outcome shape:** per-condition adherence survival curves + decay half-lives + a
dominance-analysis attribution of the soft/hard hazard gap to salience, framing,
compaction-interaction, and prior, with a probe-reactivity bound.

**Critic:** Three problems. (a) The 8x number is a relayed premise with no resolved
citation — the README says "原论文" but never names it. If the study cannot even locate
the source, the headline framing ("explain the 8x gap") is built on sand; and if the gap
does not replicate in a matched-pair design, the paper has no phenomenon. (b) The draft
quietly merges two distinct regimes — *in-context decay over turns with the constraint
still verbatim present* vs. *decay under compaction where the constraint text may be
literally deleted or paraphrased away*. These have different mechanism menus: under
compaction, "salience" partly collapses into "survival of the constraint text through the
operator," which is a property of the *operator*, not of the model's attention. Conflating
them makes the mechanism attribution uninterpretable. (c) "Soft vs. hard" as defined risks
being confounded with "in-context-only vs. weight-backed" — which is not a bug, it *is*
mechanism 3 — but then the type factor and the prior factor are partially the same thing,
and the draft should say so instead of listing them as if independent.

**Refined:** The problem is defined as a **two-regime, four-factor mechanism-attribution
study**. Regime A (growth-only): constraint stays verbatim in context; decay over turns
measures attention/behavioral drift (salience-as-attention, framing, prior). Regime B
(compaction): a compaction operator rewrites context at scheduled points; decay
additionally reflects textual survival of the constraint through the operator
(salience-as-survival). The two regimes are run under one harness so their curves are
directly comparable, and the compaction operator is an explicit manipulated factor, not
background noise. The type/prior near-identity is handled head-on: "hard norm" is
*operationally defined* as a constraint the model already enforces at a measurable rate
with **no injection at all** (the M5 zero-shot compliance proxy), and "soft policy" as one
with near-zero no-injection compliance; the prior factor is thus measured per-constraint
as a continuous covariate rather than assumed from the type label. Stage-0 of the study
(before any mechanism claim) is: (i) locate and verify the source of the ~8x figure
[VERIFY — must resolve to a citable paper or be reframed as "a folklore-level effect we
first measure cleanly"], and (ii) replicate the gap directionally in the matched-pair
design. If (i) fails, the paper's framing shifts from "explaining a reported 8x gap" to
"first controlled measurement + mechanism attribution of soft/hard decay asymmetry" —
which is, if anything, a stronger novelty claim.

---

## Stage 2 — Motivation

**Draft.** Why this, why now:

- **The failure is real and governance-relevant.** A long-running agent that silently
  drops "always disclose you are an AI to customers" or "never quote prices without legal
  review" fails its operator long before it fails any safety eval. Safety-focused
  evaluation does not watch this surface (OffTopicEval makes the same deployment argument
  for operational-scope policies).
- **The fix-shipping crowd has skipped the explanation.** The practical response to
  constraint rot is already an industry pattern: pin the system prompt, re-inject policies
  after compaction, restate every k turns ("pinning-repair"). These are fixes shipped
  without a mechanism story — nobody has measured *which* mechanism the fix addresses, so
  nobody knows when the fixes will fail. A mechanism study is the non-obvious move in a
  space where everyone else ships mitigations.
- **The scaffolding-rot adjacency.** Anthropic engineering guidance is reported to advise
  that prompt scaffolding "rots" against model upgrades and context operations [VERIFY —
  relayed claim from engineering-practice commentary, not a verified primary source; must
  be traced to a citable document or dropped]. If salience dominates, scaffolding rot is
  a placement problem (cheap fix); if the prior dominates, no prompt engineering closes
  the gap and durable soft policy requires training-time reinforcement — a result with
  direct product implications.
- **Actionability is conditional on attribution** [digest N2-M3]: salience-dominant →
  placement/restatement guidance; framing-dominant → wording guidance; prior-dominant →
  the negative result that prompt-level policy is intrinsically second-class, which is the
  most publishable outcome of the three.
- **Timing.** The ablation is runnable in weeks on API + one open-weights model. Two
  windows are live: ICLR (abstract/paper ~Sep 25 [VERIFY exact 2027-cycle dates]) and FSE
  (~Oct 2 [VERIFY]). The ingredients (survival modeling of dialogue failure, shallow-
  alignment diagnostics, wording-sensitivity measures) all exist as separate 2025-era
  papers; the factorial unification is unclaimed territory — but plausibly not for long.

**Critic:** (a) Two [VERIFY] tags are load-bearing: the 8x source and the Anthropic
scaffolding-rot guidance. The motivation currently leans on both; if both dissolve, what
remains? (b) "Nobody has measured which mechanism" is asserted, not searched — digest N3's
absence_comment explicitly orders a Semantic Scholar pass for exact-precedent phrases
("constraint decay asymmetry", "system prompt adherence over turns") before submission;
the motivation should not overclaim priority before that search runs. (c) The venue pair
is odd — FSE wants an SE artifact/engineering story, ICLR wants an ML finding; writing one
paper for both risks writing for neither. The motivation should commit to a primary
framing.

**Refined:** The motivation is restructured to survive both [VERIFY] failures. Load-
bearing core (no verification needed): (1) soft policies live only in context, so any
context operation is an existential threat to them in a way it is not to weight-backed
norms — this asymmetry is *structural*, worth measuring whether the folklore multiplier is
8x or 3x; (2) mitigation practice (pinning, re-injection) is widespread and mechanism-
blind, so a mechanism result immediately re-prices existing fixes. Color, clearly tagged:
the 8x figure [VERIFY, downgrade to "reported" until sourced] and the scaffolding-rot
guidance [VERIFY, relayed; use only as an aside if traceable]. Priority claim is
conditioned: "to our knowledge, and pending the pre-submission precedent search (Semantic
Scholar, queries fixed in digest N3), no matched-design comparison exists." Primary
framing decision: **mechanism/empirical study for ICLR** (the finding is the headline;
survival modeling and dominance analysis are ML-native); FSE is the fallback window with
a re-skinned intro (policy adherence as a software-reliability property of LLM-integrated
systems) only if the ICLR window is missed — one primary target, not a straddle.

---

## Stage 3 — Related Work

**Draft.** Named priors with boundary statements (all corpus-grounded per digest N3 unless
noted):

- **[SafetyFewTokensDeep, OpenReview:6Mxhg9PtDE]** — "Safety Alignment Should Be Made More
  Than Just a Few Tokens Deep": characterizes the *alignment prior* (per-token KL,
  aligned-vs-base) for hard refusals. Boundary: token depth within one response, never
  turn depth within a dialogue; never touches in-context soft policies.
- **[TimeToInconsistency, OpenReview:88C7vSdn0t]** — survival modeling of multi-turn
  failure (first inconsistency = event, right-censoring). Boundary: observational
  covariates; predicts *when*, never manipulates wording/position/repetition, so cannot
  attribute *why*.
- **[SinkTrack, OpenReview:Gg1aPETCL6]** — instruction forgetting as positional-salience
  loss; training-free attention-sink anchoring fix. Boundary: *presupposes* the salience
  mechanism and mitigates it; never tests it against framing/prior alternatives.
- **[PrefEval, OpenReview:QWunLKbBGF]** — soft preference adherence across long distractor
  spans (LMSYS-Chat-1M padding). Boundary: one constraint tier only; varies distractor
  length, never the constraint statement itself.
- **[OffTopicEval, OpenReview:EcIyiJrajc]** — policy-conditioned agents, accept/refuse
  tradeoff on out-of-scope queries. Boundary: single-shot policy adherence, no decay
  dimension, no factorial manipulation.
- **[SafeDialBench, OpenReview:KFjtRqVnKH]** — multi-turn safety consistency under
  jailbreak pressure. Boundary: hard-norm side only, adversarial-only; no benign decay,
  no soft comparison arm.
- **[ICFBench, OpenReview:hcJywRYc3n]** — *intended* forgetting of revoked context via
  paired NoForget/Forget design. Boundary: the complementary failure (unintended decay of
  still-valid constraints) is out of scope; but its paired-condition causal-isolation
  logic is the template for our reactivity control (M6).
- **[TARE, OpenReview:YEBDvqsniH]** — wording/paraphrase sensitivity ("textual
  sharpness") as worst-case over a semantic neighborhood. Boundary: point-wise, single-
  shot; never longitudinal durability of a constraint.
- **[RECAST, OpenReview:90tCp2KszA]** — dual-mode constraint verification (rule-based +
  LLM-judged). Boundary: verifier taxonomy reused here; no decay or type-asymmetry
  content.
- **[LLMsGetLost, Laban et al., arXiv:2505.06120]** (non-corpus, verified) — 39% average
  multi-turn degradation, aptitude-vs-unreliability decomposition. Boundary: task
  performance, not constraint adherence; no stratification by constraint type.
- **Pinning/compaction line.** The README itself cites no specific pinning or compaction
  papers [VERIFY — its citation list is the digest's corpus set above; the
  "pinning-repair crowd" referenced in our audit context is engineering practice
  (system-prompt pinning, post-compaction re-injection, context-summarization memory
  managers in agent frameworks) plus a fast-moving arXiv literature on context
  compression/summarization memory. Before submission, run the precedent search and cite
  the strongest 2-3 representatives of (i) compaction/summarization memory ops and (ii)
  prompt re-injection heuristics; until then this line is held as a placeholder rather
  than fabricating citation keys].

**Gap statement:** each ingredient exists separately — soft-tier adherence (PrefEval,
OffTopicEval), hard-tier persistence (SafeDialBench), decay-as-survival (TimeToInconsistency),
salience mechanism (SinkTrack), framing sensitivity (TARE), prior depth
(SafetyFewTokensDeep), verifiable checking (RECAST) — but **no work compares soft vs.
hard decay in one matched design, and none manipulates the three candidate mechanisms
factorially, and none crosses any of this with compaction operators.**

**Critic:** (a) The honest weakness: all ten anchors are OpenReview-corpus or one arXiv
paper; the compaction axis — which the refined problem definition promoted to a first-
class factor — has *zero* cited prior work. A reviewer will ask "you study decay under
compaction and cite no compaction literature?" (b) The boundary statements are digest-
inferred gap claims (N4 is all HYPOTHESIS-source), not author admissions; the paper must
phrase them as "X does not do Y," never "X admits Y." (c) Missing adjacent line: context-
window eviction / KV-cache and memory-management papers, and the "instruction hierarchy /
system-prompt privilege" line (e.g., OpenAI's instruction-hierarchy work) which is
directly about why system-level constraints should dominate — arguably the closest thing
to a prior-mechanism intervention [VERIFY — from memory, must confirm].

**Refined:** Related work is organized into four lanes with one-sentence boundaries:
(1) *what decays* (PrefEval, OffTopicEval, SafeDialBench, LLMsGetLost — outcome tier
coverage, no cross-tier matching); (2) *how to model decay* (TimeToInconsistency —
adopted, extended from observational to interventional); (3) *candidate mechanisms studied
in isolation* (SinkTrack = salience, TARE = framing, SafetyFewTokensDeep = prior — each
studies exactly one and cannot see the asymmetry); (4) *apparatus* (RECAST verifiers,
ICFBench paired-isolation logic, LMSYS-Chat-1M padding — reused, credited). A fifth lane,
**context-operations** (compaction/summarization memory, prompt pinning/re-injection,
instruction-hierarchy training), is flagged as mandatory pre-submission literature debt
with fixed search queries [VERIFY]; the paper's novelty claim is stated conditionally on
that search coming back clean, and phrased throughout as third-party gap analysis rather
than imputed author admissions.

---

## Stage 4 — Sub-problems

**Draft.**

- **SP1 (the hard part): De-confounding the three mechanisms.** In the wild, hard norms
  are imperatively worded AND prominently placed AND weight-reinforced (digest C1). Only
  factorial manipulation on content-matched pairs separates them — and the prior can
  never be manipulated, only measured (C4), so the design is intrinsically asymmetric:
  two factors experimental, one correlational.
- **SP2: Matched pair construction with mechanical verifiability.** Soft/hard pairs
  matched on topic, length, syntax, and — critically — both members must have *rule-
  checkable* compliance criteria (C3). Soft constraints are naturally graded; restricting
  to mechanically checkable ones narrows the construct but buys non-circular ground truth.
- **SP3: Probe reactivity.** Measuring adherence requires probing, and probes can refresh
  the constraint's salience (C2) — the instrument perturbs the measurand. Needs a
  measured bound, not an assumption.
- **SP4: Prior-strength measurement.** "Alignment prior strength" is unobservable;
  proxies (no-injection compliance, base-vs-instruct delta, per-token KL) are confounded
  with model family and recipe (C4).
- **SP5: Compaction-operator realism.** A compaction factor is only meaningful if the
  operators are the ones production systems actually run (keep-top truncation,
  LLM summarization, verbatim-pin + summarize-rest). Toy operators would make the
  headline regime unconvincing; but real operators (e.g., a frontier model's built-in
  compaction) are black boxes that confound the operator with the model.

**Critic:** (a) SP1 is correctly named the hard part, but the draft understates *why* it
is hard even with a factorial: framing and salience manipulations apply to the injected
statement, while the prior attaches to the *content* — so the type contrast rides on the
pair bank's content matching (SP2), meaning SP1's validity is hostage to SP2's quality.
Say so explicitly: SP2 is the construct-validity linchpin (digest Claim 3), SP1 is the
inferential hard part, and they fail jointly. (b) SP5 as drafted has no resolution
sketch. (c) Missing sub-problem: analysis-validity — a 4-factor × survival-model design
invites researcher degrees of freedom (digest t5); with a 6-week clock, pre-registration
discipline is not optional garnish, it is what makes a fast mechanism paper credible.

**Refined:** Five sub-problems, with dependencies made explicit:

1. **SP1 — Mechanism de-confounding (hard part, inferential).** Two experimental factors
   (framing via wording variants; salience via position × repetition × compaction-
   survival) + one measured covariate (prior, SP4). Validity is *conditional on SP2*:
   if pairs are unmatched, the type×turn coefficient absorbs difficulty differences and
   every attribution downstream is garbage. Failure mode named in the paper.
2. **SP2 — Pair bank as construct-validity linchpin.** 40 pairs; matching on topic
   domain, token length ±10%, verifier type; wording variants checked for semantic
   equivalence (embedding threshold + human audit); acceptance gate: independent raters
   cannot distinguish pair members' *difficulty*, only their *type*.
3. **SP3 — Reactivity bounding.** Anti-reactivity probe authoring (no constraint
   keywords) + within- vs. between-conversation probing contrast on calibration cells;
   run FIRST (digest sequencing: RQ_INF_2 gates everything).
4. **SP4 — Prior proxy triangulation.** Three imperfect instruments, entered as
   covariates; attribution to "prior" is explicitly a diagnosis of exclusion
   (residual), stated as an upper bound on the correlational claim.
5. **SP5 — Compaction operators, three-tier realism.** Tier 1: transparent scripted
   operators we control (keep-top-k, keep-first+last, summarize-with-fixed-prompt) —
   primary, fully reproducible. Tier 2: one production framework's real compaction
   [VERIFY availability] as an ecological-validity spot check, reported descriptively,
   never entered into the factorial. Tier 3 (out of scope, stated): provider-internal
   black-box compaction. Plus **SP6 (process): pre-registration** — model spec, factor
   set, gate criteria frozen before scale-up; all cells reported.

---

## Stage 5 — Methods

**Draft.** The core is the **ablation matrix**:

**constraint type (soft/hard) × framing (advisory/standard/imperative) × salience
(position: sys-head / sys-tail / mid-conversation × repetition: 1/3/5) × compaction
operator (none / keep-top / summarize / summarize-with-pin)** — with mechanical violation
detection at scripted probes, survival-curve fitting, and dominance-analysis attribution.

Components (digest M1-M6, extended):

- **M1 — Matched constraint-pair bank.** 40 soft/hard pairs (pilot: 20), 3 wording
  variants each, drawn from OffTopicEval-style operational policies + PrefEval-style
  preferences (soft) and standard refusal categories (hard); IFEval-style rule-checkable
  compliance criteria wherever possible. Equivalence checks per SP2.
- **M2 — Salience controller.** Places the statement (3 loci), restates 1/3/5 times at
  scheduled turns, holds total context tokens constant via length-matched filler.
- **M2b — Compaction controller (new vs. digest).** At scheduled turns (e.g., every 20
  turns or at a token budget), applies the assigned operator to the transcript: `none`
  (growth-only regime A); `keep-top` (retain system prompt + last k turns verbatim —
  the audit's KEEP-TOP condition); `summarize` (fixed summarization prompt over evicted
  span, summary replaces it); `summarize+pin` (summarize, but constraint statements are
  verbatim-pinned — the pinning-repair fix, included as a *manipulated mitigation cell*
  so the fix crowd's remedy is evaluated inside the mechanism design). Logs whether the
  constraint text survived each compaction verbatim / paraphrased / deleted — the
  *textual-survival* mediator variable.
- **M3 — Long-horizon probe environment.** 30-turn (pilot) / 100-turn (scale-up)
  conversations padded with LMSYS-Chat-1M distractor turns; probes every 5 turns; probes
  authored under the anti-reactivity rule (no constraint mention or topic keywords).
  **Mechanical violation detection:** primary metric uses rule-based programmatic
  checkers ONLY (format/lexical/refusal-trigger checks, RECAST's deterministic mode);
  LLM-judged soft constraints are a separately-reported secondary stratum with 10% human
  audit, κ ≥ 0.8 gate. No LLM judge inside the headline number.
- **M4 — Survival modeling + attribution.** Discrete-time hazard (cloglog link), event =
  first sustained violation, right-censoring; mixed effects: hazard ~ turn × type ×
  framing × salience × compaction + (1|pair) + (1|model). Soft/hard gap = type×turn
  coefficient; mechanism shares via dominance analysis / partial-R²; compaction regime
  adds the mediation read-out: how much of the compaction-cell gap is explained by
  textual survival (operator property) vs. residual behavioral decay (model property).
- **M5 — Prior proxy battery.** No-injection zero-shot compliance; base-vs-instruct
  delta (open-weights pair); optional per-token KL on violating continuations. Covariates
  only.
- **M6 — Reactivity calibration.** Within- vs. between-conversation probing on 4
  flagged cells (~480 extra conversations); global correction if the delta is small and
  type-uniform; design escalation if type-dependent (pre-registered decision rule).

**Critic:** (a) The full matrix is now 2×3×(3×3)×4 = 216 cells before models and seeds —
untenable in six weeks; the draft must commit to a pilot fraction and say which
interactions are estimable and which are aliased. (b) `summarize+pin` is doing double
duty as a factor level and a mitigation baseline; cleaner to define the factorial over
{none, keep-top, summarize} and treat `summarize+pin` as a mitigation arm analyzed
against the factorial, not inside it. (c) Textual survival under `summarize` is partly
random (the summarizer may or may not keep the policy); that makes the compaction factor
heterogeneous *within* cell — exploit it (survival becomes a measured mediator with
natural variation) rather than pretend the cell is homogeneous. (d) The hard-norm side
under compaction is nearly vacuous: deleting a refusal instruction changes little because
the prior enforces it — which is not a flaw, it *is the predicted signature of mechanism
3*, and the methods should elevate this to a named, pre-registered contrast: **the
compaction-deletion natural experiment** (constraint text gone: soft adherence should
crater to no-injection baseline; hard adherence should barely move — the cleanest
possible demonstration that the prior, not the text, carries hard norms).

**Refined:** Pilot factorial is fractionalized and staged:

- **Pilot (regime A + keep-top only):** 2 models (1 frontier API, 1 open-weights
  instruct) × type(2) × framing(2: advisory/imperative) × position(2: sys-head/mid-conv)
  × repetition(2: 1/3) × compaction(2: none/keep-top) = 64 cells × 20 pairs (nested, not
  crossed: 10 pairs per half-fraction) × 3 seeds ≈ **1,900-2,300 conversations/model**,
  30 turns, probes every 5. Two- and three-way interactions with type estimable;
  higher-order aliased by design (declared).
- **Scale-up:** ≥6 models / ≥3 families (incl. base/instruct pair), framing 3-level,
  repetition {1,3,5}, add `summarize` operator with textual-survival logged as a
  *measured mediator* (per critic (c)); `summarize+pin` and every-k-turn restatement run
  as **mitigation arms** outside the factorial; 100-turn horizon on a fractional subset.
- **Named confirmatory contrasts (pre-registered):**
  1. *Gap replication:* soft hazard > hard hazard, growth-only cells.
  2. *Boosted-soft:* imperative + head + rep-3(pilot)/5(scale-up) soft vs. standard hard
     — how much of the gap do salience+framing close? (RQ_INF_1)
  3. *Compaction-deletion natural experiment:* post-deletion soft adherence →
     no-injection baseline vs. hard adherence ≈ unchanged — the signature test of the
     prior mechanism (critic (d), promoted to co-headline).
  4. *Reactivity:* within/between probing delta, type-uniformity test (gates the rest).
- Violation detection, survival model, proxy battery, and audit gates as drafted; all
  analysis code and the pair bank frozen and hashed before scale-up.

---

## Stage 6 — Experiment Design

**Draft.** Arms & scale: pilot as above (~4k-4.6k conversations total across 2 models,
~60k assistant calls); scale-up ~20k conversations. Cost: pilot API class $10²-10³;
open-weights half on 1×A100-80GB, 3-5 days; scale-up $10³-low-10⁴ or ~2 GPU-weeks on
8×A100. Human effort: ~2 person-weeks harness + verifiers; 40-60 annotator-hours audit.

Go/no-go gates:
- **G0 (week 1):** 8x-source verification [VERIFY] + precedent search come back; verifier
  suite passes κ ≥ 0.8 on audit sample.
- **G1 (week 2-3):** reactivity calibration (M6 subset): delta small + type-uniform →
  proceed with within-conversation probing; type-dependent → escalate to between-
  conversation design (accept cost, cut scale-up model count).
- **G2 (week 3-4):** pilot gap replication: soft half-life < hard half-life
  directionally, ≥1 factor×type interaction detectable. Fail → the premise, not the
  mechanism, becomes the paper (a null-replication of folklore is still a paper, but
  re-target FSE/later window).
- **G3 (week 5):** dominance analysis stable under Weibull refit + leave-one-pair-out.

Milestones against the windows (today = Aug 13):
- **W1 (Aug 13-20):** pair bank v1, harness, verifiers, G0.
- **W2-3 (Aug 20-Sep 3):** reactivity cells + pilot run, G1, G2.
- **W4 (Sep 3-10):** pilot analysis; freeze pre-registration; launch scale-up fraction.
- **W5 (Sep 10-17):** scale-up (compaction mediator + mitigation arms; as much of the
  6-model sweep as budget allows).
- **W6 (Sep 17-25):** analysis, writing → **ICLR abstract/paper ~Sep 25** [VERIFY exact
  dates]. If G2 slipped one week: **FSE ~Oct 2** [VERIFY] with the SE framing
  (policy-adherence reliability of LLM-integrated systems), pilot + partial scale-up
  only, mitigation arms emphasized.

**Critic:** (a) The schedule allocates zero slack for the single most common failure —
harness/verifier iteration (digest Stage-1 success criterion explicitly anticipates probe
redesign). One redesign cycle costs a week; the plan dies on contact unless W1-W2
overlap. (b) The 6-model scale-up inside W5 is fantasy on one A100; either secure an
8×A100 reservation now or pre-commit to 3 models (2 API + 1 open) and say the family-
generalization claim is scoped down for this submission. (c) The ICLR-vs-FSE fork is
decided too late (W6); venue determines framing, framing determines what W4-W5 must
produce — decide at G2. (d) No explicit budget owner for the between-conversation
escalation path at G1; if it triggers, something must be named to be cut.

**Refined:** Final plan with slack and forks resolved early:

- **Arms:** (i) growth-only factorial; (ii) keep-top factorial; (iii) summarize +
  mediator (scale-up); (iv) mitigation arms (summarize+pin, every-k restatement);
  (v) reactivity calibration; (vi) prior-proxy battery (offline, cheap, week 1).
- **Scale commitment (fixed now):** pilot 2 models; scale-up **3 models** (2 dated API
  snapshots + 1 open-weights instruct with its base twin for M5) — family
  generalization explicitly deferred to a journal/extended version. 8×A100 only if
  already reserved by Aug 20; otherwise open-weights stays single-model.
- **Cost envelope:** ≤ $3k API + ≤ 10 A100-days + ≤ 60 annotator-hours.
- **Gates with named cuts:** G1 escalation → cut the `summarize` operator from this
  submission (keep-top suffices for the compaction claim; summarize moves to future
  work). G2 fail → pivot paper to "the asymmetry folklore does not survive matched
  measurement," target FSE Oct 2.
- **Schedule (overlapped):** W1 harness+bank *with* a 5-pair smoke run (Aug 13-19); W2
  probe-redesign slack + reactivity cells (Aug 19-26); W3 full pilot (Aug 26-Sep 2);
  **G2 + venue decision Sep 3**; W4 scale-up launch + pre-registration freeze (Sep
  3-10); W5 scale-up + analysis overlap (Sep 10-18); W6 writing (Sep 18-25) → ICLR;
  FSE Oct 2 as the one-week-slip absorber. Both window dates [VERIFY] in week 1, since
  the whole schedule hangs on them.

---

## Residual risks (carried forward, not resolved)

1. The ~8x premise may not source or replicate — mitigated by the G2 pivot framing.
2. Prior mechanism is correlational-only by construction (SP4); attribution to it is a
   diagnosis of exclusion — stated as such, with the compaction-deletion contrast as the
   strongest available causal-adjacent evidence.
3. Type-dependent probe reactivity would invalidate the cheap design — mitigated by
   running M6 first and pre-registering the escalation.
4. Precedent risk: a direct soft-vs-hard decay comparison may exist outside the corpus —
   mitigated by the G0 search; novelty claim written conditionally until then.
