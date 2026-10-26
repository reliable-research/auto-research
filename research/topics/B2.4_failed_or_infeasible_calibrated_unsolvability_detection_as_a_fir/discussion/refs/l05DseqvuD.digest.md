# Digest (lightweight, backfilled): AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?

- **Title**: AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?
- **OpenReview id**: l05DseqvuD
- **URL**: https://openreview.net/forum?id=l05DseqvuD
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `l05DseqvuD`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
Multi-agent LLM systems now solve tasks through role specialization, message passing, and tool use, but this same structure makes them brittle. As shown by @hong2023metagpt and @li2023camel, these systems produce long collaborative trajectories in which one agent’s early output becomes another agent’s context, so a local mistake can propagate into a global failure. @cemri2025mast makes the severity of this problem explicit by documenting high failure rates and recurring failure modes across mainstream multi-agent frameworks. This implies that improving agentic systems requires more than end-task evaluation; it requires localizing the specific agent-step pair that first made success unattainable.

The core gap is that existing failure analysis methods do not provide scalable, causally grounded attribution. @zhang2025whowhen correctly formulates the problem as identifying the earliest decisive error step, but their results show that even strong reasoning models remain ineffective, especially for step-level localization. This failure is not simply a model-capability issue; it reflects a supervision issue. Available datasets are manually annotated and small, as seen in both @cemri2025mast and @zhang2025whowhen, while judge-style inference asks a general-purpose LLM to infer latent causal responsibility from long trajectories without enough task-specific training data.

This gap matters because precise attribution is the missing interface between failure observation and system imp

## Method (from corpus proposal, truncated)
We propose an automated failure-attribution framework that converts decisive-error localization into a scalable learning problem. The central idea is to generate high-fidelity supervision by replaying trajectories under controlled counterfactual interventions and synthetic perturbations, then train a dedicated tracer with reinforcement learning to predict the responsible agent and earliest decisive step. This formulation directly addresses the data scarcity and weak-judge limitations exposed by @zhang2025whowhen and @cemri2025mast.

1. **Counterfactual Decisive-Error Discovery**: For each failed multi-agent trajectory, we replay the execution while replacing one step at a time with a minimally corrected action proposed by an analyzer model. The earliest step whose correction flips the final outcome from failure to success is labeled as the decisive error, implementing the causal definition introduced by @zhang2025whowhen. This is needed because superficial trace inspection is insufficient; attribution must be grounded in outcome-changing interventions rather than textual plausibility.

2. **Programmatic Fault Injection from Successful Traces**: To expand coverage beyond naturally failed runs, we perturb selected actions in successful trajectories and replay the downstream execution. If the perturbed run fails, the injected step is treated as the decisive error by construction, yielding synthetic but precise labels. This complements the limited manually annotated resources in 

## Limitation (as used in digest.md N4, this topic)
Defines attribution as replaying a failed trajectory with one step at a time counterfactually corrected, and labels as the 'decisive error' the earliest step whose correction flips failure to success — presupposes such a correction exists; has no admissible 'task itself infeasible' outcome.

## Relevance to B2.4
Co-closest prior work (with Who&When, arXiv:2505.00212) named explicitly in the Related Work nearest-neighbor sentence per stage_review.md's Stage 2 fix; B2.4's B0 control (label-space-restricted attributor) directly operationalizes this paper's own label space to show it forces FBR≈1.0 on unsolvable instances by construction.
