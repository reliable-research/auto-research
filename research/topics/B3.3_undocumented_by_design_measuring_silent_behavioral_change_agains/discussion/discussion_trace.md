# Discussion Trace — B3.3 (Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs)

> Complete round-by-round record of the `auto-research-discussion` 6-stage critic/refiner loop for this topic — every draft version, every critique (comments + severities + resolution), every decision, and every refiner pass, across Stage 1 (Problem Definition) through Stage 6 (Experiment Design), plus the final cross-stage consistency check. Extracted verbatim from `pipeline.md` (previously inline there) per the `auto-research-discussion` skill's updated "Final deliverables" spec (three separate output files: `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). Mode: **autoclaude** (self-play, Claude as student+teacher). Source seed: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9). Round cap: 5/stage (none hit) — all six stages converged in 1 critic round + 1 refiner pass each.
>
> This content originally lived inline in `discussion/pipeline.md`; that file now carries only a one-line pointer to this file plus the `goal.md`-schema Phase Log (phase-gate tracking, distinct from this stage-transcript trace). See `experiment_design.md` for the standalone Stage 6 spec, and `paper_draft.md` for the assembled paper.

---


## Seed brief

- **One-sentence description:** Measure what fraction of statistically-detectable cross-version behavioral changes in a deployed AI system (e.g., an LLM API) are absent from the vendor's own changelog, and identify which behavior categories concentrate this "silent" change.
- **Apparent inputs:** paired pre/post-update API snapshots; the vendor's changelog/release-note text for that version transition; a fixed, category-stratified battery of behavioral probes.
- **Apparent outputs:** a per-probe genuine-diff flag; a per-probe documented/silent label; a per-category and overall silent-change rate with uncertainty bounds; a ranked taxonomy of which categories concentrate silent change.
- **Closest research areas:** black-box LLM API auditing / model-equality testing (LogProbTracking, RankUniformity); relational fairness audits across model releases (BiasSimilarity); technical AI-governance capability gaps (TAIG); longitudinal behavioral-drift measurement (Chen, Zaharia & Zou 2023).
- **In scope:** externally measuring documentation fidelity for versioned, black-box AI APIs using probe suites the auditor controls. **Out of scope:** building or training a new model; recovering the vendor's true/complete changelist (no such ground truth is obtainable); live enforcement or legal remedies.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already carries its own asymmetry/taste self-check (`paper.md` Steps 0/3) and its own formal notation (`paper.md` Step 5) and pre-registered hypotheses/fallbacks (Step 6). Reconstruction risk is low; the risk is redundancy with `paper.md`'s own Step 5/6 — so Stage 5/6 below are framed as decomposing and stress-testing the measurement instrument's individual properties (signal-vs-noise separation, alignment validity, category-taxonomy construct validity, boundary attribution, coverage stability), rather than re-deriving `paper.md`'s three headline hypotheses (H1–H3) from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given paired pre/post-update snapshots of a deployed AI system (e.g., an LLM API) and the vendor's changelog/release-note text covering that version transition, determine what proportion of the system's statistically-detectable behavioral changes have no corresponding entry in the vendor's own changelog, and in which behavioral categories these undocumented ("silent") changes concentrate.
- `input`: (1) two API snapshots of the same system pinned to a version transition; (2) the vendor's changelog/release-note text for that transition; (3) a fixed, category-stratified battery of behavioral probes run identically against both snapshots.
- `output`: (1) a per-probe genuine-change flag, separating real cross-version diffs from same-version sampling noise; (2) a per-probe documented/silent label produced by aligning each flagged diff against the changelog's claims; (3) a per-category and overall silent-change rate with uncertainty bounds; (4) a ranked taxonomy of which behavioral categories concentrate silent change.
- `constraints`: version transitions must be attributable to a bounded release window even though many vendors do not publish clean version-boundary dates for rolling/API-served deployments; the same-version sampling distribution must be independently estimable so a genuine cross-version diff can be separated from ordinary output stochasticity; the vendor's changelog text is treated as the documentation-of-record to align measured diffs against.
- `objective`: a documented-vs-silent classification, and the resulting silent-change rate, is correct if it matches the joint outcome of the diff-detector (genuine-change flag) and the changelog-alignment procedure (documented/silent label).
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 already settles this as a measurement/characterization study ("the headline deliverable is a rate and category-distribution... with the probe+alignment pipeline as instrumentation"), and the seed's own core question ("有多大比例未出现在厂商变更说明里") asks for a proportion, not a proposed fix.

**critique:**
- summary: Strong draft, evidence-traceable to the seed and to `paper.md`'s own Step 5 notation, but the objective has a real evaluability gap, and one pair of terms is used inconsistently.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective says a classification is 'correct' if it matches the pipeline's own output, which is circular unless it also states what the resulting *rate* is a claim about. Digest N5's own C3 and paper.md's Step-5 'lower bound' row and Assumption A6 are explicit that no ground truth of 'all actual changes' in a release exists — so the measured silent-change rate is a coverage-conditioned lower bound, not the true rate. An objective that doesn't say this as part of what counts as a correct answer risks reading as if the pipeline recovers the true rate, which nothing in the seed material supports and which C3 explicitly rules out."}`
  - `{severity: minor, field: "summary/input", anti_pattern: null, comment: "'statistically-detectable behavioral changes' (summary) and 'genuine-change flag' (output item 1) are describing the same construct with two different terms across the same paragraph — pick one term and use it consistently, or the reader has to infer they're the same thing."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in `paper.md`'s Step 5 and Assumptions — no new content needed).

### Refiner pass

- `objective` (refined): "A documented-vs-silent classification is accepted only relative to a stated probe suite and changelog corpus; the resulting silent-change rate is reported and evaluated as a **coverage-conditioned lower bound** on the true rate, not as a point estimate of it — no experiment can certify the true rate, because no independent record of 'all actual changes' in a release exists (paper.md A6). A rate estimate is judged correct only if it is *stable* under variation of the probe subset used to compute it, which is the closest checkable proxy this design can offer for 'not an artifact of an arbitrary probe list.'"
- `summary`/`output` (refined): standardized on "detected diff" as the one term for a probe flagged as showing a genuine (non-noise) cross-version change; "silent" reserved exclusively for the documented/silent label.
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md`'s own Step-5 notation): "Versions $v_t, v_{t+1}$; probe suite $P=\{p_1,\dots,p_M\}$ with category map $c(p_i)\in\mathcal{C}$; samples $S_{p,v}$. $D(p)=1$ iff a within-version-null-corrected two-sample test flags $p$ as changed. Changelog claims $\mathcal{K}=\{k_1,\dots,k_R\}$ for the transition. $\mathrm{Doc}(p)=1$ iff some $k\in\mathcal{K}$ entails $p$'s diff; $\mathrm{Silent}(p) = D(p)\wedge\neg\mathrm{Doc}(p)$. Report $\rho = \frac{\sum_p \mathrm{Silent}(p)}{\sum_p D(p)}$ and $\rho_c$ per category $c$, as lower bounds conditioned on $P$."
- `changes_made`: tightened objective's evaluability condition to state the lower-bound framing explicitly; standardized terminology between summary and output; added formal_summary.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: The party that controls when a deployed AI system changes is also the sole author of the record of what changed, so external, reproducible measurement is the only way to bound how much that record omits — and no one has actually run this measurement.
- `why_it_matters`: Integrators, auditors, and regulators who rely on vendor changelogs as a complete record of behavioral change have no independent way to check that assumption; if a substantial share of real behavioral change is silent, any accountability process built on "the changelog says what changed" silently inherits an unverifiable gap. This is not a hypothetical concern — the changelog's author and the party whose incentives govern what gets disclosed are the same party, a structural conflict of interest with no natural correction mechanism (digest README: "厂商结构性不会自己做" — vendors will not structurally do this themselves).
- `who_cares`: Downstream integrators whose applications depend on stable behavior between releases; third-party auditors and regulators implementing "ongoing monitoring" mandates (per `[TAIG, OpenReview:Be2B6f0ps1]`'s own catalog of governance requirements current tooling cannot yet satisfy); researchers deciding whether existing black-box audit tools already solve this or only adjacent problems.
- `evidence`: `[LogProbTracking, OpenReview:hFxivbAgVP]`'s own motivation frames its problem as continuous *change detection*, not documentation-fidelity measurement; `[RankUniformity, OpenReview:PSIe9mmF7a]`'s own motivation is *model-substitution* detection against a trusted reference, not changelog alignment; `[Chen, Zaharia & Zou, 2023]` (arXiv:2307.09009) directly demonstrates substantial behavioral drift between two dated GPT-3.5/GPT-4 snapshots without ever cross-referencing OpenAI's own release notes — itself evidence that the alignment step this paper proposes has not been done, even by the closest existing precedent.

**critique:**
- summary: Grounded, real citations, correctly distinguishes the paper's gap from its nearest neighbors — but the motivation covers only the headline rate, not the taxonomy output Stage 1 also promised.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's output (4) is a *ranked taxonomy of which behavioral categories concentrate silent change* — a claim about structure, not just prevalence. why_it_matters motivates why a silent-change rate matters at all, but never explains why the category breakdown specifically matters, as opposed to just reporting one aggregate percentage. A reader could reasonably ask: 'if the overall rate is what's actionable, why build a whole category taxonomy?' — that question is currently unanswered."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, an aggregate rate alone tells an integrator or regulator *that* silence is common but not *where to look*. A auditor with finite attention has to decide which behavior categories to monitor most closely between releases; a category-level taxonomy is what turns 'undocumented change happens' into an actionable prioritization (e.g., 'safety-relevant behavior is disproportionately silent, so audit that category on every release even when the changelog says nothing'), which a single pooled percentage cannot support."
- `changes_made`: added the category-level actionability argument, closing the output-coverage gap.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each at the approach + limitation level (`approach_summary` fields present for all nine); per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_logprobtracking` | Anon., LogProbTracking (OpenReview:hFxivbAgVP) | **true** | Detects THAT an endpoint's response distribution shifted via a nonparametric two-sample test on first-token top-k logprobs, but never attributes the shift to a behavior category or aligns it to changelog text — a bare change signal, not a documented/silent label. |
| `rw_rankuniformity` | Anon., RankUniformity (OpenReview:PSIe9mmF7a) | **true** | Answers a binary "is the served model the same as a trusted local reference?" via rank-uniformity testing; requires a fully accessible reference distribution and never operates over vendor-published documentation. |
| `rw_biassimilarity` | Anon., BiasSimilarity (OpenReview:EveruzAsGI) | false (construct-mismatched) | Measures whether a tuned release departs from its base model, but confined to the fairness/stereotype construct (BBQ/UNQOVER) via pairwise similarity; doesn't span general behavior categories or cross-reference any vendor disclosure. |
| `rw_taig` | Reuel et al., TAIG (OpenReview:Be2B6f0ps1) | false (survey, no instrument) | Catalogs the ongoing-monitoring capability gap at the governance-survey level; names the missing tooling but builds and runs no empirical measurement of documentation fidelity for any deployed system. |
| `rw_safeharbor` | Anon., SafeHarbor (OpenReview:dLojMSgSFW) | false (policy proposal) | Establishes the legal/technical *conditions* for independent evaluation to be possible at all; supplies no measurement instrument and no empirical silent-change rate. |
| `rw_robustaudit` | Anon., RobustAudit (OpenReview:AiaVCVDuxF) | false (different threat model) | Targets manipulation-robustness of a one-shot *fairness* audit under an assumed labeled ground-truth prior; the changelog setting has no such labeled ground truth of "all actual changes," and the concern here is longitudinal documentation fidelity, not single-audit manipulation. |
| `rw_fairbetting` | Anon., FairBetting (OpenReview:EEVpt3dJQj) | false (reusable statistic, not a solution) | Supplies anytime-valid sequential testing machinery for a group-fairness null, reusable for streaming monitoring, but offers no mechanism to parse prose changelogs or build a behavior-category taxonomy of undocumented change. |
| `rw_lamda` | Anon., LAMDA (OpenReview:1FnCrZtBNQ) | false (different unit of analysis) | A rigorous longitudinal concept-drift benchmark for a *first-party* classifier's own accuracy degradation over time — not the gap between a black-box vendor's behavior and that vendor's own published documentation. |
| `rw_chen2023` | Chen, Zaharia & Zou (2023), arXiv:2307.09009 | **true** | Demonstrates GPT-3.5/GPT-4 behavioral drift across two dated snapshots on a fixed task battery (math, refusal, code, formatting), but never cross-references OpenAI's changelog to compute a documented-vs-silent rate, and its narrow battery gives low category coverage. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but one baseline label needs scrutiny.
- comments:
  - `{severity: major, field: "specific_related_works[rw_chen2023].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Chen et al.'s I/O framing never produces a documented/silent label or a changelog-aligned rate — it reports raw behavioral drift on a fixed battery, full stop. Per the stage-3 rubric, a work whose I/O doesn't match this paper's framing 'is not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying there is a ρ or F1 number from Chen et al. to compare against, and there isn't one."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the *protocol* of a fixed, category-diverse task battery run at two time points is still legitimately borrowable as a design precedent).

### Refiner pass

- `rw_chen2023.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — Chen et al. report no silent-change rate and no changelog alignment to compare against. Its **fixed, category-diverse task-battery-at-two-time-points protocol** is borrowed as this paper's own probe-suite design precedent (Stage 0 pilot battery), independent of its published drift findings."
- `rw_logprobtracking.is_potential_baseline` and `rw_rankuniformity.is_potential_baseline` notes sharpened in parallel, since the same risk applies: both remain **true** but explicitly as *change-detection-only sanity-check comparators* ("does something we'd call a genuine diff also get flagged as changed by a narrower prior detector"), never as a documented/silent-rate or F1 number to beat — consistent with `study_type: empirical` forbidding outcome-tier, beats-baseline framing.
- `changes_made`: clarified all three borrowed-baseline roles to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. The closest candidate for a framing-tier RQ (`rw_taig`'s "the monitoring/auditing capability gap is real and unaddressed") is not a distinct framing check — it restates this paper's own RQ1 ("what proportion of detected diffs are undocumented"), which is already the paper's central mechanism-tier question. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one novel decisive component):

- **`sp_signal_from_noise`** — *description:* Separate a genuine cross-version behavioral change from ordinary same-version LLM sampling stochasticity (temperature, prompt sensitivity, load-dependent routing), for an arbitrary probe in a general category-stratified battery, not just a single fixed prompt. *why_it_is_a_problem:* every downstream claim (documented/silent label, silent-rate, category taxonomy) is only meaningful if it is computed over genuine diffs — a detector that can't separate signal from noise manufactures its own findings. *technical_challenge:* the same-version null distribution is itself a moving target (load-dependent routing means "the same version" doesn't yield i.i.d. output), so significance alone is gameable by probe count and trivially small effect sizes. *source_limitation_ids:* `["lim_logprobtracking"]` (its two-sample test is real but scoped to a single fixed prompt's first-token logprob distribution, not a general category-stratified behavioral probe).
- **`sp_prose_to_behavior_alignment`** — *description:* Determine whether a detected behavioral diff is entailed by any claim in the vendor's changelog text for that transition. *why_it_is_a_problem:* without this, "silent" is undefined — the whole paper's estimand depends on a documented/silent label existing at all. *technical_challenge:* changelog prose is unstructured and variable-granularity ("improved reasoning" could entail many probe categories at once), so matching a diff to a claim is an open, many-to-many semantic-entailment problem, not a lookup. *source_limitation_ids:* `["lim_shared_no_disclosure_alignment"]` (a shared limitation across `rw_logprobtracking`, `rw_rankuniformity`, `rw_biassimilarity`, `rw_fairbetting`, `rw_chen2023`: none of them aligns a detected diff to the vendor's own disclosure text — this is the one gap the entire N3 landscape leaves open).
- **`sp_category_construct_validity`** — *description:* Define probe-category boundaries such that a reported concentration of silent change reflects genuine behavioral-domain structure, not an artifact of how the auditor happened to draw category lines. *why_it_is_a_problem:* if categories were chosen post hoc to fit an observed pattern, a "concentration" finding would be circular — the taxonomy would be reverse-engineered from the very result it's supposed to explain. *technical_challenge:* there is no existing, externally-validated taxonomy of "LLM behavior categories for changelog-alignment purposes" to borrow wholesale. *source_limitation_ids:* `["__novel__"]` — no cited work needs to solve this because none of them reports a cross-category concentration finding for a changelog-alignment estimand in the first place.
- **`sp_boundary_attribution`** — *description:* Attribute a detected diff to a specific, bounded release window when the vendor does not publish a clean version-boundary date (rolling deploys, undated changes, A/B routing). *why_it_is_a_problem:* if the "before" and "after" snapshots aren't reliably pinned to the same release transition the changelog describes, the whole alignment step is comparing the wrong things. *technical_challenge:* version boundaries for API-served models are not a given, clean, discrete event — pairing snapshots is itself an inference under uncertainty. *source_limitation_ids:* `["__novel__"]`.
- **`sp_partial_identification`** — *description:* Report a silent-change rate whose absolute correctness cannot be certified, because no independent ground truth of "all actual changes" in a release exists, without overclaiming precision the estimand doesn't have. *why_it_is_a_problem:* a rate presented as if it were the true fraction, when it is structurally only a lower bound, would misrepresent the finding's evidentiary weight to exactly the accountability audience this paper is trying to serve. *technical_challenge:* the estimand is only partially identified — the only checkable property left is whether the reported number is *stable*, not whether it is *correct* in an absolute sense. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's four outputs); one pair of sub-problems risks reading as the same underlying concern twice.
- comments:
  - `{severity: minor, field: "sp_category_construct_validity / sp_partial_identification", anti_pattern: "overlap", comment: "Both are, at bottom, about whether the reported number(s) can be trusted — this can read as one 'is our estimate trustworthy' sub-problem stated twice. They are genuinely distinct, but the descriptions don't yet make the distinction sharp enough: one is about whether *category boundaries* are circular, the other about whether the *absolute rate* is identified at all, and a design could fix one while still failing the other (e.g., perfectly externally-anchored categories with a chi-square-significant concentration finding, yet the underlying overall rate is still only a lower bound; or, conversely, a rate that is provably stable across probe subsets, computed over an arbitrarily gerrymandered set of categories)."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_category_construct_validity.technical_challenge` sharpened to end with: "...this is a **taxonomy-circularity** problem — it concerns whether the *category boundaries themselves* could have manufactured an apparent concentration pattern, independent of whether the overall rate is correctly estimated."
- `sp_partial_identification.technical_challenge` sharpened to end with: "...this is an **estimand-identifiability** problem distinct from taxonomy circularity — it would remain even under a single, uncontested category, because no amount of category-design rigor supplies the missing ground truth of 'all actual changes' that full identification would require."
- `changes_made`: made the taxonomy-circularity-vs-estimand-identifiability distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations — one individual, one shared across 5 works — 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_calibrated_diff_detector`** → targets `sp_signal_from_noise`. *proposed_approach:* For each probe, draw N=50 samples per snapshot; estimate the null via within-version resampling; run a permutation/bootstrap two-sample test at α=0.05, Holm-corrected across probes within a transition; require an effect-size floor (|Cliff's δ| ≥ 0.33) in addition to significance; run the identical pipeline on a same-version (A/A) resample pair as a null control. *key_insight:* a fixed significance threshold alone is gameable by probe count and trivially small effect sizes when the same-version null is itself a moving target (load-dependent routing) — requiring a corrected test *and* an effect-size floor *and* an A/A control margin turns "is this a real diff" into a falsifiable, checkable condition rather than an assumed one, generalizing `rw_logprobtracking`'s narrow logprob-only two-sample test to an arbitrary category-stratified probe. *hypotheses:* ["The same-version (A/A) null control will flag a same-version resample pair as containing a detected diff (D=1) at a rate at or below the nominal α=0.05, while the cross-version arm's count of detected diffs will exceed the A/A arm's false-diff count by at least 3×."]
- **`m_entailment_alignment`** → targets `sp_prose_to_behavior_alignment`. *proposed_approach:* Parse changelog/release-note text into discrete candidate claims; score entailment between each detected diff's description and the claim set; calibrate the entailment threshold τ on a human-labeled dev subset; compare against a naive keyword/string-match baseline (B0). *key_insight:* changelog prose is unstructured and variable-granularity, so only a semantic — not lexical — matcher can generalize across vendors' differing disclosure styles; the string-match comparison is what makes "semantic matching earns its complexity" a checkable claim instead of an assumed one. *hypotheses:* ["The overall silent-change rate ρ (fraction of detected diffs with no matching changelog claim) exceeds 0.50, with the bootstrap 95% CI lower bound also exceeding 0.50.", "M4's automatic documented/silent labeling achieves F1 ≥ 0.70 against a human-labeled subset, exceeding the naive string-match baseline's F1 by a nontrivial, pre-specified margin."]
- **`m_category_anchored_taxonomy`** → targets `sp_category_construct_validity`. *proposed_approach:* Define each probe category by anchoring it to an independently published, externally-validated benchmark chosen for an unrelated original purpose (MMLU for factual QA, GSM8K for reasoning, TruthfulQA for hallucination, XSTest for over-refusal, AdvBench/HarmBench for under-refusal on harmful requests, IFEval for formatting/instruction-following, BFCL for tool-calling) rather than inventing category boundaries after seeing which probes showed silent changes. *key_insight:* a taxonomy invented post hoc to fit an observed concentration pattern would make the "concentration" finding circular; anchoring categories to benchmarks designed and published for unrelated purposes breaks that circularity, so a rejected homogeneity test reflects genuine behavioral-domain structure rather than a taxonomy artifact. *hypotheses:* ["ρ_c is non-uniform across the externally-anchored categories (chi-square rejects equality at α=0.05), with safety/refusal, formatting/instruction-following, and latency/cost each significantly exceeding factual-accuracy in pairwise, Holm-corrected proportion tests."]
- **`m_boundary_fingerprinting`** → targets `sp_boundary_attribution`. *proposed_approach:* Continuously poll the vendor API and log a lightweight distributional fingerprint (first-token top-k logprob profile) even outside announced release windows; declare a "clean" version boundary only where a fingerprint discontinuity exceeds within-version fingerprint variance; restrict headline silent-rate claims to clean-boundary transitions, reporting quarantined (undated/ambiguous) transitions separately. *key_insight:* an announced release date is not a reliable pairing device for rolling/undated deploys, since the announcement and the actual behavioral change point can diverge; a data-driven discontinuity in a cheap, continuously logged fingerprint is checkable independent of what the vendor chooses to announce. *hypotheses:* ["Transitions flagged as clean-boundary by the fingerprint-discontinuity test show a significantly higher rate of detected diffs (D=1) than transitions without a discontinuity, and restricting the headline silent-change rate to clean-boundary transitions yields a materially different estimate than a naive pooled estimate that includes quarantined transitions."]
- **`m_coverage_stability_check`** → targets `sp_partial_identification`. *proposed_approach:* Explicitly frame the reported rate as a coverage-conditioned lower bound; validate its stability (not its absolute correctness, which is uncheckable) by recomputing ρ from two independent random halves of the probe suite within the same transition and measuring agreement. *key_insight:* no oracle exists to certify the true silent-change rate, but split-sample stability is the closest checkable proxy for "this lower bound is a property of the vendor's disclosure practice, not an artifact of which probes happened to be included." *hypotheses:* ["Silent-change rate estimates computed from two disjoint random halves of the probe suite, within the same transition, agree within a pre-specified tolerance in a majority of tested (vendor × transition) cells."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but one method carries two headline claims and needs a one-line justification for why that's one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_entailment_alignment.hypotheses", anti_pattern: null, comment: "Two hypotheses here (the overall silent rate, and the F1-vs-string-match instrument-validity claim) are doing different jobs — one is the paper's headline empirical finding, the other is an instrument-validity check on the classifier that produced it. Worth stating explicitly why one method produces both, so this doesn't read as scope creep bundled into a single method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_entailment_alignment.key_insight` extended: "...a single entailment-scoring pipeline yields two distinct, separately falsifiable readouts from one classifier: the documented/silent label itself, aggregated into ρ (tests the headline prevalence claim), and that same label's agreement with human adjudication and with a string-match lower bound (tests whether the classifier that produced ρ is trustworthy) — one instrument, two readouts, not two mechanisms."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **6 hypotheses total** (1 + 2 + 1 + 1 + 1 across the five methods respectively — `m_entailment_alignment` carries two, per the refiner's one-instrument-two-readouts justification above), mixing instrument-validity claims with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. `rw_logprobtracking`/`rw_rankuniformity` below are sanity-check comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets` (probe sources + changelog corpus):
- MMLU, GSM8K, TruthfulQA, IFEval, BFCL — one benchmark anchoring each of factual QA, reasoning/math, hallucination, formatting/instruction-following, and tool-calling respectively; justification: each is an independently published, externally-validated benchmark, chosen so `rq_category_concentration`'s category boundaries are not invented post hoc (per `m_category_anchored_taxonomy`).
- XSTest and AdvBench/HarmBench — jointly anchor the safety/refusal category. (draft initially listed both with justification only "safety category probes," flagged below.)
- Self-scraped vendor changelog / release-note corpus (OpenAI, Anthropic, Google API release notes) — the documentation-of-record `m_entailment_alignment` aligns against.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Same-version A/A control (identical pipeline on two same-version resamples) — the necessary control for every cross-version claim; instantiates `m_calibrated_diff_detector`'s hypothesis directly.
- Naive keyword/string-match changelog aligner (B0) — the weak lower baseline that justifies `m_entailment_alignment`'s semantic-matching complexity.
- `rw_logprobtracking` and `rw_rankuniformity`, run as change-detection-only comparators — if a probe's diff is flagged by neither prior detector, that's a sanity check on the present method's added coverage, not a claim of superiority.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_aa_control` | `sp_signal_from_noise` | "The same-version (A/A) null control will flag a same-version resample pair as containing a detected diff (D=1) at a rate at or below the nominal α=0.05, while the cross-version arm's count of detected diffs will exceed the A/A arm's false-diff count by at least 3×." |
| `rq_silent_rate` | `sp_prose_to_behavior_alignment` | "The overall silent-change rate ρ (fraction of detected diffs with no matching changelog claim) exceeds 0.50, with the bootstrap 95% CI lower bound also exceeding 0.50." |
| `rq_alignment_validity` | `sp_prose_to_behavior_alignment` | "M4's automatic documented/silent labeling achieves F1 ≥ 0.70 against a human-labeled subset, exceeding the naive string-match baseline's F1 by a nontrivial, pre-specified margin." |
| `rq_category_concentration` | `sp_category_construct_validity` | "ρ_c is non-uniform across the externally-anchored categories (chi-square rejects equality at α=0.05), with safety/refusal, formatting/instruction-following, and latency/cost each significantly exceeding factual-accuracy in pairwise, Holm-corrected proportion tests." |
| `rq_boundary_validity` | `sp_boundary_attribution` | "Transitions flagged as clean-boundary by the fingerprint-discontinuity test show a significantly higher rate of detected diffs (D=1) than transitions without a discontinuity, and restricting the headline silent-change rate to clean-boundary transitions yields a materially different estimate than a naive pooled estimate that includes quarantined transitions." |
| `rq_coverage_stability` | `sp_partial_identification` | "Silent-change rate estimates computed from two disjoint random halves of the probe suite, within the same transition, agree within a pre-specified tolerance in a majority of tested (vendor × transition) cells." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step-6/Step-9 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but the safety/refusal probe-source justification is thin relative to the rubric's "why this dataset actually stresses the hypothesis" bar.
- comments:
  - `{severity: major, field: "datasets[XSTest+AdvBench/HarmBench]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'safety category probes' doesn't say why two sources are needed for one category, or what each stresses that the other doesn't — it reads as citation padding, not a design decision."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "XSTest — *justification:* probes over-refusal (safe prompts wrongly refused), the false-positive direction of a silent safety-behavior change. AdvBench/HarmBench — *justification:* probes under-refusal (harmful prompts answered when they should be refused), the false-negative direction. A vendor could silently shift in either direction between versions (tightening refusal to reduce liability, or loosening it to reduce false-refusal complaints); using only one source would make `rq_category_concentration`'s safety/refusal category blind to whichever direction it didn't cover."
- `changes_made`: gave both safety-probe sources a hypothesis-linked, direction-specific reason instead of a shared generic label.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_matters`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_signal_from_noise.source_limitation_ids = ["lim_logprobtracking"]` ∈ Stage 3 ✓; `sp_prose_to_behavior_alignment.source_limitation_ids = ["lim_shared_no_disclosure_alignment"]` (spans 5 Stage-3 works, all present) ✓; remaining three sub-problems `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (genuine-diff flag, documented/silent label, per-category and overall rate, ranked taxonomy) are each reachable: diff flag via `sp_signal_from_noise`, documented/silent label and overall rate via `sp_prose_to_behavior_alignment`, taxonomy via `sp_category_construct_validity`, with `sp_boundary_attribution` and `sp_partial_identification` covering the two structural caveats (attribution, identifiability) that qualify all of the above — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs; recount of hypotheses vs. RQs: 6 Stage-5 hypotheses, 6 Stage-6 RQs, 1:1, none dropped or duplicated.

**What was hardest:** as with the B5.5 exemplar, the recurring tension was **not disagreement about facts** (the seed material is unusually well-specified, down to a full formal notation and pre-registered fallbacks in `paper.md`) but **scope discipline** — repeatedly checking whether a stage-4/5 sub-problem was quietly restating `paper.md`'s own already-finished Step 5/6 rather than adding something this schema's structure specifically demands (e.g., the taxonomy-circularity concern in `sp_category_construct_validity`, which `paper.md`'s Assumption A5 gestures at as a feasibility risk but never states as its own falsifiable hypothesis until this run's Stage 5).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists). Every finding enumerated and statused; historical rounds above are untouched.

**Already applied / logged as resolved (no action needed this round):**
1. `stage_review.md` Stage 2 REVISE (explicit nearest-neighbor sentence naming Chen, Zaharia & Zou 2023) — present in `paper_draft.md` Introduction and Related Work opening.
2. `stage_review.md` Stage 4 REVISE (per-RQ falsification conditions) — present in all six RQ subsections of `paper_draft.md`/`.tex` and `experiment_design.md`.
3. `stage_review.md` Phase A item 2 (reference-cache integrity: 9 N3-cited works backfilled as `selected`) — fixed per `pipeline.md`; residual digest gap for the 4 load-bearing entries closed in the Phase F/G session (real N0–N12 digests built).
4. `stage_review.md` Phase A item 4 (H3 Claim–Evidence Map fallback annotation) — fixed in `paper.md` (merged row, `F3 fallback` cited).
5. `stage_review.md` Phase A item 5, Finding A (H1 cross-vendor aggregation vote rule) — fixed in `paper.md` Step 6 RQ1 and mirrored into `paper_draft.*` RQ2 and `experiment_design.md` RQ2.
6. `stage_review.md` Phase A item 5, Finding B (explicit PG-1…PG-6 gate ids on A1–A6) — fixed in `paper.md` Assumptions + Step 9.
7. `stage_review.md` Phase G [major] (zero `\cite`/no `refs.bib`) — fixed: `gen_refs_bib.py`-generated `refs.bib`, 12/12 keys cited, 0 undefined citations.
8. `stage_review.md` Phase G Finding 1 [moderate] (RQ2 missing cross-vendor vote rule) — fixed in `paper_draft.*`.
9. `stage_review.md` Phase G Finding 2 [moderate] (RQ1/RQ3 missing pre-committed fallback actions) — fixed in `paper_draft.*`.
10. `stage_review.md` Phase G Finding 3 [minor] (Conclusion missing global-pivot F-G1 mention) — fixed in `paper_draft.*` Conclusion.
11. `taste_audit.md` — 🟢 both passes (pre-draft and Phase H re-audit), no action items to apply.

**Applied this round:**
12. `stage_review.md` Phase G Finding 4 [minor], the one OPEN item (RQ-vs-H numbering mismatch between `paper_draft.*` and `paper.md`, logged as a to-do at Phase G) → applied the review's own recommended remedy, an explicit RQ↔H crosswalk: a "Numbering crosswalk to the pre-registered protocol" paragraph added directly after the Research-questions list in `paper_draft.md` and `paper_draft.tex` (RQ1↔H3(b)/PG-1, RQ2↔H1+vote rule, RQ3↔H3(a)/PG-3, RQ4↔H2; RQ5/RQ6 = instrument-validity checks A4/PG-4 and A5/PG-5, no H-number), and a matching crosswalk line added to `experiment_design.md`'s header block. Full re-numbering was deliberately not done, per the review's own caution that re-numbering risks introducing fresh errors. `paper_draft.pdf` recompiled: exit 0, 13 pages, 0 errors, 0 undefined citations.

**Rejected as moot:**
13. `stage_review.md` Phase A item 2 "Also fixed" note (thin 150-candidate harvest; fresh harvest from new angles recommended before Phase E) — rejected — the cache now holds 12 `selected` records (above the <5 "thin" threshold) after the 9-record N3 backfill, `pipeline.md`'s freshness sweep (2 targeted searches on the manipulated-variable angle) found no genuine method-twin, and a new web harvest cannot change the deliverables absent new experiments; the recommendation remains recorded in `pipeline.md`'s "Next action" for the future real-compute run, where it belongs.

**Cross-deliverable consistency check (this round):** RQ count (6/6), effect-size floor (Cliff's δ ≥ 0.33), α=0.05 Holm-corrected, 3× A/A margin, F1 ≥ 0.70, κ ≥ 0.6, ≥200 diff/claim pairs, ≥1000 bootstrap resamples, ≥2-of-≥3 vendor vote with 20-diff power floor, ≥20 diffs/category for RQ4, and the F-G1 global pivot all match between `paper_draft.md` and `experiment_design.md`; target hypotheses in `experiment_design.md` remain verbatim from Stage 5 / `paper.md`. No mismatch found; no fix needed beyond item 12.
