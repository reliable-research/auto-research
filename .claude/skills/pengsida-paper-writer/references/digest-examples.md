# Paper Digest (N1–N12) — Two Corpus Papers

Applying the `paper-knowledge-service` extraction schema (N1–N12 argument chain)
to two downloaded award papers. Source abstracts: `assets/corpus-sample/`. This
follows the node definitions in the uploaded digest (n1_problem … n12_contribution_type),
including the N4/N5 motivation-vs-limitation-vs-inherent-challenge distinction and the
N6 challenge→mechanism mapping.

═══════════════════════════════════════════════════════════════════════════════
## Paper A — Direct Preference Optimization (NeurIPS 2023 Outstanding Runner-Up)
═══════════════════════════════════════════════════════════════════════════════

**N0 metadata** — DPO; Rafailov et al.; NeurIPS 2023; ML/NLP.

**N1 problem (objective)** — Steer a pretrained LM to align with human preference data
*without* the RLHF reward-model + RL loop. Inputs: a pretrained LM + a dataset of pairwise
human preferences. Outputs: a fine-tuned policy. Constraint: stay close to the reference
model; objective: maximize agreement with preferences via a single optimization.

**N2 motivation** — Precise control of LM behavior is hard because pretraining is
unsupervised; steerability matters for deployment.

**N4 prior limitations** — RLHF is "complex and often unstable": it first fits a reward
model, then runs RL, requiring sampling from the LM and heavy hyperparameter tuning.

**N5 challenges (inherent)** — C1: optimizing a preference objective while not drifting
from the reference model. C2: doing so without an unstable RL inner loop.

**N6 methodology** — overview: reparameterize the reward so the optimal policy has a
closed form, turning RLHF into one classification loss.
key_components: M1 = reward reparameterization (reward expressed via the policy);
M2 = closed-form optimal-policy mapping; M3 = simple classification (logistic) loss.
challenge_arguments: C1 ← [M1, M2] (closed form keeps the policy tied to reference);
C2 ← [M3] (classification loss removes the RL loop). unaddressed: none claimed.

**N7 contributions** — CO1: DPO algorithm (technical_artifact, testable). CO2: stability +
no sampling/tuning (empirical_finding, testable).

**N9 results** — Matches/exceeds PPO-RLHF; exceeds PPO on sentiment control; matches or
improves summarization & single-turn dialogue; simpler to train.

**N12 contribution_type** — `system`/method. Rationale: the central contribution is a new
training algorithm (DPO), not a dataset, benchmark, or measurement study.

═══════════════════════════════════════════════════════════════════════════════
## Paper B — Segment Anything (ICCV 2023, SA project)
═══════════════════════════════════════════════════════════════════════════════

**N0 metadata** — Segment Anything (SAM/SA-1B); Kirillov et al.; ICCV 2023; CV.

**N1 problem (objective)** — Build a promptable image-segmentation foundation model that
transfers zero-shot to new image distributions and tasks. Inputs: an image + a prompt.
Outputs: a valid segmentation mask. Constraint: generality across tasks; objective:
zero-shot transfer without task-specific training.

**N2 motivation** — Foundation models reshaped NLP/CV via zero-shot transfer; segmentation
lacks an equivalent, so building one unlocks many downstream tasks.

**N4 prior limitations** — Prior segmentation models are task-specific and fully supervised;
they do not transfer zero-shot to new distributions/tasks.

**N5 challenges (inherent)** — C1: define a task general enough to enable zero-shot transfer.
C2: obtain enough mask supervision at scale. C3: design a model that is promptable in real
time.

**N6 methodology** — overview: co-design a promptable task, a promptable model, and a
data engine that bootstraps a massive dataset.
key_components: M1 = promptable segmentation task; M2 = SAM (image encoder + prompt encoder
+ fast mask decoder); M3 = data engine (model-in-the-loop annotation) → SA-1B (1B masks /
11M images). challenge_arguments: C1 ← [M1]; C2 ← [M3]; C3 ← [M2]. unaddressed: none claimed.

**N7 contributions** — CO1: promptable segmentation task (conceptual_framework). CO2: SAM
model (technical_artifact/tool). CO3: SA-1B dataset (dataset). All released.

**N9 results** — Zero-shot performance across numerous tasks "often competitive with or
even superior to" fully-supervised prior results.

**N11 artifacts** — has_code/has_model/has_data all true; SAM + SA-1B released at
segment-anything.com (license-respecting, privacy-respecting).

**N12 contribution_type** — `dataset`+`tool`/foundation (per the digest enum, the WHOLE-paper
filing is best read as a resource/foundation contribution; the digest would likely tag `tool`
since artifact release is central, with the dataset as a co-headline). Rationale: the value is
generality + released artifacts, not a single-benchmark method win.

═══════════════════════════════════════════════════════════════════════════════
## Why this digest matters for the skill
═══════════════════════════════════════════════════════════════════════════════

The N4/N5 split (prior-failure vs problem-inherent difficulty) is exactly the distinction
the skill's Introduction "technical challenge" guidance blurs. The N6 challenge→mechanism
mapping is a sharper version of the skill's method "three elements". And N12's 11-value enum
is a superset of the skill's 5 archetypes — see `comparison.md` for the reconciliation.
