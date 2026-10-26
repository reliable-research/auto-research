# Research Taste Audit — B4.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "A growing family of test-time stopping mechanisms for LLM reasoning — confidence-based early exit, verifier-based trimming, agreement-threshold adaptive sampling — is evaluated only by end accuracy and token savings, never by how far each one falls short of the best a deployer could achieve if the future were known; without that distance, nobody can say how much headroom is actually left to capture. ... a single aggregate number is not enough, because which rule looks best can flip with the deployer's own exchange rate."

**Method** (Stage 5, summary-level): "We build a checkpoint-probing instrument that reconstructs a per-instance oracle stopping point offline (and certifies its own reconstruction noise), decompose regret into stop-too-early/stop-too-late mass to localize exactly where each online signal decouples from correctness, fit a learned estimator over the running signal history to track the resulting non-stationary, sign-changing marginal utility, sweep the accuracy–compute exchange rate to test whether rule rankings are stable, and isolate genuine mid-trajectory value from pre-decoding difficulty prediction with a capacity-matched control."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "evaluated only by end accuracy and token savings, never by how far each one falls short of ... if the future were known" — a diagnosability/measurement absence (no instrument exists to compute the quantity that would settle the question), not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the observation that existing rules are validated at one implicit operating point (one λ, no oracle reference) and the claim that conclusions drawn there may not hold more broadly (the λ-sensitivity argument).
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0/Step 3 independently ran a deletion test on exactly this question before this audit started and rejected a bridge reading; this audit is an independent check using a different taxonomy, not a rubber stamp of that prior self-check.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build an instrument... reconstruct... decompose... sweep... isolate" is characterization/measurement instrumentation, not "integrate/unify" two existing methods — none of the five methods glues two prior systems together (the rule bank re-implements existing heuristics only as *measured conditions*, per `paper.md`'s own Step 3 note, never as a component being fused into something new). The secondary Formal Derivation reading comes from the regret/utility formalization itself (U_λ(k), t*(x,λ), R_λ(r,x)) being a conceptual contribution in its own right — a definitional apparatus other papers could adopt, not just a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued into a named result. The instrument (checkpoint probing, oracle reconstruction, regret decomposition, λ-sweep, pre-decoding control) is purpose-built for this identifiability problem, and the rule bank (DEER-style, TrimR-style, etc.) is explicitly a *measured condition*, not a component being combined into the contribution.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* checkpoints (reasoning-transition markers), *which* formula (U_λ = â_k − λ·c_k), *which* three signals, *which* exact rival explanation is being ruled out (pre-decoding difficulty prediction) and by *which* exact control (capacity-matched, token-matched prefix-only predictor). This matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6) — closer to `paper.md`'s own Step 5 table, which converts every load-bearing adjective in the claims ("online," "informative," "decouple," "overthinking") into an explicit computable quantity.
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "a growing family of test-time stopping mechanisms," a mildly generic scene-setting phrase, but it still ties to a specific, named list of five real cited mechanisms rather than being swappable filler for an unrelated topic.

## 4. Dominant verb(s)

Method sentence's main verbs: **reconstruct, decompose, isolate, sweep**. `isolate` and `decompose` are in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `reconstruct` and `sweep` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea — this matches `paper.md`'s own Step 3 self-audit, which explicitly checked for exactly this and flagged only one instance of a combine-adjacent verb ("combine the signal history" describing the learned estimator, M6) as needing to stay framed as a *measured condition* rather than the headline move. Checking the assembled `paper_draft.md` below against that same flag: the Methodology section's "Learned History Estimator" subsection describes the mechanism as *predicting a signed continuation gain from the running signal history* — "predict," not "combine" or "integrate," as its main verb — so the flagged risk did not resurface in the final prose.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (reconstruct/decompose/isolate/sweep) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the single worst flag.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

Like the B5.5 exemplar, this topic's own seed material (`paper.md` Step 0 asymmetry/deletion-test and Step 3 self-audit) had *already* run an informal version of this same check before this audit began — the reverse-digest generation process for this topic was itself designed to reject Bridge+Synthesis framing, and it went further than B5.5's seed by pre-naming the exact load-bearing verbs it expected ("reconstruct, measure, quantify, decompose, isolate, certify") and pre-flagging one risky verb ("combine," M6) to watch for. This audit is independent confirmation using a different, externally-sourced taxonomy — not the same prompt logic that authored `paper.md` — and it agrees, while also closing the loop on `paper.md`'s own self-flagged risk by checking the final assembled prose rather than only the design-stage note.

The practical implication for the other topics in this batch: a 🟢 here should not be read as evidence that a rich, pre-registered seed automatically implies a clean taste audit — it is evidence that *this* seed's asymmetry (the future is unobservable online but reconstructable offline under mechanical verifiability) survives being asked, independently, "could this be reframed as a generic bridge between stopping-rule engineering and regret theory?" The honest answer, checked here, is no: deleting the domain nouns from the motivation ("a growing family of X mechanisms is evaluated only by Y, never by Z") leaves a sentence that is still meaningful in the abstract, but the *specific* claim about what regret is and how it is computed collapses without the mechanical-verifiability and offline-probing content — which is exactly the deletion-test criterion `paper.md`'s own Step 0 already applied and this audit independently re-derives.
