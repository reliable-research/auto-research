# Research Taste Audit — T3.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Memory-pinning mechanisms for LLM agents can only preserve a governance constraint if the upstream step — deciding which spans are the rules — correctly recognizes it as one in the first place, and this recognition step has never been measured for adversarial robustness. Existing treatments of 'which text is binding' assign that status by channel position known a priori, not computed from content, so an adversary who preserves a rule's binding force while flattening its register into small talk defeats pinning without ever touching the pinning mechanism itself — and these two failure directions (evasion, spoofing) cannot be safely collapsed into one number because they serve opposite-goaled adversaries."

**Method** (Stage 5, summary-level): "We build GovSpan-Adv, a validity-gated bidirectional-rewrite testbed that provably decouples binding force from surface register, measure five identifier families' miss-pin and false-pin rates as separate paired statistics (not pooled accuracy), embed the same items in long unsegmented transcripts under an adaptive attacker to test joint localization, and run a blind boundary audit that decomposes measured fragility into genuine identifier failure versus contested ground truth, while a cross-family ablation isolates the finding from attacker-defender self-consistency."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "this recognition step has never been measured for adversarial robustness" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "an adversary who preserves a rule's binding force while flattening its register... defeats pinning" — the worry that an assumed-solved precondition is actually brittle, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0/Step 3 self-audit independently arrived at the same conclusion ("the framing is NOT 'pinning and adversarial robustness were never connected.' It is 'pinning silently assumes an identification step; we test whether that step holds.'"). This audit is an independent check using a different taxonomy, not a restatement of that self-audit, and it agrees.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build a testbed... measure... embed... run a blind audit... isolate" is characterization/measurement instrumentation, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the force/register decoupling itself and the validity-gate criterion being a conceptual/definitional contribution (a checkable criterion for what counts as a valid disguise), not merely a measurement pipeline — directly parallel to the force⟂register invariant `paper.md` Step 0 already isolates as "not a bridge... an invariant internal to the phenomenon."

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued. GovSpan-Adv's validity-gated bidirectional rewriter, the paired per-direction metrics, the depth-stratified localization harness, and the blind boundary audit are each purpose-built for this identifiability problem — none is a straightforward reuse of an existing pipeline.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* two properties (binding force vs. surface register), *which* validity gate (NLI entailment back-check + 2-annotator confirmation), *which* five identifier families, *which* two directions (evasion/spoofing), and *which* confound the cross-family ablation rules out. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "keeping governance constraints resident and enforced" in the broader pinning framing, which is slightly generic infrastructure language but still ties to a specific claim (pinning's guarantee is only as good as its identification precondition) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, measure, embed, decompose, isolate**. `isolate` and `decompose` are in or adjacent to the human-heavy archetype cluster (with *decouple, separate, disentangle*); `measure` and `embed` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea (the two places existing mechanisms are reused — ASIDE's privilege signal, SeqMonitor's cumulative-context monitor — are explicitly framed in Stage 3 as *adapted identifier families under test*, not as the paper's own connecting move).
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/decompose/measure/build/embed) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and even pre-selected verbs (isolate/measure/decompose) for exactly this reason. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees.

The one place this idea could have drifted toward a flagged pattern is the identifier suite itself: five identifier families, two of them (ASIDE's privilege signal, SeqMonitor's cumulative-context monitor) adapted from existing work, could easily have been written up as "we integrate privilege-signal and trajectory-monitoring approaches into a unified identifier" — a textbook Synthesis/Unification framing. Stage 3's refiner pass explicitly heads this off by reframing both as *identifier families under test*, not components being unified into the paper's own method — which is exactly the distinction that keeps the Method Paradigm label at Empirical Mapping rather than sliding into Synthesis/Unification. This is a real, load-bearing framing choice, not a coincidence of wording.
