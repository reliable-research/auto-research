# Research Taste Audit — B6.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Treating pre-2022 human text as a costless, self-certifying negative anchor is now load-bearing for an entire emerging research line — corpus-level AI-content prevalence estimation — precisely because it lets researchers avoid per-document ground truth; but if that anchor's implied error guarantee quietly decays with the ordinary passage of time, every downstream prevalence estimate built on it inherits an unstated and directional bias. ... its validity is asserted by convention ..., never measured."

**Method** (Stage 5, summary-level): "We construct a year-stratified corpus of certified pre-2022 human text, run a battery of existing detectors and a mixture-based prevalence estimator across it, and disentangle any observed false-positive-rate drift among three rival mechanisms — genuine stylistic drift, composition confound, and content leakage/estimator staleness — using controls each immune to exactly one alternative (a leakage-immune pre-2018 sub-range, a composition-matched resample, synthetic-drift injection); we bound the anchor's own residual impurity rather than assume it away; we measure how much this drift actually shifts a downstream corpus-level prevalence estimate by swapping the reference age directly; and we define the resulting validity envelope from a confidence bound rather than a raw significance threshold, so 'under-sampled' and 'genuinely safe' are never conflated."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "its validity is asserted by convention..., never measured" — a diagnosability/measurement absence about an existing, in-use methodological convention, not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the convention's implicit assumption that "pre-2022 = clean forever" — an untested claim that the anchor's guarantee holds under an idealized temporal-stationarity regime that may not transfer to the full historical range it is actually applied over.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0/Step 3 already ran this exact self-check ("the sentence has no generic truth value once the nouns are removed... it names one object whose two properties are forced apart by one mechanism") and rejected a bridge reading independently, before this audit began.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we construct... run... disentangle... bound... measure... define" is characterization/measurement instrumentation of an existing convention, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the confidence-bound validity envelope itself being a conceptual/decision-rule contribution (a formal object, `E_k(ε,δ)`), not just a measurement pipeline — mirroring how a three-conjunct criterion can be both a measurement device and a definitional one.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued. The instrument (disentanglement controls, purity bounding, composition-matched resampling, reference-swap propagation test, confidence-bound envelope) is purpose-built for auditing this specific convention's temporal validity — the existing detectors are used as instruments *inside* the design, not combined with each other as the contribution itself.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three rival mechanisms (style, composition, leakage/staleness), *which* specific sub-range is leakage-immune (≤2018), *which* estimator's reference is swapped and how (MonitorAIScale, holding the target fixed), *which* two envelope constructions are being compared (naive significance threshold vs. confidence-bound tolerance). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "an entire emerging research line," which is slightly generic scale-of-stakes language but still anchors to a specific claim (the mixture-estimation reframing) rather than being swappable filler that could describe any AI-safety topic.

## 4. Dominant verb(s)

Method sentence's main verbs: **construct, disentangle, bound, swap, define**. `disentangle` is explicitly in the human-heavy archetype cluster (with *decouple, separate, isolate*); `bound` and `swap` are neutral, task-specific verbs pointing at a precise operation, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (disentangle/bound/swap/construct/define) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and its own "deletion test" ("delete the domain nouns... the residue is unevaluable") is a genuinely sharper self-check than most seeds in this set carry. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees.

Worth flagging honestly rather than glossing over: this topic's core method leans heavily on the same rhetorical moves (disentangle, isolate, bound) that scored well for the B5.5 exemplar too — that consistency is expected, not suspicious, since both topics were generated from the same reverse-digest process that explicitly optimizes against the Bridge+Synthesis template at generation time (see `paper.md` Step 3 in both topics). The genuinely load-bearing check here was not "does it use the right verbs" (that was close to guaranteed given how the seed was written) but whether the *specificity* score held up independently — and it does: every rival mechanism, every control, and every construct in the method sentence names a precise, checkable target rather than a generic "we carefully account for confounds" gesture. The practical implication for the other topics in this set: a topic whose seed was generated with a weaker Step-0/Step-3 self-audit could still fail this independent check even while using superficially similar verbs, so this pass is worth running per-topic rather than assumed from one clean result elsewhere in the set.
