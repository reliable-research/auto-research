# Poison Half-Life: A Censoring-Aware Survival Analysis of Agent Memory Poisoning Under Memory-Management Policies

> Assembled from the six confirmed stage outputs in `discussion_trace.md`, post-audit (`taste_audit.md`: 🟢) and post-review (`stage_review.md`: two REVISE fixes applied). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets with stated rationale, not results. This is defensive-security measurement research: poison is instantiated only from already-published attacks used as a fixed treatment, and every question is about how long adversarial content *persists* under benign management policies, to inform defenses — no attack recipe is given.

## Abstract

Autonomous agents that persist across sessions keep a long-lived memory, and the memory-management policies that make that memory useful — summarization, consolidation and reflection, eviction and time-to-live, deduplication — are tacitly trusted to also let benign traffic wash adversarial content out over time. We show this trust rests on a measurement that cannot express its own answer: the persistence of memory poisoning is reported as a fixed-checkpoint binary (is the poisoned claim present after a repair step?), which cannot state a neutralization *rate* and silently equates a claim's literal removal with the end of its behavioral influence. We treat each injected poisoned claim as the subject of a survival analysis and estimate its behavioral-adoption survival function, hazard, and half-life over benign interaction time, under a censoring-aware estimator that handles both right-censoring (poison that outlives the horizon) and the interval-censoring of intermittent probes. Neutralization is defined behaviorally — the agent's action ceases to be steered by the claim, read out by a validated mechanical probe — not by literal detectability, so *laundering* (a claim that survives summarization in a detector-invisible but behaviorally-active form) becomes its own measurable state rather than a false "repair." We make memory-policy aggressiveness the manipulated treatment, replaying identical benign traffic across policy levels with a matched-salience benign tracer as the isolating control, and separate content-neutralization from structural eviction as competing risks. The central pre-registered test asks whether utility-improving policies *lengthen* poison half-life — reclassifying the step the field scores as repair as a persistence-amplifying laundering step — or whether persistence is invariant to policy, which would cleanly refute it.

## Introduction

Autonomous agents that persist across sessions now keep a long-lived memory: a store of past observations, distilled reflections, and reusable facts that the agent writes to, reads from, and acts on across many interactions (Packer et al., 2023; Park et al., 2023). Because that store grows without bound, every practical deployment runs a memory-management policy over it — summarizing old context to fit a window, consolidating episodes into reflections, expiring stale entries by time-to-live, deduplicating near-repeats. These policies are chosen for utility, and they carry an unstated security dividend that operators increasingly lean on: the belief that a long stream of benign interactions, filtered through summarization and eviction, will eventually wash adversarial content out of memory on its own — that poisoning is a transient the system self-heals.

Yet a security question about that memory is measured with an instrument that cannot express its answer. The persistence of a memory-poisoning attack is reported as a fixed-checkpoint binary — after a write, an execution, and a repair step, is the poisoned claim still there? (Chen et al., 2026). A binary at one observation time cannot state how *fast* poison is neutralized, cannot distinguish a policy that cleans slowly from one that never finishes, and — most consequentially — conflates two things a defender must keep apart: whether the claim's literal text has been removed from the store, and whether the claim has stopped steering the agent's behavior. These are already known to come apart. Injection and execution dissociate across models (Leong, 2026a), and adversarial content can survive summarization in a form a content detector no longer flags while still shaping what the agent does (Wang et al., 2026). A measurement built on literal presence scores such a laundered claim as repaired at the exact moment it becomes most dangerous.

The nearest prior work approaches this from an adjacent angle. Persistence benchmarks establish that poisoning survives repair at high rates, but as a checkpoint probability, not a survival curve, with the memory policy fixed inside the benchmark rather than manipulated (Chen et al., 2026). Mechanistic evaluations show injection and execution decouple across defenses and models, but over short horizons and without a persistence-over-time estimand (Leong, 2026a). The laundering mechanism itself has been demonstrated as an existence result — that content *can* survive summarization invisibly — but on a single pathway, never as a rate that scales with how aggressively memory is managed (Wang et al., 2026). None of these treats the memory-management policy as a variable to turn up or down, and none reports a neutralization time. The gap is not that persistence is unstudied; it is that persistence has never been measured as a rate that a management policy can move.

Turning persistence into a measurable rate surfaces its own difficulties. Neutralization is never observed directly: probes are intermittent, so the event falls between two observations (interval censoring), and some poison outlives the horizon entirely (right censoring) — a fixed checkpoint discards exactly this structure. The event itself must be defined as loss of *behavioral* adoption rather than literal removal, or laundering is scored as repair and the study builds its own opposite into the instrument. Memory policies are chosen for utility and change what the agent sees and stores, so a raw correlation between an aggressive policy and longer persistence could be salience or reduced exposure to corrective evidence rather than laundering — and because aggressive summarization compresses the same benign stream, holding the input stream fixed does not hold *exposure* fixed. Finally, a claim can stop being adopted for two unrelated reasons — its content was corrected, or its whole memory slot was evicted by a time-to-live rule regardless of content — and a half-life that lumps these together is uninterpretable.

Our design turns each of these obstacles into a specific measurement choice rather than a hedge. Each poisoned claim becomes a survival subject, and its behavioral-adoption survival function and hazard are recovered from interval-censored probes with a censoring-aware estimator, so a half-life with a confidence interval replaces a checkpoint. The event is read behaviorally by a validated mechanical probe, with literal detectability tracked as a *separate* covariate, so the laundering state — literally absent yet still behaviorally adopted — becomes a cell one can count rather than a blind spot. Memory-policy aggressiveness is the manipulated treatment, with identical benign traffic and identical injected claims replayed across policy levels and a matched-salience benign tracer as the isolating control, so the residual exposure confound is closed by the tracer's invariance rather than assumed away. And content-neutralization is separated from structural eviction as competing risks, so the laundering claim can be made specific: that aggressive policy lowers the rate at which a claim's *content* is corrected, not the rate at which its slot is mechanically evicted.

We evaluate this design across long benign interaction streams drawn from a long-term memory benchmark, with poison instantiated only from published attacks used as fixed treatments, on a grid of memory-management policies crossed with published defenses, comparing against a single-checkpoint evaluation, an append-only control policy, and the benign tracer placebo.

In summary, we contribute:
- A censoring-aware persistence estimand for agent memory poisoning — a behavioral-adoption survival function, hazard, and half-life over interaction time — of which the fixed-checkpoint persistence binary used by current benchmarks is the degenerate single-observation-time special case.
- A behavioral event definition that separates a poisoned claim's continued steering of the agent from its literal detectability, making *laundering* (detector-invisible but behaviorally active) an explicitly measured state rather than a false repair, together with a validated mechanical acceptance probe for reading it.
- A policy-as-treatment design, with matched replayed traffic and a matched-salience benign tracer as the isolating control, that estimates the causal effect of memory-management aggressiveness on the persistence hazard and separates laundering from salience and from reduced exposure to corrective evidence.
- A pre-registered test of the reclassification hypothesis — that utility-improving memory management *lengthens* poison half-life, making the step the field scores as repair a persistence-amplifying laundering step — with a competing-risks decomposition that pins any such effect on the content-neutralization hazard specifically, and a clean falsification (half-life invariant to policy) stated in advance.

## Problem Definition

**Formal setup.** An agent maintains a memory store *M_t* that evolves over benign interaction time *t* = 0, 1, …, *T* under a memory-management policy *π* and an optional defense *d*. At *t* = 0 a fixed, already-published attack injects a set of poisoned claims *P* = {*p₁*, …, *pₙ*} into the store; the attack is a treatment, not a contribution of this work. For each claim *pᵢ*, an acceptance probe *a*(*pᵢ*, *t*) ∈ {adopted, not-adopted} decides, mechanically, whether the agent's action at time *t* is steered by *pᵢ*. The neutralization time is τᵢ = the first *t* after which *a*(*pᵢ*, ·) is *durably* not-adopted (remains not-adopted through all subsequent probes), and τᵢ is right-censored at *T* if no such *t* exists. A separate literal-presence indicator *ℓ*(*pᵢ*, *t*) ∈ {present, absent} records whether *pᵢ*'s content is still detectable in *M_t* by a content detector. The object of study, per (*π*, *d*) cell, is the survival function *S*_{π,d}(*t*) = P(τ > *t*), the hazard *h*_{π,d}(*t*), and the half-life *t*₁/₂ = inf{*t* : *S*(*t*) ≤ 0.5}; the state {*ℓ* = absent, *a* = adopted} is the *laundering* signature. Because *a* is observed only at intermittent probe times spaced Δ apart, τᵢ is additionally interval-censored to the window between the last adopted and first durably-not-adopted probe.

**Why this is hard.** Four properties of this estimand defeat a fixed-checkpoint measurement. First, τ is observed only through a discrete probe schedule and a finite horizon, so both interval-censoring (the event lies inside a probe gap) and right-censoring (the event never occurs before *T*) are structural, not incidental — a single checkpoint discards them and returns a probability at one time in place of a rate. Second, the event must be behavioral adoption, not literal presence: *ℓ* and *a* provably diverge under laundering, so an estimator keyed on *ℓ* would record τ at the moment a claim becomes detector-invisible while it is still steering behavior — the exact inversion the study exists to detect. Third, *π* is chosen for utility and alters both what enters *M_t* and how much of the benign stream the agent is exposed to (aggressive summarization compresses it), so a correlation between aggressive *π* and larger τ could be salience or reduced exposure to corrective evidence rather than laundering; holding the *input* stream fixed does not hold *exposure* fixed. Fourth, τ can be reached by two competing causes — the claim's content is corrected, or its slot is evicted by a time-to-live/dedup rule regardless of content — whose naive pooling biases each other's hazard and renders *t*₁/₂ uninterpretable, while the laundering hypothesis is specifically a claim about the *content-correction* cause.

## Method Overview

At a conceptual level the study is a single measurement pipeline with five cooperating parts that turn a stream of intermittent yes/no probes into a policy-attributable, cause-resolved persistence rate. Injected claims and a benign traffic stream enter the pipeline; a censoring-aware estimator turns the probe sequence into a survival curve and a half-life; a behavioral probe (paired with a literal-presence detector) decides what the event *is* and exposes the laundering state; a policy-as-treatment contrast turns the curve into a causal effect of memory-management aggressiveness; a validation protocol makes the probe's readings trustworthy; and a competing-risks decomposition makes the resulting half-life interpretable by separating content-correction from structural eviction.

The **censored persistence estimator** takes each claim's interval-censored probe sequence and the horizon and returns a survival function, a hazard, and a half-life with a confidence interval, reporting cells that never cross the half-life as right-censored rather than dropping them. The **behavioral acceptance probe** decides neutralization by whether the agent's action is steered by the claim, records literal detectability in parallel, and defines the laundering cell where the two disagree. The **policy-as-treatment contrast** makes memory-management aggressiveness the manipulated variable, replays identical claims and traffic across policy levels, fits a proportional-hazards model with policy as the covariate, and uses a matched-salience benign tracer as the control that isolates laundering from salience and exposure. The **acceptance-probe validation** anchors the event's ground truth in a mechanical task outcome and validates it against human raters before any curve is trusted. The **competing-risks decomposition** separates content-neutralization from structural eviction as cause-specific hazards on a normalized interaction-time axis, so the laundering effect can be pinned on the content cause specifically.

## Methodology

### Censored Persistence Estimator

**Challenge.** Neutralization is observed only through intermittent probes and a finite horizon, so the raw data are interval-censored and right-censored; a fixed-checkpoint binary discards this and cannot express a neutralization rate or a half-life at all.

**Insight.** Re-reading "is the claim adopted at time *t*?" as repeated interval-censored observations of one survival subject recovers the full survival and hazard functions, of which the checkpoint binary is simply the survival function evaluated at one time and thresholded — so the continuous estimand strictly contains the checkpoint, rather than competing with it.

**Method.** Each poisoned claim is a survival subject with event time τ (durable loss of behavioral adoption). From the probe sequence we estimate the survival function *S*(*t*) with a nonparametric estimator appropriate to interval-censored data (Turnbull's estimator when probe gaps straddle events; Kaplan–Meier on the right-censored reduction when events are localized to a single gap), and the cumulative hazard with a Nelson–Aalen estimator (Kaplan and Meier, 1958; Nelson–Aalen). The half-life is the median survival time with a bootstrap confidence interval; cells whose *S*(*t*) does not reach 0.5 within *T* are reported as half-life ≥ *T* (right-censored), never coerced to a point value. We additionally test each cell's hazard against the constant-hazard (exponential) null, because a non-constant hazard is precisely the time structure a single checkpoint cannot summarize.

### Behavioral Acceptance Probe

**Challenge.** If neutralization is scored by whether the claim's literal text is still retrievable, a laundered claim — surviving summarization in a detector-invisible but behaviorally-active form — is recorded as repaired while it is still steering the agent, building the study's opposite conclusion into its instrument.

**Insight.** Separating behavioral adoption from literal detectability is what makes laundering *observable* as its own state rather than a blind spot: a single content-match metric conflates the two and cannot see the {literally absent, behaviorally adopted} cell where laundering lives.

**Method.** Neutralization is scored by a mechanical acceptance probe — a task whose correct output flips if and only if the poisoned claim is behaviorally adopted (for example, a query whose ground-truth answer differs depending on whether the agent acts on the injected claim), so the event's ground truth is a task outcome, not a subjective judgment. In parallel, a content detector records the literal-presence indicator *ℓ* on the same schedule; the detection instrument is the trajectory-signature detector of published defense work (Leong, 2026b), used here as the literal-presence covariate. The laundering cell is defined as {*ℓ* = absent, *a* = adopted}, and its per-cell frequency is a first-class reported quantity.

### Policy-as-Treatment Contrast

**Challenge.** Memory-management aggressiveness is chosen for utility and co-varies with content salience and with how much benign, potentially corrective traffic the agent is exposed to, so a raw association between aggressive policy and longer persistence is not yet evidence of laundering.

**Insight.** Replaying identical injected claims and identical benign traffic across policy levels converts the utility–persistence confound into a within-subject contrast — but this alone does not close the loop, because aggressive summarization compresses the identical stream and so reduces *exposure* to corrective evidence; the matched-salience benign tracer is the load-bearing control that closes exactly this gap, since if reduced exposure (not laundering) were the mechanism, a benign claim of matched salience would persist longer under aggressive policy too. The poison hazard ratio is interpretable as laundering only conditional on the tracer's hazard ratio being null.

**Method.** Memory-policy aggressiveness is the manipulated treatment, instantiated at three levels — append-only (minimal), periodic summarization (moderate), and consolidation/reflection with deduplication and time-to-live (aggressive) — drawn from documented memory-control-plane configurations (Yang, 2026). The same claims and benign stream are replayed across levels. Because adoption is observed only on the fixed probe grid, the hazard regression is specified as a *grouped-time* proportional-hazards model — a complementary log-log link on per-interval event indicators, the discrete-time counterpart of the Cox model (Cox, 1972) that is exact under interval-censored observation rather than an approximation to it — yielding a hazard ratio for aggressive-versus-minimal policy; the proportionality assumption is checked with policy-by-time interaction diagnostics, and where it fails, the pre-registered fallback contrast is the difference in restricted mean survival time over the horizon, which needs no proportionality and remains estimable in heavily censored cells where the median does not. A matched-salience benign tracer claim, injected alongside the poison and probed identically, is run through the same contrast as the placebo whose hazard ratio must be shown equivalent to null (not merely non-significant) for the poison effect to read as laundering.

### Acceptance-Probe Validation

**Challenge.** An unreliable probe injects measurement noise indistinguishable from real hazard, so an unvalidated event reading would make the survival curve a measurement of the probe rather than of the poison — and its error could be comparable to the effect being estimated.

**Insight.** Anchoring the event's ground truth in a mechanical task outcome makes it reproducible, but reproducibility must still be demonstrated against human judgment before any curve is trusted; this is a measurement-reliability step, logically separate from the construct choice of what the event *is*.

**Method.** The probe is pre-registered as a deterministic decision rule and validated against at least two independent human raters on a held-out probe set, requiring Cohen's κ ≥ 0.7 and an adjacent/borderline-only confusion structure (no systematic misread of one adoption type), audited on 50 probes in the pilot and 300 before scale-up. A κ below threshold blocks scale-up and triggers probe-rule refinement rather than being absorbed into noisier curves.

### Competing-Risks Decomposition

**Challenge.** A poisoned claim can stop being adopted because its content was corrected or because its whole memory slot was evicted by a time-to-live/dedup rule regardless of content; a half-life that pools these two exits is uninterpretable, and the laundering hypothesis is specifically about the content-correction rate.

**Insight.** The laundering prediction is sharp only under a competing-risks view: aggressive policy should lower the *content-neutralization* cause-specific hazard (correction stalls once the claim is detector-invisible) while leaving the *structural-eviction* cause-specific hazard unchanged — a directional prediction a pooled survival curve cannot even state.

**Method.** We model content-neutralization and structural-eviction as competing risks via cause-specific hazards and cumulative incidence functions, on an interaction-turn-normalized time axis so cells with different traffic volume are comparable. The per-cell persistence classification (e.g. fast-cleaned / slow-cleaned / laundered / structurally-evicted) is computed from the cause-specific curves, and its stability is checked by recomputing it on two disjoint random half-samples of the injected claims.

## Experiments

### Experimental Setup

**Benign streams and configurations.** Long benign interaction streams are drawn from a long-term memory benchmark (Uddin et al., 2026) — chosen because the central hazard-ratio question and its placebo need streams long enough that the right-censoring fraction at horizon *T* stays low enough for the half-life confidence interval to close; a short stream would leave most subjects censored and underpower the headline contrast. Memory-management policy levels (minimal / moderate / aggressive) are instantiated from documented memory-control-plane configurations (Yang, 2026). All runs are sandboxed with no live-deployment side effects.

**Treatments (published, used as fixed treatments — not contributions).** Poison is instantiated only from already-published attacks: the persistence-benchmark attack of Chen et al. (2026), the memory-poisoning attack of Devarangadi Sunil et al. (2026), and the summarization-surviving (laundering-prone) contamination of Wang et al. (2026), spanning single-fact, procedural, and consolidation-surviving poison types. Defenses enter the grid as fixed treatments, not as systems evaluated on their own leaderboards: A-MemGuard (Wei et al., 2025), MemLineage (Ouyang and Hou, 2026), the trajectory-signature detector (Leong, 2026b), and the repair ("Forget") step of the persistence benchmark (Chen et al., 2026).

**Baselines** (sanity-check comparators, not competitors — this is a measurement study, and no research question is framed as "our procedure beats baseline X"). The fixed-checkpoint Write–Execute–Forget protocol (Chen et al., 2026) is run as a single-observation-time evaluation to show empirically that thresholding one checkpoint mis-estimates the continuous survival curve. An append-only / no-management policy is the null against which "aggressiveness" is defined. The matched-salience benign tracer is the placebo whose persistence must be policy-invariant.

**Design grid and sample size.** Full grid: 3 policy levels × 5 defense conditions × ≥3 attack families × ≥3 backbones. Pilot: 1 backbone × 3 policies × {no defense, A-MemGuard} × 1 attack family. Per (policy × defense) cell we inject n = 60 poisoned claims (survival subjects) — sized so that under an anticipated ~50% censoring fraction the Kaplan–Meier median (half-life) confidence-interval half-width falls below 0.15·*T*; a pilot cell exceeding that width triggers a pre-committed enlargement to 150 claims/cell, not a null claim. Horizon *T* = 200 benign interaction turns; probes every Δ = 10 turns (the interval-censoring width). All parameters are frozen and hashed before evaluation.

**Compute budget and determinism.** The full grid is 3 × 5 × 3 × 3 = 135 cells per replication. Each cell runs one *T* = 200-turn stream plus, at each of the 20 probe times, one probe battery over its 120 subjects (60 poison + 60 tracer claims): ≈ 27,000 stream turns and ≈ 324,000 probe calls per full-grid replication — order 10⁵–10⁶ model calls per backbone, dominated by probe calls, which is why probes are batched per probe time and why the 6-cell pilot must price a per-cell cost before any scale-up is committed. Backbone model identifiers and versions are pinned in the frozen configuration; probe and detector calls run at temperature 0 with fixed decoding parameters; agent-turn non-determinism is handled by re-running every pilot cell once with a different seed and reporting the between-run half-life discrepancy as a floor on interpretable cross-cell differences before any cross-cell comparison is made.

**Metrics.** The behavioral-adoption survival function, its Nelson–Aalen hazard, and the half-life with bootstrap CI; the constant-hazard-null test outcome per cell; the policy hazard ratio for aggressive-vs-minimal (grouped-time proportional-hazards; pooled and per backbone); the laundering-cell frequency and its trend across policy levels; the content-neutralization and structural-eviction cause-specific hazards; and the split-half persistence-classification agreement rate.

**Research questions:**
1. RQ1 — Does continuous survival estimation recover persistence structure a fixed checkpoint cannot?
2. RQ2 — Does poison half-life increase with memory-management aggressiveness?
3. RQ3 — Is the policy effect specific to adversarial content, or does a matched-salience benign tracer persist too?
4. RQ4 — Is the persistence increase carried by laundering rather than by literal retention?
5. RQ5 — Does the persistence effect appear in the content-neutralization hazard specifically (Forget-as-amplification)?
6. RQ6 — Is the per-cell persistence classification stable across independent random sub-samples?
7. RQ7 — Does the mechanical acceptance probe agree with human adjudication?

#### RQ1: Does continuous survival estimation recover persistence structure a fixed checkpoint cannot?

**Setup.** For each (policy × defense) cell, estimate the interval-censored survival function and half-life with bootstrap CI, and test the cell's hazard against the constant-hazard (exponential) null. Compare the continuous estimate against the fixed-checkpoint binary evaluated at the benchmark's repair time.

**Expected outcome.** For at least 80% of tested cells the estimator returns a half-life whose 95% CI half-width is below 0.15·*T*, and the hazard is statistically non-constant (rejects the exponential null at α = 0.05, Holm-corrected) in at least half of tested cells — establishing that persistence has a time structure a single checkpoint cannot summarize, and that the checkpoint's thresholded value falls outside the continuous estimator's band in a nontrivial fraction of cells.

**Falsification condition.** Refuted if the hazard is statistically constant (exponential not rejected) in the large majority of cells — then a single rate suffices and the continuous estimator adds nothing over a checkpoint — or if the half-life CIs fail to close (half-width ≥ 0.15·*T*) in most cells even after the pre-committed enlargement, meaning the estimand is not recoverable at feasible sample sizes.

**Hypothesis (plain language).** Poison neutralization has a shape over time, not just an endpoint, and that shape is measurable — so a checkpoint binary is a lossy special case of the rate, not an equivalent summary.

**Metrics.** Per-cell half-life and CI half-width; fraction of cells rejecting the constant-hazard null; checkpoint-vs-curve discrepancy rate.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Does poison half-life increase with memory-management aggressiveness?

**Setup.** Grouped-time proportional-hazards model (complementary log-log link on probe-interval event indicators — the discrete-time Cox specification, exact under interval censoring) of the behavioral-adoption hazard on policy level (minimal / moderate / aggressive), with identical claims and benign stream replayed across levels; hazard ratio for aggressive-vs-minimal, Holm-corrected across defenses and backbones; sign and magnitude checked per backbone; proportionality checked by policy-by-time interaction, with restricted-mean-survival-time difference as the pre-registered fallback contrast where it fails.

**Expected outcome.** Poison half-life is monotonically non-decreasing in memory-policy aggressiveness, with a hazard ratio for aggressive-vs-minimal policy ≤ 0.7 (|log HR| ≥ 0.36, Holm-corrected p < 0.05) under the behavioral-adoption event — i.e. the more aggressively memory is managed for utility, the *longer* poison survives.

**Falsification condition.** Refuted toward *policy-invariance* if the aggressive-vs-minimal hazard-ratio CI contains 1 in the majority of cells (half-life does not move with policy) — the clean refutation of the reclassification hypothesis; refuted toward the *cleanup intuition* if HR > 1 with |log HR| ≥ 0.36 (aggressive policy significantly *shortens* half-life), meaning utility-improving management does wash poison out faster, as operators assume.

**Hypothesis (plain language).** Utility-improving memory management prolongs, rather than shortens, the time a poisoned claim keeps steering the agent.

**Metrics.** Policy hazard ratio and CI (pooled and per backbone); half-life by policy level; monotonicity across the three levels; proportionality diagnostic and, where invoked, the restricted-mean-survival-time difference.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Is the policy effect specific to adversarial content, or does a matched-salience benign tracer persist too?

**Setup.** Run the matched-salience benign tracer claims through the identical policy contrast (same replayed traffic, same probe schedule, same grouped-time hazard specification) as RQ2, with the tracer arm sized identically to the poison arm (n = 60 tracer claims per cell) so the placebo cannot pass by being underpowered; compare the tracer's aggressive-vs-minimal hazard ratio against the poison's.

**Expected outcome.** The benign tracer shows no policy-dependent persistence effect, demonstrated by equivalence rather than by failure to reject: its aggressive-vs-minimal log-hazard-ratio falls within a pre-registered equivalence margin of |log HR| < 0.18 (half the poison effect floor of RQ2) under a two-one-sided-tests (TOST) procedure at α = 0.05 — so the poison effect in RQ2 is specific to adversarial content, not generic retention of, or reduced corrective exposure for, any salient content.

**Falsification condition.** Refuted if the benign tracer *also* persists significantly longer under aggressive policy (its hazard-ratio CI excludes 1 in the same direction as the poison's) — then the RQ2 effect is generic retention or reduced exposure to corrective traffic, not poison-specific laundering, and the causal reading of RQ2 is invalid (the run measures a salience/exposure artifact, per the placebo discipline). Distinctly, the control is *unresolved* — not passed — if the tracer arm can neither show a directional effect nor establish equivalence at the pre-registered margin: an underpowered placebo is treated as a failed control that blocks the causal reading, never as a passed one. This is the study's primary placebo: anything other than demonstrated tracer equivalence invalidates the causal claim regardless of how strong RQ2 looks.

**Hypothesis (plain language).** The policy effect is about adversarial content being laundered, not about aggressive memory simply holding on to whatever is salient.

**Metrics.** Benign-tracer hazard ratio and CI; TOST equivalence outcome at the pre-registered margin; poison-vs-tracer hazard-ratio difference.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Is the persistence increase carried by laundering rather than by literal retention?

**Setup.** Within each policy level, measure the frequency of the laundering cell {literally absent, behaviorally adopted} and the frequency of literal retention {literally present, behaviorally adopted}; test whether the laundering-cell frequency increases with policy aggressiveness and whether it, rather than literal retention, accounts for the RQ2 hazard shift.

**Expected outcome.** The laundering-cell frequency is strictly greater than zero and increases with policy aggressiveness, and the policy→persistence effect is carried by this cell rather than by increased literal retention — behaviorally-active-but-detector-invisible claims become more common exactly as memory is managed more aggressively.

**Falsification condition.** Refuted if the persistence increase is accounted for by rising literal presence (aggressive policy *retains* more poison literally) with the laundering cell flat or empty across policy levels — then the mechanism is retention, not laundering, and the "detector-invisible persistence" claim falls even if RQ2 holds.

**Hypothesis (plain language).** Aggressive management does not keep the poison's text around; it keeps the poison's influence around after the text is gone.

**Metrics.** Laundering-cell and literal-retention-cell frequencies by policy level; mediation of the RQ2 hazard shift by the laundering cell.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Does the persistence effect appear in the content-neutralization hazard specifically (Forget-as-amplification)?

**Setup.** Estimate cause-specific hazards for content-neutralization versus structural-eviction (and their cumulative incidence functions) per policy level; test whether the aggressive-policy effect lands in the content-neutralization hazard and not the structural one. Additionally compare behavioral-adoption hazard immediately before and after the benchmark's "Forget"/repair operation under aggressive consolidation.

**Expected outcome.** The two cause-specific hazards are separately estimable, and the aggressive-policy effect appears in the content-neutralization hazard specifically — aggressive management lowers the rate at which a claim's content is corrected while leaving structural eviction unchanged — so the operation the benchmark scores as repair does not durably lower behavioral adoption under aggressive consolidation.

**Falsification condition.** Refuted if the aggressive-policy effect appears in the *structural-eviction* hazard (aggressive policy simply evicts slots more slowly) rather than the content-neutralization hazard, or if post-"Forget" behavioral adoption drops below tolerance and stays down — in which case the Forget step genuinely repairs and the amplification reclassification fails.

**Hypothesis (plain language).** The step called repair does not correct the claim's content; under aggressive consolidation it stops correction from finishing.

**Metrics.** Content-neutralization vs. structural-eviction cause-specific hazards by policy level; pre-vs-post-Forget behavioral-adoption hazard.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Is the per-cell persistence classification stable across independent random sub-samples?

**Setup.** Split each cell's injected claims into two disjoint random halves; compute the persistence classification (fast-cleaned / slow-cleaned / laundered / structurally-evicted) independently on each half; compare agreement across cells.

**Expected outcome.** The two half-sample classifications agree in at least 80% of tested cells — the persistence label describes the cell, not which particular claims happened to be sampled.

**Falsification condition.** Refuted if agreement falls below 80% of cells, meaning the classification is driven by sampling noise rather than a stable cell-level property, and per-cell persistence labels should not be reported.

**Hypothesis (plain language).** The persistence verdict for a cell is a property of the policy-and-defense condition, not an artifact of the specific poisoned claims drawn.

**Metrics.** Split-half classification agreement rate across cells.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Does the mechanical acceptance probe agree with human adjudication?

**Setup.** On a held-out probe set (50 probes in the pilot, 300 before scale-up), compare the mechanical acceptance-probe verdict against at least two independent human raters; compute Cohen's κ and inspect the confusion structure.

**Expected outcome.** The probe agrees with human adjudication at Cohen's κ ≥ 0.7, with disagreements confined to adjacent/borderline cases rather than a systematic misread of one adoption type — validating the event definition that every survival curve depends on.

**Falsification condition.** Refuted if κ < 0.7, or if disagreements show a systematic structure (one adoption type consistently misread) rather than adjacent-case noise — either blocks scale-up and forces probe-rule refinement, since an event read with error comparable to the effect floor would make the survival curves measure the probe.

**Hypothesis (plain language).** The mechanical probe reads "is the agent steered by the poison?" the way a careful human would, reliably enough to trust the curves built on it.

**Metrics.** Cohen's κ against human raters; confusion-structure (adjacent vs. systematic).

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, a natural extension is multi-agent contagion — how a laundered claim in one agent's shared memory re-seeds others, and whether a transmission/reproduction number governs it — explicitly out of scope here because it changes the unit of analysis from a single claim's trajectory in one store to a population process across stores, and would need its own identifiability design rather than an extension of the single-subject survival estimand above; Byzantine-tolerant collaborative-memory defenses (Lee et al., 2026; Wang et al., 2026b) are the natural treatment set for that follow-up.

### Threats to Validity

**Construct validity.** The persistence estimand is only as sound as its event definition and its probe. The central construct choice — neutralization as durable loss of *behavioral adoption*, with literal detectability tracked separately — is what keeps laundering from being scored as repair; the mechanical acceptance probe that reads it is validated against ≥2 human raters at Cohen's κ ≥ 0.7 with an adjacent-only confusion structure (RQ7), and a threshold miss blocks scale-up rather than being absorbed into noisier curves. A distinct construct threat is that behavioral adoption is probed on a fixed task family per attack, so a claim that steers behavior only in rare, unprobed contexts could read as neutralized while merely dormant; this bounds the claim to the probed behavioral surface and motivates adaptive probe design as future work.

**Internal validity.** The causal reading of the policy contrast rests on two controls. Identical claims and benign traffic are replayed across policy levels, so composition is held fixed; but because aggressive summarization compresses the stream and thereby reduces exposure to corrective evidence, the matched-salience benign tracer (RQ3) is the load-bearing placebo — a non-null tracer hazard ratio invalidates the causal claim regardless of the poison result, the tracer's null must itself be demonstrated by equivalence test at a pre-registered margin with a tracer arm sized like the poison arm (a merely underpowered tracer is a failed control, not a passed one), and this is checked before RQ2 is interpreted. Attack instantiation and benign-stream content are frozen and hashed before evaluation, so no threshold or policy choice can be tuned on the outcome.

**External validity.** The study is scoped to sandboxable, single-store agent memory with published attacks and defenses across the tested policy levels, attack families, and backbones (pilot: 1 backbone × 1 attack family; scale-up: ≥3 × ≥3); it does not cover multi-agent shared-memory contagion, non-sandboxable live deployments, or attack families outside the published treatment set, and findings are not asserted beyond the tested grid without further runs.

**Conclusion validity.** A single poisoned claim's trajectory cannot separate a policy-driven persistence change from ordinary probe noise, so every rate claim is licensed only through the censoring-aware estimator and the grouped-time hazard model over many independently injected claims, with a pre-registered power target (n = 60 claims/cell sized for a half-life CI half-width < 0.15·*T* under ~50% censoring) and a pre-committed enlargement rule (to 150/cell) rather than a null claim for underpowered cells. Half-life is uninterpretable if content-correction and structural eviction are pooled, so the competing-risks decomposition (RQ5) separates them, and the per-cell classification is certified only when it is split-half stable (RQ6), never from a single sample.

## Related Work

The single closest prior work is the memory-poisoning persistence benchmark of Chen et al. (2026), with the mechanistic persistence evaluation of Leong (2026a) second; it is worth stating the delta plainly before surveying the wider landscape. Chen et al. already measure whether poisoning survives a repair step, and Leong already shows that a poisoned claim's literal presence and its behavioral effect come apart — so this paper concedes both the persistence question and the literal-vs-behavioral distinction as prior art. What neither does, and what this paper is built to do, is measure persistence as a *continuous, censoring-aware hazard over the behavioral-adoption event* with the *memory-management policy as a manipulated treatment*; Chen et al.'s fixed Write–Execute–Forget checkpoint is exactly the single-observation-time special case of that estimand (evaluate the survival function at one time and threshold it), which is why the reviewer question "isn't this just the benchmark with more timepoints?" is answered by subsumption rather than avoided — the extra timepoints change the estimand from a probability into a rate that a policy can move.

**Attacks on agent memory.** The attack surface itself was established by the memory- and knowledge-base-poisoning line: AgentPoison optimizes triggered poison records against retrieval-backed agent memory (Chen et al., 2024), and query-only memory injection shows poison can be planted through nothing but ordinary interaction (Dong et al., 2025). These attacks define the threat model whose *aftermath* this paper measures — our treatments are drawn from their published successors — and neither reports how long its poison persists under ongoing memory management, only whether it lands and fires. The persistence question is sharpened by misattribution: poisoned-memory failures are routinely misread as model failure (Ahad et al., 2026), so a store that is never suspected is never manually repaired, which makes persistence under *default* management policies — exactly this paper's estimand — the operative security regime rather than an edge case.

**Persistence and mechanism of memory poisoning.** Benchmarks establish that agent memory poisoning survives repair at high rates (Chen et al., 2026), and mechanistic evaluations show injection and execution dissociate across many defenses and models (Leong, 2026a). Both make persistence and the literal-vs-behavioral gap visible, but as checkpoint probabilities over short horizons with the memory policy fixed inside the benchmark — neither reports a neutralization rate or turns the policy into a variable. The laundering mechanism these rely on is itself demonstrated as an existence result: adversarial content can survive summarization in a form a content detector no longer flags while still shaping behavior (Wang et al., 2026), shown on a single pathway rather than as a rate that scales with management aggressiveness — the very scaling this paper measures.

**Defenses for agent memory.** Proactive frameworks guard the memory itself (Wei et al., 2025), lineage-guided enforcement constrains what may be written and propagated (Ouyang and Hou, 2026), and trajectory-signature detectors flag poisoning from behavioral traces (Leong, 2026b). Each is designed to reduce poisoning, and each enters this study as a fixed *treatment* on the grid rather than as a system evaluated on its own leaderboard; crucially, a detector's visibility is exactly what laundering evades, which is why detection here doubles as the literal-presence covariate rather than the neutralization event. None of these defenses is evaluated as a continuous persistence-rate modifier under varying memory policies, which is the axis this paper adds.

**Memory management and benign forgetting.** A separate line studies how *benign* memory decays: benchmarks of long-term retention and forgetting for personalized agents (Uddin et al., 2026), architectural studies showing that where the memory control plane sits shapes what is forgotten across many configurations (Yang, 2026), and operating-system-style and reflection-based memory managers that summarize and consolidate for utility (Packer et al., 2023; Park et al., 2023). These characterize benign forgetting and supply the policy axis and the benign streams this study manipulates, but none measures *adversarial*-content persistence, and none asks whether a policy tuned for benign utility inverts on adversarial content — the question this paper's policy-as-treatment design is built to answer.

**Survival analysis and competing risks.** The estimand borrows standard, decades-validated statistical machinery — the Kaplan–Meier survival estimator (Kaplan and Meier, 1958), Cox proportional-hazards regression for covariate effects on the hazard (Cox, 1972), and cause-specific hazards for competing risks — applied here not as a novel statistical contribution but as the instrument that turns intermittent adoption probes into a policy-attributable, cause-resolved persistence rate. The contribution is the estimand's construction for this problem (behavioral event, interval-censored probes, laundering cell, policy treatment), not the survival mathematics, which is used off the shelf.

## Conclusion

This work reframes a security assumption — that utility-improving memory management also washes adversarial content out of a long-lived agent's memory — as an empirical question with a precise identifiability structure, rather than trusting the checkpoint benchmark whose binary cannot even state a rate. The central methodological wager is that poison persistence is only decision-relevant once it is measured as a *behavioral-adoption* hazard over interaction time, with the memory policy as a manipulated treatment and content-correction separated from structural eviction — because the alternative, a fixed-checkpoint binary keyed on literal presence, scores a laundered claim as repaired at the moment it is most dangerous. Whichever way the central test resolves, the finding is actionable: if aggressive management lengthens half-life, then the memory-management step operators lean on as free hygiene is a persistence amplifier that demands a continuously-running companion defense, and the benchmark checkpoint labeled "repair" is mislabeled; if half-life is invariant to policy, that null is itself the license the field currently lacks to treat washout as real, made credible by the pre-registered power behind it. Two limitations bound the claim from the outset and are next steps rather than afterthoughts: behavioral adoption is read on a fixed probe surface per attack, so a claim that steers behavior only in rare, unprobed contexts could read as neutralized while dormant, pointing toward adaptive probing; and the estimand is single-store, leaving multi-agent shared-memory contagion — where a laundered claim re-seeds other agents — as a distinct population-level problem needing its own identifiability design.

## References

> Every entry below is a real, verified work (arXiv IDs resolved via the arXiv API; classical statistics references are standard published works). `discussion/refs.bib` is the machine-readable source; the `.tex` build wires `\citep`/`\citet` keys to it. This list is the Markdown-readable mirror.

- Chen, Z., Xiang, Z., Xiao, C., Song, D., Li, B. AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases. arXiv:2407.12784, 2024.
- Dong, S., Xu, S., He, P., Li, Y., Tang, J., Liu, T., Liu, H., Xiang, Z. Memory Injection Attacks on LLM Agents via Query-Only Interaction. arXiv:2503.03704, 2025.
- Ahad, T., Hossain, I., Alam, M. J., Puppala, S., Alam, S. B., Talukder, S. The Misattribution Gap: When Memory Poisoning Looks Like Model Failure in Agentic AI Systems. arXiv:2605.22842, 2026.
- Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., Gonzalez, J. E. MemGPT: Towards LLMs as Operating Systems. arXiv:2310.08560, 2023.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., Bernstein, M. S. Generative Agents: Interactive Simulacra of Human Behavior. arXiv:2304.03442, 2023.
- Chen, X., Xie, X., Fu, W., Zhou, J., Yu, S., Xuan, Q. MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair. arXiv:2607.27080, 2026.
- Leong, J. W. Injection-Execution Dissociation: A Mechanistic Evaluation of Persistent Memory Attacks and Defenses in Stateful LLM Agents. arXiv:2605.08442, 2026a.
- Wang, Y., Goyal, A., Chen, Y., Sundaram, H. State Contamination in Memory-Augmented LLM Agents. arXiv:2605.16746, 2026.
- Wei, Q., Yang, T., Wang, Y., Li, X., Li, L., Yin, Z., Zhan, Y., Holz, T., Lin, Z., Wang, X. A-MemGuard: A Proactive Defense Framework for LLM-Based Agent Memory. arXiv:2510.02373, 2025.
- Ouyang, C., Hou, R. MemLineage: Lineage-Guided Enforcement for LLM Agent Memory. arXiv:2605.14421, 2026.
- Leong, J. W. Forensic Trajectory Signatures for Agent Memory Poisoning Detection. arXiv:2606.30566, 2026b.
- Devarangadi Sunil, B., Sinha, I., Maheshwari, P., Todmal, S., Mallik, S., Mishra, S. Memory Poisoning Attack and Defense on Memory Based LLM-Agents. arXiv:2601.05504, 2026.
- Uddin, M. N., Shubham, K., Blanco, E., Baral, C., Wang, G. From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents. arXiv:2604.20006, 2026.
- Yang, D. Control-Plane Placement Shapes Forgetting: An Architectural Study of Agent Memory Across Thirteen System Configurations. arXiv:2606.15903, 2026.
- Lee, H., Yun, V.-D., Panagou, D., Karimireddy, S. P. Robust Multi-Agent LLMs under Byzantine Faults. arXiv:2605.09076, 2026.
- Wang, Z., He, D., Zhang, Z., Liu, Y., Liu, J., Zeng, Z., Qin, Z., Li, Z., Li, X., Yao, H., An, J., Liu, Y., Li, Y., Sun, Q., Liu, X., Zhu, L. Combating Knowledge Corruption in Agent Systems: A Byzantine-Tolerant Secure Collaborative RAG Framework. arXiv:2608.04366, 2026b.
- Kaplan, E. L., Meier, P. Nonparametric Estimation from Incomplete Observations. Journal of the American Statistical Association, 53(282):457–481, 1958.
- Cox, D. R. Regression Models and Life-Tables. Journal of the Royal Statistical Society, Series B, 34(2):187–220, 1972.

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → method → experiments → related work with no forward references to undefined terms; the behavioral-event distinction is introduced in the Introduction and Problem Definition before any estimator uses it.
- **Terminology discipline** — "behavioral adoption," "laundering cell," "poison half-life," "content-neutralization vs. structural eviction," "policy aggressiveness" each defined at first use and used consistently; no internal stage IDs (`sp_*`, `m_*`, `rq_*`) in prose — checked against `discussion_trace.md`.
- **Notation with worked example** — the formal setup defines (*M_t*, *P*, *pᵢ*, *a*, *ℓ*, τ, *S*, *h*, *t*₁/₂) and the Methodology/Experiments reuse it consistently; no separate numeric worked example is included because no numbers exist yet (would require fabricating results).
- **RQ framing matches outcomes** — all 7 RQs are graded/quantitative (hazard ratios, CI widths, cell frequencies, κ, agreement rates), each answered in its own subsection with an explicit falsifiable expected outcome and a Falsification condition, not a binary yes/no.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]`; only explicit `[placeholder — fill in after experiments are run]` markers in Results.
- **Artifact plan** — the sandbox harness (policy grid, probe scheduler, survival/competing-risks estimators) and the validated acceptance-probe suite are the natural release artifacts; not yet built, so not claimed as available.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. All results are explicit placeholders; all numbers are pre-registered design targets with rationale. Natural next steps: run the pilot from the standalone experiment protocol and splice real numbers into the Result slots, or `research-paper-writing` for prose polish once a target venue (USENIX Security / CCS measurement track, or an ICLR safety track) is chosen.
