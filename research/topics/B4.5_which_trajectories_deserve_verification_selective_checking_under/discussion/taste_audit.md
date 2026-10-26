# Research Taste Audit — B4.5

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Test-time-scaling pipelines that sample many candidate trajectories per query increasingly pair the sampler with a verifier, but the literature that treats compute as an explicitly metered, allocable resource has only ever metered *generation* — never the calls to the verifier itself... a policy that only ever reports accuracy on the verified fraction throws away information the budget already bought: a verified-incorrect trajectory does not reveal the right answer, but it does remove a wrong one from contention, and if that elimination is not exploited, some of the value the budget purchased is simply discarded at the aggregation step."

**Method** (Stage 5, summary-level): "We score every trajectory with three verifier-free signals and measure each one's AUROC against verifier-labeled correctness (turning proxy validity into a first-class measured quantity, including a direct count of confident-but-wrong under-selection); rank trajectories by that signal and spend a fixed budget on the most-uncertain candidates, comparing a static ranking against a sequential reallocation policy measured against a hindsight-optimal benchmark; combine verified and unverified evidence with an elimination-aware aggregator that exploits verified-incorrect outcomes rather than discarding them; and audit realistic verifiers against gold labels while freezing a policy across a task-domain shift to check whether verifier-realism and domain-transfer premises actually hold rather than assuming they do."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Resource Bottleneck** (secondary: **Evidence Gap**)
- rationale: the motivation's load-bearing claim is that verifier calls are the metered, scarce, costly resource ("has only ever metered *generation* — never the calls to the verifier itself," "the more expensive step") — a scarcity/cost framing, not a "two literatures never connected" framing. The secondary Evidence Gap reading is licensed by the fact that no existing account *measures* how to spend that scarce resource once it's recognized as scarce (there is no AUROC-style validity check, no budget–accuracy curve, anywhere in the corpus for verifier calls specifically).
- Explicitly **not** Bridge Opportunity: there is no "generation-budget theory and verifier-imperfection theory have developed in isolation, so we connect them" clause anywhere in the motivation. paper.md's own Step 0/Step 3 independently arrived at the same scarce-resource framing and its own self-audit already rejected a bridge reading ("Risk exists: 'budget allocation exists for generation, we bring it to verification' is a bridge. Fixed framing: the opportunity is the Step-0 asymmetry... PASS after fix.").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Optimization / Search**)
- rationale: "we score... measure... audit... compare" is characterization/measurement instrumentation — an AUROC table, a budget–accuracy curve, a gap-closure measurement — not "integrate/unify" two existing methods. The secondary Optimization/Search reading comes from the allocation policy itself: ranking trajectories and spending a fixed budget on the most-uncertain ones, with a sequential-reallocation variant benchmarked against a hindsight-optimal allocation, is literally a budget-allocation strategy — matching the axis's own trigger phrase "allocate budget" directly.

## 3. Diagnostics

- `surface_stitching` = **1** — not a textbook "A + B" combination (no "we combine self-consistency and PRM scoring to get X"). Some combination is present — an existing uncertainty signal (self-consistency mode share, already used by Wang et al. 2023) is paired with an existing allocation framing (budget-constrained selection, already used for generation by Compute-Optimal-TTS/CaTS) — but a genuinely new mechanism sits between them: metering *verifier* calls specifically (not generation calls), the oracle/realistic two-tier trust audit, and the elimination-aware aggregator are all purpose-built for this problem, not borrowed wholesale.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* three signals (mode share, normalized sequence log-likelihood, verbalized confidence), *which* failure mode is measured (confident-but-wrong consensus pools, defined by an explicit mode-share threshold), *which* aggregation rule and why (elimination of verified-incorrect answers, not a generic "smart combination"), *which* shift axes are audited (verifier class, task domain) and by what mechanism (freeze-then-retest). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one generic-adjacent clause is "test-time-scaling pipelines... increasingly pair the sampler with a verifier," which is scene-setting rather than a specific claim, but it still ties directly to a concrete follow-on point (verifier calls, not generation calls, are the unmetered resource) rather than being swappable filler for an unrelated topic.

## 4. Dominant verb(s)

Method sentence's main verbs: **score, measure, rank, combine (via elimination), audit, freeze**. `isolate`/`meter` also appear in paper.md's own Step 3 self-audit framing of this same idea. None of these is in the LLM-heavy connecting-verb cluster (*integrate, unify, merge, adapt, combine-as-glue, leverage, bridge, reconcile*) — note that "combine" here is qualified by a specific mechanism ("via elimination of verified-incorrect answers"), not a bare connecting verb standing in for an unspecified fusion, which is the distinction the rubric asks for. `measure`, `audit`, and `freeze` are neutral, task-specific verbs; `rank` and `score` are the same. No instance of *integrate/unify/merge/adapt/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **neutral, leaning human-heavy** (via `isolate`/`meter` in the paper.md framing this idea inherits).

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (1 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (score/measure/rank/combine-via-elimination/audit/freeze) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 2/Step 3) had *already* run its own informal asymmetry/archetype/bridge-synthesis self-check before this audit even started, explicitly naming and rejecting the nearest bridge-shaped alternative framing ("budget allocation exists for generation, we bring it to verification"). This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote paper.md), and it agrees — same conclusion as the B5.5 audit, reached by an unrelated topic's seed material that also happened to have already run its own Step 0/3 self-check.

One genuine point of friction worth surfacing honestly rather than smoothing over: the `surface_stitching` score of 1 (not 0) reflects a real fact about this idea's lineage — mode share as a signal is not new (Wang et al. 2023), and budget-constrained allocation as a framing is not new (Compute-Optimal-TTS, CaTS) either. What keeps this off the Bridge+Synthesis cell is not that the ingredients are novel, but that the *target* of the metering (verifier calls, not generation calls) and the specific instruments built around that target (the AUROC/CBW measurement, the elimination-aware aggregator, the freeze-then-retest audits) are genuinely new and precisely named, rather than the ingredients being glued together with a connecting verb and no further mechanism. This is exactly the "verb choice and specificity reinforce each other" pattern `archetype-verbs.md` describes for `replace`/`decouple`-style human-authored ideas, applied here to a `meter`/`isolate`/`audit` cluster instead.

The practical implication for the other topics in this batch: this pass (🟢, no manufactured flag) should not be read as "every topic in the set will pass automatically" — the auditor is cheapest to run per topic, right after Stage 2/5 confirm, before committing to a full paper draft, precisely because a different topic's seed material might not have run its own Step 0/3 self-check as thoroughly as this one and B5.5 both happened to.
