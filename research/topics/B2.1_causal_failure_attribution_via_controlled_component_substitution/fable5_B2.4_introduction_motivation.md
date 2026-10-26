# Failed or Infeasible? — Introduction & Motivation

> **Status: pre-registered specification. No experiments have been run.** Every
> bracketed value (`[N]`, `[XX.X%]`, `[AUROC = CC]`, …) is a placeholder to be
> filled from Stage-2 output, never before. Filling one early would be HARKing —
> the exact failure the pre-experiment gate exists to prevent.
>
> Archetype: **empirical/measurement** (primary) + **resource/benchmark**
> (secondary). The contribution is a *measured directional estimand* plus a
> released instrument — not a new method. Audited by novelty-auditor 🟢,
> research-taste-auditor 🟢, se-paper-reviewer (no fatal flag), and
> pengsida-stage-reviewer Stage-5 PASS.

---

## Motivation

LLM agents are deployed not to answer but to *act* — they call tools, query
databases, edit files, execute commands, and coordinate multi-step workflows.
When such a run fails, the operative question is no longer whether the final
answer is wrong but **why the run failed**: a flawed plan, a wrong tool, a
misread error, an early stop. This question is load-bearing, because its answer
drives what happens next — retry, repair, escalate to a human, fine-tune the
policy, or abandon.

Current failure-attribution pipelines answer it under a hidden assumption:
**every failed trace contains a culpable agent decision.** A single asymmetry
breaks that assumption. Whether a task admits *any* solution is fixed by its
specification *before any agent acts* and is certifiable by a mechanical check
over the environment; attribution, by contrast, reads only the *post-hoc
trace*, in which the counterfactual that defines blame — the earliest step whose
correction would flip failure to success — **provably does not exist on an
unsolvable instance.** A required column may be dropped, a needed tool removed, a
stated goal contradicted by a stated constraint. Here the correct diagnosis is
not "the agent failed" but "the task was infeasible" — and a system with no
category for the second cannot express it.

The distinction is operational, not cosmetic, and it cuts both ways.
Misdiagnosing an impossible task as an agent failure wastes retries, produces
misleading debugging evidence, blames the wrong component, and corrupts repair
supervision. Overusing "unsolvable" as a safe excuse abandons hard-but-solvable
tasks. A trustworthy stack therefore needs a *calibrated* boundary between
**unsolved by this agent** and **unsolvable for any agent under this
environment** — not merely an added refusal button, and not a rate read off the
agent's own behavior.

That boundary is hard to observe from a failed trace alone: a competent agent
exhausting an impossible task and an incompetent agent botching a solvable one
produce superficially similar traces — repeated tool errors, dead-end reasoning,
budget exhaustion. To measure the confusion cleanly we need tasks whose
solvability is known *independently of agent behavior*. This motivates our
central design: construct matched solvable/unsolvable pairs in which
infeasibility is injected by typed mechanical mutation and certified by a script
that checks the altered element is *required* and admits *no substitute*, then
measure whether a third-party attribution system falsely blames the agent when
no success-producing action exists.

---

## Introduction

When an autonomous LLM agent is handed a task — write a SQL query, book a flight
through a tool API, resolve a customer's account issue, run a build script — and
the run ends without success, automated debugging and monitoring systems ask one
question: **what did the agent do wrong?** Failure-attribution systems exist to
answer it, localizing the plan, tool call, or execution step responsible, and
their verdicts increasingly drive automated repair, retry, escalation, and the
training data for the next agent. The strongest current formulations make the
target explicit: attribution is identifying the earliest agent step whose
*counterfactual correction* would have flipped failure into success
\citep{who_when,agentracer}.

That definition presupposes such a correcting step *exists*, and excludes a
practically common failure mode: the task may have been **infeasible before the
agent ever acted** — a required schema element absent, a necessary tool removed,
a requested resource nonexistent, or a goal that contradicts the environment. On
such an instance no success-flipping correction exists, so a system with no
`unsolvable` outcome must still emit a label, and it nominates a culprit — a
*label-restricted* attributor therefore misattributes *every* certified-
unsolvable instance by construction, at an expected false-blame rate near 1.0
(§[control]). This is a *structural* blind spot in the formulation, not a tuning
error of any one judge: an impossible task and an agent that truly failed are
indistinguishable to a vocabulary that has no word for the first.

Turning this blind spot into a measured quantity has been blocked by
measurement, not modeling. A misattribution rate needs ground truth about
solvability, and the two obvious sources both disqualify: human labels do not
scale to the pair counts a rate estimate needs, and the agent's own failure is
circular — it defines "unsolvable" as "whatever the agent did not solve," the
exact conflation under study. Ground truth must therefore come from the task
specification alone, before any agent acts; the soundness of that certification
is the load-bearing assumption of the whole study, and we defend it with a
leakage audit and an adversarial oracle-falsification gate before any rate is
reported.

Prior work touches parts of this problem without isolating it. Attribution
benchmarks \citep{who_when,agentracer,elephant} assume the task is solvable and
the trace holds a decisive error; failure taxonomies \citep{mast} catalog *how*
agent systems fail but provide no mechanically certified task-level
infeasibility; and refusal-and-calibration work treats abstention as a property
of *model knowledge*, not of an external environment. Two recent benchmarks come
closest and are worth conceding precisely. APB \citep{apb} injects broken-tool
and unsolvable tasks and reports the *acting agent's* calibrated-refusal rates,
but validates ground truth by LLM-judge plus human review and never asks whether
a *third-party attributor* misdiagnoses an already-failed trace. Rigorous-
benchmark guidance \citep{abc} certifies that *each task is solvable* as a
quality gate — the mirror image of our move: we certify *unsolvability* by a
script check that the altered element is required and admits no substitute, and
keep it as a first-class measured condition rather than discarding it. No prior
testbed dissociates *unsolvable-for-anyone* from *unsolved-by-this-agent* by
construction, which is the one dissociation the question requires.

We study the missing case directly, around one question: **can agent failure-
attribution systems distinguish "the agent failed" from "the task was
infeasible"?** We construct matched pairs differing only by a typed mechanical
mutation — remove a required schema element, delete a necessary tool, eliminate
an environment resource, or contradict a task constraint. The solvable member
retains a passing reference solution; the unsolvable member is certified by an
oracle script verifying the altered element is *required* and admits *no
substitute* (schema-graph unreachability for SQL, tool-signature non-coverage
for function-calling, an environment-state assertion for stateful tasks). Ground
truth thus holds by construction. Every pair is gated by a leakage audit — a
text-only probe, surface-statistic matching, and a two-rater human check — so no
measured rate can be an artifact of detecting the mutation rather than reasoning
about feasibility.

Over this instrument we evaluate three quantities. The **false-blame rate
(FBR)** — the probability an attributor labels a certified-unsolvable task
`agent_failure`. The reverse **cop-out rate (CoR)** — the probability it labels a
*failed-but-solvable* task `unsolvable`. And the **calibration boundary** — the
confidence attached to the `unsolvable` verdict swept into a per-domain
risk–coverage curve, which is what separates a useful infeasibility detector from
a system that merely refuses more often. A control reader calibrated directly on
the oracle label but evaluated only on held-out pairs then separates a *fixable
attribution-design gap* from a *hard information ceiling* on what a trace can
reveal.

Because ground truth is certified rather than judged, the misattribution rate
becomes measurable for the first time. Across **[N]** matched pairs spanning
**[D]** agent domains, baseline pipelines falsely blame the agent on **[XX.X%]**
of certified-unsolvable instances, exceeding the reverse cop-out rate by
**[YY.Y pp]** — a *directional* over-blame bias, not symmetric confusion. The
oracle-calibrated ceiling probe reaches **[AUROC = CC]** on held-out traces while
the best deployed strategy reaches only **[AUROC = DD]**; per our pre-registered
three-branch rule this locates the gap in **[attribution design / an information
ceiling / INCONCLUSIVE]**. Misattribution is not uniform across domains: a
secondary, exploratory localization (logistic regression on domain, operator
type, and agent family; not a pre-registered directional hypothesis) reports
where over-blame concentrates and by how much. The leakage audit confirms the
pairs are not trivially separable from text alone — the text-only probe obtains
**[AUROC = EE]**, below the pre-registered **[< 0.60]** threshold.

This paper makes four contributions:

1. **Unsolvability as a missing attribution outcome.** We show current
   formulations implicitly assume a success-flipping correction exists, so a
   label-restricted attributor misattributes *every* certified-unsolvable task by
   construction (expected FBR ≈ 1.0).
2. **A mechanically certified paired-task instrument.** Solvable/unsolvable pairs
   whose ground truth is a *script-certified required-and-no-substitute* oracle —
   not human or LLM judgment — gated by a pre-registered leakage audit (text-only
   AUROC below **[0.XX]** per domain), enabling measurement that never relies
   circularly on agent behavior.
3. **A directional misattribution estimand.** We define and measure FBR
   (**[XX.X%]**) and its directional gap over CoR (**[YY.Y pp]**) across domains,
   backbones, and attribution strategies with pair-clustered bootstrap CIs — an
   error an aggregate refusal rate cannot capture.
4. **The calibration boundary of infeasibility attribution.** Per-domain
   risk–coverage curves plus a ceiling-probe control dissociating design-limited
   from information-limited failure.

As agents move into more complex environments, some failures come not from bad
reasoning but from impossible specifications. Attribution should not be a two-way
choice between success and agent error; recognizing infeasibility as a first-
class, calibratable outcome is necessary for reliable debugging, efficient retry,
and trustworthy long-horizon operation.

---

## Placeholder legend (fill from Stage-2 output; do not unbracket before data)

```text
[N]  = matched task pairs                 [D] = domains
[K]  = agent backbones                    [M] = attribution strategies
[XX.X%] = baseline FBR on certified-unsolvable tasks   (H1; floor >= 20%)
[YY.Y pp] = FBR - CoR directional gap                  (H2; floor >= 10 pp)
[CC] = privileged ceiling-probe AUROC (held-out)       (B-alt1)
[DD] = best deployed attributor AUROC                  (H3; floor >= 0.65)
[EE] = text-only leakage AUROC                         (H4; gate < 0.60)
[0.XX] = per-domain leakage-gate value                 (H4)
[control] = forward-ref to the B0-a label-restricted control arm
[domain heterogeneity] = report post hoc; do NOT name a direction as a result
```

Deliberately excluded: `[ZZ%]` "adding the label reduces false blame" and
`[BB pp]` cop-out increase. That is an *intervention* claim with no hypothesis in
Step 6; it belongs in a measurement paper only if a randomized label-space A/B
(H5, with its own alpha and power) is pre-registered first.

## Bib entries required in refs.bib (verify IDs before compile)

```text
who_when    Which Agent Causes Task Failures and When?      arXiv:2505.00212  (ICML'25)
agentracer  AgenTracer: Who Is Inducing Failure ...          arXiv:2509.03312
elephant    Seeing the Whole Elephant: Failure Attribution   arXiv:2604.22708
apb         Agent Planning Benchmark                         arXiv:2606.04874  (concede: agent-refusal vs third-party)
abc         Best Practices for Rigorous Agentic Benchmarks   arXiv:2507.02825  (concede: certify-solvable mirror)
mast        MAST failure taxonomy                            arXiv:2503.13657
```

## Audit trail (this version)

- **pengsida-stage-reviewer (Stage 5): PASS.** Reverse-outline chain reads clean;
  one message per paragraph; contribution quotable ("a directional misattribution
  estimand ... an aggregate refusal rate cannot capture"). Prior REVISE flags
  fixed: Intro ¶2 blind spot now *shown* via forward-ref to the B0-a control; the
  measurement-block argument and the neighbor positioning are now separate
  paragraphs.
- **research-taste-auditor: 🟢.** Opportunity = failure/risk (not Bridge); method =
  empirical-mapping (not Synthesis). Verbs certify/inject/dissociate/measure/gate.
  No firing conditions. Oracle kept prominent so C2 never reads as "assembled four
  datasets."
- **novelty-auditor: 🟢 overall**, carried by the directional estimand (C1, C3).
  C2 (instrument) hardened from 🟡 by conceding both nearest neighbors: APB
  (agent-refusal vs third-party attribution) and ABC (certify-solvable mirror).
  Decay note: fast-publishing cluster; the script-certified no-substitute oracle +
  directional estimand is the durable moat.
- **se-paper-reviewer: no fatal flag.** R2 positioning pre-empts folded in (APB,
  ABC). R3 significance strong for SE (new estimand on verifier-equipped
  benchmarks). Devil's Advocate attacks neutralized: (i) oracle-soundness is now
  named as the load-bearing precondition rather than assumed away; (ii) the
  per-domain direction is marked exploratory/post-hoc, not sold as a
  pre-registered result.
