# Discussion Trace — T3.2 (auto-research-discussion, all six stages)

> Extracted verbatim from `pipeline.md` per the `auto-research-discussion` skill's updated "Final deliverables" spec (deliverable 3: the complete round-by-round record — every draft, every critique with severities/resolution, every decision, every refiner pass). No content was regenerated or altered in this extraction; `pipeline.md` now carries only a pointer to this file plus its own Phase Log (the separate `goal.md` §2 phase-gate tracking section, which is not part of this trace).

# Auto-Research-Discussion Run — T3.2 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T3.2**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already ran its own asymmetry/taste self-audit at Step 0/3 and a full pre-registration through Step 9), so genuine disagreement surfaced quickly but didn't require re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. One REVISE finding from `stage_review.md` (a missing nearest-neighbor sentence in Related Work) and one REVISE finding on the Experiments section (the reactivity-calibration RQ's gating role was buried inside its own subsection rather than stated up front) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Determine whether the previously reported ~8x differential decay rate between soft organizational-policy adherence and hard safety-norm adherence in LLM in-context constraint following is driven by contextual salience (position/repetition), wording framing (strength), or pretraining/alignment-prior strength.
- **Apparent inputs:** matched soft-policy/hard-safety-norm constraint-statement pairs; a long-horizon multi-turn conversation environment padded with realistic distractor turns; orthogonal manipulation schedules for wording strength, context position, and repetition count; a prior-strength proxy battery.
- **Apparent outputs:** per-turn, per-condition constraint-adherence measurements; fitted discrete-time survival curves and decay half-lives per condition; a variance decomposition attributing the soft/hard decay-rate gap to salience, framing, and a residual (prior-linked) share.
- **Closest research areas:** long-context preference/policy adherence measurement (PrefEval, OffTopicEval); multi-turn dialogue-consistency and degradation (SafeDialBench, "LLMs Get Lost in Multi-Turn Conversation"); mechanistic accounts of context degradation (SinkTrack's positional-salience account, ICFBench's paired forgetting design); alignment-prior depth and wording robustness (SafetyFewTokensDeep, TARE, RECAST).
- **In scope:** measuring existing prompted LLM agents' constraint-decay behavior under a manipulated salience/framing treatment, with the unmanipulable alignment prior proxied rather than intervened on directly. **Out of scope:** training new alignment methods or mitigation systems; multi-agent or tool-using deployments; live, non-sandboxable deployments.
- **Confidence: high.** As with the calibration exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already carries its own internal cross-referencing (N-node ↔ C/M-component ↔ RQ ids) and its own asymmetry/taste self-check (`paper.md` Step 0/3). Reconstruction risk is low; the risk is instead *redundancy* with `paper.md`'s own Step 6, which is why stages 5/6 below are framed as validating the **measurement instrument's own properties** (matched-pair construction, reactivity calibration, proxy validity) rather than re-deriving `paper.md`'s hypotheses verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a matched bank of soft-policy and hard-safety-norm constraint statements injected into long-horizon multi-turn LLM conversations, and given the ability to orthogonally manipulate the constraint's wording strength, context position, and repetition count, determine which of three candidate mechanisms — contextual salience, wording framing, or pretraining/alignment-prior strength — drives the previously reported ~8x differential decay rate between soft and hard constraint adherence.
- `input`: (1) matched pairs of soft/hard constraint statements (same topic domain, comparable length, comparable verifier type); (2) a long-horizon multi-turn conversation environment with realistic distractor turns; (3) manipulation schedules for wording strength (advisory/standard/imperative), context position (system-head/system-tail/mid-conversation), and repetition count; (4) a battery of prior-strength proxies (no-injection compliance, base-vs-instruct compliance delta, per-token KL for open-weight models).
- `output`: (1) per-turn, per-condition constraint-adherence measurements; (2) fitted discrete-time survival/decay curves and half-lives per condition; (3) a variance decomposition attributing the soft/hard decay-rate gap to salience, framing, and a residual (prior-linked) share.
- `constraints`: constraint pairs must be verifiably matched on topic/length/verifier-type; conversations run to a bounded horizon with probes at scheduled turns; the probing instrument's own potential to refresh salience must be measured, not assumed neutral.
- `objective`: a mechanism-attribution claim is accepted only if it is derived from a pre-registered dominance/partial-R² decomposition of the fitted hazard model, and only after the measurement instrument's own reactivity has been calibrated and shown not to differentially bias the attribution by constraint type.
- `study_type`: `empirical` — stated explicitly: digest N12 already classifies this `empirical` ("the projected results... are measurement findings — variance shares and half-life contrasts — not a released benchmark or trained system"), and the core question is a mechanism-attribution/measurement question, not a proposed fix.

**critique:**
- summary: Grounded and well-scoped, but the objective has an evaluability gap that mirrors a structural risk `paper.md` itself already names, and the summary quietly presupposes the premise it's supposed to test.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says a mechanism-attribution claim requires a dominance decomposition, but never states what happens if the decomposition's precondition fails — i.e., if the ~8x gap itself does not replicate directionally in a content-matched design. paper.md's own Assumption A1 and 'Global fallback F-G1' treat non-replication as a first-class, differently-shaped outcome ('the gap does not survive content-matched... measurement'), not a footnote. An objective that is silent on this forces a mechanism-attribution finding onto a premise that might not hold."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'determine which of three candidate mechanisms... drives the previously reported ~8x... decay rate' presupposes both that the gap replicates and that it is fully decomposable among exactly these three mechanisms. Prefer language that treats replication as the first thing being checked, not a given."}`
- decision: `move_to_refiner` (both are formalize-level fixes using content already stated in paper.md's own assumptions — no new content needed).

### Refiner pass

- `objective` (refined): "A mechanism-attribution claim is accepted only if (i) the soft/hard decay-rate gap first replicates directionally in the content-matched design (the fitted hazard ratio's confidence interval excludes 1), and (ii) the attribution itself is derived from a pre-registered dominance/partial-R² decomposition whose measurement instrument has been calibrated and shown not to differentially bias the comparison by constraint type. If the gap does not replicate, the study reports non-replication of the premise itself as the finding, rather than forcing a mechanism attribution onto an effect that isn't there."
- `summary` (refined): "...determine **whether, and to what degree,** three candidate mechanisms — contextual salience, wording framing, and pretraining/alignment-prior strength — account for the previously reported ~8x differential decay rate..., **first requiring that the gap itself replicate in a matched-pair design uncontaminated by verifier-class or difficulty confounds.**"
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation): "Constraint `c` has type τ(c)∈{soft,hard}, wording w(c)∈{advisory,standard,imperative}, position p∈{sys-head,sys-tail,mid-turn}, repetition r∈{1,3,5}. Conversation turns t=1..T; probe outcome A_c(t)∈{0,1}. Discrete-time hazard h(t|τ,w,p,r) fitted via `hazard ~ turn × τ × w × p × r + (1|pair) + (1|model)`. Gap `G = exp(β_{τ×turn})`. Determine the dominance-weight/partial-R² share of factor blocks {w, p, r} versus the residual (prior-proxy-linked) share in explaining `β_{τ×turn}`, conditional on `G`'s confidence interval excluding 1."
- `changes_made`: tightened the objective's evaluability condition to name the non-replication branch explicitly; removed the summary's presupposition that the gap and its three-way decomposability are givens; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: If deployed LLM agents' soft organizational policies decay dramatically faster than hard safety norms, but nobody knows whether that is because soft policies are less salient in context, worded more weakly, or simply lack the deep alignment-training reinforcement that hard norms have, then any attempt to fix the gap is guesswork — and the guess can be wrong in an expensive direction.
- `why_it_matters`: Soft policies (scope limits, tone rules, business preferences) govern the difference between a compliant agent and a silently drifting one; unlike hard-safety failures, soft-policy violations rarely trip any alarm, so an agent that has drifted out of its declared role can operate undetected for many turns before anyone notices (digest N2 MotivationItem 1: "creating an invisible governance gap"). Whether this is fixable by placement/wording changes or requires training-time reinforcement is not a stylistic question — it is the entire difference between a cheap deployment-time patch and an unsolved training problem, and current practice conflates the two because no one has separated them.
- `who_cares`: Organizations deploying long-running LLM agents governed by system-prompt policies; teams deciding whether restatement/placement heuristics are sufficient mitigation, or whether they need to invest in training-time interventions instead; researchers who currently report soft-policy decay (PrefEval) and hard-norm persistence under pressure (SafeDialBench) as separate phenomena with no shared causal account.
- `evidence`: `[OffTopicEval, OpenReview:EcIyiJrajc]`'s own motivation argues an agent "may be unsafe even when it never produces overtly harmful content, simply because it answers requests that lie outside its declared role" — establishing soft-policy drift as a distinct, real failure surface, independent of hard-safety failure. `[PrefEval, OpenReview:QWunLKbBGF]` and `[SafeDialBench, OpenReview:KFjtRqVnKH]` each report degradation within their own constraint tier but neither compares soft against hard within one matched causal design — itself evidence the question is open (digest N3 absence_comment: no corpus paper runs the salience/framing/prior ablation together).

**critique:**
- summary: Stake-specific and well-cited, but coverage of Stage 1's third output — the residual, prior-linked share specifically — is thin.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a three-way variance decomposition, and the residual (prior-linked) share is the one component that can never be directly manipulated — only proxied. why_it_matters justifies attributing the gap to salience/framing (both manipulable, both actionable by a policy author) but never explains why bothering to model and report the unmanipulable residual specifically matters. A skeptical reader could reasonably ask: 'why not just report whether manipulating salience+framing closes the gap, full stop, and skip the proxy battery?' Without an answer, CO4's negative-guidance clause ('if the prior dominates, no amount of prompt engineering will make soft policies as durable as safety norms') is asserted by elimination rather than motivated."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the decision this study is meant to license is binary and expensive to get wrong: if salience and framing can close the gap, the fix is a placement/wording change available to any policy author today; if a nonzero residual survives even after matching a soft policy's presentation to a hard norm's, that residual is evidence that training-time reinforcement — not prompt engineering — is required. But 'we manipulated wording and position and the gap didn't fully close' is, by itself, equally consistent with an untested fourth mechanism as with a real prior-linked residual. The proxy battery is what turns 'we didn't test for it' into 'we measured it, and it does or does not move the residual' — the only way the training-route guidance is falsifiable rather than inferred by elimination."
- `changes_made`: added the argument for why the unmanipulable residual specifically needs its own instrumented coverage, not just an assumed leftover.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (grounded corpus search over `topics/corpus/ideas.jsonl`, one non-corpus canonical anchor independently verified). No landscape-only mentions are padded in.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation → sub-problem it will motivate):

| work_id | citation | is_potential_baseline | limitation |
|---|---|---|---|
| `rw_prefeval` | Anon., PrefEval (OpenReview:QWunLKbBGF) | false (soft-only, no hard arm) | Measures soft-preference decay via distractor-padded long conversations, but has no hard-norm comparison arm and doesn't factorially manipulate wording/position/repetition — documents soft-constraint failure, not its mechanism. |
| `rw_offtopiceval` | Anon., OffTopicEval (OpenReview:EcIyiJrajc) | false (query-type variation, not longitudinal decay) | Measures accept/refuse tradeoff for policy-conditioned agents across query types (in-domain / out-of-domain / laundered), not decay of adherence over repeated turns. |
| `rw_safedialbench` | Anon., SafeDialBench (OpenReview:KFjtRqVnKH) | false (adversarial-only, hard-norm only) | Scores hard-safety consistency under seven jailbreak strategies; no soft-policy arm, no benign (attack-free) decay measurement to compare against. |
| `rw_timetoinconsistency` | Anon., TimeToInconsistency (OpenReview:88C7vSdn0t) | **true** | Models turn-level hazard of first inconsistency with *observational* semantic-drift covariates; predicts when failure happens but never intervenes on wording, position, or repetition, so its hazard model cannot separate salience from framing from prior — correlational decay modeling, not causal mechanism attribution. `lim_timetoinconsistency_correlational`. |
| `rw_sinktrack` | Anon., SinkTrack (OpenReview:Gg1aPETCL6) | false | Presupposes positional salience loss as *the* mechanism of instruction forgetting and builds a mitigation for it; never tests whether constraint type or alignment prior modulates decay under the same positional disadvantage. |
| `rw_safetyfewtokensdeep` | Anon., SafetyFewTokensDeep (OpenReview:6Mxhg9PtDE) | **true** | Characterizes the alignment prior's depth via per-token KL between aligned and base models, but only for hard-safety refusals against adversarial exploits; its unit of analysis is token depth within one response, not turn-level decay of an in-context-injected soft policy. `lim_safetyfewtokensdeep_narrow_unit`. |
| `rw_tare` | Anon., TARE (OpenReview:YEBDvqsniH) | false | Measures wording/paraphrase sensitivity as *point-wise*, single-shot robustness of a task prompt; doesn't study whether wording strength modulates the *longitudinal* durability of a constraint over a long interaction. |
| `rw_icfbench` | Anon., ICFBench (OpenReview:hcJywRYc3n) | **true** | Tests suppression of *revoked* context (forgetting that should happen) via a paired NoForget/Forget design — the opposite failure direction from unintended decay of a still-valid constraint — and doesn't distinguish constraint types by stakes or prior. |
| `rw_recast` | Anon., RECAST (OpenReview:90tCp2KszA) | false | Its dual-mode (rule + judge) verifier taxonomy is reusable machinery, but RECAST's own contribution is many-constraint instruction-data synthesis, not decay measurement — no reputation/decay dimension exists in its design. |
| `rw_llmsgetlost` | Laban et al., 2025 (arXiv:2505.06120) | false (canonical anchor, not a runnable baseline) | Establishes large-scale multi-turn performance degradation (aptitude loss vs. unreliability), but doesn't stratify degradation by constraint type or manipulate salience/framing/prior — the asymmetry itself is invisible to its design. |

**critique:**
- summary: Grounding is solid and every limitation is specific, not generic, but one baseline label overclaims comparability in the same way a mismatched-I/O work always does.
- comments:
  - `{severity: major, field: "specific_related_works[rw_icfbench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "ICFBench's paired design tests suppression of revoked context — the opposite failure direction from this paper's unintended decay of a still-valid constraint. Marking it a straightforward baseline risks implying ICFBench's own reported forgetting-suppression numbers are being compared against, which they never are; per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.'"}`
- decision: `move_to_refiner` (a wording-precision fix — the paired causal-isolation *structure* is still legitimately borrowable as a design template).

### Refiner pass

- `rw_icfbench.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — ICFBench's own reported forgetting-suppression rates are not compared against. Its paired NoForget/Forget causal-isolation *structure* is borrowed as the design template for the within-/between-conversation reactivity calibration, independent of its published findings."
- `changes_made`: clarified ICFBench's baseline role to avoid an implied I/O-mismatched comparison, mirroring the same fix pattern the exemplar run applied to its own structurally-borrowed-not-compared work.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The measurement-validity concern closest to a framing-tier candidate — `lim_timetoinconsistency_correlational` ("its hazard model cannot separate salience from framing from prior") — is not itself promoted to a framing-tier RQ, because the reactivity-calibration question it might suggest is already covered end-to-end as a mechanism-tier hypothesis at Stage 5/6 (targeting the sub-problem below, not this limitation). Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4):

- **`sp_confound_orthogonalization`** — *description:* Orthogonalize a naturally confounded triple: in ecological deployment, hard safety norms are simultaneously stated more imperatively, placed more prominently, and reinforced more heavily during alignment training than soft policies. *why_it_is_a_problem:* without intervention, any observed soft/hard decay gap is uninterpretable — it could trace to any one of the three factors or their interaction, and correlational analysis (as in `rw_timetoinconsistency`) cannot separate them. *technical_challenge:* the three factors are causally intertwined in the wild; only intervention on content-matched pairs, holding each factor independently controllable, can decompose their joint contribution — and even then the third factor (alignment prior) cannot be directly manipulated, only proxied. *source_limitation_ids:* `["lim_timetoinconsistency_correlational"]`.
- **`sp_reactivity_confound`** — *description:* Separate genuine constraint decay from measurement-induced salience refresh caused by the act of probing itself. *why_it_is_a_problem:* a probe that exercises the constrained behavior implicitly re-mentions its topic, refreshing salience — the measurement instrument may be perturbing the very quantity it measures, and if this refresh differs by constraint type, every downstream mechanism attribution is contaminated. *technical_challenge:* authoring probes that never mention the constraint or its topic keywords reduces but cannot provably eliminate reactivity; the residual can only be bounded by a between-conversation design that is itself expensive (one conversation consumed per probe point). *source_limitation_ids:* `["__novel__"]` (no cited work targets probe-induced reactivity for constraint-decay measurement; ICFBench's paired design is structurally adjacent but targets the opposite phenomenon).
- **`sp_matched_pair_construction`** — *description:* Construct soft/hard constraint pairs matched on everything except type, despite soft policies being naturally graded (tone, scope, style) and hard norms naturally binary (refuse/comply). *why_it_is_a_problem:* an unmatched pair turns the claimed type contrast into a difficulty/verifiability contrast — "soft rots faster" could just mean "harder, fuzzier tasks fail sooner," a different and less interesting finding. *technical_challenge:* matching requires simultaneously controlling topic domain, token length, and verifier class, while preserving genuinely different compliance semantics — over-matching risks artificial pairs, under-matching risks confounding type with difficulty. *source_limitation_ids:* `["__novel__"]` (no cited work constructs soft/hard matched pairs at all; `rw_prefeval` and `rw_safedialbench` each instrument one type only).
- **`sp_prior_proxy_triangulation`** — *description:* Estimate the alignment/pretraining prior's contribution to constraint durability despite this mechanism being fundamentally unmanipulable at inference time. *why_it_is_a_problem:* a constraint's alignment-training reinforcement is baked into the weights before the study begins, so without a credible proxy this third candidate mechanism is un-investigable, and any "residual" attributed to it is really just unexplained variance. *technical_challenge:* no single proxy is unconfounded with model family, scale, or training recipe; triangulating with multiple imperfect instruments yields, at best, an upper bound on what correlational adjustment can claim, never a causal estimate. *source_limitation_ids:* `["lim_safetyfewtokensdeep_narrow_unit"]`.

**critique:**
- summary: Coverage is clean (solving all four jointly would deliver Stage 1's objective) and each is method-free, but one sub-problem's technical challenge silently folds together two different kinds of matching that fail in different ways.
- comments:
  - `{severity: minor, field: "sp_matched_pair_construction.technical_challenge", anti_pattern: null, comment: "The challenge folds covariate matching (topic domain, token length, verifier class — checkable at construction time) together with outcome matching (turn-1 baseline adherence parity, per paper.md Step 5's own 'matched' definition — only checkable after a pilot run). These fail differently: a covariate mismatch is a construction-time authoring error; an outcome mismatch can only be caught by piloting and may force dropping pairs post hoc. Worth making the two-step audit explicit rather than treating 'matching' as one monolithic check."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_matched_pair_construction.technical_challenge` sharpened to end with: "...covariate matching (topic domain, token length, verifier class) is checkable at authoring time; but even covariate-matched pairs may not be equally easy for the model, so a second, only-checkable-after-piloting criterion — turn-1 baseline adherence within a small tolerance — is also required, and pairs failing either check must be dropped or the type contrast risks being a difficulty contrast in disguise."
- `changes_made`: made the two-step (construction-time vs. pilot-time) matching audit explicit.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; 2 sourced from related-work limitations, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_matched_pair_bank_construction`** → targets `sp_matched_pair_construction`. *proposed_approach:* Author 20 (pilot) / 40 (scale-up) soft/hard constraint pairs matched on topic domain, token length (±10%), and verifier class, each in 3 wording-strength variants (advisory/standard/imperative) checked for semantic equivalence (embedding similarity ≥ 0.90 plus human audit); run a pilot audit dropping any pair whose turn-1 baseline adherence differs by more than 5 points between its soft and hard member. *key_insight:* covariate matching alone cannot guarantee equal task difficulty, so treating turn-1 adherence parity as a second, empirically-checked matching criterion — not an assumption — is what keeps the eventual type contrast interpretable as a type effect rather than a difficulty effect. *hypotheses:* ["At least 80% of constructed pairs will survive both the covariate-matching construction criteria and the turn-1 baseline-adherence audit (≤5-point difference) without requiring re-authoring."]
- **`m_orthogonal_manipulation_harness`** → targets `sp_confound_orthogonalization`. *proposed_approach:* Cross wording strength × context position × repetition count orthogonally within each constraint type, holding total context token count constant across cells via length-matched filler, and fit a mixed-effects discrete-time hazard model (`hazard ~ turn × type × wording × position × repetition + pair/model random effects`) whose `type×turn` coefficient is the target gap. *key_insight:* a single fitted model yields, from one specification, both the overall gap estimate and a dominance/partial-R² decomposition of that gap across the three manipulated factor blocks — orthogonal crossing is what makes the decomposition interpretable rather than a post hoc correlation. *hypotheses:* ["At least one manipulated factor block (wording, position, or repetition) shows a statistically significant factor×type×turn interaction at Holm-Bonferroni-corrected α=0.05.", "The manipulated factor blocks (salience + framing) jointly absorb more than 50% of the type×turn gap coefficient's partial-R², rather than the majority of the gap surviving unexplained by any manipulated factor."]
- **`m_boosted_soft_contrast`** → targets `sp_confound_orthogonalization`. *proposed_approach:* Construct a specific "boosted-soft" cell (imperative wording + system-head position + repetition 5) and contrast its fitted half-life against both the standard-soft and standard-hard cells, computing the fraction of the log-half-life gap recovered (`κ_close`). *key_insight:* the partial-R² decomposition above tells you how much of the *observed, average* gap tracks manipulated factors, but the practically decisive question — how close does maximally boosting a soft policy's presentation actually get to hard-norm durability? — needs a specific, pre-registered contrast cell, not an average partial effect. *hypotheses:* ["The boosted-soft cell achieves gap closure κ_close ≥ 0.5 (bootstrap 95% CI lower bound > 0.25) while its half-life remains statistically distinguishable from the standard-hard cell (half-life-ratio CI excludes 1) — presentation narrows but does not eliminate the gap."]
- **`m_prior_proxy_battery`** → targets `sp_prior_proxy_triangulation`. *proposed_approach:* Measure three proxies per constraint — no-injection zero-shot compliance rate, base-vs-instruct compliance delta on an open-weights model pair, and (where weights are accessible) per-token KL divergence on the constraint-violating continuation — entered as covariates, never manipulated factors, in the same hazard model. *key_insight:* because the prior cannot be intervened on directly, triangulating with three imperfect, differently-biased instruments and checking they agree (non-flat, positively correlated) is what distinguishes a real residual-mechanism signal from proxy noise masquerading as one. *hypotheses:* ["The prior-strength proxies (no-injection compliance rate and base-vs-instruct compliance delta) have standard deviation greater than 0.1 and Spearman correlation greater than 0.3 with each other across constraints, indicating shared, non-degenerate signal rather than uninformative or contradictory readings."]
- **`m_reactivity_calibration`** → targets `sp_reactivity_confound`. *proposed_approach:* Run a calibration subsample where each conversation is probed exactly once at a randomly assigned turn (between-conversation design) rather than every 5 turns (within-conversation design), on a small set of pilot-flagged cells, and compare the fitted hazard curves between the two probing regimes via an equivalence test on the probing-regime × type interaction. *key_insight:* an anti-reactivity probe-authoring rule reduces but cannot provably eliminate salience refresh; the only way to bound the residual is to measure it directly against a design that structurally cannot suffer from it, and to check specifically whether the residual is uniform across constraint types — if not, the main design's attribution is invalid, not just noisy. *hypotheses:* ["The 95% CI of the probing-regime × type interaction hazard ratio lies entirely within [0.80, 1.25] (equivalence bound), indicating probe reactivity — whatever its magnitude — does not differentially bias the soft/hard comparison the main design relies on."]

**critique:**
- summary: Every method has a real mechanism and every hypothesis names a threshold, but `m_boosted_soft_contrast` is questionable as a *separate* method rather than a second readout of the model already fit in `m_orthogonal_manipulation_harness`.
- comments:
  - `{severity: major, field: "m_boosted_soft_contrast", anti_pattern: "mismatch (borderline goal_restatement)", comment: "Both m_orthogonal_manipulation_harness and m_boosted_soft_contrast fit and read off the same mixed-effects hazard model over the same factorial design — the 'boosted-soft cell' is a specific slice of the model already specified above, not a new instrument. Presenting it as a fifth, independent method risks reading as two methods for the price of one mechanism. Either justify explicitly why this is a distinct design decision (a specific pre-registered contrast vs. an average partial-R² decomposition are different statistical objects even from one fit), or merge them."}`
- decision: `move_to_refiner` (the fix is a merge-with-justification, not new content — the mechanism and hypotheses are already sound).

### Refiner pass

- `m_boosted_soft_contrast` merged into `m_orthogonal_manipulation_harness` as its third hypothesis, with `key_insight` extended: "...a single fitted hazard model licenses two distinct, separately falsifiable readouts without being two mechanisms: an *average* partial-R² decomposition of the type×turn gap across factor blocks (tests whether manipulated factors matter on average), and a *specific*, pre-registered contrast at one boosted-presentation cell against standard-soft and standard-hard (tests the practically decisive question of how far maximal boosting actually closes the gap). One instrument, two estimands, not two mechanisms — the same justification structure the calibration exemplar used for its own two-hypothesis method."
- `changes_made`: merged the two methods into one (`m_orthogonal_manipulation_harness`, now carrying 3 hypotheses), with the one-instrument-two(-now-three)-estimands justification made explicit rather than left implicit.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **6 hypotheses total** (1 + 3 + 1 + 1 across `m_matched_pair_bank_construction`, `m_orthogonal_manipulation_harness`, `m_prior_proxy_battery`, `m_reactivity_calibration` respectively), mixing instrument-validity claims (pair-construction survival rate, proxy signal validity, reactivity equivalence) with the study's headline empirical predictions (interaction significance, partial-R² share, boosted-cell gap closure) — a deliberate design choice for an `empirical` study_type, explained in the Stage 6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- LMSYS-Chat-1M — *justification:* real, large-scale conversational distractor pool needed to pad long-horizon conversations realistically without hand-authoring filler; this is the exact padding protocol `rw_prefeval` already validated for the same purpose, reused here rather than invented fresh.
- IFEval — *justification:* provides rule-checkable instruction-constraint templates, needed for the rule-verifiable subset of the constraint-pair bank that both RQ2/RQ3's cleanest cells and the difficulty-artifact sanity check depend on (graded judge-based verifiers alone would confound "soft decays faster" with "judge-scored constraints decay faster").
- HEx-PHI and AdvBench — *justification:* standard, named hard-norm probe-request taxonomies, needed to instantiate the "hard" side of matched pairs with established harmful-instruction categories rather than inventing ad hoc ones whose severity calibration would itself need justifying.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- No-injection floor arm — identical harness with the constraint statement never injected; establishes that turn-1 adherence is caused by injection at all, so "decay" means regression toward a measured no-constraint floor, not toward zero from an undefined starting point.
- No-manipulation natural-wording replication arm (standard wording, sys-head, repetition 1) — the first, necessary check of whether the ~8x-style premise gap even replicates in matched pairs, independent of any of the manipulated-factor claims below (tests Assumption A1 before anything else is asked of the design).
- Naive every-k-turn verbatim-restatement heuristic — a mitigation practitioners already use informally with no theoretical grounding; checks whether the study's own repetition-factor findings are at least consistent with what ad hoc practice already does.
- SinkTrack-style training-free context anchoring (open-weights models only) — the one prior method in the related-work set that treats positional salience as *the* operative mechanism; an informative sanity comparator for whether a competing salience-only intervention produces a similar or different effect size than this design's own position/repetition manipulation.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_pair_bank_survival` | `sp_matched_pair_construction` | "At least 80% of constructed pairs will survive both the covariate-matching construction criteria and the turn-1 baseline-adherence audit (≤5-point difference) without requiring re-authoring." |
| `rq_factor_significance` | `sp_confound_orthogonalization` | "At least one manipulated factor block (wording, position, or repetition) shows a statistically significant factor×type×turn interaction at Holm-Bonferroni-corrected α=0.05." |
| `rq_manipulated_share` | `sp_confound_orthogonalization` | "The manipulated factor blocks (salience + framing) jointly absorb more than 50% of the type×turn gap coefficient's partial-R², rather than the majority of the gap surviving unexplained by any manipulated factor." |
| `rq_boosted_closure` | `sp_confound_orthogonalization` | "The boosted-soft cell achieves gap closure κ_close ≥ 0.5 (bootstrap 95% CI lower bound > 0.25) while its half-life remains statistically distinguishable from the standard-hard cell (half-life-ratio CI excludes 1) — presentation narrows but does not eliminate the gap." |
| `rq_prior_proxy_signal` | `sp_prior_proxy_triangulation` | "The prior-strength proxies (no-injection compliance rate and base-vs-instruct compliance delta) have standard deviation greater than 0.1 and Spearman correlation greater than 0.3 with each other across constraints, indicating shared, non-degenerate signal rather than uninformative or contradictory readings." |
| `rq_reactivity_equivalence` | `sp_reactivity_confound` | "The 95% CI of the probing-regime × type interaction hazard ratio lies entirely within [0.80, 1.25] (equivalence bound), indicating probe reactivity — whatever its magnitude — does not differentially bias the soft/hard comparison the main design relies on." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3 and walking-skeleton numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but the RQs are listed as if independent when one of them structurally gates the validity of three others.
- comments:
  - `{severity: major, field: "research_questions (execution order)", anti_pattern: "not a named rubric anti-pattern, but a real omission: setup specificity requires the sequencing that makes the RQs jointly interpretable", comment: "rq_reactivity_equivalence tests exactly the assumption (probe reactivity is type-uniform) that rq_factor_significance, rq_manipulated_share, and rq_boosted_closure all silently rely on — if reactivity turns out to be type-dependent, the within-conversation hazard estimates those three RQs use are differentially biased, not just noisy. paper.md's own Step 6 flags this explicitly ('RUN FIRST — gates E1/E2'), but nothing in the current draft states that rq_reactivity_equivalence must be evaluated before the other three RQs' results are treated as trustworthy. Listing all six RQs as a flat, order-independent set risks a reader (or a future experimenter) running the headline analyses before the calibration check that licenses them."}`
- decision: `move_to_refiner`.

### Refiner pass

- Added an explicit **Execution order** note to the confirmed Stage 6 output: "`rq_reactivity_equivalence` must be evaluated first, on the calibration subsample, before `rq_factor_significance`, `rq_manipulated_share`, or `rq_boosted_closure` are treated as trustworthy. If the equivalence test fails (the interaction CI extends outside [0.80, 1.25]), the three gated RQs must be rerun on the reactivity-free between-conversation design, or their scope explicitly narrowed, before any mechanism-attribution claim is reported."
- `changes_made`: made the RQ dependency structure explicit rather than leaving it implicit in each RQ's own setup description.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage (`m_boosted_soft_contrast` was merged, not renamed-and-orphaned — its hypothesis and target survive intact inside `m_orthogonal_manipulation_harness`).
3. **Reference integrity** — `sp_confound_orthogonalization.source_limitation_ids = ["lim_timetoinconsistency_correlational"]` ∈ Stage 3 limitations ✓; `sp_prior_proxy_triangulation.source_limitation_ids = ["lim_safetyfewtokensdeep_narrow_unit"]` ∈ Stage 3 ✓; the other two sub-problems' `["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (per-turn adherence, survival curves/half-lives, variance decomposition) are each reachable: adherence measurements + curves via `sp_matched_pair_construction` + `sp_confound_orthogonalization`, the residual/prior share via `sp_prior_proxy_triangulation`, and the entire chain's validity via `sp_reactivity_confound` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.
6. **Hypothesis↔RQ recount:** 6 hypotheses at Stage 5 (1 pair-construction + 3 orthogonal-harness/boosted-contrast + 1 prior-proxy + 1 reactivity) → 6 mechanism-tier RQs at Stage 6, one-to-one, verbatim. 0 framing-tier, 0 outcome-tier. Counts match exactly.

**What was hardest:** unlike a typical fresh idea, the seed material (`paper.md`) had *already* run its own asymmetry/taste self-check (Step 0/3) and a full pre-registration (Steps 5–9) — so the recurring tension was **not** disagreement about facts but **scope discipline**: repeatedly checking whether a Stage-5/6 hypothesis was quietly restating `paper.md`'s own already-finished experiment design rather than adding something this schema's structure specifically demands (e.g., the pair-construction survival-rate hypothesis and the execution-order note, both of which `paper.md`'s Assumptions/Step-6 gesture at operationally but never state as a standalone, falsifiable claim in their own right).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: fold-in pass over `stage_review.md` (5-stage review + Phase A re-run) and `taste_audit.md` against the current deliverables. Historical rounds above are untouched. Note on the interrupted prior attempt: an earlier revision agent was killed early; its only surviving partial work was the B-alt baseline sentence already present in `paper_draft.md`'s Baselines paragraph but not yet mirrored into `paper_draft.tex` — completed below (item 12). No duplicate sections or Phase Log rows existed.

1. **stage_review.md → Stage 2 REVISE (missing nearest-neighbor sentence in Related Work)** → verified already applied: nearest-neighbor sentences naming PrefEval and TimeToInconsistency with the explicit delta are present in `paper_draft.md` (Intro ¶3 and Related Work opening) and `paper_draft.tex` (lines 42, 208). No change needed.
2. **stage_review.md → Stage 4 REVISE (RQ6-gates-RQ2/3/4 buried in RQ6's subsection)** → verified already applied: an "Execution order." paragraph precedes the RQ list in both `paper_draft.md` and `paper_draft.tex`, and RQ6's own heading carries the "(evaluated first — gates RQ2, RQ3, and RQ4)" reminder; `experiment_design.md` has the matching "Execution order" section. No change needed.
3. **stage_review.md → Phase A item 2 REVISE (reference-cache integrity: 10 N3 keys absent)** → verified already applied in `reference_candidates.jsonl` (160 records, 15 selected, no `pending`). The residual null `pdf_path`/`digest_path` for the 10 added records remains the explicitly disclosed follow-up for a future harvest pass — logged, not blocking, per the review's own disposition.
4. **stage_review.md → Phase A item 5 REVISE (assumptions table merged three §3.2 slots)** → verified already applied in `../paper.md`: A1–A8 restructured into five explicit columns with named gates PG-1…PG-8 and per-assumption consequences.
5. **stage_review.md → Phase A item 6, item 1 (missing R1 estimand sentence)** → verified already applied: "Estimand (R1, guidance.md §3.4)" sentence opens `../paper.md` Step 5 (quantity + unit of analysis + reference population + decision fed, in one sentence).
6. **stage_review.md → Phase A item 6, item 6 (incomplete R2 instrument-validation plan)** → verified already applied: full five-step (①–⑤) R2 subsection for the M3 verifier sits under the Assumptions table in `../paper.md`, externally grounded via `AdversarialPragmaticsAI2607`.
7. **stage_review.md → Phase A item 6, item 9 (no per-cell power / thin-cell rule)** → verified already applied: pre-declared thin-cell rule (INCONCLUSIVE, never null, never silently dropped; collect-more/narrow/stop ladder) is in `../paper.md` Step 6; `experiment_design.md` RQ2's sample-size rationale restates the per-cell INCONCLUSIVE marking.
8. **stage_review.md → Phase A item 1 minor observation (t3/t4/CO2 defined in digest.md but never re-cited by literal id in paper.md)** → rejected — the review itself classifies this as "a labeling thinness, not a broken reference," with the content covered under equivalent framing (A4/A6, H1); no fix was requested.
9. **stage_review.md → Phase A item 6 advisory (paper.md Step 2 could optionally name the E2 boosted-soft cell as an A4-style counterfactual)** → rejected — explicitly optional per the review ("nothing is missing evidence-wise"); adding it would introduce new framing content beyond what the review asks for.
10. **stage_review.md → Phase A item 6 stylistic note (not every design constraint uses the literal "X removes confound Y" template)** → rejected — marked "stylistic, non-blocking" by the review; the confounds are substantively named.
11. **taste_audit.md → forward caution (verdict flips to 🟡 if Related Work/Method drifts to "we combine PrefEval's protocol and TimeToInconsistency's model" as headline framing)** → checked at draft level as the audit requested: both nearest-neighbor sentences frame the pair as delta-and-differentiate ("neither compares soft against hard constraint decay within one matched, causally interventional design"), and no combine/integrate/unify verb appears in a claim position in Abstract, Intro, or Method. Verdict remains 🟢; no change needed.
12. **Cross-deliverable consistency check (this pass)** → one mismatch found and fixed: the B-alt strongest-alternative-explanation control was present in `experiment_design.md` (Baselines, with provenance note) and in `paper_draft.md`'s Baselines paragraph, but missing from `paper_draft.tex`. Mirrored the sentence into the tex Baselines paragraph and recompiled (`latexmk -pdf`; clean, 12 pages, `paper_draft.pdf` regenerated). All other cross-checks pass: 6 mechanism-tier RQs in both `paper_draft.md` and `experiment_design.md` (0 framing, 0 outcome); the six `target_hypotheses` in `experiment_design.md` are byte-identical to Stage 5/6's confirmed strings above; effect floors and margins match across deliverables (interaction hazard ratio 1.5 at ≥80% power, α=0.05 Holm-Bonferroni; κ_close ≥ 0.5 with bootstrap 95% CI lower bound > 0.25, 10,000 resamples; TOST equivalence bounds [0.80, 1.25]; ≈960 conversations/model pilot, n=60/cell; ≈480-run calibration subsample).

**Result:** 12 findings enumerated — 7 verified already applied (items 1–7), 1 applied this pass (item 12's tex mirror + recompile), 3 rejected as advisory/non-blocking per the reviews' own dispositions (items 8–10), 1 verified-no-drift check (item 11). No hypothesis wording, thresholds, or citations were altered.
