# Auto-Research-Discussion Run — B3.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> **This file is the complete Stage 1–6 discussion trace**, extracted verbatim from `pipeline.md` (which retains only a pointer to this file plus its own Phase Log / goal.md run-state section). See `experiment_design.md` for Stage 6's standalone, executable experiment spec, and `paper_draft.md`/`.tex`/`.pdf` for the assembled paper.
>
> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B3.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries a formal Step-5 notation table, Steps 0/3 asymmetry and taste self-checks, and Step 6 pre-registered hypotheses with fallbacks), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure what fraction of a fixed library of production-style structured-output contracts (JSON-schema conformance targets, machine-checkable formatting conventions, few-shot prompt templates) newly fail after a provider-side LLM version upgrade, in excess of within-version sampling noise, and identify which contract-level features predict this fragility.
- **Apparent inputs:** a constructed contract library (prompt template + input distribution + deterministic acceptance predicate, each carrying a pre-registered feature vector); sequences of individually addressable, successive LLM versions (dated closed-API snapshots and archived open-weight checkpoints); a deterministic pass/fail validator per contract.
- **Apparent outputs:** a per-version-transition, noise-floor-adjusted breakage rate (overall and per contract type); a fitted fragility predictor model (odds ratios + predictive AUC); an estimate of how much breakage two mitigations (constrained decoding, prompt recompilation) remove.
- **Closest research areas:** LLM behavioral-drift / endpoint monitoring (ChatGPTDrift, LogProbTracking); instruction-following constraint verification (RECAST, AutoIF, IFEval/FollowBench); input-side prompt robustness (CoIPO, TARE); constrained decoding (DiffusionCFG); declarative prompt compilation (DSPy); longitudinal drift-benchmark methodology (LAMDA); weight-space version fragility (CAR-LoRA).
- **In scope:** measuring breakage of a constructed contract library against pinned, successive real model versions. **Out of scope:** training or fine-tuning new models; live/non-sandboxable production monitoring deployments; claiming a general theory of why models drift (this is a measurement study of the downstream consequence, not a study of the drift mechanism itself).
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest + pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste check (`paper.md` Step 0/3, which explicitly rejects a "we connect drift-detection to downstream contracts" bridge framing). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 5/6, which is why stages 5/6 below are framed as surfacing the measurement instrument's own validity properties (validator calibration, version-addressability, cheap-signal specificity) rather than re-deriving `paper.md`'s three headline hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed library of production-style structured-output contracts — each a (prompt template, input distribution, deterministic acceptance predicate) triple — and given sequences of individually addressable, successive versions of one or more LLM APIs and open-weight model families, determine what fraction of contracts that passed under a prior version newly fail under the next version, after subtracting a within-version resampling noise floor, and identify which contract-level features (schema nesting depth, constraint density, few-shot example count, ...) predict this breakage.
- `input`: (1) a contract library with a pre-registered feature vector per contract; (2) sequences of pinned, individually re-queryable versions; (3) a deterministic pass/fail validator per contract; (4) a fixed sampling budget (n=20 draws per contract-version pair).
- `output`: (1) a per-version-transition breakage rate B(v→v′), overall and per contract type, reported against its within-version noise floor B_null; (2) a fitted fragility predictor model (odds ratios + cross-family predictive AUC); (3) an estimate of how much of the measured breakage two existing mitigations (grammar-constrained decoding, per-version prompt recompilation) remove.
- `constraints`: the contract library must have a mechanically checkable, non-subjective ground truth for pass/fail; every claim of "breakage" must be reported as an excess over the within-version noise floor, not a raw flip count.
- `objective`: a breakage-rate claim is accepted only if it significantly exceeds the within-version noise floor under a paired test; a feature is accepted as a fragility predictor only if its odds ratio survives multiple-comparison correction and the fitted model retains above-chance predictive AUC on a held-out model family.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 and `paper.md` Step 2 already settle this as a measurement/characterization study ("Primary: Measurement / audit study"), not a proposed fix being pitted against baselines.

**critique:**
- summary: Strong, evidence-traceable draft with a genuinely evaluable objective — but the objective is silent on a real dependency between its two outputs, and the constraints list omits a boundary condition the seed material itself already flags.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective states acceptance criteria for the breakage rate and for the fragility predictors as if they were independent claims, but paper.md's own Step 6 RQ2 assumption states the fragility question is conditional: 'RQ1's phenomenon existing (else fragility is undefined).' If no version transition shows breakage in excess of the noise floor, asking 'which features predict breakage' is not merely unanswered — it is not a well-posed question at all under this objective. As written, a reader can't tell what the objective says should happen to the second claim if the first one comes back null."}`
  - `{severity: minor, field: "constraints", anti_pattern: null, comment: "Constraints require versions to be 'individually addressable and re-queryable' but say nothing about what happens when that fails — and digest N6's own feasibility section names exactly this failure mode as the single biggest risk ('closed-API historical snapshots being deprecated mid-study... changing silently'). A problem statement that requires addressability without naming what happens when it's violated leaves that boundary condition implicit rather than stated."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A breakage-rate claim for a given version transition is accepted only if B(v→v′) significantly exceeds the within-version noise floor B_null under a paired test; a contract feature is accepted as a fragility predictor only if its odds ratio survives multiple-comparison correction and the fitted model retains above-chance predictive AUC on a held-out model family — **and this second claim is conditional on the first**: if no tested transition shows breakage in excess of B_null, the fragility-predictor question is reported as *not answerable under this design* (fragility of a phenomenon that isn't shown to exist), not silently tested anyway."
- `constraints` (extended): "...; version addressability is treated as a graded property, not a binary precondition — closed-API dated snapshots are individually addressable only for the duration they remain undeprecated and unchanged, which the design cannot guarantee, so primary claims are anchored on permanently re-queryable open-weight checkpoints and closed-API results are reported as a secondary, addressability-bounded arm."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5 notation): "Contract c = (T, D, A): template T, input distribution D, deterministic acceptance predicate A. Version lineage L = (v_0,...,v_k). For (c,v), draw n=20 i.i.d. samples, p̂(c,v) = pass fraction. c passes at v iff p̂≥0.9, fails iff p̂≤0.5 (indeterminate band excluded from the primary statistic). Breakage rate B(v→v′) = |{c: pass@v ∧ fail@v′}| / |{c: pass@v}|; noise floor B_null(v) computed by the identical procedure over a within-version split-half. Determine, for each L, whether ΔB = B(v→v′) − B_null is significantly positive, and which components of c's feature vector predict per-contract breakage."
- `changes_made`: made the RQ2-depends-on-RQ1 conditional explicit in `objective`; turned addressability into a graded, explicitly-bounded constraint rather than an unstated binary assumption; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Production software increasingly delegates structured-output correctness — the thing downstream code actually parses — to a model version the contract owner cannot pin or fully observe, and provider-side model upgrades are frequent and only loosely documented, but how much of this contracted behavior actually survives a version jump has never been directly measured.
- `why_it_matters`: When a provider upgrades the underlying model, any silent shift in the model's tendency to honor a structured-output contract can break downstream code with zero change on the application side — teams currently learn about this reactively, from their own production incidents, rather than from a number they could check before adopting a new version. This matters specifically because endpoints are documented to drift (ChatGPTDrift's snapshot comparisons; LogProbTracking's framing of endpoint-change detection as an open monitoring problem) and prompt templates are documented to be wording-fragile (DSPy's own motivation: hand-written templates are "brittle" and "do not transfer cleanly across tasks or models") — but neither premise, on its own, tells anyone the *downstream* consequence: what fraction of contracts actually break, and by how much this exceeds ordinary sampling noise.
- `who_cares`: Engineering teams maintaining LLM-integrated production pipelines who must decide whether to adopt a new model version; providers deciding how much backward-compatibility testing to run before releasing an upgrade; researchers building longitudinal LLM-drift benchmarks who need a downstream-consequence metric, not just an endpoint-change detector.
- `evidence`: `[ChatGPTDrift, arXiv:2307.09009]` documents large, task-dependent behavior and format-compliance shifts between GPT-3.5/GPT-4 snapshots; `[LogProbTracking, OpenReview:hFxivbAgVP]` treats "detection of whether an endpoint's response distribution has changed" as a live, unsolved monitoring problem; `[DSPy, OpenReview:sY5N0zY5Od]` asserts hand-written prompts are brittle and don't transfer across models, offering recompilation as an unquantified fix. No paper in a corpus of 11,683 combines a constructed contract library, a validator, and a longitudinal version-transition design (digest N3 search-honesty note) — itself evidence the downstream number is genuinely unmeasured, not just underreported.

**critique:**
- summary: The stakes for the headline breakage-rate claim are concrete and well-cited, but the motivation doesn't yet explain why the *other two* stage-1 outputs — the fragility predictors and the mitigation-headroom estimate — matter in their own right, as opposed to being incidental byproducts of measuring the rate.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 promises three outputs: the noise-adjusted rate, a fragility predictor model, and a mitigation-headroom estimate. why_it_matters only motivates the first ('teams learn about breakage reactively... rather than from a number they could check'). It never argues why *knowing which contract features predict fragility* is independently valuable — e.g., for prioritizing regression testing — nor why *bounding how much breakage is avoidable* by existing mitigations matters as a deployment decision, as opposed to an inherent cost of upgrading. Without this, a reader could ask 'why not just report one overall rate number and stop there' — a real, unaddressed gap, since digest N0's own abstract independently promises exactly this prioritization angle without it appearing in the motivation proper."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a single pooled rate is not actionable by itself: a team cannot decide *which* of their hundreds of production contracts to re-test before adopting a new version without knowing which contract-level features predict fragility — schema depth, constraint density, and few-shot count are all knowable from a contract at authoring time, before any model is ever queried, which is what makes a validated predictor model something a team can act on pre-emptively rather than discover post-incident. Separately, whether measured breakage is an *inherent* cost of upgrading or an *avoidable* one changes what a team should actually do about it: if grammar-constrained decoding or prompt recompilation removes most of the measured breakage, the right response is engineering investment in mitigation; if it does not, the right response is treating regression testing as a mandatory, non-skippable release gate. Both downstream decisions require the mitigation-headroom estimate, not just the rate."
- `changes_made`: added the prioritization argument for the fragility-predictor output and the avoidable-vs-inherent argument for the mitigation-headroom output, closing the partial-output-coverage gap.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — the digest's own N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_chatgptdrift` | Chen, Zaharia & Zou, arXiv:2307.09009 | false (single provider, single snapshot pair, no rate) | Documents behavior shifts between two GPT snapshots on a general task suite, but covers one provider and one snapshot pair, on tasks not designed as production contracts — no per-upgrade breakage *rate*, no per-type decomposition, no fragility predictors. |
| `rw_logprobtracking` | Anon., LogProbTracking (OpenReview:hFxivbAgVP) | **true** (as a cheap-signal comparator, not a rate-measuring rival) | Detects *that* an endpoint's response distribution changed; says nothing about *what breaks downstream* — a detectable distribution shift may correspond to 0% or 50% of contracts newly failing, and the method neither quantifies nor predicts which. |
| `rw_coipo` | Anon., CoIPO (OpenReview:TUd3c7Vr1z) | false (input-side perturbation direction) | Studies prompt-wording perturbation with the model held fixed — the exact dual of the upgrade setting (prompt fixed, model varies); its robustness scores cannot be read as upgrade-survival predictions. |
| `rw_tare` | Anon., TARE (OpenReview:YEBDvqsniH) | false | Same input-side/model-fixed direction as CoIPO; optimizes prompts against a semantic-paraphrase neighborhood, not against a future model version. |
| `rw_dspy` | Anon., DSPy (OpenReview:sY5N0zY5Od) | **true** (as a mitigation baseline, not a rate-measuring rival) | Asserts hand-written templates are brittle and don't transfer across models, and offers re-compilation as the fix — but never quantifies the breakage phenomenon itself, so the cost/benefit of recompiling per version is asserted, not measured. |
| `rw_recast` | Anon., RECAST (OpenReview:90tCp2KszA) | false (training-time reward signal, single snapshot) | Builds real programmatic constraint-verification machinery, but deploys it as a training-time reward/filter at a single model snapshot; never applies its verifiers longitudinally across versions of the same model. |
| `rw_autoif` | Anon., AutoIF (OpenReview:cRR0oDFEBC) | false | Same as RECAST — generates verifiable instructions plus executable checkers as training supervision at one snapshot, not as a longitudinal measurement tool. |
| `rw_diffusioncfg` | Anon., DiffusionCFG (OpenReview:7Sph4KyeYO) | false (decoding-time guarantee lineage, not a runnable comparator for this study's harness) | Guarantees schema conformance only when the deployer controls decoding (token-mask/grammar access) for diffusion LLMs specifically; the common production case this paper targets — contracts enforced purely through prompts against a black-box API — gets no guarantee from constrained decoding, and the paper never measures how often unconstrained prompt-level contracts are violated, let alone across versions. |
| `rw_carlora` | Anon., CAR-LoRA (OpenReview:5GimteSrgW) | false | Establishes version-fragility for weight-space downstream artifacts (LoRA adapters degrading when a base checkpoint changes) — a different artifact class from prompt/contract-space fragility, which is where most production LLM integrations live. |
| `rw_lamda` | Anon., LAMDA (OpenReview:1FnCrZtBNQ) | false (methodological template, not a runnable comparator) | Provides the longitudinal-drift-benchmark methodology (consistent representation, temporally structured evaluation) but for Android malware; no analogous temporally structured benchmark exists for LLM contract behavior across model versions. |

**critique:**
- summary: Every limitation is specific and problem-tied (not "scalability issues"-style vagueness), and the two `is_potential_baseline` flags for LogProbTracking/DSPy are correctly scoped as comparators rather than rivals — but one baseline label needs the same scrutiny B5.5's SOTOPIA label needed.
- comments:
  - `{severity: major, field: "specific_related_works[rw_diffusioncfg].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "DiffusionCFG's method is specific to diffusion-based LLMs and CFG–regular-language intersection at the decoder level; this study's open-weight anchor lineages (Llama, Qwen) are autoregressive, not diffusion models. Citing DiffusionCFG as though its actual implementation is directly reusable as the constrained-decoding mitigation arm would be an I/O mismatch — its published method targets a different model family than the one this paper's mitigation arm runs on. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.'"}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the decoding-time-guarantee *concept* is still legitimately borrowable as a mitigation arm's lineage).

### Refiner pass

- `rw_diffusioncfg.is_potential_baseline` set to `false` (unchanged), but the field's accompanying note is sharpened: "Not a baseline or a directly reused implementation — DiffusionCFG's own reported guarantees are diffusion-LLM-specific. Its **decoding-time-guarantee concept** (grammar/token-mask constraints eliminate schema-tier failures by construction) is borrowed as the *conceptual lineage* for this study's grammar-constrained-decoding mitigation arm, implemented instead with an autoregressive-compatible tool (xgrammar/outlines) on the open-weight chains — independent of DiffusionCFG's own published results."
- `changes_made`: clarified DiffusionCFG's role to avoid an implied direct-reuse claim across incompatible model families.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_coipo`/`rw_tare`'s "input-side vs. model-side" duality) is not a distinct framing check but is already covered end-to-end as a mechanism-tier RQ in Stage 6 (the cheap-signal specificity test), sourced directly as a sub-problem in Stage 4 rather than manufactured as a framing-tier RQ. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C4 plus the CoIPO/TARE limitation plus a novel mitigation sub-problem):

- **`sp_ground_truth_definition`** — *description:* Define an objective, automatable pass/fail ground truth for "contract breakage" that is calibrated against what a real downstream parser would actually reject. *why_it_is_a_problem:* every downstream number inherits whatever bias the acceptance predicate has — too strict inflates breakage, too lenient hides it. *technical_challenge:* JSON-schema conformance is mechanically checkable, but formatting-convention adherence and few-shot template-following admit graded compliance (correct fields, reordered keys), so the strict/lenient boundary is a genuine design choice with no ground truth of its own to check against except real parser behavior. *source_limitation_ids:* `["__novel__"]` — problem-inherent to defining breakage at all, not tied to one prior tool's failure.
- **`sp_version_attribution`** — *description:* Attribute an observed behavior change to a specific, citable, replicable version transition. *why_it_is_a_problem:* without this, a measured "breakage" cannot be tied to a version anyone else could re-query to verify. *technical_challenge:* closed-API endpoints can change silently within a named snapshot and get deprecated, so addressability is not guaranteed by simply naming a version string. *source_limitation_ids:* `["__novel__"]`.
- **`sp_noise_confound`** — *description:* Separate genuine cross-version breakage from ordinary within-version sampling/serving nondeterminism. *why_it_is_a_problem:* without this, any observed pass→fail flip rate is unfalsifiable as an "upgrade effect." *technical_challenge:* requires a null model computed by the *identical* pass/fail procedure applied to a within-version partition, not an assumed or externally-sourced noise estimate. *source_limitation_ids:* `["__novel__"]`.
- **`sp_power_collinearity`** — *description:* Identify which contract-level features predict fragility with enough statistical power and without collinearity confounding per-feature claims. *why_it_is_a_problem:* contract features are naturally correlated (deep schemas tend to have more fields and constraints), so naive per-feature correlations would misattribute effects. *technical_challenge:* requires a multivariate model with grouped cross-validation and enough independent version transitions × contract diversity for power, not just a bigger single-family sample. *source_limitation_ids:* `["__novel__"]`.
- **`sp_causal_specificity`** — *description:* Determine whether measured breakage reflects a version-specific effect on this contract, or is fully explained by generic, cheaply-detectable distribution shift / input-side prompt sensitivity already characterized in the literature. *why_it_is_a_problem:* if a $0.01 first-token logprob detector already predicts which contracts will break just as well as the constructed contract library does, the expensive library adds nothing beyond what cheap monitoring already gives. *technical_challenge:* CoIPO/TARE study the *dual* direction (prompt varies, model fixed) and don't measure the upgrade setting; isolating "this contract's specific structure matters" from "the endpoint just changed generally" requires comparing two different signals' predictive power on the same (contract, version) pairs, not asserting the distinction. *source_limitation_ids:* `["lim_coipo_tare_dual"]` (Stage 3: CoIPO + TARE's input-side/model-fixed limitation).
- **`sp_avoidable_vs_inherent`** — *description:* Determine how much of the measured breakage is removable by existing mitigations (grammar-constrained decoding, per-version prompt recompilation) versus an inherent cost of upgrading. *why_it_is_a_problem:* without this, teams cannot decide whether to invest engineering effort in mitigation or simply budget for breakage as a release cost. *technical_challenge:* grammar-constrained decoding only guarantees the schema tier by construction, leaving convention-tier and semantic-envelope failures untouched, so an aggregate single mitigation number would conflate tiers with very different treatability. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all six would jointly deliver stage 1's three outputs), and the ground-truth/noise/attribution/power sub-problems are each genuinely distinct — but two sub-problems both hinge on "ruling out an alternative explanation" and risk reading as the same concern twice.
- comments:
  - `{severity: minor, field: "sp_noise_confound / sp_causal_specificity", anti_pattern: "overlap", comment: "Both are, at a glance, 'is this breakage real or a confound' questions, which can read as the same sub-problem restated. They are genuinely distinct — one is a within-version *sampling-noise* question (would the same version flip pass/fail on its own, at zero temperature drift, purely from resampling?), the other is a between-explanation *causal-specificity* question (even granting the effect is non-noise, is it attributable to this contract's structure and this version change specifically, or would a generic, contract-agnostic distribution-shift detector predict it equally well?) — but the descriptions don't make the distinction sharp enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_noise_confound.technical_challenge` sharpened to end with: "...this is a **sampling-noise** problem — would the identical procedure flip pass/fail on the *same* version, absent any upgrade at all — not a question about what caused a real effect."
- `sp_causal_specificity.technical_challenge` sharpened to end with: "...this is a **causal-specificity** problem distinct from sampling noise — even an effect that clears the noise floor could still be fully explained by a generic, contract-agnostic signal (endpoint-wide distribution shift) rather than this contract's specific structure; ruling that out requires a head-to-head predictive comparison, not just clearing `sp_noise_confound`'s bar."
- `changes_made`: made the sampling-noise-vs-causal-specificity distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 1 sourced from a related-work limitation, 5 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_validator_construction`** → targets `sp_ground_truth_definition`. *proposed_approach:* A three-tier deterministic checker per output — parse tier (does it parse as the expected envelope?), schema tier (`jsonschema` Draft 2020-12 validation), convention tier (regex/rule checkers in the style of AutoIF's executable verification functions and IFEval's rule set); a contract passes iff all applicable tiers pass. Validators are unit-tested against hand-constructed positive/negative example outputs before any measurement run, and the strict/lenient boundary (e.g., trailing prose around a JSON block) is a pre-registered, sensitivity-analyzed design constant. *key_insight:* ground-truth ambiguity can't be resolved analytically, but it can be turned into an explicit calibration exercise against hand labels plus a sensitivity sweep, rather than a hidden design choice asserted by fiat. *hypotheses:* ["Validator-vs-hand-label agreement on a held-out calibration set of positive/negative example outputs is ≥0.95, across all three tiers."]
- **`m_version_paired_harness`** → targets `sp_version_attribution`. *proposed_approach:* Execute the library against pinned, individually addressable versions at fixed decoding settings (n=20 samples per contract-version pair); run a LogProbTracking-style first-token top-k logprob canary beside every collection batch; anchor primary claims on permanently downloadable open-weight lineages (e.g. Llama 2→3→3.1→3.3, Qwen2→2.5→3), treating closed dated snapshots as a secondary, addressability-bounded arm. *key_insight:* addressability failure on closed endpoints can't be fixed retroactively, but it can be *detected* via the canary and structurally sidestepped by anchoring the headline claims on lineages where the addressability assumption holds by construction. *hypotheses:* ["Across the collection window, open-weight anchor lineages trigger zero canary-flagged re-collection events, while at least one closed-API dated-snapshot chain triggers at least one — i.e., the addressability risk this design anchors around on open-weight chains is not a hypothetical one."]
- **`m_noise_floor_estimator`** → targets `sp_noise_confound`. *proposed_approach:* For each version, split the 20 samples per contract into two disjoint 10-sample halves and run the identical breakage-computation pipeline between the halves as if they were two "versions," yielding the pseudo-breakage rate B_null; claim upgrade-induced breakage only where B(v→v′) significantly exceeds B_null under a paired, BH-corrected test. *key_insight:* applying the *identical* measurement operation to a within-version partition and a cross-version partition is what turns "is this real or noise" from an assumption into a checkable, apples-to-apples comparison — this is the one genuinely new methodological move in the design (the rest of the pipeline reuses existing verification/monitoring machinery). *hypotheses:* ["On the open-weight anchor lineages, for at least half of tested version transitions, B(v→v′) exceeds B_null by a BH-corrected paired-permutation test (α=0.05), the pooled point estimate ΔB is at least 3 percentage points, and strict-envelope contract types (schema, convention) show larger ΔB than few-shot template contracts."]
- **`m_fragility_predictor_model`** → targets `sp_power_collinearity`. *proposed_approach:* Mixed-effects logistic regression of the per-contract breakage event on the pre-registered 7-feature vector (schema nesting depth, field count, required-field ratio, constraint count, few-shot example count, instruction token length, delimiter/casing rule count) plus contract type, with random intercepts for version transition and model family; predictive utility assessed separately via grouped 5-fold and leave-one-family-out cross-validation; the contract library's stratified sampling design deliberately decorrelates depth from constraint count. *key_insight:* a multivariate model with grouped CV is what lets a per-feature claim survive both collinearity (features are naturally correlated) and repeated-testing inflation, which a marginal correlation table cannot. *hypotheses:* ["In the mixed-effects model, at least one of {schema nesting depth, constraint density} has an odds ratio ≥1.3 with 95% CI excluding 1 after BH correction; few-shot example count has an odds ratio <1; and leave-one-family-out predictive ROC-AUC is ≥0.65."]
- **`m_cheap_signal_decorrelation`** → targets `sp_causal_specificity`. *proposed_approach:* Run the LogProbTracking-style first-token top-k logprob two-sample detector on the same (contract, version) pairs used for the fragility model; compute its own AUC for predicting per-contract breakage; compare that AUC directly to `m_fragility_predictor_model`'s structural-feature AUC. *key_insight:* a cheap, contract-agnostic distribution-shift signal and a structural fragility model are answering different questions; only a head-to-head predictive comparison — not an assumption — shows whether breakage carries information specific to a contract's structure that the cheap signal misses. *hypotheses:* ["The structural fragility model's breakage-prediction AUC exceeds the first-token logprob detector's AUC by a pre-registered margin of at least 0.10."]
- **`m_mitigation_headroom_bound`** → targets `sp_avoidable_vs_inherent`. *proposed_approach:* On the open-weight chains, re-run the contract library under (a) a grammar-constrained decoding arm (xgrammar/outlines-style, guaranteeing the schema tier by construction while leaving the convention tier free) and (b) a DSPy-style per-version prompt recompilation arm; compare each arm's tier-decomposed B(v→v′) to the unmitigated arm on identical contracts via paired tests. *key_insight:* because constrained decoding only guarantees the schema tier, a tier-decomposed comparison — not an aggregate single number — is what distinguishes "mitigation eliminates the avoidable share" from "mitigation just moves which tier fails"; both arms share the same paired-against-unmitigated, tier-decomposed evaluation design even though they are different treatment techniques, which is what makes this one coherent method with two arms rather than two unrelated methods. *hypotheses:* ["(a) Grammar-constrained decoding removes at least 90% of schema-tier breakage.", "(b) Per-version prompt recompilation yields at least a 25% relative reduction in total B(v→v′), significant by a paired test on identical contracts (α=0.05)."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but `m_mitigation_headroom_bound` bundles two distinct mitigation techniques under one method_id, and needs a one-line justification for why that's one method with two arms rather than two separate methods competing for the same sub-problem.
- comments:
  - `{severity: minor, field: "m_mitigation_headroom_bound.hypotheses", anti_pattern: null, comment: "Grammar-constrained decoding and prompt recompilation are unrelated techniques (a decoding-time constraint vs. a prompt-compilation step) bundled into one method. Worth stating explicitly why this is one evaluation mechanism applied to two treatment arms, rather than scope creep disguised as a single method — the risk is a reviewer asking why these weren't proposed as two separate sub-problems/methods."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_mitigation_headroom_bound.key_insight` extended: "...the shared instrument here is the tier-decomposed, paired-against-unmitigated comparison protocol itself, not either mitigation technique — structurally analogous to a trial that tests two different drugs against the same placebo arm and the same pre-registered endpoint definitions. The sub-problem (`sp_avoidable_vs_inherent`) asks one question — how much of the measured breakage is avoidable — and both arms are two ways of answering that same question with the same measurement protocol, which is why they are one method with two hypotheses rather than two competing methods."
- `changes_made`: justified the two-arms-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **7 hypotheses total** (1+1+1+1+1+2 across the six methods respectively — `m_mitigation_headroom_bound` carries two, per the refiner's shared-protocol-two-arms justification above), mixing instrument-validity claims (validator calibration, version-addressability asymmetry, cheap-signal specificity) with the study's three headline empirical predictions (breakage-vs-noise, fragility predictors, mitigation headroom) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The cheap-signal comparison (`rq_cheap_signal_specificity`) is a mechanism-tier identifiability/specificity check on the measurement itself (does breakage carry contract-specific structure beyond a generic signal), not an "our system wins" claim — matching stages.md's guidance that for non-technical study types, "hypotheses and RQs are about attributes of the measurement/procedure... and baselines are optional sanity checks at best, not competitors to beat."

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- SchemaStore (schemastore.org) — real-world JSON schemas, sampled and stratified by nesting depth and constraint count; sources the schema-contract genre with a moderate, naturally occurring feature distribution.
- JSONSchemaBench — ~10K real-world JSON schemas for schema-constrained generation evaluation; scales the schema-contract genre beyond SchemaStore's coverage for the Stage-2 fragility model's power requirement.
- IFEval — programmatically verifiable instruction constraints; sources the format-convention contract genre with an established, machine-checkable rule set.
- WildChat-1M — real user–LLM conversations, mined for production-style few-shot/structured-output templates; sources the few-shot-template contract genre from genuinely in-the-wild usage rather than authored examples.
- Berkeley Function Calling Leaderboard (BFCL) v3 — function-calling structured-action contracts; extends contract coverage to the function-calling genre.
- FollowBench — multi-constraint instructions. (draft initially listed FollowBench with justification only "the benchmark RECAST builds on" — flagged below.)
- Model version chains: dated OpenAI gpt-4o snapshots (secondary, closed-API arm); Llama 2→3→3.1→3.3; Qwen2→Qwen2.5→Qwen3 (primary, open-weight anchor lineages).

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Within-version split-half noise floor (B0) — the necessary null every breakage claim in `rq_breakage_exceeds_noise` is tested against.
- LogProbTracking-style first-token logprob detector — the cheap-signal comparator for `rq_cheap_signal_specificity`; if it predicts breakage as well as the structural model, the contract library adds nothing beyond what cheap monitoring already gives.
- Grammar-constrained decoding arm (conceptual lineage: DiffusionCFG, implemented via xgrammar/outlines on the open-weight chains) — the schema-tier mitigation upper bound for `rq_mitigation_schema_tier`.
- DSPy-style per-version prompt recompilation — the mitigation baseline for `rq_mitigation_recompilation`.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_validator_agreement` | `sp_ground_truth_definition` | "Validator-vs-hand-label agreement on a held-out calibration set of positive/negative example outputs is ≥0.95, across all three tiers." |
| `rq_addressability_canary` | `sp_version_attribution` | "Across the collection window, open-weight anchor lineages trigger zero canary-flagged re-collection events, while at least one closed-API dated-snapshot chain triggers at least one — i.e., the addressability risk this design anchors around on open-weight chains is not a hypothetical one." |
| `rq_breakage_exceeds_noise` | `sp_noise_confound` | "On the open-weight anchor lineages, for at least half of tested version transitions, B(v→v′) exceeds B_null by a BH-corrected paired-permutation test (α=0.05), the pooled point estimate ΔB is at least 3 percentage points, and strict-envelope contract types (schema, convention) show larger ΔB than few-shot template contracts." |
| `rq_fragility_predictors` | `sp_power_collinearity` | "In the mixed-effects model, at least one of {schema nesting depth, constraint density} has an odds ratio ≥1.3 with 95% CI excluding 1 after BH correction; few-shot example count has an odds ratio <1; and leave-one-family-out predictive ROC-AUC is ≥0.65." |
| `rq_cheap_signal_specificity` | `sp_causal_specificity` | "The structural fragility model's breakage-prediction AUC exceeds the first-token logprob detector's AUC by a pre-registered margin of at least 0.10." |
| `rq_mitigation_schema_tier` | `sp_avoidable_vs_inherent` | "Grammar-constrained decoding removes at least 90% of schema-tier breakage." |
| `rq_mitigation_recompilation` | `sp_avoidable_vs_inherent` | "Per-version prompt recompilation yields at least a 25% relative reduction in total B(v→v′), significant by a paired test on identical contracts (α=0.05)." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step-6/Step-9 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation-provenance note instead of a real methodological reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "datasets[FollowBench]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'the benchmark RECAST builds on' is not a justification — it says nothing about which RQ needs FollowBench specifically or why."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "FollowBench — multi-constraint instructions stratified by constraint count; *justification:* sources contracts at the high end of the constraint-density range needed for `rq_fragility_predictors`, giving the constraint-density feature enough variance in the library for its odds ratio to be estimable — SchemaStore/JSONSchemaBench schemas alone skew toward moderate constraint counts."
- `changes_made`: gave FollowBench's inclusion an RQ-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_causal_specificity.source_limitation_ids = ["lim_coipo_tare_dual"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (noise-adjusted breakage rate, fragility predictor model, mitigation-headroom estimate) are each reachable: the rate via `sp_ground_truth_definition` + `sp_version_attribution` + `sp_noise_confound` (+ `sp_causal_specificity` for its causal validity), predictors via `sp_power_collinearity`, mitigation headroom via `sp_avoidable_vs_inherent` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, including the cheap-signal comparison (correctly mechanism-tier, not outcome-tier — see Stage 6 header).

**What was hardest:** as with the B5.5 exemplar, the recurring tension was **not disagreement about facts** (the seed material is unusually well-specified, down to a formal Step-5 notation table and Step-6 pre-registered hypotheses with fallbacks) but **scope discipline** — repeatedly checking whether a stage-5/6 hypothesis was quietly restating `paper.md`'s own already-finished RQ1–RQ3, versus adding something this schema's structure specifically demands. The three purely-instrument-validity hypotheses (validator agreement, canary/addressability asymmetry, cheap-signal AUC gap) are exactly this: `paper.md`'s own Assumptions A1–A3 gesture at validator construct validity, version addressability, and causal specificity as *risks to detect*, but never state them as the paper's own falsifiable hypotheses in their own right — that promotion from "assumption with a mitigation" to "stated, testable hypothesis" is what Stage 5's structure specifically forced.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`, `pipeline.md`'s Phase G findings; no `design_review.md` exists for this topic). Every finding was enumerated and checked against the current deliverables before acting.

**Findings already applied or logged as resolved (no action needed):**
- `stage_review.md` Stage 2 REVISE (nearest-neighbor sentence in Related Work) — applied in the earlier pass; verified present as the opening of Related Work in `paper_draft.md`/`.tex`.
- `stage_review.md` Stage 4 REVISE (Falsification condition line on all seven RQ subsections) — applied; verified present in all seven RQ subsections of `paper_draft.md`/`.tex` and mirrored in `experiment_design.md`.
- `stage_review.md` Phase A items 1/2/5/6/7 (digest N12 absence_comment; reference-cache records; Gate/Consequence on A1–A6; Estimand R1; R2 five-step validator plan; Confound Ledger R3; INCONCLUSIVE pre-declaration) — all applied to `digest.md`/`paper.md`/`reference_candidates.jsonl`; logged as resolved in `pipeline.md`.
- Phase G [major] bibliography wiring; [moderate] freshness-sweep paragraph leak; [moderate] missing Threats to Validity section; [minor] EPC-vs-LogProbTracking ranking clause — all applied and logged as resolved in `pipeline.md`.
- `taste_audit.md` — both audits are 🟢 verdicts with no action items; nothing to apply.

**Finding applied this round:**
1. Source: `pipeline.md` Phase G finding 4 / `stage_review.md` resume-pass Step 4 (also echoed in the first phase-log table's "one cosmetic [minor] open"). Finding: [minor] RQ numbering mismatch — `paper.md` headlines RQ1–RQ3 (H-RQ1–H-RQ3) while the draft numbers RQ1–RQ7, and the mapping was invisible to a reader of the paper alone; the logged to-do was a one-line mapping note. What changed: added a "Numbering note" immediately after the Research questions list stating the mapping (draft RQ3 ↔ H-RQ1, RQ4 ↔ H-RQ2, RQ6–RQ7 ↔ H-RQ3; draft RQ1/RQ2/RQ5 promote the pre-registered instrument-validity checks A1/A3/B-alt into numbered questions). Files: `paper_draft.md` (Experiments section) and `paper_draft.tex` (same location); `paper_draft.pdf` recompiled via `latexmk -pdf` — 0 errors, 16 pages, all 17 citations resolve, no undefined-citation warnings.

**Rejected as moot:** none — no other review finding remained open.

**Cross-deliverable consistency check (this round):** RQ counts (7 = 7), target hypotheses (verbatim in `experiment_design.md`, matching `paper.md` Stage-5/6 statements), effect floors and margins (validator agreement ≥0.95; power to separate B = 5% from B_null = 1% at α = 0.05; pooled ΔB ≥ 3 pp; OR ≥ 1.3 at ≥0.8 power; leave-one-family-out AUC ≥ 0.65; cheap-signal AUC margin ≥ 0.10; schema-tier reduction ≥ 90%; recompilation relative reduction ≥ 25%), and the pivoted-abstract fallback sentence all match between `paper_draft.md` and `experiment_design.md`. No mismatch found; no fix needed beyond the numbering note above.
