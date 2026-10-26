# Discussion Trace — T5.2 (full Stage 1-6 round-by-round record)

> Extracted verbatim from `pipeline.md` (previously embedded there under "# Auto-Research-Discussion Run" through "## Cross-stage consistency check"), per the `auto-research-discussion` skill's updated "Final deliverables" spec: the discussion trace is its own standalone artifact, separate from `pipeline.md`'s phase-gate log. This is the audit trail — every draft version, every critique (comments, severities, resolution), every decision, every refiner pass — that fed `paper.md` and `paper_draft.md`. See `experiment_design.md` for the standalone Stage 6 protocol rendered as a runnable spec.

# Auto-Research-Discussion Run — T5.2 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.2**. Round cap: 5/stage. Five of six stages converged in 1 critic round + 1 refiner pass; **Stage 4 (Sub-Problems) took 2 critic rounds** because round 1's critique surfaced a genuine coverage gap large enough to require a re-proposed draft, not a refiner-level patch (per `discussion_loop.md`'s rule that major fixes needing new structure are a proposer job, not a refiner job).
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing bridge sentence between the two Related-Work threads, and an under-explained result direction in the design-specificity RQ) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure which classes of design properties (naming/layering conventions, cross-cutting boundaries, temporal/ordering properties) an existing, unmodified test suite is *structurally* incapable of expressing, using constructed design mutants — behaviorally equivalent but convention-violating program variants — as a mechanical probe.
- **Apparent inputs:** a subject program with a mature, unmodified test suite; a machine-readable per-project rule set for naming/layering/temporal conventions (Checkstyle/ArchUnit/trace rules); a mutation-operator catalog per constraint category; an independently-generated differential input corpus.
- **Apparent outputs:** an admitted, dual-oracle-certified design-mutant set per category; kill/survive verdicts from the unmodified suite (and from a matched convention-neutral control); a per-category survival profile contrasted against the suite's ordinary functional mutation score; a determination of whether any observed gap is structural (test-proof) or merely quantity-limited (fixable by adding more functional tests).
- **Closest research areas:** mutation-testing adequacy theory (Jia & Harman, 2011); oracle-quality/checked-coverage work (Schuler & Zeller, 2011); architecture-conformance checking (Murphy et al.'s Reflexion models); LLM-code-test-discrimination work that treats tests as an oracle for functional correctness only (BinaryMatrixTests, UTRL, AutoCodeBench, VERINA, DefectFocusedReview, SelfRefMAS).
- **In scope:** measuring mature, already-existing test suites on real subject systems against *mechanically checkable* design conventions. **Out of scope:** tacit/undocumented conventions (digest C4); building a new mutation-testing tool as the primary contribution (the instrumentation is a secondary, technical-artifact deliverable, not the headline claim); LLM-authored-code review as a downstream application.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) — `paper.md` already carries its own formal notation (Step 5), assumptions with failure/detection pairs (A1–A6), pre-registered experiments with fallback wordings (E1–E3), mandatory baselines (B0, B-alt), a walking skeleton (Step 9), and its own taste self-audit (Step 3) that already rejected a Bridge/Synthesis framing before this run started. The risk here is not reconstruction, it's **redundancy with `paper.md`'s own Step 5/6** — stage 5/6 below are framed to add instrument-validity claims (equivalence-oracle mislabel rate, checker precision, split-half reliability) that `paper.md`'s Assumptions section gestures at (A3, A4) but never states as falsifiable Stage-5 hypotheses in their own right, mirroring exactly the kind of value-add the B5.5 run found in its own mature seed.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a subject program with a mature, unmodified test suite, and a machine-readable catalog of the program's naming/layering/temporal design conventions, determine which categories of behavior-preserving convention violations the suite structurally fails to detect, using constructed design mutants — programs that violate a convention while remaining indistinguishable in behavior from the original under a bounded equivalence check — and contrasting the resulting per-category survival rate against the suite's ordinary functional mutation score.
- `input`: (1) subject program P with existing unmodified test suite T; (2) a per-project rule set of machine-readable design conventions (naming/layering/temporal); (3) a mutation-operator catalog producing candidate variants per convention category; (4) an independently-generated differential input corpus disjoint from T.
- `output`: (1) an admitted design-mutant set per category, each certified functionally equivalent (bounded) and convention-violating by oracles independent of T; (2) per-mutant kill/survive verdicts from T; (3) a per-category Design-Mutant Survival Rate (DMSR) profile contrasted with T's Functional Mutation Score (FMS).
- `constraints`: mutant admission requires two oracles independent of T — a bounded functional-equivalence check via an independent differential corpus, and a convention-violation check via a machine-readable rule checker; only mechanically-checkable (non-tacit) conventions are in scope; equivalence is bounded by a stated input budget, never claimed as absolute/undecidable equivalence.
- `objective`: a category is reported as a genuine blind spot only if its DMSR clears a pre-registered gap over the suite's functional survival rate.
- `study_type`: `empirical` — stated explicitly, matching digest N12's `value: "empirical"` and the seed's own framing of mutation testing as a measuring instrument, not a proposed fix.

**critique:**
- summary: The input/output/constraints are well specified and evidence-traceable to `paper.md`'s Step 5 notation, but the `objective` has a real evaluability gap that `paper.md`'s own Assumptions section (A3, and the B-alt control) already shows is live.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective as drafted would call a category a 'blind spot' purely from a DMSR-over-FMS gap. But paper.md's own A3 states the equivalence oracle only gives *bounded* equivalence with a stated mislabel-rate risk, and paper.md's own B-alt control exists precisely because a DMSR gap could be produced by the generic equivalent-mutant effect (equivalent mutants of any kind being hard to kill) rather than by convention-violation specifically. An objective that doesn't name these two alternative explanations as things the claim must survive is not fully evaluable — a reader can't tell a genuine blind spot from an oracle artifact or from generic equivalent-mutant fragility."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "paper.md's own Claim 3 and its E3/augmentation-arm design distinguish a *structural* (test-proof) blind spot from a *quantity-limited* one (fixable by adding more, stronger functional tests) — this is a fourth, distinct output the draft's three-item output list doesn't promise, even though the seed material treats it as a headline claim, not an afterthought."}`
- decision: `move_to_refiner` (both flags are formalize-level: the fixes use content `paper.md` already states — A3, B-alt, and the augmentation arm — no new content needs to be invented).

### Refiner pass

- `output` (extended, 4th item added): "...(4) a determination of whether an observed per-category gap is *structural* (persists under a capability-matched test-suite augmentation) or *quantity-limited* (closes once functional-test strength is increased)."
- `objective` (refined): "A category is reported as a genuine, design-specific, structural blind spot only if, jointly: (a) its DMSR clears a pre-registered gap over the suite's functional survival rate; (b) that gap is not reproduced by a matched, convention-neutral control of the same operator family (ruling out the generic equivalent-mutant effect); and (c) the gap does not close under a capability-matched test-suite augmentation (ruling out a quantity-limited explanation). A category failing (a) is reported as *not classifiable as a blind spot*; failing (b) alone is reported as *equivalent-mutant-driven, not design-specific*; failing (c) alone is reported as *quantity-limited, not structural* — none of these three weaker outcomes is silently folded into a positive blind-spot claim."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5 notation verbatim): "Program P, suite T, mutant m, category c ∈ {NAM, LAY, TMP}. K_T(m) ∈ {0,1} kill; EQ_B(m) bounded functional equivalence at budget B; V(m) violation flag from an independent rule checker. Admitted set D_c = {m : op(m)∈c, EQ_B(m)=1, V(m)=1}; matched neutral set N_c = {m : op(m)∈c, EQ_B(m)=1, V(m)=0}. DMSR_c = |{m∈D_c : K_T(m)=0}| / |D_c|; FMS/FSR from the suite's default functional mutants. The object of study is the joint behavior of (DMSR_c − FSR), (P(K_T=1|D_c) − P(K_T=1|N_c)), and ΔDMSR_c under a capability-matched augmentation."
- `changes_made`: added the fourth output item; tightened `objective` into a three-conjunct evaluability condition; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: "Passes the existing test suite" is increasingly used as the de facto gate for accepting a coding agent's change, but no one has measured which classes of design properties — as opposed to functional behavior — that gate is structurally blind to.
- `why_it_matters`: If a green suite is treated as evidence that an agent-authored change respects a codebase's design intent (naming conventions, layering boundaries, event ordering) when in fact whole categories of design violation are invisible to any amount of functional testing, teams relying on this gate are exposed to design decay that no additional functional test can catch — and, worse, cannot currently tell which categories are genuinely invisible versus incidentally caught (e.g., a naming violation caught only because a test happens to assert a literal identifier string). Existing mutation-testing theory formalizes adequacy purely behaviorally — the equivalent-mutant problem, as classically defined, is about behavior, full stop — so this paper's dual-oracle admission procedure and resulting per-category profile is the only account of design-adequacy that is *measured through the suite itself*, as opposed to checked by separate machinery (contrast: architecture-conformance tools like Reflexion models build wholly separate apparatus precisely because they assume the suite cannot check this).
- `who_cares`: engineering teams and platform designers deciding whether "tests pass" is sufficient gating for autonomous coding-agent changes; researchers building coding-agent guardrails who currently treat green CI as ground truth; mutation-testing researchers extending adequacy theory beyond functional correctness.
- `evidence`: `[SelfRefMAS, OpenReview:Cug26Y0RlT]`'s own framing explicitly names the circularity risk — "the code can hallucinate, the tests can hallucinate" — direct evidence that practitioners in LLM-code pipelines already worry about self-validating loops; `[VERINA, OpenReview:0A4Uf88pog]`'s need for formal specs *in addition to* a test suite is indirect evidence that tests under-express intended behavior; and the digest's own corpus search (N3, 11,683 papers) found no work directly studying design-constraint mutation, itself evidence the question is open.

**critique:**
- summary: Motivation is stake-specific and evidence-backed, but it covers only Stage 1's original three outputs — the fourth output (structural-vs-quantity-limited) confirmed by Stage 1's refiner has no matching argument for why it matters practically.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's newly-confirmed output (4) is a structural-vs-quantity-limited determination, not just an existence claim. The current why_it_matters explains why a blind spot mattering at all, but never explains why distinguishing 'test-proof' from 'fixable by adding more tests' matters in practice — a reader could reasonably ask 'once you know there's a gap, why not just add more/better tests and be done', and the motivation as drafted doesn't preempt that."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, if the gap could simply be closed by investing in more or better functional tests, the practical remedy is routine test-suite investment — no new gating discipline is required, and the finding would be a resourcing problem, not a design-adequacy one. What makes this worth *measuring* rather than assumed either way is the live possibility that the gap is structural: functional tests, however numerous or strong, are not built to check convention adherence at all, so no realistic increase in test-suite investment would close it. Telling these two futures apart — 'buy more tests' versus 'a fundamentally different gate is needed for design compliance' — is exactly what the capability-matched augmentation check is for, and it is invisible to a single DMSR-vs-FMS snapshot that stops at existence."
- `changes_made`: added the structural-vs-quantity-limited coverage argument.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are **specific (deep) tier** — six are corpus-grounded (`[GROUNDED:corpus]`, from the local 11,683-paper OpenReview corpus per digest N3), three are canonical non-corpus SE references retained because the corpus has essentially no classic mutation-testing/architecture-conformance work (per digest N3's own search-honesty note). No landscape-only mentions are padded in; per the no-fabrication rule, nothing beyond these nine is invented.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_binarymatrix` | Anon., "How Many Code and Test Cases Are Enough?" (OpenReview:RomWar2kVN) | false | Models wrong-programs × trusted-tests as a binary matrix whose rank bounds discrimination power — but every row is a *functionally wrong* program by construction; a functionally-equivalent-but-design-violating variant is an all-pass row, invisible to a rank-of-failures analysis. |
| `rw_utrl` | Anon., "Learning to Generate Unit Test via Adversarial RL" (OpenReview:VqjNYF9nbP) | **true** | Trains test generators with a discrimination reward that scores a suite purely by its ability to reject *functionally wrong* programs; a convention-violating-but-behaviorally-identical mutant is, by the reward's own construction, correctly accepted — it cannot express design conformance at all. |
| `rw_defectfocused` | Anon., "Towards Practical Defect-Focused Automated Code Review" (OpenReview:mEV0nvHcK3) | false | Reframes review around merge-request-level *key bug detection* — still a functional-defect target; does not model naming/layering/temporal conventions as a separate category that review could miss. |
| `rw_verina` | Anon., "VERINA: Benchmarking Verifiable Code Generation" (OpenReview:0A4Uf88pog) | false | Needs formal specs and proofs *in addition to* a test suite to pin down intended behavior — indirect evidence tests under-express properties, but treated as a benchmark-scope choice, not a measured account of *which* properties tests structurally can't reach. |
| `rw_autocodebench` | Anon., "AutoCodeBench: LLMs are Automatic Code Benchmark Generators" (OpenReview:fN0MED2Idq) | false | Builds benchmarks by generating a solution first, then execution-grounded tests, deliberately equating "correct" with "passes the derived functional tests" — the whole pipeline is built to make functional correctness the oracle and cannot surface orthogonal design properties. |
| `rw_selfrefmas` | Anon., "AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework" (OpenReview:Cug26Y0RlT) | false | Names the code-and-tests-hallucinate-together circularity problem but resolves it only by adding more agents/verification inside the same LLM loop — no test-suite-independent oracle of the kind this paper's design needs. |
| `rw_jiaharman` | Jia & Harman, "An Analysis and Survey of the Development of Mutation Testing" (IEEE TSE, 2011) | **true** | The standard reference establishing the mutation score and the equivalent-mutant problem — but framed entirely around *behavioral* change; an equivalent mutant is defined as one no test can kill because behavior is unchanged, full stop, and the framework never asks whether such a mutant nonetheless violates a design convention. |
| `rw_schulerzeller` | Schuler & Zeller, "Assessing Oracle Quality with Checked Coverage" (ICST, 2011) | false | Introduces checked coverage — the fraction of executed code whose result is actually asserted — but is scoped to single-execution output/assertion pairs; cannot characterize whole property classes that may never be observable through any single execution's checked output. |
| `rw_murphyreflexion` | Murphy et al., "Software Reflexion Models" (IEEE TSE, 2001) | false | Checks implementation-vs-intended architecture conformance with dedicated model-based machinery, precisely because the ordinary test suite is assumed unable to check design conformance — never measures, through the suite itself, how much of that conformance space is actually invisible to it. |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but two baseline labels need scrutiny for the same reason.
- comments:
  - `{severity: major, field: "specific_related_works[rw_jiaharman].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Jia & Harman is a survey/foundational reference establishing a concept (the mutation score, the equivalent-mutant problem), not a runnable system with its own reported numbers on these subject systems. Marking it a straightforward baseline risks implying its own published figures are being compared against, which they are not — only its *definition* (functional mutation score under default operators) is instantiated as this paper's B0 arm, computed fresh."}`
  - `{severity: minor, field: "specific_related_works[rw_utrl].is_potential_baseline", anti_pattern: null, comment: "Same shape of ambiguity at lower stakes: UTRL's discrimination-reward *training procedure* (or a comparable off-the-shelf generator, per paper.md's A6 substitution clause) is borrowed to build the augmentation arm's stronger test set — not a system whose own reported numbers this paper compares against."}`
- decision: `move_to_refiner` (both are wording-precision fixes, not structural ones — the underlying research contribution each supplies is still legitimately usable).

### Refiner pass

- `rw_jiaharman.is_potential_baseline` retained `true`, note sharpened: "Not a baseline in the beat-a-number sense. Its **mutation-score definition and default-operator practice** is instantiated as this paper's B0 arm, computed on our own subject systems — not a comparison to Jia & Harman's own published figures."
- `rw_utrl.is_potential_baseline` retained `true`, note sharpened: "Its **discrimination-reward test-generation procedure** (or a capability-matched substitute, per the augmentation arm's validity gate) supplies the stronger-suite arm for the structural-vs-quantity-limited check — not a comparison to UTRL's own reported numbers."
- `changes_made`: clarified both baselines' roles as protocol/definition borrowing, not results-comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — all nine limitations describe what prior work fails to do, not a claim this paper itself needs to independently verify as true before proceeding; the paper's own claims are already carried end-to-end as mechanism-tier hypotheses in Stage 5/6. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, drawn directly from digest N5's C1–C5):

- **`sp_oracle_independence`** — *description:* Certify, from sources independent of T, both that a candidate mutant is behaviorally equivalent to P and that it genuinely violates a named convention. *why_it_is_a_problem:* without independence from T on both counts, "T didn't kill it" and "it doesn't actually violate the convention" (or "it isn't actually equivalent") are indistinguishable. *technical_challenge:* neither equivalence nor violation has a ground-truth source inside the object being measured; both certifications must come from elsewhere, and equivalence itself is only decidable up to a stated budget. *source_limitation_ids:* `["lim_binarymatrix_allpass_row", "lim_utrl_functional_reward_only"]`.
- **`sp_nonlocal_construction`** — *description:* Construct mutations that violate non-local conventions (layering, cross-cutting boundaries) while remaining a minimal, functionally-equivalent change. *why_it_is_a_problem:* standard mutation operators perturb one local statement; a layering violation is a property of a call graph or module boundary, not a single line. *technical_challenge:* an operator family must relocate or reroute a call across a declared boundary while preserving the call multiset and observable behavior — a much stronger equivalence-preservation burden than a local edit. *source_limitation_ids:* `["lim_murphyreflexion_separate_machinery"]`.
- **`sp_temporal_kill_semantics`** — *description:* Extend the classical "kill = different final output" criterion so an order-swap that preserves final output but violates a required event ordering is still detectable as a violation. *why_it_is_a_problem:* temporal/ordering properties are properties of an execution trace, not of an input/output pair; the standard mutation-testing kill criterion, by construction, cannot see them. *technical_challenge:* the extension must be principled (trace-order assertions) rather than circular (defined by the very suite being measured). *source_limitation_ids:* `["lim_jiaharman_behavioral_scope_only"]`.
- **`sp_groundtruth_scoping`** — *description:* Restrict the study to conventions that are mechanically checkable (Checkstyle/ArchUnit/trace-rule representable), excluding tacit or undocumented ones, without letting this restriction quietly become the whole finding. *why_it_is_a_problem:* without a machine-checkable ground truth, "violates convention X" has no independent oracle at all — but restricting scope risks understating how much of the real design-conformance space is left unmeasured. *technical_challenge:* the restriction must be stated as a defended scoping choice with an audited-checker-precision gate, not an unexamined default. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: The five sub-problems are each real, method-free, and individually well-formed — but a coverage check against Stage 1's just-confirmed output reveals a genuine gap, not a cosmetic one.
- comments:
  - `{severity: major, field: "sub_problems (as a set)", anti_pattern: "undercoverage", comment: "Stage 1's confirmed objective (post-refiner) requires three conjuncts to hold before a category counts as a blind spot: (a) a DMSR-over-FSR gap, (b) that gap surviving a matched convention-neutral control (ruling out the generic equivalent-mutant effect), and (c) the gap surviving a capability-matched test-suite augmentation (ruling out a quantity-limited explanation). None of the five sub-problems above targets (b) or (c) — they cover admission (oracle independence), construction (non-local operators, temporal kill semantics), and scoping, but nothing here is *about* ruling out the two named alternative explanations that Stage 1's own objective requires. If all five were solved, a reader still could not tell a genuine, design-specific, structural blind spot apart from an equivalent-mutant artifact or a quantity-limited one — the sub-problem set does not jointly deliver Stage 1's output/objective."}`
- decision: **not** `move_to_refiner`. Per `discussion_loop.md`: a major coverage gap requiring genuinely new sub-problems is a proposer-level fix, not something the (deliberately conservative, non-inventing) refiner should patch. Re-propose a `draft_v2`.

### Round 2 (critic phase, on the re-proposed draft)

**draft_v2** (adds two sub-problems, keeps the original five untouched and unrenamed):

- **`sp_design_specificity`** *(new)* — *description:* Rule out the alternative explanation that observed survival reflects the generic equivalent-mutant effect (equivalent mutants of any kind being hard to kill) rather than convention-violation specifically. *why_it_is_a_problem:* every admitted design mutant is, by construction, also an equivalent mutant — so a naive DMSR-vs-FSR gap alone cannot distinguish "the suite can't see design" from "the suite is generically weak against any equivalent mutant, and this happens to be one." *technical_challenge:* isolating the effect requires a control group of mutants that share the *same* operator family and locality footprint but do *not* violate the convention (`EQ_B=1, V=0`), and comparing kill probability between the two matched groups — a within-family, matched-control design that no single-arm DMSR measurement can substitute for. *source_limitation_ids:* `["__novel__"]` — justified as decisive-but-novel because none of Stage 3's nine works model mutants as members of an equivalence class with an internal violating/non-violating split; none needs this control because none attempts to measure design-conformance-specific detectability at all.
- **`sp_structural_vs_quantity`** *(new)* — *description:* Determine whether an observed category-level gap is structural (persists no matter how much stronger the functional test suite becomes) or quantity-limited (closes once functional-test investment increases). *why_it_is_a_problem:* a finding that stops at "current suites miss this" is actionable only as "add more tests" unless it is shown the gap survives a genuine increase in functional-test strength — the practical stakes of the whole paper (per Stage 2's refined `why_it_matters`) hinge on this distinction. *technical_challenge:* the augmentation used for the comparison must be capability-matched (raise the suite's ordinary functional mutation score by a real, pre-committed margin) or the comparison is not informative — a weak augmentation would trivially "fail to close the gap" for the wrong reason. *source_limitation_ids:* `["__novel__"]` — none of the nine related works considers a test-suite-strength manipulation at all; this is a decisive component this paper's own three-conjunct objective requires.

**critique (round 2):**
- summary: The two new sub-problems close the coverage gap cleanly and are each specific and method-free; one small overlap-adjacent risk is worth tightening before moving on.
- comments:
  - `{severity: minor, field: "sp_design_specificity / sp_oracle_independence", anti_pattern: "overlap", comment: "Both invoke 'independent of T' reasoning and could read as restating each other. They are genuinely distinct — sp_oracle_independence is about the *admission* procedure not being decided by the suite under study at all (an independence problem, orthogonal to whether the convention is easy or hard to codify); sp_design_specificity is about *interpreting* an already-admitted set's survival, asking whether violation-status carries any information about kill probability once equivalence is already fixed (a confound-isolation problem, not an independence problem) — but the current descriptions don't make the distinction sharp enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_oracle_independence.technical_challenge` sharpened to end with: "...this is an **admission-independence** problem: the oracle deciding equivalence and violation must not be derived from T, regardless of whether the convention itself is easy or hard to codify."
- `sp_design_specificity.technical_challenge` sharpened to end with: "...this is a **confound-isolation** problem distinct from admission-independence: even with a perfectly T-independent admission procedure, a DMSR-vs-FSR gap alone cannot tell whether kill probability responds to violation-status at all, which is exactly what the matched neutral control is built to test."
- `changes_made`: made the admission-independence-vs-confound-isolation distinction explicit in both `technical_challenge` fields; preserved all seven sub-problems and their stable IDs from round 2 unchanged.
- `declined_to_fix`: none.

**Confirmed Stage 4** (7 sub-problems: `sp_oracle_independence`, `sp_nonlocal_construction`, `sp_temporal_kill_semantics`, `sp_groundtruth_scoping`, `sp_design_specificity`, `sp_structural_vs_quantity`, `sp_generalization_scope` — the last carried over from round 1's original five; 3 sourced from Stage-3 limitations, 4 `__novel__` with stated decisive-component justifications). *Note: `sp_generalization_scope` (the fifth original sub-problem — enough systems/categories sampled that the finding isn't an artifact of specific choices, `source_limitation_ids: ["__novel__"]`) was carried through both rounds unchanged; it is listed in full in the Stage 5/6 tables below where its target methods reference it.*

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (7 methods, one per confirmed sub-problem):

- **`m_dual_oracle_admission`** → targets `sp_oracle_independence`. *proposed_approach:* admit a candidate mutant only if (a) a bounded differential-execution check against an independent input corpus (disjoint from T) finds no observed behavioral difference at a stated budget, and (b) a rule-based checker independent of T (Checkstyle/ArchUnit/trace monitor) certifies it violates a named convention. *key_insight:* requiring both certifications from sources outside T is what makes "T failed to catch it" a claim about T, not about the oracle's own reliability. *hypotheses:* ["Restricting to mutants surviving the audited equivalence-budget check yields an equivalence-oracle mislabel rate below 5% against a stratified human audit (n≥300), i.e. DMSR is not primarily an artifact of equivalence-oracle noise.", "The violation checker achieves precision ≥0.90 against the same human audit per category, i.e. V(m)=1 meaningfully approximates human-judged convention violation rather than checker noise."]
- **`m_nonlocal_operator_catalog`** → targets `sp_nonlocal_construction`. *proposed_approach:* build layering/cross-cutting operators that relocate a call across a declared module boundary while preserving the call multiset (call-graph-equivalent, not just line-equivalent). *key_insight:* preserving the call multiset while breaking only the *layering* rule is what keeps the mutation minimal and admissible rather than a sweeping, hard-to-certify rewrite. *hypotheses:* ["The layering/cross-cutting operator family yields at least 50 dual-oracle-admitted mutants per subject system after filtering — the non-local category is constructible at usable yield, not merely a theoretical category."]
- **`m_extended_temporal_kill`** → targets `sp_temporal_kill_semantics`. *proposed_approach:* build order-swap operators on pairs of output-commutative operations, and extend the kill criterion to include trace-order assertions from an independent trace monitor, not just final-output diffing. *key_insight:* a same-final-output ordering violation can register as "violating" under the trace monitor even where it would never register as "killed" under output-diff alone — the extension is what makes temporal properties visible to the measurement at all. *hypotheses:* ["At least one admitted temporal/ordering mutant has confirmed-identical final output (via the differential corpus) yet is flagged as convention-violating by the trace-order checker, demonstrating the extended kill criterion captures cases invisible to an output-diff-only criterion."]
- **`m_scoped_codifiable_conventions`** → targets `sp_groundtruth_scoping`. *proposed_approach:* restrict admission to conventions with a Checkstyle/ArchUnit/trace-rule representation, and gate any category's results from confirmatory to exploratory status if the checker's audited precision falls below 0.90. *key_insight:* an explicit, audited scoping rule turns "we only look at easy conventions" from an unexamined default into a stated, checkable boundary condition. *hypotheses:* ["Restricting to codifiable conventions still admits at least 150 mutants per category per system in at least 9 of 12 tested systems, i.e. the restriction is not so narrow that it starves the measurement of admitted cases."]
- **`m_design_specificity_control`** → targets `sp_design_specificity`. *proposed_approach:* for every admitted design mutant, construct a matched convention-neutral mutant from the same operator family and locality footprint (equivalent, but not violating), and compare kill probability between the two matched sets. *key_insight:* if kill probability is statistically indistinguishable between the violating and non-violating matched sets, that is evidence the suite has zero differential sensitivity to violation-status — supporting a genuine, convention-specific blind spot rather than an artifact of "equivalent mutants are hard to kill in general." *hypotheses:* ["The absolute difference in kill probability between the design-mutant set and its matched, convention-neutral control is below 0.05 per category."]
- **`m_augmentation_arm`** → targets `sp_structural_vs_quantity`. *proposed_approach:* augment each subject suite with a capability-matched, discrimination-optimized generated test set (raising the suite's functional mutation score by a pre-committed margin) and re-measure per-category DMSR before and after. *key_insight:* if the gap were merely a matter of insufficient functional-test investment, a real increase in functional-test strength — even from tests with no design-awareness at all — should shrink it; a gap that survives is evidence of a limit on what functional tests can express in principle, not how many exist. *hypotheses:* ["For the non-local categories (layering/cross-cutting, temporal/ordering), the absolute DMSR reduction after a capability-matched augmentation (raising the functional mutation score by at least 10 points) is below 0.10, with no significant per-mutant kill change, across a majority of tested systems."]
- **`m_multi_system_category_design`** → targets `sp_generalization_scope`. *proposed_approach:* run all three categories across at least 12 subject systems spanning two ecosystems (Java, Python), fit one mixed-effects model (`kill ~ mutant_type + category + (1|system)`), and additionally compute the trajectory-style classification from two disjoint random half-samples of systems. *key_insight:* random system effects absorb system-level idiosyncrasy so a category-level claim survives individual systems behaving unpredictably; the same fitted structure supports both a significance test and a resampling-based reliability check. *hypotheses:* ["The category fixed effect in the mixed-effects model is significant at α=0.05, pooled across all tested systems.", "Per-category classifications computed from two disjoint random half-samples of systems agree in a majority of category comparisons."]

**critique:**
- summary: Every method traces to a real sub-problem with an actual mechanism (no goal-restatement), but one hypothesis is stated as a bare existence claim, which is close to unfalsifiable in practice.
- comments:
  - `{severity: major, field: "m_extended_temporal_kill.hypotheses", anti_pattern: "unfalsifiable_hypothesis (near-tautology)", comment: "'At least one admitted temporal/ordering mutant' is a claim that is almost guaranteed to hold the moment any temporal mutants are admitted at all — with even a modest admitted count, finding a single instance is not a meaningful test of anything. A hypothesis this weak could pass by construction rather than by evidence, which fails the stage-6 rigor filter ('no tautologies... the experiment has to be able to fail') before it even reaches stage 6."}`
- decision: `move_to_refiner` (a rate-based rewording using content the draft already implies — the mechanism doesn't change, only the threshold).

### Refiner pass

- `m_extended_temporal_kill.hypotheses` (refined): ["At least 50% of admitted temporal/ordering mutants have confirmed-identical final output (via the differential corpus) yet are flagged as convention-violating by the trace-order checker — a majority, not merely an existence instance, since kill-vs-violate independence for this category is exactly what is being measured, and a weaker existence claim would be true almost by construction."]
- `m_multi_system_category_design.key_insight` (formalized-for-free, no flag needed): extended with: "...a single mixed-effects specification yields two distinct, separately falsifiable estimands from one fit: the category fixed-effect test (does structure exist across categories) and the split-half agreement rate computed by refitting on each disjoint half (is that structure a property of the condition, not of which systems happened to be sampled) — one model, two readouts, not two mechanisms, mirroring the same one-instrument-two-estimands logic already used for the equivalence/violation oracle pair in `m_dual_oracle_admission`."
- `changes_made`: rate-based rewording of the temporal-kill hypothesis; explicit one-instrument-two-estimands justification for the two-hypothesis method.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 7 methods, **9 hypotheses total** (2 + 1 + 1 + 1 + 1 + 1 + 2, respectively), deliberately mixing instrument-validity claims (oracle mislabel/precision rates, non-local yield, scoping yield, split-half reliability) with the study's headline empirical predictions (temporal-kill-extension necessity, design-specificity control, structural-vs-quantity persistence, category structure) — the same deliberate design choice B5.5 made for an `empirical` study_type, since instrument-validity claims are themselves falsifiable, first-class hypotheses for a measurement paper, not throat-clearing.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 9 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. B0/B-alt/augmentation below are sanity-check and confound-isolation comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Defects4J-derived Java subject projects shipping Checkstyle + ArchUnit configurations — *justification:* mature JUnit suites plus machine-readable naming/layering rules already in the project, giving ground truth without inventing rule sets; primary pilot + scale-up corpus.
- A Python subset with mature pytest suites and flake8/import-linter configurations — *justification:* the cross-ecosystem arm needed by `rq_category_structure`/`rq_split_half_reliability`'s generalization claim (Stage 4's `sp_generalization_scope`) — without a second ecosystem, "the finding generalizes beyond one language's tooling idioms" cannot be tested at all.
- (draft initially listed "a general benchmark of open-source projects" with justification only "more subject systems is better" — flagged below.)

`baselines` (confound-isolation and sanity-check comparators, not outcome-tier competitors):
- B0 — default functional mutation arm (PIT/pitest, mutmut) on the identical unmodified suite — the necessary reference defining FMS/FSR for every DMSR-vs-FSR contrast.
- B-alt — matched convention-neutral equivalent-mutant control (same operator family, same locality, `V=0`) — isolates design-specificity per `sp_design_specificity`.
- Augmentation arm — a discrimination-optimized generated test set (UTRL-style, or a capability-matched substitute per the augmentation validity gate) — the stronger-suite comparator for `sp_structural_vs_quantity`.

`research_questions` (9, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_equivalence_oracle_validity` | `sp_oracle_independence` | "Restricting to mutants surviving the audited equivalence-budget check yields an equivalence-oracle mislabel rate below 5% against a stratified human audit (n≥300), i.e. DMSR is not primarily an artifact of equivalence-oracle noise." |
| `rq_violation_checker_precision` | `sp_oracle_independence` | "The violation checker achieves precision ≥0.90 against the same human audit per category, i.e. V(m)=1 meaningfully approximates human-judged convention violation rather than checker noise." |
| `rq_nonlocal_yield` | `sp_nonlocal_construction` | "The layering/cross-cutting operator family yields at least 50 dual-oracle-admitted mutants per subject system after filtering — the non-local category is constructible at usable yield, not merely a theoretical category." |
| `rq_temporal_kill_extension` | `sp_temporal_kill_semantics` | "At least 50% of admitted temporal/ordering mutants have confirmed-identical final output (via the differential corpus) yet are flagged as convention-violating by the trace-order checker — a majority, not merely an existence instance, since kill-vs-violate independence for this category is exactly what is being measured, and a weaker existence claim would be true almost by construction." |
| `rq_codifiable_scope_yield` | `sp_groundtruth_scoping` | "Restricting to codifiable conventions still admits at least 150 mutants per category per system in at least 9 of 12 tested systems, i.e. the restriction is not so narrow that it starves the measurement of admitted cases." |
| `rq_design_specificity` | `sp_design_specificity` | "The absolute difference in kill probability between the design-mutant set and its matched, convention-neutral control is below 0.05 per category." |
| `rq_structural_vs_quantity` | `sp_structural_vs_quantity` | "For the non-local categories (layering/cross-cutting, temporal/ordering), the absolute DMSR reduction after a capability-matched augmentation (raising the functional mutation score by at least 10 points) is below 0.10, with no significant per-mutant kill change, across a majority of tested systems." |
| `rq_category_structure` | `sp_generalization_scope` | "The category fixed effect in the mixed-effects model is significant at α=0.05, pooled across all tested systems." |
| `rq_split_half_reliability` | `sp_generalization_scope` | "Per-category classifications computed from two disjoint random half-samples of systems agree in a majority of category comparisons." |

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is generic filler rather than a hypothesis-linked reason.
- comments:
  - `{severity: major, field: "datasets[general benchmark]", anti_pattern: "weak justification (fails the rubric's 'why this dataset actually stresses the hypothesis')", comment: "'More subject systems is better' is not a justification tied to any RQ — it doesn't say which hypothesis needs a third dataset or what it adds beyond the two already listed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "A held-out set of ~3 additional systems (mixed Java/Python, drawn after the primary corpus is fixed) — *justification:* reserved specifically as the pre-registered replication set for `rq_split_half_reliability`'s split-half check, so the reliability claim is tested on data not used to tune the operator catalog or checker thresholds, rather than only re-splitting the same fixed corpus post hoc."
- `changes_made`: gave the third dataset entry a hypothesis-linked reason (pre-registered held-out replication) instead of a generic "more is better" note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (only the *what* and *why*, never Checkstyle/ArchUnit/PIT by name outside Stage 5's `proposed_approach`).
2. **ID stability** — no id renamed mid-run; `sp_*`/`m_*`/`rq_*` stable stage-to-stage, including the two sub-problems added at Stage 4 round 2 (`sp_design_specificity`, `sp_structural_vs_quantity`), which kept their names through the refiner pass and into Stage 5/6.
3. **Reference integrity** — `sp_oracle_independence.source_limitation_ids`, `sp_nonlocal_construction.source_limitation_ids`, `sp_temporal_kill_semantics.source_limitation_ids` each ∈ Stage 3 limitations ✓; all four `__novel__`-sentinel sub-problems carry a stated decisive-component justification ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four confirmed outputs (admitted mutant set, kill/survive verdicts incl. matched control, DMSR-vs-FMS profile, structural-vs-quantity determination) are each reachable: (1)/(2) via `sp_oracle_independence` + category-construction sub-problems, (3) via `sp_generalization_scope`, (4) via `sp_structural_vs_quantity` — and the objective's three conjuncts (gap exists / not equivalent-mutant-artifact / not quantity-limited) are covered respectively by `sp_generalization_scope`, `sp_design_specificity`, and `sp_structural_vs_quantity`. Nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** unlike a stage where every round converges in one critic pass, Stage 4 genuinely required backing out of the refiner path — the round-1 critique found that the sub-problem set inherited wholesale from digest N5's C1–C5 (written before `paper.md`'s own Step 5/6/9 material was developed further) no longer covered what Stage 1's own refined objective already demanded. This is the same category of tension B5.5's run flagged as hardest ("scope discipline" against a mature seed) but sharper here: it wasn't a wording gap the refiner could patch, it was a structural gap requiring two genuinely new sub-problems, which is exactly the case `discussion_loop.md` reserves for a re-propose rather than a refiner pass.


---

## Post-review revision round (2026-07-05)

> Scope: fold every REVISE/major/minor finding from `stage_review.md` and `taste_audit.md` (no `design_review.md` exists) into the three deliverables. A prior attempt at this pass was killed early by an API limit before writing anything — verified by absence of this section and of a Review-revision row in `pipeline.md` before this round. Each finding below was re-checked against the *current* files, not taken on the review files' word.

| # | Source → finding | Status | Verification / change |
|---|---|---|---|
| 1 | `stage_review.md` Stage 2 REVISE — two Related-Work clusters (LLM-code-testing, classical SE adequacy/conformance) sat side by side with no argued connection | already applied — verified, no change needed | Connecting sentence ("the first supplies the applied stakes/motivation... the second supplies the theoretical vocabulary... this paper extends") present in `paper_draft.md` (Introduction ¶3 and Related Work ¶1) and mirrored in `paper_draft.tex` (lines 42, 269); `paper_draft.pdf` already compiled from that source. |
| 2 | `stage_review.md` Stage 4 REVISE — RQ6's falsification condition omitted its reversed polarity (small gap = supporting outcome) | already applied — verified, no change needed | Explicit reversed-polarity statement ("Readers should not expect 'bigger gap, stronger finding' here...") present in `paper_draft.md` RQ6 Falsification condition and `paper_draft.tex` (line 217); also cross-referenced in `experiment_design.md` RQ6's Expected-outcome polarity note. |
| 3 | `stage_review.md` Phase A item 1 — digest N4–N8, N12 missing 3-part `absence_comment` | already applied — verified, no change needed | `digest.md` now carries 12 `absence_comment` blocks covering all non-GIVEN nodes. |
| 4 | `stage_review.md` Phase A item 2 (major) — digest N3's 9 citation keys absent from `reference_candidates.jsonl` | partially applied upstream; residual remains OPEN — environment-blocked, logged, not fixable in this pass | All 9 keys verified present as `verdict: selected` with paper-specific `why` (cache lines 151–159). Residual: `JiaHarman2011`, `BinaryMatrixTests`, `UTRL` still have `pdf_path`/`digest_path` = null, `verified.id_resolves` = false — resolving requires a real network harvest + extraction-mode digest (prior WebFetch attempt hit an OpenReview bot wall). This is a pre-Phase-B blocker on the reference cache, not a defect in the three deliverables; it remains recorded in `pipeline.md` Phase A row and is re-logged here rather than blocked on. |
| 5 | `stage_review.md` Phase A item 5 — assumption A3 stated no gate/consequence on audit failure | already applied — verified, no change needed | `paper.md` A3 now carries the explicit gate (mislabel ≥ 5% → re-filter to structurally-guaranteed subfamilies → if still ≥ 5%, demote to exploratory, symmetric with A4). |
| 6 | `stage_review.md` Phase A item 6 (R1) — missing estimand sentence in Step 5 | already applied — verified, no change needed | "Estimand (guidance.md §3.4 R1)" sentence present at top of `paper.md` Step 5 (quantity / unit of analysis / reference population / decision). |
| 7 | `stage_review.md` Phase A item 6 (R2) — A4 violation-oracle validation was a bare precision number | already applied — verified, no change needed | `paper.md` A4 hardened to the full 5-step R2 sequence incl. two independent raters, κ ≥ 0.7, confusion-structure check, freeze-before-scale; widened gate (precision < 0.90 or κ < 0.7 or systematic confusion). Mirrored in `experiment_design.md` RQ2. |
| 8 | `stage_review.md` Phase A item 6 (R3) — confound-removal never stated as explicit one-liners | already applied — verified, no change needed | Three R3 one-liners (X_diff independence, matched neutral set N_c, A6 capability-matched augmentation gate) present in `paper.md` Step 5. |
| 9 | `stage_review.md` Phase A item 6 (item 9) — no power justification for the 150-mutant floor; no thin-cell rule | already applied — verified, no change needed | Power statement (power ≥ 0.90 at α = 0.05 for effect floor `DMSR_c − FSR ≥ 0.25` at n = 150) + thin-cell INCONCLUSIVE rule present in `paper.md` Step 6 and reproduced verbatim in `experiment_design.md` Design constants. |
| 10 | `stage_review.md` Phase A item 6 — from-memory exemplar citation in digest N12 ("Property-Based-Testing-in-Practice") | already applied — verified, no change needed | Replaced in `digest.md` by cache-verified `OnBlindSpotsNLGMetrics` (`acl_he-etal-2023-blind`, `verdict: selected`); the from-memory key no longer appears as a live citation. |
| 11 | `taste_audit.md` §6 — residual risk of Bridge-shaped "two literatures, unconnected" drift in Related Work during assembly | already applied — verified, no change needed | Same underlying issue as finding 1; audit verdict itself is 🟢 with no open action items of its own. |

**Cross-deliverable consistency check (this round):** `paper_draft.md` and `experiment_design.md` agree on all shared quantities — 9 mechanism-tier RQs (0 framing, 0 outcome); RQ thresholds 5% (RQ1), 0.90 precision + κ ≥ 0.7 (RQ2), ≥ 50/system (RQ3), ≥ 50% (RQ4), ≥ 150/category/system in ≥ 9 of 12 (RQ5), < 0.05 (RQ6), < 0.10 with ΔFMS ≥ +10 pts gate (RQ7), α = 0.05 (RQ8), majority split-half agreement (RQ9); design constants (12 × 3 scale-up, N_diff ≥ 10,000, Holm correction, mixed-effects model, 0.25 effect floor, thin-cell INCONCLUSIVE rule). All 9 `target_hypotheses` in `experiment_design.md` remain byte-identical to Stage 5's confirmed text above. No mismatch found; no deliverable edit required. One pre-existing, deliberately-flagged note retained unchanged: `experiment_design.md` RQ1's flag that `paper.md` A3's *detection probe* (manual audit of 100 surviving mutants) uses a different n than the Stage-5/RQ1 study-level validity audit (n ≥ 300 stratified) — the two deliverables agree with each other on n ≥ 300; the flag documents an upstream `paper.md` internal note and no review file requests changing it, so it is left as an honest documented discrepancy rather than silently harmonized.

**Files touched this round:** `discussion_trace.md` (this section), `pipeline.md` (Phase Log row). No prose, design, or `.tex` change was required — every review finding was already reflected in the current deliverables (the review files record fixes applied at review time), so `paper_draft.pdf` was not recompiled.
