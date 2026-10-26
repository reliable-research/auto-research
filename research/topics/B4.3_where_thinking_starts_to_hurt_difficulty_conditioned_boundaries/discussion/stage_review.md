# Pengsida Stage Review — B4.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/where a phenomenon occurs" with no new pipeline proposed as a fix — the measurement harness (triangulated proxy, paired change-point test, cross-arm agreement criterion, decoupled cheap-signal predictor) is the *analytical apparatus* that makes the phenomenon observable and reportable, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "if budget-allocation systems keep scaling thinking length under the assumption that returns merely flatten, but the true failure mode is that returns can turn *negative*... naive always-think-longer... policies actively destroy correctness" is a first-principles framing (a root asymmetry, not a patch), and the stakes are stated concretely against a named class of deployed systems (serving policies that must set a thinking-token budget today), not a generic AI-importance appeal. The Einstein ratio holds: the Introduction's first two paragraphs are pure problem/stakes, with zero method leak — the word "triangulate" and its siblings don't appear until paragraph 5.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The four thematic paragraphs are genuinely threaded (each ends on a problem-tied limitation, not a generic one — e.g. "neither validates how much of the achievable oracle accuracy-cost tradeoff a coarse decision actually recovers relative to a continuously localized boundary"), which clears the "citation dump" failure mode. But the section, as first drafted, opened straight into the four thematic paragraphs without ever stating in one place which single prior work (or pair of works) is the *closest* competitor. `pipeline.md`'s own Stage 3 discussion had already identified the two nearest neighbors — the inverted-U theory paper and the canonical overthinking-documentation paper — but that ranking hadn't yet been pulled to the front of the Related Work section itself. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor paragraph, naming the inverted-U theory work and the canonical overthinking-documentation work as the two closest prior works and stating the precise two-sided delta (theory validated only on synthetic difficulty; empirical observation with no localized boundary), rather than leaving four parallel threads for the reader to rank unassisted. This is now the opening paragraph of the Related Work section in `paper_draft.md`/`.tex`.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the difficulty proxy, the tipping point, the cross-arm agreement criterion, and the oracle-gap recovery quantity are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: "no single manipulation realizes the exact counterfactual... what is achievable... is evidence that a finding survives across manipulations that differ in exactly how they impose length" is exactly the step that makes the cross-arm agreement requirement a stated *mitigation*, not a silently oversold *elimination*, of the intervention-vs-emergence confound — the draft says this explicitly rather than asserting confound-freedom by fiat. No orphan components — every one of the four modules (difficulty triangulation, paired change-point test, triangulated intervention design, decoupled cheap-signal predictor) traces to a named sub-problem from `pipeline.md`, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ6 is a genuine falsification design (recomputing whether a detected flip replicates under a second, independently-manipulated arm, not just correlating with it), and RQ4/RQ5's decoupling controls (length-only null, coarse difficulty-bin classifier) are built specifically to rule out the strongest rival explanations. But the first assembled draft's RQ subsections, as initially drafted, stopped at "**Expected outcome.**" without a separately stated **Falsification condition** line — e.g., RQ2's expected-outcome sentence described what a detected flip would look like, but never stated, in its own labeled line, what result would refute it (a monotone-non-decreasing curve everywhere, under every arm). Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim — and the underlying `digest.md`/`paper.md` material already had exactly this discipline (N9's per-result "FALSIFICATION CONDITION" fields, and `paper.md` Step 6's pre-committed fallback wording) that hadn't yet been carried into the first assembled `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all six RQ subsections, stating the specific, concrete statistical condition that would refute each expected outcome — not a vague restatement of the outcome's negation, but the same rigor already present in `digest.md` N9 and `paper.md` Step 6 (e.g. RQ2's falsification condition names the exact "no significant negative forward difference anywhere, under any arm" condition and its consequence — the paper's own headline reframing to a well-powered null). This is now present in every RQ subsection of `paper_draft.md`/`.tex`.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Test-time 'thinking' has become one of the few knobs..." / "Yet a central assumption behind budget-allocation decisions... remains unmeasured" / "The nearest existing work approaches this question from two adjacent but incomplete angles..." / "Turning this gap into something measurable surfaces its own difficulties" / "Our approach turns each of these obstacles into an explicit design commitment rather than a hedge" / "We evaluate this design on natural math and science benchmarks...") reconstructs the whole five-move arc (problem → gap → nearest work's shared shortfall → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across title, abstract, and Introduction: "the same generative process that produced a correct answer can overwrite it, so the marginal return can turn negative rather than flatten, and this failure mode is difficulty-conditioned rather than uniform." The Conclusion names two real forward-looking limitations (the unidentified causal counterfactual; out-of-scope cross-model-family transfer) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor paragraph to the opening of the Related Work section, naming the inverted-U theory paper and the canonical overthinking-documentation paper as the two closest prior works and stating the precise delta (rather than leaving four parallel thematic threads unranked).
2. **Stage 4 fix** — added a **Falsification condition** line to each of the six RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — goal.md §3 checklist, 2026-07-04

> This is the first execution of goal.md's canonical 8-item Phase A gate against `README.md` + `digest.md` + `paper.md` + `reference_candidates.jsonl` (the review above this heading is the `pengsida-stage-reviewer` advisory pass over the already-assembled `paper_draft.*`, which is a different, later-stage check — see the process caveat at the end of this section). Triggered by the Task-1 upgrade of `reference_candidates.jsonl` from its flat ad hoc harvest schema to goal.md §1's canonical schema (150 harvested candidates triaged: 7 selected / 143 rejected, plus 12 cache-integrity backfills — see jsonl for detail). Standard applied throughout: guidance.md.

### 1. Digest self-verification — **PASS, with one fix applied**

- Cross-node references (N4→N3 keys, N6 Challenge Arguments→C1–C4/M1–M5, N7 CO1–3→M/C/RQ ids, N8 RQ1/RQ_INF_1/RQ_INF_2→M/C/CO ids, N9 Results→RQ ids, Claims→N2/N4/N5/N8/N9) all resolve internally. All nodes N0–N12 + Claims present.
- **Gap found:** goal.md §3 item 1 requires "every non-GIVEN item carries its 3-part absence comment" — only N0, N10, N11 had the full `what_missing`/`why_matters`/`implication` triplet; N1, N2, N5, N6, N7, N8, N12 (all HYPOTHESIS-tagged) had only `Status`/`Source`/`Locator` lines or nothing.
- **Fix applied:** added the 3-part absence comment to N1, N2, N5, N6, N7, N8, N12 in `digest.md` (citing goal.md §3 item 1).

### 2. Reference-cache integrity — **REVISE → partially fixed, one residual gap logged**

- **Gap found (blocking-grade before the fix):** digest.md N3 cites 10 works by key (`WhenMoreIsLess`, `DEER`, `DiffAdapt`, `AdaptiveThinking`, `CaTS`, `JET`, `FirstImpression`, `ThinkingSpeed`, Muennighoff 2025 `s1`, Chen et al. 2024) and `paper.md` Step 2/digest N12 name 2 archetype structural exemplars (`Are Emergent Abilities... a Mirage?`, `LLMs Get Lost In Multi-Turn Conversation`) — **none of these 12 existed in `reference_candidates.jsonl` at all** before this run; the file held only the 150 unrelated harvested candidates. This is exactly the failure mode goal.md §3 item 2 exists to catch ("no `pending`/uncached entry cited anywhere").
- **Fix applied:** backfilled all 12 as `selected` cache records (relevance tags matching their role already implied by `paper.md`: baselines for DEER/DiffAdapt/AdaptiveThinking/s1/Chen-2024; method-twins for WhenMoreIsLess/ThinkingSpeed; adjacent for CaTS/JET/FirstImpression; background for the two archetype exemplars).
- **Residual gap (logged, not fixed — no local PDF/digest cache exists for any of the 12):** `pdf_path`/`digest_path` are `null` for all 12 backfills (`verified.id_resolves: false` per the file's own rule). This means the "load-bearing entries have resolvable digest_path" sub-clause of item 2 **still fails** for 6 load-bearing entries (the 3 baselines DEER/DiffAdapt/AdaptiveThinking + method-twins WhenMoreIsLess/ThinkingSpeed + the 2 canonical baselines). **Action before Phase E:** run a real harvest-and-digest pass (fetch OpenReview PDFs for the 8 corpus ids + arXiv PDFs for 2501.19393/2412.21187/2304.15004/2505.06120, then `paper-digest` extraction mode) — this is the single most important open item from this Phase A run.
- **Spot-check (3 ids fetched):** `arXiv:2501.19393` confirmed live (title "s1: Simple test-time scaling", introduces budget forcing — matches digest N3's description exactly). `arXiv:2412.21187` confirmed live (title "Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs" — matches). `OpenReview:ESELaMThLN` blocked by an OpenReview bot-check page on direct fetch; corroborated instead via the local `topics/corpus/ideas.jsonl` lookup used to build the backfill (paper_id/paper_title/paper_url present and consistent) — treated as verified-by-local-corpus rather than verified-by-live-fetch.
- **No `pending` entries cited anywhere** — confirmed; every record in the rewritten jsonl is `selected` or `rejected`.

### 3. Tag discipline — **PASS**

- No untagged assertion found in digest.md; every N-node item carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]` consistently.
- No silent HYPOTHESIS→GIVEN promotion in `paper.md`: predicted-direction language ("Predicted direction:", pre-committed fallback wording, explicit `needs-experiment` status in the Claim–Evidence Map) is maintained throughout; no hypothesis is asserted as settled fact.

### 4. Claim–Evidence Map completeness — **REVISE → fixed**

- Original 5 rows all traced to an H-id or `supported-by-design`; no fallback-less H-id. But the Abstract v0 / Step 0 asymmetry sentence's causal claim ("the same process that produced a correct answer can overwrite it") had **no traced row** — an orphan claim, since no pre-registered experiment tested the *mechanism*, only the *existence/location* of the flip (H1a/H2) and the *predictability* of it (H1b/H3).
- **Fix applied:** added mechanism-analysis experiment M6 (see item 6 below) and a new Claim–Evidence Map row tracing the causal-mechanism claim to M6, with its own falsification condition and downgrade-to-descriptive-only wording (citing goal.md §8's `stale_claim_after_verdict` gate for future enforcement).

### 5. Hypothesis/assumption machinery — **REVISE → fixed**

- H1a/H1b/H2/H3: all seven guidance.md §3.1 slots present in substance (quantified binary statement, `applies_if`, metric, test, alpha, effect floor, aggregation rule, verbatim fallback) — written in prose per-experiment rather than the literal `H<k>: applies_if: ...` key-value template, but no slot's *content* is missing. Treated as PASS (substance, not format, is what the checklist gates).
- **Gap found:** guidance.md §3.2 requires every A\* to carry a `consequence` slot ("what happens to which H\* if it fails — degrade, restrict scope, or block"). A3 and A6 had this implicitly; **A1, A2, A4, A5 did not** — they stopped at `Detection:` with no stated downstream action.
- **Fix applied:** added an explicit `*Consequence:*` clause to all six assumptions (A1 block, A2 degrade-to-native-tags, A3 block-and-pivot-to-F-G1, A4 restrict-scope, A5 degrade-with-re-audit, A6 restrict-scope-to-powered-cells) in `paper.md`, citing guidance.md §3.2.
- B0 + B-alt + F-G1 all present per §3.3 — **PASS**, unchanged.

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 A2 evidence standard) — **REVISE → fixed**

- Item 1 (estimand in one sentence, R1): **missing** — no single "Estimand:" sentence existed anywhere in `paper.md`. **Fixed:** added at the top of Step 5.
- Item 2 (verb check / Prime Directive): PASS, unchanged (Step 3 table, all PASS).
- Items 3–5, 7, 9: PASS (see items 5 above for 3/4; R3 confound-naming present in B-alt and M1's cross-check design; R7 power/INCONCLUSIVE discipline present via A6/t4).
- Item 8 (≥1 mechanism analysis, R6) and item 10 (A2 archetype evidence standard requires R2+R3+R4+R5+**R6**, all met "by the plan" not "by intention"): **missing** — Step 6 had localization (H1a/H2) and prediction (H1b/H3) but no analysis of *why* the flip occurs. **Fixed:** added M6 (trace-content mechanism probe: self-correction / verification-step density before vs. after L\*_s, with its own pre-registered prediction and falsification condition) as a new subsection of Step 6, budgeted alongside E1, and linked it into the Claim–Evidence Map (item 4 above).
- **Method-twin gap (found via Task 1's freshness-sweep-style harvest, guidance.md Part 4 situation 6):** the fresh 150-candidate harvest surfaced `2512.24574` (CREST — attention-head steering that cuts token usage / raises accuracy, explicitly framed around overthinking/underthinking) as a method-twin not previously in the cache, and reinforced `ThinkingSpeedESEL` (backfilled in item 2) as a second, closely related steering-based method-twin. Per situation 6 this required a `paper.md` repositioning, not a silent citation. **Fixed:** added Step 4 — Method-Twins (concede-and-differentiate), naming what CREST/ThinkingSpeed concede (test-time reasoning trajectories are steerable) and what remains B4.3's own contribution (measuring the boundary in an *unmodified* model before any steering, plus the cheap pre-hoc predictor and oracle-gap quantification, neither of which either method-twin provides).

### 7. Stage cross-check (advisory) — **PASS (previously completed)**

- The `pengsida-stage-reviewer` pass recorded above this heading already performed this check (against the assembled `paper_draft.md`/`pipeline.md` Stage 1–4 outputs rather than `paper.md`/`digest.md` directly) and logged/fixed 2 REVISE findings (Stage 2 nearest-neighbor paragraph, Stage 4 per-RQ falsification lines). No new STOP or REVISE surfaces when re-checked against the now-updated `paper.md` (the Step 4 Method-Twins section added in this run is consistent with, and extends, the existing Stage 2 fix's nearest-neighbor framing — both should be merged into one paragraph at the next Phase E pass, as noted in Step 4 itself).
- **Process caveat (not a paper.md/digest.md content gap, logged for the record):** `paper_draft.md`/`.tex`/`.pdf` already exist in `discussion/`, produced via `auto-research-discussion` → `taste_audit.md` → `stage_review.md` → draft assembly, **without** `B_pilot/`, `results/*.json`, `verdicts.json`, or `claim_map.md` ever having been created — i.e. Phases B/C/D were skipped rather than gated through, and Phase E prose was written directly from the pre-registered spec's predicted-direction language rather than from verdict-selected, results-spliced wording (goal.md §6's "splice, don't re-decide" rule). This is an out-of-order construction relative to goal.md's canonical pipeline (§2), not a defect in `paper.md`/`digest.md` themselves, and is out of scope for this Phase A run to remediate (no real experiment compute exists in this environment; Task instructions stop at the Phase A gate). Flagged here so a future run does not mistake the existing `paper_draft.*` for verdict-backed prose.

### 8. Taste audit currency — **PASS**

- `taste_audit.md` audits the Motivation (pipeline.md Stage 2) and Method (Stage 5) summary sentences. This Phase A run's edits (Step 4 Method-Twins, Step 5 Estimand, Assumptions consequences, Step 6 M6) add machinery and close gaps but do **not** materially change the audited asymmetry statement (Step 0, unedited) or the formal definition table (Step 5's Notation/adjective-definition table, unedited — the Estimand line only restates existing content as a single sentence). No re-audit triggered per goal.md §3 item 8. Advisory note: fold the Step 4 method-twin concession and the M6 mechanism probe into `taste_audit.md`'s Method summary at the next scheduled re-audit (Phase H at the latest), since a materially fuller method description could shift the `bottleneck_specificity` diagnostic.

### Overall Phase A gate: **REVISE (fixes applied this run; one residual action item logged)**

All static-document gaps found (items 1, 4, 5, 6) were fixed directly in `digest.md`/`paper.md` in this run. Item 2's cache-integrity gap was fixed for cache *existence* (12 backfills, all now `selected`) but not for cache *resolvability* (no local PDF/digest exists yet for those 12 — a real harvest-and-digest action, not a document-editing one, and therefore explicitly **not** attempted here). Per goal.md, Phase B may proceed once that one residual harvest is done; this environment has no experiment compute, so Phase B/C are out of scope for this run regardless (per Task instructions).
