# Research Taste Audit — B5.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Protocol-layer mechanism design — structured bid schemas, verifiable commitment schemes — is the default engineering-first answer to negotiation manipulation between autonomous LLM agents, but whether it actually closes off manipulation, or only the fraction of it that happens to live inside its observable, enforceable action space, has never been measured category by category... establishing that a category is protocol-invariant only proves a negative; testing whether an actual model-layer instrument recovers ground on exactly the categories protocols cannot reach is what turns 'this sub-field should exist' into 'this sub-field has already produced a working instrument on the residue.'"

**Method** (Stage 5, summary-level): "We instantiate five structurally distinct manipulation categories as bilateral bargaining scenarios with hidden, machine-checkable ground truth, cross them with a four-rung protocol ladder implemented as deterministic environment-side wrappers, score every trial against precomputed truthful-play surplus rather than a message's structural form, isolate the protocol's effect from attacker competence via a dual prompted/scripted attacker design, validate the scoring rule against human judgment before trusting any verdict, and test whether an activation-probe monitor recovers ground on exactly the categories no protocol reaches without collapsing legitimate agreement."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "has never been measured category by category" / "whether it actually closes off manipulation... has not been measured" — a diagnosability absence, not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by the evidence clause itself: DSIC-by-construction guarantees (`AMenuNet`) are explicitly narrow-regime ("only over a formal bid action space") — the motivation's complaint is precisely that a guarantee proven under narrow assumptions is being informally assumed to transfer to a broader, untested regime.
- Explicitly **not** Bridge Opportunity: there is no "protocol-layer and model-layer defenses have developed in isolation, so we connect them" clause anywhere in the motivation. `paper.md`'s own Step 3 self-audit already checked for exactly this risk and rejected it ("the contribution is not the connection but the *location of a boundary invariant*") — this audit is independent confirmation of that same conclusion, not a rerun of the same reasoning.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we instantiate... cross... score... isolate... validate... test" is characterization/measurement instrumentation — building and running an ablation matrix, not integrating two existing methods into one. The secondary Formal Derivation reading comes from the fixable/invariant/undecided verdict rule itself: a pre-registered threshold-based decision rule with an explicit undecided category is a conceptual/decision-rule contribution (a taxonomy boundary with stated failure conditions), not merely a measurement pipeline with no conceptual payload.
- Note the taxonomy risk this idea sits closest to without falling into: the method *does* combine several components (a scenario generator, a scorer, an attacker-mode design, a validity audit, a defense arm) — which could superficially look like "combine A, B, and C." The diagnostics below check this directly rather than taking the taxonomy label's word for it.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued with a connecting verb. Every component (the dual-reference-style category taxonomy, the ground-truth content scorer, the deterministic enforcement design, the prompted/scripted confound control, the validity-audit gate, the joint recovery test) is purpose-built for this specific identifiability problem — reused ingredients (probe-training data, protocol wrappers) are instrumentation, not the paper's claimed contribution.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* five categories, *which* four protocol rungs, *which* axis is independent of which (structure vs. content), *which* confound (attacker competence vs. protocol effect), *which* threshold (kappa ≥ 0.7; MSR ≤5%/≥10%). Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "protocol-layer mechanism design is the default engineering-first answer to negotiation manipulation," which reads as scene-setting but still ties to a specific, checkable claim (a mechanism's guarantee covers only its observable action space) rather than being generic, swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **instantiate, cross, score, isolate, validate, test**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `score`, `validate`, and `test` are neutral, task-specific verbs; `instantiate` and `cross` describe a factorial design, not a connecting operation between two literatures. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (instantiate/cross/score/isolate/validate/test) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the single worst flag.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This result should be read with one honest caveat attached: `paper.md`'s own Step 3 already ran an internal taste self-check before this audit started, using the same trigger vocabulary (bridge / synthesis / load-bearing verbs) this skill uses, and reached the same conclusion ("gate, isolate, measure, adjudicate, classify — from the formalize/measure family"). This audit used a different, externally-sourced taxonomy and independently-computed diagnostic scores rather than re-running `paper.md`'s own reasoning, and it agrees — which is real, non-circular confirmation, but it is *expected* agreement given how carefully `paper.md` was already built to avoid this exact failure mode, not a surprising independent discovery.

Where this audit adds something `paper.md`'s self-check didn't check: the `bottleneck_specificity` and `surface_stitching` scores address a risk `paper.md`'s Step 3 didn't explicitly consider — that a six-component measurement instrument (taxonomy + scorer + enforcement + confound control + validity audit + defense arm) could read as "stitch five existing techniques together" even if the framing avoids bridge/synthesis language. Scoring `surface_stitching = 0` here is the more load-bearing check for a design this componentized: each of the six pieces earns its place by tracing to a distinct sub-problem in `pipeline.md` (checked as part of Stage 4/5's own cross-stage consistency pass), not by being a plausible-sounding addition to a growing pipeline.

The practical implication for the other topics in this set: a 🟢 on one componentized measurement study does not mean every multi-part instrument in this set will pass automatically — a design that reused the same six-part structure without each part tracing to a distinct, named sub-problem would be exactly the `surface_stitching ≥ 2` case this audit is built to catch. Running this pass per-topic, right after Stage 2/5 confirm, is what makes that check possible before a full paper draft is committed to.
