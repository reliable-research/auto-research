# Digest: Is Corpus-Level Estimation Strategy-Proof? The Economics of Evasion at Population Scale

> **REVERSE-DIGEST DISCLAIMER.** This document does not summarize an existing paper. No such
> paper has been written. It is speculative scaffolding built backward from a one-paragraph
> research-idea seed (topic code B6.5, label `[矛盾]` / "contradiction", parent topic "B6.
> Contamination-mechanism layer (synthetic corpus)") to the shape a full N0–N12 digest would
> take *if* the idea were executed as described. Every field below is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README; **[HYPOTHESIS]** = reasoned
> elaboration / prediction, not a fact; **[PLACEHOLDER]** = genuinely unknowable until the
> work exists (authors, numbers, DOI, artifacts); **[GROUNDED:corpus]** = grounded in a real
> paper retrieved from the local OpenReview idea corpus (`topics/corpus/ideas.jsonl`), with a
> resolvable `paper_id`/URL. Do not cite this file as evidence of a real *result*; the N3
> works, however, are real papers.

---

## N0 — Metadata

- `title`: "Is Corpus-Level Estimation Strategy-Proof? The Economics of Evasion at Population Scale" **[GIVEN]** (seed README, English gloss of 语料级估计的策略稳健性)
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — no paper exists, no authors assigned
- `abstract` **[HYPOTHESIS]** (drafted by synthesizing the seed's core question + minimal experiment into abstract prose; a draft, not a real printed abstract):
  > "Recent work has shown that single-document detectors of LLM-generated text can be
  > defeated by a rewriting/paraphrase adversary operating within a modest per-document
  > budget, casting doubt on the reliability of AI-text detection at the level of individual
  > documents. This raises a natural but under-examined question: does the same fragility
  > propagate to *corpus-level* estimation, where the goal is not to label any single
  > document but to estimate the aggregate proportion of AI-generated content in a
  > population of documents? Building on distributional prevalence estimators that fit an
  > AI/human mixing coefficient by maximum likelihood over aggregate token statistics, we
  > formalize a cost–accuracy game between a budget-constrained paraphrasing adversary and a
  > population-scale distributional estimator, and study how the adversary's budget required
  > to bias the corpus-level estimate by a fixed margin scales with corpus size. We
  > hypothesize that, unlike single-document detection, distributional estimation error
  > induced by a fixed-budget adversary shrinks (or the required budget grows) as corpus size
  > increases, making evasion of corpus-level estimates economically unattractive at scale
  > even when per-document detection remains evadable."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"NLP"` **[HYPOTHESIS]** (task is AI-generated-text detection/estimation; the economics/game-theory framing is a secondary lens on an NLP measurement problem, not a standalone Theory or Security contribution)
- **Status:** `PARTIAL` — title given, everything else hypothesized/placeholder; no `authors`/`abstract` are real.
- `absence_comment`: `{"what_missing": "There is no real author list or printed abstract because no paper has been written yet — only a one-paragraph research-idea seed exists.", "why_matters": "A reader relying on this digest for citation or attribution would be citing a nonexistent work.", "implication": "Treat N0 purely as a planning placeholder; re-derive it from the actual paper once written."}`

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]** (full predicate; task kind / domain / outcome all present):
  *"Estimate the population-level proportion of AI-generated documents within a large text
  corpus under a rewrite-budget-bounded paraphrasing adversary, and characterize whether the
  adversary's cost of biasing that aggregate estimate grows uneconomically with corpus size,
  in contrast to the known cost-effectiveness of evading single-document AI-text detectors."*
  - Self-check: task kind = measurement/estimation (a mixing coefficient) plus an
    adversarial cost analysis; domain = AI-generated-text prevalence in document corpora;
    outcome shape = a cost–accuracy curve (min adversary budget to bias the estimate by ε vs.
    corpus size N). All three land.
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment:
  1. A corpus of N documents with a known ground-truth mixture of human-written and
     LLM-generated text (for controlled evaluation).
  2. A corpus-level distributional/prevalence estimator (not a per-document classifier).
  3. An adversary with a fixed total rewrite/paraphrase budget (tokens rewritten, fraction of
     documents touched, or paraphrase-compute/API spend).
- `outputs` **[HYPOTHESIS]**:
  1. An estimated population proportion α̂ of AI-generated content with an associated error
     bound / confidence interval relative to ground truth.
  2. A cost–accuracy curve: minimum adversary budget required to bias α̂ by a margin ε, as a
     function of corpus size N (and its fitted scaling exponent).
- `constraints`:
  - "The adversary operates under a fixed, given rewrite budget (not unlimited)." **[GIVEN]**
    (seed: 给定改写预算的对抗者)
  - "The estimator only needs the aggregate/population distribution, not correct per-document
    labels." **[GIVEN]** (implied by 语料级 "corpus-level" vs. 单文档 "single-document")
  - "Single-document detection is presupposed already broken by paraphrasing (an established
    prior result, not something this paper re-derives)." **[GIVEN]** (seed: 单文档检测已被证明可被改写击穿)
- **Status:** `PARTIAL` — objective/inputs/outputs are plausible reconstructions, not extracted from a real methods section.
- `absence_comment`: `{"what_missing": "No formal problem statement exists yet beyond the seed's one-sentence core question.", "why_matters": "Downstream nodes (N6 methodology, N8 RQs) depend on a stable formulation; an under-specified one could drift.", "implication": "Revisit N1 first once any real draft exists, since it anchors everything else."}`

---

## N2 — Motivation

**[HYPOTHESIS]**, reconstructed from the seed's `parent_topic` framing ("B6. Contamination
mechanism layer (synthetic corpus)") and echoing the real, corpus-grounded motivation of the
population-scale monitoring literature (see `[MonitorAIScale, OpenReview:bX3J7ho18S]` in N3).
No invented statistics.

- `motivation_text`: "As synthetic (LLM-generated) text increasingly contaminates corpora used
  for training-data curation, content-authenticity auditing, and platform-scale moderation,
  decision-makers rarely need a verdict on any single document — they need to know what
  *fraction* of a large corpus is synthetic. A real and growing line of work reframes AI-text
  detection as a corpus-level measurement problem precisely because instance-level detection
  is unstable under paraphrasing and adversarial pressure. But if the well-established result
  that single-document detectors are broken by paraphrasing is uncritically generalized to
  imply that corpus-level contamination estimates are equally gameable, practitioners may
  wrongly abandon population-scale auditing — or wrongly trust it. Determining whether the two
  problems actually share the same fragility (or not) is therefore consequential for how much
  trust to place in corpus-level contamination measurements used in data-curation and
  governance pipelines." **[HYPOTHESIS]**, `evidence`: `[]`
- **Status:** `PARTIAL` — a reasoned reconstruction from the parent-topic label plus the real N3 motivation texts, not text extracted from a real Introduction.
- `absence_comment`: `{"what_missing": "No real Introduction/Motivation section exists to quote for this specific paper.", "why_matters": "A reviewer cannot verify this framing matches what the authors would actually argue.", "implication": "Treat this as a plausible motivation sketch to be replaced by the authors' actual framing."}`

---

## N3 — Related Works

**Method note.** Grounded via keyword search over the local OpenReview corpus
(`topics/corpus/ideas.jsonl`, 11,683 papers) using `search_ideas.py`. Queries spanned the
mechanism (machine-generated-text detection; token-score aggregation), the failure mode
(paraphrase / adaptive-attack evasion; watermark removal), the evaluation target
(corpus-/population-level prevalence and proportion estimation; quantification), and the
economic lens (strategic manipulation under a budget; mechanism design). All seven entries
below are **real papers** with resolvable OpenReview IDs, tagged `[GROUNDED:corpus]`. Each
`approach_summary` is grounded in the paper's own motivation/method text.

| citation_key | approach_summary | source | location |
|---|---|---|---|
| `[MonitorAIScale, OpenReview:bX3J7ho18S]` | Reframes AI-text detection as a *measurement* rather than classification problem: fits a distributional maximum-likelihood mixture model over aggregate token-occurrence statistics (e.g. adjective frequencies) from human vs. AI reference corpora to estimate the *proportion* of AI-modified text in a corpus, validated on semi-synthetic mixtures with known AI fractions. This is the closest real precedent for the corpus-level estimator this topic studies. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "estimates the proportion of AI-modified text in a corpus by modeling it as a mixture", "paper_url": "https://openreview.net/forum?id=bX3J7ho18S"}` |
| `[DetectGPT, OpenReview:UiAyIILXRd]` | Zero-shot, per-document machine-generated-text detector: compares a passage's log-probability to the expected log-probability of small semantics-preserving perturbations (T5 mask-filling), using negative local curvature of the model's log-prob function as the signal. The canonical single-document baseline whose known paraphrase-fragility motivates the topic. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "estimating the local curvature of a language model's log-probability function", "paper_url": "https://openreview.net/forum?id=UiAyIILXRd"}` |
| `[AdaptiveWMAttack, OpenReview:AsODat0dkE]` | Models watermark evasion as an explicit optimization problem: formalizes robustness-as-objective (expected verification failure + quality-preservation term) and trains a low-cost, budget-constrained *adaptive* paraphrase attacker via DPO with surrogate watermark keys, arguing adaptive attackers should be the baseline, not an edge case. Directly the "economics of evasion" / budget-bounded adversary lens. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "model watermark evasion as an explicit optimization problem", "paper_url": "https://openreview.net/forum?id=AsODat0dkE"}` |
| `[MarkovCalib, OpenReview:Lzwkeg2o2z]` | A detector-agnostic calibration layer that treats a base detector's per-token scores as noisy evidence and applies pairwise-MRF mean-field inference (plus positional down-weighting of unstable early tokens) before *aggregating* to a passage-level decision, to improve robustness including under paraphrasing. Relevant to how per-document signals are aggregated. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "refines token-level detection scores before final passage-level aggregation", "paper_url": "https://openreview.net/forum?id=Lzwkeg2o2z"}` |
| `[DUCI, OpenReview:EUSkm2sVJ6]` | Estimates the *proportion* of a dataset used in training by debiasing noisy per-record membership-inference signals (correcting for estimated TPR/FPR) and aggregating them into an unbiased proportion estimate with asymptotic-normality confidence intervals. A general "debias-and-aggregate weak signals into a population proportion" template applicable to a corpus-level AI-prevalence estimator. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "unbiased estimator of dataset usage with confidence intervals", "paper_url": "https://openreview.net/forum?id=EUSkm2sVJ6"}` |
| `[AnchorPeerReview, OpenReview:HyZwf1rt4s]` | Builds a paired human/LLM peer-review benchmark and a manuscript-conditioned detector (Anchor), benchmarking zero-shot detectors in the strict low-false-positive regime; explicitly motivated by prior *population-level* estimates of LLM involvement in reviews. Shows the instance-level detection layer that sits atop corpus-level prevalence claims. | [GROUNDED:corpus] | `{"page": null, "section_title": "Motivation", "quote": "estimated substantial LLM involvement in conference reviews at the population level", "paper_url": "https://openreview.net/forum?id=HyZwf1rt4s"}` |
| `[UCB-S, OpenReview:lsxeNvYqCj]` | Incentive-aware bandit mechanism (UCB-S) for a setting where arms strategically inflate an observed statistic (click-through rate) under a manipulation budget; uses confidence-based screening to make manipulation unprofitable and proves regret bounds across all Nash equilibria. A real ML instantiation of the "is this statistic strategy-proof / robust to budget-bounded manipulation?" question the title poses. | [GROUNDED:corpus] | `{"page": null, "section_title": "Method", "quote": "aligning arm incentives ... induce approximate truthfulness in equilibrium", "paper_url": "https://openreview.net/forum?id=lsxeNvYqCj"}` |

- **Status:** `FOUND` (as a related-work set) — seven real, resolvable papers spanning the corpus-level estimator, the single-document baseline, the budget-bounded adversary, aggregation, proportion estimation, the instance-level layer, and the strategy-proofness lens. Relevance judgments are the digest author's, not the papers' own related-work framing.
- `absence_comment`: `null`

---

## N4 — Prior Limitations

**[HYPOTHESIS]** — inferences about what each cited work demonstrably does *not* cover, tied to
its own motivation/method text; every `affects_works` string matches an N3 `citation_key`
verbatim.

| limitation_text | affects_works | limitation_type | source |
|---|---|---|---|
| "The distributional mixture-MLE estimator is validated only on *semi-synthetic* mixtures generated under a benign, non-adversarial process; it never models an adversary who paraphrases specifically to shift the estimated mixing coefficient, so its reported accuracy says nothing about strategy-proofness under a budget-bounded attacker." | `["[MonitorAIScale, OpenReview:bX3J7ho18S]"]` | generalizability | HYPOTHESIS |
| "The detector produces per-document curvature verdicts and, as the topic's premise and follow-up work note, degrades under paraphrasing; it offers no aggregate-estimate quantity and thus no notion of whether averaging over a corpus could restore robustness that per-document detection loses." | `["[DetectGPT, OpenReview:UiAyIILXRd]"]` | generalizability | HYPOTHESIS |
| "The adaptive attack defines its evasion objective and budget *per text* against a per-text watermark verifier; it never asks whether the same per-document budget still suffices to move a population-level statistic, i.e. whether evasion cost changes when the target shifts from one verdict to an aggregate estimate." | `["[AdaptiveWMAttack, OpenReview:AsODat0dkE]"]` | generalizability | HYPOTHESIS |
| "The calibration layer improves *passage-level* (single-document) aggregation of token scores under benign sampling noise (a Markov smoothness prior), but assumes noise is incidental, not adversarially coordinated across documents, and still targets a per-passage decision rather than a corpus proportion." | `["[MarkovCalib, OpenReview:Lzwkeg2o2z]"]` | generalizability | HYPOTHESIS |
| "The debias-and-aggregate proportion estimator assumes the per-record measurement error rates (TPR/FPR) are stationary and estimable from reference models; an adversary who deliberately shifts per-record signals to bias the aggregate violates that stationarity assumption, which is outside the method's scope." | `["[DUCI, OpenReview:EUSkm2sVJ6]"]` | theoretical | HYPOTHESIS |
| "The peer-review work builds an instance-level detector benchmarked at low FPR and merely *cites* prior population-level LLM-prevalence estimates as motivation; it neither analyzes the robustness of those population estimates to strategic evasion nor connects the low-FPR instance layer to an aggregate estimator's error." | `["[AnchorPeerReview, OpenReview:HyZwf1rt4s]"]` | scalability | HYPOTHESIS |
| "The strategy-proofness result is developed for bandit *allocation* under a manipulation budget, with a payment-free mechanism disciplining arms via screening; it provides the economic vocabulary of 'robust to budget-bounded manipulation' but has no existing bridge to text-corpus distributional prevalence estimation." | `["[UCB-S, OpenReview:lsxeNvYqCj]"]` | theoretical | HYPOTHESIS |

- `grounding_check`: `true` — every limitation lists at least one `affects_works` entry matching an N3 `citation_key`.
- **Status:** `PARTIAL` overall — reasoned inferences about what the cited works do not cover, not limitations the papers' own authors state about themselves.
- `absence_comment`: `{"what_missing": "These are the digest author's inferences of coverage gaps, not verbatim author-stated limitations.", "why_matters": "Real N4 limitations should be near-verbatim author claims; confidence should be downgraded accordingly.", "implication": "Re-derive N4 from each paper's own Limitations text when the real paper is scoped."}`

---

## N5 — Challenges

**[HYPOTHESIS, tightly derived]** — problem-inherent obstacles implied by the core question,
passing the N4-vs-N5 test (about the problem, not a named tool's failure). Stable C-ids.

| id | text | source |
|---|---|---|
| C1 | "An estimator that needs only the aggregate proportion may average out *independent* per-document paraphrase noise, but it is unclear whether this averaging survives when an adversary *coordinates* rewrites across the whole corpus specifically to shift the aggregate statistic in one direction (a directional, correlated perturbation rather than i.i.d. noise)." | HYPOTHESIS |
| C2 | "Defining a realistic adversary 'cost' (tokens rewritten, paraphrase-compute/API spend, or fraction of documents touched) is itself non-trivial, because different cost models imply different optimal attacks — uniformly light rewriting of every document vs. heavy rewriting of a concentrated subset — and the strategy-proofness conclusion must not be an artifact of one arbitrary cost model." | HYPOTHESIS |
| C3 | "There is no natural ground truth for the 'true corpus-level AI-generation proportion' in real uncurated corpora, so testing strategy-proofness requires constructing synthetic/semi-synthetic corpora with known, controllable mixtures — raising external-validity concerns about transfer to real corpora." | HYPOTHESIS |
| C4 | "A fully adaptive (white-box) adversary who knows the exact corpus-level estimator's aggregation statistic could target it directly — a strictly harder setting than the budget-bounded, non-omniscient paraphrase adversary the seed's 'given rewrite budget' framing implies." | HYPOTHESIS |

- `conflation_check`: `true` — averaging/coordination robustness (C1) vs. cost-model definition (C2) vs. ground-truth/external-validity (C3) vs. adaptive-adversary threat model (C4) are distinct.
- **Status:** `PARTIAL` — derived from the seed's core question and standard practice for adversarial-estimation studies.
- `absence_comment`: `{"what_missing": "No paper exists with an explicit challenges discussion.", "why_matters": "A real design must argue it overcomes these in N6; a real paper might surface additional ones.", "implication": "Use as a working challenge list to validate/replace once real methodology begins."}`

---

## N6 — Methodology

**[HYPOTHESIS]** — extrapolated from the seed's minimal experiment (a rewrite-budget adversary
vs. distribution estimator cost-accuracy game), operationalized against the real N3 methods.

### `overview`
"The method constructs synthetic/semi-synthetic corpora with known ground-truth AI proportions,
builds a corpus-level distributional prevalence estimator (a mixture maximum-likelihood
estimator over aggregate token statistics à la `[MonitorAIScale, OpenReview:bX3J7ho18S]`, and,
as an alternative, a debias-and-aggregate estimator over per-document detector scores à la
`[DUCI, OpenReview:EUSkm2sVJ6]`), and pits it against a budget-constrained paraphrasing
adversary whose objective is to bias the *aggregate* estimate α̂ rather than to individually
evade detection. A best-response search over the adversary's budget-allocation strategy
(uniform light rewriting vs. concentrated heavy rewriting) finds the minimum budget to bias α̂
by a target margin ε; this search is then repeated as corpus size N is scaled up, fitting how
minimum-budget-to-bias-ε scales with N to test whether evasion cost grows uneconomically.

**Staged plan.**
- **Pilot (= the seed's minimal experiment):** one fixed corpus size, one generator family,
  the distributional estimator (M2) vs. a non-adaptive fixed-budget paraphrase adversary
  (M3) — measure the cost–accuracy game (M4) at a single N. Reproduce single-document
  fragility (M1) as the control.
- **Scale-up:** sweep corpus size N across orders of magnitude (M5), add multiple generator
  families and domains, add the *adaptive/coordinated* adversary variant, and fit the
  budget-vs-N scaling exponent." **[HYPOTHESIS]**

### `key_components`
| id | name | text (what is measured/built, with what instrument, at what granularity) |
|---|---|---|
| M1 | Single-document detector control | A per-document zero-shot detector (`[DetectGPT, OpenReview:UiAyIILXRd]`-style log-prob curvature via T5 mask-fill perturbations, or a Fast-DetectGPT variant) scored under an open scoring LM (e.g. GPT-2/OPT). Instrument: per-document AUROC before/after paraphrase. Granularity: per document. Purpose: reproduce the known collapse under paraphrasing as the pessimistic baseline. |
| M2 | Corpus-level prevalence estimator | Primary: a mixture-MLE estimator (`[MonitorAIScale, OpenReview:bX3J7ho18S]`-style) that estimates token-occurrence distributions over a stable restricted vocabulary from human and AI reference corpora and fits a single mixing coefficient α̂ by maximizing corpus log-likelihood, with a bootstrap CI. Alternate: `[DUCI, OpenReview:EUSkm2sVJ6]`-style debias-and-aggregate of M1's per-document scores. Granularity: whole corpus. |
| M3 | Budget-constrained adversary simulator | A parameterized LLM paraphraser applied under a global budget B (total tokens rewritten, or fraction f of documents touched × rewrite strength). Non-adaptive variant: fixed paraphraser (DIPPER-style). Adaptive variant: a preference-optimized paraphraser à la `[AdaptiveWMAttack, OpenReview:AsODat0dkE]` trained to shift α̂ using a surrogate estimator. Granularity: per-document rewrite decisions under a shared budget constraint. |
| M4 | Cost–accuracy best-response search | A search over allocation strategies (uniform-light vs. concentrated-heavy; which documents to rewrite) to find, for a given estimator and corpus, the minimum budget needed to bias α̂ by margin ε. Instrument: greedy/grid search against a surrogate estimator; report budget-to-bias-ε. |
| M5 | Corpus-scale sweep | Repetition of M4 across N ∈ {10², 10³, 10⁴, 10⁵}, fitting minimum-budget-to-bias-ε vs. N by log-log regression to recover a scaling exponent β (flat/sublinear vs. linear vs. superlinear), with bootstrap CIs on β. |

(all `source="inferred/HYPOTHESIS"`, `location` null — no real paper text to anchor to)

### `challenge_arguments`
| challenge_id | argument_text | mechanism_components |
|---|---|---|
| C1 | "M2's aggregation-based estimator is argued to average out independent per-document paraphrase noise; M3's *adaptive/coordinated* variant plus M4's best-response search explicitly test whether a correlated, directional rewrite allocation defeats this averaging." | `["M2", "M3", "M4"]` |
| C2 | "M3 makes the cost model explicit and parameterized (tokens / fraction touched / paraphrase-compute), and M4 explores multiple allocation strategies under the *same* fixed budget, so the strategy-proofness conclusion can be checked for robustness across cost models rather than assumed." | `["M3", "M4"]` |
| C3 | "Using synthetic/semi-synthetic corpora with controlled ground-truth mixtures (following `[MonitorAIScale, OpenReview:bX3J7ho18S]`'s semi-synthetic validation) is the mechanism that makes M5's scaling curve measurable at all, at the acknowledged cost of external validity (see N10)." | `["M2", "M5"]` |

(all `source="inferred/HYPOTHESIS"`)

### `unaddressed_challenges`
`["C4"]` — "The fully adaptive white-box adversary (C4) who directly targets the exact
estimator's aggregation statistic is out of scope for the budget-bounded paraphrase adversary
the minimal experiment describes; M3/M4's adaptive variant approximates but does not assume a
fully estimator-omniscient attacker." **[HYPOTHESIS]**

### `feasibility` **[HYPOTHESIS]**
- **Order of magnitude.** Reference corpora ≈ 10⁴ human + 10⁴ AI documents (reused from
  existing benchmarks, no new annotation). Synthetic evaluation corpora up to N = 10⁵ documents.
  #estimator fits ≈ (5 corpus sizes) × (≈3 allocation strategies) × (2 estimator families) ×
  (3–5 seeds) ≈ several hundred fits — each fit is cheap (token-count MLE / score aggregation,
  CPU-seconds to minutes). **Dominant cost = paraphrasing:** rewriting up to ~10⁵ documents
  with an LLM paraphraser is a few GPU-days on a local 7B model, or a low-hundreds-of-dollars
  API-cost class. Annotator-hours ≈ 0 (ground truth is synthetic).
- **Biggest feasibility risk + mitigation.** The *adaptive* adversary (M3 DPO variant, C1)
  needs a training signal against a non-differentiable corpus estimator. Mitigation: follow
  `[AdaptiveWMAttack, OpenReview:AsODat0dkE]` — optimize against a *surrogate* estimator with
  best-of-N preference data rather than gradients, and treat the adaptive result as a lower
  bound on evasion difficulty rather than a tight optimum.

- **Status:** `PARTIAL` — a plausible operational extrapolation from one sentence, not extracted content.
- `absence_comment`: `{"what_missing": "No real methods section exists; M1-M5 are a best-guess operationalization of the seed's cost-accuracy game.", "why_matters": "A real implementation might choose a different estimator family (score histograms, perplexity-curvature statistics, n-gram drift) or cost model.", "implication": "Use as a starting design sketch, not a commitment to specific techniques."}`

---

## N7 — Contributions

**[HYPOTHESIS]** — framed from the extrapolated method + the seed's stated potential finding.

| id | text | contribution_type | is_testable | has_rq |
|---|---|---|---|---|
| CO1 | "A cost–accuracy framework that formalizes 'evasion economics' for corpus-level AI-text prevalence estimation, distinguishing it conceptually and operationally from single-document detection evasion." | conceptual_framework | true | true |
| CO2 | "An empirical (hypothesized) demonstration that the adversary budget required to bias a corpus-level estimate by a fixed margin grows with corpus size N, in contrast to single-document detection where a roughly fixed per-document paraphrase cost suffices regardless of corpus size." | empirical_finding | true | true |
| CO3 | "A corpus-level prevalence estimator that remains accurate under a bounded-budget paraphrasing adversary even when a paired single-document detector's per-document accuracy collapses under the same attack." | technical_artifact | true | true |
| CO4 | "A characterization of the boundary conditions (adversary budget, coordination capability, corpus size) under which the pessimistic single-document conclusion does vs. does not transfer to the corpus-level setting." | empirical_finding | true | true |

- **Status:** `PARTIAL` — claims a paper answering this idea would plausibly make, not extracted contributions.
- `absence_comment`: `{"what_missing": "No paper exists to state these contributions in its own words.", "why_matters": "Contribution framing strongly shapes novelty assessment; this is a guess.", "implication": "Replace verbatim once a real Contributions list exists."}`

---

## N8 — Research Questions

| id | text | rq_source | addresses_challenges | tests_contributions | evaluates_mechanisms | answered_by_experiment |
|---|---|---|---|---|---|---|
| RQ1 | "Is corpus-level (population-scale) distribution estimation of AI-generated text similarly fragile to adversarial paraphrasing as single-document detection has been shown to be, or does the cost of evasion become uneconomical as corpus scale increases?" **[GIVEN]** (near-verbatim restatement of the seed's 核心问题) | explicit | `["C1","C2","C4"]` | `["CO1","CO2","CO4"]` | `["M1","M2","M3","M4","M5"]` | "The cost–accuracy game between the budget-bounded paraphrase adversary (M3/M4) and the corpus-level estimator (M2), swept across corpus sizes (M5), with M1 as the fragile control." |
| RQ_INF_1 | "What is the minimum adversary rewrite budget required to shift the corpus-level estimate by a fixed margin ε, and how does that minimum budget scale with corpus size N (fitted exponent β)?" **[HYPOTHESIS]** (inferred — the minimal experiment describes exactly this cost-accuracy game; makes the scaling claim implicit in 语料级天然更抗规避 testable) | inferred | `["C1","C2"]` | `["CO2","CO3"]` | `["M4","M5"]` | "The M5 corpus-scale sweep of the M4 best-response search, fitting minimum-budget-for-ε-bias vs. N by log-log regression." |
| RQ_INF_2 | "Does a dedicated distributional/aggregating estimator (M2) provide robustness to a fixed-budget adversary that a naive average-of-per-document-predictions estimator does not, i.e. is any robustness a property of aggregation design rather than of corpus-level estimation per se?" **[HYPOTHESIS]** (inferred — isolates the internal-validity confound flagged in N10 t3) | inferred | `["C1","C3"]` | `["CO3","CO4"]` | `["M1","M2"]` | "Compare α̂ error under attack for the mixture-MLE estimator, the debias-and-aggregate estimator, and a naive per-document-average estimator, at matched budget and corpus size." |

- `datasets` **[HYPOTHESIS]**: `{"names": ["RAID (Dugan et al., 2024) — large multi-domain, multi-generator machine-generated-text detection benchmark including adversarial/paraphrase variants, referenced as @dugan2024raid by [AnchorPeerReview, OpenReview:HyZwf1rt4s]", "HC3 (Human ChatGPT Comparison Corpus, Guo et al., 2023) — paired human/LLM answers for controlled human-vs-AI mixtures, referenced as @guo2023hc3 by [AnchorPeerReview, OpenReview:HyZwf1rt4s]", "Semi-synthetic mixed corpora with experimenter-controlled ground-truth AI proportion, built from the above (mirrors the semi-synthetic validation of [MonitorAIScale, OpenReview:bX3J7ho18S])"], "source": "inferred"}`
- `baselines` **[HYPOTHESIS]**: `{"names": ["Single-document DetectGPT/Fast-DetectGPT detector as the known-fragile control ([DetectGPT, OpenReview:UiAyIILXRd])", "Naive corpus estimate = mean of per-document detector predictions (no calibration/aggregation design)", "Distributional mixture-MLE estimator ([MonitorAIScale, OpenReview:bX3J7ho18S]-style) as the proposed corpus estimator", "Non-adaptive fixed paraphrase adversary (DIPPER-style) vs. adaptive DPO-tuned adversary ([AdaptiveWMAttack, OpenReview:AsODat0dkE]-style)"], "source": "inferred"}`
- `metrics` **[HYPOTHESIS]**: `{"names": ["Absolute error |α̂ − α| between estimated and true corpus AI-proportion", "Per-document detection AUROC (the known-fragile baseline, for comparison)", "Adversary budget spent (tokens rewritten / fraction of corpus touched / paraphrase-compute units)", "Minimum budget to bias α̂ by margin ε", "Fitted scaling exponent β of minimum-budget-to-bias-ε vs. corpus size N (log-log slope)"], "source": "inferred"}`
- **Analysis plan** **[HYPOTHESIS]**: sample size = 3–5 seeds per (N, strategy, estimator) cell, N swept over {10²…10⁵}; statistical test = bootstrap 95% CIs on α̂ error and on the scaling exponent β, with a one-sided test of H₀: β ≤ 0 vs. H₁: β > 0 (budget grows with N); significance threshold α = 0.05. Expected effect direction: |α̂ − α| stays near the no-adversary baseline as N grows under a fixed budget, and β > 0 (budget-to-bias-ε increases with N), while per-document AUROC collapses regardless of N.
- **Status:** `PARTIAL` — RQ1 faithfully restates the given core question; RQ_INF_1/RQ_INF_2, datasets, baselines, metrics, and analysis plan are inferred but grounded in real named benchmarks and the N3 estimator families.
- `absence_comment`: `{"what_missing": "No real evaluation section exists to extract explicit RQs/datasets/baselines/metrics from.", "why_matters": "Benchmark and metric choices materially affect how convincing any result would be.", "implication": "Validate RAID/HC3 suitability and estimator choices against the real detection literature once the paper is scoped."}`

---

## N9 — Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].** No experiment has been run. Nothing below is a
real number; each states only a predicted *direction*, explicitly falsifiable.

| rq_id | result_text (hypothesized direction) | result_type | evidence_strength | rq_answered |
|---|---|---|---|---|
| RQ1 | "[HYPOTHESIS] The corpus-level estimator's proportion error under a fixed-budget adversary is predicted to remain near the no-adversary baseline even as the paired single-document detector's per-document AUROC collapses under the same paraphrasing — i.e., corpus-level estimation is hypothesized to be more strategy-proof than single-document detection." | quantitative | missing | false |
| RQ_INF_1 | "[HYPOTHESIS] The minimum adversary budget to bias α̂ by margin ε is predicted to grow with corpus size N (fitted β > 0, ideally ≥ linear), making aggregate-estimate evasion increasingly uneconomical at scale, in contrast to single-document evasion cost which stays roughly flat in N." | quantitative | missing | false |
| RQ_INF_2 | "[HYPOTHESIS] The mixture-MLE and debias-and-aggregate estimators are predicted to show materially smaller α̂ error under attack than the naive per-document-average estimator at matched budget — indicating robustness stems from aggregation *design*, partially, rather than from corpus-level estimation alone." | quantitative | missing | false |

**Falsification conditions** (mirroring the seed's framing that this is a reversible prediction):
- **RQ1 refuted if** the corpus-level estimator's proportion error grows to the same order of
  magnitude as single-document detection failure under the same adversary budget — i.e.,
  aggregation provides no meaningful robustness benefit and the seed's counterintuitive result
  does not hold.
- **RQ_INF_1 refuted if** the minimum budget-to-bias-ε stays flat or *shrinks* as N grows
  (fitted β ≤ 0; evasion gets cheaper, not more expensive, at scale), so evasion economics do
  not favor the defender at population scale.
- **RQ_INF_2 refuted if** the naive average estimator is *equally* robust to the dedicated
  estimators under attack — which would suggest any observed robustness is a generic property
  of aggregating many documents, not of the specific estimator, weakening CO3.

- **Status:** `NOT_FOUND` for all — no experiment run.
- `absence_comment`: `{"what_missing": "No experimental data exists; only directional hypotheses and falsification conditions.", "why_matters": "Reporting a fabricated number would misrepresent an unexecuted study as having empirical support.", "implication": "Re-derive this node from a real experiment before any evidence_strength above 'missing' is claimed."}`

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS]** — anticipated limitations of this class of study; no real Limitations section exists.

| threat_id | category | description | mitigation |
|---|---|---|---|
| t1 | external | "Findings would be demonstrated on synthetic/semi-synthetic corpora built from a limited set of LLM generator families and domains (e.g. RAID/HC3 text), and may not generalize to the full diversity of real-world contaminated corpora or to unseen generator models." | "Include multiple generator families (e.g. GPT-, Llama-, Claude-class) and multiple domains from RAID; report per-generator and per-domain breakdowns rather than a single pooled number." |
| t2 | construct | "The adversary 'budget' (tokens / API cost / fraction of documents rewritten) is a simplification of real adversarial cost, which also involves detection-of-evasion risk, latency, and coordination overhead not captured by a scalar budget." | "Report the scaling result under ≥2 distinct cost models (per-token vs. per-document-touched) and show the strategy-proofness conclusion's sign is invariant to the choice (C2)." |
| t3 | internal | "The core comparison (corpus estimator vs. single-document detector) may share the same underlying detection signal, so any robustness advantage could be an artifact of the specific aggregation method rather than a general property of corpus-level estimation." | "RQ_INF_2 directly tests this by comparing a naive-average estimator against two independent estimator families (mixture-MLE and debias-and-aggregate); report all three." |
| t4 | conclusion | "The scaling exponent β is estimated from a small range of corpus sizes N with limited seeds, so an apparent budget-grows-with-N trend could be statistical noise or a small-N artifact." | "Fit β by log-log regression with bootstrap 95% CIs and pre-register the one-sided test H₀: β ≤ 0; require the CI to exclude 0 before claiming a scaling effect." |
| t5 | scope | "The threat model is explicitly restricted to a budget-bounded, non-omniscient adversary (N6 unaddressed C4); a fully adaptive white-box adversary targeting the exact aggregation statistic is out of scope and could behave differently." | null |

- **Status:** `PARTIAL` — anticipated standard limitations for this class of study, not authors' own stated limitations.
- `absence_comment`: `{"what_missing": "No real Limitations/Threats-to-Validity section exists to extract from.", "why_matters": "Authors might identify different or additional threats once the study is designed and run.", "implication": "Use as an anticipatory design checklist, not a substitute for a real self-reported limitations section."}`

---

## N11 — Artifacts

**[PLACEHOLDER]** — nothing released because no paper/implementation exists yet.

- `artifacts`: `[]`
- `has_code`: `false`
- `has_data`: `false`
- `has_model`: `false`
- **Status:** `NOT_FOUND`
- `absence_comment`: `{"what_missing": "No code repository, dataset, model, or demo exists because this is a pre-paper research-idea seed.", "why_matters": "A reader cannot yet reproduce or build on this work.", "implication": "Revisit N11 only once an actual implementation and paper exist; do not infer artifacts from the N6 sketch."}`

---

## N12 — Contribution Type

- `value`: `"empirical"` **[HYPOTHESIS]**
- `rationale`: "The minimal experiment is a cost–accuracy game measured empirically between a
  simulated budget-bounded adversary and a corpus-level estimator across corpus sizes (N6's
  M4/M5), and N9's hypothesized results are quantitative measurements (proportion error,
  budget-to-bias-ε, scaling exponent β) that would be the paper's actual evidence. The object
  of study is measuring a phenomenon — whether evasion cost scales with corpus size — rather
  than proving a theorem (`theoretical`), releasing a benchmark as the primary artifact
  (`benchmark`/`dataset`), or shipping a deployable system (`system`/`tool`). The estimator in
  M2 is instrumental to the measurement, not marketed as the deliverable, so `empirical` fits
  better than `system`."
- `source`: `HYPOTHESIS`
- `absence_comment`: `{"what_missing": "No real paper exists to state its own contribution-type self-classification; this is the digest author's inference from the N6/N9 method-and-results shape, not an author statement.", "why_matters": "Contribution-type materially gates which archetype evidence standard (guidance.md Part 2) the eventual paper.md is held to; a wrong classification here would misdirect the whole evidence plan.", "implication": "Re-confirm N12 against the actual paper.md archetype declaration (Step 2) once written, and re-derive from the real paper's own framing if one is ever published."}`

---

## Claims

1. **[HYPOTHESIS]** "Corpus-level (population-scale) distributional estimation of AI-generated
   text is more robust to a budget-bounded paraphrasing adversary than single-document
   detection is, because aggregation averages out independent per-document evasion noise." —
   `evidence`: `[{"type": "argument", "text": "Derived from the seed's stated contrast between single-document fragility and hypothesized corpus-level robustness; grounded in the corpus-level mixture-MLE estimator of [MonitorAIScale, OpenReview:bX3J7ho18S] vs. the per-document detector [DetectGPT, OpenReview:UiAyIILXRd].", "source": "HYPOTHESIS", "location": null}]`
2. **[HYPOTHESIS]** "The minimum adversary budget to bias a corpus-level estimate by a fixed
   margin grows with corpus size N (fitted exponent β > 0), making large-scale evasion of
   aggregate estimates uneconomical even when per-document evasion stays cheap and effective."
   — `evidence`: `[{"type": "argument", "text": "The falsifiable scaling claim (RQ_INF_1) that must hold for the seed's 'reverses the pessimistic single-document conclusion' framing; the budget-optimizing adversary is instantiated after [AdaptiveWMAttack, OpenReview:AsODat0dkE].", "source": "HYPOTHESIS", "location": null}]`
3. **[HYPOTHESIS]** "Any measured robustness may be a property of aggregation *design* rather
   than of corpus-level estimation per se — a naive average-of-predictions estimator might not
   share it." — `evidence`: `[{"type": "argument", "text": "Motivates RQ_INF_2 and N10 t3; the two dedicated estimator families follow [MonitorAIScale, OpenReview:bX3J7ho18S] and [DUCI, OpenReview:EUSkm2sVJ6].", "source": "HYPOTHESIS", "location": null}]`
4. **[HYPOTHESIS]** "If a fully adaptive, estimator-aware (white-box) adversary is considered
   instead of a budget-bounded, non-omniscient one, the robustness advantage may not hold — the
   claim is conditional on a narrower threat model." — `evidence`: `[{"type": "argument", "text": "Follows from N6 unaddressed_challenges (C4) and N10 t5; the strategy-proofness-under-manipulation-budget framing is borrowed from [UCB-S, OpenReview:lsxeNvYqCj].", "source": "HYPOTHESIS", "location": null}]`
5. **[PLACEHOLDER]** "No quantitative evidence yet exists for any of the above — every numeric
   claim (error rates, scaling exponents, thresholds) is a directional placeholder for planning
   only and must not be treated as a reported finding." — `evidence`: `[{"type": "observation", "text": "N9 is NOT_FOUND/missing; N11 confirms no artifacts exist.", "source": "PLACEHOLDER", "location": null}]`

---

## Self-verification pass

- **V-01 (locator integrity):** No item is tagged `source="extracted"`/`status="FOUND"` on the
  basis of a nonexistent paper; the N3 works are real (`[GROUNDED:corpus]`) with resolvable
  `paper_url`s but `page=null` (OpenReview idea records carry no page anchors). Everything else
  is `[HYPOTHESIS]`/`[PLACEHOLDER]` and marked PARTIAL/NOT_FOUND.
- **V-04 (ID consistency):** checked —
  `N4.affects_works` ⊆ `N3.citation_key` = {`[MonitorAIScale, OpenReview:bX3J7ho18S]`,
  `[DetectGPT, OpenReview:UiAyIILXRd]`, `[AdaptiveWMAttack, OpenReview:AsODat0dkE]`,
  `[MarkovCalib, OpenReview:Lzwkeg2o2z]`, `[DUCI, OpenReview:EUSkm2sVJ6]`,
  `[AnchorPeerReview, OpenReview:HyZwf1rt4s]`, `[UCB-S, OpenReview:lsxeNvYqCj]`} (all 7 used,
  verbatim). `N6.challenge_arguments[].challenge_id` ⊆ {C1–C4}; `mechanism_components` ⊆
  {M1–M5}; `N6.unaddressed_challenges = ["C4"]` ⊆ {C1–C4}. `N8.addresses_challenges` ⊆ {C1–C4};
  `tests_contributions` ⊆ {CO1–CO4}; `evaluates_mechanisms` ⊆ {M1–M5}. `N9.rq_id` ∈ {RQ1,
  RQ_INF_1, RQ_INF_2} = `N8` ids. All resolve.
- **V-11 (empty nodes):** N11 NOT_FOUND with `artifacts=[]` and all three flags false; all of
  N0–N12 plus Claims present.
