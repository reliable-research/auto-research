# Skill Regression Against Top-Tier Best Papers

Goal: run each skill template against a real award-winning paper, mark where the skill
predicts/explains the paper's structure (PASS) and where it has no slot for what the
paper actually does (GAP -> patch).

## Sample (best/outstanding papers across venues)
- DPO — NeurIPS 2023 Outstanding Runner-Up (ML/NLP, method)
- Segment Anything — ICCV 2023 (CV, task+dataset+model / foundation model)
- 3D Gaussian Splatting — SIGGRAPH 2023 Best (CG, representation/system, speed claim)
- Visual Autoregressive (VAR) — NeurIPS 2024 Best (CV/generative, scaling-law finding)
- Vision Transformers Need Registers — ICLR 2024 Outstanding (CV, diagnosis->fix)
- "Are Emergent Abilities a Mirage?" — NeurIPS 2023 Outstanding (analysis/position, no new method)
- "Segment Anything" + LAION/Datasets&Benchmarks track — dataset/benchmark papers
- "Learning-Rate-Free Learning (D-Adaptation)" — ICML 2023 Outstanding (theory/optimizer)

## Test 1 — Abstract templates (Challenge->Contribution / +Insight / Multi-contribution)

DPO abstract maps cleanly:
  Task: align LMs to human preference.
  Challenge: RLHF is complex/unstable (reward model + RL).
  Insight: reward model can be reparameterized so optimal policy is closed-form.
  Contribution: DPO = solve RLHF with a simple classification loss.
  Benefit: stable, lightweight, no sampling/heavy tuning.
  Experiment: matches/beats PPO-RLHF on sentiment/summarization/dialogue.
  -> PASS, exactly Version 2 (Challenge->Insight->Contribution). Skill nails this.

3D Gaussian Splatting:
  Lead claim is SPEED + QUALITY simultaneously (real-time 1080p, SOTA quality).
  Skill abstract templates have "benefit" + "experiment summary" but no explicit
  guidance that the headline result can BE the contribution (a Pareto/efficiency
  frontier: same quality, radically faster). The "contribution+advantage" sentence
  exists (V3) but the skill never tells you a quantified frontier claim
  (X quality at Yx speed) is a first-class abstract move.
  -> GAP A: efficiency/Pareto-frontier contributions ("as good but Nx faster/cheaper").

"Are Emergent Abilities a Mirage?":
  No new task, no method, no pipeline. Contribution = a claim that overturns a belief,
  backed by analysis (emergence is an artifact of nonlinear/discontinuous metrics).
  Skill abstract + intro templates ALL assume a method/pipeline contribution.
  -> GAP B: analysis / refutation / "position" papers (contribution is a finding, not a system).

Segment Anything:
  Three coupled contributions: task (promptable segmentation) + model (SAM) + data engine/dataset (SA-1B).
  Skill V3 handles "multiple contributions", but the SAM story is specifically
  task+model+data co-design for a FOUNDATION MODEL / zero-shot transfer claim.
  Skill has no notion of "we release a task+dataset+model and the contribution is
  generality/zero-shot transfer", which is now a dominant CV/NLP paper archetype.
  -> GAP C: resource/foundation-model papers (dataset+benchmark+model, generality claim).

## Test 2 — Introduction logic map (task->metric->SOTA fails->root issue->our fix->why)

Vision Transformers Need Registers:
  Story is: observe an ARTIFACT (high-norm tokens in feature maps) -> diagnose cause
  -> minimal fix (add register tokens). This is "Pipeline Version 4 (observation-driven)"
  -> mostly PASS, the observation-driven template fits. Good.
  BUT the paper's spine is a DIAGNOSIS section (characterize the phenomenon) that
  precedes the fix. Skill's intro logic jumps task->SOTA-fail->our-method and has no
  first-class "phenomenon characterization / empirical diagnosis" beat.
  -> GAP D: diagnosis-first papers (characterize a phenomenon, then fix it).

D-Adaptation (learning-rate-free):
  Contribution is removing a hyperparameter with a theoretical guarantee.
  Skill intro/method are entirely empirical-pipeline shaped; no slot for a theorem
  as the core contribution, proof sketch, or assumption/limitation of a bound.
  -> GAP E: theory-driven contributions (a guarantee/bound is the deliverable).

## Test 3 — Experiments guide (baselines / ablations / harder settings)

Skill's 3 core questions (better than baselines? which module? generalize?) PASS for
DPO, SAM, 3DGS. But:
  - VAR / scaling-law-finding papers: the key evidence is a SCALING CURVE + an
    emergent property (power-law fit, zero-shot generalization), not a single SOTA table.
    Skill experiments guide has no "scaling study / power-law" evidence type.
  - "Emergent Abilities a Mirage": the key experiment is a RE-ANALYSIS under a changed
    metric, plus a predictive test. Skill has no "reanalysis / measurement-choice
    sensitivity" experiment type.
  -> GAP F: scaling studies and re-analysis/measurement-sensitivity as evidence types.
  - Foundation/zero-shot papers evaluate by TRANSFER across many downstream tasks
    (zero-shot/few-shot), not just one benchmark + ablation.
  -> GAP G: zero-shot/transfer-suite evaluation across many tasks.

## Test 4 — Paper-review dimensions (5 reject dimensions)

The 5 dimensions hold for method papers. Missing reviewer lenses surfaced by sample:
  - Reproducibility / open release (SAM, OLMo, LAION): release of code+data+weights is a
    scored contribution at top venues now; skill treats reproducibility only as "writing clarity".
  - Claim scope vs generality: foundation-model claims invite "does it really transfer
    or just on your eval?" — a distinct reject axis.
  - For analysis/position papers: "is the claim a strawman? is the reframing fair?"
  -> GAP H: add reviewer lenses for release/reproducibility and for analysis/position claims.

## Summary of patches
A. Efficiency/Pareto-frontier contribution pattern (abstract + intro + experiments).
B. Analysis / refutation / position paper archetype (whole new section guide).
C. Resource / dataset-benchmark / foundation-model archetype (whole new section guide).
D. Diagnosis-first beat in introduction + method.
E. Theory-driven contribution beat (theorem/guarantee/proof-sketch/assumptions).
F. Scaling-study and re-analysis evidence types in experiments.
G. Zero-shot / transfer-suite evaluation type in experiments.
H. New reviewer lenses (reproducibility/release; analysis-claim fairness) in paper-review.
