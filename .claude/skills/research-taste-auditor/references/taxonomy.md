# The two-axis research-taste taxonomy

Source: Chen, Zhao & Cohan, "Measuring the Gap Between Human and LLM Research
Ideas," arXiv:2607.01233. The taxonomy was built by the paper's authors from
NSF / NIH / AHRQ / DARPA proposal-writing guidance, then refined on a held-out
set of papers. Definitions below are paraphrased for this skill, not quoted.

Every idea gets **one label from each axis**. The two axes are disjoint —
never put a method-style concept ("integrates X and Y") on the opportunity
axis, or a gap-style concept ("nothing explains why...") on the method axis.

## Axis 1 — Opportunity Pattern (the motivation: why is this gap worth chasing?)

| Label | Core question it answers | Typical trigger words |
|---|---|---|
| **Puzzle / Contradiction** | Is there a paradox, tradeoff, surprising failure, or evidence that conflicts with itself? | "surprisingly," "despite," "paradox," "counter to expectation" |
| **Explanation Gap** | Is there a phenomenon that works/fails/varies and nobody has a causal or mechanistic account of *why*? | "it remains unclear why," "no account of," "unexplained" |
| **Scope Mismatch** | Does prior work only hold under narrow, unrealistic, or untested assumptions/regimes? | "assumes," "does not transfer to," "breaks down under," "idealized" |
| **Evidence Gap** | Is there no good way to measure, benchmark, audit, diagnose, validate, or compare the thing in question? | "no benchmark for," "hard to measure," "lacks diagnostics" |
| **Bridge Opportunity** | Are two literatures / methods / evidence streams sitting disconnected, and could linking them help? | "has not been connected to," "in isolation from," "meanwhile, separately" |
| **Failure / Risk Gap** | Is the existing approach brittle, unreliable, biased, unsafe, non-private, or hard to reproduce? | "fails when," "vulnerable to," "unreliable," "risk of" |
| **Resource Bottleneck** | Is progress blocked by cost, compute, data, time, deployment friction, or scalability? | "expensive," "does not scale," "requires prohibitive," "data-hungry" |

**Calibration numbers** (from Table 1 / Table 9 of the source paper, matched
literature-grounded ideation task, 11,683 paired human/LLM ideas): human
published papers use **Bridge Opportunity** as the primary opportunity label
only **12.1%** of the time. Across nine evaluated LLMs (Claude, Gemini, GPT,
Qwen, DeepSeek families), the rate is **47.1%–64.2%**. Human ideas also spread
much more evenly across all seven labels (normalized entropy ≥0.92); LLM
ideas concentrate more (entropy 0.55–0.76).

## Axis 2 — Method Paradigm (the method: what kind of contribution closes the gap?)

| Label | Core move | Typical trigger words |
|---|---|---|
| **Synthesis / Unification** | Integrates, reconciles, bridges, or unifies separate literatures/theories/methods/evidence streams. | "integrate," "unify," "combine," "reconcile," "bring together" |
| **Relax / Extend Scope** | Makes prior work hold under weaker assumptions, broader regimes, noisier or more realistic conditions. | "generalize," "relax the assumption," "extend to," "under weaker conditions" |
| **Robustification** | Reduces failure, brittleness, bias, uncertainty, or unreliability of an existing approach. | "more robust," "reduce failure rate," "mitigate bias," "harden against" |
| **Formal Derivation** | Introduces a theory, theorem, bound, proof, formal objective, taxonomy, or conceptual distinction. | "we prove," "we derive," "we formalize," "a bound on" |
| **Empirical Mapping** | Builds or applies systematic measurement: benchmarks, diagnostics, datasets, comparative or characterization studies. | "we measure," "we benchmark," "we characterize," "we quantify," "we localize" |
| **Artifact / System** | The central deliverable is a concrete tool, software system, platform, device, material, or workflow. | "we build a system," "our tool," "we release a platform" |
| **Optimization / Search** | Uses optimization, search, tuning, screening, allocation, or scaling strategies to find or improve a solution efficiently. | "we optimize," "search over," "allocate budget," "scale efficiently" |

**Calibration numbers**: human published papers use **Synthesis / Unification**
as the primary method label only **5.1%** of the time. Across the same nine
LLMs, the rate is **22.5%–38.7%**. Method-axis entropy for humans is ≥0.92,
vs. 0.72–0.88 for LLMs — narrower but less concentrated than the opportunity
axis.

## The headline finding, stated precisely

The gap is not "LLMs write bad ideas." Individually polished, plausible ideas
can still come from a narrow region of research taste. The overrepresented
region is specifically **Bridge Opportunity (axis 1) crossed with
Synthesis/Unification (axis 2)** — i.e., "these two things haven't been
connected, so let's connect them." The paper's mechanism analysis (Section
4.5) traces this to a recipe: pick a high-frequency technical concept, then
apply a safe connecting verb to it (see `archetype-verbs.md`).

**This does not mean Bridge/Synthesis ideas are invalid.** Real, published
papers do sometimes connect two literatures. The finding is about
*overrepresentation in the LLM output distribution*, not about any single
idea being wrong. Extended thinking mode made the concentration *worse*, not
better (bridge share rose from 49.7%→71.1% for one tested model), and giving
the model the full source papers instead of abstracts didn't fix it either —
so this bias survives more compute and more context. Treat a Bridge+Synthesis
label as a prompt to double-check specificity, not an automatic disqualifier.
