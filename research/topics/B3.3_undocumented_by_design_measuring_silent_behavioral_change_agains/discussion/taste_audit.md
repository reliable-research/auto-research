# Research Taste Audit — B3.3

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "The party that controls when a deployed AI system changes is also the sole author of the record of what changed, so external, reproducible measurement is the only way to bound how much that record omits — and no one has actually run this measurement. An aggregate rate alone tells an integrator or regulator *that* silence is common but not *where to look*; a category-level taxonomy is what turns 'undocumented change happens' into an actionable prioritization."

**Method** (Stage 5, summary-level): "We run a calibrated diff detector (same-version null estimation, effect-size floor, A/A control) against a category-stratified probe suite anchored to externally-validated benchmarks, align each detected diff to the vendor's changelog claims by semantic entailment (calibrated against human labels and a string-match floor), attribute diffs to release windows via a data-driven fingerprint-discontinuity boundary check, and report the resulting silent-change rate explicitly as a coverage-conditioned lower bound whose stability we check via split-sample agreement rather than claiming point-estimate correctness."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "no one has actually run this measurement" / "no independent way to check that assumption" — a diagnosability absence (no way to measure/audit documentation completeness), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the structural-conflict-of-interest framing (the changelog's author and the party whose incentives govern disclosure are the same actor, with "no natural correction mechanism") — a worry about an unreliable, structurally-biased record, not a claim that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0 deletion test and Step 3 self-audit already ran this exact check and rejected a bridge reading ("this is not 'changelogs and behavior audits were never connected, so we connect them' — the load-bearing content is the structural conflict of interest").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we run... align... attribute... report" is characterization/measurement instrumentation — building a diagnostic pipeline and reporting a quantified rate with confidence bounds, not "integrate/unify" two existing methods into a new system. The secondary Formal Derivation reading comes from the paper's explicit partial-identification framing itself (the `paper.md` Step-5 formal definitions of $D(p)$, $\mathrm{Doc}(p)$, $\mathrm{Silent}(p)$, and the lower-bound status of $\rho$) — a conceptual/definitional contribution about what the estimand even means, not just a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **1** — some combination (the diff-detection step echoes the two-sample-test spirit of `[LogProbTracking]`, and entailment matching draws on generic NLI tooling), but a real, purpose-built mechanism links the parts: the category-anchoring move (borrowing benchmark taxonomies to avoid circularity), the boundary-fingerprinting move (a data-driven discontinuity test, not a calendar lookup), and the split-sample stability check are not present in any single prior work and were assembled specifically to make the documented-vs-silent estimand checkable. Not a "we combine X and Y to get Z" construction.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* effect-size floor (Cliff's δ ≥ 0.33), *which* entailment threshold (τ tuned on a labeled dev subset), *which* specific benchmarks anchor *which* specific category, *what* the fingerprint-discontinuity test specifically checks. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "vendors of deployed AI systems routinely ship updates whose behavioral consequences are only partially, if at all, described" — a somewhat generic-sounding opening, but it still ties directly to the specific claim being made (structural conflict of interest as the object of measurement), not swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **run, align, attribute, isolate**. `isolate` (via the A/A control's role — "isolating real change from sampling noise," `paper.md`'s own Abstract v0 phrasing) is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `align`, `attribute`, and `run` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/align/attribute/run) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: `paper.md`'s own Step 0 (asymmetry deletion test) and Step 3 (taste self-audit) had *already* run an informal version of this exact check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and it explicitly named and rejected the risk that "align changelog text with behavior diffs" could read as a Bridge Opportunity. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees on both the categorical labels and the underlying diagnostics.

The practical implication: **this specific pass (🟢, no manufactured flag)** should not be read as evidence that every topic in the broader set will pass automatically — several other seeds may have thinner Step-0/Step-3 self-audits, or may lean on a real cross-domain-transfer move (borrowing statistical-auditing machinery from fairness/change-detection literature into a new *documentation-fidelity* target, as this paper explicitly does) that gets *written up* in bridge language by default (see `archetype-verbs.md`'s cross-domain-transfer note). What kept this idea off that path is specific: the motivation is framed around the *structural conflict of interest* and *what becomes measurable as a result* (a coverage-conditioned lower bound with a category taxonomy), not around "two literatures have developed in isolation" — and the method's key moves (category anchoring to break circularity, fingerprint-based boundary attribution, split-sample stability in place of an uncheckable point estimate) are each a specific, nameable operation on a specific bottleneck, not a generic synthesis label. Running this auditor per-topic, right after Stage 2/5 confirm, is what makes catching a thinner self-audit elsewhere possible before a full draft is committed to.
