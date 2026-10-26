# Research Taste Audit — T3.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "If deployed LLM agents' soft organizational policies decay dramatically faster than hard safety norms, but nobody knows whether that is because soft policies are less salient in context, worded more weakly, or simply lack the deep alignment-training reinforcement that hard norms have, then any attempt to fix the gap is guesswork — and the guess can be wrong in an expensive direction. ...if a nonzero residual survives even after matching a soft policy's presentation to a hard norm's, that residual is evidence that training-time reinforcement — not prompt engineering — is required."

**Method** (Stage 5, summary-level): "We construct content-matched soft/hard constraint pairs, orthogonally manipulate wording strength, context position, and repetition count while proxying the unmanipulable alignment prior with a triangulated covariate battery, decompose the resulting type×turn decay-gap coefficient via a dominance/partial-R² analysis of one fitted hazard model, test whether a maximally boosted soft-policy presentation closes the gap at a specific pre-registered contrast cell, and calibrate probe-induced measurement reactivity via a within-/between-conversation equivalence test."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Explanation Gap** (secondary: **Evidence Gap**)
- rationale: the motivation's load-bearing claim is "nobody knows whether that is because..." — a phenomenon (the ~8x decay-rate gap) is taken as given and the claim is that no one has a causal/mechanistic account of *why* it happens. That is the textbook Explanation-Gap trigger ("it remains unclear why"), not a "two literatures never connected" framing. The secondary Evidence-Gap reading is licensed by digest N3's own absence_comment — "no corpus paper runs the salience/framing/prior ablation together" — a genuine measurement-absence claim, not a bridge claim.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the confirmed motivation. `paper.md`'s own Step 0 arrived at the same asymmetry framing independently (its own deletion-test judges the claim as "not a bridge... one confounded quantity is being split into separable causes"), and its Step 3 self-audit explicitly checked and rejected the Bridge label before this audit ever ran.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we construct... manipulate... proxy... decompose... test... calibrate" is characterization/measurement instrumentation applied to an existing phenomenon, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the matched-pair definition and the dominance/partial-R² decomposition criterion themselves being conceptual, decision-rule-like contributions (a precise operational definition of "matched," a precise operational definition of "closes the gap"), not just a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **1** — `paper.md`'s own Step 3 self-audit already names and defuses the real risk here: a naive framing would read "we combine PrefEval's padding protocol, TimeToInconsistency's survival modeling, and RECAST's verifier taxonomy," which *is* textbook A+B+C stitching. The confirmed Stage 5 draft doesn't lead with that — it leads with the matched-pair audit, the orthogonal-crossing design, the proxy triangulation, and the reactivity calibration as the load-bearing mechanism, with the borrowed instrumentation reused but not the headline move. Scored 1, not 0, because the reliance on borrowed instrumentation (survival-modeling machinery, a verifier taxonomy, a padding protocol) is real and more substantial here than a purpose-built-from-scratch instrument would be — this is the more marginal of the two diagnostics relative to the calibration exemplar, worth flagging honestly rather than rounding down to a clean 0.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three factors (wording level, position, repetition count) cross *which* fixed coefficient (`type×turn`), *which* three named proxies (no-injection compliance, base-vs-instruct delta, per-token KL), and *which* specific calibration contrast (within- vs. between-conversation probing, equivalence-tested against a named bound). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "any attempt to fix the gap is guesswork," a slightly generic-sounding motivational flourish — but even that clause is anchored to a specific, real, binary practical bifurcation (a placement/wording fix vs. a training-time fix) rather than being swappable filler that could describe any other paper.

## 4. Dominant verb(s)

Method sentence's main verbs: **construct, manipulate, proxy, decompose, test, calibrate**. None of these is on the LLM-heavy list (integrate, unify, merge, adapt, combine, leverage). `decompose` and `calibrate` function structurally like the human-heavy cluster's *separate/isolate* (splitting a confounded quantity into independently-attributable shares is the same move as "isolate," just applied to a statistical coefficient rather than a physical component); `construct`, `proxy`, and `test` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral** (leaning human-heavy via `decompose` ≈ `separate`).

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (construct/decompose/calibrate/test) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the worst one.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp, and it is worth being honest that it is a *slightly less clean* pass than some other topics in this set: `surface_stitching` scored 1, not 0, because this idea's instrumentation really does lean on three borrowed components (a padding protocol, a survival-modeling framework, a verifier taxonomy) more heavily than a purpose-built-from-scratch measurement instrument would. The reason the verdict still lands clean is that `paper.md`'s own Step 3 self-audit already identified exactly this risk before this audit ran, and pre-committed to framing the contribution as "the causal isolation design + the attribution result," not "we combine X, Y, and Z" — a discipline the confirmed Stage 5 method output preserves.

The practical implication: this pass should not be read as evidence that borrowing established instrumentation is automatically safe — it is safe *here* specifically because the borrowed pieces are demoted to commodity infrastructure and the load-bearing claim (the matched-pair audit, the orthogonal decomposition, the boosted-cell contrast, the reactivity calibration) is genuinely novel to this design. If the eventual Related Work or Method prose ever drifts toward "we combine PrefEval's protocol and TimeToInconsistency's model" as the *headline* framing rather than background infrastructure, that drift alone would be enough to push `surface_stitching` from 1 to 2 and flip the verdict to 🟡 — worth a second look at draft time, not just at this audit's single pass.
