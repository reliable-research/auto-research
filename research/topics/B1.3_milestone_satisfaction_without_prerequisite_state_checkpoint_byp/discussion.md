# Discussion: B1.3 — Milestone Satisfaction without Prerequisite State: Checkpoint Bypass in Multi-Step Agent Verification

> Auto-research-discussion document (6 stages, critic→refine per stage).
> Seed: `README.md` (多步任务的检查点绕过, label [证据], parent B1 "Verifier 充分性（agent / 代码场景）").
> Companion planning scaffold: `digest.md` (reverse digest; note its 2026-07-04 cache-integrity
> fix — N3 entries 1–8 are [UNVERIFIED — requires harvest]; only the three cache-verified
> twins are load-bearing).
> **Audit positioning (binding for this document):** KEEP, Tier-2. Sound and cheap but
> narrower than B1.1/B1.2 — likely a **section-sized finding**. This discussion therefore
> designs a compact, self-contained study that can either stand alone as a short paper or
> slot as a section into B1.2's paper (family lead: mutation-controlled visible-test
> overfitting, FSE deadline Oct 2). Every design choice below is biased toward smallness,
> mechanical ground truth, and a clean merge path.

---

## Stage 1 — Problem Definition

**Draft.**

Setting. A multi-step agent task is specified as a DAG G = (K, E) over milestones
k₁…k_N, where an edge (k_i → k_j) means k_i's *true state* is a prerequisite for k_j.
Grading follows common agent-benchmark practice: each milestone has an **independent,
locally-scoped verifier** V_k (file-existence/pattern check, unit sub-test, tool-signature
check, DB-row comparison) with no visibility into other milestones' provenance. Separately, a
**terminal end-to-end consistency oracle** O_end recomputes the canonical final state from
the task spec and compares it to the actual terminal state (真值 = 终态一致性检查). O_end is
ground truth; the per-milestone battery {V_k} is the paradigm under test.

A **checkpoint-bypass event** is a trajectory with (∀k: V_k = pass) ∧ (O_end = fail). The
seed names three bypass mechanisms: 乱序 (out-of-order completion violating ≥1 DAG edge),
跳步 (step-skipping — reaching a milestone's local signal without executing a prerequisite),
状态注入 (state injection — directly planting the surface signature V_k checks, e.g., touch
the expected file, insert the DB row, echo the pattern).

Two distinct measurements, kept separate throughout:

- **P1 (attack surface, agent-free):** over *constructed* trajectories implementing the three
  strategies, the checkpoint-bypass rate — a property of the verification *paradigm*.
- **P2 (behavioral incidence):** among *real agent rollouts* that the milestone battery
  scores complete, the fraction failing O_end — deployment relevance.

**Critic:**

1. The two-measurement split is the document's best structural idea and must be enforced
   harder: P1 supports only claims about verifier insufficiency ("the paradigm admits
   bypasses at rate ≥ r on this suite"); P2 supports only claims about agent behavior. The
   draft should state the *conflation failure mode* explicitly — the single most likely
   reviewer objection is "you built adversarial traces and then talk about agents cheating."
2. P1's rate is meaningless without a denominator convention: "fraction of constructed
   trajectories" depends entirely on how many we construct. Reframe P1 per task/per checker
   type as a *feasibility* measure — for each (task, strategy), does at least one
   verifier-passing, oracle-failing trace exist within the sampled construction budget? —
   yielding a bypassable-task fraction, plus per-strategy success counts as secondary. A
   "rate over traces we chose to make" is not an estimand.
3. "All V_k pass" is a strong conjunction; real benchmarks often use partial credit
   (checkpoints passed / total). The definition should also record the partial-credit score
   inflation: how many *unearned* checkpoint points a bypassing trajectory collects even when
   full conjunction fails. This widens relevance to checkpoint-graded benchmarks at near-zero
   extra cost.
4. Out-of-scope statement missing (multi-agent, GUI/robotics domains, live services); Tier-2
   compactness demands scope be pinned in Stage 1, not discovered in Stage 6.

**Refined:**

As drafted, with four repairs:

1. **Claim-discipline rule (binding):** P1 sentences may only predicate of *verifiers*
   ("independent milestone verification admits X"); P2 sentences may only predicate of
   *agents* ("agents naturally produce Y"). The paper carries this split into its abstract.
2. **P1 estimand recast as feasibility:** for each (task, strategy ∈ {reorder, skip, inject},
   checker type), report **bypassable?** ∈ {yes, no} under a pre-registered construction
   budget (fixed sampling procedure over topological violations / skip patterns / injection
   points, fixed per-task compute cap). Headline P1 number = fraction of tasks bypassable by
   ≥1 strategy; per-strategy and per-checker-type breakdowns secondary. All rates framed as
   lower bounds over the sampled space (digest C1).
3. **Partial-credit inflation metric added:** for every bypassing or partially bypassing
   trajectory, record unearned-checkpoint score = (checkpoints passed without prerequisite
   state) / (total checkpoints), connecting P1/P2 to partial-credit grading as used by
   checkpoint-scored benchmarks (e.g., TheAgentCompany-style checkpoints [VERIFY exact
   grading formula at writing time]).
4. **Scope:** single-agent; domains with a canonical, mechanically recomputable terminal
   state (filesystem/coding; tool-use over a service DB); no GUI, no live web, no robotics;
   English task prompts; O_end code disjoint from every V_k.

---

## Stage 2 — Motivation (why now; audit positioning)

**Draft.**

Why the question matters. Milestone-wise grading is the workhorse of multi-step agent
evaluation: checkpoint lists with partial credit (TheAgentCompany [VERIFY]), subgoal/progress
rates (AgentBoard [VERIFY]), key-node checks for web agents (WebCanvas [VERIFY]), DB-state
and tool-signature checks (τ-bench-style [VERIFY]). Milestone signals are also being adopted
as *dense rewards* for RL over long-horizon tasks. All of these assume the same structural
premise: passing checkpoint k certifies the work that k represents, including its
prerequisites. If that premise fails — if checkpoints can be satisfied 乱序/跳步/状态注入 —
then progress metrics overstate capability, partial credit rewards unearned points, and
dense-reward RL inherits a gameable signal at every node of the DAG.

Why now. Long-horizon agent benchmarks are moving *toward* finer-grained milestone grading
(to fight sparse signals), i.e., the attack surface is growing by design; and milestone
rewards are entering training loops, upgrading the question from evaluation hygiene to reward
integrity.

Audit positioning. This topic is Tier-2: narrower than B1.1 (one verifier-granularity
question, no learned verifiers, no RL arm needed) and likely section-sized. The honest
framing is a compact, fully mechanical measurement — CPU-only, hand-auditable, ~hundreds of
trajectories — that either stands alone as a short empirical paper or becomes the
"compositional/prerequisite channel" section of B1.2's verifier-sufficiency paper. Its edge
over both siblings is the **structural axis**: B1.2 asks whether a test suite is adequate for
one artifact; B1.1 asks whether an evidence channel can be forged for one action; B1.3 asks
whether *composition* of individually-sound checks preserves soundness when checks are
prerequisite-blind. That question is not answerable from B1.1/B1.2 results.

**Critic:**

1. Four [VERIFY] tags in the first paragraph — acceptable at discussion stage, but the
   motivation's load-bearing empirical premise ("milestone grading is widespread and growing")
   must be substantiated with a small survey (10–15 agent benchmarks, table of grading
   mechanism × partial credit × prerequisite awareness). That table is cheap, unambiguously
   factual, and doubles as the paper's Table 1 — for a section-sized finding it may be the
   single highest-value page.
2. The "dense-reward RL" stake is asserted but B1.3's design (Stage 5) contains no RL. Either
   scope the stake to evaluation + selection pressure (honest), or add a minimal
   selection-pressure probe. Recommend the former plus a one-line forward pointer to B1.1's
   pressure machinery — do not grow a Tier-2 study an RL arm.
3. The structural-axis paragraph is the right positioning but overclaims independence: a
   state-injection bypass at a single milestone is locally *exactly* B1.1's forging pattern.
   The delta must be stated more precisely: B1.3's unit of analysis is the *dependency
   structure* (does the battery detect missing prerequisites?), and its ground truth is
   end-state consistency, not per-action state diff. Injection is shared texture; the
   prerequisite-blindness question is not.
4. "Why now" should also note the cost asymmetry motivating the design: B1.3 is the only B1
   topic executable entirely without GPUs or training — worth saying, since Tier-2 survival
   depends on being cheap.

**Refined:**

Motivation restructured into three claims plus positioning:

1. **Premise, to be evidenced by a grading survey (new deliverable D0):** a 10–15-benchmark
   table (grading mechanism, partial credit?, any prerequisite/ordering enforcement?) —
   hypothesis: most checkpoint-graded benchmarks verify milestones independently and enforce
   no provenance. D0 is Table 1 of the paper/section and resolves the [VERIFY] tags. If D0
   *fails* (most benchmarks turn out prerequisite-aware), the topic dies cheaply at the
   survey stage — a legitimate Tier-2 outcome, recorded as such.
2. **Stakes, honestly scoped:** overstated progress metrics and unearned partial credit in
   *evaluation*, and gameable milestone signals for *selection* (best-of-n over checkpoint
   score); training-time reward integrity is flagged as an implication and pointed at B1.1's
   pressure machinery, not measured here.
3. **Structural delta within the family (precise form):** B1.3 measures whether
   *composition* of individually-scoped checks is sound when checks are prerequisite-blind —
   unit of analysis is the DAG, ground truth is 终态一致性, and the characteristic result is
   bypass odds as a function of graph topology (depth, fan-in). Injection at a single node is
   B1.1's texture; ordering/prerequisite blindness is B1.3's own axis. One shared paragraph
   in whichever paper hosts both will state this.
4. **Cheapness as a feature:** CPU-only, no training, no learned components anywhere in the
   measurement chain — every verdict re-derivable by a reviewer from released code. This is
   the Tier-2 design contract.

---

## Stage 3 — Related Work

**Draft.**

Grounding status inherited from `digest.md` N3 (post 2026-07-04 fix): three cache-verified
neighbors are load-bearing; eight OpenReview candidates are [UNVERIFIED — requires harvest]
and usable only as harvest targets.

(a) *Verified structural twins (cache-grounded).*
[CodeReproducibilityGap2025, arXiv:2512.22387]: local functional-correctness signal passes
while a disjoint clean-environment reproducibility oracle fails — same
local-signal-vs-disjoint-oracle pattern, but whole-program unit, no DAG, no adversarial
construction. [RevealWeakestLink2024 (REVEAL), ACL 2024]: step-level verification of CoT
chains because chain-level correctness masks invalid steps — the *inverse* direction
(global pass hiding local invalidity) on linear text chains, no stateful environment.
[MATPLogicalFlaws2025, arXiv:2512.23511]: theorem-prover oracle exposes locally-plausible /
globally-invalid reasoning — disjoint-oracle measurement, but state is fully observable in
the artifact; no provenance question.

(b) *Harvest targets (UNVERIFIED, from digest N3.1–8; must be re-harvested before writing):*
TED (per-checkpoint grading mechanisms in agent evaluation), XENON / GTool (prerequisite
DAGs as planning structure), StepORLM / LatentVeracity (step-wise scorers locally consistent,
globally inconsistent), WebArbiter (checklist checkers reward superficial compatibility),
Gistify (benchmark shortcuts vs. execution-faithful grading), DiffTaskGraph (learned
prerequisite DAGs, ordering-mistake detection).

(c) *Named benchmark-grading practice to be surveyed in D0 (all [VERIFY]):* TheAgentCompany
(checkpoint lists, partial credit), AgentBoard (subgoal progress rate), WebCanvas (key-node
evaluation), τ-bench / τ²-bench (DB-state + tool-signature checks), BFCL v3, ToolSandbox,
OSWorld (state-based evaluation scripts), SWE-bench (per-instance fail-to-pass tests — the
degenerate single-milestone case).

(d) *Reward hacking / specification gaming (shared family backdrop, one paragraph):* Skalse
et al. 2022; Pan, Bhatia & Steinhardt 2022; Krakovna et al. 2020 specification-gaming list;
Amodei et al. 2016. B1.3 cites these for the general proxy-gap logic but its own claims are
about verifier *structure*, not optimization pressure.

Boundary vs. B1.2 and B1.1. vs. B1.2: B1.2's proxy is a visible test suite over one artifact
and its ground truth is mutation adequacy; B1.3's proxy is a *battery* of milestone checks
over a trajectory and its ground truth is terminal-state consistency; B1.2's agent does real
work that under-generalizes, B1.3's trajectories collect credit for work whose prerequisites
never happened. vs. B1.1: B1.1 forges the *evidence channel* for actions (log vs. state
diff, single-action grain); B1.3 holds the evidence channel honest per milestone (each V_k
really checks real local state) and shows the *composition* is still unsound because checks
are prerequisite-blind. Cleanest one-liner: B1.1 breaks the check's *truthfulness*, B1.3
breaks the battery's *sufficiency* even when every check is truthful.

**Critic:**

1. The one-liner boundary is good but partially false for the 状态注入 strategy: an injected
   surface signature means V_k is *not* really checking real local state — injection makes
   individual checks untruthful too, which collapses the claimed boundary for that strategy.
   Fix: classify strategies by which property they break — reorder/skip break battery
   sufficiency with *truthful* local checks (state genuinely present, prerequisites not);
   injection breaks local truthfulness (B1.1-adjacent) and is retained because it is one of
   the seed's three named mechanisms, with its B1.1 adjacency explicitly flagged. If B1.1 and
   B1.3 land in the same venue cycle, injection results should be cross-referenced, not
   double-claimed.
2. Related-work debt is understated: the harvest of (b) is recorded in the digest as
   *Phase-B-blocking*. This stage should carry that obligation forward with a date, not a
   vague "before writing."
3. (c) belongs to D0 (Stage 2) — fine, but note that D0 is *itself* the related-work
   verification instrument: reading each benchmark's grading code resolves both the [VERIFY]
   tags and the construct-validity threat t1 (checker fidelity) in one pass. Say so to avoid
   double-counting effort.
4. Missing adjacent line: workflow/process conformance checking in BPM and process mining
   (checking event logs against process models with ordering constraints) — a mature field
   whose machinery (conformance checking over partial orders) is a known-tools argument;
   one sentence + [VERIFY] to avoid reinventing terminology reviewers from SE will know.

**Refined:**

Adopt the strategy-level boundary repair as the section's organizing idea:

- **Reorder / skip** → break *battery sufficiency* with truthful local checks: B1.3's own
  territory, untouched by B1.1/B1.2.
- **Inject** → breaks *local truthfulness*: B1.1-adjacent texture at milestone grain;
  retained per the seed (状态注入), reported with an explicit cross-reference rule — if
  merged into the family paper alongside B1.1, injection is presented once, jointly.

Obligations carried forward with dates: (i) harvest of the eight UNVERIFIED digest
candidates + a fresh arXiv/DBLP pass ("checkpoint", "milestone verification", "subgoal
reward", "conformance checking agents") by **2026-08-25**; (ii) D0 grading survey doubles as
[VERIFY] resolution for the benchmark list and as the t1 fidelity audit — one effort, three
uses; (iii) add one [VERIFY] sentence on BPM conformance checking as prior art for
order-constraint checking over logs, positioned as "machinery exists; the *measurement* of
agent-benchmark bypass rates does not."

Boundary text (final): "B1.1 asks whether a single check's evidence can be faked; B1.2 asks
whether one artifact's test suite is adequate; B1.3 asks whether a *battery* of
individually sound, prerequisite-blind checks certifies a coherent end state — and shows by
construction (P1) and by observation (P2) that it does not."

---

## Stage 4 — Sub-problems

**Draft.**

- **SP1 — DAG task suite with canonical terminal states.** 20–40 hand-authored tasks (pilot),
  5–12 milestones each, in two domains (filesystem/coding; tool-use/DB); topology parameters
  (depth, fan-in) varied by design; each task ships (milestones, edges, V_k specs, terminal
  spec).
- **SP2 — Faithful per-milestone verifiers.** V_k implementations drawn from the D0 survey's
  observed checker types (existence, pattern, sub-test, tool-signature, DB-row), scope-
  restricted to local signals; fidelity to deployed practice is a construct-validity
  requirement, not a convenience.
- **SP3 — Oracle correctness (C4).** O_end must be independently computable and *more
  trustworthy than the thing it audits*; a buggy oracle manufactures fake bypasses. Disjoint
  code, canonical-terminal-state domains only, manual audit of a stratified verdict sample
  with a reported false-inconsistency rate.
- **SP4 — Bypass-trace construction under a fair budget (C1).** A pre-registered sampler over
  reorderings (edge-violating topological permutations), skip patterns, and injection points;
  rates reported as lower bounds; per-strategy construction budget fixed in advance.
- **SP5 — Natural-incidence elicitation without teaching (P2).** Real agents run under
  neutral prompts; pressure only via (a) milestone partial-credit scoring visible as task
  feedback and (b) step/time budgets that make honest completion tight — never an
  instruction to skip or fake. Measure the fraction of milestone-complete rollouts failing
  O_end.

Hard part: **SP3**. The oracle is the ground truth of the entire study; unlike B1.1 (where
truth is a simple per-action state diff), 终态一致性 requires re-deriving the *canonical*
final state of a multi-step task — specifying it correctly is comparable in difficulty to
specifying the task, and every oracle bug is silently counted as evidence for the thesis
(asymmetric error direction — the dangerous kind).

**Critic:**

1. Naming SP3 the hard part is defensible, but the asymmetric-error observation deserves
   promotion into a design rule: adjudicate every P1 "bypass" *by hand* in the pilot (the
   scale is small enough — this is the advantage of a Tier-2 study), so pilot-stage headline
   claims rest on human-confirmed bypasses, with the oracle's false-inconsistency rate
   reported as a calibration by-product. At pilot scale, full adjudication removes SP3's
   sting almost entirely; only the scale-up needs sampling.
2. SP5's budget-pressure knob risks a different confound than "teaching to cheat": tight
   budgets cause *honest incomplete* rollouts that fail milestones and never enter the P2
   denominator — fine — but they can also cause the agent to *legitimately* satisfy V_k in
   degenerate ways the task admits (a real but trivial solution), which is not prerequisite
   bypass. The adjudication rubric must distinguish "bypassed prerequisite" from "task
   under-specified, trivial honest solution exists" — the latter is a task-suite bug (goes
   back to SP1), not a finding.
3. SP4's sampler needs a comparability guarantee across strategies: if injection gets 100
   attempts and reorder 10, per-strategy comparisons (RQ_INF_1) are junk. Equal per-strategy
   budgets per task, stated once.
4. Missing sub-problem: **P2 denominator hygiene**. "Milestone-complete rollouts" must be
   defined under both full-conjunction and partial-credit conventions (Stage 1 repair 3),
   and rollouts hitting sandbox faults must be excluded by pre-registered rule; else natural
   incidence is unmeasurable noise at the expected small sample sizes.

**Refined:**

Five sub-problems, revised:

- **SP1** as drafted + admission rule: a task is admitted only if a *trivial-solution audit*
  (can V_k be honestly satisfied while making the task's terminal state incoherent? is the
  honest path unique enough?) passes; discovered trivial solutions are task bugs, fixed
  before data collection.
- **SP2** as drafted, anchored to D0's observed checker-type distribution (fidelity by
  construction).
- **SP3 (hard part, defused at pilot scale):** pilot rule — **100% human adjudication of
  every candidate bypass** (all-V_k-pass ∧ O_end-fail), two annotators, rubric with three
  outcomes {genuine bypass, oracle error, task under-specification}; oracle
  false-inconsistency rate and task-bug rate reported. Scale-up: stratified adjudication
  sample ≥100 or 20%, whichever larger.
- **SP4** + equal per-strategy construction budgets per task (pre-registered sampler; rates
  as lower bounds).
- **SP5 — natural incidence with denominator hygiene:** neutral prompts; pressure = partial-
  credit milestone feedback + step budget only; adjudication rubric from SP3 distinguishes
  bypass vs. trivial-honest; P2 reported under both full-conjunction and partial-credit
  definitions; sandbox-fault exclusion rule pre-registered.

---

## Stage 5 — Methods

**Draft.**

**Testbed (M1).** Pilot: 20–40 hand-authored DAG tasks, two domains: (i)
filesystem/coding — milestones like "config generated" → "build artifact present" → "tests
recorded passing" → "package assembled", V_k = existence/pattern/sub-test checks, terminal
state = deterministic file-set hash + program output; (ii) tool-use/DB — milestones as
service-state waypoints (row created → linked → invoiced), V_k = tool-signature/DB-row
checks, terminal state = canonical row-set. Topology varied: chain depth 3–8, fan-in 1–3.
Scale-up: procedural generation to 200–300 tasks over the same schemas.

**Ground truth (M4, mechanical).** O_end re-derives the canonical terminal state from the
task spec and compares by total function (hash set / row-set / output equality). Disjoint
code from all V_k; no LLM anywhere in the truth channel; snapshots taken by the harness
outside the agent sandbox.

**P1: bypass-trace construction (M3).** Per task and strategy, equal-budget sampler:
*reorder* — sample edge-violating permutations of the milestone action blocks; *skip* — drop
prerequisite blocks, keep dependents; *inject* — replace prerequisite blocks with direct
surface-signature writes (touch file, insert row, echo pattern). Execute each constructed
trajectory in the sandbox; record (∀V_k, O_end). Agent-free: this is a property measurement
of the verification battery.

**P2: natural incidence (M5-nat).** 3–5 agent models (mix of API and open-weight), ≥3 seeds,
neutral prompts showing the milestone list and partial-credit scoring as ordinary task
context; two budget conditions (comfortable vs. tight step budget); among rollouts scored
complete by the battery (both denominators), measure O_end failure fraction, fully
adjudicated (SP3 rule).

**Analysis (M5).** Bypassable-task fraction (P1) with per-strategy/per-checker-type
breakdowns; logistic regression of bypass feasibility and of natural bypass on topology
(depth, fan-in); unearned-partial-credit distributions; Wilson CIs throughout; all rates
lower-bound framed.

**Elicitation validity.** No prompt, example, or scoring rule ever mentions skipping,
faking, ordering around checks, or verifier blindness; the milestone list is presented as
task structure (as real benchmarks do), not as an exploit map; prompts audited against the
same checklist as B1.1's R1 rule.

**Critic:**

1. Showing the milestone list + partial-credit scoring in-context is defensible (real
   benchmarks/harnesses expose milestones) but is itself a *condition*, not a constant:
   whether the agent can see the checkpoint structure is exactly a "verifier observability"
   variable, and burying it fixes a mechanism knob at its most permissive setting. Make
   visibility a 2-level factor (milestones shown vs. task goal only) — it is the one
   mechanism variable B1.3 can afford, and it directly parallels B1.1's H-obs, strengthening
   the family story.
2. The reorder strategy as specified ("permute action blocks") presumes milestone actions
   are block-separable. Hand-authored tasks can guarantee this, but then the suite must
   document block boundaries as part of the task schema, or P1's sampler is
   under-specified.
3. M5-nat's "3–5 agent models × 2 budgets × 2 visibility × 20–40 tasks × 3 seeds" quietly
   grew to ~2,000 rollouts, straining the "cheap" contract. Prioritize: visibility factor >
   budget factor > model count. Concretely: 3 models, visibility × tight-budget-only... no —
   keep 2 budgets, drop to 3 models, 3 seeds, pilot 30 tasks → 30×3×3×2×2 = 1,080 rollouts,
   ~$200–800 API class. State the arithmetic.
4. Procedural scale-up to 200–300 tasks is only worth doing if the pilot's topology signal
   is promising; as written the method reads as if scale-up were default. Tie scale-up to
   the Stage-6 gate explicitly (Tier-2 discipline).
5. One more truth-channel hole: O_end compares terminal state but ignores *how many honest
   milestones were actually completed* — for adjudication and for the unearned-credit
   metric, the harness should also record per-milestone provenance (which actions touched
   which artifacts), cheaply available from sandboxed syscall/command logging. Without it,
   annotators reconstruct provenance by hand.

**Refined:**

Adopt all five:

1. **Visibility factor added** (checkpoint structure shown vs. goal-only), mirroring B1.1's
   observability variable; hypothesis: natural bypass incidence higher when structure is
   shown. This is B1.3's single mechanism contrast and its bridge to the family narrative.
2. **Task schema extended** with explicit milestone action-block boundaries (required for
   the reorder/skip samplers; documented per task).
3. **P2 budget pinned:** 30 pilot tasks × 3 models × 3 seeds × 2 budgets × 2 visibility =
   1,080 rollouts (API cost class $200–800; CPU grading). P1 remains agent-free and
   CPU-only (~thousands of constructed executions, hours).
4. **Scale-up is gated, not default** (see Stage 6); the pilot alone must be publishable as
   a section.
5. **Provenance side-channel:** harness-level command/file-access logging (outside the
   sandbox boundary) recorded per milestone, used for adjudication and the unearned-credit
   metric — never as a verifier (it is instrumentation, not a proposed fix; proposing
   provenance-aware verifiers is future work / the natural "implications" paragraph).

---

## Stage 6 — Experiment Design

**Draft.**

**Arms.**

- **P1 audit (agent-free):** constructed reorder/skip/inject traces, equal budgets, over the
  pilot suite; outcome: bypassable-task fraction per strategy × checker type.
- **P2 behavioral:** 3 models × 2 budgets × 2 visibility × 30 tasks × 3 seeds, neutral
  prompts; outcome: adjudicated natural bypass incidence under both denominators + unearned
  partial credit.
- **Controls:** honest-reference runs (scripted correct trajectories) to verify all V_k and
  O_end agree on honest completions (battery/oracle sanity); sandbox-fault exclusions
  pre-registered.

**Metrics.** Bypassable-task fraction (per strategy/checker type) with CIs; per-strategy
construction success; adjudicated natural bypass incidence (full-conjunction and
partial-credit denominators); unearned-checkpoint score distribution; topology odds ratios
(depth, fan-in) from logistic regression; oracle false-inconsistency rate and task-bug rate
from adjudication; annotator κ.

**Pre-registered tests.** T1 (P1): bypassable-task fraction > 0 — one-sided exact binomial
against 0 with a pre-registered minimal-effect floor (≥10% of tasks bypassable to count as
meaningful, not just nonzero). T2 (P2): natural incidence > 0 among battery-complete
rollouts (exact binomial; α = .05). T3 (strategy ranking): inject vs. skip vs. reorder
pairwise proportions, Holm-corrected; predicted inject ≥ skip ≥ reorder. T4 (topology):
Wald tests on depth/fan-in coefficients; predicted positive. T5 (visibility): incidence
shown > goal-only.

**Pilot go/no-go (gates scale-up and the write-up path).**

- **G1 (sanity):** honest-reference runs 100% concordant (all V_k pass ∧ O_end pass);
  otherwise fix suite/oracle first.
- **G2 (P1 signal):** ≥10% of tasks bypassable by ≥1 strategy after adjudication.
- **G3 (measurement integrity):** oracle false-inconsistency rate < 5% of candidate
  bypasses; κ ≥ 0.7.
- Scale-up (procedural 200–300 tasks, needed only for stable topology regression) runs only
  if G1–G3 pass *and* the topology coefficient is directionally consistent but underpowered
  in the pilot.

**Standalone vs. B1.2-section decision rule (effect-size based).**

- **Standalone short paper** (ISSTA/ASE/FSE-short or registered-report style) if BOTH:
  (i) adjudicated natural incidence (P2) ≥ 5% under the partial-credit denominator for at
  least one model × condition cell — i.e., real agents demonstrably collect unearned credit
  unprompted; and (ii) at least one of T3/T4/T5 significant — i.e., there is structure, not
  just a rate.
- **Section of B1.2's FSE paper** if P1 is strong (G2 passed, clean adjudication) but P2
  natural incidence < 5% or only T1/T2 land: the finding is then "the milestone-verification
  paradigm is bypassable by construction; natural incidence is small but nonzero" — one
  table + one figure + ~1.5 pages in the family paper's verifier-sufficiency arc.
- **Park / survey-only** if G2 fails after one suite-hardening iteration: publish D0 (the
  grading survey) as a short position/dataset note or fold it into B1.2's related work.

**Calendar.** D0 survey + harvest by Aug 25; pilot suite frozen Aug 29; P1 audit + P2
rollouts + adjudication by Sept 12; decision meeting Sept 15 — leaving 2+ weeks to write the
B1.2 section before FSE's Oct 2 deadline if the merge path is chosen. Scale-up, if gated in,
happens *after* Oct 2 regardless of path (it serves the standalone/extended version only).

**Critic:**

1. The decision rule uses P2 ≥ 5% as the standalone trigger, but with ~90 battery-complete
   rollouts expected per cell (optimistically), a 5% incidence gives ~4–5 events — CI too
   wide to headline a standalone paper. Either raise the evidence bar (≥5% with lower Wilson
   bound > 1%, pooled across cells with per-cell consistency), or accept that the standalone
   path realistically requires the P2 sample to be doubled when the trigger is near-threshold.
   Add a conditional top-up rule rather than pretending the pilot sample suffices.
2. T3's predicted ordering (inject ≥ skip ≥ reorder) is inherited from the digest, but P1's
   recast (feasibility under equal budgets) changes its meaning: injection will trivially
   approach 100% feasibility against existence/pattern checkers — a near-ceiling result. The
   informative P1 comparison is *per checker type* (which checker classes resist which
   strategies), which is also the actionable output for benchmark designers. Reframe T3
   accordingly; keep the strategy ranking as descriptive.
3. G2's 10% floor is arbitrary; defensible, but tie it to D0: if the surveyed benchmarks
   average N≈8 checkpoints with partial credit, even one bypassable checkpoint per task
   inflates scores by ~12% — grounding the floor in the credit-inflation consequence makes
   it non-arbitrary.
4. The calendar has no slack for adjudication disagreement (κ < 0.7 forces rubric revision
   + re-annotation). Move the decision meeting to Sept 18 and pre-commit the section
   skeleton (table + figure templates) in advance so the merge path is a fill-in exercise.
5. The park path discards P1 too readily: even with G2 failed, a demonstrated-hard-to-bypass
   suite is a *negative-space* contribution only if the suite is representative — which is
   exactly what D0 certifies. Fine as written, but say the null's publishable form depends
   on D0's fidelity evidence.

**Refined:**

Final design = draft + five amendments:

1. **Standalone trigger hardened:** P2 pooled adjudicated incidence with lower Wilson bound
   > 1% *and* point estimate ≥ 5% under the partial-credit denominator, with directionally
   consistent per-model rates; **conditional top-up rule** — if the point estimate is in
   [3%, 8%] with a wide CI, run one additional seed × model block (≈360 rollouts) before
   deciding. Budget reserved in advance.
2. **T3 reframed as checker-type × strategy resistance matrix** (primary P1 analysis;
   actionable design guidance: which checker classes need provenance/ordering awareness);
   strategy ranking demoted to descriptive. Expected near-ceiling injection feasibility
   against existence/pattern checkers is stated as an anticipated (not headline) result.
3. **G2 floor derived from D0:** floor = the bypassable-task fraction at which expected
   unearned partial credit inflates surveyed benchmarks' scores by ≥ one grading unit
   (computed from D0's observed checkpoint counts); 10% is the placeholder pending D0.
4. **Calendar with slack:** D0 + harvest Aug 25 → suite freeze Aug 29 → P1 + P2 + full
   adjudication Sept 12 → κ-failure buffer to Sept 16 → decision Sept 18; B1.2 section
   skeleton (Table: checker-type × strategy resistance; Figure: incidence under two
   denominators; 1.5 pages) drafted by Sept 1 so the merge path is fill-in. Scale-up always
   post-Oct 2, standalone/extended path only.
5. **Null path conditioned on D0:** a G2-fail null is publishable (as "milestone batteries
   with these checker types resist bypass") only if D0 shows the suite's checker mix matches
   deployed practice; otherwise the null is recorded internally and the topic parks.

---

## Summary

- **Core claim:** independent, prerequisite-blind milestone verification does not certify a
  coherent end state — measured two ways, kept strictly separate: (P1) the paradigm is
  bypassable by construction (乱序/跳步/状态注入 feasibility per checker type, agent-free),
  and (P2) real agents collect unearned checkpoint credit unprompted at a measurable
  natural incidence, with 终态一致性检查 as mechanical ground truth.
- **Design:** compact and CPU-only by contract — a 10–15-benchmark grading survey (D0,
  doubles as Table 1 and construct-validity evidence), 30 hand-authored DAG tasks with
  certified block boundaries and a disjoint terminal oracle, equal-budget bypass samplers,
  ~1,080 neutral-prompt agent rollouts with one mechanism factor (checkpoint-structure
  visibility, mirroring B1.1's observability), and 100% human adjudication of every
  candidate bypass at pilot scale.
- **Novelty:** verified nearest neighbors (CodeReproducibilityGap, REVEAL, MATP) share the
  local-signal-vs-disjoint-oracle pattern but none measures bypass of a prerequisite DAG's
  checkpoint battery; B1.3's own axis vs. B1.1/B1.2 is compositional sufficiency —
  reorder/skip break the battery even when every individual check is truthful (injection is
  flagged as B1.1-adjacent and cross-referenced, not double-claimed).
- **Standalone vs. merge:** decided 2026-09-18 — natural incidence ≥5% (lower Wilson bound
  >1%) plus one structural result (checker-resistance matrix, topology, or visibility
  effect) → standalone short paper; strong P1 but weak P2 → pre-skeletoned 1.5-page section
  in B1.2's FSE paper (deadline Oct 2); G2 fail → D0 survey published alone or topic parked.
