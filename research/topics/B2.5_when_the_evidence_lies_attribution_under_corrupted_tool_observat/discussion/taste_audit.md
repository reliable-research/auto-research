# Research Taste Audit — B2.5

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Failure attribution for LLM agents is being industrialized as the mechanism that routes real debugging effort — retrain the planner, patch the tool, add a retry — but every attribution method proposed so far treats the trajectory log as trustworthy evidence, so if a tool's schema-valid output is simply wrong, nothing in the current pipeline is positioned to catch that the diagnosis itself may be misdirected. The same trajectory log that constitutes the failure evidence is produced by the very tool call under suspicion, so any diagnostic procedure that reads the log at face value inherits the corruption into its own premises before it starts reasoning about whose fault the failure is."

**Method** (Stage 5, summary-level): "We build a schema-preserving semantic-corruption injector gated by three independent validity checks, verify each corruption's causal decisiveness by counterfactual twin-replay, run existing attribution methods blinded to injection metadata against matched overt-error and agent-side-fault controls, probe the mechanism with a one-sentence trust-license prompt intervention, and score every method's native output against a pre-registered, dual-annotated mapping onto a shared plan/tool/execution ontology."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the load-bearing claim is "nothing in the current pipeline is positioned to catch that the diagnosis itself may be misdirected" and "inherits the corruption into its own premises" — a diagnosability/measurement absence (no attribution method's reliability under this specific fault mode has been checked), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the claim that current attribution is "unreliable" under this fault mode, not merely unmeasured.
- Explicitly **not** Bridge Opportunity: there is no "attribution research and tool-corruption research have developed in isolation" clause in the confirmed Motivation. `paper.md`'s own Step 0/Step 3 already caught and rejected a naive bridge framing ("the literature has industrialized both halves of B2.5 separately but never crossed them") and demoted it to a Related-Work positioning sentence rather than the opportunity itself — the confirmed Stage 2 motivation reflects that fix, anchoring on the trace-as-evidence asymmetry instead.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build... verify... run... probe... score" is characterization/measurement instrumentation — building a testbed to measure existing methods' behavior — not "integrate/unify" two existing methods into one. The secondary Formal Derivation reading comes from the decisiveness-vs-stealth distinction (Stage 4's refiner pass) and the pre-registered mapping rubric being conceptual/definitional contributions in their own right (what counts as "decisive," what counts as "undetectable"), not just a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The injector, twin-replay oracle, blinded harness, matched controls, and mapping rubric are purpose-built for this identifiability problem; existing attribution methods appear only as *objects of measurement*, run unmodified and blinded, not as components being glued together.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three validity gates, *which* twin-replay procedure, *which* one-sentence trust-license intervention, *which* matched agent-side-fault control. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "failure attribution for LLM agents is being industrialized," which is slightly generic framing language but still ties to a specific, checkable claim (Who&When/AgenTracer's own stated purpose of driving real interventions) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, verify, run, probe, score**. `verify` and `isolate`-family reasoning (via the twin-replay oracle and the matched agent-side-fault control) sit in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `build`, `run`, `probe`, and `score` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (verify/isolate/build/run/probe/score) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and that self-check explicitly caught a naive bridge framing in an early draft of Claim 1 ("the literature has industrialized both halves of B2.5 separately but never crossed them") and demoted it to Related-Work positioning rather than letting it anchor the opportunity. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), applied to the Stage 2/Stage 5 outputs of the discussion-loop run rather than to `paper.md`'s own text directly — and it agrees that the corrected framing holds.

The one place this idea could have drifted toward Bridge+Synthesis and didn't: the Related Work section (Stage 3) genuinely does connect two previously separate lines — attribution methods (Who&When, AgenTracer, MAST) and tool-channel corruption/robustness work (ChatInject, MCP-SafetyBench, ResiliBench). It would have been easy to motivate the paper as "we bridge these two literatures." The confirmed Motivation instead leads with the trace-as-evidence structural asymmetry (Evidence Gap) and treats the two literatures' disconnection as supporting evidence for that gap being real and unaddressed, not as the opportunity itself — the distinction the reframing guidance in `archetype-verbs.md` draws between a Bridge/Synthesis write-up and a mechanism-first write-up of what could be the same underlying observation.
