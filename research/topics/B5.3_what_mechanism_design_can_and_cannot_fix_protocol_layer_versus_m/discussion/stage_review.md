# Pengsida Stage Review — B5.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **against the first assembled `paper_draft.md`** rather than against the raw `pipeline.md` structured fields alone — this is what lets the review quote actual sentences (an Introduction paragraph, a Related Work sentence, an RQ subsection) instead of grading a schema in the abstract, matching how the calibration run (`B5.5/discussion/stage_review.md`) was actually conducted. Two structural requirements — an explicit nearest-neighbor sentence in Related Work, and an explicit Falsification-condition line per RQ — were written into the draft from the start (`paper_assembly.md`'s rules for this run require both explicitly), so this review checks that both are genuinely present and load-bearing rather than re-discovering them as new findings. One real REVISE fired anyway, in Stage 5, from actually running the reverse-outline test rather than assuming the prose would pass; it is fixed below and already reflected in `paper_draft.md`/`.tex`.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon occurs" with no new pipeline proposed as a fix — the six-part apparatus (category taxonomy, ground-truth scorer, deterministic enforcement, dual-attacker confound control, validity audit, defense-recovery test) is the *analytical apparatus* that makes the boundary observable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — the Introduction's second paragraph states the gap in first-principles terms ("a protocol can only make an action unprofitable if that action lives inside the space it can observe and mechanically enforce... negotiation manipulation does not respect that boundary"), not a patch-shaped complaint, and the stakes are concrete: misallocated defense-engineering investment and a sub-field's claim to exist resting on an untested assumption. The Einstein ratio holds — paragraphs 1–2 of the Introduction are pure problem/stakes, with the protocol-layer mechanisms named only as the *existing* engineering answer being questioned, not as this paper's own proposed fix.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: PASS**

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded — each ends on a problem-tied limitation, not a generic one (e.g., mechanism-design networks "deliver strong guarantees, but only over a formal, well-defined action space... that has nothing to say about a negotiator who can also persuade, fabricate context, or renege through a natural-language channel the mechanism never observes"), which clears the citation-dump failure mode. The nearest-neighbor sentence is present up front, not buried: "The closest prior work to this paper sits on opposite poles of the boundary this paper measures... auction-design networks such as AMenuNet already deliver incentive compatibility by construction, and work on strategic dishonesty already shows that model-layer probing can catch deception that fools output-level checks — but neither crosses a manipulation-category axis with a protocol-constraint axis in the same bilateral negotiation setting." All nine deep-tier related works from `pipeline.md`'s confirmed Stage 3 appear in the four threads; none is dropped silently.

**Checked but not flagged:** the corpus-only citation constraint (no fabrication) means literature coverage is bounded by what the local corpus actually returned (digest N3's own search-honesty note) — this is an honest, disclosed limit rather than a fixable gap, and matches the calibration run's treatment of the same constraint.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely before it is used — the manipulation-category taxonomy, the ground-truth scorer, and the deterministic enforcement design are all given in Problem Definition/Methodology ahead of any claim that invokes them. The inferential chain is licensed at its load-bearing hinge, stated explicitly rather than asserted by fiat: "structural conformance and content truthfulness are logically independent properties of a message, [so] the only way to avoid conflating them is to score success against the hidden parameters a message's content should have matched, never against the message's form." No orphan components — all six methods (taxonomy, scorer, enforcement, confound control, validity audit, defense-recovery test) trace to a named sub-problem in `pipeline.md`, with no leftover machinery; this was checked directly against `pipeline.md`'s cross-stage consistency pass rather than re-derived from scratch.

**Note for Stage 4:** the discharge test here isn't ablation — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: PASS**

**Why, quoting the draft:** Every one of the six RQ subsections states a **Falsification condition** distinct from its Expected outcome, not a restatement of the outcome's negation — e.g., RQ4's falsification condition ("refuted if the protocol effect's sign disagrees between the two attacker arms in a majority of categories, which would mean apparent protocol effects are largely an artifact of attacker competence") names the strongest alternative explanation (attacker-competence artifact) and states exactly what result would establish it, which is the discharge test this archetype variant asks for. RQ3 is a genuine falsification design in its own right — attack-execution rate is checked *against* manipulation-success rate specifically to rule out "the ladder suppressed the attempt" as an alternative to "the ladder defeated the attempt," not merely reported alongside it.

**Checked, not blocking (anticipatory, per `mined_review_checks.md`'s default minor severity for design-stage documents):** the Experimental Setup does not state a contamination/leakage check for the three source corpora (CraigslistBargain, Deal-or-No-Deal, CaSiNo) against the model families' likely pretraining data — a real reviewer question for anything LLM-evaluation-based, but not fixable at the design-spec stage without inventing a procedure the pipeline outputs never specified. Noted here as a watch item for the eventual experiments write-up, not a design defect serious enough to gate this draft.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first-pass draft:** The reverse-outline test mostly passes — paragraphs 3–6 each open with their single message ("The nearest existing work approaches this from either side of the boundary without crossing it" / "Turning this gap into a measurable question surfaces four difficulties of its own" / "Our approach turns each of these obstacles into a specific design choice" / the evaluation preview). But paragraph 1's first sentence, as originally drafted, was scene-setting rather than the paragraph's actual message: *"Autonomous LLM agents are beginning to negotiate real transactions on behalf of their principals... without a human reading every message first."* The paragraph's real point — that protocol-layer constraint is the field's default, assumed-sufficient answer to this — only arrived in sentence 2 ("The default engineering answer to keeping these negotiations honest is a protocol-layer one..."). Per the Stage 5 bar, a paragraph whose point arrives in sentence 2 rather than sentence 1 is a buried message, not a pass, even though the paragraph is otherwise well-formed and the rest of the Introduction's arc reconstructs cleanly from first sentences alone.

**THE ONE FIX (applied):** Merge the scene-setting clause into the same sentence as the paragraph's actual claim, so sentence 1 itself states the message: *"As autonomous LLM agents begin negotiating real transactions on behalf of their principals — clearing a price, splitting a resource, settling contract terms, often without a human reading every message first — the default engineering answer to keeping these negotiations honest is a protocol-layer one: constrain what an agent is allowed to say, not what model is saying it."* This was applied to `paper_draft.md`'s first paragraph (and carried into `paper_draft.tex`) before the draft below was finalized.

**Re-checked after the fix:** reading only each paragraph's first sentence now reconstructs the full six-move arc (default-answer premise → gap and doubt → nearest prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in the abstract, the Introduction's second paragraph, and the title's "Enforceable, Not Certifiable" framing: "a protocol can only make an action unprofitable if that action lives inside the space it can observe and mechanically enforce." The Conclusion names two real forward-looking limitations (ladder/model-family scope; the fact-table residue) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 5 fix** — rewrote the Introduction's first paragraph so its single message (protocol-layer constraint as the field's default, assumed-sufficient answer) lands in sentence 1 instead of arriving in sentence 2, in both `paper_draft.md` and `paper_draft.tex`.

No other REVISE or STOP fired. The nearest-neighbor sentence (Stage 2) and the per-RQ falsification-condition lines (Stage 4) were verified present and load-bearing rather than discovered as gaps, since `paper_assembly.md`'s rules for this run required both explicitly from the first assembly — this review's job on those two points was to confirm the requirement was actually met, not to re-earn credit for following an instruction already given.

---

## Phase A (re-run)

> Date: 2026-07-04. This is goal.md §3's Phase-A validation checklist (distinct from the auto-research-discussion Stage 1-5 review above, which checks prose construction quality against `stages.md`/`archetypes.md`; this pass checks the bundle — `README.md`, `digest.md`, `paper.md`, `reference_candidates.jsonl` — against goal.md's own gate, applying guidance.md as the standard). Run immediately after Task 1's reference-cache rewrite (150 ad hoc harvest records converted to the canonical schema, selected/rejected per candidate). Phase B/C are out of scope in this environment (no real experiment compute) — this run stops at the Phase A gate per its own instructions.

**1. Digest self-verification — PASS.** Re-executed `digest.md`'s own Self-verification pass: all of N0-N12 plus Claims are present; every non-FOUND node (N0, N1, N2, N3, N10, N11) carries a full 3-part `absence_comment`; `N4.affects_works` ⊆ N3 citation keys verbatim (checked all 9); `N6.challenge_arguments[].challenge_id` ∈ {C1..C5} and `mechanism_components` ⊆ {M1..M6}; `N8.addresses_challenges/tests_contributions/evaluates_mechanisms` ⊆ valid id sets; `N9.results[].rq_id` ∈ {RQ1, RQ_INF_1, RQ_INF_2} = N8 ids. No dangling cross-references found.

**2. Reference-cache integrity — REVISE, fixed.** The 150 ad hoc harvest records in `reference_candidates.jsonl` (Task 1's input) contained **none** of the 9 external works `digest.md` N3 actually cites (AMenuNet, UCB-S, StrategicPersuasion, StrategicDishonesty, AmongUs, HonestyBestPolicy, SOTOPIA, ThreatSnapshots, HonestyHelpfulness) or the canonical Rosenschein & Zlotkin (1994) anchor — those are grounded via a separate 11,683-paper OpenReview idea-proposal corpus (`topics/corpus/ideas.jsonl`), not the per-topic arXiv/OpenReview harvest this file's lifecycle (goal.md §1) describes. Literally applying "every N3 key is a `selected` cache record" would have failed outright.
Fix applied (in Task 1's rewrite): backfilled all 10 works as `selected` records with relevance matching their N3/N4 role (`baseline`: AMenuNet, UCB-S, SOTOPIA, Rosenschein & Zlotkin; `method-twin`: StrategicPersuasion, StrategicDishonesty, AmongUs; `adjacent`: HonestyBestPolicy, ThreatSnapshots; `background`: HonestyHelpfulness), each `why` citing the exact digest.md N3/N4 sentence it backs. Spot-checked 3 ids by fetching the corpus record directly (cNb5hkTfGC, IbDr8xgUMW, mM7VurbA4r) — all three resolve to real papers matching `digest.md`'s descriptions, not fabrications. No `pending` verdict remains anywhere in the 160-record cache.
**Residual, non-blocking gap:** the 10 backfilled records have `pdf_path`/`digest_path` = null (`verified.id_resolves: false`) — only corpus proposal-text is available locally, not a full PDF/digest under the standard convention. This is the cross-mechanism seam goal.md §9 already names as a standing TODO ("`paper-digest`... N3 grounded in the local cache... digest_path cache convention" not yet unified across the two corpora) — a skill-maintenance item, not a per-run defect, since `digest.md`'s own N3 header already discloses that these 9 entries are `[GROUNDED:corpus]` from proposal text rather than full digests.

**3. Tag discipline — PASS.** Every `digest.md` field carries an explicit `[GIVEN]`/`[HYPOTHESIS]`/`[PLACEHOLDER]`/`[GROUNDED:corpus]` tag; no untagged assertion found. `paper.md` states throughout that "no number below is a result; every threshold is a pre-registered commitment" and contains no numbers presented as findings. No silent `[HYPOTHESIS]`→`[GIVEN]` promotion found anywhere.

**4. Claim-Evidence Map completeness — PASS.** All 8 claims in `paper.md`'s Claim-Evidence Map trace to H1/H2/H3 or a Step-5 supported-by-design definition; H1/H2's family has fallback coverage via the global pivot F-G1; H3/RQ_INF_2 has its own dedicated fallback text. No orphan claims either direction.

**5. Hypothesis/assumption machinery — REVISE, fixed.** H1/H2/H3 fill guidance.md §3.1's seven slots in substance (applies_if / metric / test+alpha / effect_floor / aggregation / verbatim fallback), though organized under prose headers (Assumption/Hypothesis/Metric/Verification/Fallback) rather than the literal labeled-slot format — left as-is; a formatting preference, not a missing-content defect (advisory for Phase F). B0 + B-alt + F-G1 are all present with pre-committed wording — PASS. **Real defect found:** A1-A7 in `paper.md`'s Assumptions section filled the proposition/failure_mode/detection slots but had no explicit `gate: PG-*` label and no explicit `consequence:` clause naming which H\* degrades, is restricted, or is blocked — guidance.md §3.2 requires both, and Part 6 self-check item 4 ("Every A\* has a detection method and a gate?") fails without them. **Fix applied:** added explicit `Gate: PG-1..PG-7` and `Consequence:` clauses to all seven assumptions in `paper.md`, each naming the specific H\* affected and whether the failure blocks (A1, and A3 for its rung), narrows scope (A5), downgrades to undecided (A4, A7), or restricts to a sub-arm (A2, A6) — citing guidance.md §3.2.

**6. Method-rigor audit — REVISE, fixed.** Two gaps found against guidance.md Part 6 / Part 3.4: **(a)** no standalone one-sentence Estimand (R1: quantity, unit of analysis, reference population, decision fed) existed anywhere in `paper.md` — Part 6 item 1 fails as a self-contained document even though N1's objective made it reconstructable. **Fix:** added "Step 4 — Estimand (R1)" naming quantity=MSR, unit=one trial per (category,rung) cell, reference population=the three-corpus scenario pool, decision fed=the fixable/invariant/undecided adjudication. **(b)** no budgeted mechanism-layer analysis (R6, Part 6 item 8) explaining *why* an invariant verdict holds, beyond the headline MSR number. **Fix:** added a "Mechanism analysis (R6)" subsection decomposing residual P3 MSR into an AER-vs-MSR gap contrast (executed-and-succeeding vs. executed-and-blocked vs. never-executed) for every protocol-invariant category, using only already-computed M4 quantities. **Advisory, not blocking:** the R2 instrument-validation protocol is present only in abbreviated form (the κ≥0.7 human-audit gate, A1) without the full five-step sequence spelled out for the M1 taxonomy itself (the taxonomy's five categories are given directly by the seed's core question rather than learned from data, so steps ①②④ apply more weakly than to a data-driven rubric); recommend spelling out the freeze-before-scale step explicitly at Phase B time. R3 (confound-naming, in A3/B-alt) and R5 (rival→ablation pairing, B-alt) — PASS. R4/R7/R8 are correctly deferred to Phase D/E (no results exist yet to gloss or report).

**7. Stage cross-check (advisory) — PASS.** Already performed above (auto-research-discussion Stage 1-5 review): archetype classified Analysis/Finding-variant empirical measurement study; N1↔Stage1, N3/N4↔Stage2, N6↔Stage3, N8/E*↔Stage4 all cross-checked; the one REVISE that fired (Stage 5 Introduction paragraph) was fixed and is already reflected in `paper_draft.md`/`.tex`. No new stage-cross-check defect found in this re-run.

**8. Taste audit currency — PASS.** `taste_audit.md` audited the Motivation (Stage 2) and Method (Stage 5) summary text. This Phase A pass's edits (Estimand, assumption gates/consequences, mechanism-analysis paragraph) do not alter the Step 0 asymmetry sentence or the Step 5 formal definitions the taste audit evaluated — the recorded 🟢 "reads as human-shaped" verdict remains current; no re-run required.

### Phase A gate result: **PASS (post-fix)**

Items 2, 5, and 6 fired REVISE and were fixed directly in this pass (`reference_candidates.jsonl` backfilled; `paper.md` Assumptions given explicit gates/consequences; `paper.md` given an explicit Estimand and a mechanism-analysis plan). No item produced STOP. One non-blocking residual note carries forward (item 2's cross-corpus digest_path seam) and one advisory carries forward (item 6's abbreviated R2 protocol for the M1 taxonomy) — neither blocks Phase B, both are recorded here for the next agent who resumes this bundle. Per this task's scope, the run stops at the Phase A gate; Phase B (walking skeleton) requires real experiment compute not available in this environment.
