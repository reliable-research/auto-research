# Research Taste Audit — B3.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "A cheap per-version probe battery is one of the few practical ways a team could audit an LLM version update without a full downstream re-test, but which behavioral axis's drift actually forecasts real breakage — as opposed to merely tracking how much the update changed overall — has not been directly measured... knowing the ranking alone does not make continuous auditing sustainable: providers ship new versions at a cadence that compounds across every deployed integration a team maintains, and each additional probe family in the battery carries its own item-bank curation cost... which is exactly why identifying the smallest subset that still retains most of the predictive power, not merely the full ranking, is what turns this from a one-off academic comparison into a protocol a team could actually run continuously."

**Method** (Stage 5, summary-level): "We administer five behavioral-probe families identically to both versions of a pair and regress downstream breakage jointly on all five drift scores in one fit, so which axis governs breakage — and whether any axis carries signal at all — comes from a single instrument. We define downstream breakage functionally, per task, before pooling across a heterogeneous downstream suite. We gate every reported cross-version drift against a within-version noise floor and require the resulting family ranking to survive rewording across independent paraphrase sets. We disentangle each family's own marginal contribution from what it merely shares with the other four via VIF-checked partial correlation. And we admit a version pair to the retrospective corpus only after a reachability gate, then directly test whether pairs lost to deprecation mid-study differ systematically from the retained sample."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "which behavioral axis's drift actually forecasts real breakage... has not been directly measured" and "no cited work compares [probe families] against each other or against a downstream-breakage ground truth" (per `pipeline.md` Stage 2/3) — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the motivation's own risk framing: a team that probes the wrong axis "gets a false sense of having audited the update while the real risk... goes undetected" — the worry that a governance practice (probe-based re-testing) may be silently misdirected, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "capability testing and safety testing have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0/Step 3 self-audit independently arrived at the same non-bridge framing ("The opportunity is *not* 'probes and breakage were never connected, we connect them.' It is an asymmetry...").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "administer... compute... regress... gate... disentangle" is measurement instrumentation and a comparative predictive-validity study, not "integrate/unify" two existing methods into a new pipeline. The secondary Formal Derivation reading comes from the minimal-sufficient-subset criterion itself (`AUC(S) ≥ AUC(F) − δ`) and the corpus-admission gate being conceptual/decision-rule contributions — precise operational definitions of "minimal," "breakage," and "stable," not just a measurement pipeline running borrowed instruments.

## 3. Diagnostics

- `surface_stitching` = **1** — some combination is real here (the per-family probe implementations are borrowed designs — `RefusalIndex`'s rank-invariant construction, `B-Calibration`'s semantic-calibration error, `OffTopicEval`/`ProSafePrune`'s accept-refuse framings), so this isn't a from-scratch instrument the way B5.5's dual-reference scorer was. But a genuine new mechanism links the borrowed pieces into a result none of them alone produces: the joint-regression identification step, the VIF-checked partial-correlation disentanglement, the dual noise-floor-and-paraphrase gate, and the corpus-admission/attrition-bias test are all purpose-built for this paper's specific identifiability problem, not a glue of two pre-existing end-to-end methods.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* standardized coefficient in *which* joint regression, *which* VIF threshold before trusting a partial correlation, *which* percentile of *which* null distribution counts as "above noise," *which* Kendall-τ threshold counts as "rank-stable." Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "one of the few practical ways a team could audit an LLM version update without a full downstream re-test," which is mildly generic practitioner-appeal phrasing but still ties to a specific, later-justified claim (minimality's cadence/scale argument) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **administer, regress, gate, disentangle**. `disentangle` is explicitly in the human-heavy archetype cluster (with *decouple, separate, isolate*); `regress`, `administer`, and `gate` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea — even though the method's *inputs* are borrowed single-axis instruments, the verb describing what the method *does* to them is never "combine" or "integrate."
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (disentangle/regress/administer/gate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks. Note that `surface_stitching` at 1 (rather than 0) is the one diagnostic worth watching if this idea is later reframed — the method's reliance on four borrowed single-axis instruments as feature inputs is the closest this idea comes to a stitching risk, and it stays off the flag threshold only because the joint-regression/disentanglement/gating apparatus around those inputs is genuinely new machinery, not a thin wrapper.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: `paper.md` Step 0/Step 3 had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started ("Bridge? ... PASS. Mere synthesis? Risk: 'we assemble five existing single-axis instruments.' Correction: the deliverable is the adjudication... a measurement result the five instruments individually cannot produce. PASS after reframing."). This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees — including landing on the same specific risk `paper.md`'s own Step 3 flagged ("we assemble five existing instruments"), which is exactly why `surface_stitching` is scored 1 rather than 0 here rather than being waved through as a clean 0.

The practical implication: this specific pass (🟢, no manufactured flag) confirms the idea is specific enough to survive scrutiny, but the non-zero `surface_stitching` score is worth keeping in mind if the paper is later compressed for a shorter venue — the biggest risk to this particular idea's taste rating is an abstract that leads with "we combine five behavioral probes" rather than with the identification/disentanglement/gating apparatus that is the actual contribution. The Method Overview and Methodology sections in the assembled draft below are written to lead with the apparatus, not the borrowed inputs, for exactly this reason.
