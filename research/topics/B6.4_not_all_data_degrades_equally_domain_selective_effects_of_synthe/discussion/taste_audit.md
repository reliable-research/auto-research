# Research Taste Audit — B6.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed, post-tightening — see note in Section 6): "Downstream capability damage from synthetic contamination is plausibly not a property of the corpus as a whole but of the domain it lands in — domains with mechanically verifiable correctness structure (code, mathematics) may convert a subtly wrong synthetic document into corrupted supervision, while style-tolerant domains (prose, dialogue) may absorb the same dose as benign variation — and no existing framework can currently tell a practitioner whether this asymmetry is real... The two adjacent literatures matter only as evidence that this asymmetry is currently unmeasurable, not as the motivation itself: model-collapse theory's global mixing-ratio abstraction has no domain axis to express it with, and data-mixture optimization's domain axis is assumed clean, never contaminated."

**Method** (Stage 5, summary-level): "We isolate syntheticness from co-occurring textual degeneracy with a degeneracy-matched real-text control arm; we normalize capability damage across four domains with incommensurable ground-truth structures using a dual (benchmark-metric and validation-loss) normalization inside one mixed-effects model; we characterize dose-response shape and test cross-scale rank-stability with a staged ratio/scale design that concentrates scarce large-scale compute on the two most informative ratio extremes; and we rule out a generator-specific artifact by requiring the resulting ranking to replicate under a second, independently-sourced contamination generator."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "no existing framework can currently tell a practitioner whether this asymmetry is real" — a measurement/diagnosability absence, not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the explicit follow-on clause naming *why* it's unmeasurable: model-collapse theory's mixing-ratio abstraction has no domain axis, and data-mixture optimization's domain axis is assumed clean — both are narrow-assumption failures of existing frameworks, not a claim that the frameworks should be linked.
- Explicitly **not** Bridge Opportunity: there is no "let's connect/integrate these two literatures" clause. `paper.md`'s own Step 0/Step 3 independently ran the identical self-check and explicitly rejected an earlier bridge-shaped draft of this same motivation (digest N2-Item2's "crossing the contamination axis with the domain axis is the natural but missing experiment" — flagged and fixed in `paper.md` before this pipeline run even started). See Section 6 for a related phrasing risk this audit caught independently.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Robustification**)
- rationale: "we isolate... we normalize... we characterize... we rule out" is measurement instrumentation and characterization, not "integrate/unify" two existing methods. The secondary Robustification reading comes from three of the four methods existing specifically to harden the central measurement against a named confound (degeneracy, generator identity, scale) rather than to produce the measurement itself.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together. Each of the four methods (degeneracy-matched control, dual normalization, staged dose-response/scale design, cross-generator replication) is a purpose-built instrument for one named confound.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* two normalizations, *which* control arm and *what* it's matched on, *which* two ratio extremes and *why* those specifically, *which* two generator properties (family, quality tier) must differ for replication to mean anything. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft phrase is "no existing framework can currently tell a practitioner whether this asymmetry is real," which is a fairly standard evidence-gap construction but still ties to a specific, nameable absence (no domain axis in either literature) rather than being generic filler swappable into another paper.

## 4. Dominant verb(s)

Method sentence's main verbs: **isolate, normalize, characterize, rule out**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `normalize`, `characterize`, and `rule out` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/normalize/characterize/rule out) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

Two things are worth being honest about rather than glossing over.

First, this idea's low bridge-risk is not an accident of this audit alone: `paper.md`'s own Step 0 (asymmetry derivation) and Step 3 (an explicit "taste self-audit" table) had *already* caught and fixed a bridge-shaped draft of this exact motivation earlier in the seed's own history — digest N2's second motivation item ("crossing the contamination axis with the domain axis is the natural but missing experiment") is precisely the Bridge Opportunity template, and `paper.md` explicitly names it as failing its own deletion test before replacing it with the correctness-strictness asymmetry used here. This audit is independent confirmation using a different, externally-sourced taxonomy — not the same prompt logic that wrote `paper.md` — and it agrees with `paper.md`'s own fix.

Second — and this is the part a rubber-stamped audit would have missed — the Stage 2 draft produced fresh during *this* pipeline run (before this audit) had partially regressed toward the same bridge-adjacent phrasing the seed material had already rejected: its `summary` field opened with "Model-collapse theory and data-mixture optimization each independently assume away exactly the variable this problem needs," which reads close to a "two literatures, neither..." construction even though the accompanying `why_it_matters` field correctly led with the asymmetry. This did not formally cross the verdict thresholds above (Method Paradigm is not Synthesis/Unification, so condition 1 cannot fire regardless of the Opportunity label; the dominant verbs are still human-heavy), so this is reported as an **honest 🟢, not a manufactured flag** — but the `summary` field was proactively tightened in `pipeline.md` (see Stage 2, confirmed output) to lead with the asymmetry claim directly and demote the two-literatures comparison to supporting evidence, matching `paper.md`'s own already-established discipline rather than drifting back toward the pattern it had rejected. This is exactly the kind of check that's cheap to run per-topic right after Stage 2/5 confirm, before a full paper draft is written around a phrasing choice nobody re-examined.
