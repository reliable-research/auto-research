# Pengsida Stage Review — B4.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding, with Resource (dataset/instrument) as a secondary archetype.** Per `archetypes.md`'s tells: the core question is "we characterize how much achievable utility current stopping rules leave on the table," with no new stopping *method* being pitted against baselines to win — the checkpoint-probing instrument, the regret decomposition, and the learned estimator are the *analytical apparatus* that makes the phenomenon (regret) observable at all, matching digest N12's own `empirical` classification and `paper.md` Step 2's explicit tie-break ("the logged-trajectory corpus exists to support the measurement, not as the primary claimed contribution"). The secondary Resource archetype is licensed by the same Step 2 note: the released checkpoint-level trajectory corpus is a genuine, reusable artifact, so per `archetypes.md`'s hybrid-paper guidance ("run the dominant archetype's bar and add the secondary one's Stage-4 check"), Stage 3/4 below use the **Analysis/Finding** column as primary, with the **Resource** column's coverage/leakage/quality-control check added at Stage 4.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "nobody can say how much headroom is actually left to capture" is a first-principles framing (a genuine diagnosability gap, not a patch on an existing rule), and the stakes are stated concretely: a deployer cannot currently distinguish a nearly-optimal rule from one leaving most of the achievable headroom on the table, and "which rule looks best can flip with the deployer's own exchange rate." The Einstein ratio holds: the Introduction's opening paragraphs are pure problem/stakes, with zero method leak (probing, thresholds, and the learned estimator appear starting only in paragraph 5). Feasibility evidence (checklist item 6) is unusually strong for this stage: `paper.md`'s own Walking Skeleton section gives an explicit, binary, pre-stated pass criterion (four numbered conditions, ~10–25 GPU-hours, 1–2 days wall-clock) — exactly the minimum-viable exploratory design this bar asks for, carried into the Experiments section below as the pilot design.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap by scoring a stopping rule against a reconstructed oracle — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The five thematic threads in the first assembled draft were genuinely argued, not a citation dump — each ends on a problem-tied limitation (e.g., "Best-of-Infinity... characterizes only the parallel dimension of test-time compute... its reference point is the infinite-sample vote, which can itself be wrong, rather than an accuracy-per-compute oracle"). But the section never stated, in one place, which single prior work is the *closest* competitor before diving into the threads. Digest N4 and `paper.md`'s own related-work engagement already do this ranking work implicitly (DEER and TrimR are the two works whose checkpoint/transition-based architecture this paper's instrument most directly reuses and extends), but that ranking never surfaced as an explicit opening sentence in the first assembled `paper_draft.md`. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the start of Related Work naming DEER and TrimR as the closest prior work (the two training-free, checkpoint/transition-based exit rules this paper's instrument directly builds on) and stating the precise delta — neither is scored against a reconstructed oracle — rather than leaving the reader to infer the ranking from five parallel threads.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — the oracle t*(x,λ), the utility function U_λ(k), and the regret R_λ(r,x) are all given in Problem Definition ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge, and the draft states it explicitly rather than asserting the pre-decoding control by fiat: "realized trajectory behavior can diverge from [a pre-decoding difficulty estimate] in both directions... only a signal that reads the trajectory as it actually unfolds can catch that divergence" — this is exactly the sentence that makes the pre-decoding control non-redundant with a plain difficulty-prediction baseline, and its absence would leave the strongest alternative explanation (mid-trajectory signals are just re-deriving difficulty) unaddressed. No orphan components — every one of the five modules (checkpoint-probing instrument, decomposed regret attribution, learned history estimator, exchange-rate sweep, pre-decoding control) traces to a named sub-problem, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational, plus (secondary, Resource archetype) whether the released corpus's quality is characterized rather than assumed. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding primary + Resource secondary)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The primary Analysis/Finding question — is the claimed cause isolated from its strongest alternative — is well-served structurally: `rq_predecoding_control` is a genuine falsification design (recomputing stopping value with mid-trajectory signals removed, not just correlating them with outcomes), and every RQ subsection in the first assembled draft already carried both an "Expected outcome" and an explicit "Falsification condition" line, so no fix was needed there. The gap was in the **secondary Resource-archetype check**: per `archetypes.md`'s hybrid guidance, a paper whose secondary contribution is a released corpus (the checkpoint-level trajectory corpus, CO4/M5 in the digest) must have its Stage 4 bar include "coverage and quality controls... reported" and "leakage/contamination checked and ruled out," not just an internal assumptions table. The first assembled draft's Experimental Setup subsection listed datasets, baselines, and metrics, but never surfaced the verifier-grading audit (digest assumption A1: "manual audit of 50 verifier decisions per benchmark; >2% grading errors → fix grader before Stage 1") or a benchmark-contamination check as first-class, reader-visible parts of the evaluation plan — they existed only in `paper.md`'s internal assumptions table (A1), which does not survive into the assembled paper draft's prose. A released corpus whose labels were never audited, and whose source benchmarks were never checked for pretraining contamination, is exactly the failure mode `mined_review_checks.md`'s Stage-6 "Data" tier (dataset provenance, contamination and leakage) flags as a default reviewer question for anything LLM-based.

**THE ONE FIX (applied):** Add an explicit paragraph to Experimental Setup stating the verifier-grading audit (manual audit of 50 verifier decisions per benchmark, gated at >2% error) and a benchmark-contamination check (reporting any known train/pretraining overlap for the released corpus's source benchmarks) as first-class parts of the evaluation plan, not an internal caveat.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Test-time reasoning lets a language model trade additional inference compute for a chance at a better answer" / "Yet no current stopping rule is measured against what the future of its own trajectory would have told it" / "The nearest existing work approaches this gap from adjacent but distinct angles" / "Turning this gap into a measurable quantity surfaces four distinct obstacles" / "Our approach turns each obstacle into one instrument with a specific, falsifiable role" / "We evaluate this design across mechanically verifiable reasoning benchmarks") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title, abstract, and Introduction: "the utility-optimal moment to stop is a functional of the trajectory's unobserved future, while every deployable stopping signal reads only the past." The Conclusion names a real forward-looking limitation (the reference-agreement-style risk that the reconstructed oracle's own precision, not just the rules being measured, bounds what can be concluded at the hardest difficulty tier) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the opening of the Related Work section, naming DEER and TrimR as the closest prior work (the two checkpoint/transition-based, training-free exit rules this paper's instrument most directly builds on and diverges from) and stating the delta plainly, rather than leaving five parallel threads unranked.
2. **Stage 4 fix** — added a verifier-grading-audit and benchmark-contamination paragraph to Experimental Setup (both `paper_draft.md` and `paper_draft.tex`), surfacing digest assumption A1 as a first-class, reader-visible evaluation-plan item rather than an internal caveat, per this paper's secondary Resource archetype.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per `goal.md` §3's 8-item checklist (distinct from the `pengsida-stage-reviewer` Stage 1–5 review above, which checks the *auto-research-discussion* pipeline's stage outputs against `archetypes.md`'s rubric — this section checks `README.md`/`digest.md`/`paper.md` against `goal.md`'s own binary gate, applying `guidance.md` as the construction standard). Companion work: `discussion/reference_candidates.jsonl` was rewritten from the flat ad hoc harvest schema into `goal.md` §1's canonical schema in the same pass (see pipeline.md entry); several findings below depend on that rewrite.

### 1. Digest self-verification — **PASS (one fix applied)**

Re-executed the checks `digest.md` claims: all thirteen nodes N0–N12 plus a final Claims section are present; every non-`FOUND` node (N0–N2, N4–N11) carried the required 3-part `absence_comment` (`what_missing`/`why_matters`/`implication`) — **except N12**, whose `[HYPOTHESIS]`-tagged `value`/`rationale` had no `status` or `absence_comment` field at all, inconsistent with every other node. **Fixed**: added `status: PARTIAL` and a 3-part `absence_comment` to N12 (digest.md), citing guidance.md's general non-`FOUND`-item discipline. Cross-node references resolve: N4's `affects_works` cite `citation_key` strings verbatim from N3; N6's `challenge_arguments.mechanism_components` cite real M-ids; N8's `evaluates_mechanisms`/`tests_contributions` cite real M-/CO-ids; the Claims section's `location` fields point to real N-ids. No dangling references found.

### 2. Reference-cache integrity — **REVISE (fixed)**

Found two compounding problems, both now fixed as part of the Task 1 reference-cache rewrite:
- The 150-candidate `reference_candidates.jsonl` (110 arXiv + 40 OpenReview/ACL, harvested from `arxiv_corpus`/`openview_corpus`) was in the flat ad hoc harvest schema, not `goal.md` §1's canonical schema, and every entry was `pending`. **Fixed**: every one of the 150 was read (digest skimmed; title+abstract+N1/N2/N7 extracted programmatically for triage) and given a `verdict` (`selected`/`rejected`) + `relevance` + a specific one-sentence `why`, in the canonical schema. Result: 10 selected (`adjacent`/`contrast`/`background`), 140 rejected — no entry left `pending`.
- **More serious finding**: none of digest.md N3's nine corpus-grounded works (DEER, JET, CaTS, Best-of-Infinity, TrimR, Adaptive Thinking, CoT-Length, SAFER, First Impression) or the one canonical non-corpus reference (Snell et al. 2024) appeared in `reference_candidates.jsonl` at all — they were grounded from a separate proposal corpus (`topics/corpus/ideas.jsonl`, 11,683 OpenReview proposal records) that the arXiv/OpenReview-PDF harvest never touched. This is exactly the failure this checklist item exists to catch: **every N3 key must be a `selected` cache record**, and none was. **Fixed**: backfilled all 10 as `selected` records (`baseline`/`method-twin`/`adjacent`/`contrast` per guidance.md Part 5's definitions, matching how `paper.md`'s M3 rule bank and B-alt control actually use each one), sourced from digest.md N3/N4 and the `topics/corpus/ideas.jsonl` proposal records themselves. **Residual limitation (not blocked, flagged for the record)**: these 10 backfilled entries have `pdf_path`/`digest_path` = `null` (`verified.id_resolves: false`) because no local PDF cache exists for the `ideas.jsonl` proposal corpus in this environment; before Phase E, a real PDF/digest fetch for at least the two `baseline` entries (DEER, TrimR) and the two `method-twin` entries (CaTS, CoT-Length) should be attempted so citations in the final paper rest on more than a proposal-text record.
- Spot-checked 3 ids by live fetch: `arXiv:2408.03314` (Snell et al. 2024) and `arXiv:2601.00084` ("Exploration in the Limit") both resolved and matched their recorded titles/abstracts exactly; `openreview.net/forum?id=NpU7ZXafRi` (DEER) hit OpenReview's bot-verification wall on fetch, so it is corroborated only via the local `topics/corpus/ideas.jsonl` record (title + proposal text match "Dynamic Early Exit in Reasoning Models") rather than a live re-fetch — noted as a partial verification, not a failure.
- No `pending` entries remain anywhere in the cache (confirmed by scanning all 160 final records).

### 3. Tag discipline — **PASS**

No untagged assertions found in `digest.md`; every claim carries `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]`. No silent `[HYPOTHESIS]`→`[GIVEN]` promotion: `paper.md` consistently uses "predicted"/"pre-registered"/hypothesis language and never asserts N9's placeholder directions as findings.

### 4. Claim–Evidence Map completeness — **REVISE (fixed)**

Every claim traced to an H-id or a supported-by-design definition, and every H-id had a pre-committed fallback — except **H3c** (the checkpoint-discretization instrument-validity check under E3), which had a full binary criterion and fallback wording in Step 6 but no row in the Claim–Evidence Map table, an orphan under the checklist's "no orphans either way" rule. **Fixed**: added a Claim–Evidence Map row for H3c (paper.md), framed as the construct-validity precondition the other rows' oracle-relative claims depend on, with its fallback noted as demoting those rows to instrument-relative claims if H3c fails.

### 5. Hypothesis/assumption machinery — **REVISE (fixed)**

- H\*: all of H1a/H1b/H2a/H2b/H2c/H3a/H3b/H3c fill the binary-statement, metric, test, alpha, effect-floor, aggregation, and verbatim-fallback slots (guidance.md §3.1). `applies_if` is given per-experiment (E1/E2/E3 "Assumptions:" lines) rather than per individual H-id; since every H-id under one E-block shares the same assumption set unambiguously, this is treated as satisfying the slot, not a gap.
- A\*: A1–A7 filled `assumption`/`failure_mode`/`detection`/`gate` but **not** the `consequence` slot (guidance.md §3.2: "what happens to which H\* if it fails — degrade, restrict scope, or block") — the table had no column for it at all. **Fixed**: added an explicit `Consequence` column to every A1–A7 row (paper.md), naming which H\* is blocked/restricted/degraded and how.
- Power (Part 6 item 9): no named power target existed beyond the ad hoc AIME "descriptive only" carve-out; guidance.md's worked A6 instance (B6.3) explicitly wants a named test, named power ≥0.9 (here: ≥0.8, justified below), a named minimum n, and a pre-declared thin-cell-is-INCONCLUSIVE rule. **Fixed**: added **A8** (paper.md) — a power assumption with an explicit ≥0.8 power target for the Wilcoxon test against each H\*'s stated effect floor, a pre-Stage-1 power calculation from a 100-instance pilot subsample, and an explicit rule that under-powered cells are pre-declared INCONCLUSIVE rather than scored as null (generalizing the AIME carve-out instead of leaving it as the only instance of the rule).
- B0 + B-alt + F-G1: all three present with pre-committed wording (fixed-budget placebo/justification-criterion arm; prefix-only-allocator rival-explanation control with matched capacity/budget; global pivot to a regret-certification-benchmark framing). **PASS**, no fix needed.

### 6. Method-rigor audit — **REVISE (fixed)**

Guidance.md Part 6 items 1–10 checked against the plan (not intention):

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Estimand in one sentence (R1) | REVISE→fixed | No single labeled estimand sentence existed (only distributed notation in Step 5). Added one explicit `Estimand:` line to Step 5, citing R1. |
| 2 | Verb check | PASS | Already run at Step 3; independently spot-checked against `taste_audit.md` — consistent. |
| 3 | H\* seven slots | PASS | See item 5 above. |
| 4 | A\* detection + gate | PASS (after item-5 fix added `consequence`) | |
| 5 | B0+B-alt+F-G\* | PASS | |
| 6 | Instrument R2 5-step plan | PASS (adapted) | The core "instrument" (checkpoint logger + oracle reconstructor) is not a taxonomy/rubric/LLM-judge, so R2's literal 5-step human-rater-κ template does not apply verbatim; A1 (verifier-audit, >2% error gate), A2 (probe-faithfulness, ≥90% agreement gate), A3 (split-half noise floor, ≤⅓-of-regret gate) jointly serve as an archetype-appropriate substitute with acceptance thresholds, consistent with mechanical verifiers being ground truth by construction rather than needing human validation. |
| 7 | Confound naming (R3) | REVISE→fixed | No design constraint had an explicit "constraint X removes confound Y" sentence. Added a **Confound ledger** (paper.md, 5 entries: counterfactual probing, exact-pairing replay, dev/eval split, split-half oracle, capacity-matched B-alt) citing R3. |
| 8 | Mechanism analysis (R6) | PASS | M2's stop-too-early/stop-too-late decomposition + H3b (failure-mode shift with λ) is the required ≥1 mechanism-layer analysis. |
| 9 | Power per cell / thin-cell INCONCLUSIVE (R2 worked instance / Part 4 situation 5) | REVISE→fixed | See A8 above. |
| 10 | Archetype named + Part 2 evidence standard met | PASS (with the above fixes) | Archetype = `empirical` (A2) primary, `dataset/instrument` (A3) secondary, self-declared in paper.md Step 2 using guidance.md's own Part 2 taxonomy (note: this is a different, compatible naming from the pre-existing `pengsida-stage-reviewer` review above, which uses `archetypes.md`'s own "Analysis/Finding" label — not a contradiction, a different reviewer's taxonomy). A2's evidence standard (validated instrument + controlled comparison + pre-registered effect-floor tests + rival-explanation ablation + ≥1 mechanism analysis) is now met by the plan after the items-1/6/7/9 fixes above; R8 (honest scale / dropped-row rule) was also missing and is fixed below. |

Additionally found and fixed: **R8 (honest scale)** had no matched-set/dropped-row handling rule (goal.md hard gate: "Dropped rows logged and excluded from every headline n"). **Fixed**: added an explicit dropped-row rule to Step 6's Common protocol (paper.md) — an instance dropped for any rule is dropped from the whole comparison set for that (benchmark, λ) cell, with a reason code logged, headline n always post-drop, and drop rate reported per benchmark.

### 7. Stage cross-check (advisory) — **PASS (already satisfied)**

The `pengsida-stage-reviewer` review above (this same file, pre-existing) already ran this cross-check against the confirmed `pipeline.md` stage outputs and the assembled `paper_draft.md`: Stage 1 (N1↔Stage 1) PASS, Stage 2 (N3/N4↔Stage 2) REVISE→fixed (nearest-neighbor sentence), Stage 3 (N6↔Stage 3) PASS, Stage 4 (N8/E\*↔Stage 4) REVISE→fixed (verifier-audit/contamination paragraph), Stage 5 (Writing) PASS. No new STOP-level finding from re-running it against the Task-1/Task-2 edits made in this pass, since those edits only add rigor scaffolding (consequence fields, confound ledger, estimand line, dropped-row rule, power assumption, one Claim–Evidence Map row, N12 absence_comment, cache backfill) and do not alter the archetype, the asymmetry statement, the RQ set, or the assembled prose's claims.

### 8. Taste audit currency — **PASS**

`taste_audit.md` is current: it was run *after* Stage 5's final method summary and independently re-checked the assembled `paper_draft.md`'s Methodology prose against its own self-flagged risk (the "combine" verb on M6), confirming the risk did not resurface. None of this Phase-A pass's fixes touch the asymmetry statement (Step 0) or the formal definition (Step 5's notation) — they add missing scaffolding (consequence fields, confound ledger, an estimand sentence restating existing notation, a power assumption, a dropped-row rule, one Claim–Evidence Map row, and cache records) without changing what the paper claims or how it is framed. Per goal.md §3 item 8's own trigger condition ("if the recorded audit predates a *material edit to the asymmetry statement or formal definition*"), no re-run is required.

### Gate result: **REVISE → fixed in this pass; Phase A now PASSES**

Six of eight items required a fix (items 1, 2, 4, 5, 6, and the R8 sub-finding folded into item 6); none required a STOP. All fixes were applied directly to `paper.md`/`digest.md`/`reference_candidates.jsonl` in this pass, each citing the specific guidance.md section it satisfies. No Phase B/C work was attempted — no real experiment compute exists in this environment; this run stops at the Phase A gate per the task's scope. One residual item is flagged (not blocking): the 10 backfilled N3-derived cache records lack a locally cached PDF/digest and should be fetched for real before Phase E's `refs.bib` generation.
