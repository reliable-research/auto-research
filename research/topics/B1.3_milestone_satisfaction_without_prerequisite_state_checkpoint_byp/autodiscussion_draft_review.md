# B1.3 Autodiscussion Draft Review — "Unearned Checkpoints" (room 70be6a8a)

> Reviewer pass 2026-08-14. Inputs: `research-report.md`, `experiment-spec.md`, `paper-draft.md`
> (completed_jobs_dirs/ZB1.3...--70be6a8a) audited against `discussion.md` (binding design doc,
> Tier-2 / section-sized positioning) and the seed `README.md`. Room closed with 2 unresolved
> MAJOR critiques (inferred in §6). Citation sweep: WebSearch unavailable this session; all
> checks done via the arXiv export API (id_list + one title search) — a narrower sweep than
> usual, noted per item.

---

## 1. Architecture of the draft (what it actually proposes)

Three estimands, kept strictly separate: **P1** — task-level adversarial bypassability of a
frozen milestone battery under equal-budget, score-guided reorder / skip / direct-injection
beam searches, qualified post hoc by a milestone-disjoint **Transition Provenance Contract
(TPC)** certifying broken provenance ∧ terminal incoherence; **P2** — run-level natural
incidence of unearned checkpoint credit in neutral-prompt agent rollouts, adjudicated blind
against the same TPC; **C** — compositional insufficiency: reorder/skip-only bypasses on tasks
whose checkpoints are first probe-qualified as individually truthful, so the failure is
attributable to prerequisite-blind composition rather than checker false positives. Controls:
aggregate-budget-matched valid-action fuzzing (for P1), topologically-valid complete-block
controls (oracle soundness / V rate), uniform vs dependency-guided mutation (for C). Rigor
machinery: sealed candidate manifests, budget ledgers, blinded double adjudication with
Krippendorff's α gates, preregistered power simulations, mixed-effects chain-length model.
Scale: a 600-task attack cohort **harvested from public agent benchmarks**, a nested 400-task
neutral cohort (4,000 rollouts), and a 600-task probe-eligible cohort with 800 mutation/control
traces per task. The paper-draft is a plan-style paper (no results), spec is implementation-grade.

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|--------------|-------|--------|
| N1 | Milestone batteries can award full credit for oracle-incoherent end states; measure latent bypassability (P1) | **HackDetect** (Shao et al., arXiv:2607.22368, 2026-07): post-hoc audit of *observed* shortcut engagement + Mislead gap across 15 benchmarks, 2,385 traces; **ABC** (Zhu et al., arXiv:2507.02825): outcome-validity checklist | Latent (constructed) bypassability of *prerequisite structure* specifically, with equal-budget strategy comparison; HackDetect audits what agents already did, ABC audits practices not attack surface | **Defensible, must position vs HackDetect explicitly** — draft does cite it; delta is real but the "nobody measures unearned credit" framing must be softened |
| N2 | Compositional insufficiency C: every check individually truthful, composition still unsound (reorder/skip) | REVEAL (ACL 2024, inverse direction — chain pass hides step invalidity); MATP (arXiv:2512.23511) and CodeReproducibilityGap (arXiv:2512.22387) share local-signal-vs-disjoint-oracle pattern, no DAG / no adversarial construction | No twin found: truthful-local-checks + prerequisite-DAG + terminal-oracle attribution is B1.3's own axis (matches discussion.md Stage 3) | **Novel — the sharpest claim; the draft's best conceptual contribution** (crisper than discussion.md's version) |
| N3 | Neutral-prompt natural incidence P2, separate from constructed attacks | HackDetect again (real traces, 67% exposure in some suites); SpecBench (arXiv:2605.21384) measures reward hacking of long-horizon coding agents against spec-based checks | Prerequisite/provenance-specific incidence with denominator hygiene and no attack prompting | **Overlapping-but-distinct; needs the 2026 neighbors cited to survive review** |
| N4 | TPC as milestone-disjoint provenance/terminal oracle formalism | BPM / process-mining conformance checking (ordering constraints over event logs — mature field, flagged in discussion.md, absent from draft); τ-bench-style DB-state checks | Applying conformance-style order checking as *measurement instrument* for benchmark validity, not as a proposed verifier | **Fine if BPM prior art is acknowledged; currently reinvents terminology** |
| N5 | Single-milestone degenerate case = insufficient tests | **UTBoost** (arXiv:2506.09289) already shows SWE-bench test insufficiency flips leaderboard entries | B1.3 generalizes to N-milestone DAGs | Must cite; currently missing |

## 3. Consistency vs discussion.md (the binding design doc)

**Verdict: silent scope inflation — the sibling failure signature, in aggravated form.**
discussion.md's audit positioning is *binding*: Tier-2, section-sized, CPU-only, "biased toward
smallness, mechanical ground truth, and a clean merge path" into B1.2's FSE paper. The draft
instead specifies a flagship preregistered program:

| Binding decision (discussion.md) | Draft package | Status |
|---|---|---|
| 30 hand-authored pilot tasks, 2 domains, certified block boundaries, trivial-solution audit | 600 tasks harvested from a census of public benchmarks + 600-task probe cohort | **Inflated ~20×; harvesting also imports the task-bug problem SP1's audit was designed out of** |
| ~1,080 neutral rollouts, $200–800 API class | 4,000 neutral rollouts + 720,000 constructed search traces + ~480,000 mutation/control traces | **Inflated; violates the cheapness contract** |
| D0 grading survey (10–15 benchmarks) = Table 1, motivation evidence, [VERIFY] resolution, t1 fidelity audit | Dropped entirely; motivation anchored on AutoTool/MedAI, which the draft *itself concedes* do not evidence milestone-grading prevalence | **Dropped — the single highest-value page per the critic** |
| Visibility factor (checkpoint structure shown vs goal-only) — the one mechanism knob, bridge to B1.1's H-obs | Absent | **Dropped** |
| Unearned-partial-credit inflation metric (both denominators) | P2 run-level only; no partial-credit score inflation | **Dropped** |
| Primary P1 analysis = checker-type × strategy resistance matrix (T3 reframed; actionable for benchmark designers) | Primary = directed-vs-fuzzing risk difference; no checker-type breakdown | **Dropped** |
| Pilot gates G1–G3, standalone-vs-B1.2-merge decision rule, calendar (freeze 8-29, decide 9-18, FSE 10-2) | No gates, no merge path, no calendar | **Dropped** |
| 100% human adjudication at pilot scale (defuses SP3) | Sampled double-coding (N₂≥300, N₄≥400) with α≥0.80 power simulations | Rigorous but only makes sense at the inflated scale |
| Topology (depth, fan-in) regression | Chain-length model kept for P2 only | Partial |
| P1/P2 claim discipline; equal budgets; lower-bound framing; oracle disjointness; injection = B1.1-adjacent (excluded from C) | All faithfully kept; C formalizes the Stage-3 strategy-boundary repair | **Kept — the conceptual core is faithful and improved** |

## 4. Citation audit (arXiv API; zero-confabulation check)

| Citation in draft | Verified? | Notes |
|---|---|---|
| AutoTool, arXiv:2512.13278v2 | ✅ real (Zou et al., 2025-12) | Real but a *weak motivation anchor* — generic agent paper, no milestone grading |
| MedAI, arXiv:2512.11682v2 | ✅ real (Cofala et al., 2025-12) | Same — CURE-Bench competition report; odd anchor choice |
| ABC / Zhu et al. "2026" | ✅ real, arXiv:2507.02825 (2025-07) | Year off (v1 July 2025); id missing from draft |
| TheAgentCompany, Xu et al. | ✅ real, arXiv:2412.14161 | Correct |
| HackDetect, Shao et al. | ✅ real, arXiv:2607.22368 (2026-07) | Correct + closest neighbor; id missing from draft |
| "Howe et al., Defining and Characterizing Reward Hacking" | ⚠️ real paper, **wrong first author** | arXiv:2209.13085 is **Skalse**, Howe, Krasheninnikov, Krueger (NeurIPS 2022) |
| SpecBench arXiv:2605.21384 | ✅ exists (2026-05) | **Missing from draft** |
| Countdown-Code arXiv:2603.07084 | ✅ exists (2026-03) | **Missing** — milestone-reward RL stake |
| RHB arXiv:2605.02964 | ✅ exists (2026-05) | **Missing** |
| Verification Horizon arXiv:2606.26300 | ✅ exists (2026-06) | **Missing** |
| UTBoost arXiv:2506.09289 | ✅ exists (2025-06) | **Missing** — degenerate single-milestone case |
| Twins: CodeReproducibilityGap 2512.22387, MATP 2512.23511, REVEAL | ✅ first two verified via API | **All three cache-verified twins from discussion.md missing** |

Zero confabulated citations (sibling signature holds) — but 1 misattribution, 2 missing ids,
and **8+ missed load-bearing neighbors** including all five 2026 verifier-gaming papers.

## 5. Gap to implementation

The spec is unusually concrete (schemas, budget ledgers, sealing, 28 ordered tasks) but its
"Inputs You Must Provide" section **externalizes the entire hard part**: per-benchmark
`TaskAdapter`s; per-task hand-authored TPC YAML, prerequisite DAGs, local-state oracles,
probe strata + generators — *for 600 harvested tasks*; trained human adjudicators; restorable
sandboxes for every suite. SP3 (oracle correctness — discussion.md's named hard part with
asymmetric error danger) is thereby assumed as input, not solved. The sampling frame itself is
speculative: no evidence that hundreds of public tasks with ≥2 checkpoint credits *and
documented prerequisite edges* exist. Compute: ~1.2M sandbox executions + 4,000 agent runs +
thousands of human labels — months and $10k–100k class vs the pilot's hours and $200–800.
No code exists. The feasible path is discussion.md's 30-task pilot instantiating the same
three estimands (P1 feasibility, P2 two-denominator incidence, C) at 1/20 scale with 100%
adjudication, gates, and the B1.2 merge route.

## 6. Verdict + top-3 fixes + inferred unresolved MAJORs

**Verdict: REVISE (conceptual core sound, packaging non-compliant).** The P1/P2/C separation,
the TPC, C's truthful-local-checks qualification, and the fuzzing/valid-order controls are a
genuine sharpening of discussion.md. But the draft silently inflates a section-sized Tier-2
study into an unexecutable flagship program, drops every deliverable that made the study cheap
and evidence-grounded (D0, visibility factor, unearned-credit metric, resistance matrix,
gates, merge path), and misses the 2026 neighbor literature it must be positioned against.

**Inferred unresolved MAJOR-1 (scope/feasibility):** the 600-task × three-cohort preregistered
design cannot be executed under any Tier-2 budget — TPCs, probes, oracles, and adapters are
"inputs you must provide" for hundreds of tasks whose existence is unverified — and the room
never reconciled the spec's scale with the binding section-sized positioning.
**Inferred unresolved MAJOR-2 (motivation grounding):** with D0 dropped and AutoTool/MedAI
explicitly conceded as non-evidence, the prevalence premise ("prerequisite-blind milestone
grading is widespread") — and hence the who-cares chain — rests on nothing the draft contains.

**Fix 1 — Rescope to the pilot contract.** 30 hand-authored DAG tasks (2 domains, depth 3–8,
fan-in 1–3, block boundaries, trivial-solution audit), equal-budget P1 samplers + fuzzing
control, 1,080 neutral rollouts (3 models × 3 seeds × 2 budgets × 2 visibility), 100% human
adjudication, gates G1–G3, standalone-vs-B1.2-merge decision rule, scale-up gated post-Oct-2.
Keep C, the valid-order control, and TPC formalism at pilot scale — they port cleanly.
**Fix 2 — Restore the evidence spine.** D0 grading survey as Table 1 + motivation; visibility
factor; unearned-partial-credit metric; checker-type × strategy resistance matrix as primary
P1 output; topology odds for P1 and P2.
**Fix 3 — Citation repair.** Correct Skalse attribution; add arXiv ids; add SpecBench,
Countdown-Code, RHB, Verification Horizon, UTBoost, the three verified twins, BPM conformance
checking; state the HackDetect delta (latent-vs-observed) in one explicit paragraph.

Applied in `paper-draft.revised.md` (this directory).
