# Research Taste Audit — B4.6

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation confirmed at Stage 2 + Method confirmed at Stage 5 of `discussion_trace.md`), **before** paper assembly — per the skill's own guidance that idea-level flags are cheapest to catch before drafting. Date: 2026-08-15. Note the seed here is immature (README-only, no digest/paper.md), so unlike B5.5 there is no prior Step-0/Step-3 self-audit to confirm — this is the idea's *first* taste check, which raises rather than lowers the bar for honesty.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed; quoted with light joining): "Serving cost, not capability, is becoming the binding constraint on coding-agent deployment … and today's serving stacks price generation while treating verification as opaque tool time. Verification steps break both assumptions in a specific, checkable way: their execution cost spans orders of magnitude, their outputs are large, volatile, and re-fed into the prompt, and their failure outcomes trigger retry loops whose generation cost is causally downstream of the verification event. … Two workload characterizations now exist and neither carries verification-step semantics: no verification-attributed cost share, no retry-loop attribution, no cache-interaction analysis. … Cache invalidation is a distinct harm from token volume because agent serving is prefill-dominated: … content that churns — as verification output does — can cost multiples of its own length."

**Method** (Stage 5, summary-level): "We bound the verification-induced dollar share of each session between two attribution rules with known-direction bias; replay each session through a prefix-cache simulator with counterfactual re-renderings to attribute cache invalidation to verification content specifically; stratify per-class cost against action-divergence to measure whether the cost–value frontier across lint/type-check/unit/build/suite is degenerate; and partition rescheduling counterfactuals by an agent-visibility invariance predicate, evaluating agent-transparent reschedules by exact replay and agent-visible ones by live, non-inferiority-gated re-execution."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Resource Bottleneck**)
- rationale: the load-bearing motivation clauses are measurement absences — "neither carries verification-step semantics," "no verification-attributed cost share, no retry-loop attribution, no cache-interaction analysis" — i.e., no good way to measure/audit the quantity in question. The secondary Resource Bottleneck reading is licensed by "serving cost … is becoming the binding constraint," which frames the stakes as cost/scalability.
- Bridge Opportunity was explicitly considered and rejected: the motivation does mention two communities (serving-systems work and agent-side budget research) optimizing different terms, which superficially resembles "two literatures in isolation." But the claim is not "these should be connected" — it is "a specific quantity that both communities' cost models need (the verification-induced component and its cache interaction) has never been measured." The deletion test confirms it: remove every reference to the second community and the motivation still stands on the unmeasured quantity alone. That is an Evidence Gap, not a Bridge.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "bound … replay … stratify … measure" is systematic measurement/characterization instrumentation. The secondary Formal Derivation reading comes from the two conceptual objects the method contributes — the known-direction-bias interval attribution rule and the agent-visibility invariance predicate that partitions valid from invalid counterfactual evaluation — both taxonomy-boundary contributions rather than measurements per se.
- Not Synthesis/Unification: no pair of existing methods is glued; the cache simulator, the attribution ledger, and the two-tier evaluation are purpose-built for this identification problem.

## 3. Diagnostics

- `surface_stitching` = **0** — nothing is "A + B." The nearest-neighbor's machinery (dollar-priced speculation, 2606.07846) is not imported and combined; it is the *object* of the framing-tier test. Each instrument exists because a specific identification problem (no counterfactual in traces; churn/volume/position entanglement; off-policy replay invalidity) demands it.
- `bottleneck_specificity` = **3** — the targets are exact and nameable at every step: *which* costs (execution seconds, feedback tokens, retry-segment generation, re-prefilled tokens), *which* mechanism of cache damage (volatile spans — paths, timestamps, durations, truncation boundaries — churning a radix-tree prefix cache), *which* boundary makes counterfactuals valid (byte-identical agent-visible sequence), *which* failure mode would falsify the premise (liberal bound < 0.10; invalidation ratio ≤ 1.1; degenerate frontier within 1.5×). At or above the human calibration baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing. The one near-generic clause is "serving cost, not capability, is becoming the binding constraint," which is a framing sentence that could open several systems papers; it survives here only because Stage 2's critic forced it to be wired to concrete evidence (the enterprise inference-economics line and the 95T-token production study exist *because* operators meter this). Scored 1, not 0, to record that residual genericity honestly.

## 4. Dominant verb(s)

Method sentence main verbs: **bound, attribute, replay, stratify, partition** (with *measure* as the umbrella). *Partition* and *attribute* sit in the human-heavy family (decouple/separate/isolate/localize); *bound* and *stratify* are neutral, task-specific operations; *replay* is domain vocabulary, not a connecting verb. No instance of *integrate / unify / merge / combine / leverage / bridge* appears in claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** (Evidence Gap × Empirical Mapping) |
| 2 | `surface_stitching` ≥ 2, OR `boilerplate` ≥ 2, OR `bottleneck_specificity` ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (bound / attribute / replay / stratify / partition) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. This is reported honestly, not manufactured in either direction: the audit specifically hunted for the two most plausible failure readings — the two-communities sentence as a Bridge framing (rejected by the deletion test above), and the seed card's own "treat verification as a first-class scheduling unit" slogan as an integrate-style move (it is an *elevate/formalize* move: it names a specific object currently invisible to schedulers and gives it a measured profile, which is the replace/formalize family, not the connect family) — and neither survives contact with the confirmed text.

## 6. Interpretation

Two notes for downstream phases. First, the 🟢 is conditional on the framing staying measurement-first: the seed card's falsifiable claim is written in beats-baseline language ("$/resolved-task 降低 ≥X% 相对 agent 原生策略"), and the discussion loop had to re-translate it three separate times (Stages 1, 5, 6 — see the trace's "what was hardest" note) into an avoidable-share estimand. If a later edit lets the paper drift back into "our scheduler beats the native policy," the idea's taxonomy cell moves toward Optimization/Search with a thinner delta against the crowded agentic-scheduling cluster — re-run this audit if that happens (this is the trigger condition for the goal.md §3 item-8 currency rule). Second, the `boilerplate = 1` clause is the abstract's opening-sentence risk; Phase E should keep the binding-constraint claim attached to its evidence rather than promoting it to a standalone truism.
