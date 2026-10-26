# Existing Draft Review — B1.2 可见测试过拟合的出现边界

Reviewed against: topic README (B1.2, 父 topic B1 Verifier 充分性), audit verdict KEEP-TOP (lead of the execution-oracle cluster, target FSE 2027, deadline Oct 2, 2026).

## 来源 (Source)

- Job dir: `~/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB1.2--1d4c9a92`
- Files: `research-report.md` (101 KB, "6 confirmed steps"), `experiment-spec.md` (29 KB), `paper-draft.md` (54 KB, title in draft: *"How Adequate Must Tests Be? Measuring False Acceptance of Agent Patches via Controlled Mutation-Kill Sweeps"*; report banner title: *"Adequacy Is the Attack Surface"*).
- All files dated **2026-07-20** on disk; content carries no internal date but matches the ~2026-07 generation batch. Seeds inside the spec use `global_seed=20240601`.

## Architecture

The draft is a **measurement-framework / empirical-study paper** (not a method paper). Its design skeleton, as actually drafted:

**Core quantity.** False-acceptance curve **F(s) = P(H=0 | V=1, m(T_v)=s)** — the probability that a patch accepted by the visible suite (V=1) fails a strengthened held-out oracle (H=0), as a function of the visible suite's mutation-kill score s — plus an onset estimate **s\*** and a per-patch gaming-vs-honest-incompleteness diagnostic.

**Pipeline stages (3 methods, m-1..m-3):**
1. **Adequacy-controlled suite construction (m-1).** Per bug, materialize the full test×mutant kill matrix (PIT for Java, cosmic-ray for Python) + per-test statement-coverage vectors; then select visible sub-suites by **MILP** (CBC, simulated-annealing fallback, 10k candidates/cell) hitting 4 target kill-score bins ([0.1,0.3], [0.3,0.5], [0.5,0.8], [0.8,1.0]) under hard constraints: **suite size exactly fixed, coverage within ±2pp** of a reference suite. Equivalent mutants handled as first-class machinery: TCE (compiler equivalence) + 60s/mutant dynamic probing, with residual uncertainty carried as an **adequacy interval [s_lo, s_hi]**, never silently filtered.
2. **Frozen-agent sweep + F(s) estimation (m-2).** One frozen fix-until-pass agent — pinned **Qwen2.5-Coder-32B-Instruct** on vLLM, temp 0.2, 8-attempt budget, per-run deterministic seeds, withheld tests *physically removed* from the workspace, full JSONL action traces. Every visible-accepted patch is re-judged by an **augmented held-out oracle** = full reference suite + benchmark hidden tests + mutation-guided generated tests (EvoSuite/Pynguin) whose assertions are re-derived by executing on the ground-truth fixed version. Onset adjudicated by model selection: segmented (change-point) binomial regression vs smooth logistic vs flat null, ΔBIC ≥ 6, refit at s, s_lo, s_hi.
3. **Gaming-vs-incompleteness diagnostic (m-3).** Supervised classifier (GBT) over three signal families: (a) behavioral — **metamorphic perturbations** of visible-test inputs (gamed patches show an "input-locality fingerprint": correctness concentrated exactly on memorized test points); (b) structural — hard-coded visible-test literals, patch-locus distance from defect; (c) trajectory — test-file reads followed by value-specific edits. Ground truth: 300 accepted-but-wrong patches doubly annotated by 3 humans with adjudication; classifier trusted only if held-out balanced accuracy ≥ 0.75 and annotator κ ≥ 0.6.

**Testbeds:** SWE-bench Verified (100 Python bugs) + Defects4J v2.0 (100 Java bugs), stratified by suite size and mutant density.

**IV / DV:** IV = mutation-kill adequacy s (swept, size/coverage-matched); DVs = F(s), onset s\*, gaming/incomplete attribution. **Ground truth** = augmented held-out oracle (H) + adjudicated human labels (attribution).

**Experiment arms:** 6 mechanism RQs, each with a pre-registered falsification threshold — RQ1 sampler feasibility (≥80% cells), RQ2 equivalent-mutant band shrinkage (median ≤0.05), RQ3 F(low)−F(high) ≥ 20pp else premise falsified, RQ4 s\* stability under band endpoints (≤0.1 shift), RQ5 diagnostic accuracy vs patch-size baseline and a PATCH-SIM-style comparator, RQ6 human decidability (κ ≥ 0.6). Baselines: flat-F null, unfiltered-survivor band, size-only classifier, PATCH-SIM-style classifier. This falsification-first structure is unusually disciplined and is a genuine architectural highlight.

## Novelty highlight

**Sharpest claim:** *no prior study treats test-suite adequacy as a controlled independent variable* — everyone else holds the suite fixed (as trusted oracle, filtering target, or generation target), so the calibration question "how strong must a visible suite be before its green result can gate agent patches" has never been answered. The operational delta is threefold: (i) kill-matrix + MILP sampler that makes adequacy a *manufacturable* variable at matched size/coverage; (ii) equivalent-mutant uncertainty propagated as an interval on the x-axis of the whole curve (with the onset claim pre-registered to die if the band flips the model family); (iii) the first *human-validated* attribution separating deliberate suite-gaming from honest incompleteness — prior classifiers (PATCH-SIM 2018, DiffTGen 2017) classify correctness, not intent.

**Nearest prior as the draft states it:** EvalPlus (weak suites inflate pass@k — but strengthens suites rather than sweeping adequacy), Stroebl et al. limits-of-resampling (false-positive ceiling under a *fixed* unmeasured verifier), Just et al. 2014 (mutation score ↔ real-fault detection, correlational), APR overfitting literature (Smith/Qi 2015), SWE-bench as baseline substrate. The draft's related-work scan found 1 candidate baseline and 0 high-threat works among 13 deeply compared.

**What the scan visibly misses:** 17 cited works were "no fetchable full text, listed for coverage only" — and these include the two *closest 2026 competitors*: **SpecBench** (reward hacking of long-horizon coding agents against held-out validation, 2026) and **RHB** (reward-hacking-behaviors benchmark for SWE agents, 2026). Both measure exactly the V=1/H=0 phenomenon; neither (to my knowledge) *controls adequacy as a swept variable*, so the delta survives — but the draft never argues this explicitly, which a reviewer will demand. Also absent: the SWE-bench weak-test/insufficient-oracle critiques (e.g., test-augmentation works showing Verified's fail-to-pass tests under-specify correctness) and the RLVR verifier-quality literature that crystallized in 2026.

**Load-bearing?** Yes, entirely. This is a measurement paper; if any 2026 work already sweeps suite adequacy against agent false acceptance, the contribution collapses to a replication. The controlled-sweep + interval-carried-uncertainty combination is the paper. (The gaming/incomplete diagnostic is a second, semi-independent novelty leg that could survive even if the sweep were partially scooped.)

## Freshness check vs 2026-08

The draft's motivation is built on classical APR overfitting + reward-overoptimization citations. It **already anticipates** the RLVR/verifier crystallization structurally (it cites SpecBench, RHB, ROC-n-reroll, co-evolving coder/tester RL — all shallowly) but **does not use any of the production acceptance-gap evidence** now available:

- **ReactBench 60.8% of green-test patches fail static analysis** — this is a direct, production-scale instance of V=1 hiding quality failure; it belongs in ¶1–2 of the intro as evidence that the pass signal is *already* failing in the wild, not hypothetically.
- **Faros: 31.3% of agent PRs merged with zero review, defect rate 9%→54%** — this is the strongest possible "who cares" for the calibrated sufficiency floor F(s): teams are *currently* using green-suite-as-sole-gate, and it is measurably unsafe. The draft's "engineering teams that use a suite's pass signal as a standalone acceptance gate" claim was speculative in July; it is now empirically documented.
- **METR merge rates** — usable as evidence that human review does not fully absorb the gap either.

**Verdict: motivation should be updated.** The crystallized RLVR/verifier subfield cuts both ways: it raises crowding risk (SpecBench/RHB must be deeply differentiated, not coverage-listed) but also validates the topic's importance. The update is cheap — intro + related work only; the design itself needs no change, and in fact the production numbers strengthen the case for the F(s) curve as the deliverable practitioners lack.

## Gap to submission (FSE 2027, due 2026-10-02)

**Status: pre-registration only. Nothing has been executed.** The experiment-spec states explicitly that the coding agent "will implement all code… It will not run the experiments." The paper draft's six RQ sections contain hypotheses and *expected* outcomes, no results; the abstract says "We will evaluate…". Concretely missing:

- No code exists (kill-matrix builder, sampler, equivalence filter, agent harness, oracle builder, diagnostic, annotation tooling — all specified, none implemented).
- No data: the 100+100 stratified bug lists are unselected; mutation-tooling compatibility per repo unverified (cosmic-ray on SWE-bench repos is the flagged dominant CPU cost and biggest feasibility risk).
- No annotators recruited; 30-patch pilot + 300-patch labeling is a long-lead-time human study.
- Open design decisions unresolved (reference-suite size k policy, interval-denominator convention, coverage scope).
- Related work needs the 2026 refresh above; Threats to Validity and Data Availability sections not yet drafted in FSE form.

**Next actions (ordered):**
1. **Pilot RQ1+RQ2 on ~20 bugs (10 per benchmark) immediately** — kill matrix, sampler, equivalence band. This is CPU-only, needs no GPU or annotators, and is the design's kill-switch: if bins are infeasible or bands >0.10, the whole sweep fails and you need to know in August, not September.
2. **Stand up the frozen-agent harness** (Qwen2.5-Coder-32B on vLLM) and pilot RQ3 on the same bugs to measure visible-acceptance rates per bin — this determines whether the <120-patches-per-bin contingency triggers and whether the full 200-bug sweep fits the compute window.
3. **Recruit 3 SE annotators now and run the 30-patch codebook pilot** as soon as the first accepted-but-wrong patches exist (human-study lead time is the schedule's critical path alongside mutation compute).
4. **Rewrite intro + related work**: pull ReactBench/Faros/METR numbers into the motivation; add a explicit "delta vs SpecBench/RHB" paragraph (they benchmark gaming at fixed adequacy; we sweep adequacy and localize the onset).
5. **Pre-commit a descope fallback**: if mutation analysis on SWE-bench Verified proves too expensive by early September, ship Defects4J-only for the full pipeline + SWE-bench as a smaller replication — the claims are already scoped per-benchmark, so this survives review.

Timeline judgment: ~7 weeks to deadline. Feasible only if step 1 starts immediately and the annotation pilot overlaps the sweep; the full 200×4-bin design with 300-patch annotation is at the edge of the window.
