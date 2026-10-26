# Research Taste Audit — B4.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Practitioners who deploy LLM reasoning systems under a real, metered dollar budget must decide how to split that budget among thinking longer, sampling more, or paying a verifier to select among candidates — but no existing study prices all three levers, including the verifier's own cost, in one currency and measures their empirical exchange rate. Every prior allocation study either fixes the budget's unit to something other than dollars (FLOPs, tokens, sample counts, trajectories) or treats the verifier as a free or externally-priced oracle-like resource."

**Method** (Stage 5, summary-level): "We meter chain-of-thought length, sample count, and verifier calls in one dollar unit including the verifier's own cost, fit a single interaction-aware response surface across the full (L,N,V) grid instead of sweeping levers independently, replicate the identical matched-cost protocol across task families ordered by verifiability to test whether allocation transfers or is family-specific, bin and regression-adjust for stochastic realized cost so that 'matched budget' is a measured property of collected data rather than of requested settings, and decompose any verifier-attributed accuracy gain against a budget-matched majority-vote control and a ground-truth selection ceiling to rule out coverage as the true source of measured verifier value."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Scope Mismatch**)
- rationale: the motivation's load-bearing claim is "no existing study prices all three levers... in one currency" — a diagnosability/measurement absence (no instrument exists to answer "what does a marginal dollar buy on each lever"), not a "two literatures never connected" framing. The secondary Scope Mismatch reading is licensed by "every prior allocation study either fixes the budget's unit to something other than dollars... or treats the verifier as a free... resource" — prior work's claims hold only under an idealized cost model (FLOPs-matched, or verifier-as-oracle) that doesn't match deployment reality.
- Explicitly **not** Bridge Opportunity: there is no "test-time-compute economics and LLM inference have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 3 self-audit independently checked this same question and reached the same conclusion ("the claim is not 'econometrics and test-time scaling were never connected.' It is that one measurable quantity... has been left outside every prior budget constraint... PASS").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we meter... fit... replicate... bin... decompose" is characterization/measurement instrumentation — building a matched-cost grid and extracting a frontier — not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from `paper.md`'s own Step 5, which turns informal notions ("exchange rate," "frontier shape," "matched budget") into precise computable definitions (MRS as a local finite difference on a fitted surface, an Aitchison-distance permutation test for "stability") — a conceptual/definitional contribution sitting alongside the measurement pipeline, not merely a pipeline.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued with a connecting verb. The five components (cost meter, interaction-surface model, verifiability-stratified replication, matched-cost binning, coverage/selection decomposition) are purpose-built responses to five distinct identifiability problems that a naive grid scan would not solve on its own.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three levers, *which* accounting convention for a shared dollar unit, *which* two interaction terms (N×V, L×V), *which* four-family verifiability ordering, *which* specific control (budget-matched majority vote) rules out *which* specific confound (coverage vs. selection). Matches or exceeds the human baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "practitioners who deploy LLM reasoning systems... must decide how to split that budget," which is fairly generic deployment framing, but it still ties directly to the specific, checkable claim that follows it (no study prices the verifier's own cost) rather than functioning as swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **meter, fit, replicate, bin, decompose**. `decompose` sits in the same family as *isolate/disentangle/separate*, which the source paper's archetype-verb analysis places in the human-heavy cluster; `meter`, `fit`, `replicate`, and `bin` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge/reconcile* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (meter/fit/replicate/bin/decompose) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0's asymmetry sentence and Step 3's self-audit) had *already* run its own informal Bridge/Synthesis self-check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and its own worked example (Step 0's "deletion test") is essentially a hand-rolled version of this skill's `bottleneck_specificity` check. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees.

Two things are worth flagging honestly rather than papering over. First, the primary Opportunity label landed on **Evidence Gap** here and on **Evidence Gap (secondary: Failure/Risk Gap)** for the calibration reference (B5.5) — both measurement-absence framings, which is unsurprising given both seeds share the "[证据]" (evidence-type) label in `38_topics.txt`'s taxonomy; this is a property of how these two topics were seeded, not evidence the auditor always returns the same label. Second, the secondary Method label (**Formal Derivation**) is doing real work here, not decorative padding: `paper.md` Step 5's table of computable definitions (efficient/dominated, MRS, "non-constant," "stable across families") is exactly the kind of conceptual-distinction contribution the taxonomy's Formal Derivation cell describes, sitting alongside — not replacing — the Empirical Mapping primary label.

The practical implication for the other topics in this batch: this specific pass (🟢, no manufactured flag) should not be read as "every topic in this set will pass automatically" — the auditor is cheapest to run *per topic*, right after Stage 2/5 confirm, before committing to a full paper draft, precisely because a thinner seed (less self-audited than this one) could easily land in the overrepresented cell.
