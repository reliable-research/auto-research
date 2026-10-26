# Discussion Trace — B3.5 (auto-research-discussion, all six stages)

> Extracted verbatim from `pipeline.md` (the run's original Stage 1–6 critic/refiner transcript), per the `auto-research-discussion` skill's updated "Final deliverables" spec, which calls for the discussion trace as a standalone file. Nothing below was regenerated or altered — this is the same content that fed the confirmed stage outputs behind `paper.md` and `paper_draft.md`. See `pipeline.md` for the goal.md Phase Log (bundle validation, compile, review-gate tracking) and `experiment_design.md` for the standalone Stage 6 spec.

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B3.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material is unusually mature (`paper.md` already carries a pre-registered asymmetry sentence, formal notation, and hard-coded fallback wording), so genuine disagreement surfaced but didn't require re-proposing.

---

## Seed brief

- **One-sentence description:** Measure whether the capability-orthogonal component of inter-version behavioral drift is correlated across LLM vendors beyond what an independence (exchangeability) null predicts, and whether cross-vendor behavioral diversity converges or diverges over a studied release window.
- **Apparent inputs:** a fixed, cross-domain probe battery spanning several behavioral axes, a priori partitioned into capability-loaded and capability-neutral axes; a longitudinal panel of dated model-version releases per vendor (pinned API snapshots for closed vendors, immutable checkpoints for open-weight vendors); release metadata.
- **Apparent outputs:** per-vendor drift vectors; a cross-vendor drift-vector correlation matrix under a permutation-null test (both calendar-time and release-index alignment); a time-indexed behavioral-diversity index and its trend; a conditional interpretive statement on the validity of multi-vendor redundancy as a risk-hedging strategy.
- **Closest research areas:** cross-model functional-similarity measurement (`GreatModelsThinkAlike`/CAPA); algorithmic-monoculture / RLHF diversity collapse (`CommunityAlignmentMonoculture`, `DiversityAwarePO`, `DQO`); recursive-training / synthetic-data homogenization mechanisms (`MultiEntityRecursion`, `ModelCollapseMemorization`); measurement-theoretic diversity construction (`MeasureDatasetDiversity`); single-snapshot inter-model homogeneity (`ArtificialHivemind`).
- **In scope:** behaviorally auditing existing, already-released commercial and open-weight model version sequences. **Out of scope:** verifying actual training-data or alignment-recipe overlap inside closed vendors (unobservable, digest C5); training or fine-tuning new models; single-snapshot-only comparisons with no longitudinal component.
- **Confidence: high.** As with the calibration exemplar (B5.5), the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already cross-references its own N-node ↔ M-component ↔ RQ ids and already ran its own asymmetry/bridge/synthesis self-check (`paper.md` Step 0/Step 3). Reconstruction risk is low; the risk is redundancy with `paper.md`'s own Step 5/6, so stages 4–6 below are framed to surface the schema's own required structure (per-sub-problem falsifiable hypotheses, mechanism-tier RQs) rather than re-deriving `paper.md`'s H1–H3 verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed cross-domain probe battery and a longitudinal panel of dated model-version releases across multiple LLM vendors, determine whether inter-version behavioral drift is correlated across vendors beyond what an independence (exchangeability) null would predict, and whether cross-vendor behavioral diversity trends toward convergence or divergence over the studied release window.
- `input`: (1) a fixed probe battery spanning several behavioral axes, administered identically to every collected version of every vendor's model; (2) a per-vendor ordered panel of dated releases with release dates; (3) release/version metadata.
- `output`: (1) per-vendor drift vectors (per-axis score deltas between consecutive versions); (2) a cross-vendor drift-vector correlation matrix with permutation-null significance, under both calendar-time and release-index alignment; (3) a time-indexed cross-vendor behavioral-diversity index and its trend; (4) an interpretive statement on the validity of multi-vendor redundancy as a risk-hedging strategy, conditional on (2)–(3).
- `constraints`: the probe battery must be held fixed across all vendor/version combinations for drift to be comparable; whether vendors actually share training data or alignment recipes is not directly observable and can only be inferred indirectly from behavioral correlation, since training pipelines are proprietary for all major closed vendors.
- `objective`: a correlation is accepted as "excess" (i.e., beyond independent development) only if it exceeds a pre-registered permutation-null threshold on the tested axes.
- `study_type`: `empirical` — stated explicitly: the seed's own core question ("不同厂商的模型是否朝相关方向漂移...行为空间的多样性随时间收敛还是发散？") and digest N12 already settle this as a measurement/characterization study, not a proposed fix or new system.

**critique:**
- summary: Solid, evidence-traceable draft, but the objective has a real evaluability gap that `paper.md`'s own Step 0 already discovered and that this draft has not yet imported.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'Exceeds a pre-registered permutation-null threshold' does not say what happens when the observed correlation is fully explained by every vendor simply getting more capable over time — a trivial shared attractor that produces positive drift correlation with zero shared-pipeline cause (digest C2). paper.md's own Step 0 asymmetry sentence makes exactly this point: 'raw agreement... is uninformative... the capability-orthogonal components... are exchangeable.' An objective that doesn't name this as first-class risks the whole study measuring something uninformative — a real, not hypothetical, failure mode this seed already anticipated."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "'vendor' is used ambiguously — does it mean a company (OpenAI) or a specific deployed model family within that company? Should be pinned down before input/version-panel construction is designed."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content the seed material already supplies — no new content needed).

### Refiner pass

- `objective` (refined): "A cross-vendor correlation is accepted as evidence of homogenization only if it (a) exceeds the 95th percentile of a permutation-based exchangeability null on the capability-neutral axes specifically, and (b) survives residualizing out the mean cross-vendor drift direction (the shared 'rising-tide' capability-improvement component); a correlation that appears only on capability-loaded axes, or that vanishes after residualization, is reported as *correlated improvement, not homogenization* rather than resolved by treating raw correlation as sufficient."
- `output` (clarified): "'vendor' denotes an organization's model family under one release cadence (e.g., 'GPT', 'Claude', 'Gemini', 'Llama'), not an individual snapshot — each vendor contributes exactly one drift-vector sequence."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md`'s own notation): "Vendors v ∈ V, each with an ordered panel of dated releases (m_{v,1},...,m_{v,T_v}). Fixed battery P partitions into K axes, a priori split into capability-loaded K_cap and capability-neutral K_neu. Drift vector d_{v,t} = per-axis z-normalized score deltas between m_{v,t} and m_{v,t+1}. Residualized drift d̃_{v,t} = d_{v,t} − proj onto the cross-vendor mean drift direction ḡ. Determine whether mean pairwise correlation ρ̄ of {d_{v,t}} restricted to K_neu — and of {d̃_{v,t}} — exceeds a permutation-null threshold, and whether a diversity index D(τ) over vendors' behavioral profiles trends downward across calendar time τ."
- `changes_made`: closed the evaluability gap in `objective` by importing the capability-residualization criterion; disambiguated "vendor"; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Multi-vendor redundancy (ensembling, fallback routing, LLM-as-judge panels, A/B deployment) is treated as a risk-hedging strategy against any single vendor's failure modes, biases, or outages, but this strategy silently assumes vendors' models evolve independently — an assumption current evidence has never tested longitudinally.
- `why_it_matters`: Concrete mechanisms exist by which independently-developed vendors could nonetheless converge: shared pretraining corpora and a shared pool of AI-generated web text acting as a cross-model data-sharing channel (`MultiEntityRecursion`'s "convergence toward homogeneous behavior"), and algorithmic monoculture in RLHF/DPO candidate generation (`CommunityAlignmentMonoculture`). If these operate across vendors over time, the independence assumption behind multi-vendor redundancy breaks without anyone noticing, because the failure is invisible at any single point in time.
- `who_cares`: Practitioners architecting ensembling/fallback-routing systems around vendor diversity; safety and reliability teams deciding whether multi-vendor deployment is a genuine hedge or a false sense of security; researchers deciding whether single-snapshot inter-model similarity findings (`ArtificialHivemind`'s 71–82% pairwise embedding cosine similarity) predict a *trend*, or are just a snapshot with no trajectory.
- `evidence`: `[GreatModelsThinkAlike, OpenReview:3Z827FtMNe]` shows models that improve independently nonetheless "think alike" and produce correlated mistakes at a single point in time, already destabilizing LLM-as-judge and weak-to-strong training; `[ArtificialHivemind, arXiv:2510.22954]` measures pronounced inter-model homogeneity but explicitly states its analysis "falls short of establishing causality" and has no temporal component — itself evidence the longitudinal question is open.

**critique:**
- summary: Good stake-specific motivation with real citations, but it under-covers one of Stage 1's four confirmed outputs.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a diversity-index *trend* over time — a distinct quantity from output (2)'s pairwise drift-vector correlation. The motivation only argues why correlated drift matters; it never explains why the diversity trend needs to be tracked as a separate quantity. A skeptical reader could ask: 'if drift vectors are correlated, doesn't the population's diversity necessarily shrink — why measure both?' The answer is that the two are logically separable (vendors could drift in correlated *directions* without the population's spread shrinking, e.g. if they move together but stay spread out; or diversity could shrink from independent convergence on a common optimum with no pairwise drift correlation at all) — but the draft never states this, so the motivation currently only justifies half of what Stage 1 promised."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, pairwise drift correlation and population-level diversity are not the same claim and can diverge: vendors could drift in correlated directions while the overall behavioral spread stays wide (correlated but not collapsing), or the population could narrow through several vendors independently converging on the same locally-optimal behavior with no pairwise drift correlation at all (collapsing but not correlated). A redundancy strategy is undermined by either failure mode on its own, so both the pairwise-correlation question and the population-diversity-trend question have to be tracked, not inferred from each other."
- `changes_made`: added the logical-separability argument distinguishing correlation from diversity-trend, closing the output-coverage gap.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level; no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_capa` | Anon., "Great Models Think Alike" (OpenReview:3Z827FtMNe) | **true** | Measures functional similarity (CAPA) at a single snapshot on benchmark tasks; has no temporal component, so it cannot say whether cross-model similarity increases across successive releases or attribute a trend to shared vendor pipelines. |
| `rw_monoculture` | Anon., "Community Alignment" / algorithmic monoculture (OpenReview:4NtoAVqfhA) | false (single-pipeline, not cross-vendor) | Characterizes homogenization as a property of one preference-collection pipeline (narrow RLHF/DPO candidate space); doesn't measure convergence across vendors or across dated releases of deployed models. |
| `rw_recursion` | Anon., "Multi-Entity Recursion" (OpenReview:JEU4PBaX85) | false (simulated, not deployed) | Theorizes and simulates a shared-synthetic-data channel that could homogenize behavior, but validates it in controlled training setups on toy/single-family models, not by auditing real multi-vendor version sequences released in the wild. |
| `rw_diversitypo` | Anon., "Diversity-Aware Policy Optimization" (OpenReview:5eZ0iykpDU) | false (single-model training artifact) | Documents RL post-training collapsing *one model's* output diversity; doesn't address cross-vendor convergence at all. |
| `rw_dqo` | Anon., "Diversity-Quality Optimization" (OpenReview:BV3bLKaJ3Y) | false (single-model training artifact) | Same limitation as above — mode collapse within one model's RLHF/GRPO training, not cross-vendor. |
| `rw_measurediversity` | Anon., "Measure Dataset Diversity, Don't Just Claim It" (OpenReview:jsKr6RVDDs) | false (methodological framework, not empirical) | Supplies validity/reliability criteria for a diversity *construct* but is aimed at dataset construction; offers no probe battery, no drift metric, and no longitudinal protocol for deployed-model behavioral change. |
| `rw_modelcollapse` | Anon., "Model Collapse... Memorization" (OpenReview:6xCcjYa97j) | false (theory, controlled training) | Explains diversity/quality degradation under recursive training on synthetic data through a generalization-to-memorization lens; theory for a mechanism, not a behavioral audit of real vendors. |
| `rw_hivemind` | Zhang et al. (?), "Artificial Hivemind" (arXiv:2510.22954) | **true** | Measures pronounced inter-model behavioral homogeneity (71–82% pairwise embedding cosine similarity) at a single point in time; explicitly states the analysis "falls short of establishing causality" and has no version-sequence/trajectory component. |

**critique:**
- summary: Grounding is solid and every limitation is specific, but one baseline label needs the same scrutiny the exemplar run flagged for its own nearest analog.
- comments:
  - `{severity: major, field: "specific_related_works[rw_hivemind].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "ArtificialHivemind's I/O framing is single-snapshot (one embedding-similarity reading across contemporaneous models) — genuinely different from this paper's longitudinal, per-version-step drift framing. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying this paper's drift-correlation numbers are being compared against ArtificialHivemind's reported cosine-similarity numbers, which they are not — only its measurement *idea* (embedding-based cross-model similarity) is reusable, as a same-time comparator, not a longitudinal one."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the *instrument* is still legitimately borrowable as a cross-check arm, per `paper.md`'s own `B-alt-RisingTide` design, which reuses exactly this kind of contemporaneous-similarity check).

### Refiner pass

- `rw_hivemind.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — ArtificialHivemind's own reported similarity numbers are not compared against. Its **contemporaneous cross-model similarity protocol** is borrowed as a same-time comparator arm (does same-time similarity behave differently from drift-*direction* similarity — the CAPA-style cross-check in `paper.md`'s `B-alt`), independent of its published findings."
- `rw_capa.is_potential_baseline` given the identical clarifying note for consistency (CAPA's own functional-similarity metric is borrowed as an instrument for the same contemporaneous cross-check, not as a number to beat).
- `changes_made`: clarified both single-snapshot works' role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (whether single-snapshot homogeneity from `rw_hivemind`/`rw_capa` predicts a longitudinal trend) restates this paper's own core question rather than a distinct framing check, and is already covered end-to-end as mechanism-tier RQs in Stage 6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C4 plus two schema-required components paper.md's Assumptions section only gestures at):

- **`sp_battery_construct_validity`** — *description:* Ensure the fixed probe battery's axes actually cover the behavioral dimensions relevant to "drift," rather than an arbitrary or biased slice of behavior space. *why_it_is_a_problem:* any drift or diversity claim is only as meaningful as the battery that produced it — an unvalidated or biased battery makes the whole finding an artifact of instrument choice. *technical_challenge:* automated axis scorers (refusal/sycophancy/stance detectors) must themselves be shown valid against human judgment before their deltas can be trusted as behavioral signal rather than scorer noise. *source_limitation_ids:* `["__novel__"]`.
- **`sp_capability_confound`** — *description:* Separate genuine cross-vendor behavioral homogenization from the trivial case where every vendor simply gets more capable over time, producing positively correlated drift with no shared-pipeline cause. *why_it_is_a_problem:* this is the seed's own load-bearing asymmetry (digest C2) — without addressing it, any positive correlation is uninterpretable, since a universal capability attractor guarantees some positive correlation regardless of whether vendors share anything. *technical_challenge:* capability improvement and genuine homogenization are not naturally separable in the raw drift signal; disentangling them requires an explicit axis partition (capability-loaded vs. capability-neutral) and a residualization procedure that removes the shared "rising tide" direction before testing correlation. *source_limitation_ids:* `["__novel__"]`.
- **`sp_time_alignment`** — *description:* Produce a cross-vendor correlation estimate that isn't an artifact of how vendor version sequences are aligned in time, given that vendors release on independent, asynchronous schedules. *why_it_is_a_problem:* there is no natural "comparable version step" across vendors, so a correlation computed under one alignment convention could disagree with — or simply not exist under — another. *technical_challenge:* calendar-time alignment and release-index alignment encode different (and equally defensible) notions of "the same point in each vendor's trajectory," and can yield materially different correlation estimates from the same underlying data. *source_limitation_ids:* `["__novel__"]`.
- **`sp_dimensionality_weighting`** — *description:* Show that any observed cross-vendor correlation is not an artifact of which behavioral axis happens to dominate the drift vector, or of an arbitrary per-axis weighting choice. *why_it_is_a_problem:* behavior space is high-dimensional (refusal, stance, sycophancy, factuality, tone, safety posture), and a single scalar correlation computed over an unexamined combination of axes could be driven entirely by one axis while looking like a broad-spectrum finding. *technical_challenge:* no principled a priori weighting of axes exists, so robustness has to be demonstrated empirically — per-axis breakdown plus a leave-one-axis-out re-estimate — rather than assumed. *source_limitation_ids:* `["__novel__"]`.
- **`sp_diversity_operationalization`** — *description:* Construct a defensible cross-vendor behavioral-diversity index whose convergence or divergence over time is itself a meaningful, validated claim, not an ad hoc statistic. *why_it_is_a_problem:* "diversity" is a latent construct — if it is operationalized without explicit conceptualization and validation, a reported trend could be an artifact of the particular index chosen rather than a real property of the vendor population. *technical_challenge:* the index must be shown reliable and non-redundant with the drift-correlation quantity above (i.e., detect a genuinely distinct failure mode: population-level narrowing that pairwise drift correlation would not catch, and vice versa). *source_limitation_ids:* `["lim_measurediversity_construct"]` (maps to `rw_measurediversity`'s limitation: it supplies validity criteria for a diversity construct but no concrete instrument for this setting).
- **`sp_noise_floor`** — *description:* Establish that measured inter-version change exceeds ordinary measurement noise before any cross-vendor correlation on that change is interpreted as a real signal. *why_it_is_a_problem:* if version-to-version score deltas are within the noise band of repeated measurement on the *same* fixed model, "drift correlation" would just be correlated measurement noise, and the entire question would be moot. *technical_challenge:* establishing a noise floor requires a same-snapshot test–retest design (split-half plus repeated-interval re-probing) distinct from, and prior to, any actual cross-version comparison. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all six would jointly deliver Stage 1's objective and outputs), but two sub-problems risk reading as the same underlying "is the measurement trustworthy" concern stated twice.
- comments:
  - `{severity: minor, field: "sp_battery_construct_validity / sp_noise_floor", anti_pattern: "overlap", comment: "Both ultimately ask 'can this measurement be trusted,' which can read as one sub-problem restated. They are genuinely distinct — one is about whether the battery's *axes* validly represent the behavioral space the paper claims to be measuring (a coverage/bias question, checked once against human judgment), the other is about whether *repeated measurement* of one fixed model is stable enough to distinguish real change from noise (a reliability/test-retest question, checked continuously via re-probing) — but the descriptions don't make that distinction explicit."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_battery_construct_validity.technical_challenge` sharpened to end with: "...this is a **construct-validity** problem — does the chosen axis set represent the thing the paper claims to measure — distinct from whether repeated measurement of one fixed model is itself stable."
- `sp_noise_floor.technical_challenge` sharpened to end with: "...this is a **measurement-reliability** problem distinct from construct validity: even a perfectly representative battery still needs its own test–retest stability established before any delta on it is trusted as signal rather than sampling noise."
- `changes_made`: made the construct-validity-vs-reliability distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 1 sourced from a related-work limitation, 5 `__novel__` with stated decisive-component justifications; **`C5` — the unobservability of the actual causal mechanism behind any correlation — is deliberately not elevated to a sub-problem**: `paper.md`'s own N6 lists it as an `unaddressed_challenge`, and no method in Stage 5 below claims to resolve it. It remains a scope boundary stated in Stage 1's `constraints`, not a gap this paper's method targets.).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_probe_battery`** → targets `sp_battery_construct_validity`. *proposed_approach:* Assemble a fixed battery spanning capability-loaded axes (factuality, instruction/format compliance, reasoning) and capability-neutral axes (refusal, sycophancy, political/moral stance), each scored by a dedicated automated instrument (keyword+classifier refusal detector, opinion-agreement flip probes, IFEval-style verifiable constraints, held-fixed QA slice, fixed stance battery); validate every automated scorer against human labels on a held-out subset before use. *key_insight:* a battery's construct validity has to be earned per-axis against human judgment, not asserted, because a scorer disagreement would silently corrupt every downstream drift and correlation number computed from it. *hypotheses:* ["Each automated axis scorer achieves inter-rater agreement κ ≥ 0.70 against human labels on a held-out validation subset of at least 500 items per axis; any axis that fails this bar is re-instrumented or dropped before the main analysis."]
- **`m_capability_residualization`** → targets `sp_capability_confound`. *proposed_approach:* Compute cross-vendor drift-vector correlation separately on capability-loaded axes (K_cap) and capability-neutral axes (K_neu); separately, project out the cross-vendor mean drift direction (the shared "rising tide") from every vendor's drift vector and recompute correlation on the residual. *key_insight:* a benign, capability-only explanation predicts correlation concentrated on K_cap and attenuated after residualization; genuine homogenization predicts correlation that survives both cuts — so the same two operations that would refute a real effect are exactly what makes a surviving effect credible. *hypotheses:* ["If observed cross-vendor drift correlation is driven by shared capability improvement rather than genuine homogenization, correlation on K_cap axes will be significantly higher than on K_neu axes.", "If observed correlation is driven by the shared capability-improvement direction, residualized drift correlation will be substantially attenuated relative to raw drift correlation; a homogenization claim requires it not be."]
- **`m_dual_alignment`** → targets `sp_time_alignment`. *proposed_approach:* Compute the cross-vendor correlation matrix twice — once under calendar-time-bin alignment, once under release-index alignment — using the identical estimator and permutation-null machinery in both cases. *key_insight:* if a correlation finding is genuine rather than an artifact of one arbitrary alignment convention, its sign should not depend on which convention is used. *hypotheses:* ["The sign of the mean pairwise cross-vendor drift correlation is identical under calendar-time and release-index alignment in the majority of tested vendor pairs."]
- **`m_axis_robustness`** → targets `sp_dimensionality_weighting`. *proposed_approach:* Report per-axis pairwise correlation alongside the aggregate, and recompute the aggregate after removing the single most-correlated axis (leave-one-axis-out). *key_insight:* a correlation that survives removing its single strongest contributing axis cannot be an artifact of one dominant, arbitrarily-weighted dimension. *hypotheses:* ["A significant aggregate cross-vendor drift correlation, if present, holds (is individually significant) on at least half of the tested behavioral axes, and remains significant after the single most-correlated axis is removed."]
- **`m_diversity_index`** → targets `sp_diversity_operationalization`. *proposed_approach:* Construct a time-indexed cross-vendor diversity index as the Vendi Score over vendors' per-axis behavioral profiles at each calendar bin, with a secondary index (mean pairwise CAPA-style functional distance across vendors) computed in parallel; fit a Theil–Sen trend to each and compare their signs. *key_insight:* a single diversity claim computed only one way is exactly what index-shopping would produce; requiring two independently constructed indices to agree in sign is what makes a reported trend a property of the vendor population rather than of the index's specific construction. *hypotheses:* ["The Theil–Sen slope of the primary (Vendi) diversity index is significantly negative over the studied window, with a total decline of at least 10% of the window-initial value.", "The sign of the diversity trend is consistent between the primary (Vendi) index and the secondary (mean pairwise CAPA-distance) index."]
- **`m_noise_floor_gate`** → targets `sp_noise_floor`. *proposed_approach:* Re-probe every pinned snapshot twice (a split-half re-probe and a two-week test–retest re-probe); take the 95th percentile of the resulting same-model score-delta distribution as the noise floor ν; classify a version-step as "drifted" only if its measured delta magnitude exceeds ν. *key_insight:* the noise floor has to be measured empirically from the same instrument applied to a model that is not changing, because no analytic formula substitutes for actually observing how much a fixed model's scores move on repeated measurement. *hypotheses:* ["At least two-thirds of true version-steps across the tested vendor panel exceed the empirically-measured noise floor ν — i.e., models measurably drift at all under this battery, which is a precondition for every other hypothesis in this study."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold, but one method bundles two headline claims and needs a one-line justification for why that is one mechanism, not two — the same pattern flagged in the calibration exemplar.
- comments:
  - `{severity: minor, field: "m_capability_residualization.hypotheses", anti_pattern: null, comment: "The two hypotheses here (K_cap-vs-K_neu asymmetry, and raw-vs-residualized attenuation) are the paper's most central claims — the entire Step-0 asymmetry sentence rests on both holding together. Worth stating explicitly why one mechanism produces both, so this doesn't read as two methods folded into one entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_capability_residualization.key_insight` extended: "...both readouts come from one construction: partitioning axes into K_cap/K_neu and residualizing out ḡ are the same operation (project out the shared component, whether defined by axis membership or by the empirical mean-drift direction) applied at two granularities — one instrument, two falsifiable predictions, not two separate mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly, mirroring the exemplar's `m_matched_conditions` fix.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **8 hypotheses total** (1 + 2 + 1 + 1 + 2 + 1 across the six methods respectively), mixing instrument-validity claims (battery validation, noise floor) with the study's headline empirical predictions (capability-residualization, diversity trend) — a deliberate design choice for an `empirical` study_type, explained in the Stage 6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- IFEval — *justification:* verifiable-constraint instruction/format-compliance prompts; supplies the capability-loaded instruction-compliance axis needed by `rq_raw_capability_difference` and `rq_residualized_attenuation`.
- TruthfulQA + SimpleQA — *justification:* held-fixed factual-QA slice; supplies the capability-loaded factuality axis for the same two RQs.
- A curated borderline-safety refusal set — *justification:* supplies the capability-neutral refusal axis needed by `rq_raw_capability_difference`, `rq_alignment_stability`, and `rq_axis_robustness`.
- Anthropic sycophancy-eval-style opinion-flip probes — *justification:* supplies the capability-neutral sycophancy axis, same RQs as above.
- GlobalOpinionQA-style stance battery — *justification:* supplies the capability-neutral political/moral-stance axis, same RQs as above.
- (draft initially listed "NoveltyBench / INFINITY-CHAT-style open-ended prompts" with justification only "digest mentions it for the diversity axis" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Permutation / shuffled-vendor-pairing exchangeability null — the necessary control for every correlation claim (`rq_raw_capability_difference` through `rq_axis_robustness`).
- Single-vendor drift-only analysis — a degenerate no-cross-vendor baseline confirming the correlation machinery reduces to nothing informative when there is nothing to correlate against.
- CAPA / ArtificialHivemind-style contemporaneous cross-model similarity check — cross-check that same-time similarity is not being silently substituted for drift-*direction* similarity (per Stage 3's sharpened role for these two works).

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_battery_validity` | `sp_battery_construct_validity` | "Each automated axis scorer achieves inter-rater agreement κ ≥ 0.70 against human labels on a held-out validation subset of at least 500 items per axis; any axis that fails this bar is re-instrumented or dropped before the main analysis." |
| `rq_raw_capability_difference` | `sp_capability_confound` | "If observed cross-vendor drift correlation is driven by shared capability improvement rather than genuine homogenization, correlation on K_cap axes will be significantly higher than on K_neu axes." |
| `rq_residualized_attenuation` | `sp_capability_confound` | "If observed correlation is driven by the shared capability-improvement direction, residualized drift correlation will be substantially attenuated relative to raw drift correlation; a homogenization claim requires it not be." |
| `rq_alignment_stability` | `sp_time_alignment` | "The sign of the mean pairwise cross-vendor drift correlation is identical under calendar-time and release-index alignment in the majority of tested vendor pairs." |
| `rq_axis_robustness` | `sp_dimensionality_weighting` | "A significant aggregate cross-vendor drift correlation, if present, holds (is individually significant) on at least half of the tested behavioral axes, and remains significant after the single most-correlated axis is removed." |
| `rq_diversity_trend` | `sp_diversity_operationalization` | "The Theil–Sen slope of the primary (Vendi) diversity index is significantly negative over the studied window, with a total decline of at least 10% of the window-initial value." |
| `rq_diversity_index_consistency` | `sp_diversity_operationalization` | "The sign of the diversity trend is consistent between the primary (Vendi) index and the secondary (mean pairwise CAPA-distance) index." |
| `rq_noise_floor_gate` | `sp_noise_floor` | "At least two-thirds of true version-steps across the tested vendor panel exceed the empirically-measured noise floor ν — i.e., models measurably drift at all under this battery, which is a precondition for every other hypothesis in this study." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3/B0/B-alt numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to "the digest mentions it" instead of a real methodological reason — the identical anti-pattern the calibration exemplar caught in its own Stage 6.
- comments:
  - `{severity: major, field: "datasets[NoveltyBench/INFINITY-CHAT]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it for the diversity axis' says nothing about which RQ specifically needs it or why the correlation-axis prompt sets above are insufficient for the diversity computation."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "NoveltyBench / INFINITY-CHAT-style open-ended prompts — *justification:* the Vendi Score computation in `rq_diversity_trend` and `rq_diversity_index_consistency` needs open-ended generations with a large possible-response space to make a diversity statistic meaningful; the closed-form, single-correct-answer axis prompts used for drift-vector correlation (IFEval, TruthfulQA/SimpleQA) would produce a degenerate, near-constant diversity index regardless of the true population spread, so a separate open-ended prompt set is required specifically for the two diversity RQs, not the six correlation RQs."
- `changes_made`: gave the open-ended-prompt dataset's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_diversity_operationalization.source_limitation_ids = ["lim_measurediversity_construct"]` ∈ Stage 3 limitations ✓ (traces to `rw_measurediversity`); all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (drift vectors, correlation matrix, diversity trend, interpretive statement) are each reachable: drift vectors via `sp_noise_floor` + `sp_battery_construct_validity`; correlation matrix via `sp_capability_confound` + `sp_time_alignment` + `sp_dimensionality_weighting`; diversity trend via `sp_diversity_operationalization`; the interpretive statement (output 4) is not a separate sub-problem/method/RQ — it is a conditional synthesis over the (correlation, diversity) outcome pairs, carried into the Experiments section's setup and the Conclusion, exactly mirroring `paper.md`'s own Claim–Evidence Map treatment of this as a conditional statement rather than a new measured quantity. Nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.
6. **Deliberately excluded from the sub-problem/method/RQ chain:** `C5` (unobservability of the actual causal mechanism) — confirmed at Stage 4 as a stated scope boundary in Stage 1's `constraints`, not a gap any Stage 5 method claims to close. This mirrors `paper.md`'s own explicit "not computable from observables... deleted from claims" treatment (Step 5 table) and `N6.unaddressed_challenges = ["C5"]`.

**What was hardest:** as with the calibration exemplar, the recurring tension was not disagreement about facts — `paper.md` is unusually well pre-registered, down to hard-coded thresholds — but **scope discipline**: repeatedly checking whether a Stage 5/6 hypothesis was quietly restating one of `paper.md`'s own H1/H2/H3 rather than adding something the schema's finer granularity specifically requires (e.g., the battery-validation and noise-floor-gate hypotheses, which `paper.md`'s Assumptions table (A2, A4) states as gates but never elevates to falsifiable hypotheses of their own the way this schema does).


---

## Post-review revision round (2026-07-05)

> Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists for this topic). Every finding in those files was enumerated and its status checked against the current deliverables. This section appends the disposition record; no past round above was rewritten.

**Already applied before this pass (verified present in current deliverables, no action needed):**

1. `stage_review.md` Stage 2 REVISE (nearest-neighbor sentence naming Artificial Hivemind + delta) — confirmed present in `paper_draft.md`/`.tex` Related Work opening.
2. `stage_review.md` Stage 4 REVISE (explicit **Falsification condition** line per RQ) — confirmed present in all 8 RQ subsections of `paper_draft.md`/`.tex`.
3. `stage_review.md` Phase A item 1 REVISE (digest.md N12 missing status + 3-part absence_comment) — fixed in `digest.md` per Phase A record.
4. `stage_review.md` Phase A item 2 REVISE (reference-cache integrity: 150 candidates verdicted, 7 N3 corpus records appended) — fixed in `reference_candidates.jsonl` per Phase A record.
5. `stage_review.md` Phase A item 5 REVISE (Assumptions table PG-1..PG-6 gate IDs + consequence column) — fixed in `paper.md` (verified: PG-gates present in Step 5 Assumptions table).
6. `stage_review.md` Phase A item 6 REVISE (R1 estimand sentence; M1 5-step R2 instrument-validation plan; R6 mechanism analysis; INCONCLUSIVE pre-declaration rule; CAPA definition at first use) — all fixed in `paper.md` (verified: Estimand sentence, per-axis log-odds R6 subsection, CI-half-width-0.15 / <4-pairs INCONCLUSIVE rule all present).
7. `stage_review.md` Phase G finding 1 [major] (no `refs.bib`/`\cite` infrastructure) — fixed: `gen_refs_bib.py` + natbib wiring present, compile clean per Phase I log.
8. `stage_review.md` Phase G finding 2 [major] (method-twin `BoundarySyncRepCoupling2607` uncited) — fixed: concede-and-differentiate Related Work paragraph present in `paper_draft.md`/`.tex`.
9. `taste_audit.md` (original + 2026-07-04 re-audit) — verdict 🟢 both passes, zero action items; nothing to apply.

**Applied in this pass (was OPEN):**

10. `stage_review.md` Phase G finding 3 [minor] — `paper.md` H3 (aggregate-ρ̄ sign under both alignments) vs. `paper_draft.tex`/`experiment_design.md` RQ4 (per-pair majority-sign) stated different alignment-stability granularity; the review required reconciliation before Phase B ever scores H3, offering two options (rewrite H3 to per-pair, or note in `paper.md` that Stage 6 refined it). **Change:** took the second option, preserving the pre-registered H3 wording — added a "Granularity reconciliation note" to `paper.md`'s E3 recording the Stage-6 refinement (`m_dual_alignment`/`rq_alignment_stability`, per-pair majority-sign) and declaring it the operative binary criterion for H3's first conjunct, with aggregate-ρ̄ sign reported as descriptive only; conjuncts 2–3 unchanged. **Files:** `../paper.md` (E3 note added); `experiment_design.md` (Cross-references bullet updated from "still open" to resolved, with the operative scoring rule restated). `paper_draft.md`/`.tex` needed no change — their RQ4 wording already matches the now-operative per-pair form verbatim — so no recompile was required.

**Rejected as moot:** none — every enumerated finding was either already applied or applied above.

**Cross-deliverable consistency check (this pass):** RQ count 8 = 8 (`paper_draft.md` Experiments vs. `experiment_design.md`); target hypotheses in `experiment_design.md` remain byte-identical to the Stage 5 wording in this trace; effect floors and margins match across deliverables — κ ≥ 0.70 on ≥500 items/axis (RQ1), ≥10k permutation draws + BH q = 0.05 (RQ2–RQ5), majority-of-pairs sign stability (RQ4), ≥3 of 6 axes + leave-one-axis-out (RQ5), Theil–Sen slope negative with ≥10% window decline (RQ6), two-index sign agreement (RQ7), ≥2/3 of version-steps above ν (RQ8). No new mismatch found.
