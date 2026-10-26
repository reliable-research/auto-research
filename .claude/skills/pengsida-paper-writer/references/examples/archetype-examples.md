# Worked Archetype Examples

One annotated exemplar per archetype, taken from the downloaded corpus
(`../corpus/manifest.json`). Each shows how the archetype's abstract move maps onto real
award-winning text. The full abstracts are in `../../assets/corpus-sample/`. Reuse the
*structure*, never the wording.

## Method / Pipeline — DPO (NeurIPS 2023 Outstanding Runner-Up)

Abstract Version 2 (Challenge → Insight → Contribution), the skill's default:

1. Task: precise control of LM behavior / alignment to human preference.
2. Challenge: "RLHF is a complex and often unstable procedure" — reward model + RL loop.
3. Insight (one sentence): a new parameterization of the reward model lets the optimal
   policy be extracted in closed form.
4. Contribution: this turns RLHF into a single classification loss (named DPO).
5. Benefit: stable, lightweight, no sampling, no heavy tuning.
6. Experiment summary: matches or beats PPO-RLHF on sentiment, summarization, dialogue.

Why it works: the insight sentence is separate from, and motivates, the contribution
sentence — exactly the V2 split. Note the contribution sentence names the method and its
form ("simple classification loss") without describing every step.

## Efficiency / Frontier — 3D Gaussian Splatting (SIGGRAPH 2023 Best Paper)

The headline result *is* the contribution; both axes appear up front (see
`paper-archetypes.md` §2 and the abstract Special Case):

1. Task + prior trade-off as the challenge: radiance-field methods get high quality but
   are "costly to train and render, while recent faster methods inevitably trade off
   speed for quality" — and none reach real-time at 1080p. The trade-off is stated as the
   thing the paper dissolves.
2. Frontier claim with both axes quantified: "state-of-the-art visual quality" AND
   "high-quality real-time (>= 30 fps) ... at 1080p resolution." Quality and cost in the
   same breath.
3. The three contributions each tie to the frontier (representation that avoids empty-space
   compute; optimization/density control; fast visibility-aware renderer).

Lesson: do not bury the speed axis in the experiment summary; the operating point
(30 fps, 1080p, unbounded scenes) is in the abstract so the efficiency claim is concrete.
This abstract also carries a secondary scaling-free Version-3 multi-contribution shape.

## Analysis / Refutation / Position — "Are Emergent Abilities a Mirage?" (NeurIPS 2023 Outstanding)

The contribution is a *finding*, not a system (see `paper-archetypes.md` §3):

1. Prevailing belief, stated fairly at its strongest: LLMs show emergent abilities that are
   "sharp" and "unpredictable." The challenged view is given its real force first — no
   strawman.
2. Counter-claim: the apparent emergence comes from "the researcher's choice of metric
   rather than ... fundamental changes in model behavior with scale."
3. Form of evidence (the "experiment" slot for analysis papers): a simple mathematical
   model plus three independent tests — predictive tests on GPT-3/InstructGPT, a
   meta-analysis over BIG-Bench, and a constructive demonstration (induce "emergence" at
   will in vision tasks by changing the metric). This is the re-analysis / measurement-
   sensitivity + predictive-test evidence pattern in `experiments.md`.
4. Scope stated honestly: emergence "may not be a fundamental property" — a bounded claim,
   not an over-generalization.

Lesson: represent the opposing view strongly, make a falsifiable counter-claim, and back
it with re-analysis under changed measurement plus a predictive test.

## Resource / Foundation Model — Segment Anything (ICCV 2023, SA project)

Task + data + model co-designed; value is generality and release (see §4):

1. All three named together and tied to one goal: "a new task, model, and dataset for
   image segmentation."
2. Scale/data engine as a contribution: a data-collection loop yields "over 1 billion
   masks on 11M ... images."
3. Generality is the claim, not a single-benchmark win: the model is "promptable, so it can
   transfer zero-shot to new image distributions and tasks," evaluated across "numerous
   tasks" with zero-shot often competitive with fully supervised prior work.
4. Release/reproducibility is explicit and first-class: SAM + SA-1B released to "foster
   research into foundation models."

Lesson: the abstract motivates by what becomes possible (zero-shot transfer across many
tasks) and treats the released artifacts as part of the contribution.

VAR (NeurIPS 2024 Best Paper) is a hybrid worth noting: primarily a method, but its
abstract leans on two non-method evidence types this skill now covers — a power-law
scaling study ("linear correlation coefficients near -0.998") and zero-shot downstream
transfer (in/out-painting, editing). Use the scaling-study and transfer-suite evidence
types in `experiments.md` even inside a method paper when the contribution is a property.

## Theory — "Is OOD Detection Learnable?" (NeurIPS 2022 Outstanding)

The deliverable is a set of guarantees/impossibility results (see §5):

1. Setting + assumptions: PAC learnability of OOD detection, posed as an open problem.
2. Main results stated honestly, including the negative ones: a necessary condition for
   learnability, then "several impossibility theorems" under some scenarios.
3. Practical reconciliation: those impossibility conditions "may not hold in some practical
   scenarios," so the paper gives necessary-and-sufficient conditions characterizing
   learnability where it *is* achievable.
4. Consequences: the theory retro-explains several representative empirical OOD methods.

Lesson: a theory abstract states the result and the conditions under which it holds,
acknowledges the limits (impossibility regimes), and connects back to practice — rather
than describing a pipeline.
