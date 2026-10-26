# Research Taste Audit — B3.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Providers ship new model versions frequently and users observe behavioral change, but are never told which of three very different things happened underneath — the model got smarter, its safety/alignment posture shifted, or nothing except its default formatting habits changed — and these three have completely different, and completely un-interchangeable, downstream consequences for whoever integrates the model. ... the canonical longitudinal audit of ChatGPT's behavior over time found that part of an apparent capability regression in code generation was in fact caused by newly added markdown fencing breaking an executability check — a format change that got scored and reported as a capability loss."

**Method** (Stage 5, summary-level): "We build three probe batteries, each engineered so the other two axes have minimal effect on its measured quantity by construction, and calibrate the resulting decomposition by testing blind recovery of a known dominant axis on constructed control pairs before interpreting any real pair. We regress out and separately report cross-axis leakage rather than letting it silently bias axis shares, estimate a within-version noise floor from repeated sampling so ordinary run-to-run variability cannot masquerade as drift, and test whether the resulting axis-dominance structure agrees across vendors via a rank-agreement statistic against a permutation null."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "users... are never told which of three very different things happened" / "a single blended... score cannot tell these apart" — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the documented ChatGPTBehavior incident: an *existing, actively used* auditing practice (blended before/after deltas) is shown to be unreliable, misreporting a format change as a capability loss — a risk in current practice, not just an unmeasured phenomenon.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. The related-work threads (auditing, refusal/policy measurement, judge-bias literature) are each cited for a *specific instrument limitation* they carry (needs white-box access; single-axis; single time-point), not as two disconnected fields waiting to be linked. `paper.md`'s own Step 0/Step 3 independently arrived at the same non-bridge framing (the "one-directional confounding" argument) and its Step 3 self-audit already rejected a bridge reading.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we build... batteries... calibrate... regress out... estimate... test" is measurement instrumentation and characterization, not "integrate/unify" two existing methods or literatures. The secondary Formal Derivation reading comes from the method's precise definitions doing real work — axis share, leakage share, noise floor, and recovery accuracy are each given an explicit, checkable definition (`paper.md` Step 5) rather than left as informal notions, which is closer to "we formalize a quantity" than to a pure measurement pipeline with no conceptual apparatus.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together with a connecting verb. Each battery, the leakage regression, the noise-floor model, and the control-pair calibration protocol are purpose-built for this attribution problem, not borrowed wholesale from elsewhere.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three axes, *which* control-pair construction recipes (base vs. domain-SFT, base vs. safety-SFT, altered template), *which* cross-axis regression, *which* specific noise-floor stability check (early-half vs. late-half within 20%). Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "providers ship new model versions frequently and users observe behavioral change," which is scene-setting rather than argument, but it is immediately anchored to a specific, cited incident (the markdown-fencing misattribution) rather than left as unsupported scene-setting.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, calibrate, regress (out), estimate, test**. None of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea. The mechanism that does the real work — holding two axes fixed "by construction" — is best described by *isolate*, which is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*). `calibrate`, `regress`, and `estimate` are neutral, task-specific verbs rather than connecting verbs.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/calibrate/estimate/test/build) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, using the "deletion test" (Step 0) to confirm the core sentence is not a generic connecting-verb template. This audit is independent confirmation using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's, not the same prompt logic that wrote `paper.md`), and it agrees on the substance while adding a check `paper.md` did not run: the `surface_stitching` / `bottleneck_specificity` / `boilerplate` scoring and the archetype-verb check, both of which came back clean independently.

One point worth surfacing honestly rather than glossing over: the method's secondary Method-Paradigm label (**Formal Derivation**) is close enough to a genuine synthesis-adjacent reading that it deserves a sentence of scrutiny. The reason it does not tip the primary label is that the formal apparatus (axis share, leakage share, noise floor) is built to make *this specific attribution problem* checkable — it is not "unifying" two prior formalisms, and no cited related work contributes a formal object that this paper's definitions integrate or reconcile. If a future revision of this idea leaned harder on citing, say, a general variance-decomposition framework from statistics and framed the contribution as "bringing mixed-effects modeling into LLM auditing," that framing shift alone (not the underlying mechanism) would risk tipping the Method-Paradigm label toward Synthesis/Unification — worth flagging as a phrasing trap to avoid during paper assembly, even though the current confirmed Stage 5 wording does not fall into it.

The practical implication for the other topics in this batch: this specific pass (🟢, no manufactured flag) should not be read as "every topic in the set will pass automatically." This seed's Step-0/Step-3 self-audit was already unusually rigorous (a "deletion test" for the core sentence, an explicit adjective-to-formal-definition audit at Step 5) before this external audit ran at all — other seeds with thinner self-checks, or ones that genuinely do transfer a technique across domains, are more likely to need the reframe pass in Step 6 of the auditor's procedure. Running this audit per-topic, right after Stage 2/5 confirm and before committing to a full paper draft, is what makes an honest 🟢 (versus a manufactured one) possible.
