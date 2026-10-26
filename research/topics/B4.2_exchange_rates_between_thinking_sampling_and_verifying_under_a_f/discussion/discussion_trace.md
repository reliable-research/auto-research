# Auto-Research-Discussion Run — B4.2 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B4.2**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries its own asymmetry sentence, archetype self-audit, formal notation, assumptions table, and pre-committed fallback wording), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and a missing "allocation-moot" gate in the Experiments setup) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure the empirical accuracy-per-dollar exchange rates among three test-time compute levers — chain-of-thought length, sample count, and verifier calls — under a fixed dollar budget in which the verifier's own invocation cost competes with generation, and test whether the resulting frontier's shape is stable across task families that differ in how cheaply they can be verified.
- **Apparent inputs:** a per-query dollar budget ladder; a base LLM with a controllable thinking-token cap; a sampling mechanism; a verifier callable per candidate with its own metered cost; a frozen price sheet; task families spanning exact-match, executable, MCQ, and rubric-graded verifiability.
- **Apparent outputs:** per-configuration accuracy and realized dollar cost; the accuracy-per-dollar Pareto frontier per family/budget with confidence bands; marginal rates of substitution between lever pairs; a cross-family statistical verdict on frontier-shape stability.
- **Closest research areas:** compute-optimal / FLOPs-matched test-time allocation (Snell et al.); sample-then-verify theory (verifier-free suboptimality bounds, optimal-transport verification bounds, Best-of-Majority regret bounds, communication-theoretic reranking laws); CoT-length scaling (inverted-U length/accuracy); step-level token budgeting (Plan-and-Budget); asymmetric verification in web-search agents; repeated-sampling coverage scaling (Brown et al., "Large Language Monkeys").
- **In scope:** measuring exchange rates for existing prompted LLM systems and existing selection/verification methods under one frozen price sheet, using an open-weight model with controllable thinking budget as the primary instrument. **Out of scope:** training new verifiers or allocation policies; guaranteeing generalization across future pricing regimes or untested model families (this is digest N5's `C5`, explicitly flagged `unaddressed` in the seed material itself, not silently dropped here).
- **Confidence: high.** Exactly as with the calibration reference (B5.5), the "repo" here is itself a prior reverse-digest + pre-registered spec (`digest.md` N0–N12 + `paper.md` Steps 0–9) — already internally cross-referenced (challenge ↔ mechanism ↔ RQ ids) and already carrying its own asymmetry/taste self-check (`paper.md` Step 0 and Step 3). Reconstruction risk is low; the risk instead is *redundancy* with `paper.md`'s own Step 6 hypotheses (H1a/H1b/H1c/H2a/H2b/H3a/H3b), which is why Stage 5/6 below are deliberately framed as validating the **measurement instrument's properties** (price-sheet robustness, bin population, coverage/selection identifiability), not re-deriving `paper.md`'s headline hypotheses verbatim.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed per-query dollar budget and three tradeable test-time compute levers — chain-of-thought length, independent sample count, and verifier invocations, each priced in the same dollar unit including the verifier's own token cost — determine the empirical exchange rates among the levers and the shape of the resulting accuracy-per-dollar Pareto frontier, and whether that frontier's shape is stable across task families that differ in how cheaply and reliably candidate answers can be verified.
- `input`: (1) a per-query dollar budget ladder spanning multiple levels; (2) a base LLM with a controllable thinking-token cap L; (3) a sampling mechanism producing N independent generations; (4) a verifier callable per candidate with its own metered cost, offered at multiple strengths including a free (zero-cost) selection option; (5) a frozen per-token price sheet unifying generation and verification cost into one dollar unit; (6) task families with checkable/gradable ground truth spanning different verifiability regimes (exact-match math, executable code, MCQ, rubric-graded open QA).
- `output`: (1) realized dollar cost and accuracy at each point of a (L, N, V) allocation grid, per family and budget level; (2) the non-dominated accuracy-per-dollar frontier per family/budget, with confidence bands; (3) estimated marginal rates of substitution (MRS) between lever pairs along the frontier; (4) a cross-family statistical verdict on whether frontier shape (dominant-lever mix, elbow location, MRS signs) is stable or family-specific.
- `constraints`: task outcomes must be checkable/gradable so accuracy-per-dollar is computable; the three levers' costs must be reducible to one dollar unit under a single frozen price sheet at experiment time; realized cost is stochastic (output length varies), so "matched budget" must be operationalized as a cost bin, not exact equality.
- `objective`: A frontier-shape or exchange-rate claim is accepted only if it is estimated within pre-specified matched-cost bins with bootstrap confidence bands and survives a stated statistical test (a permutation test for cross-family stability, a likelihood-ratio test for lever interactions) at a pre-registered significance threshold; claims about absolute dollar magnitudes are reported separately from claims about frontier shape/ordering, since only the latter is asserted to be robust to price-sheet perturbation.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 classifies the contribution type as `empirical` outright ("what N9's results are designed to validate is a measured phenomenon... obtained by running existing models, existing benchmarks... under a new cost-normalized protocol"), and `paper.md` Step 2 independently arrives at the same classification ("Primary: empirical (measurement study)... Secondary: technical_artifact, strictly in support").

**critique:**
- summary: Strong draft, fully traceable to the seed, but the objective has a real evaluability gap around edge-case cells, and the input field smuggles in a method-level instrument choice.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective doesn't say what happens to a (family, budget) cell in which no evaluated allocation beats a fixed reference allocation by any meaningful margin at matched or lower cost — paper.md's own 'Mandatory controls' section (B0) treats this exact case as load-bearing ('any cell failing this is reported as allocation is moot... and excluded from exchange-rate claims'), but the stage-1 objective as drafted is silent on it. Without naming this case, a reader can't tell whether such a cell would be silently dropped, would count as evidence of constancy, or would block the whole family's claim — three very different outcomes."}`
  - `{severity: minor, field: "input", anti_pattern: "later_stage_content (light method leak)", comment: "Listing 'a free (zero-cost) selection option' as one of the verifier's given strengths is fine (majority vote is a genuinely available, cost-free choice), but the earlier draft also listed an oracle upper bound as a given input before this pass caught it — an oracle-based ground-truth selector is a specific instrument choice for decomposing coverage from selection quality (a method decision), not a resource the problem statement is handed. Keep the input to what's actually given: a verifier with metered cost at multiple strengths, nothing about how selection quality will be isolated."}`
- decision: `move_to_refiner` (both flags are formalize/precision-level fixes using content already in the digest and paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "...; a (family, budget) cell in which no evaluated allocation beats the fixed floor-allocation by a pre-specified margin at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported separately as **allocation-moot**, rather than being silently dropped or scored as evidence of constancy."
- `input` (refined): item (4) tightened to: "a verifier callable per candidate with its own metered cost, offered at multiple strengths including a free (zero-cost) selection option" — the oracle-selector instrument is deliberately left out of `input` (it belongs to Stage 5, where it is introduced as a method component, not a given resource).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Query q from family F. Allocation a = (L, N, V): thinking-token cap L, sample count N, verifier mode V. Price sheet P = (p_in, p_out) converts calls to dollars. Realized cost c(q,a) sums generation-call and verifier-call tokens under P. Budget level B_k defines a matched-cost bin 𝔅_k = {a : |E[c(·,a)] − B_k| ≤ ε·B_k}. Accuracy Acc_F(a) is the grader's mean success rate over F. Determine, per (F, B_k): the non-dominated set over (E[c], Acc_F), the marginal rate of substitution between lever pairs on that set, and whether the set's allocation-mix composition is stable across F."
- `changes_made`: named the allocation-moot exclusion rule explicitly in `objective`; removed an oracle-selector instrument from `input`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Practitioners who deploy LLM reasoning systems under a real, metered dollar budget must decide how to split that budget among thinking longer, sampling more, or paying a verifier to select among candidates — but no existing study prices all three levers, including the verifier's own cost, in one currency and measures their empirical exchange rate.
- `why_it_matters`: Every prior allocation study either fixes the budget's unit to something other than dollars (FLOPs, tokens, sample counts, trajectories) or treats the verifier as a free or externally-priced oracle-like resource, so none of them can answer the question a deploying engineer actually has: given one more dollar, which lever buys the most accuracy right now, at this budget level, on this kind of task? Treating verification as free systematically overstates its apparent value, because a verifier that "wins" against a cheaper alternative might only be winning because its own cost was never charged against the same budget the alternative had to pay from. This is exactly the condition under which a real allocation decision — spend the next dollar on more thinking, more samples, or a verifier call — is currently being made without the instrument to answer it.
- `who_cares`: Engineering teams setting per-query compute budgets for production LLM reasoning systems (coding assistants, math tutors, agentic QA); researchers building compute-optimal allocation policies who need a verifier-cost-aware baseline to evaluate against; the sample-then-verify theory literature, which currently treats verifier feedback as an available oracle-like resource rather than a metered budget competitor.
- `evidence`: `[SnellTTC, OpenReview:4FWAwZtd2n]`'s own motivation frames the allocation problem at "matched FLOPs," never dollars, and evaluates on a single task family (MATH-style reasoning) with no verifier-cost meter. `[AsymVerify, OpenReview:hxL4Uf9tR3]`'s own motivation argues that shifting budget to a cheaper verifier "can yield a much better accuracy-cost trade-off" — but only within one domain (web-search agents) and with cost measured in trajectories/tool calls, not a dollar unit shared with a CoT-length axis. `[BrownMonkeys, arXiv:2407.21787]` shows sampling coverage scales log-linearly with N but explicitly notes selection strategies plateau without a verifier — evidence the sampling lever's realized value is inseparable from a priced selection mechanism, which no existing coverage study meters.

**critique:**
- summary: Well-evidenced and specifically tied to stage 1's cost-unification framing, but coverage of stage 1's fourth output — the cross-family stability verdict — is thin.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is a claim about whether frontier shape transfers across task families or is family-specific — a distinct deliverable from the single-family exchange rate. why_it_matters explains why measuring the exchange rate matters for one deployment decision, but never explains why the cross-family verdict specifically matters, as opposed to a team just measuring its own task family directly. Without that, a reader could reasonably ask 'why should I care whether this transfers to other domains if I only deploy on one' — a real, unaddressed gap."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the cross-family verdict answers a different question than the single-family exchange rate does: running a full matched-cost grid per task family is itself expensive — the grid, samples, and verifier calls this paper measures are exactly what it costs to re-derive an exchange rate from scratch. Whether one measured frontier transfers to a new task family therefore determines whether a team can reuse a previously measured allocation policy when they add a new deployment, or must re-run the entire costly measurement themselves — a distinction invisible from any single-family measurement alone."
- `changes_made`: added the reuse/re-measurement-cost argument connecting the cross-family verdict to a concrete, practitioner-facing decision.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3's own methodology note states each was read at the motivation+method level via a corpus search (5 queries against 11,683 OpenReview papers), not a title-only scan; one (Brown et al.) is a canonical non-corpus anchor, flagged as such rather than fabricated.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation(s) → sub-problem it will motivate):

| work_id | citation | is_potential_baseline | limitation(s) |
|---|---|---|---|
| `rw_snelltc` | Anon., "SnellTTC" (OpenReview:4FWAwZtd2n) | **true** (re-priced in dollars, per `paper.md`'s baseline list) | `lim_snelltc_flops`: denominates budget in FLOPs, single task family (MATH-style), never prices verifier cost in the same currency as generation. Also contributes to `lim_singlefamily_scope` (shared). |
| `rw_verifierfreesuboptimal` | Anon., "VerifierFreeSuboptimal" (OpenReview:beeNgQEfe2) | false (asymptotic theory, not a runnable system) | `lim_verifiertheory_no_cost` (shared, see below): bounds suboptimality in horizon H and sample count n; verifier is an abstract available resource, no metered cost. |
| `rw_planandbudget` | Anon., "PlanAndBudget" (OpenReview:ctspw4CqbS) | false (single-axis token allocator) | `lim_planandbudget_tokenonly`: token-denominated step-level allocation across sub-questions; never trades tokens against additional samples or verifier calls. Also contributes to `lim_singlefamily_scope`. |
| `rw_cotlength` | Anon., "CoTLength" (OpenReview:6QDFsYxtI1) | false (single-axis length/accuracy curve) | `lim_cotlength_singleaxis`: characterizes the inverted-U length-accuracy relationship holding the sampling and verification axes fixed; no cross-lever cost normalization. Also contributes to `lim_singlefamily_scope`. |
| `rw_asymverify` | Anon., "AsymVerify" (OpenReview:hxL4Uf9tR3) | **true** (closest two-lever precedent; protocol borrowed, not its numbers) | `lim_asymverify_narrow`: splits budget between exploration and verification only in one domain (web-search agents), cost measured in trajectories/tool calls rather than a shared dollar unit, and no CoT-length axis at all. Also contributes to `lim_singlefamily_scope`. |
| `rw_otverify` | Anon., "OTVerify" (OpenReview:BBDhQJh6GB) | false (transport-theoretic bound) | `lim_verifiertheory_no_cost` (shared): bounds sub-optimality via transport cost and verifier ROC geometry; verifier feedback still treated as free of its own cost. |
| `rw_bestofmajority` | Anon., "BestOfMajority" (OpenReview:a6CVQpjbXq) | **true** (baseline candidate, re-priced) | `lim_verifiertheory_no_cost` (shared): minimax-optimal regret in coverage, reward-model error, and k; no dollar cost model for the reward-model calls themselves. |
| `rw_rerankinglaws` | Anon., "RerankingLaws" (OpenReview:rhCgizNupi) | false (communication-theoretic asymptotics) | `lim_verifiertheory_no_cost` (shared): asymptotic error-decay laws in hypothesis count N; no notion of a priced selection step. |
| `rw_brownmonkeys` | Brown et al., 2024 (arXiv:2407.21787) | **true** (protocol borrowed as the zero-verifier-cost arm) | `lim_brownmonkeys_coverage_unpriced`: coverage scales with N, but coverage is not deliverable accuracy without a selector, and the selector's cost/quality is never separated from coverage itself. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but one baseline label needs precision, mirroring a classic I/O-mismatch risk.
- comments:
  - `{severity: major, field: "specific_related_works[rw_brownmonkeys].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Brown et al.'s own reported metric is coverage as a function of N — no accuracy-per-dollar framing, no cost meter, no selector built in. Marking it a straightforward baseline risks implying its own published coverage numbers are being compared against, which they are not. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.'"}`
- decision: `move_to_refiner` (a wording-precision fix — the self-consistency/majority-vote *protocol* is still legitimately borrowable as a zero-cost experimental arm, independent of the published coverage curve).

### Refiner pass

- `rw_brownmonkeys.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — Brown et al.'s own reported coverage curves are not compared against. Its **self-consistency / majority-vote selection protocol** is borrowed as a zero-verifier-cost experimental arm (the all-sampling comparator), independent of its published findings."
- `changes_made`: clarified BrownMonkeys' baseline role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`lim_verifiertheory_no_cost`, "no cost model enters the sample-then-verify theory bounds") restates this paper's own core measurement question, already covered end-to-end as mechanism-tier RQs in Stage 6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3** (9 works; 6 distinct limitation ids, one of which — `lim_verifiertheory_no_cost` — is shared across four theory papers, and one — `lim_singlefamily_scope` — is shared across four scope-limited empirical/allocation papers).

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's `C1`–`C4`, `C5` deliberately excluded — see note below):

- **`sp_cost_commensuration`** — *description:* Reduce three differently-metered levers — thinking tokens priced as output, extra samples multiplying both input and output cost, verifier calls consuming their own input (candidate) and output (judgment) tokens — to one fair dollar unit before any cross-lever comparison is meaningful. *why_it_is_a_problem:* without a shared currency, any claim that one lever "buys more" than another is an artifact of an implicit, unstated price assumption rather than a real finding. *technical_challenge:* the three levers are priced at different granularities and asymmetries (input vs. output rates differ, and a verifier's "candidate" tokens are the other lever's output), so building a single per-call dollar meter that treats generation and verification symmetrically is itself a nontrivial accounting design, not a lookup. *source_limitation_ids:* `["lim_snelltc_flops", "lim_verifiertheory_no_cost"]`.
- **`sp_lever_interaction`** — *description:* Determine how the marginal value of each lever depends on the settings of the other two — e.g., verifier value at N=1 vs. large N; CoT length changing what a verifier must read. *why_it_is_a_problem:* if lever values are assumed additive when they actually interact, an exchange rate measured at one point of the grid is silently wrong everywhere else, undermining any claim to have measured "the" exchange rate. *technical_challenge:* separating interaction from noise requires a combinatorial grid, not a one-lever-at-a-time sweep, and a chosen functional form for the interaction terms that isn't guaranteed to match the true response surface. *source_limitation_ids:* `["lim_asymverify_narrow"]` (the closest prior interaction structure — a two-lever explore/verify split — studies interaction between only two of the three levers, in one domain).
- **`sp_verifiability_heterogeneity`** — *description:* Establish whether the efficient allocation mix differs by task family's "checkability" rather than assuming one universal exchange rate. *why_it_is_a_problem:* a single-family measurement licenses no claim about whether the found allocation transfers; treating it as universal without testing would overgeneralize a domain-specific artifact. *technical_challenge:* verifiability differences are confounded with everything else that differs between task families (difficulty, answer format, grader noise), so isolating "verifiability class" as the explanatory factor requires a family set spanning the verifiability spectrum while holding the measurement protocol identical. *source_limitation_ids:* `["lim_singlefamily_scope"]`.
- **`sp_stochastic_cost_matching`** — *description:* Compare allocations at a genuinely matched dollar cost when the realized cost of any given (L,N,V) setting is itself a random variable. *why_it_is_a_problem:* without this, an apparent accuracy difference between two allocations could just be a cost difference in disguise, invalidating every frontier and MRS claim built on "matched budget" comparisons. *technical_challenge:* nominal settings only target, not fix, a budget, and the (L,N,V) × budget-level × family grid is already combinatorially large before adding cost-bin pruning and regression adjustment on realized cost. *source_limitation_ids:* `["__novel__"]` — no cited work needs to solve this because none of them runs a stochastic-cost, multi-lever grid in the first place.
- **`sp_selection_vs_coverage_confound`** — *description:* Separate how much of a verify-heavy allocation's apparent accuracy gain is due to having more candidates to choose from (coverage) versus the verifier's own selection quality. *why_it_is_a_problem:* without separating these, a verifier's measured "value" could really be free coverage gains from extra sampling that any selector — even a random one — would capture, misattributing coverage's value to the verifier lever. *technical_challenge:* coverage and selection quality are both functions of N and are not separable from the accuracy number alone; isolating them requires a control condition run at the same cost as the verifier condition. *source_limitation_ids:* `["lim_brownmonkeys_coverage_unpriced"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's four outputs), but one pair of sub-problems risks reading as the same underlying issue twice, and the deliberate exclusion of `C5` needs to be stated, not just silently absent.
- comments:
  - `{severity: minor, field: "sp_lever_interaction / sp_selection_vs_coverage_confound", anti_pattern: "overlap", comment: "Both concern how the verifier's value depends on N, which can read as the same sub-problem stated twice. They are genuinely distinct — one is a functional-form question (how large is the N×V interaction term, i.e. how much does the verifier's marginal value change with N), the other is a causal-identification question (is an observed verify-heavy accuracy gain actually attributable to verification, or fully explained by the extra candidates its dollars could have bought instead) — but the descriptions don't make that distinction explicit enough."}`
  - `{severity: major, field: "summary", anti_pattern: null, comment: "Digest N5's C5 (cross-model / cross-pricing generalization) is not represented by any sub-problem, and its absence isn't explained anywhere in this stage's output. C5 is explicitly marked `unaddressed` in digest N6 and is treated as a stated external-validity threat in paper.md (t4), not a gap this paper's design closes — but a sub-problems stage that silently drops one of the five listed challenges without comment reads as an oversight rather than a deliberate scoping decision."}`
- decision: `move_to_refiner` (both are precision/documentation fixes on content already established in the digest — no new sub-problem or limitation is being invented).

### Refiner pass

- `sp_lever_interaction.technical_challenge` sharpened to end with: "...this is a **functional-form** question — how large the interaction terms are and in which direction — not a question about whether an observed effect is real or a byproduct of something else; that latter question is `sp_selection_vs_coverage_confound`'s job."
- `sp_selection_vs_coverage_confound.technical_challenge` sharpened to end with: "...this is a **causal-identification** problem distinct from the interaction question above: even a verifier with a measurably nonzero interaction term could, in principle, be adding zero value beyond what its dollars would have bought as extra samples — identification, not magnitude, is what's at stake here."
- `summary` (stage-level, refined) — added a closing sentence: "A fifth challenge from the digest — generalization across models and future pricing regimes (`C5`) — is deliberately **not** one of these five sub-problems: it is not a gap this paper's design closes but a stated external-validity limitation (mitigated only partially, by a multi-model replication in the scale-up stage), carried forward honestly into the paper's Limitations rather than manufactured into a sub-problem with no real solution attached."
- `changes_made`: made the interaction-vs-identification distinction explicit in both `technical_challenge` fields; added an explicit statement of why `C5` has no corresponding sub-problem.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 4 sourced from Stage 3 limitations, 1 `__novel__` with a stated decisive-component justification; `C5` explicitly scoped out with reasoning, not silently dropped).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_unified_cost_meter`** → targets `sp_cost_commensuration`. *proposed_approach:* A per-call accounting layer logging input/output token counts for every generation and verifier call from the inference engine's usage fields, converting to dollars via one frozen price sheet, with a parallel provider-neutral normalized-token-unit account kept for price robustness, attributing each dollar to whichever lever produced it. *key_insight:* cost commensuration cannot be solved analytically — there is no "true" exchange rate between an input and an output token, or between a generation call and a verifier call — but it can be turned into an explicit, checkable accounting convention plus a stated sensitivity band, rather than an implicit assumption baked silently into whichever metric happens to get reported. *hypotheses:* `["The frontier-shape ordering (which family is most verify-heavy) is preserved under a ±3x perturbation of the input/output and generator/verifier price ratios for at least the majority of tested (family × budget) cells — i.e., the meter's qualitative conclusions are not an artifact of one specific price sheet, even though absolute dollar magnitudes are."]`
- **`m_interaction_surface_model`** → targets `sp_lever_interaction`. *proposed_approach:* Fit a single response-surface model (accuracy as a function of L, N, V-mode, and realized cost, with explicit N×V and L×V interaction terms) across the full grid, rather than sweeping one lever at a time; test interaction terms via likelihood-ratio tests against the additive (no-interaction) model. *key_insight:* if lever values were additive, measuring each lever's exchange rate once would suffice everywhere on the grid; the interaction terms are exactly the test of whether that shortcut is valid, so the same fitted surface that estimates the frontier also directly falsifies (or confirms) the additive-shortcut assumption. *hypotheses:* `["The N×V interaction term is statistically significant (likelihood-ratio test, Holm-corrected) on at least one task family, meaning a verifier's exchange rate measured at one sample count N does not transfer unchanged to a different N.", "The magnitude of the L×V interaction term is smaller than the N×V interaction term's magnitude in a majority of tested cells where both are significant — i.e., verifier value interacts more strongly with how many candidates it screens than with how long each candidate is."]`
- **`m_verifiability_stratified_replication`** → targets `sp_verifiability_heterogeneity`. *proposed_approach:* Run the identical matched-cost grid protocol (same meter, same bins, same statistical tests) across four task families pre-ordered a priori by verifiability class (executable code > exact-match math > MCQ > rubric-graded open QA), then test cross-family equality of the efficient-set allocation-mix composition via a permutation test on Aitchison distance. *key_insight:* holding the measurement protocol byte-for-byte identical across families is what makes a cross-family difference attributable to verifiability rather than to some uncontrolled difference in how each family was measured. *hypotheses:* `["The permutation test rejects cross-family equality of allocation-mix composition for at least 2 of 6 family pairs at Holm-corrected α=0.05.", "The verify-heavy dollar share at each family's max-accuracy efficient point follows the pre-registered verifiability ordering (code ≥ math ≥ MCQ ≥ open QA), with the code-vs-open-QA gap ≥0.10 absolute dollar share."]`
- **`m_matched_cost_binning`** → targets `sp_stochastic_cost_matching`. *proposed_approach:* Compute each grid configuration's expected cost from pilot token statistics, retain only configurations whose expected cost falls within a pre-specified tolerance band of each target budget level, and regression-adjust the fitted accuracy-cost surface on each query's realized (not nominal) cost within its bin. *key_insight:* because output length is stochastic, no configuration can be assigned an exact cost in advance — the fix is not a smarter length-control mechanism but an explicit acceptance criterion (the bin) plus a post-hoc adjustment, so "matched budget" becomes a measured property of the data actually collected, not an assumption about the settings requested. *hypotheses:* `["At least 8 grid configurations populate each matched-cost bin per family and budget level using the pre-specified ±10% tolerance, without needing the pre-declared ±15% widening amendment.", "Frontier confidence bands computed with realized-cost regression adjustment are narrower than bands computed from nominal-cost grouping alone, on a majority of tested bins — demonstrating the adjustment step is load-bearing, not cosmetic."]`
- **`m_coverage_selection_decomposition`** → targets `sp_selection_vs_coverage_confound`. *proposed_approach:* For every verify-heavy efficient allocation (L, N, V>0), run a budget-matched majority-vote control at the same cost bin that reallocates the verifier's dollars into additional samples (L, N′, 0), plus a zero-cost ground-truth oracle-selection arm at the same (L,N); assert a verifier's measured value only where it beats its budget-matched majority-vote control. *key_insight:* coverage and selection quality are both functions of the same generated pool, so the only way to attribute an accuracy gain specifically to the verifier — rather than to the extra candidates its dollars could have paid for instead — is a control that spends the identical dollars on more candidates and no verifier at all. *hypotheses:* `["The verifier-lever accuracy gain over its budget-matched majority-vote control is statistically significant (paired bootstrap, Holm-corrected p<0.05) for the strong-verifier condition on at least one task family — i.e., at least one measured 'verifier value' finding survives this control rather than being fully explained by reallocated coverage.", "The oracle-selection arm's accuracy exceeds the strong verifier's accuracy at matched (L,N) in every tested cell, bounding realizable verifier value strictly below the coverage ceiling."]`

**critique:**
- summary: Every method has a real mechanism and the hypotheses are mostly falsifiable with stated thresholds — but one hypothesis is a near-tautology that would pass by construction and doesn't test anything about the verifier.
- comments:
  - `{severity: major, field: "m_coverage_selection_decomposition.hypotheses[1]", anti_pattern: "tautology", comment: "'The oracle-selection arm's accuracy exceeds the strong verifier's accuracy at matched (L,N) in every tested cell' is true almost by construction: the oracle selects using ground-truth labels over the same candidate pool the verifier scores, so it cannot do worse than any non-oracle selector operating on strictly less information over the same candidates — this is a property of the oracle's definition, not a finding about the verifier being evaluated. Per the stage-6 rigor filter ('no tautologies — if an RQ would pass by construction, discard it and tighten'), the discipline needs to be applied here too: the genuinely falsifiable, sub-problem-relevant question is whether the *gap size* between oracle and verifier accuracy shrinks or stays constant as N grows, which is an actual claim about how much headroom the verifier lever leaves on the table."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_coverage_selection_decomposition.hypotheses[1]` replaced with: "The oracle-minus-strong-verifier accuracy gap at matched (L,N) shrinks — rather than staying flat or widening — as N increases on at least one task family, i.e., additional candidates make the verifier's realized selection quality converge toward the coverage ceiling rather than leaving a constant or growing amount of realizable accuracy on the table."
- `changes_made`: replaced a near-tautological ordering claim with a falsifiable claim about the trend of the oracle–verifier gap.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **9 hypotheses total** (1 + 2 + 2 + 2 + 2 across the five methods respectively), deliberately weighted toward instrument-validity claims (price-sheet robustness, bin population, adjustment load-bearingness, oracle-gap trend) that `paper.md`'s own Assumptions/threats tables (`A2`, `A5`, `t1`, `t2`) treat as mitigations to build into the protocol but never state as falsifiable hypotheses in their own right — this is the deliberate redundancy-avoidance move flagged in the seed brief above.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against `study_type=empirical`):**
- **Mechanism-tier: 9 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. All baselines below are sanity-check comparators or ceilings, never competitors to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- MATH-500 (math, exact-match) — pilot family; cheap and unambiguous grading makes it the right family to validate the cost meter and fit the first interaction surface before scaling up.
- HumanEval+ / a LiveCodeBench slice (code, executable) — the most verify-heavy family under the pre-registered ordering, needed so the verifiability-stratified replication and the coverage/selection decomposition both have a family where the verifier lever plausibly has the most headroom to show anything at all.
- GPQA-Diamond (MCQ, option match) — an intermediate anchor on the verifiability ordering, needed so the ordering claim isn't just a two-point comparison between math and open QA.
- FRAMES / a SimpleQA subset (open QA, rubric-graded) — the least verifiable family; needed both to test whether the verifiability ordering holds at its weakest-signal end, and because it's the family where the coverage/selection confound is sharpest (the rubric judge is itself a verifier-like instrument).

`baselines` (sanity-check comparators/ceilings, not outcome-tier competitors):
- Fixed floor allocation (L=512, N=1, V=0) — the necessary "why bother allocating at all" gate; every lever-value claim is reported relative to this floor, and the allocation-moot exclusion rule from Stage 1's objective is defined against it.
- Budget-matched majority-vote control (reallocates the verifier's dollars into more samples) — the specific control `m_coverage_selection_decomposition` needs.
- Difficulty-conditioned compute-optimal allocator (re-priced in dollars, per SnellTTC's framing) — *justification, round 1:* "an existing allocation policy from the literature, re-priced."
- Zero-cost ground-truth oracle selector — the upper-bound arm for `m_coverage_selection_decomposition`, explicitly a sanity ceiling, not a competitor.

`research_questions` (9, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_price_robustness` | `sp_cost_commensuration` | "The frontier-shape ordering (which family is most verify-heavy) is preserved under a ±3x perturbation of the input/output and generator/verifier price ratios for at least the majority of tested (family × budget) cells — i.e., the meter's qualitative conclusions are not an artifact of one specific price sheet, even though absolute dollar magnitudes are." |
| `rq_nv_interaction` | `sp_lever_interaction` | "The N×V interaction term is statistically significant (likelihood-ratio test, Holm-corrected) on at least one task family, meaning a verifier's exchange rate measured at one sample count N does not transfer unchanged to a different N." |
| `rq_interaction_magnitude_ordering` | `sp_lever_interaction` | "The magnitude of the L×V interaction term is smaller than the N×V interaction term's magnitude in a majority of tested cells where both are significant — i.e., verifier value interacts more strongly with how many candidates it screens than with how long each candidate is." |
| `rq_crossfamily_shape` | `sp_verifiability_heterogeneity` | "The permutation test rejects cross-family equality of allocation-mix composition for at least 2 of 6 family pairs at Holm-corrected α=0.05." |
| `rq_verifiability_ordering` | `sp_verifiability_heterogeneity` | "The verify-heavy dollar share at each family's max-accuracy efficient point follows the pre-registered verifiability ordering (code ≥ math ≥ MCQ ≥ open QA), with the code-vs-open-QA gap ≥0.10 absolute dollar share." |
| `rq_bin_population` | `sp_stochastic_cost_matching` | "At least 8 grid configurations populate each matched-cost bin per family and budget level using the pre-specified ±10% tolerance, without needing the pre-declared ±15% widening amendment." |
| `rq_adjustment_loadbearing` | `sp_stochastic_cost_matching` | "Frontier confidence bands computed with realized-cost regression adjustment are narrower than bands computed from nominal-cost grouping alone, on a majority of tested bins — demonstrating the adjustment step is load-bearing, not cosmetic." |
| `rq_verifier_beats_coverage_control` | `sp_selection_vs_coverage_confound` | "The verifier-lever accuracy gain over its budget-matched majority-vote control is statistically significant (paired bootstrap, Holm-corrected p<0.05) for the strong-verifier condition on at least one task family — i.e., at least one measured 'verifier value' finding survives this control rather than being fully explained by reallocated coverage." |
| `rq_oracle_gap_shrinks` | `sp_selection_vs_coverage_confound` | "The oracle-minus-strong-verifier accuracy gap at matched (L,N) shrinks — rather than staying flat or widening — as N increases on at least one task family, i.e., additional candidates make the verifier's realized selection quality converge toward the coverage ceiling rather than leaving a constant or growing amount of realizable accuracy on the table." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E3 grid parameters and Assumptions table as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces verbatim to a Stage 5 hypothesis, but one baseline's justification is a provenance note instead of a reason tied to a specific RQ.
- comments:
  - `{severity: major, field: "baselines[Difficulty-conditioned compute-optimal allocator]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset/baseline actually stresses the hypothesis')", comment: "'An existing allocation policy from the literature, re-priced' restates where the baseline comes from, not which RQ needs it or why comparing against it would mean something for an empirical, non-outcome-tier study."}`
- decision: `move_to_refiner`.

### Refiner pass

- `baselines` entry replaced: "Difficulty-conditioned compute-optimal allocator (SnellTTC policy, re-priced in dollars) — *justification:* this is the one prior allocator that already conditions its choice on an interaction-like signal (per-prompt difficulty), so comparing its FLOPs-native decision boundary against this paper's dollar-metered interaction surface (`rq_nv_interaction`, `rq_interaction_magnitude_ordering`) tests whether a difficulty-conditioned policy derived without a cost meter happens to land near the dollar-optimal frontier, or whether re-pricing reveals it was tuned for a different currency than the one that matters at deployment."
- `changes_made`: gave the SnellTTC baseline a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_matters`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — every Stage 4 `source_limitation_ids` entry ∈ Stage 3 limitation ids (or the `["__novel__"]` sentinel) ✓; every Stage 5 `target_sub_problem_id` ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (per-configuration cost/accuracy, the frontier, the MRS estimates, the cross-family stability verdict) are each reachable: (1)+(2) via `sp_cost_commensuration` + `sp_stochastic_cost_matching`; (3) via `sp_lever_interaction`; (4) via `sp_verifiability_heterogeneity`, with `sp_selection_vs_coverage_confound` guarding the *validity* of any verify-heavy reading that feeds into (4) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** the recurring tension was **not disagreement about facts** (the seed material — especially `paper.md`'s own Assumptions table and pre-committed fallback wording — is unusually well-specified) but **avoiding redundancy with `paper.md`'s own Step 6**, which already states H1a/H1b/H1c/H2a/H2b/H3a/H3b as the paper's headline empirical predictions. Stage 5/6 here were repeatedly steered toward genuinely distinct, instrument-validity-tier claims — price-sheet robustness, matched-cost bin population, whether the realized-cost adjustment is load-bearing, and whether the oracle–verifier gap shrinks with N — that `paper.md`'s own Assumptions/threats sections (`A2`, `A5`, `t1`, `t2`) gesture at as things the protocol should guard against, but never states as falsifiable hypotheses in their own right.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists for this topic). Every finding was enumerated and its status verified against the current deliverables before deciding whether any action remained. Historical rounds above are untouched.

1. **stage_review.md → Stage 2 REVISE (nearest-neighbor sentence missing from Related Work opening)** — verified already applied: `paper_draft.md` line "The closest prior work to this paper is the study of asymmetric verification for web-search agents..." opens the Related Work section, and the two-lever paragraph restates the delta (single domain, trajectory-priced, no CoT-length axis). No change needed.
2. **stage_review.md → Stage 4 REVISE (allocation-moot exclusion rule absent from Experimental Setup baselines)** — verified already applied in `paper_draft.md`/`.tex` Baselines paragraph. **Completed further in this round:** the rule's "pre-specified margin" was quantified inline as ≥5 accuracy percentage points (the value `paper.md`'s pre-registered B0 gate fixes), in both the Formal Setup and Baselines paragraphs of `paper_draft.md` and `paper_draft.tex`, and in `experiment_design.md`'s fixed-floor baseline row — the margin's value had remained "an earlier stage's fine print," which is the exact defect class the Stage 4 finding named. No other number invented; the value is copied from `paper.md` B0.
3. **stage_review.md → Phase A re-run, 5 REVISE items (digest N12 status line; 9 missing N3 cache records; A1–A7 `consequence` column; R1 Estimand sentence; R2 5-step instrument validation ×2; INCONCLUSIVE power rule)** — verified already applied in `digest.md`/`paper.md` (spot-checked: A1–A7 table has the `consequence` column; the Power/INCONCLUSIVE rule paragraph exists in `paper.md` Step 6; `experiment_design.md` carries the INCONCLUSIVE rule in its design constants). No change needed.
4. **stage_review.md → Phase A item 2 residual (9 cache records lacking PDF/digest)** — verified resolved per `pipeline.md` row "reference-cache integrity ... RESOLVED" (all 9 fetched, digested, `verified.id_resolves=true`). No change needed.
5. **stage_review.md → Phase A item 7 pre-Phase-E to-do (concede-and-differentiate paragraph for method-twin `ComputeAccuracy251224776`)** — verified already applied: "Cross-model compute-accuracy frontiers" paragraph present in `paper_draft.md` and `.tex`, cited via `\citep{ComputeAccuracy251224776}`. No change needed.
6. **stage_review.md → Phase G [major] (zero `\cite` commands, no `refs.bib`)** — verified fixed: 10 unique keys cited in `paper_draft.tex`, all resolving to `refs.bib` (15 entries, script-generated by `gen_refs_bib.py`) and to `selected` cache records; compile shows zero undefined citations. No change needed.
7. **taste_audit.md (original + Phase H re-audit)** — 🟢 verdict, no condition fired, no action items issued. Nothing to apply.
8. **pipeline.md open to-dos** — rejected as out of scope for a revision pass, not open review findings: Phase B/C require compute unavailable in this environment; the 5 `adjacent` uncited refs are explicitly "no action unless a future pass pulls their claims into prose"; the cross-model generalization limitation is deliberately carried in the Conclusion.

**Cross-deliverable consistency check (this round):** RQ count 9 = 9 between `paper_draft.md` Experiments and `experiment_design.md`; all shared constants match (2-of-6 family pairs at Holm-corrected α=0.05; 0.10 absolute dollar-share gap; ±10%→±15% bin tolerance; ≥8 configurations/bin; 10,000 bootstrap resamples / permutations; n≥300 pilot / n≥500 Stage-2; power ≥0.8 on a 5pp reference contrast). The one gap found — the unquantified floor margin — is fixed as item 2 above. Target-hypothesis fields in `experiment_design.md` left byte-identical to their Stage 5/`pipeline.md` verbatim sources; none paraphrased or touched.

**Files changed this round:** `paper_draft.md` (2 edits), `paper_draft.tex` (2 edits, recompiled — exit 0, 14 pages, zero undefined citations), `experiment_design.md` (1 edit), plus this appended section and one `pipeline.md` Phase Log row.
