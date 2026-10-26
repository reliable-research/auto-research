# Pricing the Verifier: Dollar-Denominated Exchange Rates between Thinking, Sampling, and Verifying

> Assembled from the six confirmed stage outputs in `pipeline.md`, post-audit (`taste_audit.md`: 🟢). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets, not results.

## Abstract

Deploying an LLM reasoning system under a fixed dollar budget means splitting that budget among three available levers: lengthening chain-of-thought reasoning, drawing more independent samples, and paying a verifier to select among them. We show this choice rests on an asymmetry no existing budget analysis prices: a dollar spent on verification buys no accuracy by itself, since a verifier only ever re-scores candidates that a generation dollar already produced — yet every prior allocation study of these levers denominates its budget in FLOPs, tokens, or trajectories, and none charges a verifier's own invocation cost against the same constraint its candidates were generated under. We meter chain-of-thought length, sample count, and verifier calls in one dollar unit, fit a single interaction-aware response surface across the resulting allocation grid instead of sweeping each lever separately, replicate the identical protocol across task families ordered by how cheaply they can be checked, and decompose any verifier-attributed accuracy gain against a budget-matched majority-vote control and a ground-truth selection ceiling. We report the resulting accuracy-per-dollar frontier, the estimated exchange rates between lever pairs, and whether the frontier's shape is a universal property of test-time compute or specific to how verifiable a task family is.

## Introduction

Deploying a large language model to reason under a metered budget is no longer a theoretical exercise. Every call to a hosted model has a dollar price attached, and a system built to answer hard questions under that price has three commonly available levers to spend it on: let the model think longer before answering, draw several independent attempts and combine them, or spend part of the budget on a second model that checks the attempts before one is chosen. Each lever is cheap to add to an existing pipeline, which is exactly why teams reach for some combination of all three without much scrutiny of whether that combination is a good use of the budget it consumes.

Yet a specific asymmetry among these three levers goes unpriced by every existing analysis of the trade-off. A dollar spent on longer reasoning or on an additional sample can, by itself, produce a correct answer that did not exist before. A dollar spent on verification cannot: a verifier only ever re-scores candidates that generation has already produced, so its entire contribution is derivative of dollars spent elsewhere in the same budget. This would be an academic distinction if verification were free, but it is not — every verifier call consumes its own input and output tokens, priced exactly like the calls it is scoring. Whether a marginal dollar is better spent generating one more candidate or checking the candidates already generated is therefore a live, metered trade-off, not a fixed pipeline choice, and no existing study prices it as one.

The nearest existing work approaches this gap from adjacent but distinct angles. Compute-optimal allocation studies, including the difficulty-conditioned strategy selection of Snell et al., and step-level token budgeting such as Plan-and-Budget, both establish that *how* a fixed amount of compute is allocated matters as much as how much is spent — but both denominate that amount in FLOPs or tokens, evaluate within a single task family, and never charge a verifier's own invocation cost against the budget it competes for. A separate line of theoretical work on sample-then-verify pipelines — bounding suboptimality under verifier-free trace distillation, casting verifier-guided sampling as optimal transport, deriving minimax-optimal regret for frequency-filtered best-of-N selection, and modeling generator-reranker systems as noisy communication channels — treats the verifier as an available resource with a formal performance bound, but none of these frameworks lets the verifier's own cost enter the budget constraint it is supposedly helping to spend. A third line of work characterizes a single lever in isolation: the inverted-U relationship between chain-of-thought length and accuracy, or the log-linear scaling of sampling coverage with sample count, each holding the other two levers fixed and offering no way to normalize a lever's value against the cost of the other two. A fourth, closer precedent maps an empirical compute-accuracy Pareto frontier across nineteen open-source reasoning models, conceding the frontier-mapping methodology this paper also uses — but its compute axis is a single FLOPs measure of reasoning length across models, never decomposed into thinking-length, sample-count, and verifier-call levers, and no dollar meter charges any model's verifier or selection cost against its generation cost. A fifth, contemporaneous line of work already prices LLM inference decisions in real dollars — dollar-metered speculative execution for agent workflows, and enterprise-scale inference-economics case studies of coding agents — so dollar denomination itself is no longer new; but these works price a speculation-scheduling decision or a deployment-configuration choice, not an allocation among thinking, sampling, and verification, and none charges a verifier's invocation cost against the generation budget it competes with. The closest prior work to this trade-off is a study of asymmetric verification for web-search agents, which already splits a budget between an exploration lever and a verification lever with both metered in a shared unit — but only within one domain, with cost measured in trajectories and tool calls rather than dollars, and with no chain-of-thought-length axis to complete the three-lever picture this paper needs.

Turning this asymmetry into a measurable question surfaces its own difficulties. The three levers are priced at different granularities — output tokens, doubled input-and-output cost per extra sample, and a verifier's own input-plus-output cost — so mapping them onto one fair dollar unit is a design problem in its own right, not a lookup. The marginal value of any one lever depends on where the other two are set: a verifier is worthless when there is only one candidate to screen and increasingly informative as the candidate pool grows, while longer reasoning changes both the accuracy and the length — hence the cost — of what the verifier has to read. Task families differ in how cheaply and reliably their answers can be checked at all, from executable tests to exact-match answers to rubric judgments, so any single measured exchange rate cannot be assumed to transfer to a family with a different verifiability profile. Models cannot be made to emit exactly a target number of tokens, so a "matched budget" can only be targeted, not fixed, forcing every comparison to be made across realized rather than nominal cost. And because coverage — whether some sample among many happens to be correct — and selection quality — whether a verifier picks the correct one — are both functions of the same generated pool, an accuracy gain attributed to the verifier can just as easily be a gain that any selection rule, even a free one, would have captured from having more candidates to begin with.

Our approach turns each of these obstacles into a specific design choice rather than a hedge. A per-call dollar meter charges every generation and verifier token against one frozen price sheet, with a parallel provider-neutral accounting kept so that qualitative conclusions can be checked for robustness to that price sheet rather than assumed to be independent of it. A single interaction-aware response surface is fit across the full allocation grid, rather than one lever at a time, so that whether the levers trade off additively or interact is itself a testable output of the fit, not an assumption baked into the experimental design. The identical measurement protocol is replicated, unchanged, across task families pre-ordered by verifiability, so that any cross-family difference in the efficient allocation can be attributed to verifiability rather than to inconsistent measurement. Grid configurations are retained only within a pre-specified matched-cost tolerance band around each target budget, with a regression adjustment on realized cost layered on top, so that "matched budget" describes the data actually collected rather than the settings requested. And every verifier-attributed accuracy gain is checked against a budget-matched majority-vote control that spends the identical dollars on more candidates instead of a verifier, together with a zero-cost ground-truth selection ceiling, so that a verifier's measured value is never assumed but always shown to survive its cheapest alternative explanation.

We evaluate this design across task families spanning executable code, exact-match mathematics, multiple-choice science questions, and rubric-graded open-domain question answering, comparing the resulting accuracy-per-dollar frontier against a fixed floor allocation, a budget-matched majority-vote arm, a zero-cost ground-truth selection ceiling, and an existing FLOPs-native allocation policy re-priced into the same dollar unit.

In summary, we contribute:
- An identification and formalization of the asymmetry underlying test-time budget allocation: verification is a second-order lever whose value is always derivative of dollars spent on generation, making its exchange rate with the other two levers a function of the allocation itself rather than a fixed constant.
- A dollar-denominated measurement instrument that meters chain-of-thought length, sample count, and verifier calls in one currency, including the verifier's own invocation cost, with an explicit price-sheet-robustness check built in rather than assumed.
- An interaction-aware allocation grid and a cross-family replication protocol that jointly test whether the accuracy-per-dollar frontier's shape is a universal property of test-time compute or a property specific to how verifiable a task family is.
- A coverage/selection decomposition — a budget-matched majority-vote control paired with a ground-truth selection ceiling — that isolates genuine verifier value from the accuracy any equally-priced selection-free alternative would have captured from the same candidate pool.

## Problem Definition

**Formal setup.** Consider a query $q$ drawn from a task family $F$. An allocation $a = (L, N, V)$ fixes a thinking-token cap $L$, a sample count $N$, and a verifier mode $V$. A frozen price sheet $P = (p_{in}, p_{out})$ converts every generation and verifier call's input and output tokens into dollars; the realized cost $c(q,a)$ sums this conversion over every call — generation and verification alike — that answering $q$ under allocation $a$ requires. A budget level $B_k$ defines a matched-cost bin $\mathfrak{B}_k = \{a : |\mathbb{E}[c(\cdot,a)] - B_k| \leq \varepsilon \cdot B_k\}$. Accuracy $\text{Acc}_F(a)$ is the family's grader's mean success rate over allocation $a$. The object of study is, per $(F, B_k)$: the non-dominated set over $(\mathbb{E}[c], \text{Acc}_F)$ — the accuracy-per-dollar frontier — the marginal rate of substitution between lever pairs along that set, and whether the set's allocation-mix composition is stable across $F$. A $(F, B_k)$ cell in which no evaluated allocation beats the fixed floor allocation by a pre-specified margin ($\geq 5$ accuracy percentage points, per the pre-registered B0 gate) at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported separately as **allocation-moot**, rather than silently dropped or scored as evidence that the levers are interchangeable.

**Why this is hard.** Fixing a price sheet does not by itself fix a fair accounting of the three levers: thinking tokens are priced as output only, an additional sample multiplies both input and output cost, and a verifier call consumes its own input (the candidate under review) and output (the judgment) tokens — so converting an allocation $a$ into a single realized cost $c(q,a)$ is a design decision, not a lookup, and every downstream claim inherits whatever convention that decision fixes. The marginal value of any one component of $a$ depends on the other two: the same increment of $V$ is worth more when $N$ is large than when $N=1$, and a longer $L$ changes both the accuracy and the length — hence the verifier's own reading cost — of what $V$ must screen, so no single exchange rate between two levers can be assumed constant across the grid without being tested. Task families differ in how cheaply and reliably $\text{Acc}_F$ can even be computed, from executable tests to rubric judgments, so a frontier measured on one family licenses no claim about a family with a different verifiability profile. Because $c(q,a)$ is realized through a stochastic generation process, no allocation can be pinned to an exact cost in advance, so membership in $\mathfrak{B}_k$ can only be targeted and must be adjusted for post hoc using realized, not nominal, cost. Finally, because $\text{Acc}_F(a)$ under $V>0$ reflects both how many candidates were generated and how well $V$ selected among them, an observed accuracy gain cannot be attributed to verification without a control that isolates selection quality from coverage.

## Method Overview

At a conceptual level, the study is a single measurement pipeline with five cooperating parts, each closing one of the difficulties above. Queries and allocations enter the pipeline; a shared dollar meter turns every call — generation and verification alike — into one comparable cost; an interaction-aware surface fit over the resulting grid turns cost and accuracy into a frontier, a set of marginal rates of substitution, and an explicit test of whether the levers trade off additively; a cross-family replication of the identical protocol turns a single frontier into a verdict about whether its shape is universal or family-specific; and a coverage/selection control turns any verifier-attributed accuracy gain into a claim that has survived its cheapest rival explanation.

The **unified dollar cost meter** takes every generation and verifier call's token usage and converts it to dollars under one frozen price sheet, with a parallel provider-neutral accounting kept alongside it so conclusions can be checked against price-sheet perturbation rather than assumed robust to it. The **interaction-aware response surface** takes the resulting (cost, accuracy) grid and fits accuracy as a joint function of the thinking cap, sample count, and verifier mode, with explicit interaction terms, so that whether one lever's value depends on the others' settings is measured rather than assumed away. The **verifiability-stratified replication** takes the identical protocol and reruns it, unchanged, across task families ordered a priori by how cheaply and reliably they can be checked, turning a single-family frontier into a cross-family stability verdict. The **matched-cost binning and adjustment** step takes the grid's inherently stochastic realized costs and turns them into pre-specified tolerance bins with a post hoc regression adjustment, so "matched budget" is a property of the data collected rather than the settings requested. The **coverage/selection decomposition** takes every verify-heavy point on the frontier and checks it against a budget-matched majority-vote control and a ground-truth selection ceiling, so a verifier's apparent value is only asserted once it has survived the alternative explanation that its dollars would have bought the same accuracy as extra samples.

## Methodology

### Unified Dollar Cost Meter

**Challenge.** The three levers are priced at different granularities and asymmetries — thinking tokens are output-only, an additional sample multiplies both input and output cost, and a verifier's own input-plus-output tokens are charged on top — so no single lookup converts an allocation into one fair dollar figure.

**Insight.** Cost commensuration cannot be resolved analytically — there is no single "true" exchange rate between an input and an output token, or between a generation call and a verifier call — but it can be turned into an explicit, checkable accounting convention with a stated sensitivity band, rather than an implicit assumption baked silently into whichever number happens to get reported.

**Method.** A per-call accounting layer logs input and output token counts for every generation and verifier call directly from the inference engine's usage fields, converting each to dollars under one price sheet frozen at experiment start, and attributing every dollar to whichever lever generated it. A parallel account expresses the same costs in provider-neutral normalized token units, so that any conclusion can be re-checked without the frozen price sheet's specific numbers.

### Interaction-Aware Response Surface

**Challenge.** The marginal value of any one lever plausibly depends on where the other two are set — a verifier is worth more against a larger candidate pool, and reasoning length changes what a verifier must read — so treating the three levers as independently priced would silently assume away exactly the structure this study needs to measure.

**Insight.** If the levers traded off additively, a single exchange rate measured once would apply everywhere on the grid; fitting the interaction terms directly is what turns that convenient assumption into a testable claim rather than a design default.

**Method.** A single response-surface model regresses accuracy on the thinking cap, sample count, and verifier mode jointly, with explicit interaction terms between sample count and verifier mode and between thinking cap and verifier mode, fit once across the full grid rather than one lever at a time. Each interaction term is tested against the additive (no-interaction) model via a likelihood-ratio test.

### Verifiability-Stratified Replication

**Challenge.** A frontier measured on a single task family licenses no claim about whether it transfers to a family with a different verifiability profile, and verifiability is naturally confounded with everything else that differs between task families — difficulty, answer format, grader noise.

**Insight.** Holding the measurement protocol byte-for-byte identical across families — same meter, same bins, same statistical tests — is what makes an observed cross-family difference attributable to verifiability rather than to an inconsistency in how each family happened to be measured.

**Method.** The identical matched-cost grid protocol is run across four task families pre-ordered a priori by verifiability class — executable code, exact-match mathematics, multiple-choice science questions, and rubric-graded open-domain question answering — and cross-family equality of the efficient set's allocation-mix composition is tested via a permutation test on Aitchison distance between family pairs at matched budget levels.

### Matched-Cost Binning and Realized-Cost Adjustment

**Challenge.** Because models cannot be forced to emit exactly a target number of tokens, no allocation's dollar cost can be fixed in advance, so a "matched budget" comparison risks silently comparing allocations at different realized costs.

**Insight.** The fix is not a better length-control mechanism but an explicit acceptance criterion plus a post hoc adjustment: "matched budget" becomes a measured property of the data actually collected, not an assumption about the settings requested.

**Method.** Each grid configuration's expected cost is estimated from pilot token statistics, and only configurations whose expected cost falls within a pre-specified tolerance band of each target budget level are retained. The fitted accuracy-cost surface is additionally regression-adjusted on each query's realized — not nominal — cost within its bin, so that residual within-bin cost variation is accounted for rather than ignored.

### Coverage/Selection Decomposition

**Challenge.** Coverage — whether some sample among many is correct — and selection quality — whether a verifier picks the correct one — are both functions of the same generated candidate pool, so an accuracy gain under a verify-heavy allocation cannot be attributed to the verifier without ruling out that the same dollars, spent on more candidates and no verifier, would have produced the same gain.

**Insight.** The only way to attribute an accuracy gain specifically to verification, rather than to the candidates its dollars could have paid for instead, is a control that spends the identical dollars on more samples and no verifier at all — and a ground-truth selection ceiling that caps what any selector, however good, could realize from the same pool.

**Method.** For every verify-heavy point on the fitted frontier, a budget-matched majority-vote control reallocates the verifier's dollars into additional samples at the same cost bin, and a zero-cost ground-truth oracle-selection arm is run at the same thinking cap and sample count. A verifier's measured accuracy value is asserted only where it exceeds its budget-matched majority-vote control; the oracle arm bounds how much of that value could ever be realized by any selector operating on the same pool.

## Experiments

### Experimental Setup

**Datasets.** MATH-500 (math, exact-match) — the pilot family, chosen because unambiguous grading lets the cost meter and the first interaction-surface fit be validated cheaply before scaling up. HumanEval+ together with a LiveCodeBench slice (code, executable) — the most verify-heavy family under the pre-registered verifiability ordering, needed so the stratified replication and the coverage/selection decomposition both have a family where the verifier lever has the most headroom to show anything at all. GPQA-Diamond (graduate-level science, option match) — an intermediate anchor on the verifiability ordering, so the ordering claim is not a two-point comparison between math and open QA alone. FRAMES together with a SimpleQA subset (open QA, rubric-graded) — the least verifiable family, needed both to test whether the ordering holds at its weakest-signal end and because the rubric judge is itself a verifier-like instrument, making the coverage/selection confound sharpest here.

**Sample sizes and power.** The pilot stage runs $n \geq 300$ questions per family (math, code), pre-registered to give power $\geq 0.8$ for a 5-percentage-point paired contrast at $\text{Acc} \approx 0.6$; the cross-family replication stage runs $n \geq 500$ questions per family across all four families. Any $(family, budget)$ cell, or any specific interaction or marginal-rate-of-substitution test, whose *realized* power falls below 0.8 for its own pre-registered effect floor is pre-declared **INCONCLUSIVE** for that cell or test only — never scored PASS/FAIL and never silently folded into an aggregate. One dataset-arithmetic constraint is stated here rather than discovered later: GPQA-Diamond contains 198 questions and HumanEval+ 164, so the multiple-choice family must draw from the larger GPQA pool (the 448-question main set or the 546-question extended set) and the code family's LiveCodeBench slice must contribute at least 336 problems for the $n \geq 500$ replication target to be reachable; where a family's realized pool still falls short of the target, the INCONCLUSIVE rule applies to its affected cells rather than the target being quietly lowered.

**Baselines** (sanity-check comparators and ceilings, not competitors to beat — this is a measurement study, and no research question here is framed as "our procedure beats baseline X"). A fixed floor allocation (minimal thinking cap, a single sample, no verifier) is the necessary "why bother allocating at all" gate: a $(family, budget)$ cell in which nothing beats this floor by a pre-specified margin ($\geq 5$ accuracy percentage points, per the pre-registered B0 gate) at matched or lower cost is excluded from exchange-rate and frontier-shape claims and reported as **allocation-moot** rather than folded silently into the frontier, per the Problem Definition's exclusion rule. A budget-matched majority-vote control reallocates a verify-heavy allocation's verifier dollars into additional samples at the same cost. A difficulty-conditioned compute-optimal allocator, re-priced in dollars from its native FLOPs-matched formulation, tests whether an allocation policy tuned without a cost meter happens to land near the dollar-optimal frontier once re-priced. A zero-cost ground-truth oracle selector provides the coverage ceiling for the coverage/selection decomposition — a sanity bound, not a target to beat.

**Metrics.** Realized dollar cost and family accuracy at each grid point; the non-dominated accuracy-per-dollar frontier per family and budget level with bootstrap confidence bands; interaction-term coefficients and their likelihood-ratio statistics; the allocation-mix (dollar-share) vector at each frontier point and the Aitchison-distance permutation statistic across families; and the oracle-minus-verifier accuracy gap at matched thinking cap and sample count.

**Research questions:**
1. RQ1 — Is the frontier-shape ordering robust to price-sheet perturbation?
2. RQ2 — Does the verifier's exchange rate interact with sample count?
3. RQ3 — Does verifier value interact more strongly with sample count than with thinking length?
4. RQ4 — Does frontier shape differ across task families?
5. RQ5 — Does the verify-heavy dollar share follow the pre-registered verifiability ordering?
6. RQ6 — Do matched-cost bins populate without needing the pre-declared tolerance-widening amendment?
7. RQ7 — Is the realized-cost adjustment load-bearing for frontier confidence bands?
8. RQ8 — Does verifier value survive a budget-matched coverage-only control?
9. RQ9 — Does the oracle–verifier accuracy gap shrink as sample count grows?

#### RQ1: Is the frontier-shape ordering robust to price-sheet perturbation?

**Setup.** Recompute the frontier-shape ordering (which family is most verify-heavy at its max-accuracy efficient point) under a $\pm 3\times$ perturbation of the input/output token price ratio and the generator/verifier price ratio, holding everything else fixed, for every tested (family × budget) cell.

**Expected outcome.** The ordering is preserved under perturbation for at least the majority of tested cells — the meter's qualitative conclusions are not an artifact of one specific price sheet, even though absolute dollar magnitudes are.

**Falsification condition.** Refuted if the ordering changes for more than half of tested cells under the $\pm 3\times$ perturbation — that would mean the frontier-shape finding is a price-sheet artifact rather than a structural property of the levers.

**Hypothesis (plain language).** The qualitative story (which lever dominates where) does not depend on the specific price sheet used to measure it, even though the exact dollar numbers do.

**Metrics.** Ordering agreement rate across the perturbation band, per cell and pooled.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Does the verifier's exchange rate interact with sample count?

**Setup.** Fit the interaction-aware response surface on the pilot grid (MATH-500) and test the sample-count × verifier-mode interaction term against the additive model via a likelihood-ratio test, Holm-corrected across families and fairness references where applicable.

**Expected outcome.** The interaction term is statistically significant on at least one task family, meaning a verifier's exchange rate measured at one sample count does not transfer unchanged to a different sample count.

**Falsification condition.** Refuted if the likelihood-ratio test finds no significant sample-count × verifier-mode interaction on any tested family — that would mean the additive (constant-exchange-rate) model already suffices and the more complex surface adds nothing.

**Hypothesis (plain language).** A verifier bought at one sample count is not worth the same amount when the sample count changes.

**Metrics.** Interaction-term coefficient and its likelihood-ratio statistic, per family.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Does verifier value interact more strongly with sample count than with thinking length?

**Setup.** Among cells where both the sample-count × verifier-mode and thinking-cap × verifier-mode interaction terms are significant, compare their fitted magnitudes.

**Expected outcome.** The sample-count interaction's magnitude exceeds the thinking-cap interaction's magnitude in a majority of such cells — verifier value depends more on how many candidates it screens than on how long each one is.

**Falsification condition.** Refuted if the thinking-cap interaction's magnitude is equal to or exceeds the sample-count interaction's magnitude in a majority of qualifying cells.

**Hypothesis (plain language).** What mainly changes a verifier's marginal value is the size of the candidate pool it screens, not the length of each candidate.

**Metrics.** Ratio of interaction-term magnitudes, per qualifying cell.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Does frontier shape differ across task families?

**Setup.** Run the identical matched-cost grid protocol across all four task families and compute the permutation test (10,000 permutations) on Aitchison distance between each family pair's efficient-set allocation-mix composition at matched budget levels, Holm-corrected across the six family pairs and tested budget levels.

**Expected outcome.** The permutation test rejects cross-family equality of allocation-mix composition for at least 2 of the 6 family pairs at Holm-corrected $\alpha = 0.05$.

**Falsification condition.** Refuted if no family pair shows a significant difference in allocation-mix composition at any tested budget level — that would mean a single allocation policy, once measured, transfers across verifiability regimes without adjustment.

**Hypothesis (plain language).** The efficient way to spend a test-time budget is not the same for every kind of task.

**Metrics.** Aitchison distance and permutation p-value, per family pair and budget level.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Does the verify-heavy dollar share follow the pre-registered verifiability ordering?

**Setup.** At each family's max-accuracy efficient point, compute the verifier's dollar share of total spend, and compare the four families against the pre-registered ordering (executable code $\geq$ exact-match math $\geq$ multiple-choice $\geq$ rubric-graded open QA).

**Expected outcome.** The ordering holds, with the code-versus-open-QA gap at least 0.10 in absolute dollar share, at a majority of tested budget levels.

**Falsification condition.** Refuted if the observed ordering contradicts the pre-registered verifiability ordering (for example, if open QA turns out to be the most verify-heavy family) or if the code-versus-open-QA gap falls below 0.10 at every tested budget level.

**Hypothesis (plain language).** Task families that are cheaper and more reliable to check spend more of their budget on verification at their best efficient point.

**Metrics.** Verifier dollar-share vector per family, per budget level.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Do matched-cost bins populate without needing the pre-declared tolerance-widening amendment?

**Setup.** Count the number of distinct grid configurations whose expected pilot cost falls within the pre-specified $\pm 10\%$ tolerance band of each target budget level, per family and budget level.

**Expected outcome.** At least 8 configurations populate every matched-cost bin under the $\pm 10\%$ tolerance, without triggering the pre-declared amendment to widen the tolerance to $\pm 15\%$.

**Falsification condition.** Refuted if any bin requires the pre-declared widening amendment to reach 8 configurations — that would mean the grid's cost granularity is coarser than assumed and every downstream frontier comparison in that bin rests on fewer configurations than intended.

**Hypothesis (plain language).** The grid, as designed, is fine-grained enough to compare several distinct allocations at every budget level without loosening the matching criterion.

**Metrics.** Configuration count per bin, per family and budget level.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Is the realized-cost adjustment load-bearing for frontier confidence bands?

**Setup.** Compute frontier confidence bands twice per family and budget level — once using the realized-cost regression adjustment, once using nominal-cost grouping alone — and compare band widths.

**Expected outcome.** Bands computed with the realized-cost adjustment are narrower than bands computed from nominal grouping alone, on a majority of tested bins.

**Falsification condition.** Refuted if the two approaches yield equally wide (or the adjustment yields wider) confidence bands on a majority of bins — that would mean the adjustment step adds complexity without improving precision, and nominal-cost grouping would suffice.

**Hypothesis (plain language).** Accounting for each query's actual realized cost, rather than just which nominal bin it fell into, meaningfully sharpens the frontier estimate.

**Metrics.** Confidence-band width under each method, per bin.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ8: Does verifier value survive a budget-matched coverage-only control?

**Setup.** For every verify-heavy point on the fitted frontier, compare its accuracy against a budget-matched majority-vote control that reallocates the identical dollars into additional samples at zero verifier cost, via paired bootstrap (10,000 resamples), Holm-corrected across families.

**Expected outcome.** The strong-verifier condition's accuracy gain over its budget-matched majority-vote control is statistically significant on at least one task family.

**Falsification condition.** Refuted if no task family shows a significant gain over the budget-matched majority-vote control — that would mean every measured "verifier value" finding is fully explained by the extra candidates the same dollars would have bought instead.

**Hypothesis (plain language).** At least somewhere, a verifier is worth more than simply buying more candidates with the same money.

**Metrics.** Paired accuracy difference and bootstrap confidence interval, per family.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ9: Does the oracle–verifier accuracy gap shrink as sample count grows?

**Setup.** At fixed thinking cap, compare the accuracy gap between the zero-cost ground-truth oracle selector and the strong verifier across increasing sample counts, on each task family.

**Expected outcome.** The gap shrinks — rather than staying flat or widening — as sample count increases, on at least one task family.

**Falsification condition.** Refuted if the gap stays flat or widens with sample count on every tested family — that would mean additional candidates do not help the verifier close in on the coverage ceiling, leaving a constant or growing amount of realizable accuracy permanently on the table.

**Hypothesis (plain language).** Giving the verifier more candidates to choose from lets it capture more of the accuracy that was already latent in the pool, not just a fixed fraction of it.

**Metrics.** Oracle-minus-verifier accuracy gap as a function of sample count, per family.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, a natural extension is to replicate the grid across additional model families and a second, independently-priced provider — the cross-model, cross-pricing generalization question this design does not close (a single frozen price sheet and a bounded set of models cannot establish that absolute exchange rates transfer to a different pricing regime or model capability tier). This is treated here as a stated limitation rather than an unaddressed sub-problem, per the scoping decision in the underlying discussion log.

## Related Work

The closest prior work to this paper is the study of asymmetric verification for web-search agents, and it is worth stating the delta plainly before surveying the wider landscape: that work already splits a budget between an exploration lever and a verification lever with both metered in one shared unit — but only within a single domain, with cost measured in trajectories and tool calls rather than dollars, and with no chain-of-thought-length axis at all, leaving the three-lever, dollar-denominated, cross-family question this paper targets entirely open.

**Compute-optimal and step-level allocation.** Snell et al. formalize inference-time methods as proposer-verifier combinations under a fixed compute budget and learn a difficulty-conditioned allocation policy across best-of-N, guided search, and sequential revision strategies; Plan-and-Budget decomposes a query into sub-questions and allocates a fixed token budget across them under a diminishing-returns model. Both establish that allocation, not just quantity, of test-time compute matters — but both denominate the budget in FLOPs or tokens, evaluate within a single task family, and never charge a verifier's own invocation cost against the same constraint it competes for.

**Sample-then-verify theory.** A cluster of theoretical results characterizes the sample-then-verify pipeline from different angles: one bounds the suboptimality gap between verifier-free trace distillation and a verifier-based alternative as a function of horizon and sample count; another casts verifier-guided sampling as optimal transport, decomposing achievable performance into a transport cost and terms determined by the verifier's ROC geometry; a third proves minimax-optimal regret for a frequency-filter-then-rerank selection rule as a function of coverage, reward-model error, and candidate count; a fourth models generator-reranker systems as noisy communication channels and derives asymptotic error-decay rates in the number of hypotheses. All four treat verifier feedback as an available resource with a formal performance bound, but none lets the verifier's own metered cost enter the budget constraint whose trade-off it is meant to characterize.

**Single-lever scaling characterizations.** Work on chain-of-thought length models each additional reasoning step as simultaneously reducing per-step difficulty and adding error-accumulation risk, deriving a non-monotonic, inverted-U relationship between chain length and accuracy; work on repeated sampling shows that coverage — the fraction of problems solved by at least one of many independent samples — scales approximately log-linearly with sample count, while noting that common selection strategies plateau well below that coverage ceiling without a verifier. Both characterize a single lever's scaling behavior in isolation, holding the other two levers fixed, with no mechanism for normalizing that lever's value against what the other two levers would have cost.

**Cross-model compute-accuracy frontiers.** A recent empirical study maps the Pareto frontier between task accuracy and inference compute across nineteen open-source reasoning models spanning dense, mixture-of-experts, and Mamba-hybrid architectures, finding a task-dependent saturation knee and an architectural advantage for mixture-of-experts models. We concede this paper's frontier-mapping methodology directly — both papers report a non-dominated accuracy-vs-compute set and look for where it saturates — but its compute axis is a single FLOPs measure of a model's own reasoning-token usage, compared *across* models rather than across allocations of thinking length, sample count, and verifier calls *within* one model, and no dollar meter separates a verifier or selection cost from the generation cost it is charged against. Its cross-model saturation-knee finding and this paper's cross-family verifiability-ordering finding are complementary readings of a compute-accuracy relationship, not competing measurements of the same object.

**Dollar-denominated inference economics.** A recent line of work prices LLM inference decisions in real dollars: cost-aware speculative execution for agent workflows prices each speculative downstream launch at separate input and output token rates and decides via an expected-dollar-value rule, and an enterprise case study of coding agents compares cloud API serving against on-premise quantized models on realized dollar cost, including prompt-caching effects. We concede that dollar denomination, as a budget unit, is therefore no longer new — these works establish exactly the deployment reality this paper's meter is built for. But their decision objects differ from ours in kind: one decides *whether to launch a speculative operation*, the other decides *which deployment configuration to buy*, and neither allocates a fixed budget among thinking length, sample count, and verifier calls, fits an exchange rate between any pair of those levers, or charges a verifier's own invocation cost against the generation budget whose products it re-scores. The three-lever, dollar-denominated allocation estimand remains unclaimed.

**Two-lever domain-specific allocation.** The closest prior work, on asymmetric verification for deep web-search agents, splits a test-time budget between exploration (a search agent generating parallel candidate answers) and verification (the same scaffold re-prompted to check a candidate), showing that shifting budget toward the cheaper verification lever improves the accuracy-cost trade-off. This is the only prior study that meters two of the three levers this paper studies in one shared cost unit and treats their trade-off as a genuine allocation decision rather than a fixed pipeline choice — but it does so in a single domain, with cost measured in trajectories and tool calls rather than a dollar unit shared with a chain-of-thought-length axis, and without the fourth-quadrant question of whether its finding transfers to task families with a different verifiability profile.

## Conclusion

This work reframes a routine deployment choice — how to split a metered budget among thinking, sampling, and verifying — as a precise measurement question rather than an engineering default, by identifying and pricing an asymmetry every prior allocation analysis left implicit: verification's value is always derivative of dollars spent on generation, and its own invocation cost has not previously been charged against the same allocation budget it competes for — even in the recent dollar-denominated inference-economics literature, which prices scheduling and deployment decisions rather than this three-lever allocation. The central methodological wager is that this derivative-value structure is only measurable once all three levers share one dollar unit, their interactions are fit rather than assumed away, and any verifier-attributed gain is checked against the cheapest rival explanation — that the same dollars, spent on more candidates instead, would have bought the same accuracy. Whichever way the frontier's shape and the levers' exchange rates turn out, the finding is decision-relevant: a universal, family-independent frontier would mean a single allocation policy, once measured, is reusable across deployments; a family-specific frontier would mean each new task family needs its own measurement before its budget can be allocated well. Two limitations bound this claim from the outset and are natural next steps rather than afterthoughts: the design's conclusions about frontier *shape* are intended to be robust to price-sheet perturbation, but its absolute dollar magnitudes are necessarily tied to the specific models and price sheet tested, leaving generalization across pricing regimes and model families as an explicitly acknowledged limitation rather than a claim this design can support; and the coverage/selection decomposition bounds, but cannot eliminate, the possibility that a stronger verifier than the ones tested here would close the oracle gap further than reported.

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → method → experiments → related work without forward references to undefined terms.
- **Terminology discipline** — "allocation," "matched-cost bin," "frontier," "marginal rate of substitution," "allocation-moot" each defined at first use in Problem Definition, used consistently thereafter; no internal stage IDs (`sp_*`, `m_*`, `rq_*`) leaked into prose — checked directly against `pipeline.md`.
- **Notation with worked example** — the formal setup section defines $(q, F, a, L, N, V, P, c(q,a), B_k, \mathfrak{B}_k, \text{Acc}_F)$ and the Problem Definition/Methodology sections consistently reuse this notation; no separate worked numeric example is included since no numbers exist yet (would require fabricating results).
- **RQ framing matches outcomes** — all 9 RQs are graded/quantitative (rates, coefficients, gaps, agreement proportions), each answered in its own subsection with an explicit falsifiable expected outcome and a distinct falsification condition, not a binary yes/no.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]` placeholders; only explicit `[placeholder — fill in after experiments are run]` markers in Results, per the drafting convention this is a pre-registered spec, not a report.
- **Artifact plan** — the dollar-metered harness (cost meter, grid sampler, interaction-surface fitting code, and the per-query cost logs it produces) is the natural release artifact; not yet built, so not claimed as available.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. Natural next steps: `research-paper-writing` for LaTeX conversion and prose polish once a target venue is chosen, or back into this pipeline if a stage needs revision (e.g., if piloting surfaces that matched-cost bins need the pre-declared tolerance-widening amendment far more often than expected, that is exactly the kind of cross-stage problem that becomes visible only once a draft exists, per `paper_assembly.md`).
