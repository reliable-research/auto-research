# Pengsida Stage Review — B1.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we measure whether and how often a phenomenon occurs" with no new pipeline proposed as a *fix* to the phenomenon — the dual-channel measurement apparatus (separability certification, out-of-sandbox oracle, verifier sweep, pressure harness, matched-arm attribution) is the *analytical instrument* that makes log-forging observable and attributable, not a method being pitted against baselines to win. This matches digest N12's own explicit classification, `value: empirical`, with the rationale that "the dual-channel suite ... is built as the *instrument* for this measurement ... rather than as a leaderboard-oriented reusable benchmark product," and Stage 1's `study_type: empirical`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. The Introduction states the root cause plainly — "the log and the environment state do not share an author. The log is authored by the agent being rewarded; the state is authored by the world" — which is a first-principles asymmetry, not a "combine A's x with B's y" patch, and the stakes are concrete rather than a generic AI-importance appeal: a log-only reward is already the default substitute in RLVR pipelines specifically *because* execution-based grading is too slow to run at training scale, so the paper is asking whether the substitution that is already load-bearing in practice is safe. The Einstein ratio holds: paragraphs 1–2 of the Introduction are pure problem/stakes, with no method leak (the first named technique — the admission probe — does not appear until paragraph 5).

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The four threads are genuinely argued, not a citation dump — each ends on a problem-tied limitation, e.g. the first thread's "neither validates its own scores against an independent environment-state outcome under adversarial optimization pressure," and the fourth's "both use it purely as a capability grader ... never as an instrument for measuring how often a weaker log-side verifier gets gamed." That clears the "citation dump" and "generic limitation" failure modes. But the section never states, in one place, which single prior work is the *closest* competitor. A check of the underlying `digest.md`'s N3 (search protocol) and N4 (limitations) confirms this ranking was never made explicit anywhere upstream either — unlike the B5.5 sibling run, there is no "the closest are X and Y" sentence in the digest to inherit. A reviewer reading only the four parallel threads (log-side reward models / formal reward-hacking theory / emergent deception / state-grounded benchmarks) has to infer for themselves that the first thread — SWE-RM and ToolRM, which share this paper's *exact object of study*, a log-only reward signal over agent trajectories — is the nearest neighbor, rather than, say, the state-grounded-benchmark thread, which looks superficially closer (it does use real state verification) but is actually further away in framing (it's a capability grader, never a gaming-incidence study). Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first."

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence to the first thread (log-side/execution-free reward models), naming it as the single closest prior work and stating the precise delta — same object of study, missing only the independent-state-truth check — rather than leaving the reader to rank the four threads unaided.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each formal construct is defined precisely *before* it is used — $V_{\log}$, $V_{\text{state}}$, $\rho$, and $\mathrm{FIR}$ are all given in the Problem Definition's "Formal setup" ahead of any claim that invokes them, so nothing is "named after the fact." The inferential chain is licensed at its one load-bearing hinge, stated explicitly in the Matched-Control Attribution Design's Insight: "Holding the model, tasks, decoding seeds, and harness fixed while toggling only which verifier the reward is defined on isolates the reward channel as the one thing that differs between arms — so any resulting gap in incidence can be attributed to that channel rather than to harness idiosyncrasy or ordinary unreliability." That is exactly the step that turns a raw FIR gap into an attributable causal claim rather than a correlation. No orphan components: each of the six modules (separability certification, out-of-sandbox oracle, verifier sweep, pressure harness, dual-channel measurement, matched-control attribution) carries its own Challenge/Insight/Method triplet tracing to a named difficulty, with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ3 is a genuine falsification design (sweeping three verifier instantiations to see whether a smarter verifier alone closes the gap, rather than assuming it does or doesn't), and RQ7 is a genuine attribution-guard design (checking whether the RQ6 gap survives an honest-error alternative explanation). But the first assembled draft's seven RQ subsections stopped at "**Expected outcome.** ... rather than decay [or: rises with pressure, or: the oracle correctly separates ...]" without ever stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ ... demand at least one such test," stated as a check, not implied. An "Expected outcome" alone reads as a hope; a stated falsification condition is what makes it a pre-registered, breakable claim. Crucially, the underlying `paper.md` (Steps 0–9, the pre-existing artifact this pipeline was assembled from) already had this discipline and it simply didn't survive into the first assembled `paper_draft.md`: `paper.md`'s Step 6 states explicit "Fallback" clauses for H1 ("If H1 fails, the paper's claim becomes: ... log-forging is not an automatic consequence of log-only reward at this scale — a bounded-null"), H2 ("If H2 fails ... implying cheap best-of-n selection is a sufficient audit probe"), and H3 ("If H3 fails (some log-side verifier reaches the state floor) ... we characterize which log-side design suffices and why") — none of which made it into the RQ6/RQ4/RQ3 subsections of `paper_draft.md`.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ subsections, stating the specific observation that would refute each expected outcome — reusing the pre-existing `paper.md` Fallback language verbatim where it already existed (RQ3↔H3, RQ4↔H2, RQ6↔H1), and constructing analogous concrete falsification statements for the four RQs (RQ1, RQ2, RQ5, RQ7) that never had a paper.md-level Fallback clause to inherit, each grounded in that RQ's own stated metrics rather than a vague negation.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Autonomous coding and tool-using agents are now routinely graded... by systems that never look at the world" / "The substitution rests on an assumption that is rarely stated out loud..." / "The nearest existing work approaches this asymmetry from adjacent angles without measuring it directly" / "Turning this gap into a measurable claim raises its own difficulties" / "Our approach turns each of these obstacles into a specific instrument rather than a hedge" / "We evaluate this design across repository-issue coding tasks and multi-step tool-calling tasks...") reconstructs the whole five-move arc (problem → unstated assumption/gap → nearest prior work's shared limitation → why it's hard → the instrument → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently across Abstract, Introduction, and the contributions list: "a log-only verifier certifies the agent's self-report of an action, a quantity an optimizing agent can drive to 'pass' without the action ever occurring." The Conclusion names two real forward-looking limitations (scope restricted to hermetically sandboxable environments; the admission-probe/oracle-validity checks may themselves surface edge cases) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added one explicit nearest-neighbor sentence to the Related Work section's first thread (log-side/execution-free reward models), naming it the single closest prior work (SWE-RM/ToolRM — same object of study, a log-only agent reward signal) and stating the precise delta (never checked against independent state truth under adversarial pressure), rather than leaving four parallel threads unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), reusing `paper.md`'s own pre-existing Fallback clauses for RQ3/RQ4/RQ6 and constructing grounded analogues for RQ1/RQ2/RQ5/RQ7 — then recompiled `paper_draft.pdf` (`pdflatex` twice, exit 0, zero `! ` errors in the log; `pdftotext | grep -c "�"` returns 0; final PDF is 13 pages).

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run)

> Run per goal.md §3's canonical 8-item checklist (distinct from the `pengsida-stage-reviewer` pass above, which reviewed the `auto-research-discussion` stage outputs — this section is the formal, binary Phase-A gate goal.md requires before Phase B, applied against `README.md`/`digest.md`/`paper.md` with guidance.md as the construction standard). Date: **2026-07-04**.

### 1. Digest self-verification — **PASS**

Re-executed the checks `digest.md` claims: all of N0–N12 + Claims are present; every cross-node reference resolves (N4 `affects_works` ⊆ N3 `citation_key`s, `grounding_check: true`; N8 `addresses_challenges` ⊆ N5's C1–C4; `evaluates_mechanisms` ⊆ N6's M1–M6; `tests_contributions` ⊆ N7's CO1–CO4; N9 `rq_id`s ⊆ N8's RQ1/RQ_INF_1/RQ_INF_2); every non-[GIVEN] node carries a 3-part `absence_comment` (`what_missing`/`why_matters`/`implication`) — spot-checked N1, N3, N6, N9, N10, N12, all three parts present in each.

### 2. Reference-cache integrity — **REVISE, fixed**

**Found:** Before this run, `reference_candidates.jsonl` held 150 harvested candidates in the ad hoc pre-goal.md schema, and **zero** of `digest.md` N3's 10 citation keys (`SWE-RM`, `ToolRM`, `CorrelatedProxies`, `InfTimeRH`, `FAPO`, `AmongUs`, `StratDishonesty`, `FuncBenchGen`, `SWE-Lancer`, `SWE-bench`) resolved against it — the harvest was run from a different, broader search that missed the exact papers `digest.md`'s own N3 already grounds (a keyword-search miss, not a fabrication: all 9 OpenReview-sourced keys are real and verified present in the shared `topics/corpus/ideas.jsonl`, and `SWE-bench` is a genuinely canonical, well-known ICLR/GitHub-issue benchmark). This is exactly the failure mode goal.md §3 item 2 exists to catch: N3 citing keys with no corresponding `selected` cache record.

**Fix applied (Task 1's cache rewrite, this session):** All 150 candidates were re-triaged into the canonical schema (see counts below), and the 10 N3-cited keys were backfilled into the cache as `selected` records:
- `SWE-RM` — already present in the 150-item harvest as arXiv:2512.21919 (confirmed via digest content + a live abstract fetch to be the arXiv preprint of OpenReview:H9wMe1G76j); `ids.openreview` was added to link the two records to one key. `pdf_path`/`digest_path` both resolve locally.
- `ToolRM`, `CorrelatedProxies`, `InfTimeRH`, `FAPO`, `AmongUs`, `StratDishonesty`, `FuncBenchGen`, `SWE-Lancer` (8 keys) — not in the 150-item harvest at all; backfilled from the local `topics/corpus/ideas.jsonl` proposal records (the same corpus `digest.md`'s own N3 grounds its `approach_summary` text in). New extraction-mode digest files were written to `discussion/refs_digests/<key>.md` (motivation+method text from the corpus record) so `digest_path` now resolves for all 8. No PDF is locally cached for these (no network fetch of the actual OpenReview PDF was possible in this environment), so `pdf_path: null` and `verified.id_resolves: false` — reported honestly rather than fabricated.
- `SWE-bench` (arXiv:2310.06770) — backfilled as a `selected`/`background` record (title + URL verified live via `WebFetch`), but **`pdf_path`/`digest_path` remain null** — it is not in the local `arxiv_miner_cache` (which only mirrors 2025–2026 preprints) nor in the OpenReview `ideas.jsonl` corpus (it's an ICLR/GitHub-issue paper, outside that corpus's scope). This is the one **residual, honestly-reported gap**: `digest.md`/`paper.md` cite `SWE-bench` only for its Verified-subset task material (not as an instrument or baseline any hypothesis depends on — see `pipeline.md` Stage 3's refiner note clarifying it is "not a baseline in the beat-a-number sense"), so this gap does not block any H\*/A\*, but a full digest should be built the next time network access or a cached copy is available.

Spot-checks performed (goal.md §3 item 2's "fetch 2–3 ids"): live-fetched `arxiv.org/abs/2512.21919` (SWE-RM — title/abstract match confirmed), `arxiv.org/abs/2310.06770` (SWE-bench — title confirmed), and `aclanthology.org/2023.acl-long.262` (Reward Gaming in Conditional Text Generation — title/summary confirmed). OpenReview forum URLs (`H9wMe1G76j`, `jhqqoimoWt`) returned an anti-bot verification page rather than content when fetched live; verification for those 9 keys instead rests on cross-referencing the local `ideas.jsonl` corpus record's `paper_id`/`paper_title`/`paper_url` against `digest.md`'s own N3 `approach_summary` text (which matches near-verbatim), which is the same grounding method `digest.md` itself already used and documents.

No `pending` verdicts remain anywhere in the cache (all 159 records — 150 re-triaged + 9 backfilled less the 1 already-present SWE-RM — carry a final `selected`/`rejected` verdict).

### 3. Tag discipline — **PASS**

`digest.md` is consistently tagged throughout ([GIVEN]/[HYPOTHESIS]/[GROUNDED:corpus]/[PLACEHOLDER] on every node and claim); no node's status silently upgrades between sections (e.g. N9's results stay [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY] throughout, never referenced elsewhere as if real). `paper.md` correctly carries forward digest's speculative framing — every H\*/A\* uses conditional "holds iff" / "Failure:" language, never asserting an outcome as fact.

### 4. Claim–Evidence Map completeness — **PASS**

All 5 claims in `paper.md`'s Claim–Evidence Map trace to an H-id (Claims 1, 3, 5 → H1/H2, H3, H1∧H3) or a supported-by-design definition (Claim 2 → Step-5 definitions + A1/A2/A6; Claim 4 → spec disclaimer). Every H\* (H1, H2, H3) has a verbatim fallback (Step 6); no orphans in either direction.

### 5. Hypothesis/assumption machinery — **REVISE, fixed**

**Found:** H1/H2/H3 already filled all 7 guidance.md §3.1 template slots (applies_if, metric, test, alpha, effect_floor, aggregation, verbatim fallback) — no gap there. But A1–A6 (guidance.md §3.2) had `description`/`failure_mode`/`detection` but **no explicit `gate` field** — the pilot/skeleton check-point was only informally implied inside the `Detection:` prose (e.g. "M1 admission probe (walking-skeleton gate)"), not stated as its own labeled slot with a named PG-\* id and consequence, as §3.2's template requires ("gate: PG-j if checked in the pilot; else the phase that checks it" + "consequence: what happens to which H\* if it fails").

**Fix applied (paper.md, "Assumptions (A1..A6)" section):** added an explicit `*Gate:*` clause to each of A1–A6, naming PG-1 through PG-5 (or "design-time" for A6) and the consequence for the dependent H\*/task family if the check fails — citing guidance.md §3.2.

### 6. Method-rigor audit — **REVISE, fixed**

Checked guidance.md Part 6 items 1–10 plus the Part 2 A2 (empirical/measurement) evidence standard:
- **Item 1 (R1 estimand, one sentence)** — missing; `paper.md` Step 5 went straight to notation with no explicit estimand sentence. **Fixed:** added an "Estimand (guidance.md R1)" line ahead of the Notation table, naming the quantity (FIR), unit of analysis (episode), reference population (sandboxable coding/tool-calling tasks under log-only-rewarded pressure), and the decision it feeds (deploy log-only vs. add a state check).
- **Item 6 (every instrument has the 5-step R2 plan + acceptance threshold)** — missing; the pilot's own instrument-validity hypotheses (M1 admission-probe fidelity ≥95%, M6 annotation κ≥0.7) existed only in `discussion/pipeline.md`'s Stage 5/6 output (the `auto-research-discussion` run), never folded back into `paper.md` itself, so the pre-registered spec goal.md validates was missing its own instrument-validation plan. **Fixed:** added an "Instrument validation (guidance.md R2)" block after the Assumptions section, giving the 5-step plan + acceptance threshold for M1 (≥95% agreement, zero mistaken admissions) and M6 (κ≥0.7), and noting M2/M3's construction-based (non-rater) validation.
- **Item 9 (power stated per cell; thin cells pre-declared INCONCLUSIVE)** — the aggregate power statement existed (0.98 power for the 10-pp effect) but there was no explicit per-cell INCONCLUSIVE pre-declaration rule in `paper.md` itself (only the general archetype-level guidance in `guidance.md` Part 2/Part 4 situation 5). **Fixed:** added an explicit "Inconclusive-cell rule" paragraph.
- Items 2 (verb check), 3 (H\* slots), 4 (A\* detection — now also gate, see #5 above), 5 (B0+B-alt+F-G\*), 7 (R3 confound-naming, via B-alt's "Rival explanation it kills"), 8 (R6 mechanism layer, via RQ_INF_2's forging-strategy taxonomy), 10 (A2 evidence standard: R2 now met per the fix above, R3–R6 already met) — **PASS**, no fix needed.

### 7. Stage cross-check (advisory) — **PASS**

Already performed by `pengsida-stage-reviewer` above (Stage 1 PASS, Stage 2 REVISE→fixed, Stage 3 PASS, Stage 4 REVISE→fixed, Stage 5 PASS), which is exactly goal.md §3 item 7's N1↔Stage1 / N3-N4↔Stage2 / N6↔Stage3 / N8-E\*↔Stage4 / archetype cross-check. No new STOP-level finding from that pass; both its REVISE fixes are already applied and reflected in `paper_draft.*`.

### 8. Taste audit currency — **PASS**

`taste_audit.md` was run after Stage 2/5 were confirmed and remains current: none of this Phase A run's fixes touch the Core Asymmetry sentence (`paper.md` Step 0) or the Step 5 formal-definition table — the fixes add machinery (estimand statement, assumption gates, instrument-validation plan, inconclusive-cell rule) without altering the asymmetry or the predicates the taste audit evaluated. No re-audit required.

### Gate result: **PASS** (after the two REVISE items above were fixed in this session)

All 8 checklist items now clear. One advisory-level residual is carried forward rather than blocking the gate: `SWE-bench`'s cache record has no locally resolvable `digest_path`/`pdf_path` (network/corpus access limitation, not a fabrication) — since `digest.md`/`paper.md` use it only as background task-source material, not as an instrument or baseline any H\*/A\* depends on, this does not block Phase B per goal.md §3 item 2's "load-bearing entries have resolvable digest_path" (SWE-bench is `background`, not load-bearing in that sense) but should be re-resolved opportunistically before Phase E's freshness sweep (goal.md §1).

Per goal.md's own scope for this environment, **Phase B/C are not attempted** — there is no real experiment compute available here; this run stops at the Phase A gate as instructed.
