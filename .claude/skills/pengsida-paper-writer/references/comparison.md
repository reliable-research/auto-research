# Two-Paper Comparison (DPO vs Segment Anything)

A node-by-node comparison of the two digested papers (`digest-examples.md`), then a
reconstruction of each through the skill's archetype lens. This is the "compare the
correlation between two papers" task: where their argument chains align and where they
diverge.

## Node-by-node correlation

| Node | DPO (method) | Segment Anything (resource/foundation) | Correlation |
|---|---|---|---|
| N1 problem | align an LM to preferences w/o RL loop | promptable zero-shot segmentation | Both reframe a task to remove a constraint (RL loop / task-specificity) |
| N2 motivation | steerability of unsupervised LMs | foundation-model zero-shot transfer | Both invoke a broader trend as the "why" |
| N4 prior limits | RLHF unstable/complex | prior models task-specific, supervised | Both attack a *process/scope* limit, not an accuracy gap |
| N5 challenges | stay near reference; avoid RL | general task; mask scale; real-time prompt | DPO: 2 coupled; SAM: 3 independent (task/data/model) |
| N6 method | reparam → closed form → 1 loss | task + model + data-engine co-design | DPO collapses a pipeline; SAM *adds* a pipeline (data engine) |
| N7 contributions | 1 algorithm + 1 empirical finding | task + model + dataset (3, co-designed) | DPO single-thread; SAM multi-artifact |
| N9 results | matches/beats PPO-RLHF, simpler | zero-shot ≈ supervised across tasks | Both claim parity-or-better vs a stronger-resourced baseline |
| N12 type | system/method | tool+dataset / foundation | Different archetypes |

**Strongest correlation:** both are "dissolve-a-constraint" papers — DPO removes the RL
loop while matching PPO; SAM removes task-specificity while matching supervised models. In
the skill's vocabulary both lead with a parity-or-better claim against a more expensive
incumbent. This is the efficiency/frontier *move* (`paper-archetypes.md` §2) operating
inside two different archetypes.

**Strongest divergence:** contribution shape. DPO's N6/N7 is a single mechanism that
*subtracts* complexity; SAM's is three co-designed artifacts that *add* a data engine. A
reviewer reads DPO for elegance (one loss) and SAM for generality (zero-shot breadth) — so
the skill routes them to different abstract templates: DPO → Abstract Version 2
(Challenge→Insight→Contribution); SAM → resource/foundation framing naming task+data+model.

## Reconstruction through the skill

**DPO, reconstructed by the skill** (method archetype, Abstract V2): Task (align LMs) →
Challenge (RLHF complex/unstable, N4) → Insight (reward reparameterization yields a
closed-form optimal policy, N6/M1–M2) → Contribution (DPO = one classification loss, N7/CO1)
→ Benefit (stable, no sampling/tuning, N7/CO2) → Evidence (≥ PPO-RLHF, N9). The skill's
default template reproduces DPO's real abstract structure almost exactly — confirming the
template is well-calibrated for the dominant archetype.

**SAM, reconstructed by the skill** (resource/foundation, §4): name task+model+dataset
together → motivate by what becomes possible (zero-shot transfer) → evidence = transfer
breadth across many tasks, not one benchmark → release as a first-class contribution. The
skill's resource/foundation rules reproduce SAM's structure — which the *original* (method-only)
skill could not represent, validating the archetype expansion from earlier turns.

## What the comparison teaches the skill

1. The "dissolve-a-constraint / parity-or-better" move is archetype-independent and worth
   naming explicitly as a cross-cutting framing (added to `paper-archetypes.md`).
2. The N4-vs-N5 distinction (prior-failure vs inherent difficulty) sharpens the skill's
   Introduction guidance — a paper's challenge paragraph should separate "what prior work
   can't do" from "why the problem is hard regardless" (added to `introduction.md`).
3. Digesting before writing/reviewing gives the skill a checkable structure: extract N1–N12,
   then map each Abstract/Intro claim back to a node — the claim-evidence map becomes node-anchored.
