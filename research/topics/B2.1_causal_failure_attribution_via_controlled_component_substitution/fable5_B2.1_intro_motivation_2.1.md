# When the Evidence Lies: Attribution under Corrupted Tool Observations

> **DRAFT — Introduction + Motivation.** All bracketed quantities `[XX]` are placeholders
> pending experiments; every claim traces to an H-id or a Step-5 definition in `paper.md`.
> Confirmatory hypotheses: H1, H2 (direction), H3. Exploratory: H2b (M5 type-grid).
> Primary estimand population: AgentDojo + GAIA (Who&When is an additive confirmatory extension).

---

## 1. Introduction

Automated failure attribution has become the control layer of the LLM-agent stack. When a
multi-step agent trajectory fails, deciding *which* component is to blame — the plan, a
tool, or the execution layer — is what routes every corrective action that follows:
whether to retrain the planner, patch a tool, add a retry, or curate new training data.
Because inspecting long trajectories by hand is prohibitively expensive and inconsistent,
this decision is now made by machines: LLM judges that read the trajectory log and name a
responsible step [Who&When], trained tracers that predict the decisive error
[AgenTracer], and runtime monitors that flag high-risk interactions online
[SupervisorAgent]. Attribution is no longer a diagnostic afterthought — its verdicts now
select which component gets the next engineering intervention, so a wrong verdict does not
just mislead a developer, it misspends the fix.

**Every one of these methods reads the trajectory log as trustworthy evidence.** They
differ in how they consume it — all-at-once, step-by-step, binary search, learned, or
online — but they share one premise: that what a tool *returned* is what actually
happened. This premise holds a hidden assumption up to the light only when it breaks. And
it breaks in a specific, common way. A tool can return an observation that is
*syntactically and schema-valid* — it parses, it type-checks, the framework accepts it
without raising — yet *semantically wrong*: a stale API value, a subtly incorrect retrieval,
an off-by-an-order-of-magnitude number, a plausible but false entity. The literature shows
this channel is neither exotic nor adversarial-only: it is an actively exploited attack
surface [ChatInject, MCP-SafetyBench] and, even without an attacker, a pervasive
reliability failure of real tools [ResiliBench]. When such an observation is the true root
cause of a downstream failure, the attribution method must diagnose the very failure whose
decisive evidence has *already lied to it*.

We argue this creates a structural blind spot, and we state it as an asymmetry rather than
a gap between literatures. **Every check an attribution pipeline can run certifies the
*form* of a tool observation; the diagnosis then consumes its *content* as an unquestioned
premise.** Schema validation, parser acceptance, exception flags, and monitor triggers all
inspect grammar. None inspects truth. So a schema-valid lie is not merely undetected — it
is re-used, as evidence, against the plan and execution layers that faithfully consumed it.
The same trajectory is simultaneously the crime scene and the witness, and validity
checking guards only the witness's grammar. This is a property of the evidence channel
itself, and it would hold even if some prior work had already studied corrupted tool
outputs — because it is not about unoccupied territory, it is about what trace-reading
diagnosis structurally must do when its input is a well-formed falsehood.

This asymmetry yields two testable predictions that no prior work has measured. First, a
*rate* prediction: attribution methods should misattribute tool-caused failures away from
the tool layer **specifically when the corruption is schema-valid** — measurably more often
than when the same tool fault is overt (an exception, timeout, or empty return that the
framework surfaces as a visible error). We call this difference, per method, the **Δ-trust
gap** — the misattribution rate on silent semantic corruptions minus the rate on matched
overt errors. It is the unit of evidence in this paper: not "attribution is imperfect" (it
always is), but "attribution degrades *because the evidence is well-formed*." Second, a
*direction* prediction: when misattribution occurs, blame should skew toward the **plan
layer** rather than execution, because plan critique sits immediately downstream of reading
the observation, while execution verdicts key on mechanical success/failure signals that a
schema-valid corruption deliberately never trips.

The obstacle to measuring either prediction is that the ground truth does not exist in
nature. Given only a *naturally* failed trajectory, a reasonable plan built on a bad
observation is causally indistinguishable from a bad plan built on a good one — separating
them requires a counterfactual the trace does not contain (what would the step have looked
like under a *correct* observation?) plus the world knowledge to recognize the observation
as wrong. This is precisely the reasoning the attribution methods under test cannot
perform; if we could not perform it either, "misattribution" would be undefined. **Our
enabling contribution is an instrument that manufactures this ground truth forward rather
than annotating it backward.** We start from a *reproducibly successful* agent run, inject
exactly one schema-valid semantic lie into a single tool observation (under numeric, entity,
boolean, structural, and stale-value mutation families), and keep the trajectory only if the
lie is *decisive*: the corrupted run fails the task's programmatic checker while its
identical twin with the original observation restored succeeds. This forward construction
gives a hidden, replay-certified ground-truth label (layer = tool, at the injection step)
that no backward annotation of a natural failure can supply. Concretely, a trajectory earns
a certified label only when it satisfies a single-fault causal invariant, restricted here to
the observation slot:

```text
one injected schema-valid observation lie
+ outcome flip (corrupted twin fails the checker)
+ stable identity replay (untouched twin succeeds)
+ stable sham control (identity-mutation twin does not shift attribution)
= certified tool-layer attribution label
```

Against this certified ground truth we run existing attribution methods **unmodified and
blinded** to the injection metadata, and score their verdicts against two matched controls —
overt tool errors (same root-cause layer, visible signal) and genuine plan failures (a
false-positive control) — so that any measured Δ-trust gap reflects the *silence* of the
corruption, not the difficulty of the task or the idiosyncrasy of the injector. The
construction is deliberately in the lineage of forward-injected, test-certified defect
benchmarks from software engineering (e.g. Defects4J for automated program repair): a defect
is trusted as ground truth because a deterministic test certifies it, not because a human
annotated it after the fact — we bring that certification standard to the agent
observation channel. We share the replay-based, reproducible-environment attribution setup
of recent full-observability benchmarks [AgenTracer; TraceElephant], and we concede that
machinery openly; our delta is not the replay harness but *what we inject and what we
measure*. Prior replay-attribution work injects faults into **agent actions** and scores
attribution over **naturally arising** failure distributions; we instead inject a
schema-valid lie into a **tool observation** and hold the corruption's *silence* as the
controlled variable, which is the only way the direction-of-blame estimand below becomes
identifiable.

With this instrument we answer the paper's core question — *do existing attribution methods
systematically misattribute schema-valid tool corruptions, in which direction, and why?* —
and report three findings, each with a control that pre-empts its most deflationary reading.

**(1) A systematic Δ-trust gap.** [XX of 5] attribution methods misattribute schema-valid
semantic corruptions at a rate **[+XX] percentage points** higher than matched overt errors
(Holm-corrected *p* < .05), even though the corruption is, by construction, invisible to
every surface signal they rely on; the attribution layer is reliable on tool faults *only
when the fault announces itself*. This gap is not an artifact of methods keying on obvious
symptoms: a trivial surface-heuristic attributor (blame the layer nearest the visible error
signal) recovers only **[XX]%** of the certified tool-layer labels and explains at most
**[XX] pp** of any method's gap, so what degrades under silence is causal attribution, not
symptom-reading.

**(2) A directional skew toward the plan layer.** Among misattributed cases, blame lands on
the plan layer **[XX]%** of the time — a share exceeding the plan base-rate on matched
controls by **[+XX] pp** (exact binomial *p* < .05 against the control base-rate, not against
an assumed even split), confirming that silent corruption does not merely add noise to
localization but *channels* blame to the component sitting immediately downstream of the
corrupted read.

**(3) The mechanism is a removable trust assumption, not (only) a capability ceiling.** A
one-sentence *trust-license* intervention — adding to the judge prompt that tool returns may
be silently wrong and must be independently sanity-checked — reduces misattribution by
**[XX] percentage points** absolute on the corrupted set ([X of 3] judges, paired McNemar
*p* < .05) **without** inflating false positives on genuine plan failures (≤ [3] pp,
non-inferiority), while a matched *agent-side-fault* control (injecting the identical wrong
value into the agent's own action rather than the tool's return) is localized correctly —
together isolating the cause as an *evidence-channel* trust asymmetry rather than an
intrinsic difficulty of spotting subtle values.

We stress what this paper is and is not. It is a **measurement study**: we do not propose a
new attribution method, and we make no claim to *solve* the blind spot. The corruption suite
is instrumentation for the measurement — a replay-verified stress test that, for the first
time, lets the community *audit the auditors* — not a leaderboard. Its purpose is the
treatment-versus-control contrast that makes the Δ-trust gap a clean, falsifiable quantity.
Every prediction above carries a pre-registered falsifier: if the Δ-trust gap is
statistically indistinguishable from zero for a majority of methods, the attribution layer
is empirically *robust* to lying evidence and we release the suite as the certification of
that robustness; if a trust license fails to move misattribution, the blind spot is a deeper
counterfactual-reasoning deficit and cheap prompt fixes are ruled out. The finding is
designed to be informative in either direction.

**Contributions.**

- **C1 — A replay-verified corruption instrument.** A fault-injection testbed that mutates
  one tool observation per trajectory under five schema-preserving operator families and
  certifies, by counterfactual twin replay, that each corruption is the decisive cause of
  failure — yielding hidden ground-truth tool-layer labels with matched overt-error and
  genuine-plan-failure controls. Released for reuse.
- **C2 — The Δ-trust gap: a systematic misattribution finding.** The first measurement that
  existing attribution methods (LLM judges, a trained tracer, a runtime monitor)
  misattribute *schema-valid* tool corruptions **[+XX] pp** more than *overt* ones — a bias
  that appears precisely because the false evidence is well-formed — with a surface-heuristic
  control that separates genuine causal attribution from symptom-reading.
- **C3 — A directional characterization of the bias.** Misattribution skews toward the plan
  layer (π_plan = [0.XX]); we further map (as an exploratory analysis, H2b) how the skew
  varies with corruption type, trajectory locus, and subtlety across a controlled grid.
- **C4 — Mechanism evidence, and a cheap tested remedy.** A trust-license prompt
  intervention plus a matched agent-side-fault control show the bias is a removable trust
  assumption over the observation channel, not a raw capability ceiling — a concrete,
  low-cost design recommendation for anyone building attribution pipelines today.

---

## 2. Motivation

**Why the target matters: attribution is a control layer, and a biased controller
misroutes every fix it triggers.** Failure attribution is being industrialized precisely
because it is load-bearing: it is framed as a first-class judging problem because manual log
inspection does not scale [Who&When], and dedicated tracers are trained so that attribution
can drive debugging, data curation, and iterative self-improvement [AgenTracer]. That makes
attribution a *controller*: its output selects the intervention. A controller with a
systematic bias is worse than a noisy one — noise averages out, but a bias that chronically
relabels tool-caused failures as plan or execution failures aims every downstream fix at the
wrong component. The planner gets retrained for a mistake it did not make; the tool that
lied stays unmonitored; and the actual vulnerability — blind trust in well-formed tool
output — is not just unfixed but *reinforced*, because each misrouted fix appears to
"resolve" a case whose true cause is untouched. The cost of the blind spot is not a single
wrong verdict; it is a corrective loop that silently optimizes the wrong part of the system.

**Why the fault mode is real, not a constructed edge case.** The corrupted-but-well-formed
observation sits at the intersection of two active literatures, each of which establishes
one half of its reality while measuring the wrong thing for our question. The agent-security
line shows the tool-return channel is an exploited attack surface: agents consume untrusted
tool outputs as reasoning context, and attacks can be structurally disguised inside
well-formed returns [ChatInject, MCP-SafetyBench]. The robustness line shows that even with
no adversary, tools are unreliable by default — APIs time out, return stale data, and fail
validation as a matter of course [ResiliBench]. But both lines score *attack success* or
*task completion under stress*; neither asks whether post-hoc diagnosis correctly localizes
the corrupted return as root cause. A stale API result, a subtly wrong retrieval, or a
poisoned-but-valid tool return therefore lands in the blind spot *between* what the security
literature measures (did the payload succeed?) and what the attribution literature assumes
(is the log faithful?). Recent robustness benchmarks do inject at the parameter or tool-noise
level and even trace how errors *propagate* downstream [AgentProp-Bench], but they measure
task-completion resilience or cascade length, never whether the diagnosis that follows
localizes the corrupted return as the root cause — the propagation is characterized, the
*misattribution* it induces is not. We are not inventing a fault mode; we are measuring the
diagnostic consequence of one that both literatures already document.

**Why existing attribution methods are structurally, not incidentally, exposed.** The
exposure is not a fixable oversight in any single method — it follows from how each class of
method is built. LLM judges *read the trajectory as testimony*; when the testimony is
well-formed, they have no signal that distinguishes a lie from the truth, so they inherit
the corruption into their own premises. Trained tracers learn from fault distributions:
because their supervision comes from perturbing *agent actions* in successful traces
[AgenTracer], a tracer has, by construction, never seen a trajectory whose decisive error is
a lying *observation* — the fault mode is outside its training support. Runtime monitors are
deliberately triggered by *overt* signals — explicit errors, repetitive behavior, excessive
observation length [SupervisorAgent] — precisely the signals a schema-valid corruption is
engineered not to emit. Three different design philosophies, one shared premise, one shared
blind spot: the trajectory's grammar is checkable, its truth is not. This is why the problem
is a property of the *evidence channel* and not of any method's cleverness — and why the
right response is first to *measure* the bias under controlled ground truth, before anyone
proposes a fix.

**Why measuring it is hard, and what makes it now possible.** The reason this bias has gone
unmeasured is that the ground truth is genuinely unavailable from traces alone. To score a
method's verdict you must know the true responsible layer; but for a schema-valid corruption,
the trajectory offers no surface marker (the corruption is form-invisible), the diagnosis
consumes the corrupted evidence circularly, and separating "reasonable plan given bad input"
from "bad plan given good input" demands a counterfactual the trace does not hold. Our
instrument dissolves exactly this obstacle by giving the *experimenter* — not the methods
under test — the counterfactual: the uncorrupted twin. The move is to stop annotating blame
*backward* from a natural failure and instead manufacture it *forward* from a known-good run,
so the causal source is fixed by construction rather than inferred after the fact. Replay
verification then converts an unobservable ("was the tool the decisive cause?") into a binary
check ("does restoring the original observation flip the outcome to success?") — the same
certification standard that lets forward-injected defect suites like Defects4J serve as
trusted ground truth for automated program repair, here transplanted to the agent
observation channel. The resulting hidden label lets us compute, for the first time, how far
each method's verdict drifts from truth *as a function of the evidence being silent*. The
measurement was not impossible in principle; it was missing an instrument that manufactures
replay-certified tool-layer ground truth. That instrument is what makes the core question —
*does the evidence channel's trust asymmetry bias real attribution methods, and can it be
cheaply repaired?* — answerable now.

---

### Self-review (five dimensions)

| # | Dimension | Status | Note |
|---|---|---|---|
| 1 | Contribution clarity | pass | Headline = Δ-trust gap finding + mechanism; instrument (C1) framed as enabling, not headline (fixes archetype). |
| 2 | Writing clarity | pass | Each paragraph opens with its one message; asymmetry stated once, reused. |
| 3 | Bridge-risk (Gate 4) | **pass (fixed)** | Opportunity re-anchored on the form/content asymmetry; "unmeasured in prior work" demoted to related-work positioning, never the #1 abstract claim. Claim explicitly survives "someone already crossed the literatures." |
| 4 | Confirmatory/exploratory (Gate 11) | **pass (fixed)** | Stated in header + C3: H1/H2/H3 confirmatory, H2b (type-grid) exploratory. |
| 5 | Estimand pinned (Gate 12/G6) | **pass (fixed)** | Primary population = AgentDojo + GAIA; Who&When additive. Stated in header. |
| — | Falsifiability | pass | Every finding paragraph names its pre-registered falsifier (F1/F-G1/F0, F2, F3). |
| — | Placeholder honesty | pass | All numbers bracketed `[XX]`; no fabricated result stated as fact. |
| — | Symptom-reading defense | **pass (added)** | Surface-heuristic control in finding (1)/C2 separates causal attribution from symptom-reading — pre-registered ceiling on its share of the gap. |
| — | Method-twin concession (novelty-auditor) | **pass (added)** | TraceElephant (arXiv:2604.22708) + AgentProp-Bench conceded explicitly; delta = observation-slot injection + direction estimand they cannot isolate. |
| — | Direction base-rate (se-reviewer DA) | **pass (fixed)** | C3 binomial now against the control plan base-rate, not 0.5 — closes the corpus-base-rate confound. |

### Anticipated reviewer novelty attacks (defensive, from the audit)

1. **"This is TraceElephant/AgenTracer with a different injection target."** — Response
   (now in-text): we share and openly concede the replay-attribution harness; the delta is
   (a) injecting a *schema-valid semantic* corruption into a *tool observation* rather than
   an agent action, and (b) the *direction-of-blame* estimand, which their natural-failure
   distribution and action-fault injection cannot make identifiable.
2. **"The plan-skew is just the corpus base rate."** — Response: C3 is scored against the
   plan base-rate on matched controls, and the always-predict-plan floor (B0) is required in
   every table; a skew that does not beat that floor is not reported as a finding.
3. **"The misattribution is symptom-reading, not a trust asymmetry."** — Response: the
   surface-heuristic control caps how much of the gap obvious-symptom-reading can explain;
   the trust-license intervention + agent-side-fault control jointly localize the cause.

**Scope-guard (deliberately NOT absorbed from the sibling draft).** The forward-injection
labeling here is restricted to the **observation slot only** — plan/tool-binding injection is
kept as a *control* (B-alt agent-side-fault arm), not promoted to a co-equal arm, because
B2.5's contribution is the evidential-circularity asymmetry unique to the observation channel
(the diagnosis consumes the corrupted evidence). Expanding to a general three-slot
"certified attribution benchmark" would flatten that asymmetry into a resource paper and
collide with sibling projects B2.2/B2.3/B2.4. Archetype stays **empirical/measurement**
(headline = the finding), not benchmark/resource.

### Claim–evidence map (Intro/Motivation claims)

| Claim | Evidence | Status |
|---|---|---|
| Attribution is a load-bearing control layer whose bias misroutes fixes | Who&When / AgenTracer motivation (industrialized attribution) | supported (corpus-grounded) |
| Schema-valid semantic corruption is a real, documented fault mode | ChatInject, MCP-SafetyBench, ResiliBench motivations | supported (corpus-grounded) |
| Prior work never scores attribution against this condition | N3/N4 corpus audit; related-work positioning only | supported-by-design |
| Methods misattribute schema-valid corruptions **[+XX] pp** more than overt | H1 / Δ-trust gap (C2) | **needs-experiment** (placeholder) |
| Misattribution skews to plan layer, π_plan = [0.XX] | H2 (C3) | **needs-experiment** (placeholder) |
| Trust license cuts misattribution [XX] pp without FPR inflation | H3 + B-alt (C4) | **needs-experiment** (placeholder) |
| Replay verification yields decisive tool-layer ground truth (certified-label invariant) | M1+M2 defs; skeleton G1/G2 | needs-experiment (construction-gated) |
| Δ-trust gap is not a symptom-reading artifact (≤[XX] pp from surface heuristic) | surface-heuristic baseline (B0 extension) | **needs-experiment** (placeholder) |
