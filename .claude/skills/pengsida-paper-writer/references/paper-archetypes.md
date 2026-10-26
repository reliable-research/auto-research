# Paper Archetypes

The section guides default to one archetype: an **empirical method/pipeline** paper
(propose a system, beat baselines, ablate modules). That covers most submissions, but
top-tier best papers regularly take other shapes. Before drafting, identify the
archetype — it changes what counts as the contribution, the Introduction spine, and the
evidence reviewers expect. This guide was tightened by regression-testing the skill
against a random sample of 28 award/outstanding papers across 8 venues; the measured
archetype mix was method/pipeline 46%, resource/foundation 36%, analysis/position 11%,
theory 4%, efficiency-as-primary-frame 4% (see `corpus-evidence.md`). Representative
winners: DPO, Segment Anything, 3D Gaussian Splatting, Visual Autoregressive Modeling,
"Vision Transformers Need Registers", "Are Emergent Abilities of LLMs a Mirage?",
D-Adaptation.

## 1. Empirical Method / Pipeline (default)

Contribution = a new method/module/representation that improves a task. Use the standard
guides as-is: `introduction.md`, `method.md`, `experiments.md`. Evidence = SOTA
comparison + ablations + harder-setting generalization. Example: DPO (a simpler training
objective that matches/beats PPO-RLHF) maps exactly onto Abstract Version 2
(Challenge → Insight → Contribution).

## 2. Efficiency / Pareto-Frontier (a sub-mode of method papers)

Contribution = matching or beating quality while being dramatically cheaper/faster/
smaller — the headline result *is* the contribution. Example: 3D Gaussian Splatting
(SOTA quality at real-time speed). Writing rules:

1. State the frontier explicitly and quantitatively in the Abstract: "comparable/better
   [quality metric] at [N×] [speed/memory/cost]". One sentence, with both axes.
2. In the Introduction, make the trade-off prior methods accept the technical challenge
   (e.g. "quality methods are too slow; fast methods lose quality"); your method dissolves
   the trade-off.
3. In Experiments, the primary evidence is a two-axis comparison (quality vs cost), not a
   single-axis table. Plot or tabulate both; report the operating point, hardware, and
   protocol so the efficiency claim is verifiable and fair.
4. Beware the reviewer question "cheaper, but at what hidden cost?" — pre-empt it
   (quality parity at the SAME setting, no per-scene retuning).

## 3. Analysis / Refutation / Position

Contribution = a *finding* or *reframing*, not a system. Examples: "Are Emergent
Abilities a Mirage?" (emergence is an artifact of discontinuous metrics); position papers.

1. The Abstract's "contribution" slot holds a claim, not a method: state the prevailing
   belief, then your counter-claim, then the form of evidence (re-analysis, new metric,
   controlled experiment, theory).
2. Replace the Method section with a **claim-and-argument** structure: state the
   hypothesis, the test that could falsify it, and the analysis that supports it.
3. Be scrupulously fair: represent the view you challenge at its strongest (no strawman).
   Reviewers reject analysis papers mainly for unfairness or over-claiming.
4. Evidence = re-analysis, measurement-sensitivity studies, or predictive tests (see the
   new evidence types in `experiments.md`). Quantify the claim's scope and its limits.

## 4. Resource / Dataset-Benchmark / Foundation Model

Contribution = a task, dataset, benchmark, or broadly transferable model — value comes
from **generality and reuse**, not a single-benchmark win. Examples: Segment Anything
(promptable-segmentation task + SAM model + SA-1B dataset), large open corpora/models.

1. Co-design framing: when the contribution is task + data + model together, the Abstract
   should name all three and tie them to one goal (e.g. zero-shot transfer).
2. The Introduction motivates by **what becomes possible** (downstream tasks, zero-shot
   use), not by beating one prior number.
3. Evidence = breadth: zero-shot/few-shot transfer across many downstream tasks and
   domains, plus dataset statistics, collection protocol, and quality/ethics controls.
4. Reproducibility/release is a first-class contribution here: state exactly what is
   released (data, code, weights, license) and document it for reuse.
5. Pre-empt "does it really transfer, or only on your eval?" with diverse, held-out
   transfer settings.

## 5. Theory-Driven

Contribution = a guarantee, bound, or impossibility result. Example: D-Adaptation
(learning-rate-free optimization with a convergence guarantee).

1. The Abstract states the result and the conditions under which it holds; the practical
   payoff (e.g. one fewer hyperparameter) is the benefit sentence.
2. Replace module-design subsections with: setting/assumptions → main theorem (informal)
   → proof sketch/intuition → consequences. State assumptions honestly; their tightness
   is part of the contribution.
3. Evidence = the proof, plus empirical confirmation that the assumptions and the
   predicted behavior hold in practice. A theory paper still benefits from experiments
   that test the bound's predictions.

## Cross-Cutting Move: Dissolve-a-Constraint / Parity-or-Better

Independent of archetype, many award papers share one framing: they remove a constraint the
incumbent approach was assumed to require, while matching or beating it. DPO removes the RL
loop and still matches PPO-RLHF; 3D Gaussian Splatting removes the speed/quality trade-off;
Segment Anything removes task-specificity and matches supervised models. The recipe:

1. Name the constraint prior work treats as necessary (an RL loop, per-task training, a
   quality/speed trade-off).
2. State your parity-or-better result against the stronger-resourced incumbent in one
   sentence, with the constraint explicitly dropped.
3. Make the mechanism that dissolves the constraint the core contribution.

This pairs with whatever archetype applies (method, efficiency, resource). When a paper has
this shape, lead the abstract with the dissolved constraint plus the parity claim.

## Diagnosis-First (a spine used by archetypes 1 and 3)

Some papers lead with characterizing a phenomenon, then fix or explain it. Example:
"Vision Transformers Need Registers" (characterize high-norm artifact tokens → add
register tokens to remove them). Spine: observe a concrete anomaly → characterize it
empirically → diagnose the cause → minimal intervention → show the anomaly is gone and
downstream metrics improve. This pairs with Introduction "Pipeline Version 4
(observation-driven)" but adds an explicit empirical **diagnosis** beat before the fix.

## How to use this file

1. Pick the archetype (a paper can be a primary archetype with a secondary mode, e.g.
   method + efficiency, or analysis + theory).
2. Apply the archetype-specific rules above on top of the standard section guides.
3. Study the matching worked exemplar in `examples/archetype-examples.md` — one annotated
   real award abstract per archetype (DPO, 3D Gaussian Splatting, "Emergent Abilities a
   Mirage?", Segment Anything, "Is OOD Detection Learnable?").
4. Re-check the five reject dimensions in `paper-review.md`, including the archetype-aware
   reviewer lenses added there.
