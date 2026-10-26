# Research Taste Audit — B4.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Test-time 'thinking' budget is one of the few levers that can be turned up after training to try to buy more accuracy from a reasoning model, but the entire literature that builds stopping rules, difficulty probes, and length-shortening objectives on top of this lever presupposes — without ever measuring — that there is a difficulty-conditioned point past which more thinking stops helping and starts hurting. If budget-allocation systems keep scaling thinking length under the assumption that returns merely flatten, but the true failure mode is that returns can turn negative (a correct answer state gets overwritten by continued reasoning), naive always-think-longer policies do not just waste compute — they actively destroy correctness, and nobody has measured where."

**Method** (Stage 5, summary-level): "We triangulate an operational difficulty proxy against two independent stratifications to rule out model-idiosyncrasy, localize a per-stratum tipping point with a paired-bootstrap slope-sign change-point test under three independent length-control arms (reporting agreement across arms as the confound mitigation), and evaluate whether cheap entropy/consistency signals computed from a short trace prefix predict that tipping point beyond what a coarser difficulty-bin decision and a length-only null already provide."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is that the entire adaptive-reasoning literature "presupposes — without ever measuring" the boundary — a diagnosability/measurement absence, exactly the Evidence Gap trigger ("no good way to measure, benchmark, audit... the thing in question"). The secondary Scope Mismatch reading is licensed by the one theoretical account that *does* predict the shape (`[WhenMoreIsLess, OpenReview:6QDFsYxtI1]`) doing so only under a narrow, experimenter-constructed difficulty variable on synthetic tasks — prior work holding only under an idealized regime.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation or method; `paper.md`'s own Step 0/Step 3 self-audit already independently ran this same check and rejected a bridge reading ("The opportunity is an unmeasured invariant... not a connection between two fields").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "triangulate... localize... evaluate whether... predict" is characterization/measurement instrumentation — building a boundary map and a change-point test, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the paired-bootstrap slope-sign change-point criterion and the notation table (Stage 1's `formal_summary`; `paper.md` Step 5) being a genuine conceptual formalization of what "tipping point" and "difficulty-conditioned" mean, not just a measurement pipeline description.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued with a connecting verb. The instrument (triangulated proxy, paired change-point test, decoupled cheap-signal predictor, cross-arm agreement criterion) is purpose-built for this identifiability problem, and the one component that reuses prior work (the prefill-probe reimplementation) is explicitly built in as a *baseline*, not folded into "the method."
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* proxy triangulation, *which* significance test on *which* paired statistic, *which* two decoupling controls (coarse-bin probe, length-only null) and *what each rules out*. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "one of the few levers that can be turned up after training," which is slightly generic framing language but still ties to a specific claim (thinking budget as a post-training-controllable resource) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **triangulate, localize, evaluate, predict**. `localize` and `triangulate` sit with the human-heavy cluster (*separate, disentangle, isolate*-adjacent — pinpointing/decoupling operations on a specific target, not a connecting operation between two things); `evaluate` and `predict` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea. Notably, `paper.md`'s own Step 3 self-audit independently landed on almost the same verb list ("measure, stratify, localize, isolate, predict, censor") before this audit was run.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (triangulate/localize/evaluate/predict) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp, for a specific reason worth stating plainly: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and it landed on almost the identical verb list this audit independently derived (`measure, stratify, localize, isolate, predict, censor` vs. this audit's `triangulate, localize, evaluate, predict`). That convergence, using two differently-sourced taxonomies (the seed's own deletion-test heuristic vs. this skill's externally-calibrated Chen/Zhao/Cohan taxonomy), is stronger evidence of a clean idea than either check alone — it means the human-shaped reading isn't an artifact of one particular check's blind spot.

One thing worth flagging honestly rather than glossing over: the predictor evaluation (`m_decoupled_cheap_signals`'s second hypothesis, corrected during the discussion-loop's Stage 5/6 critique in `pipeline.md`) came *close* to a different failure mode this skill doesn't score directly — outcome-tier "beats baseline" framing creeping into an otherwise Empirical-Mapping method. That's a `stages.md` tier-violation risk, not a taste-taxonomy flag (the method's *shape* is still Empirical Mapping, not Synthesis/Unification, regardless of how the predictor's win condition was phrased) — but it's the kind of drift worth naming here too, since both failure modes (generic-taxonomy drift and outcome-tier framing drift) point toward the same underlying discipline: state the claim in terms of what the *instrument* establishes, not in terms of a competition won. The practical implication for the other topics in this batch: a 🟢 taste verdict and a clean tier accounting are two different checks that can drift independently, and both are worth running even when the other already passed.
