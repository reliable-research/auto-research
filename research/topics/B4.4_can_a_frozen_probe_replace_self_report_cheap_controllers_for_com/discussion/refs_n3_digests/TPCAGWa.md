# Digest (stub, corpus-grounded): Beyond Linear Probes: Dynamic Safety Monitoring for Language Models

> **Source disclosure.** This is a minimal N0/N1/N2/N6-only digest built from the OpenReview submission's own reconstructed proposal text in the local corpus (`openview_corpus/ideas.jsonl`, paper_id `AGWa8whf92`) -- no full PDF is cached locally for this OpenReview-only submission, so N3-N12 (related work read by the authors, results, threats, artifacts) are NOT available and are intentionally omitted rather than guessed. This is the same source digest.md's own N3/N4 quote from. Tag: [GROUNDED:corpus].

- **paper_id**: AGWa8whf92
- **paper_url**: https://openreview.net/forum?id=AGWa8whf92

## N2 Motivation (verbatim from proposal.motivation)

Large language model safety systems increasingly rely on automated monitors that detect harmful prompts or unsafe model behavior before responses are generated. Many practical moderation pipelines employ classifiers trained on datasets such as those introduced in @han2024wildguard to identify malicious intent or adversarial jailbreak attempts. However, high‑accuracy moderation systems are often implemented using large language models themselves, which introduces substantial computational overhead when deployed as always‑on safety monitors.

Activation‑space probes provide a promising alternative because they reuse the representations already produced by the base model. Linear probes introduced by @alain2017linearprobe have demonstrated that many high‑level concepts are detectable directly from hidden representations using simple classifiers. These probes are extremely efficient and have therefore become a popular choice for monitoring internal model states. Nevertheless, their representational capacity is limited: a linear probe can only detect safety signals that are linearly separable in activation space. Evidence from recent representation analysis suggests that many neural features are not strictly linear, indicating that safety‑relevant patterns may depend on interactions among multiple neurons.

Recent work such as @cunningham2025cheapmonitors addresses this limitation by cascading inexpensive probes with more powerful downstream models, typically routing uncertain cases to an additional LLM monitor. While effective, this strategy introduces architectural complexity and requires additional models at inference time. This motivates the search for a monitoring approach that can both increase expressive power beyond linear probes and adapt its computational cost dynamically—without relying on external monitoring systems.

## N6 Methodology (verbatim from proposal.method)

We propose Truncated Polynomial Classifiers (TPCs), an activation‑space monitoring framework that extends linear probes with progressively evaluable polynomial terms. The core idea is to represent the safety classifier as a polynomial over the model’s hidden activations, where each degree captures increasingly complex neuron interactions. Because polynomial expansions are additive across degrees, the classifier can be evaluated incrementally, enabling dynamic scaling of monitoring strength during inference.

1. **Polynomial Activation-Space Classifier**: We model the safety decision as a polynomial function over the activation vector extracted from an LLM layer. The degree‑1 component corresponds exactly to a standard linear probe as introduced by @alain2017linearprobe, while higher‑degree terms capture multiplicative neuron interactions inspired by findings in @jayakumar2020multiplicative. This formulation enables the classifier to represent complex nonlinear decision boundaries while maintaining an interpretable structure in terms of explicit monomials.

2. **Low-Rank Polynomial Parameterization**: Directly parameterizing high‑order polynomial tensors leads to a combinatorial explosion in parameters. To address this, we adopt low‑rank tensor decompositions similar to those used in scalable polynomial models such as @dubey2022polynomialinterpretability and polynomial neural networks studied in @chrysos2022polynomialnetworks. By representing higher‑order weight tensors through symmetric CP factorization, the model captures rich neuron interactions while keeping parameter counts and computation manageable.

3. **Progressive Degree-Wise Training**: To ensure that truncated versions of the polynomial perform well as standalone classifiers, we train the model incrementally across polynomial degrees. Inspired by progressive learning strategies such as the layer‑wise training paradigm explored in @belilovsky2019layerwise, each degree is optimized sequentially while freezing previously learned terms. This produces a sequence of nested classifiers where each additional degree refines the decision boundary without degrading earlier stages.

4. **Dynamic Cascaded Evaluation**: At inference time, the polynomial can be evaluated progressively. The classifier first computes the linear term and only evaluates higher‑order terms when the prediction remains uncertain. This mechanism effectively turns a single polynomial model into an internal cascade of classifiers, achieving the adaptive compute allocation that motivates cascaded monitoring systems like @cunningham2025cheapmonitors while avoiding the need for external models.

Together, these components transform a polynomial classifier into a dynamic safety monitor that balances efficiency and expressivity. The linear probe provides a lightweight baseline check, while higher‑degree terms progressively strengthen the monitoring decision when additional evidence is required.

## Status

PARTIAL -- motivation+method only, grounded in the paper's own OpenReview proposal text; N0/N1/N3-N12 not reconstructed here (see digest.md N3/N4 for this paper's role in the B4.4 lineage).
