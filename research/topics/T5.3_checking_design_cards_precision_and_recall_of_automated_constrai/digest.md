# Digest: Checking Design Cards: Precision and Recall of Automated Constraint Verification against Human Review

> **REVERSE PAPER-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet. This document
> projects an N0–N12 digest forward from an abstract research idea (topic code T5.3), as a
> planning aid. Every field is tagged `[GIVEN]` (verbatim/near-verbatim from the seed
> README), `[HYPOTHESIS]` (reasoned prediction, grounded in the seed + real literature —
> NOT a fact), or `[PLACEHOLDER]` (genuinely unknowable until the work is done — never
> invented). N3 entries drawn from the local OpenReview corpus are additionally tagged
> `[GROUNDED:corpus]`; two canonical software-engineering references that the corpus does
> not cover are tagged `[NON-CORPUS]`. Do not read any HYPOTHESIS or PLACEHOLDER content as
> a reported finding.

**Seed source:** `topics/T5.3_checking_design_cards_precision_and_recall_of_automated_constrai/README.md`
**Topic code:** T5.3 · **Label:** [证据] (Evidence) [GIVEN]
**Parent topic:** T5. 设计约束合规（coding agent）— "Design constraint compliance (coding agent)" [GIVEN]

---

## N0 — Metadata

- `title`: "Checking Design Cards: Precision and Recall of Automated Constraint Verification against Human Review" **[GIVEN]** (verbatim from seed README)
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — no paper, no authors exist yet.
- `abstract` **[HYPOTHESIS, drafted — not a real abstract]**:
  > "Coding agents increasingly produce patches that must comply with explicit design
  > constraints, expressed here as structured 'design cards.' We build a prototype automated
  > constraint verifier and evaluate it against a three-way alignment of design cards, agent
  > patches, and independent human review. We measure precision and recall of the automated
  > verifier relative to human judgments across constraint categories, and characterize which
  > kinds of constraints can be reliably automated versus which inherently require human
  > review. Our (hypothesized) findings suggest a split between structurally checkable
  > constraints, where automation performs comparably to human review, and semantically or
  > intent-laden constraints, where automated precision and/or recall degrades substantially."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"SE"` **[HYPOTHESIS]** — inferred from domain (coding agents, design constraint compliance, patch review are software-engineering-flavored; no explicit venue given).

**Status:** PARTIAL (title given, abstract/authors are placeholders/drafts, not real).

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS, built as a full predicate from the core question]**:
  "Measure the precision and recall of an automated constraint-verification prototype at
  detecting design-constraint violations in coding-agent-produced patches, relative to
  independent human review, in order to determine which categories of design constraints can
  be safely automated and which categories inherently require human judgment."
  - Kind of task: measurement / benchmarking study of a detection tool.
  - Domain: coding-agent-generated code patches checked against explicit design constraints.
  - Outcome shape: per-constraint-category precision/recall figures plus an
    automatable-vs-human-required categorization.

- `inputs` **[HYPOTHESIS, inferred from the minimal experiment]**:
  1. Design constraint cards (explicit, structured statements of design rules) [GIVEN — "约束卡" named directly in the minimal experiment]
  2. Coding-agent-produced patches (diffs) [GIVEN — "agent patch" named directly]
  3. Human reviewer judgments per (card, patch) pair [GIVEN — "人类评审" named directly]

- `outputs` **[HYPOTHESIS]**:
  1. Per-constraint-category precision/recall of the automated verifier vs. human review
  2. A classification of constraint types into "automatable" vs. "requires human review"

- `constraints` **[GIVEN — explicit in the seed's minimal experiment]**:
  "Ground truth is established via three-way alignment: constraint cards + agent patch +
  human review (三方对齐评测) — i.e., no single source (card text alone, verifier output
  alone) is treated as sufficient ground truth; separability of automatable vs.
  human-required constraints is judged against this three-way alignment."

---

## N2 — Motivation

**[HYPOTHESIS — reconstructed from parent-topic framing, no invented statistics]**

- `motivation_text`: "The parent topic (T5, '设计约束合规（coding agent）' — design
  constraint compliance for coding agents) frames a broader concern: as coding agents
  autonomously produce patches at a pace and volume that outstrips manual review capacity,
  teams need some form of automated gate-keeping to check that agent output respects
  explicit design constraints (architectural boundaries, style/naming rules, security
  invariants, etc.). If an automated constraint verifier's precision/recall against human
  judgment is unknown, teams cannot tell whether relying on it is safe (silent violations
  slipping through, i.e. false negatives) or costly (reviewer fatigue from false positives).
  This topic exists to put a number on that gap and to identify which constraint types are
  inherently unautomatable, so that human review effort can be targeted where it is actually
  needed rather than spread uniformly across all constraints." — `source="inferred"`,
  `evidence=[]` (no paper exists to cite evidence from).

---

## N3 — Related Works

**Corpus search performed** over `topics/corpus/ideas.jsonl` (11,683 OpenReview papers)
with the provided keyword tool, across five angles: (1) `constraint; verifier;
verification; code`, (2) `static analysis; code review; false positive`, (3) `llm judge;
human agreement; evaluation; alignment with human`, (4) `coding agent; patch; software
engineering; SWE-bench`, (5) `instruction following; constraints; checklist; rubric;
verifiable`. Seven entries below resolve to real corpus papers (`[GROUNDED:corpus]`, keyed
`[ShortName, OpenReview:paper_id]`). This is an SE-flavored topic and the corpus skews
ML/LLM; two canonical SE references the corpus does not cover are kept and clearly marked
`[NON-CORPUS]`. Relevance framing to T5.3 is my synthesis (`source="inferred"`); the
papers' existence is not.

| citation_key | approach_summary | source |
|---|---|---|
| **[DefectReview, OpenReview:mEV0nvHcK3]** — "Towards Practical Defect-Focused Automated Code Review" | Reframes automated code review around merge requests and key-bug detection instead of isolated comment generation; combines static code slicing for dependency-aware context with a multi-role LLM pipeline that explicitly balances coverage (recall) and precision via validation + filtering. Reports that on prior benchmarks fewer than 10% of comments are truly high quality. The closest corpus analog to "automated checker on agent-produced diffs, measured for precision vs coverage." | [GROUNDED:corpus] |
| **[TrustOrEscalate, OpenReview:UHPnqSTBPO]** — "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement" | Frames LLM-based evaluation as selective prediction: the judge answers only when its estimated human-agreement confidence exceeds a threshold calibrated (learn-then-test) on a small human-labeled set, and escalates uncertain cases through a cascade of stronger judges, yielding a bounded disagreement risk. Directly relevant to operationalizing "automated verifier vs human review" with a calibrated precision floor. | [GROUNDED:corpus] |
| **[RLCF-Checklists, OpenReview:RPRqKhjrr6]** — "Checklists Are Better Than Reward Models For Aligning Language Models" | Decomposes an instruction into a checklist of atomic yes/no requirements and scores each item with the most reliable available mechanism, arguing that global/monolithic rubrics miss instruction-specific requirements. Provides a concrete template for turning a "design card" into a set of item-level, separately-checkable predicates. | [GROUNDED:corpus] |
| **[RECAST, OpenReview:90tCp2KszA]** — "RECAST: Expanding the Boundaries of LLMs' Complex Instruction Following with Multi-Constraint Data" | Synthesizes multi-constraint instructions and pairs each constraint with a validation mechanism (rule-based or model-based), showing LLM constraint-satisfaction degrades as the number of simultaneous constraints grows. Establishes that per-constraint verifiability varies by constraint type — the empirical premise behind T5.3's automatable-vs-human split. | [GROUNDED:corpus] |
| **[SWE-bench, OpenReview:VTF8yNQM66]** — "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" | Execution-verified benchmark pairing GitHub issues with resolving pull requests, using fail-to-pass tests as an objective correctness oracle over repository-scale code edits. The canonical source of realistic coding-agent patches and the reference for what "objectively/executably checkable" means (a subset of the constraint spectrum T5.3 studies). | [GROUNDED:corpus] |
| **[SWE-RM, OpenReview:H9wMe1G76j]** — "SWE-RM: Execution-free Feedback for Software Engineering Agents" | Trains an execution-free reward model that scores full SE-agent trajectories, motivated by test suites being incomplete, noisy, or misaligned so execution outcomes alone are insufficient supervision. Grounds the claim that many design constraints cannot be reduced to a passing test and need a non-execution judge. | [GROUNDED:corpus] |
| **[VerifDynamics, OpenReview:DcEuBwrWnB]** — "Variation in Verification: Understanding Verification Dynamics in Large Language Models" | Treats verification as a capability distinct from generation and empirically disentangles problem difficulty, generator capability, and verifier capability, showing verification quality does not scale simply with model size. Warns that a single aggregate accuracy number hides strong per-regime variation — motivating T5.3's per-category precision/recall reporting. | [GROUNDED:corpus] |
| **[ReflexionModel, Murphy et al., 2001]** — "Software Reflexion Models: Bridging the Gap between Design and Implementation," IEEE TSE 27(4) | Classic architecture-conformance technique: developers specify a high-level model and a mapping to source, and a tool computes convergences/divergences/absences between the intended and as-built structure — the canonical "structural design constraint, automatically checkable" archetype. Corpus lacks a direct architecture-conformance entry. | [NON-CORPUS] |
| **[Johnson et al., 2013]** — "Why Don't Software Developers Use Static Analysis Tools to Find Bugs?," ICSE 2013 | Interview study finding that false positives and poor result presentation are the dominant reasons developers abandon static analysis tools, establishing that precision (not just recall) governs whether an automated checker is usable in practice. Corpus lacks a dedicated static-analysis-adoption entry. | [NON-CORPUS] |

**Status:** FOUND (9 works; within the 5–10 target). Seven are real corpus papers (id
resolvable in `ideas.jsonl`); two are clearly-marked canonical SE references.

---

## N4 — Prior Limitations

**[HYPOTHESIS — what the N3 works do NOT cover relative to T5.3's core question, each tied to N3 citation_key(s); defensible from each cited work's own motivation/method]**

| id | limitation_text | affects_works | limitation_type |
|---|---|---|---|
| L1 | Defect-focused automated review is optimized and measured for catching *bugs* on merge requests and balances precision/coverage against a defect oracle, not against a *taxonomy of explicit design constraints* with a per-category precision/recall protocol; it therefore leaves open how automation performs across heterogeneous constraint types (structural vs style vs intent). | [DefectReview, OpenReview:mEV0nvHcK3] | generalizability |
| L2 | The selective-judge framework bounds *aggregate* disagreement with humans via a calibrated confidence threshold, but does not decompose where the abstentions concentrate by constraint type — so it cannot say *which categories* of design constraint the automated judge can vs cannot safely rule on, which is exactly T5.3's second question. | [TrustOrEscalate, OpenReview:UHPnqSTBPO] | precision |
| L3 | Checklist- and multi-constraint-following work assumes constraints are already reducible to atomic yes/no items with a reliable per-item checker, and studies constraint *satisfaction by a generator*, not the *detection precision/recall of a verifier* against human-labeled violations on real code diffs. | [RLCF-Checklists, OpenReview:RPRqKhjrr6], [RECAST, OpenReview:90tCp2KszA] | precision |
| L4 | Execution-based (SWE-bench) and execution-free (SWE-RM) SE evaluation both target end-to-end *task resolution / trajectory quality* judged by tests or a reward model; neither measures how well an automated checker matches *human review* on a fixed, explicit constraint per patch, and SWE-bench's oracle only covers the executably-testable slice of constraints. | [SWE-bench, OpenReview:VTF8yNQM66], [SWE-RM, OpenReview:H9wMe1G76j] | recall |
| L5 | Verification-dynamics analysis shows verifier quality varies with difficulty/generator/verifier but is studied on math/reasoning correctness with automatic ground truth, not on design-constraint compliance where the "ground truth" is itself noisy human review — leaving the human-review noise ceiling unquantified. | [VerifDynamics, OpenReview:DcEuBwrWnB] | generalizability |
| L6 | Reflexion models and static-analysis adoption studies establish that *structural* constraints are automatable and that *false positives* drive tool abandonment, but predate coding agents and give no evidence on semantic/intent-level design constraints or on agent-generated patches specifically. | [ReflexionModel, Murphy et al., 2001], [Johnson et al., 2013] | generalizability |

`grounding_check`: **true** — every limitation cites at least one N3 `citation_key`, each string matching N3 verbatim.

---

## N5 — Challenges

**[HYPOTHESIS, tightly derived from the core question — problem-inherent, not tied to any single prior tool's failure; N4-vs-N5 test applied]**

| id | text |
|---|---|
| C1 | Design constraints vary intrinsically in operationalizability: some are objectively checkable by rule/structure (e.g., "must not call API X," "layer A must not import layer B"), others require semantic or contextual judgment (e.g., "preserve separation of concerns"). Any single verifier design will not generalize evenly across this spectrum, so an aggregate accuracy number is uninformative. |
| C2 | "Human review" is not a noise-free gold standard: reviewers can disagree on whether a given patch violates a given card, so the ground truth against which the verifier is scored carries irreducible uncertainty that caps the achievable agreement for *any* automated checker. |
| C3 | An agent patch can satisfy a constraint's literal text while violating its intent (or vice versa); correctly judging a violation requires reasoning about the design intent behind a card, not surface pattern-matching against its wording. |
| C4 | Precision and recall trade off for any verifier: tuning for high recall inflates false positives and reviewer burden (the documented cause of tool abandonment), while tuning for high precision silently misses real violations. The acceptable operating point is itself constraint-type-dependent. |

`conflation_check`: **true** — the four challenges target distinct obstacles (operationalizability spectrum, ground-truth noise, intent-vs-literal, precision/recall trade-off) with no near-duplicates merged.

---

## N6 — Methodology

**[HYPOTHESIS — extrapolated from the one-sentence minimal experiment: "约束卡 + agent patch + 人类评审三方对齐评测" / "constraint cards + agent patches + human review three-way alignment evaluation"]**

### `overview`
"The (hypothesized) study builds a constraint-verifier prototype that ingests explicit
design constraint cards alongside coding-agent-produced patches, decomposes each card into
item-level checkable predicates, applies a hybrid of mechanisms (rule/AST checks, an
architecture-conformance check, and an LLM-as-judge with calibrated abstention) to output a
violation / no-violation judgment per (card, patch) pair, and compares those judgments
against an independently collected human-review ground truth over the same pairs. Precision,
recall, F1 and human-agreement (Cohen's κ) are computed *per constraint category*, and
categories are bucketed into 'reliably-automatable' vs 'human-required.' **Staged plan —
Stage 1 (pilot = the seed's minimal experiment):** a small three-way-aligned set (design
cards + agent patches + human review) sized for one saturated annotation round, establishing
the protocol, inter-rater agreement, and a first per-category precision/recall reading.
**Stage 2 (scale-up):** expand card taxonomy coverage and patch volume (multiple agents,
multiple repositories), add the calibrated-abstention and static-analysis baselines, and
run the pre-registered statistical comparison." — `source="inferred"`

### `key_components`
| id | name | text |
|---|---|---|
| M1 | Design Card Corpus & taxonomy | A curated set of explicit design constraint cards, each labeled with a category (structural/architectural boundary, naming/style rule, security invariant, API-usage restriction, intent-level design principle) and decomposed into item-level yes/no predicates in the style of [RLCF-Checklists, OpenReview:RPRqKhjrr6]. Granularity: one card = one constraint; measured attribute = category + predicate list. |
| M2 | Agent Patch Corpus | Diffs produced by ≥2 coding agents on tasks scoped under the cards, seeded from SWE-bench-style issue→PR pairs [SWE-bench, OpenReview:VTF8yNQM66], deliberately balanced to include both compliant and violating patches per category. Instrument: git diff + task metadata; granularity = one (card, patch) pair per verdict. |
| M3 | Automated Constraint Verifier (prototype) | The core instrument: a hybrid checker emitting a violation/no-violation label per (card, patch) pair. Sub-mechanisms — (a) rule/AST matcher for API/naming constraints, (b) reflexion-model-style architecture-conformance checker for structural constraints [ReflexionModel, Murphy et al., 2001], (c) LLM-as-judge with confidence-calibrated abstention/escalation [TrustOrEscalate, OpenReview:UHPnqSTBPO] for intent-level constraints. Measured output: label + confidence per pair. |
| M4 | Human Review Panel & adjudication | ≥3 independent reviewers label each (card, patch) pair (violation/no-violation + rationale); disagreements adjudicated; inter-rater agreement (Fleiss' κ) recorded as the ground-truth-noise ceiling. Granularity = per pair, per reviewer. |
| M5 | Three-Way Alignment Analysis | The comparison layer: computes per-category precision, recall, F1, and verifier-vs-human Cohen's κ of M3 against the adjudicated M4 labels; derives the automatable-vs-human-required bucketing by testing whether per-category verifier–human agreement is statistically indistinguishable from human–human agreement. |

### `challenge_arguments`
| challenge_id | argument_text | mechanism_components |
|---|---|---|
| C1 | "By categorizing cards and decomposing them into item-level predicates (M1) and computing precision/recall *separately per category* (M5), the study surfaces which categories the verifier handles well vs poorly instead of one aggregate number that would hide the variation flagged by [VerifDynamics, OpenReview:DcEuBwrWnB]." | [M1, M5] |
| C2 | "Using a ≥3-reviewer panel with adjudication and an explicitly recorded inter-rater agreement (M4) both reduces idiosyncratic reviewer noise and *quantifies the residual ceiling*, so the verifier's agreement can be judged relative to human–human agreement rather than against an assumed-perfect oracle." | [M4] |
| C3 | "Intent-level constraints are routed to an LLM-as-judge sub-mechanism (M3c) that reasons jointly over card semantics and patch content, with calibrated abstention so it declines rather than guesses on low-confidence intent judgments — a partial, explicitly-imperfect mitigation for literal-vs-intent mismatch." | [M3] |
| C4 | "Reporting precision and recall separately per category, plus a confidence-thresholded operating curve (M5), makes the precision/recall trade-off visible per constraint type — directly addressing the false-positive-driven abandonment risk documented by [Johnson et al., 2013]." | [M5] |

### `unaddressed_challenges`
`["C2"]` — **[HYPOTHESIS, flagged]**: M4 *measures* inter-rater agreement, but if reviewers
disagree substantially the human-review ground truth is itself shaky and the per-category
precision/recall numbers inherit that noise; the methodology bounds but cannot eliminate
this. This rests on an inferred methodology sketch (`source="inferred"`), not an extracted
one — flagged explicitly to avoid confidence inflation.

### Feasibility
**Order-of-magnitude effort (Stage 1 pilot):** ~5 constraint categories × ~10 cards ≈ 50
cards; ~4 agent patches/card ≈ 200 (card, patch) pairs; 3 reviewers × 200 pairs ≈ 600 human
labels at ~2 min/label ≈ **20 annotator-hours** plus adjudication. Verifier runs: 200 pairs
× 3 sub-mechanisms, LLM-judge at a few calls/pair ≈ **low thousands of API calls** (cost
class: tens of USD on a mid-tier model). No GPU training required — the LLM-judge is
inference-only. **Stage 2 scale-up** roughly 5–10× the pairs and reviewer-hours; still
inference-only, cost class low-hundreds USD. **Biggest feasibility risk:** constructing a
*balanced, non-trivial* patch corpus where violations are neither obvious nor absent per
category — a corpus too easy inflates all numbers and hides the automatable-vs-human split.
**Mitigation:** seed patches from real SWE-bench issue→PR pairs and have the human panel
pre-screen difficulty, discarding trivially-compliant pairs before scoring.

---

## N7 — Contributions

**[HYPOTHESIS — what such a paper would claim, framed from the method + expected findings]**

| id | text | contribution_type | is_testable | has_rq |
|---|---|---|---|---|
| CO1 | A constraint-verifier prototype that checks coding-agent-produced patches against explicit, category-labeled design cards via a hybrid rule/conformance/LLM-judge pipeline. | tool | true | true |
| CO2 | An empirical measurement of the verifier's per-constraint-category precision and recall relative to adjudicated human review, benchmarked against the human–human agreement ceiling. | empirical_finding | true | true |
| CO3 | A categorization of design-constraint types into automatable vs inherently-human-required, operationalized as a statistical test of verifier–human vs human–human agreement per category. | conceptual_framework | true | true |
| CO4 | A three-way aligned corpus (design cards × agent patches × adjudicated human labels) reusable as a benchmark for future constraint-verifier work. | dataset | true | false |

---

## N8 — Research Questions

- **RQ1** **[GIVEN — near-verbatim restatement of the seed's core question, first half]**:
  "Given explicit design constraint cards, what is the precision/recall of an automated
  checker at catching violations in coding-agent patches, relative to human review?"
  - `rq_source`: "explicit"
  - `evaluates_mechanisms`: [M3, M5]
  - `addresses_challenges`: [C1, C4]
  - `tests_contributions`: [CO1, CO2]
  - `answered_by_experiment`: "Three-way alignment: run M3 on every (card, patch) pair; treat adjudicated M4 labels as reference; report per-category precision/recall/F1 and verifier–human Cohen's κ. Compare the hybrid verifier against baselines with McNemar's test on paired violation/no-violation decisions."

- **RQ2** **[GIVEN — near-verbatim restatement of the seed's core question, second half]**:
  "Which categories of constraints can be automated, and which inherently require human
  review?"
  - `rq_source`: "explicit"
  - `evaluates_mechanisms`: [M1, M5]
  - `addresses_challenges`: [C1, C2]
  - `tests_contributions`: [CO3]
  - `answered_by_experiment`: "Per category, test whether verifier–human agreement (Cohen's κ) is statistically indistinguishable from human–human agreement (Fleiss' κ from M4) via bootstrap CI overlap; a category is 'automatable' iff the verifier reaches the human-agreement band, else 'human-required.'"

- `datasets` **[HYPOTHESIS]**: `names=["Constructed design-card corpus (category-labeled, item-decomposed)", "SWE-bench / SWE-bench Verified issue→PR patches (source of realistic agent patches)", "Constructed violating-patch variants per card category"]`
- `baselines` **[HYPOTHESIS]**: `names=["Naive regex/keyword constraint matcher", "AST/reflexion-model structural conformance checker (structural constraints only)", "Single-shot LLM-as-judge (no abstention)", "Calibrated selective LLM-judge (Trust-or-Escalate style)"]`
- `metrics` **[HYPOTHESIS]**: `names=["Precision (per category)", "Recall (per category)", "F1 (per category)", "Verifier–human Cohen's κ", "Human–human Fleiss' κ (ceiling)", "Matthews Correlation Coefficient"]`
- **Analysis plan [HYPOTHESIS]:** Stage-2 target ≥ 1,000 (card, patch) pairs (≥ ~150/category, ≥ ~30 violations/category for stable recall CIs). Paired significance via McNemar's test on verifier-vs-baseline decisions, α = 0.05, Holm correction across categories. Effect direction expected: verifier–human κ ≈ human–human κ on structural/API/naming categories (no significant gap); verifier–human κ significantly below the ceiling on intent-level/design-principle categories.

---

## N9 — Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY. No real numbers exist. `evidence_strength="missing"` and `rq_answered=false` for every entry by construction — the study has not been run.]**

| rq_id | result_text (hypothesized direction) | result_type | evidence_strength | rq_answered |
|---|---|---|---|---|
| RQ1 | "The verifier is predicted to reach precision/recall statistically indistinguishable from human review on structurally/syntactically checkable constraints (forbidden APIs, naming, layer-import boundaries), but substantially lower recall — and possibly lower precision — on semantically/intent-laden constraints (separation-of-concerns, design-intent rules)." | quantitative | missing | false |
| RQ2 | "A minority of categories (the structurally checkable ones) will be classified 'automatable' (verifier–human κ within the human–human band); the majority requiring semantic/design-intent judgment will be classified 'human-required.'" | quantitative | missing | false |

**Falsification conditions [HYPOTHESIS]:**
- **RQ1 refuted if:** verifier precision/recall is statistically indistinguishable *across* syntactic and semantic categories — i.e., uniformly high or uniformly low rather than split (no significant category × verifier interaction at α = 0.05).
- **RQ2 refuted if:** the majority (not minority) of categories reach the human–human agreement band — automation covers most constraint types rather than only the structurally checkable subset. Also refuted if *no* category, including structural ones, reaches the human-agreement band (would indict the verifier construct, not the automatable/human split).

---

## N10 — Threats / Self-Limitations

**[HYPOTHESIS — anticipated limitations of this kind of study; no paper exists to state these itself]**

| threat_id | category | description | mitigation |
|---|---|---|---|
| t1 | construct | "Human review" is the reference, but reviewer disagreement, fatigue, or inconsistent card application biases the measured precision/recall — the "human review = correct" construct is not guaranteed. | Use ≥3 reviewers with adjudication; report Fleiss' κ as an explicit ceiling (M4); score verifier agreement relative to that ceiling, not against an assumed-perfect oracle. |
| t2 | external | Findings likely derive from a few coding-agent models and a limited set of repos/languages; the automatable-vs-human categorization may not transfer to other agents, languages, or domains. | Use ≥2 agents and multi-repo SWE-bench-sourced patches; pre-register the category taxonomy; report per-category results so transfer can be assessed category-by-category. |
| t3 | internal | If the same team authors the cards, curates which patches enter the corpus, and builds the verifier, selection/confirmation bias can inflate agreement. | Separate card-authoring, patch-curation, and verifier-building roles; pre-screen patch difficulty with the human panel before scoring; seed patches from real issue→PR pairs. |
| t4 | conclusion | Per-category recall CIs can be wide when violations per category are few, risking over-reading a null result as "automatable." | Power the design for ≥30 violations/category; use bootstrap CIs and Holm-corrected McNemar tests; treat under-powered categories as "inconclusive," not "automatable." |
| t5 | reproducibility | If the LLM-judge relies on a closed/proprietary model, precision/recall may not reproduce as the model is updated or deprecated. | Pin model versions; report at least one open-weight LLM-judge; release the corpus and prompts (CO4). |

**Status:** NOT_FOUND (no author-stated Threats section exists yet — these are anticipated).
`absence_comment`: `what_missing`: "No paper, hence no authors'-own Limitations/Threats-to-Validity section, exists yet." `why_matters`: "A reader cannot distinguish which limitations the future authors would acknowledge versus reviewer-raised ones." `implication`: "Treat every threat above as a reviewer-anticipated risk for the eventual study design, not a confirmed self-report."

---

## N11 — Artifacts

**[PLACEHOLDER — nothing has been released; the paper does not exist]**

`artifacts`: `[]`
`has_code`: `false`
`has_data`: `false`
`has_model`: `false`

**Status:** NOT_FOUND. `absence_comment`: `what_missing`: "No code repository, dataset, model, or demo has been released, because no study has been conducted yet." `why_matters`: "Reproducibility and follow-on benchmarking depend entirely on whether the eventual design-card corpus, agent-patch corpus, and verifier prototype are released — and CO1/CO4 explicitly hypothesize a tool and a dataset as contributions." `implication`: "Any future actual paper on this topic should be checked for artifact release as a first-class deliverable."

---

## N12 — Contribution Type

- `value`: **`empirical`** **[HYPOTHESIS]**
- `rationale`: "The core question and minimal experiment center on *measuring* precision and
  recall of an automated checker against human review and on *characterizing* which
  constraint categories resist automation — what N9's results would validate is a set of
  per-category precision/recall statistics plus a statistical automatable-vs-human split,
  analogous to how [VerifDynamics, OpenReview:DcEuBwrWnB] is a measurement study of an
  existing capability even though it uses concrete models as instruments, and how
  [Johnson et al., 2013] is an empirical study despite being about tools. The verifier
  prototype (M3) is built as the *instrument* for the measurement, not framed in the seed as
  the headline downloadable deliverable; the question is 'how good is automated checking, and
  which constraint types resist it,' not 'here is a tool, use it.' This tips the whole-paper
  classification to `empirical` over `tool` — with `tool` (CO1) the closest runner-up if a
  future draft foregrounds the released verifier, and `benchmark` (CO4) a secondary
  possibility if the three-way corpus becomes the headline artifact."

---

## Claims

**[Each tagged HYPOTHESIS or PLACEHOLDER — no real claims exist yet]**

1. **[HYPOTHESIS]** "Automated constraint verification will show a real, measurable
   precision/recall gap relative to human review, with the gap concentrated in
   semantically-defined constraint categories rather than structural ones — operationalized
   as verifier–human κ falling below the human–human band only on intent-level categories."
   — evidence: none yet (type="argument", source="inferred", location=null — prospective).
2. **[HYPOTHESIS]** "The three-way alignment treats human review as ground truth, but human
   review itself carries irreducible disagreement (Fleiss' κ < 1) that caps the achievable
   agreement ceiling for any automated checker; measuring and reporting that ceiling is what
   makes the precision/recall numbers interpretable." — evidence: none yet.
3. **[HYPOTHESIS]** "Some subset of design constraints is inherently non-automatable — the
   automatable/human-required split is a property of the constraint type (its
   operationalizability), not merely of verifier engineering effort." — evidence: none yet.
4. **[HYPOTHESIS]** "False positives, not just false negatives, govern whether the verifier
   is adoptable: per the static-analysis-adoption literature, high recall bought with low
   precision is self-defeating, so the study reports a per-category operating curve rather
   than a single blended accuracy." — evidence: none yet ([Johnson et al., 2013] cited as
   the grounding, not as a result of this study).
5. **[PLACEHOLDER]** "No numeric precision/recall values, no constructed design-card corpus,
   and no released artifacts exist yet — every quantitative figure in this digest is a
   directional prediction pending the actual study, not a reported finding." — this claim
   exists to prevent this digest from being mis-cited as containing real results.
