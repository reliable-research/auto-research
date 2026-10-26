# Research Taste Audit — B3.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Production software increasingly delegates structured-output correctness — the thing downstream code actually parses — to a model version the contract owner cannot pin or fully observe, and provider-side model upgrades are frequent and only loosely documented, but how much of this contracted behavior actually survives a version jump has never been directly measured... a single pooled rate is not actionable by itself: a team cannot decide which of their contracts to re-test without knowing which contract-level features predict fragility, and whether measured breakage is inherent or avoidable changes what a team should actually do about it."

**Method** (Stage 5, summary-level): "We build a three-tier deterministic contract validator calibrated against hand labels, execute a stratified contract library against pinned successive model versions with a canary to detect closed-endpoint addressability failure, compute breakage only as an excess over a within-version split-half noise floor, fit a mixed-effects fragility model over pre-registered contract features, compare its predictive power head-to-head against a cheap distribution-shift detector to rule out generic causal confounds, and bound how much of the measured breakage two existing mitigations (grammar-constrained decoding, per-version prompt recompilation) remove, tier by tier."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "has never been directly measured" / "no paper... directly measures per-version-upgrade breakage rates" (digest N3 absence_comment) — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the CoIPO/TARE limitation this idea explicitly names: existing input-side robustness work "assumes" the model is fixed and only the prompt varies — the exact narrow regime this paper's setting (prompt fixed, model varies) falls outside of.
- Explicitly **not** Bridge Opportunity: there is no "endpoint-drift detection and downstream contracts have developed in isolation, we connect them" clause anywhere in the motivation; `paper.md`'s own Step 0/Step 3 independently pre-empted exactly this framing and rejected it ("Risk: framing as 'we connect endpoint-drift detection to downstream contracts.' Fails if framed that way").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Robustification**)
- rationale: "we build... execute... compute... fit... compare... bound" is characterization/measurement instrumentation — "we measure/quantify/characterize" is exactly the Empirical Mapping trigger cluster. The secondary Robustification reading comes from the mitigation-headroom arm (`m_mitigation_headroom_bound`): the paper does evaluate whether existing techniques reduce failure, though as a *measurement of headroom*, not as a newly proposed mitigation being sold as the contribution.

## 3. Diagnostics

- `surface_stitching` = **1** — not a "textbook A+B": no single pair of pre-existing methods is glued with a connecting verb to produce "the method." But several individual components genuinely reuse existing machinery as stated components (AutoIF/IFEval-style validators, a LogProbTracking-style canary and cheap-signal comparator, a DiffusionCFG-lineage decoding constraint, DSPy-style recompilation) rather than one purpose-built end-to-end apparatus. The real mechanism linking these reused parts — the split-half noise floor as the null every breakage claim is tested against, plus the tier-decomposed mitigation-attribution design — is genuinely new, which is why this isn't a 2 or 3: the paper's own Step 3 self-audit already names this honestly ("the only methodological novelty is the split-half within-version noise floor... reused components are stated as reused"), and that audit is corroborated here rather than contradicted.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three validator tiers, *which* specific noise-floor construction (split-half, identical procedure), *which* seven named features, *which* two mitigation arms and what each tier-decomposed comparison isolates. Matches the source paper's strong-model band (2.3–2.6) and exceeds the human baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "production software increasingly embeds LLM calls behind structured-output contracts," a somewhat generic scene-setting sentence, but it still ties to a specific claim (a contract owner cannot pin or observe the model version) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, execute, compute, fit, compare, bound**. `bound` and `isolate`-family reasoning (the cheap-signal "rule out generic causal confounds" move) sit in or adjacent to the human-heavy archetype cluster (with *decouple, separate, isolate*); `compute`, `fit`, and `compare` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (build/compute/fit/compare/bound) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. Note this is a slightly less pristine pass than a hypothetical 0/0/3 profile — `surface_stitching = 1` is a genuine, non-zero score, honestly reported rather than rounded down, because several components really are reused off-the-shelf machinery. It still clears the threshold (the condition requires ≥2), and the paper's own Step-3 self-audit already disclosed this reuse rather than dressing it up as novel algorithmic contribution — which is precisely the behavior that keeps a partly-reused method from reading as a disguised A+B stitch.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: `paper.md` Step 0/Step 3 had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started (explicitly naming and rejecting the "we connect drift-detection to downstream contracts" bridge framing). This audit is independent confirmation using a different, externally-sourced taxonomy, and it agrees — while also surfacing one honest wrinkle (`surface_stitching = 1`, not 0) that the seed's own self-audit didn't quantify.

The practical implication for the wider topic set: this pass being 🟢 does not mean every empirical-measurement topic in this collection will pass automatically — a paper that leans more heavily on off-the-shelf validators/monitors without a genuinely new null-model or attribution design (the thing that kept `surface_stitching` from crossing to 2) would land closer to the flagged zone. The auditor is cheapest to run **per topic, right after Stage 2/5 confirm**, before committing to a full draft — which is exactly when it ran here.
