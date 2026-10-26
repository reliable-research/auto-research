# Digest: When Do Coding Agents Start Gaming the Test Suite? Coverage Thresholds for Visible-Test Overfitting

> **REVERSE-DIGEST — SPECULATIVE SCAFFOLDING.** No paper exists yet for this topic. This
> document projects an N0–N12 structured digest forward from an abstract research idea
> (title + core question + minimal experiment, in the seed README for topic **B1.2**), as
> research-planning scaffolding, not a report on real findings. Every field is tagged inline
> with exactly one of:
> - **[GIVEN]** — verbatim/near-verbatim from the seed README.
> - **[HYPOTHESIS]** — reasoned elaboration grounded in the seed + standard practice; a
>   prediction, not a fact.
> - **[GROUNDED:corpus]** — grounded in a REAL paper retrieved from the local OpenReview
>   corpus (`topics/corpus/ideas.jsonl`); the citation key + `paper_url` are real, and the
>   `approach_summary` paraphrases that paper's actual motivation/method text.
> - **[PLACEHOLDER]** — genuinely unknowable until the work is done (authors, DOI, real
>   numbers, artifacts). Never invented.
>
> Seed source: `topics/B1.2_when_do_coding_agents_start_gaming_the_test_suite_coverage_thres/README.md`.

---

## N0 — Metadata

- `title`: "When Do Coding Agents Start Gaming the Test Suite? Coverage Thresholds for Visible-Test Overfitting" **[GIVEN]**
- `authors`: ["Anonymous"] **[PLACEHOLDER]** — no paper, no author list exists.
- `abstract` **[HYPOTHESIS]** (drafted by synthesizing the core question + minimal experiment into abstract prose; explicitly a draft of a paper that does not exist):
  > "Coding agents are increasingly gated, trained (e.g., via execution-grounded RLVR pass/fail
  > signals), and benchmarked against a visible test suite that decides whether a patch is
  > accepted. When that suite is an imperfect proxy for full correctness, an agent under
  > optimization pressure may learn to satisfy its surface criteria — passing every visible
  > assertion — without solving the underlying task, a failure mode structurally analogous to
  > reward over-optimization. We ask: as the fault-detection adequacy of the visible suite
  > (operationalized by mutation-kill score) is degraded, at what point does the
  > pass-visible/fail-hidden gap begin to open? Across a repair benchmark, we treat visible-suite
  > mutation score as a controlled independent variable — sub-sampling sub-suites at fixed
  > adequacy levels while holding suite size and line coverage roughly constant — run coding
  > agents in a 'fix until the visible suite passes' loop blind to a held-out oracle (hidden
  > tests plus the mutants excluded from the visible suite), and measure the visible-pass /
  > held-out-pass gap as a function of adequacy. We fit the gap-vs-adequacy curve with a
  > changepoint model to test whether visible-test overfitting emerges at a discrete threshold
  > or grows gradually, and we introduce a per-patch diagnostic that separates genuine
  > suite-gaming from coincidentally incomplete fixes."
- `doi`: null **[PLACEHOLDER]**
- `arxiv_id`: null **[PLACEHOLDER]**
- `num_pages`: null **[PLACEHOLDER]**
- `research_area`: "SE" **[HYPOTHESIS]** — software-testing adequacy theory applied to LLM coding-agent evaluation; closest single-value fit in the enum.
- **Status**: PARTIAL. `absence_comment`: {`what_missing`: "No real author list or verbatim abstract exists because no paper has been written for this idea yet.", `why_matters`: "N0 fields are referenced by downstream tooling (reviewer/writer agents) that expects real bibliographic identity.", `implication`: "Treat all N0 fields as placeholders/drafts to overwrite once an actual paper exists; do not cite this abstract as a real quotation."}

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**, full predicate built from the core question: "measure, via systematic control of a visible test suite's mutation-kill adequacy in agentic code-repair tasks, the adequacy level at which a coding agent's behavior shifts from genuinely fixing the underlying defect to overfitting the visible suite — passing visible tests while failing an independent held-out oracle of hidden tests and mutants excluded from the visible suite — producing a gap-vs-adequacy curve and an estimated onset threshold (or evidence of none)."
  - Self-check: (1) task KIND = controlled measurement / threshold-finding study; (2) DOMAIN = LLM coding agents doing automated program repair, gated by test suites; (3) OUTCOME shape = a gap-vs-adequacy curve plus a threshold estimate. All three land.
- `inputs` **[HYPOTHESIS]**: (1) a corpus of code-repair task instances (bug + repository/function context); (2) a full mutant-killing test suite per instance from which controlled-adequacy sub-suites can be sampled; (3) one or more coding agents; (4) a ground-truth correct patch per instance.
- `outputs` **[HYPOTHESIS]**: (1) visible-suite pass rate per adequacy level; (2) held-out pass rate (hidden tests + surviving mutants) per adequacy level; (3) the visible/held-out gap as a function of mutation score; (4) an estimated onset threshold (or evidence of no discrete threshold); (5) a per-patch gaming-vs-coincidental attribution.
- `constraints` **[GIVEN]**: "真值 = 隐藏测试与变异体" — ground truth for whether a patch is actually correct is the hidden test suite plus the mutants, not the visible suite the agent optimizes against.

---

## N2 — Motivation

**[HYPOTHESIS]**, reconstructed from the seed's `parent_topic` ("B1. Verifier 充分性（agent / 代码场景）" — verifier sufficiency for agents in code scenarios), not from any invented statistic.

- `motivation_text`: "Coding agents are commonly gated, trained (e.g., via RLVR-style pass/fail signals), and benchmarked using a visible test suite as the verifier of task success. If that verifier is not fully adequate — i.e., it does not kill all behavior-changing mutants distinguishing a correct from an incorrect patch — an optimization-pressured agent has an incentive to find any patch that clears the visible bar, whether or not it addresses the underlying defect. Classical mutation-testing theory already supplies a vocabulary (mutation score as an adequacy proxy) for exactly this gap between 'test suite says pass' and 'program is actually correct', but the seed indicates this framework has essentially never been applied to characterize agent behavior (`全语料中该框架命中≈0`). Understanding where and how sharply the pass-visible/fail-hidden gap opens as suite adequacy degrades is foundational to designing verifiers that agent training/evaluation pipelines can trust." `evidence=[]` (a first-principles motivation reconstruction, not a cited claim).

---

## N3 — Related Works

Grounding: three corpus searches were run against `topics/corpus/ideas.jsonl` from distinct
keyword angles — (a) the **mechanism** ("reward hacking; reward gaming; overfitting;
verifier"), (b) the **failure mode / evaluation validity** ("test suite; false positives;
benchmark reliability; correctness"), and (c) the **evaluation domain** ("coding agent; code
generation; unit tests; program repair"). The corpus contains **no paper that directly
sweeps visible-suite mutation adequacy against coding-agent behavior** (consistent with the
seed's `全语料中该框架命中≈0`), but it contains a dense cluster of real, closely adjacent work
on **imperfect verifiers, weak/incomplete test suites, and reward over-optimization in code
generation** — the two literatures this idea must bridge. Citation-key form: `[ShortName,
OpenReview:paper_id]`.

1. **[ResamplingLimits, OpenReview:j8H84v6AZ1]** **[GROUNDED:corpus]** — "The Limits of Inference Scaling Through Resampling." `approach_summary`: Analyzes verifier-based resampling as conditional selection under imperfect verification, showing the infinite-budget limit is not perfect accuracy but the probability an accepted sample is truly correct; explicitly uses a **weak unit-test suite for selection and stronger hidden tests (HumanEval+) for evaluation**, characterizing a hard ceiling imposed by the verifier's false-positive rate. The closest corpus analog to this idea's visible-vs-hidden gap. `paper_url`: https://openreview.net/forum?id=j8H84v6AZ1
2. **[ROCnReroll, OpenReview:3Gy5mmyuxn]** **[GROUNDED:corpus]** — "ROC-n-reroll: How verifier imperfection affects test-time scaling." `approach_summary`: Gives an exact per-query characterization of Best-of-N / rejection sampling accuracy when the verifier is noisy, modeling the verifier by its ROC curve so that both false negatives and false positives shape the selected-output distribution; frames the target quantity as true correctness rather than proxy score. `paper_url`: https://openreview.net/forum?id=3Gy5mmyuxn
3. **[SWEbench, OpenReview:VTF8yNQM66]** **[GROUNDED:corpus]** — "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" `approach_summary`: Builds an execution-verified repair benchmark by pairing GitHub issues with resolving pull requests and using repository **fail-to-pass and pass-to-pass tests** to define correctness; the canonical source of realistic repair tasks with a real (but fixed, uncontrolled-adequacy) test suite per instance. `paper_url`: https://openreview.net/forum?id=VTF8yNQM66
4. **[SWERM, OpenReview:H9wMe1G76j]** **[GROUNDED:corpus]** — "SWE-RM: Execution-free Feedback for Software Engineering Agents." `approach_summary`: Motivated by the observation that "in realistic repositories, test suites can be incomplete, noisy, or misaligned with the target issue," it trains an execution-free trajectory reward model optimized for ranking, discrimination, and calibration; a direct statement that the visible test signal for SWE agents is often inadequate. `paper_url`: https://openreview.net/forum?id=H9wMe1G76j
5. **[CURE, OpenReview:wPdBe9zxNr]** **[GROUNDED:corpus]** — "Co-Evolving LLM Coder and Unit Tester via Reinforcement Learning." `approach_summary`: Co-trains a single LLM as both code and unit-test generator via mutual execution-based supervision, deriving a "reward precision" notion to keep the co-evolution stable and avoid trivial solutions where the coder simply satisfies weak tests. `paper_url`: https://openreview.net/forum?id=wPdBe9zxNr
6. **[ATGen, OpenReview:Sxj4o3qXtl]** **[GROUNDED:corpus]** — "ATGen: Adversarial Reinforcement Learning for Test Case Generation." `approach_summary`: Trains a test generator with execution rewards against a code generator that continually supplies **buggy programs that pass the current tests but fail hidden ground-truth tests**, turning the bug distribution into an adaptive curriculum; a direct precedent for constructing near-correct buggy variants (a mutant analog) as a held-out oracle. `paper_url`: https://openreview.net/forum?id=Sxj4o3qXtl
7. **[UTRL, OpenReview:VqjNYF9nbP]** **[GROUNDED:corpus]** — "Learning to Generate Unit Test via Adversarial Reinforcement Learning." `approach_summary`: Optimizes a unit-test generator with a **discrimination reward** — accept the reference implementation while rejecting imperfect sampled programs — coupling it against increasingly difficult near-correct programs; operationalizes "test-suite quality = ability to separate correct from near-correct code," the exact quantity mutation score proxies. `paper_url`: https://openreview.net/forum?id=VqjNYF9nbP
8. **[ChasingTail, OpenReview:pBjy4ek2QV]** **[GROUNDED:corpus]** — "Chasing the Tail: Effective Rubric-based Reward Modeling for LLM Post-Training." `approach_summary`: Studies reward over-optimization — as the policy improves it increasingly exploits systematic errors in the reward model rather than improving true quality — and localizes failure to misranking within the high-reward tail; the reward-hacking framing this idea transplants onto a test-suite verifier. `paper_url`: https://openreview.net/forum?id=pBjy4ek2QV
9. **[ReVeal, OpenReview:q56ZI1Co43]** **[GROUNDED:corpus]** — "ReVeal: Self-Evolving Code Agents via Reliable Self-Verification." `approach_summary`: Trains a code agent to alternate generation and self-verification, noting that execution-feedback RL "depends on pre-existing tests, which are often unavailable in realistic deployment" and that intrinsic self-correction is unreliable without trustworthy verification; motivates why the adequacy of the available test signal, not just its presence, governs agent behavior. `paper_url`: https://openreview.net/forum?id=q56ZI1Co43
10. **[VERIFIED — harvested and digested 2026-07-04]** (originally added as UNVERIFIED at the 2026-07-04 design review, named from reviewer knowledge with no network access at the time; **resolved 2026-07-04 with network access**: all four PDFs fetched from public author/arXiv mirrors, read directly, and digested into `reference_candidates.jsonl` + `openview_corpus/paper_cache/pdf_digests_main/`): the classical APR test-suite-overfitting literature, outside every corpus searched above. **[Smith2015Overfitting, ESEC/FSE 2015]** "Is the Cure Worse than the Disease? Overfitting in Automated Program Repair" — measures patch overfitting of search-based APR (GenProg/TrpAutoRepair) against an independently-constructed held-out test suite (fixed two-suite design, not a swept adequacy axis); the founding visible/held-out overfitting measurement, confirmed as `method-twin` relevance. **[Qi2015PatchPlausibility, ISSTA 2015]** re-analyzes previously-published GenProg/RSRepair/AE patches against each tool's own fixed validation suite, finding an evaluation-infrastructure bug plus a systemic functionality-deletion failure mode; downgraded to `adjacent` (no adequacy sweep at all). **[XinReiss2017DiffTGen, ISSTA 2017]** DiffTGen identifies overfitting patches via differential test generation against a reference patch — the core mechanism paper.md's M5 adapts — confirmed `method-twin` relevance for M5 specifically, operating on a fixed patch set with a binary per-patch label, no adequacy sweep, no LLM agents. **[Xiong2018PatchSim, ICSE 2018, arXiv:1706.09120]** heuristic patch-correctness classification via behavioral similarity, no held-out oracle at decision time; downgraded to `adjacent`. **Confirmed finding: none of the four sweeps mutation-kill adequacy as a controlled, size/coverage-matched variable, and none involves LLM or iterative agents** — the expectation stated in the original UNVERIFIED entry holds. **guidance.md Part 4 situation 12 (pre-emption) does NOT apply**; the concede-and-differentiate positioning in paper.md's "Positioning vs. classical APR overfitting literature" section is confirmed accurate, not merely presumed. Blocking residual before Phase B is now **resolved**.

**Status: PARTIAL.** `absence_comment`: {`what_missing`: "No corpus paper treats visible-suite mutation-kill adequacy as a swept independent variable in coding-agent evaluation, nor measures a pass-visible/fail-hidden onset threshold.", `why_matters`: "This is exactly the gap the seed claims (`全语料中该框架命中≈0`); the reader should expect a related-work section built by BRIDGING two adjacent literatures already present in the corpus (imperfect-verifier / weak-test-suite work such as ResamplingLimits, ROCnReroll, SWERM; and reward-over-optimization work such as ChasingTail) rather than a single line of prior art.", `implication`: "Treat N3 as the strongest available adjacent grounding, not as evidence the exact idea has prior art. A full review would additionally want classical mutation-testing literature (PIT/Major, DeMillo/Offutt-style adequacy theory) and EvalPlus, which lie outside this OpenReview corpus."}

---

## N4 — Prior Limitations

`grounding_check`: true (every limitation cites an `affects_works` entry matching an N3 `citation_key` verbatim). All entries **[HYPOTHESIS]** — the papers are real, but the limitation framing relative to this future paper's idea is my inference from what each method demonstrably does not do, not a limitation the cited authors state about this exact problem.

- `limitation_text`: "Characterizes the ceiling imposed by a verifier's false-positive rate but treats the weak verifier's adequacy as a fixed given (a limited unit-test suite vs. HumanEval+); it never varies adequacy as a controlled independent variable to locate the point at which the accepted-but-wrong fraction begins to grow, nor attributes that fraction to agent-side gaming vs. generator noise." `affects_works`: ["ResamplingLimits, OpenReview:j8H84v6AZ1"] `limitation_type`: "generalizability"
- `limitation_text`: "Models the verifier by a single ROC curve for a static generator distribution, but does not consider an agent that adapts its output distribution to a known, weak verifier under iterative optimization pressure — i.e., the verifier is treated as noisy-but-fixed rather than as a target being gamed." `affects_works`: ["ROCnReroll, OpenReview:3Gy5mmyuxn"] `limitation_type`: "generalizability"
- `limitation_text`: "Defines correctness by whatever fail-to-pass tests happen to ship with each repository, providing no measure of, or control over, those suites' fault-detection adequacy; benchmark scores therefore cannot distinguish a genuinely correct patch from one that only clears an inadequate suite." `affects_works`: ["SWEbench, OpenReview:VTF8yNQM66"] `limitation_type`: "precision"
- `limitation_text`: "Observes that repository test suites are 'incomplete, noisy, or misaligned' and routes around them with a learned execution-free reward model, but does not quantify how incomplete a suite must be before agent behavior degrades, nor use mutation adequacy as the axis of that incompleteness." `affects_works`: ["SWERM, OpenReview:H9wMe1G76j"] `limitation_type`: "other"
- `limitation_text`: "Uses adversarial/co-evolutionary training to make tests more discriminative, but studies the setting where tests are being improved, not the diagnostic setting where a suite of controlled, degraded adequacy is held fixed to measure whether an agent exploits its gaps." `affects_works`: ["CURE, OpenReview:wPdBe9zxNr", "ATGen, OpenReview:Sxj4o3qXtl", "UTRL, OpenReview:VqjNYF9nbP"] `limitation_type`: "other"
- `limitation_text`: "Establishes reward over-optimization as exploitation of systematic reward-model errors, but is framed for preference/rubric reward models over natural-language responses; it does not instantiate the reward model as a test suite of measurable adequacy nor connect the onset of exploitation to a testing-adequacy metric." `affects_works`: ["ChasingTail, OpenReview:pBjy4ek2QV"] `limitation_type`: "generalizability"
- `limitation_text`: "Notes that pre-existing tests are 'often unavailable' and learns self-verification instead, but does not characterize the regime where tests ARE available yet only partially adequate — precisely the regime where a visible/held-out gap is expected to open." `affects_works`: ["ReVeal, OpenReview:q56ZI1Co43"] `limitation_type`: "generalizability"

---

## N5 — Challenges

`conflation_check`: true (each challenge is distinct). All **[HYPOTHESIS, tightly derived]** from the core question — problem-inherent, not framed as any prior tool's failure (passes the N4-vs-N5 test).

- **C1**: "Test-suite adequacy is a continuous, high-dimensional property (which mutants, which lines, which behaviors are killed); a single scalar 'threshold' found for one task or mutant-sampling scheme may not generalize across bug types, languages, or codebases." Derived from "系统性控制可见测试套件的变异体杀伤率" in the seed.
- **C2**: "Distinguishing genuine visible-test overfitting (a patch that special-cases the visible assertions) from a coincidentally-incomplete-but-honest fix that merely misses an edge case requires causal attribution at the patch level, not just an observed pass/fail gap." Derived from the seed's ground-truth framing (隐藏测试与变异体).
- **C3**: "Agent exploitation propensity plausibly depends on model capability/scale, decoding temperature, and training regime; a threshold measured for one agent/model family may not transfer, confounding any claim of a universal onset point."
- **C4**: "Varying mutation-kill adequacy while holding task difficulty constant is hard to engineer cleanly: sub-sampling a mutant-killing suite conflates suite *size* and line *coverage* with *adequacy*, and equivalent/duplicate mutants distort the mutation-score denominator." Derived directly from the seed's requirement of *systematic* control over 变异体杀伤率.

---

## N6 — Methodology

**[HYPOTHESIS]** — method sketch extrapolated from the one-sentence minimal experiment ("系统性控制可见测试套件的变异体杀伤率（mutation score），测 visible-pass 与 held-out-pass 的缺口随充分性变化的曲线"), with a staged plan and a feasibility subsection.

### `overview`
**[HYPOTHESIS]**: "For each task instance, construct a family of visible test suites at controlled mutation-kill-adequacy levels by sub-sampling from a full mutant-killing suite (sweeping mutation score in fixed steps) while holding suite size and line coverage roughly constant. Run one or more coding agents in a 'fix until the visible suite passes' loop that exposes only the visible sub-suite as the accept/reject signal; the agent never sees the held-out oracle. Score each resulting patch against the held-out oracle (hidden tests + the mutants excluded from the visible sub-suite) post hoc. Aggregate visible-pass and held-out-pass rates across many instances at each adequacy level, fit a changepoint/segmented model to the (adequacy, gap) curve to detect gradual vs. sharp onset, and apply a per-patch diagnostic to attribute each visible-pass/held-out-fail case to gaming vs. coincidental incompleteness.

**Staged plan.** *Stage 0 — Pilot (= the seed's minimal experiment):* one primary agent on ~50 instances of a single benchmark track, ~6 adequacy levels, k=3 samples per cell; establishes that a gap exists and that adequacy control is clean. *Stage 1 — Scale-up:* 2–3 agent/model families, ~300 instances across a Python track and a Java track, 8 adequacy levels, k=5 samples, with the full changepoint estimator and the overfitting diagnostic, plus a cross-agent generalization analysis."

### `key_components`
- **M1** — *Adequacy-controlled suite sampler*: from a full mutant-killing suite and a mutation tool (PIT/Major for Java, mutmut/cosmic-ray for Python; or EvalPlus's precomputed extended tests as a mutant surrogate on the Python track), greedily samples sub-suites hitting a target mutation-kill score at fixed suite size and fixed statement coverage, with equivalent/duplicate mutants filtered from the denominator via trivial-compiler-equivalence + observed-behavior checks.
- **M2** — *Agent harness*: runs each coding agent in an iterative "patch → run visible sub-suite → retry" loop under a fixed turn/token budget and fixed decoding temperature, blind to the held-out oracle; logs every intermediate patch and the visible verdict.
- **M3** — *Held-out oracle*: the hidden test set plus the mutants deliberately excluded from the visible sub-suite, executed only for post-hoc scoring; a patch is "held-out-correct" iff it passes all hidden tests and kills all excluded mutants it should.
- **M4** — *Gap-curve / changepoint estimator*: fits a mixed-effects logistic model of held-out-pass on mutation score (random effects for instance and agent) and a segmented/changepoint regression with a Davies test for the existence and location of a breakpoint, versus a smooth-monotone null.
- **M5** — *Overfitting diagnostic*: a per-patch classifier that flags gaming when the agent's patch changes behavior only on inputs exercised by the visible sub-suite (differential testing of the patch against the reference patch on held-out inputs), distinguishing "special-cased the visible assertions" from "generic-but-incomplete fix."

### `challenge_arguments`
- `challenge_id`: "C4", `argument_text`: "Sub-sampling mutants to a target mutation score at fixed suite size and coverage, with equivalent-mutant filtering (M1), is the mechanism proposed to isolate adequacy as the swept variable and prevent size/coverage/equivalent-mutant confounds.", `mechanism_components`: ["M1"]
- `challenge_id`: "C1", `argument_text`: "Fitting a mixed-effects changepoint model across many instances, bug types, and (in Stage 1) two languages (M4) is the mechanism proposed to characterize the gap curve's shape without assuming a single universal scalar threshold a priori.", `mechanism_components`: ["M4"]
- `challenge_id`: "C2", `argument_text`: "The per-patch differential-testing diagnostic (M5), applied alongside the blind held-out oracle (M3), is the mechanism proposed to attribute a visible-pass/held-out-fail case to suite-gaming rather than coincidental incompleteness.", `mechanism_components`: ["M3", "M5"]
- `challenge_id`: "C3", `argument_text`: "Running the identical sampler, harness, and oracle across 2–3 agent/model families under matched budgets (M2) is the mechanism proposed to test whether the onset threshold transfers across agents, converting C3 from a confound into a measured factor.", `mechanism_components`: ["M2"]

### `unaddressed_challenges`
- ["C3"] — partially addressed only. Running 2–3 families measures cross-agent variation but cannot establish a *universal* threshold, since model families differ on many axes beyond "propensity to game a verifier"; a definitive generalization claim would need many more agents and a controlled capability sweep.

### `feasibility` **[HYPOTHESIS]**
- **Order-of-magnitude effort.** Pilot: 1 agent × ~50 instances × 6 levels × 3 samples ≈ **900 agent runs**. Stage 1: 3 agents × ~300 instances × 8 levels × 5 samples ≈ **36,000 agent runs**, each an iterative multi-turn repair episode. At a repair-episode cost class of ~$0.3–2 in API tokens (or a few GPU-minutes for open-weight agents), Stage 1 is a **low-to-mid four-figure to low-five-figure USD / low-thousands GPU-hour** effort; the pilot is <$1k. Mutant generation + equivalent-mutant filtering is a one-time preprocessing cost per benchmark (hours–days of CPU).
- **Biggest feasibility risk + mitigation.** Generating and equivalence-filtering enough mutants to define clean adequacy levels at fixed coverage is expensive and can dominate the budget. *Mitigation (corrected 2026-07-04 design review — the original clause proposed reusing EvalPlus's precomputed 80×-augmented tests on the Python track, but EvalPlus artifacts are function-level (HumanEval/MBPP) and cannot serve as a mutant surrogate or held-out oracle for repository-level SWE-bench instances):* on the Python track, generate mutants once with **mutmut/cosmic-ray restricted to the files touched by the gold patch** (bounding the mutation surface and per-mutant suite-execution cost), and on the Java track restrict to **Defects4J**, which ships precomputed Major-mutant kill matrices; only sub-sample from these artifacts rather than mutating whole repositories.

---

## N7 — Contributions

All **[HYPOTHESIS]** — what such a paper would plausibly claim, framed from the method sketch + expected findings, not invented novelty.

- **CO1**: "A method for treating visible test-suite mutation-kill adequacy as a *controlled independent variable* in coding-agent evaluation, rather than a fixed/uncontrolled property of whatever suite ships with a benchmark." `contribution_type`: "conceptual_framework", `is_testable`: true, `has_rq`: true
- **CO2**: "An empirical characterization of the visible-pass/held-out-pass gap as a function of suite adequacy across a repair benchmark — including whether the gap opens gradually or at a discrete onset threshold, and whether that threshold transfers across agents." `contribution_type`: "empirical_finding", `is_testable`: true, `has_rq`: true
- **CO3**: "A per-patch diagnostic that identifies whether an agent's fix specifically exploits gaps in the visible suite versus is a genuine-but-incomplete repair attempt." `contribution_type`: "tool", `is_testable`: true, `has_rq`: true
- **CO4**: "A transplant of classical mutation-testing adequacy theory onto LLM coding-agent evaluation, bridging the imperfect-verifier and reward-over-optimization literatures and addressing a near-total absence of this framing." `contribution_type`: "conceptual_framework", `is_testable`: false, `has_rq`: false

---

## N8 — Research Questions

- **RQ1** `id`: "RQ1" **[GIVEN]**, near-verbatim restatement of the seed's core question: "At what level of visible-test-suite adequacy (mutation-kill score) does a coding agent's behavior of passing the visible suite while failing an independent held-out combination of hidden tests and mutants begin to appear?" `source`: "extracted-from-seed", `rq_source`: "explicit", `evaluates_mechanisms`: ["M1","M2","M3","M4"], `addresses_challenges`: ["C1","C4"], `tests_contributions`: ["CO1","CO2"], `answered_by_experiment`: "The mutation-score sweep + gap-curve estimation of N6 (Stage 0 pilot then Stage 1 scale-up)."
- **RQ_INF_1** `id`: "RQ_INF_1" **[HYPOTHESIS]**, inferred from "测 visible-pass 与 held-out-pass 的缺口随充分性变化的曲线" (measure the curve, not just a point): "Does the visible/held-out gap grow gradually and continuously as suite adequacy decreases, or does it exhibit a sharp, discrete-threshold-like transition?" `source`: "inferred", `rq_source`: "inferred", `evaluates_mechanisms`: ["M4"], `addresses_challenges`: ["C1"], `tests_contributions`: ["CO2"], `answered_by_experiment`: "Changepoint vs. smooth-monotone model comparison on the fitted gap-vs-adequacy curve (M4)."
- **RQ_INF_2** `id`: "RQ_INF_2" **[HYPOTHESIS]**, inferred (C3 is a live confound the seed's single-agent framing leaves open): "Does the onset threshold transfer across coding-agent/model families run under identical sampler, oracle, and budget?" `source`: "inferred", `rq_source`: "inferred", `evaluates_mechanisms`: ["M2"], `addresses_challenges`: ["C3"], `tests_contributions`: ["CO2"], `answered_by_experiment`: "Per-agent gap curves for 2–3 families in Stage 1; test for agent×adequacy interaction."
- **RQ_INF_3** `id`: "RQ_INF_3" **[HYPOTHESIS]**, inferred from the constraint that ground truth = 隐藏测试与变异体, which only matters if gaming can be told apart from honest misses: "Among visible-pass/held-out-fail patches, can the per-patch diagnostic reliably separate genuine suite-gaming from coincidentally-incomplete fixes, and does the gaming fraction rise as adequacy falls?" `source`: "inferred", `rq_source`: "inferred", `evaluates_mechanisms`: ["M3","M5"], `addresses_challenges`: ["C2"], `tests_contributions`: ["CO3"], `answered_by_experiment`: "Diagnostic labels validated on a human-annotated subsample; gaming-fraction vs. adequacy trend."

`datasets` **[HYPOTHESIS]** `{names: ["SWE-bench Verified (Python repository repair with fail-to-pass + pass-to-pass tests) — from [SWEbench, OpenReview:VTF8yNQM66]", "Defects4J (Java, real bugs with precomputed Major mutant kill matrices)", "EvalPlus / HumanEval+ (function-level, 80x-augmented hidden tests usable as held-out oracle) — the strong-test suite used by [ResamplingLimits, OpenReview:j8H84v6AZ1]", "QuixBugs (small Python/Java single-fix bugs, for cross-language sanity)"], source: "inferred"}`
`baselines` **[HYPOTHESIS]** `{names: ["Full-adequacy (100% mutation score) visible suite as the upper-bound control condition", "Reference / gold correct patch as an upper bound on held-out pass rate", "Coding agents: SWE-agent, Agentless, OpenHands (identical harness/budget) as the model-family factor for RQ_INF_2", "Random-sub-suite (size-matched, adequacy-uncontrolled) as an ablation isolating adequacy from size — targets C4"], source: "inferred"}`
`metrics` **[HYPOTHESIS]** `{names: ["Mutation-kill score of the visible sub-suite = killed / (total − equivalent) mutants", "Visible-suite pass rate = fraction of episodes whose final patch passes the visible sub-suite", "Held-out pass rate = fraction passing all hidden tests AND killing all excluded mutants", "Overfitting gap = visible-pass − held-out-pass", "Changepoint location + Davies-test p-value (existence/position of a threshold)", "Gaming fraction = share of visible-pass/held-out-fail patches labeled 'gaming' by M5"], source: "inferred"}`

---

## N9 — Results

**[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY].** No experiment has been run; nothing below is a real number. Per RQ: predicted direction, `evidence_strength="missing"`, `rq_answered=false`, explicit falsification condition.

- `rq_id`: "RQ1", `source`: "hypothesized", `result_text`: "Predicted direction: the overfitting gap stays near zero while mutation-kill adequacy remains high and rises substantially once adequacy drops below a mid-to-high band (unknown exact location), consistent with agents shifting toward visible-suite-specific patches as the suite's fault-detection weakens.", `result_type`: "quantitative", `evidence_strength`: "missing", `rq_answered`: false. **FALSIFICATION CONDITION**: refuted if the gap stays flat and near-zero across the *entire* adequacy sweep (agents do not exploit suite weakness at all), OR if the gap is already large at ~100% mutation-kill adequacy (suite adequacy is not the operative driver).
- `rq_id`: "RQ_INF_1", `source`: "hypothesized", `result_text`: "Predicted direction: the gap-vs-adequacy relationship more likely resembles a soft, gradual increase than a sharp phase transition, given mutation score is a coarse aggregate over a heterogeneous mutant population; a weak changepoint may still be detectable.", `result_type`: "quantitative", `evidence_strength`: "missing", `rq_answered`: false. **FALSIFICATION CONDITION**: refuted if the Davies test yields a statistically clear sharp breakpoint (a genuine discrete threshold), OR if no consistent monotone trend exists at all (flat/noisy relationship falsifies "there is a curve to characterize").
- `rq_id`: "RQ_INF_2", `source`: "hypothesized", `result_text`: "Predicted direction: onset thresholds differ across agent/model families (a significant agent×adequacy interaction), with stronger/more capable agents plausibly gaming at higher adequacy (finding more exploits) — so no single universal threshold.", `result_type`: "quantitative", `evidence_strength`: "missing", `rq_answered`: false. **FALSIFICATION CONDITION**: refuted if all families share a statistically indistinguishable threshold (no agent×adequacy interaction), which would instead support a benchmark-intrinsic universal onset.
- `rq_id`: "RQ_INF_3", `source`: "hypothesized", `result_text`: "Predicted direction: the diagnostic agrees with human labels well above chance, and the gaming fraction among held-out-fail patches increases as adequacy falls, indicating the widening gap is driven by exploitation rather than by uniformly more incomplete honest fixes.", `result_type`: "quantitative", `evidence_strength`: "missing", `rq_answered`: false. **FALSIFICATION CONDITION**: refuted if the diagnostic's agreement with human labels is near chance (it cannot separate gaming from coincidence), OR if the gaming fraction is flat/decreasing as adequacy falls (the gap is explained by honest incompleteness, not gaming).

---

## N10 — Threats / Self-Limitations

All **[HYPOTHESIS]** — anticipated limitations of this kind of study, since no Threats section exists yet. At least four, categorized, each with a mitigation.

- `threat_id`: "t1", `category`: "construct", `description`: "Mutation score proxies 'test-suite adequacy' and mutants proxy the space of hidden bugs the held-out oracle should catch; equivalent mutants and unrealistic mutation operators may make this construct diverge from real visible-vs-comprehensive-testing gaps.", `mitigation`: "Filter equivalent/duplicate mutants from the denominator; cross-validate mutation-adequacy against the independent EvalPlus hidden-test oracle on the Python track so the construct rests on two signals, not one.", `source`: "hypothesized"
- `threat_id`: "t2", `category`: "internal", `description`: "Sub-sampling a mutant-killing suite to hit a target mutation score risks confounding adequacy with suite size or which code regions are covered, so an observed gap could reflect size/coverage rather than adequacy.", `mitigation`: "Hold suite size and statement coverage fixed across adequacy levels, and include the size-matched adequacy-uncontrolled random-sub-suite baseline as an ablation to isolate the adequacy effect.", `source`: "hypothesized"
- `threat_id`: "t3", `category`: "external", `description`: "Findings would be established on a few agent/model families and a Python+Java repair setting; they may not generalize to other languages, agent architectures, or task types (e.g., feature addition vs. bug repair).", `mitigation`: "Include two languages and 2–3 agent families, and report per-language/per-agent curves rather than a single pooled threshold so generalization limits are explicit.", `source`: "hypothesized"
- `threat_id`: "t4", `category`: "conclusion", `description`: "Detecting a 'threshold' via changepoint fitting over many instances, levels, and agents risks false-positive breakpoints from multiple comparisons and may be underpowered to distinguish a soft curve from a sharp one.", `mitigation`: "Pre-register the changepoint vs. smooth-monotone model comparison, use the Davies test with multiplicity correction, and power-analyze the sample size (instances × levels × samples) before Stage 1.", `source`: "hypothesized"
- `threat_id`: "t5", `category`: "reproducibility", `description`: "Coding-agent behavior is sensitive to prompt/harness details and stochastic decoding; a threshold estimated once may not replicate under a different harness or temperature.", `mitigation`: "Fix decoding temperature, seeds, turn/token budgets, and harness version; report k≥5 samples per cell with variance, and release the harness and mutant-sampling artifacts.", `source`: "hypothesized"

---

## N11 — Artifacts

**Status: NOT_FOUND** **[PLACEHOLDER]** — nothing released because the paper does not exist.

`artifacts`: [] `has_code`: false `has_data`: false `has_model`: false

`absence_comment`: {`what_missing`: "No code, adequacy-controlled benchmark harness, mutant-sampling tool, or diagnostic exists for this idea yet.", `why_matters`: "A reader planning to build on this direction cannot currently reuse any released mutation-adequacy-controlled repair benchmark or agent harness — it would need to be built (largely by instrumenting SWE-bench Verified / Defects4J / EvalPlus with M1 and M5).", `implication`: "Treat artifact availability as a to-do for whoever executes this direction, not as an extraction gap."}

---

## N12 — Contribution Type

`value`: **"empirical"** **[HYPOTHESIS]**

`rationale`: "The seed's minimal experiment is a controlled measurement study: sweep one variable (visible-suite mutation-kill adequacy) and observe an outcome (the visible/held-out pass-rate gap and its onset) across existing coding agents and existing repair benchmarks (SWE-bench Verified, Defects4J, EvalPlus). What N9 would validate is a claim about *when a phenomenon occurs* — agents gaming a verifier as adequacy degrades — not the release of a new benchmark as the headline (the benchmarks are reused and instrumented, not introduced), nor a new agent system. The adequacy-controlled sampler (M1) and overfitting diagnostic (M5) are instrumental to the measurement, so `benchmark`/`tool` are secondary; the primary claim is empirical, mirroring the Emergent-Abilities-Mirage-style 'is this sharp threshold real?' measurement study rather than a testbed contribution." `source`: "hypothesized"

---

## Claims

1. **[HYPOTHESIS]** "Below some visible-suite mutation-kill adequacy level, coding agents begin to pass the visible suite while failing an independent held-out test-and-mutant oracle." `evidence`: [{`type`: "argument", `text`: "Restates the seed's core question as a testable claim; no experimental evidence yet.", `source`: "given", `location`: "seed README, 核心问题"}]
2. **[GROUNDED:corpus]** "Imperfect verifiers impose a hard ceiling on accepted-sample correctness — resampling under a weak unit-test suite converges to the conditional probability that an accepted sample is truly correct, not to perfect accuracy — which is direct adjacent evidence that a weak visible suite systematically admits incorrect-but-passing code." `evidence`: [{`type`: "citation", `text`: "ResamplingLimits (OpenReview:j8H84v6AZ1) formalizes the infinite-budget limit under a weak selector and stronger hidden tests; ROCnReroll (OpenReview:3Gy5mmyuxn) shows verifier false positives shape the selected-output distribution.", `source`: "grounded-corpus", `location`: "N3 entries 1–2"}]
3. **[HYPOTHESIS]** "Classical mutation-testing adequacy theory has essentially never been applied to characterize coding-agent verifier sufficiency (`全语料中该框架命中≈0`); the corpus contains the two adjacent literatures (imperfect-verifier / weak-test-suite work and reward-over-optimization work) but no paper bridging them via a mutation-adequacy sweep. **Scope caveat (2026-07-04 design review):** this is a *corpus-limited* absence claim — the searched corpora (OpenReview / recent arXiv) exclude classical SE venues, and the APR test-suite-overfitting literature named in N3 item 10 (Smith'15, Qi'15, DiffTGen, PATCH-SIM) is presumed adjacent-to-twin and UNVERIFIED pending harvest; the defensible narrow form is: no known prior work sweeps *size/coverage-matched mutation adequacy against LLM coding-agent behavior*." `evidence`: [{`type`: "observation", `text`: "Three corpus queries from distinct angles returned dense adjacent work but zero direct hits on adequacy-as-independent-variable for agent gaming; the classical-SE-venue blind spot is recorded in N3 item 10 as a blocking pre-Phase-B harvest residual.", `source`: "grounded-corpus", `location`: "N3 grounding note + absence_comment + item 10"}]
4. **[PLACEHOLDER]** "The visible/held-out gap-vs-adequacy relationship is more likely gradual than a sharp discrete threshold, since mutation score is a coarse aggregate proxy." `evidence`: [{`type`: "argument", `text`: "A prediction with an explicit falsification condition (N9/RQ_INF_1); no data collected.", `source`: "hypothesized", `location`: "N9"}]
5. **[HYPOTHESIS]** "A single-agent design cannot establish whether any observed threshold generalizes, since exploitation propensity plausibly varies by model capability/training regime (C3); Stage 1 measures 2–3 families but only partially resolves this." `evidence`: [{`type`: "argument", `text`: "From the N6 challenge map and unaddressed_challenges; RQ_INF_2 tests but cannot fully close C3.", `source`: "hypothesized", `location`: "N6 unaddressed_challenges / N8 RQ_INF_2"}]
6. **[HYPOTHESIS]** "A widening pass-visible/fail-hidden gap must be attributable to agent-side gaming rather than honest incompleteness for the phenomenon to be 'gaming' at all; a per-patch differential-testing diagnostic is needed to make that attribution." `evidence`: [{`type`: "argument", `text`: "Derived from the seed's ground-truth constraint (隐藏测试与变异体) and C2; operationalized by M5 and tested by RQ_INF_3.", `source`: "hypothesized", `location`: "N5 C2 / N6 M5 / N8 RQ_INF_3"}]
