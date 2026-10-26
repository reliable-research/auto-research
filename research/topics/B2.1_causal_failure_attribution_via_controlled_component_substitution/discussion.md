# B2.1 — Research Discussion: Causal Failure Attribution via Controlled Component Substitution

> Auto-research-discussion (6 stages, critic→refine per stage). Topic B2.1 受控替换归因协议,
> family lead of B2 失败归因（plan / tool / execution）, audit verdict **KEEP-TOP**, target
> **FSE 2027 (deadline Oct 2, 2026)**. Absorbs the retired siblings' questions: **B2.3**
> (cross-backbone stability of the diagnosis) as an experimental axis and **B2.2**
> (minimal replay budget) as an efficiency section. Consistent with `digest.md`
> (C1–C4, M1–M5, CO1–CO3, RQ1/RQ_INF_1, t1–t5) and the pre-registered spec in `paper.md`
> (E1–E4, H-sec, PG-1–PG-6, F-G1, CR-1–CR-5); this document is the discussion layer above
> both, and is where the two absorbed axes are integrated for the first time.

---

## Stage 1 — Problem Definition

**The attribution task (what a method must do).**

- **Input:** a failing tool-use agent trajectory τ — the full recorded run of a
  plan–executor–tool pipeline (plan text, executor messages, tool calls, tool
  returns/observations, memory writes, final outcome test result = fail). Two access
  regimes are distinguished, because they define two different tasks:
  - *Post-hoc regime:* the trajectory text only (what Who&When-style judges consume).
  - *Interventional regime:* trajectory + checkpointed harness with replay access,
    metered by a replay budget C (what ablation / do-then-verify / mutation-kill
    methods consume). Methods are only ever compared within a regime or under
    explicit budget matching (paper.md B-alt).
- **Output:** a blamed component ĉ ∈ K = {plan, tool, obs} (primary task), optionally a
  blamed step index ŝ (secondary task) and a confidence p̂ ∈ [0,1] (for calibration
  scoring). "I cannot localize" is a legal output and is scored, not discarded.

**What counts as the "decisive cause."** The decisive cause of a benchmark trajectory is
defined *counterfactually and by construction*, not by annotation: component c is the
decisive cause iff the trajectory was produced by injecting exactly one fault δ_c into a
reproducibly-succeeding base run, and the certification triple holds —

1. **flip:** the outcome flips from majority-success to majority-failure under k replays of δ_c;
2. **no-op null:** the class-matched no-op substitution δ_∅^c (same edit pathway, no fault)
   does *not* flip the outcome;
3. **identity stability:** the zero-edit identity replay δ_id is stable (intrinsic
   stochasticity below bound).

This is the labeling invariant from paper.md Step 3: a label exists iff
(single injected fault) ∧ (outcome flip) ∧ (controls null). No human judgment is in the
label path; humans appear only in a post-hoc audit of the instrument (κ ≥ 0.7 on a
200-trajectory sample, PG-5).

**Unit of measurement.** The benchmark's atomic unit is one **certified substitution
trial**: the tuple `(base_task, scaffold, backbone, checkpoint, fault_template_id,
component_class c, injected_step s*, k replay outcomes, flip bit, control outcomes,
label ℓ = c)`. Attribution accuracy is `Acc(m) = mean 1[m(τ) = ℓ(τ)]` over certified
trials; every statistic is cluster-robust at the base-task level (trials sharing a base
task are one cluster — the effective n is the cluster count).

**What the paper measures.** Two nested questions: (RQ1) is the instrument itself valid —
does failure *track* the substituted component above the no-op control at all? — and
(RQ_INF_1) given certified labels, how accurate are existing attribution methods,
mechanically scored. RQ1 is a measurement no prior work reports; RQ_INF_1 is what the
released corpus makes repeatable for anyone.

**Critic:** The definition quietly equates "the decisive cause" with "the fault we
injected," and that identity can fail in two ways. First, *latent-cause masking*: the base
run may contain a dormant natural weakness, and the injected fault may merely be the
straw that breaks it — the counterfactual contrast certifies a difference-maker *relative
to this base run*, not "the" unique cause in any absolute sense; calling it THE decisive
cause overclaims. Second, *granularity mismatch with the field*: the crowded literature
(Who&When, TRAIL, AgenTracer) scores *step-level* attribution — where step accuracy is a
dismal ~14% — while B2.1's primary unit is a 3-way component label, which a reviewer can
wave off as "a 3-class problem a coin flips at 33%; you made the task easy enough to be
uninteresting."

**Refined:** Both objections are absorbed into the definition rather than argued away.
(1) The claim is scoped explicitly: ℓ = c certifies that δ_c is a *sufficient
difference-maker relative to a certified-reproducible base run* — the Lewis-style
counterfactual contrast is the definition, stated in those words in the paper; the
reproducibility gate (majority-success base under temperature-0 replay, PG-1) is what
makes "relative to this base" a strong baseline (a run that succeeds 4/5 times has no
*active* natural fault), and the residual masking possibility is registered as threat t3
rather than defined away. (2) The benchmark is two-tier by design: every trial records
the injected step index s*, so **step-level attribution (strict and tolerance-w) is a
first-class secondary metric**, directly comparable to Who&When's 14.2% step numbers —
but on labels that are causally certified instead of human-annotated. The component-level
task is kept as primary not because it is easier but because it is the *actionable* unit
(which pipeline stage do you fix) and the unit at which the certification controls are
clean; the step-level track inherits the same certified trials for free. A random-guess
floor and the frozen surface heuristic B0-b are mandatory baselines precisely so "33%
coin flip" is answered with a measured floor, not a shrug.

---

## Stage 2 — Motivation

**Why mechanical ground truth, and why now.** Agent-trajectory failure attribution is the
single largest tag in the recent arXiv crawl — **53.8% of recent papers** in the tracked
family — and it is crowding fast. But the crowd shares one load-bearing weakness: its
ground truth is **LLM-judge or human-annotated blame labels**. Who&When's labels are
manual; its methods are scored by agreement with those annotations; the best reported
numbers (≈53.5% agent-level, ≈14.2% step-level) are agreement-with-annotators, not
agreement-with-causality. TRAIL's taxonomy labels are expert-annotated. Judge-based
scoring of judge-like methods is circular: a plausible-sounding post-hoc narrative can
score well against a plausible-sounding annotation while both miss the actual causal
locus. Nobody in the 53.8% can currently answer "is the blame *correct*?" — only "is the
blame *agreed with*?"

**The durable artifact argument.** Methods in a crowded area have a half-life of months;
measurement instruments do not. Defects4J (2014) outlived every fault-localization method
evaluated on it because it fixed the ground truth, not a technique. B2.1's bet is the
same shape: when the attribution-method churn washes through, the thing the field keeps
is the corpus whose labels are certified by construction plus the substitution protocol
that manufactures more of them. The audit accordingly classifies B2.1 as family lead and
the label corpus (CO1) + protocol (CO2) as the headline; the method comparison (CO3) is
the demonstration.

**Why FSE.** Fault injection, mutation analysis, and benchmark curation are core SE
methodology; FSE referees will recognize the Defects4J lineage and will *demand* exactly
the controls this design pre-registers (no-op arms, instrument validation, versioned
release). The same paper at an ML venue would be reviewed as "just a dataset."

**Critic:** The crowding statistic cuts both ways, and the strongest version of the
objection is: *the moat is already breached*. AgenTracer already injects faults into
successful traces and labels the decisive step "by construction"; if 53.8% of the field
is here, the expected time until someone publishes an injected-fault *benchmark* (not
just injected-fault *training supervision*) is short — possibly negative. A second
objection: mechanical labels certify a **synthetic** fault distribution; a benchmark of
faults nobody's agent naturally commits could be dismissed as measuring the wrong thing,
however clean its labels ("your ground truth is perfect for a population of zero").

**Refined:** (1) The AgenTracer boundary is the paper's sharpest related-work sentence
and must be stated as such: AgenTracer *uses* injection to mint training rewards for a
learned tracer — one perturbed action, no component taxonomy, no no-op or identity
controls, no measurement of whether failure tracks the substituted component, no released
certified evaluation corpus. B2.1's contribution is the **certification protocol as an
instrument** (controls, validity measurement RQ1, versioned tiers) — the thing that turns
injection from a training trick into ground truth. That delta is real but perishable,
which is exactly why the audit makes the **scoop check mandatory before build** (Stage 6,
with concrete queries and a pre-named pivot: if a certified injected-fault benchmark
already exists, the absorbed axes — cross-backbone label survival and the replay-budget
frontier — become the headline, since no existing artifact reports either). (2) The
synthetic-distribution objection is met three ways, all pre-registered: the fault
taxonomy is grounded in the pipeline's own architecture (the three classes are the three
component slots, not invented categories); every method is *also* scored on the
naturally-failing, human-labeled Who&When set with the gap reported (t1 mitigation,
B-alt's second rival); and the claim discipline deletes the adjective "realistic"
entirely (paper.md Step 5) — the paper claims *validated labels for method evaluation*,
never *representative faults*.

---

## Stage 3 — Related Work

**External nearest neighbors** (real works; [VERIFY] marks anything whose bibliographic
details must be confirmed at the scoop-check step):

- **Who&When** (Zhang et al., "Which Agent Causes Task Failures and When?") — the
  canonical failure-attribution dataset: 127 multi-agent failure logs, *human-annotated*
  responsible-agent and decisive-step labels, LLM-judge attribution strategies
  (all-at-once / step-by-step / binary-search); best ≈53.5% agent / 14.2% step accuracy.
  Boundary: human-agreement labels, no causal certification; B2.1 uses it as the
  natural-failure contrast set and its judges as baselines.
- **TRAIL** (Deshpande et al., "Trace Reasoning and Agentic Issue Localization") —
  expert-annotated taxonomy of errors in agentic traces (GAIA/SWE-bench substrates).
  Boundary: rich taxonomy, annotated labels; no injected ground truth, no protocol for
  certifying a label causally.
- **MAST** (Cemri et al., "Why Do Multi-Agent LLM Systems Fail?") [VERIFY exact venue] —
  failure *taxonomy* from human analysis. Boundary: taxonomy supply, not ground truth.
- **AgenTracer** ("Who Is Inducing Failure in LLM Agentic Systems?") — programmatic fault
  injection into successful traces to mint by-construction decisive-step labels, used as
  RL supervision for a trained tracer. **Closest real precedent.** Boundary (one line):
  injection as *training supervision* for one method vs. injection as a *certified,
  controlled, released measurement instrument* for all methods — no controls, no
  taxonomy, no RQ1-style validity measurement, no corpus release [VERIFY release status
  at scoop check].
- **DoVer** ("Intervention-Driven Auto Debugging") — rewind–edit–replay to test a blame
  hypothesis counterfactually. Boundary: DoVer *verifies one hypothesis per failure*;
  B2.1 *manufactures the ground truth* any verifier can be scored on. DoVer-style
  do-then-verify is an M4 baseline.
- **FAMAS** (spectrum-based failure attribution for MAS) [VERIFY — cited 2026 in sibling
  scout] — SBFL transferred to agent trajectories; correlational suspiciousness.
  Boundary: a method to be scored, and evidence that SE fault-localization machinery is
  actively migrating to agents (timing pressure).
- **AgentDebug / AgentErrorTaxonomy** ("Where LLM Agents Fail and How They Can Learn from
  Failures") [VERIFY] — module-level error typing + earliest-critical-error
  counterfactual test + re-rollout. Boundary: single corrective replay per candidate, no
  budget bound, no certified corpus.
- **Causal Agent Replay (CAR)** and **CausalFlow** [VERIFY — both surfaced as 2026
  preprints in the sibling scout] — SCM-style step-level do() interventions with replay /
  causal responsibility scores. Boundary: attribution *methods* with replay cost as their
  own admitted limitation; both are natural M4 baselines and both make the B2.2-absorbed
  budget axis topical.
- **GraphTracer** (arXiv:2510.10581) [VERIFY] — graph-guided failure tracing. Boundary:
  method, not instrument.
- **Defects4J** (Just et al., ISSTA 2014) — the framing ancestor. Boundary: Defects4J
  annotates real bugs *backward* because a deterministic triggering test certifies each;
  agent pipelines have no such test, which is precisely why B2.1 manufactures ground
  truth *forward* (paper.md Step 0 asymmetry). Also the mutation-testing and delta
  debugging (Zeller & Hildebrandt) lineages, inherited via the two internal adjacents.

**Internal adjacents (portfolio positioning — one-line boundaries so the family does not
self-collide):**

- **Training-free sparse mutation-kill step-credit attribution** (sibling draft
  7882f741): a budget-bounded attribution *method* — rank steps by how often semantic
  mutants flip the oracle under replay budget C. Boundary: B2.1 is the **instrument that
  scores it** — mutation-kill enters B2.1 as one M4 baseline, and its budget-C framing is
  inherited wholesale by B2.1's efficiency section (absorbed B2.2). B2.1 claims no new
  attribution method; the sibling claims no ground-truth corpus.
- **ZV3 Agent Delta Debugging** (sibling draft 88f7a201): statistical certification
  (α/β guarantees) of *minimal failure-inducing sets* over deletion/replacement
  interventions on natural failures. Boundary: ZV3 searches for unknown, possibly
  multi-element causes in naturally failing runs; B2.1 manufactures known single-component
  causes in reproducibly succeeding runs. They are duals — ZV3-style search is an M4
  candidate on B2.1's corpus, and B2.1's single-fault scope explicitly cedes the
  multi-fault / minimal-set territory to ZV3 (threat t5 stays scoped out).
- **ZB2.4 / "False Blame" (certified-infeasible tasks)**: attribution when the task was
  never solvable and the honest label is "unsolvable." Boundary: B2.1's base tasks are
  certified *feasible* by the reproducibility gate, so the infeasibility label-space
  question is excluded by construction and owned by ZB2.4.
- **ZB2.5 / "When the Trace Lies" (schema-valid tool corruptions)**: directional
  misattribution under semantically-false-but-schema-valid tool outputs. Boundary: that
  is a *depth study of one cell* of B2.1's taxonomy; B2.1's tool/obs templates include
  schema-valid variants but its claims stay at certified component level — the
  directional-bias deep dive and the trust-license fix belong to ZB2.5.

**Critic:** Assembled this way, a hostile reviewer compresses the novelty to
"AgenTracer's injection + DoVer's replay + a no-op arm = incremental engineering," and
the [VERIFY]-tagged entries are a second exposure: if CAR/CausalFlow/FAMAS turn out to be
non-archival or misremembered, the related-work section is built partly on sand — while
if they are real and *one of them shipped a certified corpus*, Stage 2's moat claim is
false. The internal positioning has a subtler risk: with four siblings publishing
adjacent drafts, reviewers who find them will ask why this is six papers and not one.

**Refined:** (1) The incrementality compression is answered by relocating the novelty
where no prior work stands: **RQ1 is a measurement that does not exist in the
literature** — no paper reports whether failure actually tracks a substituted component
above matched no-op controls, yet every intervention-based method (DoVer, CAR,
AgenTracer's labeling trick, the mutation-kill sibling) silently assumes it. The paper's
first result is the validity measurement of the field's shared premise; the corpus is
what that measurement certifies. That is not a sum of existing parts. (2) Every [VERIFY]
entry is resolved in the mandatory scoop-check step (Stage 6) *before build*, with a
pre-named pivot if the moat is gone — the tags are a scheduled task, not a hope. (3) The
portfolio question is answered structurally in the paper: B2.1 is the family's
*instrument* paper and cites none of the sibling drafts as prior work (they are
unpublished); internally, the boundary lines above are the contract — B2.1 takes
component-level certified ground truth + validity + efficiency axes; methods
(mutation-kill, ZV3), label-space extensions (ZB2.4), and per-cell depth studies (ZB2.5)
stay outside its claims.

---

## Stage 4 — Sub-problems

**SP1 — Fault-injection taxonomy design.** Which component classes, which templates.
Classes = the pipeline's own slots: plan corruption (delete/reorder/replace a step,
infeasible sub-goal, corrupted planner prompt), tool breakage (error stub, empty/
malformed return, wrong-signature swap), observation pollution (contradiction, noise,
truncation, schema-valid falsehood), with memory-write and environment-state faults as a
candidate fourth/fifth class. *Hard part:* **class purity under severity control** — a
polluted observation is operationally adjacent to a broken tool, and certification
selects for faults severe enough to flip outcomes, so class identity can end up
confounded with fault subtlety (paper.md's E4 severity confound; PG-5's κ ≥ 0.7 audit
with adjacent-class-only confusion is the acceptance test).

**SP2 — Substitution-protocol validity (confound control).** The protocol must prove the
*edit pathway itself* is inert before any flip is attributed to the fault. *Hard part:*
building validated class-matched no-op generators (δ_∅^c: paraphrase-equivalent plan
step, identically-bound tool, re-serialized observation — each audited to κ ≥ 0.7,
≥95% rated equivalent) and separating edit-induced disturbance from intrinsic replay
stochasticity via the identity tier δ_id. This is where the benchmark lives or dies
(A2/A4, PG-2/PG-4): a no-op arm that flips outcomes makes every label noise.

**SP3 — Attribution-method zoo selection and fair comparison.** Which methods get scored:
LLM-judge (3 context strategies), frozen surface heuristic B0-b, ablation/leave-one-out,
DoVer-style do-then-verify, mutation-kill (internal sibling), FAPO/CRM-style step
localizer, random/majority. *Hard part:* **regime fairness** — interventional methods
consume replays and checkpoint access that post-hoc judges lack, so any gap is
confounded with compute until budget-matched (H-sec's budget-matched judge control);
plus external-method reproducibility (PG-6 smoke tests; drop-with-stated-reason, never
silent omission).

**SP4 — Cross-backbone stability of the diagnosis (absorbed B2.3).** If the executor
backbone is swapped, does the certified label survive (does δ_c still flip on backbone
B?) and does a method's diagnosis stay stable (same blamed component)? *Hard part:*
**label non-transfer is the expected case, not the failure case** — a fault certified on
backbone A may be routed around by a stronger backbone B, so "the same benchmark across
backbones" is not well-defined; the design answer is per-backbone certified tiers with a
measured **label survival rate** as a first-class result, not an assumption.

**SP5 — Replay-budget efficiency (absorbed B2.2).** Interventional attribution costs
replays; the benchmark must report accuracy *per unit of replay budget*, and the
labeling protocol itself must know its own minimal k. *Hard part:* **defining a budget
unit comparable across methods** (replays? model calls? tokens?) without privileging any
method family — resolved by metering replays-from-checkpoint as the unit (matching the
mutation-kill sibling's budget C) and reporting token cost as a secondary column; plus
the k-sensitivity question for certification itself (is k = 4 enough for stable labels?).

**Critic:** Five sub-problems is a scope explosion for a 7-week runway, and SP4/SP5 are
each a paper on their own — B2.3 and B2.2 existed as separate topics precisely because
they are deep. Folding them in as required axes risks the classic absorbed-sibling
failure mode: two shallow bonus sections that reviewers read as padding, executed at the
cost of depth on SP1–SP3, which are the actual load-bearing core. Additionally SP1's
"candidate fourth/fifth class" (memory, environment) is scope creep inside a sub-problem.

**Refined:** The absorption contract is made explicit and minimal. SP1–SP3 are the paper;
SP4 and SP5 are **one pre-registered experimental axis each, with fixed minimal
designs and no open-ended exploration**: SP4 = one second backbone (the pinned
open-weights tier that the release plan already requires for longevity — so the
cross-backbone axis reuses infrastructure the versioning story needs anyway), reporting
exactly two numbers per class (label survival rate; per-method accuracy delta) plus one
diagnosis-stability confusion table; SP5 = one budget sweep C ∈ {2, 4, 8, 16} for the
replay-consuming M4 methods on the certified pilot subset, plus one k-sensitivity check
(k ∈ {2, 4, 8}) on a 50-trial subsample for the labeling protocol itself. Both axes are
sized to be cut cleanly (pre-declared descope ladder, Stage 6) without touching the core
claims — if cut, they are named future work, not silent absences. The taxonomy is frozen
at **three classes** for this paper; memory/environment faults are named as the corpus's
v2 extension surface, which also gives the versioned-release story content.

---

## Stage 5 — Methods / Benchmark Design

**Task substrate.** Requirements, in order of priority: (i) *replayable* — tool calls
must return identical results on re-execution; (ii) *checkpointable* — mid-trajectory
state can be restored; (iii) *outcome-testable* — a deterministic pass/fail oracle;
(iv) tool-use-rich (≥ 5 steps typical). This rules out live-web GAIA verbatim and points
to: containerized file-system/CLI tasks (Terminal-Bench-style), local-API tool suites,
and GAIA-style questions served from **cached/snapshotted tool backends** (frozen search
corpus, pinned API fixtures). Target: ~200 base tasks entering the Stage-0 gate, ≥ 60
surviving reproducibility (A1; PG-1 floor 30).

**Injection mechanism.** Orchestrator-message-level edits (DoVer-style), never
weight/state surgery: plan faults edit the plan message; tool faults rebind the tool to a
faulty implementation; observation faults rewrite the return payload en route to the
executor. One fault per trajectory, injected at recorded step s*, replayed forward from
the checkpoint k = 4 times at temperature 0. Fault templates are parameterized with a
pre-registered severity knob (A3/PG-3) — severity is fixed *before* scoring, never tuned
on results.

**Label certification (the core mechanism).** A trial earns label ℓ = c iff:
base run majority-success (reproducibility gate) ∧ δ_c replays majority-failure (flip)
∧ the class-matched no-op δ_∅^c does not flip ∧ identity replay δ_id is stable
(FlipRate(δ_∅^c) ≤ 0.10, FlipRate(δ_id) ≤ 0.05 at the arm level). Non-flipping
injections are *discarded, not mislabeled* (inject ≠ cause, C3). The full control
lattice — identity tier, per-class no-op tier, fault tier — is what distinguishes this
from AgenTracer-style injection.

**Metrics.**
- *Attribution accuracy:* top-1 component accuracy overall and per class; step-level
  strict and tolerance-w accuracy as the secondary track.
- *Directional mis-blame:* the 3×3 confusion matrix P(ĉ = j | ℓ = i), plus a named
  **upstream-blame bias** statistic (rate at which downstream faults — obs — are blamed
  on upstream components — plan — and vice versa); this is the quantity the ZB2.5 sibling
  studies in depth for one cell, reported here at taxonomy level.
- *Calibration:* ECE over p̂ plus selective-risk curves (accuracy at coverage κ when the
  method may abstain) — attribution tools are used to *decide what to fix*, so knowing
  when the method knows is part of the benchmark.
- *Validity (RQ1):* FlipRate(δ_c) − FlipRate(δ_∅^c) per class with cluster-robust CIs.
- *Efficiency (SP5):* accuracy-vs-replay-budget curves; accuracy-per-replay; token cost.
- *Stability (SP4):* label survival rate across backbones; per-method accuracy delta;
  diagnosis agreement rate.

**Baseline suite (M4 + controls).** LLM-judge × {all-at-once, step-by-step,
binary-search}; frozen deterministic surface heuristic B0-b (blame the component hosting
the last step before the first logged error signal — regex/status-code rules, no LLM);
ablation/leave-one-out; DoVer-style do-then-verify; mutation-kill step-credit (internal
sibling method, budget-bounded); FAPO/CRM-style step localizer; random and
majority-class. Controls: budget-matched judge (H-sec — same replay budget as
interventional arms, passively consumed); contamination control (≥ 30 held-out or
paraphrased base tasks scored separately, B-alt-2); Who&When natural-failure contrast.

**Critic:** The substrate choice is the design's soft underbelly, and the critic should
say it plainly: *the reproducibility requirement selects for exactly the tasks where
attribution is easiest.* Deterministic, snapshotted, single-scaffold tasks with clean
tool schemas are the tasks where B0-b's regex heuristic plausibly hits 0.90 — triggering
CR-1's premise-collapse branch — and where "realism" objections bite hardest: the corpus
risks certifying labels for a toy slice while natural agent failures live in the messy,
non-replayable world. Relatedly, temperature-0 + fixed scaffold means the corpus
measures one operating point of one architecture; the cross-backbone axis mitigates the
backbone half but not the scaffold half.

**Refined:** Three commitments. (1) **The easy-slice risk is instrumented, not
denied**: B0-b's accuracy *is* a headline reported number (the heuristic-sufficiency
rate, per class) — if the certified tier is symptom-readable, CR-1 pre-commits the paper
to saying so and to releasing the residual slice (no error signal fired, or signal on a
non-faulted component) as the challenge tier; the fault library deliberately includes
signal-free templates (schema-valid falsehoods, semantically wrong plan steps that crash
nothing) so the residual slice is populated by design, not by luck. (2) **The realism
boundary is priced in**: the paper claims a validated instrument for scoring attribution
methods, contrasts every method against Who&When natural failures with the gap reported,
and deletes "realistic" from its claim vocabulary (Step 5 table). The honest scope
sentence — certified ground truth is currently *manufacturable only where replay is
controllable* — is itself the Step-0 asymmetry, stated as a finding about the field, not
an apology. (3) **Scaffold generality is scoped**: one scaffold for v1, stated in the
title-page claims; the versioned-tier release schema (`corpus-v1-<scaffold>-<backbone>`)
makes additional scaffolds a config-path extension, and the walking skeleton proves
scale-up is config-not-code.

---

## Stage 6 — Experiment Design

**Step 0 — Mandatory scoop check (before any build; ~1 day).** Queries, run over
arXiv + Semantic Scholar + OpenReview + GitHub, window Jan 2025 → now:

1. `("fault injection" OR "injected fault") AND ("failure attribution" OR "blame") AND ("LLM agent" OR "multi-agent")` — looking for any released *benchmark* (not method) with injected ground truth.
2. Forward-citation walk of **AgenTracer**, **Who&When**, and **TRAIL** (papers since Jan 2026 citing them, filtered by "benchmark", "ground truth", "injection", "counterfactual") — the scoop, if it exists, cites at least one of these.
3. `"controlled substitution" OR "component swap" OR "counterfactual replay" AND agent AND benchmark` plus the literal strings `"Defects4J for agents"` / `"agent fault benchmark"` (arXiv full-text + GitHub repo search).
4. FSE/ICSE/ISSTA/ASE 2026–27 accepted-paper and preprint lists filtered for agent + fault/attribution; simultaneously resolve every [VERIFY] tag from Stage 3 (FAMAS, AgentDebug, CAR, CausalFlow, GraphTracer, MAST venue, AgenTracer release status).

*Decision rule:* no certified injected-fault benchmark with controls found → build as
specified. A partial scoop (injection benchmark without validity controls / without
component taxonomy) → build, with the delta sharpened to the certification protocol +
RQ1. A full scoop (certified corpus with controls released) → pivot headline to the two
absorbed axes (cross-backbone label survival + replay-budget frontier), which no
existing artifact reports, reusing the same harness.

**Go/no-go pilot (walking skeleton; ≈$21–105, < 1 day compute).** 20 GAIA-style tasks,
one scaffold, four arms: (1) base + reproducibility gate (target ≥ 12 survivors);
(2) tool-break injection, k = 3; (3) class-matched no-op δ_∅^tool, k = 3; (4) identity
replay δ_id, k = 3. **Pass iff** yield ≥ 12 ∧ crash(δ_∅^tool) ≤ 10% ∧
FlipRate(tool-break) − FlipRate(δ_∅^tool) ≥ 0.20 ∧ δ_id flips ≤ 1 ∧ ≥ 10 labeled
trajectories. Skeleton pass certifies scale-up is a config change. Skeleton fail routes
by tier: no-op crash → harness bug (fix, re-run); identity-tier instability → k↑ once,
then the F-G1 negative-result pivot (which is itself a publishable FSE paper: "the
field's substitution premise does not hold").

**Arms and scale.**

| Arm | Question | Scale (Stage 1 → Stage 2) |
|---|---|---|
| E1 flip-rate vs class-matched no-op + identity tier | RQ1 validity | ≥100 injection + ≥100 no-op per class + ≥100 δ_id → ~3× at Stage 2 |
| E2 method suite vs B0-b floor | do methods beat the trivial floor | n≈300 certified (~100/class) → n≈1,500–3,000 |
| E3 headroom below ceiling | best-method Acc ≤ 0.90? | same corpus |
| E4 plan-vs-tool asymmetry (severity-matched) | class difficulty ordering | same corpus, severity-matched template pairs |
| H-sec budget-matched judge | intervention access vs compute | paired on certified tier |
| **E5 cross-backbone (absorbed B2.3)** | label survival + diagnosis stability | full certified Stage-1 set re-certified on pinned open-weights backbone-2 (~300 trials × k=4, local GPU) |
| **E6 replay-budget (absorbed B2.2)** | accuracy per replay; minimal k | budget sweep C∈{2,4,8,16} on certified pilot subset (~100 trials × 4 budgets × 3 methods); k-sensitivity k∈{2,4,8} on 50 trials |

All inference cluster-robust at base-task level; powered-cell rule: cells < 80 certified
trajectories or simulated cluster-robust power < 0.8 are pre-declared INCONCLUSIVE.
Human audits: PG-5 taxonomy audit (2 raters, 200 trajectories, κ ≥ 0.7) + δ_∅ and B0-b
calibration slices (50 each).

**Compute estimate.** Primary backbone: ~200 base tasks × 5 gate replays + ~3 classes ×
5 templates × ~60–100 tasks × (1 + k) runs + no-op/identity arms + method-suite replays
≈ **15,000–30,000 agent runs**; at $0.10–0.50/run ⇒ **$2k–6k API** at Stage-2 scale
(Stage 1 alone ≈ $500–1,500). E5 runs on a pinned open-weights backbone on local GPUs
(the same tier the release-longevity plan requires) — GPU-days, not API dollars. E6
reuses certified trials, ~1,200 extra replays ≈ $150–600. Total within a small-lab
budget; the walking skeleton bounds the downside to ~$100 before commitment.

**FSE-2027 milestone plan (working back from Oct 2, 2026; today Aug 13).**

| Window | Milestone | Gate |
|---|---|---|
| Aug 13–16 | Scoop check + [VERIFY] resolution + substrate freeze | scoop decision rule |
| Aug 17–21 | Harness + walking skeleton | **go/no-go Aug 21** (PG-2/3/4 in miniature) |
| Aug 22–Sep 4 | Stage 1: Stage-0 gate at scale (PG-1), δ_∅/B0-b generator validation, E1 complete, first certified n≈300, method smoke tests (PG-6) | E1 verdict Sep 4; H1-partial ⇒ certified-tier partition |
| Sep 5–18 | Stage 2 scale to n≥1,500 certified; E2–E4 + H-sec; **E5 backbone tier; E6 budget sweep**; PG-5 human audit runs in parallel from Sep 8 | powered-cell check Sep 15 |
| Sep 12–25 | Analysis + writing in parallel (intro/method sections start Sep 12 from paper.md's pre-registered skeleton) | full draft **Sep 26** (hard internal deadline) |
| Sep 26–29 | Internal review: se-paper-reviewer pass + novelty audit + threats section | |
| Sep 29–Oct 1 | Artifact packaging (versioned corpus tier, harness, re-certification script) + submission buffer | submit ≤ Oct 1 |

**Critic:** Seven weeks end-to-end for a benchmark paper is the plan's single biggest
risk, and the milestone table hides three fragilities. (1) It assumes the walking
skeleton passes on the first harness build — checkpoint-replay infrastructure for agent
scaffolds is notoriously fiddly, and one lost week (a realistic estimate for cache-layer
bugs alone) cascades into everything. (2) The PG-5 human audit (2 independent raters,
200 trajectories, κ ≥ 0.7, with a re-taxonomize-and-revalidate loop on failure) is on
the critical path in the busiest window; rater recruitment alone can eat the slack.
(3) Stage-2 scale (n≈3,000 in paper.md) plus two absorbed axes plus a full method suite
is quietly more compute-hours and analysis than the two-week window Sep 5–18 holds.
If any two of these slip, the plan delivers a rushed draft to the field's most
methodology-sensitive venue.

**Refined:** The plan ships with a **pre-declared descope ladder**, cut in this order
and never renegotiated at deadline time: (D1) Stage-2 target drops from 3,000 to the
1,500 floor (the powered-cell rule, not the round number, is binding — ~100+ certified
per class per cell suffices for the 0.10-gap tests); (D2) E6 shrinks to the k-sensitivity
check plus a single-budget-pair comparison (C = 4 vs 16), full sweep to camera-ready;
(D3) E5 shrinks to the tool-fault class only (label survival is most interpretable
there), full-taxonomy backbone tier to camera-ready; (D4) FAPO/CRM-style localizer
dropped from the zoo (PG-6 wording covers it). The core that is never cut: E1 + controls,
E2/E3 on the certified tier, B0-b, PG-5 audit — that set alone is the FSE paper. Schedule
hardening: harness work starts Aug 14 *in parallel* with the scoop check (the scoop
decision only gates *scale-up*, not harness construction, and the harness survives every
pivot including F-G1); raters are recruited **now** (Aug 17 target) with the audit run
incrementally as certified trajectories accumulate rather than as a Sep batch; writing
starts from paper.md's pre-registered skeleton on Sep 12, so the draft is assembled, not
composed, in the final fortnight. Venue fallback pre-named: if the Sep 26 full-draft gate
fails, the target rolls to **ISSTA 2027 / ASE 2027** with the extra months spent on the
full Stage-2 scale and both absorbed axes at full size — the deadline pressure is real,
but the artifact's value does not expire on Oct 2; only the crowding clock argues for
FSE, which is why the descope ladder exists.

---

*End of discussion. Upstream documents: `README.md` (seed), `digest.md` (N0–N12),
`paper.md` (pre-registered spec). Downstream: `discussion/experiment_design.md` and the
draft under `discussion/` should be reconciled with the two absorbed axes (E5, E6) and
the descope ladder introduced here.*
