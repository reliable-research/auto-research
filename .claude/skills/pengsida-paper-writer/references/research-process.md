# Research Process Guide

Distilled from Prof. Peng Sida's `learning_research` notes (problem finding, idea
generation, experiments, rebuttal, slides). The writing templates live in the section
guides; this file covers everything around the writing.

## The Core Capability of a Top Student

Set a long-horizon research goal that has real scientific and practical value (find
genuinely valuable problems inside real applications). Derive a roadmap from that goal.
Each paper should solve a piece of the goal and visibly show progress along the roadmap.
Aim for demos that are clearly compelling.

A paper requires three trainable capabilities: generating ideas (finding important
problems + proposing solutions), writing/presentation, and experiments.

## Stage Model (how to ramp up)

1. Breadth first: learn deep-learning fundamentals for coverage, not depth — know which
   algorithms exist, their rough principles, and where they apply. Do course assignments;
   completing them is the real test of understanding.
2. Depth next: shadow a senior student's project. Master one paper end to end — algorithm
   details and implementation details — to learn how a paper is actually produced
   (problem → idea → experiments → writing). Get a customized study plan for your chosen
   sub-direction.
3. First-author project: under guidance, drive your own project, ideally to a submission.
   Research differs sharply from coursework: it is frontier and open-ended, so there is no
   fixed route — expect iteration and mentorship.

## Generating Ideas

1. Anchor on importance. A good problem is one whose solution gives readers new knowledge
   and matters in a real application — not a common or trivial failure case.
2. Build field vision by reading papers actively: for each, extract the task, the precise
   technical challenge, the insight, and why the method works (the same four questions used
   when writing an Abstract/Introduction).
3. Prefer ideas where the expected gain is surprising or insightful rather than a
   predictable, well-explored improvement.
4. State the candidate idea as: target failure case + technical reason it persists +
   your insight + why your insight resolves the reason. If any slot is vague, the idea is
   not ready.

## Running and Debugging Experiments

1. Plan experiments backward from claims. Each claimed contribution needs a validation
   experiment; each key module/parameter needs an ablation. (See `experiments.md`.)
2. Keep a disciplined experiment log: hypothesis, setup, change made, result, and the
   conclusion drawn. Without a log, results are not reusable.
3. When something does not work, the skill is diagnosis: form a hypothesis for the failure,
   isolate one variable, and test it. Treat "why it failed" as a first-class question, not
   an afterthought — most progress comes from understanding negative results.
4. Keep protocols fair and fixed (same split, preprocessing, evaluation) so comparisons and
   ablations are trustworthy.

## Weekly Meeting / Presentation Discipline

1. Present progress as a short PPT each week: what was claimed, what was tested, what the
   result implies, what is next. This trains the same compression skill that good writing
   needs.
2. Make the story legible to someone outside your immediate problem; if they cannot follow
   the motivation, neither will a reviewer.

## Rebuttal

1. Read every review charitably and extract the underlying concern behind each comment,
   not just the surface wording.
2. Group concerns by the five rejection dimensions (contribution, clarity, empirical
   strength, evaluation completeness, method soundness — see `paper-review.md`).
3. For each concern, respond with concrete evidence: a number, a new experiment, a
   clarified claim, or an explicit scope statement. Concede what is fair; defend what is
   supported; never argue without evidence.
4. Prioritize the concerns most likely to drive the score. Fix the paper where the rebuttal
   reveals a real gap, not only the response letter.

## Slides / Talks

1. Lead with the problem and why it matters, then the insight, then results — the same
   backward-then-forward logic as the Introduction.
2. One message per slide; let figures and demos carry the impact. Keep the demo memorable.

## Recommended Outside Reading (referenced by the original notes)

Research-method essays by Bill Freeman, John Schulman, Michael Nielsen, Zhihua Zhou,
Zhilin Yang, Richard Hamming ("You and Your Research"), and Xintao Wang's notes on
research programming and experiments. Seek these out when building research taste.

Source: https://github.com/pengsida/learning_research
