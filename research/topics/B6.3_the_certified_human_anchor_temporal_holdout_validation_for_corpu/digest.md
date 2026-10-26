# Digest: The Certified-Human Anchor: Temporal Holdout Validation for Corpus-Level AI-Content Estimators

> **REVERSE-DIGEST DISCLAIMER.** No paper exists yet. This is speculative scaffolding for
> research planning, built backward from a one-paragraph seed idea (topic code **B6.3**,
> parent topic **B6. 污染机制层（合成语料）/ Contamination Mechanism Layer (Synthetic Corpus)**,
> label **[证据] / "Evidence"**). Every field below is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README; **[HYPOTHESIS]** = reasoned
> elaboration grounded in the seed + standard practice, explicitly a prediction, not a fact;
> **[GROUNDED:corpus]** = an N3 entry drawn from a real OpenReview paper in the local
> `topics/corpus/ideas.jsonl`; **[PLACEHOLDER]** = genuinely unknowable until the work is done
> (never invented). No numeric result, author name, or identifier below is real, except the
> OpenReview paper ids in N3, which are real corpus records.

---

## N0 Metadata

- **title** [GIVEN]: "The Certified-Human Anchor: Temporal Holdout Validation for Corpus-Level AI-Content Estimators" — verbatim from seed README.
- **authors** [PLACEHOLDER]: `["Anonymous"]` — paper unwritten, no authors exist yet.
- **abstract** [HYPOTHESIS] (drafted, not real — synthesized from the seed's core question + minimal experiment):
  > "Corpus-level AI-content estimators — methods that report what *fraction* of a corpus is
  > AI-generated rather than labeling individual documents — are calibrated against a corpus
  > presumed 'certified human,' most often text authored before the ~November 2022 release of
  > ChatGPT, on the assumption that such text cannot itself be LLM-contaminated. We ask what
  > form of error bound this pre-2022 anchor can actually license, and how much of that bound
  > is eroded by an orthogonal confound: human writing style is not static, and secular
  > stylistic drift alone could inflate an estimator's false-positive rate on human text
  > regardless of any actual AI contamination. Using a temporal-holdout protocol, we measure
  > false-positive-rate drift across year-stratified slices of certified pre-2022 human corpora,
  > propagate it into the bias of a mixture-based prevalence estimator, and derive boundary
  > conditions (a time-window / genre / domain validity envelope) under which the pre-2022
  > anchor's implied error guarantee remains valid."
- **doi** [PLACEHOLDER]: `null`.
- **arxiv_id** [PLACEHOLDER]: `null`.
- **num_pages** [PLACEHOLDER]: `null`.
- **research_area** [HYPOTHESIS]: `"NLP"` — measurement target is text corpora / writing style; could also file under AI/ML (detector calibration), but the object of study is NLP-centered.

**Status:** N/A (no FOUND/PARTIAL/NOT_FOUND applies pre-paper) — every field above is either GIVEN or explicitly marked speculative.

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS] (full predicate, built from the GIVEN core question):
  > "estimate the calibration error bound that a pre-2022 human-authored corpus can provide
  > when used as a certified-human negative anchor for corpus-level AI-content estimators,
  > and measure how much temporal distribution drift in human writing style — independent of
  > any actual AI contamination — erodes that bound, via a temporal-holdout protocol that
  > measures cross-year false-positive-rate on year-stratified human text and propagates the
  > drift into the bias of a mixture-based prevalence estimator."
  - Self-check: (1) kind of task = calibration/error-bound estimation + measurement study; (2) domain = AI-generated-text detection / corpus contamination; (3) outcome shape = an explicit error bound + stated boundary conditions. All three land.
- **inputs** [HYPOTHESIS] (inferred from the minimal experiment):
  1. "one or more corpus-level AI-content estimators (both instance-aggregating detectors and mixture/prevalence estimators) to be validated"
  2. "human-authored text with reliable publication-year metadata, spanning multiple years before and after the 2022 cutoff"
  3. "a designated pre-2022 cutoff date marking the nominal certified-human anchor boundary"
- **outputs** [HYPOTHESIS]:
  1. "an empirical false-positive-rate (FPR) drift curve as a function of publication year / temporal distance from the anchor"
  2. "explicit boundary conditions (a validity envelope: time window, domain, genre) under which the pre-2022 anchor's implied error bound holds"
- **constraints** [GIVEN] (the seed's explicit ground-truth/separability assumption, restated close to source): text authored strictly before the ~2022 LLM-proliferation point is treated as a certified human-authored negative sample, so any false positive measured against it is attributable only to detector error or stylistic drift — not to genuine AI-content contamination. This assumption is exactly what the seed's core question interrogates ("2022 年前语料作为认证人类负样本").
- **Source discipline:** objective/inputs/outputs = HYPOTHESIS (inferred, anchored to the seed's minimal experiment); constraints = GIVEN.

---

## N2 Motivation

[HYPOTHESIS — reconstructed from the parent-topic framing and grounded in the N3 corpus, not from any published statistic]

- The corpus-level framing is now an active research direction, not a straw man: recent work
  reframes AI-text detection from per-document classification to *population-level prevalence
  estimation* precisely because instance-level detectors are unstable and biased, and it does
  so by modeling a target corpus as a mixture of a **human reference distribution** and an AI
  reference distribution ([MonitorAIScale, OpenReview:bX3J7ho18S]). That human reference *is*
  the certified-human anchor — so its validity is load-bearing for every prevalence estimate
  the method produces. [HYPOTHESIS, grounded]
- A near-universal convention is to source that human reference from pre-2022 text on the
  assumption it is LLM-free. But the anchor's *temporal* validity is asserted, not tested. If
  ordinary secular drift in human writing (vocabulary, syntax, topical fashion, platform
  conventions all shift over years, independent of any AI influence) inflates an estimator's
  FPR on human text, then the pre-2022 anchor silently injects an uncharacterized false-positive
  source — inflating reported AI-prevalence, or misattributing natural stylistic change to AI
  generation. [HYPOTHESIS]
- The broader contamination-detection literature shows that "seen vs. unseen" or "human vs. AI"
  gaps are far more fragile than assumed once distributions shift ([BenchContamFragility,
  OpenReview:bhR00j6Mku]; [MinKpp, OpenReview:ZGkfoufDaU]); by analogy, the temporal gap between
  a pre-2022 anchor and a present-day human sample is a distribution shift the field has not
  audited. This paper's premise: anchor validity is itself a contamination-adjacent
  methodological question deserving an explicit, reported error bound, not an assumption to wave
  away. [HYPOTHESIS, no evidence — the paper doesn't exist yet]

---

## N3 Related Works

**Corpus search performed** over `topics/corpus/ideas.jsonl` (11,683 OpenReview papers) with the
scratchpad keyword tool, from five angles: (a) AI-generated / machine-generated text detection
and detector false-positive behavior; (b) corpus-level / prevalence / proportion estimation of
AI content; (c) temporal distribution shift, concept drift, temporal holdout evaluation;
(d) benchmark/data contamination detection and its assumption fragility; (e) pre-training-data
/ membership-inference detectors and calibration. Nine real corpus papers are used below; all
are tagged `[GROUNDED:corpus]`. No corpus paper performs this exact study (temporal-holdout FPR-drift
bounding of a pre-2022 certified-human anchor), so N3 is genuinely adjacent grounding — see the
absence_comment. No non-corpus entries are included.

- **[MonitorAIScale, OpenReview:bX3J7ho18S]** `[GROUNDED:corpus]` — approach_summary: Reframes
  AI-text detection from instance classification to a *measurement* problem, estimating the
  fraction of AI-modified text in a corpus via a distributional maximum-likelihood framework
  that models the corpus as a mixture of a human-written reference distribution and an
  LLM-generated reference distribution over a stable vocabulary (e.g., adjectives), fitting a
  single mixing coefficient. Demonstrated on AI-conference peer reviews. This is the archetypal
  *corpus-level AI-content estimator* whose human reference corpus is the anchor under audit.
  url: https://openreview.net/forum?id=bX3J7ho18S
- **[LAMDA, OpenReview:1FnCrZtBNQ]** `[GROUNDED:corpus]` — approach_summary: Builds a longitudinal
  (2013–2025, >1M-app) benchmark to study concept drift in Android malware detection, holding a
  consistent static feature space fixed across years so that model-degradation-over-time can be
  measured cleanly; explicitly motivated by evidence that improper temporal evaluation inflates
  performance estimates. The methodological template for a temporal-holdout, year-stratified
  validation protocol. url: https://openreview.net/forum?id=1FnCrZtBNQ
- **[BenchContamFragility, OpenReview:bhR00j6Mku]** `[GROUNDED:corpus]` — approach_summary: Shows
  that benchmark-contamination detectors rest on a single operational assumption — seen members
  stay statistically distinguishable from unseen non-members — and stress-tests representative
  detector *families* (reference-based, reference-free, perturbation-based, output-distribution)
  to demonstrate the assumption breaks under staged post-training. The direct analogue of
  auditing the "pre-2022 = clean human" assumption across detector families.
  url: https://openreview.net/forum?id=bhR00j6Mku
- **[MarkovCalib, OpenReview:Lzwkeg2o2z]** `[GROUNDED:corpus]` — approach_summary: Treats a
  metric-based detector's token-level scores as noisy evidence and adds a Markov-random-field
  calibration layer before passage-level aggregation, explicitly because detectors built on
  noisy local evidence are brittle under paraphrasing and distribution shift. Evidence that
  detector calibration is distribution-shift-sensitive at the mechanism level.
  url: https://openreview.net/forum?id=Lzwkeg2o2z
- **[DetectGPT, OpenReview:UiAyIILXRd]** `[GROUNDED:corpus]` — approach_summary: Zero-shot
  machine-generated-text detection that thresholds the local probability-curvature of a passage
  under a source model, needing no trained classifier or labeled data. A canonical detector
  baseline whose per-document decisions would be aggregated into a corpus-level FPR.
  url: https://openreview.net/forum?id=UiAyIILXRd
- **[LearnToDistance, OpenReview:2ZUPeEM3FH]** `[GROUNDED:corpus]` — approach_summary: Rewrite-based
  detection that *learns* the distance between a text and its LLM rewrite (via normalized
  log-likelihood) rather than using fixed edit/semantic distances, explicitly because
  likelihood-based signals degrade when prompt or domain shifts. A modern detector whose known
  domain-shift sensitivity is precisely what temporal drift would exercise.
  url: https://openreview.net/forum?id=2ZUPeEM3FH
- **[MinKpp, OpenReview:ZGkfoufDaU]** `[GROUNDED:corpus]` — approach_summary: A reference-free
  pre-training-data detector (Min-K%++) scoring whether tokens are local maxima of the model's
  conditional distribution; motivated by the finding that membership heuristics degrade to
  near-random when training and non-training data are *closely matched*. Evidence that
  detector reliability collapses as two distributions converge — the temporal analogue of a
  human anchor drifting toward the present.
  url: https://openreview.net/forum?id=ZGkfoufDaU
- **[ContamICL, OpenReview:YlpaaYxx4t]** `[GROUNDED:corpus]` — approach_summary: Detects LLM data
  contamination at the *dataset* level via in-context-learning behavior, explicitly noting that
  sample-level contamination signals are easily confounded by distribution shift, motivating a
  collection-level rather than per-instance target. Direct support for corpus-level over
  instance-level estimation and for the distribution-shift confound.
  url: https://openreview.net/forum?id=YlpaaYxx4t
- **[DnR, OpenReview:FiMZSxo4DO]** `[GROUNDED:corpus]` — approach_summary: A single-call black-box
  detector (Disrupt-and-Recover) that shuffles tokens within chunks, asks an LLM to restore
  order once, and uses recovery similarity as a detection proxy — designed for closed-model,
  low-query settings. A deployment-realistic detector family to include in the estimator
  battery. url: https://openreview.net/forum?id=FiMZSxo4DO

**Status:** PARTIAL. **absence_comment:**
- `what_missing`: "No corpus paper performs a temporal-holdout validation of a pre-2022
  certified-human anchor or measures cross-year false-positive-rate drift for corpus-level
  AI-content estimators specifically; the closest, [MonitorAIScale, OpenReview:bX3J7ho18S],
  *uses* a human reference corpus but never audits its temporal validity."
- `why_matters`: "Without a direct precedent, N4's limitations are constructed from each cited
  paper's own stated scope (what it does and demonstrably does not cover) rather than from a
  prior study that attempted this exact question and fell short."
- `implication`: "Treat N3 as adjacent grounding, not as evidence this exact study has been
  attempted — which is itself informative: the seed idea occupies a genuine unaddressed gap
  sitting directly downstream of an active corpus-level-estimation line ([bX3J7ho18S])."

---

## N4 Prior Limitations

`grounding_check`: **true** [HYPOTHESIS] (every limitation cites ≥1 N3 citation_key, verbatim form).

- **limitation_text** [HYPOTHESIS]: "The mixture-based corpus prevalence estimator constructs its
  human reference distribution from a fixed reference corpus and treats it as an unproblematic
  ground truth; it does not test whether the *temporal composition* of that human reference
  confounds the estimated AI fraction, i.e., whether a human corpus drawn from a different era
  than the target corpus biases the mixing coefficient." — `affects_works`:
  `["[MonitorAIScale, OpenReview:bX3J7ho18S]"]`. `limitation_type`: `precision`.
- **limitation_text** [HYPOTHESIS]: "Detector-calibration and detection methods are validated
  against human samples drawn from the same contemporaneous distribution as the AI samples, and
  their known failure mode is distribution shift in prompt/domain — but none of them isolate or
  bound *temporal* shift in the human reference as a distinct axis, so a detector's FPR on
  temporally distant human text is uncharacterized." — `affects_works`:
  `["[DetectGPT, OpenReview:UiAyIILXRd]", "[LearnToDistance, OpenReview:2ZUPeEM3FH]", "[MarkovCalib, OpenReview:Lzwkeg2o2z]", "[DnR, OpenReview:FiMZSxo4DO]"]`.
  `limitation_type`: `generalizability`.
- **limitation_text** [HYPOTHESIS]: "Contamination/membership detectors are shown to degrade as
  the target and reference distributions converge or shift, and their assumption fragility is
  stress-tested across detector families — but this diagnosis stops at the seen/unseen or
  human/AI axis and is never turned into an explicit false-positive-rate bound as a function of
  temporal distance for a certified-human anchor." — `affects_works`:
  `["[BenchContamFragility, OpenReview:bhR00j6Mku]", "[MinKpp, OpenReview:ZGkfoufDaU]", "[ContamICL, OpenReview:YlpaaYxx4t]"]`.
  `limitation_type`: `theoretical`.
- **limitation_text** [HYPOTHESIS]: "The longitudinal concept-drift benchmark establishes that a
  temporally structured, feature-consistent corpus is needed to measure model degradation over
  time, but it targets malware classification and reports accuracy decay, not a calibrated
  false-positive-rate *bound* for a text negative-anchor — so its protocol must be adapted, not
  reused, for anchor validation." — `affects_works`: `["[LAMDA, OpenReview:1FnCrZtBNQ]"]`.
  `limitation_type`: `other`.

---

## N5 Challenges

`conflation_check`: **true** [HYPOTHESIS] (four genuinely distinct obstacles).

- **C1** [HYPOTHESIS]: "Confounding drift sources — an observed rise in false-positive rate over
  calendar years could stem from (a) genuine secular change in human writing style, (b) undetected
  AI-generated content leaking into nominally 'pre-2022 human' corpora, or (c) staleness of the
  estimator itself; these three cannot be disentangled from an FPR-vs-year curve alone." (N4-vs-N5
  test: about the problem's inherent identifiability, not any specific tool's failure — N5.)
- **C2** [HYPOTHESIS]: "No verifiable ground truth for 'certified human' — the 2022 cutoff is a
  metadata proxy, not a per-document certification; scraped corpora may contain pre-existing
  drafts revised later, translated or heavily edited text, or misdated records, so the anchor's
  actual purity is unverifiable at scale."
- **C3** [HYPOTHESIS]: "Non-stationarity of the estimator under test — a detector or reference
  distribution being validated may itself have been trained/estimated on data spanning multiple
  years, so both the anchor and the estimator carry independent temporal dependence, complicating
  the definition of a clean, single-point-in-time calibration reference."
- **C4** [HYPOTHESIS]: "Sparse and uneven historical coverage — pre-2022 human corpora suitable as
  a temporally-stratified anchor are unevenly distributed across genre, domain, and language,
  and per-year sample sizes shrink for older slices, limiting the years/domains over which drift
  can be reliably estimated."

---

## N6 Methodology

**overview** [HYPOTHESIS]: The paper constructs a year-stratified corpus of certified pre-2022
human-authored text (and matched post-2022 human text), runs a battery of existing corpus-level
AI-content estimators over each yearly slice, measures the empirical false-positive rate as a
function of publication year / temporal distance from the anchor, fits a trend/change-point model
to that curve, propagates the drift into the bias of a mixture-based prevalence estimator, and
translates the fit into explicit boundary conditions — a stated time window, genre, and domain
scope — within which the pre-2022 anchor's implied error bound can be trusted.
**Staged plan:** **(Pilot)** = the seed's minimal experiment — one genre (e.g., timestamped arXiv
abstracts or dated news), ~8–12 year buckets, 2–3 detectors, FPR-vs-year drift curve + boundary
condition, no scale-up. **(Scale-up)** = 3–4 genres/domains × multiple languages, the full
estimator battery including the mixture prevalence estimator, confound stress-tests, and a
statistically bounded validity envelope.

**key_components** [HYPOTHESIS] (ids assigned before challenge_arguments):
- **M1** — *Year-stratified anchor corpus construction*: assemble known-human text with reliable
  publication-year metadata pre-2022, at the granularity of one bucket per calendar year, drawn
  from timestamped sources (arXiv abstracts, dated news / CC-News, Project Gutenberg by first
  publication, Pushshift/Reddit by post date, dated Amazon reviews); balance per-year token count
  and genre so year is not confounded with topic. Instrument: metadata-filtered sampling with
  per-bucket size and genre logged.
- **M2** — *Estimator battery*: apply representative existing estimators to each yearly slice —
  zero-shot curvature ([DetectGPT, OpenReview:UiAyIILXRd]), rewrite/likelihood
  ([LearnToDistance, OpenReview:2ZUPeEM3FH]), black-box recovery ([DnR, OpenReview:FiMZSxo4DO]),
  and the corpus-level mixture estimator ([MonitorAIScale, OpenReview:bX3J7ho18S]) — at a fixed
  decision threshold, so drift is a property of the phenomenon not one detector's idiosyncrasy.
- **M3** — *FPR drift-curve estimation*: compute empirical FPR per year-bucket (fraction of
  certified-human documents flagged AI) and fit a trend/change-point model (e.g., segmented
  regression / Mann-Kendall trend) to quantify drift magnitude and any breakpoint as a function
  of temporal distance from the anchor.
- **M4** — *Error-bound / boundary-condition derivation*: translate the fitted curve into an
  explicit statistical bound — a confidence interval on FPR as a function of temporal distance —
  and identify the boundary (time window, genre, domain) beyond which the certified-human anchor's
  guarantee no longer holds at a stated confidence level.
- **M5** — *Confound stress-tests*: isolate stylistic drift from mislabeling/leakage confounds via
  held-out genres, synthetic-drift injection (controlled lexical/syntactic perturbation of a fixed
  human sample), and cross-domain replication — directly targeting C1/C2.
- **M6** — *Prevalence-estimator bias propagation*: hold the target corpus fixed and swap the human
  reference between year buckets in the mixture estimator ([MonitorAIScale, OpenReview:bX3J7ho18S]),
  measuring how the estimated AI-fraction shifts as the anchor ages — converting per-document FPR
  drift into a corpus-level estimand bias, the quantity that actually matters downstream.

**challenge_arguments** [HYPOTHESIS, argued by the (hypothetical) authors, not verified]:
- `challenge_id="C1"`, `mechanism_components=["M4","M5"]`: "Combining stress-tests (M5) with the
  explicit bound derivation (M4) lets us attribute the majority of observed FPR drift to stylistic
  change rather than corpus leakage or estimator staleness, though full disentanglement is not
  claimed."
- `challenge_id="C2"`, `mechanism_components=["M1"]`: "Using multiple independent,
  strongly-provenanced pre-2022 sources (M1) minimizes — but does not eliminate — the risk that a
  single mislabeled or misdated document distorts the anchor."
- `challenge_id="C3"`, `mechanism_components=["M2","M6"]`: "Testing multiple estimator families (M2)
  and separately probing the mixture estimator's reference dependence (M6) argues that observed
  drift is a property of the anchor/drift phenomenon rather than any one estimator's training cutoff."
- `challenge_id="C4"`, `mechanism_components=["M1"]`: "Deliberately sourcing slices across multiple
  decades and reporting per-bucket sample sizes (M1) argues for adequate historical range despite
  acknowledged uneven genre/domain/language coverage."

**unaddressed_challenges** [HYPOTHESIS]: `["C2"]` — even with M1's provenance controls, full
certification of "no AI involvement whatsoever" in any pre-2022 document is fundamentally
unverifiable at corpus scale; flagged as residual, not solved.

**feasibility** [HYPOTHESIS]:
- *Effort / compute (order of magnitude).* Pilot: ~10 year-buckets × ~3,000 human documents ≈
  30k documents × ~3 detectors ≈ ~10^5 detector inferences. Zero-shot curvature and rewrite
  detectors need 1 local LM forward pass (plus a few perturbations) per document — a few GPU-days
  on a single mid-size GPU; the black-box and mixture estimators add ~10^4–10^5 API calls (a
  low-hundreds-USD API cost class). Scale-up (4 genres × 2 languages × full battery ≈ ~10^6
  inferences) is a low-thousands-USD / single-node-week compute class. No model training or human
  annotation is required for the core measurement; a small validation set (~1–2k documents,
  ~40–80 annotator-hours) may be used to spot-check anchor purity.
- *Biggest feasibility risk + mitigation.* The dominant risk is C4-adjacent: **year is confounded
  with genre/topic/source** in available corpora (older slices are thinner and skew to books /
  formal text), so an apparent FPR-vs-year slope could be a genre effect. Mitigation: fix a single
  source with continuous long-span coverage per experiment (e.g., arXiv abstracts 2007–2022 or a
  single continuously-archived news source), match per-year token budgets, and use M5's
  synthetic-drift injection on a *fixed* human sample as a genre-controlled sanity check that
  isolates temporal style change from source composition.

---

## N7 Contributions

- **CO1** [HYPOTHESIS] `contribution_type="empirical_finding"`, `is_testable=true`, `has_rq=true`:
  "A year-stratified, temporal-holdout certified-human benchmark methodology for stress-testing the
  validity of AI-content-estimator negative anchors."
- **CO2** [HYPOTHESIS] `contribution_type="empirical_finding"`, `is_testable=true`, `has_rq=true`:
  "An empirical measurement of false-positive-rate drift as a function of temporal distance from a
  pre-2022 human-text anchor, across multiple detector families, and its propagation into
  corpus-level prevalence-estimator bias."
- **CO3** [HYPOTHESIS] `contribution_type="theoretical_result"`, `is_testable=true`, `has_rq=true`:
  "Explicit boundary conditions (a stated validity envelope: time window, genre, domain) under
  which pre-2022 corpora can serve as certified-human negative samples with a quantified error
  bound."
- **CO4** [HYPOTHESIS] `contribution_type="conceptual_framework"`, `is_testable=false`,
  `has_rq=false`: "A cautionary methodological recommendation for the broader
  contamination-detection literature: pre-2022-anchor validity should be explicitly bounded and
  reported, not assumed."

---

## N8 Research Questions

- **RQ1** [GIVEN] (near-verbatim restatement of the seed's core question, part 1): "What form of
  error bound can pre-2022 corpora, used as certified-human negative samples, provide to
  corpus-level AI-content estimators?" `rq_source="explicit"`. `evaluates_mechanisms=["M3","M4"]`.
  `addresses_challenges=["C2","C3"]`. `tests_contributions=["CO1","CO3"]`. `answered_by_experiment`:
  "cross-year FPR measurement on a fixed-source certified-human corpus and derivation of a
  confidence-bounded FPR envelope, per the minimal experiment."
- **RQ2** [GIVEN] (near-verbatim restatement of the seed's core question, part 2): "To what extent
  does temporal distribution drift in human writing style itself contaminate the validity of this
  pre-2022 anchor?" `rq_source="explicit"`. `evaluates_mechanisms=["M1","M3","M5"]`.
  `addresses_challenges=["C1","C4"]`. `tests_contributions=["CO2"]`. `answered_by_experiment`:
  "cross-year human-corpus FPR drift measurement plus synthetic-drift and cross-genre controls, per
  '跨年份人类语料的假阳性率漂移测量'."
- **RQ3** [HYPOTHESIS] (inferred, downstream of [MonitorAIScale, OpenReview:bX3J7ho18S]): "Does
  anchor temporal drift bias a mixture-based corpus-level prevalence estimator, i.e., does swapping
  an aged pre-2022 human reference into the estimator shift the estimated AI-fraction on a fixed
  target corpus?" `rq_source="inferred"`. `evaluates_mechanisms=["M2","M6"]`.
  `addresses_challenges=["C3"]`. `tests_contributions=["CO2","CO3"]`. `answered_by_experiment`:
  "hold target corpus fixed, vary the human reference year bucket in the mixture estimator, measure
  change in the estimated mixing coefficient."

**datasets** [HYPOTHESIS] `names`: `["arXiv abstracts (timestamped, 2007–2022, single-source long-span human anchor)", "CC-News / dated news archive", "Project Gutenberg (dated by first publication)", "Reddit/Pushshift comments (post-date stratified, pre-2022)", "matched post-2022 human comparison slices from the same sources", "RAID (Robust AI Detection benchmark, for estimator sanity-checking)", "M4 (multi-generator multi-domain multilingual detection benchmark)", "HC3 (Human ChatGPT Comparison Corpus, for AI-side reference)"]`. `source="inferred"`.
**baselines** [HYPOTHESIS] `names`: `["DetectGPT zero-shot curvature detector [DetectGPT, OpenReview:UiAyIILXRd]", "Learn-to-Distance rewrite detector [LearnToDistance, OpenReview:2ZUPeEM3FH]", "Disrupt-and-Recover black-box detector [DnR, OpenReview:FiMZSxo4DO]", "mixture-based corpus prevalence estimator [MonitorAIScale, OpenReview:bX3J7ho18S]"]`. `source="inferred"`.
**metrics** [HYPOTHESIS] `names`: `["false-positive rate (FPR) per publication-year bucket — fraction of certified-human documents flagged AI at a fixed threshold", "slope / regression coefficient of FPR vs. temporal distance", "change-point / breakpoint location (year)", "width of the derived FPR confidence bound at a stated confidence level", "bias of the estimated AI-fraction (mixing-coefficient shift) under reference-year swap"]`. `source="inferred"`.
**analysis_plan** [HYPOTHESIS]: per genre, ~8–12 year buckets × ~3,000 documents (≈24k–36k human
documents/genre); test the FPR-vs-year trend with a Mann-Kendall trend test and a mixed-effects
logistic regression (document flagged ~ temporal distance, random intercept per source), α=0.05
Bonferroni-corrected across detectors; RQ3 tested by paired comparison of estimated AI-fraction
across reference-year swaps (permutation test). Expected effect direction: **positive** FPR-vs-year
slope and **positive** mixing-coefficient bias as the anchor ages.

---

## N9 Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY, no real numbers, `evidence_strength="missing"`, `rq_answered=false` throughout.]**

- **rq_id="RQ1"**, `source="PLACEHOLDER"`, `result_type="quantitative"`, `evidence_strength="missing"`, `rq_answered=false`.
  `result_text` (hypothesized direction, falsifiable): "Existing corpus-level estimators are
  predicted to show a non-zero baseline false-positive rate even on strictly certified pre-2022
  human text — i.e., the pre-2022 anchor licenses a finite, non-trivial FPR bound, not a clean
  zero-error guarantee."
  **Falsification condition:** refuted if measured FPR on pre-2022 anchors is statistically
  indistinguishable from zero across all tested detectors and all sampled years — supporting a
  near-perfect zero-FPR guarantee instead.

- **rq_id="RQ2"**, `source="PLACEHOLDER"`, `result_type="quantitative"`, `evidence_strength="missing"`, `rq_answered=false`.
  `result_text` (hypothesized direction, falsifiable): "Within-source FPR on certified-human text is
  predicted to increase with temporal distance from the anchor year (detectors flag more human text
  as AI the further in time a sample sits from the ~2022 calibration point), and synthetic-drift
  injection on a fixed human sample reproduces a matching FPR rise, consistent with stylistic drift
  as a genuine confound."
  **Falsification condition:** refuted if within-source FPR is flat across years (no significant
  Mann-Kendall trend) and synthetic-drift injection leaves FPR unchanged — indicating drift is not a
  significant confound and the anchor generalizes across time.

- **rq_id="RQ3"**, `source="PLACEHOLDER"`, `result_type="quantitative"`, `evidence_strength="missing"`, `rq_answered=false`.
  `result_text` (hypothesized direction, falsifiable): "Swapping an older pre-2022 human reference
  into the mixture-based prevalence estimator, with the target corpus fixed, is predicted to shift
  the estimated AI-fraction upward (an aged anchor makes present-day human text look more 'AI-like'
  relative to the reference), so anchor drift induces a measurable positive bias in the corpus-level
  estimand."
  **Falsification condition:** refuted if the estimated AI-fraction is invariant (within CI) to the
  reference year bucket — indicating the prevalence estimator is robust to anchor age.

---

## N10 Threats / Self-Limitations

[HYPOTHESIS — anticipated limitations of this kind of study; no author statement exists yet, so
every item is a prediction, not an extracted acknowledgment.]

- **t1** `category="construct"`: "The 'certified-human' label relies on publication-year metadata as
  a proxy for authorship provenance, which may not capture true human-sole authorship (ghostwriting,
  later heavy editing, translation)." `mitigation`: "spot-check anchor purity on a ~1–2k-document
  human-validated subset (M5) and report residual mislabeling rate as an explicit uncertainty on
  the bound."
- **t2** `category="internal"`: "Publication year is confounded with genre, topic, and source
  composition in available corpora, so an apparent FPR-vs-year slope could be a genre/topic effect
  rather than temporal style drift." `mitigation`: "fix a single continuously-archived source per
  experiment, match per-year token budgets, and use M5 synthetic-drift injection on a fixed sample
  as a genre-controlled sanity check."
- **t3** `category="internal"`: "A residual confound between genuine stylistic drift and undetected
  AI-content leakage into supposedly pre-2022 corpora (mis-dated or later-revised documents) could
  inflate the apparent drift signal (C1/C2)." `mitigation`: "restrict to sources with hard
  archival timestamps predating late-2022 and report leakage sensitivity from the M5 stress-tests."
- **t4** `category="external"`: "Findings are likely specific to the tested detectors, languages,
  and genres (e.g., English arXiv/news) and may not generalize to other languages, genres, or
  detector architectures released after the study." `mitigation`: "run the scale-up stage across
  ≥2 languages and ≥3 genres and report the validity envelope's scope explicitly rather than as a
  universal claim."
- **t5** `category="conclusion"`: "Per-year sample sizes shrink for older slices (C4), widening
  confidence intervals and risking under-powered trend tests that either miss or overstate drift."
  `mitigation`: "report per-bucket n and CI widths, pre-register the Mann-Kendall + mixed-effects
  analysis and α=0.05 Bonferroni correction, and treat under-powered buckets as inconclusive rather
  than null."

**Status:** N/A pre-paper — these are HYPOTHESIS-tagged anticipated threats. If/when the real paper
is written, re-extract this node from its actual Limitations/Threats section.

---

## N11 Artifacts

**Status: NOT_FOUND.** [PLACEHOLDER] — nothing released because the paper does not exist yet.

- `artifacts`: `[]`
- `has_code`: `false`
- `has_data`: `false`
- `has_model`: `false`

**absence_comment:**
- `what_missing`: "No code, dataset, model, or demo artifact exists, since this is a
  reverse-constructed digest of an unwritten paper."
- `why_matters`: "A reader cannot yet assess reproducibility or reuse the year-stratified anchor
  corpus (M1) or the estimator battery (M2)."
- `implication`: "Treat N11 as fully prospective; if executed, the year-stratified corpus (M1) and
  the estimator battery + drift-curve code (M2/M3) would be the natural artifacts to release."

---

## N12 Contribution Type

- **value**: `empirical` [HYPOTHESIS]
- **rationale**: "The minimal experiment — cross-year false-positive-rate drift measurement on human
  corpora yielding boundary conditions for anchor validity — is a *measurement* study of how a
  widely-used methodological convention (the pre-2022 human anchor) behaves under temporal stress,
  and of how that drift propagates into a real corpus-level estimator's bias
  ([MonitorAIScale, OpenReview:bX3J7ho18S]). It does not introduce a new detector, headline a new
  dataset, or ship a system/tool: the year-stratified corpus is instrumental to the measurement, not
  the primary claimed contribution. What N9 would validate is an empirical claim about FPR-drift
  magnitude and where the anchor becomes unsafe — the defining signature of `empirical`, not
  `dataset`, `benchmark`, or `theoretical` (the derived bound in CO3 is an empirical envelope, not a
  proof-gated theorem)."
- **source**: `HYPOTHESIS`.

---

## Claims

1. **[HYPOTHESIS]** "Pre-2022 corpora, though commonly treated as a clean certified-human negative
   anchor for corpus-level AI-content estimators, license only a bounded — not a zero — error
   guarantee, and that bound has not previously been made explicit." `evidence`: `[{type: "argument",
   text: "constructed from the seed's core question and the absence of any corpus paper auditing the
   anchor's temporal validity, including [MonitorAIScale, OpenReview:bX3J7ho18S] which uses but never
   audits a human reference", source: "HYPOTHESIS", location: "seed README core question; N3"}]`.
2. **[HYPOTHESIS]** "Temporal drift in human writing style is a genuine, measurable confound on
   AI-detector false-positive rates, independent of any actual AI-generated content in the corpus."
   `evidence`: `[{type: "citation", text: "detector reliability is shown to collapse as reference and
   target distributions converge/shift ([MinKpp, OpenReview:ZGkfoufDaU]; [BenchContamFragility,
   OpenReview:bhR00j6Mku]; [MarkovCalib, OpenReview:Lzwkeg2o2z]); temporal distance is an unaudited
   instance of that shift", source: "HYPOTHESIS", location: "N3/N4"}]`.
3. **[PLACEHOLDER]** "The false-positive-rate drift, once measured, will define an explicit boundary
   condition (time window / genre / domain) beyond which the pre-2022 anchor should no longer be
   trusted at face value." `evidence`: `[{type: "experiment", text: "no data collected yet — the
   paper's core predicted finding, stated as a falsifiable direction in N9 (RQ1/RQ2)",
   source: "PLACEHOLDER", location: "N9"}]`.
4. **[HYPOTHESIS]** "Any downstream corpus-level prevalence estimate (parent topic B6) that relies on
   a pre-2022 human anchor without stating its temporal-validity bound carries an uncharacterized,
   directional bias in the reported AI-fraction." `evidence`: `[{type: "argument", text: "follows
   from RQ2 and RQ3's hypothesized directions applied to the mixture estimator of
   [MonitorAIScale, OpenReview:bX3J7ho18S]", source: "HYPOTHESIS", location: "N2/N8"}]`.

---

## Self-verification pass (adapted checklist)

- **ID consistency:** `N4.limitations[].affects_works` ⊆ `N3.works[].citation_key` ✓ (all four cite
  verbatim N3 keys: bX3J7ho18S; {UiAyIILXRd, 2ZUPeEM3FH, Lzwkeg2o2z, FiMZSxo4DO};
  {bhR00j6Mku, ZGkfoufDaU, YlpaaYxx4t}; 1FnCrZtBNQ). `N6.challenge_arguments[].challenge_id` ⊆
  {C1,C2,C3,C4} ✓. `N6.challenge_arguments[].mechanism_components` ⊆ {M1..M6} ✓.
  `N6.unaddressed_challenges` = {C2} ⊆ {C1..C4} ✓. `N8.RQ.addresses_challenges` ⊆ {C1..C4} ✓.
  `N8.RQ.tests_contributions` ⊆ {CO1..CO4} ✓. `N8.RQ.evaluates_mechanisms` ⊆ {M1..M6} ✓.
  `N9.results[].rq_id` ∈ {RQ1,RQ2,RQ3} = `N8` ids ✓.
- **N3 grounding:** 9/9 entries are real corpus papers with valid OpenReview ids + urls, tagged
  `[GROUNDED:corpus]`; 0 non-corpus entries. ✓
- **Absence comments:** all non-GIVEN, non-FOUND items (N0 authors/doi/etc., N3 status, N11) carry a
  real 3-part rationale; N10 mitigations are now concrete (not null). ✓
- **N12 rationale:** cites the specific mismatch (measurement study vs. dataset/benchmark/theoretical)
  and names the estimator whose bias is measured. ✓
- **Field-name discipline:** `objective`, `motivations`, `citation_key`, `limitation_text`,
  `limitation_type`, `text`, `evaluates_mechanisms`, `addresses_challenges`, `tests_contributions`
  used verbatim. ✓
- **Every node N0–N12 present** (+ Claims), none omitted. ✓
