# Research Taste Audit — B1.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "The assumption that stacking a second, independently-sound check onto a verification gate can only tighten it — never loosen it — is already load-bearing in deployed LLM-agent and code-verification pipelines (reward chains, flawed-positive detectors, execution-free reward models, guardrail aggregation), yet no cited system and no prior account of proxy-reward hacking actually tests whether the *composition step itself*, as distinct from each stacked check, preserves soundness — every one of them validates the added check by its own individual tightening effect or by end-task performance gains, never by examining the combined gate's own soundness."

**Method** (Stage 5, summary-level): "We construct matched task variants where each single verifier's soundness is exhaustively, non-vacuously certified before composition; stamp every certificate with the budget it was earned at and mandatorily re-attack any 'emergent' shortcut's single-gate variants at 10× that budget before accepting the label; apply an identical budget-matched adversarial attacker to single and composed gates across a benchmark/verifier-pair grid to convert a hand-built existence counterexample into a prevalence estimate; and classify every discovered shortcut with an ablation triple plus a structural taxonomy, regressed on a coverage-complementarity score computed from the two verifiers' mutant-kill sets."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Puzzle / Contradiction** (secondary: **Evidence Gap**)
- rationale: the motivation's load-bearing move is an explicit *contradiction* — extensionally, the AND/OR of two sound acceptors on a fixed task is trivially sound (a provable fact), yet in the facet-relative regime real pipelines actually occupy, composition is claimed to destroy exactly the soundness precondition it's assumed to preserve. This is the textbook "surprising, counter-to-expectation" trigger for Puzzle/Contradiction, not a diagnosability complaint alone. The secondary Evidence Gap reading is licensed by "no cited system... actually tests" — there is genuinely no benchmark/audit for the composed gate's own soundness, which is the diagnosability half of the claim.
- Explicitly **not** Bridge Opportunity: there is no "reward-hacking theory and verifier-composition practice have developed in isolation" clause anywhere in the motivation. The paper's own seed material (`paper.md` Step 3) independently ran this exact self-check and rejected a bridge reading ("Bridge check: FAIL-risk framing would be 'we connect verifier theory with composition analysis.' Rejected... PASS as framed.").

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we construct... certify... re-attack... attack... classify... regress" is measurement instrumentation and characterization — building a benchmark/audit procedure for a previously unaudited property, not "integrate/unify" two existing methods. The secondary Formal Derivation reading is licensed by the facet-relative soundness formalization itself (`Sound(V,t,Π)`, the shortcut/emergent/complementarity definitions) and the four-class structural taxonomy — both are conceptual/formal contributions in their own right (CO3), not just measurement plumbing.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing tools being glued with a connecting verb. The instrument (bounded-DSL construction, budget-stamped certification with mandatory re-attack, matched adversarial search, ablation-triple classification) is purpose-built for this specific identifiability problem, and every component exists because a specific confound (vacuity, budget asymmetry, shared blind spots) demanded it.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* Boolean composition rules (AND/OR specifically, not aggregation in general), *which* re-attack multiplier and why (10×, tied to the specific budget-symmetry confound it tests), *which* four taxonomy classes (named and distinguished: OR-weak-branch, AND-constraint-displacement, facet-split, threshold-interaction), *which* complementarity statistic (1 − Jaccard over mutant-kill sets, not "some measure of overlap"). Matches the source paper's human baseline (2.56) and its strongest tested models (2.3–2.6).
- `boilerplate` = **0** — every clause in the extracted motivation and method ties to a specific mechanism or a specific cited system's own stated validation gap (RewardChain/FAPO's end-task-gains-only validation; R2-Guard's own documented under-estimation; CorrelatedProxies' ensembling-doesn't-help observation). There is no generic "X has attracted increasing attention, however, prior work suffers from limitations" scaffolding anywhere in the two sentences audited — the paper's own Step 3 self-audit explicitly forbids exactly that template for its abstract, and it shows.

## 4. Dominant verb(s)

Method sentence's main verbs: **construct, certify, re-attack, attack, classify, regress**. None of these appear on the LLM-heavy list (integrate, unify, merge, adapt, combine, leverage, bridge, reconcile). `classify` and `regress` are neutral, task-specific verbs; `certify` and `re-attack` are domain-specific verbs invented for exactly this measurement problem, not generic connecting verbs. No verb here is drawn from the human-heavy cluster either (replace, decouple, isolate, disentangle) — this idea's verb profile is genuinely its own, neither template.
Archetype family: **neutral** (leaning human-heavy in spirit — "certify then re-attack to attribute" is functionally an isolation/attribution move, close to the *isolate/disentangle* family, even though the literal verb differs).

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 0 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (construct/certify/re-attack/attack/classify/regress) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks, and the diagnostics are at or beyond the human baseline on every axis scored.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp, for the same structural reason a prior audit on a different topic (B5.5) in this same batch was: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and that self-check was explicit about rejecting the bridge/synthesis template ("Not a bridge: it names a violated closure property... not a connection between two fields"). This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), run cold against the confirmed Stage 2/Stage 5 outputs rather than against `paper.md`'s own self-audit language — and it agrees on every axis, including the two diagnostics (`surface_stitching`, `boilerplate`) that `paper.md`'s own self-audit never scored numerically.

One honest note on where this idea sits relative to the taxonomy's calibration data: its Opportunity Pattern (Puzzle/Contradiction) is a different primary label than B5.5's (Evidence Gap) — worth recording so a reader of both audits in this batch doesn't assume every topic lands in the same cell. The two ideas share a clean pass, but for structurally different reasons: B5.5's strength is a diagnosability absence ("this has never been measured"), while B1.4's strength is a genuine logical contradiction ("the naive extensional argument is trivially true, and it is also the wrong argument for the regime that matters"). Both are legitimate, non-Bridge shapes; neither should be read as evidence that this taxonomy always returns 🟢 for topics drawn from this same reverse-digest pipeline — it is cheapest to keep running this audit per-topic, right after Stage 2/5 confirm, rather than assuming a pattern from one or two clean results.
