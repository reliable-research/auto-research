# Pengsida Stage Review — B7.2

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** the final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize. Stages 1–4 below are checked against the confirmed `discussion_trace.md` stage outputs; Stage 5 (Writing) is checked against the first assembled draft of `paper_draft.md`. Two REVISE findings fired and were applied (see "Fixes applied"); the draft in `paper_draft.md`/`.tex`/`.pdf` already reflects them.

## Archetype classification (done first, per `archetypes.md`)

**Analysis / Finding.** The core question is "we ask how often / how fast a phenomenon (poison persistence) occurs, and whether a policy amplifies it" — a characterization, with **no new pipeline proposed as a fix**. The apparatus (censoring-aware survival estimator, behavioral acceptance probe, policy-as-treatment contrast, competing-risks decomposition) is the *analytical instrument that makes the phenomenon observable as a rate*, not a method pitted against baselines to win. This matches `study_type: empirical` from Stage 1 and the topic's `[证据]` (evidence) label. Stage 3 ("Method") and Stage 4 ("Experiments") below therefore use the **Analysis/Finding** column of the archetype table — Stage 3 asks "is each inferential step licensed?", Stage 4 asks "is the finding falsification-tested, not merely correlated?" — not the default method-paper ablation bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why (quoting the confirmed draft):** The problem clears the "so what?" test before any method appears. The framing is first-principles, not a patch: the root asymmetry is stated as "the persistence of memory poisoning is reported only as a fixed-checkpoint binary … that … conflates a claim's literal removal with the end of its behavioral influence" — an attack on why the current measurement *cannot even ask the right question*, not a tweak to it. The stakes are concrete and current, not a generic AI-importance appeal: "operators increasingly rely on 'it will get summarized/consolidated away' as an implicit, free mitigation," and the consequence is named — "the policy chosen for utility is silently a security liability, and the checkpoint labeled repair is an amplification step." Importance holds (a live, catalogued agent risk with a named fast-follower incumbent, MemSecBench); the problem is open (no one estimates a hazard or treats the policy as a manipulated variable); feasibility is real (the minimal experiment reuses published attacks/defenses as fixed treatments — no new attack needed). The Einstein ratio holds: the motivation spends its energy on why the checkpoint measurement is the wrong instrument, not on the cleverness of survival analysis.

**Note for Stage 2:** Passing here means Related Work must now establish that no prior work has already closed this exact gap — specifically that the nearest neighbor (MemSecBench) does *not* already produce the continuous estimand. Checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The thematic threads are genuinely argued, each ending on a problem-tied limitation rather than a generic one (e.g. the persistence-benchmarks thread ends "reports persistence as a fixed Write–Execute–Forget checkpoint binary … no neutralization time, no hazard, and the memory policy is a fixed part of the benchmark rather than a manipulated variable") — this clears the citation-dump failure mode. **But** the first assembled Related Work never states, in one place, which single prior work is the *closest* competitor and confronts it head-on. The discussion trace's Stage-3 refiner already did this analysis — MemSecBench is the nearest neighbor and its checkpoint is the *degenerate single-observation-time special case* of this paper's estimand — but that ranking and its delta did not survive into the assembled prose, which left four parallel threads for the reader to rank themselves. Per the Stage-2 bar: "Hiding the method-twin is the fastest way to a desk reject … reviewers find it anyway; confront it first." The reviewer question this invites — "isn't this just MemSecBench with more timepoints?" — must be answered in the section, not left implicit.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence opening the Related Work, naming MemSecBench (and Injection-Execution Dissociation as the second-closest) as the closest prior work, conceding what they share (persistence measurement; the literal-vs-behavioral decoupling), and stating the precise delta plainly: a continuous, censoring-aware *behavioral*-adoption hazard with memory policy as a manipulated treatment, of which their checkpoint binary is the single-timepoint special case.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used, and the one load-bearing inferential hinge is stated explicitly rather than assumed. The chain is: behavioral adoption (not literal presence) is the event → therefore laundering (detector-invisible but behaviorally-active) is scored as *alive*, not neutralized → therefore a rise in the {literal-absent, behaviorally-adopted} cell with policy aggressiveness is *measurable evidence of laundering* rather than a definitional artifact. That hinge — "separating behavioral adoption from literal detectability is exactly what makes laundering observable as its own measurable state" — is the step that licenses every downstream persistence claim, and the draft states it, doesn't assert it by fiat. No orphan machinery: each of the five modules (survival estimator, behavioral probe, policy-treatment contrast, probe validation, competing-risks decomposition) traces to a named sub-problem, and the competing-risks module in particular earns its place by making the laundering claim *specific* (aggressive policy lowers the content-neutralization cause-specific hazard, not the structural one) rather than leaving "persists longer" ambiguous between correction and TTL eviction. The exposure-confound hole that a naive matched-stream design would leave open is caught and closed by the benign tracer being promoted from placebo to the isolating control (discussion trace, Stage 5 major) — the analogue of handling the obvious failure case before it is raised.

**Note for Stage 4:** the discharge test here is not ablation (that is the method-paper bar) — it is whether the finding is falsification-tested rather than merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative? — is well-served structurally. The placebo (RQ on the benign tracer) is a genuine falsification design for the causal reading: if reduced exposure to corrective evidence, not laundering, drove persistence, the matched-salience benign tracer would persist longer too, and the whole causal story would break. And RQ on the competing-risks decomposition is a real attempt to break the laundering claim (if the persistence increase lived in the *structural-eviction* hazard, or in literal retention, the mechanism would be reattributed away from laundering). **But** the first assembled draft's RQ subsections stopped at an "Expected outcome" line without ever stating the converse — the specific observation that would *refute* each expectation. An "Expected outcome" alone reads as a hope; the discipline the discussion trace already carries (each hypothesis's clean-falsification clause — "if half-life is invariant to memory policy, the hypothesis is cleanly falsified") did not survive into the assembled subsections. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ … demand at least one such test" — stated as a check, not implied.

**THE ONE FIX (applied):** Add an explicit **Falsification condition** line to all seven RQ subsections, each stating the concrete statistical observation that would refute that RQ's expected outcome (not a vague negation) — e.g. for the central reversal, "Refuted if the aggressive-vs-minimal hazard-ratio CI contains 1 across the majority of cells (half-life invariant to policy), or if HR > 1 (aggressive policy *shortens* half-life, i.e. the consolidation-as-cleanup intuition holds)"; for laundering, "Refuted if the persistence increase is accounted for by rising literal-presence (retention), with the laundering cell flat across policy levels."

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** The reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Autonomous agents that persist across sessions now keep a long-lived memory…" / "Yet a security question about that memory is measured with an instrument that cannot express its answer…" / "The nearest prior work approaches this from an adjacent angle…" / "Turning persistence into a measurable rate surfaces its own difficulties…" / "Our design turns each of these obstacles into a specific measurement choice…" / "We evaluate this design across…") reconstructs the whole five-move arc (problem → gap → nearest prior work + shared limitation → why it is hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is reused consistently in title and abstract: "the memory-management step the field scores as repair is, under utility-improving policies, a persistence-amplifying laundering step." The Conclusion names a real forward-looking limitation (the behavioral-adoption event is defined per attack family, so a claim that steers behavior only in rare, unprobed contexts could read as neutralized when it is dormant — pointing toward adaptive probe design) rather than recapping the abstract at the same altitude. Archetype-appropriately, the quotable contribution is a *finding/claim*, not a pipeline.

---

## Fixes applied

1. **Stage 2 fix** — added an explicit nearest-neighbor sentence opening the Related Work, naming MemSecBench (and Injection-Execution Dissociation) as the closest prior work, conceding the shared ground (persistence measurement; literal-vs-behavioral decoupling), and stating the delta: a continuous censoring-aware behavioral-adoption hazard with memory policy as a manipulated treatment, subsuming their checkpoint binary as the single-timepoint special case.
2. **Stage 4 fix** — added a **Falsification condition** line to each of the seven RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), each stating the concrete refuting observation, then recompiled `paper_draft.pdf`.

Both fixes are reflected in the current `paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list. No STOP fired at any stage; no hypothesis or contribution wording was strengthened by either fix (the nearest-neighbor sentence concedes ground, and the falsification lines only make pre-existing expected outcomes breakable).
