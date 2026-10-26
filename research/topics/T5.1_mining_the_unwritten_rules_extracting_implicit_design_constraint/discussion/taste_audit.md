# Research Taste Audit — T5.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Passing a project's automated test suite is treated, in nearly every coding-agent benchmark, as the criterion for a mergeable patch — but the actual criterion maintainers apply also includes error-handling, architectural, and API conventions that are never written into any spec, linter rule, or test, and that a project's own contributors absorb only by accumulating review feedback over time... a patch can carry maximal behavioral evidence (every test passes) and zero compliance evidence at the same time... none of this is informative unless the catalog itself is trustworthy: a violation-rate number computed against a spurious, hallucinated, or one-off 'rule' is not evidence about agent compliance with anything a maintainer actually enforces."

**Method** (Stage 5, summary-level): "We mine constraint candidates only from review comments that demonstrably induced a later code change, cluster and merge them into a per-repository catalog admitted only above a multi-thread support threshold, build and validate a compliance judge against blind human annotation before trusting its labels at scale, assign categories under measured dual-annotator reliability rather than by assumption, and isolate the resulting category-wise violation distribution and the agent-vs-human-gold gap from a catalog-free judging alternative."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is that no automated, per-project instrument exists to measure design-constraint compliance at all ("none of this is informative unless the catalog itself is trustworthy" / "a patch can carry maximal behavioral evidence... and zero compliance evidence") — a diagnosability/measurement absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the certification risk named explicitly: test-pass rate is treated as sufficient certification for mergeability when it structurally cannot be.
- Explicitly **not** Bridge Opportunity: there is no "review-mining and agent-evaluation have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 3 self-audit independently ran this exact check before this audit started and rejected a bridge reading, describing the paper's value as "measuring an orthogonal, currently-unmeasured compliance signal," not connecting two fields.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we mine... cluster and merge... build and validate... assign... isolate" is measurement instrumentation and characterization, not "integrate/unify" two existing methods into one. The secondary Formal Derivation reading comes from the method's definitional work being load-bearing in its own right — `paper.md` Step 5 gives precise, checkable definitions for "change-inducing," "implicit/unwritten," and "genuine project constraint" that the method's validity gates directly operationalize, not just measurement machinery bolted onto vague terms.

## 3. Diagnostics

- `surface_stitching` = **1** — the pipeline reuses standard components (sentence embeddings, clustering, an LLM extractor/judge), but a real mechanism links them: the change-inducing filter as a *behavioral* definition of "enforced expectation," the ≥3-thread support threshold as an admission rule, and the judge-validity gate as a precondition on using any automated label at scale. This is not "we combine embedding model X and clustering algorithm Y to get a catalog" — the novel content is the gating logic between the off-the-shelf parts, not the parts themselves.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* filter (a follow-up commit editing the anchored lines), *which* threshold (≥3 distinct threads), *which* gate (κ ≥ 0.6 against blind dual-human annotation), *which* three categories and their measured reliability. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one generic-sounding clause is "as coding agents are increasingly delegated to open pull requests autonomously," a scene-setting sentence common to many agent papers — but it is immediately anchored to the specific, checkable claim that follows (test-pass rate and compliance are orthogonal signals), not left as free-floating scaffolding.

## 4. Dominant verb(s)

Method sentence's main verbs: **mine, gate, isolate, formalize** (per `paper.md` Step 3's own self-audit note: "corrected to gate/formalize/isolate/measure family"). `isolate` and `formalize` are both explicitly in the human-heavy archetype cluster; `mine` and `gate` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (mine/gate/isolate/formalize) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and had already caught and corrected its own draft verb choice — Step 3 explicitly notes the original framing "leaned on 'mine/leverage review history'" and was corrected to the gate/formalize/isolate/measure family before this audit ever ran. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), applied to the *discussion-loop's* confirmed Stage 2/5 outputs rather than to `paper.md` directly, and it agrees with the seed's own self-correction.

The practical implication: **this specific pass (🟢, no manufactured flag)** should not be read as evidence every seed in this topic set will pass automatically — several other topics may lean on a real cross-domain-transfer move (a technique imported from one subfield into agent evaluation) that gets *written up* in bridge language by default even when the underlying contribution is specific, per `archetype-verbs.md`'s cross-domain-transfer note. This one specifically avoided that failure mode because its central move — treating unwritten conventions as measurable via a *behavioral* proxy that never existed as a signal before — is native to the SE-measurement framing rather than borrowed and glued from elsewhere. The auditor is cheapest to run **per topic, right after Stage 2/5 confirm**, before committing to a full paper draft — flagging early is the entire point of running it here rather than after the draft is written.
