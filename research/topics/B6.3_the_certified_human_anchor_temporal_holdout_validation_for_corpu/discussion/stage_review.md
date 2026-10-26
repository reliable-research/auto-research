# Pengsida Stage Review — B6.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how much a phenomenon occurs" with no new pipeline proposed as a fix for it — the disentanglement controls, purity bound, composition-matched resampling, reference-swap test, and confidence-bound envelope are the *analytical apparatus* that makes the phenomenon (anchor drift) measurable and attributable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification, `paper.md` Step 2's explicit "Primary: empirical (measurement study)... not a new detector, dataset headline, or theorem," and Stage 1's confirmed `study_type: empirical`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "a pre-2022 document's authorship and the guarantee that document is assumed to license are not the same property, and they come apart under time" is a first-principles framing (naming the root asymmetry, not patching a symptom), and the stakes are stated concretely: an entire class of prevalence estimates inherits "an unstated and directional bias" if the convention is wrong, not a generic AI-safety appeal. The Einstein ratio holds — the Introduction's first two paragraphs are pure problem/stakes with zero method leak, and the critic round in `pipeline.md` Stage 1 caught and removed an actual method leak from an earlier draft's `constraints` field ("must hold source, genre, and token budget fixed" → refined to state the composition-confound *risk* rather than the token-budget-matching *technique*), which is exactly the kind of drift this stage exists to catch before it reaches the paper.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. the temporal concept-drift paragraph: "it targets classification-accuracy decay in a fixed feature space for a different domain (malware), not a calibrated false-positive-rate bound for a text negative-anchor"), which clears the "citation dump" failure mode. But the **first assembled draft's** Related Work section opened directly into the four thematic paragraphs with no single sentence stating, up front, which one prior work is the nearest competitor — a reader had to read all four threads and infer for themselves that the mixture-estimation framework was the closest, rather than being told plainly. Digest N3's own search-honesty note already names this ranking ("the closest, `[MonitorAIScale]`, uses a human reference corpus but never audits its temporal validity"), but that ranking had not yet been promoted into the Related Work section's own opening sentence. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the top of the Related Work section, naming the mixture-estimation framework as the closest prior work and stating the precise delta ("it never tests whether the reference's temporal composition confounds the estimated AI fraction — which is precisely the instrument this paper audits directly, rather than merely reusing"), rather than leaving the reader to rank the four threads unassisted. The same sentence was also folded into the Introduction's related-work paragraph for consistency, so a reader never encounters an unranked list of competitors in either location.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the disentanglement controls, the purity bound, the composition-matched resample, and the confidence-bound envelope are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge, stated explicitly in the Method Overview: composition-matching must be checked *before* the three-way disentanglement (style vs. leakage vs. staleness) is even meaningful, because "if year and corpus composition are entangled, a change in FPR_k(y) need not be a temporal signal at all" — this sequencing, caught during the Stage 4 critic round in `pipeline.md` (the `sp_confound_disentanglement` / `sp_composition_confound` overlap flag), is exactly the kind of hinge that makes the downstream attribution claim valid rather than assumed. No orphan components — every one of the five modules (disentanglement controls, purity bounding, composition matching, reference-age propagation, confidence-bound envelope) traces to a named sub-problem, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally (RQ4 is a genuine falsification design: recomputing the drift verdict on a composition-matched resample to see if the verdict *changes*, not just correlates; RQ5 likewise intervenes on the reference age directly rather than inferring propagation). But the **first assembled draft's** RQ subsections stopped at "**Expected outcome.** ... for at least 2 of the 3 detector families" without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," stated as an explicit check, not implied by the expected-outcome wording alone. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `pipeline.md`/`paper.md` material already had this discipline (`paper.md`'s Step 6 "Fallback F1/F2/F3" clauses and the "Falsification condition" lines already present in `paper.md`'s Results section, N9) that had not yet been carried into the RQ subsections of the assembled Markdown draft.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific observation that would refute each expected outcome — not a restatement of the outcome's negation in vague terms, but the concrete statistical condition (mirroring the rigor already present in `paper.md`'s N9 and Step 6 Fallback wording). This is now present in every RQ subsection of `paper_draft.md`/`.tex`.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Estimating how much of a corpus is AI-generated has quietly shifted..." / "Yet a pre-2022 document's authorship and the guarantee... are not the same property..." / "The nearest existing work approaches this gap from adjacent but distinct angles..." / "Turning this gap into a measurable question surfaces its own difficulties." / "Our approach turns each of these obstacles into a specific design choice rather than a hedge." / "We evaluate this design across multiple continuously-archived, hard-timestamped text sources...") reconstructs the whole five-move arc (practice → gap → prior work's nearest neighbor and shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and Introduction: "a document's authorship and the false-positive guarantee it is assumed to license are properties of different objects... so the guarantee can decay even when every label is correct." The Conclusion names two real forward-looking limitations (purity-check coverage; source/genre/language scope) rather than only recapping the abstract, and explicitly distinguishes what this paper measures from what a follow-up "drift-robust estimator" would need to fix — keeping the empirical scope honest rather than overclaiming a repair this paper does not attempt.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the opening of the Related Work section (and echoed it in the Introduction's related-work paragraph), naming the mixture-estimation framework (`MonitorAIScale`) as the closest prior work and stating the delta plainly, rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's checklist (the gate-file, distinct from the `pengsida-stage-reviewer` auto-research-discussion pass above, which reviewed the Stage 1–6 *discussion loop*, not the bundle's own `goal.md`/`guidance.md` compliance). Applies `guidance.md` as the construction standard. Date: **2026-07-04**. Reads: `README.md`, `digest.md`, `paper.md`, `discussion/reference_candidates.jsonl`.

### Checklist walk (goal.md §3, items 1–8)

1. **Digest self-verification** — **PASS.** Independently re-executed (not just re-read) every ID-consistency claim in `digest.md`'s own "Self-verification pass": `N4.limitations[].affects_works` ⊆ `N3` citation keys ✓; `N6.challenge_arguments[].challenge_id` ⊆ {C1–C4} ✓ and `.mechanism_components` ⊆ {M1–M6} ✓; `N6.unaddressed_challenges = {C2}` ⊆ {C1–C4} ✓; every `N8.RQ.evaluates_mechanisms`/`.addresses_challenges`/`.tests_contributions` resolves to valid M/C/CO ids ✓; `N9.results[].rq_id` ∈ {RQ1,RQ2,RQ3} = `N8` ids ✓. All N0–N12 nodes + Claims present; every non-GIVEN/non-FOUND item (N0 placeholders, N3 status, N10, N11) carries its 3-part absence comment. No gap found.

2. **Reference-cache integrity** — **FAILED on first pass, fixed.** `digest.md` N3 cites 9 `[GROUNDED:corpus]` keys (MonitorAIScale, LAMDA, BenchContamFragility, MarkovCalib, DetectGPT, LearnToDistance, MinKpp, ContamICL, DnR) sourced from `topics/corpus/ideas.jsonl` (the shared 11,683-paper OpenReview idea corpus) — real OpenReview submissions (independently confirmed by looking up each `paper_id` in that corpus: e.g. `bX3J7ho18S` = "Monitoring AI-Modified Content at Scale..."). **None of these 9 keys existed in `discussion/reference_candidates.jsonl`** before this run — the topic's own 150-candidate harvest (110 arXiv + 40 ACL-2023, drawn from `arxiv_miner_cache`/`openview_corpus/paper_cache`) never included them, because it was a separate, later, differently-sourced harvest that never surfaced this topic's own load-bearing N3 citations. This is exactly the failure mode goal.md §3 item 2 exists to catch ("every N3 key is a selected cache record"). **Fix applied (citing goal.md §1 lifecycle + §3 item 2):** backfilled all 9 as `selected` records in `reference_candidates.jsonl`, using the exact citation keys from `digest.md`/`paper.md`, with `relevance` set per each paper's documented role there (`method-twin` for MonitorAIScale — the estimator whose reference is directly swapped in H3; `baseline` for the three battery detectors DetectGPT/LearnToDistance/DnR; `adjacent` for LAMDA/BenchContamFragility/MarkovCalib/MinKpp/ContamICL — motivating/template evidence, not instruments). Since no PDF is cached locally for these OpenReview ids, `pdf_path=null` and `verified.id_resolves=false` (honest per the task's own rule, not silently marked resolved); a lightweight digest was reconstructed for each from the real `proposal.motivation`/`proposal.method` text already present in `topics/corpus/ideas.jsonl` (the same source `digest.md`'s N3 `approach_summary` drew on) and written to `discussion/corpus_backfill_digests/<key>.digest.md`, so `digest_path` is resolvable even though the PDF is not. **Residual, explicitly not fabricated:** a full paper-digest PDF-extraction pass for these 9 remains a pre-Phase-E to-do (would need the actual PDFs fetched) — flagged here, not silently closed. The topic's other 150 harvested candidates were separately triaged per Task 1 of this run (3 selected — 1 adjacent, 2 background archetype exemplars — and 147 rejected, each with a specific why); combined with the 9 backfilled N3 records, the cache now totals 159 records / 12 selected / 147 rejected; no candidate anywhere in the cache is left `pending`.

3. **Tag discipline** — **PASS.** Scanned all of `digest.md`: every substantive bullet carries one of `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`; no bare assertion found; no `[HYPOTHESIS]` silently reads as settled fact anywhere (N9's results are explicitly `[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]` with falsification conditions, not asserted findings).

4. **Claim–Evidence Map completeness** — **PASS.** `paper.md`'s Claim–Evidence Map traces all 4 digest Claims + the CO4 recommendation to an H-id or a supported-by-design definition; every H-id (H1, H2/H2b, H3) has a pre-committed fallback (F1/F2/F3) or is covered by the global pivot F-G1; no orphans in either direction.

5. **Hypothesis/assumption machinery** — **REVISE found, fixed (2 items).**
   - **H2b lacked an effect-size floor** (guidance.md §3.1: "Effect floor is mandatory: significance without magnitude passes nothing"). As originally written, H2b's pass criterion was "Mann-Kendall p < 0.05, monotone" with no stated minimum magnitude — a synthetic-drift injection could register as statistically significant while moving FPR by a fraction of a percentage point, which would not actually support the mechanism claim H2b exists to establish. **Fix:** added an explicit floor — "at least 1 percentage point absolute between the lowest and highest perturbation intensity" — so H2b is now binary-checkable at a stated magnitude, matching H1/H2/H3's existing floors.
   - All seven §3.1 slots otherwise present for H1/H2/H3 (applies_if via the listed Assumption line, metric, test, alpha and aggregation stated once in Step 6's "Common design" preamble and applied uniformly, effect_floor, verbatim fallback). A1–A6 each have `failure_mode`/`detection`/`consequence`; A1 and A6 carry explicit `PG-1`/`PG-2` pilot-gate ids, A2–A5 name the walking-skeleton as their checking phase (guidance.md §3.2's "else the phase that checks it" clause) rather than a numbered id — acceptable per the template, not a gap.

6. **Method-rigor audit** (guidance.md Part 6 items 1–10 + Part 2's A2 evidence standard) — **REVISE found, fixed (2 items); rest PASS.**
   - **Item 1 (R1 estimand) failed originally:** `paper.md` Step 5 opened directly into `**Notation.**` with no one-sentence estimand (quantity + unit of analysis + reference population + decision it feeds) anywhere in the file, despite goal.md §0 explicitly requiring "formal problem definition (estimand + notation + ...)". **Fix:** added one `**Estimand (R1).**` sentence at the top of Step 5, before Notation, naming the quantity (FPR as a function of temporal distance Δ), the unit (one detector×year-bucket cell), the reference population (hard-timestamped single-source human documents), and the decision it feeds (whether a given historical year is safe to draw a human reference from).
   - **Item 6 (R2 instrument validation) failed originally:** A1's purity spot-check is a human-rubric annotation task (judging "genuinely human-authored" vs. mis-dated/ghostwritten/revised) — exactly the class of instrument guidance.md's R2 sequence covers — but as written it specified only "human spot-check... report residual mislabeling rate," with no independent-rater agreement statistic or acceptance threshold. **Fix:** added the R2 five-step shape inline in A1 — categories grounded in the source's own timestamp/version-history metadata, a pilot-refine step, **two independent annotators** with a **κ ≥ 0.7** acceptance threshold, a confusion-structure check, and freeze-before-scale — with an explicit fallback to guidance.md Part 4 situation 7 (refine-and-re-validate) if κ < 0.7.
   - All other Part 6 items (2 verb check, 3 hypothesis slots — see item 5, 4 assumption slots, 5 B0/B-alt/F-G* structure, 7 confound-naming via the B-alt rival↔control mapping, 8 mechanism analysis via H2b, 9 power/INCONCLUSIVE via A6, 10 archetype-evidence match) were already present and are not touched — this topic's plan already met the A2 evidence standard (validated instrument [now genuinely R2-complete], controlled comparison, pre-registered trend tests with effect floors, rival-explanation ablations via B-alt, ≥1 mechanism analysis via H2b) before this run; only the two specific gaps above were real.

7. **Stage cross-check (advisory)** — **PASS, already done.** The existing `pengsida-stage-reviewer` pass earlier in this file (Stage 1–5 against the `auto-research-discussion` loop's own outputs, not re-duplicated here) already fired and fixed 2 REVISE items (Stage 2 nearest-neighbor sentence, Stage 4 falsification conditions); nothing further surfaced on re-reading against the now-corrected `paper.md`.

8. **Taste audit currency** — **PASS, no re-audit required.** `taste_audit.md`'s 🟢 verdict covers the Motivation (Stage 2) and Method (Stage 5) sentences and the Step 0/Step 3 asymmetry/bridge/synthesis self-check. None of today's three fixes (estimand sentence, H2b effect floor, A1's R2 protocol) touch the asymmetry statement, the motivation, or the method's dominant verbs — they are precision additions inside the already-audited formal spec and assumption ledger, not new framing. No material edit to re-audit against.

### Gate result

**Items 2, 5, 6 initially failed; all three fixed in this pass (reference cache backfilled; H2b effect floor added; A1 R2-validated). Items 1, 3, 4, 7, 8 passed on first read.**

**PHASE A GATE: PASS** (post-fix). All eight checklist items clear. Cleared to proceed to Phase B (walking skeleton) — not attempted in this run, per instruction scope.
