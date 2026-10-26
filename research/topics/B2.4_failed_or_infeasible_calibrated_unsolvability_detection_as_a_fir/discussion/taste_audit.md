# Research Taste Audit — B2.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run in `pipeline.md`, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Failure-attribution pipelines are built on the implicit assumption that every failed run contains a culpable agent decision; treating 'the task was never solvable' as an admissible outcome, rather than an unmodeled edge case, changes what these pipelines can be trusted to tell a downstream consumer... the two error directions have asymmetric downstream costs that a single fixed cutoff cannot serve... only a full calibration characterization lets each consumer choose its own operating point."

**Method** (Stage 5, summary-level): "We certify ground-truth unsolvability mechanically via typed mutation operators plus a requirement-and-no-substitute script oracle, run a matched attribution battery (LLM-judge, trained tracer, first-party self-report, and a label-space-restricted control) over both members of each pair, build an oracle-calibrated ceiling probe to dissociate a fixable attribution-design gap from an information-theoretic limit, sweep the unsolvable-confidence threshold into risk–coverage curves, and gate every domain through a leakage audit before any rate is reported."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is that current attribution pipelines have "no admissible" way to express task infeasibility and that whether they can distinguish it "has not been directly measured" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the claim that these systems "systematically over-blame the agent" — a worry about an existing mechanism's reliability, not a call to link two fields.
- Explicitly **not** Bridge Opportunity: there is no "attribution and unsolvability have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 3 self-audit independently ran the identical check ("Is the opportunity a Bridge? ... PASS") before this audit even started.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we certify... run a battery... build a probe... sweep... gate" is measurement instrumentation and characterization, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the design-vs-information-limit dissociation itself being a conceptual distinction (a boundary between two rival explanations for the same observed gap), not merely a measurement pipeline — structurally analogous to the three-conjunct criterion in the B5.5 exemplar.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together. The oracle-calibrated ceiling probe, the label-space-restricted control, and the leakage-audit gate are each purpose-built for this specific identifiability problem (design-limited vs. information-limited; genuine feasibility reasoning vs. surface-artifact detection).
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* mutation types (missing-resource, contradictory-constraint, stale-reference), *which* oracle check (required AND no-substitute), *which* two controls (`B0` label-restricted, `B-alt` oracle-calibrated), *which* gate threshold (text-only probe AUROC < 0.60). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "changes what these pipelines can be trusted to tell a downstream consumer," which is slightly generic trust-language but still ties to the specific retry/escalate/abandon policy argument developed immediately after it, rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **certify, run, build, dissociate, sweep, gate**. `dissociate` sits in the same family as the human-heavy cluster (*decouple, separate, disentangle*) per `archetype-verbs.md`; `certify`, `sweep`, and `gate` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (certify/run/build/dissociate/sweep/gate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 2/Step 3) had *already* run its own informal Bridge/Synthesis self-check before this audit even started, and independently listed almost the identical verb set ("certify, inject, measure, sweep, dissociate, gate") as evidence against a forbidden framing. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees with that self-check rather than merely repeating it — the taxonomy labels (Evidence Gap / Empirical Mapping) and the diagnostic scores are a genuinely separate pass, not a restatement of `paper.md`'s own reasoning.

One thing worth flagging honestly rather than glossing over: `bottleneck_specificity` and the verb check both benefit from the fact that `paper.md` had already forced every construct (the oracle, the two controls, the gate) into a precisely named object before this audit ran. A seed with a thinner Step-0/Step-3 self-audit could plausibly land in the same Evidence-Gap/Empirical-Mapping cell but score lower on specificity if its constructs were left vaguer — the taxonomy cell alone would not have caught that; the diagnostic scores are doing real, separate work here, and it is the combination of a clean categorical label *and* clean diagnostics that earns the 🟢, not the label by itself.
