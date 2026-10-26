# Pengsida Stage Review — B5.1

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the updated pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask how much and for whom a phenomenon occurs" with no new pipeline proposed as a fix — the testbed (concealment controller, paired toughness-matched injection, cross-model matrix, fidelity auditor) is the *analytical apparatus* that makes the phenomenon measurable, not a method being pitted against baselines to win. This matches digest N12's own `"empirical"` classification and `study_type: empirical` from Stage 1. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — "there is no controlled, mechanically-scored measurement of how much surplus a counterparty can extract... leaving principals with no way to price the economic risk of delegating bargaining to an LLM" is a first-principles framing (a genuine measurement absence, not a patch on an existing metric), and the stakes are stated concretely: real money transferred every time the agent negotiates again, not a generic AI-importance appeal. The Einstein ratio holds — the confirmed Stage 1/2 outputs spend their energy on why the gap matters (who is exposed, why per-tactic and per-sophistication granularity specifically matter) and only name the toughness-subtraction/fidelity-conditioning acceptance criteria as *evaluability conditions* on the objective, not as method content.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap, and — per the mined-checks pattern that caught B5.5's buried twin — that the single closest prior work is named plainly, not left for the reader to infer. Checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The seven works are each given a specific, problem-tied limitation (e.g., TensorTrust/ChatInject: "success is binary instruction-integrity, not a continuous economic quantity"; StrategicPersuasion: "doesn't model a bilateral price negotiation with two-sided private reservations, multi-round concession dynamics, or an economic-surplus payoff") — this clears the "citation dump" and "generic limitation" failure modes cleanly. But nowhere in the confirmed Stage 3 output, nor in `paper.md`'s own N3, is a single work named as the *closest* prior work with its delta stated plainly. Digest N3's own coverage note comes closest ("neither isolates and prices individual manipulation tactics") but that sentence characterizes the whole landscape, not one nearest neighbor. Per the Stage 2 bar: "Is the single closest prior work named and its delta stated plainly? Hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first." A reviewer reading only the seven parallel limitations has to rank them unaided — and the two most methodologically adjacent works (TensorTrust and ChatInject, the only cited works that already run *controlled, templated, single-variable adversarial injection* — this paper's own core methodological move) are never elevated above the other five as the nearest neighbor.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence at the opening of Related Work naming TensorTrust and ChatInject as the closest prior work by injection methodology, and stating the precise delta (their success construct is binary instruction-integrity; this paper's is a continuous, concealed-ground-truth economic quantity) — rather than leaving the reader to infer which of the seven threads is closest.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — `ΔS`, the paired-injection/toughness-subtraction discriminator, and the fidelity/genuineness re-probe are all given in Problem Definition/Methodology ahead of any claim that invokes them (no "named after the fact" violation). The inferential chain is licensed at its one load-bearing hinge: a tactic's ΔS against the no-tactic control could in principle be driven by generic assertiveness rather than the tactic's specific content — the budget-matched generic-toughness arm exists precisely to make that alternative explanation testable and subtractable, and the draft states this explicitly ("a tactic that does not survive this subtraction is attributable to aggression, not tactic-specific manipulation") rather than asserting tactic-specificity by fiat. No orphan components — every one of the six modules (paired injection, concealment controller, cross-model matrix, variance-control design, sophistication crossing, fidelity auditor) traces to a named sub-problem, and every sub-problem traces to at least one hypothesis and RQ (cross-stage check in `pipeline.md`), with no leftover machinery.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: `rq_fidelity_loadbearing` is a genuine falsification design (recomputing the accept/reject verdict on verified-fidelity, verified-genuine dialogues to see if the verdict *changes*, not just correlates with the raw statistic), and `rq_toughness_survival` is likewise built to *refute* tactic-specificity if the toughness-subtracted effect vanishes. But the confirmed Stage 6 output states each RQ's `expected_outcome` (which, verbatim, are Stage 5's hypotheses) without a parallel line stating what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test" stated as a check, not implied. `paper.md`'s own Step 6 already has this discipline as pre-committed fallbacks (F1, F2, F3, F-G1) — e.g., F1: "If no tactic reaches ΔS ≥ 0.10 but ≥1 reaches ΔS ≥ 0.03... reframe the headline from magnitude to reliability"; F-G1: "no tactic clears ΔS ≥ 0.10 over B0, none survives the B-alt toughness subtraction → pivot... to robustness-bound (negative-result)" — but this discipline did not survive into the first assembled `paper_draft.md`'s RQ subsections, which stopped at "Expected outcome."

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all nine RQ subsections, stating the specific observation that would refute each expected outcome — translating `paper.md`'s own F1/F2/F3/F-G1 fallback logic into a per-RQ falsification statement, not inventing new content.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes on the assembled `paper_draft.md` — reading only each Introduction paragraph's first sentence ("Autonomous LLM agents are increasingly delegated to negotiate real economic transactions" / "Yet no controlled measurement exists of how much surplus a specific linguistic tactic can extract" / "The nearest existing work approaches this gap through controlled adversarial injection, not economic pricing" / "Turning this gap into a measurable question surfaces its own difficulties" / "Our approach turns each of these obstacles into a specific instrument-design choice" / "We evaluate this design across...") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title and abstract: "a reservation price never enters either agent's visible context, so any shift in the agreed price away from that concealed ground truth is, by construction, attributable to something other than the payoff structure itself." The Conclusion names a real forward-looking limitation (the four-tactic, single-good scope, and the possibility that the toughness-subtraction discriminator itself needs refinement in multi-issue settings) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph, naming TensorTrust and ChatInject as the closest prior work by injection methodology and stating the delta plainly (binary instruction-integrity vs. continuous, concealed-ground-truth economic surplus) — rather than leaving seven parallel limitations unranked.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the nine RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), translating `paper.md`'s own pre-committed fallbacks (F1, F2, F3, F-G1) into per-RQ falsification statements, then compiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — 2026-07-04

> Runs goal.md §3's 8-item checklist against `README.md`/`digest.md`/`paper.md`, applying `guidance.md` as the standard, after Task 1's reference-cache upgrade (`reference_candidates.jsonl` rewritten from the flat 150-candidate harvest schema into goal.md §1's canonical schema: 15 selected / 142 rejected, each with a `relevance` tag and a specific `why`). No Phase B/C compute exists in this environment — this pass stops at the Phase A gate as instructed and does not attempt walking-skeleton execution.

### 1. Digest self-verification — **REVISE (fixed)**
All of N0–N12 + Claims are present in `digest.md`, and every non-GIVEN node I checked carried a 3-part `absence_comment` (`what_missing`/`why_matters`/`implication`) **except N12** (Contribution Type), which had a `rationale`/`source` but no `absence_comment` despite being tagged `[HYPOTHESIS]` — a tag-discipline gap under goal.md §3 item 1's "every non-GIVEN item carries its 3-part absence comment." **Fix applied:** added N12's `absence_comment` (digest.md), explaining that the `empirical` classification is this pipeline's own inference, not an author self-classification, and why the distinction matters (it gates which guidance.md Part 2 archetype evidence standard applies). Cross-node references (N3 citation keys reused verbatim in N4/N6/N10/Claims) all resolve internally.

### 2. Reference-cache integrity — **REVISE (partially fixed; one residual open item)**
Before Task 1, every `digest.md` N3 citation key (ARIA, CompeteAI, StrategicPersuasion, TensorTrust, ChatInject, StrategicDishonesty, ClickBandit — all sourced from `topics/corpus/ideas.jsonl`, a *different* corpus than the one harvested into `reference_candidates.jsonl`) had **no cache record at all** — a hard failure of goal.md §3 item 2 ("every N3 key is a selected cache record"). **Fix applied:** backfilled all 7 as `verdict: selected` records in `reference_candidates.jsonl` (keys `ARIA2025`, `CompeteAI2024`, `StrategicPersuasion2024`, `TensorTrust2024`, `ChatInject2025`, `StrategicDishonesty2025`, `ClickBandit2024`), each with a `relevance` tag matching its role already established in `pipeline.md`/this file (TensorTrust/ChatInject = `method-twin`, StrategicPersuasion = `baseline`, ARIA/CompeteAI/StrategicDishonesty = `adjacent`, ClickBandit = `background`).
**Residual open item (not fixable without network access — attempted and blocked):** none of these 7 has a locally cached PDF or a standalone extraction-mode digest; `verified.id_resolves = false` for all seven, and their `approach_summary` in `digest.md` N3 remains sourced from `ideas.jsonl`'s own related-work summary text, not an independently fetched paper. I attempted one spot-check fetch (`https://openreview.net/forum?id=fsW7wJGLBd`, TensorTrust) via `WebFetch`; it returned only a bot-verification page, confirming no outbound network access in this environment. This is now explicitly documented (`digest.md` N3 `absence_comment`) as a blocking pre-Phase-E task rather than a silent gap: goal.md §1 step ② ("Digest every potentially load-bearing candidate... with `paper-digest` in extraction mode") must run for these 7 once a connected session is available. Of the 150 harvested candidates, all have non-null `pdf_path` and all 150 files were confirmed present on disk (`verified.id_resolves = true`); no `pending` verdict remains anywhere in the cache (150/150 harvested + 7 backfilled all resolved to `selected`/`rejected`).

### 3. Tag discipline — **PASS**
`digest.md` tags every assertion `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[PLACEHOLDER]` throughout; no silent promotion found (e.g., Abstract v0 in `paper.md` explicitly re-states "no experiment has been run; ΔS values are the pre-registered target, not results" rather than letting the draft abstract read as a finding).

### 4. Claim–Evidence Map completeness — **PASS**
Every row in `paper.md`'s Claim–Evidence Map traces to an H-id or a Step-5 supported-by-design definition; no orphans in either direction. (The map now has 8 rows after fix 6 below adds the H4/F4 mechanism row — see item 6.)

### 5. Hypothesis/assumption machinery — **REVISE (fixed)**
H1–H3 fill guidance.md §3.1's seven slots in substance (statement+magnitude+direction, `applies_if`, metric, test, alpha, effect floor, aggregation rule, verbatim fallback), though embedded in prose rather than a literal key-value block — accepted as substance-equivalent. The **assumption ledger had a real, not cosmetic, defect**: A3 (injection fidelity), A5 (cross-model footing), and A6 (tactic ≠ phrasing confound) each said "detected by: pilot ..." while Step 9's Walking Skeleton explicitly **defers M6** ("No LLM judge in the skeleton"), runs **one** manipulator/counterparty pair only, and uses a **single** anchoring intensity — i.e., none of A3/A5/A6 can actually be checked in the pilot as specified, contradicting their own "gate" claim. This is exactly guidance.md §3.2's warning that "assumption verification is an activity, not a paragraph." **Fix applied:** added explicit `Gate:` lines to all six assumptions in `paper.md` — A1→**PG-1** (pilot), A2→**PG-2** (pilot), A4→**PG-3** (pilot), and A3/A5/A6 honestly re-gated to **Stage-2 scale-up**, with H1's pilot-stage reading now flagged provisional on A3 until Stage-2. B0 + B-alt + F-G1 were already present with pre-committed wording (unchanged, still PASS).

### 6. Method-rigor audit — **REVISE (fixed)**
Ran guidance.md Part 6 items 1–10 plus Part 2's A2 (empirical/measurement) evidence standard — validated instrument (R2) + controlled comparison (R3) + effect-size-floored tests (R4) + rival-explanation ablations (R5) + ≥1 mechanism analysis (R6) — against the plan as written, three misses found and fixed:
- **Item 1 (R1 estimand)** — Step 5 had notation and definitions but no single estimand sentence naming quantity/unit/population/decision. **Fix:** added an explicit "Estimand (guidance.md R1)" sentence to `paper.md` Step 5.
- **Item 6 (R2 instrument validation)** — the M6 fidelity/genuineness auditor is an LLM-judge instrument but had no stated 5-step R2 sequence or κ acceptance threshold; per R2's closing rule, "asserted validation numbers without protocol are treated as absent." **Fix:** added a full 5-step R2 plan (ground categories → draft-wide/refine on held-out set → validate against ≥2 human raters at **κ ≥ 0.7** → inspect confusion structure → freeze before scale-up) as a new `paper.md` Step-6 subsection.
- **Item 8 (R6 mechanism analysis)** — the A2 archetype requires ≥1 mechanism analysis, but the plan had only headline magnitude/interaction tests, no analysis of *why* any tactic works. **Fix:** added **RQ4/H4/F4** to `paper.md` Step 6 — a dose-response mechanism test (does the anchor's numeric distance from the ZOPA-fair point predict price beyond a perceived-toughness covariate?), distinct from the B-alt categorical subtraction, with its own fallback and a new Claim–Evidence Map row explicitly marked mechanism-tier (not promoted to the abstract unless it survives).
- **Item 9 (thin cells)** — Part 4 situation 5 requires under-powered cells be pre-declared INCONCLUSIVE, never null, never silently dropped; no such rule existed. **Fix:** added an explicit thin-cell INCONCLUSIVE rule to `paper.md`'s Assumptions section.
Items 2–5, 7, 10 (verb check, B0/B-alt/F-G1, confound-naming, archetype-named) were already met — **PASS** on those sub-items unchanged.

### 7. Stage cross-check (advisory) — **PASS (already run; now slightly extended)**
`pengsida-stage-reviewer`'s Stages 1–5 review (top of this file) already ran with 2 REVISE findings fixed before `paper_draft.*` was produced. That review predates today's Task 1/2 changes; the archetype classification (Analysis/Finding via `archetypes.md`) and Stage 1–5 verdicts are unaffected by today's additive fixes (new RQ4, gate labels, R2 plan, N3 backfill are rigor scaffolding, not reframing), so no re-run of the full stage-reviewer skill was triggered — advisory, does not block.

### 8. Taste audit currency — **PASS, no re-audit triggered**
Today's edits (Estimand sentence, assumption gates, R2 validation plan, RQ4 mechanism test, thin-cell rule, N3 backfill/concessions) are additive rigor scaffolding — none changes the core asymmetry sentence (Step 0) or the formal ΔS definition (Step 5's `σ`/`ΔS_t` equations are unchanged, only a preceding estimand sentence was added). Per goal.md §3 item 8, re-audit is required only on a "material edit to the asymmetry statement or formal definition" — not triggered here. `taste_audit.md` remains current.

### New finding outside the 8-item checklist: undiscovered method-twins (guidance.md Part 4 situation 6)
Task 1's cache upgrade surfaced two arXiv papers — **DECEPTICON** (2512.22894, dark-pattern manipulation of web agents, including an "urgency" tactic category) and **TRAP** (2512.23128, a 630-combination persuasion/manipulation-tactic injection benchmark for web agents) — that are genuine structural twins on tactic-injection methodology and were **not** in `digest.md`'s original N3 sweep (which only searched `topics/corpus/ideas.jsonl`, missing the separately-harvested arXiv cache). This is exactly guidance.md Part 4 situation 6 ("method-twin discovered mid-run... concede-and-differentiate, at source... a paper.md repositioning + Phase A re-check, never a silent related-work paragraph"). **Fix applied:** added both as N3 works 8–9 with dedicated N4 limitations (7–8) in `digest.md`, and referenced them alongside TensorTrust/ChatInject in N6's M2 description — conceding what's shared (both independently confirm a named manipulation-tactic taxonomy steers LLM-agent behavior) and stating the delta (binary task-redirection/UI-deviation success vs. this paper's continuous, concealed-valuation economic surplus).

### Overall Phase A gate: **REVISE** (not a clean PASS; not a STOP)
Six concrete fixes were applied directly to `digest.md`/`paper.md` (items 1, 2-partial, 5, 6×3). One item (2) has a residual, environment-blocked gap (no network access to fetch/digest the 7 backfilled N3 works) that is now explicitly documented rather than silently absent. Per the task's scope, this run stops at the Phase A gate — no walking-skeleton (Phase B) execution was attempted. **Before Phase B can proceed:** (a) fetch/digest the 7 backfilled OpenReview works in a connected session; (b) note that `discussion/paper_draft.md/.tex/.pdf` (Phase E/F/I outputs, produced before today's Task 1/2 changes) are now **stale** relative to the updated `paper.md`/`digest.md` — they do not yet reflect RQ4/H4/F4, the assumption gate corrections, the R2 validation plan, or the DECEPTICON/TRAP concession — and must be regenerated by re-entering Phase E once Phase A closes cleanly.
