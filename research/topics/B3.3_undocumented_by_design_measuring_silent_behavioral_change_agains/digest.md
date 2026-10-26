# Digest: Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet for topic **B3.3**.
> This document projects a full N0–N12 digest as if a paper answering the seed's core question
> had been written, so the idea can be planned/reviewed like a real submission. Every field is
> tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README · **[HYPOTHESIS]** = reasoned
> elaboration/prediction, not fact · **[PLACEHOLDER]** = genuinely unknowable until the work is
> done (never invented) · **[GROUNDED:corpus]** = a real paper retrieved from the local
> OpenReview corpus (`topics/corpus/ideas.jsonl`), cited with its `OpenReview:paper_id`.
> Treat all [HYPOTHESIS]/[PLACEHOLDER] content as a plan, not a result.

**Seed provenance:** `topics/B3.3_undocumented_by_design_measuring_silent_behavioral_change_agains/README.md`
— code B3.3, label `[证据+矛盾]` (evidence+contradiction), parent topic "B3. 跨版本行为漂移 / 纵向审计"
(cross-version behavioral drift / longitudinal audit). [GIVEN]

---

## N0 Metadata

- **Title:** "Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs" [GIVEN — verbatim from seed]
- **Authors:** ["Anonymous"] [PLACEHOLDER — no paper/authors exist yet]
- **Abstract** [HYPOTHESIS — drafted here by synthesizing the seed's core question + minimal
  experiment into abstract prose; this is a planning draft, not a real abstract]:
  > "Vendors of deployed AI systems (e.g., LLM APIs) routinely ship version updates whose
  > behavioral consequences are only partially, if at all, described in public changelogs and
  > release notes. We ask: of the behavioral changes that can be measured empirically across
  > consecutive versions of a system, what proportion never appears in the vendor's own
  > changelog, and in which behavioral categories do these silent changes concentrate? We build
  > a pipeline that (i) runs a standardized behavioral probe suite against paired pre/post-version
  > snapshots of a target system, (ii) statistically scores which probes show a genuine
  > behavioral diff relative to same-version sampling noise, and (iii) aligns each detected diff
  > against the vendor's changelog text for that release window to classify it as documented or
  > silent. Because vendors have no structural incentive to self-report every behavioral
  > consequence of an update, we argue this kind of external, reproducible audit is necessary
  > infrastructure for AI accountability, not an optional nicety."
- **DOI:** null [PLACEHOLDER]
- **arXiv ID:** null [PLACEHOLDER]
- **num_pages:** null [PLACEHOLDER]
- **research_area:** "AI/ML" [HYPOTHESIS — the subject system is an LLM/AI service; the
  methodology borrows from software-evolution / mining-software-repositories practice
  (SE-adjacent), but the target phenomenon, audience, and likely venue center on AI system
  behavior and accountability, so AI/ML is the better single-value fit]

**Status:** PARTIAL. `absence_comment`: {"what_missing": "Real authors and a verbatim abstract
cannot exist because no paper has been written yet.", "why_matters": "Bibliographic identity is
what downstream tools (se-paper-reviewer, pengsida-paper-writer) key off of, and fabricating it
would misrepresent a planning artifact as a real citation.", "implication": "Treat N0 as a
naming/framing placeholder only; re-run this digest once an actual paper or preprint exists."}

---

## N1 Problem Formulation

- **Objective** [HYPOTHESIS — full predicate built from the seed's core question + minimal
  experiment]: "measure, via automated alignment of vendor changelog/release-note text against
  empirically measured behavioral differences across consecutive versions of a deployed AI
  system (e.g., an LLM API), what proportion of statistically-detected behavioral changes are
  undocumented, and which behavioral categories concentrate this silent-change rate — producing
  an accountability-oriented longitudinal audit report and a reusable audit pipeline."
  - Self-check: KIND=measurement/audit; DOMAIN=deployed LLM/AI-system APIs across versions;
    OUTCOME shape=a quantified silent-change rate + category taxonomy + audit report. All three
    land, so the objective is well-formed. [HYPOTHESIS]

- **Inputs** [HYPOTHESIS, inferred from the minimal experiment]:
  1. Paired system snapshots (version *t* and *t+1*) of a deployed AI system/API.
  2. The vendor's published changelog / release-note text covering the *t→t+1* transition.
  3. A standardized battery of behavioral probes/tasks executed identically against both snapshots.

- **Outputs** [HYPOTHESIS, inferred]:
  1. A per-behavioral-category "silent-change rate" (fraction of measured diffs with no
     corresponding changelog entry).
  2. A taxonomy of which behavior categories concentrate silent changes.
  3. An aligned changelog-to-diff mapping artifact usable as an audit trail.

- **Constraints** [GIVEN — the seed states this directly]: the analysis requires (a) a notion of
  "measurable behavioral difference" that is separable from output noise/nondeterminism, and
  (b) treating changelog text as the documentation-of-record to align empirically measured diffs
  against ("变更日志文本 vs 实测行为差分的对齐分析" — alignment analysis of changelog text vs.
  measured behavioral diff).

**Status:** FOUND (objective/inputs/outputs inferred but closely grounded; constraints given).
Source: inferred for objective/inputs/outputs, extracted (near-verbatim) for constraints.

---

## N2 Motivation

[HYPOTHESIS — reconstructed from the seed's parent-topic framing "B3. 跨版本行为漂移 / 纵向审计"
(cross-version behavioral drift / longitudinal audit); no statistics invented.]

- Deployed AI systems (LLM APIs in particular) are updated on a schedule and cadence controlled
  entirely by the vendor, and downstream integrators/auditors have no independent signal of
  whether behavior they rely on has changed except what the vendor chooses to publish.
  `evidence: []` [HYPOTHESIS]
- If silent (undocumented) behavioral changes are common, users/auditors cannot attribute
  downstream regressions, incidents, or safety-relevant shifts to a specific vendor update,
  which undermines any accountability process that assumes changelogs are a complete record.
  This is exactly the "regulation demands monitoring that current tooling cannot yet deliver"
  gap catalogued for AI governance. `evidence: []` [HYPOTHESIS, echoes [TAIG, OpenReview:Be2B6f0ps1]]
- The seed's own framing states the practical stakes directly: findings "directly serve
  accountability" because "vendors will not structurally do this themselves" ("结论直接服务问责，
  厂商结构性不会自己做") — i.e., the motivation is that this auditing function has no natural
  first-party owner and must be built and run by a third party. `evidence: []` [GIVEN, near-verbatim]

**Status:** PARTIAL — no real paper text exists to extract from; all motivation items are
reasoned reconstructions. `absence_comment`: {"what_missing": "There is no written
Introduction/Motivation section to quote.", "why_matters": "A reviewer needs to know these
motivation claims are a planning hypothesis, not evidence the (nonexistent) authors presented.",
"implication": "Use this section to judge whether the idea is worth writing up, not as citable
motivation text."}

---

## N3 Related Works

**Grounding method.** Entries tagged **[GROUNDED:corpus]** are real papers retrieved from the
local OpenReview corpus (`topics/corpus/ideas.jsonl`) via keyword search over five angles
(black-box API auditing / model-equality testing; continuous drift monitoring of LLM endpoints;
relational fairness audits of tuned-vs-base releases; technical AI-governance capability gaps;
longitudinal concept-drift benchmarks). `approach_summary` fields paraphrase each paper's actual
motivation/method text. One canonical non-corpus entry (Chen et al. 2023) is included and clearly
flagged, as it is the single most on-point published work and is directly cited by one corpus
paper. Each entry's `citation_key` is the exact string N4 references.

- **[LogProbTracking, OpenReview:hFxivbAgVP]** — "Log Probability Tracking of LLM APIs."
  approach_summary: Frames the practical problem as *continuous detection of whether an
  endpoint's response distribution has changed*, not one-off identification. Repeatedly queries
  the API with a fixed minimal prompt, requests only the top-k log-probabilities of the first
  generated token, and applies a nonparametric two-sample test to detect shifts in their
  aggregate distribution — a cheap black-box change-detector for deployed LLM APIs.
  paper_url: https://openreview.net/forum?id=hFxivbAgVP [GROUNDED:corpus]
- **[RankUniformity, OpenReview:PSIe9mmF7a]** — "Auditing Black-Box LLM APIs with a Rank-Based
  Uniformity Test." approach_summary: Casts API auditing as model-equality testing: for each
  natural prompt, draw one target completion and many reference completions, score them under a
  trusted local reference model, and test whether the target's percentile ranks are uniform.
  Non-uniformity flags that the provider silently substituted a quantized/fine-tuned/different
  model. paper_url: https://openreview.net/forum?id=PSIe9mmF7a [GROUNDED:corpus]
- **[BiasSimilarity, OpenReview:EveruzAsGI]** — "Bias Similarity Measurement: A Black-Box Audit
  of Fairness Across LLMs." approach_summary: Argues that per-model scalar bias scores cannot
  answer *relational* questions such as "does a tuned release actually depart from its base
  model?"; represents each model's bias behavior as a multi-view signature over shared prompts
  (BBQ, UNQOVER) and computes pairwise similarity to detect inheritance, drift, and cross-family
  clustering. paper_url: https://openreview.net/forum?id=EveruzAsGI [GROUNDED:corpus]
- **[TAIG, OpenReview:Be2B6f0ps1]** — "Open Problems in Technical AI Governance" (Reuel et al.).
  approach_summary: Decomposes EU/US/China governance mandates (registration, evaluation,
  auditing, *ongoing monitoring*) into concrete technical requirements and maps each to the
  state of AI/ML tooling, exposing where methods to satisfy accountability/monitoring mandates
  are missing, unreliable, or immature. paper_url: https://openreview.net/forum?id=Be2B6f0ps1
  [GROUNDED:corpus]
- **[SafeHarbor, OpenReview:dLojMSgSFW]** — "Position: A Safe Harbor for AI Evaluation and Red
  Teaming." approach_summary: Argues that independent third-party evaluation is a structural
  prerequisite for accountability, yet Terms-of-Service prohibitions and unilateral enforcement
  make it hostile; proposes paired legal + technical safe harbors tied to researcher conduct.
  paper_url: https://openreview.net/forum?id=dLojMSgSFW [GROUNDED:corpus]
- **[RobustAudit, OpenReview:AiaVCVDuxF]** — "Robust ML Auditing using Prior Knowledge."
  approach_summary: Shows black-box audits are vulnerable to platforms that serve a compliant
  *audit-facing* model distinct from the *user-facing* one; proposes leveraging the auditor's
  private labeled prior (a risk-bounded "expectable set") so that fairness-preserving
  manipulation becomes statistically detectable. paper_url:
  https://openreview.net/forum?id=AiaVCVDuxF [GROUNDED:corpus]
- **[FairBetting, OpenReview:EEVpt3dJQj]** — "Auditing Fairness by Betting." approach_summary:
  Reframes fairness auditing as evidence accumulation in a betting game whose wealth process is a
  martingale under the null, giving *anytime-valid* sequential tests that remain correct under
  continuous monitoring, optional stopping, and policy/distribution drift — the statistical
  machinery for repeated longitudinal audits. paper_url:
  https://openreview.net/forum?id=EEVpt3dJQj [GROUNDED:corpus]
- **[LAMDA, OpenReview:1FnCrZtBNQ]** — "LAMDA: A Longitudinal Android Malware Benchmark for
  Concept Drift Analysis." approach_summary: Constructs a decade-spanning (2013–2025, >1M apps)
  dataset with a consistent feature representation and structured temporal-drift evaluation
  protocol, exemplifying rigorous longitudinal measurement of behavioral change under proper
  temporal splits (avoiding the inflation that improper temporal evaluation causes). paper_url:
  https://openreview.net/forum?id=1FnCrZtBNQ [GROUNDED:corpus]
- **[Chen, Zaharia & Zou, 2023]** — "How Is ChatGPT's Behavior Changing over Time?" (arXiv:2307.09009).
  approach_summary: The canonical direct precedent — evaluates GPT-3.5/GPT-4 on a fixed task
  battery (math, sensitive-question refusal, code generation, formatting) at two dated snapshots
  and shows substantial behavioral drift between them. **[NON-CORPUS — canonical, cited as
  @chen2023chatgptbehavior by LogProbTracking; included because it is the closest published
  analog and confidently known to exist, but it was not retrieved from the local corpus.]**

**Status:** FOUND (as a grounded hypothesis set). `absence_comment`: {"what_missing": "No paper
in the corpus studies 'silent/undocumented LLM behavioral change measured against vendor
changelogs' as its primary research question; the retrieved works cover the component
capabilities (change detection, model-equality testing, relational audits, governance gaps,
longitudinal benchmarking) but none aligns measured diffs to the vendor's own disclosure text.",
"why_matters": "This is precisely the open niche the seed targets; the related work establishes
that every ingredient exists but the documented-vs-silent alignment does not.", "implication":
"Before drafting a real paper, add a targeted arXiv/ACL search for changelog-fidelity and
API-transparency studies to confirm the niche remains open."}

---

## N4 Prior Limitations

**Grounding rule applied:** every limitation cites an N3 `citation_key` verbatim.
`grounding_check: true` [HYPOTHESIS — computed against the N3 list; none are ungrounded].

- **[LogProbTracking, OpenReview:hFxivbAgVP]**: Produces a bare *change signal* — it detects
  THAT an endpoint's distribution shifted, but never attributes the shift to a behavior category
  nor aligns it against the vendor's changelog text, so it cannot say whether a detected change
  was documented or silent. `affects_works: ["[LogProbTracking, OpenReview:hFxivbAgVP]"]`
  [HYPOTHESIS] `limitation_type: scope`
- **[RankUniformity, OpenReview:PSIe9mmF7a]**: Answers a binary "is the served model the same as
  a trusted reference?" and requires a fully-accessible local reference distribution; it does not
  operate over vendor-published documentation, does not categorize *what kind* of behavior
  changed, and presupposes a reference the changelog-audit setting lacks.
  `affects_works: ["[RankUniformity, OpenReview:PSIe9mmF7a]"]` [HYPOTHESIS] `limitation_type: generalizability`
- **[BiasSimilarity, OpenReview:EveruzAsGI]**: Measures whether a tuned release departs from its
  base model, but confined to the fairness/stereotype construct (BBQ/UNQOVER) and to model-pair
  similarity; it neither spans general behavior categories (refusal, formatting, reasoning,
  latency) nor cross-references any vendor disclosure to compute a documented-vs-silent rate.
  `affects_works: ["[BiasSimilarity, OpenReview:EveruzAsGI]"]` [HYPOTHESIS] `limitation_type: generalizability`
- **[TAIG, OpenReview:Be2B6f0ps1]**: Identifies and catalogs the monitoring/auditing capability
  gap at the level of a governance survey; it names the missing tooling but does not itself build
  or run an empirical measurement of documentation fidelity for any deployed system.
  `affects_works: ["[TAIG, OpenReview:Be2B6f0ps1]"]` [HYPOTHESIS] `limitation_type: other`
- **[SafeHarbor, OpenReview:dLojMSgSFW]**: A position/policy proposal establishing the *legal and
  technical conditions* for independent evaluation; it supplies no measurement instrument and no
  empirical silent-change rate, so it motivates the audit without operationalizing it.
  `affects_works: ["[SafeHarbor, OpenReview:dLojMSgSFW]"]` [HYPOTHESIS] `limitation_type: other`
- **[RobustAudit, OpenReview:AiaVCVDuxF]**: Targets manipulation-robustness of a single-time
  *fairness* audit and assumes the auditor holds a labeled ground-truth prior; the changelog
  setting has no such labeled ground truth of "all actual changes," and the concern is
  longitudinal documentation fidelity rather than a one-shot fairness metric.
  `affects_works: ["[RobustAudit, OpenReview:AiaVCVDuxF]"]` [HYPOTHESIS] `limitation_type: scope`
- **[FairBetting, OpenReview:EEVpt3dJQj]**: Provides anytime-valid sequential testing but only
  for a group-fairness two-sample null; it offers no mechanism to parse prose changelogs or to
  build a behavior-category taxonomy of undocumented change — it is a statistical tool the audit
  can reuse, not an alignment method. `affects_works: ["[FairBetting, OpenReview:EEVpt3dJQj]"]`
  [HYPOTHESIS] `limitation_type: scope`
- **[LAMDA, OpenReview:1FnCrZtBNQ]**: A longitudinal drift benchmark for a supervised classifier's
  *own* accuracy degradation over time; it measures drift in a first-party model, not the gap
  between a black-box vendor's behavior and that vendor's published documentation.
  `affects_works: ["[LAMDA, OpenReview:1FnCrZtBNQ]"]` [HYPOTHESIS] `limitation_type: generalizability`
- **[Chen, Zaharia & Zou, 2023]**: Demonstrates that ChatGPT behavior drifts across two dated
  snapshots on a handful of tasks, but does not systematically cross-reference findings against
  OpenAI's changelog to compute a documented-vs-silent rate, and its narrow task battery gives
  low coverage of behavior categories. `affects_works: ["[Chen, Zaharia & Zou, 2023]"]`
  [HYPOTHESIS] `limitation_type: precision`

**Status:** FOUND (as a hypothesis set — every item traces to a real N3 work). Source: inferred
throughout (no real paper text to extract limitations from).

---

## N5 Challenges

[HYPOTHESIS, but tightly derived from the core question itself — these are about the PROBLEM,
not about what the N3/N4 prior tools fail to do (N4-vs-N5 test applied).] `conflation_check:
true` [HYPOTHESIS — each challenge below is distinct].

- **C1**: Distinguishing a genuine behavioral change from ordinary LLM output stochasticity
  (sampling temperature, prompt sensitivity, non-determinism, load-dependent routing) requires a
  statistically defensible notion of "diff," since two samples from the *same* version already
  differ; the null of "no change" must be estimated from same-version resampling. [HYPOTHESIS]
- **C2**: Vendor changelogs are unstructured natural-language prose at variable granularity
  ("improved reasoning", "safety updates"), not a structured diff; mapping a vague changelog
  sentence to a specific measured behavioral category is an open-ended, many-to-many semantic
  entailment problem, not a lookup. [HYPOTHESIS]
- **C3**: There is no independent ground truth for "the complete set of actual changes" in a
  release — the vendor never reveals it — so any measured silent-change rate is a *lower bound*
  conditioned on probe-suite coverage, not the true rate; the estimand itself is only partially
  identified. [HYPOTHESIS]
- **C4**: For API-served models, version boundaries are not clean discrete events (rolling
  deploys, A/B routing, silent backend/quantization swaps, undated changes), so pairing "version
  *t*" against "*t+1*" samples and attributing a diff to a specific release window is itself an
  inference under uncertainty, not a given. [HYPOTHESIS]

**Status:** FOUND (as hypothesized challenges). Source: inferred.

---

## N6 Methodology

[HYPOTHESIS — extrapolated from the seed's one-sentence minimal experiment: "变更日志文本 vs 实测
行为差分的对齐分析" (alignment analysis of changelog text vs. measured behavioral diff), with
operationalization borrowed from the N3 corpus works.]

**Overview:** The method runs a fixed, category-stratified battery of behavioral probes against
paired pre/post-update snapshots of a target AI API; estimates a per-probe null distribution from
same-version resampling and flags probes whose cross-boundary shift exceeds that noise floor by a
significance threshold; parses the vendor's changelog text for the corresponding release window
into discrete claims; semantically aligns each detected shift to changelog claims (or their
absence) via entailment scoring with human adjudication on a labeled subset; and aggregates the
labels into a per-category silent-change rate and a ranked taxonomy of where silence concentrates.

**Staged plan** [HYPOTHESIS]:
- **Stage 0 — Pilot (= the seed's minimal experiment):** on ONE vendor and ONE well-dated version
  transition of a single LLM API, run a small probe suite (~200 probes across 5–6 categories),
  compute behavioral diffs vs. same-version noise, and manually align each detected diff to that
  release's changelog. Deliverable: a first documented-vs-silent count and a working pipeline.
- **Stage 1 — Scale-up:** extend to 3 vendors (e.g., OpenAI, Anthropic, Google) × multiple
  version transitions each × a ~1–2k-probe suite, with automatic changelog alignment validated
  against human labels, yielding stable per-category silent-change rates with confidence intervals
  and cross-vendor comparison.

**Key components:**
- **M1 — Behavioral probe suite**: a category-stratified battery of standardized tasks —
  factual QA, refusal/safety behavior, instruction-following/formatting, reasoning/math,
  tool/function-calling, and latency/cost — each probe a fixed (prompt, decoding-config) pair
  run identically against both snapshots. Categories are the unit of the final taxonomy. [HYPOTHESIS]
- **M2 — Version-snapshot capture pipeline**: timestamped polling of the vendor API plus a
  lightweight distributional fingerprint (first-token top-k logprob profile, in the style of
  [LogProbTracking, OpenReview:hFxivbAgVP]) to infer likely version boundaries and pin each probe
  run to a release window aligned to the vendor's changelog feed. [HYPOTHESIS]
- **M3 — Behavioral diff scoring**: per-probe two-sample comparison — draw N repeated samples per
  snapshot, estimate the same-version null by within-version resampling, and flag a genuine diff
  when a distribution-distance statistic (e.g., permutation/bootstrap two-sample test, or the
  martingale sequential test of [FairBetting, OpenReview:EEVpt3dJQj] for streaming monitoring)
  exceeds threshold after multiple-comparison correction. [HYPOTHESIS]
- **M4 — Changelog-to-behavior alignment**: parse changelog/release-note text into discrete
  candidate claims, then semantic-entailment match each detected behavioral diff against the
  claim set to label it *documented* or *silent*; calibrate the automatic matcher against a
  human-labeled subset (precision/recall reported). [HYPOTHESIS]
- **M5 — Silent-rate aggregation & taxonomy**: aggregate per-probe documented/silent labels into
  category-level silent-change rates with bootstrap confidence intervals, and rank categories to
  produce the taxonomy of where silence concentrates. [HYPOTHESIS]

**Challenge arguments:**
- `challenge_id: C1` ← `mechanism_components: [M1, M3]`: same-version resampling plus
  significance-thresholded two-sample testing in M3, applied to the fixed M1 probe suite, is
  argued to separate genuine behavioral change from ordinary output stochasticity. [HYPOTHESIS]
- `challenge_id: C2` ← `mechanism_components: [M4]`: semantic-entailment (not string) matching in
  M4, calibrated on human labels, is argued to handle the unstructured, variable-granularity
  prose of vendor changelogs. [HYPOTHESIS]
- `challenge_id: C4` ← `mechanism_components: [M2]`: timestamped polling plus logprob-profile
  fingerprinting in M2 is argued to approximate clean version boundaries for rolling-deploy
  APIs, pinning diffs to release windows — though only approximately. [HYPOTHESIS]

**Unaddressed challenges:** `["C3"]` — no component resolves the lack of an independent ground
truth for "all actual changes"; the method reports a lower-bound silent-change rate conditioned
on probe-suite coverage. [HYPOTHESIS; flagged per V-08 since this whole node is inferred.]

**Feasibility subsection** [HYPOTHESIS — order-of-magnitude planning estimates]:
- **Pilot (Stage 0):** ~200 probes × 2 snapshots × ~50 samples/probe ≈ 20k API calls; at
  short prompts/completions this is a **low-hundreds-of-USD** API-cost class. Human alignment of
  ~200 detected-diff/changelog pairs ≈ **10–20 annotator-hours**. No GPU training needed;
  reference-model logprob scoring runs on a single commodity GPU or is skipped for API-only probes.
- **Scale-up (Stage 1):** ~3 vendors × ~4 transitions × ~1.5k probes × ~50 samples ≈ 0.9M calls,
  a **low-thousands-of-USD** API-cost class; alignment-label adjudication ≈ **80–150 annotator-hours**
  (two annotators + adjudication for inter-rater reliability on a stratified subset).
- **Biggest feasibility risk:** version boundaries are undated / rolling (C4), so pre/post pairing
  is unreliable and diffs may be misattributed to the wrong release. **Mitigation:** continuous
  daily M2 fingerprint logging *before* a suspected update so boundaries are detected from the
  data rather than assumed from announcement dates, and restrict headline results to transitions
  with a clean fingerprint discontinuity, reporting undated ones separately.

---

## N7 Contributions

[HYPOTHESIS — what such a paper would plausibly claim, framed from the method + expected findings.]

- **CO1** [`empirical_finding`, is_testable=true, has_rq=true]: An empirical measurement of the
  proportion of statistically-detected behavioral changes across versions of a deployed AI system
  that are absent from the vendor's published changelog. [HYPOTHESIS]
- **CO2** [`tool`, is_testable=true, has_rq=true]: A reusable probe-suite + changelog-alignment
  pipeline (M1–M5) for auditing documented-vs-silent behavioral change, applicable to any
  versioned AI API, with reported alignment precision/recall against human labels. [HYPOTHESIS]
- **CO3** [`empirical_finding`, is_testable=true, has_rq=true]: A taxonomy of behavioral
  categories where silent changes concentrate (vs. categories vendors reliably document).
  [HYPOTHESIS]

**Status:** FOUND (as hypothesized contributions). Source: inferred.

---

## N8 Research Questions

- **RQ1** [GIVEN — near-verbatim restatement of the seed's core question]: "Of the behavioral
  changes that can be measured empirically across system versions, what proportion do not appear
  in the vendor's changelog?" `rq_source: explicit` `evaluates_mechanisms: [M3, M4]`
  `addresses_challenges: [C1, C2]` `tests_contributions: [CO1]` `answered_by_experiment:
  "changelog-vs-behavioral-diff alignment over paired snapshots (the seed's minimal experiment,
  scaled in Stage 1)"`
- **RQ2** [GIVEN — the seed's second clause, "静默变更集中在哪些行为类别"]: "In which behavioral
  categories do silent (undocumented) changes concentrate?" `rq_source: explicit`
  `evaluates_mechanisms: [M1, M5]` `addresses_challenges: [C2]` `tests_contributions: [CO3]`
  `answered_by_experiment: "per-category aggregation of the alignment labels (M5) with bootstrap CIs"`
- **RQ3** [HYPOTHESIS — inferred: validates the pipeline artifact CO2]: "How accurately does the
  automatic changelog-to-behavior alignment (M4) reproduce human documented-vs-silent labels, and
  does the diff-detector (M3) control false positives against same-version noise?" `rq_source:
  inferred` `evaluates_mechanisms: [M3, M4]` `addresses_challenges: [C1, C2]` `tests_contributions:
  [CO2]` `answered_by_experiment: "precision/recall of M4 vs. a human-labeled alignment subset;
  empirical false-positive rate of M3 on same-version (null) probe pairs"`

**Datasets / probe sources** [HYPOTHESIS — real named benchmarks that genuinely fit as probe
material, plus the changelog corpus]: `names: ["MMLU (factual/knowledge QA)", "GSM8K
(reasoning/math)", "TruthfulQA (factual-accuracy/hallucination)", "XSTest (refusal/over-refusal
safety behavior)", "AdvBench / HarmBench prompts (safety/refusal)", "IFEval (instruction-following
& formatting compliance)", "ToxiGen (toxicity/safety)", "BFCL (tool/function-calling behavior)",
"self-scraped vendor changelog / release-note corpus (OpenAI, Anthropic, Google API release
notes)"]`
- Rationale: these are established, category-diverse behavioral benchmarks; each maps cleanly to
  one M1 category, so per-category silent-change rates are interpretable. The changelog corpus is
  the documentation-of-record for M4. [HYPOTHESIS]

**Baselines** [HYPOTHESIS — drawn from N3 where possible]: `names: ["[LogProbTracking,
OpenReview:hFxivbAgVP] as a change-detection-only baseline (flags that something changed, cannot
label documented/silent)", "[RankUniformity, OpenReview:PSIe9mmF7a] as a substitution-detection
baseline", "naive keyword/string-match changelog alignment (weak lower baseline for M4)",
"assume-everything-undocumented baseline (trivial upper bound on silent rate)", "human-annotator
alignment (reference upper bound, not a competing method)"]`

**Metrics** [HYPOTHESIS]: `names: ["silent-change rate (% of detected diffs with no matching
changelog claim)", "per-category silent-change breakdown with bootstrap 95% CIs", "precision /
recall / F1 of automatic M4 alignment vs. human labels", "M3 false-positive rate on same-version
null pairs", "effect size of detected behavioral diffs (Cliff's delta or standardized mean diff)"]`

**Analysis plan** [HYPOTHESIS]: per behavioral probe, draw N≈50 samples per snapshot; test each
diff with a permutation/bootstrap two-sample test at α=0.05 with Holm–Bonferroni correction
across probes within a transition; require detected diffs to also exceed a minimum effect-size
floor (|Cliff's delta| ≥ 0.33) to be counted, guarding against trivially-significant-but-tiny
shifts. Silent-change rate reported per category with bootstrap CIs; cross-category concentration
tested with a chi-square / proportion test. Expected effect direction: silent-change rate > 50%
overall (RQ1), and non-uniform across categories with safety/refusal, formatting, and latency/cost
higher than factual accuracy (RQ2); M4 F1 vs. humans expected ≥ 0.7 and M3 null false-positive
rate ≤ α (RQ3).

---

## N9 Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY. No experiment has been run; nothing here is a
real number. Every item states its falsification condition explicitly.]**

- `rq_id: RQ1` — **Predicted direction:** a substantial majority (predicted > 50%) of
  statistically-detected behavioral changes across version boundaries will have no matching entry
  in the vendor's changelog (undocumented-by-design is the expected default). `result_type:
  quantitative` `evidence_strength: missing` `rq_answered: false`
  **Refuted if:** the measured silent-change rate is low (most statistically-detected diffs DO
  correspond to an explicit changelog claim), in which case the central premise does not hold for
  the systems tested. [PLACEHOLDER]

- `rq_id: RQ2` — **Predicted direction:** silent changes concentrate in safety/refusal behavior,
  formatting/instruction-following, and latency/cost, while core factual-accuracy changes are
  comparatively more likely to be documented (accuracy regressions are more reputationally
  salient). `result_type: quantitative` `evidence_strength: missing` `rq_answered: false`
  **Refuted if:** silent changes are distributed roughly uniformly across categories (no
  significant concentration), or concentrate opposite to the prediction (e.g., factual accuracy
  is the most silently altered category). [PLACEHOLDER]

- `rq_id: RQ3` — **Predicted direction:** automatic M4 alignment reproduces human
  documented-vs-silent labels at F1 ≥ 0.7, and M3's false-positive rate on same-version null
  probe pairs stays at or below the nominal α, so the headline silent-rate is not an artifact of
  the detector. `result_type: quantitative` `evidence_strength: missing` `rq_answered: false`
  **Refuted if:** M4 F1 is near chance (the prose→behavior matching is unreliable) or M3 flags a
  material fraction of same-version pairs as changed (the pipeline manufactures spurious diffs),
  either of which would invalidate CO1/CO2. [PLACEHOLDER]

---

## N10 Threats / Self-Limitations

[HYPOTHESIS — forward-looking risk list; no authors exist yet to have "acknowledged" these.
Each carries a concrete mitigation.]

- **t1** [`construct`]: "Behavioral change," operationalized as a statistical distributional diff
  over a fixed probe suite, may not match what a "meaningful" or "accountability-relevant" change
  means to end users or regulators — a significant tiny shift is not necessarily consequential.
  `mitigation: "require a minimum effect-size floor (|Cliff's delta| ≥ 0.33) in addition to
  significance, and report category-level rather than raw per-probe rates."` [HYPOTHESIS]
- **t2** [`internal`]: The probe suite (M1) is a finite sample of possible behaviors; its
  coverage choices could systematically under- or over-estimate the silent-change rate, and the
  changelog matcher (M4) could confound the alignment. `mitigation: "pre-register the probe
  categories and their weights, run an ablation over probe subsets to test rate stability, and
  calibrate M4 on a held-out human-labeled set with reported precision/recall."` [HYPOTHESIS]
- **t3** [`external`]: Findings from one or a few vendors/model families may not generalize to
  vendors with different documentation cultures or release cadences. `mitigation: "span ≥3
  vendors in Stage 1 and report per-vendor rates separately rather than a single pooled number."`
  [HYPOTHESIS]
- **t4** [`conclusion`]: The silent-change rate is only partially identified (C3): with no ground
  truth of all actual changes, it is a lower bound conditioned on probe coverage, and multiple
  testing across many probes inflates false positives. `mitigation: "frame the estimand
  explicitly as a lower bound, apply Holm–Bonferroni correction, and report the same-version
  null false-positive rate (RQ3) so readers can discount the detector's error."` [HYPOTHESIS]
- **t5** [`reproducibility`]: Continuously and partially rolled-out API updates (C4) mean the exact
  diff measured at one time may not be reproducible later, threatening replication of reported
  rates. `mitigation: "log raw probe responses, timestamps, and M2 logprob fingerprints, release
  them as a frozen audit trail, and restrict headline claims to transitions with a clean
  fingerprint discontinuity."` [HYPOTHESIS]

**Status:** PARTIAL. `absence_comment`: {"what_missing": "No real Limitations/Threats section
exists because no paper has been written.", "why_matters": "A reviewer should not mistake this
forward-looking risk list for author-acknowledged limitations, which carry more evidentiary
weight.", "implication": "Use this list as a pre-registration-style risk checklist to design
around before running the study."}

---

## N11 Artifacts

**Status:** NOT_FOUND. `artifacts: []`. `has_code: false`, `has_data: false`, `has_model: false`.
[PLACEHOLDER — nothing can be released because no paper/implementation exists yet.]
`absence_comment`: {"what_missing": "There is no code repository, probe-suite dataset, or model
associated with this topic — it is a research idea, not a completed project.", "why_matters":
"Artifact availability is a real reviewer signal (reproducibility, reusability of the probe suite
and alignment pipeline); its current absence is the accurate status.", "implication": "If executed,
the probe suite (M1), the version-capture pipeline (M2), the alignment code (M4), and the frozen
raw-response audit trail are the natural artifacts to release."}

---

## N12 Contribution Type

**value:** `empirical` [HYPOTHESIS]

**rationale:** The headline deliverable is a *measurement* — the rate and category-distribution of
undocumented behavioral change (CO1/CO3) — validated by the seed's changelog-vs-behavior alignment
analysis, with the probe suite/pipeline (CO2) serving as instrumentation rather than the primary
artifact. Per the N12 disambiguation hints, a measurement study is `empirical` when the study's
finding is the main contribution and the supporting tooling is a means to that end; this matches
the seed's framing ("结论直接服务问责" — the *conclusions* serve accountability, not the tooling
per se). Had the reusable pipeline been the headline (as in a released-tool paper), `tool` would
be the better fit — flagged so a real write-up can re-decide based on which N9 result it foregrounds.
[HYPOTHESIS]

---

## Claims

- "A substantial share of empirically measurable behavioral changes across AI-system versions go
  unmentioned in vendor changelogs." — `evidence: [{type: "argument", text: "core question framed
  around 'what proportion... never appears in changelogs', implying the expected finding is
  non-trivial; every N3 component capability exists but none aligns diffs to disclosure",
  source: "HYPOTHESIS", location: null}]` [HYPOTHESIS]
- "Silent changes are not uniformly distributed across behavior types — safety/refusal,
  formatting, and latency are disproportionately likely to go undocumented relative to factual
  accuracy." — `evidence: [{type: "argument", text: "seed's second clause asks specifically where
  silent changes concentrate, implying a non-uniform distribution is the expected finding",
  source: "HYPOTHESIS", location: null}]` [HYPOTHESIS]
- "Existing black-box audit tools ([LogProbTracking, OpenReview:hFxivbAgVP], [RankUniformity,
  OpenReview:PSIe9mmF7a]) can detect THAT a served model changed but cannot label a change as
  documented or silent, because none aligns detected diffs to vendor disclosure text." —
  `evidence: [{type: "citation", text: "N4 limitations grounded in the two papers' own
  method scope", source: "GROUNDED:corpus", location: "N3/N4"}]` [HYPOTHESIS]
- "Vendors have no structural incentive to voluntarily produce this accounting, so third-party
  measurement is a necessary accountability mechanism." — `evidence: [{type: "citation", text:
  "near-verbatim from seed: '结论直接服务问责，厂商结构性不会自己做'", source: "GIVEN",
  location: "README.md, 最小实验 line"}]` [GIVEN]
- "The measured silent-change rate is a lower bound, not the true rate, because no independent
  ground truth of 'all actual changes' in a release exists." — `evidence: [{type: "argument",
  text: "derived from C3 — vendors do not reveal a complete changelist, so probe-suite coverage
  caps what can be detected", source: "HYPOTHESIS", location: null}]` [HYPOTHESIS]

---

## Self-verification pass (per `references/self-verification.md`)

- **V-01 locator integrity:** No item is tagged `source="extracted"`+`status="FOUND"` with a
  missing locator; all extracted-style content is [GIVEN] anchored to the seed README, all
  method/result content is [HYPOTHESIS]/[PLACEHOLDER], and all N3 corpus entries carry a real
  `OpenReview:paper_id` + paper_url.
- **V-04 ID consistency (EX-09):**
  - N4 `affects_works` ⊆ N3 `citation_key`s: every affects_works string
    (`[LogProbTracking, OpenReview:hFxivbAgVP]`, `[RankUniformity, OpenReview:PSIe9mmF7a]`,
    `[BiasSimilarity, OpenReview:EveruzAsGI]`, `[TAIG, OpenReview:Be2B6f0ps1]`,
    `[SafeHarbor, OpenReview:dLojMSgSFW]`, `[RobustAudit, OpenReview:AiaVCVDuxF]`,
    `[FairBetting, OpenReview:EEVpt3dJQj]`, `[LAMDA, OpenReview:1FnCrZtBNQ]`,
    `[Chen, Zaharia & Zou, 2023]`) appears verbatim as an N3 citation_key ✓
  - N6 `challenge_arguments[].challenge_id` ⊆ {C1,C2,C3,C4} ✓ (uses C1,C2,C4);
    `mechanism_components` ⊆ {M1..M5} ✓; `unaddressed_challenges=[C3]` ⊆ {C1..C4} ✓
  - N8 `addresses_challenges` ⊆ {C1..C4} ✓; `tests_contributions` ⊆ {CO1,CO2,CO3} ✓
    (RQ1→CO1, RQ2→CO3, RQ3→CO2, covering all three); `evaluates_mechanisms` ⊆ {M1..M5} ✓
  - N9 `rq_id` ∈ {RQ1,RQ2,RQ3} = N8 ids ✓
- **V-08:** N6 `unaddressed_challenges` and all N9 results re-flagged as inferred/[HYPOTHESIS],
  not extracted-confidence.
- **V-10/V-11:** N10 status PARTIAL with a non-empty, mitigated, categorized list (≥4:
  construct/internal/external/conclusion/reproducibility); N11 NOT_FOUND with all three flags
  `false` and `artifacts=[]`.
- **V-12:** N12 rationale cites the instrumentation-vs-finding distinction and names the `tool`
  alternative rather than asserting circularity.
- **Empty-node check (EX-11):** N0–N12 plus Claims all present.
