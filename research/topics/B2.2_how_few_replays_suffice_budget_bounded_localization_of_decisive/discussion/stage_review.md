# Pengsida Stage Review — B2.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs" (how few replays suffice, how much structured search saves) with no new localization *algorithm* proposed as the deliverable — digest N12 states this explicitly: "no new localization algorithm is claimed as the primary novelty (bisection and group testing are classical primitives being characterized)." The checkpointed replay harness, fault-injected corpus, monotonicity diagnostic, and cost-accounting instrument are the *analytical apparatus* that makes the phenomenon observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "current replay-based attribution systems... spend that budget exhaustively... without ever asking how few replays would have sufficed" is a first-principles framing (the root asymmetry between causally-verified-but-expensive and cheap-but-unverified attribution), not a patch justification. The stakes are stated concretely: causally verified attribution either stays "an expensive offline process" or becomes "cheap enough to run every time a trajectory fails" — a real practitioner consequence, not a generic AI-importance appeal. The Einstein ratio holds: Introduction paragraphs 1–2 are pure problem/stakes, with bisection and group testing not named until paragraph 5.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The three thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "InT... TRIM... AttnRL... iStar... intervenes during generation, training, or rollout construction — none provides post-hoc localization of a decisive step in an already-failed, already-logged trajectory"), which clears the "citation dump" failure mode. But the section, as first assembled, never stated in one place which single prior work is the *closest* competitor. `pipeline.md`'s Stage 3 already did this ranking work internally (AgenTracer and DoVer are the two systems that actually replay, as opposed to Who&When's log-only judging) — but that ranking never made it into the assembled Related Work's opening sentence in the first draft. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming AgenTracer and DoVer as the closest prior work and stating the precise delta (neither characterizes an accuracy-vs-replay-budget tradeoff), rather than leaving the reader to infer the ranking from three parallel thematic paragraphs.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the suffix-replay predicate g(k), the decisive-step definition (an outcome-flipping counterfactual), the monotonicity-violation rate, and the replay-unit cost accounting are all given in Problem Definition/Methodology ahead of any claim that invokes them. The inferential chain is licensed at its one load-bearing hinge: "a decisive failure corrupts state every later checkpoint inherits and no earlier checkpoint carries" is exactly the fact that makes g(k) near-monotone, and the draft states this explicitly rather than asserting bisection's efficiency by fiat — and then goes further, measuring the *rate* at which that hinge actually holds (the monotonicity-violation rate) rather than assuming it universally. No orphan components — every one of the five modules (cost accounting, bisection + monotonicity diagnostic, vote de-noising, group testing, matched-budget corpus/baseline suite) traces to a named sub-problem, with no leftover machinery. The one place a reviewer would press hardest — "isn't bisection just ddmin renamed?" — is confronted directly in Related Work rather than avoided: "this paper does not propose bisection or group testing as new search algorithms; the contribution is characterizing how these classical primitives... behave once every one of [ddmin's] assumptions is violated."

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (RQ3 is a genuine falsification design: stratifying by the monotonicity-violation rate to see whether bisection's advantage over uniform sampling actually *shrinks* where the diagnostic says it should, not just correlating two numbers; RQ7's budget-matched uniform-sampling arm is the isolation control that rules out "the savings just come from having replay access at all"). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ...at least 90% of the exhaustive scan's exact-step accuracy while consuming at most 25%..." without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` material already had this discipline (its Step 6 "Fallback" clauses per RQ) that had not yet been carried into the assembled `research_questions` field of the Stage 6 pipeline output, since the `auto-research-discussion` schema itself only has an `expected_outcome` field, not a dedicated falsification field.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in the pre-existing `paper.md`'s Step 6 Fallback clauses).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Long LLM-agent trajectories... are now routine in agent development, and when one of these trajectories fails, someone has to find the one step that decided the outcome" / "Yet every replay re-invokes real LLM and tool calls, so replay count is itself a scarce, costly resource" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning that question into a measurable one surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific measurement design rather than a hedge" / "We evaluate this design on trajectories with programmatically injected, replay-verified failure locations...") reconstructs the whole five-move arc (problem → gap → nearest prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in the abstract and the first Contributions bullet: "a decisive failure corrupts agent and environment state that every later checkpoint inherits but no earlier checkpoint carries, so this replay outcome is close to a step function of the checkpoint index." The Conclusion names two real forward-looking limitations (injected-vs-natural construct validity; two-environment external validity) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming AgenTracer and DoVer as the closest prior work and stating the delta plainly (neither characterizes an accuracy-vs-replay-budget tradeoff), rather than leaving three parallel thematic paragraphs unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run against goal.md §3's checklist (not the auto-research-discussion Stage 1–6 review above, which is a different, complementary pass). Inputs: `README.md`, `digest.md`, `paper.md`, and the just-upgraded `discussion/reference_candidates.jsonl` (canonical schema, 159 records: 150 harvested + triaged, 9 added to close a cache-integrity gap found below). Date: 2026-07-04.

### 1. Digest self-verification — **PASS**

Re-executed the cross-node checks `digest.md`'s own self-verification pass claims. Confirmed: N4 `affects_works` (L1–L7) each match an N3 `citation_key` exactly and vice versa; N6 `challenge_arguments`/`unaddressed_challenges` ids ⊆ N5's {C1..C4}, `mechanism_components` ⊆ N6's {M1..M6}; N8 `addresses_challenges`/`evaluates_mechanisms`/`tests_contributions` all resolve into N5/N6/N7; N9 `rq_id`s all exist in N8. All of N0–N12 plus Claims are present. Every non-FOUND node (N0 PARTIAL, N1 PARTIAL, N10 NOT_FOUND, N11 NOT_FOUND) carries a full 3-part `absence_comment`. No fabricated numbers found outside flagged planning estimates.

### 2. Reference-cache integrity — **REVISE, fired and fixed**

**Finding.** `digest.md` N3 grounds its Related Works table in 9 specific citations (Who&When `OpenReview:GazlTYxZss`, AgenTracer `OpenReview:l05DseqvuD`, DoVer `OpenReview:mrEK16Jy6h`, InT `OpenReview:YAhTj2VgBw`, TRIM `OpenReview:MoKrugWUfC`, AttnRL `OpenReview:NCN8oUsiNf`, iStar `OpenReview:ooROvpmxMV`, BAI-LD `OpenReview:gYetLsNO8x`, and Zeller & Hildebrandt 2002), and `paper.md`'s Related Work / baseline suite (M5) / assumption ledger repeat these same 9 as the load-bearing prior work. **None of the 8 OpenReview ids were present anywhere in the harvested 150-candidate `reference_candidates.jsonl`** — not `pending`, simply never harvested at all. The 150-candidate pool (110 arXiv "recent listing" papers + 40 ACL-2023-anthology papers) shows no evidence of query angles targeting failure-attribution/replay/best-arm-identification-by-name, i.e. a harvest-adequacy failure per guidance.md Part 5 ("cache thin... the harvest was inadequate, not the field empty"). This is worse than the checklist's "no pending entry cited anywhere" bar — it's zero entries, pending or otherwise, for the paper's actual grounding citations.

**Fix applied.** Verified all 8 OpenReview ids resolve in the local corpus (`topics/corpus/ideas.jsonl`, 11,683 entries) by `paper_id`/`paper_title`/`proposal` match against `digest.md`'s grounded summaries. Live OpenReview web-fetch was attempted for 2 ids (`GazlTYxZss`, `l05DseqvuD`) and blocked by a bot-verification wall in this sandboxed environment; the local-corpus record served as the spot-check instead, cross-checking 3 ids in total (`GazlTYxZss`, `l05DseqvuD`, `mrEK16Jy6h`) — their corpus `proposal.motivation`/`proposal.method` text matches `digest.md`'s grounded quotes closely (e.g. AgenTracer's corpus method text — "replaying trajectories under controlled counterfactual interventions and synthetic perturbations" — matches digest N3's "replaying the execution while replacing one step at a time"). Added all 9 as canonical cache records (`WhoWhen2025`, `AgenTracer2025`, `DoVer2025`, `InT2025`, `TRIM2025`, `AttnRL2025`, `iStar2025`, `BAILD2025`, `ZellerHildebrandt2002`), `verdict: selected`, relevance tagged per guidance.md Part 5 (`method-twin`: AgenTracer, DoVer — the two nearest-neighbor works per this file's own Stage 2 finding above; `baseline`: Who&When, and BAI-LD's sibling theory; `adjacent`: InT, TRIM, AttnRL, iStar; `contrast`: BAI-LD, Zeller & Hildebrandt — cited specifically as frames whose assumptions don't transfer, not as runnable competitors). `pdf_path`/`digest_path` are `null` for all 9 (this corpus caches proposal text, not PDFs), so `verified.id_resolves = false` per the "true iff pdf_path non-null" rule — recorded honestly rather than papered over.

**Also completed (Task 1 proper).** All 150 originally-harvested candidates were triaged against digests (skimmed; 2 PDFs pulled via `pdftotext` for ambiguous titles): **6 selected / 144 rejected**, each rejection carrying a specific, paper-content-based reason (see `reference_candidates.jsonl`). Combined with the 9 added grounding entries: **15 selected / 144 rejected out of 159 total cache records.** No `pending` verdicts remain anywhere in the file.

### 3. Tag discipline — **PASS**

Spot-checked N2 (motivation items), N6 (methodology/challenge_arguments), and N9 (results) — every assertion carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`; no untagged assertions found; no `[HYPOTHESIS]` silently reads as `[GIVEN]` anywhere (N9's predicted directions are explicitly `evidence_strength="missing"`, `rq_answered=false`).

### 4. Claim–Evidence Map completeness — **PASS**

All 8 rows in `paper.md`'s Claim–Evidence Map trace to either an H-id (H1–H4) or a `supported-by-design` definition (Step 0/Step 5/A3; CO1/Step 9/A1–A2; Claim 4/A3; A4/A6/t1). Every H1–H4 has a verbatim, pre-committed fallback in Step 6. No orphans in either direction.

### 5. Hypothesis/assumption machinery — **REVISE, fired and fixed**

**Finding (a).** H1 (RQ1), H2 (RQ_INF_1), and H4 (RQ_INF_3) were missing the `aggregation` slot guidance.md §3.1 requires of every H\* (H3/RQ_INF_2 already had it, implicitly, via its "holds in all three layers" wording). The scale-up design explicitly varies 2 environments × 2 agent scaffolds × 2 LLM families; without a pre-committed cross-stratum rule, a pooled PASS could be carried entirely by one favorable condition — exactly the ambiguity guidance's aggregation slot exists to close off in advance.
**Fix applied.** Added explicit **Aggregation** lines to all four RQ subsections in `paper.md` Step 6: pooled-primary-plus-≥3-of-4-strata-agreement for H1/H2; an explicit (previously implicit) restatement of H3's built-in conjunctive all-3-layers rule; pooled-only (with stated rationale: the noise axis is a sampling-temperature property, not an environment property) for H4.

**Finding (b).** The Assumptions table (A1–A7) carried only 3 of guidance.md §3.2's 5 required slots (`assumption`, `failure_mode`, `detection`) — no explicit `gate` (PG-id) or `consequence` (which H\* degrades/restricts/blocks) columns, despite goal.md §3 item 5 explicitly calling out "detection **and gate**." Some gate/consequence content was informally folded into the detection prose for a couple of rows (e.g. A2's "Blocks all comparisons if <95%") but not systematically, and never named which H\* is affected.
**Fix applied.** Added explicit `gate` and `consequence` columns across A1–A7 in `paper.md`, naming concrete gate ids (**PG-1**..**PG-3**, mapped to the walking-skeleton/corpus-construction steps in Step 9/N6) or a phase pointer (Phase D) where no pilot gate applies, plus a per-H\* consequence statement for each.

**Finding (c), discovered while fixing (b).** No assumption or R2 validation plan existed for the one genuinely judgment-based instrument in the design: mapping the natural-failure slice's re-hosted Who&When logs onto this paper's own plan/tool/execution layer taxonomy (Who&When's schema doesn't natively carry this label). Per Part 2 A2's evidence standard, any such instrument needs the guidance.md §3.4 R2 validation sequence. **Fix applied.** Added **A8** to the assumption ledger with a 5-step R2 mini-plan (ground categories in this paper's own N1 definitions → 2 independent human raters on a held-out sample → κ ≥ 0.7 required → inspect disagreement structure → freeze before scoring) and a new **PG-4** gate; consequence is scoped to withhold only the natural-failure leg of RQ_INF_2/RQ_INF_3 if κ < 0.7, not to block the injected-fault corpus results (which assign layer deterministically by construction and don't need R2).

B0 + B-alt + F-G1 were already present with pre-committed wording — no fix needed there.

### 6. Method-rigor audit — **REVISE, fired and fixed**

Checked guidance.md Part 6 items 1–10 against the plan (post-fix):
1. **R1 estimand** — was missing entirely (Step 0's asymmetry sentence and Step 5's formal definitions serve different purposes; neither states quantity/unit-of-analysis/reference-population/decision in one sentence). **Fixed**: added a new "Step 1 — Estimand (guidance.md §3.4 R1)" section to `paper.md`.
2. Verb check — PASS, unchanged (`taste_audit.md` 🟢, confirmed still applicable, see item 8 below).
3. H\* seven-slot completeness — fixed under item 5(a) above.
4. A\* detection+gate completeness — fixed under item 5(b)/(c) above.
5. B0+B-alt+F-G\* — PASS.
6. Instrument R2 plans — fixed under item 5(c) (A8/PG-4); the injected-fault corpus's layer assignment is deterministic-by-construction and correctly has no R2 plan (R2 only applies to judgment-based instruments).
7. Confound-removal one-liners (R3) — PASS: the B-alt design's "budget-matched uniform holds replay access and spend constant, isolating the *structure*..." and M2's verify-by-round-trip construction both name their confound explicitly.
8. ≥1 mechanism analysis (R6) — PASS: the monotonicity-violation-rate diagnostic (M6) plus RQ_INF_2/RQ_INF_3's stratified analyses.
9. Power stated per cell; thin cells INCONCLUSIVE — was satisfied only at the pooled n=300 level; RQ_INF_2's 3-layer stratification (~90–100/layer) had no power statement of its own. **Fixed**: added a per-layer power statement (~65–70% power at α=0.017 Holm-corrected) with an explicit INCONCLUSIVE-not-FAIL rule for underpowered layers.
10. Archetype named (measurement/characterization, A2) and its Part 2 evidence standard (validated instrument + controlled comparison + effect-size-floored tests + rival-explanation ablations + ≥1 mechanism analysis) — **PASS after the above fixes** (item 6's R2 gap was the one open piece of the A2 evidence standard).

### 7. Stage cross-check (advisory) — **PASS**

Already performed by the existing `pengsida-stage-reviewer` pass above (N1↔Stage 1, N3/N4↔Stage 2/3, N6↔Stage 3, N8↔Stage 4), with 2 REVISE fixes already folded into `paper_draft.*`. No new STOP-level cross-stage conflict surfaced in this re-run.

### 8. Taste audit currency — **PASS, no re-run required**

`taste_audit.md`'s recorded 🟢 verdict predates today's fixes, but none of today's fixes touch the asymmetry statement (Step 0) or the formal definitions (Step 5) — they add estimand/aggregation/gate/consequence scaffolding and one new assumption (A8), none of which changes a verb, a bridge/synthesis framing, or the abstract's language. Per goal.md §3 item 8, no "material edit to the asymmetry statement or formal definition" occurred, so no re-audit is triggered.

---

### Phase A gate result: **REVISE (fired on items 2, 5, 6) → all fixes applied in this pass → PASS**

No STOP-level finding. Two checklist items fired REVISE (reference-cache integrity; hypothesis/assumption machinery, with a closely-related method-rigor-audit finding under item 6) and all three were fixed directly in `paper.md` and `reference_candidates.jsonl` in this same pass, per the instruction to resolve REVISE-level static-document gaps immediately rather than defer them. Phase B (walking skeleton) is not attempted here — per this run's scope, real experiment compute does not exist in this environment; that remains a future run's job once resumed via `pipeline.md`.
