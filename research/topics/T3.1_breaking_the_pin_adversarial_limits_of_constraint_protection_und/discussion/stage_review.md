# Pengsida Stage Review — T3.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding**, with a secondary **Resource/instrument** aspect. Per `archetypes.md`'s tells: the core question is "we ask where exactly a known phenomenon's boundary sits, and at what price" — no new pinning defense is proposed as the paper's headline offering; the five variants are the *object of study*, not a contribution being pitted against baselines to win. This matches digest N12's own `empirical` classification (Stage 1's confirmed `study_type: empirical`) and `paper.md`'s own Step 2 archetype call ("Primary: Measurement/boundary-characterization study... Secondary: Protocol/instrument artifact — instrumental, not headline"). Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar; the secondary resource aspect is folded into Stage 3's orphan-component check (does the reusable protocol/oracle earn its place) rather than given its own separate verdict, per `archetypes.md`'s hybrid-paper guidance ("run the dominant archetype's bar and add the secondary one's Stage-4 check").

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. The confirmed Stage 2 motivation states the stakes concretely, not as a generic AI-safety appeal: "an operator choosing among the five variants... needs to know not just that each eventually fails, but at what attack strength... because a variant that fails only at a strength far beyond any deployed adversary's practical budget is a very different deployment decision from one that fails cheaply." This is a first-principles framing (the root issue is that "not unconditionally robust" is not an actionable deployment fact) rather than a patch justification. Feasibility evidence is present and unusually strong for this stage: `paper.md`'s Step 9 walking skeleton specifies a concrete, one-day, three-arm, single-model minimum-viable check (1,800 rollouts, deterministic oracle only, binary pass/fail criterion) before any scale-up — exactly the "minimum-viable exploration" this stage's checklist asks for.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this gap and must name the nearest competitor plainly — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The ten related works are genuinely threaded by role (attack machinery borrowed for the two attack families; oracle methodology borrowed for the violation check; benign compression work contrasted against the adversarial framing; a memory pipeline that inspires one defense variant), and each limitation is problem-tied rather than generic — e.g. `pipeline.md`'s Stage 3 states LightMem's limitation as "its consolidation step is never adversarially stress-tested," not a vague "has limitations." This clears the citation-dump failure mode. But the confirmed Stage 3 output never states, in one sentence, which single prior work is the *closest* to this paper as a whole. `pipeline.md` marks both `rw_slotgcg` and `rw_tensortrust` as `is_potential_baseline: true`, but a reader assembling the draft from these ten entries would have to work out for themselves which one is nearest — the entries are correctly per-role-differentiated (SlotGCG's role is attack machinery, TensorTrust's role is closest evaluation-design precedent) but never explicitly ranked against each other in prose. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming TensorTrust as the closest prior work in evaluation-design terms (attack/defense matrix, robustness-vs-usability trade-off) and LightMem as the closest prior work in mechanism terms (the structural-slot variant's inspiration), stating the precise delta for each, rather than leaving the reader to infer ranking from ten parallel entries.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used. The strength-normalization scheme, the two-tier violation oracle (with its before/after-compaction attribution gate), and the dual-currency cost ratio are all specified in the confirmed Stage 5 output before any hypothesis invokes them — no "named after the fact" violation. The inferential chain is licensed at its one load-bearing hinge: `m_two_tier_violation_oracle`'s key insight states that "a persistence oracle checks a relational property across two time points (present-before, violated-after), which is exactly what none of the existing single-turn... oracles... are built to check" — this is exactly the step that justifies why a *new* oracle definition (not just a reused judge) is a decisive component here, not decoration. No orphan components — every one of the five methods traces to a named sub-problem (`sp_lossy_compaction_tradeoff`, `sp_strength_commensurability`, `sp_violation_oracle_definition`, `sp_cost_currency_commensurability`, `sp_stochastic_boundary_identifiability`), and the secondary resource/instrument aspect (a reusable protocol) is exactly what falls out of these five components being specified precisely enough to reuse — it earns its place rather than being bolted on.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational, and whether the claimed cause (adversarial injection) is isolated from its strongest alternative (generic benign compaction degradation). Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally. `rq_benign_vs_adversarial_attribution` is a genuine falsification design targeting exactly the right alternative explanation (generic benign compaction degradation, not adversarial injection), backed by two controls (`paper.md`'s B0 no-defense-under-benign-compaction, and the budget-matched benign-filler control) that would produce a *different* result if the alternative explanation were true. But the first assembled draft's RQ subsections stopped at "**Expected outcome.**... rather than a missing data point" without ever stating the converse — what specific observation would refute each expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline in full (its own Fallback F1/F2/F3 clauses) that had not yet been carried into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — reusing the concrete statistical conditions already pre-registered in `paper.md`'s Fallback clauses (F1, F2, F3) and B0/B-alt control read-outs, not inventing new thresholds.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Long-horizon LLM agents now rely on periodic context compaction..." / "Yet a load-bearing safety assumption behind this design remains unmapped..." / "The nearest existing work approaches this gap from adjacent but distinct angles..." / "Turning this gap into a measurable question surfaces its own difficulties..." / "Our approach turns each of these obstacles into a specific design choice..." / "We evaluate this design across...") reconstructs the whole five/six-move arc (setting → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in both title and abstract: "a pinned constraint survives only if it re-wins the retention-budget competition at every compaction event, whereas an adversary need only make it lose once." The Conclusion names real forward-looking limitations (currency-dependence of the cost ranking; the amortized-attack calibration gap) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming TensorTrust (closest in evaluation-design terms) and LightMem (closest in mechanism terms) as the two nearest prior works and stating each delta plainly, rather than leaving ten parallel entries unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), reusing `paper.md`'s pre-registered Fallback (F1/F2/F3) and control (B0/B-alt) read-outs rather than inventing new ones, then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — goal.md §3 checklist, run 2026-07-04

> Context: this pass runs goal.md's own Phase A checklist (distinct from the
> `pengsida-stage-reviewer` Stage 1–5 review above, which checks the
> `auto-research-discussion` schema). It runs **after** Task 1 of this session
> upgraded `discussion/reference_candidates.jsonl` from an ad hoc harvest schema
> (topic_id/rank/score/ref_id/...) to goal.md §1's canonical schema
> (key/ids/venue/relevance/verdict/why/verified), with all 150 harvested
> candidates individually digested and adjudicated: **12 selected, 138
> rejected** (0 left `pending`). Selected keys: `JailbreakVsFilters2025`
> (background), `TRAP2026` (adjacent), `GoExploreRedTeam2026` (adjacent),
> `GCGDiffusion2026` (adjacent), `RecursiveLM2026` (adjacent),
> `TrustworthyAgenticAI2025` (contrast), `FoldAct2025` (adjacent),
> `AgenticSTS2026` (method-twin), `ForensicTrajSig2026` (adjacent),
> `PackKV2026` (background), `ClawAgentSecurity2026` (background),
> `ContextAsATool2025` (adjacent).

1. **Digest self-verification — PASS (with one fix applied).** Re-executed
   digest.md's own claimed checks: N0–N12 + Claims all present; every
   non-`FOUND` node carries a 3-part `absence_comment`
   (`what_missing`/`why_matters`/`implication`), except **N12, which had no
   `Status` line at all** — every other node (N0–N11) has one, so this was a
   tag-discipline inconsistency, not a deliberate omission. **Fixed:** added
   `Status: PARTIAL` + a 3-part `absence_comment` to N12 in `digest.md`
   (guidance.md Part 6 item 3 / goal.md §3 item 1 & 3). N4's
   `affects_works` strings all resolve verbatim against N3 `citation_key`s
   (`grounding_check: true`, spot-checked). N8's `rq_source`/
   `evaluates_mechanisms`/`addresses_challenges`/`tests_contributions` cross-refs
   into M1–M5/C1–C5/CO1–CO3 all resolve.

2. **Reference-cache integrity — REVISE (fixed).** This is the load-bearing
   finding of this run. digest.md's N3 (and, downstream, `paper.md`'s
   Notation gloss and `discussion/paper_draft.md`/`.tex`'s Related Work,
   which cite the same names 6×) ground their related work in **ten
   citation keys — ChatInject, ThreatSnapshots, SlotGCG, TAO-Attack,
   GuidedBench, TensorTrust, COMI, InfoChannel, LightMem, GCG — none of
   which resolve as records in `reference_candidates.jsonl`.** Spot-checked
   3 OpenReview IDs (`WVhgFSKniL`, `fsW7wJGLBd`, `dyJ0GWpjJB`) directly
   against the cache file: no match. Root cause: N3's search method note
   says it searched a *different, general* OpenReview corpus
   (`topics/corpus/ideas.jsonl`, 11,683 papers) than this topic's own
   formal harvest (`reference_candidates.jsonl`, 150 candidates from arXiv +
   a targeted OpenReview pull) — the two were never reconciled. This
   directly fails goal.md §3 item 2 ("every N3 key is a `selected` cache
   record") and goal.md §8's hard gate ("citations only via `selected`
   cache keys"). **Fix applied (this run, static-document only, no
   re-harvest — none of the ten OpenReview IDs appear anywhere in the 150
   harvested candidates, so this cannot be resolved by re-adjudicating the
   existing harvest; it needs a future *re-harvest* targeted at those exact
   IDs):** added an explicit provenance-caveat block to `digest.md`'s N3
   (before the citation list) and to `paper.md`'s Step 5 (after the formal
   Objective), each (a) naming the gap precisely, (b) marking the ten keys
   **unverified/pending re-harvest** rather than silently citable, and (c)
   cross-linking the twelve cache-verified `selected` records from Task 1
   that cover overlapping or adjacent ground today (`AgenticSTS2026` as the
   closest method-twin — a bounded, ablatable memory-contract testbed;
   `ForensicTrajSig2026`, `FoldAct2025`, `TRAP2026`, `GoExploreRedTeam2026`,
   `GCGDiffusion2026`, `TrustworthyAgenticAI2025`, `RecursiveLM2026` as
   adjacent/contrast; `JailbreakVsFilters2025`, `PackKV2026`,
   `ClawAgentSecurity2026` as background structural exemplars). **Residual
   risk, not fixable within this session's scope:** `paper_draft.md`/`.tex`
   (Phase E/F outputs that already exist for this topic) still cite the
   ten unverified keys in prose; per goal.md §8's `stale_claim_after_verdict`
   discipline this must be resolved (either a targeted re-harvest that
   makes them cache-resolvable, or a Related-Work rewrite sourced from the
   twelve verified entries) **before** Phase E is next touched — flagged
   here rather than silently patched in the downstream prose, since Task 2
   is scoped to `paper.md`/`digest.md` only.

3. **Tag discipline — PASS (one fix folded into item 1).** No untagged
   assertions found; no silent `[HYPOTHESIS]`→`[GIVEN]` promotions (Claim1
   is the only `[GIVEN]` claim and it traces correctly to the seed
   README's 核心问题; Claims 2–4 stay `[HYPOTHESIS]`; Claim5 stays
   `[GROUNDED:corpus]`, and its corpus is now correctly caveated as the
   *other* corpus per item 2 above, not silently equated with the topic's
   own harvest). N12's missing `Status` line (item 1) was the one
   discipline gap found.

4. **Claim–Evidence Map completeness — PASS.** Every row in `paper.md`'s
   Claim–Evidence Map traces to an H-id (H1/H2/H3) or a
   `supported-by-design` control (B0+B-alt) or digest N3/N4; every
   H-traced row has a matching fallback row (F1/F2/F3) immediately below
   it; no orphans in either direction.

5. **Hypothesis/assumption machinery — PASS (substance verified against
   guidance.md §3.1/§3.2/§3.3).** H1/H2/H3 each carry, in substance if not
   under literal field labels, all seven §3.1 slots (binary statement,
   `applies_if`→the listed Assumption line, metric, test, alpha embedded
   as "Holm-corrected p<0.05" / analogous, effect floor — e.g. H2's
   `θ_R = 2×` — aggregation rule — e.g. "≥4 of 5 variants" — and a verbatim
   fallback F1/F2/F3). A1–A6 each carry assumption/failure-mode/
   detection/gate/consequence (the table compresses gate+consequence into
   the "detection" column's prose, e.g. A1: "...else demote soft
   constraints to secondary" — present, just not column-separated). B0
   (benign no-defense placebo) + B-alt (budget-matched benign-filler rival)
   + F-G1 (global pivot, abstract pre-written) are all present with
   pre-committed wording, per §3.3.

6. **Method-rigor audit — REVISE (fixed).** Guidance.md Part 6 items 1–5,
   7, 9 hold (estimand stated in Step 5's Objective paragraph; verb check
   already passed at Step 3; H*/A* completeness per item 5 above;
   confounds named per constraint — B0 removes the "is pinning doing
   anything" confound, B-alt removes the "generic degradation" confound, A3
   removes the "currency-choice" confound; power stated per cell with
   thin cells routed to "boundary-unresolved" exclusion, guidance.md Part 4
   situation 5's INCONCLUSIVE discipline under a different label). **Item
   6 (every instrument has the 5-step R2 plan with an acceptance
   threshold) failed as drafted:** the soft-constraint LLM-judge oracle
   (M3) stated only step③ of guidance.md §3.4 R2 (validate against human
   raters) and set its acceptance bar at **Cohen's κ ≥ 0.6**, undershooting
   R2's stated required minimum of **κ ≥ 0.7**; steps①(ground categories
   externally)②(held-out refine with named ops)④(confusion-structure
   check) were absent entirely. **Fixed in `paper.md`:** inserted the full
   5-step R2 sequence for the oracle (grounding checklist items in the
   pinned constraint's own spec; held-out-slice refinement; ≥2-rater
   validation; confusion-structure inspection gating the freeze; freeze
   before scale) immediately after the Oracle-procedure paragraph in Step
   5, and raised the G0 gate (both in the A1 assumption-ledger row and the
   Global-gates list) from κ ≥ 0.6 to **κ ≥ 0.7**, citing guidance.md §3.4
   R2. Item 8 (≥1 mechanism analysis budgeted, guidance.md R6): satisfied
   by H1's full pre-registered resistance ordering (`d_slot > d_cksum >
   d_kcopy > d_reinj > d_0`), which is itself a mechanism-level test (which
   *specific* architectural property — distance from dependence on the
   lossy pass — drives resistance), not merely a headline existence claim.
   Part 2's A2 evidence standard (validated instrument + controlled
   comparison + pre-registered effect-size-floored tests + rival-ablation
   pairing + ≥1 mechanism analysis) is now met in full once the R2 fix
   above lands; it was not met as drafted, since a not-yet-validated
   instrument invalidates every downstream rate built on it.

7. **Stage cross-check (advisory) — PASS, already on file.** The
   `pengsida-stage-reviewer` review above (Stages 1–5 of the
   `auto-research-discussion` schema) already ran this cross-check and
   fired two REVISEs (Stage 2 nearest-neighbor sentence, Stage 4
   falsification conditions), both already fixed and reflected in
   `paper_draft.md`/`.tex`. No STOP fired there or here.

8. **Taste audit currency — PASS, no re-run needed.** `taste_audit.md`
   audited the asymmetry statement (Step 0) and the method summary
   (Stage 5); neither was materially edited by this run's two fixes (the
   oracle-validation fix changes an acceptance threshold and adds
   procedural steps, not the asymmetry or method framing; the citation
   caveat is a provenance note, not a reframing). No re-audit triggered.

### Gate result: **PASS with 2 REVISE items, both fixed in this run.**

No item fired STOP. Both REVISE items (reference-cache integrity; the
oracle's R2 validation plan) were fixed directly in `digest.md`/`paper.md`
per this run's Task 2 scope. One residual, out-of-scope risk is flagged
(item 2's note on `paper_draft.md`/`.tex` still citing unverified keys) for
whoever next touches Phase E. Per this run's instructions, **no Phase B/C
work was attempted** — no real experiment compute exists in this
environment; the run stops at this Phase A gate.
