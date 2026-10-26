# Research Taste Audit — B4.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Compute-allocation controllers are usually built from whichever signal is easiest to obtain — an extra self-report call, a handful of self-consistency samples — without asking whether a signal that costs almost nothing (a probe on a hidden state the model has already computed) could do the same job, because no prior comparison charges every controller's own signal-acquisition cost against the same budget it is trying to save."

**Method** (Stage 5, summary-level): "We recycle self-consistency samples' correctness as free probe-training labels, meter every controller's own signal-acquisition cost inside one dollar-denominated threshold-sweep router so probe/self-report/training-free signals are compared at identical realized spend, test whether the probe's routing quality transfers across tasks and backbones, guard the self-report baseline against being an artificially weak strawman by requiring two prompt-tuned variants and reporting the stronger, and isolate genuine decision-quality gains from mere budget arithmetic via a cost-free AUROC contrast."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Resource Bottleneck**)
- rationale: the motivation's load-bearing claim is "no prior comparison charges every controller's own signal-acquisition cost against the same budget it is trying to save" — a measurement/accounting absence, not a "two literatures never connected" framing. N4's own audit (quoted in Stage 2's `evidence` field) is explicit that the probe papers report token savings, the self-report literature doesn't price elicitation, and the router-benchmark literature evaluates a different (model-choice) controller class — three separate absences of the *same* measurement, not a missing bridge between two fields. The secondary Resource Bottleneck reading is licensed by the whole idea being organized around dollar/compute cost accounting as the central constraint.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 3 self-audit independently arrived at the same rejection — "Risk: 'connect probing to compute allocation.' Rejected — the antecedents ([DiffAdapt], [AdaptiveThinking]) already probe hidden states for allocation. The content is the *asymmetry in signal cost under a shared budget*... not a connection."

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Artifact/System**)
- rationale: "we recycle... meter... test... guard... isolate" is characterization/measurement instrumentation — a matched-budget comparison of existing controller families, not "integrate/unify" them into one new controller. `paper.md`'s own N12 rationale is explicit that "the paper proposes no new controller mechanism." The secondary Artifact/System reading comes from the precompute-then-simulate harness (digest CO3) being a reusable released instrument in its own right, independent of the measurement it first produces — though digest N12 itself already checked and rejected promoting this to the paper's *primary* contribution ("this would flip to `benchmark` only if the released two-tier cache + simulator were promoted to the paper's primary contribution").

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no ensemble gluing the probe, self-report, and training-free signals into one controller. `paper.md` Step 3 explicitly rejects that reading: "Rejected — the design does not fuse them; it *isolates and prices* each as a competing controller under one meter." The five method components (recycled-label pipeline, dual-cost router, transfer design, dual self-report operationalization, cost-free decision-quality isolation) are each purpose-built for a distinct accounting or validity problem, not stitched from two prior methods.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* signal-acquisition cost is charged to *which* controller, *which* five budget points, *which* two self-report variants, *which* three held-out transfer benchmarks, *which* specific cost-free statistic (AUROC) isolates decision quality from budget arithmetic. Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is the Stage 2 opener "as test-time compute scaling makes per-query budget decisions economically material" — a mildly generic AI-economics framing, but it still ties to a specific, checkable claim (a dollar-metered three-way comparison) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **recycle, meter, isolate, guard, test**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `meter`, `recycle`, `guard`, and `test` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (recycle/meter/isolate/guard/test) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template ("It is NOT a bridge... it names an invariant... that produces a testable ordering among controllers"). This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees.

One genuine risk worth naming rather than glossing over: the idea's *object* — a frozen probe on hidden states, competing against self-report and training-free signals — is itself drawn wholesale from prior work (`[DiffAdapt]`, `[AdaptiveThinking]` already build such probes). That could have tempted a lazier framing into "integrate probing with cost accounting" (a Bridge/Synthesis read). What keeps this idea off that cell is specifically that it does not propose to *combine* the probe with anything — it prices three pre-existing, independently-operated controller families against one shared meter and reports which one a fixed dollar buys the most accuracy from. The practical implication for the rest of this topic batch: a **🟢 here** should not be read as "every seed in this style will pass automatically" — several other frozen-probe or routing-adjacent seeds could plausibly get *written up* in "combine internal signals with external ones" language by default; this specific pass is a property of this motivation/method pair's actual verbs and target-specificity, checked directly, not assumed from the topic area.
