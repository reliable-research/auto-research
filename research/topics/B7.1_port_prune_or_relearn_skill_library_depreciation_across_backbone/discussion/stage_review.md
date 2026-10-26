# Pengsida Stage Review — B7.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢, `taste_audit.md`) and **before** the final `paper_draft.md` was locked. Stages 1–4 below were checked against the confirmed stage outputs in `discussion_trace.md`; Stage 5 (Writing) was checked against the first assembled draft of `paper_draft.md`. Four REVISE findings fired and were applied — the confirmed outputs in `discussion_trace.md` mark them `[SR-fix]` inline, and the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them. This file records the review that produced the fixes, not a pending to-do list.

## Archetype classification

**Analysis / Finding** (with a measurement-study evidence standard — guidance.md Part 2 A2). Per `archetypes.md`'s tells: the core question is "does a phenomenon (per-skill value change under backbone upgrade, up to an asset-to-liability flip) occur, how large is it, and why" — no new pipeline is proposed as a fix. The apparatus (frozen-library replay, placebo null instrument, leave-one-out ledger, mechanism signatures, oracle-normalized sweep) is the *analytical instrument* that makes the phenomenon observable and decomposable, not a method pitted against baselines to win: Stage 1's confirmed objective states this explicitly ("never as a beats-baseline contest") and Stage 6 emits zero outcome-tier RQs. This matches the topic card's own [证据]/evidence label and `study_type: empirical` from Stage 1. Stages 3 ("Method") and 4 ("Experiments") below therefore use the **Analysis/Finding** column: the Stage-3 bar is "is each inferential step licensed", and the Stage-4 bar is "is the finding falsification-tested, with the claimed cause isolated from its strongest alternative."

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why, quoting the confirmed outputs:** The problem clears the "so what" test before any apparatus appears — "every skill in the library was acquired under a specific backbone whose failure modes it encodes... when the backbone is upgraded, that encoding is silently invalidated, yet the library carries no record of which behaviors were compensations" is a root-cause framing (the library's missing compatibility axis), not a patch, and the stakes are concrete and two-sided: "never-retire risks negative transfer, full-relearn forfeits the amortized acquisition investment." The decision recurs at every model release, which answers "why now" with a mechanism rather than a trend appeal — and the occupancy sweep's finding that the adjacent (environment) axis is already TAKEN makes "important and still open" checkable rather than asserted. First-principles check: the motivation attacks why the *decision* is unmeasurable (no per-skill value record survives an upgrade), not merely "libraries can go stale," and the heterogeneity argument ("both corners can be far from the frontier simultaneously") is what makes the per-skill resolution non-optional rather than a bigger-is-better instrument choice.

**Feasibility evidence (checklist item 6):** the minimum-viable check is stated in the seed and survives into Stage 6's pilot design — one stream (MBPP+), one upgrade pair, bare-vs-library paired replay is a roughly-one-day binary check of whether any measurable library-level delta exists before the full grid is bought.

**Note for Stage 2:** passing here obligates Related Work to establish that no environment-axis diagnostic, no cross-model transfer study, and no ops pipeline already closes this exact gap — checked next.

---

## Stage 2 — Related Work (vs. confirmed Stage 3 output)

**STAGE 2 VERDICT: REVISE** *(fired, fixed)*

**Why, quoting the draft:** The specific tier is genuinely threaded — each entry ends on a problem-tied limitation, not a generic one (e.g. SkillGuard's "a skill can satisfy its contract perfectly... and yet be economically worthless... or actively harmful; contract violation is neither necessary nor sufficient for value loss"), and the nearest-neighbor pair (Library Drift for the staleness estimator, AFTER for the backbone axis) is confronted with explicit deltas rather than buried. But the section fails the **no-accidental-self-refutation** check as it stands: SkillOps (arXiv:2605.13716) — an *operational maintenance pipeline for skill libraries*, i.e. the closest thing in the literature to an incumbent for the very port/prune/relearn decision this measurement is built to feed — sat in the **general tier** with a one-line scan note and no comparison. A reviewer's cheapest kill is "SkillOps already maintains skill libraries; what does your measurement add to its pipeline?", and the confirmed output could not answer it, because the discipline of the comparison protocol (alignment → method_addresses → gap) was never run on that work. For every other 2026 work the draft did run it; the omission is exactly the "buried twin" pattern, applied not to the estimand twin but to the *decision* twin.

**THE ONE FIX (applied):** Promote SkillOps to the specific tier with a full comparison and limitation: its maintenance triggers are environment events (dependency bumps, API changes), not backbone releases, and it prescribes ops actions without any per-skill value estimand — "no signal tells it *what a skill is worth* after a backbone swap, so it cannot rank retirement candidates" (`lim_ops_no_econ`). Recorded as `[SR-fix]` in `discussion_trace.md` Stage 3 and carried into `paper_draft.md`'s Related Work (maintenance-and-governance thread) with the delta stated plainly.

**Secondary check (no further finding):** the engagement-tier honesty note (all 2026 characterizations bounded by the repo's scan records; no network) is present and each quantitative claim ("+0.0pp vs +16.2pp", "73.1%", "880 pairs") traces to README lines 24–26 — no characterization exceeds its source.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus, vs. confirmed Stage 5 output)

**STAGE 3 VERDICT: REVISE** *(fired, fixed)*

**Why, quoting the draft:** Constructs are defined before use (marginal utility on an activation set, retention with an acquisition-value floor, the three mechanism signatures), and most inferential hinges are stated rather than assumed — e.g. the placebo's identification role ("H1's causal reading is licensed jointly with H3, not by H1's contrast alone") and the same-backbone pairing that cancels the capability confound. But the apparatus's single most load-bearing inferential step was **unlicensed**: `m_utility_ledger` claims that "masking one skill on its own activation set turns an infeasible 2^K factorial into K bounded paired contrasts" — which identifies a *per-skill* quantity only if cross-skill interactions are second-order. Skills in a library are not independent by construction (retrieval competes; skills compose; a masked skill's neighbor may substitute for it), so leave-one-out deltas can misattribute shared value or hide redundancy: a skill whose function is duplicated by another shows u_k ≈ 0 under masking while the *pair* carries real value. The chain "masked delta, therefore per-skill utility, therefore per-skill retention, therefore ranking" had an unjustified jump at its first link — precisely the Analysis/Finding failure mode ("each inferential step licensed") this stage exists to catch, and it contaminates H4, H5, and H7 downstream if false.

**THE ONE FIX (applied):** State the additivity licensing assumption explicitly in the method, and give it a *detection*, not a hope: a pairwise-interaction probe — pair-masking over the top-frequency skill pairs, with a pre-set bound (interaction share ≤ 15% of total attributed value) — plus a pre-committed downgrade if the bound is exceeded: report utilities at retrieval-cluster granularity instead of single-skill granularity and re-evaluate the heterogeneity and reliability claims at that granularity. Recorded as `[SR-fix]` in `discussion_trace.md` Stage 5; carried into `paper_draft.md` (Per-Skill Utility Ledger subsection + Threats to Validity) and into the experiment spec's assumption ledger.

**Orphan-component check:** none found — all five apparatus modules trace to a named sub-problem, and no module is decoration (the placebo and the forced-use arm each name the confound they remove, per guidance.md R3).

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation, vs. confirmed Stage 6 output)

**STAGE 4 VERDICT: REVISE** *(fired, fixed)*

**Why, quoting the draft:** The falsification discipline is mostly real: RQ3 is a genuine null-instrument design (the placebo must *fail* to reproduce the harm, and a placebo reproducing ≥50% of it refutes the content story), RQ8 was explicitly de-circularized in-stage (portability measured on validation inputs disjoint from the task stream), and the strongest-alternative question ("the gap is context load / invocation shift / task mix, not content") has named arms. But RQ7's decision-adequacy criterion contained a **fuzzy, cherry-pickable clause**: the draft inherited Stage 5's sweep framing in which the estimate-driven rule's frontier is compared against corners "at at least one operating point." A swept threshold traces many operating points; with enough of them, *some* point favors the rule by chance, so as stated the claim is close to unfalsifiable — the quantitative version of "no pre-stated yes/no bar." The minimum-viability rule ("binary success criterion, set in advance") requires the operating point to be fixed before results exist.

**THE ONE FIX (applied):** Pre-register the operating point *inside the hypothesis*: the cost comparison is taken at matched success — where each policy's success rate is within ±1pp of the never-retire corner's success rate — and RQ7's verdict is computed only there (oracle-recovery ≥80% at that point, majority of cells, Holm-corrected across upgrade pairs), with the full frontier curves reported descriptively only. Recorded as `[SR-fix]` in `discussion_trace.md` Stage 5 (H7 wording) and mirrored in `experiment_design.md` and `paper_draft.md` RQ7.

**Secondary check (no further finding):** every RQ subsection carries an explicit falsification condition (the converse observation that would refute the expectation), per-cell power language distinguishes INCONCLUSIVE (under-powered) from a substantive null, and refuting results are pre-committed to full-prominence reporting (the F-G pivot wording exists for the H1-family null).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion, vs. the first assembled `paper_draft.md`)

**STAGE 5 VERDICT: REVISE** *(fired, fixed)* → **PASS on re-check**

**Why, quoting the draft:** The abstract carries the chain (problem → unmeasured axis → instrument → pre-registered tests) without asserting untested findings as fact ("We pre-register tests of..." — correctly hedged for a spec-stage draft), and one quotable sentence exists and is used consistently: "every skill encodes the failure modes of the backbone that acquired it, but the library carries no record of which backbone that was." The reverse-outline test, however, failed at one paragraph: the first assembled Introduction carried a paragraph whose opening sentence announced the measurement difficulty ("Turning this question into a measurement surfaces...") but whose body then ran through *both* the identification obstacles *and* the why-mechanisms-matter-for-the-decision argument — two messages in one paragraph, with the second (obsolescence vs. interference vs. cost drag demanding different actions) buried after sentence 4, exactly the "buried message" failure mode. A reader skimming first sentences lost the entire mechanism-decomposition motivation.

**THE ONE FIX (applied):** Split into two paragraphs with declarative topic sentences — one for the identification obstacles ("Turning this question into a measurement surfaces three confounds that a naive with/without comparison cannot separate."), one for the decision-relevance of mechanisms ("Even a clean measurement is not yet a decision: which action is right depends on why a skill lost value."). Applied to `paper_draft.md` and `.tex` before rendering; the re-check's reverse outline now reconstructs the full arc (deployment reality → unmeasured axis → nearest work's shared limitation → identification obstacles → mechanism/decision argument → the apparatus → the evaluation) from first sentences alone.

**Conclusion check:** names a real forward-looking limitation (single-harness scope; the additivity downgrade path; unmeasurable below-floor skills) rather than recapping the abstract — passes.

---

## Fixes applied (summary)

1. **Stage 2 fix** — SkillOps promoted to the specific tier with an explicit comparison and the `lim_ops_no_econ` limitation; maintenance-thread delta stated plainly in Related Work.
2. **Stage 3 fix** — leave-one-out additivity assumption made explicit with a pairwise-interaction probe (≤15% bound) and a pre-committed cluster-granularity downgrade; wired into the method section, threats, and the experiment spec.
3. **Stage 4 fix** — RQ7's operating point pre-registered (matched-success band ±1pp vs. never-retire; oracle-recovery ≥80% evaluated only there; frontiers descriptive).
4. **Stage 5 fix** — two-message Introduction paragraph split with declarative topic sentences.

All four are reflected in the current `paper_draft.md`/`.tex`/`.pdf` and marked `[SR-fix]` at their origin points in `discussion_trace.md`. No pre-registered hypothesis was weakened or strengthened by any fix: fixes 1 and 4 are positioning/prose; fix 2 adds an assumption gate and a downgrade path; fix 3 *narrows* H7's claimable region (harder to pass, not easier).
