# Research Taste Audit — B3.5

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Multi-vendor redundancy is treated as a risk-hedging strategy against any single vendor's failure modes, biases, or outages, but this strategy silently assumes vendors' models evolve independently — an assumption current evidence has never tested longitudinally, because concrete mechanisms (a shared pool of AI-generated web text, algorithmic monoculture in RLHF/DPO candidate generation) could produce convergence invisible at any single point in time. Pairwise drift correlation and population-level diversity are logically separable failure modes — vendors could drift in correlated directions while staying spread out, or converge independently with no pairwise correlation — so both have to be tracked, not inferred from each other."

**Method** (Stage 5, summary-level): "We administer a fixed, capability/neutral-axis-partitioned probe battery to dated version panels across vendors, extract per-vendor drift vectors, and test cross-vendor correlation against a permutation exchangeability null on the capability-neutral axes; we residualize out the shared cross-vendor mean drift direction to separate genuine homogenization from correlated capability improvement, check the correlation's sign stability across two independent time-alignment conventions and its robustness to removing the single most-correlated axis, and track a two-index (Vendi + CAPA-distance) cross-vendor diversity trend, gated throughout by an empirically-measured noise floor establishing that any of this is measurable at all."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "current evidence has never tested longitudinally" / "invisible at any single point in time" — a diagnosability/measurement absence (no instrument exists to track drift-correlation across dated version sequences), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the stake itself: if homogenization is real, an existing, actively-used governance heuristic (multi-vendor redundancy) is unreliable — a risk claim, not a bridging claim.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation, let's connect them" clause anywhere in the motivation. `paper.md`'s own Step 3 self-audit independently reached the same verdict ("The framing is not 'connect longitudinal drift with cross-model similarity'; it is 'isolate the component of drift on which independence is testable'").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we administer... extract... test... track" is characterization/measurement instrumentation — building and applying a drift-correlation and diversity-trend instrument, not integrating two existing methods into one system. The secondary Formal Derivation reading comes from the capability/K_neu residualization construction itself: defining what "homogenization" formally means (a claim that must survive axis-partitioning *and* projecting out a shared direction) is a conceptual distinction the paper introduces, not merely a measurement pipeline borrowed off the shelf.

## 3. Diagnostics

- `surface_stitching` = **1** — several of the individual instruments are commodity parts (IFEval, TruthfulQA/SimpleQA, Vendi Score, a CAPA-style distance), which on their own would read as "glue A+B+C+D together." But a real mechanism links them: the capability/neutral axis partition and the residualization-against-the-shared-drift-direction are the load-bearing move, and no borrowed instrument contains that move — it is purpose-built for this identifiability problem. Not a 0 (the battery genuinely reuses off-the-shelf scorers), but well short of 2–3 (textbook A+B glue with nothing else added).
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* axis partition (K_cap vs. K_neu), *which* direction is projected out (ḡ, the empirical cross-vendor mean drift vector), *which* two alignment conventions, *which* axis is dropped in the robustness check, *which* two diversity indices must agree in sign. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "multi-vendor redundancy... risk-hedging strategy," which is a slightly generic governance phrase, but it still ties to a specific, checkable claim (an assumption of *independence*, not vendor diversity in the abstract) rather than being swappable filler that could describe any AI-safety topic.

## 4. Dominant verb(s)

Method sentence's main verbs: **residualize, isolate, test, gate**. `residualize` and `isolate` sit squarely in the human-heavy archetype cluster (the paper's own Step 3 self-audit lists exactly this verb set: "isolate, measure, test, gate, residualize, falsify" and confirms none of "leverage/unify/integrate" appears in any claim position). No instance of *integrate/unify/merge/adapt/combine/leverage* appears anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (residualize/isolate/test/gate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful independent confirmation, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) already ran its own informal bridge/synthesis self-check before this audit started, and explicitly recorded its own worry about exactly this risk — Step 3's own table asks "Is the method mere Synthesis (CAPA + Vendi + IFEval glued together)?" and answers "PASS with guard," naming the same load-bearing element (the exchangeability null + capability-residualization) this audit independently identified as the reason `surface_stitching` doesn't score higher. That two independently-run checks — one from a different taxonomy, one from the paper's own self-audit — converge on the same diagnosis (real instrument-stitching risk, resolved by the residualization mechanism being genuinely load-bearing) is stronger evidence than either check alone.

The practical implication for the broader topic set: this 🟢 should not be read as "every topic in this set passes automatically" — the honest reason this one is clean is that `paper.md`'s Step 0 asymmetry sentence was *already* built specifically to reject a generic "correlation implies sharing" framing (its own deletion test: "without the domain nouns the sentence is empty and, read generically, false"). Topics whose seed material lacks this kind of pre-built asymmetry check are more likely to land in Bridge+Synthesis by default. Running this audit per-topic, right after Stage 2/5 confirm, remains the right point to catch it if a future topic's self-audit is thinner.
