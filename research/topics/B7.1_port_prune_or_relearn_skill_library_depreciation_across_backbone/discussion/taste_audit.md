# Research Taste Audit — B7.1

> Skill: `research-taste-auditor` (taxonomy/calibration from Chen, Zhao & Cohan, arXiv:2607.01233). Run on the core idea as confirmed at Stage 2 (Motivation) and Stage 5 (Method) of the discussion-loop run in `discussion_trace.md`, **before** paper assembly. Seed maturity note: unlike B5.5, this topic had no `paper.md` Step-0/Step-3 self-audit to lean on — the framing below was constructed during the stages, so this audit is the *first* taste check the idea has received, not a confirmation of one.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed — summary + load-bearing clause): "Every backbone upgrade silently converts an agent's accumulated skill library from a maintained asset into an unaudited liability candidate, and teams currently choose among port-everything, wipe-and-relearn, or ad hoc pruning with no measured basis for any of the three. [...] every skill in the library was acquired under a specific backbone whose failure modes it encodes — a workaround for a weak model's parsing errors, a scaffold for reasoning steps the weak model could not take alone. When the backbone is upgraded, that encoding is silently invalidated, yet the library carries no record of which behaviors were compensations."

**Method** (Stage 5, summary-level): "We freeze a skill library acquired under an older backbone and replay the identical, mechanically-verified task stream under newer backbone generations in paired arms — bare, full-library, token-matched placebo-library, and per-skill leave-one-out masked arms — to estimate each skill's signed change in marginal utility per token; we decompose measured value loss into obsolescence, interference, and cost drag from mechanical trace signatures; and we test whether thresholding the estimates recovers most of an oracle's cost–success frontier at a pre-registered operating point."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the load-bearing motivation clauses are measurement-absence clauses — "no measured basis for any of the three", "the library carries no record of which behaviors were compensations", and the seed's own novelty ledger ("从 framing 到 measured estimand", README line 34). The secondary Failure/Risk reading is licensed by the negative-transfer worry ("if they actively mislead the stronger model — the library becomes worse than nothing"), a reliability risk of current practice, not a two-literatures framing.
- Explicitly **not** Bridge Opportunity, but this deserved a real check rather than a wave-through, because the idea imports economics vocabulary (depreciation, capital goods, amortization) into the agent-skills literature — the surface shape of a bridge move. The check: the motivation nowhere claims "skill-library research and economics have developed in isolation and should be connected"; the economic terms are *operationalized mechanically* (tokens billed, execution outcomes, acquisition ledgers) as names for measured quantities, and the gap claimed is "an assumed quantity has never been measured on this axis" — the S1/S5 shape of guidance.md, not a linking claim. The nearest-neighbor economics paper (Token Economics, arXiv:2605.09104) is cited as *already having made* the conceptual connection, which is precisely why the remaining gap is a measurement gap, not a bridge.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "freeze... replay... estimate... decompose... test whether thresholding recovers" is characterization/measurement instrumentation end to end. The secondary Formal Derivation reading comes from the estimand construction itself (per-skill marginal utility on an activation set, retention ratio with an acquisition-value floor, and the three-way mechanism taxonomy with mechanical signatures) — a conceptual/definitional contribution, but in service of the measurement, not a theory deliverable.

## 3. Diagnostics

- `surface_stitching` = **0** — nothing is glued to anything: no pair of existing methods is combined. The apparatus (frozen-library replay, placebo null instrument, leave-one-out ledger, signature-based decomposition, oracle-normalized sweep) is purpose-built for one identification problem: attributing value change to backbone generation.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* axis (backbone generation as the treatment variable, environment held fixed — deliberately avoiding the occupied axis), *which* quantity (signed change in success-benefit-per-token on the skill's activation set), *which* three confounds the arms remove (context load, invocation propensity, task difficulty), *which* three loss mechanisms with *which* mechanical signatures. Matches the human calibration baseline (2.56) at ceiling.
- `boilerplate` = **1** — mostly load-bearing; the one softish clause is "teams currently choose among port-everything, wipe-and-relearn, or ad hoc pruning", which is a practice claim asserted without a named survey behind it (it is defended in the paper only as the corner-policy structure of the decision space, which is definitional). One point, not two: the sentence could not be swapped into a different paper without rewriting, but it is the least evidenced sentence in the extracted pair.

## 4. Dominant verb(s)

Method sentence main verbs: **freeze, replay, estimate, decompose, test**. `decompose` sits in the human-heavy cluster (with *decouple/separate/disentangle*); `replay`, `estimate`, `test` are neutral task-specific verbs; no *integrate/unify/merge/combine/leverage/bridge* appears in any claim position in either extracted sentence. The motivation's operative verb is *measure* (via "no measured basis").
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** (Evidence Gap × Empirical Mapping) |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (decompose/replay/estimate/test) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires. No reframe pass is required, and none is manufactured — this is an honest clean pass, with the one genuine near-risk (economics-vocabulary import reading as a bridge move) examined explicitly in §2 and found to be an operationalized measurement framing rather than a connecting claim.

## 6. One watch item for the writing stage (not a flag)

The verdict above audits the *idea*. The residual risk is presentational: if the paper's abstract were ever rewritten to lead with "we connect the economics of capital goods with LLM skill libraries", condition 1 would be re-entered by prose alone. The assembled draft leads with the unmeasured-axis claim and the mechanical estimand instead; any future revision that touches the abstract's first two sentences should re-run this audit (trigger mirrors goal.md §3 item 8).
