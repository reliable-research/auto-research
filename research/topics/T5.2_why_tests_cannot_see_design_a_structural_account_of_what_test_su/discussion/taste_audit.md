# Research Taste Audit — T5.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run in `pipeline.md`, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "'Passes the existing test suite' is increasingly used as the de facto gate for accepting a coding agent's change, but no one has measured which classes of design properties — as opposed to functional behavior — that gate is structurally blind to... Existing mutation-testing theory formalizes adequacy purely behaviorally — the equivalent-mutant problem, as classically defined, is about behavior, full stop — so this paper's dual-oracle admission procedure and resulting per-category profile is the only account of design-adequacy that is measured through the suite itself, as opposed to checked by separate machinery."

**Method** (Stage 5, summary-level): "We admit *design mutants* only when certified, by oracles independent of the suite under study, as both behaviorally equivalent (bounded differential execution) and convention-violating (rule checker); construct matched convention-neutral controls from the same operator families to isolate design-specificity from the generic equivalent-mutant effect; extend the classical output-diff kill criterion with trace-order assertions so temporal/ordering violations are visible at all; and test whether an observed gap survives a capability-matched test-suite augmentation to distinguish a structural limit from a quantity-limited one."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Explanation Gap**)
- rationale: the motivation's load-bearing claim is "no one has measured which classes... that gate is structurally blind to" — a diagnosability/measurement absence ("no benchmark for," "hard to measure" territory), not a "two literatures never connected" framing. The secondary Explanation Gap reading is licensed by the motivation's own contrast — existing theory doesn't explain *why* or *which* design properties escape testing, only that behavior-preserving mutants exist as a category.
- Explicitly **not** Bridge Opportunity: there is no "mutation testing and architecture conformance have developed in isolation, so we connect them" clause. `paper.md`'s own Step 3 self-audit had already flagged and rejected exactly this risk before this run started — it explicitly rewrote the framing away from "mutation testing 框架的又一处直接迁移" (yet another direct transfer) toward "the opportunity is the asymmetry [that test verdicts are near-constant on behavior-equivalence classes while design conventions vary within them]; mutation is merely the measuring instrument." This audit independently confirms that self-correction held through Stages 1–6 of the discussion loop.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "admit... construct... extend... test whether" is measurement instrumentation and characterization, not "integrate/unify" two existing methods into one. The secondary Formal Derivation reading comes from the admission rule itself — `EQ_B(m)`, `V(m)`, `D_c`, `N_c`, and the three-conjunct blind-spot definition (Stage 1's refined `objective`) are a conceptual/definitional contribution (a taxonomy boundary and a formal criterion), not merely a measurement pipeline glued from parts.

## 3. Diagnostics

- `surface_stitching` = **1** — the instrumentation does compose existing tools (a mutation engine, Checkstyle/ArchUnit, a differential-testing generator), which keeps this from a clean 0. But a real, new mechanism sits between them: the *admission rule* (require both independent oracles to agree before a mutant counts), the *matched-neutral-control* comparison, and the *extended kill criterion* are not something any of the composed tools does on its own — this is "some combination, but a real mechanism links the parts," not "we combine X and Y to get Z, nothing else added."
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* two oracles, *which* operator family per category, *which* matched-control comparison, *which* augmentation validity gate. Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "coding agents increasingly author production code," which is slightly generic AI-framing language but still ties to a specific, checkable claim (green-suite gating) rather than being swappable filler for an unrelated topic.

## 4. Dominant verb(s)

Method sentence's main verbs: **admit, construct, extend, test**. `extend` and `construct` are neutral, task-specific verbs (not on either archetype list); `admit` functions like the human-heavy family's *isolate/separate* (it is precisely an isolation/inclusion criterion, not a connecting move); `test whether X survives Y` is the human-heavy family's core move (falsification framing, adjacent to *disentangle/expose*). No instance of *integrate/unify/merge/adapt/combine/leverage/bridge/reconcile* appears in a claim position anywhere in the extracted idea — even though the underlying instrumentation literally does compose PIT/pitest, Checkstyle, ArchUnit, and a differential-testing generator, none of those tools is described as being "integrated" or "unified"; each supplies one independent oracle to an admission rule.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (admit/construct/extend/test) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely an absence of the single worst one.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is not a rubber stamp, and it is worth being honest about why it came out clean: `paper.md`'s own Step 3 ("Taste self-audit") had *already* run an informal version of this exact check before this discussion-loop run began, and it explicitly flagged the risk that the seed's own phrasing ("mutation testing 框架的又一处直接迁移" — yet another direct transfer of the mutation-testing framework) invites a Bridge/Synthesis reading, then reframed the opportunity around the behavior/design asymmetry instead of the tool-transfer move. This audit is independent confirmation using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's, not the same prompt logic that wrote `paper.md`), and it agrees with the seed's own self-correction rather than merely repeating it.

The one place a Bridge-shaped read could still sneak back in during paper assembly is the Related Work section: with nine cited works split across an LLM-code-testing cluster and a classic-SE cluster (mutation theory, oracle quality, architecture conformance), it would be easy to drift into "these two literatures haven't been connected, so we connect them" phrasing purely as a transition device, even though the confirmed Stage 2/5 idea itself does not read that way. This is exactly the kind of surface-level drift the `pengsida-stage-reviewer` Related Work bar is built to catch (see `stage_review.md`), and it is the one flag actually raised there — not a taste-audit finding, but the same underlying risk showing up one stage later, in the prose rather than the idea.
