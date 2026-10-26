# Research Taste Audit — B1.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Independent per-milestone verification is the standard way multi-step agent benchmarks, reward signals, and deployment 'task complete' judgments grade long-horizon tasks, but whether this local-checking paradigm is actually sufficient evidence of true task success — rather than something a trajectory can satisfy without ever establishing what each checkpoint is supposed to certify — has not been directly measured... no existing work directly quantifies how often this happens under an explicit prerequisite structure with an independent terminal ground truth."

**Method** (Stage 5, summary-level): "We build a locality-scoped per-milestone verifier suite whose code-level scope restriction is directly auditable, paired with a topology-stratified adversarial trace generator that constructs reorder/skip/inject bypass trajectories, and a terminal state-consistency oracle validated by manual audit of its own false-inconsistency rate. We isolate whether observed bypass is attributable to structural locality rather than weak checker implementations via a strongest-local-checker control, and measure natural bypass incidence in real agent rollouts to separate a constructibility result from a live deployment risk."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "has not been directly measured" / "no existing work directly quantifies how often this happens" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "the verifier itself becomes the attack surface, not the task" — the worry that an existing grading paradigm is brittle/exploitable, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0 and Step 3 independently arrived at the same framing and already ran a bridge/synthesis self-check, explicitly stating "It is not a bridge: it names no pair of literatures to connect; it states a property of one object (the checkpoint check). PASS."

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build a...suite...construct...isolate...measure" is characterization/measurement instrumentation — a bypass rate estimated against a ground-truth oracle — not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from Stage 1's formal apparatus itself (the non-injective checkpoint→state map, the bypass event `B(τ):=A(τ)=1 ∧ Ω(τ)=0`, the sufficiency definition `A(τ)=1⟹Ω(τ)=1`) being a conceptual/definitional contribution in its own right, not merely a measurement pipeline description.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together. The instrument (locality-scoped verifiers, topology-stratified bypass constructor, disjoint oracle, strongest-checker control) is purpose-built for this specific identifiability problem, not an assembly of two existing tools under a connecting verb.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three bypass strategies (reorder/skip/inject), *which* single conjunction defines a bypass event (`A(τ)=1 ∧ Ω(τ)=0`), *which* control isolates structural locality from weak implementation (the strongest-local-checker arm), and *which* audit bounds the oracle's own error (a stratified 50–100-verdict manual review with a stated ≤5% threshold). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one softer clause is "multi-step agent benchmarks...increasingly rely on per-milestone grading because directly verifying full end-to-end correctness is expensive," which leans toward generic framing language, but it still ties to a specific, load-bearing claim (locality as a cost-driven design choice with a specific failure mode) rather than being generic filler swappable into an unrelated paper.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, construct, isolate, measure**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `construct` and `measure` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea. Notably, `paper.md`'s own Step 3 self-audit independently names its load-bearing verbs as "formalize, isolate, construct, measure, bound, gate" and explicitly checked for and avoided the integrate/unify/leverage family — this audit's verb-level finding agrees with that self-check using a different taxonomy.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/construct/measure/build) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 2/Step 3) had *already* run its own informal asymmetry/archetype/bridge/synthesis self-check before this audit even started — including an explicit deletion test on the invariant sentence (Step 0) and an explicit verb-family check that named "formalize, isolate, construct, measure, bound, gate" as load-bearing and confirmed the integrate/unify/leverage family was checked and avoided (Step 3). This audit is independent confirmation using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's two-axis framework and diagnostic rubric, not the same prompt logic that wrote `paper.md`), and it agrees on every axis.

No reframe was needed. The idea's specificity is also visible in a place the taxonomy doesn't directly score but is worth naming: the motivation and method both center on one precise, checkable non-injectivity claim (a checkpoint's local signal is a many-to-one projection of causal history) rather than a vague "verification is hard" framing — this is exactly the kind of nameable-mechanism specificity the source paper's `bottleneck_specificity` diagnostic is designed to reward, and it shows up consistently across Stage 1's formal apparatus, Stage 4's sub-problem decomposition (existence vs. attribution, kept explicitly distinct), and Stage 5's methods (each with a stated, falsifiable threshold). As with the B5.5 precedent, this specific pass (🟢, no manufactured flag) is evidence about this topic's seed quality, not a claim that every other topic in the set will pass automatically — some seeds may have thinner self-audits or lean on a cross-domain-transfer move that gets written up in bridge language by default. The auditor is cheapest to run per topic, right after Stage 2/5 confirm, before committing to a full paper draft.
