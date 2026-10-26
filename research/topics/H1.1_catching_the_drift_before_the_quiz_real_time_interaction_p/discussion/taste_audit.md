# Research Taste Audit — H1.1

> Skill: `research-taste-auditor` (taxonomy and calibration from Chen, Zhao & Cohan,
> arXiv:2607.01233). Run on the **confirmed Stage 2 (Motivation) + Stage 5 (Method) outputs**
> from `discussion_trace.md`, after the discussion loop closed and **before** paper assembly —
> catching a template-shaped idea is cheaper before drafting than after. Date: 2026-08-15.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed; condensed from its own summary sentence): "Skill erosion
under AI assistance is causally established and pattern-mediated, but every existing measurement
arrives after the fact; nobody knows how early the erosive patterns are visible in the behavior
stream — to humans or to any statistical procedure — so the drift can only be named after the
quiz, when nothing can be done about it, by which point measurement structurally favors the
vendor rather than the person incurring the invisible harm."

**Method** (Stage 5, confirmed; condensed from its own summary sentence): "We estimate a
calibrated prognostic risk — that a session, if uninterrupted, terminates in an erosive
pattern — from query-stream prefixes only; measure the human prefix-labeling ceiling that bounds
any such detector; convert risk into at most one timed alert per session via a first-crossing
trigger; gate any live intervention behind a sealed, prevalence-anchored exact-bound
authorization decision; and, if authorized, isolate the nudge's content effect from notification
reactivity with a matched placebo inside a four-arm trial that internally re-tests the published
hand-vs-AI gap."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the load-bearing claims are measurement absences — "every existing measurement
  arrives after the fact," "nobody knows how early the patterns are visible at all" — i.e., no
  way to measure/diagnose the thing at the moment it matters. The secondary Failure/Risk reading
  is licensed by "a harm invisible at decision time to the person incurring it" — an unreliability/
  harm framing about current practice, not a two-literatures framing.
- Explicitly **not** Bridge Opportunity: no "X and Y have developed in isolation" clause appears
  anywhere in the confirmed motivation. The JITAI and ITS literatures are *credited as
  precedents* ("we import the vocabulary rather than reinventing it") — the gap claimed is not
  "mHealth and developer tooling haven't been connected" but "no one can see this specific harm
  at prefix time." That distinction was enforced at Stage 2/3 (the closed-loop novelty claim is
  scoped to sensor + outcome, precisely to avoid the loop-concept overclaim).

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "estimate … measure the ceiling … characterize precision at prefix lengths …
  estimate the causal effect" is systematic measurement and characterization — the classifier and
  nudge are instruments of the measurement, not products pitched against baselines (Stage 1's
  `study_type: empirical` and the zero-outcome-tier RQ audit encode this). The secondary Formal
  Derivation reading comes from the sealed decision-analytic gate: a pre-registered,
  prevalence-anchored authorization *rule* (exact bound + alert minimum + annoyance budget) is a
  decision-procedure contribution, not a measurement per se.

## 3. Diagnostics

- `surface_stitching` = **1** — there is one imported template (the JITAI loop shape:
  tailoring variable, decision points, proximal/distal outcomes), and the write-up says so
  openly. But real, purpose-built mechanism sits between the parts: the prognostic reframing of
  hindsight labels, the human prefix ceiling as denominator, the first-crossing trigger with
  pre-notification risk freezing, and the sealed prevalence-anchored gate are none of them
  "glue" — each answers a named sub-problem. Not a 0 because the loop template is genuinely
  inherited; not a 2 because the new mechanism is where the paper lives.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which*
  asymmetry (labels are hindsight summaries of complete sessions; decisions must be made at
  prefix time), *which* quantity (P(terminates erosive | first k queries)), *which* bound (the
  human prefix ceiling), *which* authorization criterion (CP 90% LB ≥ prevalence + 0.10, ≥5
  alerts, FPB ≤ 0.3), *which* confound the placebo removes (notification reactivity). At or
  above the human calibration mean (2.56).
- `boilerplate` = **1** — mostly load-bearing; the one soft patch is the normative-urgency
  phrasing ("measurement structurally favors the vendor," "accountability instrument"), which
  edges toward AI-governance stock language but remains tied to a checkable property (prefix-only
  features deployable without model access). Watch this leg in the FAccT position form, where the
  temptation to inflate it into generic AI-harms framing will be strongest.

## 4. Dominant verb(s)

Method-summary main verbs: **estimate, measure, gate, isolate, re-test** (with *freeze/seal* and
*trigger* as supporting operations). `isolate` and `decouple`-family verbs are in the human-heavy
cluster; `estimate/measure/gate` are neutral, task-specific verbs. No *integrate / unify / merge /
combine / leverage / bridge* appears in claim position in either extracted sentence. The one
place a connecting verb appears in the wider Stage-2 text is "we import the vocabulary" —
which is a crediting move about prior work, not the method's own claim verb.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** (Evidence Gap × Empirical Mapping) |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant method verb from the LLM-heavy archetype list | **No** (estimate/measure/gate/isolate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. This is an honest pass, not a
manufactured one — and it is worth recording *why* it passes, because the idea contains exactly
the ingredient that usually gets flagged: a cross-domain transplant (the JITAI closed loop into
AI-assisted skill formation). Per the auditor's own cross-domain-transfer note, such a move reads
as Bridge/Synthesis only when written as "connecting the two literatures"; here it is written as
a *credited inheritance plus a named insufficiency* ("no JITAI work senses AI-interaction
patterns or targets skill formation; the labels that exist are hindsight-only; we estimate the
prefix-time risk those labels cannot give"), which keeps the opportunity on Evidence Gap and the
method on Empirical Mapping. The framing discipline that produced this came from the earlier
critic rounds (discussion.md Stage 2 critic (c) explicitly killed the "nobody owns the closed
loop" overclaim), and this audit independently confirms the result with an external taxonomy.

## 6. Regression watch (for later passes)

Two places where redrafting could re-introduce the flagged shape, checked again at any future
re-audit: (a) the FAccT position form's normative leg drifting into generic AI-harms boilerplate
(boilerplate → 2); (b) any abstract rewrite that leads with "we bring just-in-time adaptive
interventions to AI-assisted programming" (Bridge/Synthesis phrasing for what is currently an
Evidence-Gap/Empirical-Mapping claim). Neither is present in the confirmed outputs or the
assembled draft.
