# Research Taste Audit — B5.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run in `pipeline.md`, **before** final paper assembly.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "The surplus a stronger negotiator extracts from a weaker one is not fixed by the capability gap alone but by how much of that gap can pass through the action-space channel the bargaining protocol leaves open to the weaker party — so narrowing that channel could in principle deny the stronger side the surface through which its advantage converts into surplus, without changing either agent's underlying capability. Whether this channel-gating actually holds for present-day LLM bargainers, and how large the effect is relative to the raw capability gap, has never been measured: existing weak-vs-strong studies score adversarial interaction only by win/loss outcomes or supervision-label quality, never by a continuous economic outcome against a computable reference split, and existing protocol-restriction findings (AI control) restrict the strong/untrusted side or the surrounding protocol, never the weak party's own expressive channel as self-protection in a bargaining setting."

**Method** (Stage 5, summary-level): "We build a capability-gap-controlled bilateral bargaining harness with a computable fair reference (Nash bargaining, checked against equal split and Kalai–Smorodinsky), quantify capability gap two ways (an exogenous general-capability score delta and an endogenous negotiation-specific Elo), and measure how a weak agent's normalized surplus loss scales with that gap; we then restrict the weak agent's entire turn to a schema-validated structured offer (deleting its free-text channel) and test, via a same-model causal contrast and a cross-tier substitution test, whether this constraint lowers surplus loss or lets a lower-capability tier match a higher one; a bilateral both-constrained control and tactic-tagged transcripts attribute how much of any effect flows through the rhetorical channel versus substantive bargaining strategy."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "has never been measured" / "never by a continuous economic outcome" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the underlying worry that a weak principal's agent may be silently exploitable at deployment. Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause. This required a deliberate framing choice — see §6 below.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Robustification**)
- rationale: "we build... quantify... measure... test" is characterization/measurement instrumentation of an existing phenomenon, not "integrate/unify" two existing methods. The secondary Robustification reading comes from the structured-offer constraint itself being tested as a hardening intervention against an existing failure mode (exploitability) — but it is tested, not proposed-and-optimized, which keeps Empirical Mapping primary.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The bargaining harness, dual gap measure, and structured-offer deletion are each purpose-built for this identifiability problem; no pair of pre-existing methods is being glued with a connecting verb.
- `bottleneck_specificity` = **3** — the target is exact at every step: *which* two gap measures, *which* three reference splits, *which one field* is deleted from the weak agent's turn (the natural-language message, nothing else), *which* two contrasts (same-model, cross-tier) the deletion licenses. Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "as LLM agents are increasingly delegated bilateral negotiation on a principal's behalf" (used in the Stage 2 draft's opening, not the refined `summary` above) — generic deployment-framing language, but it still anchors a specific claim (principal/adversary asymmetry) rather than being freely swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, quantify, measure, restrict, test, attribute**. `restrict` sits in the same family as `isolate`/`decouple` (the human-heavy archetype cluster — "deleting one field" is structurally a decoupling move: separating the rhetorical channel from the offer channel). `measure`, `quantify`, `attribute` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (restrict/measure/quantify/attribute) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the worst one.

## 6. Interpretation (why this pass required a deliberate framing choice, not just a lucky one)

This idea sits closer to the Bridge-Opportunity trap than the B5.5 companion topic did, and it is worth being honest about that rather than reporting a clean pass without comment. The underlying move — "AI-control research already shows protocol-level restriction protects a weak/trusted party; test whether the same move protects a weak party in *bargaining* specifically" — is a textbook instance of `archetype-verbs.md`'s **cross-domain-transfer note**: transferring a technique from one field (AI-control/safety) into an adjacent one (bargaining/mechanism-design) is common and legitimate, but it is exactly the move that tends to get *written up* in Bridge/Synthesis language by default ("these two things haven't been connected; we bridge them").

`paper.md`'s own Step 3 self-audit had already flagged this risk independently ("the motivation must not lean on 'no one connected weak-vs-strong oversight to bargaining'; it must lead with the mechanism"), and the Stage 2 critic round in `pipeline.md` re-derived the same concern from scratch before reconciling with that prior self-audit. The corrected `summary` above leads with the **channel-gating mechanism** ("surplus extraction is gated by an action-space channel, not fixed by capability gap alone") rather than the cross-literature analogy — the AI-control finding is cited only as *evidence the mechanism is plausible in an adjacent domain*, not as the thing being bridged. That is the difference between this audit's two worked examples in `archetype-verbs.md` (`archetype-verbs.md`'s own MBFL/agent-trajectory pair): same underlying transfer, but the mechanism-first framing is what keeps the label on Evidence Gap / Empirical Mapping rather than tipping it to Bridge / Synthesis.

The practical takeaway for the pipeline as a whole: a 🟢 here is not evidence that Bridge-Opportunity risk was absent, but that it was caught and specifically written around — exactly the value this audit is supposed to add, and exactly why it needs to run on the actual confirmed Stage 2/5 text rather than on the seed's own prior self-audit alone.
