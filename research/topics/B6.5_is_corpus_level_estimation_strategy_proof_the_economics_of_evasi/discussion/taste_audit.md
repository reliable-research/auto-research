# Research Taste Audit — B6.5

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Practitioners increasingly rely on corpus-level AI-text prevalence estimates... precisely because they have been told instance-level detection is unreliable under adversarial paraphrasing, but whether that reframe genuinely trades away the adversary's leverage, or merely defers the same fragility to a different statistic, has not been directly measured... a single-N confirmation cannot distinguish 'robust regardless of scale' from 'coincidentally robust at this one tested size' — a fitted exponent β with a confidence interval is exactly the transferable safety-margin function a decision-maker needs, and the only form in which the seed's counterintuitive claim is falsifiable at all."

**Method** (Stage 5, summary-level): "We formalize a cost–accuracy game between a budget-bounded paraphrase adversary and a corpus-level distributional prevalence estimator; test whether directionally coordinated (not just independent) rewrites defeat the estimator's aggregation-based robustness; require the fitted budget-scaling exponent to hold sign under two independent cost models; validate ground-truth recoverability with a shuffled-label negative control; and isolate whether robustness stems from estimator design (mixture-MLE / debias-aggregate) rather than generic averaging via a naive-average control."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "has not been directly measured" — a diagnosability/measurement absence about whether corpus-level estimation actually resists evasion, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by "treating it as a safe fallback is actively dangerous" — the worry that an assumed-safe governance instrument may be unreliable, not that two fields need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0 (deletion-test asymmetry check) and Step 3 self-audit already ran this exact check and rejected a bridge reading independently of this audit.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we formalize... test... require... validate... isolate" is characterization/measurement instrumentation — fitting a scaling exponent and running isolation controls — not "integrate/unify" two existing methods into a new combined one. The secondary Formal Derivation reading comes from the cost–accuracy game itself and the operational definitions of "strategy-proof at scale" / "uneconomical evasion" (`paper.md` Step 5's adjective-to-computable-quantity table) being a genuine conceptual/formal contribution, not just a measurement pipeline.

## 3. Diagnostics

- `surface_stitching` = **1** — this is the most honest score in this audit, and deserves scrutiny rather than a rubber stamp: the two core instruments (the `MonitorAIScale`-style mixture-MLE estimator and the `AdaptiveWMAttack`-style adaptive paraphraser) are genuinely **borrowed off-the-shelf**, not purpose-built the way the calibration reference's (B5.5) instrument was. A skeptical reader could describe the base setup as "estimator A vs. adversary B, pitted against each other." What keeps this above a "textbook A+B" (score 3) is that the paper's actual claims are not "A beats B" but sit *on top* of that pairing: the scaling-exponent measurement across N, the cost-model-invariance requirement, the coordinated-vs-independent attacker isolation, and the naive-average confound control are all new analytical apparatus built to interrogate the A-vs-B pairing rather than just report its outcome. Scored 1, not 0, specifically to avoid over-crediting a study that does lean on two existing instruments — the "new mechanism in between" is real but sits alongside, not fully underneath, the base combination.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* two cost models, *which* specific 2× ratio threshold for the naive-average control, *which* exact tolerance for ground-truth recovery, *which* one-sided test on the scaling exponent β. Matches the strongest tested models in the source paper's calibration (2.3–2.6) and the human baseline (2.56).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "as synthetic text increasingly contaminates corpora used for training-data curation... and platform-scale moderation," which is fairly generic scene-setting, though it still anchors to a specific claim (corpus-level estimation being treated as a *safe fallback*) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **formalize, test, require, validate, isolate**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `formalize` is itself named in `taxonomy.md`'s Formal Derivation trigger words and is a human-majority-cluster verb per `archetype-verbs.md`; `test`, `require`, and `validate` are neutral, task-specific verbs, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea — even though the underlying instruments genuinely are adapted from prior work, the write-up does not lean on "adapt" or "combine" language to describe what the paper contributes.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (formalize/test/require/validate/isolate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. This is a genuine pass, not a manufactured one — but it is a **closer** pass than the calibration reference's, and that nuance is worth stating plainly rather than smoothing over (see §6).

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This idea clears the bar, but for a different reason than the calibration reference did. B5.5's instrument (dual-reference scorer, three-conjunct coordination criterion) was purpose-built for its identifiability problem, landing `surface_stitching=0`. Here, the two base instruments genuinely *are* two pre-existing methods (`MonitorAIScale`'s estimator, `AdaptiveWMAttack`'s adversary-construction protocol) run against each other — the honest description of the base setup is closer to "A vs. B" than B5.5's was. What keeps the verdict 🟢 is that the paper's actual falsifiable claims (the scaling exponent's sign and magnitude across N; its invariance across two cost models; its survival against a stronger, coordinated attacker; its attribution to estimator design rather than generic averaging) are analytical constructs layered on top of the A-vs-B pairing, not the pairing itself, and `paper.md`'s own Step 3 self-audit independently anticipated exactly this risk ("method = MonitorAIScale estimator (M2) + AdaptiveWMAttack adversary (M3) glued together. FAIL if the contribution is the combination") and pre-committed to answering it the same way this audit does.

The practical takeaway for future topics in this batch: a 🟢 verdict does not mean "no combination of existing tools is present" — it means the paper's *claimed contribution* is not the combination itself. Where a topic's base setup literally instantiates two named prior methods against each other (as here), it is worth explicitly checking `surface_stitching` above 0 rather than defaulting to 0, and stating in the interpretation section exactly what sits on top of the borrowed instruments — otherwise a genuine 🟢 risks reading, on a skim, like a rubber-stamped one.
