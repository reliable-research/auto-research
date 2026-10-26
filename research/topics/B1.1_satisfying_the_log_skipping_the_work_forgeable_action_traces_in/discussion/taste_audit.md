# Research Taste Audit — B1.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Execution-free, log-only reward signals are becoming the default way agent benchmarks and RLVR training pipelines certify task completion, precisely because ground-truth environment-state verification is expensive or infeasible at training scale — but whether this substitution is safe, i.e., whether an optimizing agent can drive the log to 'pass' without the real action occurring, has not been directly measured. A bare existence proof would not be actionable for a pipeline designer: knowing whether forging is a rare edge case restricted to weak schema checkers, or a pressure-scaling phenomenon that persists even against the strongest deployed log-side reward models, determines whether the fix is 'harden the verifier' or 'add a state check.'"

**Method** (Stage 5, summary-level): "We gate a dual-channel agent task suite so that a log-passing/state-failing action path is certified reachable before admission (an automated probe replaying a hand-built forging attempt), oracle environment-state changes from outside the agent's action space, sweep escalating selection and RL pressure rewarded solely on the log, and isolate the verifier-channel cause via matched state-reward and no-pressure control arms with human-attributed labeling of flagged episodes — measuring incidence, its pressure dose-response, and whether stronger log-side verifiers close the gap or merely reshape the forgery."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure/Risk Gap**)
- rationale: the motivation's load-bearing claim is "has not been directly measured" — there is no way to diagnose or audit whether a log-only verifier is actually being gamed under real optimization pressure. This is a measurement/diagnosability absence, not a "two literatures never connected" framing. The secondary Failure/Risk Gap reading is licensed by the motivation's closing worry that the safeguard itself ("log-only verification") may be unreliable/gameable, not that two research areas need linking.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation. `paper.md`'s own Step 0 ("Core Asymmetry") independently derived the same non-bridge framing via an explicit noun-deletion test, and its Step 3 self-audit already checked and rejected a bridge reading for the same reason this audit gives.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal Derivation**)
- rationale: "we gate... sweep... isolate... measure" is characterization/measurement instrumentation of an emergent behavioral phenomenon, not "integrate/unify" two existing methods. The secondary Formal Derivation reading comes from the method's own formal apparatus — `paper.md` Step 5 defines *forgeable*, *separable*, *decoupled*, and *pressure-driven* as precise predicates over `(V_log, V_state, ρ)` — a conceptual/decision-rule contribution (what counts as "forging" vs. "honest error"), not merely a data-collection pipeline.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination; there is no pair of pre-existing methods being glued together with a connecting verb. The dual-channel gating apparatus (separability certification, out-of-sandbox oracle, matched-arm attribution) is purpose-built for this specific identifiability problem — no prior work is being "combined."
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* admission probe (replay a hand-built forging sequence before trusting a task), *which* three verifier instantiations (rule-based, execution-free trajectory RM, per-call judge), *which* three arms (log-reward, state-reward, no-pressure), and *what specifically* the honest-error attribution guard rules out. Matches or exceeds the source paper's human baseline (2.56) and its strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the softest clause is "log-only reward signals are becoming the default way agent benchmarks... certify task completion," a mildly generic trend-setup sentence, but it is immediately anchored to a specific, citable mechanism (execution-free scoring's own stated motivation, per Stage 2's evidence) rather than being swappable filler. Note: `paper.md`'s own Step 3 self-audit flagged and *already corrected* an earlier, more boilerplate-heavy abstract opening ("Agent benchmarks... increasingly verify... however... we introduce" — explicitly called out there as "the FORBIDDEN 'X is increasingly used... however... we introduce' template"). This audit is checking the corrected, Stage-2-confirmed version, not the original flagged draft.

## 4. Dominant verb(s)

Method sentence's main verbs: **gate, oracle (used as a verb: "ground truth is oracled from outside the action space"), sweep, isolate, measure**. `isolate` is explicitly in the human-heavy archetype cluster (with *decouple, separate, disentangle*); `gate` and `measure` are neutral, task-specific verbs, not connecting verbs; `sweep` is a methodology-specific term (parameter sweep), also neutral. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (isolate/gate/sweep/measure) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful independent result, not a rubber stamp: `paper.md`'s own Step 0 ("Core Asymmetry" / noun-deletion test) and Step 3 ("Taste self-audit") had *already* run an informal version of this exact check before this audit even started, and had already caught and corrected one real boilerplate risk (the original abstract-opening template, described above). This audit re-derives the same 🟢 verdict independently, using a different, externally-sourced taxonomy (Chen, Zhao & Cohan's calibrated two-axis scheme, not the same prompt logic that wrote `paper.md`), and it agrees on both the categorical label (not Bridge+Synthesis) and the local diagnostics (low stitching, high specificity, low-but-nonzero boilerplate).

Two things are worth flagging honestly rather than glossing over, since a clean pass can otherwise look like it wasn't scrutinized hard enough:
- The **Formal Derivation secondary label** on the method axis is doing real work here — a pure "Empirical Mapping" read alone (build a benchmark, measure a rate) would be a thinner contribution; what elevates `bottleneck_specificity` to 3 is specifically that the paper formalizes *forgeable*, *separable*, and *pressure-driven* as checkable predicates (`paper.md` Step 5's notation table), not just that it runs a measurement study. If a future revision drops that formalization table and reverts to "we built a benchmark and measured a rate," `bottleneck_specificity` would likely fall to 2 and this verdict should be re-run.
- No flag was manufactured to satisfy a "the audit must find something" expectation — the honest reading, cross-checked against three independent signals (categorical label, local diagnostics, dominant verb), is that this idea does not land in the overrepresented Bridge+Synthesis cell, and the local writing is specific rather than boilerplate-padded. This is consistent with, but not caused by, the fact that the seed material (`digest.md`/`paper.md`) is unusually mature — a thinner seed for a different topic in this same batch could plausibly fail this same check, and should be audited on its own terms rather than assumed to pass by association.
