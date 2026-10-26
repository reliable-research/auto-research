# Auto-Research-Discussion Run — T5.3 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.3**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (`paper.md` already carries formal notation, hard-coded hypotheses, pre-committed fallback wording, and a walking skeleton), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure the precision and recall of an automated constraint-verification prototype at detecting design-constraint violations in coding-agent-produced patches, relative to independently adjudicated human review, and determine which categories of design constraints can be safely automated versus which inherently require human judgment.
- **Apparent inputs:** category-labeled design constraint cards; coding-agent-produced patches scoped to those cards (both compliant and violating); an automated verifier's per-(card, patch) judgment; independent multi-reviewer human judgments over the same pairs.
- **Apparent outputs:** per-category precision/recall/F1 of the verifier against adjudicated human labels; per-category verifier–human vs. human–human agreement (Cohen's κ vs. Fleiss' κ); a three-way classification of each constraint category as automatable / human-required / inconclusive.
- **Closest research areas:** automated code review (DefectReview); LLM-judge calibration and selective prediction (Trust-or-Escalate); checklist/constraint decomposition for instruction-following (RLCF-Checklists, RECAST); execution-based and execution-free SE-agent evaluation (SWE-bench, SWE-RM); verifier-capability measurement (VerifDynamics); architecture-conformance checking (Reflexion models); static-analysis tool adoption (Johnson et al., 2013).
- **In scope:** measuring an existing/prototype hybrid verifier's precision-recall against human review across a fixed constraint-category taxonomy on coding-agent patches. **Out of scope:** training a new verifier model from scratch; claiming the verifier is a state-of-the-art method to be adopted; live/production deployment; population-scale or multi-repository generalization beyond the pre-registered corpus.
- **Confidence: high.** As with a prior mature seed in this repository, `paper.md` here is itself a pre-registered specification with formal notation (Step 5), hard-coded falsifiable hypotheses (Step 6, H1–H3), pre-committed fallback wording for every failure mode, an explicit taste self-audit (Step 3), and a walking skeleton (Step 9) — reconstruction risk is low. The risk instead is redundancy with `paper.md`'s own Step 5/6, which is why Stage 5/6 below reuse `paper.md`'s already-designed formal apparatus and hypotheses as authored design targets rather than re-deriving them from scratch, and instead spend their critic rounds on gaps `paper.md` didn't fully close (see Stage 1 and Stage 4 below).

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a set of design constraint cards, each labeled with a category (architectural boundary, API-usage restriction, naming/style, security invariant, or intent-level design principle), and coding-agent-produced patches scoped to those cards, determine the precision and recall of an automated constraint verifier at detecting violations, relative to an independently adjudicated human review, and determine which constraint categories the verifier can match human-level agreement on versus which remain dependent on human judgment.
- `input`: (1) a corpus of category-labeled design constraint cards; (2) a corpus of coding-agent-produced patches, each scoped to one or more cards, spanning both compliant and violating instances; (3) an automated verifier's violation/no-violation judgment (with confidence) for every (card, patch) pair; (4) independent judgments from ≥3 human reviewers for the same pairs, adjudicated into a reference label.
- `output`: (1) per-category precision, recall, and F1 of the verifier against the adjudicated human labels; (2) per-category Cohen's κ between verifier and human labels, compared against the human–human (Fleiss') κ ceiling; (3) a classification of each constraint category as automatable, human-required, or inconclusive.
- `constraints`: the human-review reference is not assumed noise-free — its own inter-rater agreement must be measured and used as the ceiling against which verifier performance is judged; categories with too few observed violations must be reported as inconclusive rather than automatable, regardless of point estimates.
- `objective`: a category is accepted as "automatable" only if the gap between human–human agreement and verifier–human agreement is small enough, with a stated confidence interval, and estimated from enough violations to be trusted — never resolved by eyeballing a point estimate.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 classifies this as a measurement/characterization study (the verifier is the *instrument*, not the headline deliverable), and the core question ("哪类约束可自动化、哪类本质需要人") is a characterization question, not a claim of a superior new method.

**critique:**
- summary: Strong, evidence-traceable draft with a real formal skeleton already implied, but the objective has an unaddressed edge case and the summary quietly presupposes a settled taxonomy.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective doesn't say what happens when the human-review reference *itself* fails to clear a usability floor for a category — i.e., when reviewers disagree so much with each other that a ceiling of κ_H ≈ 0 makes any verifier-vs-human comparison meaningless. paper.md's own Step-5/A2 machinery already anticipates this ('reference-unstable' categories, excluded from the main partition and reported as their own finding) but Stage 1's objective as drafted only distinguishes automatable/human-required/inconclusive-by-sample-size, silently assuming the human reference is always trustworthy enough to compare against. Without naming this as a first-class possible outcome, the objective is not fully evaluable for every category that could arise."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'design constraint cards, each labeled with a category' presupposes the category taxonomy is already clean and non-overlapping. Whether cards can be assigned categories with adequate inter-annotator agreement is itself a construction question (digest A1), not a given — the summary should not assume it's settled."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content `paper.md`'s Step 5/A2 already supports — no new content needed).

### Refiner pass

- `objective` (refined): "A category is accepted as automatable only if (i) the measured human–human agreement clears a stated interpretability floor for that category, and (ii) conditional on (i), the 95% CI of the gap between that human–human ceiling and verifier–human agreement excludes values above a small, pre-specified threshold, estimated from enough observed violations to be trusted. If (i) fails, the category is reported as *reference-unstable* — a distinct, reportable outcome in its own right, not silently folded into either automatable or human-required."
- `summary` (refined): "...design constraint cards, each assigned to a category from a fixed taxonomy whose inter-annotator agreement is itself checked rather than assumed..." (removes the presupposed-settled-taxonomy framing).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation rather than inventing new symbols): "Card set C with category map τ: C → T, T = {structural, API, naming, security, intent-level}. Patch set P; evaluation unit (c, p) ∈ C×P. Verifier V: (c,p) → {violation, no-violation} with confidence q(c,p). Human panel of r ≥ 3 reviewers gives labels h_1..h_r(c,p); adjudicated reference y(c,p). Per category t: κ_H,t = human–human agreement (Fleiss' κ); κ_V,t = verifier–human agreement (Cohen's κ) against y; n_t = observed violation count. Category t is classified automatable / human-required / reference-unstable / inconclusive as a function of (κ_H,t, κ_V,t, n_t) — never by an unweighted point-estimate comparison."
- `changes_made`: tightened objective's evaluability condition to cover the reference-unstable edge case; removed a presupposition from summary; added formal_summary reusing `paper.md`'s existing notation.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: As coding agents produce patches faster than teams can manually review them against explicit design constraints, automated constraint verification is being treated as viable delegated gatekeeping — but whether such a verifier's precision and recall actually match human review, and for which kinds of constraints, has not been measured.
- `why_it_matters`: If a verifier is deployed uniformly across all constraint categories without knowing where it silently misses violations (false negatives) or drowns reviewers in spurious flags (false positives — the documented cause of static-analysis tool abandonment), a team cannot tell whether it is safely offloading review effort or quietly eroding the very design guarantees the cards exist to enforce. The risk is not symmetric across constraint types: catching a forbidden-API call is a different kind of claim than judging whether a patch preserves "separation of concerns," and treating both the same way behind one blended accuracy number hides exactly the information a team needs to decide where human review remains mandatory.
- `who_cares`: Engineering teams and platform builders deciding whether an automated constraint gate is safe to rely on for coding-agent output; designers of design-card / constraint-specification schemes deciding which constraint categories are worth encoding as explicit cards at all; researchers studying LLM-judge and verifier reliability who need an empirical account of where verifier–human agreement holds and where it breaks down.
- `evidence`: `[DefectReview, OpenReview:mEV0nvHcK3]` reports that on prior benchmarks fewer than 10% of automatically generated review comments are truly high quality — direct evidence that automated review signal quality is not a solved problem even before constraint-specific structure is considered. `[Johnson et al., 2013]` establishes, from developer interviews, that false positives — not false negatives — are the dominant reason static-analysis tools are abandoned in practice, meaning adoption risk here is asymmetric and precision-sensitive in a way one aggregate accuracy number cannot surface. `[VerifDynamics, OpenReview:DcEuBwrWnB]` shows verifier quality does not scale simply with model size and varies strongly by regime — evidence that a single verifier-quality number is likely to mask real per-category variation here too.

**critique:**
- summary: Stake-specific motivation with real citations, but coverage of Stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (2) is the human–human κ ceiling, not just the verifier's own scores — and why_it_matters never explains why measuring that ceiling matters, as opposed to simply trusting human review as ground truth. Without this, a reader could ask 'why not just compare the verifier to human labels directly and skip measuring reviewer agreement' — a real, unaddressed gap, since the whole automatable/human-required/reference-unstable classification in Stage 1's refined objective depends on that ceiling being measured rather than assumed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...Moreover, treating human review as an infallible reference would be its own mistake: without measuring how much reviewers agree with *each other* in the first place, a team cannot tell whether an apparent verifier–human disagreement reflects a real verifier failure or simply the reviewers' own unresolved disagreement about what the card requires — a distinction that determines whether the fix belongs in the verifier or in clarifying the card itself. This is exactly why the measured ceiling, not an assumed-perfect reference, has to be part of what gets reported."
- `changes_made`: added the reference-usability coverage argument, tying it to the refined Stage 1 objective's reference-unstable outcome.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level; per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list. Seven are real corpus papers (`[GROUNDED:corpus]`); two are canonical, real, pre-2020 software-engineering references the corpus does not cover (`[NON-CORPUS]`) — carried forward from digest.md exactly as sourced, not invented for this stage.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_defectreview` | Anon., "Towards Practical Defect-Focused Automated Code Review" (OpenReview:mEV0nvHcK3) | false (optimized/measured against a defect oracle, not a constraint taxonomy) | Balances precision/coverage against catching *bugs* on merge requests, not against a per-category taxonomy of explicit design constraints — leaves open how automation performs across heterogeneous constraint types. |
| `rw_trustorescalate` | Anon., "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement" (OpenReview:UHPnqSTBPO) | **true** | Bounds *aggregate* disagreement with humans via a calibrated confidence threshold, but doesn't decompose where abstentions concentrate by constraint type — can't say which categories the judge can vs. cannot safely rule on. |
| `rw_rlcfchecklists` | Anon., "Checklists Are Better Than Reward Models For Aligning Language Models" (OpenReview:RPRqKhjrr6) | false (studies generator satisfaction, not verifier detection) | Assumes constraints are already reducible to atomic yes/no items with a reliable per-item checker; studies constraint *satisfaction by a generator*, not the detection precision/recall of a verifier against human-labeled violations on real diffs. |
| `rw_recast` | Anon., "RECAST: Expanding the Boundaries of LLMs' Complex Instruction Following with Multi-Constraint Data" (OpenReview:90tCp2KszA) | false (same generator-satisfaction framing as above) | Shows LLM constraint-satisfaction degrades as constraint count grows and that per-constraint verifiability varies by type — the empirical premise behind the automatable/human-required split — but still measures generator compliance, not verifier detection accuracy against human review. |
| `rw_swebench` | Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" (OpenReview:VTF8yNQM66) | false (execution oracle for task resolution, not a per-card verifier) | Execution-verified benchmark using fail-to-pass tests as an objective correctness oracle over repository-scale edits — the canonical source of realistic agent patches, but its oracle only covers the executably-testable slice of constraints, not per-card human-judged compliance. |
| `rw_swerm` | Anon., "SWE-RM: Execution-free Feedback for Software Engineering Agents" (OpenReview:H9wMe1G76j) | false (trajectory-level reward model, not per-constraint verifier) | Trains an execution-free reward model scoring whole SE-agent trajectories, motivated by test suites being incomplete or misaligned — grounds the claim that many design constraints can't be reduced to a passing test, but doesn't measure per-(card, patch) verifier agreement with human review. |
| `rw_verifdynamics` | Anon., "Variation in Verification: Understanding Verification Dynamics in Large Language Models" (OpenReview:DcEuBwrWnB) | false (studies math/reasoning verification, different domain and ground-truth type) | Empirically disentangles problem difficulty, generator capability, and verifier capability on math/reasoning correctness with *automatic* ground truth, showing verifier quality doesn't scale simply — but never studies a domain where the "ground truth" is itself noisy human review, leaving the human-review noise ceiling unquantified. |
| `rw_reflexionmodel` | Murphy, Notkin & Sullivan, "Software Reflexion Models: Bridging the Gap between Design and Implementation," IEEE TSE 27(4), 2001 | **true** | Canonical architecture-conformance technique — computes convergences/divergences/absences between an intended high-level model and as-built source structure — the archetype of a structurally checkable, automatically verifiable design constraint. Predates coding agents entirely; gives no evidence on semantic/intent-level constraints or agent-generated patches. |
| `rw_johnson2013` | Johnson et al., "Why Don't Software Developers Use Static Analysis Tools to Find Bugs?," ICSE 2013 | false (interview study, not a runnable method) | Establishes from developer interviews that false positives — not false negatives — are the dominant reason static-analysis tools get abandoned, so precision (not just recall) governs real-world usability; predates LLM-based verification and coding agents entirely. |

**critique:**
- summary: Grounding is solid and every limitation is specific and problem-tied, but one baseline label needs the same scrutiny a mismatched-I/O work gets elsewhere in this rubric.
- comments:
  - `{severity: major, field: "specific_related_works[rw_reflexionmodel].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Reflexion models' I/O framing is a 2001-era, tool-specific architecture-conformance check with no released software applicable to modern coding-agent patches or this paper's card taxonomy — genuinely different infrastructure from this paper's setting, even though the underlying *idea* (structural conformance checking) is exactly what one of this paper's verifier sub-mechanisms borrows. Per the stage-3 rubric, marking it a straightforward runnable baseline risks implying Reflexion models' own published numbers are being compared against, which they cannot be — the paper is 24 years old and predates the corpus entirely."}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the *protocol idea* is still legitimately borrowable as the design for one verifier sub-mechanism and one baseline arm).

### Refiner pass

- `rw_reflexionmodel.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-published-number sense — no running Reflexion-models implementation is compared against. Its **architecture-conformance protocol idea** (convergences/divergences between an intended model and as-built structure) is borrowed as the design for the structurally-checkable sub-mechanism and as a baseline *arm's* mechanism, independent of the 2001 paper's own reported results."
- `changes_made`: clarified Reflexion models' baseline role to avoid an implied comparison against a 2001 tool's own numbers.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — every limitation above is already fully absorbed into this paper's own sub-problems and mechanism-tier hypotheses (Stage 4/5/6 below), not a separate gap this paper is willing to spend an independent experiment confirming on its own. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, 4 from digest N5's C1–C4, 1 added as a novel decisive component):

- **`sp_operationalizability_spectrum`** — *description:* Report verifier performance stratified by constraint-category operationalizability (structurally checkable through intent-laden) rather than as one aggregate number. *why_it_is_a_problem:* An aggregate accuracy figure can hide a verifier that is excellent on syntactic categories and mediocre on semantic ones behind a blended score that looks acceptable overall. *technical_challenge:* no single verifier mechanism is likely to handle both deterministic pattern-matching and semantic intent-reasoning equally well, so the category-level split itself must be measured with enough per-category statistical power to be believed, not merely asserted. *source_limitation_ids:* `["lim_verifdynamics"]` (`rw_verifdynamics`'s limitation explicitly motivates this — aggregate accuracy hides per-regime variation, and this paper's own domain has never had that variation measured).
- **`sp_reference_noise_ceiling`** — *description:* Establish and report how much human reviewers agree with each other, per category, before judging the verifier against them. *why_it_is_a_problem:* If the reference itself is unreliable, an apparent verifier failure could really be unresolved disagreement about what the card means — conflating the two would misattribute the fix. *technical_challenge:* achieving usable multi-reviewer agreement on intent-laden cards may itself fail (digest A2), which the methodology must detect and report as its own outcome rather than silently assume away. *source_limitation_ids:* `["__novel__"]` — no cited work studies a domain where the verification reference is itself noisy human judgment; `rw_verifdynamics` comes closest but explicitly uses automatic, not human, ground truth.
- **`sp_intent_vs_literal`** — *description:* Correctly judge violations of intent-level constraints, where a patch can satisfy a card's literal wording while violating what the card is actually meant to prevent (or vice versa). *why_it_is_a_problem:* surface pattern-matching against a card's text cannot distinguish literal compliance from intent compliance, so any verifier relying only on textual matching will systematically misjudge exactly the constraints hardest to automate. *technical_challenge:* no reliable per-item checker exists for constraints that are not already reducible to atomic yes/no predicates. *source_limitation_ids:* `["lim_checklists_recast"]` (`rw_rlcfchecklists`, `rw_recast` both assume atomic, reliably-checkable constraint items and don't address intent-laden ones).
- **`sp_precision_recall_tradeoff`** — *description:* Determine and report the precision/recall operating point that is actually adoptable per constraint category, rather than a single blended threshold. *why_it_is_a_problem:* tuning for high recall inflates false positives and reviewer burden (the documented driver of tool abandonment), while tuning for high precision silently misses real violations — the acceptable trade-off is category-dependent, not a single global setting. *technical_challenge:* the precision-maximizing threshold for one category may not simultaneously satisfy another category's precision floor, so a single fixed operating point cannot be adoptable everywhere at once. *source_limitation_ids:* `["lim_johnson2013"]` (`rw_johnson2013` establishes that false positives, not false negatives, drive real-world tool abandonment, but predates coding agents and gives no per-category evidence).
- **`sp_corpus_nontriviality`** — *description:* Construct a (card, patch) pair corpus where violations are neither trivially obvious nor practically absent per category. *why_it_is_a_problem:* a corpus that is too easy would make every verifier configuration — including a naive keyword matcher — look accurate, hiding the true automatable/human-required split behind an artifact of corpus difficulty rather than constraint operationalizability. *technical_challenge:* real coding-agent patches may rarely violate certain categories naturally, forcing either violation scarcity or reliance on constructed violations that risk being over-obvious; telling genuine difficulty apart from artificial difficulty requires an independent pre-screen, not just a larger sample. *source_limitation_ids:* `["__novel__"]` — `rw_swebench` supplies realistic patches but was never built or evaluated for constraint-violation balance or difficulty.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's three outputs), but two sub-problems risk reading as the same underlying concern stated twice.
- comments:
  - `{severity: minor, field: "sp_operationalizability_spectrum / sp_intent_vs_literal", anti_pattern: "overlap", comment: "Both sub-problems are framed around the structural-vs-semantic spectrum, which can read as the same sub-problem restated. They are genuinely distinct — one is about *how results are reported/decomposed* (a measurement-design problem: don't average away category variation), the other is about *a specific verifier judgment failure mode* (a semantics problem: literal text vs. intended meaning) — but the descriptions don't make that distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_operationalizability_spectrum.technical_challenge` sharpened to end with: "...this is a **reporting-granularity** problem — ensuring the analysis surfaces category-level variation that already exists, not a claim about why any particular category is hard to judge correctly."
- `sp_intent_vs_literal.technical_challenge` sharpened to end with: "...this is a distinct **judgment-mechanism** problem from reporting granularity — even with perfect per-category reporting, a verifier that only pattern-matches card text has no way to detect a literal-compliance/intent-violation mismatch; the fix has to live in what the verifier reasons over, not just in how results are stratified."
- `changes_made`: made the reporting-granularity vs. judgment-mechanism distinction explicit in both technical_challenge fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 3 sourced from Stage 3 limitations, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods, hypotheses reusing `paper.md`'s Step 5/6 formal apparatus as authored design targets):

- **`m_category_stratified_scoring`** → targets `sp_operationalizability_spectrum`. *proposed_approach:* Compute precision, recall, F1, and κ separately for each of the five constraint categories rather than pooling into one aggregate number; require every automatable/human-required verdict to be issued per category, never in aggregate. *key_insight:* an aggregate metric is a weighted average that can hide a verifier that is excellent on syntactic categories and poor on semantic ones behind a mediocre-but-passable blended score — stratification is what makes hidden variation visible at all. *hypotheses:* ["On the four structurally-defined categories (architectural boundary, API-usage restriction, naming/style, security invariant) jointly, the verifier reaches precision ≥ 0.85 and recall ≥ 0.80, with Wilson 95% CI lower bounds ≥ 0.75 for both.", "The intent-level category's F1 falls at least 0.15 below the minimum F1 among the four structural categories, and this category effect is statistically significant via a likelihood-ratio test on a logistic regression of per-pair verifier correctness on category, at α = 0.05."]
- **`m_measured_human_ceiling`** → targets `sp_reference_noise_ceiling`. *proposed_approach:* Recruit ≥3 independent reviewers per (card, patch) pair, adjudicate disagreements into a reference label, and compute Fleiss' κ among the raw reviewer labels per category as an explicit, reported ceiling — then judge the verifier's Cohen's κ against that ceiling via a bootstrap-CI gap rather than an assumed-perfect reference. *key_insight:* since human review is the yardstick, the yardstick's own reliability has to be measured, not assumed — a verifier can only meaningfully be said to fail relative to a ceiling that is itself known to be attainable. *hypotheses:* ["Fleiss' κ among the human reviewers is at least 0.4 in every constraint category, establishing the human–human reference as usable rather than assumed usable.", "The verifier–human κ gap's 95% bootstrap CI (10,000 resamples, clustered by card) has an upper bound at or below 0.10 for at least two constraint categories, licensing an automatable classification for those categories, while the intent-level category's gap CI lower bound exceeds 0.10, licensing a human-required classification, with at most one category classified inconclusive."]
- **`m_intent_routing_with_abstention`** → targets `sp_intent_vs_literal`. *proposed_approach:* Route intent-laden categories to an LLM-as-judge sub-mechanism that reasons over both a card's stated text and its design rationale, calibrated to abstain (defer to human review) below a confidence threshold; route structurally-checkable categories to a deterministic rule/AST or architecture-conformance check instead. *key_insight:* a verifier forced to answer every pair with equal confidence is forced to guess exactly where literal-text matching is least informative; calibrated abstention converts a forced wrong guess into an honest "escalate to human." *hypotheses:* ["A single-shot LLM judge with no card decomposition and no calibrated abstention (baseline B-alt), budget-matched in total token spend per pair to the full hybrid verifier, shows a per-category F1 pattern within 0.05 of the hybrid verifier's own per-category F1 pattern — i.e., the category-level split is attributable to the constraints' intrinsic operationalizability rather than to the routing/decomposition mechanism itself."]
- **`m_operating_curve_reporting`** → targets `sp_precision_recall_tradeoff`. *proposed_approach:* Report a per-category confidence-thresholded precision-recall operating curve rather than a single blended accuracy number, and require the deployed operating point on each category to clear a stated precision floor. *key_insight:* precision and recall trade off at a rate that differs by category, so a single fixed threshold applied everywhere picks an operating point that is wrong for some category by construction. *hypotheses:* ["The full hybrid verifier beats a naive keyword/regex matcher (baseline B0) on pooled paired violation/no-violation decisions (McNemar's test, α = 0.05, Holm-corrected across categories)."]
- **`m_prescreened_corpus_construction`** → targets `sp_corpus_nontriviality`. *proposed_approach:* Seed (card, patch) pairs from real SWE-bench-style issue→PR tasks, have the human panel pre-screen and discard pairs that are trivially compliant or trivially violating (measured by reviewer median judgment time), and require a minimum share of "non-obvious" pairs plus a minimum violation count per category before that category enters the analysis. *key_insight:* a corpus can be class-balanced in raw violation counts yet still be trivial if every violation is obvious at a glance — the pre-screen targets difficulty directly, which class balance alone cannot fake. *hypotheses:* ["At least 20% of pairs surviving the human pre-screen in each constraint category have a median reviewer judgment time exceeding a pre-specified non-obviousness threshold, and at least 30 adjudicated violations are retained per category before that category enters the analysis; categories not meeting this bar are reported as inconclusive rather than folded into an aggregate."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis is falsifiable with a stated threshold — but one method's key_insight and its hypothesis are testing different things.
- comments:
  - `{severity: major, field: "m_operating_curve_reporting", anti_pattern: "mismatch", comment: "The key_insight is entirely about category-dependent trade-off curves — 'a single fixed threshold... picks an operating point that is wrong for some category by construction' — but the sole hypothesis only tests whether the hybrid verifier beats a naive baseline in aggregate (McNemar's test on pooled decisions). Beating a keyword matcher says nothing about whether operating points actually differ by category; as drafted, the method's headline insight is untested by its own hypothesis."}`
- decision: `move_to_refiner` (the fix is to add the operating-curve claim as its own falsifiable hypothesis, using content the method's own key_insight already supports — not a redesign).

### Refiner pass

- `m_operating_curve_reporting.hypotheses` extended with a second entry: "No single confidence threshold clears a 0.85 precision floor simultaneously on all five constraint categories — the precision-maximizing operating threshold differs significantly across categories, demonstrating that operating points are not category-invariant."
- `changes_made`: added the category-varying-threshold hypothesis so the method's key_insight (trade-off curves are category-dependent) is actually tested, alongside the pre-existing baseline-beating hypothesis (is a verifier needed at all).
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **8 hypotheses total** (2 + 2 + 1 + 2 + 1 across the five methods respectively — `m_category_stratified_scoring`, `m_measured_human_ceiling`, and `m_operating_curve_reporting` each carry two, each pair justified as one instrument yielding two separately falsifiable estimands rather than scope creep, mirroring the refiner's own justification for `m_operating_curve_reporting`'s pair above).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our verifier beats baseline X" as a headline claim. B0 and B-alt below are sanity-check/rival-explanation comparators embedded inside mechanism-tier hypotheses, never a competitor the paper claims to beat as its contribution.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Constructed design-card corpus (category-labeled, item-decomposed per `rw_rlcfchecklists`'s template) — *justification:* the necessary substrate for `rq_category_stratified_reliability` and `rq_automatable_partition`; without category-labeled cards there is no unit to stratify results by.
- SWE-bench / SWE-bench Verified issue→PR patches (`rw_swebench`) — *justification:* supplies ecologically real, not synthetic, patches for `rq_corpus_nontriviality_gate`'s non-obviousness pre-screen; a fully synthetic corpus would let violations be constructed as obvious by design, defeating the pre-screen's purpose.
- (draft initially listed the calibrated selective judge (Trust-or-Escalate style) with justification only "digest lists it as a baseline" — flagged below.)

`baselines` (sanity-check/rival-explanation comparators, not outcome-tier competitors):
- B0 — naive keyword/regex matcher (no AST, no LLM) — necessary control for `rq_verifier_beats_naive`: if B0 already sits inside the human-agreement band on some category, that category needed no verifier research at all.
- B-alt — single-shot LLM judge, no card decomposition, no abstention, budget-matched to the hybrid verifier's total token spend — isolates whether an observed category split reflects the constraints' intrinsic operationalizability or the routing/decomposition mechanism itself (`rq_instrument_invariance`).

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_category_stratified_reliability` | `sp_operationalizability_spectrum` | "On the four structurally-defined categories (architectural boundary, API-usage restriction, naming/style, security invariant) jointly, the verifier reaches precision ≥ 0.85 and recall ≥ 0.80, with Wilson 95% CI lower bounds ≥ 0.75 for both." |
| `rq_category_effect_significant` | `sp_operationalizability_spectrum` | "The intent-level category's F1 falls at least 0.15 below the minimum F1 among the four structural categories, and this category effect is statistically significant via a likelihood-ratio test on a logistic regression of per-pair verifier correctness on category, at α = 0.05." |
| `rq_reference_usability` | `sp_reference_noise_ceiling` | "Fleiss' κ among the human reviewers is at least 0.4 in every constraint category, establishing the human–human reference as usable rather than assumed usable." |
| `rq_automatable_partition` | `sp_reference_noise_ceiling` | "The verifier–human κ gap's 95% bootstrap CI (10,000 resamples, clustered by card) has an upper bound at or below 0.10 for at least two constraint categories, licensing an automatable classification for those categories, while the intent-level category's gap CI lower bound exceeds 0.10, licensing a human-required classification, with at most one category classified inconclusive." |
| `rq_instrument_invariance` | `sp_intent_vs_literal` | "A single-shot LLM judge with no card decomposition and no calibrated abstention (baseline B-alt), budget-matched in total token spend per pair to the full hybrid verifier, shows a per-category F1 pattern within 0.05 of the hybrid verifier's own per-category F1 pattern — i.e., the category-level split is attributable to the constraints' intrinsic operationalizability rather than to the routing/decomposition mechanism itself." |
| `rq_verifier_beats_naive` | `sp_precision_recall_tradeoff` | "The full hybrid verifier beats a naive keyword/regex matcher (baseline B0) on pooled paired violation/no-violation decisions (McNemar's test, α = 0.05, Holm-corrected across categories)." |
| `rq_threshold_category_dependence` | `sp_precision_recall_tradeoff` | "No single confidence threshold clears a 0.85 precision floor simultaneously on all five constraint categories — the precision-maximizing operating threshold differs significantly across categories, demonstrating that operating points are not category-invariant." |
| `rq_corpus_nontriviality_gate` | `sp_corpus_nontriviality` | "At least 20% of pairs surviving the human pre-screen in each constraint category have a median reviewer judgment time exceeding a pre-specified non-obviousness threshold, and at least 30 adjudicated violations are retained per category before that category enters the analysis; categories not meeting this bar are reported as inconclusive rather than folded into an aggregate." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step 5/6 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but two issues need fixing: one dataset justification is a citation to the digest instead of a methodological reason, and one RQ is close to tautological as framed.
- comments:
  - `{severity: major, field: "datasets[calibrated selective judge]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest lists it as a baseline' says nothing about which RQ needs it or why — and it isn't a dataset at all, it's a baseline mislabeled as one."}`
  - `{severity: major, field: "rq_verifier_beats_naive", anti_pattern: "tautology", comment: "As framed ('the hybrid verifier beats a naive keyword matcher'), this risks passing by construction — a hybrid verifier with an LLM-judge component beating a pure keyword matcher in aggregate is close to guaranteed and not informative on its own. paper.md's own Step-6 framing of B0 is sharper: the informative question is not whether the hybrid wins in aggregate, but *for which categories B0 already suffices* — if B0 already sits inside the human-agreement band on some category, that category needed no verifier research at all, independent of whether the hybrid also beats it there. The RQ description should be reframed around per-category sufficiency, not an aggregate win/loss."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry corrected: the calibrated selective judge (Trust-or-Escalate style) is removed from `datasets` (it is a baseline, not a dataset) and added to `baselines` as a **secondary, non-gating comparator**: "reported descriptively per category alongside B0/B-alt, with no pass/fail criterion attached — included because it is the nearest published calibrated-judge protocol, not because any RQ requires beating it."
- `rq_verifier_beats_naive.description` reframed (hypothesis text unchanged, verbatim match preserved): from "does the hybrid verifier beat a naive baseline" to "for which constraint categories does even a naive keyword/regex matcher already reach the human-agreement band, making further verifier engineering unnecessary there — and does the full hybrid verifier improve on B0 where it does not." The pre-registered McNemar test remains the headline statistical procedure; the description now states the informative, non-tautological framing explicitly.
- `changes_made`: gave the mislabeled dataset entry a correct home and a hypothesis-linked reason instead of a provenance note; reframed one RQ's description to remove tautology risk while preserving its verbatim hypothesis and statistical test.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the verifier itself is the object of study established in Stage 1's `input`, not a method the paper proposes to solve a problem).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_operationalizability_spectrum.source_limitation_ids = ["lim_verifdynamics"]` ∈ Stage 3 ✓; `sp_intent_vs_literal.source_limitation_ids = ["lim_checklists_recast"]` ∈ Stage 3 ✓; `sp_precision_recall_tradeoff.source_limitation_ids = ["lim_johnson2013"]` ∈ Stage 3 ✓; `sp_reference_noise_ceiling` and `sp_corpus_nontriviality` both `["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓ (recounted: 8 Stage-5 hypotheses, 8 Stage-6 RQs, one-to-one).
4. **Output coverage** — Stage 1's three outputs (per-category P/R/F1; per-category κ vs. ceiling; automatable/human-required/inconclusive classification) are each reachable: output 1 via `sp_operationalizability_spectrum` + `sp_precision_recall_tradeoff`; output 2 via `sp_reference_noise_ceiling`; output 3 via `sp_reference_noise_ceiling` (+ `sp_intent_vs_literal` and `sp_corpus_nontriviality` for the classification's reliability) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, with B0/B-alt framed as sanity-check/rival-explanation comparators embedded in mechanism-tier RQs, never as a beat-the-baseline headline claim.

**What was hardest:** the recurring tension was **not** disagreement about facts (the seed material — especially `paper.md`'s Step 5/6 formal apparatus — is unusually well-specified) but making sure this schema's structure added something `paper.md` didn't already state as a standalone, falsifiable claim. The clearest example is Stage 5's `m_operating_curve_reporting` fix: `paper.md`'s own B0 discussion already gestured at "some categories need no further verifier research," but until the refiner pass forced a second, category-varying-threshold hypothesis, the method's stated key_insight (trade-off curves are category-dependent) had no hypothesis actually testing it — a gap this schema's method↔hypothesis coupling is specifically built to catch.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

Historical rounds above are unchanged. This round enumerates every finding in `stage_review.md` and `taste_audit.md` (no `design_review.md` exists), determines its status against the current deliverables, and applies what was still open. A prior attempt at this pass was interrupted after splitting the old monolithic `pipeline.md` into this file plus `experiment_design.md`; that split was kept, and this round completes the unfinished remainder (paper_draft sync, this record, the Phase Log row).

1. **`stage_review.md` Stage 2 REVISE (nearest-neighbor sentence in Related Work)** → already applied: present in `paper_draft.md` (Related Work opening paragraph and Introduction paragraph 3) and mirrored in `paper_draft.tex`. No change made.
2. **`stage_review.md` Stage 4 REVISE (explicit Falsification condition per RQ)** → already applied: all eight RQ subsections in `paper_draft.md`/`.tex` carry a **Falsification condition** line. No change made.
3. **`stage_review.md` Phase A item 2 (reference-cache integrity)** → already applied in `reference_candidates.jsonl` (158 rows, 12 selected / 146 rejected, all N3 keys present). No change made.
4. **`stage_review.md` Phase A item 5 (Assumptions `Consequence` slots)** → already applied in `paper.md`'s Assumptions table. For `paper_draft.md`: rejected — moot; the draft never contained an assumptions table (design-machinery lives in `paper.md`), and its substantive protections (reference-unstable outcome, inconclusive gating, verifier freeze) already appear in the draft prose.
5. **`stage_review.md` Phase A item 6 / scope-note re-open item (propagate R1 Estimand to `paper_draft.*`)** → was OPEN; applied: added an explicit **Estimand** paragraph (Δ_t = κ_H,t − κ_V,t, unit of analysis, reference population, per-category delegation decision) to `paper_draft.md` Problem Definition, mirrored in `paper_draft.tex`.
6. **`stage_review.md` Phase A item 6 / scope-note re-open item (propagate R2 instrument validation of taxonomy T)** → was OPEN; applied: added the 5-step taxonomy-validation discipline (external grounding, held-out refinement with named merge/split operations, ≥2 annotators at κ ≥ 0.7, confusion-structure inspection, freeze before scale-up) to `paper_draft.md` Methodology → Category-Stratified Scorer, mirrored in `paper_draft.tex`.
7. **`stage_review.md` Phase A item 6 / scope-note re-open item (propagate E3 mechanism analysis)** → was OPEN; applied: added a **Mechanism analysis (supplementary)** paragraph (error-taxonomy coding pass, budget, pre-committed reading) to `paper_draft.md` Experiments after RQ8, mirrored in `paper_draft.tex`; matches the section already present in `experiment_design.md`.
8. **Cross-deliverable consistency check (task item 6)** → two statistics mismatches found and fixed in `paper_draft.md`/`.tex`: RQ2 setup omitted the agent covariate that `paper.md` H2 and `experiment_design.md` specify (added; `experiment_design.md` RQ2 wording tightened from parenthetical to direct statement); RQ4 setup omitted the Holm correction across five categories and the <30-violations force-to-inconclusive rule that `paper.md` E2 and `experiment_design.md` RQ4 specify (added). RQ counts (8=8), all effect floors/margins (0.85/0.80 precision/recall, 0.75 Wilson lower bounds, 0.15 F1 gap, κ ≥ 0.4, Δ_t 0.10 band, 0.05 F1 tolerance, 0.85 precision threshold, 20% non-obvious share, 30 violations/category, ≥1,000 pairs, ≥150/category, 10,000 clustered resamples) verified identical across `paper_draft.md` and `experiment_design.md`; all 8 target hypotheses in `experiment_design.md` left byte-identical to `paper.md`'s.
9. **`taste_audit.md` (verdict 🟢; `surface_stitching` = 1 and `boilerplate` = 1 near-miss notes)** → rejected — no directive: the audit fires no condition and asks for no change; its one substantive concern (hybrid construction as confound) is already discharged by the B-alt invariance design (RQ5) present in all deliverables.

`paper_draft.tex` recompiled successfully after mirroring (`latexmk -pdf`, 14 pages, `paper_draft.pdf` regenerated).
