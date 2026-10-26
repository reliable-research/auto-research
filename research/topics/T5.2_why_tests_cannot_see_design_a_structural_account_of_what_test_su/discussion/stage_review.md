# Pengsida Stage Review — T5.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "which categories of design property does an existing suite fail to detect" with no new pipeline proposed as a fix — the dual-oracle admission procedure, the matched-neutral control, and the extended kill criterion are the *analytical apparatus* that makes the phenomenon measurable, not a method being pitted against baselines to win. This matches digest N12's `value: "empirical"` and `paper.md` Step 2's own classification ("Primary: empirical... Secondary: technical artifact"), and Stage 1's `study_type: empirical` in `pipeline.md`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. Quoting the draft's second Introduction paragraph: "A test verdict... is therefore near-constant across an entire class of programs that behave identically. Design conventions... are free to vary *within* that same behavior-equivalence class." This is a first-principles framing (a structural asymmetry, not a patch on an existing tool), and the stakes are concrete, not a generic AI-importance appeal: a change can be "exactly the kind of change a codebase's design intent forbids" while being invisible to the one gate teams actually rely on. The Einstein ratio holds — the Introduction's first four paragraphs are pure problem/gap/difficulty, with the method not introduced until paragraph five ("Our approach turns each of these obstacles into a specific design decision").

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The nine cited works are threaded, not dumped — each of the two paragraphs ends on a problem-tied limitation rather than a generic one (e.g., the binary-matrix work's "every row is a functionally wrong program by construction, making a functionally-equivalent-yet-convention-violating variant an all-pass row invisible to a rank analysis"), which clears the citation-dump failure mode. But the first assembled draft's two paragraphs — an LLM-code-testing cluster and a classical-SE-adequacy/conformance cluster — sat side by side with no argued connection between them, reading as two separate literatures rather than one positioned landscape. This is exactly the "coverage" failure the Stage 2 bar warns about: *"does the comparison across works make the problem setting more legible, rather than reading as a disconnected list?"* The risk here is not a buried nearest-neighbor (both nearest neighbors — the binary-matrix work and the classical mutation-score literature — were already named up front), it is a buried *relationship between the two clusters*, which is the surface-level Bridge-flavored drift the taste audit's Section 6 flagged as the one place this idea could still slip into generic "two literatures, unconnected" phrasing during assembly, even though the underlying idea itself passed the taste audit cleanly.

**THE ONE FIX (applied):** Add one explicit sentence stating *why* the two clusters belong in the same section — not as a transition device, but as a substantive claim about what each supplies to this paper (applied stakes vs. theoretical vocabulary) — rather than leaving the reader to infer the connection.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely before it is used — $\mathrm{EQ}_B(m)$, $V(m)$, $D_c$, and $N_c$ are all given in Problem Definition ahead of any claim that invokes them, and each of the seven Methodology subsections opens with the specific difficulty it resolves before its mechanism (e.g., "Extended Temporal Kill Criterion" states the classical kill criterion's blindness first, then the trace-order extension). The one load-bearing inferential hinge is stated explicitly rather than asserted by fiat: "If the suite's kill probability carries no information about whether a matched mutant actually violates the convention, that is precisely what a convention-blind suite would produce" — this is exactly what makes the Design-Specificity Control non-redundant with a raw DMSR-vs-FSR comparison. No orphan components: all seven modules (dual-oracle admission, non-local operator catalog, extended temporal kill, codifiable-convention scoping, design-specificity control, augmentation arm, multi-system/cross-category design) trace to one of the seven sub-problems confirmed in `pipeline.md` Stage 4, including the two added in Stage 4's round 2 (design-specificity, structural-vs-quantity) — neither reads as leftover machinery; each is invoked by name in a falsification condition in Experiments.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ6 is a genuine falsification design (the matched-neutral-control comparison directly targets "is this just the generic equivalent-mutant effect"), and RQ7's augmentation arm is a genuine falsification design for "is this just under-investment in functional tests, not a structural limit." But the first assembled draft's RQ6 subsection stopped at stating the 0.05 threshold without warning the reader which direction of result actually supports the paper's claim — and RQ6 is the one RQ in this paper where the intuitive direction ("bigger gap = stronger finding") is *backwards*: a small kill-probability gap between the design-mutant set and its matched neutral control is the outcome consistent with genuine convention-blindness, while a large gap would instead show the suite partially senses conventions. Per the Analysis/Finding bar: falsification tests must be stated as an explicit, checkable condition, not left for the reader to work out the polarity of on their own — and a reviewer encountering RQ6 cold, expecting the paper's usual "bigger effect, stronger claim" pattern from RQ3/RQ4/RQ8, would very likely misread a "small gap" result as a null/negative finding rather than the load-bearing positive evidence it actually is.

**THE ONE FIX (applied):** Add an explicit sentence to RQ6's Falsification condition stating the reversed polarity directly — "a small gap here is the outcome that supports a genuine, convention-specific blind-spot claim... Readers should not expect 'bigger gap, stronger finding' here — the polarity is reversed relative to most difference-based tests in this paper" — so the direction of a successful result is stated, not implied.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Coding agents increasingly propose... changes to production codebases, and the practical question... is answered... by one signal" / "A test verdict, however, is in practice almost entirely a function of a program's observable input/output behavior" / "The closest existing work approaches this gap from the LLM-code-testing side and from classical software-engineering foundations" / "Turning this gap into a measurable claim surfaces its own obstacles" / "Our approach turns each of these obstacles into a specific design decision" / "We evaluate this design across mature open-source Java and Python subject systems") reconstructs the whole five-move arc (problem → asymmetry/gap → nearest prior work and its shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in the Abstract and reprised in the Conclusion: a passing test suite "is, in practice, almost entirely a verdict about input/output behavior," while "design conventions... can vary freely within a single behavior-equivalence class." The Conclusion names two real, forward-looking limitations (the codifiable-conventions scoping boundary, and the equivalence oracle's own bounded-budget nature) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added one explicit sentence connecting the two Related-Work clusters (the LLM-code-testing line supplies the applied stakes; the classical SE-adequacy/conformance line supplies the theoretical vocabulary this paper extends), so the section reads as one positioned landscape rather than two literatures placed side by side.
2. **Stage 4 fix** — added an explicit reversed-polarity statement to RQ6's Falsification condition in both `paper_draft.md` and `paper_draft.tex`, then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Re-run 2026-07-04, triggered by the reference-cache upgrade (Task 1 of this pass): `discussion/reference_candidates.jsonl` was rewritten from a flat 150-candidate harvest (ad hoc `topic_id/rank/score` schema, all `verdict` implicitly `pending`) into goal.md §1's canonical schema, with every candidate given a `selected`/`rejected` verdict and a specific `why`. That upgrade is a materially new input to Phase A checklist item 2, so the full §3 checklist is re-run here against the current `README.md`/`digest.md`/`paper.md`, per goal.md §2's resumability rule (input-file hash changed for the cache) and guidance.md throughout as the construction standard.

**Harvest outcome (Task 1):** 150 candidates classified — 7 `selected` (1 `method-twin`, 1 `background`, 5 `adjacent`), 143 `rejected`, each with a paper-specific one-sentence `why` (no generic "off-topic" boilerplate). None of the 40 OpenReview (ACL 2023) candidates and only ~7/110 arXiv candidates were load-bearing; this matches guidance.md Part 5's expectation that a broad harvest legitimately rejects most hits — the harvest was not thin (cache still ≥5 selected), so no re-harvest was triggered.

### 1. Digest self-verification — **REVISE, fixed**

Re-executed digest.md's own claimed checks: N0–N12 + Claims all present ✓; cross-node references (L1–L9 → N3 keys; challenge_arguments → C*/M*; RQ* → M*/C*/CO*) all resolve ✓. But six nodes (N4, N5, N6, N7, N8, N12) — all-`[HYPOTHESIS]`, non-`[GIVEN]` — lacked the 3-part `absence_comment` (`what_missing`/`why_matters`/`implication`) that N0, N1, N2, N9, N10, N11 all carry, violating goal.md §3 item 1's "every non-GIVEN item carries its 3-part absence comment." **Fixed**: added a `Status`/`absence_comment` block to each of N4–N8 and N12 in `digest.md`, matching the shape already used elsewhere in the file.

### 2. Reference-cache integrity — **REVISE, partially fixed; one residual blocking item**

**Finding (major):** none of digest.md N3's 9 citation keys (`BinaryMatrixTests`, `UTRL`, `DefectFocusedReview`, `VERINA`, `AutoCodeBench`, `SelfRefMAS`, `JiaHarman 2011`, `SchulerZeller 2011`, `MurphyReflexion 2001`) existed anywhere in `reference_candidates.jsonl` (verified by direct grep of all 9 OpenReview IDs/names against the 150-line harvest — zero hits). N3 was built from a disjoint source (`topics/corpus/ideas.jsonl`, an 11,683-paper OpenReview "ideas" corpus with a `proposal`/`related_works` schema, no `pdf_path`/`digest_path` fields) that bypasses goal.md §1's harvest→digest→select lifecycle entirely. This is a direct violation of goal.md §3 item 2 ("every N3 key is a `selected` cache record") and the goal.md §8 hard gate ("Citations only via `selected` cache keys").

**Fixed (partial):** appended all 9 works to `reference_candidates.jsonl` as `verdict: selected`, with `relevance` assigned per digest.md's own characterization (`JiaHarman2011`→baseline, `BinaryMatrixTests`/`UTRL`→method-twin, `AutoCodeBench`/`MurphyReflexion2001`→contrast, the remaining 4→adjacent) and a `why` quoting digest.md's own L1–L9 limitation text, using the real OpenReview `paper_id`/`paper_url` from `ideas.jsonl` for the 6 corpus works and standard bibliographic identifiers for the 3 canonical works.

**Residual blocking item (not fixed — no compute/network available this pass):** all 9 appended entries have `pdf_path: null`, `digest_path: null`, `verified.id_resolves: false` — no PDF was ever cached and no extraction-mode `paper-digest` run was ever performed for them (goal.md §1 step ②). A WebFetch spot-check attempt on one OpenReview ID (`RomWar2kVN`, per the checklist's "spot-check 2–3 ids by fetching") hit a bot-verification wall and returned no paper content, so even minimal online verification was not possible in this environment. **This keeps checklist item 2 short of "all-clear"**: the load-bearing `baseline`/`method-twin` entries (`JiaHarman2011`, `BinaryMatrixTests`, `UTRL`) do not have a resolvable `digest_path`, which goal.md §3 item 2 requires. Recorded as the blocking pre-Phase-B action item in `pipeline.md`.

### 3. Tag discipline — **PASS**

Every assertion in digest.md carries one of `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[NON-CORPUS:canonical]`/`[PLACEHOLDER]`; no silent `[HYPOTHESIS]`→`[GIVEN]` promotion found (N9's Results stay `[PLACEHOLDER]`, N1's `objective`/`inputs`/`outputs` stay `PARTIAL`, etc.). One related but distinct finding folded into item 6 below: N12's rationale cited an exemplar ("Property-Based-Testing-in-Practice") **from memory**, not tagged and not in the cache — this is a citation-discipline defect, not a tag-discipline one; fixed under item 6.

### 4. Claim–Evidence Map completeness — **PASS**

`paper.md`'s 7-row Claim–Evidence Map: every claim traces to an H-id (H1/H2/H3) or is marked `supported-by-design`; every H-id (H1, H2, H3) has a fallback (FB1, FB2, FB3) and the global pivot F-G1 covers the central-family-fails case; no orphan claims and no orphan H-ids found.

### 5. Hypothesis/assumption machinery — **REVISE, fixed**

H1/H2/H3 each fill guidance.md §3.1's seven slots (statement, `applies_if`, metric, test, α, effect floor, aggregation, verbatim fallback) — PASS, no fix needed. A1/A2/A4/A5/A6 each fill §3.2's slots including a stated gate/consequence — PASS. **A3 was the one exception**: it stated the assumption (`EQ_B` mislabels <5%), the failure mode, and a detection method (manual audit of 100 surviving mutants), but named **no gate or consequence** if the audit fails — every sibling assumption (A1, A2, A4, A6) states what happens on failure, A3 didn't. **Fixed**: added an explicit gate to A3 in `paper.md` — mislabel rate ≥5% triggers re-filtering to structurally-guaranteed operator subfamilies and, if still ≥5% after restriction, demotion to exploratory (mirroring A4's treatment), citing guidance.md §3.2.

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 A2 evidence standard) — **REVISE, fixed**

- Item 1 (estimand, R1): **missing** — `paper.md` Step 5 opened directly with Notation, no prior one-sentence estimand (quantity/unit-of-analysis/reference-population/decision). **Fixed**: added an explicit "Estimand (guidance.md §3.4 R1)" sentence at the top of Step 5.
- Item 4 (every A* has detection **and gate**): A3 gap, see item 5 above — fixed there.
- Item 6 (every instrument has the 5-step R2 plan with an acceptance threshold): **REVISE** — A4's violation-oracle (M3 checker) validation was a bare precision number (≥0.90 against a single audit), missing R2's ①ground-in-external-source, ②held-out-calibration-refinement, ③**≥2 independent raters with κ≥0.7**, ④confusion-structure inspection, and ⑤freeze-before-scale steps. Guidance.md is explicit: "asserted validation numbers without the protocol are treated as absent." **Fixed**: hardened A4 in `paper.md` to the full 5-step R2 sequence, adding the missing κ≥0.7 two-rater requirement and the confusion-structure check, and widened the gate to precision<0.90 **or** κ<0.7 **or** systematic (non-adjacent) confusion.
- Item 7 (every design constraint names its confound, R3): **REVISE, fixed** — the confound-removal logic was present in the design (independent `X_diff` generator, matched neutral set `N_c`, capability-matched augmentation gate) but never stated as explicit "constraint X removes confound Y" one-liners. **Fixed**: added three R3 one-liners to `paper.md` Step 5, immediately after the adjective→definition→measurement table.
- Item 9 (power stated per cell; thin cells pre-declared INCONCLUSIVE): **REVISE, fixed** — the ≥150-mutants/category/system threshold (A2) existed but was never justified by a stated power calculation, and no explicit rule pre-declared under-yield cells INCONCLUSIVE (as opposed to silently dropped or scored as null), contrary to guidance.md §3.2's worked A6 example and Part 4 situation 5. **Fixed**: added a power statement (≥0.90 power at α=0.05 to detect the pre-registered 0.25 effect floor at n=150) and an explicit thin-cell INCONCLUSIVE rule to Step 6's Design constants in `paper.md`.
- Items 2, 3, 5, 8, 10: PASS as previously found (Stage 3/taste-audit already enforce the verb check; B0/B-alt/F-G1 present; ≥1 mechanism analysis via IKF_c/design-specificity control; archetype named and A2 evidence standard now met after the above fixes).
- **Citation-from-memory defect** (surfaced while checking Part 5's "never cite from memory" rule against N12): digest.md's archetype-classification rationale (N12) cited "Property-Based-Testing-in-Practice" as a structural exemplar with no cache record and no verifiable identity — exactly the anti-pattern guidance.md Part 2/5 warns against. **Fixed**: replaced it with a cache-verified exemplar this pass's Task 1 harvest actually surfaced and selected — `[OnBlindSpotsNLGMetrics, acl_he-etal-2023-blind]` (`relevance: background`, `verdict: selected`), whose stress-test-for-blind-spots evidence shape is the real structural analogue guidance.md Part 2 asks for.

### 7. Stage cross-check (advisory) — **PASS (no re-run needed)**

The existing `pengsida-stage-reviewer` pass (top of this file) already covers N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E*↔Stage 4 against the confirmed `pipeline.md` outputs, and its two REVISE findings are already applied. None of this pass's edits change N1/N3-content/N6/N8/archetype in a way that invalidates that cross-check (the N3 *cache-integrity* fix adds provenance to already-cited keys without changing which works are cited or what they're claimed to show); no re-run needed.

### 8. Taste-audit currency — **PASS (no re-run needed)**

`taste_audit.md` audited the asymmetry statement (Step 0) and formal definitions (Step 5) as they stood before this pass. This pass's edits (estimand sentence, A3 gate, A4 R2 hardening, R3 one-liners, power/INCONCLUSIVE rule, N4–N8/N12 absence comments, the N12 exemplar-citation swap) add missing rigor scaffolding and fix a citation-provenance defect; none alter the asymmetry sentence's content, the formal definitions in the adjective→definition→measurement table, or the load-bearing verbs Step 3 already audited. No material edit to the asymmetry/formal-definition content occurred, so no re-audit is triggered per goal.md §3 item 8.

### Overall Phase A gate: **REVISE** (not clean PASS)

Six of eight checklist items pass cleanly or pass after the fixes applied directly in `digest.md`/`paper.md` this pass (items 1, 3, 4, 5, 6, 7, 8 — noting 3/6 include the memory-citation fix). **Item 2 (reference-cache integrity) remains short of all-clear**: the cache now correctly lists all 9 of digest.md's N3 works as `selected` with accurate relevance/why, closing the "every N3 key is a selected cache record" half of the check — but the "load-bearing entries have resolvable `digest_path`" half is still false for `JiaHarman2011`, `BinaryMatrixTests`, and `UTRL` (no PDF ever cached, no extraction-mode digest ever run, network spot-check blocked in this environment). Per goal.md §8's hard gate ("Citations only via `selected` cache keys ... no instrument runs at scale without passing R2 validation" and this checklist's own "load-bearing entries have resolvable digest_path"), **this blocks Phase B** until a real harvest+digest pass (goal.md §1 steps ①–②, using the OpenReview `paper_url`s now recorded in the cache) caches actual PDFs/digests for these 3 load-bearing works, or two independent human-checked bibliographic substitutes are accepted in their place. This is a bounded, well-specified action item, not a re-litigation of the whole cache — everything else in Phase A is clear.
