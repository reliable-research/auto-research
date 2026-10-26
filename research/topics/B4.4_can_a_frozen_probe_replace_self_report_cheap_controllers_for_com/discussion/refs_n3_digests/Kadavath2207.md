# Digest (stub, general-knowledge): Language Models (Mostly) Know What They Know

> **Source disclosure.** No PDF is cached locally for arXiv:2207.05221 in this environment (offline
> corpus). This stub is included per digest.md N3 item 10's own disclosure: "Included from general
> knowledge with high confidence; not retrieved from the local corpus." No numeric results are
> asserted here to avoid fabrication -- only the well-established framing that the paper introduces.
> Tag: [HYPOTHESIS] (general-knowledge, non-corpus) per digest.md's own convention for this entry.

- **arxiv_id**: 2207.05221
- **paper_url**: https://arxiv.org/abs/2207.05221

## N2 Motivation (paraphrased, general knowledge -- not a verbatim quote)

Large language models are increasingly deployed in settings where knowing whether an answer is
likely correct matters as much as the answer itself. Whether models' self-evaluations (elicited
confidence, or the probability they assign to "the proposed answer is true") track actual
correctness is an open question with direct implications for any system that wants to use a
model's own signal to decide when to trust, defer, or seek more compute.

## N6 Methodology (paraphrased, general knowledge -- not a verbatim quote)

Studies how well a model's self-reported confidence (verbalized judgments, and a "P(True)"-style
probability that a proposed answer is correct, read from the model itself) correlates with actual
correctness across tasks and model scales, and how that calibration behaves under distribution
shift and multi-answer settings.

## Status

PARTIAL -- included as the canonical, widely-cited source for the self-report/verbalized-confidence
and P(True) elicitation formats this paper's own M3b operationalizes; no PDF cached locally, so no
paper-specific numbers are asserted here. See digest.md N3 item 10 for this paper's role in the
B4.4 lineage.
