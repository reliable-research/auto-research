# Research Taste Audit — B5.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Autonomous LLM agents are increasingly delegated to negotiate real economic transactions on a principal's behalf, but there is no controlled, mechanically-scored measurement of how much surplus a counterparty can extract from such an agent using specific, named linguistic manipulation tactics — leaving principals with no way to price the economic risk of delegating bargaining to an LLM. ...a defense's effectiveness cannot be reported as a single aggregate verdict: if bargaining-zone reasoning and manipulation warnings recover surplus against false urgency and emotional pressure but leave anchoring's transfer largely intact... a principal told only 'defenses work' would under-protect against exactly the tactic likeliest to survive the fix."

**Method** (Stage 5, summary-level): "We build a paired-injection bargaining harness that isolates a single linguistic tactic's effect from generic toughness via a budget-matched control; conceal each side's reservation price from the agents while verifying that concealment against leakage probes; run the identical tactic set through a cross-model matrix on a shared action grammar; power the design with paraphrase/intensity variants to confirm the effect is tactic-level, not string-level; cross three counterparty-sophistication conditions with all four tactics to test whether cheap defenses recover surplus, and by how much per tactic; and audit realized tactic fidelity and concession genuineness to show that conditioning on verified delivery actually changes the verdict, not just decorates it."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "there is no controlled, mechanically-scored measurement of how much surplus... [tactics] extract" — a diagnosability/measurement absence ("no good way to measure... price"), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "leaving principals with no way to price the economic risk" — the worry that a governance-relevant vulnerability (manipulable delegated bargaining) exists and is unquantified, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 3 self-audit independently ran the bridge/synthesis deletion test and rejected a bridge reading ("A bridge version... is explicitly rejected").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build... isolate... conceal... run... power... cross... audit" is measurement instrumentation and characterization, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the toughness-subtraction discriminator and the fidelity-conditioning test each being a conceptual/decision-rule contribution (a criterion for when a raw statistic is trustworthy), not merely a measurement pipeline step.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together. The instrument (concealment controller, paired toughness-matched injection, cross-model matrix, variance-structure design, sophistication crossing, fidelity auditor) is purpose-built for this identifiability problem, and the closest prior instruments (TensorTrust/ChatInject's injection methodology, StrategicPersuasion's persuasion-as-utility-change framing) are each borrowed for one narrow property, not stitched together wholesale.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* four tactics, *which* two controls (no-tactic, toughness-matched), *which* statistic (`ΔS`, paired by scenario), *which* re-probe defines genuine-vs-feigned concession (remove the tactic's factual claim, check if the price still holds). Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "Autonomous LLM agents are increasingly delegated to negotiate real economic transactions on a principal's behalf," which is scene-setting rather than a specific claim, but it still anchors a specific downstream stake (surplus is the principal's money, not an abstract harm) rather than being freely swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **isolate, conceal, audit, price** (secondary: build, run, cross). `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `conceal` and `audit` are neutral, task-specific verbs; `price` is the paper's own headline verb (its title label is literally "welfare-pricing catalog") and is neutral/measurement-specific, not a connecting verb. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/conceal/audit/price) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: `paper.md`'s Step 0 (deletion-test asymmetry sentence) and Step 3 (explicit bridge/synthesis/verb self-check) had *already* run an informal version of this audit before this pass even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and its own stated verb check ("isolate, price, measure, gate, conceal — from the formalize/isolate/measure family") anticipates this skill's `archetype-verbs.md` almost exactly. This audit is independent confirmation using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's, not the same prompt logic that wrote `paper.md`), and it agrees.

One genuine tension worth surfacing rather than hiding: the method's secondary axis (Formal Derivation, for the toughness-subtraction and fidelity-conditioning decision rules) sits close to a "we built an instrument with several checks bolted on" reading, which is the kind of thing that *could* drift toward `surface_stitching` if the six modules were ever described as independently-motivated add-ons rather than jointly necessary for one identifiability chain (concealment → isolation → comparability → power → defense-crossing → fidelity gating, in that dependency order). The `bottleneck_specificity=3` and `surface_stitching=0` scores hold because each module's proposed_approach in Stage 5 states specifically *what confound it rules out*, not merely *that it exists* — but this is the property to re-check first if the paper draft ever compresses the Methodology section's per-module "Challenge → Insight → Method" structure into a flatter list.
