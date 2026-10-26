# Digest: Estimating Contamination from Generators You Have Never Seen: Robustness Limits of Distributional Estimators

> **REVERSE-PAPER-DIGEST DISCLAIMER.** No paper exists yet for this topic. This is speculative
> scaffolding for research planning only, constructed from a one-paragraph seed idea (topic
> code B6.1). Every field below is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README; **[HYPOTHESIS]** = reasoned
> elaboration/prediction, not a fact; **[PLACEHOLDER]** = genuinely unknowable until the work
> is actually done (never invented); **[GROUNDED:corpus]** = anchored to a real paper found in
> the local OpenReview corpus (`topics/corpus/ideas.jsonl`), cited by its real `paper_id`.
> Do not read any [HYPOTHESIS]/[PLACEHOLDER] content as having occurred.

---

## N0 Metadata

- `title` [GIVEN]: "Estimating Contamination from Generators You Have Never Seen: Robustness Limits of Distributional Estimators"
- `authors` [PLACEHOLDER]: `["Anonymous"]` — no paper/authors exist yet.
- `abstract` [HYPOTHESIS] (drafted, not real — synthesized from the core question + minimal experiment):
  > "Corpus-level estimators of synthetic-text contamination are typically calibrated and
  > validated against a fixed, known set of text generators. We ask how such distributional
  > (corpus-level, ratio-based) estimators behave when the generator that actually produced the
  > contaminating text was never seen during calibration, and when that text has been further
  > obscured by paraphrasing. Using controlled corpora with known ground-truth mixture ratios,
  > we run leave-one-generator-out cross-validation together with a paraphrase-strength sweep
  > and trace the resulting estimation-error curves. We further ask whether any statistical
  > feature of text remains separable across generators and paraphrase strength — i.e.,
  > whether a generator-invariant signature for contamination estimation exists. (Draft
  > abstract — not a real result; the underlying study has not been conducted.)"
- `doi` [PLACEHOLDER]: `null`
- `arxiv_id` [PLACEHOLDER]: `null`
- `num_pages` [PLACEHOLDER]: `null`
- `research_area` [HYPOTHESIS]: `"NLP"` (secondary: AI/ML) — inferred from the domain of LLM-generated-text detection / corpus contamination measurement.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No authors, DOI, arXiv id, or page count exist because no paper has been written for this seed idea.", `why_matters`: "Downstream tools (paper-writer, reviewer agents) need to know this digest describes a hypothetical future paper, not a retrievable document.", `implication`: "Treat every bibliographic field except `title` as a placeholder to be filled in once (if) the study is actually written up."}

---

## N1 Problem Formulation

- `objective` [HYPOTHESIS]: "Measure, via controlled leave-one-generator-out cross-validation and a paraphrase-strength sweep, the degradation rate of corpus-level (distributional) synthetic-text-proportion estimators when applied to text from generators and paraphrase transformations absent from their calibration set, and determine whether a generator-invariant statistical feature exists that preserves estimator reliability across this generalization gap."
  - Self-check: kind of task = measurement/robustness characterization; domain = corpus-level contamination/synthetic-text-proportion estimation for LLM-generated text; outcome shape = estimation-error curves + a feature-existence finding (or explicit negative result). All three dimensions land.
- `inputs` [HYPOTHESIS]:
  - Controlled synthetic/human text mixtures constructed at known ground-truth ratios.
  - A pool of candidate text generators (multiple LLM families/checkpoints), with one generator withheld per leave-one-generator-out (LOGO) fold.
  - A paraphrasing pipeline with an adjustable "strength" parameter (e.g., number of rewrite rounds, paraphraser model, decoding temperature).
  - One or more candidate corpus-level (distributional) proportion estimators under test.
- `outputs` [HYPOTHESIS]:
  - An estimated synthetic-text ratio per test corpus.
  - Estimation-error curves as a function of (a) held-out generator identity and (b) paraphrase strength.
  - A determination of whether any statistical feature remains generator-invariant (separable) across both stress axes.
- `constraints` [GIVEN]: "真值 = 受控混合比例" — ground truth is defined as the researcher-controlled mixture proportion; the seed explicitly anchors validity to this controlled setup rather than to any independently verified real-corpus label.

**Status:** PARTIAL (inferred, not extracted — no paper exists). `absence_comment`: {`what_missing`: "There is no explicit formulation section to extract from; this objective is reconstructed from the seed's core question and minimal experiment.", `why_matters`: "A reviewer needs to know the objective was authored by the digest-writer, not read verbatim from a paper.", `implication`: "Treat the objective as a testable prediction of what the eventual paper would state, not as a confirmed problem statement."}

---

## N2 Motivation

`motivations` [HYPOTHESIS] (reconstructed from `parent_topic`: "B6. 污染机制层（合成语料）" — the "contamination mechanism layer (synthetic corpora)" branch of the broader topic tree; now anchored to real corpus papers):

- **M-item 1** [HYPOTHESIS, GROUNDED:corpus]: Web-scraped pretraining corpora already contain substantial AI-generated content produced by *many different* systems, not a single known model — the setting studied by `[RecursiveMultiEntity, OpenReview:JEU4PBaX85]`, whose own motivation states corpora "now contain substantial AI-generated content from many different systems." Auditing this contamination requires a *corpus-level* proportion estimate, not just per-document flags. `evidence: [{type: "citation", text: "JEU4PBaX85 motivation", source: "extracted", location: null}]`.
- **M-item 2** [HYPOTHESIS, GROUNDED:corpus]: Contamination fraction is causally consequential: `[IterativeRetrainStability, OpenReview:JORAfH2xFd]` shows the mixing parameter between real and synthetic data determines whether iterative retraining is stable or collapses. If the fraction matters for training decisions, then an estimator of that fraction that fails silently on unseen generators is dangerous precisely where it is used. `evidence: [{type: "citation", text: "JORAfH2xFd contraction condition on mixing parameter", source: "extracted", location: null}]`.
- **M-item 3** [HYPOTHESIS, GROUNDED:corpus]: Post-hoc text detectors are known to "degrade rapidly as generation quality improves, failing to generalize across model generations and sampling strategies" (`[Kirchenbauer-Watermark, OpenReview:aX8ig9X2a7]` motivation); paraphrasing is a realistic, low-cost further perturbation. Whether these failure modes propagate to *distributional* (aggregate) estimators — and how fast — is a prerequisite for trusting any contamination estimate used to filter training data. `evidence: [{type: "citation", text: "aX8ig9X2a7 motivation on detector degradation across generations", source: "extracted", location: null}]`.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper text exists to extract explicit motivation claims from; the three items are the digest-writer's reconstruction, though each is now anchored to a real corpus paper's stated motivation.", `why_matters`: "Motivation framing determines how strongly a reader should weight the eventual findings.", `implication`: "Read these as reconstructed stakes grounded in adjacent real work, not as this (nonexistent) paper's own asserted motivation."}

---

## N3 Related Works

**Corpus search performed** over `topics/corpus/ideas.jsonl` (11,683 OpenReview papers) with the provided keyword tool, six query angles: (1) `machine-generated text; detection; paraphras`, (2) `contamination; synthetic data; pretraining corpus`, (3) `proportion estimation; quantification; prevalence; mixture`, (4) `unseen; generalization; out-of-distribution detector; cross-model`, (5) `benchmark contamination; data leakage`, (6) `watermark; provenance; robustness attack; evade detection`. The MGT-detection and synthetic-contamination clusters returned strong ML-native hits; the entries below are the closest real neighbors. All are tagged [GROUNDED:corpus]; their *fit* to this future paper is the digest-writer's judgment, not an author's own related-work section.

`works`:

1. `citation_key`: "[DetectGPT, OpenReview:UiAyIILXRd]" — *DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature*. `approach_summary` [GROUNDED:corpus]: Zero-shot, per-passage detector that scores a candidate text by the local curvature of the source model's log-probability — comparing the passage's log-prob to the mean log-prob of T5 mask-fill perturbations; a consistent drop signals model-generated text. Requires access to (or a surrogate of) the *source* model's likelihood. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=UiAyIILXRd"}.
2. `citation_key`: "[Learn-to-Distance, OpenReview:2ZUPeEM3FH]" — *Learn-to-Distance: Distance Learning for Detecting LLM-Generated Text*. `approach_summary` [GROUNDED:corpus]: Rewrite-based per-passage detector that learns (rather than fixes) a distance between a text and its LLM rewrite via normalized log-likelihood, exploiting that machine text stays closer to its rewrite than human text; explicitly notes curvature methods "depend strongly on assumptions" that break under distribution shift. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=2ZUPeEM3FH"}.
3. `citation_key`: "[D&R, OpenReview:FiMZSxo4DO]" — *D&R: Recovery-based AI-Generated Text Detection via a Single Black-box LLM Call*. `approach_summary` [GROUNDED:corpus]: Disrupt-and-Recover per-passage detector: within-chunk token shuffling, one black-box recovery call, and recovered-vs-original similarity as a proxy for posterior concentration; designed to work without likelihood access, but still a binary per-document decision. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=FiMZSxo4DO"}.
4. `citation_key`: "[MarkovCalibration, OpenReview:Lzwkeg2o2z]" — *Beyond Raw Detection Scores: Markov-Informed Calibration for Boosting Machine-Generated Text Detection*. `approach_summary` [GROUNDED:corpus]: Wraps existing metric detectors (DetectGPT/Fast-DetectGPT/DNA-GPT) in a pairwise-MRF calibration layer over token scores, treating token-level detector outputs as noisy unary evidence before passage-level aggregation. Directly formalizes the "aggregate noisy local scores into one decision" step that a distributional estimator generalizes. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=Lzwkeg2o2z"}.
5. `citation_key`: "[Kirchenbauer-Watermark, OpenReview:aX8ig9X2a7]" — *A Watermark for Large Language Models*. `approach_summary` [GROUNDED:corpus]: Embeds a detectable statistical signal at generation time by pseudorandomly green-listing the vocabulary and soft-biasing sampling; detection is a one-proportion z-test needing no model access. A *provenance* approach that requires cooperation at generation time — the complement of estimating contamination from generators you never controlled. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=aX8ig9X2a7"}.
6. `citation_key`: "[DRCT, OpenReview:oRLwyayrh1]" — *DRCT: Diffusion Reconstruction Contrastive Training towards Universal Detection of Diffusion Generated Images*. `approach_summary` [GROUNDED:corpus]: Improves detector generalization to *unseen* generators (diffusion image variants) by contrastive training on diffusion-reconstructed hard samples; its motivation documents that "detectors trained on a narrow set of models exhibit severe performance degradation when confronted with images from unseen diffusion variants" — the exact unseen-generator failure mode, in the image modality. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=oRLwyayrh1"}.
7. `citation_key`: "[RecursiveMultiEntity, OpenReview:JEU4PBaX85]" — *What happens when generative AI models train recursively on each others' outputs?*. `approach_summary` [GROUNDED:corpus]: Models multi-entity recursive training through a shared synthetic-data channel where each entity mixes reused real data with generation-indexed synthetic data produced by *all* entities; quantifies convergence toward homogeneity under a controlled synthetic-mixing fraction. Grounds the "many unknown generators contaminate a shared corpus" premise. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=JEU4PBaX85"}.
8. `citation_key`: "[IterativeRetrainStability, OpenReview:JORAfH2xFd]" — *On the Stability of Iterative Retraining of Generative Models on Their Own Data*. `approach_summary` [GROUNDED:corpus]: Theoretical fixed-point analysis of retraining on real+synthetic mixtures; derives conditions on the *mixing parameter* under which the retraining operator is a contraction (stable) rather than collapsing. Establishes that the contamination fraction is the causal quantity a contamination estimator must recover. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=JORAfH2xFd"}.
9. `citation_key`: "[PreferenceLeakage, OpenReview:grIvSXVJ65]" — *Preference Leakage: A Contamination Problem in LLM-as-a-judge*. `approach_summary` [GROUNDED:corpus]: Characterizes contamination arising when synthetic data from frontier LLMs leaks into an LLM-as-judge evaluation pipeline; measures the effect for known related generator/judge families. An adjacent contamination-measurement study bound to the specific model families it studies. `source`: extracted. `location`: {url: "https://openreview.net/forum?id=grIvSXVJ65"}.
10. `citation_key`: "[Gumbel-Max-Watermark-Proportions, arXiv:2607.00224]" — *Sample Complexities of Estimating Gumbel–Max Watermark Proportions with and without Reduction to Pivotal Statistics* [added on Phase A re-check, `discussion/reference_candidates.jsonl` — this arXiv:math.ST preprint surfaced in the 150-candidate harvest and is the closest prior work on the exact estimand]. `approach_summary` [GROUNDED:reference_candidates.jsonl, key `SampleComplexitiesofEsti700224`]: Derives matching information-theoretic lower bounds and near-optimal estimators (an event-counting estimator under full observation; a Laguerre-polynomial estimator under reduction to pivotal statistics) for the sample complexity of estimating the mixing proportion ε of Gumbel-max-watermarked LLM text within a document. `source`: extracted. `location`: {url: "https://arxiv.org/abs/2607.00224"}.

**Status:** FOUND (9 real corpus works discussed with grounded approach summaries, plus 1 arXiv work added on Phase A re-check — see `absence_comment`). `absence_comment`: {`what_missing`: "Item 10 (Gumbel-Max watermark proportion estimation) was not part of the original 6-query-angle OpenReview corpus search that produced items 1–9; it surfaced only from the separate 150-candidate `reference_candidates.jsonl` harvest, reviewed for the first time during this Phase A re-check.", `why_matters`: "Per guidance.md Part 4 situation 6, a method-twin discovered mid-run requires a paper.md repositioning, not a silent related-work addition — item 10 is the closest prior work on the *estimand* (a mixing proportion) of any cited work, closer than DRCT on that specific dimension.", `implication`: "paper.md's Related Work / baseline framing has been updated in this same Phase A pass (see paper.md's Step 5 note and Threats); `paper_draft.md`/`.tex` (already compiled, upstream of this re-check) still needs the same repositioning at the next Phase E pass — flagged in `discussion/stage_review.md`."}

---

## N4 Prior Limitations

`grounding_check`: `true` (every limitation below cites `affects_works` matching an N3 `citation_key` verbatim).

`limitations` (all [HYPOTHESIS] — reasoned inferences about what each cited work demonstrably does not cover relative to this idea's core question; each defensible from the cited paper's own motivation/method):

1. `limitation_text` [HYPOTHESIS]: "These are per-passage binary/score detectors that output a decision (or calibrated score) for a single document; none estimates a *corpus-level mixture proportion*, and none reports estimation error as a continuous function of held-out generator identity or paraphrase strength. Summing per-instance decisions is known to bias an aggregate proportion, which is exactly the aggregation step MarkovCalibration treats as noisy — but even there the target remains a per-passage label, not a corpus ratio." `affects_works`: `["[DetectGPT, OpenReview:UiAyIILXRd]", "[Learn-to-Distance, OpenReview:2ZUPeEM3FH]", "[D&R, OpenReview:FiMZSxo4DO]", "[MarkovCalibration, OpenReview:Lzwkeg2o2z]"]`. `limitation_type`: `generalizability`.
2. `limitation_text` [HYPOTHESIS]: "DetectGPT's perturbation-discrepancy score assumes access to the source model's likelihood (or a close surrogate) — a known-generator assumption. When the true generator is structurally unseen at calibration, the surrogate-likelihood signal is untested, and the method provides no characterization of its degradation rate across a family of held-out generators." `affects_works`: `["[DetectGPT, OpenReview:UiAyIILXRd]"]`. `limitation_type`: `generalizability`.
3. `limitation_text` [HYPOTHESIS]: "Watermarking recovers provenance only for text produced under a cooperating, generation-time-instrumented model; it cannot estimate contamination from generators the auditor never controlled or watermarked. The paper's own motivation concedes that non-watermark post-hoc detectors 'degrade rapidly... failing to generalize across model generations and sampling strategies,' but offers no distributional estimator that remains reliable for such uncontrolled generators." `affects_works`: `["[Kirchenbauer-Watermark, OpenReview:aX8ig9X2a7]"]`. `limitation_type`: `generalizability`.
4. `limitation_text` [HYPOTHESIS]: "DRCT tackles the unseen-generator degradation directly, but (a) in the image modality, (b) by training-time hard-sample augmentation that produces a still-binary detector rather than a corpus-proportion estimator, and (c) without a paraphrase-strength (text-rewrite) stress axis or a quantified degradation *rate* across held-out generators." `affects_works`: `["[DRCT, OpenReview:oRLwyayrh1]"]`. `limitation_type`: `generalizability`.
5. `limitation_text` [HYPOTHESIS]: "These works treat the synthetic-mixing fraction as a *controlled input* to study downstream training dynamics (collapse/stability, homogenization); neither provides an *inverse* estimator that recovers an unknown contamination fraction from an observed corpus, and so neither addresses whether such recovery is robust when the contaminating generators were absent from any calibration set." `affects_works`: `["[RecursiveMultiEntity, OpenReview:JEU4PBaX85]", "[IterativeRetrainStability, OpenReview:JORAfH2xFd]"]`. `limitation_type`: `generalizability`.
6. `limitation_text` [HYPOTHESIS]: "Preference-leakage contamination is measured for specific, related generator/judge families used in the study design; the analysis does not test corpus-level proportion error under a leave-one-generator-out protocol, nor degradation as a function of paraphrase-attack strength." `affects_works`: `["[PreferenceLeakage, OpenReview:grIvSXVJ65]"]`. `limitation_type`: `generalizability`.
7. `limitation_text` [HYPOTHESIS, added on Phase A re-check per reference-cache freshness sweep — guidance.md Part 4 situation 6]: "[Gumbel-Max-Watermark-Proportions, arXiv:2607.00224] derives information-theoretic sample-complexity bounds and near-optimal estimators (event-counting; Laguerre-polynomial under pivotal reduction) for the *same estimand* this paper targets — a mixing proportion of machine-generated vs. human text in an observed sample — making it the closest prior work on the estimand itself, closer than DRCT on the *estimator* dimension even though DRCT remains closer on the *unseen-generator* dimension. Its estimator is provably sample-efficient only under a cooperative watermarking assumption (a known pseudorandom green-list scheme) and reports no result for a generator absent from that scheme, nor for paraphrase-attacked text; it does not address whether proportion estimation remains reliable for an uncooperative, structurally unseen generator, which is this paper's core question." `affects_works`: `["[Gumbel-Max-Watermark-Proportions, arXiv:2607.00224]"]`. `limitation_type`: `generalizability`.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper text exists to extract explicit prior-limitations claims from; each item above is the digest-writer's reasoned inference from the cited work's own stated scope/assumptions, not an author-conceded limitation.", `why_matters`: "A reviewer needs to know these limitations were derived, not quoted, so their defensibility rests on the cited paper's own methodology matching the summary above.", `implication`: "Re-verify each `affects_works` link against the cited paper directly before using any limitation as a novelty argument in prose."}

---

## N5 Challenges

`conflation_check`: `true` (each challenge below is distinct).

`challenges` [HYPOTHESIS, tightly derived from the core question — properties of the problem itself, not failures of any named prior tool]:

- `id`: "C1", `text`: "The space of possible text generators (model families, fine-tunes, decoding configurations) is open-ended and continually growing, so no calibration set can be exhaustive; any estimator must generalize out-of-distribution to a structurally unseen generator, not merely an unseen sample from a known one."
- `id`: "C2", `text`: "Paraphrasing can be applied at continuously variable strength, smoothly interpolating between clearly-synthetic and clearly-human text, so the true/false separability boundary — and any single scalar contamination estimate — is inherently unstable near the margin, independent of which estimator is used."
- `id`: "C3", `text`: "Real-world corpora have no independently verified ground-truth label for their true synthetic-text fraction; controlled mixtures with known ratios are the only setting in which estimator error is directly measurable, so validation is necessarily confined to a proxy setting that may not transfer to real corpora."
- `id`: "C4", `text`: "Generator identity and paraphrase strength are confounded stress factors that act simultaneously on any statistical signature; isolating which one drives degradation (versus their interaction) is statistically difficult with a finite generator/paraphrase pool."
- `id`: "C5", `text`: "Estimating an aggregate proportion by thresholding-and-summing per-instance classifier scores is systematically biased under distribution shift (the quantification-learning problem); the bias itself moves with the held-out generator, so the estimator's error cannot be corrected by a fixed calibration constant."

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "There is no author-stated challenges section to extract because no paper exists; C1–C5 are the digest-writer's decomposition of the seed's core question into distinct technical difficulties.", `why_matters`: "A reviewer should not treat C1–C5 as claims the (nonexistent) paper makes about itself — they are the problem's inherent difficulties, used downstream to justify each method component (N6 `challenge_arguments`).", `implication`: "Re-derive this list from the actual paper's own stated challenges once (if) it is written; verify no challenge was silently dropped or merged in that process."}

---

## N6 Methodology

**`overview`** [HYPOTHESIS]: "The study constructs controlled synthetic/human text corpora at known mixture ratios from a pool of several LLM generators, and evaluates candidate corpus-level (distributional) contamination-ratio estimators under two orthogonal stress protocols. **Staged plan.** *Stage 1 — Pilot (the seed's minimal experiment):* on a small generator pool (~5 generators) and one text domain, run leave-one-generator-out (LOGO) cross-validation crossed with a paraphrase-strength sweep, plotting estimation-error curves against the controlled ground-truth ratio; this is the smallest experiment that answers RQ1 directionally. *Stage 2 — Scale-up:* expand to a larger, architecturally diverse generator pool (10–15 generators spanning ≥3 families and multiple decoding configs), multiple mixture ratios (e.g., 0.05–0.5), and a search over candidate statistical features for one whose class-conditional separability stays stable across both axes (RQ2), with bootstrap confidence intervals and a mixed-effects model to disentangle generator vs. paraphrase effects (C4)."

**`key_components`** [HYPOTHESIS] — operationalized (what is measured/built, with what instrument, at what granularity):
- `id`: "M1", `name`: "Controlled corpus + LOGO construction", `text`: "Instrument: a corpus builder that samples a human base set (e.g., news/web prose) and a synthetic set generated by each pool generator, then mixes them at a programmatic ratio r∈{0.05,0.1,0.2,0.3,0.5}. Granularity: per document, with a per-corpus manifest recording (source generator, true label, mixture ratio). LOGO: one generator's documents are excluded from all estimator-calibration data and used only in the held-out test corpus. Output measured: true r (exact, by construction)."
- `id`: "M2", `name`: "Paraphrase-strength sweep", `text`: "Instrument: a parameterized paraphrase pipeline (paraphraser model ∈ {DIPPER-style, instruction-tuned rewriter}; strength = number of recursive rewrite rounds k∈{0,1,2,3} × decoding temperature). Granularity: applied to the synthetic portion only, per document, before mixing. Output measured: paraphrase strength index and a semantic-fidelity check (embedding cosine to the pre-paraphrase text) to confirm meaning preservation."
- `id`: "M3", `name`: "Candidate distributional-estimator suite", `text`: "Built estimators: (a) classify-and-count with a supervised MGT classifier; (b) quantification-corrected classify-and-count (adjusted-count / EM prior-shift correction) to counter C5's shift bias; (c) a zero-shot aggregate over per-passage detector scores from N3 (DetectGPT-, Learn-to-Distance-, D&R-style) pooled to a corpus ratio; (d) a distribution-matching estimator (Kullback-Leibler / MMD between the test corpus feature histogram and calibrated human/synthetic references). Granularity: one estimated ratio r̂ per test corpus."
- `id`: "M4", `name`: "Error-curve evaluation", `text`: "Instrument: computes bias (E[r̂]−r) and variance of r̂ against true r, aggregated per held-out generator and per paraphrase-strength level, with nonparametric bootstrap CIs (≥1000 resamples). Output: estimation-error curves along the LOGO axis and the paraphrase-strength axis, plus a degradation-slope statistic (Δ error per unit paraphrase strength)."
- `id`: "M5", `name`: "Generator-invariance probe", `text`: "Instrument: for each candidate feature family (perplexity/log-likelihood under a reference model; stylometric n-gram and burstiness statistics; sentence-embedding directions), measure human-vs-synthetic separability (AUROC / effect size) within each held-out generator × paraphrase-strength cell, then test whether separability is statistically flat across cells (variance-components analysis). Output: a ranked list of features by cross-condition stability, and a pass/fail on 'fully invariant feature exists.'"

**`challenge_arguments`** [HYPOTHESIS — a predicted argument structure, not a reported author claim]:
- `challenge_id`: "C1", `argument_text`: "Holding an entire generator out of calibration (not just a sample) operationalizes generalization to a structurally unseen generator directly.", `mechanism_components`: `["M1"]`.
- `challenge_id`: "C2", `argument_text`: "Sweeping paraphrase strength continuously (rounds × temperature) turns the unstable margin into a measured error curve instead of a binary pass/fail judgment.", `mechanism_components`: `["M2", "M4"]`.
- `challenge_id`: "C4", `argument_text`: "Crossing the LOGO axis with the paraphrase-strength axis in one factorial evaluation, then fitting a mixed-effects model with generator and paraphrase as separate factors, reads off whether degradation tracks generator identity, paraphrase strength, or their interaction.", `mechanism_components`: `["M1", "M2", "M4"]`.
- `challenge_id`: "C4", `argument_text`: "The generator-invariance probe searches for a feature stable across both confounded axes at once, addressing the disentanglement difficulty at the feature level.", `mechanism_components`: `["M5"]`.
- `challenge_id`: "C5", `argument_text`: "Including a quantification-corrected estimator (prior-shift/adjusted-count) alongside naive classify-and-count isolates how much of the LOGO degradation is the aggregate proportion bias rather than the base classifier's per-instance error.", `mechanism_components`: `["M3", "M4"]`.

**`unaddressed_challenges`**: `["C3"]` — [HYPOTHESIS] the minimal experiment uses only controlled synthetic mixtures with researcher-defined ground truth; it proposes no mechanism for validating estimator error on real, unlabeled corpora, so C3 (no ground truth outside the controlled setting) remains open by design.

**`feasibility`** [HYPOTHESIS]:
- *Order of magnitude.* Generators: ~5 (pilot) → ~12 (scale-up). Documents: ~2k synthetic per generator + ~10k human base ≈ 20–25k generated documents; paraphrase sweep multiplies synthetic docs by ~4 (k∈{0,1,2,3}) → ~40k paraphrase calls. Estimator runs: 4 estimators × (5 or 12 LOGO folds) × 4 paraphrase levels × 5 mixture ratios × ≥1000 bootstrap resamples for CIs. Compute class: generation + paraphrasing dominate — a few hundred GPU-hours on open 7–13B models, or low-thousands-of-dollars API cost if using hosted generators; estimator evaluation itself is CPU/GPU-light. Annotator-hours: ~0 required (ground truth is synthetic by construction); a small human spot-check of paraphrase fidelity (~10–20 hours) is optional.
- *Biggest feasibility risk + mitigation.* Risk: the "unseen generator" gap is confounded by paraphrase-fidelity drift — heavy paraphrasing can push synthetic text off-manifold in ways that spuriously inflate (or deflate) estimator error and masquerade as a generator effect. Mitigation: gate every paraphrased document on the embedding-cosine fidelity check in M2, report results stratified by fidelity band, and include a k=0 (no-paraphrase) control column so the pure LOGO effect is always separable from the paraphrase effect.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No Methods section exists to extract because no paper/study has been conducted; `overview`, `key_components` (M1–M5), `challenge_arguments`, and `feasibility` are the digest-writer's proposed instrumentation for answering RQ1/RQ2, not a reported implementation.", `why_matters`: "Downstream tools (paper.md, paper-writer) treat M1–M5 as the method to *pre-register and then execute*, not as results already obtained — conflating the two would misrepresent an unexecuted plan as a completed method.", `implication`: "Once (if) the study runs, replace this section with the actually-implemented method, keeping the same M-ids where the design didn't change so `paper.md`'s cross-references stay valid."}

---

## N7 Contributions

`contributions` [HYPOTHESIS]:

- `id`: "CO1", `text`: "An empirical characterization of how fast corpus-level contamination/proportion estimators degrade when the text generator is held out of calibration (leave-one-generator-out).", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id`: "CO2", `text`: "An empirical characterization of how estimator error scales with paraphrase-attack strength, independent of and in interaction with generator identity.", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id`: "CO3", `text`: "Either the identification of a candidate generator-invariant statistical feature for contamination estimation, or a rigorous negative result establishing that no such feature was found among those tested.", `contribution_type`: `empirical_finding`, `is_testable`: `true`, `has_rq`: `true`.
- `id`: "CO4", `text`: "A reusable stress-testing protocol (controlled-mixture test suite + LOGO cross-validation + paraphrase-strength sweep + quantification-corrected estimator baselines) for evaluating the robustness of future contamination estimators.", `contribution_type`: `technical_artifact`, `is_testable`: `false`, `has_rq`: `false`.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper exists, so CO1–CO4 are not asserted contributions but the digest-writer's prediction of what the eventual paper would claim if the pre-registered experiments in `paper.md` Step 6 are run as designed.", `why_matters`: "A reviewer must not cite CO1–CO4 as an established result; they are conditional on RQ1/RQ2 actually being answered by the (not-yet-run) study.", `implication`: "Downstream (paper.md, claim_map.md) treats CO1–CO3 as `needs-experiment` and CO4 as `supported-by-design`, matching Phase D's verdict-lookup discipline once real results exist."}

---

## N8 Research Questions

`research_questions`:

- `id`: "RQ1", `text`: "语料级占比估计器对未见过的生成器和改写攻击的退化速率是多少？(What is the degradation rate of corpus-level proportion estimators under (a) leave-one-generator-out cross-validation and (b) a paraphrase-strength sweep?)" [GIVEN — near-verbatim restatement of the seed's core question, first clause], `rq_source`: `"explicit"`, `evaluates_mechanisms`: `["M1", "M2", "M3", "M4"]`, `addresses_challenges`: `["C1", "C2", "C4", "C5"]`, `tests_contributions`: `["CO1", "CO2"]`, `answered_by_experiment`: "LOGO cross-validation crossed with a paraphrase-strength sweep, reading estimation-error curves against true controlled-mixture ratios; degradation quantified as the in-distribution→LOGO bias increase and the error slope per paraphrase level." [HYPOTHESIS for the experiment description, GIVEN for the RQ text itself]
- `id`: "RQ2", `text`: "存在生成器不变的统计特征吗？(Does a generator-invariant statistical feature exist that preserves separability across held-out generators and paraphrase strengths?)" [GIVEN — near-verbatim restatement of the seed's core question, second clause], `rq_source`: `"explicit"`, `evaluates_mechanisms`: `["M5"]`, `addresses_challenges`: `["C4"]`, `tests_contributions`: `["CO3"]`, `answered_by_experiment`: "Feature-invariance probe (AUROC/effect-size per LOGO × paraphrase-strength cell) with a variance-components test for cross-cell flatness." [HYPOTHESIS]

**Evaluation design** [HYPOTHESIS]:

`datasets`: `{names: ["M4 news base corpus (human side: real news/web prose, e.g. a RealNews / C4-RealNewsLike subset)", "MGTBench / RAID-style multi-generator machine-text collections as the synthetic side and cross-check", "HC3 (Human-ChatGPT Comparison Corpus) as an auxiliary in-domain human/synthetic reference", "DIPPER-paraphrased variants of the synthetic portion at k∈{0,1,2,3} rewrite rounds"], source: "inferred"}` — these are real, widely-used MGT-evaluation resources that genuinely fit a controlled-mixture, multi-generator setup; the controlled mixtures are constructed by the authors from them.

`baselines`: `{names: ["Naive classify-and-count with a supervised MGT classifier (lower-bar)", "Quantification-corrected classify-and-count (adjusted-count / EM prior-shift)", "Zero-shot per-passage detectors pooled to a corpus ratio — DetectGPT [UiAyIILXRd], Learn-to-Distance [2ZUPeEM3FH], D&R [FiMZSxo4DO]", "MarkovCalibration-wrapped detector [Lzwkeg2o2z] pooled to a ratio", "Distribution-matching (MMD/KL) estimator"], source: "inferred"}` — drawn from N3.

`metrics`: `{names: ["Estimation bias = E[r̂] − r (signed) and |E[r̂] − r| (absolute), per condition", "Estimator variance / bootstrap CI width of r̂", "LOGO generalization gap = (LOGO absolute error) − (in-distribution absolute error)", "Degradation slope = Δ(absolute error) per paraphrase-strength level", "Feature separability = AUROC (human vs synthetic) per LOGO × paraphrase cell, and its cross-cell variance"], source: "inferred"}`.

**Analysis plan** [HYPOTHESIS]: Sample size — ≥1000 documents per (generator, paraphrase-level, mixture-ratio) cell so a 0.03 absolute-error difference is detectable. Statistical test — for RQ1, a linear mixed-effects model with fixed effects for validation regime (in-dist vs LOGO) and paraphrase strength and a random intercept per generator; report the regime coefficient and the paraphrase-strength slope with 95% bootstrap CIs. For RQ2, a variance-components / Levene-style test that a feature's per-cell AUROC is statistically flat (H0: cross-cell variance = 0). Significance threshold — α = 0.05, Holm-corrected across the estimator suite. Expected effect direction — LOGO error > in-distribution error; absolute error increases monotonically with paraphrase strength. Cells below the ≥1000-document power floor are pre-declared **INCONCLUSIVE**, not null (guidance.md Part 4 situation 5) — this is stated explicitly in `paper.md`'s Step 6/9 fix applied in this Phase A re-check.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper exists, so RQ1/RQ2, the evaluation design, and the analysis plan are the digest-writer's pre-registration draft, not a reported study design.", `why_matters`: "`paper.md` Step 6 elevates this section into binding hypotheses (H1–H3) with effect floors and verbatim fallbacks — a reviewer needs to know the chain of authorship (seed → this digest → paper.md), not read N8 as an author's own methods section.", `implication`: "Any change to RQ1/RQ2 wording after this point must propagate to `paper.md`'s H1/H2/H3 and back to this section — they must stay in lockstep (checked by Phase A checklist item 4, Claim–Evidence Map completeness)."}

---

## N9 Results

**CRITICAL — no paper exists, so no numbers are reported.** Every result below is
`source`: **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**, `evidence_strength`: `"missing"`,
`rq_answered`: `false`. Each includes an explicit falsification condition.

- `rq_id`: "RQ1", `result_text`: "[HYPOTHESIZED DIRECTION] Estimation error increases both under leave-one-generator-out validation (relative to in-distribution validation) and as paraphrase strength increases, with the two effects compounding; the quantification-corrected estimator degrades more slowly than naive classify-and-count but does not fully close the LOGO gap.", `result_type`: `quantitative`, `evidence_strength`: `"missing"`, `rq_answered`: `false`. **Falsification condition:** refuted if the mixed-effects regime coefficient is not significantly positive (LOGO error statistically indistinguishable from in-distribution error across tested generators) and/or the paraphrase-strength slope is ≤ 0.
- `rq_id`: "RQ2", `result_text`: "[HYPOTHESIZED DIRECTION] No single candidate feature remains fully generator-invariant across both stress axes simultaneously; at most partial/relative invariance is observed (some features degrade more slowly than others, none statistically flat).", `result_type`: `quantitative`, `evidence_strength`: `"missing"`, `rq_answered`: `false`. **Falsification condition:** refuted if some candidate feature's per-cell AUROC passes the flatness test (cross-cell variance not significantly > 0) across all held-out generators and paraphrase strengths — that outcome would instead support existence of a generator-invariant feature.

---

## N10 Threats / Self-Limitations

`threats` [HYPOTHESIS — anticipated limitations of this kind of study; no paper exists, so nothing here is author-stated]:

- `threat_id`: "t1", `category`: `external`, `description`: "Findings are limited to the specific pool of generators and paraphrasers tested; degradation rates and feature-invariance conclusions may not extend to future, architecturally different generator families.", `mitigation`: "Span ≥3 model families and multiple decoding configs in the scale-up pool; report the LOGO gap per held-out generator so readers can gauge variance across generator types rather than a single pooled number."
- `threat_id`: "t2", `category`: `construct`, `description`: "The controlled clean-binary-mixture operationalization of 'contamination ratio' may not represent real-world contamination such as iterative human-AI co-writing or partial post-editing, which don't reduce to a per-document synthetic/human label.", `mitigation`: "Include at least one partial-post-editing condition (paraphrase applied to a fraction of each document) as a robustness probe, and state explicitly that C3 (no real-corpus ground truth) bounds external construct validity."
- `threat_id`: "t3", `category`: `internal`, `description`: "The paraphrase-strength parameterization (rounds × temperature) is a design choice that may not correspond monotonically to real adversarial paraphrase strategies, and heavy paraphrasing can push text off-manifold, confounding the generator effect.", `mitigation`: "Gate every paraphrased document on an embedding-cosine fidelity check (M2), stratify results by fidelity band, and always include a k=0 no-paraphrase control column."
- `threat_id`: "t4", `category`: `conclusion`, `description`: "With a finite generator pool, the LOGO folds are not independent (generators from one family share artifacts), so naive per-fold significance tests may overstate confidence in the degradation-rate estimate.", `mitigation`: "Use a mixed-effects model with a random intercept per generator family and report bootstrap CIs that resample generators, not just documents."
- `threat_id`: "t5", `category`: `reproducibility`, `description`: "Distributional-estimator and detector baselines are numerous and inconsistently implemented; relative-robustness conclusions may be sensitive to the specific baseline implementations chosen.", `mitigation`: "Release the controlled-mixture manifests, paraphrase pipeline configs, and estimator code (CO4) so baselines are re-runnable on the identical corpora."
- `threat_id`: "t6", `category`: `scope`, `description`: "The study is likely restricted to one language (English) and one text domain (news/web prose), limiting applicability to code, multilingual text, or multimodal contamination.", `mitigation`: null.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "There is no Threats-to-Validity section to extract because no paper exists; the items above are the digest-writer's anticipation, now with concrete mitigations.", `why_matters`: "A reviewer should not treat these as author self-disclosures — they are predictions about what limitations this class of study typically has.", `implication`: "Re-derive this section from the actual paper's own Limitations section once (if) it is written."}

---

## N11 Artifacts

`artifacts`: `[]`. `has_code`: `false`. `has_data`: `false`. `has_model`: `false`.

**Status:** NOT_FOUND. `absence_comment` [PLACEHOLDER]: {`what_missing`: "No code, dataset, or model has been released because no paper or study exists yet for this seed idea.", `why_matters`: "Artifact availability is a standard reviewer signal for empirical reproducibility; its absence here is total and by construction.", `implication`: "Not reviewer-relevant signal about a real paper's rigor — it reflects that the work has not been performed. Revisit once (if) the study is conducted and the CO4 protocol/artifacts are released."}

---

## N12 Contribution Type

`value`: `"empirical"` [HYPOTHESIS]

`rationale` [HYPOTHESIS]: "The core deliverable is a measurement study of an existing phenomenon — how fast known corpus-level estimator designs degrade under two realistic stress conditions (unseen generators, paraphrase strength) and whether a generator-invariant feature exists — validated by estimation-error curves and a feature-invariance test against a controlled ground-truth ratio (N9/RQ1–RQ2), not by introducing a new system or a benchmark as the primary product. This mirrors the classification logic of the exemplar empirical best-papers (e.g., NeurIPS_2025 'Why Diffusion Models Don't Memorize', which is `empirical` because its scaling-law measurements are the deliverable). If the eventual paper instead centers on releasing the controlled test suite (CO4) as a reusable benchmark, reclassify to `benchmark`."

`source`: `"inferred"`.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper exists to state its own contribution type; `empirical` is the digest-writer's classification by analogy to the cited exemplar (NeurIPS 2025 'Why Diffusion Models Don't Memorize'), not a self-declaration.", `why_matters`: "The contribution-type gates which archetype evidence standard (guidance.md Part 2) the eventual paper is held to; misclassifying it here would let the wrong evidence bar apply downstream.", `implication`: "Reclassify to `benchmark` if CO4 (the stress-testing protocol) ends up being the paper's headline deliverable rather than CO1–CO3 (the measured degradation law and feature-invariance verdict), per the rationale's own stated trigger condition."}

---

## Claims

1. [HYPOTHESIS] "Corpus-level (distributional) proportion estimators degrade significantly faster under leave-one-generator-out validation than under in-distribution validation." `evidence`: `[{type: "argument", text: "Follows from C1 (open-ended generator space) and C5 (shift-dependent quantification bias), operationalized by the LOGO design of M1 and the estimator suite M3; the unseen-generator failure mode is documented in the image modality by DRCT [oRLwyayrh1] and asserted for text detectors by Kirchenbauer-Watermark [aX8ig9X2a7].", source: "inferred", location: null}]`.
2. [HYPOTHESIS] "Estimation error increases with paraphrase-attack strength, independent of and possibly compounding with generator novelty." `evidence`: `[{type: "argument", text: "Follows from C2 (continuously variable, unstable separability margin) and the sweep/error-curve design of M2/M4.", source: "inferred", location: null}]`.
3. [HYPOTHESIS] "Quantification-corrected estimators (prior-shift/adjusted-count) degrade more slowly than naive classify-and-count but do not fully close the LOGO gap." `evidence`: `[{type: "argument", text: "Follows from C5 and the estimator contrast in M3; the aggregation-of-noisy-scores failure is formalized by MarkovCalibration [Lzwkeg2o2z].", source: "inferred", location: null}]`.
4. [PLACEHOLDER] "Whether any generator-invariant statistical feature exists for robust contamination estimation is fully open; the paper's central deliverable is either such a feature or a rigorous negative result — not knowable in advance." `evidence`: `[{type: "argument", text: "This is RQ2, posed as an open question in the seed's core question rather than something the seed asserts an answer to.", source: "extracted", location: null}]`.
5. [HYPOTHESIS] "Findings will likely be specific to the tested generator/paraphraser pool and may not generalize to future architectures — an anticipated external-validity limitation reviewers should probe regardless of the main result's direction." `evidence`: `[{type: "argument", text: "Standard external-validity concern for any leave-one-X-out study with a finite X pool; mitigated but not eliminated by spanning ≥3 model families (t1).", source: "inferred", location: null}]`.
