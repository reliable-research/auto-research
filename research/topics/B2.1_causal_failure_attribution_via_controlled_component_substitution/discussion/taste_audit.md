# Research Taste Audit — B2.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "A wave of failure-attribution methods for multi-agent and tool-use systems has been proposed, but every one of them is validated against human-annotated or single-culprit blame labels rather than a known, injected causal ground truth — so a method can produce a plausible-looking blame assignment that is symptom-matching rather than causally correct, and no existing evaluation can currently tell the difference. Establishing whether 'failure follows the substituted component' is even a reliable premise is foundational: intervention-based auto-debugging and counterfactual label generation already lean on a version of this premise without measuring its reliability across a plan/tool/observation taxonomy."

**Method** (Stage 5, summary-level): "We checkpoint a reproducibly-succeeding tool-use agent run, inject exactly one fault (a corrupted plan step, a broken tool, or a polluted observation) while holding the other two pipeline components fixed, and replay k times; an outcome-flip gate certifies a trajectory's ground-truth failure-locus label only when the outcome flips against a matched no-op control, ruling out substitution-induced or stochastic false positives. We apply every candidate attribution method uniformly to every certified trajectory, score blame against the by-construction ground truth with a full confusion matrix, and add a budget-matched control that separates causal-intervention access from raw compute so an apparent method advantage cannot be explained by extra replay budget alone."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "validated against... labels rather than a known injected causal ground truth" / "no existing evaluation can currently tell the difference" — a diagnosability/measurement-absence claim ("hard to measure," "lacks diagnostics"), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "a method can produce a plausible-looking blame assignment that is symptom-matching rather than causally correct" — the worry that existing attribution tools may be unreliable in a specific, nameable way (symptom-matching passing as causal reasoning), not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0 (core asymmetry) and Step 3 (self-audit) independently already rejected a bridge reading — the initial risk they flagged and fixed was framing this as "port Defects4J to agents," which they explicitly corrected to lead with the domain-specific asymmetry (ground truth is manufacturable forward-only in this setting, not backward as in Defects4J) rather than a cross-domain connection.

**Method Paradigm:** primary **Artifact/System** (secondary: **Empirical Mapping**)
- rationale: the central deliverable named in both the motivation and the method sentence is a released, reusable resource — the certified fault corpus and the substitution harness that manufactures it (digest N12's own classification: `benchmark`, not `dataset` or `empirical` alone). "We checkpoint... inject... certify... apply... score" describes building and operating a concrete measurement instrument, not proving a theorem or reconciling two theories. The secondary Empirical Mapping reading comes from the method's second half — applying the instrument to characterize existing methods' accuracy — which is a demonstration of the artifact's value (per `paper.md` Step 2's own "Secondary: Empirical measurement (CO3)... a demonstration of the resource, not the headline"), not the headline contribution itself.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The method borrows individual plumbing pieces from prior work (AgenTracer's inject-and-replay trick, DoVer's checkpoint-and-edit mechanism, SelfEvolveBench's reproducibility gate), but the load-bearing mechanism — the outcome-flip *labeling invariant* (single injected fault ∧ observed outcome flip ∧ no-op control does not flip) — is not assembled by gluing two existing methods together with a connecting verb. No cited work defines or enforces this specific decision procedure (digest N4's own limitations confirm this: WhoAndWhen and DoVer validate against human agreement or argue the single-culprit assumption is weak, but neither manufactures a controlled, class-conditional ground truth).
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three fault classes, *which* certification gate (flip rate vs. a matched no-op control, not mere injection), *which* compute-parity control (a specific budget-matched judge variant), *which* scoring structure (class-conditional confusion matrix, not pooled accuracy alone). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "a wave of failure-attribution methods for multi-agent and tool-use systems has been proposed," which is a somewhat generic scene-setting sentence, but it still ties directly to a specific, checkable claim (every one of them validated against human/single-culprit labels) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **checkpoint, inject, hold fixed, certify, apply, score, isolate**. `certify` and `isolate` are in or adjacent to the human-heavy archetype cluster (with *decouple, separate, disentangle*, and the closely related family *expose, invert, recast*); `checkpoint`, `inject`, `apply`, `score` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (certify/isolate/inject/apply/score) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the single worst one.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuine, independently-arrived-at result, not a rubber stamp: `paper.md`'s Step 0 (核心问题's "asymmetry") and Step 3 (its own taste self-audit table) had *already* run an informal version of this check before this audit even started, and had already caught and corrected exactly the failure mode this skill is designed to catch — an early framing risk of "port Defects4J to agents" that reads as a textbook Bridge Opportunity, corrected in the seed material itself to lead with the domain-specific asymmetry instead. This audit, run independently with a different, externally-sourced taxonomy (not the same reasoning that wrote `paper.md`'s self-check), agrees with that correction and finds no further residual bridge-framing risk in the confirmed Stage 2/5 outputs.

One place worth flagging honestly rather than smoothing over: the Method Paradigm's primary label (**Artifact/System**) is a close call against **Empirical Mapping** — both are legitimately present, and a differently-worded method summary emphasizing the accuracy-measurement half first could plausibly flip which one reads as primary. This doesn't change the verdict (neither label is the flagged Synthesis/Unification cell, and the Opportunity axis is unambiguously not Bridge), but it is a genuine judgment call, not a clean-cut classification, and is reported as such rather than forced to look more decisive than it is.

**No reframe was performed** — the skill's Step 6 reframe pass is only triggered by a 🔴 or two-or-more 🟡 flags, and none fired here. The confirmed Stage 2/5 motivation and method are carried into the final paper draft unchanged by this audit.
