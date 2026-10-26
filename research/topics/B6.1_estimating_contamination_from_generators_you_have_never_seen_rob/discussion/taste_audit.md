# Research Taste Audit — B6.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Corpus-level contamination estimators are the practical instrument teams actually reach for when deciding how much of a corpus is synthetic and whether to filter or down-weight it — but their reliability has only ever been demonstrated against a fixed, known set of calibration generators, which is precisely the condition that fails to hold once a corpus is contaminated by generators the auditor never anticipated... a diagnosed degradation on its own does not tell a practitioner what to do next: it does not distinguish 'this is fixable' from 'this is structurally obstructed.'"

**Method** (Stage 5, summary-level): "We run leave-one-generator-out cross-validation crossed with a paraphrase-strength sweep to measure estimator degradation; contrast a quantification-corrected estimator against a naive one to isolate aggregation bias from base-classifier error; use a capability-matched seen/unseen swap on identical held-out documents to separate genuine unseen-ness from a generator's intrinsic detectability; fit a single joint mixed-effects specification to disentangle the generator-novelty and paraphrase-strength effects from each other; and apply a pre-committed cross-cell flatness-plus-floor test to certify (or rule out) a generator-invariant statistical feature."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "reliability has only ever been demonstrated against a fixed, known set of calibration generators" and "whether that same failure propagates to the aggregate, corpus-level estimators... has not been measured" — a diagnosability/measurement absence (no way to audit how an estimator behaves off-calibration), not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the fact that existing estimator validity is implicitly assumed only under the narrow regime (known generators, no paraphrase) it was calibrated on — exactly the "assumes X, does not transfer outside X" pattern.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0/Step 3 self-audit independently arrived at the same non-bridge framing and rejected a bridge reading before this audit was run.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we run... cross-validation crossed with a... sweep to measure... contrast... isolate... use a... swap to separate... fit a... specification to disentangle... apply a... test to certify" is characterization/measurement instrumentation — building the apparatus that makes a degradation rate and a feature-invariance verdict observable — not "integrate/unify" two existing methods into a new one. The secondary Formal Derivation reading comes from the invariance criterion itself (the flatness-test-plus-floor rule) being a conceptual/decision-rule contribution — a precise, falsifiable definition of what "generator-invariant" even means — not merely a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. Leave-one-generator-out cross-validation, quantification correction, and AUROC-based separability testing are each individually standard statistical tools, but no pair of them is glued together with a connecting verb to form "the method." The load-bearing new construct is the joint factorial design (generator × paraphrase, disentangled in one specification) plus the capability-matched swap plus the flatness-and-floor invariance criterion — all purpose-built for this specific degradation-and-existence question, not a merger of two pre-existing named methods.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* axis (generator identity vs. paraphrase strength $k$), *which* correction (prior-shift/adjusted-count quantification correction), *which* confound (unseen-ness vs. intrinsic per-generator difficulty, isolated by a specific matched-swap design), *which* invariance criterion (cross-cell flatness test AND a 0.70 floor, not just "still separable on average"). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "the practical instrument teams actually reach for," which is mildly generic framing language, but it still ties to a specific, checkable claim (estimators are used for filtering/down-weighting decisions) rather than being swappable filler that could describe any unrelated paper.

## 4. Dominant verb(s)

Method sentence's main verbs: **measure, contrast, isolate, separate, disentangle, certify**. `isolate`, `separate`, and `disentangle` are explicitly in the human-heavy archetype cluster per `archetype-verbs.md`. `measure`, `contrast`, and `certify` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/separate/disentangle/measure/contrast/certify) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started — it explicitly reasoned through "Bridge? ... PASS. Synthesis? ... PASS after centering the framing on the measured law. Load-bearing verbs: measure, isolate, gate, characterize, falsify — none from integrate/unify/leverage. PASS." This audit is independent confirmation using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's calibrated human/LLM corpus, not the same prompt logic that wrote `paper.md`), and it agrees on both the categorical labels and the verb-level check.

One place this audit adds information `paper.md`'s self-check didn't: it separately scores `bottleneck_specificity` and `boilerplate` against an external calibration (human baseline 2.56 / 0.48), rather than a binary self-assessment, and confirms the idea doesn't just avoid Bridge/Synthesis but also avoids the more common failure of a *technically-not-Bridge* idea that's still generic and hedgy at the sentence level (the condition-2 check). It passed that separately, which is worth stating plainly rather than treating the categorical PASS as sufficient on its own.

The practical implication for the rest of the batch: this specific pass (🟢, no manufactured flag) is a topic-specific result — the seed's already-mature Step-0/Step-3 self-audit made a flag less likely here, but it is not evidence that every other topic in this batch will pass automatically. The auditor is cheapest to run per topic, right after Stage 2/5 confirm, before committing to a full paper draft — which is exactly when it ran here.
