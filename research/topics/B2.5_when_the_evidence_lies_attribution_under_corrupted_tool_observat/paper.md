# When the Evidence Lies: Attribution under Corrupted Tool Observations — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1–C4, M1–M6, CO1–CO4, RQ1, RQ_INF_1, RQ_INF_2, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** In failure attribution, every check the pipeline can run certifies the *form* of a tool observation, but the diagnosis consumes its *content* as an unquestioned premise — so a schema-valid lie is not merely undetected, it is actively re-used as evidence against the plan and execution layers that consumed it.

This is an invariant of the evidence channel (digest C1 form-invisibility + C2 evidential circularity), not a bridge between two literatures: the same trace serves as both crime scene and witness, and validity checking guards only the witness's grammar.

**判据 (deletion test).** Delete the domain nouns — *tool observation, attribution pipeline, plan/execution layers, schema*:

> "Every check certifies the form of an input, but the diagnosis consumes its content as a premise — so a valid lie is re-used as evidence against whoever consumed it."

Without the domain nouns the sentence loses its truth conditions: (a) "valid" has no referent — schema-validity is a property of typed tool returns specifically, and it is exactly the property that makes the corruption invisible to parse/exception/monitor signals (C1); (b) "whoever consumed it" cannot predict a *direction* — the directional prediction (blame flows to the plan layer, RQ_INF_1) exists only because plan critique sits immediately downstream of reading the observation in the plan/tool/execution ontology. The stripped sentence is an empty truism about garbage-in; the full sentence is a falsifiable claim about where the garbage lands. Not a bridge — PASS.

## Step 2 — Archetype

**Primary: empirical (measurement study)**, per digest N12: the paper measures how *existing* attribution methods behave under a controlled fault mode; no new attribution method is proposed. **Secondary: dataset/instrumentation** (CO1, the replay-verified corruption suite) — instrumentation for the measurement, not the headline.

Downstream consequences:
- **(a) Abstract contribution slot:** a quantified bias — the Δ-trust gap and its direction — plus mechanism evidence (trust-license probe), NOT a system or a SOTA number.
- **(b) Intro logic:** "here is a structural blind spot and an instrument that makes it measurable for the first time" (what becomes possible: auditing the auditors), not "we beat method X".
- **(c) Evidence standard for results:** treatment-vs-matched-control contrasts with pre-registered tests, per-cell breakdowns (M5 grid), and an intervention that discriminates between rival mechanisms (C2 trust vs C3 capability). A large misattribution rate alone is insufficient; the *gap against overt-error controls* is the unit of evidence.

## Step 3 — Taste self-audit

- **Bridge check:** FAIL in naive form ("attribution literature and robustness literature were never crossed" — digest Claim 1 flirts with this). **Fix (idea skeleton, not wording):** the gap statement is demoted to related-work positioning; the *opportunity* is re-anchored on the Step-0 asymmetry — validity checks certify form while diagnosis consumes content. The corrected framing stands even if someone had already "crossed the literatures": the claim is about a structural property of trace-reading diagnosis, testable by intervention (M6 trust probe), not about unoccupied territory.
- **Synthesis check:** PASS. The method is not gluing existing parts: M1+M2 construct a ground truth that does not exist in nature (counterfactual-replay-verified tool-layer root causes), and M6's paired controls isolate a cause. Existing methods appear only as *objects of measurement*, run unmodified and blinded.
- **Verb audit:** load-bearing verbs are *inject, verify (by replay), isolate, measure, intervene*. No integrate/unify/leverage/combine in any claim. PASS.
- **Abstract-opening rule:** abstract v0 (below) opens with the mechanism/asymmetry; the "X is increasingly used… however… we introduce" template is not used. PASS.

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The Δ-trust gap — the difference in misattribution rate between
schema-valid-semantically-corrupted and overt tool-caused failures, per attribution method — over
the population of verified, replay-decisive tool-caused failures drawn from single-agent
(AgentDojo), long-horizon (GAIA), and logged multi-agent (Who&When) trajectories (population
subject to the pre-committed framework-narrowing rule in Step 9's gate G6); the decision it
feeds is whether an attribution pipeline's plan/tool/execution verdict can be trusted to route
real corrective effort (planner retraining vs. tool patching vs. no action) when the trace's own
evidence may be silently wrong, and, if not, whether the failure is a removable trust assumption
(H3) or a deeper counterfactual-reasoning ceiling.

**Notation.** A trajectory τ = (q, (a₁,o₁),…,(a_T,o_T)) with task q, actions a_t, tool observations o_t, and a programmatic checker V(τ) ∈ {0,1}. A corruption operator μ ∈ 𝕄 (M1's five families) maps o_t ↦ o′_t. replay(τ, t, o) re-executes τ from step t with observation o substituted, at temperature 0 / fixed seed. An attribution method A maps τ ↦ (ℓ̂, t̂), ℓ̂ ∈ {plan, tool, execution}, via a pre-registered per-method mapping rubric R_A (M3).

Every load-bearing adjective/verb from the digest Claims, formalized:

| Term (from Claims/RQs) | Formal definition | Measured by |
|---|---|---|
| **schema-valid** (corruption) | S(o′_t)=1 iff (i) o′_t re-validates against the tool's declared JSON schema/return type, (ii) the framework's native parser accepts it without raising, (iii) plausibility screen (below) passes | M1's three automated gates; gate pass/fail logged per candidate |
| **semantically incorrect** | o′_t ≠ o_t on a load-bearing field, where "load-bearing" = the field is referenced by the agent's step t+1..T in the uncorrupted run (string/AST trace match) | M1 instrumentation log |
| **decisive cause** (ground truth = tool layer at step t) | V(τ_corrupted)=0 ∧ V(replay(τ_corrupted, t, o_t))=1 | M2 twin replay; binary, per trajectory |
| **misattribution rate** | m_A(D) = 1 − (1/|D|)·Σ_{τ∈D} 1[ℓ̂_A(τ)=tool], D a set of verified tool-caused failures | M4, on D_sem and D_overt |
| **Δ-trust gap** (headline) | Δ_A = m_A(D_sem) − m_A(D_overt), task- and step-matched sets | M4 + M6(a) |
| **systematic** (RQ1's "systematically misattribute") | Δ_A > 0 at Holm-corrected p < .05 for a strict majority of tested methods | H1 verification procedure |
| **direction** / **skew toward plan** | π_plan(A) = |{τ: ℓ̂_A(τ)=plan}| / |{τ: ℓ̂_A(τ)≠tool}| among misattributed cases; skew iff π_plan > 0.5 (binomial) | M4; H2 |
| **subtle** (plausible corruption) | screen model (≠ any judge model, per A7) answers "not self-evidently wrong in context" with confidence ≥ 0.8; "borderline" = [0.5, 0.8) | M1 gate (iii), stratifier for M5 |
| **overt** (tool error) | observation replaced by exception/timeout/empty return that the framework surfaces as an error object (ResiliBench-style) | M6(a) construction |
| **trust-license reduces bias** | δ_A = m_A^{licensed}(D_sem) − m_A^{base}(D_sem) < 0, paired per trajectory; **without harming** = FPR increase on plan-failure controls ≤ non-inferiority margin (H3) | M6(c) paired runs |
| **control false-positive rate** | FPR_A = fraction of verified genuine-plan-failure controls with ℓ̂_A = tool | M4 on M6(b) |
| **mapping validity** | Cohen's κ between two annotators applying R_A to raw method outputs | M3 dual-annotation subsample |

Deleted adjectives: "trustworthy", "blind", "structural" appear only in motivation prose, never in a claim — each claim below traces to a quantity in this table.

## Assumptions (A1..A7)

Each row fills guidance.md §3.2's five slots: assumption, failure_mode ("How it could fail"),
detection, gate, and **consequence** (what happens to which H\* if it fails — degrade, restrict
scope, or block; added per goal.md §3 item 5 / guidance.md §3.2, which this table previously
omitted).

| Id | Assumption | How it could fail | Detection / gate | Consequence if it fails |
|---|---|---|---|---|
| A1 | **Injection yield:** ≥20% of schema-valid corruptions of load-bearing fields are decisive (M2 twin flips) | Agents recover, checkers insensitive, fields not load-bearing | Walking-skeleton gate G1: yield ≥20% on 100 candidates; digest N6 go/no-go | **Block.** G1 is a pre-scale go/no-go: below 20% yield, scale-up does not proceed at all (no H1/H2/H3 can be tested) until load-bearing-field targeting is revised and the pilot re-run. |
| A2 | **Replay determinism:** the uncorrupted twin reproducibly succeeds at temp 0/fixed seed | Framework nondeterminism (tool state, timestamps, sampling) | Skeleton gate G2: twin-replay agreement ≥90% on 20 uncorrupted re-runs; else pin/mock tool state | **Block.** Below 90% agreement, M2's ground-truth label (decisive cause = tool) is not trustworthy, so no corrupted trajectory can be certified — blocks H1/H2/H3 until tool state is pinned/mocked and G2 re-cleared. |
| A3 | **Layer-mapping validity:** every baseline's native output maps onto {plan, tool, execution} with κ ≥ 0.7 (C4, t1) | Method outputs agent names/steps that straddle layers | Pilot dual-annotation of 50 outputs per method before unblinding; disputed trajectories excluded in sensitivity analysis | **Degrade (per-method scope restriction).** A method whose mapping κ < 0.7 is not dropped outright but is reported with disputed trajectories excluded from its H1/H2/H3 numbers and flagged as mapping-noise-limited, per t1's mitigation — it does not block the other methods' tests. |
| A4 | **Control matchability:** overt-error and plan-failure controls constructible on the same tasks at matched step loci | Some tasks cannot produce overt errors at matched steps | Skeleton constructs both controls for every task family; unmatched tasks dropped symmetrically | **Restrict scope.** Task families that cannot produce matched controls are dropped from B0/B-alt entirely (symmetrically, so D_sem/D_overt/D_agent-side stay task-matched) — narrows the claim's task coverage but does not block H1/H2/H3 on the remaining matched families. |
| A5 | **Baselines runnable unmodified:** Who&When judge protocols reproducible; AgenTracer checkpoint (or faithful re-train) available; SupervisorAgent trigger logic re-implementable post-hoc | Missing artifacts, license issues | Skeleton runs each baseline end-to-end on 5 trajectories; failure ⇒ pre-registered substitution (drop baseline, note in scope, never swap silently) | **Degrade (per-baseline).** A baseline that fails the 5-trajectory smoke test is dropped from H1's method count (denominator shrinks from 5, never silently substituted) and the drop is stated in scope — does not block H1 for the remaining baselines, but weakens the "≥3 of 5" aggregation's evidential weight if more than one drops. |
| A6 | **Clean plan-failure controls:** M6(b) trajectories have verifiably uncorrupted observations | Natural logs contain silent tool faults (the very phenomenon!) | Observation audit: re-execute the control tasks' tool calls against ground-truth state; discard non-verifiable logs | **Restrict scope.** Non-verifiable logs are discarded from the false-positive control set (M6(b)); if too few verifiable plan-failure trajectories remain, H3's false-positive-rate check (FPR ≤ 3pp non-inferiority) is pre-declared INCONCLUSIVE rather than scored on a contaminated or underpowered control set — does not block H1/H2. |
| A7 | **No screen leakage:** the plausibility-screen model is disjoint from every judge/agent backbone family | Shared blind spots make "subtle" circularly defined (t3) | Config check in harness; plus t3's same-family vs cross-family breakdown at scale-up | **Degrade (interpretive, not blocking).** If leakage is detected, the "subtle" stratifier in the M5 grid is not dropped but its results are reported separately for same-family vs. cross-family judge/backbone pairs (t3's mitigation), and the type-dependence sub-claim (H2b) is qualified rather than retracted. |

## Instrument validation: the plausibility screen (guidance.md R2, 5 steps)

The screen is a load-bearing LLM-judge instrument (it gates M1 admission via gate (iii), defines
the construct "subtle," and stratifies the M5 grid) and therefore gets the full R2 sequence —
promoted here from the earlier draft's screen-validation RQ, which had never entered this binding
spec (goal.md §8: no instrument runs at scale without passing R2). Acceptance thresholds below are
pre-registered targets, not observed numbers.

1. **Ground.** The category boundary (plausible / borderline / self-evidently-wrong, cutpoints
   0.8 and 0.5 per the Step 5 "subtle" row) is grounded in M1's operator-family definitions and
   in the plausible-in-context standard of the cache's corruption literature (ChatInject's
   well-formed malicious tool returns; DECEPTICON's normal-looking-but-misleading content).
2. **Draft & refine.** The screen prompt is drafted wide, then refined on a held-out calibration
   set built by the walking skeleton: 50 gate-passing + 50 gate-rejected injection candidates,
   with named merge/split operations on the category boundary recorded per revision.
3. **Validate.** Two independent human raters judge the same held-out set ("is this value
   self-evidently wrong in context?", blinded to the screen's verdict). Acceptance (all three):
   rater–rater κ ≥ 0.7; ≥90% of gate-passing corruptions rated plausible-in-context; the
   gate-rejected calibration set rated plausible at a substantially lower rate (< 60%).
4. **Inspect confusion structure.** Screen–rater disagreements must concentrate in the borderline
   band [0.5, 0.8); a systematic collapse of plausible ↔ self-evidently-wrong fails validation
   even if the aggregate thresholds pass.
5. **Freeze.** Screen prompt, model id, and both cutpoints are hashed into `B_pilot/` before any
   scale-up (gate G5, Step 9); at scale, a sensitivity analysis re-stratifies the M5 grid at
   cutpoints 0.7 and 0.9 to show the "subtle" construct is not an artifact of the 0.8 constant.

Failure at step 3 or 4 follows guidance.md situation 7: refine categories on the held-out set and
re-validate, or coarsen to a binary plausible/implausible screen; the screen never scales
unvalidated, and H2b's subtlety factor is pre-declared INCONCLUSIVE if validation cannot be passed.

## Step 6 — Pre-Registered Experiments

### E1 (RQ1): Does schema-valid corruption cause systematic misattribution?

- **Assumption:** A1, A2, A3, A4, A5.
- **Hypothesis H1 (binary):** For ≥3 of the 5 non-human baselines (Who&When all-at-once / step-by-step / binary-search judges, trained tracer, runtime monitor), Δ_A ≥ +10 percentage points AND the paired test rejects at Holm-corrected p < .05. Additionally m_A(D_overt) ≤ 40% for those methods (they must be competent on overt errors, else the gap is uninterpretable).
- **Metric:** Δ_A = m_A(D_sem) − m_A(D_overt) (Step 5 table); secondary: step-localization accuracy (exact, ±1).
- **Verification:** n ≥ 300 verified corrupted trajectories per framework per arm (digest N8: ~80% power for a 10 pp gap at α=.05 given ~30% baseline); McNemar on task-matched treatment/control pairs, two-proportion z otherwise; Holm–Bonferroni across the 5-method family; cluster-robust errors by task template (t5).
- **Fallback F1 (pre-committed wording):** "Contrary to the structural-blind-spot hypothesis, {k} of 5 attribution methods localize schema-valid semantic corruptions to the tool layer as reliably as overt errors (Δ within ±10 pp, n.s.); the attribution layer is empirically robust to lying evidence, and we release the verified corruption suite as the stress test that certifies this robustness." (Feeds F-G1. Applies only if the F0 condition below did NOT fire — F1 asserts competence-relative robustness and is unusable when methods flunk overt errors.)
- **Fallback F0 (pre-committed wording, premise-collapse branch):** Fires if m_A(D_overt) > 40% for ≥3 of the 5 methods — methods cannot reliably localize even overt, signal-emitting tool faults. In this cell H1 is unscoreable and **F1 and F-G1 are both explicitly unusable** (each asserts "as well as overt errors," which is vacuous here); the overt-error failure rate itself becomes the headline: "Current attribution methods misattribute even overt, signal-emitting tool faults ({m}% mean misattribution on exceptions/timeouts, against a {c}% always-predict-plan floor); the attribution layer is not yet reliable enough for the schema-validity distinction to be measurable — before asking whether attribution is *biased* by lying evidence, the field must first clear the competence bar this suite's overt arm sets, which we release as that entry test." Combination rule: F0 pre-empts F1/F-G1 wholesale; E2/E3 are then reported descriptively only (their verdicts pre-declared INCONCLUSIVE, since both condition on an interpretable Δ).

### E2 (RQ_INF_1): Is the misattribution directional, and type-dependent?

- **Assumption:** A1–A3; conditional on E1 producing ≥120 misattributed cases per method. **Honest power statement:** the previously drafted ≥50-case minimum gives only ~0.51 power for the pre-registered criterion (exact binomial, two-sided α=.05, true π_plan=0.65) — a coin flip against a real skew, which would have let F2 fire as a false finding; at n=120 the same test has ~0.89 power (critical count 72/120). Pre-declared bands: ≥120 cases → H2 scored; 50–119 → INCONCLUSIVE (π_plan reported with CI, no PASS/FAIL verdict, F2 does not fire); <50 → descriptive only, no test.
- **Hypothesis H2 (binary):** Pooled per method, π_plan ≥ 0.65 with exact binomial p < .05 against 0.5, for every method that showed a significant Δ in E1. Type-dependence sub-hypothesis H2b: ≥1 of the three M5 factors (operator family, locus tercile, subtlety) is a significant predictor (likelihood-ratio test, p < .05) in the mixed-effects logistic model.
- **Metric:** π_plan (Step 5); cross-tabulation over the M5 grid (each cell pre-filled to ≥15 verified trajectories).
- **Verification:** Exact binomial per method (Holm-corrected across methods); mixed-effects logistic regression, fixed effects = M5 factors, random intercepts = task and framework (digest N8 analysis plan, hardened with the cell-minimum).
- **Fallback F2 (pre-committed wording):** "Misattribution under corrupted observations is real but directionally diffuse: blame scatters across plan and execution (π_plan = {x}, n.s. vs 0.5), indicating the blind spot corrupts localization noise-wise rather than channeling it to one layer — a distinct and reportable failure geometry."
- **Fallback F2b (pre-committed wording, H2b):** "Misattribution direction shows no detectable dependence on corruption type, locus, or subtlety (no M5 factor significant at p < .05 in the mixed model): within the measured grid the blind spot is indiscriminate across corruption families — no operator, position, or subtlety level is 'safer' than another, which simplifies the practical guidance but removes the type-targeting half of Claim 4; the direction claim (H2) stands or falls on its own verdict." (F2 and F2b are independent: any of the four H2×H2b outcome cells maps to main/F2 wording for direction crossed with main/F2b wording for type-dependence.)

### E3 (RQ_INF_2): Is the mechanism the trust assumption (C2) or a capability ceiling (C3)?

- **Assumption:** A1–A4, A6; applies to the 3 LLM-judge baselines only (the tracer/monitor cannot take a prompt intervention — pre-declared scope).
- **Hypothesis H3 (binary):** For ≥2 of 3 judge variants, the one-sentence trust license reduces m_A(D_sem) by ≥5 percentage points absolute (paired McNemar p < .05) AND the FPR increase on genuine-plan-failure controls is ≤3 percentage points (non-inferiority margin, one-sided 95% CI upper bound ≤ 3 pp).
- **Metric:** δ_A (Step 5) on D_sem; FPR_A on M6(b) controls.
- **Verification:** Within-method paired design, same trajectories with/without the license sentence; McNemar for the reduction, Farrington–Manning non-inferiority test for FPR; Holm across the 3 judges.
- **Fallback F3 (pre-committed wording):** "A minimal license to distrust observations does not repair attribution ({δ} pp, n.s.) — the blind spot is not a removable prompt-level trust assumption but a counterfactual-reasoning deficit (C3): knowing evidence *may* lie does not reveal *which* observation lies. Cheap prompt fixes are ruled out; observation-side verification machinery is required." (If instead reduction succeeds but FPR inflates >3 pp: "the license trades misattribution for indiscriminate tool-blaming — trust is a dial, not a switch.")

### Mandatory baselines

- **B0 — "why do this at all" control: the overt-error arm + a constant-guess attributor.** M6(a) overt errors establish that methods *can* localize tool faults when the fault emits a signal (if m_A(D_overt) were already ≥ m_A(D_sem), there is no specific form-invisibility problem — just bad attribution, and the paper's premise dies honestly — routed to F0, not improvised). The constant attributor (always-predict-plan, the corpus majority class) floors the comparison: any judge whose accuracy on D_sem does not beat always-plan is not performing attribution on corrupted evidence at all. Both are required in every results table. Neither component carries a null prediction, so neither can serve goal.md §5's placebo-first check — that job belongs to B0-placebo below.
- **B0-placebo — null-by-construction validity gate (operationalizes goal.md §5 step 1).** Two components, both with pre-committed null criteria, evaluated before any H\* is scored; either being non-null means the pipeline measures an artifact and the run is invalid (no hypothesis may be scored "to see"):
  - **(i) Sham-injection arm:** verified genuine-plan-failure trajectories (M6(b)) are passed through the *identical* injection→replay→serialization machinery with the identity mutation (o′_t = o_t), paired against their untouched twins. Null criterion: per method, the attribution-label distribution on sham-processed vs. untouched twins is equivalent (paired two-one-sided-tests, equivalence margin ±3 pp per layer share). A shift means the harness itself (serialization format, replay side-effects, injection bookkeeping leaking into the trace) alters attribution — an artifact that would contaminate Δ_A.
  - **(ii) Label-shuffle analysis placebo:** recompute Δ_A after permuting the D_sem/D_overt arm labels within task- and step-matched pairs (1,000 permutations). Null criterion: the permuted-label Δ distribution is centered on zero (and the observed Δ_A's permutation p is reported alongside the parametric test). A permuted null not centered on zero flags an analysis-code artifact (asymmetric matching, dropped-row asymmetry).
  Both null criteria are frozen (hashed) with the skeleton's thresholds; Phase D step 1 checks B0-placebo (i)+(ii) first, before B0's competence readings and before any H1/H2/H3 verdict.
- **B-alt — strongest-alternative-explanation control: the matched agent-side-fault arm.** Rival explanation: *"subtly wrong values are just intrinsically hard to spot, regardless of which layer produced them — the result is a capability artifact of the injector's difficulty, not an evidence-channel trust asymmetry."* Control: take the same mutation operators and inject the identical wrong value into the **agent's action** (AgenTracer-style action perturbation — e.g., the agent itself writes the wrong number into its next call) on matched tasks, replay-verified the same way. Same semantic delta, same subtlety screen, same budget; only the causal locus differs. If methods correctly blame the agent-side wrong value but exonerate the tool-side one, the cause is the trust asymmetry over the observation channel — the rival is eliminated. Pre-registered criterion: m_A(agent-side) < m_A(D_sem) − 10 pp for the methods passing H1; if instead the two are indistinguishable, F3-style capability wording takes over the mechanism claim.

### Confound-removal ledger (guidance.md R3)

Every control/design constraint above removes a *named* confound; stated explicitly here because
none of Steps 5–6 named one previously (goal.md §3 item 6 / guidance.md Part 6 item 7):

- **Task- and step-locus-matching D_sem against D_overt (M6(a))** removes the *task-difficulty
  confound* — without matching, a raw Δ_A could reflect "overt-error tasks happen to be easier,"
  not a genuine trust asymmetry over the observation channel.
- **Using the identical mutation operators, subtlety screen, and budget for the agent-side-fault
  arm as for D_sem (B-alt)** removes the *injector-difficulty confound* — without this, a positive
  Δ_A could mean "this corruption family is just hard to spot anywhere," not that the tool-observation
  channel specifically is over-trusted.
- **Blinding every attribution method to injection metadata (M3)** removes the *demand-characteristic
  confound* — without blinding, a method could (consciously or not) key on the experiment's own
  injection markers rather than genuinely diagnosing the trajectory.
- **Freezing the per-method mapping rubric R_A before any results are seen (M3, A3)** removes the
  *experimenter-mapping-bias confound* — without pre-registration, a generous or strict mapping
  choice made after seeing results could manufacture or hide the Δ-trust gap.
- **Crossing judge/backbone model family in the scale-up (t3, A7)** removes the *shared-blind-spot
  confound* — without this cross, a same-family judge could "believe" the same corrupted premise
  the agent believed for reasons of model-family bias rather than the evidence-channel trust
  asymmetry this paper targets.
- **The constant always-predict-plan floor (B0)** removes the *trivial-majority-class confound* —
  without it, a method could appear to "detect" the tool layer at a rate no better than always
  guessing the corpus-majority label, which would not constitute attribution at all.

### Global fallback F-G1

If the central hypothesis family (H1) fails outright — methods are robust — the archetype pivots from *empirical bias measurement* to *benchmark/resource with a robustness finding* (digest N12 explicitly licenses this pivot). Pivoted abstract sentence, pre-committed: "We introduce a counterfactual-replay-verified suite of schema-valid semantic corruptions of tool observations and show, contrary to the structural expectation that trace-reading attribution must inherit lying evidence into its premises, that current attribution methods localize such corruptions about as well as overt errors — establishing the corruption suite as a certification instrument and isolating which corruption types still evade which method class."

**Scope of F-G1:** it applies only in the *robust-and-competent* cell — H1 fails with m_A(D_overt) ≤ 40% (methods handle overt errors, and handle semantic corruptions about as well). In the premise-collapse cell (m_A(D_overt) > 40% for ≥3 of 5 methods), F-G1's "about as well as overt errors" is vacuous and unusable; E1's F0 wording takes over the headline wholesale, per its stated combination rule.

## Step 9 — Walking Skeleton

**One binary question:** *Can this pipeline manufacture replay-verified tool-caused failures at usable yield, and does at least one unmodified judge score differently on them than on overt errors?*

- **Arms (2):** (1) semantic corruption (M1, numeric-perturbation operator only) vs (2) overt error (exception substitution) — same tasks, same step loci.
- **Task set:** 10 AgentDojo tasks (2 domains × 5), single-agent ReAct-style framework, one backbone. 100 injection candidates → target ≥20 verified corrupted trajectories (A1 gate) + 20 matched overt controls.
- **Framework reach (all 3 estimand frameworks touched, 1 case each):** in addition to the AgentDojo core, the skeleton runs (a) one full injection→replay cycle end-to-end on 1 GAIA task, and (b) one twin-replay determinism attempt on 1 Who&When-logged trajectory — the known likely breaker, since replaying a *logged* multi-agent run requires reconstructing tool state that may no longer exist. These smoke cases exist to make the config-not-code claim demonstrated rather than asserted.
- **Method under test:** Who&When all-at-once LLM judge only, with its mapping rubric R written before any output is seen.
- **Instrument validation inside the skeleton:** the plausibility screen's R2 steps ②–④ run here (50 gate-passing + 50 gate-rejected candidates, 2 human raters) — gate G5 below; screen prompt + cutpoints frozen (hashed) on pass, per the Instrument-validation section.
- **Deterministic metrics only:** yield (verified/candidates), twin-replay agreement rate, rubric-mappable fraction, screen–rater agreement on the calibration set, and the raw 2×20 layer-accuracy table. No significance tests, no CIs, no grid.
- **Cost:** ~100 agent runs + ~120 replay runs + 40 judge calls, plus ~5 GAIA/Who&When smoke runs and ~200 human rater judgments (2 raters × 100 candidates) ≈ 1–2 days wall-clock, order $50–200 API spend (consistent with digest N6 pilot arithmetic).
- **Pass criterion (all six, binary):** G1 yield ≥ 20%; G2 twin-replay agreement ≥ 90%; G3 rubric maps ≥ 95% of judge outputs without adjudication; G4 both arms produce a complete, non-degenerate accuracy table (neither 0% nor 100% in both arms); G5 plausibility screen passes R2 step ③ (rater κ ≥ 0.7, ≥90% gate-passing plausible, gate-rejected < 60%) with step-④ confusion structure clean; G6 the GAIA cycle completes end-to-end AND the Who&When replay attempt is adjudicated. **G6's Who&When half narrows rather than blocks (pre-committed):** if the logged-trajectory replay cannot meet the G2 determinism bar, scale-up proceeds with the estimand's population narrowed to AgentDojo + GAIA; Who&When demotes to a stated stretch arm (and remains the source of M6(b) plan-failure controls only, which need per-tool-call audit, not full-run replay), recorded in `pipeline.md` before any scaling. **Skeleton passed ⇒ scale-up (the G6-surviving frameworks, 5 operators, 5 methods, n≥300/arm, M5 grid, trust probe) is a config change — more tasks, more operators, more methods in the same harness — not a code change.** Any other gate failure triggers the linked assumption's mitigation (A1: load-bearing-field targeting; A2: tool-state pinning; A3: rubric revision *before* unblinding; G5: situation-7 screen refinement) before any scaling.

## Claim–Evidence Map

| # | Abstract-bound claim | Traces to | Status |
|---|---|---|---|
| 1 | The condition "semantically wrong, schema-valid observation scored against attribution ground truth" is unmeasured in prior work (digest Claim 1) | N3/N4 corpus audit; positioning only, not a contribution slot (Step 3 fix) | supported-by-design (corpus-grounded) |
| 2 | A replay-verified corruption suite with matched controls exists and is releasable (CO1) | M1+M2 definitions (Step 5: schema-valid, decisive); skeleton G1–G2 | needs-experiment (construction gated by skeleton) |
| 3 | Attribution methods misattribute schema-valid tool corruptions systematically more than overt ones (CO2, digest Claim 2) | H1 (Δ_A ≥ 10 pp, majority of methods); validity gated by B0-placebo (i)+(ii) null | needs-experiment; fallback-covered (F1 / F-G1; premise-collapse branch: F0) |
| 4 | The misattribution skews toward the plan layer and depends on corruption type (CO3, digest Claim 3) | H2 (π_plan ≥ 0.65), H2b (M5 factor LRT) | needs-experiment; fallback-covered (F2 for direction; F2b for type-dependence) |
| 5 | The bias is a trust-assumption effect, not (only) a capability ceiling (CO4, digest Claim 4) | H3 (δ ≥ 5 pp, FPR ≤ 3 pp) + B-alt agent-side-fault contrast | needs-experiment; fallback-covered (F3; B-alt criterion) |
| 6 | Methods are competent on overt tool errors (premise legitimacy) | H1's m_A(D_overt) ≤ 40% clause + B0 | needs-experiment (B0 arm); failure branch fallback-covered (F0) |

Every claim resolves to an H-id or a Step-5 definition; no claim depends on unformalized adjectives.

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — WRITTEN BEFORE ANY RESULTS; ALL BRACKETED QUANTITIES PENDING]**
>
> Every check a failure-attribution pipeline can run certifies the form of a tool observation; the diagnosis then consumes its content as an unquestioned premise. A schema-valid lie in an agent trajectory is therefore not merely invisible — it is re-used as evidence against the plan and execution layers that consumed it. We isolate this asymmetry with a fault-injection testbed that corrupts one tool observation per trajectory under schema-preserving mutations, verifies each corruption's decisiveness by counterfactual replay, and measures unmodified attribution methods — LLM judges, a trained tracer, a runtime monitor — against matched overt-error and genuine-plan-failure controls. We quantify the Δ-trust gap [pending], the directional skew of blame toward the plan layer [pending], and, via a paired trust-license intervention and a matched agent-side-fault control, whether the bias is a removable trust assumption or a counterfactual-reasoning deficit [pending].

(148 words; opens on the asymmetry; verbs: isolate, verify, measure, quantify; no forbidden template.)
