# Research Taste Audit — T3.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Memory-pinning is one of the main proposed mechanisms for keeping safety- and task-critical constraints alive through the lossy context-compaction that long-horizon LLM agents require, but whether — and how cheaply — an adversary can defeat it has so far only been shown to happen at all, never mapped as a function of attack strength or priced against what the defense costs to run... the cost ratio is not a restatement of the boundary but the one piece of information an operator needs to trade marginal robustness against marginal overhead, which no break-through curve by itself supplies."

**Method** (Stage 5, summary-level): "We implement five pinning variants as interchangeable middleware wrappers, instrumented per-turn; normalize two structurally incomparable attack families (gradient-optimized suffix search; template-role forgery) onto one comparable strength axis; define a two-tier oracle for constraint violation gated by a before/after-compaction attribution requirement; convert attacker and defender effort into a common cost currency under two independent conversions; and fit a power-gated, bootstrap-interval break-through boundary per variant, checking whether the resulting robustness ranking is stable across models and attack families."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is that a known failure ("broke every tested model") has "never [been] mapped as a function of attack strength or priced against what the defense costs to run" — an absence of measurement/diagnostic instrumentation, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the premise that pinning is relied on as a safeguard whose reliability is itself in question, not by a bridging move.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0/Step 3 independently pre-empted this reading — its domain-noun-deletion test on the core asymmetry sentence returned an empty schema (a bridge-style sentence survives deletion as generic filler; this one does not), and its Step 3 explicitly names and rejects the naive "prompt-injection × memory-compaction, never combined" framing in favor of the durability/cost asymmetry.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we implement... normalize... define... convert... fit" is measurement instrumentation and characterization, not "integrate/unify" two existing methods into one system. The secondary Formal Derivation reading comes from the strength-normalization scheme, the two-tier violation oracle, and the cost-ratio definition each being conceptual/measurement-definitional contributions (a formalization of what "boundary" and "cost" mean under heterogeneous mechanisms), not just a pipeline of borrowed parts.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The instrument (structural defense matrix, log-normalized strength axis, two-tier oracle, dual-currency cost accounting, power-gated boundary fit) is purpose-built for this identifiability problem; the borrowed attack machinery (GCG/SlotGCG-style optimization; ChatInject-style template forgery) is explicitly demoted to "component reused for its mechanism, not a system this paper synthesizes with another."
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* five variants, *which* attack families and how their strength is normalized, *which* two-tier oracle and its κ threshold, *which* two cost currencies, *which* rank-correlation test. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "one of the main proposed mechanisms for keeping safety- and task-critical constraints alive," which is a slightly generic framing move but still ties to a specific claim (pinning specifically, not memory/agent-safety generally) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **implement, normalize, define, convert, fit**. `normalize` and `convert` sit in the same family as `isolate`/`separate` (making incommensurable things comparable by an explicit, principled transformation) — the human-heavy archetype cluster. `define` and `fit` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (normalize/convert/define/fit/implement) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters here specifically)

This idea sits closer to the Bridge/Synthesis danger zone than a typical clean pass, and it is worth saying exactly why it still clears it. The seed's surface description — "prompt-injection attacks" meets "context-compaction memory systems" — is precisely the shape of pairing that an under-specified LLM ideation pass would default to bridging ("these two research threads haven't been connected; we connect them"). Two things pull it off that template instead:

1. **The load-bearing object is a property of the compaction game itself, not a connective move.** `paper.md`'s Step 0 states the durability/cost asymmetry (an all-quantifier defender vs. an exists-quantifier attacker over repeated lossy-compaction events, with an amortizable offline attack budget against a non-amortizable per-turn defense budget) as the thing being measured. This asymmetry would exist and be worth measuring even if only one of the two literatures (compaction *or* injection attacks) had ever been named — it is not a claim that gains its force from *linking* two fields.
2. **The method's actual new content is a set of definitions and normalizations (Empirical Mapping + Formal Derivation), not an act of combination.** Reusing GCG/SlotGCG/ChatInject's attack machinery and TensorTrust/GuidedEval's evaluation ideas is honestly disclosed reuse (see `pipeline.md` Stage 3's careful "borrowed component, not a baseline" framing for exactly this reason) — but the paper's contribution is the strength-normalization scheme, the two-tier persistence oracle, and the dual-currency cost ratio, each a specific measurement instrument this paper is introducing, not a synthesis of the borrowed parts into a new system.

The practical implication: this is a genuinely useful, independent confirmation, not a rubber stamp — the seed material (`paper.md` Step 0/Step 3) already ran its own informal version of this same check before this audit started, and this audit (a different, externally-sourced taxonomy, not the same prompt logic that authored `paper.md`) agrees with it rather than merely repeating it. A topic whose surface framing pattern-matches to "attack literature meets defense-system literature" is exactly the case where independently re-running this check, rather than trusting the seed's self-audit, is worth the cost.
