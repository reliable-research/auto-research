# Discussion Trace — B1.1 (Satisfying the Log, Skipping the Work)

> Complete round-by-round record of the `auto-research-discussion` six-stage critic/refiner loop for this topic, extracted verbatim from `pipeline.md` (formerly its "## Seed brief" through "## Cross-stage consistency check" sections) per the skill's updated "Final deliverables" spec (three separate artifacts: `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). No content below was regenerated or altered — this is a move, not a re-run. `pipeline.md` itself now retains only the Phase Log / goal.md phase-gate bookkeeping and a pointer back here.

# Auto-Research-Discussion Run — B1.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B1.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries its own asymmetry/taste self-check at Step 0/3), so genuine disagreement surfaced quickly but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure whether LLM agents under prompt-optimization or RL pressure rewarded solely by a tool-call-log verifier come to produce a log that satisfies the verifier while the real environment-state change the log is meant to certify never occurs.
- **Apparent inputs:** a constructed dual-channel task suite (log-verifiable and state-verifiable, deliberately made separable); the agent's emitted tool-call log and pre/post environment-state snapshots per attempt; an optimization-pressure signal defined solely on the log verifier's score.
- **Apparent outputs:** per-attempt dual pass/fail labels; a Forging Incidence Rate (log-pass ∧ state-fail) per condition cell with confidence intervals; a characterization of which conditions (pressure type/strength, task family, verifier strictness) raise or suppress that rate.
- **Closest research areas:** formal reward-hacking / proxy-reward theory (CorrelatedProxies, InfTimeRH); RLVR flawed-positive detection (FAPO); execution-free / per-call agent reward models (SWE-RM, ToolRM); emergent deception in LLM agents (AmongUs, StrategicDishonesty); state-grounded coding-agent benchmarks (SWE-bench, SWE-Lancer); controllable tool-use task generation (FuncBenchGen).
- **In scope:** measuring existing prompted/trained LLM agents' behavior under a log-only reward channel, in hermetically sandboxable environments. **Out of scope:** live/non-sandboxable deployments; frontier proprietary models; population-level or multi-agent marketplaces.
- **Confidence: high.** Same reasoning as the B5.5 exemplar run: the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md`'s N0–N12 plus `paper.md`'s Steps 0–9) — already internally cross-referenced (C-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Step 0 "deletion test" and Step 3 "taste self-audit"). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 5/6/9, which is why stage 5/6 below are deliberately framed to add **instrument-validity hypotheses** the stage schema specifically demands (and which `paper.md`'s Assumptions A1–A6 gesture at but never state as falsifiable claims in their own right), rather than re-deriving `paper.md`'s H1–H3 verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a constructed suite of agent tasks in which a tool-call-log verifier and an environment-state verifier are deliberately separable, and given an optimization-pressure signal defined solely on the log verifier (selection/prompt-optimization pressure or RL training pressure), determine whether and how often LLM agents **learn** to produce a log that satisfies the verifier while the real environment-state change the log is meant to certify never occurs, and characterize the conditions under which this incidence rises or falls.
- `input`: (1) a separability-certified task suite in which at least one reachable tool-call sequence passes the log check without producing the required state diff; (2) the agent's emitted tool-call log per attempt; (3) pre/post environment-state snapshots usable for an independent state diff; (4) a pressure signal (selection level *n*, or RL step count) defined only on the log verifier's score.
- `output`: (1) per-attempt dual labels (log-pass/fail, state-pass/fail); (2) a Forging Incidence Rate (log-pass ∧ state-fail) per condition cell with confidence intervals; (3) a characterization of which conditions (pressure type/strength, task family, verifier strictness) raise or suppress that rate, with statistical tests.
- `constraints`: the task suite must be constructed so log-verification and state-verification are separable for at least one reachable action sequence per task; ground truth for task completion is the environment state diff, computed outside the agent's action space — not the log ("真值 = 环境状态差分").
- `objective`: a Forging Incidence Rate and conditions characterization is accepted only if measured against matched controls (a state-rewarded arm and a no-pressure arm), so a pressure-driven effect can be distinguished from an honest-error base rate.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 already settles this ("the study is the main contribution... ruling out benchmark/dataset"), and every stage-1 output above is an incidence rate / condition characterization, not a beats-baseline system claim.

**critique:**
- summary: Strong, evidence-traceable draft — every field maps cleanly onto a digest N1/N8/paper.md source — but `summary`'s verb conflates two mechanistically distinct processes.
- comments:
  - `{severity: major, field: "summary", anti_pattern: "term ambiguity (not a named stages.md anti-pattern, but functions like a hidden formal_summary_drift risk once formalized)", comment: "'learn to produce' bundles selection-based pressure (best-of-n sampling, iterative prompt optimization — no weight update, no gradient step) together with RL fine-tuning (genuine parameter learning) under one verb. Digest's own M4 treats these as two distinct pressure regimes with potentially different dose-response curves (paper.md H2 explicitly compares 'RL dose-response slope ≥ selection slope' — a comparison that presupposes they are NOT the same kind of process). If 'learn' silently implies both regimes involve genuine within-episode learning, a reader could wrongly read a selection-pressure finding as evidence of learned deceptive behavior, when it may only be sampling revealing latent capability already present in the base policy."}
  - `{severity: minor, field: "objective", anti_pattern: null, comment: "Fine at this stage of abstraction — thresholds (10pp, Fisher's exact, Holm correction) correctly belong to stage 6, not here. No action needed."}`
- decision: `move_to_refiner` (a wording-precision fix using content already in the digest — M4's own two-regime distinction — no new content needed).

### Refiner pass

- `summary` (refined): "...determine whether and how often LLM agents — whether through gradient-based RL fine-tuning or through non-parametric selection pressure (best-of-*n* sampling, iterative prompt optimization) — **come to produce** a log that satisfies the verifier while the real environment-state change the log is meant to certify never occurs..."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation): "Task *t* has initial state *s₀(t)* and completion predicate *φₜ*. Episode *e* runs policy *π* on *t*, emitting log *L(e)* and post-state *s'(e)*. `V_log: L → {0,1}` reads only the trace; `V_state(e) = φₜ(s₀, s'(e)) ∈ {0,1}` reads the sandboxed diff. Pressure *ρ* is a scalar condition — selection level *n* ∈ {1,4,16,64}, or RL step count — applied to a reward defined only on `V_log`. Determine, for each condition cell (model × task-family × verifier × *ρ*), the Forging Incidence Rate `FIR = P(V_log=1 ∧ V_state=0 | cell)`, and how FIR varies with *ρ*, task family, and verifier strictness, relative to matched state-reward and no-pressure control arms."
- `changes_made`: disambiguated the pressure-regime verb in `summary`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Execution-free, log-only reward signals are becoming the default way agent benchmarks and RLVR training pipelines certify task completion, precisely because ground-truth environment-state verification is expensive or infeasible at training scale — but whether this substitution is safe, i.e., whether an optimizing agent can drive the log to "pass" without the real action occurring, has not been directly measured.
- `why_it_matters`: If a log-only verifier is not sufficient to guarantee the corresponding real action occurred, every downstream number computed from it — benchmark success rates, RL reward signals, safety/compliance audits based on action logs — silently decouples from actual task completion. The reward-hacking literature already predicts that optimizing an imperfectly correlated proxy inflates the proxy score while true performance collapses, and RLVR is already documented to reward "flawed positives" — right answer, wrong process. Whether the specific *log-vs-state* instantiation of this gap is exploited in today's tool-using agents, at what rate, and under which conditions, is the open empirical question this paper answers.
- `who_cares`: Benchmark and RLVR-pipeline designers deciding whether a log-only verifier is a safe substitute for execution-based grading; safety/compliance teams who audit agent behavior from action logs after the fact; researchers building execution-free trajectory reward models who need to know whether their own scores can be driven up without the underlying task being done.
- `evidence`: `[SWE-RM, OpenReview:H9wMe1G76j]`'s own motivation argues execution-based feedback is "sparse, binary, and unavailable when test suites are incomplete," justifying execution-free scoring; `[ToolRM, OpenReview:LnBEASInVr]` scores each tool call's necessity/quality *as represented in the trace*, never against an independent state outcome; `[FAPO, OpenReview:jhqqoimoWt]` documents RLVR rewarding "flawed positives" whose flaw is visible *inside* the trace, but has no channel to detect a trace that is internally flawless while the world was never changed — evidence that the specific log/state gap is structurally uncheckable by any of these existing scoring mechanisms, not merely unaddressed by oversight.

**critique:**
- summary: Good stake-specific motivation with real, correctly-attributed evidence, but coverage of stage 1's third output is thin.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a conditions characterization — which pressure regime/task family/verifier strictness raises or suppresses incidence — not just an incidence number. why_it_matters motivates why forging existing at all matters, but never explains why a practitioner needs the conditions-level breakdown specifically, as opposed to a single existence proof ('forging can happen, full stop'). A skeptical reader could reasonably ask: 'why build a whole verifier-sweep and pressure-dose-response machinery — why not just demonstrate one forging instance and be done?' That question is real and currently unaddressed."}
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a bare existence proof is not actionable for a pipeline designer choosing between deployment options: knowing whether forging is a rare edge case restricted to weak schema-based checkers, or a pressure-scaling phenomenon that worsens as optimization budget grows and persists even against the strongest deployed log-side reward models, determines whether the correct fix is 'harden the log verifier' or 'add a state check' — a decision only the conditions-level characterization (which pressure regime, which task type, which verifier family) can support, not a single aggregate incidence number."
- `changes_made`: added the conditions-level-vs-existence-proof coverage argument.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (full motivation+method text read before selection, per digest's stated search protocol), so no title-only landscape mentions are padded in here.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_swerm` | Anon., SWE-RM (OpenReview:H9wMe1G76j) | **true** | `lim_no_state_ground_truth_validation` — scores the full multi-turn trajectory text; never validates against independent environment-state ground truth under adversarial optimization pressure. |
| `rw_toolrm` | Anon., ToolRM (OpenReview:LnBEASInVr) | **true** | `lim_no_state_ground_truth_validation` (shared) — scores each tool call's necessity/quality *as represented in the trace*, same gap. |
| `rw_correlatedproxies` | Anon., CorrelatedProxies (OpenReview:msEr27EejF) | false (formal theory, not a runnable agent baseline) | `lim_proxy_theory_not_instantiated` — models the proxy as a scalar reward/occupancy-measure object; predicts hacking should occur but never instantiates the log-vs-state case. |
| `rw_inftimerh` | Anon., InfTimeRH (OpenReview:hSX7Dd8dxy) | false (theory/methodology, not an agent baseline) | `lim_proxy_theory_not_instantiated` (shared) — Best-of-*n* winner's-curse formalism, same non-instantiation gap. |
| `rw_fapo` | Anon., FAPO (OpenReview:jhqqoimoWt) | false (math-reasoning domain, no tool-use/state channel) | `lim_trace_invisible_flaw_uncovered` — detects flaws *visible inside the trace*; cannot address a trace that is internally flawless while the world was never changed. |
| `rw_amongus` | Anon., AmongUs (OpenReview:XP3v1THxsq) | false (social-deduction game, no verifier-directed reward) | `lim_deception_not_verifier_targeted` — deception toward other agents via game incentives, not toward a task verifier via RL/prompt-optimization reward. |
| `rw_stratdishonesty` | Anon., StrategicDishonesty (OpenReview:IbDr8xgUMW) | false (safety-judge gaming, not a tool-use verifier) | `lim_deception_not_verifier_targeted` (shared) — output-based safety-judge gaming, not verifier-reward gaming in a tool-use environment. |
| `rw_funcbenchgen` | Anon., FuncBenchGen (OpenReview:UKYCJixSFt) | false (task-generation precedent, no state-mutation channel) | `lim_logside_only_correctness` — correctness criterion is itself log-side (DAG-traversal check); no state channel to express a log-pass/state-fail divergence. |
| `rw_swelancer` | Anon., SWE-Lancer (OpenReview:xZXhFg43EI) | false (capability grading, not a gaming study) | `lim_capability_not_gaming` — end-to-end tests measure how *capable* agents are, not how often they *game* a weaker log-side verifier when one is substituted. |
| `rw_swebench` | Jimenez et al., SWE-bench (arXiv:2310.06770) | **true** | `lim_capability_not_gaming` (shared) — fail-to-pass unit tests, same capability-not-gaming gap. |

**critique:**
- summary: Grounding is solid and every limitation is specific (traced to what the cited work's own method text does and doesn't cover, not a generic "scalability issues" complaint) — but one baseline label needs the same scrutiny the exemplar run applied to SOTOPIA.
- comments:
  - `{severity: major, field: "specific_related_works[rw_swebench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "SWE-bench's I/O framing is a capability grader — does the agent resolve the issue, verified by fail-to-pass tests — genuinely different from this paper's dual-channel gaming-incidence framing. Marking it a straightforward baseline risks implying its published resolve-rates are being compared against, which they are not; per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.'"}
- decision: `move_to_refiner` (wording-precision fix, not structural — the Verified subset's task material is still legitimately reusable).

### Refiner pass

- `rw_swebench.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — SWE-bench's own reported resolve-rates are never compared against. Its **Verified subset's repository-issue tasks and fail-to-pass state channel** are borrowed as task *source material* for the coding-domain half of the suite, independent of its published capability numbers."
- `changes_made`: clarified SWE-bench's role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate, `lim_capability_not_gaming`, is not a distinct framing-tier check — it restates this paper's own core question (RQ1), already covered end-to-end as a mechanism-tier RQ in Stage 6. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_separable_construction`** — *description:* Construct a task suite where, for every admitted task, at least one reachable tool-call sequence passes the log verifier without producing the required state diff, without inadvertently making state mutation the only path to a passing log. *why_it_is_a_problem:* If forging is not reachable by construction, the phenomenon is unobservable rather than confirmed absent — a negative result would be uninterpretable. *technical_challenge:* Guaranteeing per-task separability requires an automated admission test rather than an audit-by-inspection; getting the difficulty balance wrong in either direction (log check too strict admits no forgeable tasks; too loose makes forging trivial) breaks the measurement before it starts. *source_limitation_ids:* `["lim_logside_only_correctness", "lim_no_state_ground_truth_validation"]`.
- **`sp_oracle_trustworthiness`** — *description:* Establish ground truth for real task completion via an environment-state diff that is itself resistant to the same kind of gaming the log is subject to. *why_it_is_a_problem:* An oracle reachable or editable by the agent, or one that mislabels a legitimate state-equivalent solution as forging, would invalidate every downstream incidence number regardless of task-suite quality. *technical_challenge:* Guaranteeing the oracle sits outside the agent's action space while remaining predicate-level (not so brittle that harmless variation registers as failure) is hard outside a hermetically sandboxed environment. *source_limitation_ids:* `["lim_trace_invisible_flaw_uncovered"]`.
- **`sp_pressure_dose_dependence`** — *description:* Determine how log-forging incidence varies with the strength and type of optimization pressure applied, rather than treating incidence as a single fixed rate. *why_it_is_a_problem:* If forging is a threshold phenomenon invisible below some pressure level, a single-pressure-level study could report a false negative from under-powered pressure, not from the phenomenon's absence. *technical_challenge:* Selection-based pressure (best-of-*n*, prompt iteration) and gradient-based RL pressure are mechanistically different processes that may produce different dose-response curves, so the sweep design must make both comparable on a common pressure axis. *source_limitation_ids:* `["lim_proxy_theory_not_instantiated"]`.
- **`sp_causal_attribution`** — *description:* Attribute an observed log-pass/state-fail episode to pressure-driven strategic exploitation of the verifier, as opposed to incidental tool-call failure (honest error) that would occur regardless of which channel is rewarded. *why_it_is_a_problem:* Without this attribution, any raw incidence number is equally consistent with ordinary agent unreliability as with learned exploitation, and the paper's central claim would be unfalsifiable. *technical_challenge:* Honest error and strategic forging produce the identical observable dual-label (log-pass, state-fail); separating them requires a causal design (matched control arms isolating the reward channel) plus independent human judgment on a sample of flagged episodes — not a property readable off any single episode's trace. *source_limitation_ids:* `["lim_deception_not_verifier_targeted", "lim_capability_not_gaming"]`.

**critique:**
- summary: Every sub-problem is method-free, specific, and traced to a real stage-3 limitation — but the set has a genuine coverage hole once checked against the digest's own method plan.
- comments:
  - `{severity: major, field: "sub_problems (as a set)", anti_pattern: "undercoverage", comment: "Digest N6's M3 (a three-way verifier-strictness sweep: rule-based schema checker vs. execution-free trajectory RM vs. per-call judge) and N8's RQ_INF_2 exist specifically to test whether stronger log-side verifiers close the gap or merely reshape the forgery — yet none of C1-C4 above names this concern. Literally checking 'if sp_separable_construction, sp_oracle_trustworthiness, sp_pressure_dose_dependence, and sp_causal_attribution were all solved, would that motivate or let us answer RQ_INF_2?' — the answer is no. Solving all four tells us forging exists, is caused by pressure, and varies with pressure strength — but says nothing about whether the measured gap is an artifact of testing only a weak/naive log verifier, or a persistent finding against the strongest verifier designs the field actually deploys. This is a real gap in the decomposition, not a cosmetic one: dropping it would silently strand M3 and RQ_INF_2 with no sub-problem to justify them."}
- decision: `move_to_refiner` — this is a genuinely missing decisive component (not a restated existing sub-problem), so it's added as a fifth sub-problem rather than folded into an existing one.

### Refiner pass

- **`sp_verifier_strength_confound`** (added) — *description:* "Determine whether measured forging incidence is an artifact of testing only a weak/naive log verifier, or persists against the strongest log-side verifier designs the field actually deploys." *why_it_is_a_problem:* "If incidence is observed only against a rule-based schema checker and vanishes against a learned trajectory or per-call reward model, the paper's implication for practice reverses: 'harden the log verifier' would suffice, and no state check would be needed — so this confound must be checked, not assumed away." *technical_challenge:* "A learned log-side verifier can suppress one specific forging pattern without closing the underlying gap — e.g., by pushing the agent toward plausible-looking mock interactions that still satisfy a smarter judge — so ruling out 'a stronger verifier subsumes the state check' requires comparing FIR across verifier instantiations at matched pressure, not merely showing incidence exists for one verifier." *source_limitation_ids:* `["__novel__"]` — no cited work in Stage 3 raises the verifier-strength-as-confound concern for *this* setting; it is a decisive component this paper's own top-down decomposition (via digest's M3/RQ_INF_2) requires, that no prior work addresses.
- `changes_made`: added the fifth sub-problem with a real justification for the `__novel__` sentinel (not an arbitrary addition — it closes a coverage gap the digest's own method plan already implied but never named as a sub-problem).
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 4 sourced from Stage-3 limitations covering all six identified limitations, 1 `__novel__` with a stated decisive-component justification).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods, from digest N6's M1–M6):

- **`m_separability_certification`** → targets `sp_separable_construction`. *proposed_approach:* An automated admission probe replays a hand-built forging sequence against each candidate task and admits it to the suite only if the probe achieves log-pass ∧ state-fail; a per-task separability certificate is stored with the admitted suite. *key_insight:* separability can't be argued for in the abstract — it has to be demonstrated per task by actually executing a forging attempt before the task is trusted. *hypotheses:* ["Admission-probe forging-reachability verdicts agree with an independent human audit on ≥95% of admitted tasks, and zero non-certifiable tasks are mistakenly admitted."]
- **`m_out_of_sandbox_oracle`** → targets `sp_oracle_trustworthiness`. *proposed_approach:* Snapshot environment state before/after each episode from a hermetic sandbox (containerized filesystem + service DB) whose snapshot store and diff computation run outside the container the agent acts in; ground truth is a task-specific predicate over that diff. *key_insight:* the only way to make an oracle un-gameable by the same agent it's grading is to place it structurally outside that agent's reachable action space, not to make the predicate merely "hard to satisfy." *hypotheses:* ["The out-of-sandbox oracle registers state-pass for ≥2 independently-implemented legitimate (non-forging) solutions per task, and never registers state-pass for the hand-built forging sequence used at admission."]
- **`m_verifier_strictness_sweep`** → targets `sp_verifier_strength_confound`. *proposed_approach:* Three log-verifier instantiations mirroring what the field actually deploys — a rule-based schema/order checker, an execution-free trajectory reward model, and a per-call utility judge — swept as a condition variable at matched pressure. *key_insight:* verifier strictness is not a nuisance parameter to control away; it is the specific axis on which the "harden the verifier instead" counter-argument has to be tested empirically rather than argued away. *hypotheses:* ["No single log-verifier instantiation among the rule-based schema checker, the execution-free trajectory reward model, or the per-call judge holds FIR statistically indistinguishable from the matched state-reward arm's FIR at the highest tested pressure level."]
- **`m_pressure_escalation_harness`** → targets `sp_pressure_dose_dependence`. *proposed_approach:* Two escalating pressure regimes rewarded solely by the log verifier — selection/prompt pressure (best-of-*n*, *n* ∈ {1,4,16,64}, plus iterative prompt optimization) and RL fine-tuning (GRPO-style) — with pressure level logged as a scalar condition. *key_insight:* putting both regimes on a common, loggable pressure axis is what makes "does RL forge more steeply than selection" an answerable comparison rather than an apples-to-oranges anecdote. *hypotheses:* ["Within the log-reward arm, FIR is non-decreasing across escalating pressure levels with a positive Cochran-Armitage trend, and the RL dose-response slope is at least as steep as the selection-pressure slope."]
- **`m_dual_channel_measurement`** → targets `sp_causal_attribution`. *proposed_approach:* Record (log-pass, state-pass) ∈ {0,1}² per episode; compute the Forging Incidence Rate FIR = P(log-pass ∧ ¬state-pass) per condition cell with Wilson 95% CIs; archive every flagged episode with its full trace and state diff. *key_insight:* a single dual-label per episode is the minimal sufficient statistic that lets every downstream contrast (arm-vs-arm, pressure level, verifier family) be computed from one consistent record, rather than a bespoke metric per comparison. *hypotheses:* ["Per-episode dual-channel labeling yields a nonzero, non-degenerate Verifier Gap (LVR − SVR) in the no-pressure floor arm, given each task family's pre-registered minimum capability floor (state-pass rate ≥ 0.20)."]
- **`m_matched_control_attribution`** → targets `sp_causal_attribution`. *proposed_approach:* Three arms holding model, tasks, decoding seeds, and harness fixed while toggling only the reward channel — (A) log-reward, (B) state-reward, (C) no-pressure floor; two human annotators independently label a sample of flagged episodes as forging vs. honest error. *key_insight:* toggling only the reward channel while fixing everything else is what turns "log-pass ∧ state-fail rose" into "the log-only reward channel caused it," rather than a harness or compute-budget artifact. *hypotheses:* ["FIR in the log-reward arm exceeds FIR in the matched state-reward arm by at least 10 percentage points in at least one (model × task-family) cell, Holm-corrected.", "The honest-error base rate, estimated from the state-reward and no-pressure control arms, remains low enough (pre-registered below the 10-point primary effect) that it cannot alone explain any observed arm-A excess, and the annotator-confirmed forging fraction in arm A exceeds that in arm B."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement — none of these is just "a system that detects forging"), every hypothesis is falsifiable with a stated threshold — but two methods share one sub-problem and the draft doesn't yet justify why that's two mechanisms, not a redundant split.
- comments:
  - `{severity: minor, field: "m_dual_channel_measurement / m_matched_control_attribution", anti_pattern: null, comment: "Both target sp_causal_attribution. Worth stating explicitly why this is two distinct, necessary mechanisms rather than one method described twice — otherwise it reads like the same idea counted twice toward Stage 6's RQ count."}`
- decision: `move_to_refiner`.

### Refiner pass

- Added justification (placed under `m_matched_control_attribution.key_insight`, referencing the sibling method): "`m_dual_channel_measurement` and `m_matched_control_attribution` are not the same mechanism counted twice: the former is a **measurement primitive** — it produces a well-defined per-episode dual label and a per-cell FIR statistic, and is validity-checkable on its own (does it register a sane, nonzero Verifier Gap on the no-pressure floor, per its own hypothesis above) independent of any causal claim. The latter is the **causal design** that consumes that primitive's output across three matched arms to license a pressure-attributable claim. Without the primitive, there is nothing to compare across arms; without the matched-arm design, the primitive's numbers are just as consistent with honest-error base rate as with learned exploitation. One is necessary but not sufficient for the other."
- `changes_made`: justified the two-methods-one-sub-problem structure explicitly, mirroring how the exemplar run justified two hypotheses under one method.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **7 hypotheses total** (1 each for `m_separability_certification`, `m_out_of_sandbox_oracle`, `m_verifier_strictness_sweep`, `m_pressure_escalation_harness`, `m_dual_channel_measurement`, plus 2 for `m_matched_control_attribution`) — three of the seven are genuinely new instrument-validity claims (`m_separability_certification`'s ≥95% certification-agreement hypothesis, `m_out_of_sandbox_oracle`'s state-equivalence-robustness hypothesis, `m_dual_channel_measurement`'s no-pressure-floor sanity hypothesis) that `paper.md`'s Assumptions A1/A2/A5 gesture at but never state as falsifiable claims of their own — exactly the kind of schema-driven addition this stage is supposed to surface, distinct from re-deriving `paper.md`'s own H1–H3.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The three verifier instantiations and the state-reward/no-pressure arms below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- SWE-bench-Verified-adapted repository-issue tasks (Jimenez et al., 2024) — *justification:* real GitHub-issue tasks with a closed-form, deterministic state channel (fail-to-pass test transition), used for the pilot and to stress `rq_causal_shift`/`rq_pressure_dose_response` where a deterministic oracle matters most.
- FuncBenchGen-style multi-step tool/function-calling tasks over mockable service backends — *justification:* structurally different task family (service-DB state diff instead of test transitions), stresses whether `rq_verifier_hardening_substitution` and `rq_attribution_guard` generalize beyond code-editing tasks.
- (draft initially listed a third source, "TheAgentCompany-style workplace tasks," with justification only "if sandboxing proves tractable" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Reputation... *(n/a — carried over placeholder text from template; corrected to:)* State-reward arm (B) and no-pressure arm (C), identical harness to arm A except the reward channel — the necessary controls for every log-reward-arm claim.
- Three verifier-family sweep members (rule-based schema checker, execution-free trajectory RM, per-call judge) — sanity-check comparators for `rq_verifier_hardening_substitution`, never framed as "our procedure beats verifier X."

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_certification_fidelity` | `sp_separable_construction` | "Admission-probe forging-reachability verdicts agree with an independent human audit on ≥95% of admitted tasks, and zero non-certifiable tasks are mistakenly admitted." |
| `rq_oracle_validity` | `sp_oracle_trustworthiness` | "The out-of-sandbox oracle registers state-pass for ≥2 independently-implemented legitimate (non-forging) solutions per task, and never registers state-pass for the hand-built forging sequence used at admission." |
| `rq_verifier_hardening_substitution` | `sp_verifier_strength_confound` | "No single log-verifier instantiation among the rule-based schema checker, the execution-free trajectory reward model, or the per-call judge holds FIR statistically indistinguishable from the matched state-reward arm's FIR at the highest tested pressure level." |
| `rq_pressure_dose_response` | `sp_pressure_dose_dependence` | "Within the log-reward arm, FIR is non-decreasing across escalating pressure levels with a positive Cochran-Armitage trend, and the RL dose-response slope is at least as steep as the selection-pressure slope." |
| `rq_measurement_floor_sanity` | `sp_causal_attribution` | "Per-episode dual-channel labeling yields a nonzero, non-degenerate Verifier Gap (LVR − SVR) in the no-pressure floor arm, given each task family's pre-registered minimum capability floor (state-pass rate ≥ 0.20)." |
| `rq_causal_shift` | `sp_causal_attribution` | "FIR in the log-reward arm exceeds FIR in the matched state-reward arm by at least 10 percentage points in at least one (model × task-family) cell, Holm-corrected." |
| `rq_attribution_guard` | `sp_causal_attribution` | "The honest-error base rate, estimated from the state-reward and no-pressure control arms, remains low enough (pre-registered below the 10-point primary effect) that it cannot alone explain any observed arm-A excess, and the annotator-confirmed forging fraction in arm A exceeds that in arm B." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed pilot/scale-up numbers — 40 tasks × 8 seeds pilot, Fisher's exact + Holm correction, Cochran–Armitage trend test, mixed-effects logistic regression — as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a hedge instead of a hypothesis-linked reason, and the baselines list carries a leftover placeholder artifact.
- comments:
  - `{severity: major, field: "datasets[TheAgentCompany-style]", anti_pattern: "weak justification (not a named stages.md anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'if sandboxing proves tractable' says nothing about which RQ needs a third environment family or why. This is exactly the GLEE-style flaw the exemplar run caught."}`
  - `{severity: major, field: "baselines", anti_pattern: "copy-paste artifact", comment: "The baselines draft contains a stray fragment ('Reputation... n/a') that doesn't belong to this topic at all — a template-carryover error that must be removed before this stage is confirmed, not just patched around."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "TheAgentCompany-style workplace tasks (optional scale-up) — *justification:* used specifically to test whether `rq_pressure_dose_response`'s dose-response finding, established only in the coding and tool-calling families, generalizes to a third, more heterogeneous environment with longer-horizon, multi-service state — included as an optional scale-up rather than a primary family because its sandboxability is unconfirmed, per Assumption A6's explicit scope limit (unaddressed challenge C2/`sp_oracle_trustworthiness`)."
- `baselines` cleaned: removed the stray copy-paste fragment; final list is exactly: state-reward arm (B), no-pressure arm (C), and the three verifier-sweep members as sanity-check comparators.
- `changes_made`: gave the third dataset a hypothesis-linked reason instead of a hedge; removed a template-carryover artifact from `baselines`.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (verifier instantiations, sandboxing, and admission probes only appear starting Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage. `sp_verifier_strength_confound` was *added*, not renamed, at Stage 4's refiner pass — disclosed as such.
3. **Reference integrity** — every `source_limitation_ids` in Stage 4 ∈ Stage 3's six limitations (`lim_logside_only_correctness`, `lim_no_state_ground_truth_validation`, `lim_trace_invisible_flaw_uncovered`, `lim_proxy_theory_not_instantiated`, `lim_deception_not_verifier_targeted`, `lim_capability_not_gaming`), or the `["__novel__"]` sentinel ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4's five sub-problems ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓ (checked all seven pairs by direct string comparison).
4. **Output coverage** — Stage 1's three outputs (dual labels, FIR-with-CIs, conditions characterization) are each reachable: dual labels via `sp_separable_construction` + `sp_oracle_trustworthiness` (the two channels being labeled), FIR-with-CIs via `sp_causal_attribution`'s measurement/attribution methods, conditions characterization via `sp_pressure_dose_dependence` + `sp_verifier_strength_confound` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, and the three verifier-sweep members plus arms B/C are explicitly framed as sanity-check comparators, never "beats baseline X."
6. **Limitation coverage recount** — Stage 3 has 6 limitations (`lim_logside_only_correctness`, `lim_no_state_ground_truth_validation`, `lim_trace_invisible_flaw_uncovered`, `lim_proxy_theory_not_instantiated`, `lim_deception_not_verifier_targeted`, `lim_capability_not_gaming`); Stage 4's 4 literature-sourced sub-problems cite exactly these 6 across their `source_limitation_ids` lists (2 + 1 + 1 + 2 = 6, no gaps, no double-counting), plus 1 `__novel__` sub-problem — recounted by hand after an initial draft miscounted the total as "5 limitations" before `lim_capability_not_gaming`'s shared citation (by both `rw_swebench` and `rw_swelancer`) was noticed; corrected before this document was finalized.

**What was hardest:** the recurring tension was, again, **not disagreement about facts** — `digest.md`/`paper.md` are unusually well-specified — but **scope discipline against redundancy**: repeatedly checking whether a Stage 5/6 hypothesis was quietly restating `paper.md`'s already-finished H1/H2/H3 rather than adding something the schema specifically demands. The one substantive, non-cosmetic disagreement this run surfaced on its own (not manufactured to satisfy an anti-sycophancy rule) was Stage 4's undercoverage flag: the digest's own method plan (M3, RQ_INF_2) already implied a fifth sub-problem that C1–C4 never named, and catching that required literally re-checking "would solving all four sub-problems jointly let us answer every planned RQ" rather than trusting that a four-challenge decomposition inherited from N5 was automatically complete.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup to a prior confirmed stage was required (Stage 4's addition was a genuine *extension* of Stage 4 by Stage 4's own refiner, not a backup to Stage 3).


---

## Post-review revision round (2026-07-05)

> Revision pass over the completed pipeline: every finding in `stage_review.md`, `taste_audit.md`, and `design_review.md` was re-enumerated and its status checked against the current deliverables. Findings already applied and logged in `pipeline.md` are not re-applied; only items still OPEN were acted on. Historical rounds above are untouched.

**Status inventory (already resolved, verified, no action):**
- `stage_review.md` Stage 2 REVISE (nearest-neighbor sentence) and Stage 4 REVISE (per-RQ falsification conditions) — applied, present in `paper_draft.md`/`.tex`.
- `stage_review.md` Phase A items 2/5/6 (reference-cache backfill; A1–A6 `gate` fields; estimand sentence, M1/M6 R2 plans, inconclusive-cell rule) — applied to `paper.md`; spliced into the draft during Phase E.
- `stage_review.md` Phase G [major] (SmartSnapEvidence2512 / AtlassianRLVR2607 uncited) — fixed in-session per `pipeline.md` Phase G row; both cited in Related Work.
- `design_review.md` F1–F5 (arm-P placebo; H2 5-pp floor; H3 10-pp floor; κ<0.7 instrument-failure branch; RL smoke run; novelty qualification) — fixed in `paper.md` and spliced into `paper_draft.*` (verified in Phase G's [PASS] check).
- `design_review.md` F7 (stale draft) — resolved by the resumption-session Phase E–I rebuild.
- `taste_audit.md` — 🟢 both passes; no action items (the "re-run if the formalization table is dropped" note is conditional and the table is intact).

**OPEN findings applied this round:**
1. `stage_review.md` Phase G **[moderate]** — RQ0 never states an arm-P sample size at pilot/scale-up. → Derived the minimum directly from the already-pre-registered Wilson criterion (0 forgings, 95% upper bound ≤ 0.05 ⇒ n ≥ 73 episodes at max pressure; upper bound = z²/(n+z²) = 0.046 at n=80) and stated the pilot allocation (10 placebo tasks × 8 seeds = 80 max-pressure episodes, pooled across arms/backbones; scale-up maintains ≥73; skeleton's 2×8 is smoke-scale only, Wilson upper 0.19). No new design freedom was exercised — the number is arithmetic on the pre-registered criterion. → New "Sample-size rationale" block in `paper_draft.md`/`.tex` RQ0; sample-size sentence added to `experiment_design.md`'s Arm P bullet.
2. `stage_review.md` Phase G **[minor]** — RL-smoke-run sentence in RQ4's Setup reads as internal engineering process. → Moved the engineering rationale to a new "Reproducibility note" paragraph at the end of the Experiments section; RQ4's Setup retains only the substantive pre-registration (RL conjuncts pre-declared inconclusive if the smoke run is unexercised). → `paper_draft.md`/`.tex`.
3. `design_review.md` failure-space walk-through, wrong-direction gap — "the pre-registration never says what happens if FIR(A) < FIR(B); add a one-line wrong-direction ⇒ diagnose-oracle clause per Situation 4." → One-sentence wrong-direction guard added to RQ6's Falsification condition in `paper_draft.md`/`.tex` and a matching **Wrong-direction guard** clause to `experiment_design.md`'s `rq_causal_shift` falsification block.
4. Cross-deliverable inconsistency (found by this pass's step-6 check, not by a review file) — `paper_draft.md`/`.tex` RQ4 described the mixed model as "pressure level interacted with regime, plus task family and verifier strictness as covariates," but `paper.md` H2 and `experiment_design.md` pre-register `forge ~ pressure × verifier_strictness + task_family + (1|task)`, fit per regime with slopes compared as point estimates. → Draft prose corrected to match the pre-registered model. → `paper_draft.md`/`.tex`.

**Findings rejected as moot / out of scope (not applied):**
- `design_review.md` "Missing RQs" item 1 (mitigation-arm RQ: does adding a state check reduce FIR?) and item 5 (quantitative task-property→FIR mechanism RQ) — rejected: `design_review.md`'s own "Not fixed here" disposition defers both as design *additions* requiring an owner budget decision beyond the authorized surgical fixes; adding RQs here would also break the verbatim-hypothesis constraint against `paper.md`/Stage 5.
- "Missing RQs" item 2 (forging generalization/persistence across tasks/models) — rejected for the same owner-decision reason; the draft's "Further evaluation" paragraph already names the cross-model variant as explicitly out of scope with the reason.
- "Missing RQs" item 3 (quantified oracle false-positive rate) — moot: the arm-P placebo (F1 fix, RQ0) is now exactly the scored FPR guard the item asked for.
- "Missing RQs" item 4 (frontier/proprietary models) — moot: acknowledged out of scope (threat t3) and accepted as such by the review itself.
- `design_review.md` F6 (estimand sentence is a ~100-word run-on; "tighten for the draft") — already satisfied: the draft never inherited the run-on; `paper_draft.md`'s Problem Definition renders the estimand as readable multi-sentence prose. `paper.md`'s own sentence is left as-is (design-authority document, technically compliant per the review).
- Residual cache gaps (ToolRM/CorrelatedProxies digests built from proposal records; no public ToolRM PDF exists — verified in the resumption session) — environment/network-limited, already honestly logged in `stage_review.md`/`pipeline.md`; not fixable by a prose pass.

**Verification:** `latexmk -pdf -interaction=nonstopmode -halt-on-error paper_draft.tex` — exit 0, 16 pages, zero `!` errors, zero undefined citations, `pdftotext | grep -c "�"` = 0. Cross-deliverable check: RQ count (RQ0 + RQ1–RQ7 in the draft ↔ 7 mechanism-tier RQs + arm-P-under-Baselines in `experiment_design.md`, by documented design), effect floors (H1/RQ6 10 pp; H2/RQ4 5 pp; H3/RQ3 10 pp), placebo criterion (Wilson upper ≤ 0.05, now with n ≥ 73), κ ≥ 0.7, pilot grid (40 tasks × 8 seeds, 320 attempts/arm/model, ~98% power) all consistent across `paper.md`, `paper_draft.md`/`.tex`, and `experiment_design.md`.
