# Does the Diagnosis Survive a Model Swap? Cross-Backbone Stability of Failure Attribution

**Introduction & Motivation — pre-registration draft (v5)**

> Status: pre-experiment specification. Every bracketed value `[PLACEHOLDER: …]` is a
> pre-registered slot filled from `results/*.json` after the pilot/Stage-2 runs. This is a
> measurement paper with no baseline to beat, so the headline is a **measured κ**, never an
> "XX% gain." The entire §1 ¶5 finding is refuted if κ ≥ 0.8 uniformly. Citation keys are
> placeholders to be reconciled with `refs.bib`.

---

## 1. Introduction

Automated failure attribution has become a standard instrument for debugging LLM-agent
pipelines. Given a failed trajectory, an attribution procedure names the layer that broke —
a faulty *plan*, a mis-issued *tool* call, or a broken *execution* step — and the community
now treats this as a first-class task with dedicated benchmarks, datasets, and trained
tracers that link failures to a responsible agent and decisive step [Who&When; AgenTracer;
MAST]. Even under a single fixed backbone the task is hard: step-level attribution accuracy
on the Who&When benchmark sits around 12–14% [Who&When; CAR; TraceElephant], a difficulty
that has driven a wave of causal, counterfactual, and graph-based methods [CAR; CausalFlow].
Across all of this work, a plan/tool/execution label is consumed as a property *of the task
and its failure* — a statement about what went wrong — and reused to compare frameworks,
route repair effort, and build the taxonomies through which the field reasons about agent
reliability.

Every such label, however, is produced inside a single fixed execution stack: one agent
backbone generates the trajectory, and one judge — often from the same family — reads it.
Practitioners routinely swap the underlying LLM, for cost, latency, or capability, while
holding the agent scaffold fixed, and they carry the attribution tooling across the swap
unchanged. This exposes an invariance the pipeline was never verified to possess.
Programmatic fault injection can hold the *cause* of a failure fixed across backbones,
because the injected layer is fixed by construction; but nothing holds the *evidence* fixed,
because the trajectory any attribution procedure must read is itself a function of the
executing backbone. A plan/tool/execution label therefore silently asserts that the
diagnosis is invariant to a factor its own computation is a direct function of. If that
assertion fails, results reported as task properties are in fact properties of a *(task,
backbone)* pair, and tooling validated on one backbone must be re-validated on every other —
a materially stronger and more expensive claim than the literature currently makes.

Answering this is not a matter of re-running one tool under two models, because three
difficulties are intrinsic to the question rather than to any method. *First, the diagnosis
is itself model-produced:* attribution is usually performed by an LLM judge, so a naive
cross-backbone comparison conflates the backbone that *produced* the failure with the one
that *diagnosed* it — and judges are known to favor related generators and to flip under
surface perturbations [PreferenceLeakage; BiasScope]. A single-judge design cannot separate
"diagnosis is model-specific" from "the judge is noisy." *Second, the comparable failure set
is backbone-dependent:* a stronger backbone may recover from an injected fault and simply
succeed, so agreement is computable only over the *intersection* of jointly-failing cells — a
selected, non-random subsample that makes any headline number uninterpretable unless the
failure-overlap rate is reported beside it. *Third, the label space may not be a natural
kind:* a single failure can span layers, so any stability number is conditional on human
coders first agreeing on the codebook — a validity gate that must pass before a backbone
effect can even be defined. A credible study therefore gates on human–human agreement,
decomposes the judge–agent confound, and reports censoring as a first-class quantity.

Two recent lines come closest. Benchmark studies of attribution report an *effect of
backbone* on attribution *accuracy* — stronger models attribute more accurately on a fixed
trace collection [TraceElephant]. Like that work, we treat the backbone as the variable of
interest; *unlike* it, we swap the backbone that **executes** the task rather than the one
that attributes a set of already-collected traces, we hold an **injected cause fixed** rather
than scoring against organic ground truth, and we measure label **agreement** rather than
accuracy. Separately, observability studies report that different backbones exhibit distinct,
model-specific failure signatures and that attribution diverges across LLM judges [MAESTRO],
but qualitatively — over a coarse symptom taxonomy, without a chance-corrected estimand, a
cause-fixed suite, or a censoring correction. Notably, *both* of these nearest neighbors name
controlled fault injection and MAS-specific attribution as open future directions — precisely
the axis we measure. We do not propose another attribution method. **We measure whether any
attribution method's label survives a backbone swap when the injected cause is held fixed** —
the invariance both lines assume but neither tests.

We build a controlled fault-injection suite over GAIA and WebArena-style tasks, run every
injected cell through *K* backbones spanning families and capability tiers under one
byte-identical scaffold, apply a single pre-registered codebook to every failure trace, and
compute chance-corrected cross-backbone agreement with all thresholds fixed before data. Our
**primary pre-registered finding** is the stability band of that agreement: across
*K* = [PLACEHOLDER: 6–8] backbones we report Fleiss' κ = [PLACEHOLDER: 0.XX] (95%
task-cluster-bootstrap CI [PLACEHOLDER]), which our hypothesis places in the "model-specific"
band (κ < 0.6) rather than the "stable" band (κ ≥ 0.8); if instead κ ≥ 0.8 uniformly, the
paper reports the equally-informative certification that diagnosis is a task property. Three
supporting measurements exist only to *interpret* that number, not to co-headline it: a
judge×agent factorial attributes [PLACEHOLDER: XX]% of label variance to the *judge*
backbone, so part of any "diagnosis" is an artifact of the diagnosing model; agreement is not
correctness, since [PLACEHOLDER: XX]% of jointly-failing cells are labeled *consistently
wrong* against the injected ground truth; and the comparison is well-posed at all only because
the failure-overlap rate is Ω = [PLACEHOLDER]. Whichever band the κ lands in, the qualitative
claim — that attribution's backbone-dependence must be measured, not assumed — does not turn
on the specific model generation tested. The practical consequence is a single rule:
single-backbone attribution claims should be reported as *(task, backbone)*-pair properties,
and we release the suite so per-backbone re-validation is cheap.

**Contributions.**

- **A new estimand and its measurement** — the chance-corrected cross-backbone agreement of
  plan/tool/execution attribution labels under a held-fixed injected cause — reported
  overall, per layer, and per model-family pair, with pre-registered decision bands that make
  the result informative whether attribution proves stable or model-specific.
- **A judge×agent factorial decomposition** separating agent-backbone-driven from
  judge-backbone-driven instability and quantifying the surface-style share — turning the
  "which model is being diagnosed vs. doing the diagnosing" confound into an estimated
  variance share.
- **A censoring-aware measurement protocol** that reports the failure-overlap rate as a
  first-class quantity beside every agreement number — instantiated on a fault-injection suite
  adapted from prior programmatic-injection work [AgenTracer], released so any single-backbone
  attribution claim can be re-validated per backbone at low cost.

---

## 2. Motivation

Three forces make this measurement worth its GPU time.

**The attribution literature validates labels *within* a fixed stack, and the studies that
vary the backbone vary the wrong one.** The field moved fast from defining attribution
[Who&When] to scaling it via counterfactual replay and programmatic fault injection
[AgenTracer] to organizing it into a taxonomy [MAST]. Where a backbone axis appears, it is the
*attributor's* backbone applied to a fixed trace collection and scored for accuracy
[TraceElephant], or the *judge's* backbone scored for divergence over organic failures on a
coarse symptom taxonomy [MAESTRO] — leaving open whether the same injected *cause* receives
the same *layer label* when the *executing* backbone changes. Both of the closest works
explicitly list controlled fault injection and MAS-specific attribution as future work,
marking the gap rather than closing it.

**The judge side is independently known to be non-invariant — on every axis except this
one.** LLM judges inflate scores for related generators [PreferenceLeakage], flip under
structured surface perturbations [BiasScope], and diverge as attributors of the same failures
[MAESTRO]. This is exactly why a cross-backbone attribution study cannot use a single fixed
judge and call the result "the backbone effect": the judge is a second, unvalidated
dependency. Our factorial design converts this confound from an assumption into an *estimated
variance share* — the quantification that prior qualitative observations of model-specific
signatures never supplied, and it is what lets us say whether observed instability is a
property of how agents *fail* or of how models *judge*.

**The practical stakes are asymmetric and already live.** Backbone swaps happen constantly in
deployed agent systems. If attribution is stable, the community earns a clean license to keep
reporting diagnoses as task properties — a genuinely useful confirmation. If it is not, an
entire class of published claims is mis-scoped, and the corrective (per-backbone
re-validation) is expensive unless someone supplies the instrument to do it cheaply. Either
outcome changes practice, which is the property that makes this a measurement worth
pre-registering rather than a result worth hoping for.

---

## Appendix A — Four-pass review record (v4 → v5)

The draft was audited by four skills; every change below is traceable to a specific finding.

| Finding | Skill | Fix applied in v5 |
|---|---|---|
| Fault-injection suite drifted into the *claimed* novelty layer | novelty-auditor (boundary error) | Contributions reordered — estimand first; suite credited to AgenTracer as inherited instrument |
| Delta-durability attack unaddressed (ML category bar) | novelty-auditor | §1 ¶5 durability sentence: qualitative claim is generation-robust even if κ is not |
| Claims-only vs. TraceElephant; no concession of shared ground | se-paper-reviewer (R2) | §1 ¶4 "Like that work… unlike it…" concede-and-claim |
| MAESTRO adjacency to claim 2 unconfirmed from snippet | novelty-auditor | Full-text read: MAESTRO swaps judge not executor, organic + coarse symptom taxonomy, no estimand → distinct; both twins name our axis as future work |
| κ read as a finding, not a pre-registered slot | pengsida-stage-reviewer | §1 ¶5 recast as "primary pre-registered finding," conditional mood structural |
| Codebook validity stated as difficulty, not precondition on the number | pengsida-stage-reviewer | §1 ¶3 third obstacle frames the human–human κ gate as a validity precondition |
| Mild bridge-cadence in §1 ¶4 opener | research-taste-auditor (nit) | Left — mechanism underneath is a genuine estimand; framing firewall keeps 🟢 |

**Aggregate verdict.** novelty 🟢 (carried by the estimand claim; no hidden twin after
full-text checks of both nearest neighbors) · taste 🟢 (opportunity = failure/risk +
evidence-gap; method = empirical-mapping + formalize; no flags fire) · se-reviewer R2 pass
with concede-and-claim added · stage-review pass with mood + precondition fixes. Remaining
gates are empirical, not framing: the one-day skeleton go/no-go, and filling the pre-registered
κ / variance-share / Ω slots from real runs.

### Novelty claim ledger

| # | Claim | Type | Nearest prior work | Delta | Stance |
|---|---|---|---|---|---|
| 1 | Cross-backbone stability of the attribution *label* is unmeasured | new estimand | TraceElephant (backbone → attribution *accuracy*) | swaps executor not attributor; label *agreement* not accuracy; cause-fixed injection not organic ground truth | 🟢 novel |
| 2 | Judge×agent factorial decomposes instability source | new instrument | MAESTRO (qualitative model-specific signatures + judge divergence) | chance-corrected variance decomposition vs. qualitative observation; causal-layer taxonomy vs. coarse symptom taxonomy | 🟢 novel |
| 3 | Censoring / failure-overlap as a first-class reported quantity | new instrument | none proximate found | Ω correction on a selected-subsample agreement statistic; no attribution paper reports it | 🟢 novel |
| 4 | Fault-injection suite | inherited machinery | AgenTracer (programmatic injection) | none — reused and credited, not claimed as novel | (instrument) |

### Anticipated reviewer attacks (defensive)

1. *"This is TraceElephant / MAST with more models."* (high) — Answerable now: TraceElephant
   swaps the attributor over a fixed trace pool and scores accuracy; we swap the executor with
   the injected cause fixed and measure chance-corrected label agreement. Both papers name our
   axis as future work.
2. *"The κ evaporates with the next model generation."* (med) — Answerable now: the reported
   qualitative finding is that backbone-dependence must be measured, not assumed; the specific
   κ is a snapshot, the obligation it establishes is not.
3. *"Your taxonomy is arbitrary, so the number is meaningless."* (med) — Partially answerable:
   the human–human κ gate is a pre-registered precondition; if it fails, the study reports that
   the label is ill-defined rather than reporting a backbone effect. Needs the pilot to clear
   the gate.
