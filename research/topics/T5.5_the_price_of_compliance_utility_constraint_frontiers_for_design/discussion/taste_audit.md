# Research Taste Audit — T5.5

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Enforcing design constraints on coding agents is routinely treated as a low-cost governance lever... but whether compliance is actually cheap, and whether its price scales at a predictable, near-linear rate, has never been directly measured for coding agents... a team that measures only the *average* cost across a limited pilot range cannot tell a graceful frontier from a knee-shaped one from that average alone... which is precisely why the frontier's *shape*, not its average price, is the deliverable this problem is built to produce."

**Method** (Stage 5, summary-level): "We build a κ-audited, bindingness-screened catalog of machine-checkable design rules parameterized by breadth × strictness, sweep it across executable coding benchmarks under prompt-only / checker-in-the-loop-retry / binary-all-on enforcement arms, jointly test the pass-rate and cost curves for a statistically detectable knee via a dual Davies-test-plus-ΔAIC criterion (reporting cross-axis disagreement as a distinct 'shape-discordant' outcome rather than resolving it by fiat), decompose measured cost into mechanism-attributable vs. constraint-attributable shares via an arm × strength interaction model, and isolate constraint-content effects from generic instruction-length effects via a token-count-matched placebo-prompt control."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Resource Bottleneck**)
- rationale: the motivation's load-bearing claim is "has never been directly measured" / "no corpus paper... jointly sweeps design-constraint strength and measures a pass-rate × violation-rate × cost frontier" (digest N3's own honest coverage report) — a measurement/diagnosability absence, not a "two literatures never connected" framing. The secondary Resource Bottleneck reading is licensed by the seed's own `[资源]` (Resource) label and the cost/compute framing throughout (token budget, retry cost, API price), though the *headline* question is the shape verdict, not the harness's existence.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation, so we connect them" clause anywhere in the motivation. paper.md's own Step 0 independently arrived at the same asymmetry framing, and its Step 3 self-audit already checked and rejected a bridge reading ("the framing is not 'constraint-following research... and coding benchmarks... were never connected, we connect them'... this measures an invariant of one process. PASS.").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build... sweep... test... decompose... isolate" is characterization/measurement instrumentation — a systematic sweep-and-diagnose apparatus, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the dual-criterion breakpoint test and the mechanism-share decomposition themselves being conceptual/decision-rule contributions (a shape taxonomy — graceful / knee / shape-discordant — and a cost-attribution formula), not merely a measurement pipeline with no conceptual apparatus attached.

## 3. Diagnostics

- `surface_stitching` = **1** — the harness does assemble existing pieces (BigCodeBench-style tasks, SWE-bench Verified, off-the-shelf static-analysis linters), which paper.md's own Step 3 self-audit already flags honestly ("the harness does assemble existing pieces... but the method's load-bearing moves are *isolation* moves, not assembly"). Scored 1, not 0, precisely because that assembly is real — but a real mechanism (the κ-audit gate, the dual-criterion test, the arm×strength decomposition, the placebo control) sits between the assembled pieces and the claimed contribution, which is what keeps this off 2–3.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* ~20 rules and rule types, *which* two strength axes (breadth vs. strictness) and how they're factorially separated, *which* three enforcement arms, *which* dual criterion (Davies + ΔAIC, jointly required) and *which* two curves it's applied to, *which* specific cost-decomposition ratio and its now-guarded denominator, *which* placebo margin (3pp) rules the content-vs-length confound in or out. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one generic-adjacent clause is "organizations want them to obey not just functional correctness but design-level constraints," which reads as scene-setting rather than argument, but it still ties to a specific claim (the shared-generation-budget asymmetry) rather than being swappable filler that could describe any LLM-agent paper.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, sweep, test, decompose, isolate**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `sweep`, `test`, `decompose` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea — matching paper.md's own Step 3 verb audit ("sweep, measure, isolate, screen, audit, decompose, test (a shape), gate. No load-bearing integrate / unify / combine / leverage. PASS."), independently reproduced here against the *confirmed Stage 2/5 outputs* of this run rather than paper.md's pre-existing draft text.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (build/sweep/test/decompose/isolate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp, for two reasons specific to this run. First, `surface_stitching` was deliberately *not* scored 0 — the harness's real reliance on assembled off-the-shelf pieces (BigCodeBench-style tasks, SWE-bench Verified, static-analysis linters) was weighed honestly rather than waved away, and it still lands well under the ≥2 flag threshold because a real mechanism (the κ-audit gate, the dual-criterion test, the arm×strength decomposition, the length-matched placebo) sits between the assembled pieces and the claim, not just a connecting verb. Second, paper.md's own Step 3 had *already* run an equivalent self-check before this audit started (same PASS verdict on the bridge/synthesis/verb checks) — this audit is independent confirmation using a different, externally-sourced taxonomy applied to this run's own *confirmed Stage 2/5 outputs* (not paper.md's pre-existing prose), and it agrees. That convergence is evidence the idea's specificity survives being independently re-derived through the discussion loop, not just an artifact of one earlier self-audit being repeated verbatim.

One genuine residual risk worth flagging rather than suppressing: the secondary Resource Bottleneck / Formal Derivation labels mean this idea sits closer to a hybrid than the B5.5 exemplar's cleanly single-labeled Evidence Gap / Empirical Mapping placement — the seed's own `[资源]` tag and paper.md's Global Fallback F-G1 (pivoting to a `benchmark/resource` framing if the central hypotheses all fail) both acknowledge this paper could end up being read primarily for its released catalog+harness rather than its shape finding. That is a legitimate, pre-committed pivot (not a taste problem), but it is worth the paper draft below stating plainly which framing is primary so a reader isn't left to guess.
