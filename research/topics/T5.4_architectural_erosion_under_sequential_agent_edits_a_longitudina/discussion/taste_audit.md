# Research Taste Audit — T5.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after"). This audit is independent of `paper.md`'s own Step 3 self-check (same seed, different taxonomy, run cold against the *stage-confirmed* wording rather than the pre-registered spec's own phrasing) — it is not a re-statement of that self-check.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Test suites are the dominant, often sole, automated acceptance gate for autonomous coding-agent patches, but test suites are constitutionally blind to dependency-direction, layering, and module-boundary structure — so whether repeated agent editing under this gate quietly accumulates architectural damage that no single-patch review would catch is a live, unanswered governance question... a rate estimate alone is not actionable at the point where it would matter... knowing the concrete patch-level carriers... is what would let a team turn a lagging, trajectory-level diagnosis into a leading, per-patch check."

**Method** (Stage 5, summary-level): "We restrict the acceptance oracle to test execution only (verified structurally uninformative by a static scan of its own test files) while independently extracting architecture metrics after every accepted step; we isolate agent-attributable erosion via a human-gold counterfactual arm on the identical task sequence, distinguishing it from structural growth any correct implementation would also require; we model the resulting per-step metric series with trajectory-level random effects and a nonparametric trend test to detect slow compounding drift against noise; and we attribute erosion rate to specific conditions and patch-level mechanisms (cross-layer imports, duplication, edit locality) via a contrastive factorial design and within-trajectory feature regression."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "whether... quietly accumulates architectural damage that no single-patch review would catch" and "a live, unanswered governance question" — a diagnosability/measurement absence (no instrument exists to see this), not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "test suites are constitutionally blind" and "treating 'the tests are green' as a proxy for 'the codebase is healthy' is actively misleading" — the worry that an existing, widely-relied-on gate (the test suite) may be unreliable as a safeguard, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause in the confirmed Stage 2 wording. `paper.md`'s own Step 3 self-audit independently flagged and demoted the same risk in its own drafting process (digest Claim 4, "fills a documented gap between two literatures," was explicitly excluded from the abstract as positioning-only) — this audit arrives at the same conclusion via a different taxonomy and independently of that self-check, which is worth noting as corroboration rather than circularity, since the wording audited here (Stage 2's confirmed motivation) was drafted fresh in this pipeline, not copied from `paper.md`'s Step-3-corrected text.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we restrict... isolate... model... attribute" is characterization/measurement instrumentation of an existing phenomenon, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the definitional work carrying real weight in its own right — "architecture-blind" is given a checkable formal property (zero import-structure assertions in the gate's own test files, verified by static scan) and "agent-attributable erosion" is given a precise counterfactual-subtraction definition — these are conceptual/definitional contributions, not just a data-collection pipeline.

## 3. Diagnostics

- `surface_stitching` = **1** — the instrument does combine existing tooling (a SWE-bench-style harness, off-the-shelf static-analysis extractors, mixed-effects models, a survival-analysis borrow from dialogue-degradation work) but a real mechanism links them: the deliberate architecture-blindness of the gate crossed with the human-gold counterfactual is an isolation *logic*, not a glue job — it does identification work no single borrowed component does alone. Not a 0 (there is real reuse of existing statistical/analysis machinery), but well short of "A+B, nothing else added."
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* gate property (zero import-structure assertions, checked by a specific static scan), *which* counterfactual (human-gold patches on the identical task sequence, contrast on the shared task-intersection), *which* three patch-level features (cross-layer import edges, duplication delta, edit locality). Matches the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "delegating multi-step software-engineering work to autonomous coding agents," which is slightly generic framing language but still ties to a specific, named stake (teams currently reading green CI as a health signal) rather than being swappable filler that could sit in any AI paper's introduction.

## 4. Dominant verb(s)

Method sentence's main verbs: **restrict, isolate, model, attribute**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `attribute` and `model` are neutral, task-specific verbs, not connecting verbs; `restrict` (constraining the gate's scope on purpose) is likewise neutral-to-human-heavy in spirit, adjacent to the *strip out* / *expose* family the reference lists as behaving like the human-heavy cluster. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/attribute/model/restrict) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and had explicitly caught and reframed the same two risks this audit independently re-derives — a bridge-shaped positioning claim (digest Claim 4) demoted out of the abstract, and an "SWE-bench + static analysis + mixed models glued together" surface reading reframed around the architecture-blind-gate-crossed-with-counterfactual isolation logic. This audit used a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`) and applied it to the *stage-confirmed* Motivation/Method wording produced fresh in this pipeline's Stage 2/5 — not to `paper.md`'s already-corrected text — and it agrees.

The practical implication for the wider batch of topics this pipeline is being run across: **this specific pass (🟢, no manufactured flag)** should not be read as "every topic in the set will pass automatically." `surface_stitching=1` here is not a 0 — the design does lean on several off-the-shelf statistical/analysis tools, and a shallower motivation draft than the one this pipeline built (e.g., one that led with "SWE-bench and architecture-erosion research haven't been connected" instead of leading with the oracle-blindness invariant) would have landed exactly on the Bridge+Synthesis cell this idea currently avoids. The auditor is cheapest to run **per topic, right after Stage 2/5 confirm**, before committing to a full paper draft — which is exactly what happened here.
