# Lightweight digest (backfill): SAFER: Risk-Constrained Sample-then-Filter in Large Language Models

> **BACKFILL NOTICE.** This is not a full paper-digest N0-N12 extraction. It is a
> lightweight digest built from this topic's own digest.md N3 grounded-corpus
> record plus the underlying topics/corpus/ideas.jsonl proposal text (motivation +
> method, read from the paper's own OpenReview submission), created during the
> Phase A reference-cache upgrade because this paper is already cited as related
> work in digest.md/paper.md but had no standalone cache record. No local PDF
> is cached for this OpenReview id (see verified.id_resolves in
> reference_candidates.jsonl); the OpenReview forum id is real and resolvable
> externally.

- **Title**: SAFER: Risk-Constrained Sample-then-Filter in Large Language Models
- **OpenReview id**: kJmLmOvwLC
- **URL**: https://openreview.net/forum?id=kJmLmOvwLC

## Motivation (from the paper's own OpenReview submission text)

Open-ended QA with LLMs poses a risk-control problem that is not fully resolved by existing conformal methods. Prior work has shown that sampling multiple generations and then calibrating prediction sets can provide correctness coverage guarantees in free-form settings, using either self-consistency statistics as in @wang2024conu or a sample-then-identify pipeline as in @wang2025sample. Related work on generative conformal prediction further demonstrates that stopping and rejection rules can be calibrated over sampled outputs rather than logits, making the approach suitable for black-box or open-ended models @quach2024clm. However, these methods effectively presuppose that a correct or admissible answer can be obtained by finite sampling often enough for the target risk to be achievable.

That assumption is especially problematic in open-ended QA, where the output space is unbounded and some questions may simply not yield an admissible answer within any practical sampling cap. The limitation is visible in uncertainty-driven conformal methods based on semantic entropy, which quantify uncertainty over sampled generations but still condition on the sampled pool containing the correct answer candidate @kaur2024sescp; @kuhn2023semantic. As a result, if the desired coverage level is infeasible under bounded sampling, prior calibration procedures can return parameters that appear valid on calibration data yet do not translate into reliable test-time control.

This gap creates a concrete opportunity: instead of treating sampling adequacy and answer filtering as a single implicit process, we can model them as two distinct sources of failure and calibrate each separately. The sampling stage should explicitly test whether bounded sampling can meet a user-specified miscoverage target at all, drawing on parameter-search ideas from @angelopoulos2025ltt. The filtering stage should then operate only on the regime where admissible answers are present and use conformal risk control to prune distractors without sacrificing valid answers, as enabled by @angelopoulos2024crc. This formulation is better aligned with the actual failure modes of open-ended QA systems and enables principled abstention when the requested risk level is unattainable.

## Method (from the paper's own OpenReview submission text)

We propose SAFER, a two-stage risk-control framework for open-ended QA that decomposes failure into sampling miscoverage and filtering-induced exclusion. The key idea is to first calibrate the minimum sampling budget that can statistically cover at least one admissible answer under a bounded sampling cap, with abstention when that target is infeasible, and then calibrate a filtering threshold that removes unreliable candidates while controlling the probability of discarding all admissible ones. This addresses the central gap in prior methods by no longer assuming that finite sampling always suffices.

1. **Abstention-aware sampling calibration**: We calibrate a sampling budget s over a held-out calibration set by measuring, for each candidate budget up to a maximum cap M, how often the sampled set fails to contain any admissible answer. Using an exact binomial upper confidence bound via the Clopper-Pearson method, we select the smallest s whose upper-bounded miscoverage is below the target risk α; if even s = M fails, the system abstains. This extends the sampling-budget logic of @wang2025sample with a statistically explicit feasibility test, and operationalizes the parameter-search perspective of @angelopoulos2025ltt for bounded open-ended generation.

2. **Admissibility-based calibration subset construction**: After fixing the calibrated sampling budget, we restrict filtering calibration to calibration examples whose sampled candidate sets already contain at least one admissible answer. This separation is necessary because filtering risk should measure only the chance of removing admissible answers that were successfully captured during sampling, rather than conflating failures of generation and failures of post-processing. The design departs from prior conformal QA formulations such as @wang2024conu and @kaur2024sescp by making the conditioning event explicit.

3. **Uncertainty scoring for candidate answers**: For each sampled answer, we compute an uncertainty score that reflects answer reliability and supports downstream thresholding. SAFER can use entropy-style measures motivated by semantic uncertainty work such as @kuhn2023semantic, and the formulation is also compatible with candidate-set statistics like self-consistency frequencies from @wang2024conu. This component is needed because open-ended sampling produces many distractors, and filtering requires a scalar signal that correlates with answer admissibility.

4. **Conformalized filtering via risk control**: We calibrate an uncertainty threshold t on the admissibility-conditioned calibration subset using conformal risk control, so that the probability that filtering removes all admissible answers is controlled by a second risk level β. Concretely, we define a monotone loss indicating whether the filtered set contains no admissible answer, and select the smallest threshold satisfying the CRC bound. This directly adapts the general threshold-calibration machinery of @angelopoulos2024crc to answer-set filtering in open-ended QA.

5. **Compositional two-stage guarantee**: At test time, we first sample using the calibrated budget and either abstain if the target risk was infeasible or proceed to filtering with the calibrated threshold. Because the two stages control distinct events—failure to sample any admissible answer and failure to preserve sampled admissible answers—the overall miscoverage can be bounded by combining the stagewise risks. This retains the staged spirit of @wang2025sample while correcting its finite-sampling assumption through explicit abstention and risk decomposition.

Together, these components form a coherent system because each calibration stage addresses one identifiable failure mode and passes a statistically controlled candidate set to the next. The result is a practical open-ended QA pipeline that preserves formal guarantees even when some queries cannot be answered reliably within finite sampling.
