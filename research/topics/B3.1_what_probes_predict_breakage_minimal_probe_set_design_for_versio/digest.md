# Digest: What Probes Predict Breakage? Minimal Probe-Set Design for Version-Drift Auditing

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet for this idea. This
> digest is constructed backward from a seed research topic (title, core question, minimal
> experiment) as if a paper answering it had already been written, for research-planning
> purposes only. Every field is tagged **[GIVEN]** (verbatim/near-verbatim from the seed
> README — ground truth, never contradicted), **[HYPOTHESIS]** (a reasoned prediction, not a
> fact), or **[PLACEHOLDER]** (genuinely unknowable until the work is done). N3/N4 additionally
> use **[GROUNDED:corpus]** for real OpenReview papers located in the local corpus
> (`topics/corpus/ideas.jsonl`); their *relevance* to this not-yet-written paper is my judgment
> call, not an author's own citation. Treat every number, name, and result here as unverified
> until the actual study is run.
>
> Seed source: `topics/B3.1_what_probes_predict_breakage_minimal_probe_set_design_for_versio/README.md`
> Topic code: **B3.1**, label **[证据]** ("evidence"-type gap), parent topic **B3. 跨版本行为漂移 /
> 纵向审计** (Cross-version behavioral drift / longitudinal auditing).

---

## N0 — Metadata

- `title`: "What Probes Predict Breakage? Minimal Probe-Set Design for Version-Drift Auditing" **[GIVEN]** — verbatim from seed README.
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — paper does not exist; no authors can be known.
- `abstract` **[HYPOTHESIS]** (drafted, not real — synthesized from the seed's core question + minimal experiment; explicitly a draft):
  > "LLM providers routinely ship new model versions that silently change behavior, breaking downstream applications built on prior versions. Comprehensive re-testing after every version bump is expensive, motivating a minimal set of cheap 'probes' that can be run once per version and used to predict whether real downstream tasks will break. We ask: which minimal probe family — capability, refusal-boundary, format-preference, calibration, or safety-behavior — is most predictive of downstream breakage? On a retrospective corpus of already-occurred version pairs (successive checkpoints of open-weight families plus dated API snapshots), we administer a fixed multi-family probe battery identically to both versions, compute per-family drift magnitudes, and correlate them against ground-truth downstream behavior change (the cross-version output diff on a shared input set). We rank the probe families by predictive power and, via subset ablation, identify the smallest family subset that retains most of that power, yielding a practical version-drift auditing protocol." *(drafted abstract, not extracted from any real document)*
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"SE"` **[HYPOTHESIS]** — the deliverable is an engineering-practice artifact (a version-drift audit protocol / minimal probe-set design) for LLM-backed systems, placing it at the SE/AI-systems boundary; `AI/ML` is a defensible alternative. `SE` chosen because the headline output is an auditing protocol, not a new model or training method.

**Status:** PARTIAL — `abstract` present only as a hypothesized draft (not a real extracted abstract); `authors` is a placeholder. **[PLACEHOLDER]**
`absence_comment`: `{"what_missing": "No real authors or camera-ready abstract exist because the paper has not been written.", "why_matters": "Downstream tools (paper-writer, reviewer agents) must not treat N0 as ground-truth bibliographic identity.", "implication": "Treat N0 as a planning placeholder; re-run extraction once/if the paper is actually written."}`

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**, built as a full predicate from the core question: "via retrospective analysis of real LLM version pairs, measure which minimal probe family — capability, refusal-boundary, format-preference, calibration, or safety-behavior — best predicts downstream task behavioral breakage, and derive a validated minimal probe-set design usable as a practical version-drift auditing protocol."
  - Self-check: (1) task KIND = predictive/measurement study + design recommendation; (2) DOMAIN = LLM version-drift auditing; (3) OUTCOME shape = a ranked probe-family predictive-power comparison + a recommended minimal probe subset + an audit protocol. All three land.
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. Pairs of already-occurred model versions (v_old → v_new) — dated API snapshots and/or successive open-weight checkpoints of one or more families.
  2. A probe item bank spanning five families (capability / refusal-boundary / format-preference / calibration / safety-behavior), administered identically to both versions.
  3. A shared set of real downstream-task inputs, run through both versions, to compute ground-truth behavior change.
- `outputs` **[HYPOTHESIS]**:
  1. Per-probe-family drift-magnitude scores for each version pair.
  2. A predictive-power ranking of probe families against downstream breakage.
  3. A recommended minimal probe subset (smallest set retaining most predictive power) packaged as an audit protocol.
- `constraints` **[GIVEN]** — stated in the seed's minimal experiment: ground truth = the cross-version output diff on the same input set ("真值 = 同一输入集的跨版本输出差分"); the retrospective design requires already-occurred version pairs ("在已发生的版本对上回溯").

**Status:** FOUND (as an inferred formulation; `source="inferred"` throughout — no paper text exists to extract). **[HYPOTHESIS]**

---

## N2 — Motivation

**[HYPOTHESIS]**, reconstructed from the seed's `parent_topic` ("B3. 跨版本行为漂移 / 纵向审计" — Cross-version behavioral drift / longitudinal auditing). No invented statistics.

- `motivation_text` 1: "Applications and evaluation pipelines built on a hosted or self-hosted LLM implicitly depend on the model's current behavior; when a new version ships, that behavior can shift without notice, silently breaking downstream integrations (prompt templates, output parsers, safety filters) that were tuned against the old version." **[HYPOTHESIS]** — `evidence: []`.
- `motivation_text` 2: "Exhaustively re-validating every downstream task against every new version is costly — benchmarks are re-run across checkpoints, variants, and competing systems — so practitioners need a small, cheap, diagnostic probe set rather than a full re-test suite; this cost-under-budget pressure is exactly what motivates benchmark-compression work `[EssenceBench, OpenReview:lZlZjSxdio]`." **[HYPOTHESIS]** — `evidence: []`.
- `motivation_text` 3: "It is not obvious a priori which behavioral axis (raw capability vs. refusal boundary vs. output format vs. calibration vs. safety behavior) carries the signal for downstream breakage, so a comparative study of probe families has direct practical payoff for anyone designing a minimal audit suite." **[HYPOTHESIS]** — `evidence: []`.

---

## N3 — Related Works

Grounded via the local OpenReview corpus (`topics/corpus/ideas.jsonl`). Queries run (semicolon keyword sets): (1) *model update; version drift; behavioral change; regression testing; model versioning*; (2) *benchmark subset; coreset; efficient evaluation; predict accuracy; benchmark compression*; (3) *refusal; calibration; safety behavior; over-refusal*; (4) *prompt sensitivity; evaluation robustness; format bias; brittleness*. Full motivation+method text was read for the top hits before summarizing. All eight entries below are **real corpus papers**; none is fabricated. No non-corpus entry is included (no canonical match confidently known).

| citation_key | approach_summary | source | location |
|---|---|---|---|
| `[EssenceBench, OpenReview:lZlZjSxdio]` | "Rethinking LLM Evaluation: Can We Evaluate LLMs with 200× Less Data?" — coarse-to-fine benchmark compression that selects a tiny subset of instances to jointly reconstruct full-benchmark scores AND preserve cross-model rankings, modeling both semantic (embedding) and *ranking* redundancy (per-instance model-performance vectors) plus a surrogate that maps subset accuracy to full accuracy. The canonical "minimal set of items that preserves the conclusion" method. url: https://openreview.net/forum?id=lZlZjSxdio | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: benchmark compression)", quote: "select a tiny subset ... reconstruct full-benchmark scores and preserve cross-model rankings"}` |
| `[BiasSimilarity-BSM, OpenReview:EveruzAsGI]` | "Bias Similarity Measurement: A Black-Box Audit of Fairness Across LLMs" — represents each model's behavior on *shared prompts* as a multi-view signature (scalar, distributional, behavioral, representational) and computes pairwise similarity, explicitly to answer relational questions such as "whether a tuned release actually departs from its base model" and whether observed differences arise from directional rebalancing vs. abstention. Directly a black-box cross-version behavioral-drift audit. url: https://openreview.net/forum?id=EveruzAsGI | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: black-box audit / departs from base model)", quote: "whether a tuned release actually departs from its base model"}` |
| `[RefusalIndex, OpenReview:9gJBhkLRat]` | "Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks" — defines a Refusal Index as the Spearman rank correlation between a model's refusal probability and its error probability, computed from observable outputs in a black-box setting and invariant to overall refusal rate. A precise, drift-comparable operationalization of a refusal-boundary probe. url: https://openreview.net/forum?id=9gJBhkLRat | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: refusal boundary)", quote: "rank correlation between a model's refusal probability and its error probability"}` |
| `[OffTopicEval, OpenReview:EcIyiJrajc]` | "OffTopicEval: When Large Language Models Enter the Wrong Chat, Almost Always!" — a benchmark for operational safety in policy-conditioned agents: convert each model into purpose-specific agents via system prompts, then measure whether it simultaneously accepts in-domain and refuses out-of-domain queries, stress-tested with adaptive/adversarial and multilingual OOD prompts. An accept/refuse safety-behavior probe with a scalar score. url: https://openreview.net/forum?id=EcIyiJrajc | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: safety behavior / operational scope)", quote: "accept in-domain queries and refuse out-of-domain queries when the boundary is defined by an explicit agent policy"}` |
| `[B-Calibration, OpenReview:0sCyk9Tr5J]` | "Trained on Tokens, Calibrated on Concepts: The Emergence of Semantic Calibration in LLMs" — proposes B-calibration, collapsing full generations into semantic equivalence classes and evaluating confidence calibration of the top class, giving a calibration notion native to free-form generation (rather than only single-token/MCQ regimes). Grounds a calibration-drift probe that survives open-ended outputs. url: https://openreview.net/forum?id=0sCyk9Tr5J | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: calibration)", quote: "collapsing full sequences into equivalence classes via a user-chosen function B"}` |
| `[TARE, OpenReview:YEBDvqsniH]` | "Beyond Magic Words: Sharpness-Aware Prompt Evolving for Robust LLMs with TARE" — argues that point-wise task accuracy for a single phrasing is the wrong target because semantically equivalent paraphrases induce large behavioral changes; defines a semantic neighborhood and measures worst-case loss (textual sharpness) over paraphrases. Grounds both the format-preference/prompt-sensitivity axis and the warning that a single scalar drift measure is fragile. url: https://openreview.net/forum?id=YEBDvqsniH | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: prompt sensitivity / brittleness)", quote: "semantically equivalent reformulations can induce large behavioral changes"}` |
| `[WeightDiff, OpenReview:6As4wfTB77]` | "Learning to Interpret Weight Differences in Language Models" — studies the parameter-space difference between a pretrained model and its finetuned variant (task vectors) to make model updates interpretable. Represents the *training/model-update side* of version change — motivating why an external API consumer, who cannot see weights, needs observable behavioral probes instead. url: https://openreview.net/forum?id=6As4wfTB77 | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: model update / weight difference)", quote: "the difference between a pretrained model and its finetuned variant forms a structured vector in weight space"}` |
| `[ProSafePrune, OpenReview:QkHKaPfRAB]` | "ProSafePrune: Projected Safety Pruning for Mitigating Over-Refusal in LLMs" — documents (via OR-Bench) that false refusals on pseudo-harmful prompts are systematic and widespread and that safety behavior is concentrated in specific layers. Grounds over-refusal as a measurable, drift-prone axis distinct from harmful-content refusal. url: https://openreview.net/forum?id=QkHKaPfRAB | **[GROUNDED:corpus]** | `{page: null, section_title: "N3 (corpus search: over-refusal)", quote: "false refusals are systematic and widespread, especially for pseudo-harmful prompts"}` |

### N3 — Missing classical (pre-LLM) threads — [UNVERIFIED — requires harvest]

The recent-papers-only corpus harvest (arXiv 2606–2607 + OpenReview) structurally missed two **classical literatures that are the direct pre-LLM analog of this paper's core move** ("smallest subset of cheap tests that retains fault-detection / breakage-prediction power"). A design reviewer will demand these; they must be conceded-and-differentiated, not ignored. No network access here — these are named threads to harvest, **not verified citations**:

- **[UNVERIFIED — requires harvest] Regression test selection / test-suite minimization / test-case prioritization (software engineering).** The problem "choose a minimal subset of tests that preserves fault-detection capability after a code change" is *exactly* this paper's "minimal probe subset that preserves breakage-prediction power after a version change," transposed from code diffs to weight/behavior diffs. Canonical threads to harvest: Yoo & Harrold's survey of regression testing minimization/selection/prioritization (ACM TOSEM ~2012); Rothermel & Harrold's framework for regression test selection (1990s); coverage-based suite minimization. **Delta to concede:** these operate on white-box code coverage with a deterministic pass/fail oracle; this paper has neither code access nor a deterministic oracle — the "fault" is a probabilistic behavioral drift and the "coverage" is over behavioral axes, not code paths. The minimality *criterion* (subset retaining detection power) is shared and must be credited; the setting (black-box, behavioral, no ground-truth fault localization) is the genuine gap.
- **[UNVERIFIED — requires harvest] Concept-drift / dataset-shift detection and monitoring (ML).** The "which cheap monitor best predicts downstream model degradation" question has a large classical literature. Threads to harvest: Gama et al., "A survey on concept drift adaptation" (ACM CSUR 2014); drift detectors (DDM, ADWIN); performance-estimation-under-shift. **Delta to concede:** classical concept-drift work monitors *one deployed model's input/output stream over time* for degradation against a held-out label stream; this paper compares *two discrete model versions* on a shared frozen input set and asks which *behavioral axis* (not which input-distribution statistic) forecasts breakage. Shared: the "cheap proxy predicts expensive degradation" framing; different: version-pair vs. streaming, axis-selection vs. distribution-shift detection.

Positioning consequence for `paper.md`: the novelty is **not** "no one ever built a minimal predictive test subset" (that would be false against test-suite minimization) — it is that no prior work does axis-resolved, black-box, behavioral-drift breakage prediction across LLM version pairs. State the concession explicitly.

**Status:** FOUND (eight real corpus works, each grounded in its own motivation/method text) + 2 UNVERIFIED classical threads flagged for harvest. **[GROUNDED:corpus] + [UNVERIFIED]**
`absence_comment`: `{"what_missing": "No single corpus paper administers a multi-family (capability + refusal + format + calibration + safety) probe battery compared retrospectively against real downstream-task breakage across model versions — the exact composite this seed proposes.", "why_matters": "The novelty is the composite comparison; the found works supply strong single-axis instruments (RefusalIndex, B-calibration, OffTopicEval) and the compression/audit machinery (EssenceBench, BSM), but not the head-to-head predictive comparison.", "implication": "N4's limitations are grounded in what each cited work demonstrably does NOT cover, not in a paper that attempted the same comparison and fell short."}`

---

## N4 — Prior Limitations

`grounding_check`: **true** — every limitation cites at least one `N3.works[].citation_key`, in the exact string form used in N3. All entries `source="inferred"` **[HYPOTHESIS]** (this project's inferred limitations of the found works relative to the seed's core question; no source paper makes these claims about itself).

| limitation_text | affects_works | limitation_type |
|---|---|---|
| Benchmark compression selects a minimal item subset to preserve a *score/ranking under one metric at one time*; it does not select probes to predict *cross-version downstream breakage*, does not span behavioral axes beyond task accuracy (refusal, format, calibration, safety), and optimizes for score fidelity rather than diagnostic predictive power for a separate downstream target. | `["[EssenceBench, OpenReview:lZlZjSxdio]"]` | generalizability |
| The black-box similarity audit compares whether a tuned release departs from its base *within one behavioral construct (fairness/bias)* and outputs a pairwise similarity, but it does not connect the measured departure to any downstream application's actual breakage, nor compare which behavioral axis best forecasts that breakage. | `["[BiasSimilarity-BSM, OpenReview:EveruzAsGI]"]` | generalizability |
| The Refusal Index gives a clean, rate-invariant refusal-boundary metric, but it is a single-family instrument evaluated at a single time point; it is not compared against capability/format/calibration/safety drift, nor regressed against a downstream-breakage ground truth across version pairs. | `["[RefusalIndex, OpenReview:9gJBhkLRat]"]` | scalability |
| OffTopicEval measures accept/refuse operational safety for a fixed model under fixed policies; it does not track how that safety behavior *drifts across versions* of the same model or ask whether such drift predicts downstream failure of a deployed integration. | `["[OffTopicEval, OpenReview:EcIyiJrajc]"]` | scalability |
| B-calibration formalizes semantic calibration at a point in time but does not quantify a version-to-version *calibration-drift magnitude* comparable to drifts on other probe families, nor tie calibration drift to downstream breakage. | `["[B-Calibration, OpenReview:0sCyk9Tr5J]"]` | precision |
| TARE demonstrates that point-wise, single-phrasing measurements are brittle to paraphrase — which threatens any single scalar drift score — but it targets prompt *optimization* robustness, not the construction of a stable multi-family drift measure or the prediction of downstream breakage. | `["[TARE, OpenReview:YEBDvqsniH]"]` | precision |
| Weight-difference interpretation explains model change from the parameter side (task vectors), requiring white-box access to both checkpoints; it offers no route for an external consumer, who sees only outputs, to detect which observable probe signals forecast breakage after an update ships. | `["[WeightDiff, OpenReview:6As4wfTB77]"]` | usability |
| Over-refusal benchmarking establishes that false refusals are systematic, but as a single-axis diagnostic at one release it does not measure over-refusal *drift* across versions nor weigh it against other axes as a breakage predictor. | `["[ProSafePrune, OpenReview:QkHKaPfRAB]"]` | recall |

**Status:** FOUND (each limitation grounded in what the cited corpus work demonstrably does not cover). **[HYPOTHESIS]**

---

## N5 — Challenges

`conflation_check`: **true** (each challenge is problem-inherent and distinct; none restates a specific prior tool's failure — see N4-vs-N5 test).

- **C1** — "A version pair can drift on multiple behavioral axes (capability, refusal boundary, format, calibration, safety) simultaneously; without ground truth it is inherently unclear which axis actually governs whether a given downstream integration breaks." **[HYPOTHESIS, tightly derived from the core question's five-way comparison]**
- **C2** — "Downstream 'breakage' is task-specific and heterogeneous: the same update can break a format-sensitive parser while leaving a calibration-sensitive integration untouched, so any per-family scalar drift score must aggregate over dissimilar downstream sensitivities without a canonical weighting." **[HYPOTHESIS]**
- **C3** — "Retrospective analysis requires already-occurred version pairs with a fixed, shared input set queryable on both versions, but providers do not guarantee stable historical access, deterministic decoding, or version pinning, and sampling noise can masquerade as drift — making a clean retrospective corpus inherently hard to assemble." **[HYPOTHESIS, grounded in the seed's explicit "回溯"/retrospective framing]**
- **C4** — "The five probe families are not statistically independent (e.g., a safety-behavior shift often co-occurs with a refusal-boundary shift), so attributing predictive power to one family in isolation, rather than to a correlated bundle, is an inherent identifiability problem." **[HYPOTHESIS]**
- **C5** — "A drift score and a breakage measure are both operationalization choices (which probe items? which output-diff metric?); a fragile instrument makes any observed correlation an artifact of instrument choice rather than a real signal — the point-wise-brittleness concern `[TARE, OpenReview:YEBDvqsniH]` raises for prompts applies to drift measurement itself." **[HYPOTHESIS]**

**Status:** FOUND (hypothesized problem-inherent challenges). **[HYPOTHESIS]**

---

## N6 — Methodology

**`overview`** **[HYPOTHESIS]** — extrapolated from the seed's minimal experiment, with a staged plan:
> "For a corpus of already-occurred version pairs, the method administers a fixed probe battery spanning five behavioral families — capability, refusal-boundary, format-preference, calibration, safety-behavior — identically to both versions, computing a per-family drift-magnitude score per pair (M1–M5). Separately it computes ground-truth downstream breakage as the cross-version output diff on a shared set of real downstream-task inputs (M6). It then regresses/correlates each family's drift against the downstream-breakage ground truth, ranks the families by predictive power, runs a subset ablation to find the smallest family subset retaining most power, and partials out shared variance between correlated families (M7). **Staged plan — Pilot** (the seed's minimal experiment): 3–5 open-weight version pairs with immutable checkpoints (e.g., Llama-2→Llama-3, Qwen1.5→2→2.5, Mistral v0.1→v0.2), a ~500-item probe bank, and a ~10-task downstream suite, establishing that per-family drift correlates with output-diff ground truth at all. **Scale-up:** ~15–25 version pairs adding dated API snapshots (e.g., gpt-3.5-turbo-0301/0613/1106, gpt-4-0314/0613, dated Claude snapshots), a ~1,500-item probe bank, and a ~20-task downstream suite, powering the family ranking and the minimal-subset ablation with bootstrap confidence intervals."

**`key_components`** **[HYPOTHESIS]**:
- **M1** — "Capability probes": fixed task-accuracy battery (e.g., MMLU / GSM8K / BBH items) run identically pre/post; drift = change in per-item correctness aggregated to a signed magnitude.
- **M2** — "Refusal-boundary probes": borderline requests near the accept/refuse threshold; drift operationalized in the style of the Refusal Index `[RefusalIndex, OpenReview:9gJBhkLRat]` (rate-invariant rank measure) plus raw refusal-rate delta on a fixed borderline set (e.g., XSTest/OR-Bench items).
- **M3** — "Format-preference probes": items testing output-structure adherence (JSON-schema validity, key ordering, markdown/enumeration conventions, IFEval-style constraints); drift = change in schema-validity and structural-match rates, measured across paraphrases to guard against phrasing artifacts `[TARE, OpenReview:YEBDvqsniH]`.
- **M4** — "Calibration probes": items with known correctness labels; drift = change in a semantic-calibration error `[B-Calibration, OpenReview:0sCyk9Tr5J]` (or ECE on MCQ items) between versions.
- **M5** — "Safety-behavior probes": harm-adjacent and out-of-scope prompts; drift = change in policy-conditioned accept/refuse rates `[OffTopicEval, OpenReview:EcIyiJrajc]` and over-refusal rate on pseudo-harmful prompts `[ProSafePrune, OpenReview:QkHKaPfRAB]`.
- **M6** — "Downstream ground-truth module": runs a shared real-downstream-task input set through both versions and computes the cross-version output diff (per-task functional-equivalence checks + a semantic-diff score), producing a per-pair, per-task breakage label — the seed's `真值`.
- **M7** — "Predictive-comparison & minimal-subset engine": regresses/correlates M1–M5 drift against M6 breakage, ranks families, ablates over family subsets to find the smallest retaining most predictive power (borrowing the subset-selection framing of `[EssenceBench, OpenReview:lZlZjSxdio]`), and partials out inter-family correlation via partial correlation / multiple regression to address identifiability.

**`challenge_arguments`** **[HYPOTHESIS]**:
- `{challenge_id: "C1", mechanism_components: ["M1","M2","M3","M4","M5","M6","M7"], argument_text: "Running all five families against the same version pairs and correlating each family's drift against the same downstream ground truth (M6 via M7) empirically adjudicates which axis governs breakage rather than assuming it a priori."}`
- `{challenge_id: "C2", mechanism_components: ["M6"], argument_text: "Aggregating the ground-truth diff over a diverse multi-task downstream suite (rather than one synthetic task) is intended to represent heterogeneous downstream sensitivities, reported per-task before aggregation so format-sensitive and calibration-sensitive tasks are not silently averaged away."}`
- `{challenge_id: "C3", mechanism_components: ["M6"], argument_text: "Restricting the pilot to open-weight families with immutable, redistributable checkpoints, and repeating each probe/downstream query under fixed decoding to estimate a sampling-noise floor, sidesteps unstable historical API access and separates genuine drift from decoding variance."}`
- `{challenge_id: "C4", mechanism_components: ["M7"], argument_text: "Partialling out shared variance between correlated families (partial correlation / multiple regression in M7) attributes predictive power to families net of their overlap rather than to a correlated bundle."}`
- `{challenge_id: "C5", mechanism_components: ["M3","M7"], argument_text: "Measuring each probe family under multiple paraphrases and reporting drift as a distribution rather than a single point value tests instrument stability, so a reported correlation reflects signal rather than a phrasing artifact."}`

**`unaddressed_challenges`**: `[]` — the pilot's small pair count (C3) and the paraphrase-robustness step (C5) are only *partially* addressed at pilot scale; flagged here that C3 and C5 are mitigated but not eliminated (statistical power for the ranking is limited until scale-up). **[HYPOTHESIS — per V-08, this rests on inferred N5/N6, at inferred-level confidence.]**

**`feasibility`** **[HYPOTHESIS]** (order-of-magnitude):
- **#runs / API calls:** probe bank (~1,500 items) + downstream suite (~20 tasks × ~200 inputs ≈ 4,000 inputs) ≈ 5,500 queries × 2 versions × ~20 version endpoints ≈ **~220k generations**; ×3 paraphrase/decoding repeats for the stability check ≈ **~660k**. Open-weight portion runs on 2–4 A100-class GPUs over days; dated-API portion is a **low-thousands USD** API-cost class.
- **Annotator effort:** downstream functional-equivalence labels and probe-bank validation ≈ **40–80 annotator-hours** (much automatable via schema validators + string/semantic diff; humans adjudicate ambiguous breakage).
- **Biggest feasibility risk:** deprecated/unpinned old API versions are no longer queryable, collapsing the retrospective corpus (C3). **Mitigation:** anchor the study on open-weight families whose historical checkpoints are immutably archived on HuggingFace, treating dated closed-API snapshots as a secondary, best-effort stratum rather than the backbone.

---

## N7 — Contributions

**[HYPOTHESIS]**, framed from the sketched method + expected findings:

- **CO1** — "A minimal probe-set methodology spanning five behavioral axes (capability, refusal-boundary, format-preference, calibration, safety-behavior), each with a concrete drift instrument, for auditing LLM version drift." `contribution_type: technical_artifact`, `is_testable: true`, `has_rq: true`.
- **CO2** — "An empirical ranking of which probe family's drift magnitude best predicts real downstream-task breakage across retrospective version pairs." `contribution_type: empirical_finding`, `is_testable: true`, `has_rq: true`.
- **CO3** — "A retrospective evaluation protocol (ground truth = cross-version output diff on a shared downstream input set) plus a released probe bank and version-pair corpus usable to benchmark future probe-set designs." `contribution_type: technical_artifact`, `is_testable: true`, `has_rq: true`.

**Status:** FOUND (as hypothesized). **[HYPOTHESIS]**

---

## N8 — Research Questions

- **RQ1** **[GIVEN]** — near-verbatim from the seed's core question: "Which minimal probe family — capability, refusal-boundary, format-preference, calibration, or safety-behavior — is most predictive of downstream breakage?" `rq_source: "explicit"`. `addresses_challenges: ["C1","C2","C4"]`. `tests_contributions: ["CO2"]`. `evaluates_mechanisms: ["M1","M2","M3","M4","M5","M6","M7"]`. `answered_by_experiment`: "Retrospective correlation study: per-family drift magnitude vs. downstream output-diff ground truth over ~15–25 already-occurred version pairs; families ranked by Spearman ρ and by standardized regression coefficient."
- **RQ_INF_1** **[HYPOTHESIS]**, inferred (`rq_source: "inferred"`) — the title's "Minimal Probe-Set *Design*" implies a design question beyond ranking: "What is the smallest subset of probe families that retains most of the full battery's predictive power for downstream breakage?" `addresses_challenges: ["C2","C4"]`. `tests_contributions: ["CO1","CO2"]`. `evaluates_mechanisms: ["M7"]`. `answered_by_experiment`: "Forward/backward subset ablation over the five families, comparing each subset's cross-validated predictive R²/AUC to the full battery."
- **RQ_INF_2** **[HYPOTHESIS]**, inferred (`rq_source: "inferred"`) — from C3/C5 and the feasibility risks: "Is the measured per-family drift signal robust to decoding noise and probe-item/paraphrase choice, i.e., does drift exceed the same-version sampling-noise floor and remain stable across paraphrase sets?" `addresses_challenges: ["C3","C5"]`. `tests_contributions: ["CO1","CO3"]`. `evaluates_mechanisms: ["M3","M6","M7"]`. `answered_by_experiment`: "Repeat each probe/downstream query under fixed and re-sampled decoding and across ≥3 paraphrase sets; compare cross-version drift against a within-version null distribution."

**`datasets`** **[HYPOTHESIS]**: `{names: ["Retrospective open-weight version-pair corpus (Llama-2→Llama-3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3)", "Dated closed-API snapshot pairs (gpt-3.5-turbo-0301/0613/1106, gpt-4-0314/0613; dated Claude snapshots)", "Capability probes: MMLU / GSM8K / BIG-Bench-Hard", "Refusal-boundary probes: XSTest, OR-Bench, SimpleQA-refusal", "Format probes: IFEval + a JSON-schema-compliance set", "Calibration probes: MMLU-with-confidence / a semantic-calibration set", "Safety probes: HarmBench, Sorry-Bench, OffTopicEval", "Downstream-task suite for ground-truth output diffs (~20 real tasks: extraction-to-JSON, classification, RAG-answer, tool-call argument filling, moderation)"]}`
**`baselines`** **[HYPOTHESIS]**: `{names: ["Single-probe-family predictors (each family alone)", "Full five-family battery predictor (upper bound)", "EssenceBench-style item-subset selector applied within capability probes (compression baseline) [EssenceBench, OpenReview:lZlZjSxdio]", "Raw output-diff magnitude on the probe bank itself, ignoring family structure", "Random / uniform drift-score baseline"]}`
**`metrics`** **[HYPOTHESIS]**: `{names: ["Spearman ρ and Pearson r between per-family drift magnitude and downstream breakage magnitude", "Cross-validated R² of the predictive regression", "AUC / precision-recall for flagging a version pair as breaking a specific downstream task", "ΔAUC (or ΔR²) of a family subset vs. the full five-family battery (for the minimality RQ)", "Partial correlation of each family net of the others"]}`

**Analysis plan** **[HYPOTHESIS]**: unit of analysis = (version-pair × downstream-task) cell; target n ≈ 20 pairs × 20 tasks ≈ 400 cells at scale-up (pilot ≈ 4 pairs × 10 tasks ≈ 40). Rank families by ρ with **bootstrap 95% CIs** (10k resamples) over version pairs; test whether the top family's ρ exceeds the next family's via a **paired bootstrap / permutation test** at **α = 0.05**; for RQ_INF_1, accept a subset as "minimal-sufficient" if its cross-validated AUC is within a pre-registered margin (e.g., 0.03) of the full battery. **Expected effect direction:** refusal-boundary and safety drift show larger standardized coefficients than capability drift (see N9), and a ≤2-family subset lands within the margin.

---

## N9 — Results

**CRITICAL: no numbers exist. Every entry is [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].** `evidence_strength: "missing"` and `rq_answered: false` for all; each carries an explicit falsification condition.

- **Result 1** — `rq_id: "RQ1"`. `result_text` (hypothesized direction, not observed): "Refusal-boundary and/or safety-behavior probe drift will show the largest standardized predictive coefficient for downstream-task breakage, exceeding capability-probe drift, because production incidents around version updates cluster on policy/refusal changes rather than raw capability regressions." `result_type: "quantitative"`. `evidence_strength: "missing"`. `rq_answered: false`. **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
  **Falsification:** refuted if capability-probe drift has the highest ρ / standardized coefficient (paired bootstrap, α=0.05) with downstream breakage among the five families.
- **Result 2** — `rq_id: "RQ_INF_1"`. `result_text` (hypothesized direction): "A subset of ~2 probe families will recover most (within the pre-registered ≤0.03 AUC margin) of the full five-family battery's predictive power, supporting a genuinely 'minimal' probe set." `result_type: "quantitative"`. `evidence_strength: "missing"`. `rq_answered: false`. **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
  **Falsification:** refuted if predictive AUC degrades roughly linearly as families are dropped and no subset comes within the margin — implying all five carry non-redundant signal and no minimal subset suffices.
- **Result 3** — `rq_id: "RQ_INF_2"`. `result_text` (hypothesized direction): "Per-family cross-version drift will exceed the within-version sampling-noise floor for at least the refusal/safety/format families and remain rank-stable across ≥3 paraphrase sets, establishing that the measured drift is signal rather than instrument artifact." `result_type: "quantitative"`. `evidence_strength: "missing"`. `rq_answered: false`. **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]**
  **Falsification:** refuted if cross-version drift falls within the within-version noise band, or if the family ranking reorders across paraphrase sets — indicating the correlation in Result 1 is an artifact of probe-item/phrasing choice (C5).

**Status:** NOT_FOUND (no experiment run). **[PLACEHOLDER]**
`absence_comment`: `{"what_missing": "No actual retrospective study, version pairs, probe administrations, or correlation numbers exist yet.", "why_matters": "Any quantitative claim here would be fabricated if stated as fact rather than as a falsifiable, direction-only prediction.", "implication": "Treat N9 as pre-registered hypotheses to be tested by the seed's minimal experiment, not as findings."}`

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS]** — anticipated limitations of this kind of study; no authors have written a Threats section.

- **t1** (`category: "construct"`) — "Output-diff-based 'downstream breakage' may not capture user- or business-relevant breakage: a large surface diff can be functionally harmless, while a tiny diff can break a brittle parser — so the ground-truth operationalization only partially matches real breakage." `mitigation`: "Pair the semantic-diff score with per-task functional-equivalence checks (schema validity, tool-call executability) so breakage is defined functionally, not by raw surface distance."
- **t2** (`category: "internal"`) — "Each probe family is instantiated via one item set; an alternative battery for the same family could change the drift magnitude and thus the ranking (instrument confound, C5)." `mitigation`: "Measure each family across ≥3 paraphrase/item variants and report drift as a distribution; require rank-stability (RQ_INF_2) before trusting the ranking."
- **t3** (`category: "conclusion"`) — "With only ~15–25 version pairs, the family ranking rests on a small sample; correlated families (C4) further inflate the risk of mis-attributing predictive power." `mitigation`: "Bootstrap CIs and paired permutation tests at α=0.05 for ranking claims; partial correlation / multiple regression to disentangle correlated families."
- **t4** (`category: "external"`) — "Findings may be specific to the sampled providers, families, and update cadences and may not transfer to other model families or future update policies." `mitigation`: "Span both open-weight and closed-API strata and multiple families; report per-family-of-model breakdowns rather than one pooled number."
- **t5** (`category: "reproducibility"`) — "Retrospective closed-API version pairs depend on providers keeping older snapshots queryable; deprecated endpoints make exact replication difficult over time." `mitigation`: "Anchor the backbone on immutably archived open-weight checkpoints; release the probe bank, downstream suite, and captured outputs so the corpus is reproducible even after endpoints deprecate."

**Status:** NOT_FOUND — no real authors have stated these; all are anticipated (mitigations are proposed design choices, not author-stated). **[HYPOTHESIS]**
`absence_comment`: `{"what_missing": "No actual Limitations/Threats-to-Validity section exists because no paper has been written.", "why_matters": "A reviewer should not mistake these for author-acknowledged limitations; they are this digest's anticipatory risk assessment.", "implication": "Re-derive N10 from the real paper's own Limitations section once written."}`

---

## N11 — Artifacts

**Status: NOT_FOUND.** **[PLACEHOLDER]** `artifacts: []`. `has_code: false`, `has_data: false`, `has_model: false`.
`absence_comment`: `{"what_missing": "No code, probe item bank, retrospective version-pair corpus, or predictive model has been released, because the paper and its study do not yet exist.", "why_matters": "A reader cannot currently reproduce, reuse, or verify the minimal probe-set design; this is a real evidentiary gap.", "implication": "Once the minimal experiment is run, re-populate with real artifact URLs (probe bank, retrospective corpus, analysis code) rather than leaving a placeholder."}`

---

## N12 — Contribution Type

`value`: **`empirical`** **[HYPOTHESIS]**

`rationale` **[HYPOTHESIS]**: "The headline validation (N9) is a retrospective correlational comparison of five existing probe-family drift measures against real downstream-task breakage across version pairs — a measurement study of an existing phenomenon (which behavioral axis governs LLM version breakage), analogous to the schema's 'We compared 10 LLMs on benchmark X → empirical'. The probe battery (M1–M5) and minimal-subset engine (M7) are instrumental to that finding, not the headline deliverable, so `empirical` fits better than `benchmark` or `tool`. Had the released probe bank + corpus (CO3) been positioned as the primary contribution, `benchmark` would be the call; here the study's finding leads."

---

## Claims

1. **[HYPOTHESIS]** "Refusal-boundary and/or safety-behavior probe drift will be more predictive of downstream-task breakage than raw capability-probe drift across retrospective version pairs." `evidence: [{type: "argument", text: "production incidents around version updates concentrate on refusal/policy changes rather than capability regressions", source: "HYPOTHESIS", location: {section_title: "N9 Results, Result 1"}}]`
2. **[HYPOTHESIS]** "A subset of ~2 of the five probe families will recover most of the full battery's predictive power (within a pre-registered margin), supporting a genuinely 'minimal' probe-set design." `evidence: [{type: "argument", text: "extends the benchmark-compression premise that a tiny subset can preserve the conclusion", source: "HYPOTHESIS", location: {section_title: "N9 Results, Result 2"}}]`
3. **[HYPOTHESIS]** "Measured cross-version drift must be shown to exceed the within-version sampling-noise floor and stay rank-stable across paraphrases, or any observed drift-vs-breakage correlation is an instrument artifact." `evidence: [{type: "argument", text: "point-wise single-phrasing measurement is brittle to paraphrase [TARE, OpenReview:YEBDvqsniH]", source: "HYPOTHESIS", location: {section_title: "N9 Results, Result 3"}}]`
4. **[HYPOTHESIS]** "The output-diff ground truth for 'downstream breakage' may conflate surface-level, functionally-irrelevant drift with true breakage, threatening the construct validity of the whole predictive comparison unless paired with functional-equivalence checks." `evidence: [{type: "argument", text: "same output diff can be functionally harmless or critical depending on downstream sensitivity", source: "HYPOTHESIS", location: {section_title: "N10 Threats, t1"}}]`
5. **[PLACEHOLDER]** "No quantitative numbers, real version pairs, or datasets currently back any claim in this digest — all are pre-registered predictions pending the actual minimal experiment." `evidence: []`

---

## Self-verification pass

- **EX-09 / V-04 (cross-node ID consistency):**
  - `N4.affects_works` every string ∈ `N3.citation_key` set {EssenceBench:lZlZjSxdio, BiasSimilarity-BSM:EveruzAsGI, RefusalIndex:9gJBhkLRat, OffTopicEval:EcIyiJrajc, B-Calibration:0sCyk9Tr5J, TARE:YEBDvqsniH, WeightDiff:6As4wfTB77, ProSafePrune:QkHKaPfRAB} — all 8 limitations resolve. ✓
  - `N6.challenge_arguments[].challenge_id` ∈ {C1..C5}. ✓ `mechanism_components` ∈ {M1..M7}. ✓
  - `N6.unaddressed_challenges` = [] (valid subset). ✓
  - `N8` RQs: `addresses_challenges` ⊆ {C1..C5}; `tests_contributions` ⊆ {CO1..CO3}; `evaluates_mechanisms` ⊆ {M1..M7}. ✓
  - `N9.results[].rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2} = N8 ids. ✓
- **V-02 (absence comments):** every non-FOUND node (N0, N9, N10, N11) carries a 3-part `absence_comment`. ✓
- **V-08 (confidence under inference):** N6 `unaddressed_challenges` note flagged as inferred-level. ✓
- **EX-11 (empty-node check):** N0–N12 + Claims all present. ✓
- **N3 grounding:** all 8 entries are real corpus papers with resolvable OpenReview ids/urls, tagged [GROUNDED:corpus]; no non-corpus entry included. ✓
