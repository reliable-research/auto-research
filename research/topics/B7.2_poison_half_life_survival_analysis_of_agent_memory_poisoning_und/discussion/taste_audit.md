# Research Taste Audit — B7.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the `auto-research-discussion` run, **before** final paper assembly — the audit is cheapest to run right after Stage 2/5 confirm, and this topic's seed was thin enough that the idea's shape was genuinely in question until the stages fixed it.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Memory-management policies — summarization, consolidation/reflection, eviction/TTL, deduplication — are deployed to improve agent utility and are tacitly assumed to also let benign traffic wash adversarial content out of memory over time; but whether they neutralize a poisoned claim, leave it untouched, or actively prolong its behavioral influence has never been measured as a rate, because the persistence of memory poisoning is reported only as a fixed-checkpoint binary (present/absent after a repair step) that cannot express a neutralization time and conflates a claim's literal removal with the end of its behavioral influence."

**Method** (Stage 5, summary-level): "We treat each injected poisoned claim as a survival-analysis subject and estimate its behavioral-adoption survival function and hazard over benign interaction time under a censoring-aware, interval-censored estimator; we define neutralization behaviorally (via a validated mechanical acceptance probe) rather than by literal detectability, so laundering — a claim surviving summarization in a detector-invisible but behaviorally-active form — appears as its own measurable state; we make memory-policy aggressiveness the manipulated treatment with identical replayed benign traffic (plus a matched-salience benign tracer as the isolating control) to separate its causal effect from salience and exposure; and we separate content-neutralization from structural-eviction as competing risks so the half-life is interpretable."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the load-bearing motivation clause is "has never been measured as a rate" / "reported only as a fixed-checkpoint binary … that cannot express a neutralization time" — a diagnosability/measurement absence, the textbook Evidence-Gap trigger. The secondary Failure/Risk reading is licensed by "actively prolong its behavioral influence" and "the checkpoint labeled repair is an amplification step" — a governance mechanism (memory management) that may be silently unsafe.
- Explicitly **not** Bridge Opportunity: there is no "two literatures / methods have developed in isolation" clause anywhere. Survival analysis is not introduced as a second field being connected to security; it is the *instrument* that turns a checkpoint binary into a rate. (See §6 for why the transfer-reads-as-bridge risk was actively checked and rejected, not ignored.)

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "estimate the survival function and hazard … measure as a rate … make policy the manipulated treatment" is characterization/measurement instrumentation, not "integrate/unify two methods." The secondary Formal Derivation reading comes from the conceptual contributions that are not themselves measurements: the behavioral-adoption-vs-literal-presence event distinction, the laundering cell as a defined state {ℓ=absent, a=adopted}, and the content-neutralization-vs-structural-eviction competing-risks decomposition — these are definitional/decision-rule moves.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The estimator is not survival-analysis-off-the-shelf glued onto poisoning; it is purpose-built for the problem's specific structure: interval-censored intermittent probes, a behavioral (not literal) event, competing exit causes, and a policy-as-covariate contrast. Nothing is stitched with a connecting verb.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* estimand (behavioral-adoption survival / hazard / half-life, not literal presence), *which* confound is decoupled (utility/exposure vs. laundering, via the benign tracer), *which* reclassification (the Forget/repair operation as an amplification stage), *which* competing risks (content-neutralization vs. structural-eviction). Meets/exceeds the human baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing. The one soft clause is "deployed to improve agent utility," mild governance framing, but it ties to a specific, testable claim (utility and persistence co-move under aggressive policy) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **estimate, define, separate, isolate, measure**. `separate`/`isolate` are explicitly in the human-heavy archetype cluster (with *decouple, disentangle*); `estimate`/`define`/`measure` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/bridge/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (estimate/define/separate/isolate/measure) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely the absence of a worst-case flag.

## 6. Interpretation (the one place a critic could push, checked honestly)

This idea has a real, nameable taste risk that most B-family topics do not, and it would be dishonest to record a 🟢 without confronting it: **"apply survival analysis to memory poisoning" is a cross-domain method transfer, and `archetype-verbs.md` warns explicitly that cross-domain transfer is the move most likely to get *written up* in Bridge/Synthesis language by default** ("statistical survival analysis and agent security have not been connected; we bridge them"). If the motivation and method had been framed that way, condition 1 would fire and this would be a 🟡–🔴.

The reason it lands 🟢 is that the confirmed framing leads with a *specific insufficiency* and a *specific operation on a named target*, exactly the mechanism-framing the reference file prescribes to distinguish a legitimate transfer from a bridge:
- the insufficiency is concrete and load-bearing — *the fixed-checkpoint binary cannot express a neutralization rate and conflates literal removal with the end of behavioral influence* — not "these two fields haven't met";
- the operation is on a named quantity — *estimate the behavioral-adoption hazard and reclassify the Forget/repair step* — not "combine survival analysis with poisoning benchmarks";
- survival analysis appears as the tool that delivers the rate, never as a co-equal literature whose union is the contribution.

This matches the file's worked contrast (the MBFL→agent-trajectory example): same lineage, but the write-up names the specific weak signal being replaced and the specific limitation resolved, which pushes the label off Bridge/Synthesis and onto Evidence-Gap / Empirical-Mapping. The audit therefore confirms the idea is human-shaped **because** the framing was disciplined, not because the transfer risk was absent — and the discipline (never letting "neutralization" collapse onto literal presence) is the same one the discussion trace records as "what was hardest." No reframe is needed; the finding to carry forward is that the Abstract and Method Overview must keep leading with the checkpoint-vs-rate insufficiency and never drift into "we bring survival analysis to agent security," which would reintroduce the flag. The final taste re-audit (`pipeline.md` Phase H) re-checks the assembled Abstract against exactly this.
