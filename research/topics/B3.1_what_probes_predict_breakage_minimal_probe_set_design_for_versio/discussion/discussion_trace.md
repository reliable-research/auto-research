# Discussion Trace — B3.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Extracted verbatim from `pipeline.md` (the "## Seed brief" through "## Cross-stage consistency check" sections), per `auto-research-discussion`'s "Final deliverables" item 3. This is the complete round-by-round record across all six stages: every draft version, every critique (comments + severities + resolution), every decision, every refiner pass. It fed the already-existing, already-reviewed `paper.md` and `paper_draft.*`; nothing here was re-run or regenerated. `pipeline.md` itself now carries only a one-line pointer to this file plus its own Phase Log (goal.md phase-gate tracking, unrelated to this six-stage trace). See `experiment_design.md` for the standalone Stage 6 spec.

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B3.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature, so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure which of five observable behavioral-probe families (capability, refusal-boundary, format-preference, calibration, safety-behavior) best predicts real downstream-task breakage across already-shipped LLM version pairs, and identify the smallest family subset that retains most of that predictive power.
- **Apparent inputs:** retrospective LLM version pairs (open-weight checkpoint successions plus dated API snapshots); a five-family probe item bank administered identically to both versions of a pair; a shared set of real downstream-task inputs run through both versions to compute ground-truth output differences.
- **Apparent outputs:** per-family, per-pair drift-magnitude scores; a predictive-power ranking of the five families against downstream breakage; a minimal-sufficient family subset packaged as a practical audit protocol.
- **Closest research areas:** benchmark compression / minimal item-subset design (`EssenceBench`); cross-release black-box behavioral audits (`BiasSimilarity-BSM`); single-axis behavioral instruments for refusal, calibration, and safety (`RefusalIndex`, `B-Calibration`, `OffTopicEval`, `ProSafePrune`); prompt-sensitivity/instrument brittleness (`TARE`); training-side, white-box model-update interpretability (`WeightDiff`).
- **In scope:** black-box, retrospective auditing of already-shipped version pairs using observable probes run identically pre/post. **Out of scope:** white-box/weight-space analysis of the update itself; predicting a *future*, not-yet-shipped version's breakage; training new probes or new models.
- **Confidence: high.** As with a mature autoclaude seed, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Step 0/Step 3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Step 5/6, which is why stage 5/6 below are framed as validating the **measurement instrument's properties** (noise floor, paraphrase stability, corpus-attrition bias, family collinearity) rather than re-deriving `paper.md`'s three headline hypotheses (H1/H2/H3) from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a set of already-occurred LLM version pairs, each with a fixed five-family probe battery (capability, refusal-boundary, format-preference, calibration, safety-behavior) administered identically to both versions, and a shared set of real downstream-task inputs run through both versions to compute ground-truth output differences, determine which probe family's drift magnitude is most predictive of that downstream breakage, and identify the smallest subset of families that retains most of that predictive power.
- `input`: (1) version pairs (v_old, v_new) drawn from open-weight checkpoint successions and dated API snapshots; (2) a probe item bank spanning five behavioral families, run identically on both versions of each pair; (3) a shared downstream-task input set, run through both versions to compute output differences.
- `output`: (1) a per-family, per-pair drift-magnitude score; (2) a predictive-power ranking of the five families against downstream breakage; (3) a minimal-sufficient family subset recommended as a practical audit protocol.
- `constraints`: both versions of a pair must remain queryable under identical decoding for the full probe-plus-downstream input set; downstream breakage must be computable from a shared input set, not from provider-reported changelogs.
- `objective`: a family is accepted as predictive only if its correlation with downstream breakage exceeds a stated within-version sampling-noise floor and remains rank-stable across paraphrase sets — not just a raw nonzero correlation.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 already classifies this as a measurement/characterization study ("a retrospective correlational comparison of five existing probe-family drift measures against real downstream-task breakage"), not a proposed new detector or system being pitted against baselines to win.

**critique:**
- summary: Strong draft, evidence-traceable to the seed, but the objective has a real evaluability gap on one of its three promised outputs, and the summary quietly presupposes the ranking will be nonempty.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective states an acceptance criterion for output (2) — the ranking — via the noise-floor and paraphrase-stability gates, but says nothing about what makes output (3) — the 'minimal-sufficient' subset — acceptable. 'Retains most of that predictive power' is not evaluable as written: most compared to what margin? Without a stated threshold, a reader cannot tell whether a 4-family subset that recovers 51% of the full battery's AUC would count as 'minimal-sufficient' or not. Per the rigor filters in `stages.md` stage 6, this is exactly the kind of design parameter that must be authored (not fabricated), but stage 1's objective needs to name that a margin exists even before stage 6 fixes its numeric value."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'determine which probe family... is most predictive' presupposes some family is genuinely predictive at all. Digest N9's own Result 1 falsification path and paper.md's RQ1 fallback both explicitly allow for 'no family reaches the threshold' as a valid, reportable outcome (handing the burden to the minimal-subset question). The summary should not read as though a winning family is guaranteed to exist."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A family is accepted as predictive only if its correlation with downstream breakage exceeds a stated within-version sampling-noise floor and remains rank-stable across paraphrase sets. A subset of families is accepted as **minimal-sufficient** only if its cross-validated predictive power (AUC) falls within a pre-specified margin of the full five-family battery's predictive power — not merely 'most' of it, but within a stated, pre-registered tolerance. If no family clears the predictive-correlation gate, or if predictive power degrades roughly linearly as families are dropped with no subset clearing the margin, both are reportable outcomes under this objective, not failures of it."
- `summary` (refined): "...determine **whether, and to what degree,** each probe family's drift magnitude predicts that downstream breakage, and identify the smallest subset of families that retains most of the full battery's predictive power within a pre-specified margin..." (removes the presupposition that a clearly winning family exists).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Version pair p = (v_old, v_new), p ∈ P. Probe families F = {cap, ref, fmt, cal, saf}, index f, each with item set I_f. Downstream tasks t ∈ T with shared input set X_t. Unit of analysis: cell (p, t). D_f(p) = signed drift magnitude of family f on pair p; B(p,t) ∈ [0,1] = downstream breakage on cell (p,t). Determine π_f = predictive power of D_f for B̄(p) = mean_t B(p,t), and the minimal-sufficient subset S* ⊆ F such that AUC(S*) ≥ AUC(F) − δ for a pre-specified δ."
- `changes_made`: added a named acceptance margin to the objective for the minimal-subset output; removed the presupposition that a predictive family necessarily exists; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: A cheap per-version probe battery is one of the few practical ways a team could audit an LLM version update without a full downstream re-test, but which behavioral axis's drift actually forecasts real breakage — as opposed to merely tracking how much the update changed overall — has not been directly measured.
- `why_it_matters`: Teams that build on a hosted or self-hosted LLM re-test against every new version at a cost that scales with the number of downstream integrations; if the axis they choose to probe (typically raw capability, because benchmarks like MMLU/GSM8K are the most familiar re-test target) is not the axis that actually governs breakage, they get a false sense of having audited the update while the real risk — a refusal-boundary or safety-behavior shift that silently breaks a policy filter or an agent's tool-calling behavior — goes undetected. The problem is specifically that no cited work compares probe families against each other or against a downstream-breakage ground truth (digest N4's absence_comment): each of the grounded instruments (`RefusalIndex`, `B-Calibration`, `OffTopicEval`, `ProSafePrune`) is a precise measure of its own single axis at a single point in time, but none says whether that axis is the one a downstream consumer should actually be watching.
- `who_cares`: Teams operating LLM-backed pipelines (parsers, safety filters, tool-calling agents) who must decide what to re-test after every version bump; model providers deciding what to disclose in a changelog or model card; researchers deciding whether benchmark-compression ideas (`EssenceBench`'s subset-selection framing) transfer from "preserve a score" to "predict a different, downstream target."
- `evidence`: `[RefusalIndex, OpenReview:9gJBhkLRat]`, `[OffTopicEval, OpenReview:EcIyiJrajc]`, `[B-Calibration, OpenReview:0sCyk9Tr5J]`, and `[ProSafePrune, OpenReview:QkHKaPfRAB]` each independently demonstrate that a single behavioral axis (refusal, safety-scope, calibration, over-refusal respectively) is measurable and drift-prone, but digest N4's grounding shows none of them is evaluated against another axis or against a real downstream-task ground truth — itself evidence that the comparative question is open, not merely under-published.

**critique:**
- summary: Good stake-specific motivation with real citations, but coverage of stage 1's third output — the minimal subset — is thin relative to the ranking output.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a minimal-sufficient family subset, not just a ranking. why_it_matters motivates why knowing *which axis* matters, but never explains why a team would need the smallest sufficient subset specifically, as opposed to just running the full five-family battery every time once the ranking is known — a reader could reasonably ask 'if it's already this cheap, why does minimality matter at all?' Without an answer, the third output is left unmotivated."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, knowing the ranking alone does not make continuous auditing sustainable: providers ship new versions at a cadence that compounds across every deployed integration a team maintains, and each additional probe family in the battery carries its own item-bank curation cost, its own ambiguous-case adjudication (safety and refusal probes in particular need human review for borderline cases, unlike a deterministic schema check), and its own administration overhead repeated once per version per integration. A five-family battery run occasionally is cheap; a five-family battery run on every version bump against every integration is not — which is exactly why identifying the smallest subset that still retains most of the predictive power, not merely the full ranking, is what turns this from a one-off academic comparison into a protocol a team could actually run continuously."
- `changes_made`: added the cadence/scale argument motivating why minimality is a distinct, load-bearing output rather than a redundant restatement of the ranking.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (full motivation/method text was read for each per digest N3's own search-honesty note); no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_essencebench` | Anon., EssenceBench (OpenReview:lZlZjSxdio) | **true** | Selects a minimal item subset to preserve a score/ranking under one metric at one time; does not select probes to predict *cross-version downstream breakage*, does not span behavioral axes beyond task accuracy, and optimizes for score fidelity rather than diagnostic predictive power for a separate downstream target. |
| `rw_bsm` | Anon., BiasSimilarity-BSM (OpenReview:EveruzAsGI) | false (single-construct audit, not a breakage predictor) | Compares whether a tuned release departs from its base within one behavioral construct (fairness/bias) and outputs a pairwise similarity, but never connects the measured departure to any downstream application's actual breakage, nor compares which behavioral axis best forecasts it. |
| `rw_refusalindex` | Anon., RefusalIndex (OpenReview:9gJBhkLRat) | **true** | A clean, rate-invariant refusal-boundary metric, but a single-family instrument evaluated at one time point; not compared against capability/format/calibration/safety drift, nor regressed against a downstream-breakage ground truth across version pairs. |
| `rw_offtopiceval` | Anon., OffTopicEval (OpenReview:EcIyiJrajc) | false | Measures accept/refuse operational safety for a fixed model under fixed policies; does not track how that safety behavior drifts across versions of the same model or ask whether such drift predicts downstream failure of a deployed integration. |
| `rw_bcalibration` | Anon., B-Calibration (OpenReview:0sCyk9Tr5J) | false | Formalizes semantic calibration at a point in time but does not quantify a version-to-version calibration-drift magnitude comparable to drifts on other probe families, nor tie calibration drift to downstream breakage. |
| `rw_tare` | Anon., TARE (OpenReview:YEBDvqsniH) | false (targets prompt optimization, not drift measurement itself) | Demonstrates that point-wise, single-phrasing measurements are brittle to paraphrase — which threatens any single scalar drift score — but targets prompt *optimization* robustness, not the construction of a stable multi-family drift measure or the prediction of downstream breakage. |
| `rw_weightdiff` | Anon., WeightDiff (OpenReview:6As4wfTB77) | false (white-box, different modality) | Explains model change from the parameter side (task vectors), requiring white-box access to both checkpoints; offers no route for an external consumer, who sees only outputs, to detect which observable probe signals forecast breakage after an update ships. |
| `rw_prosafeprune` | Anon., ProSafePrune (OpenReview:QkHKaPfRAB) | false | Establishes that false refusals are systematic and widespread, but as a single-axis diagnostic at one release, does not measure over-refusal *drift* across versions nor weigh it against other axes as a breakage predictor. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but two baseline labels need scrutiny for implying a head-to-head comparison that isn't actually planned.
- comments:
  - `{severity: major, field: "specific_related_works[rw_essencebench].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "EssenceBench's I/O framing is single-benchmark item-subset selection that preserves *score/ranking fidelity* — genuinely different from this paper's cross-family breakage-predictive framing. Marking it a straightforward baseline risks implying EssenceBench's own reported reconstruction-fidelity numbers are being compared against, which they are not; per the stage-3 rubric, a mismatched-I/O work is 'not a baseline in the beat-a-number sense — at best a method-side reference,' unless the borrowed piece is scoped precisely."}`
  - `{severity: minor, field: "specific_related_works[rw_refusalindex].is_potential_baseline", anti_pattern: null, comment: "Similarly, RefusalIndex's own reported index values for any specific model are not what this paper compares against — what's borrowed is the instrument design itself, repurposed as this paper's refusal-family probe and, downstream, as one arm of the single-family-predictor baseline set in Stage 6. Worth stating that precisely so it doesn't read as a results comparison."}`
- decision: `move_to_refiner` (wording-precision fixes, not structural ones — both borrowed pieces are still legitimately usable, just not as beat-a-number baselines).

### Refiner pass

- `rw_essencebench.is_potential_baseline` retained as `true`, but sharpened: "Not a baseline in the beat-a-number sense — EssenceBench's own reported reconstruction-fidelity numbers are not compared against. Its **subset-selection framing** is borrowed as a comparison arm scoped to the capability family only (an item-level compression baseline within `M1`), independent of its published results."
- `rw_refusalindex.is_potential_baseline` retained as `true`, sharpened: "Not a baseline in the beat-a-number sense — RefusalIndex's own published index values are not compared against. Its **rank-invariant instrument design** is borrowed as this study's refusal-family probe itself, and the resulting single-family-predictor arm (refusal drift alone, Stage 6) is what actually serves as an internal comparison baseline."
- `changes_made`: clarified both baselines' roles to avoid an implied results-level comparison against I/O-mismatched or single-time-point prior work.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — every limitation above motivates a Stage 4 sub-problem directly rather than surfacing an independent, testable claim about the *existing* literature that this paper would spend an experiment confirming on its own. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."* This matches `paper.md`'s own Step 6, which contains only mechanism-tier hypotheses (H1–H3) plus two baseline controls (B0, B-alt), no framing-tier RQ.

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C5):

- **`sp_axis_attribution`** — *description:* Determine which of the five behavioral axes' drift, if any, actually governs downstream breakage, net of the fact that several axes may move together. *why_it_is_a_problem:* Without adjudicating this, a team has no principled basis for choosing which axis to re-test after a version bump — the whole practical payoff of the study collapses to "we don't know." *technical_challenge:* A version pair can drift on multiple axes simultaneously with no ground truth telling you a priori which one governs a specific downstream failure; raw pairwise correlations between one family's drift and breakage conflate that family's own signal with whatever it merely shares with correlated families. *source_limitation_ids:* `["lim_essencebench", "lim_refusalindex", "lim_offtopiceval", "lim_bcalibration", "lim_prosafeprune"]` — each cited work is a strong single-axis (or single-metric) instrument, but none is compared against another axis or against a downstream-breakage ground truth.
- **`sp_downstream_breakage_construct`** — *description:* Define "downstream breakage" for a (version pair, task) cell so that it reflects whether the integration actually stops working, not merely how much the raw output text changed. *why_it_is_a_problem:* If breakage is operationalized as raw output distance, a harmless rewording and a fatal schema violation become indistinguishable, corrupting every downstream correlation the study computes. *technical_challenge:* The same magnitude of textual diff can be functionally harmless for one task (a paraphrased explanation) and fatal for another (a broken JSON key), so a single distance-based definition cannot serve tasks with heterogeneous sensitivities without an explicit, task-aware functional check. *source_limitation_ids:* `["lim_bsm"]` — BSM computes a departure signature between releases but never connects it to whether any downstream application actually breaks.
- **`sp_retrospective_corpus`** — *description:* Assemble a corpus of version pairs where both versions remain reliably queryable on the full probe-plus-downstream input set, without the corpus silently shrinking or skewing toward whichever versions happen to still be reachable. *why_it_is_a_problem:* An unpinned or deprecated API endpoint doesn't just add noise — it can quietly remove exactly the pairs a retrospective design most needs, biasing the sample toward survivorship. *technical_challenge:* Providers offer no guarantee of stable historical access or deterministic decoding, so distinguishing "this pair was dropped because a family it drifted on is under-represented" from "this pair was dropped for an unrelated access reason" requires an explicit admission gate, not just best-effort collection. *source_limitation_ids:* `["__novel__"]` — no cited work addresses retrospective-corpus assembly or attrition risk; `WeightDiff`'s white-box framing is adjacent (it motivates *why* an external, black-box route is needed at all) but doesn't touch corpus construction.
- **`sp_family_collinearity`** — *description:* Attribute predictive power to a specific behavioral family net of the fact that the five families are not statistically independent. *why_it_is_a_problem:* A family's raw correlation with breakage can simply be borrowing a correlated family's signal (e.g., safety-behavior shifts often co-occur with refusal-boundary shifts), so reporting raw correlations alone risks crediting the wrong axis. *technical_challenge:* No single statistic separates a family's own marginal contribution from what it shares with the other four; disentangling requires partial correlation or multiple regression, checked against collinearity diagnostics before being trusted. *source_limitation_ids:* `["__novel__"]` — none of the eight cited works addresses cross-family collinearity because none compares more than one family at a time.
- **`sp_instrument_stability`** — *description:* Establish that a measured drift-to-breakage correlation reflects a real behavioral signal, not an artifact of which specific probe items or decoding samples happened to be used. *why_it_is_a_problem:* If the ranking reorders under a different (equally valid) paraphrasing of the same probes, the reported predictive-power ranking says more about instrument choice than about the models being audited. *technical_challenge:* Distinguishing genuine cross-version drift from ordinary within-version decoding noise, and confirming the ranking survives rewording, both require dedicated null-distribution and multi-paraphrase-set machinery that a single-administration design does not provide. *source_limitation_ids:* `["lim_tare"]` — TARE shows point-wise, single-phrasing measurement is brittle to paraphrase, but targets prompt-optimization robustness, not the construction of a stable drift measure.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's three outputs), but two sub-problems risk reading as the same underlying issue stated twice.
- comments:
  - `{severity: minor, field: "sp_axis_attribution / sp_family_collinearity", anti_pattern: "overlap", comment: "Both sub-problems talk about a family's correlation being contaminated by other families. They are genuinely distinct — one is about *whether any axis governs breakage at all* (an identification question, prerequisite to any ranking), the other is about *disentangling correlated families once several show a nonzero correlation* (an identifiability-conditional-on-collinearity question) — but the current phrasing doesn't make that ordering explicit enough, and a reader could merge them into 'account for correlated families' as one problem."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_axis_attribution.technical_challenge` sharpened to end with: "...this is the **identification** step — establishing whether any axis carries signal at all, prior to and independent of how that signal is later apportioned among correlated axes."
- `sp_family_collinearity.technical_challenge` sharpened to end with: "...this is the **identifiability-conditional-on-identification** step — it only applies once `sp_axis_attribution` has established that some signal exists; its job is exclusively to apportion that already-identified signal correctly among the five (possibly correlated) families, not to detect whether signal exists in the first place."
- `changes_made`: made the identification-vs-apportionment distinction explicit in both `technical_challenge` fields so the two sub-problems read as sequential, not redundant.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from a related-work limitation each pointing at one work — `lim_bsm`, `lim_tare` — 1 sourced from five related-work limitations jointly, `["lim_essencebench","lim_refusalindex","lim_offtopiceval","lim_bcalibration","lim_prosafeprune"]`, and 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_axis_ranking_regression`** → targets `sp_axis_attribution`. *proposed_approach:* Administer all five probe families identically pre/post on every version pair, compute a signed per-family drift score, and regress the downstream-breakage ground truth on all five family-drift scores **jointly** in one model, rather than computing five separate univariate correlations. *key_insight:* Reporting only pairwise correlations conflates a family's own signal with whatever it merely shares with correlated families; a single joint-regression fit yields two separately falsifiable estimands — which standardized coefficient is largest (the axis-ranking question) and whether any coefficient's confidence interval excludes zero at all (whether probe drift carries signal in the first place) — one instrument, two readouts, not two mechanisms. *hypotheses:* ["The family with the highest bootstrap-median standardized coefficient in the joint regression will be refusal-boundary or safety-behavior, not capability, with the 95% CI on the top-family-minus-capability coefficient difference strictly above zero.", "At least one family's standardized coefficient will have a 95% CI excluding zero — the joint regression will identify at least one family with non-null predictive power, rather than all five being statistically indistinguishable from a no-signal null."]
- **`m_downstream_functional_ground_truth`** → targets `sp_downstream_breakage_construct`. *proposed_approach:* Define breakage for a (pair, task) cell as one minus the fraction of a shared task input set passing deterministic functional-equivalence checks (schema validity, tool-call executability) combined with a semantic-diff threshold, computed **per task before** any aggregation across the downstream suite. *key_insight:* Anchoring breakage to functional checks the integration actually depends on, rather than raw text distance, is what keeps a harmless rewording from being scored the same as a fatal structural break; computing it per task before pooling is what lets heterogeneous task sensitivities surface instead of being averaged away. *hypotheses:* ["The correlation between per-family drift and per-task breakage will differ meaningfully between at least two tasks with different sensitivities (e.g., a format-sensitive parsing task vs. a calibration-sensitive task), rather than being uniform across the downstream suite — demonstrating breakage is genuinely task-heterogeneous rather than driven by one axis-agnostic factor."]
- **`m_corpus_construction_with_attrition_gate`** → targets `sp_retrospective_corpus`. *proposed_approach:* Anchor the retrospective corpus on version pairs with immutably archived, redistributable checkpoints (open-weight families) as the backbone, treat dated closed-API snapshots as a secondary best-effort stratum, and admit a pair to the corpus only after a walking-skeleton gate confirms both versions remain queryable on the full probe-plus-downstream input set under identical decoding. *key_insight:* The retrospective design's central risk is silent, biased corpus attrition, not just noise — gating admission on a pre-registered reachability check, rather than reporting whatever happens to still be reachable at analysis time, is what prevents survivorship from masquerading as a finding. *hypotheses:* ["Pairs that include a closed-API snapshot which became unreachable during the study will not differ systematically in mean per-family drift magnitude from pairs that remained fully reachable throughout (two-sample test, α = 0.05) — ruling out systematic corpus-attrition bias in the retained sample."]
- **`m_partial_correlation_disentanglement`** → targets `sp_family_collinearity`. *proposed_approach:* After computing all five univariate family-drift-to-breakage correlations, compute each family's partial correlation net of the other four, checking variance-inflation factors before trusting the partials, and report predictive power at the level of the disentangled contribution rather than the raw pairwise correlation alone. *key_insight:* Behavioral axes are not independent (a safety-behavior shift often co-occurs with a refusal-boundary shift), so a family's raw correlation with breakage can simply be borrowing another family's signal; only a VIF-checked partial correlation isolates the family's own marginal contribution. *hypotheses:* ["For at least one of the five families, the raw pairwise correlation and the VIF-checked partial correlation will disagree in relative rank order by at least one position, demonstrating that family collinearity is non-negligible and that reporting raw correlations alone would misattribute predictive power."]
- **`m_noise_and_paraphrase_gate`** → targets `sp_instrument_stability`. *proposed_approach:* Compute a within-version null distribution for each family's drift by re-querying under fixed and re-sampled decoding on the *same* version, requiring any reported cross-version drift to exceed the 95th percentile of that null before it counts toward the ranking; separately, recompute the family predictive-power ranking under at least three independent paraphrase sets of the same probe items and require the ranking to remain stable. *key_insight:* A scalar drift correlation cannot be trusted until it is shown to exceed ordinary decoding noise and to survive rewording — otherwise the "signal" the ranking rests on could be a property of one specific phrasing rather than the behavioral axis itself. *hypotheses:* ["At least 3 of the 5 probe families will show cross-version drift exceeding the within-version noise floor (one-sided permutation test, Holm-corrected across families, α = 0.05), and the resulting family predictive-power ranking will have Kendall τ ≥ 0.70 across at least 3 independent paraphrase sets."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but one method is carrying two headline claims and needs a one-line justification for why that's one mechanism, not two, mirroring a pattern worth checking for explicitly.
- comments:
  - `{severity: minor, field: "m_axis_ranking_regression.hypotheses", anti_pattern: null, comment: "The two hypotheses here (top-family identity, and whether any family clears the non-null bar at all) are the paper's two most central claims about axis attribution. Worth stating explicitly why one regression produces both, so this doesn't read as scope creep folded into a single method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_axis_ranking_regression.key_insight` already states the one-instrument-two-estimands justification in the draft above; refiner pass makes it more precise: "...a single joint-regression specification (`B̄ ~ Σ_f D_f`) yields two distinct, separately falsifiable estimands from one fit: which standardized coefficient is largest (tests the axis-ranking hypothesis) and whether any coefficient's CI excludes zero (tests whether probe drift carries signal at all) — one instrument, two readouts, not two mechanisms, exactly mirroring why a single mixed-effects fit can carry two estimands elsewhere in this literature."
- `changes_made`: sharpened the two-hypotheses-one-method justification so it reads as an explicit design choice rather than an implicit bundling.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (2 + 1 + 1 + 1 + 1 across the five methods respectively — `m_axis_ranking_regression` carries two, per the refiner's one-instrument-two-estimands justification above), mixing instrument-validity claims (corpus attrition, collinearity, noise/paraphrase stability) with the study's headline empirical predictions (axis ranking, task heterogeneity) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Open-weight version-pair corpus (Llama-2→Llama-3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3) — *justification:* immutably archived, redistributable checkpoints; forms the reliable backbone required by `sp_retrospective_corpus`'s admission gate.
- Probe item banks per family (capability: MMLU/GSM8K/BBH; refusal-boundary: XSTest/OR-Bench; format-preference: IFEval + a JSON-schema-compliance set; calibration: MMLU-with-confidence / a semantic-calibration set; safety-behavior: HarmBench/Sorry-Bench/OffTopicEval-style items) — *justification:* one item set per family, each grounded in the related-work instrument it borrows (`rw_refusalindex`, `rw_bcalibration`, `rw_offtopiceval`, `rw_prosafeprune`).
- Downstream-task suite (~20 real tasks: extraction-to-JSON, classification, RAG-answer, tool-call argument filling, moderation) — *justification:* spans tasks with different sensitivities (format-sensitive, calibration-sensitive, safety-sensitive) so `sp_downstream_breakage_construct`'s heterogeneity hypothesis is actually testable rather than assumed.
- (draft initially listed dated closed-API snapshot pairs with justification only "adds coverage of production-deployed systems" — flagged below.)

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Single-probe-family predictors (each family alone) — the necessary comparator for every joint-model claim about which family dominates.
- B0 — constant base-rate breakage predictor using no probe features at all — if no probe beats this, no probe carries signal and the study's basic premise fails; this arm is what justifies the problem exists.
- B-alt — a family-agnostic total-drift scalar (raw output-diff magnitude on the entire probe bank, ignoring family structure) at the same query budget — the rival explanation that "probe drift predicts breakage only because both track how big the update was," which the axis-selectivity claim must beat to mean anything.
- EssenceBench-style item-subset selector applied within the capability family only (compression baseline, `rw_essencebench`, scoped per Stage 3's sharpened role).
- Random / uniform drift-score baseline.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_axis_top_family` | `sp_axis_attribution` | "The family with the highest bootstrap-median standardized coefficient in the joint regression will be refusal-boundary or safety-behavior, not capability, with the 95% CI on the top-family-minus-capability coefficient difference strictly above zero." |
| `rq_any_family_signal` | `sp_axis_attribution` | "At least one family's standardized coefficient will have a 95% CI excluding zero — the joint regression will identify at least one family with non-null predictive power, rather than all five being statistically indistinguishable from a no-signal null." |
| `rq_downstream_heterogeneity` | `sp_downstream_breakage_construct` | "The correlation between per-family drift and per-task breakage will differ meaningfully between at least two tasks with different sensitivities (e.g., a format-sensitive parsing task vs. a calibration-sensitive task), rather than being uniform across the downstream suite — demonstrating breakage is genuinely task-heterogeneous rather than driven by one axis-agnostic factor." |
| `rq_corpus_attrition_bias` | `sp_retrospective_corpus` | "Pairs that include a closed-API snapshot which became unreachable during the study will not differ systematically in mean per-family drift magnitude from pairs that remained fully reachable throughout (two-sample test, α = 0.05) — ruling out systematic corpus-attrition bias in the retained sample." |
| `rq_family_collinearity_partial` | `sp_family_collinearity` | "For at least one of the five families, the raw pairwise correlation and the VIF-checked partial correlation will disagree in relative rank order by at least one position, demonstrating that family collinearity is non-negligible and that reporting raw correlations alone would misattribute predictive power." |
| `rq_noise_paraphrase_gate` | `sp_instrument_stability` | "At least 3 of the 5 probe families will show cross-version drift exceeding the within-version noise floor (one-sided permutation test, Holm-corrected across families, α = 0.05), and the resulting family predictive-power ranking will have Kendall τ ≥ 0.70 across at least 3 independent paraphrase sets." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 5/6 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a generic coverage claim rather than a reason tied to a specific hypothesis this dataset actually stresses.
- comments:
  - `{severity: major, field: "datasets[closed-API snapshots]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'adds coverage of production-deployed systems' says nothing about which RQ needs the closed-API stratum specifically, or why it isn't just extra data volume. `rq_corpus_attrition_bias` is exactly the RQ this stratum should be justified against — closed-API snapshots are the stratum most at risk of becoming unreachable mid-study, which is the precise condition that hypothesis tests for."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "Dated closed-API snapshot pairs (gpt-3.5-turbo-0301/0613/1106, gpt-4-0314/0613, dated Claude snapshots) — *justification:* included specifically as the stratum whose reachability is most at risk of provider-side deprecation during the study, letting `rq_corpus_attrition_bias`'s attrition-bias hypothesis be tested directly on real at-risk pairs rather than assumed away by restricting the corpus to immutable open-weight checkpoints alone."
- `changes_made`: gave the closed-API stratum's inclusion a hypothesis-linked reason instead of a generic coverage note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no specific statistical technique (regression, partial correlation, permutation tests all appear first in stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_downstream_breakage_construct.source_limitation_ids = ["lim_bsm"]` ∈ Stage 3 limitations ✓; `sp_instrument_stability.source_limitation_ids = ["lim_tare"]` ∈ Stage 3 limitations ✓; `sp_axis_attribution.source_limitation_ids` (five ids) all ∈ Stage 3 limitations ✓; `sp_retrospective_corpus` and `sp_family_collinearity` both `["__novel__"]` with stated justification ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (per-family drift score, predictive-power ranking, minimal-sufficient subset) are each reachable: drift scores via all five methods' shared instrumentation, the ranking via `sp_axis_attribution` + `sp_family_collinearity` (+ `sp_instrument_stability` for its reliability), the minimal subset via the Stage 6 experimental design's subset-ablation machinery (carried from `paper.md`'s own RQ_INF_1, not re-litigated here to avoid redundancy per the seed brief) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs; hypothesis count (6) matches RQ count (6) exactly, recounted here as required.

**What was hardest:** as with a mature seed, the recurring tension was **not disagreement about facts** but **scope discipline against `paper.md`'s own already-finished Step 5/6** — repeatedly checking whether a stage-5/6 hypothesis was quietly restating `paper.md`'s H1/H2/H3 rather than adding an instrument-validity claim this schema's structure specifically demands (corpus-attrition bias and family-collinearity rank-disagreement are exactly this: claims `paper.md`'s own Assumptions section (A4, A6) gestures at but never states as its own falsifiable hypotheses).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Revision pass over the three review artifacts (`stage_review.md`, `taste_audit.md`, `design_review.md`). Every finding was enumerated and checked against the current deliverables; findings already applied (and logged as such in `pipeline.md`) are listed for completeness with status only. Historical rounds above are untouched.

**Already applied / logged as resolved (no action this round):**
- `stage_review.md` Stage 2 REVISE (nearest-neighbor BSM paragraph) and Stage 4 REVISE (Falsification-condition lines, all 6 RQs) — present in `paper_draft.md`/`.tex`.
- `stage_review.md` Phase A items 2/4/5/6 (reference cache, H4–H6, aggregation slots + A-gate labels, R1/R2/R3/R6/R8) — fixed in `paper.md`, logged in `pipeline.md`.
- `stage_review.md` Phase G: 3 [major] (RQ1 `|P|≥60` power gate; RQ4 TOST reframing; P0 placebo paragraph) + 2 [moderate] (RQ3 `≥0.15` floor + second contrast; RQ6 minimum-not-mean) — present in both draft files.
- `design_review.md` findings #1–#6 — fixed in `paper.md`/`digest.md` per its own "Fixes applied" log.
- `taste_audit.md` — no action items; 🟢 verdict with a watch-item only (abstract leads with the apparatus, already satisfied).

**Applied this round (5 open findings):**
1. `stage_review.md` Phase G [minor] → four `adjacent`/`background` `selected` cache records were uncited. **Changed:** wove `AdversarialPragmatics1153`, `ElicitBehaviorsMultiTurn3701`, `PrincipalLoyalty0383` into the Single-axis-instruments paragraph and `EvaluatorPrefDynamics0297` into the Instrument-brittleness paragraph, each grounded strictly in its cache `why` string — in `paper_draft.md` + `paper_draft.tex` (all 17 selected records now cited).
2. `design_review.md` finding #7 [NOTE] (re-splice item: "classical concession") → the classical-literature concession added to `paper.md` Step 3 / `digest.md` N3 was never mirrored into the draft. **Changed:** added a "Classical antecedents, conceded" paragraph to Related Work (test-suite minimization / regression test selection; concept-drift detection; concede-and-differentiate delta: deterministic oracle + white-box coverage vs. black-box axis-resolved probabilistic drift), explicitly marked citations-pending-harvest, no fabricated citations — in `paper_draft.md` + `paper_draft.tex`.
3. `design_review.md` fix #6 mirror → the temporal-split forward-validation robustness check added to `paper.md` was absent from both deliverables. **Changed:** added it (reported, not a gate; fit on earlier pairs, evaluate `AUC(S*)`/rank-τ on latest held-out pairs) to `paper_draft.md`/`.tex` Experimental Setup ("Reported robustness and cost accounting") and to `experiment_design.md` (new "Reported robustness checks and cost accounting" section).
4. `design_review.md` "Missing RQs" item (cost/overhead accounting; review's own remedy: "just a reporting table", no design change) → **Changed:** pre-registered a deterministic cost-accounting table (queries / USD / wall-clock per version bump, `S*` vs. full downstream re-test) in `paper_draft.md`/`.tex` and `experiment_design.md`. Deliberately *not* added as a new RQ — the pre-registered 6-RQ set and its hypotheses are untouched.
5. `design_review.md` "Missing RQs" item (per-family probe-labeler validity; review's own remedy: "left as a limitation to state") → **Changed:** stated it as the Conclusion's third limitation ("Two limitations" → "Three limitations": probe-labeler judgments do not get the `B(p,t)` classifier's full κ≥0.7 R2 plan) in `paper_draft.md`/`.tex`, with a matching note in `experiment_design.md`.

**Rejected as moot (1):**
- `stage_review.md` Phase G [minor] RQ-numbering mismatch between `paper_draft` (presentation order) and `paper.md` (discovery order) — the review itself concludes this is a deliberate, verified-lossless renumbering, "noted for completeness, not flagged as a fix". No change.

**Verification:** `latexmk -pdf` clean (exit 0, 16 pages, 0 undefined citations). Cross-deliverable consistency re-checked: 6 RQs in both `paper_draft.md` and `experiment_design.md`; `|P| ≥ 60` floor + EXPLORATORY/INCONCLUSIVE/CONFIRMATORY tiers, `π_top ≥ 0.30`, `≥0.15` heterogeneity floor, `Δ_eq = ±0.5 SD` TOST margin, Kendall `τ ≥ 0.70` minimum-not-mean, `δ = 0.03` (H2 scope note) all matching; target hypotheses in `experiment_design.md` untouched (byte-identical to `paper.md`'s).
