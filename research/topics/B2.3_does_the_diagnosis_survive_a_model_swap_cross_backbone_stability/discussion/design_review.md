# Design Review (adversarial, 2026-07-04)

Reviewer stance: skeptical PC member; nothing in the topic's self-reported Phase A result was trusted without re-verification. Prior gate context: Phase A was recorded REVISE-blocking (backfilled load-bearing references lack cached digests) — that finding was independently confirmed and turns out to be *worse* than recorded (see Reliability Audit).

Staleness note (stated once, not re-penalized): `discussion/paper_draft.md`/`.tex`/`.pdf` (mtime 13:39/13:42) predate today's Phase A edits to `paper.md` (19:23) — the draft lacks the Estimand, R2 Instrument-validation, Aggregation-rule, and Power/INCONCLUSIVE sections. It is also a Phase-E-shaped artifact produced *before* Phases B/C (out of pipeline order per goal.md §2), though it contains no fabricated numbers (all result slots are blanks/expected-outcomes with falsification conditions). It is treated here as an auxiliary document; `paper.md` is the spec under review.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | Datasets real and costed per stage, skeleton genuinely cheap (<$20); but the A6 clean-run ∩ capability-spread tension threatens the ≈300-task grid, and the "config-not-code" scale-up claim is false for M4/M6 (skeleton never exercises them). |
| 2. Soundness | FIXABLE | Estimand, R2 plan, B0/B-alt machinery are real; but the Phase-A-added H4a INCONCLUSIVE rule structurally contradicts the 2-per-family backbone grid, within-family pairs are tier-confounded by construction, and H1's band decision has no power statement. |
| 3. Novelty & pre-emption | FIXABLE | Differentiation is a genuinely different estimand (cross-backbone agreement of attribution labels), asymmetry passes the deletion test, no bridge framing; but the non-pre-emption evidence rests on a demonstrably misdirected harvest (147/150 hits off-topic) plus memory-reconstructed twins. |
| 4. Hypothesis→fallback robustness | FIXABLE (near-SOUND) | H1/H2/B0-fail/F-G1 coverage is exemplary; gaps: H1b has no verbatim fallback, H3/H4 fallbacks cover only joint failure (mixed combos unworded), and total-censoring (Ω→0) leaves E1 without pre-committed wording. |
| 5. Method scope & RQ design | FIXABLE | All A2 mandatory shapes present; 8 RQs ↔ 8 hypotheses, kills pre-empted; missing: scaffold-generality arm, a decision rule for the 0.6–0.8 "partial" band, and a named primary judge protocol. |
| 6. Prior-work reliability | PARTIALLY RELIABLE | Item 2's residual gap honestly recorded and confirmed; but items 4/5/6 were partially rubber-stamped (seven-slot completeness is false at the individual-H level; the power fix introduced the H4a contradiction unnoticed), and 3/7 backfilled titles are wrong. |

**Overall: NEEDS-REVISION** (bottom of file).

---

## Findings (ranked most-severe first)

### F1 [BROKEN] The Phase-A-added H4a power rule contradicts the pre-registered backbone grid — H4a is structurally INCONCLUSIVE as written

Evidence: `paper.md` §Power pre-declaration: *"a family with fewer than 3 same-family backbones in the Stage-2 grid is pre-declared INCONCLUSIVE for the within-family agreement estimate and excluded from H4a's headline contrast"* — but the grid itself is *"6–8 backbones chosen to cross family with capability tier (**two sizes per family** where available)"* (`paper.md` E4 / digest N6 M2). Two per family < 3 for **every** family, so under the planned grid every family is excluded and H4a's headline contrast is empty before a single run. The Phase A gate (`stage_review.md` §6, "Fixed: added Power/INCONCLUSIVE") introduced this rule and did not check it against the grid it governs.

Fix: either (a) restate the rule at the *pair* level (H4a's permutation test needs ≥3 within-family **pairs pooled across families**, which 3–4 families × 1 pair each satisfies), or (b) enlarge to ≥3 backbones for ≥2 families. Then re-derive H4a's power from the actual pair count (≤28 pairs at K=8 — see F2).

### F2 [FIXABLE] Within-family pairs are tier-confounded by construction, undermining exactly the family-vs-capability question E4 asks

Evidence: with "two sizes per family," every within-family pair is a *cross-tier* pair, while cross-family pairs include same-tier pairs. So H4a's contrast ("mean within-family pairwise agreement exceeds cross-family by ≥ 0.10", `paper.md` E4) compares within-family-cross-tier against a mix — family effect and tier effect are entangled in the very contrast meant to separate them. R3 discipline ("constraint X removes confound Y") is not applied here: no design constraint names this confound. Pair-level n is also tiny (K=8 → 28 pairs; 3–4 within-family).

Fix: pre-register the two clean contrasts — (within-family, cross-tier) vs (cross-family, cross-tier) isolates family; (cross-family, same-tier) vs (cross-family, cross-tier) isolates tier — and state the pair counts each needs; or add a third same-family backbone at matched tier for ≥2 families.

### F3 [FIXABLE] "Scale-up is config, not code" is asserted but false for M4 and M6 — the walking skeleton never exercises the normalization arm or the judge factorial

Evidence: `paper.md` Step 9: *"Single frozen judge, T=0. No factorial, no normalization arm yet"* followed by *"Skeleton passed ⇒ pilot ... and Stage 2 are config changes (more tasks, more backbones, more judges), not code changes."* But Stage 2 requires the deterministic normalizer ν + a paraphrase model (M4) and a 3-judge cross-classified pipeline plus mixed-effects fitting (M6) — none of which exist at skeleton pass time. Building them later is new code, which is precisely the failure goal.md §8 gates on ("Skeleton pass criterion before scale-up; scale-up is config, not code") and guidance.md situation 8 names.

Fix: add to the skeleton one normalized-arm judging pass on ~10 traces and one second-judge pass (deterministic counts only, no model fitting), so every Stage-2 code path exists and only cardinalities scale.

### F4 [FIXABLE] Reference cache: the seven load-bearing records remain digest-less, and three carry *wrong titles* — worse than the recorded gap

Evidence (independently re-verified on disk): all 7 backfilled records have `digest_path: None`, `pdf_path: None`, `verified.id_resolves: false` (`reference_candidates.jsonl`). All 6 OpenReview IDs *do* resolve in `topics/corpus/ideas.jsonl` (checked; grounding is real, not confabulated). But the backfilled `title` fields were reconstructed from memory and 3 of 7 are wrong vs the corpus originals: BreakingBackbones2025 cache title "…through Backbone Model Vulnerabilities" vs corpus "Evaluating the Security of Backbone LLMs in AI Agents"; BiasScope2025 "Automated Discovery of LLM-Judge Biases" vs "BiasScope: Towards Automated Detection of Bias in LLM-as-a-Judge Evaluation"; MENLO2025 "Multilingual Evaluator Non-invariance in LLM Judges" vs "MENLO: From Preferences to Proficiency – Evaluating and Modeling Native-like Quality Across 47 Languages". Since goal.md §6 mandates `refs.bib` be *script-generated from the jsonl*, these wrong titles would propagate verbatim into the bibliography. Additionally, digest N3 citation keys (`[Who&When, OpenReview:GazlTYxZss]`) do not string-match cache keys (`WhoWhen2025`), so goal.md §3 item 2's "every N3 key is a `selected` cache record" holds only via manual id-mapping, not mechanically.

Fix: before Phase E — fetch PDFs, run `paper-digest` extraction on all 7, correct the 3 titles from the fetched metadata, and either rename N3 keys to cache keys or add an explicit `n3_key` alias field so the citation gate is mechanically checkable.

### F5 [FIXABLE] Fallback coverage has three unworded holes (individual-H and extreme-censoring outcomes)

Evidence: (a) H1b has no verbatim fallback — F-1 covers H1's stable/straddle outcomes, and `paper.md` E1 even *promotes* H1b to primary in the straddle case, but if H1 passes and H1b itself fails (no layer ordering, or reversed ordering), no pre-committed sentence exists; only `paper_draft.md` RQ2's falsification line gestures at it. (b) F-3 is scoped *"(if both fail)"* — the mixed outcomes (H3a passes/H3b fails; H3b passes/H3a fails) have no wording and no combination rule, violating guidance §3.1's "write the fallback-combination rules too… never invent combination logic at verdict time." F-4 has the same "(if unstructured)" joint scoping over H4a/H4b. (c) If Ω collapses toward 0 despite payload iteration (A2's gate is pilot Ω ≥ 0.5, with α-on-partial-cells as fallback — but α also dies if pairwise overlap is negligible), E1 has no pre-committed wording; the natural pivot ("censoring is near-total and capability-skewed; agreement is unmeasurable, which is itself the finding" — Claim 3 + H4b) exists in spirit but not as verbatim text.

Fix: add three verbatim sentences (H1b-fail incl. reversed direction per situation 4; per-H mixed wording for H3/H4 with explicit combination rules into F-3/F-4/F-G1; the Ω→0 outcome routed to Claim 3 as headline). Half a page of writing closes the entire failure space.

### F6 [FIXABLE] Feasibility pinch: A6's all-backbone clean-run restriction fights the capability-spread requirement, and the GAIA pool is smaller than the plan implies

Evidence: A6 restricts the headline analysis to *"tasks with clean-run success under all backbones"* (`paper.md` A6) while H4b requires a capability *spread* ("two sizes per family"; recovery-vs-capability correlation, ρ ≥ 0.5). The wider the spread, the smaller the clean-run intersection — including a weak backbone directly guts the analyzable grid. Then a second intersection (all-backbone *failure* under injection, Ω) is taken on top. The plan needs ≈300 base tasks (digest N6: "≈300 tasks × 3 fault layers"), but GAIA L1–2 with public answers is ~140 tasks, so most of the load falls on "WebArena-style tasks" — named but not sized, with self-hosted-environment engineering unaccounted in the 1–2 person-week estimate. No number anywhere estimates the expected size of the double intersection under a realistic weak-backbone clean-run rate.

Fix: pre-register the task-pool arithmetic (per-source counts; expected clean-run intersection under a pessimistic weak-backbone solve rate, e.g. 40%) and a pre-declared shrink axis per situation 10 (drop the weakest tier before dropping n per cell); size the WebArena slice explicitly.

### F7 [NOTE] B0 is a noise floor, not a null-by-construction placebo — but the design compensates, mostly

The test–retest arm is *not* null-by-construction: closed-weight T=0 re-execution is not bit-deterministic (provider-side nondeterminism), so within-backbone disagreement will be non-zero — the design knows this (A5 gate ≥ 0.9, "else all analyses model the noise floor explicitly") and pre-commits the premise-collapse wording (*"attribution labels are noisy, full stop"*, `paper.md` B0) — that is honest and correct routing. The actual null-by-construction element is the label-marginal-preserving permutation, but that placebo is *weak*: chance-corrected κ ≈ 0 under permutation by algebra, so it validates the κ code, not the pipeline. Boring-non-null risk for the test–retest arm: judge sampling noise alone could push within-backbone disagreement above 0.1 on long traces, tripping the premise gate for a reason unrelated to attribution. Fix (cheap): add one genuinely pipeline-level placebo — e.g., judge the *same trace* twice under the frozen judge (judge test–retest isolated from agent re-execution), and/or a no-op injection arm verifying the judge does not hallucinate a fault layer on successful traces.

### F8 [NOTE] The deepest rival explanation is named but its interpretation should be pre-committed in one place

B-alt covers the judge-side rival (style). The other genuine rival — *the injected fault genuinely cascades to a different decisive layer under a different backbone, so disagreement is faithful reporting of divergent failures, not measurement instability* — is distributed across digest C2, the tie-break rule (injected step = earliest decisive ⇒ ground truth stays the injected layer), and E2's agree-wrong tabulation, but no single pre-committed paragraph says what the headline claim becomes under this reading (answer: CO4's re-scoping survives either way, since the label still fails to transfer; only the "judges are unreliable" gloss falls). A reviewer will raise it; one paragraph pre-empts it.

### F9 [NOTE] Primary judge protocol underdetermined; partial-band decision unmapped

M3 lists two judging protocols (Who&When all-at-once and step-by-step) but Step 6 says "the pre-registered primary judge" (singular) without naming which protocol is primary — an analytic degree of freedom that must be frozen pre-B. Separately, the κ bands feed a binary decision (task property vs re-scope per CO4), but the 0.6–0.8 "partially stable" band's decision consequence is unstated beyond "layer-ordering becomes the claim" — say what a practitioner should *do* in that band.

### F10 [NOTE] Lethality iteration is an estimand-shifting knob

A2's mitigation ("iterate payloads toward irrecoverable-by-design faults") changes the fault population toward maximal-lethality artifacts, narrowing the validity envelope relative to organic failures; the Who&When complement mitigates but the Limitations section must name this envelope shift explicitly (R7). Frozen-before-Stage-2 payloads keep it pre-registered; just say so.

---

## Failure-space simulation (per-H walk-through)

| Hypothesis | If it FAILS | Covered? |
|---|---|---|
| H1 (κ CI < 0.8, instability exists) | F-1 verbatim: backbone-invariance *certification* claim, feeds F-G1 pivot (certification-protocol paper with pre-written pivoted abstract). Straddle case → "partially stable" band, H1b promoted to primary. | YES — both directions publishable; the strongest part of the spec. |
| H1b (exec > plan by ≥0.10) | No verbatim fallback in `paper.md`; reversed ordering (plan > exec) named only in stale `paper_draft.md` RQ2. | **GAP** (F5a) — small but real; wrong-direction outcome should get situation-4 full-prominence wording. |
| H2 (agree-wrong ≥ 0.05) | F-2 verbatim: consensus-as-correctness-certificate; majority-vote upgraded to contribution. | YES — clean both ways. |
| H3a/H3b (judge share > 0.20 / style share ≥ 0.10) | F-3 verbatim but scoped "(if both fail)": instability is agent-behavioral, strengthens E1. Mixed outcomes (judge-driven but style-blind; style-driven but judge-interchangeable) unworded. | **PARTIAL** (F5b). B-alt-wins outcome (judging artifact) has its own pre-committed mirror wording — good. |
| H4a/H4b (family structure / capability-skewed censoring) | F-4 verbatim "(if unstructured)": no amortization of re-validation. But H4a is structurally INCONCLUSIVE under the current grid+rule (F1), and INCONCLUSIVE ≠ FAIL — F-4's wording does not license itself from an INCONCLUSIVE. | **BROKEN until F1 fixed**; then PARTIAL (mixed outcome unworded). |
| B0 premise gate fails (cross ≤ within + 0.05) | Pre-committed: "attribution labels are noisy, full stop" — itself a publishable reliability exposé. | YES. |
| A4 fails (judge κ < 0.7) | Pre-committed: human-coded 200-trace subset becomes primary data. Note: at n=200 most H* fall to INCONCLUSIVE per the study's own cell minima — the fallback paper is then a small-n reliability study; survivable but thin. | YES, marginal. |
| A2 fails hard (Ω → 0 even after iteration) | α-on-partial-cells pre-committed; but if pairwise overlap is also negligible, no wording exists. | **GAP** (F5c). |
| All-fail / global | F-G1 pivoted abstract pre-written; B0-fail routes *around* F-G1 correctly ("F-G1 does not even apply"). | YES. |

**Is there any outcome that leaves the paper with nothing?** Only one uncovered corner: extreme censoring with a noisy-but-passing B0 — agreement unmeasurable, premise intact, no pre-committed sentence (F5c). Everything else lands on pre-written text. After the F5 fixes, the failure space is closed.

## Missing RQs / reviewer questions the design cannot currently answer

1. **Scaffold generality** — every number comes from one ReAct-style scaffold; t6's covariate reporting does not answer "is the instability scaffold-specific?" A minimal second-scaffold arm on a task subset (even 30 cells) or an explicit narrow-envelope concession per situation 14(b) is needed.
2. **Family vs tier disentanglement** — as designed, cannot be answered (F1/F2).
3. **What does the partial band (0.6 ≤ κ < 0.8) tell a practitioner to do?** The decision the estimand "feeds" (CO4) is only defined at the band edges (F9).
4. **Which judge protocol is the primary instrument?** (F9) — an unfixed analytic degree of freedom; a reviewer will call it garden-of-forking-paths.
5. **Are the 200 human-anchored traces disjoint from the evaluation traces?** R8 requires validation/evaluation disjointness; the spec never states the sampling rule for the 200-trace subset.
6. **Is disagreement mis-measurement or genuine causal divergence?** (F8) — needs one pre-committed interpretive paragraph.

## Reliability audit of prior Phase A result

Re-verified items 4, 5, 6 of goal.md §3 (the ones most plausibly rubber-stamped) plus item 2 and cache spot-checks:

- **Item 2 (cache integrity) — recorded REVISE-with-residual: ACCURATE, and understated.** Confirmed: the 7 load-bearing records have no `digest_path`/`pdf_path`, `id_resolves: false`. Independently verified all 6 OpenReview IDs resolve in `topics/corpus/ideas.jsonl` with on-topic papers — the grounding is real, not invented. NEW finding the gate missed: 3/7 backfilled titles are paraphrases that do not match the corpus titles (BreakingBackbones2025, BiasScope2025, MENLO2025 — exact strings in F4), and N3 keys don't string-match cache keys, so the "N3 cites only selected keys" gate is not mechanically checkable.
- **Item 4 (claim–evidence orphans) — recorded PASS: MOSTLY HOLDS.** Every claim-map row traces to an H-id or supported-by-design status; but "every H-id has a fallback" is true only at H-*family* granularity — H1b individually has none (F5a). Mildly rubber-stamped.
- **Item 5 (seven-slot completeness) — recorded "REVISE (fixed)" claiming only aggregation was missing: PARTIALLY RUBBER-STAMPED.** The aggregation fix is real and well-written (`paper.md` §Aggregation rule). But the fallback slot is incomplete for H1b, and F-3/F-4's joint-failure scoping leaves mixed outcomes without pre-committed combination rules, which §3.1 explicitly requires. "Every H\* fills all seven slots" is false as recorded.
- **Item 6 (Part 6 self-check / method rigor) — recorded "REVISE (fixed)": PARTIALLY RUBBER-STAMPED.** The three added sections (Estimand, R2, Power) genuinely exist in `paper.md` and are substantive. But the Power fix *introduced* the H4a-vs-grid contradiction (F1) and the gate signed off without checking the new rule against the design it constrains; item 7 (R3 one-liners) was passed on an admitted "even if not always phrased as a literal one-liner" basis, and the family/tier confound (F2) has no one-liner at all.
- **Cache spot-checks (3 records): CLEAN.** `Beyond4058`, `DICE2629`, `Safe4556` — all `digest_path`/`pdf_path` resolve on disk under `arxiv_corpus/arxiv_miner_cache/`; all three `why` texts are specific to B2.3's design (variance-decomposition precedent; judge-bias support for A4; cross-backbone factorial+validated-judge structural analog). No cross-topic contamination detected.
- **Item 1 (digest self-verification) — verified:** N6/N7/N8/N12 do now carry status/absence_comment blocks as the gate claims; N3 keys, C-ids, M-ids cross-resolve.

Net: the prior gate's *honesty* is good (its one blocking residual is real and correctly scoped), but its *thoroughness* on items 4–6 was partial — two of its own "fixes" (Power rule, aggregation) were never re-checked against the design grid and the fallback ladder they modify.

## Overall: NEEDS-REVISION

The core design is a genuinely well-shaped A2 measurement study — non-bridge asymmetry, real estimand, censoring treated as first-class, an unusually complete fallback ladder, and every A2 mandatory experiment shape present. Nothing here is unsalvageable; but four defects would surface at Phase B/C or at review time if not fixed now.

**Three highest-leverage fixes:**

1. **Repair E4:** restate the H4a power rule at the pair level (or add a third same-family backbone for ≥2 families) and pre-register the two clean family/tier contrasts with pair counts — as written, H4a is empty by construction (F1, F2).
2. **Make the cache load-bearing for real:** fetch + `paper-digest` the 7 backfilled works, correct the 3 wrong titles from fetched metadata, unify N3↔cache keys, and run one targeted re-harvest on topic-specific angles ("cross-backbone failure attribution", "LLM judge agreement agent traces", "fault injection agent evaluation") so the non-pre-emption claim rests on a real search, not on 147 off-topic hits plus memory (F4, novelty dimension).
3. **Close the failure space and the skeleton gap:** add the three missing verbatim fallbacks (H1b incl. wrong-direction, H3/H4 mixed-outcome combination rules, Ω→0 wording) and extend the walking skeleton to exercise one normalized-arm pass and one second-judge pass so "scale-up is config, not code" becomes true instead of asserted (F5, F3).

---

## Fixes applied (2026-07-04)

Applied directly after coordinator authorization; edits are surgical and each is marked in-file with "(added/amended/restated 2026-07-04 per design_review.md F\*)". No results or validation numbers were fabricated.

1. **F1** — `paper.md` §Power: H4a INCONCLUSIVE rule restated at the **pair level** (≥3 within-family pairs pooled across families; ≥6 cross-family pairs), resolution choice documented in-file (reword under the existing 2-per-family grid; no grid extension, no added cost); whole-H4a INCONCLUSIVE routing replaces the self-contradicting per-family rule.
2. **F2** — `paper.md` E4: tier-composition confound named per R3 with the removing constraint (family contrast restricted to cross-tier pairs on both sides; orthogonal (cross-family, same-tier) vs (cross-family, cross-tier) contrast estimates the tier effect; pair counts reported per arm).
3. **F4 (titles)** — `reference_candidates.jsonl`: 3 memory-paraphrased titles corrected to exact corpus originals (BreakingBackbones2025, BiasScope2025, MENLO2025), each `why` annotated with the correction; digest-less status (`digest_path`/`pdf_path` null, `id_resolves: false`) left honestly recorded as the blocking residual.
4. **F5a** — `paper.md` E1: verbatim fallback **F-1b** added for H1b (no-ordering wording + wrong-direction full-prominence wording per situation 4).
5. **F5b** — `paper.md` E3/E4: pre-committed mixed-outcome wordings added for H3a/H3b and H4a/H4b; new §"Fallback-combination rules" pins B0-fail dominance, F-C0 pre-emption, F-G1's exact joint-failure conjunction, and the B-alt-wins ∘ F-1 non-composition.
6. **F5c** — `paper.md`: new §"Extreme-censoring fallback F-C0" — Ω→0 outcome routed to a pre-committed pivot (censoring/feasibility bound becomes the headline via Claim 3 + H4b promotion; H1/H2/H3 INCONCLUSIVE, archetype stays empirical). The one previously-empty failure outcome is now covered.
7. **F3** — `paper.md` Step 9: skeleton arms extended with a vendor-disjoint secondary judge pass (minimal M6 path) and a deterministic-normalizer pass (M4 path, ν idempotence check); pass criterion (v) added; cost updated ≤216 judge calls / <$25; paraphrase arm pre-declared as the single config-only exception.
8. **F4 (harvest honesty)** — `paper.md` Claim–Evidence Map row 1 status qualified ("grounding currently weak") + new "Harvest caveat on Claim 1" paragraph barring Phase-E assertion of non-pre-emption until the named-angle re-harvest runs; `digest.md` N3 given a matching "Harvest-adequacy caveat" with the same five named re-harvest angles and situation-6 routing.

Not fixed here (needs human/compute, unchanged blocking residual): fetching PDFs + running `paper-digest` extraction on the 7 backfilled works; executing the named-angle re-harvest; N3↔cache key unification (recommend adding an `n3_key` alias field when the backfill runs); F6 task-pool arithmetic (needs real per-backbone clean-run rates from the skeleton); F7's cheap pipeline-level placebo and F8/F9 interpretive paragraphs remain recommendations.
