# Pengsida Stage Review — B2.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon (label instability) occurs" with no new attribution algorithm proposed as a fix — the instrument built here (censoring-aware metrics, judge×agent factorial, style-normalization arm, manifestation-accuracy check) is the *analytical apparatus* that makes the phenomenon measurable, not a method competing to win a benchmark. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1, and matches `paper.md`'s own Step 2 archetype call ("Primary: empirical (measurement study)... in the pattern of Emergent-Abilities-Mirage / LLMs-Get-Lost"). Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. The confirmed Stage 2 motivation states the stakes concretely and specifically: "a single low agreement number is actionable in only one blunt way... decomposing the instability turns an abandon-ship finding into an actionable one" — this is a first-principles framing of *why the decomposition matters*, not a generic AI-importance appeal, and it ties directly to Stage 1's fourth output (the variance decomposition) rather than motivating only the headline instability number. The Einstein ratio holds in the assembled Introduction: paragraphs 1–2 are pure problem/stakes ("someone has to say why... does the label survive if the backbone changes?"), with zero method leak before paragraph 5.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The confirmed Stage 3 output (`pipeline.md`) threads each related work into a problem-tied limitation — e.g. "AgenTracer's fault-injection labels are correct by construction only within the execution stack that was replayed... cross-backbone label stability is neither measured nor claimed" — which clears the "citation dump" failure mode. But the *table itself never ranks the seven works by closeness*, unlike `pipeline.md`'s own reasoning in Stage 4, which quietly treats Who&When and AgenTracer as the two works motivating the largest share of the sub-problems (`sp_manifestation_divergence` traces to both jointly). A reader of only the first assembled `paper_draft.md` Related Work section would see four thematic paragraphs of roughly equal weight and have to infer for themselves which single prior work sits closest — per the Stage 2 bar, "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the opening of the Related Work section, naming Who&When and AgenTracer as the closest prior work and stating the precise delta (both attribute via a decisive-error definition inside one execution stack; neither crosses the backbone axis), rather than leaving the reader to rank four parallel threads unaided.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely before it is used — the failing intersection $\mathcal{I}$, the failure-overlap rate $\Omega$, the agree-wrong mass, and the style-share are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: the Methodology's Manifestation-Accuracy Check states explicitly that "agreement among backbones alone cannot distinguish 'backbones manifest and diagnose the fault identically and correctly' from 'backbones manifest the fault differently but converge on the same wrong label'" and that only a comparison against the injected ground truth resolves this — exactly the step that keeps "stability" from being silently conflated with "correctness," stated as an argument rather than asserted by fiat. No orphan components — every one of the six modules (censoring-aware protocol, judge×agent factorial, manifestation-accuracy check, style-normalization arm, codebook tie-break gate, family-capability crossing) traces to a named sub-problem in `pipeline.md`, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (RQ4's agree-wrong tabulation and RQ6's tie-break re-scoring are genuine falsification designs: each recomputes a verdict under an alternative condition to see if it *changes*, not just correlates). But the first assembled draft's RQ subsections stopped at "**Expected outcome.** ... rather than 'stable'" without stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `paper.md` already had this discipline (its Step 6 "Fallback" clauses, e.g. F-1 through F-4 and the B0/B-alt controls) that did not survive into the first assembled `paper_draft.md`'s RQ subsections.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all eight RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s Step 6 fallbacks F-1–F-4 and the B0 test–retest / B-alt style-normalization controls).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Autonomous LLM agents now run multi-step pipelines... and when one of these pipelines fails, someone has to say why" / "Yet a basic question about this infrastructure remains unexamined: does the label survive if the backbone changes?" / "The nearest existing work approaches this gap from directly inside the attribution problem but never crosses the axis this paper is built to test" / "Turning 'does the label survive the swap' into a measurable question surfaces its own difficulties" / "Our approach turns each of these obstacles into a design decision rather than a hedge" / "We evaluate this design across a fault-injection suite...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across Abstract, Introduction, and Contributions bullets: "a plan/tool/execution label silently asserts an invariance its measurement pipeline never established." The Conclusion names two real forward-looking limitations (the codebook's stipulated-partition problem, and the synthetic-fault-only scope relative to production deployments) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph (and mirrored in the Introduction's related-work paragraph), naming Who&When and AgenTracer as the closest prior work and stating the delta plainly (rather than leaving four thematic paragraphs unranked).
2. **Stage 4 fix** — added a **Falsification condition** line to each of the eight RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run against goal.md §3's checklist (items 1–8), applying guidance.md as the standard, over `README.md` / `digest.md` / `paper.md` and the upgraded `reference_candidates.jsonl`. This is a distinct pass from the "Stages 1–5" review above (which is `auto-research-discussion`'s internal stage review, run before `paper_draft.*` was assembled) — this section is goal.md's own Phase A gate over the three input files. Date: 2026-07-04.

### 1. Digest self-verification — **REVISE (fixed)**

`digest.md`'s own convention (per its REVERSE-DIGEST NOTICE) is that every node carries a `**status**` + 3-part `**absence_comment**` unless the node is fully `[GIVEN]`. N0, N1, N2, N3, N4, N5, N9, N10, N11 all had this; **N6 (Methodology), N7 (Contributions), N8 (Research Questions), and N12 (Contribution Type) did not**, even though every field in all four is `[HYPOTHESIS]`/`inferred` (non-GIVEN). Cross-node references checked out otherwise (N6 challenge_arguments → N5 `challenge_id`s all resolve; N8 `evaluates_mechanisms`/`addresses_challenges`/`tests_contributions` all resolve into N6/N5/N7 ids; Claims 1–5 all cite real N-nodes).
**Fix applied**: added `status`/`absence_comment` blocks to N6, N7, N8, N12 in `digest.md` (guidance.md Part 6 self-check; goal.md §3 item 1).

### 2. Reference-cache integrity — **REVISE (partially fixed; one residual action item)**

Before this pass, **none of the seven works `digest.md` N3 actually cites and grounds N4/motivation on** — Who&When (OpenReview:GazlTYxZss), AgenTracer (OpenReview:l05DseqvuD), MAST (arXiv:2503.13657), Breaking Agent Backbones (OpenReview:kga18ld70t), PreferenceLeakage (OpenReview:grIvSXVJ65), BiasScope (OpenReview:QGOw6AU8Lp), MENLO (OpenReview:QOWYX3Q2XS) — **appeared anywhere in `reference_candidates.jsonl`**. The 150-candidate harvest (110 arXiv + 40 OpenReview/ACL) was drawn from a generic recall pass over an unrelated corpus (`arxiv_miner_cache` recent-preprint dump + a stock 2023 ACL-Anthology sample) and never actually retrieved the load-bearing related work that `digest.md` had separately grounded against `topics/corpus/ideas.jsonl`. This is exactly goal.md §3 item 2's failure mode: "every N3 key is a `selected` cache record" was false.
**Fix applied**: backfilled all seven N3-cited works into `reference_candidates.jsonl` as `verdict: selected` records (keys `WhoWhen2025`, `AgenTracer2025`, `MAST2503`, `BreakingBackbones2025`, `PreferenceLeakage2025`, `BiasScope2025`, `MENLO2025`), with `relevance` set per their role already established in `digest.md`/`paper.md` (`baseline` ×2, `method-twin` ×1, `contrast` ×1, `background` ×3) and `why` quoting the specific limitation each supports.
**Residual gap (not fixed — flagged for pre-Phase-E work, guidance.md Part 5 "when the cache is thin, re-harvest")**: none of the seven backfilled records has a locally cached `pdf_path`/`digest_path` (`verified.id_resolves: false` for all seven) — they were reconstructed from `digest.md`'s own N3 approach-summaries, not independently re-digested. Of the 150 originally-harvested candidates, after individual review only **3 were genuinely selectable** (2 `adjacent`, 1 `background` — see §Task-1 summary below); the other 147 are off-topic by generic keyword overlap only. Per Part 5, a thin/misdirected cache means **the harvest was inadequate, not the field empty** — before Phase E, re-run the harvest with angles specific to this topic (e.g. "LLM agent failure attribution backbone", "cross-model LLM judge agreement fault injection", "plan tool execution taxonomy stability") and fetch+digest (via `paper-digest` extraction mode) the seven backfilled records properly.

### 3. Tag discipline — **PASS**

No untagged assertion found in `digest.md`; every field carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`. `paper.md` carries its own explicit disclaimer ("Status: specification, no experiments run. All thresholds below are pre-registered decision rules, not results.") which functions as the tag-discipline statement for the downstream document; no HYPOTHESIS→GIVEN promotion detected (e.g. N9's results remain explicitly `PLACEHOLDER`/`missing evidence_strength` throughout, not silently asserted).

### 4. Claim–Evidence Map completeness — **PASS**

Every row in `paper.md`'s Claim–Evidence Map traces to an H-id (H1/H1b, H2, H3a/H3b, H4a/H4b) or a `supported-by-design` literature-grounded status; every H-id has a named fallback (F-1…F-4) or is covered by the global pivot F-G1; no orphans in either direction (checked against Step 6's E1–E4 and the digest Claims list 1–5).

### 5. Hypothesis/assumption machinery — **REVISE (fixed)**

- Every A1–A7 already filled guidance.md §3.2's assumption-ledger slots (failure_mode/detection/gate) — PASS, no fix needed.
- B0 (same-backbone test–retest + chance floor) and B-alt (style-normalization + judge-swap rival-explanation arm) and F-G1 (global pivot, pre-committed pivoted abstract) were all present with pre-committed wording — PASS, no fix needed.
- **But** every H\* (H1, H1b, H2, H3a, H3b, H4a, H4b) was missing guidance.md §3.1's **aggregation** slot (the pre-registered vote rule across independent instruments/settings) — none of Step 6's E1–E4 blocks stated how a verdict should be reconciled across the study's two base-task families (GAIA-derived vs. WebArena-derived cells).
**Fix applied**: added an "Aggregation rule" section to `paper.md` (guidance.md §3.1) stating the pooled-vs.-per-family vote rule (≥1 of 2 family-specific verdicts must agree with the pooled verdict, else the claim downgrades to family-conditional) and clarifying Who&When's role as a non-voting third data point.

### 6. Method-rigor audit — **REVISE (fixed)**

Checked against guidance.md Part 6 items 1–10 and the A2 (empirical/measurement) evidence standard in Part 2:
- **Item 1 (Estimand in one sentence, R1)** — missing; Step 0/2/5 stated the asymmetry and formal notation but never one estimand sentence (quantity + unit of analysis + reference population + decision fed). **Fixed**: added `## Step 1 — Estimand` to `paper.md`.
- **Item 6 (every instrument has the 5-step R2 plan with an acceptance threshold)** — the M3 attribution codebook only had steps ① (ground in Who&When/MAST) and ③ (validate against 2 human raters, κ≥0.7) explicit; steps ② (calibration-refinement with named merge/split ops on a held-out set) and ④ (confusion-structure inspection) and ⑤ (freeze/hash before scale) were missing. **Fixed**: added `## Instrument validation (guidance.md R2)` to `paper.md` with all 5 steps and their acceptance thresholds.
- **Item 9 (power stated per cell; thin cells pre-declared INCONCLUSIVE)** — only H1/H1b had a power statement (and only in aggregate, not per cell); H2/H3a/H3b/H4a/H4b had none, and no cell anywhere was pre-declared INCONCLUSIVE (situation 5 requires this). **Fixed**: added `## Power / INCONCLUSIVE pre-declaration` to `paper.md` covering H2/H3a/H3b/H4a/H4b with named minimum cell counts and the INCONCLUSIVE rule.
- Items 2 (verb check), 4 (every A\* has detection+gate), 5 (B0/B-alt/F-G\* present), 7 (design constraints name their confound — satisfied by M4/M6/B-alt's explicit confound-removal reasoning, even if not always phrased as a literal one-liner), 8 (≥1 mechanism analysis — RQ_INF_2/RQ_INF_3 supply this) all **PASS** as originally written.
- Part 2 A2 evidence standard (validated instrument + controlled comparison + pre-registered effect-size floors + rival-explanation ablations + ≥1 mechanism analysis) is met by the plan as revised.

### 7. Stage cross-check (advisory) — **PASS (already applied)**

`pengsida-stage-reviewer`'s pass (Stages 1–5 above) already ran N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E\*↔Stage 4, archetype-from-`paper.md` before `paper_draft.*` was assembled, and both its REVISE findings (nearest-neighbor sentence; falsification conditions) are already folded into `paper_draft.*`. No new STOP-level finding from this Phase-A pass.

### 8. Taste audit currency — **PASS, no re-run needed**

`taste_audit.md` predates this session's edits, but none of this pass's fixes touched the asymmetry statement (Step 0) or the formal definition (Step 5) — the new Step 1/Instrument-validation/Aggregation/Power sections are additive machinery, not a reframing. No re-audit triggered.

### Task-1 reference-cache summary (for cross-reference)

150 originally-harvested candidates processed individually (digest skimmed for each; PDF text not needed — no candidate was both ambiguous and plausibly load-bearing): **3 selected** (`Beyond4058` — background; `DICE2629` — adjacent; `Safe4556` — adjacent), **147 rejected**, each with a paper-specific one-sentence reason in `reference_candidates.jsonl`. Plus **7 backfilled** N3-grounding records (see item 2 above). Total cache: 157 records, 10 selected / 147 rejected.

### Overall Phase A gate: **REVISE → fixes applied this session; one residual pre-Phase-E action item remains (item 2's PDF/digest backfill)**

All directly-fixable static-document gaps (items 1, 5, 6) were fixed in `digest.md`/`paper.md` in this session and are reflected in those files now. Item 2's cache-integrity gap was fixed at the record-existence/verdict level but **not** at the digest-depth level (no PDF fetched, no `paper-digest` extraction run on the 7 backfilled works) — per the task's compute boundary ("no real experiment compute exists in this environment; stop at the Phase A gate"), that residual re-harvest is logged as the next action, not performed here. No STOP-level finding. Phase B is not entered in this session regardless of gate outcome, per the task's explicit scope.
