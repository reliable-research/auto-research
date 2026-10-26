# Auto-Research-Discussion Run — B6.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B6.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already runs its own asymmetry/taste self-audit and a full pre-registered experiment design), so genuine disagreement surfaced at the level of formalization discipline and coverage gaps, not at the level of basic soundness.
>
> **Full pipeline order (this run):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure how fast corpus-level (distributional, ratio-based) synthetic-text-contamination estimators degrade when the text's true generator was withheld from calibration and when the synthetic portion has been paraphrased, and determine whether any statistical feature remains generator-invariant across both stress conditions.
- **Apparent inputs:** a human base corpus; a pool of candidate LLM text generators; a paraphrasing pipeline with an adjustable strength parameter; one or more candidate corpus-level proportion estimators; a controlled, researcher-set mixture ratio.
- **Apparent outputs:** an estimated contamination ratio per test corpus; estimation-error curves indexed by held-out-generator identity and paraphrase strength; a verdict on generator-invariant-feature existence (or a rigorous negative result).
- **Closest research areas:** machine-generated-text detection (DetectGPT, Learn-to-Distance, D&R); detector-generalization-to-unseen-generators in the image modality (DRCT); watermarking-based provenance (Kirchenbauer et al.'s scheme); quantification/aggregate-proportion correction (MarkovCalibration); synthetic-data-mixing theory (the recursive multi-entity training study; the iterative-retraining stability analysis); adjacent contamination measurement (Preference Leakage).
- **In scope:** stress-testing existing/near-term corpus-level estimator designs under a leave-one-generator-out (LOGO) protocol crossed with a paraphrase-strength sweep, using controlled mixtures with a known ground-truth ratio. **Out of scope:** validating estimator error on real, unlabeled corpora (no independently verified ground truth exists there — this is C3, explicitly left open by the seed's own digest); proposing a new estimator that "beats" existing ones; multimodal or code/non-English contamination.
- **Confidence: high.** As with a prior-reverse-digested seed in this batch, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`), already internally cross-referenced (N-node ↔ C/M-component ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Steps 0/3). Reconstruction risk is low; the live risk is *redundancy* with `paper.md`'s own Step 5/6 — addressed the same way the calibration exemplar did, by framing Stage 5/6 below as validating the **measurement instrument's properties** (is the degradation real, is it attributable to unseen-ness rather than difficulty, does a usable invariant signal survive) rather than re-deriving `paper.md`'s hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a corpus-level (distributional) synthetic-text-proportion estimator and controlled test corpora built at a known mixture ratio from a pool of text generators, determine how the estimator's error changes when (a) the text's true generator was withheld entirely from the estimator's calibration set, and (b) the synthetic portion has been paraphrased at increasing strength, and determine whether any statistical feature retains human/synthetic separability across both stress conditions.
- `input`: (1) a human base text corpus; (2) a pool of candidate text generators, each capable of producing synthetic text; (3) a paraphrasing pipeline with an adjustable strength parameter; (4) one or more candidate corpus-level proportion estimators; (5) a researcher-controlled mixture ratio used to build each test corpus.
- `output`: (1) an estimated contamination ratio per test corpus; (2) an estimation-error curve as a joint function of held-out-generator identity and paraphrase strength; (3) a verdict on whether a generator-invariant statistical feature exists (or a stated negative result).
- `constraints`: ground truth is defined as the researcher-controlled mixture ratio, not an independently verified real-corpus label; a held-out generator must be excluded from calibration entirely (not merely under-sampled) for a test to count as evidence about structurally unseen generalization; paraphrasing must be checked for semantic-fidelity preservation rather than assumed to preserve meaning.
- `objective`: a claimed degradation trend (error rising with generator-novelty or with paraphrase strength) is accepted only if it is shown to be statistically distinguishable from zero while accounting for the fact that observations from the same generator or generator family are not independent draws; a claimed generator-invariant feature is accepted only if its human/synthetic separability is shown to be stable — not merely "still positive on average" — across every tested held-out-generator × paraphrase-strength condition.
- `study_type`: `empirical` — stated explicitly: digest N12 already classifies this as `empirical` ("the core deliverable is a measurement study... validated by estimation-error curves and a feature-invariance test... not by introducing a new system"), and the seed's own core question ("退化速率是多少？存在...统计特征吗？") is a rate-and-existence question, not a proposed fix.

**critique:**
- summary: The problem is clean and traceable to the seed, but the `objective` field has quietly smuggled in a specific statistical technique, and one `output` item is underspecified relative to what stage 6 will need to certify it.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "method_leak", comment: "The v1 objective's first clause ('accounting for the fact that observations from the same generator... are not independent draws') is fine as a criterion, but an earlier internal draft of this field named 'a mixed-effects model with generator-resampled bootstrap CIs' directly — that is a specific statistical technique, not an evaluable criterion. Per stages.md, objective must be evaluable without committing to how it will be evaluated; the technique belongs in Method Design (Stage 5) or Experiment Design (Stage 6), not here. Flagging this now because the draft above already shows the corrected, technique-agnostic phrasing — but it needs to be stated as the deliberate fix it is, since a downstream reviewer re-deriving objective from digest.md's N8 analysis plan (which does name 'linear mixed-effects model' and 'bootstrap CIs' explicitly) could easily reintroduce the leak."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (3) says a verdict on feature existence 'or a stated negative result' — good — but doesn't yet say what would make that verdict itself trustworthy (i.e., what a passing vs. failing feature looks like). That's appropriately deferred to Stage 5's method design, but the field should at least gesture that the verdict must be a pre-committed, falsifiable criterion rather than a post-hoc read of a table, so Stage 5 doesn't have to invent this discipline from nothing."}`
- decision: `move_to_refiner` (the major flag is exactly the kind of formalize-and-clarify fix the refiner is meant to do — the content already avoids the leak, it just needs the reasoning made explicit and locked in; the minor flag just needs one clause added).

### Refiner pass

- `objective` (locked in, with the technique-agnostic framing made explicit): "A claimed degradation trend is accepted only if it is shown to be statistically distinguishable from zero by a procedure that treats generator identity (not just document identity) as the unit of resampling — the *specific* procedure (e.g., which mixed-effects specification, which bootstrap scheme) is a Stage 5/6 design choice, not part of this problem's objective. A claimed generator-invariant feature is accepted only if human/synthetic separability is shown to be stable, via a pre-committed criterion, across every tested held-out-generator × paraphrase-strength cell — not merely positive on average across cells."
- `output` (3) extended: "...a verdict on whether a generator-invariant statistical feature exists, reported against a pre-committed, falsifiable passing criterion stated in advance of seeing the per-cell results — not a post-hoc judgment call."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's notation since it already exists and adds no new assumption): "Corpus $D$ with true synthetic fraction $r \in [0,1]$ fixed by construction. Estimator $\hat{E}: D \mapsto \hat{r} = \hat{E}(D) \in [0,1]$. Generator pool $G$; for held-out generator $g^* \in G$, calibration set $G_{\text{cal}} = G \setminus \{g^*\}$. Paraphrase strength $k \in \{0,1,2,3\}$ applied to the synthetic portion before mixing. Feature family $\phi$ with per-cell separability $\mathrm{AUROC}_\phi(g,k)$. Determine the behavior of $\mathrm{AE} = |\hat{r} - r|$ as a function of $(g^*, k)$, and whether any $\phi$ has $\mathrm{AUROC}_\phi(g,k)$ stable across all tested $(g,k)$."
- `changes_made`: locked in the technique-agnostic objective and made the reasoning for it explicit; added a pre-commitment clause to output (3); added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Corpus-level contamination estimators are the practical instrument teams actually reach for when deciding how much of a corpus is synthetic and whether to filter or down-weight it — but their reliability has only ever been demonstrated against a fixed, known set of calibration generators, which is precisely the condition that fails to hold once a corpus is contaminated by generators the auditor never anticipated.
- `why_it_matters`: Pretraining corpora already contain substantial content from many different, often unknown generating systems (the recursive multi-entity training study's own motivation states corpora "now contain substantial AI-generated content from many different systems"), and the contamination *fraction* is not a cosmetic statistic — the iterative-retraining stability analysis shows the mixing parameter between real and synthetic data determines whether iterative retraining on that corpus is a stable contraction or collapses. If the fraction that decision rests on comes from an estimator that fails silently once the true generator is unseen, teams are making a stability-relevant decision on a number that could be arbitrarily wrong without any visible warning sign. Per-document detectors are already known to degrade across generations and sampling strategies (the Kirchenbauer et al. watermarking-scheme paper's own motivation concedes this about non-watermark post-hoc detectors); whether that same failure propagates to the *aggregate, corpus-level* estimators actually used for filtering decisions — and how fast — has not been measured.
- `who_cares`: Teams deciding whether to filter or down-weight training corpora based on an estimated contamination fraction; governance or safety reviewers proposing contamination thresholds as policy; researchers building the next detector or estimator, who need to know whether "quantification correction" genuinely buys off-calibration robustness or merely relocates the failure.
- `evidence`: the recursive multi-entity training study's motivation on many-generator contamination; the iterative-retraining stability analysis's contraction condition on the mixing parameter; the Kirchenbauer et al. watermarking paper's own motivation on detector degradation across generations; DRCT's motivation, which documents the identical unseen-generator failure mode already occurring in the image modality ("detectors trained on a narrow set of models exhibit severe performance degradation when confronted with images from unseen... variants") — the text-domain, corpus-ratio analogue of that failure has not been characterized.

**critique:**
- summary: Strong, stake-specific motivation with real grounded citations, but it covers only two of stage 1's three outputs.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is the generator-invariant-feature verdict — and why_it_matters never explains why anyone should care about that verdict specifically, as opposed to just knowing 'estimators degrade.' A reader could reasonably ask: if we already know the estimator fails off-calibration, why do we need a separate feature-invariance search at all? Without an answer, CO3 (the feature-invariance contribution) reads as an add-on rather than a load-bearing part of the paper's motivation."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a diagnosed degradation on its own does not tell a practitioner what to do next: it does not distinguish 'this is fixable — a better statistical feature would close the gap' from 'this is structurally obstructed — no signal in the text survives both an unseen generator and paraphrasing, so the fix has to be something other than a smarter estimator (e.g., generation-time provenance, or explicit uncertainty reporting instead of a point estimate).' That binary is exactly what the feature-invariance verdict resolves, and it is invisible to any study that stops at reporting an error curve without also asking whether *any* candidate signal survives the same stress conditions."
- `changes_made`: added the fixable-vs-structurally-obstructed argument tying the third output to a concrete, decision-relevant payoff.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level; no additional landscape papers are invented here to pad a `general_related_works` list, per the no-fabrication rule.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_detectgpt` | DetectGPT (OpenReview:UiAyIILXRd) | true | Zero-shot per-passage curvature detector requiring source-model likelihood access; outputs a per-document decision, not a corpus ratio, and reports no error curve over held-out generators or paraphrase strength. |
| `rw_learn2distance` | Learn-to-Distance (OpenReview:2ZUPeEM3FH) | true | Rewrite-distance per-passage detector; its own motivation concedes curvature-style methods "depend strongly on assumptions" that break under distribution shift — but it stops at a better per-document score, not a corpus-level estimator. |
| `rw_dr` | D&R: Disrupt-and-Recover (OpenReview:FiMZSxo4DO) | true | Black-box recovery-based per-passage detector avoiding likelihood access, but still a binary per-document decision with no aggregate-proportion target. |
| `rw_markovcal` | MarkovCalibration (OpenReview:Lzwkeg2o2z) | true | Wraps existing detectors in an MRF calibration layer over token scores; formalizes "aggregate noisy per-instance scores into one decision," but the target remains a per-passage label, not a corpus ratio. |
| `rw_watermark` | Kirchenbauer et al., watermarking scheme (OpenReview:aX8ig9X2a7) | false (requires generation-time cooperation) | A provenance approach requiring the generator's cooperation at sampling time; cannot estimate contamination from generators the auditor never controlled — the complement of this paper's setting. |
| `rw_drct` | DRCT (OpenReview:oRLwyayrh1) | false (image modality) | Trains a detector to generalize to unseen diffusion-image variants via contrastive hard-sample augmentation; documents the identical unseen-generator degradation this paper measures, but in the image modality, via training-time augmentation rather than a corpus-ratio estimator, and with no paraphrase-strength axis. |
| `rw_recursive_multientity` | Recursive multi-entity training study (OpenReview:JEU4PBaX85) | false | Treats the synthetic-mixing fraction as a *controlled input* to study convergence toward homogeneity; provides no inverse estimator recovering an unknown fraction from an observed corpus. |
| `rw_iterretrain` | Iterative retraining stability analysis (OpenReview:JORAfH2xFd) | false | Theoretical fixed-point analysis establishing that the mixing parameter is the causally load-bearing quantity, but purely as a modeling input, not something to be estimated from data. |
| `rw_prefleak` | Preference Leakage (OpenReview:grIvSXVJ65) | false | Measures LLM-as-judge contamination for specific, related generator/judge families by design; does not test corpus-ratio error under a leave-one-generator-out protocol or paraphrase-attack strength. |

**critique:**
- summary: Grounding is specific throughout and every limitation is tied to this paper's exact gap, but four baseline labels are stated too flatly.
- comments:
  - `{severity: major, field: "specific_related_works[rw_detectgpt, rw_learn2distance, rw_dr, rw_markovcal].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "All four works are per-document detectors — their I/O framing (text in, one binary/score decision out) does not match this paper's corpus-ratio framing. Marking them 'true' baselines flatly, without qualification, risks implying they can be run unmodified against a corpus-ratio target. Per the stage-3 rubric, an I/O-mismatched work is 'not a baseline — at best a method-side reference' unless the mismatch is explicitly bridged."}`
- decision: `move_to_refiner` (this is a precision fix, not a structural one — `paper.md`'s own M3(c) already specifies exactly the bridging operation: pooling per-document scores into a corpus ratio. The refiner's job is to state that bridging explicitly rather than drop the baselines).

### Refiner pass

- `rw_detectgpt`, `rw_learn2distance`, `rw_dr`, `rw_markovcal`'s `is_potential_baseline` retained as `true`, but each field's note is sharpened: "Not a baseline in its native form — none of these four outputs a corpus ratio. Each is borrowed as a baseline only after its per-document scores are pooled into a corpus-level proportion (averaging or thresholding-and-counting the per-document decisions across a test corpus), which is itself one of the estimator designs under test (the naive classify-and-count / pooled zero-shot arms) — not a claim that these papers' own reported numbers are being reproduced or beaten."
- `changes_made`: clarified that all four per-document detectors enter this paper only via an explicit pooling operation, avoiding an implied unmodified-baseline comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. No limitation above is promoted to a stage-6 framing-tier RQ — each is already fully absorbed into a stage-4 sub-problem's `technical_challenge` and answered end-to-end by a stage-5 mechanism-tier method, so promoting one to a separate framing-tier RQ would test the same thing twice under two different tiers. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C5 plus one gap `paper.md`'s own Step 6 already treats as load-bearing but digest's C1–C5 challenge list does not separately name):

- **`sp_open_generator_space`** — *description:* Determine whether an estimator calibrated on a fixed generator pool generalizes to a generator structurally absent from that pool, not merely an unseen sample from a known one. *why_it_is_a_problem:* the space of possible generators (families, fine-tunes, decoding configurations) is open-ended and continually growing, so no calibration set can ever be exhaustive — any claim of estimator reliability is only as strong as its untested generalization to what comes next. *technical_challenge:* testing this requires excluding an entire generator's documents from calibration (not down-sampling them), which shrinks the calibration pool every fold and makes the resulting estimate noisier exactly when it needs to be most trustworthy. *source_limitation_ids:* `["lim_per_passage_generalization"]` → mapped to `rw_drct`'s limitation (the one related work that directly targets unseen-generator degradation, albeit in images).
- **`sp_paraphrase_margin_instability`** — *description:* Characterize how estimator error changes as the synthetic portion of a corpus is paraphrased at increasing strength, rather than treating "paraphrased or not" as a binary. *why_it_is_a_problem:* paraphrasing continuously interpolates between clearly-synthetic and clearly-human text, so any single error number, measured at one paraphrase setting, says nothing about where on that continuum an estimator actually breaks. *technical_challenge:* the separability margin degrades smoothly and estimator error must be traced as a continuous function of strength, not read off a single before/after comparison. *source_limitation_ids:* `["lim_per_passage_generalization"]` (the same works' shared gap: none reports error as a function of paraphrase strength either).
- **`sp_aggregation_bias`** — *description:* Determine how much of an estimator's error, when aggregating many per-document readings into one corpus-level ratio, is attributable to a systematic aggregation bias rather than to per-document classification error. *why_it_is_a_problem:* summing or thresholding per-instance scores to get an aggregate proportion is a known source of bias under distribution shift (the quantification-learning problem), and that bias shifts with the held-out generator — so it cannot be corrected by a single fixed calibration constant. *technical_challenge:* isolating the aggregation-bias component requires comparing an aggregation-aware (corrected) estimator against a naive one under matched conditions, not just reporting one number for each. *source_limitation_ids:* `["lim_markovcal_aggregation"]`.
- **`sp_novelty_vs_difficulty_confound`** — *description:* Determine whether degraded performance on a held-out generator is caused by that generator being *unseen*, or merely by that particular generator's text being *intrinsically harder to detect* regardless of calibration. *why_it_is_a_problem:* these two explanations are observationally identical in a plain LOGO comparison — a generator could look "hard" in the LOGO fold for reasons that have nothing to do with calibration status — so a LOGO gap alone cannot license a claim about *unseen-ness* specifically. *technical_challenge:* the two effects can only be disentangled by holding the same test documents fixed and varying only whether their generator was in the calibration set, which requires a matched swap design rather than a single comparison across arbitrary generators. *source_limitation_ids:* `["__novel__"]` — no cited work isolates this confound; DRCT gets closest (it targets unseen-generator degradation directly) but never controls for the held-out generator's intrinsic detectability.
- **`sp_confounded_stress_factors`** — *description:* Determine whether generator novelty and paraphrase strength each independently drive degradation, or whether one effect is really an artifact of the other. *why_it_is_a_problem:* the two stress axes act on the same documents simultaneously — a held-out generator's text might also happen to be easier or harder to paraphrase past detection — so a univariate test on either axis alone risks attributing one axis's effect to the other. *technical_challenge:* disentangling the two requires one joint statistical specification with both factors present at once and enough independent replication per cell for that separation to have power, not two separate significance tests run in isolation. *source_limitation_ids:* `["__novel__"]`.
- **`sp_feature_invariance_search`** — *description:* Determine whether any statistical feature of text retains stable human/synthetic separability across every tested held-out-generator × paraphrase-strength condition, or establish that none does. *why_it_is_a_problem:* without this, a diagnosed degradation cannot be turned into an actionable next step — whether the fix is "engineer a better feature" or "abandon this class of estimator entirely" hinges entirely on whether such a feature exists. *technical_challenge:* invariance must be checked cell-by-cell (a feature separable on average but collapsing in one condition is not invariant), which requires a combinatorially large evaluation grid and a formal cross-cell flatness test with correction for testing multiple candidate features. *source_limitation_ids:* `["__novel__"]` — no cited work runs a joint invariance test of this kind; DRCT is the nearest analogue but evaluates a trained detector's accuracy, not a candidate feature's cross-condition separability.

**critique:**
- summary: The decomposition covers all three of stage 1's outputs and every sub-problem is still method-free, but two sub-problems risk reading as the same thing under different names.
- comments:
  - `{severity: minor, field: "sp_confounded_stress_factors / sp_novelty_vs_difficulty_confound", anti_pattern: "overlap", comment: "Both are framed as 'isolating a confound,' which can read as the same sub-problem stated twice. They are genuinely distinct — one is a *continuous-factor disentanglement* problem (do generator novelty and paraphrase strength each have an independent, separately estimable effect), the other is a *categorical attribution* problem (is a LOGO gap caused by unseen-ness at all, versus a specific generator just being hard) — but the current wording doesn't make that distinction sharp enough for a reader to see they require different designs."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_confounded_stress_factors.technical_challenge` sharpened to end with: "...this is a **joint-estimation** problem over two continuously-varying factors (generator identity as a random effect, paraphrase strength $k$ as a fixed effect), answered by one specification that returns both effects at once — distinct from asking whether the LOGO effect exists *at all* net of a specific generator's difficulty, which is a separate, categorical question."
- `sp_novelty_vs_difficulty_confound.technical_challenge` sharpened to end with: "...this is a **categorical attribution** problem — unseen vs. seen for the *same* documents — answered by a matched swap, not by adding more terms to a regression; no amount of additional factorial structure in the joint model above substitutes for actually holding the test documents fixed and toggling only their calibration status."
- `changes_made`: made the joint-estimation-vs-categorical-attribution distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 3 sourced from related-work limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_logo_calibration`** → targets `sp_open_generator_space`. *proposed_approach:* For each generator in the pool, exclude all of its documents from every estimator's calibration/training data, then evaluate that estimator only on test corpora built from the excluded generator's documents; repeat across all generators (leave-one-generator-out). *key_insight:* cross-validating across generator *identity* rather than document *identity* is what actually operationalizes "structurally unseen" — a random train/test split of documents from the same generators would only test unseen samples, not unseen generators. *hypotheses:* ["Mean absolute estimation error under leave-one-generator-out validation will exceed mean absolute error under in-distribution validation by at least 0.05, significantly, for the majority of tested estimators."]
- **`m_paraphrase_sweep`** → targets `sp_paraphrase_margin_instability`. *proposed_approach:* Apply a paraphrasing pipeline to the synthetic portion of each test corpus at strength levels $k \in \{0,1,2,3\}$ (increasing rewrite rounds), gated by a semantic-fidelity check, before mixing at the target ratio; measure estimator error at every level. *key_insight:* representing paraphrase strength as a swept, ordered parameter rather than a single on/off toggle converts an unstable qualitative judgment ("does paraphrasing break detection?") into a quantitative error curve with an interpretable slope. *hypotheses:* ["Mean absolute estimation error increases monotonically with paraphrase strength $k$, with a slope significantly greater than zero."]
- **`m_quantification_correction`** → targets `sp_aggregation_bias`. *proposed_approach:* Alongside a naive classify-and-count estimator, run a quantification-corrected estimator (prior-shift/adjusted-count correction) that explicitly models and removes the aggregation-level bias induced by distribution shift, then compare the two estimators' leave-one-generator-out gaps directly. *key_insight:* because a quantification correction targets exactly the aggregate-proportion bias (not the per-instance classifier's own error rate), contrasting the corrected estimator's gap against the naive estimator's gap under identical conditions isolates how much of the total degradation is aggregation bias versus base-classifier degradation. *hypotheses:* ["The corrected estimator's leave-one-generator-out gap will be smaller than the naive estimator's gap by at least 30%, but will remain significantly greater than zero — correction reduces, but does not eliminate, degradation."]
- **`m_capability_matched_swap`** → targets `sp_novelty_vs_difficulty_confound`. *proposed_approach:* For a fixed set of documents from a given generator, evaluate estimator error twice — once with that generator included in calibration (seen) and once with it excluded (unseen/LOGO) — holding pool size, compute budget, and paraphrase strength identical between the two runs; the seen-versus-unseen difference is the pure unseen-ness effect. *key_insight:* the only way to separate "this generator's text is intrinsically hard to detect" from "this generator was unseen at calibration" is to hold the test documents themselves fixed and vary only their calibration membership — any comparison across different generators cannot make this separation cleanly. *hypotheses:* ["The seen-versus-unseen absolute-error difference, computed on the identical held-out documents, will be significantly greater than zero — i.e., detectability of the specific generator alone does not explain the leave-one-generator-out gap."]
- **`m_joint_stress_design`** → targets `sp_confounded_stress_factors`. *proposed_approach:* Cross the leave-one-generator-out axis with the paraphrase-strength axis in one full factorial grid per estimator, and fit a single mixed-effects specification (absolute error regressed on calibration regime and paraphrase strength, with a random intercept per generator family) rather than testing each axis with a separate univariate comparison. *key_insight:* because the two stress axes act on the same underlying documents, testing them separately risks each axis's estimated effect silently absorbing some of the other axis's true effect; a single joint specification with generator-family random effects is what lets both main effects be estimated net of the other. *hypotheses:* ["The calibration-regime coefficient remains significant after controlling for paraphrase strength in the joint fit.", "The paraphrase-strength coefficient remains significant after controlling for calibration regime in the joint fit."]
- **`m_invariance_probe`** → targets `sp_feature_invariance_search`. *proposed_approach:* For each candidate feature family (reference-model log-likelihood/perplexity; stylometric n-gram and burstiness statistics; sentence-embedding directions), measure human-versus-synthetic separability (AUROC) within every held-out-generator × paraphrase-strength cell, then apply a pre-committed cross-cell flatness test (variance-components / Levene-style, testing that cross-cell AUROC variance is not significantly greater than zero) combined with an absolute floor (AUROC $\ge 0.70$ in every cell). *key_insight:* invariance is a *worst-cell* property, not an average-case one — a feature that separates well in four cells and collapses in a fifth is not invariant, so only a feature clearing both the flatness test and the per-cell floor simultaneously should be certified, turning "does an invariant feature exist" into a falsifiable, pre-registered criterion instead of a post-hoc read of a results table. *hypotheses:* ["No candidate feature family will simultaneously pass the cross-cell flatness test and the 0.70 per-cell floor across all tested held-out-generator × paraphrase-strength cells — the negative branch will be the observed outcome, though a partial-invariance ranking across features remains reportable regardless."]

**critique:**
- summary: Every method carries a real, distinct mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but one method's key_insight doesn't yet justify why it needs two separately-stated hypotheses rather than reading as scope creep.
- comments:
  - `{severity: minor, field: "m_joint_stress_design.hypotheses", anti_pattern: null, comment: "Two hypotheses appear here (regime effect net of paraphrase; paraphrase effect net of regime) — worth stating explicitly why a single joint model producing two separately falsifiable estimands is one mechanism, not two, so this doesn't read as bundling two claims under one method's ledger."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_joint_stress_design.key_insight` extended: "...a single joint mixed-effects fit yields two distinct, separately falsifiable estimands from one specification: the regime main effect (net of paraphrase strength) and the paraphrase-strength main effect (net of regime) — one instrument, two readouts, because both coefficients are estimated jointly in the same model rather than by running two separate models that would each risk absorbing the other's true effect."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly, mirroring why a single specification is needed rather than two independent tests.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **7 hypotheses total** (1+1+1+1+2+1 across the six methods respectively — `m_joint_stress_design` carries two, per the refiner's one-instrument-two-estimands justification above), mixing instrument-validity claims (confound isolation, aggregation-bias attribution) with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our estimator beats baseline X" framing. All baselines below are sanity-check comparators or confound-isolation arms, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- A human base corpus of real news/web prose — *justification:* gives the LOGO/paraphrase grid a stable, non-synthetic reference side that is not itself generated by any pool generator, so any pure-human self-consistency check ($\hat r \approx 0$ at $k=0$) is meaningful.
- MGTBench- and RAID-style multi-generator machine-text collections — *justification:* the synthetic side and cross-check corpus; each already spans multiple generator families, which is exactly the kind of pool a leave-one-generator-out design needs to be non-trivial (a pool of near-identical generators would make every LOGO fold look artificially easy).
- DIPPER-paraphrased variants of the synthetic portion at $k \in \{0,1,2,3\}$ rewrite rounds — *justification:* directly operationalizes the paraphrase-strength axis at a controllable, ordered granularity.
- (draft initially listed HC3 with justification only "an auxiliary in-domain human/synthetic reference" — flagged below.)

`baselines` (sanity-check / confound-isolation comparators, not outcome-tier competitors):
- Text-blind constant estimator (always returns the calibration-set prior ratio, ignoring the corpus) — the necessary "why do this at all" gate: if no real estimator beats this in-distribution, there is no working estimator whose degradation is worth measuring.
- Capability-matched seen/unseen swap (identical held-out documents, calibration membership toggled) — not a competitor, the confound-isolation arm for `sp_novelty_vs_difficulty_confound`.
- Naive classify-and-count vs. quantification-corrected classify-and-count — a matched pair, not a beat-baseline comparison; the whole point is their *difference*, not which one wins.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_logo_gap` | `sp_open_generator_space` | "Mean absolute estimation error under leave-one-generator-out validation will exceed mean absolute error under in-distribution validation by at least 0.05, significantly, for the majority of tested estimators." |
| `rq_paraphrase_slope` | `sp_paraphrase_margin_instability` | "Mean absolute estimation error increases monotonically with paraphrase strength $k$, with a slope significantly greater than zero." |
| `rq_correction_gap` | `sp_aggregation_bias` | "The corrected estimator's leave-one-generator-out gap will be smaller than the naive estimator's gap by at least 30%, but will remain significantly greater than zero — correction reduces, but does not eliminate, degradation." |
| `rq_unseen_vs_difficulty` | `sp_novelty_vs_difficulty_confound` | "The seen-versus-unseen absolute-error difference, computed on the identical held-out documents, will be significantly greater than zero — i.e., detectability of the specific generator alone does not explain the leave-one-generator-out gap." |
| `rq_regime_independent_effect` | `sp_confounded_stress_factors` | "The calibration-regime coefficient remains significant after controlling for paraphrase strength in the joint fit." |
| `rq_paraphrase_independent_effect` | `sp_confounded_stress_factors` | "The paraphrase-strength coefficient remains significant after controlling for calibration regime in the joint fit." |
| `rq_invariant_feature` | `sp_feature_invariance_search` | "No candidate feature family will simultaneously pass the cross-cell flatness test and the 0.70 per-cell floor across all tested held-out-generator × paraphrase-strength cells — the negative branch will be the observed outcome, though a partial-invariance ranking across features remains reportable regardless." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 6/Step 9 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a provenance note rather than a reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "datasets[HC3]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'an auxiliary in-domain human/synthetic reference' says nothing about which RQ needs it or why it isn't redundant with the other three datasets already listed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "HC3 (human/ChatGPT comparison corpus) — *justification:* provides matched human-authored and model-authored responses to the *same* prompts, which is specifically what the A6 pure-human self-consistency check (`m_logo_calibration`'s $k=0$, $g^*$-absent control: every estimator should return $\hat r \approx 0$ on a corpus built entirely from HC3's human side) needs — a human corpus not itself drawn from the same web-scrape distribution as the news/web base corpus, so a passing self-consistency check here is evidence the estimators aren't just keying on domain-specific artifacts of one human source."
- `changes_made`: gave HC3's inclusion a hypothesis-linked reason (the A6 self-consistency check) instead of a generic provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (Stage 1's objective was specifically corrected for this during its own refiner pass — see above).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_open_generator_space.source_limitation_ids = ["lim_per_passage_generalization"]` and `sp_paraphrase_margin_instability.source_limitation_ids = ["lim_per_passage_generalization"]` both ∈ Stage 3 limitations ✓ (the shared limitation that no per-passage detector reports error as a function of held-out generator or paraphrase strength); `sp_aggregation_bias.source_limitation_ids = ["lim_markovcal_aggregation"]` ∈ Stage 3 ✓; the remaining three sub-problems' `["__novel__"]` sentinels each carry a stated decisive-component justification ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (estimated ratio, error curve, feature-invariance verdict) are each reachable: the estimated ratio and error curve via `sp_open_generator_space` + `sp_paraphrase_margin_instability` + `sp_aggregation_bias` + `sp_confounded_stress_factors` (which jointly cover the (a) and (b) axes of Stage 1's objective and the confound that would undermine attributing degradation to either), the feature-invariance verdict via `sp_feature_invariance_search` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** as with the calibration reference run, the recurring tension was **not disagreement about facts** (the seed material — `digest.md` N1–N12 plus `paper.md`'s own Steps 0–9 — is unusually well-specified, down to exact thresholds and fallback claims) but **keeping this run's stage outputs from silently duplicating `paper.md`'s own already-finished experiment design** rather than adding something this schema's structure specifically demands. The clearest instance: `paper.md`'s "B-alt" baseline (capability-matched seen/unseen swap) is *labeled* a baseline in the source material, but it functions as a confound-isolation method targeting a distinct sub-problem (`sp_novelty_vs_difficulty_confound`) in this schema — recognizing that required treating a `paper.md` "baseline" as a Stage-5 method with its own hypothesis, not a Stage-6 comparator, which is exactly the kind of schema-driven reclassification a single-shot draft wouldn't have forced.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

> This trace was extracted verbatim from `pipeline.md` (moved, not regenerated) per the auto-research-discussion skill's updated three-artifact deliverable spec. Post-Stage-6 provenance (bibliography wiring, adversarial review, taste re-audit, compile fixes) and the goal.md phase-gate log remain in `pipeline.md`. The standalone Stage 6 execution spec lives in `experiment_design.md`.

---

## Post-review revision round (2026-07-05)

> Revision pass over every finding/recommendation in `stage_review.md` and `taste_audit.md` (no `design_review.md` exists for this topic). Each item below states: source review file → finding → status, with what changed and where for items applied this round. Historical rounds above are untouched.

**Status of previously-fired findings (verified already applied, no action this round):**

1. `stage_review.md` → Stage 2 REVISE (nearest-neighbor/method-twin sentence missing from Related Work) → **already applied**: `paper_draft.md`/`.tex` Related Work opens with the two-nearest-works concede-and-differentiate paragraph (DRCT2024DiffusionRecon on the unseen-generator dimension; SampleComplexitiesofEsti700224 on the estimand dimension).
2. `stage_review.md` → Stage 4 REVISE (no falsification-condition line per RQ) → **already applied**: all 7 RQ subsections in `paper_draft.md`/`.tex` carry an explicit **Falsification condition** line; mirrored per-RQ in `experiment_design.md`.
3. `stage_review.md` → Phase A checklist item 1 (digest absence_comment gaps, N4/N5/N6/N7/N8/N12) → **already applied** in `digest.md` (logged as fixed within the Phase A pass).
4. `stage_review.md` → Phase A checklist item 2 (0/9 N3 keys resolved in `reference_candidates.jsonl`) → **already applied**: 9 records added; 5 of 6 load-bearing ones later got real PDFs + digests (pipeline.md "Reference-cache remediation" row).
5. `stage_review.md` → Phase A checklist item 5 (A1–A6 missing `gate`/`consequence` slots) → **already applied** in `paper.md` (all six assumptions now carry all five slots).
6. `stage_review.md` → Phase A checklist item 6 (R1 estimand sentence; M3(a) R2-lite AUROC ≥ 0.90 instrument floor; thin-cell INCONCLUSIVE pre-declaration) → **already applied** in `paper.md` (Step 5 estimand + R2-lite paragraphs; RQ1 power pre-declaration) and carried into `experiment_design.md` (Instrument validation + shared A5 power block) and `paper_draft.md`/`.tex` ("Power and inconclusive cells").
7. `stage_review.md` → Phase A "Method-twin discovered mid-run" (Step 5b fold-in pending for the draft) → **already applied** at Phase E (Related Work rewrite, pipeline.md row "E (prose re-check)").
8. `stage_review.md` → Phase G [major] missing power/INCONCLUSIVE pre-declaration in the draft → **already applied** ("Power and inconclusive cells" paragraph in `paper_draft.md`/`.tex` Experimental Setup).
9. `stage_review.md` → Phase G [major] no multiple-comparison correction stated for RQ1–RQ6 → **already applied** (Holm-correction sentence in the Metrics paragraph of `paper_draft.md`/`.tex`; mirrored in `experiment_design.md`'s shared metrics block).
10. `stage_review.md` → Phase G [moderate] Conclusion limitations thinner than the assumption ledger → **already applied** (4 named, scope-bounding limitations in the Conclusion of `paper_draft.md`/`.tex`).
11. `taste_audit.md` → both audits (original + Phase H re-audit) returned 🟢 with no action items → **nothing to apply**.

**Applied this round:**

12. `stage_review.md` → Phase G **[minor, logged as to-do, not fixed]** cosmetic overfull-hbox warnings (RQ subsection headings and long hyphenated compounds running 3–16pt past the margin) → **applied now, in `paper_draft.tex` only**: added `\usepackage{microtype}` + `\emergencystretch=1.5em` to the preamble — a pure typesetting-layer fix that resolves all 5 overfull boxes with zero wording changes, honoring the reviewer's own constraint that re-wording pre-registered prose was not authorized. Recompiled via `latexmk -pdf`: exit 0, **0 Overfull warnings** (was 5), 0 undefined citations, 0 bibtex warnings, 14 pages. No change to `paper_draft.md` (prose untouched).

**Rejected as moot (no action possible or required):**

13. `stage_review.md` → Phase A §0 flag "real spot-check of 7 OpenReview ids next time network access succeeds" → **rejected — environment-blocked, already superseded in substance**: the later reference-cache remediation pass fetched real PDFs + built digests for 5 of the 6 load-bearing records, which is a stronger verification than the requested metadata spot-check; the residual `DR2023RecoveryDetect` gap is item 14.
14. `stage_review.md` → residual honest gap: `DR2023RecoveryDetect` (OpenReview:FiMZSxo4DO) has no digest/PDF → **rejected — not fixable from this environment**: pipeline.md documents a genuine multi-angle search (OpenReview bot-blocked, no arXiv mirror, no repo PDF, Semantic Scholar + web searches empty); per the run's own "log the gap, don't fabricate" rule it stays `selected` with `verified.id_resolves: false`.
15. `stage_review.md` → Phase G [minor, N/A] reproducibility/artifact-release checks → **rejected — moot by design**: pre-results spec; the draft's Pre-handoff checklist already hedges artifacts as planned, not available.

**Cross-deliverable consistency check (this round):** RQ count 7 = 7 (`paper_draft.md` ↔ `experiment_design.md`); effect floors and margins match verbatim across both — 0.05 LOGO-gap floor (RQ1), ≥30% gap-reduction / still-significantly-positive dual condition (RQ3), 0.70 per-cell AUROC floor + flatness test (RQ7), ≥1000 docs per cell and 0.03 CI-width INCONCLUSIVE trigger (shared power block), Holm correction within estimator suite / feature families, $k \in \{0,1,2,3\}$. Target hypotheses in `experiment_design.md` remain verbatim Stage 5 quotes (unmodified). One deliberate non-edit, noted for the record: `paper.md`'s composite H1(ii) carries a $\beta_{\text{para}} \ge 0.02$/level floor that neither deliverable's RQ2 states — both deliverables consistently quote the Stage 5 `m_paraphrase_sweep` hypothesis (significance-only), so the two deliverables match each other; folding the 0.02 floor into RQ2 would mean rewording a pre-registered hypothesis, which no review requested and this pass is not authorized to do. No mismatch between the two deliverables found; nothing else fixed.
