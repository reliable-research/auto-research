# Unearned Checkpoints: Milestone Batteries That Certify No Coherent End State

> **B1.3 revised draft (2026-08-14).** Compact, registered-report-style empirical study,
> scoped per the Tier-2 audit positioning in `discussion.md`: CPU-only measurement chain,
> a 30-task hand-authored pilot, ~1,080 agent rollouts, 100% human adjudication of candidate
> bypasses, explicit go/no-go gates, and a pre-committed merge path into the B1.2
> verifier-sufficiency paper (FSE, Oct 2) if the standalone trigger is not met.
> Supersedes the room-70be6a8a draft, whose estimand structure (P1/P2/C) is retained but
> whose 600-task multi-benchmark program is descoped as a gated post-pilot extension.

## Abstract

Multi-step agent benchmarks routinely grade trajectories with a battery of independent,
locally-scoped milestone checkers — file-existence and pattern checks, sub-tests,
tool-signature and DB-row comparisons — often with partial credit per checkpoint. These
batteries share a structural premise: passing checkpoint k certifies the work k represents,
including its prerequisites. We study whether that premise holds. A checkpoint-bypass event
is a trajectory that satisfies every milestone checker while a disjoint end-state consistency
oracle certifies that the terminal state is incoherent. We measure two strictly separated
quantities plus one attribution: **P1**, whether the verification *paradigm* admits bypasses —
for each task and strategy (reorder, skip, state-inject), does an equal-budget constructed
trajectory exist that passes the battery and fails the oracle; **P2**, whether real *agents*
collect unearned checkpoint credit unprompted — the adjudicated oracle-failure fraction among
neutral-prompt rollouts the battery scores complete; and **C**, compositional insufficiency —
bypasses in which every awarded checkpoint is individually truthful (reorder/skip only), so
the failure is attributable to prerequisite-blind composition rather than checker error. A
10–15-benchmark grading survey (Table 1) establishes that prerequisite-blind milestone grading
is deployed practice; a 30-task two-domain DAG suite with hand-audited terminal oracles and a
provenance side-channel makes every verdict mechanically re-derivable; pilot gates decide
between a standalone short paper, a section in a companion verifier-sufficiency paper, and a
survey-only null report. P1 sentences predicate only of verifiers; P2 sentences only of agents.

## 1. Introduction

Milestone-wise grading is the workhorse of multi-step agent evaluation. TheAgentCompany
scores tasks with checkpoint lists and partial credit [Xu et al., arXiv:2412.14161]; subgoal
progress rates, key-node checks for web agents, and DB-state/tool-signature checks in
τ-bench-style tool-use suites follow the same pattern (surveyed in §4.1); SWE-bench's
fail-to-pass tests are the degenerate single-milestone case. Milestone signals are also
entering training loops as dense rewards for long-horizon RL, where testbeds already show
verifier gaming emerging under optimization pressure [Countdown-Code, arXiv:2603.07084] and
verification is argued to be the binding constraint on coding-agent reward design
[Verification Horizon, arXiv:2606.26300]. All of these uses assume that passing checkpoint k
certifies the work k represents, *including its prerequisite state*.

This paper asks the narrow structural question behind that assumption: **can a battery of
individually sound, prerequisite-blind milestone checks be satisfied — in order violation
(乱序), by skipping steps (跳步), or by direct state injection (状态注入) — while the task's
end state is incoherent?** We keep two measurements strictly separate, because they support
different claims:

- **P1 (attack surface; agent-free).** A property of the verification paradigm: for each
  (task, strategy), does at least one verifier-passing, oracle-failing trajectory exist within
  a pre-registered, equal-per-strategy construction budget? The headline number is the
  bypassable-task fraction — a lower bound over the sampled construction space. P1 sentences
  predicate only of verifiers ("independent milestone verification admits X").
- **P2 (behavioral incidence).** A property of agents under deployment-realistic conditions:
  among neutral-prompt rollouts that the milestone battery scores complete, the adjudicated
  fraction failing the end-state oracle. P2 sentences predicate only of agents ("agents
  naturally collect unearned credit at rate Y"). No prompt, example, or scoring rule ever
  mentions skipping, faking, or verifier blindness.

A third quantity attributes the failure. **C (compositional insufficiency)** counts only
bypasses in which every *awarded* checkpoint is individually truthful — the checked local
state is genuinely present — yet the composition is unsound because prerequisites never
executed. By construction C excludes state injection, which falsifies the local check itself
and is the adjacent territory of our companion study on evidence forging (B1.1); reorder and
skip are this paper's own axis. This strategy-level boundary is the paper's organizing idea:
*injection breaks a check's truthfulness; reorder/skip break the battery's sufficiency even
when every check is truthful.*

Why now, and why cheap. Benchmarks are moving toward finer-grained milestone grading to fight
sparse signals — the attack surface grows by design — and milestone rewards are entering
training. At the same time the entire measurement chain here is mechanical: hand-authored
tasks, code-only checkers, a disjoint terminal oracle, no LLM anywhere in the truth channel,
CPU-only grading. Every verdict is re-derivable by a reviewer from released code. That is the
design contract of this study, and the reason a section-sized budget suffices.

**Contributions.**
1. A grading survey of 10–15 deployed agent benchmarks (Table 1) documenting grading
   mechanism, partial credit, and prerequisite/ordering enforcement — the evidence that
   prerequisite-blind milestone batteries are current practice, and the fidelity anchor for
   our checker implementations.
2. A feasibility-framed adversarial audit (P1) with equal per-strategy budgets and a
   same-budget valid-action fuzzing control, reported as a **checker-type × strategy
   resistance matrix** — which checker classes resist which bypass strategies — the
   actionable output for benchmark designers.
3. A neutral-prompt incidence protocol (P2) with two pre-registered denominators
   (full-conjunction and partial-credit), an unearned-partial-credit inflation metric, one
   mechanism factor (checkpoint-structure visibility), and 100% human adjudication of every
   candidate bypass at pilot scale.
4. The compositional estimand C with a valid-order control, isolating prerequisite-blind
   composition as the failure cause when every local check is truthful.

## 2. Problem Definition

**Setting.** A multi-step task is a DAG G = (K, E) over milestones k₁…k_N; an edge
(k_i → k_j) means k_i's true state is a prerequisite for k_j. Grading follows deployed
practice: each milestone has an independent, locally-scoped verifier V_k (existence, pattern,
sub-test, tool-signature, DB-row) with no visibility into other milestones' provenance.
Separately, a terminal end-state consistency oracle O_end recomputes the canonical final
state from the task spec and compares it to the actual terminal state by total function
(file-set hash / row-set / output equality). O_end is ground truth; the battery {V_k} is the
paradigm under test. O_end's code is disjoint from every V_k, and oracle inconsistency is
never inferred from milestone outputs.

**Bypass event.** A trajectory τ with (∀k: V_k(τ) = pass) ∧ (O_end(τ) = fail). Strategies:
**reorder** (execute milestone action blocks in an edge-violating permutation), **skip**
(drop prerequisite blocks, keep dependents), **inject** (replace prerequisite blocks with
direct surface-signature writes: touch the file, insert the row, echo the pattern).

**Formal estimands.** Write Sat(τ) = ∏_k V_k(τ) and Inc(τ) = 1 − O_end(τ). For strategy
a ∈ {reorder, skip, inject} let X_{t,a}(B) be the candidate trajectories constructed for task
t by the pre-registered sampler under per-strategy budget B (equal across strategies).

- **P1 (feasibility, lower bound):** the fraction of tasks t for which
  max_{a} max_{τ ∈ X_{t,a}(B)} Sat(τ)·Inc(τ) = 1, with per-strategy and per-checker-type
  breakdowns. "Fraction of constructed traces" is *not* an estimand — feasibility under a
  fixed budget is.
- **P2 (natural incidence, two denominators):** among neutral-prompt rollouts, (i)
  full-conjunction denominator — rollouts with Sat = 1; (ii) partial-credit denominator —
  rollouts whose checkpoint score meets the surveyed benchmarks' crediting convention. P2 is
  the adjudicated fraction of denominator rollouts with Inc = 1.
- **Unearned-credit score:** for any trajectory, U(τ) = (checkpoints passed without
  prerequisite state, per adjudication) / (total checkpoints) — the partial-credit inflation
  a checkpoint-graded benchmark would award.
- **C (compositional insufficiency):** let ℓ_k(τ) = 1 iff the local fact claimed by V_k is
  genuinely true at the state where credit was first issued (adjudicated from the provenance
  side-channel, not from V_k). C is the fraction of tasks with a qualifying bypass under
  a ∈ {reorder, skip} only, additionally requiring ∀k with V_k = pass: ℓ_k = 1. Injection
  bypasses are reported separately and cross-referenced to B1.1, never double-claimed.

**Scope.** Single-agent; domains with a canonical, mechanically recomputable terminal state
(filesystem/coding; tool-use over a service DB); no GUI, live web, robotics, or multi-agent;
English prompts; evaluation-time claims only — training-time reward integrity is an
implication we flag (via Countdown-Code / Verification Horizon) and do not measure.

## 3. Related Work

**Verified structural twins.** Three works share the local-signal-vs-disjoint-oracle pattern
without measuring prerequisite-DAG bypass. AI-Generated Code Is Not Reproducible (Yet)
[arXiv:2512.22387] shows local functional-correctness signals passing while a disjoint
clean-environment reproducibility oracle fails — whole-program unit, no DAG, no adversarial
construction. REVEAL [ACL 2024] verifies CoT chains step-wise because chain-level correctness
masks invalid steps — the inverse direction (global pass hiding local invalidity) on linear
text chains without a stateful environment. Beyond Correctness [MATP, arXiv:2512.23511] uses
a theorem-prover oracle to expose locally-plausible, globally-invalid reasoning — disjoint
oracle, fully observable state, no provenance question.

**Verifier gaming and benchmark validity (2025–2026).** The Agentic Benchmark Checklist
[Zhu et al., arXiv:2507.02825] systematizes task/outcome validity and finds grading errors of
up to 100% relative in existing benchmarks, but does not treat prerequisite-blind composition
as a distinct failure or construct bypasses. UTBoost [arXiv:2506.09289] shows SWE-bench's
tests are insufficient — our degenerate single-milestone case — by augmenting test cases;
we generalize the question to N-milestone DAG batteries. HackDetect [Shao et al.,
arXiv:2607.22368] is the closest neighbor: a post-hoc audit attributing *observed* shortcut
engagement and score inflation (Mislead gap) across 15 agent benchmarks. Our delta is
direction and object: HackDetect audits what agents already did to scores; we measure the
*latent* bypassability of the prerequisite structure itself (P1, agent-free, equal-budget
construction), separately estimate neutral-prompt incidence with a mechanical rather than
LLM-judge truth channel (P2), and attribute failures to composition with truthful local
checks (C). SpecBench [arXiv:2605.21384] measures reward hacking of long-horizon coding
agents against specification checks, and RHB [arXiv:2605.02964] benchmarks tool-use exploit
rates; both study agent behavior against one proxy signal, not the compositional sufficiency
of a checkpoint battery over a prerequisite DAG. Countdown-Code [arXiv:2603.07084] and
Verification Horizon [arXiv:2606.26300] motivate the training-time stake we scope out.

**Reward hacking backdrop.** Skalse, Howe, Krasheninnikov & Krueger formalize proxy
hackability [arXiv:2209.13085, NeurIPS 2022]; Pan, Bhatia & Steinhardt (2022) and Krakovna
et al.'s specification-gaming catalogue supply the general proxy-gap logic. Our claims are
about verifier *structure*, not optimization pressure.

**Process conformance checking.** Checking event logs against process models with ordering
constraints is mature machinery in BPM/process mining (conformance checking over partial
orders). We borrow the vocabulary deliberately: the machinery exists; the *measurement* of
agent-benchmark checkpoint-bypass rates does not.

**Family boundary.** B1.1 asks whether a single check's evidence channel can be forged
(log vs. state diff, per-action grain); B1.2 asks whether one artifact's visible test suite
is adequate (mutation ground truth); B1.3 asks whether a *battery* of individually sound,
prerequisite-blind checks certifies a coherent end state — and answers by construction (P1)
and by observation (P2) that it need not. Injection at a single node is B1.1's texture and is
flagged as such wherever reported.

## 4. Method

![Figure 1: B1.3 study architecture — grading survey (D0), 30-task DAG suite with milestone checkers and disjoint end-state oracle, three bypass strategies, two measurement arms (P1 agent-free feasibility, P2 neutral-prompt incidence) plus the compositional estimand C, 100% human adjudication, and pilot gates deciding standalone vs. B1.2-section vs. park.](architecture.svg)

*Figure 1: Study architecture. Left: the D0 grading survey grounds checker types and the G2
floor. Center: each task is a prerequisite DAG whose milestones are graded by independent
local checkers V_k, with a disjoint end-state coherence oracle O_end as ground truth and a
harness-level provenance side-channel for adjudication. The bypass taxonomy (reorder / skip /
inject) feeds two strictly separated measurement arms — agent-free P1 feasibility under equal
budgets with a fuzzing control, and neutral-prompt P2 incidence over 3 models × 2 budgets ×
2 visibility × 3 seeds — whose candidate bypasses are 100% human-adjudicated into {genuine
bypass, oracle error, task bug}, yielding the resistance matrix, incidence estimates, C, and
the unearned-credit distribution. Right: gates G1–G3 route the result to a standalone short
paper, a 1.5-page section of the B1.2 FSE paper, or a survey-only report.*

### 4.1 D0 — Grading survey (Table 1)

We read the grading code of 10–15 deployed multi-step agent benchmarks (candidate list:
TheAgentCompany, AgentBoard, WebCanvas, τ-bench / τ²-bench, BFCL v3, ToolSandbox, OSWorld,
SWE-bench, plus 2026 additions surfaced during harvest) and tabulate: grading mechanism,
partial credit (formula), and any prerequisite/ordering enforcement. Hypothesis: most
checkpoint-graded benchmarks verify milestones independently and enforce no provenance. D0
(i) evidences the motivation premise, (ii) fixes our checker-type distribution (construct
validity by construction), and (iii) grounds the G2 floor (§5). If D0 *fails* — most
benchmarks turn out prerequisite-aware — the topic dies cheaply at the survey stage and D0
publishes alone; a legitimate Tier-2 outcome.

### 4.2 Task suite (M1)

Pilot: 30 hand-authored DAG tasks, two domains. (i) Filesystem/coding: milestones like
"config generated" → "build artifact present" → "tests recorded passing" → "package
assembled"; V_k = existence/pattern/sub-test checks; terminal state = deterministic file-set
hash + program output. (ii) Tool-use/DB: service-state waypoints (row created → linked →
invoiced); V_k = tool-signature/DB-row checks; terminal state = canonical row-set. Topology
varied by design: chain depth 3–8, fan-in 1–3. Each task ships (milestones, edges, V_k specs,
terminal spec, **explicit milestone action-block boundaries** — required by the reorder/skip
samplers). **Admission rule:** a task enters the suite only after a trivial-solution audit —
no honest degenerate path may satisfy the battery while leaving the terminal state incoherent;
discovered trivial solutions are task bugs, fixed before data collection. Procedural scale-up
to 200–300 tasks over the same schemas is *gated* (§5), never default.

### 4.3 Truth channel: oracle + provenance contract (M4)

Per task we author a compact **transition provenance contract**: the prerequisite DAG, each
milestone's block-completion events, and the terminal predicates O_end recomputes. O_end
re-derives the canonical terminal state from the task spec, disjoint in code from every V_k;
no LLM anywhere in the truth channel; snapshots taken by the harness outside the agent
sandbox. A **provenance side-channel** — harness-level command/file-access logging per
milestone, outside the sandbox boundary — records which actions touched which artifacts. It
is instrumentation for adjudication and the unearned-credit metric, never a verifier
(provenance-aware verifiers are the implications paragraph, i.e., future work). Because a
buggy oracle silently manufactures evidence *for* the thesis (asymmetric error), the pilot
defuses oracle risk by scale: **100% human adjudication of every candidate bypass**
(Sat = 1 ∧ Inc = 1), two annotators, rubric outcomes {genuine bypass, oracle error, task
under-specification}; the oracle false-inconsistency rate and task-bug rate are reported as
calibration by-products. Scale-up would adjudicate a stratified sample ≥ max(100, 20%).

### 4.4 P1 — bypass construction (agent-free, M3)

Per (task, strategy), a pre-registered sampler with **equal per-strategy budgets**: reorder
samples edge-violating permutations of action blocks; skip drops prerequisite blocks keeping
dependents; inject replaces prerequisite blocks with direct surface-signature writes. Each
constructed trajectory executes in the sandbox; we record (∀V_k, O_end, provenance). A
same-aggregate-budget uniform valid-action fuzzing arm controls for search volume: P1 must
reflect structured bypassability, not the background rate of stumbling into incoherence. All
rates are lower bounds over the sampled space. Primary analysis: the **checker-type ×
strategy resistance matrix** (which checker classes admit which strategies) — injection is
expected near-ceiling against existence/pattern checkers, an anticipated, non-headline
result; strategy ranking is descriptive. For C, qualifying reorder/skip bypasses additionally
require every awarded checkpoint locally truthful (ℓ_k = 1, adjudicated from provenance), and
a **valid-order control** (all blocks retained, topologically valid orders, same budget)
verifies that incoherence does not arise under honest composition — otherwise the oracle or
the task, not the battery, is at fault.

### 4.5 P2 — natural incidence (M5)

30 tasks × 3 agent models (API + open-weight mix) × 3 seeds × 2 step-budget conditions
(comfortable / tight) × 2 **visibility** conditions (checkpoint structure + partial-credit
scoring shown as ordinary task context, as real benchmarks do vs. task goal only) = **1,080
rollouts** (API cost class $200–800; CPU grading). Visibility is our single mechanism factor,
mirroring B1.1's observability variable; hypothesis: incidence is higher when structure is
shown. Elicitation validity: neutral prompts audited against a checklist — no prompt,
example, or scoring rule mentions skipping, faking, ordering around checks, or verifier
blindness; pressure comes only from visible partial-credit scoring and step budgets.
Denominator hygiene: both denominators pre-registered; sandbox-fault rollouts excluded by
pre-registered rule; the adjudication rubric distinguishes bypassed-prerequisite from
trivial-honest completions (the latter are task bugs → SP1). Honest-reference scripted runs
per task verify battery/oracle concordance before any measurement (gate G1).

### 4.6 Analysis

Bypassable-task fraction with Wilson CIs; resistance matrix; logistic regressions of bypass
feasibility (P1) and natural bypass (P2) on topology (depth, fan-in) and, for P2, on
visibility/budget/model; unearned-credit U distributions under the surveyed partial-credit
formulas; adjudication κ (target ≥ 0.7); oracle false-inconsistency and task-bug rates. All
rates lower-bound framed; P1/P2 claim discipline enforced through to the abstract.

## 5. Experiment Design

**Arms.** P1 audit (constructed reorder/skip/inject + fuzzing control, equal budgets, 30
tasks); P2 behavioral (1,080 neutral rollouts, factorial above); controls (honest-reference
runs; valid-order compositions; pre-registered exclusions).

**Pre-registered tests.** T1: bypassable-task fraction exceeds the G2 floor (one-sided exact
binomial). T2: P2 > 0 among battery-complete rollouts (exact binomial, α = .05, both
denominators). T3: checker-type × strategy resistance matrix — per-cell feasibility with
Holm-corrected pairwise contrasts between checker classes; strategy ranking (inject ≥ skip ≥
reorder) descriptive only. T4: topology — Wald tests on depth/fan-in coefficients, predicted
positive. T5: visibility — incidence(shown) > incidence(goal-only).

**Gates.** **G1 (sanity):** honest-reference runs 100% concordant (all V_k pass ∧ O_end
pass); otherwise fix suite/oracle first. **G2 (signal):** ≥ floor% of tasks bypassable by ≥1
strategy after adjudication, where the floor is derived from D0 — the bypassable-task
fraction at which expected unearned partial credit inflates surveyed benchmarks' scores by ≥
one grading unit (placeholder 10% pending D0). **G3 (integrity):** oracle
false-inconsistency < 5% of candidate bypasses; κ ≥ 0.7 (κ failure → rubric revision +
re-annotation within the calendar buffer).

**Decision rule (standalone vs. merge vs. park).** *Standalone short paper* (ISSTA/ASE/FSE
short or registered report) iff P2 pooled adjudicated incidence has lower Wilson bound > 1%
and point estimate ≥ 5% under the partial-credit denominator with directionally consistent
per-model rates, **and** ≥1 of T3/T4/T5 lands (structure, not just a rate). *Top-up rule:*
if the point estimate is in [3%, 8%] with a wide CI, run one additional seed × model block
(≈360 rollouts, budget reserved) before deciding. *B1.2-section path* if P1 is strong (G2
passed, clean adjudication) but P2 < 5%: "the paradigm is bypassable by construction; natural
incidence is small but nonzero" — one table (resistance matrix) + one figure (incidence under
two denominators) + ~1.5 pages in the family paper's verifier-sufficiency arc; skeleton
pre-committed by Sept 1. *Park / survey-only* if G2 fails after one suite-hardening
iteration: D0 publishes alone; the null ("these checker types resist bypass") is claimed only
if D0 shows our checker mix matches deployed practice.

**Calendar.** D0 + literature harvest → Aug 25; suite freeze → Aug 29; B1.2 section skeleton
→ Sept 1; P1 + P2 + full adjudication → Sept 12; κ-failure buffer → Sept 16; decision →
Sept 18; FSE deadline Oct 2. Scale-up (procedural 200–300 tasks, for stable topology
regression; and only then a multi-benchmark harvested cohort in the room-draft's style) runs
post-Oct-2, standalone/extended path only, and only if G1–G3 pass with a directionally
consistent but underpowered topology coefficient.

## 6. Threats to Validity

**Construct:** our checkers must match deployed practice — D0 fixes the checker-type
distribution and doubles as the fidelity audit. **Internal:** oracle bugs masquerade as
bypasses (asymmetric error) — defused by 100% adjudication, the valid-order control, and
reported false-inconsistency rates; trivial-honest completions are excluded by rubric and fed
back as task bugs. **External:** 30 hand-authored tasks in two domains bound generality; all
rates are lower bounds under fixed budgets; inference is to the paradigm as instantiated, not
to any named benchmark's scores — extending to harvested benchmark tasks is the gated
extension. **Elicitation:** visibility and budget are the only pressure knobs; prompts are
checklist-audited; P2 claims never leak into P1 sentences or vice versa.

## 7. Conclusion

Independent, prerequisite-blind milestone verification is a composition claim: that a
conjunction of local checks certifies a coherent end state. This study measures that claim's
failure modes with a deliberately small, fully mechanical instrument — feasibility by
construction (P1), incidence by observation (P2), and attribution by truthful-local-check
qualification (C) — grounded in a survey of deployed grading practice and hardened by
adjudication of every candidate bypass. If the premise fails at the measured rates, progress
metrics overstate capability, partial credit rewards unearned points, and milestone-shaped
rewards inherit a gameable signal at every node of the DAG; the actionable output is the
checker-type × strategy resistance matrix, which tells benchmark designers where ordering and
provenance awareness must be added. The design's smallness is not a concession but the
contract that makes every verdict re-derivable from released code.

## References

- Xu, F. F., et al. TheAgentCompany: Benchmarking LLM Agents on Consequential Real World
  Tasks. arXiv:2412.14161.
- Zhu, Y., Jin, T., Pruksachatkun, Y., et al. Establishing Best Practices for Building
  Rigorous Agentic Benchmarks. arXiv:2507.02825.
- Shao, J., Chen, H., Zhang, W., et al. Do Agent Benchmarks Measure Capability? Protocol
  Validity in the Age of Agentic AI (HackDetect). arXiv:2607.22368.
- Yu, B., Zhu, Y., He, P., et al. UTBoost: Rigorous Evaluation of Coding Agents on
  SWE-Bench. arXiv:2506.09289.
- Zhao, B., Srikanth, D., Wu, Y., et al. SpecBench: Measuring Reward Hacking in Long-Horizon
  Coding Agents. arXiv:2605.21384.
- Thaman, K. Reward Hacking Benchmark: Measuring Exploits in LLM Agents with Tool Use.
  arXiv:2605.02964.
- Khalifa, M., Khan, Z., Tafveez, O., et al. Countdown-Code: A Testbed for Studying the
  Emergence and Generalization of Reward Hacking in RLVR. arXiv:2603.07084.
- Wang, B., Zhang, C., Liu, D., et al. The Verification Horizon: No Silver Bullet for Coding
  Agent Rewards. arXiv:2606.26300.
- Vangala, B. P., Adibifar, A., Gehani, A., et al. AI-Generated Code Is Not Reproducible
  (Yet): An Empirical Study of Dependency Gaps in LLM-Based Coding Agents. arXiv:2512.22387.
- Zheng, X., Li, N., Luan, X., et al. Beyond Correctness: Exposing LLM-generated Logical
  Flaws in Reasoning via Multi-step Automated Theorem Proving. arXiv:2512.23511.
- REVEAL: step-level verification of chain-of-thought reasoning. ACL 2024.
- Skalse, J., Howe, N. H. R., Krasheninnikov, D., Krueger, D. Defining and Characterizing
  Reward Hacking. NeurIPS 2022. arXiv:2209.13085.
- Pan, A., Bhatia, K., Steinhardt, J. The Effects of Reward Misspecification. ICLR 2022.
- Krakovna, V., et al. Specification gaming: the flip side of AI ingenuity. 2020.
