# Research Taste Audit — B2.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Failure attribution for LLM-agent pipelines... is now a benchmarked, seemingly mature capability, but every one of these frameworks validates its labels inside one fixed execution stack, so a label that looks like a property of the failure itself (which layer broke) may actually be a property of the particular backbone that produced and judged the trace... a single low agreement number is actionable in only one blunt way... decomposing the instability turns an abandon-ship finding into an actionable one."

**Method** (Stage 5, summary-level): "We run an identical fault-injection suite through several LLM backbones, hold the injected ground-truth layer fixed, and measure whether a fixed attribution procedure's label survives the swap. We gate every agreement statistic on the failure-overlap rate rather than reporting it blind, cross vendor-disjoint judge backbones with agent backbones to decompose instability into agent- and judge-driven shares, isolate the surface-style share via content/order-preserving normalization, expose the ground-truth-accuracy signature (agree-wrong) that agreement alone cannot show, and test whether residual instability is structured by model family and capability tier."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is that no one has *checked* whether attribution labels survive a backbone swap — "validates its labels inside one fixed execution stack" is a measurement/diagnosability absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the motivation's stakes clause: teams "trust diagnostic tooling" built on one backbone, and if that trust is misplaced the downstream routing decisions it drives are wrong — a reliability risk in an operational governance mechanism, not merely an unmeasured quantity.
- Explicitly **not** Bridge Opportunity: there is no "attribution research and multi-backbone evaluation have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0/Step 3 self-audit independently reached the same conclusion — the asymmetry is that a label *claims* an invariance (task property) its measurement pipeline never established, which is an internal contradiction within the attribution literature's own claims, not a gap between two separate literatures.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "run... measure... gate... cross... isolate... test" is characterization/measurement instrumentation — the central deliverable is a measured agreement quantity with an interpretation rule, not a new algorithm competing on a leaderboard. The secondary Formal Derivation reading comes from the censoring accounting (failure-overlap rate as a first-class quantity with a pre-committed metric-promotion rule) and the variance-decomposition definitions themselves being a conceptual/measurement-theoretic contribution — a way of *defining* what "stable," "model-specific," and "separable" mean operationally — not just a pipeline that produces a number.

## 3. Diagnostics

- `surface_stitching` = **1** — this is the one place this audit's independent scoring diverges from `paper.md`'s own Step 3 self-audit (which claims a clean pass with no stitching at all). Being honest about it: the design does explicitly reuse AgenTracer's injection-into-successful-traces logic and Who&When's judging protocols (all-at-once / step-by-step) as base instruments — a real "borrow A's component + B's component" element exists at the instrument level. What keeps this from scoring higher is that a genuine new mechanism sits on top and does the actual explanatory work: the censoring-aware metric-promotion rule, the judge×agent factorial, the style-normalization arm, and the agree-wrong accuracy check are not present in either source paper and are what the paper's claims actually rest on. Score reflects real (if secondary) combination, not zero.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* statistic is primary under *which* overlap threshold, *which* three judges cross *which* backbones, *which* normalization arm isolates *which* confound, *which* joint outcome cell (agree-wrong) is being exposed. Matches or exceeds the human baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "practitioners routinely swap the underlying LLM... for cost, latency, or a capability upgrade," which is somewhat generic industry-motivation language but still anchors a specific, checkable claim (attribution validity does not transfer across that swap) rather than being freely swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **gate, cross, isolate, expose, decompose**. `isolate` and `decompose` sit in the human-heavy/neutral cluster (with *separate, disentangle*); `gate` and `expose` are neutral, task-specific verbs tied to a specific mechanism (the overlap-rate gate, the agree-wrong exposure), not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge* appears in a claim-bearing position anywhere in the extracted idea — the closest near-miss is "cross" in "cross vendor-disjoint judge backbones with agent backbones," which is the standard statistical-design sense of a crossed factorial, not a Bridge/Synthesis connecting move.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (gate/cross/isolate/expose/decompose) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. Note the one deliberate departure from a rubber-stamp: `surface_stitching` is scored 1, not 0, because the design genuinely does reuse two prior papers' instruments (AgenTracer's injection logic, Who&When's judging protocols) rather than building every component from scratch — that reuse is honestly disclosed rather than hidden, and it is still far from the "textbook A+B, nothing else added" pattern that would score a 3.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is an independently-derived result, not a copy of `paper.md`'s own Step 3 self-audit: this audit used a different, externally-sourced taxonomy (Chen, Zhao & Cohan's opportunity/method axes and archetype-verb data) rather than `paper.md`'s domain-noun-deletion test, and it agrees on the headline verdict (🟢) while disagreeing on one sub-score (`surface_stitching`). That disagreement is itself informative: `paper.md`'s Step 3 audit is right that the paper's *contribution* is not a stitched-together method, but it slightly overstates the case by implying zero reuse of prior instruments. The honest reading is that reuse of AgenTracer's/Who&When's machinery is real but secondary — the load-bearing novelty is the measurement obligations built around that machinery (censoring accounting, factorial decomposition, style isolation, ground-truth-accuracy exposure), which is exactly what keeps the idea off the Bridge+Synthesis cell despite the partial component reuse.

The practical implication for the wider 39-topic set: a 🟢 verdict here should not be read as evidence that scoring is being softened to always pass — this run explicitly logged a lower `surface_stitching` score than the seed's own self-audit claimed, which is the kind of genuine independent check the auditor is supposed to provide rather than a second rubber stamp on an already-confident `paper.md`.
