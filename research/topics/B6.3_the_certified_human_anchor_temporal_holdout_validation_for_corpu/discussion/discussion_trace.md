# Discussion Trace — B6.3 (`auto-research-discussion`, Stages 1-6)

> Extracted verbatim from `pipeline.md` (this is the complete round-by-round critic/refiner record — every draft, critique, decision, and refiner pass across all six stages, plus the final cross-stage consistency check). `pipeline.md` itself now retains only the Phase Log (goal.md phase-gate tracking) and a pointer to this file. See `experiment_design.md` for Stage 6's confirmed output rendered as a standalone, executable protocol.


> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B6.3**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries its own formal notation, assumptions A1–A6, and pre-registered fallbacks), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure what error bound a pre-2022 "certified-human" text corpus can actually license as a calibration anchor for corpus-level AI-content estimators, and how much of that bound is eroded by ordinary secular drift in human writing style rather than by genuine AI contamination.
- **Apparent inputs:** existing corpus-level AI-content estimators (per-document detectors plus a mixture-based prevalence estimator) at fixed decision thresholds; human-authored text with reliable publication-year metadata spanning multiple years before (and some after) a designated ~2022 cutoff; the cutoff date itself.
- **Apparent outputs:** a per-year-bucket false-positive-rate reading per estimator; a fitted drift trend relating FPR to temporal distance from the cutoff; an explicit validity envelope (time window / genre / domain) bounding when the anchor's implied error guarantee holds; the bias this drift propagates into a downstream prevalence estimate.
- **Closest research areas:** corpus-level AI-content prevalence estimation (MonitorAIScale's mixture framework); temporal concept-drift / longitudinal benchmark validation (LAMDA); contamination/membership-detector assumption fragility under distribution shift (BenchContamFragility, Min-K%++, ContamICL); per-document zero-shot and rewrite-based detection (DetectGPT, Learn-to-Distance, Disrupt-and-Recover).
- **In scope:** auditing the temporal validity of an existing methodological convention (the pre-2022 human anchor) using existing detectors and one existing prevalence estimator as instruments. **Out of scope:** training or proposing a new detector; fixing the drift (e.g., a drift-robust estimator) — the contribution is the measured bound and envelope, not a repair; per-document authorship certification at scale.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already carries its own cross-referenced ids (N-node ↔ M-component ↔ RQ) and its own asymmetry/taste self-check (`paper.md` Steps 0 and 3). Reconstruction risk is low; the risk is redundancy with `paper.md`'s own Steps 5/6 — stages 5/6 below are framed to validate the **measurement instrument's own properties** (does the disentanglement hold up, is the envelope construction load-bearing) rather than re-deriving `paper.md`'s already-designed hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a battery of existing corpus-level AI-content estimators (per-document detectors and a mixture-based prevalence estimator) run at fixed decision thresholds, and given human-authored text with reliable publication-year metadata spanning multiple years before and after a designated ~2022 cutoff, determine what false-positive-rate bound the pre-2022 portion of that text actually licenses as a "certified-human" calibration anchor, as a function of temporal distance from the cutoff, and whether that bound is eroded by ordinary secular drift in human writing style rather than by genuine AI contamination.
- `input`: (1) a battery of existing corpus-level AI-content estimators at fixed decision thresholds; (2) human-authored text with reliable publication-year metadata spanning multiple years before (and some after) a designated cutoff, drawn from a small number of continuously-archived sources; (3) the designated cutoff date itself.
- `output`: (1) a per-year-bucket empirical false-positive-rate reading for each estimator; (2) a fitted drift trend (slope and significance) relating FPR to temporal distance from the cutoff; (3) an explicit validity envelope (time window / genre / domain) within which the anchor's implied error bound is licensed; (4) the bias this drift propagates into a downstream mixture-based prevalence estimate when the human reference is swapped across ages.
- `constraints`: year-bucket comparisons must hold source, genre, and per-year token budget fixed so that year is not confounded with topic; every document treated as anchor material must carry a hard archival timestamp predating the cutoff; detector thresholds must be frozen on a held-out calibration split disjoint from all evaluation years before any evaluation FPR is computed.
- `objective`: a validity-envelope claim is correct only if it states a confidence level and is defended against the two rival explanations for any observed FPR-vs-year slope — year-correlated corpus-composition drift and undetected AI-content leakage into nominally pre-cutoff buckets — not merely a slope estimate with no such disambiguation.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 and `paper.md` Step 2 both already classify this as a measurement study of an existing convention, not a proposal for a new detector, dataset, or theorem.

**critique:**
- summary: Strong, evidence-traceable draft, but the summary quietly forecloses one of the problem's own named confounds, and one constraint bakes in a method choice rather than stating a boundary.
- comments:
  - `{severity: major, field: "summary", anti_pattern: "fields_misaligned (a framing that presupposes its own answer)", comment: "The summary asks whether the bound is 'eroded by ordinary secular drift in human writing style rather than by genuine AI contamination' — a false dichotomy. Digest N5's own C1 names *three* candidate explanations for an observed FPR-vs-year slope: (a) genuine style drift, (b) undetected AI-content leakage into nominally pre-2022 buckets, and (c) staleness of the estimator itself. Presupposing a two-way drift-vs-contamination choice quietly forecloses (b) and (c) — exactly the alternatives paper.md's own B-alt composition-matched arm and pre-2018 sub-range control are built to rule out. The problem statement should stay neutral about which explanation holds, not bake in an answer before any measurement is taken."}`
  - `{severity: major, field: "constraints", anti_pattern: "method_leak", comment: "'must hold source, genre, and per-year token budget fixed' names a specific mitigation technique (token-budget matching), not a boundary of the problem itself. The real constraint is that *any* FPR-vs-year comparison is only interpretable among comparably-composed samples — composition confound is a genuine risk the problem setting must not assume away — but the *how* (token-budget matching) is a method decision that belongs in Stage 5, not a fact about the problem."}`
- decision: `move_to_refiner` (both are precision fixes using content already in the digest/paper.md — no new content needed).

### Refiner pass

- `summary` (refined): "...determine what false-positive-rate bound the pre-2022 portion of that text actually licenses as a 'certified-human' calibration anchor, as a function of temporal distance from the cutoff, **and which of three candidate mechanisms — genuine secular drift in human writing style, undetected AI-content leakage into nominally pre-cutoff buckets, or staleness of the estimator itself — accounts for any bound erosion observed.**" (removes the two-way presupposition; names all three candidates neutrally, matching digest N5/C1).
- `constraints` (refined): "any FPR-vs-year comparison is only informative among samples that are otherwise comparably composed — an apparent temporal trend that is really a byproduct of which topics/genres happen to dominate older vs. newer text would not be evidence about time itself; every document treated as anchor material must carry a hard archival timestamp predating the cutoff; detector thresholds must be frozen on a held-out calibration split disjoint from all evaluation years before any evaluation FPR is computed." (keeps the composition-confound boundary as a stated risk, removes the token-budget-matching method choice).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, using notation already present in `paper.md` Step 5 but restated at problem-definition granularity only — no modeling choice included): "Let y* denote the certification cutoff and Δ(y) = y* − y the temporal distance of year-bucket y. For each estimator D_k, let FPR_k(y) denote its false-positive rate on certified pre-y* text drawn from bucket y. The problem is to characterize FPR_k(y) as a function of Δ(y); attribute any nonzero relationship among {style drift, composition confound, content leakage, estimator staleness}; and report the largest envelope E = {y : an upper confidence bound on FPR_k(y) stays within a stated tolerance of the nominal calibrated rate}, together with the bias this induces in a downstream mixture-based prevalence estimate π̂ when the human reference is swapped across buckets."
- `changes_made`: removed a presupposed two-way dichotomy from `summary`; removed a method choice from `constraints`, replacing it with the boundary it was meant to protect; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Treating pre-2022 human text as a costless, self-certifying negative anchor is now load-bearing for an entire emerging research line — corpus-level AI-content prevalence estimation — precisely because it lets researchers avoid per-document ground truth; but if that anchor's implied error guarantee quietly decays with the ordinary passage of time, every downstream prevalence estimate built on it inherits an unstated and directional bias.
- `why_it_matters`: As detection research shifts from unreliable per-document classification to corpus-level prevalence estimates (following `[MonitorAIScale, OpenReview:bX3J7ho18S]`'s reframing of the problem as a mixture-estimation task), the human reference distribution used to define "prevalence" becomes the single most load-bearing ingredient of the whole method — yet its validity is asserted by convention (any text safely predating ChatGPT's release is "clean"), never measured. If human writing style itself drifts over the calendar years the anchor spans, the anchor licenses a systematically time-varying false-positive rate rather than the flat guarantee researchers implicitly assume when they treat "pre-2022" as one undifferentiated pool. This is not a one-off calibration nuisance: because the corpus-level estimand mixes the anchor into every future measurement, an aging anchor's drift propagates forward into every subsequent prevalence estimate that reuses it, silently inflating apparent AI-content growth over time even if the true AI fraction were flat — a systematic measurement artifact, not sampling noise.
- `who_cares`: Researchers building or reusing corpus-level AI-content estimators who need to know whether their calibration convention stays safe as models and corpora age further past 2022; venues, institutions, and platforms relying on prevalence estimates ("X% of submissions were AI-assisted") as evidence for policy or enforcement decisions; the broader contamination-detection literature that treats "seen vs. unseen" or "human vs. AI" gaps as stable analytic devices without auditing their own temporal shelf life.
- `evidence`: `[MonitorAIScale, OpenReview:bX3J7ho18S]`'s own mixture framework fits a single mixing coefficient against a fixed human reference distribution without ever testing whether that reference's era matters; `[BenchContamFragility, OpenReview:bhR00j6Mku]` and `[MinKpp, OpenReview:ZGkfoufDaU]` both show, in the adjacent membership/contamination setting, that "seen vs. unseen" separability collapses precisely as the two compared distributions converge or shift — of which the gap between a pre-2022 anchor and a present-day corpus is an unaudited instance; digest N3's own search-honesty note (11,683 records searched) confirms no corpus paper directly performs this temporal-holdout audit, itself evidence the question is open rather than already settled.

**critique:**
- summary: Good stake-specific motivation with real citations, but one of Stage 1's four outputs is under-motivated relative to the others.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (1) is a *per-year-bucket* FPR reading, not a single pooled number. why_it_matters motivates why the validity envelope and the propagated bias matter, but never explains why year-indexed granularity specifically is needed, as opposed to one aggregate FPR measured across all pre-2022 text at once. A reader could reasonably ask 'why not just check whether pre-2022 text as a whole has near-zero FPR and be done' — which is a real, unaddressed gap, and it matters because paper.md's own envelope construct (E_k(ε,δ)) is only definable at all if FPR is tracked year-by-year."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a single pooled FPR number computed across the entire pre-2022 span cannot distinguish 'the anchor is uniformly and slightly noisy throughout' from 'the anchor is safe for recent years but already unsafe for the oldest ones' — exactly the difference between a flat guarantee and a validity envelope with a real, locatable boundary. Only a year-indexed reading can find where that boundary actually sits, which is precisely the information a downstream user needs before deciding how far back into the pre-2022 pool they can safely draw a human reference corpus — a pooled audit answers 'is there a problem on average,' not 'where does the anchor stop being safe,' and only the latter is actionable."
- `changes_made`: added the year-indexed-vs-pooled coverage argument, closing the gap on Stage 1 output (1).
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (search performed over 11,683 corpus records from five angles; no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / role / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_monitoraiscale` | Anon., MonitorAIScale (OpenReview:bX3J7ho18S) | true (the estimator whose own temporal bias is measured) | Fits a single mixing coefficient against a fixed human reference distribution and treats it as unproblematic ground truth; never tests whether the reference's temporal composition confounds the estimated AI fraction. |
| `rw_lamda` | Anon., LAMDA (OpenReview:1FnCrZtBNQ) | false (different domain: malware detection, not text) | Establishes the temporal-holdout, year-stratified validation template and shows naive temporal evaluation inflates performance estimates, but targets accuracy decay in a fixed feature space, not a calibrated FPR bound for a text negative-anchor. |
| `rw_benchcontamfragility` | Anon., BenchContamFragility (OpenReview:bhR00j6Mku) | false (stress-tests detector families, doesn't bound a rate) | Shows seen/unseen separability breaks under staged post-training across detector families, but stops at the diagnosis and never turns it into an explicit FPR bound as a function of temporal distance. |
| `rw_markovcalib` | Anon., MarkovCalib (OpenReview:Lzwkeg2o2z) | false (calibration layer, not an instrument in this study's battery) | Shows detector calibration is brittle under paraphrasing/distribution shift at the mechanism level, but doesn't isolate *temporal* shift in the human reference as a distinct, separately-bounded axis. |
| `rw_detectgpt` | Mitchell et al., DetectGPT (OpenReview:UiAyIILXRd) | **true** | Zero-shot curvature detector validated on contemporaneous human/AI samples; its FPR on temporally distant human text is uncharacterized. |
| `rw_learntodistance` | Anon., Learn-to-Distance (OpenReview:2ZUPeEM3FH) | **true** | Rewrite-based detector whose likelihood-based signal is known to degrade under prompt/domain shift; temporal shift specifically is never isolated. |
| `rw_minkpp` | Zhang et al., Min-K%++ (OpenReview:ZGkfoufDaU) | false | Shows membership-detection reliability collapses as reference and target distributions converge, the general phenomenon of which temporal drift toward the present is an unaudited special case. |
| `rw_contamicl` | Anon., ContamICL (OpenReview:YlpaaYxx4t) | false | Motivates collection-level over instance-level contamination detection because sample-level signals are confounded by distribution shift, but doesn't isolate temporal distance as the shift axis. |
| `rw_dnr` | Anon., Disrupt-and-Recover (OpenReview:FiMZSxo4DO) | **true** | Single-call black-box recovery detector for closed-model, low-query settings; like the other detectors, its temporal-shift FPR is uncharacterized. |

**critique:**
- summary: Grounding is solid and every limitation is specific, but three works marked `is_potential_baseline: true` risk being read as "comparators to beat," which would be a tier violation for an `empirical` study.
- comments:
  - `{severity: major, field: "specific_related_works[rw_detectgpt, rw_learntodistance, rw_dnr].is_potential_baseline", anti_pattern: "io_approach_mismatch (role mislabeling, not I/O mismatch per se)", comment: "Marking these three 'true' without qualification implies a beat-a-number comparison, which Stage 1's study_type=empirical explicitly forbids at Stage 6. These three detectors are not being outperformed by anything here — they are the *instruments* whose own FPR is the measured quantity (the estimator battery, digest M2). The field needs the same disambiguating note this paper's own B5.5-adjacent precedent used for a borrowed protocol: 'not a baseline in the beat-a-number sense.'"}`
  - `{severity: minor, field: "specific_related_works[rw_monitoraiscale].is_potential_baseline", anti_pattern: null, comment: "MonitorAIScale's role is actually more specific than 'baseline' — it is not run per-bucket like the three detectors above (that would just give it another FPR reading); it is the direct object of the bias-propagation test (reference-year swapping, digest M6), a distinct role from the detector battery. This should be stated explicitly, not folded into the same 'true' label as the other three."}`
- decision: `move_to_refiner`.

### Refiner pass

- `rw_detectgpt`, `rw_learntodistance`, `rw_dnr`: `is_potential_baseline` retained as `true`, but each field's note is sharpened: "Not a baseline in the beat-a-number sense — `study_type: empirical` means no detector's own published performance claims are being compared against or beaten. Each detector's **decision rule** is borrowed as one arm of the estimator battery (digest M2) whose FPR on year-stratified anchor text is itself the measured quantity, independent of how well it detects AI text in its own original evaluation."
- `rw_monitoraiscale`: note sharpened to distinguish its role from the three detectors above: "Not a battery member measured per-bucket like the instance-level detectors — it is the direct object of the bias-propagation test (RQ `rq_reference_swap_bias` below): its human reference is deliberately swapped across ages, with the resulting shift in its own output the measured quantity."
- `changes_made`: clarified all four `is_potential_baseline: true` entries' roles to avoid an implied outcome-tier comparison, and distinguished MonitorAIScale's distinct role from the three-detector battery.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_benchcontamfragility`/`rw_minkpp`/`rw_contamicl`'s shared limitation, "diagnosis stops at the seen/unseen axis, never becomes an explicit bound") is not a distinct framing check but restates this paper's own core question, already covered end-to-end as mechanism-tier RQs in Stage 6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one novel decisive component):

- **`sp_confound_disentanglement`** — *description:* Attribute an observed FPR-vs-year slope to one of three candidate mechanisms — genuine secular stylistic drift, undetected AI-content leakage into nominally pre-2022 buckets, or staleness of the estimator itself. *why_it_is_a_problem:* the paper's central causal claim (that style drift specifically erodes the anchor) is only meaningful if these three are told apart; conflated, "drift" becomes a label for any of three different phenomena. *technical_challenge:* an FPR-vs-year curve alone cannot distinguish the three — they produce observationally identical monotone trends; disentangling requires independent controls each immune to exactly one alternative. *source_limitation_ids:* `["rw_benchcontamfragility", "rw_minkpp", "rw_contamicl"]` (the shared limitation that diagnosis stops at the seen/unseen axis without a temporal bound).
- **`sp_purity_unverifiability`** — *description:* Bound the residual impurity of a "certified-human" label, given that per-document ground truth for authorship is fundamentally unverifiable at corpus scale. *why_it_is_a_problem:* if certification itself leaks, any measured FPR conflates detector error with genuine mislabeled contamination, undermining the premise that "false positive" means "wrongly flagged genuinely-human text." *technical_challenge:* there is no scalable oracle for authorship; timestamp metadata is a proxy, not a certification, and spot-checking can only bound, never eliminate, residual impurity. *source_limitation_ids:* `["__novel__"]` — no cited work needs to solve this because none of them scores the *purity* of their own human reference in the first place.
- **`sp_composition_confound`** — *description:* Separate the effect of calendar year itself from the confound that older text in most available corpora skews toward different genres/topics/lengths than newer text. *why_it_is_a_problem:* without this, an "FPR increases with age" finding could be entirely explained by "older buckets happen to be more formal/book-like," collapsing the study's central claim into a genre artifact rather than a temporal one. *technical_challenge:* composition and year co-vary in almost every available continuously-archived corpus; disentangling requires either a single-source design with matched budgets or an explicit composition-matched resampling control, and neither is guaranteed to fully succeed. *source_limitation_ids:* `["__novel__"]` — LAMDA (`rw_lamda`) establishes the temporal-holdout template but works in a fixed malware feature space with no analogous genre/topic confound; this specific text-corpus confound is not addressed by any cited work.
- **`sp_bias_propagation`** — *description:* Translate a per-document FPR drift signal into a quantified bias on the corpus-level AI-fraction estimate a downstream mixture-based prevalence estimator actually reports. *why_it_is_a_problem:* per-document drift is not automatically informative about what end users consume — the object that matters practically is a corpus-level prevalence number, so the paper's real-world stakes hinge on showing drift propagates (or doesn't) into that number, not just into an intermediate detector statistic. *technical_challenge:* the mixing coefficient is a nonlinear function of the whole reference distribution, not a simple linear pass-through of per-document FPR, so propagation must be measured directly (holding the target fixed, swapping reference age) rather than inferred analytically from the FPR slope alone. *source_limitation_ids:* `["rw_monitoraiscale"]` (its limitation: never tests whether the human reference's temporal composition confounds the estimated AI fraction).
- **`sp_envelope_calibration`** — *description:* Turn a fitted drift estimate into a defensible boundary condition — a stated time window / genre / domain envelope — rather than either an unbounded universal claim or an arbitrary cutoff. *why_it_is_a_problem:* the paper's actual deliverable is not "drift exists" but a usable validity envelope a future researcher can apply when choosing how far back to draw a human reference; without a principled way to set that boundary, the finding can't be operationalized. *technical_challenge:* per-year sample sizes shrink for older buckets, widening confidence intervals, so drawing the boundary at the first point a raw p-value crosses 0.05 risks confusing under-power with genuine safety — the boundary must be defined against a pre-declared confidence-interval tolerance, not a raw significance threshold. *source_limitation_ids:* `["__novel__"]` — LAMDA's protocol template informs *how* to structure a temporal-holdout evaluation (already credited above and in Stage 3), but not how to define a confidence-bounded validity envelope on a rate estimate specifically, which is decisive for this paper's Contribution CO3 and is addressed by no cited work.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's four outputs), but two sub-problems risk reading as the same underlying issue restated.
- comments:
  - `{severity: minor, field: "sp_confound_disentanglement / sp_composition_confound", anti_pattern: "overlap", comment: "Both are ultimately about 'is the observed slope really what it looks like,' which can read as the same sub-problem twice. They are genuinely distinct — one is a *causal-attribution* question among three substantive, competing accounts of a real phenomenon (assuming the measurement itself is sound); the other is an *internal-validity* question about whether the measurement is even measuring time at all, or a sampling artifact of corpus assembly — but the descriptions don't make that logical priority (composition confound must be ruled out before causal attribution is even meaningful) explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_composition_confound.technical_challenge` sharpened to end with: "...this is a **construct-validity** problem, prior to and distinct from the causal-attribution problem in confound disentanglement: if composition is not matched, the FPR-vs-year 'trend' may not be a temporal signal at all, in which case asking *which* temporal mechanism explains it is premature."
- `sp_confound_disentanglement.why_it_is_a_problem` sharpened to end with: "...this attribution question is only meaningful once the trend is confirmed to be a genuine temporal signal in the first place (see composition confound) — the two sub-problems are sequenced, not redundant: composition-matching validates that there is a real trend to explain; disentanglement decides which of three real-phenomenon accounts explains it."
- `changes_made`: made the construct-validity-vs-causal-attribution sequencing explicit in both `technical_challenge`/`why_it_is_a_problem` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_disentanglement_controls`** → targets `sp_confound_disentanglement`. *proposed_approach:* Run three independent controls, each immune to exactly one rival explanation: (i) restrict the drift regression to years ≤2018, immune to leakage from cutoff-adjacent buckets by construction; (ii) inject graded synthetic lexical/syntactic perturbations into a single fixed year's human sample and check whether flag rate rises monotonically with intensity, establishing that style-like change alone can move the statistic; (iii) require the slope's sign to replicate across a majority of independently-designed detector families, ruling out single-estimator staleness. *key_insight:* no single statistic separates three co-occurring explanations, but each control is built to be blind to exactly one of them, so requiring survival across all three narrows the explanation to genuine style drift by elimination rather than by assumption. *hypotheses:* `["The FPR-vs-year slope remains significant and same-signed when the drift regression is restricted to years at or before 2018 (a sub-range immune to post-2022-adjacent leakage by construction), for at least 2 of the 3 tested detector families.", "Synthetic-drift injection — graded lexical/syntactic perturbation applied to a single fixed year's human sample — produces a monotone increase in flagged rate with perturbation intensity, for at least 2 of the 3 tested detector families, replicating the sign of the slope observed on real year-to-year data."]`
- **`m_purity_bounding`** → targets `sp_purity_unverifiability`. *proposed_approach:* Restrict anchor construction to sources with hard, third-party archival timestamps, then draw a small human-audited spot-check sample per source to estimate a residual mislabeling/impurity rate, and report all downstream FPR bounds as FPR ± impurity rather than as if purity were exact. *key_insight:* purity can't be certified exactly at corpus scale, but the uncertainty it contributes can be bounded and folded into the reported error bound instead of silently assumed away — the paper's own central methodological move (bound, don't assume) applied recursively to its own anchor. *hypotheses:* `["A human-audited spot-check of the hard-timestamped anchor sources estimates a residual mislabeling/impurity rate below 1%, keeping the impurity contribution to the reported FPR bound smaller than the magnitude of any detected drift effect."]`
- **`m_composition_matching`** → targets `sp_composition_confound`. *proposed_approach:* Fix a single continuously-archived source per experiment so year is the only structural variable, match token budget and sample size per year bucket, and additionally re-run the drift regression on a composition-matched resample that equalizes topic-cluster and document-length distribution across buckets. *key_insight:* composition and year are correlated in nearly every real corpus, so the only way to know whether year is doing causal work rather than topic mix is to build a comparison where composition cannot vary, and check whether the effect survives. *hypotheses:* `["The FPR-vs-year slope detected in the raw single-source arm survives — same sign, comparable magnitude, and still significant at the pre-registered threshold — in a composition-matched resampled arm that equalizes topic-cluster and document-length distribution across year buckets."]`
- **`m_reference_swap_estimator`** → targets `sp_bias_propagation`. *proposed_approach:* Hold a target corpus fixed and swap only the human reference bucket fed into the mixture-based prevalence estimator across ages, reading off the resulting shift in the estimated AI-fraction directly, rather than inferring it analytically from the per-document FPR slope. *key_insight:* the mixing coefficient is a nonlinear function of the whole reference distribution, so the only way to measure how much anchor age matters to the number end users actually consume is to intervene on the reference directly and observe the corpus-level estimate move, holding everything else fixed. *hypotheses:* `["Swapping the human reference fed into the mixture-based prevalence estimator from a recent bucket to a temporally distant one, with the target corpus held fixed, shifts the estimated AI-fraction by a nonzero, sign-consistent amount across held-out targets of known and unknown composition."]`
- **`m_confidence_bounded_envelope`** → targets `sp_envelope_calibration`. *proposed_approach:* Define the validity envelope not as the first year a raw p-value crosses significance, but as the largest contiguous year-range whose upper confidence bound on FPR stays within a pre-declared tolerance of the nominal calibrated rate, explicitly separating "not enough data to detect drift" from "enough data to certify safety." *key_insight:* a rate estimate's confidence-interval width is itself information about whether a boundary is genuinely certified or merely unmeasured, so building the envelope's edge from the confidence bound rather than the point estimate keeps the two failure modes (unsafe vs. merely under-sampled) from being silently conflated. *hypotheses:* `["The validity envelope defined by requiring the upper confidence bound on FPR to stay within a pre-declared tolerance of the nominal calibrated rate is strictly narrower than the envelope obtained from a naive raw-significance-threshold construction, for at least one tested source/genre — demonstrating the confidence-bound construction is load-bearing, not equivalent to the naive one."]`

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and most hypotheses carry an explicit magnitude threshold, but one hypothesis is under-specified relative to the rest of the set.
- comments:
  - `{severity: major, field: "m_reference_swap_estimator.hypotheses", anti_pattern: "unfalsifiable_hypothesis (borderline — technically falsifiable, but with a bar low enough to pass almost by construction)", comment: "'a nonzero, sign-consistent amount' sets a bar that ordinary sampling noise alone could clear, unlike every other method in this set, which states an explicit floor (below 1%, immune-to-leakage restricted regression, matched-arm survival). Without a stated minimum effect size and a formal significance procedure, this is not yet a real test of whether anchor age matters *at a magnitude anyone would act on* — it would pass even if the true effect were negligible."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_reference_swap_estimator.hypotheses` (refined): `["Swapping the human reference fed into the mixture-based prevalence estimator from a recent bucket to the most temporally distant tested bucket (temporal distance ≥ 8 years), with the target corpus held fixed, shifts the estimated AI-fraction by at least 2 percentage points in the positive (older-reference-inflates-AI-fraction) direction, significant under a paired permutation test at α = 0.05 across held-out targets of both known and unknown composition."]`
- `changes_made`: replaced the vague magnitude with an explicit floor (2 percentage points), direction, and test procedure — pulled directly from the already-designed pre-registered spec in `paper.md` Step 6 (E3/H3), not fabricated fresh; authoring a stated design target with a rationale already present in the seed material is exactly the kind of formalize-for-free move the refiner is meant to make.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (2 + 1 + 1 + 1 + 1 across the five methods respectively).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The detector battery and MonitorAIScale are instruments under measurement, not competitors; the controls below are validity gates and rival-explanation checks, never a leaderboard.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- arXiv abstracts, 2007–2022, single continuously-archived source — *justification:* primary pilot source; hard timestamps satisfy the purity/leakage constraints directly and provide ≥8 pre-2018 years needed for the leakage-immune sub-range control.
- CC-News / dated news archive — *justification:* scale-up genre with faster topical churn, used to stress-test whether the composition-matching method and the drift result generalize beyond formal academic prose.
- Project Gutenberg (dated by first publication) — *justification:* extends the anchor's temporal depth well beyond what any recent corpus offers, testing whether the confidence-bounded envelope genuinely narrows for very old buckets or merely reflects thinner samples.
- Reddit / Pushshift comments (post-date stratified) — *justification:* an informal, high-topic-churn genre used as an additional composition-matching stress test and to diversify the genre coverage the validity envelope must eventually bound.
- HC3 (Human-ChatGPT Comparison Corpus) — *justification:* supplies the AI-side reference needed to build a known-ground-truth mixed target corpus for the reference-swap bias test, where the true AI fraction is known by construction.
- (draft initially listed RAID with justification only "digest mentions it as a sanity-checking benchmark" — flagged below.)

`baselines` (sanity-check / validity-gate comparators, not outcome-tier competitors):
- Anchor-as-asserted control (B0) — current practice: assume the nominal calibrated FPR holds uniformly across the whole pre-2022 span; the paper's premise only has stakes if this control is actually violated.
- Year-shuffle placebo — permute year labels within a source and re-fit the drift model; the placebo slope must be null, or the measurement pipeline itself is producing an artifact, a validity gate on the instrument rather than a competitor.
- Composition-matched resampled arm (from `m_composition_matching`) — the load-bearing rival-explanation control, not a competitor to beat.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_pre_llm_subrange` | `sp_confound_disentanglement` | "The FPR-vs-year slope remains significant and same-signed when the drift regression is restricted to years at or before 2018 (a sub-range immune to post-2022-adjacent leakage by construction), for at least 2 of the 3 tested detector families." |
| `rq_synthetic_drift_injection` | `sp_confound_disentanglement` | "Synthetic-drift injection — graded lexical/syntactic perturbation applied to a single fixed year's human sample — produces a monotone increase in flagged rate with perturbation intensity, for at least 2 of the 3 tested detector families, replicating the sign of the slope observed on real year-to-year data." |
| `rq_purity_spotcheck` | `sp_purity_unverifiability` | "A human-audited spot-check of the hard-timestamped anchor sources estimates a residual mislabeling/impurity rate below 1%, keeping the impurity contribution to the reported FPR bound smaller than the magnitude of any detected drift effect." |
| `rq_composition_matched_survival` | `sp_composition_confound` | "The FPR-vs-year slope detected in the raw single-source arm survives — same sign, comparable magnitude, and still significant at the pre-registered threshold — in a composition-matched resampled arm that equalizes topic-cluster and document-length distribution across year buckets." |
| `rq_reference_swap_bias` | `sp_bias_propagation` | "Swapping the human reference fed into the mixture-based prevalence estimator from a recent bucket to the most temporally distant tested bucket (temporal distance ≥ 8 years), with the target corpus held fixed, shifts the estimated AI-fraction by at least 2 percentage points in the positive (older-reference-inflates-AI-fraction) direction, significant under a paired permutation test at α = 0.05 across held-out targets of both known and unknown composition." |
| `rq_envelope_conservatism` | `sp_envelope_calibration` | "The validity envelope defined by requiring the upper confidence bound on FPR to stay within a pre-declared tolerance of the nominal calibrated rate is strictly narrower than the envelope obtained from a naive raw-significance-threshold construction, for at least one tested source/genre — demonstrating the confidence-bound construction is load-bearing, not equivalent to the naive one." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 6 (E1–E3, A1–A6) numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[RAID]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it' says nothing about which RQ needs it or why. As written it reads like padding rather than a load-bearing design choice."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "RAID (Robust AI Detection benchmark) — *justification:* used exclusively as a pre-registered instrument-validity check — before any threshold is frozen on the calibration split (Assumption A4), each of the three instance-level detectors is confirmed to reproduce its expected ROC behavior on RAID's known-clean human/AI samples. This underwrites A4 (no threshold leakage), which every mechanism-tier RQ in this design depends on; it is not a claim-bearing dataset for any RQ's result."
- `changes_made`: gave RAID's inclusion a role-linked reason (instrument validation feeding a named assumption) instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique. (The Stage 1 critique round explicitly caught and removed one method leak from `constraints` — see refiner pass above.)
2. **ID stability** — no id renamed mid-run; `rw_*` / `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_confound_disentanglement.source_limitation_ids = ["rw_benchcontamfragility","rw_minkpp","rw_contamicl"]` ∈ Stage 3 ✓; `sp_bias_propagation.source_limitation_ids = ["rw_monitoraiscale"]` ∈ Stage 3 ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (per-year FPR reading, drift trend, validity envelope, propagated bias) are each reachable: FPR reading/drift trend via `sp_confound_disentanglement` + `sp_composition_confound` (+ `sp_purity_unverifiability` for the uncertainty that bounds them), validity envelope via `sp_envelope_calibration`, propagated bias via `sp_bias_propagation` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** the recurring tension, as with the B5.5 exemplar, was **not disagreement about facts** (the seed material is unusually well-specified — `paper.md` already carries formal notation, six assumptions with stated failure modes, and three pre-committed fallback wordings) but **scope discipline against redundancy with `paper.md`'s own Step 6**: repeatedly checking whether a Stage 5/6 hypothesis was quietly restating an already-finished design decision rather than adding something this schema's structure specifically demands (e.g., the instrument-validity claim about the confidence-bound envelope being load-bearing relative to a naive construction, which `paper.md` builds but never states as a falsifiable hypothesis in its own right).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: revision pass over the three review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists for this topic). Every finding in those files was enumerated and checked against the current deliverables; findings already applied and logged are listed as verified, open ones were applied below. A prior attempt at this pass was interrupted before writing anything (verified: no prior revision-round section or Phase Log row existed).

1. **stage_review.md § Stage 2 (REVISE — nearest-neighbor sentence)** → verified already applied: the MonitorAIScale nearest-neighbor/delta sentence opens both the Introduction's related-work paragraph and the Related Work section in `paper_draft.md` and `paper_draft.tex`. No change needed.
2. **stage_review.md § Stage 4 (REVISE — falsification conditions)** → verified already applied: an explicit **Falsification condition** line is present in all seven RQ subsections (including the later-spliced RQ1) in both `paper_draft.md` and `paper_draft.tex`. No change needed.
3. **stage_review.md § Phase A item 2 (reference-cache backfill)** → verified already applied and logged in `pipeline.md` (initial + resume rows). No change needed.
4. **stage_review.md § Phase A item 5 (H2b effect-size floor)** → applied to `paper.md` in the review pass, but the floor had never been mirrored into the deliverables' RQ3 (which operationalizes H2b). **Changed this round:** added the "at least 1 percentage point absolute between the lowest and highest perturbation intensity" floor to RQ3's Expected outcome + Falsification condition in `paper_draft.md`/`paper_draft.tex`, and to RQ3's Statistical test + Expected outcome in `experiment_design.md`. Target hypotheses left byte-identical (the floor lives in the outcome/test fields, not the verbatim Stage 5 hypothesis).
5. **stage_review.md § Phase A item 6, R1 estimand** → verified already applied: `paper.md` Step 5 opens with the **Estimand (R1)** sentence. No change needed.
6. **stage_review.md § Phase A item 6, R2 instrument validation (A1, κ ≥ 0.7)** → applied to `paper.md` A1 and mirrored into `experiment_design.md` RQ4 in the review pass, but `paper_draft.md`/`.tex` RQ4 still described the spot-check as a bare metadata read with an unthresholded "inter-annotator agreement rate". **Changed this round:** added the two-annotator, κ ≥ 0.7 acceptance-gate protocol (with refine-and-re-validate fallback) to RQ4's Setup and Metrics in `paper_draft.md` and `paper_draft.tex`.
7. **stage_review.md § Phase G [major] 1 (missing RQ1 for H1/Claim 1)** → verified applied (RQ1 spliced, RQ2–RQ7 renumbered), with one stale remnant found this round: `paper_draft.tex`'s Pre-handoff checklist still said "all 6 RQs" (the `.md` said 7). **Changed this round:** corrected to "all 7 RQs" in `paper_draft.tex`.
8. **stage_review.md § Phase G [major] 2 (zero \cite / no refs.bib)** → verified already applied: 14-entry script-generated `refs.bib`, `\citep{}` wiring, clean compile with zero undefined citations. No change needed.
9. **stage_review.md § Phase G [moderate] (DnR lacks a real fetched PDF/digest)** → **rejected — still environment-blocked:** re-attempted the OpenReview fetch this round (`https://openreview.net/pdf?id=FiMZSxo4DO`), still HTTP 403 bot-challenge; no arXiv mirror exists. Remains on its lightweight `corpus_backfill_digests/DnR.digest.md` reconstruction, as the review itself accepted.
10. **stage_review.md § Phase G [minor] (cosmetic overfull-hbox warnings, deferred to a "future prose-polish pass")** → **applied this round (this is that pass):** added `microtype` + `\emergencystretch` to the preamble and allowed line breaks inside the checklist's notation list (typesetting-only, no content change). Overfull-hbox count: 3 → 0. Recompiled clean (`latexmk -pdf`, exit 0, 15 pages, zero errors/undefined citations).
11. **taste_audit.md (both entries 🟢, no action items)** → nothing to apply. This round's changes are precision/typesetting additions inside already-audited material (effect floor, κ gate, RQ-count fix), not a reframing — same currency argument as `stage_review.md` Phase A item 8, so no re-audit triggered.
12. **pipeline.md open to-do 2 (5 adjacent-tagged keys on lightweight digests)** → **rejected — out of scope:** the review pass itself deprioritized these as non-load-bearing (`adjacent`/background), and no review file requests them; left as a logged to-do.
13. **pipeline.md open to-do 4 (Phase B/C compute)** → **rejected — moot in this environment:** no compute available; unchanged status, consistent with the definition-of-done note.

**Cross-deliverable consistency check (post-edits):** RQ count 7 = 7 (`paper_draft.md` ↔ `experiment_design.md`); RQ1 floors 0.25% LCB / 2ν = 2% UCB; RQ3 floor 1 pp (now stated identically in all three files + `paper.md` H2b); RQ4 impurity < 1%, κ ≥ 0.7; RQ6 shift ≥ 2 pp, Δ ≥ 8 years; RQ7 ε = 1 pp, δ = 0.05; α = 0.05 with Bonferroni per-test α = 0.0167; n ≈ 3,000/bucket; "≥ 2 of 3 detector families" aggregation — all matching across `paper_draft.md`, `paper_draft.tex`, `experiment_design.md`, and `paper.md`. RQ1's target hypothesis remains a byte-identical quote of `paper.md` Step 6 H1; Stage 5 target hypotheses untouched.
