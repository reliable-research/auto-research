# Research Taste Audit — B1.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Coding agents are increasingly gated, trained, and benchmarked using a visible test suite as the sole verifier of task success, but whether — and at what point — an inadequate visible suite starts rewarding agents for gaming it rather than fixing the underlying defect has never been directly measured as a function of the suite's own fault-detection adequacy... a targeted corpus search across three independent keyword angles found no paper that treats this adequacy score as a controlled independent variable against agent behavior... the raw gap alone cannot distinguish two remediation stories that call for entirely different fixes: honest-but-incomplete repairs under a weaker suite call for a better test suite, while patches that specifically special-case the visible assertions call for anti-gaming safeguards — a distinction invisible to any metric that reports the gap's size without also attributing individual patches to one story or the other."

**Method** (Stage 5, summary-level): "We construct visible sub-suites at controlled mutation-kill adequacy while holding suite size and coverage fixed, fit a mixed-effects trend model that separates a genuine adequacy-driven gap from ordinary sampling noise, compare a segmented against a smooth model of the resulting curve to determine whether any onset is sharp or gradual, run a differential-testing diagnostic that attributes individual visible-pass/held-out-fail patches to gaming versus coincidental incompleteness, replicate the sweep across multiple agent families to test whether any threshold transfers, and isolate agent-side adaptive exploitation from a purely mechanical imperfect-verifier selection effect via a budget-matched, feedback-free control arm."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "has never been directly measured" / "a targeted corpus search... found no paper that treats this adequacy score as a controlled independent variable" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "starts rewarding agents for gaming it" — the worry that an existing verification mechanism (the visible test suite) may be unreliable under optimization pressure, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the confirmed motivation. This is not an accident — paper.md's own Step 3 self-audit already caught exactly this failure mode in an earlier draft contribution (CO4, "a transplant... bridging the imperfect-verifier and reward-over-optimization literatures") and explicitly demoted it from the contribution slot to related-work positioning before this audit ran. This audit independently confirms that fix held: the confirmed Stage 2 motivation never reintroduced bridge language.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "construct... fit... compare... run... replicate... isolate" is characterization/measurement instrumentation — building a controlled sweep and reading off its shape — not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the segmented-vs-smooth model-comparison decision procedure and the differential-testing gaming/coincidental criterion themselves being conceptual, decision-rule contributions (an operational definition of "onset" and of "gaming"), not just a measurement pipeline with no new construct.

## 3. Diagnostics

- `surface_stitching` = **1** — not a textbook "A + B" combination (there is no pair of pre-existing methods glued with a connecting verb), but several of the individual instruments (mixed-effects logistic regression, changepoint/Davies-test model comparison, differential/metamorphic testing) are standard statistical or SE tools applied here, not invented from scratch. What is new is the specific construction that links them — adequacy-controlled sub-suite sampling as the swept variable, and the gaming-vs-coincidental decision procedure built on top of it — so this is honestly scored a 1 ("some combination, but a real mechanism links the parts"), not a reflexive 0.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* scalar (mutation-kill score, with equivalent mutants filtered from the denominator), *which* model comparison (segmented vs. smooth GAM, ΔAIC ≥ 10 and a corrected Davies test), *which* behavioral signature for gaming (agreement inside the visible sub-suite's exercised inputs, ≥30% disagreement in a metamorphic neighborhood just outside it), and *which* control isolates the causal question (budget-matched, feedback-free best-of-k). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "coding agents are increasingly gated, trained, and benchmarked using a visible test suite," which is somewhat generic framing language, but it still ties to a specific claim (the suite is the *sole* verifier of task success, which is exactly the premise the paper's asymmetry argument needs) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **construct, fit, compare, run, replicate, isolate**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `compare` functions the same way here (a model-comparison decision procedure, not a connecting move); `construct`, `fit`, `run`, `replicate` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge* appears in a claim position anywhere in the extracted idea — and the pipeline log confirms these verbs were explicitly banned from abstract/intro language by paper.md's own Step 3 self-audit, a constraint honored throughout stages 1–6 above.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/compare/construct/fit/run/replicate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks, including an honest (not maximally generous) `surface_stitching` score of 1 rather than a reflexive 0.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp, for a specific reason visible directly in the source material: an *earlier* draft of this exact idea's own contribution list (paper.md Step 0, contribution CO4) did land in Bridge-Opportunity language — "a transplant of classical mutation-testing adequacy theory onto LLM coding-agent evaluation, bridging the imperfect-verifier and reward-over-optimization literatures" — and paper.md's own Step 3 self-audit caught it, demoted CO4 out of the headline contribution slot, and restated the opportunity as the Step-0 asymmetry (the exploitable slack is constructible and controllable via mutation testing, not merely "two things that haven't been connected"). This audit, run independently on the confirmed Stage 2/5 outputs using a different, externally sourced taxonomy (not the same self-audit logic that produced paper.md's Step 3), confirms that fix held all the way through the six-stage discussion loop: nothing in the confirmed motivation or method reintroduced bridge/synthesis framing.

The practical implication for the broader topic set: this specific pass (🟢, with an honestly non-maximal `surface_stitching` score) should not be read as "any idea that reuses standard statistical machinery automatically passes." What kept this idea off the flagged cell was not the absence of reused tools (mixed-effects models and changepoint tests are, in fact, reused off-the-shelf) but the presence of a specific, nameable construction — mutation-kill adequacy as a controlled independent variable, and a falsifiable behavioral signature for "gaming" — that those tools are applied *to*, rather than a generic "combine tool A and tool B" framing. That distinction is exactly what `bottleneck_specificity` is designed to surface, and it is why this idea scores a 3 there even with a non-zero stitching score.
