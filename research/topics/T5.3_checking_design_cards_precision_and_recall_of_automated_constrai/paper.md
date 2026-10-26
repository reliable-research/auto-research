# Checking Design Cards: Precision and Recall of Automated Constraint Verification against Human Review — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All thresholds below are pre-registered before any data collection. Digest ids (C1.., M1.., RQ.., CO.., L1..) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** A design constraint's automatable-ness is a fixed property of the constraint itself — whether its truth condition is computable from the patch's observable structure (AST, imports, identifiers) or only from the design intent that the card names but does not encode — and is therefore invariant to how much engineering is spent on the verifier; verifier quality is meaningful only per constraint category and only relative to the human–human agreement ceiling, never as one aggregate number.

**判据 (deletion test).** Delete the domain nouns (design constraint, patch, card, verifier, human review):

> "An X's automatable-ness is a fixed property of X — whether its truth condition is computable from Y's observable structure or only from the intent that Z names but does not encode — invariant to engineering effort on W."

Without the nouns, "the intent that Z names but does not encode" has no referent and "Y's observable structure" designates nothing: the sentence is empty, not a valid generic claim. The load is carried by the specific gap between a card's *text* (which the verifier reads) and its *intent* (which only the human reviewer reconstructs) — cf. digest C1, C3. **Not a bridge:** the sentence connects nothing to nothing; it asserts an invariant (operationalizability is intrinsic to the constraint type) that the experiments try to refute.

## Step 2 — Archetype

**Primary: `empirical` (measurement study)** — consistent with digest N12. **Secondary: `benchmark`** (CO4, the three-way-aligned corpus) with `tool` (CO1) as instrument only.

Downstream consequences:
- **(a) Abstract contribution slot:** per-category precision/recall numbers benchmarked against a *measured* human–human κ ceiling, plus a statistically operationalized automatable/human-required partition of constraint categories (CO2, CO3). NOT "we present a verifier that outperforms X."
- **(b) Intro logic:** "what becomes possible" — teams can *route* human review to exactly the constraint categories where automation is measurably below the human band, instead of reviewing uniformly (digest N2). No SOTA-beating framing anywhere.
- **(c) Evidence standard for results:** pre-registered statistical tests (κ-gap CIs, Holm-corrected McNemar), reported per category with the human ceiling in every table; a negative or uniform result is a publishable finding under the fallbacks in Step 6, because the archetype is measurement, not method superiority.

## Step 3 — Taste Self-Audit

| Check | Verdict | Note / fix |
|---|---|---|
| Is the opportunity a Bridge ("A and B never connected")? | PASS | The opportunity is an unmeasured quantity (verifier-vs-human gap per constraint type) that gates a real decision (safe delegation of review), not a connection between fields. |
| Is the method mere Synthesis? | RISK → CONTAINED | M3 *is* a hybrid (rule/AST + conformance + LLM-judge). Fix at the skeleton level: M3 is declared the **measurement instrument**, never the contribution; the contribution is the measured partition (CO2/CO3). No claim of the form "our hybrid verifier is better" survives into the abstract; B-alt (Step 6) exists precisely to prevent the hybrid from being credited for generic LLM capability. |
| Load-bearing verbs from integrate/unify/leverage family? | PASS after audit | Load-bearing verbs: **measure, bound, partition, gate, isolate, formalize**. "Hybrid" appears only in instrument description. |
| Abstract-opening rule | PASS | Abstract v0 opens with the asymmetry (operationalizability is intrinsic), not "coding agents are increasingly used… however… we introduce" — that template is banned; the digest's N0 draft abstract violates it and is superseded by Abstract v0 below. |

## Step 5 — Formal Problem Definition

**Estimand (guidance.md §3.4 R1 — added at Phase A re-run, 2026-07-04; see discussion/stage_review.md "Phase A (re-run)").** The quantity of interest is the per-category gap `Δ_t = κ_H,t − κ_V,t` between measured human–human and verifier–human agreement, with unit of analysis one adjudicated `(card, patch)` pair; the reference population is category-labeled design-card × coding-agent-patch pairs constructible from SWE-bench-seeded issue→PR tasks (digest M2); it feeds a binary per-category delegation decision — route that constraint category to automated verification vs. keep it under mandatory human review — never a paper-wide verdict on "the verifier."

**Notation.**
- Card set `C`; category map `τ: C → T`, `T = {STRUCT, API, NAME, SEC, INTENT}` (architectural boundary, API-usage restriction, naming/style, security invariant, intent-level design principle — digest M1). `T_syn = {STRUCT, API, NAME, SEC}`, `T_sem = {INTENT}`.
- Patch set `P`; evaluation unit is a pair `(c, p) ∈ C × P` with card scope applicable to the patch (digest M2).
- Verifier `V: (c, p) → {1, 0}` (violation / no-violation), with confidence `q(c,p) ∈ [0,1]` (digest M3).
- Human panel: `r ≥ 3` reviewers give labels `h_i(c,p) ∈ {1, 0}`; adjudicated reference `y(c,p)` (digest M4).
- Per category `t`: `Prec_t = TP_t/(TP_t+FP_t)`, `Rec_t = TP_t/(TP_t+FN_t)`, `F1_t`, computed w.r.t. `y`; `κ_V,t` = Cohen's κ between `V` and `y`; `κ_H,t` = Fleiss' κ among the `r` reviewers (the noise ceiling); κ-gap `Δ_t = κ_H,t − κ_V,t`.

**Adjective → definition → measurement** (every load-bearing adjective in the digest Claims gets a computable quantity or is deleted):

| Adjective/verb (from Claims 1–4) | Formal definition | Measured by |
|---|---|---|
| "automatable" (category) | `t` is automatable iff the 95% bootstrap CI (10,000 resamples, clustered by card) of `Δ_t` has upper bound ≤ 0.10 AND `n_violations(t) ≥ 30` | M5 alignment analysis |
| "human-required" (category) | 95% CI of `Δ_t` has lower bound > 0.10 | M5 |
| "inconclusive" (category) | neither of the above, or `n_violations(t) < 30` (never reported as automatable — digest t4) | M5 |
| "reliably automated" (verifier on t) | `Prec_t ≥ 0.85` AND `Rec_t ≥ 0.80`, Wilson 95% CI lower bounds ≥ 0.75 for both | M5 |
| "structurally checkable" (card) | decision procedure: two annotators independently write a deterministic checker spec (pure function of diff + AST) for the card; card is structurally checkable iff both succeed and specs agree on all pilot pairs | M1 card authoring gate |
| "intent-laden" (card) | not structurally checkable under the above procedure | M1 |
| "irreducible disagreement" (reference) | `κ_H,t < 1` as measured; interpretability requires `κ_H,t ≥ 0.4` (A2) | M4 |
| "gap concentrated in semantic categories" (Claim 1) | `min_{t∈T_syn} F1_t − F1_INTENT ≥ 0.15` AND category×correctness interaction significant (see H2) | M5 |
| "adoptable" (Claim 4) | per-category operating curve reported; verifier's chosen operating point has `Prec_t ≥ 0.85` on every category it is deployed on (FP-driven abandonment, Johnson et al. 2013 / L6) | M5 |
| "balanced, non-trivial" (corpus) | per category: 25–60% of pairs are adjudicated violations, AND ≥ 20% of pairs survive the human pre-screen as "non-obvious" (reviewer needed > 30 s median) | M2 curation gate |

Deleted adjectives: "safely" (folded into "reliably automated"), "substantially lower" (replaced by the 0.15 F1 margin), "inherently" (replaced by the human-required CI rule — "inherent" beyond that is unmeasurable and not claimed).

## Assumptions (A1..A6)

| id | Assumption | How it could fail | Detection / gate | Consequence (guidance.md §3.2 — added at Phase A re-run, 2026-07-04) |
|---|---|---|---|---|
| A1 | Design cards can be authored explicitly and category-labeled reproducibly: two annotators agree on `τ(c)` with κ ≥ 0.7. | Categories blur (a card is both API and INTENT); taxonomy T is not a partition. | Pilot card-labeling round in walking skeleton; if κ < 0.7, revise T before Stage 1 (gate G-A1). | Blocks E1/E2 entirely: T is the denominator for every per-category metric in H1–H3, so an unresolved partition failure means no H\* can be scored per-category until T is revised. |
| A2 | Human review is usable as reference: `κ_H,t ≥ 0.4` in every category. | Reviewers disagree wildly on INTENT cards (digest C2, t1) → reference is noise. | Skeleton pass criterion; if κ_H,INTENT < 0.4 the category is reported as "reference-unstable," excluded from H3's denominator, and itself becomes a finding. | Degrades H3 only: the affected category is dropped from H3's automatable/human-required partition (not scored either way); H1/H2 on other categories are unaffected. |
| A3 | A balanced, non-trivial pair corpus is constructible: ≥ 30 adjudicated violations/category at Stage 2 (≥ 8 at pilot), meeting the Step-5 "balanced, non-trivial" definition. | Agent patches rarely violate certain categories; injected violations are trivially detectable (digest N6 feasibility risk). | M2 curation gate: human pre-screen discards trivially-compliant/obvious pairs; violation counts checked before analysis (gate G-A3). | Restricts scope: categories below the 30-violation floor are forced to "inconclusive" per the Step-5 rule for H1–H3 (never scored automatable or human-required), shrinking which categories the paper can claim anything about. |
| A4 | SWE-bench-style issue→PR tasks plus ≥ 2 coding agents yield patches representative enough that per-category results transfer (digest t2). | Single-agent idiosyncrasies dominate; results are agent-specific. | Stage 2 uses ≥ 2 agents; agent-ID is a covariate in H2's regression; significant agent×category interaction triggers per-agent reporting. | Degrades H2's generality: a significant agent×category interaction narrows H2's claim to a per-agent finding and triggers per-agent reporting rather than a single pooled split. |
| A5 | The measurement is inference-only and affordable: pilot ≈ tens of USD in LLM calls, 20 annotator-hours (digest N6 feasibility); Stage 2 ≤ low-hundreds USD. | LLM-judge needs many more calls/pair for stable output. | Skeleton records cost/pair; if projected Stage-2 cost > 5× estimate, reduce LLM-judge sampling before scaling. | Degrades M3c's calibration precision (fewer judge samples/pair), which weakens the confidence estimates H2/H3 rely on for the INTENT category specifically, without blocking E1/E2 outright. |
| A6 | Role separation removes circularity: card authors ≠ patch curators ≠ verifier builders (digest t3). | Same person tunes verifier on cards they wrote → inflated agreement. | Roles assigned and logged before Stage 1; verifier frozen (code hash recorded) before adjudicated labels are revealed. | Blocks all three H\*: an undetected violation inflates `κ_V,t` (M5) for every category, invalidating H1–H3's reported gaps outright rather than merely degrading one; this is why the mitigation is a design-time freeze, not a post-hoc check. |

**Instrument validation (guidance.md §3.4 R2) for the category taxonomy `T` — added at Phase A re-run, 2026-07-04.** `T = {STRUCT, API, NAME, SEC, INTENT}` is itself a measurement instrument (every H\* is scored *per category*) and gets the full 5-step sequence, not just the κ ≥ 0.7 acceptance threshold already stated in A1: ① **ground** each category in a named external source — STRUCT in architecture-conformance literature (Reflexion models), API/NAME in static-analysis rule taxonomies, SEC in security-invariant checklists, INTENT in design-principle literature (separation-of-concerns); ② **draft wide, refine on a held-out set** — the walking skeleton's 10-card pilot labeling round is the held-out calibration set; any category pair with κ < 0.7 is merged or the boundary re-drawn with the operation named (e.g. "SEC merged into API" or "INTENT split into INTENT-behavioral/INTENT-structural"), never silently re-labeled; ③ **validate against ≥ 2 independent annotators**, κ ≥ 0.7 required (A1's stated threshold); ④ **inspect the confusion structure** — disagreements between the two annotators must land on adjacent categories (e.g. API vs. SEC) rather than a systematic collapse of one category into another, or T itself is reported as ill-defined (situation 7, guidance.md Part 4) rather than scored; ⑤ **freeze** `T` (hash the category set and predicate list) before Stage-2 scale-up, per the same freeze discipline as A6's verifier-hash gate.

## Step 6 — Pre-Registered Experiments

### E1 — RQ1 (digest N8): precision/recall of the automated checker vs human review

- **Assumptions:** A1, A2, A3, A5, A6.
- **Hypotheses (binary, hard-coded):**
  - **H1 (absolute, structural):** On each category in `T_syn`, the frozen hybrid verifier is "reliably automated" per Step 5: `Prec_t ≥ 0.85` AND `Rec_t ≥ 0.80`, Wilson 95% CI lower bounds ≥ 0.75. Pass = all four `T_syn` categories meet this.
  - **H2 (the split):** `min_{t∈T_syn} F1_t − F1_INTENT ≥ 0.15`, AND a logistic regression of per-pair verifier correctness on category (+ agent covariate, clustered SEs by card) shows a significant category effect via likelihood-ratio test at α = 0.05.
- **Metric:** `Prec_t`, `Rec_t`, `F1_t`, `κ_V,t` exactly as defined in Step 5, computed against adjudicated `y` (digest N8 metrics; MCC reported descriptively, not gated).
- **Verification:** Stage-2 corpus ≥ 1,000 pairs, ≥ 150/category, ≥ 30 violations/category (digest N8 analysis plan). Wilson CIs for Prec/Rec; 10,000-resample bootstrap clustered by card for F1 differences; verifier-vs-baseline paired decisions via McNemar's test, α = 0.05, Holm correction across the 5 categories. Verifier code hash frozen before label reveal (A6).
- **Fallback (pre-committed wording):**
  - If H1 fails: *"Even structurally-defined design constraints are not reliably automatable at prototype maturity: on ⟨failing categories⟩ the verifier's precision or recall falls below the pre-registered 0.85/0.80 bar, and we report where false positives and false negatives concentrate — a measured engineering gap for constraint checking, with the human–human ceiling showing the headroom is real."*
  - If H2 fails with uniformly high performance: *"Automated constraint verification matches human review across the full card taxonomy, including intent-level constraints; the presumed automatable/human-required divide is an engineering artifact, not an intrinsic property of constraint types."* (This is digest N9's RQ1 falsification condition, embraced as a claim.)
  - If H2 fails with uniformly low performance: escalate to F-G1.

### E2 — RQ2 (digest N8): which categories are automatable vs human-required

- **Assumptions:** A1, A2, A3, A4.
- **Hypothesis (binary, hard-coded):**
  - **H3 (partition):** Applying the Step-5 decision rule to all 5 categories: at least 2 categories are classified "automatable" (κ-gap CI upper ≤ 0.10), AND INTENT is classified "human-required" (κ-gap CI lower > 0.10), AND at most 1 category is "inconclusive." Pass = all three conjuncts.
- **Metric:** `Δ_t = κ_H,t − κ_V,t` with clustered bootstrap CI, per Step 5; `κ_H,t` from M4, `κ_V,t` from M5 (digest RQ2 analysis: verifier–human vs human–human agreement band).
- **Verification:** Same corpus as E1. 95% bootstrap CIs on `Δ_t` (10,000 resamples, clustered by card); Holm correction across 5 categories for the human-required tests; categories with `n_violations < 30` forced to "inconclusive" regardless of CI (digest t4 hardened into the decision rule).
- **Fallback (pre-committed wording):**
  - If < 2 categories automatable (but ≥ 1 structural category passes H1): *"The automatable set is narrower than the structural/semantic divide predicts: only ⟨t⟩ reaches the human-agreement band, and we report the per-category κ-gaps as a calibration map telling teams exactly how much residual human review each constraint type requires."*
  - If INTENT is NOT human-required (κ-gap CI includes ≤ 0.10): *"Intent-level design constraints, contrary to the operationalizability hypothesis, are checkable to within the human-agreement band by a calibrated LLM judge; the binding limit on automated design-review is reference noise (κ_H), not constraint semantics."*
  - If > 1 category inconclusive: *"The three-way-alignment protocol at this scale bounds but does not resolve the partition for ⟨categories⟩; we publish the corpus, the measured ceilings, and the power analysis specifying the corpus size at which the partition becomes decidable."*

### E3 — Mechanism analysis (guidance.md §3.4 R6 — added at Phase A re-run, 2026-07-04)

E1/E2 establish *that* a category-level gap exists and *which* categories it concentrates in; E3 explains *why*, so the finding is diagnosed rather than merely observed (Part 6 item 8; Part 2 A2's evidence standard requires ≥1 mechanism analysis).

- **Assumptions:** A2 (a reference-unstable category cannot be mechanism-analyzed against its own noise).
- **Design:** On every verifier error the adjudicated panel disagrees with (both false positives and false negatives), a second independent coding pass (2 raters, disagreements adjudicated) classifies the error into one of three mutually exclusive mechanism types: (i) **literal-vs-intent mismatch** — patch satisfies the card's literal text but violates its intent, or vice versa (digest C3); (ii) **structural/pattern-matching failure** — the verifier's rule/AST or conformance check misparsed or missed a syntactic pattern it should have caught; (iii) **other** (e.g. adjudication error, ambiguous card wording). Budget: all errors on the two extreme categories used in the walking skeleton (API, INTENT) at Stage 1, and a stratified sample of ≥20 errors per category at Stage 2.
- **Metric:** proportion of INTENT-category errors attributable to (i) vs. the proportion of API/structural-category errors attributable to (ii), with a 95% Wilson CI per proportion.
- **Pre-committed reading:** if (i) dominates INTENT errors and (ii) dominates structural-category errors, this is the mechanistic confirmation of the Step-0 asymmetry (the gap is *caused* by the literal/intent distinction, not an artifact of one sub-mechanism being under-engineered); if (ii) dominates INTENT errors instead, the gap is an M3 engineering artifact (the LLM-judge sub-mechanism itself is failing structurally, not on intent), which redirects the fallback ladder toward "improve M3c" rather than "INTENT is inherently human-required."
- **Reporting:** an error-taxonomy table (category × mechanism-type counts) alongside the headline Δ_t numbers, per R7's requirement that a headline number get a plain-language explanation, not just a magnitude gloss.

### Mandatory baselines

- **B0 — "why do this at all" control: naive regex/keyword matcher** (digest N8 baselines). Matches card keywords/patterns against the raw diff text; no AST, no LLM. Justification role: if B0 already sits inside the human-agreement band on any category, that category needed no verifier research and the problem shrinks; the gap between B0 and the human ceiling is the measured size of the problem. Pre-registered check: hybrid verifier must beat B0 on pooled decisions, McNemar p < 0.05 (Holm-corrected), else F-G1 territory.
- **B-alt — strongest-alternative-explanation control: single-shot LLM-as-judge, no card decomposition, no abstention, no routing** (digest N8 baselines), **budget-matched**: same base model, same total token budget per pair as the hybrid's full M3 pipeline. **The rival explanation:** *any per-category split we observe merely reflects the base LLM's generic capability profile across code-reasoning task types, not the constraint's intrinsic operationalizability nor the card-decomposition/routing mechanism.* B-alt isolates this: if B-alt shows the same category split as the hybrid (per-category F1 differences within 0.05), the split is attributed to constraint operationalizability itself (supporting the Step-0 asymmetry, since it is instrument-invariant); if the hybrid's split differs from B-alt's, the instrument shapes the answer and CO3's partition is reported as instrument-conditional. Secondary comparison arm: the calibrated selective judge (Trust-or-Escalate style, digest baselines) reported descriptively.

### Global fallback F-G1 — archetype pivot

If the central hypothesis family (H1–H3) fails jointly — no category reaches the human band and no interpretable split emerges — pivot from `empirical` (measurement of the partition) to `benchmark` (digest N12 explicitly names this runner-up): the contribution becomes the three-way-aligned corpus with its measured human-agreement ceiling (CO4) plus the negative result that no current verifier configuration reaches that ceiling anywhere. **Pivoted abstract sentence:** *"We release a three-way-aligned benchmark — category-labeled design cards, coding-agent patches, and adjudicated multi-reviewer labels with a measured human-agreement ceiling per category — on which no automated verifier configuration (rule-based, architecture-conformance, or budget-matched LLM judge) reaches the human band in any constraint category, establishing both the measurement instrument and the open gap."*

## Step 9 — Walking Skeleton

**One binary question:** *Does the three-way-alignment protocol yield a usable reference and an end-to-end per-category reading at all — i.e., κ_H ≥ 0.4 in both a structural and an intent category, with the full pipeline computing per-category P/R/κ without manual patching?*

- **Arms (2):** (1) hybrid verifier M3 (all three sub-mechanisms wired, minimal prompts); (2) B0 regex matcher. (Human panel is the reference, not an arm.)
- **Smallest task set:** 2 categories (API — structurally checkable; INTENT — intent-laden, chosen as the extremes of the Step-5 operationalizability procedure) × 5 cards × 4 patches (2 curated compliant, 2 violating, from SWE-bench-seeded tasks) = **40 pairs**; 3 reviewers × 40 = 120 labels ≈ 4 annotator-hours + 1 adjudication hour (digest N6 feasibility, scaled down).
- **Deterministic metrics only:** point-estimate `Prec_t`, `Rec_t`, `F1_t`, `κ_V,t`, `κ_H,t` (fixed seeds, temperature 0 for the LLM judge, pinned model version per digest t5). No CIs, no significance tests at this stage.
- **Expected wall-clock/cost:** ≤ 2 working days end-to-end; ≤ 10 USD LLM calls (≈ 40 pairs × few calls, digest N6 cost class).
- **Pass criterion (explicit):** ALL of — (i) `κ_H,API ≥ 0.4` and `κ_H,INTENT ≥ 0.4` (A2 gate); (ii) card category labeling κ ≥ 0.7 on the 10 cards (A1 gate); (iii) both arms produce a label for all 40 pairs and per-category metrics compute from one command; (iv) `F1_API ≠ F1_INTENT` for the hybrid arm is a readable signed number (no threshold — direction only). **Skeleton passed ⇒ scaling to Stage 1/2 changes only corpus config files (card list, pair list, category set, resample count) — no code change.** Any code change required to add a category or reviewer means the skeleton has NOT passed.

## Claim–Evidence Map

| # | Abstract-bound claim (from digest Claims) | Traces to | Status |
|---|---|---|---|
| 1 | Verifier–human gap is real and concentrated in intent-level categories (Claim 1) | H2, H3; "gap concentrated" definition (Step 5) | needs-experiment; fallback-covered (E1/E2 fallbacks) |
| 2 | Human review carries irreducible disagreement; the measured κ_H ceiling is what makes P/R interpretable (Claim 2) | A2, M4, Step-5 "irreducible disagreement" | supported-by-design (measured by protocol regardless of H outcomes) |
| 3 | The automatable/human-required split is a property of constraint type, not verifier effort (Claim 3, = Step-0 asymmetry) | H3 + B-alt instrument-invariance check | needs-experiment; fallback-covered (E2 fallback 2 states the reversal) |
| 4 | Per-category operating curves, not blended accuracy, govern adoptability (Claim 4) | Step-5 "adoptable" definition; E1 reporting format | supported-by-design (reporting commitment, not a result) |
| 5 | A reusable three-way-aligned corpus exists (CO4) | M1/M2/M4 construction + A3 gate | supported-by-design; is the F-G1 landing zone |
| — | No claim of verifier superiority as a method contribution | Step 3 audit | excluded by design |

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — written before any results; numbers are pre-registered targets, not findings.]**
> Whether a design constraint can be checked automatically is a property of the constraint itself — its truth condition is either computable from a patch's observable structure or recoverable only from the intent its design card names but does not encode. We formalize this operationalizability split and measure it: a frozen hybrid verifier (rule/AST, architecture-conformance, calibrated LLM judge) is scored per constraint category against adjudicated multi-reviewer labels on a three-way-aligned corpus of design cards, coding-agent patches, and human review, with the human–human agreement ceiling (Fleiss κ) measured rather than assumed. A category is *automatable* iff the verifier–human κ-gap's 95% CI upper bound is ≤ 0.10. Pre-registered criteria gate every claim: precision ≥ 0.85 and recall ≥ 0.80 on structural categories, an F1 margin ≥ 0.15 over intent-level categories, and budget-matched controls isolating constraint operationalizability from generic LLM capability.

(148 words. Opens with the asymmetry; verbs: formalize, measure, score, gate, isolate; no "increasingly used… however… we introduce.")
